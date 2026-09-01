#!/usr/bin/env python3
"""Build the static mandate dashboard at docs/dashboard/index.html.

Operator-side tooling. This script holds Alpaca credentials because an operator
runs it; the agent never sees them and cannot run this script. The page it
emits is regenerated from the audit tape, not written by the agent.

Stdlib only. Every remote section degrades to an explicit "unavailable" note
rather than to fabricated data.
"""

from __future__ import annotations

import html
import json
import subprocess
import urllib.error
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

from dashboard_css import CSS
from dashboard_svg import (
    FAVICON_DATA_URI,
    consumed_bar_svg,
    equity_curve_svg,
    og_card_svg,
)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "dashboard" / "index.html"
OG_OUT = ROOT / "docs" / "dashboard" / "og.svg"
AUDIT = ROOT / "state" / "audit.jsonl"
REFUSALS = ROOT / "state" / "shim_refusals.jsonl"
LEDGER = ROOT / "state" / "risk_ledger.json"
ENV_SH = ROOT / "state" / "env.sh"
BROKER_SECRETS = ROOT / "state" / "secrets.json"
SECRETS = Path.home() / ".secrets" / "alpaca.txt"

API = "https://paper-api.alpaca.markets"
SITE = "https://wjatx.github.io/mandate/dashboard/"
START_EQUITY = 100_000.0
TIMEOUT = 20

GATE_TAPE_CAVEAT = (
    "A risk-gate refusal reaches the tape as an ordinary allow/executed "
    "placement row: the broker allowed the call and the shim declined "
    "afterwards. Unless the shim populates the record's error result, the "
    "tape's own fields cannot tell a refused placement from a filled one, so "
    "these rows are not badged apart here and the shim's own log above is the "
    "record."
)

TAGLINE = "an autonomous options agent under an enforced mandate"
MECHANISM = ("The agent holds no broker credential. Every call is decided "
             "against a signed grant and lands on a hash-chained tape.")

# A leading run of identical marks this fraction of the window is pre-activity
# padding from the broker, not signal; drawing it flattens the whole line.
FLAT_HEAD_TRIM_AT = 0.20
# Marks of the flat run to keep, so the opening balance is still a visible
# segment the line departs from rather than an unexplained starting point.
ANCHOR_MARKS = 3
# Reconstructed equity must land this close to the live account figure before
# the chart will trust it, as a fraction of the opening balance.
EQUITY_AGREEMENT = 0.02

MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")


# ---------------------------------------------------------------- utilities

def esc(v) -> str:
    return html.escape("" if v is None else str(v))


def fnum(v, default=None):
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def money(v, places=2) -> str:
    f = fnum(v)
    if f is None:
        return "—"
    return f"{'-' if f < 0 else ''}${abs(f):,.{places}f}"


def signed_money(v) -> str:
    f = fnum(v)
    if f is None:
        return "—"
    return f"{'+' if f >= 0 else '-'}${abs(f):,.2f}"


def plural(n, word, suffix="s") -> str:
    if n == 1:
        return f"{n} {word}"
    if suffix == "ies" and word.endswith("y"):
        return f"{n} {word[:-1]}ies"
    return f"{n} {word}{suffix}"


def short_digest(v) -> str:
    s = str(v or "")
    body = s.split(":", 1)[1] if s.startswith("sha256:") else s
    return body[:12] if body else "—"


def utc(ts) -> str:
    """Render an ISO-8601 or epoch timestamp as 'YYYY-MM-DD HH:MM:SS UTC'."""
    if ts in (None, ""):
        return "—"
    try:
        if isinstance(ts, (int, float)):
            dt = datetime.fromtimestamp(ts, timezone.utc)
        else:
            dt = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
            dt = dt.astimezone(timezone.utc)
    except (ValueError, OSError, OverflowError):
        return esc(ts)
    return dt.strftime("%Y-%m-%d %H:%M:%S UTC")


def read_jsonl(path: Path) -> tuple[list[dict], str | None]:
    if not path.exists():
        return [], f"{path.name} not present"
    rows, bad = [], 0
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except ValueError:
            bad += 1
    return rows, (f"{bad} unparseable line(s) skipped" if bad else None)


def read_ledger() -> list[dict]:
    try:
        raw = json.loads(LEDGER.read_text())
    except (OSError, ValueError):
        return []
    return [e for e in raw if isinstance(e, dict)] if isinstance(raw, list) else []


# -------------------------------------------------------------- data access

def load_keys() -> dict[str, str]:
    # The stack's own secrets file is authoritative: it is what the re-key
    # ceremony updates on rotation, so the dashboard can never trade on a
    # different key generation than the agent. ~/.secrets is the fallback.
    try:
        blob = json.loads(BROKER_SECRETS.read_text())
        entry = next(v for k, v in blob.items() if "alpaca" in k.lower())
        inner = json.loads(entry)
        return {
            "ALPACA_KEY": inner["ALPACA_KEY"],
            "ALPACA_SECRET": inner["ALPACA_SECRET"],
        }
    except (OSError, KeyError, ValueError, StopIteration):
        pass
    kv: dict[str, str] = {}
    for line in SECRETS.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        kv[k.strip()] = v.strip().strip('"').strip("'")
    return kv


def api_client():
    """Return a getter for the paper API, or None if keys are unreadable."""
    try:
        kv = load_keys()
        headers = {
            "APCA-API-KEY-ID": kv["ALPACA_KEY"],
            "APCA-API-SECRET-KEY": kv["ALPACA_SECRET"],
        }
    except (OSError, KeyError):
        return None

    def get(path: str):
        req = urllib.request.Request(API + path, headers=headers)
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.load(resp)

    return get


def fetch(get, path: str) -> tuple[object | None, str | None]:
    """Per-section fetch. Returns (payload, error-note); never raises."""
    if get is None:
        return None, "Alpaca credentials unavailable"
    try:
        return get(path), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code} from {path}"
    except (urllib.error.URLError, OSError, ValueError, TimeoutError) as e:
        return None, f"{type(e).__name__} from {path}"


def verify_tape() -> tuple[bool, str, str]:
    """Run the tape verifier; return (ok, verdict-line, captured tail)."""
    cmd = (
        f"source {ENV_SH} && "
        f"{ROOT}/.venv/bin/python -m safe_agents.broker.auditor.tape_cli "
        f"--path {AUDIT} --verify"
    )
    try:
        proc = subprocess.run(
            ["bash", "-c", cmd], cwd=ROOT, capture_output=True,
            text=True, timeout=120, check=False,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return False, f"verifier did not run ({type(e).__name__})", ""
    out = [ln.strip() for ln in (proc.stdout + proc.stderr).strip().splitlines()]
    # The verifier's own caveat paragraph also contains "CONSISTENT"; take the
    # short summary line ("CHAIN CONSISTENT — 28 records, seq 0..27") instead.
    verdict = next(
        (ln for ln in out if "CONSISTENT" in ln.upper() and len(ln) < 90),
        f"verifier exited {proc.returncode}",
    )
    return proc.returncode == 0, verdict, "\n".join(out[-6:])


# -------------------------------------------------------- tape partitioning

def is_read(rec: dict) -> bool:
    """Read-only broker ops all carry a get_ prefix in this manifest."""
    return str(rec.get("op") or "").startswith("get_")


def is_deny(rec: dict) -> bool:
    """Refused at the broker: the call never reached Alpaca."""
    return rec.get("decision") == "deny"


def is_gate_refusal(rec: dict) -> bool:
    """Refused at the risk gate: the broker allowed the call and the
    defined-risk shim declined to place it, so the tape shows an ordinary
    allow/executed record.

    The only tape-side marker is a populated error result. Records written by
    the current shim leave error null, which is why state/shim_refusals.jsonl
    is the authoritative log for this class -- see GATE_TAPE_CAVEAT. Nothing
    here guesses: a placement row is only badged as a refusal when the tape
    itself says so.
    """
    return rec.get("decision") == "allow" and bool(rec.get("error"))


def tape_counts(records: list[dict]) -> dict[str, int]:
    ops = [str(r.get("op") or "") for r in records]
    return {
        "total": len(records),
        "place": sum(1 for o in ops if "place" in o),
        "close": sum(1 for o in ops if "close" in o),
        "cancel": sum(1 for o in ops if "cancel" in o),
        "deny": sum(1 for r in records if is_deny(r)),
        "gate": sum(1 for r in records if is_gate_refusal(r)),
        "read": sum(1 for r in records if is_read(r) and not is_deny(r)),
    }


# ------------------------------------------------------------- equity curve

def equity_series(history, live_equity):
    """Return (stamps, values, trim-note, error) of TRUE account equity.

    Two things make the raw payload unsafe to plot as-is. The window is padded
    before the account's first activity, and the two arrays disagree about what
    the padding is: `equity` reports 0.0 there while `profit_loss` reports
    -base_value. And the arrays are not always in the same frame, so a value
    can be either an absolute balance or a P&L delta. So: drop the padding,
    then build both candidates -- the raw array, and base_value + profit_loss
    -- and keep whichever lands on the live account figure.
    """
    h = history if isinstance(history, dict) else {}
    ts = h.get("timestamp") or []
    raw, pl = h.get("equity") or [], h.get("profit_loss") or []
    base = fnum(h.get("base_value"))

    # Real reporting starts at the first nonzero equity mark; an account cannot
    # have been worth exactly nothing and then worth six figures.
    padded = next((i for i, v in enumerate(raw) if fnum(v)), 0)

    absolute, rebuilt = [], []
    for i, t in enumerate(ts):
        if i < padded:
            continue
        a = fnum(raw[i]) if i < len(raw) else None
        p = fnum(pl[i]) if i < len(pl) else None
        # Pair values with their own stamp so a gap cannot shift later points.
        if a is not None:
            absolute.append((t, a))
        if p is not None and base is not None:
            rebuilt.append((t, base + p))

    def miss(series):
        if not series or live_equity is None:
            return None
        return abs(series[-1][1] - live_equity)

    tol = EQUITY_AGREEMENT * (base or START_EQUITY)
    m_abs, m_reb = miss(absolute), miss(rebuilt)
    if rebuilt and (m_reb is None or m_reb <= tol) and (m_abs is None or m_reb <= m_abs):
        # Preferred: correct across the whole window, including the flat head,
        # where the raw array reports 0.0 instead of the opening balance.
        chosen = rebuilt
    elif absolute and (m_abs is None or m_abs <= tol):
        chosen = absolute
    else:
        return None, None, "", ("portfolio history did not return an equity "
                                "series that agrees with the live account")
    if len(chosen) < 2:
        return None, None, "", "portfolio history returned too few points"

    # Clip any remaining flat lead-in, keeping one anchor mark so the start of
    # trading is still visible. Both clips are stated in prose below the chart.
    head, flat = chosen[0][1], 0
    while flat + 1 < len(chosen) and abs(chosen[flat + 1][1] - head) < 0.005:
        flat += 1
    said = []
    if padded:
        said.append(f"{plural(padded, 'mark')} of broker padding before the "
                    "account's first activity")
    if flat > FLAT_HEAD_TRIM_AT * len(chosen) and len(chosen) - flat >= 2:
        cut = max(flat - ANCHOR_MARKS + 1, 0)
        if cut:
            said.append(f"a further {plural(cut, 'mark')} flat at {money(head)}")
        chosen = chosen[cut:]
    note = "Not drawn: " + "; ".join(said) + "." if said else ""

    return ([utc(t) for t, _ in chosen], [v for _, v in chosen], note, None)


# ------------------------------------------------------------------ render

def unavailable(note: str) -> str:
    return f'<p class="unavail">Unavailable — {esc(note)}. No data is shown.</p>'


def table(headers, rows, cls: str = "") -> str:
    """rows: (row-class, [cell-html, ...]) pairs. Cells are pre-escaped."""
    head = "".join(f"<th>{esc(h)}</th>" for h in headers)
    body = "".join(
        f'<tr class="{rc}">' + "".join(f"<td>{c}</td>" for c in cells) + "</tr>"
        for rc, cells in rows
    )
    return (f'<div class="scroll"><table class="{cls}"><thead><tr>{head}</tr>'
            f"</thead><tbody>{body}</tbody></table></div>")


# ------------------------------------------------------------ spread cards

def parse_occ(sym: str) -> dict | None:
    """Split an OCC option symbol: ROOT + YYMMDD + C/P + strike in mills."""
    s = str(sym or "")
    # OCC layout is fixed-width from the right: 8 strike digits (mills),
    # 1 right, 6 date digits; whatever precedes it is the root.
    if len(s) < 16 or s[-9] not in "CP":
        return None
    if not (s[-15:-9].isdigit() and s[-8:].isdigit()):
        return None
    try:
        exp = date(2000 + int(s[-15:-13]), int(s[-13:-11]), int(s[-11:-9]))
    except ValueError:
        return None
    return {"root": s[:-15], "expiry": exp, "right": s[-9],
            "strike": int(s[-8:]) / 1000.0}


def spread_name(legs: list[str], structure: str) -> tuple[str, str]:
    """Human name and expiry caption for a set of legs. Falls back to the raw
    symbols when a leg does not parse as OCC."""
    parsed = [parse_occ(s) for s in legs]
    label = str(structure or "spread").replace("_", " ")
    if not parsed or any(p is None for p in parsed):
        return " / ".join(legs) or "spread", label.capitalize()
    root = parsed[0]["root"]
    strikes = "/".join(f"{p['strike']:g}" for p in parsed)
    kind = "call" if parsed[0]["right"] == "C" else "put"
    shape = "vertical" if "vertical" in label else label
    exp = parsed[0]["expiry"]
    name = f"{root} {strikes} {kind} {shape} · {MONTHS[exp.month - 1]} {exp.day}"
    return name, f"{label.capitalize()} · expires {exp.isoformat()}"


def spread_card(entry: dict, legs: list[dict]) -> str:
    syms = [str(p.get("symbol")) for p in legs]
    name, sub = spread_name(entry.get("legs") or syms, entry.get("structure"))
    mv = sum(fnum(p.get("market_value"), 0.0) for p in legs)
    cost = sum(fnum(p.get("cost_basis"), 0.0) for p in legs)
    pl = sum(fnum(p.get("unrealized_pl"), 0.0) for p in legs)
    cap = fnum(entry.get("max_loss_usd"))

    tp, stop = entry.get("exit_tp_value"), entry.get("exit_stop_value")
    if stop is None and entry.get("vol_pair"):
        stop_txt = '<span class="warn">no stop (vol pair)</span>'
    else:
        stop_txt = money(stop)
    exits = (f"take profit {money(tp)}<br>stop {stop_txt}"
             if (tp is not None or stop is not None or entry.get("vol_pair"))
             else "not stamped")

    rows = [
        ("Market value now", money(mv)),
        ("Entry cost", money(cost)),
        ("Unrealized P&amp;L",
         f'<span class="{"pos" if pl >= 0 else "neg"}">{signed_money(pl)}</span>'),
        ("Ledger max loss", money(cap) if cap is not None else "—"),
        ("Stamped exits", exits),
        ("Legs", "<br>".join(
            f'{esc(p.get("side"))} {esc(p.get("qty"))} <code>{esc(p.get("symbol"))}</code>'
            for p in legs) or "—"),
    ]
    kv = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in rows)

    bar = ""
    if cap:
        used = max(0.0, -pl)
        bar = (consumed_bar_svg(used, cap)
               + f'<p class="barcap">{money(used)} of {money(cap)} max loss '
                 f"used ({used / cap * 100:.0f}%)</p>")
    return (f'<div class="card"><h3>{esc(name)}</h3>'
            f'<p class="card-sub">{esc(sub)}</p>'
            f'<dl class="kv">{kv}</dl>{bar}</div>')


def positions_section(positions, err, ledger) -> str:
    if err:
        return unavailable(err)
    if not positions:
        note = ""
        if ledger:
            note = (f'<p class="note">Risk ledger still tracks '
                    f"{plural(len(ledger), 'defined-risk entry', 'ies')}"
                    f"; no matching position is open at the broker.</p>")
        return '<p class="note">No open positions.</p>' + note

    by_symbol = {str(p.get("symbol")): p for p in positions}
    cards, claimed, dangling = [], set(), 0
    for entry in ledger:
        legs = [by_symbol[s] for s in (entry.get("legs") or []) if s in by_symbol]
        if not legs:
            dangling += 1
            continue
        claimed.update(str(p.get("symbol")) for p in legs)
        cards.append(spread_card(entry, legs))

    out = f'<div class="cards">{"".join(cards)}</div>' if cards else ""
    if dangling:
        out += (f'<p class="note">{plural(dangling, "further ledger entry", "ies")}'
                f" {'has' if dangling == 1 else 'have'} no open leg at the "
                f"broker.</p>")

    loose = [p for p in positions if str(p.get("symbol")) not in claimed]
    if loose:
        rows = [("", [
            esc(p.get("symbol")), esc(p.get("side")), esc(p.get("qty")),
            money(p.get("avg_entry_price")), money(p.get("current_price")),
            money(p.get("market_value")),
            (f'<span class="{"pos" if fnum(p.get("unrealized_pl"), 0.0) >= 0 else "neg"}">'
             f'{signed_money(p.get("unrealized_pl"))}</span>'),
        ]) for p in loose]
        out += ('<div class="split"><h3>Legs with no ledger entry</h3>'
                '<p class="cap">Open at the broker but not stamped with a '
                'defined-risk grant.</p>'
                + table(["Symbol", "Side", "Qty", "Avg entry", "Current",
                         "Market value", "Unrealized P&L"], rows, "num")
                + "</div>")
    return out or '<p class="note">No open positions.</p>'


# --------------------------------------------------------------- log tables

def denies_section(records) -> str:
    denies = [r for r in records if is_deny(r)]
    if not denies:
        return ('<p class="note">No broker denies on the tape. Every call so '
                "far had a matching manifest entry.</p>")
    rows = [("deny", [
        esc(r.get("seq")), utc(r.get("ts")),
        f'{esc(r.get("tool"))}.{esc(r.get("op"))}',
        '<span class="badge crit">denied</span>',
        f'<span class="reason">{esc(r.get("reason"))}</span>',
        f'<code>{esc(short_digest(r.get("argsDigest")))}</code>',
    ]) for r in reversed(denies)]
    return table(["Seq", "Timestamp", "Call", "Outcome", "Reason", "Args"], rows)


def shim_section(refusals, note, gate_records) -> str:
    extra = ""
    if len(gate_records) > len(refusals):
        extra = (f'<p class="note">The tape carries '
                 f"{plural(len(gate_records), 'executed call')} with an error "
                 f"result; {len(refusals)} of them are detailed below.</p>")
    if not refusals:
        why = note or "no records"
        return (f'<p class="note">No defined-risk refusals recorded '
                f"({esc(why)}).</p>" + extra)
    rows = [("gate", [
        utc(r.get("refused_at")),
        f'<span class="warn">{esc(r.get("reason"))}</span>',
        esc(r.get("qty")), money(r.get("limit_price")),
        "<br>".join(esc(s) for s in (r.get("legs") or [])) or "—",
    ]) for r in reversed(refusals)]
    return table(["Refused at", "Reason", "Qty", "Limit", "Legs"], rows) + extra


def _log_rows(records) -> list:
    rows = []
    for r in reversed(records):
        pr = r.get("principal") or {}
        if is_deny(r):
            rc, badge, tone = "deny", "crit", "denied at the broker"
        elif is_gate_refusal(r):
            rc, badge, tone = "gate", "gate", "refused at the risk gate"
        else:
            rc, badge, tone = "", "ok", f'{esc(r.get("decision"))} · {esc(r.get("outcome"))}'
        detail = r.get("reason") or r.get("error")
        rows.append((rc, [
            esc(r.get("seq")), utc(r.get("ts")),
            f'{esc(r.get("tool"))}.{esc(r.get("op"))}',
            f'{esc(pr.get("agentId"))} / {esc(pr.get("skill"))}',
            f'<span class="badge {badge}">{tone}</span>',
            f'<span class="reason">{esc(detail)}</span>' if detail else "—",
            f'<code>{esc(short_digest(r.get("argsDigest")))}</code>',
        ]))
    return rows


LOG_HEADERS = ["Seq", "Timestamp", "Call", "Principal", "Decision",
               "Reason", "Args"]


def log_section(records) -> str:
    """Acting calls and every refusal up front; reads behind a disclosure."""
    acting, reads = [], []
    for r in records:
        quiet = is_read(r) and not is_deny(r) and not is_gate_refusal(r)
        (reads if quiet else acting).append(r)

    body = (table(LOG_HEADERS, _log_rows(acting))
            if acting else
            '<p class="note">No acting calls on the tape yet.</p>')
    if reads:
        body += (f'<details class="reads"><summary>Show the '
                 f"{plural(len(reads), 'read-only call')} (quotes, chains, "
                 f"clock, account and position reads)</summary>"
                 + table(LOG_HEADERS, _log_rows(reads)) + "</details>")
    return body


def orders_section(orders, err) -> str:
    if err:
        return unavailable(err)
    if not orders:
        return '<p class="note">No recent orders.</p>'
    rows = []
    for o in orders:
        # Multi-leg orders carry no top-level symbol; the legs do.
        legs = o.get("legs") or []
        if o.get("symbol"):
            sym, side = esc(o.get("symbol")), esc(o.get("side"))
        else:
            sym = "<br>".join(f'{esc(leg.get("side"))} {esc(leg.get("symbol"))}'
                              for leg in legs) or "—"
            side = esc(o.get("order_class")) or "—"
        rows.append(("", [
            sym, side, esc(o.get("type")), esc(o.get("qty")),
            esc(o.get("filled_qty")), money(o.get("filled_avg_price")),
            (
                f'<span class="badge {"ok" if o.get("status") == "filled" else "neutral"}">'
                f'{esc(o.get("status"))}</span>'
            ),
            utc(o.get("submitted_at")),
        ]))
    return table(["Symbol", "Side", "Type", "Qty", "Filled", "Fill price",
                  "Status", "Submitted"], rows, "num")


# -------------------------------------------------------------------- page

def first_acting_day(records) -> str | None:
    """Date of the first call that tried to move money, from the tape."""
    stamps = [utc(r.get("ts")) for r in records if not is_read(r)]
    return min(stamps)[:10] if stamps else None


def hero_block(account, acct_err, counts, n_gate, since) -> tuple[str, str]:
    """Two hero figures: what the mandate stopped, and what the account is
    worth. Refusals lead because the enforced mandate is the claim; equity is
    the evidence that the agent still traded under it."""
    equity = fnum((account or {}).get("equity"))
    stopped = counts["deny"] + n_gate
    split = (f'{plural(counts["deny"], "call")} denied at the broker · '
             f'{plural(n_gate, "placement")} refused at the risk gate')
    hero_note = ("Nothing has been stopped yet. Both gates are in the path of "
                 "every call and each attempt is on the tape either way."
                 if stopped == 0 else
                 "Each one is listed below with the reason it was stopped.")

    if equity is None:
        left = ('<div class="heroblock"><div class="hero">—</div>'
                + unavailable(acct_err or "no account data") + "</div>")
        tiles = ""
    else:
        traded = (f"First order placed under the mandate {esc(since)}"
                  if since else "No order placed under the mandate yet")
        left = (f'<div class="heroblock"><div class="hero">{money(equity)}</div>'
                f'<div class="hero-label">Account equity · Alpaca paper</div>'
                f'<div class="hero-split">{traded}</div></div>')
        pl = equity - START_EQUITY
        cls = "pos" if pl >= 0 else "neg"
        tiles = (
            f'<div class="tiles">'
            f'<div class="tile"><span class="tl">P&amp;L since $100,000 start</span>'
            f'<span class="tv {cls}">{signed_money(pl)}</span>'
            f'<span class="td">{pl / START_EQUITY * 100:+.3f}%</span></div>'
            f'<div class="tile"><span class="tl">Options buying power</span>'
            f'<span class="tv">{money((account or {}).get("options_buying_power"), 0)}</span>'
            f'<span class="td">Account {esc((account or {}).get("status"))}</span></div>'
            f'<div class="tile"><span class="tl">Brokered calls on tape</span>'
            f'<span class="tv">{counts["total"]}</span>'
            f'<span class="td">{counts["place"]} placements · '
            f'{counts["read"]} reads</span></div>'
            f"</div>"
        )
    right = (f'<div class="heroblock"><div class="hero">{stopped}</div>'
             f'<div class="hero-label">Calls stopped by the mandate</div>'
             f'<div class="hero-split">{split}</div>'
             f'<p class="hero-note">{hero_note}</p></div>')
    return f'<div class="heroes">{right}{left}</div>', tiles


def counts_strip(counts, n_gate) -> str:
    return (f'<p class="counts"><strong>{counts["total"]} brokered calls</strong>: '
            f'{plural(counts["place"], "placement")}, '
            f'{plural(counts["close"], "close")}, '
            f'{plural(counts["cancel"], "cancel")}, '
            f'{counts["deny"]} denied at the broker, '
            f'{n_gate} refused at the risk gate, '
            f'{counts["read"]} read-only.</p>'
            f'<p class="note">{esc(GATE_TAPE_CAVEAT)}</p>')


def agent_model() -> str:
    """The model that decides, read from the same line every acting run uses.

    Reading run/lib.sh rather than hardcoding it here means the published page
    cannot claim one model while the runs use another.
    """
    try:
        for line in (ROOT / "run" / "lib.sh").read_text().splitlines():
            if line.startswith("AGENT_MODEL="):
                return line.split("=", 1)[1].strip().strip('"')
    except OSError:
        pass
    return "unrecorded"


def reproduce_section(records, sup_records, refusals) -> str:
    """Tell the reader how to check the record themselves, with live numbers.

    The dashboard is our rendering of the tape, so on its own it asks to be
    trusted. This section hands over the file and the command instead.
    """
    head = records[-1]["hash"] if records else "—"
    return f"""
  <p class="shead">This page is our rendering of the record. Here is how to check
  the record itself, without taking our word for any of it.</p>
  <pre class="verify"><code>git clone https://github.com/wjatx/mandate
cd mandate
python3 tools/verify_tape.py tape/audit.jsonl</code></pre>
  <p class="vnote">No credentials, no network, no dependencies outside the Python
  standard library. The chain is unkeyed SHA-256, which is what makes it checkable
  by anyone. Published now:
  <strong>{len(records)}</strong> agent records,
  <strong>{len(sup_records)}</strong> supervisor records, and
  <strong>{len(refusals)}</strong> defined-risk refusals in the unchained sidecar.
  Chain head <code>{esc(short_digest(head))}</code>.</p>
  <p class="vnote">The decisions are made by <strong>{esc(agent_model())}</strong>, pinned
  in <code>run/lib.sh</code> and passed explicitly to every scheduled run. It is pinned for
  the same reason the broker's dependencies are: an unpinned model can change under a
  running system without raising anything, and a silent swap is worse than a loud break.
  Each run also logs the model it actually used, so the record shows what decided rather
  than what was configured.</p>
  <p class="vnote">The two files are different kinds of evidence. The tapes are
  hash-chained, so editing, dropping, or reordering any record breaks every hash
  after it. <code>shim_refusals.jsonl</code> is an ordinary log with no integrity
  claim: those refusals happen inside the admitted connector, so the broker sees a
  tool returning a result rather than a decision of its own. We publish it anyway,
  because the chained tape alone would show fewer refusals than the system actually
  made.</p>"""


def build() -> str:
    records, _ = read_jsonl(AUDIT)
    sup_records, _ = read_jsonl(ROOT / "state" / "audit-supervisor.jsonl")
    refusals, refusal_note = read_jsonl(REFUSALS)
    ledger = read_ledger()
    chain_ok, verdict, _ = verify_tape()

    get = api_client()
    account, acct_err = fetch(get, "/v2/account")
    positions, pos_err = fetch(get, "/v2/positions")
    history, hist_err = fetch(get, "/v2/account/portfolio/history"
                                   "?period=1W&timeframe=15Min")
    orders, ord_err = fetch(get, "/v2/orders?status=all&limit=50")

    counts = tape_counts(records)
    gate_records = [r for r in records if is_gate_refusal(r)]
    # The shim's own file is the detailed record; the tape is the fallback
    # count when that file has not been written yet.
    n_gate = len(refusals) if REFUSALS.exists() else len(gate_records)

    heroes, tiles = hero_block(account, acct_err, counts, n_gate,
                               first_acting_day(records))
    verdict_cls = "ok" if chain_ok else "crit"

    stamps, values, trim_note, chart_err = equity_series(
        history, fnum((account or {}).get("equity")))
    if hist_err or chart_err:
        chart, chart_cap = unavailable(hist_err or chart_err), ""
    else:
        chart = equity_curve_svg(
            stamps, values,
            "Account equity in dollars over the trading window, 15-minute marks.")
        chart_cap = f'<p class="cap">{esc(trim_note)}</p>' if trim_note else ""

    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>mandate — audit dashboard</title>
<meta name="description" content="{esc(MECHANISM)}">
<link rel="icon" href="{FAVICON_DATA_URI}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="mandate">
<meta property="og:url" content="{SITE}">
<meta property="og:title" content="mandate — {esc(TAGLINE)}">
<meta property="og:description" content="{esc(MECHANISM)}">
<meta property="og:image" content="{SITE}og.svg">
<meta property="og:image:type" content="image/svg+xml">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<style>{CSS}</style></head><body><main>

<section>
  <h1>mandate</h1>
  <p class="sub">{esc(TAGLINE)}. {esc(MECHANISM)}</p>
  {heroes}
  {tiles}
  <div class="verdict">
    <span><span class="badge {verdict_cls}">tape {"consistent" if chain_ok else "unverified"}</span></span>
    <span>{esc(verdict)}</span>
    <span>Generated {utc(datetime.now(timezone.utc))}</span>
  </div>
</section>

<section class="refusals">
  <h2>Refusals</h2>
  <p class="shead">What the mandate stopped, in two classes. A broker deny means
    the call never reached Alpaca. A risk-gate refusal means the broker allowed
    the call and the defined-risk shim declined to place the order.</p>
  <div class="split">
    <h3>Refused at the broker</h3>
    <p class="cap">The manifest had no entry for the call, so it was denied
      before it left the stack.</p>
    {denies_section(records)}
  </div>
  <div class="split">
    <h3>Refused at the risk gate</h3>
    <p class="cap">These reach the tape as ordinary executed calls carrying an
      error result, so the shim logs them separately.</p>
    {shim_section(refusals, refusal_note, gate_records)}
  </div>
</section>

<section>
  <h2>Account equity</h2>
  <p class="shead">True account value in dollars at 15-minute marks, rebuilt from
    the broker's portfolio history and checked against the live account figure
    above. The two differ by the time since the last mark.</p>
  {chart}
  {chart_cap}
</section>

<section>
  <h2>Open spreads</h2>
  <p class="shead">Live legs from the paper account, grouped into the
    defined-risk spreads the risk ledger stamped when each was placed.</p>
  {positions_section(positions, pos_err, ledger)}
</section>

<section>
  <h2>Decision log</h2>
  <p class="shead">Every brokered call, newest first.</p>
  {counts_strip(counts, n_gate)}
  {log_section(records)}
</section>

<section>
  <h2>Recent orders</h2>
  <p class="shead">Last 50 orders at the broker, any status.</p>
  {orders_section(orders, ord_err)}
</section>

<section>
  <h2>Verify this yourself</h2>
  {reproduce_section(records, sup_records, refusals)}
</section>

</main><footer>
<p>The audit chain is unkeyed SHA-256. Verification proves the tape is
<strong>self-consistent</strong> — no record was edited, dropped, or reordered in
place. It is not tamper-proof: anyone who can write the file can rewrite it whole
and recompute every hash. Tamper-evidence needs off-device append-only storage.</p>
<p>This page is regenerated from the audit tape; the agent cannot write this page.</p>
</footer></body></html>
"""


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OG_OUT.write_text(og_card_svg())
    OUT.write_text(build())
    print(f"wrote {OUT} ({OUT.stat().st_size:,} bytes)")
