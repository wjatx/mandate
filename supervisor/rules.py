"""Pure exit-rule arithmetic for mandate's position supervisor.

Everything here is a total function of its arguments: no MCP session, no clock
of its own, no filesystem. `supervisor.py` owns the I/O and calls in here for
every close/hold decision, so the decisions themselves are testable without
spawning a gateway. This mirrors the split the shim already uses between
alpaca_shim.py and defined_risk.py, for the same reason.

limit_price convention follows the vendor tool throughout: positive = net
debit per spread, negative = net credit per spread (per share; x100 USD).
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

# The OCC regex and the clock parser already exist and are already correct in
# the shim's pure-arithmetic module. Importing them beats copying them: two
# copies of an expiry parser is how the agent and its supervisor come to
# disagree about what "expires today" means.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "shim"))
# F401: parse_clock_timestamp is unused here and re-exported on purpose —
# supervisor.py imports it from this module, so the shim stays its one source.
from defined_risk import OCC_RE, parse_clock_timestamp  # noqa: F401

# Exit-rule constants. These mirror charter §4; the supervisor closes at 15:20
# ET rather than the charter's 15:15 opening cutoff so that a position the
# agent was supposed to close at 15:15 gets a five-minute grace period before
# the backstop reaches in and closes it on the agent's behalf.
SAME_DAY_CLOSE_HHMM = (15, 20)
VALUE_STOP_MULTIPLE = 2.0
TAKE_PROFIT_MULTIPLE = 0.5
# Charter §5, amended 2026-08-31 from -0.03 alongside the aggregate cap going
# from $30,000 to $85,000. The two must move together: at the new cap an
# ordinary day is roughly plus or minus 7% of the account, so a -3% breaker
# would demote the agent on the first normal session and re-promotion is a
# human ceremony. This value is NOT under the charter lock, so it can drift
# from the charter silently — it was found doing exactly that minutes after
# the amendment, when the supervisor still logged "-3% breaker" against a
# charter that said -25%.
CIRCUIT_BREAKER_PCT = -0.25
CREDIT_STRUCTURES = {"credit_vertical", "iron_condor"}

# Charter §4's debit-side counterparts as first ratified 2026-08-27: take
# profit at twice the debit paid, stop out at half. Since exits became stored
# at entry (§4, re-anchored the same evening) these are the FALLBACK only —
# what a row written before the gate stamped exits is priced against. Live
# rows carry their own numbers; see stored_exits(). Do not re-tune these to
# match a later amendment: their whole job is to reproduce the old behaviour
# for the rows that were entered under it.
# "long_single" is deliberately NOT here. The charter's debit rule speaks
# of *verticals*, and a lone long option has no short leg bounding its value —
# doubling on a naked long is a different bet from doubling on a spread, and
# reading the amendment as covering it would be the supervisor legislating.
# It stays clock-only, with its tactical exits left to the agent.
DEBIT_STRUCTURES = {"debit_vertical"}
DEBIT_TAKE_PROFIT_MULTIPLE = 2.0
DEBIT_STOP_MULTIPLE = 0.5

# Structures whose exits need live quotes. supervisor.py gates its quote fetch
# on this set, so a structure added to either set above starts getting quotes
# without a second edit over there.
VALUE_MANAGED_STRUCTURES = CREDIT_STRUCTURES | DEBIT_STRUCTURES


def expires_today(symbol: str, exchange_now: datetime) -> bool:
    m = OCC_RE.match(symbol)
    return bool(m) and m.group("date") == exchange_now.strftime("%y%m%d")


def past_same_day_cutoff(exchange_now: datetime) -> bool:
    return (exchange_now.hour, exchange_now.minute) >= SAME_DAY_CLOSE_HHMM


def buyback_cost(legs: list[str], qty_by_symbol: dict[str, float],
                 quotes: dict[str, dict]) -> tuple[float, list[str]]:
    """Net per-spread cost to unwind, priced against us on both sides.

    Short legs are bought back at the ASK, long legs sold at the BID — the
    worst plausible fill. A stop that prices itself at the mid triggers late,
    which on a value stop is the expensive direction to be wrong in.

    Per-share, matching limit_price's convention, and assumes 1:1 ratios —
    the only shapes the shim will accept (see defined_risk.max_loss_usd).
    Returns (cost, missing_symbols); cost is meaningless if anything is missing.
    """
    cost = 0.0
    missing: list[str] = []
    for sym in legs:
        row = quotes.get(sym) or {}
        qty = qty_by_symbol.get(sym, 0.0)
        price = row.get("ap") if qty < 0 else row.get("bp")
        if not isinstance(price, (int, float)) or price <= 0:
            missing.append(sym)
            continue
        cost += float(price) if qty < 0 else -float(price)
    return cost, missing


def entry_credit(entry: dict) -> float | None:
    """Per-share credit collected at entry, or None if the ledger cannot say.

    limit_price follows the vendor convention: negative = net credit. An entry
    written before that field existed reads as None and gets the clock rule
    only, never a value stop computed from a guess.
    """
    try:
        lp = float(entry["limit_price"])
    except (KeyError, TypeError, ValueError):
        return None
    return abs(lp) if lp < 0 else None


def entry_debit(entry: dict) -> float | None:
    """Per-share debit paid at entry, or None if the ledger cannot say.

    The mirror of entry_credit against the same vendor convention: positive =
    net debit. The field arrives from the ledger as a string ("0.05"), which
    float() handles; anything it cannot parse reads as None and gets the clock
    rule only, never a value rule computed from a guess.
    """
    try:
        lp = float(entry["limit_price"])
    except (KeyError, TypeError, ValueError):
        return None
    return lp if lp > 0 else None


def stored_exits(entry: dict) -> tuple[float, float] | None:
    """The (take-profit, stop) values stamped into the row at entry, or None.

    Charter §4 makes the entry-time numbers authoritative: "The supervisor
    enforces the stored numbers and never re-derives them from whatever the
    rules say later." This reader is the whole of that enforcement. A row
    written before the gate stamped exits — every position opened before
    2026-08-27 — reads as None and gets the constant-derived thresholds it has
    always got, so legacy rows behave identically.

    Both values must be present and parse as positive floats. A half-stamped
    row falls back for *both* thresholds rather than pairing one stored value
    with one constant: mixing the two would enforce a band that neither the
    charter nor the entry ever specified.
    """
    found: list[float] = []
    for key in ("exit_tp_value", "exit_stop_value"):
        try:
            value = float(entry[key])
        except (KeyError, TypeError, ValueError):
            return None
        if not (value > 0):  # also rejects NaN
            return None
        found.append(value)
    return found[0], found[1]


def stored_tp(entry: dict) -> float | None:
    """The stamped take-profit alone, for rows that carry no stop by design.

    Vol-pair rows (§4 as amended 2026-08-29) are stamped with a take-profit
    and no exit_stop_value, so stored_exits' both-or-neither rule would send
    them to the constant fallback and quietly resurrect the stop the charter
    removed. This reader exists so that cannot happen.
    """
    try:
        value = float(entry["exit_tp_value"])
    except (KeyError, TypeError, ValueError):
        return None
    return value if value > 0 else None


def _stamped_note(stored: bool, tp: float, stop: float) -> str:
    """Audit suffix naming the stored thresholds, empty on the fallback path.

    Empty when falling back so that a legacy row's decision text is byte-for-
    byte what it was before exits were stamped; a reason line that changed
    without the decision changing would be noise in the audit trail.
    """
    return f", exits stamped at entry tp {tp:.2f} / stop {stop:.2f}" if stored else ""


def _credit_exit(entry: dict, structure: str, legs: list[str],
                 qty_by_symbol: dict[str, float], quotes: dict[str, dict],
                 clock_note: str) -> tuple[str | None, str]:
    """Charter §4's credit rules: stop at 2x the credit, take profit at half.

    Thresholds are the ones stamped at entry when the row carries them, and
    the constants above otherwise. Both are buyback *costs*, compared the same
    way either way: cheap to close is a take-profit, expensive is a stop.
    """
    credit = entry_credit(entry)
    if credit is None or credit <= 0:
        return None, (
            f"structure={structure} but the ledger records no usable entry credit "
            f"(limit_price={entry.get('limit_price')!r}); clock rule only ({clock_note})"
        )

    cost, missing = buyback_cost(legs, qty_by_symbol, quotes)
    if missing:
        return None, (
            f"no usable quote for {', '.join(missing)}; abstaining from the value "
            f"rules this pass ({clock_note})"
        )

    stamped = stored_exits(entry)
    tp, stop = stamped or (TAKE_PROFIT_MULTIPLE * credit, VALUE_STOP_MULTIPLE * credit)

    ratio = cost / credit
    priced = (
        f"buyback {cost:.2f} vs credit {credit:.2f} ({ratio:.2f}x)"
        f"{_stamped_note(stamped is not None, tp, stop)}, {clock_note}"
    )
    if cost >= stop:
        return "VALUE_STOP", f"cost to close reached {ratio:.2f}x the credit; {priced}"
    if cost <= tp:
        return "TAKE_PROFIT", f"{1 - ratio:.0%} of the credit captured; {priced}"
    return None, f"inside the exit band; {priced}"


def _debit_exit(entry: dict, structure: str, legs: list[str],
                qty_by_symbol: dict[str, float], quotes: dict[str, dict],
                clock_note: str) -> tuple[str | None, str]:
    """Charter §4's debit rules: stop at half the debit, take profit at 2x.

    The spread's value is the negation of buyback_cost, computed from the same
    quotes the same way: unwinding a debit vertical pays us, so the cost of
    unwinding it is negative. That keeps one pricing convention for both sides
    of the book — short legs bought back at the ASK, long legs sold at the BID,
    the worst plausible fill. Priced against us like that, the debit take-profit
    triggers late and the debit stop triggers early, which are the safe
    directions to be wrong in on each rule.
    """
    debit = entry_debit(entry)
    if debit is None or debit <= 0:
        return None, (
            f"structure={structure} but the ledger records no usable entry debit "
            f"(limit_price={entry.get('limit_price')!r}); clock rule only ({clock_note})"
        )

    cost, missing = buyback_cost(legs, qty_by_symbol, quotes)
    if missing:
        return None, (
            f"no usable quote for {', '.join(missing)}; abstaining from the value "
            f"rules this pass ({clock_note})"
        )

    value = -cost
    ratio = value / debit

    # Vol-pair rows (§4 as amended 2026-08-29): take-profit and clock only,
    # no value stop. The marker is only ever written by the gate, and the tp
    # is read alone because these rows carry no stop to pair it with.
    if entry.get("vol_pair") is True:
        tp = stored_tp(entry)
        if tp is None:
            return None, (
                f"vol-pair row carries no stored take-profit; clock rule only "
                f"({clock_note})"
            )
        priced = (f"value {value:.2f} vs debit {debit:.2f} ({ratio:.2f}x), "
                  f"vol pair: no value stop, tp stamped at entry {tp:.2f}, {clock_note}")
        if value >= tp:
            return "TAKE_PROFIT", f"spread value reached {ratio:.2f}x the debit; {priced}"
        return None, f"inside the exit band; {priced}"

    stamped = stored_exits(entry)
    tp, stop = stamped or (DEBIT_TAKE_PROFIT_MULTIPLE * debit, DEBIT_STOP_MULTIPLE * debit)
    priced = (
        f"value {value:.2f} vs debit {debit:.2f} ({ratio:.2f}x)"
        f"{_stamped_note(stamped is not None, tp, stop)}, {clock_note}"
    )
    # Stop before take-profit, per the charter's precedence. For a positive
    # debit the two bands cannot overlap, but the order is the charter's and
    # is not this file's to reorder on the grounds that it cannot matter.
    if value <= stop:
        return "VALUE_STOP", f"spread value fell to {ratio:.2f}x the debit; {priced}"
    if value >= tp:
        return "TAKE_PROFIT", f"spread value reached {ratio:.2f}x the debit; {priced}"
    return None, f"inside the exit band; {priced}"


def classify_exit(entry: dict, exchange_now: datetime, qty_by_symbol: dict[str, float],
                  quotes: dict[str, dict]) -> tuple[str | None, str]:
    """Return (rule_fired, reason). rule_fired is None when nothing fires.

    Precedence is fixed by charter §4 and enforced by the order of these
    branches: same-day clock, then value stop, then take profit. The clock is
    settled here, before either value branch is consulted, so it outranks both
    sides of the book; the stop-before-take-profit half of the precedence lives
    inside each branch.
    """
    legs = entry.get("legs") or []
    structure = entry.get("structure")

    # A legless entry prices as a zero-cost unwind, which both value branches
    # would read as a filled take-profit. supervisor.py skips such entries
    # before it ever calls in here, so this guard is unreachable in the live
    # pass — it exists so that the arithmetic cannot recommend closing a
    # position the ledger cannot even name.
    if not legs:
        return None, "ledger entry records no legs; nothing to price and nothing to close"

    expiring = [s for s in legs if expires_today(s, exchange_now)]
    if expiring:
        if past_same_day_cutoff(exchange_now):
            return "CLOCK", (
                f"{len(expiring)} leg(s) expire today and the exchange clock reads "
                f"{exchange_now:%H:%M} ET, past the {SAME_DAY_CLOSE_HHMM[0]}:"
                f"{SAME_DAY_CLOSE_HHMM[1]:02d} backstop cutoff"
            )
        cutoff = f"{SAME_DAY_CLOSE_HHMM[0]}:{SAME_DAY_CLOSE_HHMM[1]:02d}"
        clock_note = f"expires today, clock {exchange_now:%H:%M} ET is before {cutoff}"
    else:
        clock_note = "no leg expires today"

    if structure not in VALUE_MANAGED_STRUCTURES:
        return None, (
            f"structure={structure or 'unrecorded'} is not value-managed; "
            f"clock rule only ({clock_note}). Tactical exits belong to the agent."
        )

    if structure in CREDIT_STRUCTURES:
        return _credit_exit(entry, structure, legs, qty_by_symbol, quotes, clock_note)
    return _debit_exit(entry, structure, legs, qty_by_symbol, quotes, clock_note)


def breach_pct(account: dict) -> float | None:
    """Day P&L as a fraction of yesterday's equity, or None if unreadable."""
    try:
        equity = float(account["equity"])
        last = float(account["last_equity"])
    except (KeyError, TypeError, ValueError):
        return None
    return (equity - last) / last if last > 0 else None



def close_order(legs: list[str], qty_by_symbol: dict[str, float]) -> list[str]:
    """Legs ordered shorts-first.

    Closing the short leg first is the whole discipline: unwinding the long
    side of a spread first leaves a naked short for as long as the second fill
    takes. Sign of the position qty is the source of truth — the ledger does
    not record per-leg sides.
    """
    return sorted(legs, key=lambda s: (qty_by_symbol.get(s, 0.0) >= 0, s))


def long_only_fragment(present: list[str], qty_by_symbol: dict[str, float]) -> bool:
    """True when every remaining open leg of an entry is long (qty > 0).

    An entry in this state is not a spread any more. The shim places spreads
    as one multi-leg order, so a long-only remainder means a shorts-first
    close broke half-way (the 2026-08-28 fill race left two of these).
    Finishing the exit only sells owned contracts; it can never uncover
    anything.
    """
    return bool(present) and all(qty_by_symbol.get(s, 0.0) > 0 for s in present)


def assignment_suspected(present: list[str], qty_by_symbol: dict[str, float]) -> bool:
    """True when a bare stock position exists in a fragment's underlying.

    Early assignment on a short leg turns that leg into stock and leaves the
    long leg as the stock's hedge. Selling the hedge is an owner decision,
    never a backstop's — assignment handling is outside the admitted surface
    by design — so a fragment with stock alongside it is left alone.
    """
    roots = {m.group("root") for s in present if (m := OCC_RE.match(s))}
    return any(r in qty_by_symbol for r in roots)


