"""Unit tests for the defined-risk shim's accept/refuse arithmetic.

Everything under test is a pure function in `defined_risk`: no vendor server,
no MCP session, no network, no filesystem. The refusal *messages* are asserted
as well as the refusals themselves — they are the text that lands on the audit
trail, so a reworded refusal should show up as a failing test, not a surprise
in the demo.

Run: .venv/bin/python -m pytest shim/
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from defined_risk import (
    ZERO_DTE_CUTOFF_LABEL,
    _entry_to_position,
    _leg_sides,
    combined_max_loss,
    entry_qty,
    exit_values,
    max_loss_usd,
    offsetting_refusal,
    open_risk_usd,
    parse_clock_timestamp,
    parse_leg,
    payoff_at_expiry,
    prune_ledger,
    zero_dte_refusal,
)

EXP = "260825"  # the "today" every test dates against
LATER = "260828"


def leg(cp: str, strike: float, side: str, *, expiry: str = EXP, root: str = "SPY", ratio: int = 1):
    """Build a parsed Leg from readable parts (strike in dollars)."""
    return parse_leg(
        {
            "symbol": f"{root}{expiry}{cp}{round(strike * 1000):08d}",
            "side": side,
            "ratio_qty": str(ratio),
        }
    )


def condor(*, put_width=5.0, call_width=5.0, expiry=EXP, ratio=1, root="SPY"):
    """A well-formed iron condor: short 645P/655C, long the wings."""
    return [
        leg("P", 645.0 - put_width, "buy", expiry=expiry, ratio=ratio, root=root),
        leg("P", 645.0, "sell", expiry=expiry, ratio=ratio, root=root),
        leg("C", 655.0, "sell", expiry=expiry, ratio=ratio, root=root),
        leg("C", 655.0 + call_width, "buy", expiry=expiry, ratio=ratio, root=root),
    ]


# --- parse_leg -------------------------------------------------------------


@pytest.mark.parametrize(
    "raw, message",
    [
        ({"symbol": "SPY", "side": "buy"}, "not a valid OCC option symbol"),
        ({"symbol": "spy260825C00650000", "side": "buy"}, "not a valid OCC option symbol"),
        ({"symbol": "SPY260825C0065000", "side": "buy"}, "not a valid OCC option symbol"),
        ({"symbol": "SPY260825X00650000", "side": "buy"}, "not a valid OCC option symbol"),
        ({"symbol": "SPY260825C00650000", "side": "short"}, "must be 'buy' or 'sell'"),
        ({"symbol": "SPY260825C00650000", "side": ""}, "must be 'buy' or 'sell'"),
        (
            {"symbol": "SPY260825C00650000", "side": "buy", "ratio_qty": "0"},
            "ratio_qty 0 must be >= 1",
        ),
    ],
)
def test_parse_leg_rejects(raw, message):
    with pytest.raises(ValueError, match=message):
        parse_leg(raw)


def test_parse_leg_reads_occ_fields():
    parsed = parse_leg({"symbol": "SPY260825P00645500", "side": "sell", "ratio_qty": "2"})
    assert (parsed.root, parsed.expiry, parsed.cp, parsed.strike, parsed.ratio_qty) == (
        "SPY",
        "260825",
        "P",
        645.5,
        2,
    )


# --- max_loss_usd: accepted structures -------------------------------------


@pytest.mark.parametrize(
    "legs, qty, limit_price, expected_loss, expected_structure",
    [
        # single long: max loss is the debit paid, x100 x qty x ratio
        ([leg("C", 650.0, "buy")], 1, 2.50, 250.0, "long_single"),
        ([leg("P", 640.0, "buy")], 3, 1.00, 300.0, "long_single"),
        ([leg("C", 650.0, "buy", ratio=2)], 3, 1.00, 600.0, "long_single"),
        # debit vertical: max loss is the debit, independent of width
        ([leg("C", 650.0, "buy"), leg("C", 655.0, "sell")], 1, 2.00, 200.0, "debit_vertical"),
        ([leg("P", 650.0, "buy"), leg("P", 645.0, "sell")], 4, 1.25, 500.0, "debit_vertical"),
        # credit vertical: max loss is width - credit
        ([leg("P", 645.0, "sell"), leg("P", 640.0, "buy")], 1, -1.50, 350.0, "credit_vertical"),
        ([leg("C", 655.0, "sell"), leg("C", 660.0, "buy")], 2, -1.50, 700.0, "credit_vertical"),
        # credit vertical edge: a one-cent-under-width credit still has risk
        ([leg("P", 645.0, "sell"), leg("P", 640.0, "buy")], 1, -4.99, 1.0, "credit_vertical"),
        # iron condor: max loss is the WIDEST wing - credit, either side only
        (condor(), 1, -2.00, 300.0, "iron_condor"),
        (condor(put_width=10.0, call_width=5.0), 1, -3.00, 700.0, "iron_condor"),
        (condor(put_width=5.0, call_width=10.0), 2, -3.00, 1400.0, "iron_condor"),
        (condor(ratio=2), 1, -2.00, 600.0, "iron_condor"),
        (condor(put_width=5.0, call_width=5.0), 1, -4.99, 1.0, "iron_condor"),
    ],
)
def test_max_loss_accepts(legs, qty, limit_price, expected_loss, expected_structure):
    loss, structure = max_loss_usd(legs, qty, limit_price)
    assert structure == expected_structure
    assert loss == pytest.approx(expected_loss)


# --- max_loss_usd: refused shapes ------------------------------------------


@pytest.mark.parametrize(
    "legs, qty, limit_price, message",
    [
        # single leg
        ([leg("C", 650.0, "sell")], 1, -1.00, "may only be long"),
        ([leg("C", 650.0, "buy")], 1, -1.00, "must be a net debit"),
        ([leg("C", 650.0, "buy")], 1, 0.0, "must be a net debit"),
        # 2-leg verticals
        ([leg("C", 650.0, "buy"), leg("C", 655.0, "buy")], 1, 2.0, "exactly one buy and one sell"),
        (
            [leg("C", 650.0, "sell"), leg("C", 655.0, "sell")],
            1,
            -2.0,
            "exactly one buy and one sell",
        ),
        ([leg("C", 650.0, "buy"), leg("P", 655.0, "sell")], 1, 2.0, "same option type"),
        (
            [leg("C", 650.0, "buy"), leg("C", 655.0, "sell", expiry=LATER)],
            1,
            2.0,
            "share underlying and expiration",
        ),
        (
            [leg("C", 650.0, "buy"), leg("C", 655.0, "sell", root="QQQ")],
            1,
            2.0,
            "share underlying and expiration",
        ),
        (
            [leg("C", 650.0, "buy"), leg("C", 655.0, "sell", ratio=2)],
            1,
            2.0,
            "equal ratio_qty",
        ),
        ([leg("C", 650.0, "buy"), leg("C", 650.0, "sell")], 1, 2.0, "distinct strikes"),
        # credit >= width leaves no defined loss to speak of
        (
            [leg("P", 645.0, "sell"), leg("P", 640.0, "buy")],
            1,
            -5.00,
            "credit exceeds spread width",
        ),
        (
            [leg("P", 645.0, "sell"), leg("P", 640.0, "buy")],
            1,
            -6.00,
            "credit exceeds spread width",
        ),
        # unrecognized leg counts
        ([], 1, 1.0, "not a recognized defined-risk structure"),
        (
            [leg("C", 650.0, "buy"), leg("C", 655.0, "sell"), leg("C", 660.0, "sell")],
            1,
            1.0,
            "not a recognized defined-risk structure",
        ),
        (condor() + [leg("C", 665.0, "buy")], 1, -2.0, "not a recognized defined-risk structure"),
        # iron condor shapes
        (
            condor()[:3] + [leg("C", 660.0, "buy", expiry=LATER)],
            1,
            -2.0,
            "share underlying and expiration",
        ),
        (condor()[:3] + [leg("C", 660.0, "buy", ratio=2)], 1, -2.0, "equal ratio_qty"),
        (
            [
                leg("P", 640.0, "buy"),
                leg("P", 645.0, "sell"),
                leg("P", 650.0, "sell"),
                leg("C", 660.0, "buy"),
            ],
            1,
            -2.0,
            "exactly two puts and two calls",
        ),
        (condor(), 1, 2.00, "must be a net credit"),
        (condor(), 1, 0.0, "must be a net credit"),
        # wings pointing the wrong way: that is two debit spreads, not a condor
        (
            [
                leg("P", 640.0, "sell"),
                leg("P", 645.0, "buy"),
                leg("C", 655.0, "sell"),
                leg("C", 660.0, "buy"),
            ],
            1,
            -2.0,
            "sell the higher-strike put",
        ),
        (
            [
                leg("P", 640.0, "buy"),
                leg("P", 645.0, "sell"),
                leg("C", 655.0, "buy"),
                leg("C", 660.0, "sell"),
            ],
            1,
            -2.0,
            "sell the higher-strike put",
        ),
        (
            [
                leg("P", 640.0, "buy"),
                leg("P", 645.0, "buy"),
                leg("C", 655.0, "sell"),
                leg("C", 660.0, "buy"),
            ],
            1,
            -2.0,
            "P wing must have exactly one buy and one sell",
        ),
        (
            [
                leg("P", 640.0, "buy"),
                leg("P", 645.0, "sell"),
                leg("C", 655.0, "sell"),
                leg("C", 660.0, "sell"),
            ],
            1,
            -2.0,
            "C wing must have exactly one buy and one sell",
        ),
        # credit at or above the widest wing
        (condor(put_width=5.0, call_width=5.0), 1, -5.00, "credit exceeds the widest condor wing"),
        (condor(put_width=10.0, call_width=5.0), 1, -10.00, "credit exceeds the widest condor wing"),
        (condor(put_width=5.0, call_width=10.0), 1, -12.00, "credit exceeds the widest condor wing"),
    ],
)
def test_max_loss_refuses(legs, qty, limit_price, message):
    with pytest.raises(ValueError, match=message):
        max_loss_usd(legs, qty, limit_price)


def test_condor_credit_uses_widest_wing_not_the_narrow_one():
    """A 3.00 credit clears the 5-wide wing but not the 10-wide one; the
    10-wide wing is what can actually lose, so it sets max loss."""
    loss, structure = max_loss_usd(condor(put_width=10.0, call_width=5.0), 1, -3.00)
    assert (structure, loss) == ("iron_condor", 700.0)


# --- exit_values: charter §4 exits, stamped at entry -----------------------
# These are the numbers the supervisor enforces for the life of the position,
# so they are asserted exactly rather than approximately: a formula that drifts
# should fail here, not show up as a position exiting somewhere unexpected.

DEBIT_VERT = [leg("C", 650.0, "buy"), leg("C", 655.0, "sell")]  # 5 wide
WIDE_DEBIT_VERT = [leg("C", 650.0, "buy"), leg("C", 660.0, "sell")]  # 10 wide
CREDIT_VERT = [leg("P", 645.0, "sell"), leg("P", 640.0, "buy")]  # 5 wide


@pytest.mark.parametrize(
    "legs, structure, limit_price, expected",
    [
        # Debit verticals: TP is half of MAXIMUM PROFIT, i.e. debit plus half
        # of (width - debit) — not a multiple of the debit. Stop is half the
        # debit paid.
        pytest.param(DEBIT_VERT, "debit_vertical", 2.00,
                     {"exit_tp_value": 3.50, "exit_stop_value": 1.00}, id="debit-2.00-on-5-wide"),
        pytest.param(DEBIT_VERT, "debit_vertical", 1.25,
                     {"exit_tp_value": 3.125, "exit_stop_value": 0.625}, id="debit-1.25-on-5-wide"),
        pytest.param(WIDE_DEBIT_VERT, "debit_vertical", 4.00,
                     {"exit_tp_value": 7.00, "exit_stop_value": 2.00}, id="debit-4.00-on-10-wide"),
        # A cheap wing: the old 2x rule would have targeted 0.10, a dime above
        # entry on a 5-wide spread. Half of max profit targets 2.55.
        pytest.param(DEBIT_VERT, "debit_vertical", 0.05,
                     {"exit_tp_value": 2.525, "exit_stop_value": 0.025}, id="debit-cheap-wing"),
        # Credit structures: buyback-COST thresholds. Half the credit is the
        # take-profit, twice the credit the stop; width does not enter.
        pytest.param(CREDIT_VERT, "credit_vertical", -1.50,
                     {"exit_tp_value": 0.75, "exit_stop_value": 3.00}, id="credit-vertical"),
        pytest.param(condor(), "iron_condor", -2.00,
                     {"exit_tp_value": 1.00, "exit_stop_value": 4.00}, id="iron-condor"),
        pytest.param(condor(put_width=10.0, call_width=5.0), "iron_condor", -3.00,
                     {"exit_tp_value": 1.50, "exit_stop_value": 6.00},
                     id="iron-condor-width-does-not-enter"),
        # long_single is not value-managed (rules.VALUE_MANAGED_STRUCTURES);
        # stamping exits on one would legislate that ruling away by accident.
        pytest.param([leg("C", 650.0, "buy")], "long_single", 2.50, {}, id="long-single-no-exits"),
    ],
)
def test_exit_values(legs, structure, limit_price, expected):
    assert exit_values(legs, structure, limit_price) == expected


@pytest.mark.parametrize(
    "legs, structure, limit_price",
    [
        # A debit at or above the width cannot profit; stamping a take-profit
        # at or below entry would be worse than stamping nothing.
        pytest.param(DEBIT_VERT, "debit_vertical", 5.00, id="debit-equals-width"),
        pytest.param(DEBIT_VERT, "debit_vertical", 6.00, id="debit-exceeds-width"),
        # Wrong-signed limit prices for the structure named.
        pytest.param(DEBIT_VERT, "debit_vertical", -2.00, id="debit-vertical-with-a-credit"),
        pytest.param(CREDIT_VERT, "credit_vertical", 1.50, id="credit-vertical-with-a-debit"),
        pytest.param(condor(), "iron_condor", 2.00, id="condor-with-a-debit"),
        pytest.param(DEBIT_VERT, "debit_vertical", 0.0, id="zero"),
        # Shapes that are not verticals, and names the gate never produces.
        pytest.param([leg("C", 650.0, "buy")], "debit_vertical", 2.00, id="one-leg-called-vertical"),
        pytest.param(condor(), "debit_vertical", 2.00, id="four-legs-called-vertical"),
        pytest.param(DEBIT_VERT, "unrecognized_structure", 2.00, id="unknown-structure"),
        pytest.param(DEBIT_VERT, "", 2.00, id="empty-structure"),
    ],
)
def test_exit_values_stamps_nothing_rather_than_guessing(legs, structure, limit_price):
    """Charter §4 exits are stamped after the vendor has accepted the order, so
    this function must never raise: an exception here would place a position
    and then fail to record it, blinding the book cap. Anything it cannot
    compute honestly comes back empty, and the supervisor prices that row with
    its own constants exactly as it did before exits were stamped."""
    assert exit_values(legs, structure, limit_price) == {}


@pytest.mark.parametrize(
    "legs, structure, limit_price, expected",
    [
        # Vol-pair leg (§4 as amended 2026-08-29): the same take-profit
        # anchor, and no stop key at all.
        pytest.param(DEBIT_VERT, "debit_vertical", 2.00,
                     {"exit_tp_value": 3.50}, id="vol-pair-debit"),
        # The flag governs debit verticals only; the shim refuses it on any
        # other structure before this function runs, and here it never
        # manufactures or removes keys a structure would not otherwise get.
        pytest.param(CREDIT_VERT, "credit_vertical", -1.50,
                     {"exit_tp_value": 0.75, "exit_stop_value": 3.00},
                     id="flag-inert-on-credit"),
        pytest.param([leg("C", 650.0, "buy")], "long_single", 2.50, {},
                     id="flag-inert-on-long-single"),
        pytest.param(DEBIT_VERT, "debit_vertical", 6.00, {},
                     id="uncomputable-still-stamps-nothing"),
    ],
)
def test_exit_values_vol_pair(legs, structure, limit_price, expected):
    assert exit_values(legs, structure, limit_price, vol_pair=True) == expected


def test_debit_take_profit_is_reachable_even_when_the_debit_exceeds_half_the_width():
    """The defect that re-anchored charter §4 the evening of 2026-08-27.

    Under the old take-profit at 2x the debit, a spread whose debit exceeded
    half its width could never take profit: twice the debit sat above the
    spread's own maximum value, so the rule was unreachable by construction.
    Half of maximum profit is always strictly inside the (debit, width) band.
    """
    width, debit = 5.0, 3.00
    assert 2.0 * debit > width  # the old target was above the spread's ceiling
    values = exit_values(DEBIT_VERT, "debit_vertical", debit)
    assert debit < values["exit_tp_value"] < width


def test_exit_values_pair_with_the_structure_max_loss_names():
    """max_loss_usd names the structure and exit_values keys off that name, so
    a structure renamed on one side and not the other would silently stop
    stamping exits. This pins them together."""
    for legs, limit_price, wants_exits in [
        (DEBIT_VERT, 2.00, True),
        (CREDIT_VERT, -1.50, True),
        (condor(), -2.00, True),
        ([leg("C", 650.0, "buy")], 2.50, False),
    ]:
        _, structure = max_loss_usd(legs, 1, limit_price)
        assert bool(exit_values(legs, structure, limit_price)) is wants_exits


# --- open-risk ledger ------------------------------------------------------

LEDGER = [
    {"order_id": "o-filled", "legs": ["SPY260825P00645000", "SPY260825P00640000"],
     "max_loss_usd": 350.0},
    {"order_id": "o-resting", "legs": ["SPY260828C00660000"], "max_loss_usd": 500.0},
    {"order_id": "o-gone", "legs": ["SPY260820C00600000"], "max_loss_usd": 700.0},
    {"order_id": None, "legs": ["SPY260819C00600000"], "max_loss_usd": 900.0},
]


@pytest.mark.parametrize(
    "positions, open_ids, expected_ids, expected_risk",
    [
        # nothing live: the whole book prunes away
        (set(), set(), [], 0.0),
        # a leg still held keeps its entry alive
        ({"SPY260825P00645000"}, set(), ["o-filled"], 350.0),
        # the *other* leg of the same entry counts too
        ({"SPY260825P00640000"}, set(), ["o-filled"], 350.0),
        # a resting order keeps its entry alive with no position yet
        (set(), {"o-resting"}, ["o-resting"], 500.0),
        # position and order together, in ledger order
        ({"SPY260825P00645000"}, {"o-resting"}, ["o-filled", "o-resting"], 850.0),
        # an unrelated position/order does not resurrect anything
        ({"AAPL260825C00200000"}, {"o-someone-else"}, [], 0.0),
        # an entry whose order id never came back is live only via its legs
        ({"SPY260819C00600000"}, set(), [None], 900.0),
    ],
)
def test_prune_ledger(positions, open_ids, expected_ids, expected_risk):
    live = prune_ledger(LEDGER, positions, open_ids)
    assert [e["order_id"] for e in live] == expected_ids
    assert open_risk_usd(live) == pytest.approx(expected_risk)


@pytest.mark.parametrize(
    "entry, positions, open_ids, live",
    [
        # ids compare as strings: the vendor may hand back a number
        ({"order_id": 12345, "legs": []}, set(), {"12345"}, True),
        ({"order_id": 12345, "legs": []}, set(), {"999"}, False),
        # a missing legs key is not an error, just no position evidence
        ({"order_id": "o1"}, set(), {"o1"}, True),
        ({"order_id": "o1"}, set(), set(), False),
        ({"legs": ["SPY260825C00650000"]}, {"SPY260825C00650000"}, set(), True),
    ],
)
def test_prune_ledger_entry_liveness(entry, positions, open_ids, live):
    assert prune_ledger([entry], positions, open_ids) == ([entry] if live else [])


@pytest.mark.parametrize(
    "entries, expected",
    [
        ([], 0.0),
        ([{"max_loss_usd": 350.0}, {"max_loss_usd": 500}], 850.0),
        ([{"max_loss_usd": "350.5"}], 350.5),  # JSON round-trips are forgiving
    ],
)
def test_open_risk_usd(entries, expected):
    assert open_risk_usd(entries) == pytest.approx(expected)


@pytest.mark.parametrize("bad", [{"max_loss_usd": "lots"}, {"max_loss_usd": None}])
def test_open_risk_usd_refuses_unusable_rows(bad):
    """A row we cannot price must not silently read as zero risk."""
    with pytest.raises(ValueError, match="unusable max_loss_usd"):
        open_risk_usd([bad])


def test_open_risk_usd_treats_missing_field_as_zero():
    assert open_risk_usd([{"order_id": "o1"}]) == 0.0


# --- 0DTE clock cutoff -----------------------------------------------------

TODAY_LEG = leg("C", 650.0, "buy", expiry=EXP)
LATER_LEG = leg("C", 650.0, "buy", expiry=LATER)


def et(hhmmss: str) -> datetime:
    """Exchange-local (ET) wall clock on 2026-08-25, the EXP expiry date."""
    return datetime.fromisoformat(f"2026-08-25T{hhmmss}-04:00")


@pytest.mark.parametrize(
    "now, legs, refused",
    [
        (et("09:30:00"), [TODAY_LEG], False),
        (et("15:14:59"), [TODAY_LEG], False),  # one second inside the window
        (et("15:15:00"), [TODAY_LEG], True),   # cutoff is inclusive
        (et("15:15:30"), [TODAY_LEG], True),
        (et("16:30:00"), [TODAY_LEG], True),   # after the close, still refused
        (et("15:30:00"), [LATER_LEG], False),  # nothing expiring today
        (et("15:30:00"), [LATER_LEG, TODAY_LEG], True),  # one 0DTE leg is enough
        (et("09:30:00"), [LATER_LEG, TODAY_LEG], False),
        (et("15:30:00"), [], False),
    ],
)
def test_zero_dte_refusal(now, legs, refused):
    result = zero_dte_refusal(now, legs)
    assert (result is not None) == refused
    if refused:
        assert ZERO_DTE_CUTOFF_LABEL in result
        assert TODAY_LEG.symbol in result
        assert LATER_LEG.symbol not in result.split("expire today")[0]


def test_zero_dte_uses_the_exchange_offset_not_utc():
    """15:20 ET is 19:20 UTC; reading the clock as UTC would let a 0DTE
    opener through. The offset in the vendor timestamp is what decides."""
    assert zero_dte_refusal(et("15:20:00"), [TODAY_LEG]) is not None
    assert zero_dte_refusal(et("13:20:00"), [TODAY_LEG]) is None


@pytest.mark.parametrize(
    "clock, expected",
    [
        ({"timestamp": "2026-08-25T07:24:25.9-04:00"}, et("07:24:25.9")),
        ({"timestamp": "2026-08-25T15:15:00-04:00"}, et("15:15:00")),
    ],
)
def test_parse_clock_timestamp(clock, expected):
    assert parse_clock_timestamp(clock) == expected


@pytest.mark.parametrize("clock", [{}, {"timestamp": None}, {"timestamp": 1755000000}])
def test_parse_clock_timestamp_refuses_unusable_clock(clock):
    with pytest.raises(ValueError, match="carried no timestamp"):
        parse_clock_timestamp(clock)


# ---------------------------------------------------------------------------
# Signed caps: the envelope block is the only source (2026-08-26 re-key design)
# ---------------------------------------------------------------------------

from defined_risk import CapsError, caps_from_manifest


def envelope_manifest(caps: dict | None) -> dict:
    """The smallest manifest shape caps_from_manifest accepts."""
    envelope: dict = {"polarity": "abstain"}
    if caps is not None:
        envelope["caps"] = caps
    return {"envelope": envelope}


GOOD_CAPS = {
    "actions_per_utc_day": 40,
    "max_loss_per_position_usd": 5000,
    "max_total_open_risk_usd": 30000,
}


def test_caps_load_from_envelope_and_carry_its_hash():
    caps = caps_from_manifest(envelope_manifest(GOOD_CAPS))
    assert caps.max_loss_per_position_usd == 5000.0
    assert caps.max_total_open_risk_usd == 30000.0
    assert caps.envelope_hash.startswith("sha256:")


def test_caps_hash_changes_when_a_cap_changes():
    """The property the whole design rests on: a different cap is a different
    envelope hash, which is what quarantines the grants."""
    a = caps_from_manifest(envelope_manifest(GOOD_CAPS))
    b = caps_from_manifest(envelope_manifest({**GOOD_CAPS, "max_total_open_risk_usd": 30001}))
    assert a.envelope_hash != b.envelope_hash


@pytest.mark.parametrize(
    "manifest, complaint",
    [
        ({}, "no envelope block"),
        ({"envelope": None}, "no envelope block"),
        ({"envelope": {"caps": GOOD_CAPS}}, "schema validation"),  # no polarity
        (envelope_manifest(None), "max_loss_per_position_usd"),
        (envelope_manifest({"actions_per_utc_day": 40}), "max_loss_per_position_usd"),
        (
            envelope_manifest({**GOOD_CAPS, "max_loss_per_position_usd": 0}),
            "max_loss_per_position_usd",
        ),
        (
            envelope_manifest({**GOOD_CAPS, "max_loss_per_position_usd": "5000"}),
            "max_loss_per_position_usd",
        ),
        (
            envelope_manifest({**GOOD_CAPS, "max_total_open_risk_usd": -1}),
            "max_total_open_risk_usd",
        ),
        (
            envelope_manifest({**GOOD_CAPS, "max_loss_per_position_usd": 50000}),
            "never be the whole book",
        ),
    ],
)
def test_caps_refuse_rather_than_default(manifest, complaint):
    with pytest.raises(CapsError, match=complaint):
        caps_from_manifest(manifest)


# --- cross-position netting (charter §2, 2026-08-31 evening) -----------------
#
# The fixtures below are the real 2026-08-31 SPY book and the offsetting condor
# a rehearsal priced against it. That trade would have collected $1,520 and
# recorded $2,480 of new risk while REDUCING the book's true worst case by $520.

def _leg(sym, side="buy"):
    """Ledger rows store no side, so reconstruction infers it; but legs handed to
    max_loss_usd are a real order and must carry their true sides."""
    return parse_leg({"symbol": sym, "side": side, "ratio_qty": "1"})


SPY_BOOK = [
    {"legs": ["SPY260904C00768000", "SPY260904C00773000"], "structure": "debit_vertical",
     "limit_price": "1.86", "max_loss_usd": 1116.0},
    {"legs": ["SPY260904P00758000", "SPY260904P00763000"], "structure": "debit_vertical",
     "limit_price": "0.95", "max_loss_usd": 570.0},
]
CONDOR_LEGS = [_leg("SPY260904C00772000", "sell"), _leg("SPY260904C00777000", "buy"),
               _leg("SPY260904P00762000", "sell"), _leg("SPY260904P00757000", "buy")]


@pytest.mark.parametrize(
    "structure, syms, expect",
    [
        pytest.param("debit_vertical", ["SPY260904C00768000", "SPY260904C00773000"],
                     [1, -1], id="debit-call-long-lower"),
        pytest.param("debit_vertical", ["SPY260904C00773000", "SPY260904C00768000"],
                     [-1, 1], id="debit-call-order-independent"),
        pytest.param("debit_vertical", ["SPY260904P00758000", "SPY260904P00763000"],
                     [-1, 1], id="debit-put-long-higher"),
        pytest.param("credit_vertical", ["SPY260904C00772000", "SPY260904C00777000"],
                     [-1, 1], id="credit-call-short-lower"),
        pytest.param("credit_vertical", ["SPY260904P00757000", "SPY260904P00762000"],
                     [1, -1], id="credit-put-short-higher"),
        pytest.param("long_single", ["SPY260904C00768000"], [1], id="long-single"),
        pytest.param("debit_vertical", ["SPY260904C00768000", "SPY260904P00773000"],
                     None, id="mixed-rights-unmodelable"),
        pytest.param("bogus", ["SPY260904C00768000", "SPY260904C00773000"],
                     None, id="unknown-structure-unmodelable"),
    ],
)
def test_leg_sides(structure, syms, expect):
    assert _leg_sides([_leg(s) for s in syms], structure, 1.0) == expect


@pytest.mark.parametrize(
    "structure, syms, limit, max_loss, expect",
    [
        pytest.param("debit_vertical", ["SPY260904C00768000", "SPY260904C00773000"],
                     1.86, 1116.0, 6, id="debit-six-lots"),
        pytest.param("debit_vertical", ["SPY260904P00758000", "SPY260904P00763000"],
                     0.95, 570.0, 6, id="debit-put-six-lots"),
        pytest.param("credit_vertical", ["SPY260904C00772000", "SPY260904C00777000"],
                     -1.00, 2400.0, 6, id="credit-six-lots"),
        pytest.param("debit_vertical", ["SPY260904C00768000", "SPY260904C00773000"],
                     0.0, 1116.0, None, id="zero-limit-unrecoverable"),
    ],
)
def test_entry_qty(structure, syms, limit, max_loss, expect):
    assert entry_qty([_leg(s) for s in syms], structure, limit, max_loss) == expect


@pytest.mark.parametrize(
    "spot, expect",
    [
        pytest.param(700.0, -1116.0, id="far-below-loses-debit"),
        pytest.param(768.0, -1116.0, id="at-long-strike-loses-debit"),
        pytest.param(773.0, 1884.0, id="at-short-strike-max-gain"),
        pytest.param(900.0, 1884.0, id="far-above-capped"),
    ],
)
def test_payoff_at_expiry_debit_call_vertical(spot, expect):
    legs = [_leg("SPY260904C00768000"), _leg("SPY260904C00773000")]
    got = payoff_at_expiry(legs, "debit_vertical", 1.86, 6, spot)
    assert got == pytest.approx(expect)


def test_combined_max_loss_independent_positions_sum():
    """A volatility pair genuinely can lose both debits, so netting changes nothing."""
    positions = [_entry_to_position(e) for e in SPY_BOOK]
    assert all(p is not None for p in positions)
    assert combined_max_loss(positions) == pytest.approx(1686.0)


def test_offsetting_condor_is_refused():
    loss, structure = max_loss_usd(CONDOR_LEGS, 8, -1.90)
    assert structure == "iron_condor"
    reason = offsetting_refusal(SPY_BOOK, CONDOR_LEGS, structure, -1.90, 8, loss)
    assert reason is not None
    assert "offsetting refusal" in reason
    assert "unwind rather than an open" in reason


def test_independent_position_is_allowed():
    legs = [_leg("SPY260904C00790000", "buy"), _leg("SPY260904C00795000", "sell")]
    loss, structure = max_loss_usd(legs, 5, 1.20)
    assert offsetting_refusal(SPY_BOOK, legs, structure, 1.20, 5, loss) is None


def test_empty_book_allows_anything():
    legs = [_leg("SPY260904C00790000", "buy"), _leg("SPY260904C00795000", "sell")]
    loss, structure = max_loss_usd(legs, 5, 1.20)
    assert offsetting_refusal([], legs, structure, 1.20, 5, loss) is None


def test_other_underlying_does_not_net():
    """QQQ positions must not net against a SPY proposal."""
    qqq = [{"legs": ["QQQ260904C00717000", "QQQ260904C00722000"],
            "structure": "debit_vertical", "limit_price": "2.48", "max_loss_usd": 992.0}]
    loss, structure = max_loss_usd(CONDOR_LEGS, 8, -1.90)
    assert offsetting_refusal(qqq, CONDOR_LEGS, structure, -1.90, 8, loss) is None


def test_unmodelable_neighbour_skips_the_check_rather_than_guessing():
    """Fails toward allowing: a false refusal stops legitimate trading, and the
    charter rule still binds the agent."""
    broken = [{"legs": ["SPY260904C00768000"], "structure": "mystery",
               "limit_price": "1.86", "max_loss_usd": 1116.0}]
    loss, structure = max_loss_usd(CONDOR_LEGS, 8, -1.90)
    assert offsetting_refusal(broken, CONDOR_LEGS, structure, -1.90, 8, loss) is None
