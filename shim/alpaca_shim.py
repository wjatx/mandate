"""Defined-risk order shim (D6 Option A) — composition-proof version.

The broker gateway spawns THIS server as the manifest's `alpaca` connector; we
spawn the vendor `alpaca-mcp-server` as our own stdio child, inheriting the
credentials the gateway delivered via env_map (ALPACA_API_KEY /
ALPACA_SECRET_KEY) plus the manifest-pinned ALPACA_PAPER_TRADE. The agent
never sees a credential, and raw `place_option_order` is absent from the
entire admitted chain: the only acting order op we expose is
`place_defined_risk_spread`, which refuses anything that is not a recognized
defined-risk structure under the per-position cap, the book-wide open-risk
cap, or the 0DTE afternoon cutoff.

Missileer twice: the gateway admits only what this file exposes, and this
file can only express defined risk. The arithmetic behind every refusal
lives in the sibling `defined_risk` module, which has no I/O of its own.
"""

from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path

# Sibling module, deliberately import-only: all accept/refuse arithmetic lives
# there so it can be tested without an MCP session (see test_alpaca_shim.py).
from defined_risk import (
    CapsError,
    RiskCaps,
    caps_from_manifest,
    exit_values,
    max_loss_usd,
    open_risk_usd,
    parse_clock_timestamp,
    parse_leg,
    prune_ledger,
    zero_dte_refusal,
)
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.server.fastmcp import FastMCP

VENDOR_PIN = "alpaca-mcp-server==2.1.1"

# The dollar caps have no home in this code: they are read at startup from the
# envelope block of the manifest named here, which every grant pins by content
# hash. The gateway quarantines the grants if that block changes, so the shim
# refusing to start without it is the matching posture — never trade uncapped.
BROKER_MANIFEST_ENV = "BROKER_MANIFEST"


def _load_caps() -> RiskCaps:
    manifest_path = os.environ.get(BROKER_MANIFEST_ENV)
    if not manifest_path:
        raise SystemExit(
            f"alpaca_shim: {BROKER_MANIFEST_ENV} is not set; the shim refuses to "
            "start without the signed risk caps (charter §5). Declare it in the "
            "manifest's mcp_servers env block."
        )
    try:
        import yaml

        manifest = yaml.safe_load(Path(manifest_path).read_text())
    except OSError as exc:
        raise SystemExit(f"alpaca_shim: cannot read manifest at {manifest_path}: {exc}")
    try:
        return caps_from_manifest(manifest)
    except CapsError as exc:
        raise SystemExit(f"alpaca_shim: {manifest_path}: {exc}")


CAPS = _load_caps()

# The enforced values and the hash that signs them are part of the advertised
# tool description ON PURPOSE: the admission registry stores descriptions and
# drift-quarantines on change, so a shim enforcing different numbers is
# structurally un-discoverable until a human re-acks the delta. What the tool
# says it enforces, what it enforces, and what the ceremony signed are one
# artifact.
PLACE_DESCRIPTION = (
    "Place a defined-risk options order (long single, vertical or iron condor).\n\n"
    "limit orders only; limit_price positive = net debit, negative = net\n"
    "credit. Refuses any shape whose max loss is not computable or exceeds\n"
    f"the per-position cap (${CAPS.max_loss_per_position_usd:,.0f}), any order that "
    f"would push total open risk over the book cap (${CAPS.max_total_open_risk_usd:,.0f}), "
    "and any 0DTE opener after the afternoon cutoff. "
    f"Enforcing envelope {CAPS.envelope_hash}."
)

# Persistent record of accepted placements, used to enforce the book cap
# across restarts. Relative paths resolve against the gateway's CWD.
LEDGER_PATH_ENV = "SHIM_LEDGER_PATH"
DEFAULT_LEDGER_PATH = "state/risk_ledger.json"

# Shim refusals reach the broker tape as ordinary executed calls (the broker
# allowed; the shim refused at execution), so the dashboard needs this
# separate append-only record to render them as denies. Best-effort: a lost
# log line loses visibility, never the refusal itself.
REFUSAL_LOG_ENV = "SHIM_REFUSAL_LOG_PATH"
DEFAULT_REFUSAL_LOG_PATH = "state/shim_refusals.jsonl"

_child: ClientSession | None = None


def _ledger_path() -> Path:
    return Path(os.environ.get(LEDGER_PATH_ENV) or DEFAULT_LEDGER_PATH)


def _read_ledger() -> list[dict]:
    """Load the ledger; a missing or unreadable file reads as an empty book."""
    try:
        raw = json.loads(_ledger_path().read_text())
    except (FileNotFoundError, ValueError, OSError):
        return []
    return [e for e in raw if isinstance(e, dict)] if isinstance(raw, list) else []


def _log_refusal(reason: str, *, qty: str, limit_price: str, legs: list[dict]) -> None:
    """Append one refusal record; best-effort (see REFUSAL_LOG_ENV comment)."""
    record = {
        "refused_at": datetime.now(UTC).isoformat(),
        "reason": reason,
        "qty": qty,
        "limit_price": limit_price,
        "legs": [leg.get("symbol") for leg in legs if isinstance(leg, dict)],
    }
    try:
        path = Path(os.environ.get(REFUSAL_LOG_ENV) or DEFAULT_REFUSAL_LOG_PATH)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a") as f:
            f.write(json.dumps(record) + "\n")
    except OSError:
        pass


def _write_ledger(entries: list[dict]) -> None:
    """Persist the ledger. Write failures propagate: a book we cannot record
    is a book we cannot cap."""
    path = _ledger_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(entries, indent=2) + "\n")


mcp = FastMCP("alpaca-defined-risk")


def _text(result) -> str:
    return "\n".join(c.text for c in result.content if hasattr(c, "text"))


async def _forward(name: str, **kwargs) -> str:
    """Call the vendor child with only the non-None arguments."""
    assert _child is not None
    args = {k: v for k, v in kwargs.items() if v is not None}
    res = await _child.call_tool(name, args)
    if res.isError:
        raise RuntimeError(_text(res))
    return _text(res)


def _vendor_data(payload: str):
    """Unwrap the vendor's {"_alpaca_mcp_security": ..., "data": ...} envelope."""
    try:
        obj = json.loads(payload)
    except ValueError:
        raise ValueError(f"vendor returned unparseable JSON: {payload[:200]!r}")
    return obj.get("data") if isinstance(obj, dict) and "data" in obj else obj


def _rows(data) -> list[dict]:
    # The vendor wraps list results one level deeper: {"result": [...]}.
    # Tolerate a bare list too, so a vendor-version bump can't silently
    # zero the book-cap's view of live risk again.
    if isinstance(data, dict) and isinstance(data.get("result"), list):
        data = data["result"]
    return [r for r in data if isinstance(r, dict)] if isinstance(data, list) else []


async def _exchange_now() -> datetime:
    """Exchange-local wall clock, taken from the broker rather than this host."""
    data = _vendor_data(await _forward("get_clock"))
    if not isinstance(data, dict):
        # TRY004 silenced: ValueError is the refusal channel here — the place
        # tool's handler catches it to write the shim refusal log. A TypeError
        # would skip that log and surface as a crash instead of a refusal.
        raise ValueError("market clock was unreadable; refusing to open a position")  # noqa: TRY004
    return parse_clock_timestamp(data)


async def _live_open_risk() -> tuple[list[dict], float]:
    """Prune the ledger against live positions/orders; return (entries, risk USD)."""
    entries = _read_ledger()
    if not entries:
        return [], 0.0
    positions = _rows(_vendor_data(await _forward("get_all_positions")))
    orders = _rows(_vendor_data(await _forward("get_orders", status="open")))
    symbols = {p["symbol"] for p in positions if p.get("symbol")}
    ids = {str(o["id"]) for o in orders if o.get("id")}
    live = prune_ledger(entries, symbols, ids)
    if live != entries:
        _write_ledger(live)
    return live, open_risk_usd(live)


def _vendor_order_id(payload: str) -> str | None:
    try:
        data = _vendor_data(payload)
    except ValueError:
        return None
    return str(data["id"]) if isinstance(data, dict) and data.get("id") else None


# Read ops proxied verbatim to the vendor child (explicit signatures — the
# gateway's admitted def-hash pins these schemas). close/cancel act ops are
# also verbatim: they only reduce or annul exposure.


@mcp.tool()
async def get_account_info() -> str:
    """Account status, equity, buying power."""
    return await _forward("get_account_info")


@mcp.tool()
async def get_clock() -> str:
    """Market clock: open state, next open/close."""
    return await _forward("get_clock")


@mcp.tool()
async def get_calendar(start: str | None = None, end: str | None = None) -> str:
    """Market calendar between start and end (YYYY-MM-DD)."""
    return await _forward("get_calendar", start=start, end=end)


@mcp.tool()
async def get_stock_latest_quote(symbols: str) -> str:
    """Latest stock quote(s); symbols is comma-separated."""
    return await _forward("get_stock_latest_quote", symbols=symbols)


@mcp.tool()
async def get_all_positions() -> str:
    """All open positions."""
    return await _forward("get_all_positions")


@mcp.tool()
async def get_open_position(symbol_or_asset_id: str) -> str:
    """One open position by symbol or asset id."""
    return await _forward("get_open_position", symbol_or_asset_id=symbol_or_asset_id)


@mcp.tool()
async def get_option_chain(
    underlying_symbol: str,
    type: str | None = None,
    strike_price_gte: str | None = None,
    strike_price_lte: str | None = None,
    expiration_date: str | None = None,
    expiration_date_gte: str | None = None,
    expiration_date_lte: str | None = None,
    feed: str | None = None,
    limit: int | None = None,
) -> str:
    """Option chain for an underlying, filterable by type/strike/expiry."""
    return await _forward(
        "get_option_chain",
        underlying_symbol=underlying_symbol,
        type=type,
        strike_price_gte=strike_price_gte,
        strike_price_lte=strike_price_lte,
        expiration_date=expiration_date,
        expiration_date_gte=expiration_date_gte,
        expiration_date_lte=expiration_date_lte,
        feed=feed,
        limit=limit,
    )


@mcp.tool()
async def get_option_contracts(
    underlying_symbols: list[str] | None = None,
    type: str | None = None,
    strike_price_gte: str | None = None,
    strike_price_lte: str | None = None,
    expiration_date: str | None = None,
    expiration_date_gte: str | None = None,
    expiration_date_lte: str | None = None,
    limit: int | None = None,
) -> str:
    """Option contract metadata, filterable by underlying/type/strike/expiry."""
    return await _forward(
        "get_option_contracts",
        underlying_symbols=underlying_symbols,
        type=type,
        strike_price_gte=strike_price_gte,
        strike_price_lte=strike_price_lte,
        expiration_date=expiration_date,
        expiration_date_gte=expiration_date_gte,
        expiration_date_lte=expiration_date_lte,
        limit=limit,
    )


@mcp.tool()
async def get_option_snapshot(
    symbols: str, feed: str | None = None, limit: int | None = None
) -> str:
    """Option snapshot(s): latest quote/trade, greeks, IV. symbols comma-separated."""
    return await _forward("get_option_snapshot", symbols=symbols, feed=feed, limit=limit)


@mcp.tool()
async def get_option_latest_quote(symbols: str, feed: str | None = None) -> str:
    """Latest option quote(s); symbols comma-separated."""
    return await _forward("get_option_latest_quote", symbols=symbols, feed=feed)


@mcp.tool()
async def get_orders(
    status: str | None = None,
    limit: int | None = None,
    symbols: list[str] | None = None,
    side: str | None = None,
) -> str:
    """List orders, filterable by status/symbols/side."""
    return await _forward("get_orders", status=status, limit=limit, symbols=symbols, side=side)


@mcp.tool()
async def close_position(
    symbol_or_asset_id: str,
    qty: str | None = None,
    percentage: str | None = None,
) -> str:
    """Close (all or part of) an open position. Only reduces exposure."""
    return await _forward(
        "close_position", symbol_or_asset_id=symbol_or_asset_id, qty=qty, percentage=percentage
    )


@mcp.tool()
async def cancel_order_by_id(order_id: str) -> str:
    """Cancel a resting order by id."""
    return await _forward("cancel_order_by_id", order_id=order_id)


@mcp.tool(description=PLACE_DESCRIPTION)
async def place_defined_risk_spread(
    qty: str,
    limit_price: str,
    legs: list[dict],
    client_order_id: str | None = None,
) -> str:
    assert _child is not None
    try:
        parsed = [parse_leg(leg) for leg in legs]
        q = int(qty)
        if q < 1:
            raise ValueError("qty must be >= 1")
        lp = float(limit_price)
        loss, structure = max_loss_usd(parsed, q, lp)
        if loss > CAPS.max_loss_per_position_usd:
            raise ValueError(
                f"defined-risk refusal: max loss ${loss:,.0f} exceeds per-position "
                f"cap ${CAPS.max_loss_per_position_usd:,.0f} ({structure})"
            )
        now = await _exchange_now()
        refusal = zero_dte_refusal(now, parsed)
        if refusal:
            raise ValueError(refusal)
        live, open_risk = await _live_open_risk()
        if open_risk + loss > CAPS.max_total_open_risk_usd:
            raise ValueError(
                f"defined-risk refusal: this order's max loss ${loss:,.0f} on top of "
                f"${open_risk:,.0f} of live open risk exceeds the book cap "
                f"${CAPS.max_total_open_risk_usd:,.0f}"
            )
    except ValueError as e:
        _log_refusal(str(e), qty=qty, limit_price=limit_price, legs=legs)
        raise
    args: dict = {
        "qty": qty,
        "type": "limit",
        "limit_price": limit_price,
        "legs": [
            {
                "symbol": leg.symbol,
                "ratio_qty": str(leg.ratio_qty),
                "side": leg.side,
                "position_intent": raw.get("position_intent"),
            }
            for leg, raw in zip(parsed, legs)
        ],
    }
    if len(parsed) == 1:
        only = args["legs"][0]
        args = {
            "qty": qty,
            "type": "limit",
            "limit_price": limit_price,
            "symbol": only["symbol"],
            "side": only["side"],
            "position_intent": only.get("position_intent"),
        }
    if client_order_id:
        args["client_order_id"] = client_order_id
    res = await _child.call_tool("place_option_order", args)
    if res.isError:
        raise RuntimeError(_text(res))
    body = _text(res)
    _write_ledger(
        live
        + [
            {
                "client_order_id": client_order_id,
                "order_id": _vendor_order_id(body),
                "legs": [leg.symbol for leg in parsed],
                "structure": structure,
                # entry limit, vendor sign convention (negative = net credit).
                "limit_price": limit_price,
                "max_loss_usd": loss,
                # Charter §4: exits are decided at entry and stored with the
                # position, so a later amendment to §4 cannot re-litigate a
                # live one. Per share, same units as limit_price. Absent for
                # structures the supervisor does not value-manage.
                **exit_values(parsed, structure, lp),
                "placed_at": now.isoformat(),
            }
        ]
    )
    return json.dumps({"defined_risk": {"structure": structure, "max_loss_usd": loss}}) + "\n" + body


async def main() -> None:
    global _child
    env = {
        **os.environ,
        "ALPACA_PAPER_TRADE": os.environ.get("ALPACA_PAPER_TRADE", "true"),
    }
    params = StdioServerParameters(command="uvx", args=[VENDOR_PIN], env=env)
    async with (
        stdio_client(params) as (read, write),
        ClientSession(read, write) as session,
    ):
        await session.initialize()
        _child = session
        await mcp.run_stdio_async()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
