"""Pure risk arithmetic for the defined-risk shim.

Everything here is a total function of its arguments: no MCP session, no
clock of its own, no filesystem. `alpaca_shim` owns the I/O (vendor calls,
ledger file) and calls in here for every accept/refuse decision, so the
decisions themselves are unit-testable without spawning the vendor server.

limit_price convention throughout follows the vendor tool: positive = net
debit per spread, negative = net credit per spread (per contract, x100 USD).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime

CONTRACT_MULTIPLIER = 100


class CapsError(ValueError):
    """The manifest cannot supply valid signed risk caps. Fatal at startup."""


@dataclass(frozen=True)
class RiskCaps:
    """The dollar caps in force, plus the envelope hash that signs them.

    Since the 2026-08-26 re-key design, the caps have no home in code: they
    live in the manifest's envelope block, which every grant pins by content
    hash (envelopeHash). Changing a cap changes the hash, which quarantines
    the grants at first exercise until a re-key ceremony re-attests them —
    the caps cannot drift apart from what was signed.
    """

    max_loss_per_position_usd: float
    max_total_open_risk_usd: float
    envelope_hash: str


def caps_from_manifest(manifest: object) -> RiskCaps:
    """Extract the signed dollar caps from a parsed manifest mapping.

    Validates through the broker's own Envelope schema and computes the same
    canonical content-hash the broker enforces grants against, so what the
    shim enforces and what the ceremony signed are one artifact. No defaults
    anywhere: a manifest that cannot produce both caps refuses, because a
    shim that guesses its own limits is the bug this design removes.
    """
    # Lazy import: the pure arithmetic in this module stays importable and
    # testable without the broker package on the path.
    from safe_agents.broker.schemas.envelope import Envelope, compute_envelope_hash

    if not isinstance(manifest, dict) or not isinstance(manifest.get("envelope"), dict):
        raise CapsError("manifest has no envelope block; refusing to run uncapped")
    try:
        envelope = Envelope.model_validate(manifest["envelope"])
    except Exception as exc:
        raise CapsError(f"envelope block failed schema validation: {exc}") from exc

    def _cap(name: str) -> float:
        value = getattr(envelope.caps, name, None) if envelope.caps else None
        if not isinstance(value, (int, float)) or isinstance(value, bool) or value <= 0:
            raise CapsError(
                f"envelope.caps.{name} is missing or not a positive number; "
                "the caps live in the envelope block so the ceremony signs them"
            )
        return float(value)

    per_position = _cap("max_loss_per_position_usd")
    book = _cap("max_total_open_risk_usd")
    if per_position > book:
        raise CapsError(
            f"envelope.caps: per-position cap ${per_position:,.0f} exceeds the "
            f"book cap ${book:,.0f}; a single position may never be the whole book"
        )
    return RiskCaps(per_position, book, compute_envelope_hash(envelope))

# 0DTE hard stop: nothing expiring today may be OPENED at or after this
# exchange-local time. Closing and cancelling stay available all session.
ZERO_DTE_CUTOFF_HHMM = (15, 15)
ZERO_DTE_CUTOFF_LABEL = "15:15"

OCC_RE = re.compile(
    r"^(?P<root>[A-Z]{1,6})(?P<date>\d{6})(?P<cp>[CP])(?P<strike>\d{8})$"
)


@dataclass
class Leg:
    symbol: str
    side: str  # buy | sell
    ratio_qty: int
    root: str
    expiry: str
    cp: str  # C | P
    strike: float


def parse_leg(raw: dict) -> Leg:
    sym = raw.get("symbol", "")
    m = OCC_RE.match(sym)
    if not m:
        raise ValueError(f"leg symbol {sym!r} is not a valid OCC option symbol")
    side = raw.get("side", "")
    if side not in ("buy", "sell"):
        raise ValueError(f"leg side {side!r} must be 'buy' or 'sell'")
    ratio = int(raw.get("ratio_qty", "1"))
    if ratio < 1:
        raise ValueError(f"leg ratio_qty {ratio} must be >= 1")
    return Leg(
        symbol=sym,
        side=side,
        ratio_qty=ratio,
        root=m.group("root"),
        expiry=m.group("date"),
        cp=m.group("cp"),
        strike=int(m.group("strike")) / 1000.0,
    )


def _condor_wing_width(wing: list[Leg], cp: str) -> float:
    """Strike width of one condor wing, which must be a credit vertical.

    Puts collect credit by selling the higher strike and buying the lower;
    calls by selling the lower and buying the higher. Anything else is a
    debit wing (or a naked pair) and is refused.
    """
    sells = [leg for leg in wing if leg.side == "sell"]
    buys = [leg for leg in wing if leg.side == "buy"]
    if len(sells) != 1 or len(buys) != 1:
        raise ValueError(
            f"an iron condor's {cp} wing must have exactly one buy and one sell leg"
        )
    width = sells[0].strike - buys[0].strike if cp == "P" else buys[0].strike - sells[0].strike
    if width <= 0:
        raise ValueError(
            "an iron condor must sell the higher-strike put and the lower-strike "
            "call (both wings credit verticals with distinct strikes)"
        )
    return width


def max_loss_usd(legs: list[Leg], qty: int, limit_price: float) -> tuple[float, str]:
    """Return (max loss in USD, recognized-structure name) or raise ValueError.

    Recognized structures (composition-proof cut):
      - single long option (debit): max loss = debit paid
      - 2-leg vertical (same type, same expiry, 1 buy + 1 sell, equal ratio):
        debit -> max loss = net debit; credit -> max loss = width - net credit
      - 4-leg iron condor (put credit wing + call credit wing, one expiry):
        max loss = widest wing - net credit
    limit_price convention follows the vendor tool: positive = net debit,
    negative = net credit (per contract, not per share).
    """
    if len(legs) == 1:
        leg = legs[0]
        if leg.side != "buy":
            raise ValueError(
                "single-leg orders may only be long (buy): a short option is "
                "not defined-risk"
            )
        if limit_price <= 0:
            raise ValueError("a long single-leg order must be a net debit (limit_price > 0)")
        return limit_price * CONTRACT_MULTIPLIER * qty * leg.ratio_qty, "long_single"

    if len(legs) == 2:
        a, b = legs
        if {a.side, b.side} != {"buy", "sell"}:
            raise ValueError("a 2-leg order must have exactly one buy and one sell leg")
        if a.cp != b.cp:
            raise ValueError("a vertical's legs must be the same option type (both C or both P)")
        if a.expiry != b.expiry or a.root != b.root:
            raise ValueError("a vertical's legs must share underlying and expiration")
        if a.ratio_qty != b.ratio_qty:
            raise ValueError("a vertical's legs must have equal ratio_qty")
        width = abs(a.strike - b.strike)
        if width <= 0:
            raise ValueError("a vertical's legs must have distinct strikes")
        per_spread = width * CONTRACT_MULTIPLIER
        if limit_price > 0:  # debit vertical
            loss = limit_price * CONTRACT_MULTIPLIER
            name = "debit_vertical"
        else:  # credit vertical: max loss = width - credit
            loss = per_spread - abs(limit_price) * CONTRACT_MULTIPLIER
            name = "credit_vertical"
            if loss <= 0:
                raise ValueError("credit exceeds spread width; order shape is wrong")
        return loss * qty * a.ratio_qty, name

    if len(legs) == 4:
        head = legs[0]
        if any(leg.root != head.root or leg.expiry != head.expiry for leg in legs):
            raise ValueError("an iron condor's legs must share underlying and expiration")
        if any(leg.ratio_qty != head.ratio_qty for leg in legs):
            raise ValueError("an iron condor's legs must have equal ratio_qty")
        puts = [leg for leg in legs if leg.cp == "P"]
        calls = [leg for leg in legs if leg.cp == "C"]
        if len(puts) != 2 or len(calls) != 2:
            raise ValueError("an iron condor must have exactly two puts and two calls")
        if limit_price >= 0:
            raise ValueError("an iron condor must be a net credit (limit_price < 0)")
        # Loss is capped by the wider wing: only one side can finish in the money.
        widest = max(_condor_wing_width(puts, "P"), _condor_wing_width(calls, "C"))
        loss = (widest - abs(limit_price)) * CONTRACT_MULTIPLIER
        if loss <= 0:
            raise ValueError("credit exceeds the widest condor wing; order shape is wrong")
        return loss * qty * head.ratio_qty, "iron_condor"

    raise ValueError(
        f"{len(legs)}-leg orders are not a recognized defined-risk structure "
        "(composition-proof shim recognizes 1-leg long, 2-leg verticals and "
        "4-leg iron condors)"
    )


# --- Exit values, computed once at entry -----------------------------------
# Charter §4: "Exit values are computed once, at entry, by the defined-risk
# gate, and stamped into the position's ledger row." Stamping them here is what
# makes the charter's first line ("not re-litigated later") structural rather
# than aspirational: the supervisor enforces these numbers, so amending §4
# cannot reach back and move a live position's exits.
#
# Per share, in limit_price's units, so the supervisor compares them directly
# against buyback_cost without a multiplier.

CREDIT_TAKE_PROFIT_FRACTION = 0.5  # close once half the credit is captured
CREDIT_STOP_MULTIPLE = 2.0  # stop when buying the spread back costs 2x credit
DEBIT_PROFIT_CAPTURE_FRACTION = 0.5  # half of maximum profit (width - debit)
DEBIT_STOP_FRACTION = 0.5  # stop when the spread is worth half the debit paid

# Money rounds to a tenth of a cent. Ledger rows are read by humans in an
# audit, and 4dp is two orders of magnitude finer than any option tick, so it
# cannot move a comparison the supervisor makes.
_EXIT_VALUE_DP = 4


def _vertical_width(legs: list[Leg]) -> float | None:
    """Strike width of a 2-leg vertical, or None if these legs are not one."""
    if len(legs) != 2:
        return None
    width = abs(legs[0].strike - legs[1].strike)
    return width if width > 0 else None


def exit_values(legs: list[Leg], structure: str, limit_price: float,
                vol_pair: bool = False) -> dict[str, float]:
    """Charter §4 exits for an accepted order, per share, keyed for the ledger.

    Returns {} for anything it cannot compute honestly, and never raises. That
    totality is deliberate and load-bearing: the shim calls this *after* the
    vendor has accepted the order, so an exception here would place a position
    and then fail to record it, blinding the book cap. A row that carries no
    exit fields is a row the supervisor prices with its own constants, which is
    exactly the behaviour that shipped before this function existed.

    - credit_vertical / iron_condor: buyback-cost thresholds. Take profit when
      the spread can be bought back for half the credit; stop when it costs 2x.
    - debit_vertical: spread-value thresholds. Take profit at half of maximum
      profit (debit + half of width - debit), stop at half the debit paid.
    - debit_vertical with vol_pair (§4 as amended 2026-08-29): take-profit
      only, no stop key. The pair is long the event; a per-leg stop closes
      the losing half of a hedged structure exactly when the thesis needs it
      held. The supervisor reads the row's vol_pair marker and enforces
      take-profit and clock with no value stop.
    - long_single: no exit fields. The charter's debit rule speaks of
      *verticals*, and rules.py deliberately leaves a naked long to the agent;
      stamping exits on one here would legislate that ruling away by accident.
    """
    if structure in ("credit_vertical", "iron_condor"):
        credit = -limit_price
        if credit <= 0:
            return {}
        tp = CREDIT_TAKE_PROFIT_FRACTION * credit
        stop = CREDIT_STOP_MULTIPLE * credit
    elif structure == "debit_vertical":
        debit = limit_price
        width = _vertical_width(legs)
        if debit <= 0 or width is None or width <= debit:
            # width <= debit is a spread that cannot profit; rather than refuse
            # an order shape the gate accepts today, stamp nothing and let the
            # supervisor fall back. Refusing here would be a new refusal.
            return {}
        tp = debit + DEBIT_PROFIT_CAPTURE_FRACTION * (width - debit)
        stop = DEBIT_STOP_FRACTION * debit
    else:
        return {}

    tp = round(tp, _EXIT_VALUE_DP)
    stop = round(stop, _EXIT_VALUE_DP)
    if tp <= 0 or stop <= 0:
        return {}
    if vol_pair and structure == "debit_vertical":
        return {"exit_tp_value": tp}
    return {"exit_tp_value": tp, "exit_stop_value": stop}


def parse_clock_timestamp(clock: dict) -> datetime:
    """Exchange-local 'now' from get_clock's data; the offset is ET."""
    ts = clock.get("timestamp")
    if not isinstance(ts, str):
        # TRY004 silenced: ValueError is the refusal channel — the shim's place
        # tool catches it to write the refusal log before re-raising.
        raise ValueError("market clock carried no timestamp; refusing to open a position")  # noqa: TRY004
    return datetime.fromisoformat(ts)


def zero_dte_refusal(now_exchange: datetime, legs: list[Leg]) -> str | None:
    """Refusal text when a leg expires today and the cutoff has passed, else None."""
    today = now_exchange.strftime("%y%m%d")
    expiring = sorted({leg.symbol for leg in legs if leg.expiry == today})
    if not expiring or (now_exchange.hour, now_exchange.minute) < ZERO_DTE_CUTOFF_HHMM:
        return None
    return (
        f"0DTE refusal: {', '.join(expiring)} expire today and the "
        f"{ZERO_DTE_CUTOFF_LABEL} exchange-local cutoff for opening 0DTE positions "
        f"has passed (clock reads {now_exchange:%H:%M} exchange-local)"
    )


# --- Open-risk ledger ------------------------------------------------------
# Every accepted placement is recorded; an entry stays LIVE while any of its
# legs is still a position or its order is still resting. Pruning on each
# placement keeps the book cap honest without a background reconciler.


def ledger_entry_is_live(
    entry: dict, position_symbols: set[str], open_order_ids: set[str]
) -> bool:
    if any(sym in position_symbols for sym in entry.get("legs", [])):
        return True
    order_id = entry.get("order_id")
    return bool(order_id) and str(order_id) in open_order_ids


def prune_ledger(
    entries: list[dict], position_symbols: set[str], open_order_ids: set[str]
) -> list[dict]:
    return [e for e in entries if ledger_entry_is_live(e, position_symbols, open_order_ids)]


def open_risk_usd(entries: list[dict]) -> float:
    total = 0.0
    for entry in entries:
        try:
            total += float(entry.get("max_loss_usd", 0.0))
        except (TypeError, ValueError):  # a malformed row must not read as zero risk
            raise ValueError(f"risk ledger entry has an unusable max_loss_usd: {entry!r}")
    return total
