#!/usr/bin/env python3
"""mandate's deterministic position supervisor — the dead-agent backstop.

There is NO model in this file and there must never be one. Every decision is
a comparison between numbers read from the broker and numbers written at
entry. That is the whole point: multi-leg options positions cannot rest
bracket orders at the venue, so if the agent process dies between decision
runs the book is unmanaged. This process holds the charter's exits (§4)
whether or not the agent is alive, on its own timer, under its own principal
whose manifest contains no place op of any kind.

One pass per invocation; launchd provides the timer.

Exit codes:
  0  pass completed (including "nothing to do")
  1  pass completed but at least one close failed
  2  could not connect to the gateway or could not read the book
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
# Every close/hold decision is arithmetic and lives in rules.py, which touches
# no I/O and is testable without a gateway. This file is the I/O half.
from rules import (
    CIRCUIT_BREAKER_PCT,
    VALUE_MANAGED_STRUCTURES,
    assignment_suspected,
    breach_pct,
    classify_exit,
    close_order,
    long_only_fragment,
    parse_clock_timestamp,
)

ENV_SUPERVISOR = ROOT / "state" / "env-supervisor.sh"
ENV_AGENT = ROOT / "state" / "env.sh"
LEDGER = ROOT / "state" / "risk_ledger.json"
ALARM = ROOT / "state" / "ALARM"

TIGHTEN_TIMEOUT_S = 60
GATEWAY_INIT_TIMEOUT_S = 180

# The 2026-08-28 fill race, twice observed: a long-leg sell submitted while
# the short leg's buy-back was still filling drew a venue 403 ("uncovered")
# and orphaned the long. Shorts are now polled OFF the book before any
# long-leg close is sent; if they have not cleared inside the budget, the
# longs wait for the next pass (the long-only fragment rule finishes them).
SHORT_CLEAR_TIMEOUT_S = 30
SHORT_CLEAR_POLL_S = 3

DEMOTE_ACTION_CLASS = "alpaca.place_defined_risk_spread"


# --- decision log ----------------------------------------------------------
# One line per decision, including every no-action. Pipe-delimited with a
# fixed field count so the dashboard can parse it without a grammar:
#
#   SUPERVISOR|<utc_iso>|<pass_id>|<DECISION>|<subject>|<detail>
#
# subject is the thing decided about (an OCC symbol, a client_order_id, or "-")
# and detail is free text with pipes and newlines stripped.

PASS_ID = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def log(decision: str, subject: str = "-", detail: str = "") -> None:
    clean = str(detail).replace("|", "/").replace("\n", " ").strip()
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    print(f"SUPERVISOR|{ts}|{PASS_ID}|{decision}|{subject or '-'}|{clean}", flush=True)


# --- payload plumbing ------------------------------------------------------


def tool_text(result) -> str:
    return "\n".join(c.text for c in result.content if hasattr(c, "text"))


def explain(exc: BaseException) -> str:
    """Flatten an exception, including anyio's TaskGroup ExceptionGroups.

    The stdio client runs the session in a task group, so a plain str() of the
    failure reads "unhandled errors in a TaskGroup (1 sub-exception)" and says
    nothing about the actual cause. An unattended process whose only output is
    a log line cannot afford that.
    """
    inner = getattr(exc, "exceptions", None)
    if inner:
        return "; ".join(explain(e) for e in inner)
    return f"{type(exc).__name__}: {exc}"


def peel(result) -> tuple[object, str | None]:
    """Return (vendor data, error text or None), peeling BOTH envelopes.

    Verified against the live gateway 2026-08-25. A brokered call comes back
    wrapped twice, and the two layers fail in different ways:

      layer 0  MCP result.isError    -> BROKER refusal (plain text, not JSON)
      layer 1  {"content":[{"text"}], "isError", "structuredContent"}
                                     -> the gateway re-serializing the shim's
                                        own CallToolResult; SHIM/vendor errors
                                        raise isError HERE, while layer 0 still
                                        reads success
      layer 2  {"_alpaca_mcp_security":..., "data": {...}}
                                     -> the vendor's trust envelope

    The shim's own _vendor_data only peels layer 2 because it speaks to the
    vendor child directly. Anything reaching the venue through the broker must
    peel all three, and must check layer 1's isError: treating it as success
    is how a close that never happened gets logged as CLOSED.
    """
    raw = tool_text(result)
    if result.isError:
        return None, f"broker refusal: {raw[:300]}" if raw else "broker refusal"
    try:
        obj = json.loads(raw)
    except ValueError:
        return None, f"unparseable gateway payload: {raw[:200]}"
    if isinstance(obj, dict) and "content" in obj:
        inner = "".join(
            c.get("text", "") for c in (obj.get("content") or []) if isinstance(c, dict)
        )
        if obj.get("isError"):
            return None, f"tool error: {inner[:300]}" if inner else "tool error"
        try:
            obj = json.loads(inner)
        except ValueError:
            return None, f"unparseable vendor payload: {inner[:200]}"
    if isinstance(obj, dict) and "data" in obj:
        obj = obj["data"]
    return obj, None


async def read_tool(session, name: str, args: dict | None = None):
    """Call a read op and return its unwrapped data, or raise with the reason."""
    data, err = peel(await session.call_tool(name, args or {}))
    if err:
        raise RuntimeError(f"{name}: {err}")
    return data


def rows(data) -> list[dict]:
    """Normalize a list-shaped payload.

    Verified against the live gateway 2026-08-25: get_all_positions returns
    {"data": {"result": [...]}}, i.e. the list is under a key, not bare. Both
    shapes are accepted here because the vendor is not ours to pin.
    """
    if isinstance(data, dict):
        for key in ("result", "positions", "orders"):
            if isinstance(data.get(key), list):
                data = data[key]
                break
    return [r for r in data if isinstance(r, dict)] if isinstance(data, list) else []


def quote_map(data) -> dict[str, dict]:
    """Per-symbol quote rows from get_option_latest_quote.

    Verified live: {"data": {"quotes": {"<OCC>": {"ap": .., "bp": ..}}}}.
    """
    if isinstance(data, dict):
        inner = data.get("quotes", data)
        if isinstance(inner, dict):
            return {k: v for k, v in inner.items() if isinstance(v, dict)}
    return {}


def load_ledger() -> list[dict]:
    """Read the risk ledger. Missing, empty or corrupt reads as no open book."""
    try:
        raw = json.loads(LEDGER.read_text())
    except FileNotFoundError:
        log("LEDGER", "-", "no risk ledger on disk; treating the book as empty")
        return []
    except (ValueError, OSError) as e:
        log("LEDGER_UNREADABLE", "-", f"{e}; treating the book as empty")
        return []
    return [e for e in raw if isinstance(e, dict)] if isinstance(raw, list) else []


def shell_env(env_file: Path) -> dict[str, str]:
    """Capture an env floor by sourcing its shell file.

    The floor is defined once, in shell, and consumed by the ceremony commands
    and by this process alike. Re-declaring those paths in Python would be a
    second source of truth that silently drifts from the first.
    """
    out = subprocess.run(
        ["bash", "-c", f'set -e; source "{env_file}"; env -0'],
        capture_output=True, text=True, cwd=ROOT, timeout=30, check=False,
    )
    if out.returncode != 0:
        raise RuntimeError(f"could not source {env_file.name}: {out.stderr.strip()}")
    env = dict(os.environ)
    for item in out.stdout.split("\0"):
        key, sep, val = item.partition("=")
        if sep:
            env[key] = val
    return env


# --- acting ----------------------------------------------------------------


async def close_legs(session, syms: list[str], tag: str, dry_run: bool) -> bool:
    """Close each listed leg. Returns True if every close succeeded."""
    ok = True
    for sym in syms:
        if dry_run:
            log("WOULD_CLOSE", sym, f"entry={tag} (dry run; nothing sent)")
            continue
        try:
            # peel() checks BOTH error layers; a shim-level failure reads as
            # success at the MCP layer and would otherwise log a phantom close.
            _, err = peel(await session.call_tool(
                "alpaca__close_position", {"symbol_or_asset_id": sym}
            ))
            if err:
                ok = False
                log("CLOSE_FAILED", sym, f"entry={tag} {err}")
            else:
                log("CLOSED", sym, f"entry={tag}")
        except Exception as e:  # noqa: BLE001 - one bad leg must not abort the rest of the book
            ok = False
            log("CLOSE_FAILED", sym, f"entry={tag} {type(e).__name__}: {e}")
    return ok


async def shorts_cleared(session, shorts: list[str], tag: str) -> bool:
    """Poll the book until no short leg is still an open position.

    A market buy-to-close on a liquid index option fills in seconds; the
    budget exists for the day that stops being true. Returning False defers
    the long legs to the next pass rather than selling a spread's cover out
    from under a still-open short.
    """
    attempts = SHORT_CLEAR_TIMEOUT_S // SHORT_CLEAR_POLL_S
    for i in range(attempts):
        if i:
            await asyncio.sleep(SHORT_CLEAR_POLL_S)
        try:
            open_now = {
                p.get("symbol")
                for p in rows(await read_tool(session, "alpaca__get_all_positions"))
            }
        except Exception as e:  # noqa: BLE001 - an unreadable book defers, never proceeds
            log("CLEAR_CHECK_FAILED", "-", f"entry={tag} {explain(e)}")
            return False
        still = [s for s in shorts if s in open_now]
        if not still:
            return True
    log("SHORTS_STILL_OPEN", ",".join(still),
        f"entry={tag} shorts not cleared after {SHORT_CLEAR_TIMEOUT_S}s; "
        "long legs deferred to the next pass")
    return False


async def close_entry(session, entry: dict, legs: list[str],
                      qty_by_symbol: dict[str, float], dry_run: bool) -> bool:
    """Close every leg: shorts first, longs only once the shorts have left
    the book. Returns True if all closes succeeded."""
    tag = entry.get("client_order_id") or entry.get("order_id") or "?"
    shorts = [s for s in legs if qty_by_symbol.get(s, 0.0) < 0]
    longs = [s for s in legs if s not in shorts]
    ok = await close_legs(session, shorts, tag, dry_run)
    if shorts and longs and not dry_run:
        if not ok:
            log("CLOSE_DEFERRED", tag,
                "a short-leg close failed; long legs held so the shorts stay covered")
            return False
        if not await shorts_cleared(session, shorts, tag):
            return False
    return await close_legs(session, longs, tag, dry_run) and ok


def demote(reason: str, dry_run: bool) -> None:
    """Drop the AGENT's place grant to in-loop, then raise the ALARM file.

    Runs under the agent's env floor because it is the agent's grant being
    tightened, not the supervisor's. ALARM is written even if the tighten call
    fails: the run scripts refuse to start while it exists, so the file is the
    backstop behind the backstop.
    """
    if ALARM.exists():
        log("ALARM_EXISTS", "-", "already demoted; skipping re-demotion, exits still run")
        return
    if dry_run:
        log("WOULD_DEMOTE", DEMOTE_ACTION_CLASS, f"{reason} (dry run; nothing sent)")
        return

    cmd = (
        'set -e; source "state/env.sh"; export BROKER_LOCAL_IDENTITY=maker; '
        '.venv/bin/python -m safe_agents.broker.grants.commands tighten '
        "--principal-agent-id hackathon-dev --skill options-trader --user wes "
        f'--tier B --action-class {DEMOTE_ACTION_CLASS} --evidence "{reason}"'
    )
    try:
        out = subprocess.run(
            ["bash", "-c", cmd], capture_output=True, text=True,
            cwd=ROOT, timeout=TIGHTEN_TIMEOUT_S, check=False,
        )
        if out.returncode == 0:
            log("DEMOTED", DEMOTE_ACTION_CLASS, out.stdout.strip()[-300:] or "tighten ok")
        else:
            log("DEMOTE_FAILED", DEMOTE_ACTION_CLASS,
                f"rc={out.returncode} {(out.stderr or out.stdout).strip()[-300:]}")
    except subprocess.TimeoutExpired:
        log("DEMOTE_FAILED", DEMOTE_ACTION_CLASS, f"tighten timed out after {TIGHTEN_TIMEOUT_S}s")
    except Exception as e:  # noqa: BLE001 - a failed demotion must still be logged, never raised
        log("DEMOTE_FAILED", DEMOTE_ACTION_CLASS, f"{type(e).__name__}: {e}")

    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    try:
        ALARM.write_text(f"{stamp}\n{reason}\n")
        log("ALARM_RAISED", str(ALARM.relative_to(ROOT)), reason)
    except OSError as e:
        log("ALARM_FAILED", str(ALARM), f"{type(e).__name__}: {e}")


# --- the pass --------------------------------------------------------------


async def run_pass(session, dry_run: bool) -> int:
    clock = await read_tool(session, "alpaca__get_clock")
    if not isinstance(clock, dict):
        # TRY004 is silenced below: it wants TypeError, but this is a
        # malformed vendor response, not a caller passing the wrong type.
        raise RuntimeError("market clock was unreadable")  # noqa: TRY004
    exchange_now = parse_clock_timestamp(clock)
    account = await read_tool(session, "alpaca__get_account_info")
    positions = rows(await read_tool(session, "alpaca__get_all_positions"))

    qty_by_symbol = {}
    for p in positions:
        try:
            qty_by_symbol[p["symbol"]] = float(p.get("qty", 0))
        except (KeyError, TypeError, ValueError):
            continue
    # is_open is logged, not gated on: the exit rules are the same whether or
    # not the venue is taking orders, and a close attempted into a closed
    # market fails loudly as CLOSE_FAILED rather than silently doing nothing.
    log("CLOCK", "-", f"exchange time {exchange_now.isoformat()}, "
                      f"market_open={bool(clock.get('is_open'))}, "
                      f"{len(qty_by_symbol)} open position leg(s)")

    # Circuit breaker first, bounded by a subprocess timeout so it can never
    # hang the pass and starve the exit rules that follow it.
    pct = breach_pct(account if isinstance(account, dict) else {})
    if pct is None:
        log("BREAKER_UNREADABLE", "-", "account carried no usable equity/last_equity")
    elif pct <= CIRCUIT_BREAKER_PCT:
        reason = (f"day P&L {pct:.2%} breached the {CIRCUIT_BREAKER_PCT:.0%} circuit "
                  f"breaker at {exchange_now.isoformat()}")
        log("BREACH", "-", reason)
        demote(reason, dry_run)
    else:
        log("NO_BREACH", "-", f"day P&L {pct:.2%} is inside the "
                              f"{CIRCUIT_BREAKER_PCT:.0%} breaker")

    entries = load_ledger()
    if not entries:
        log("NO_ACTION", "-", "risk ledger is empty; no positions to supervise")
        return 0

    failed = False
    for entry in entries:
        tag = entry.get("client_order_id") or entry.get("order_id") or "?"
        try:
            legs = [s for s in (entry.get("legs") or []) if isinstance(s, str)]
            if not legs:
                log("SKIP", tag, "ledger entry records no legs")
                continue
            present = [s for s in legs if s in qty_by_symbol]
            if not present:
                log("SKIP", tag, "no leg is an open position; entry is dead, "
                                "the shim prunes it on the next placement")
                continue
            if len(present) != len(legs):
                # A long-only remainder is a close that broke half-way (the
                # 2026-08-28 fill race); finishing it is the exit the rules
                # already ordered. Anything else — shorts remaining, or stock
                # in the underlying suggesting early assignment — stays the
                # owner's call.
                if long_only_fragment(present, qty_by_symbol) and \
                        not assignment_suspected(present, qty_by_symbol):
                    log("FRAGMENT_EXIT", tag,
                        f"only {len(present)}/{len(legs)} legs remain and all are "
                        "long; finishing the broken close")
                    if not await close_entry(session, entry, present,
                                             qty_by_symbol, dry_run):
                        failed = True
                    continue
                log("SKIP", tag, f"only {len(present)}/{len(legs)} legs are open "
                                 "positions; partial book, leaving it to the agent")
                continue

            quotes: dict[str, dict] = {}
            # Credit and debit verticals alike are priced from live quotes;
            # rules.py owns which structures those are.
            if entry.get("structure") in VALUE_MANAGED_STRUCTURES:
                qdata, qerr = peel(await session.call_tool(
                    "alpaca__get_option_latest_quote", {"symbols": ",".join(legs)}
                ))
                # A quote failure is not an exit trigger: it drops the entry to
                # the clock rule rather than closing on missing information.
                if qerr:
                    log("QUOTE_FAILED", tag, qerr)
                else:
                    quotes = quote_map(qdata)

            rule, reason = classify_exit(entry, exchange_now, qty_by_symbol, quotes)
            if rule is None:
                log("NO_ACTION", tag, reason)
                continue

            ordered = close_order(legs, qty_by_symbol)
            log("EXIT", tag, f"{rule}: {reason}; closing shorts-first "
                             f"{' -> '.join(ordered)}")
            if not await close_entry(session, entry, ordered, qty_by_symbol, dry_run):
                failed = True
        except Exception as e:  # noqa: BLE001 - never let one entry abort the rest of the book
            failed = True
            log("ERROR", tag, f"{type(e).__name__}: {e}")

    return 1 if failed else 0


async def main() -> int:
    ap = argparse.ArgumentParser(description="mandate deterministic position supervisor")
    ap.add_argument("--dry-run", action="store_true",
                    help="compute and print every decision; send nothing")
    args = ap.parse_args()

    log("PASS_START", "-", "dry run" if args.dry_run else "live")

    # Charter-lock check, deliberately non-fatal HERE: this pass only reduces
    # exposure (reads and rule-driven closes), and a book left unmanaged
    # because the surface drifted is a worse outcome than closing through it.
    # The decision runs, which can CREATE risk, refuse outright on the same
    # check (run/lib.sh preflight, exit 5). INTEGRITY_FAIL on the log is the
    # human's signal to stop everything and either re-key or investigate.
    lock_check = subprocess.run(  # noqa: ASYNC221 - preflight, nothing else is on the loop yet
        [str(ROOT / ".venv" / "bin" / "python"), str(ROOT / "tools" / "charter_lock.py"), "verify"],
        capture_output=True, text=True, check=False,
    )
    if lock_check.returncode != 0:
        for line in (lock_check.stderr or lock_check.stdout).strip().splitlines():
            log("INTEGRITY_FAIL", "-", line)
        log("INTEGRITY_FAIL", "-",
            "charter lock does not verify; continuing exits only — a human must "
            "run bin/rekey.sh (deliberate change) or investigate (tampering)")

    try:
        env = shell_env(ENV_SUPERVISOR)
    except Exception as e:  # noqa: BLE001 - report an unusable env floor as FATAL, never a traceback
        log("FATAL", "-", f"env floor unusable: {e}")
        return 2

    params = StdioServerParameters(
        command=str(ROOT / ".venv" / "bin" / "python"),
        args=["-m", "safe_agents.broker.gateway"],
        env=env,
    )
    try:
        async with stdio_client(params) as (r, w), ClientSession(
            r, w, read_timeout_seconds=timedelta(seconds=GATEWAY_INIT_TIMEOUT_S)
        ) as session:
            await session.initialize()
            rc = await run_pass(session, args.dry_run)
    except Exception as e:  # noqa: BLE001 - any gateway failure is FATAL and explained, never raised
        log("FATAL", "-", f"could not connect to or read from the gateway: {explain(e)}")
        return 2

    log("PASS_END", "-", f"exit {rc}")
    return rc


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
