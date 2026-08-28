"""Unit tests for the supervisor's exit-rule arithmetic.

Everything under test is a pure function in `rules`: no gateway, no MCP
session, no clock of its own, no filesystem. That is the point of the
rules.py/supervisor.py split, and it is what lets the charter's exits (§4) be
checked without sending an order.

The *reasons* are asserted alongside the rules. Every decision this file makes,
including every no-action, lands on the supervisor's decision log as the record
of why a position was closed or held, so a reworded reason should surface here
rather than in an audit.

Run: .venv/bin/python -m pytest supervisor/
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rules import (
    CREDIT_STRUCTURES,
    DEBIT_STRUCTURES,
    VALUE_MANAGED_STRUCTURES,
    breach_pct,
    classify_exit,
    close_order,
    entry_credit,
    entry_debit,
    stored_exits,
)

TODAY = "260827"  # the expiry every "expires today" test dates against
TOMORROW = "260828"

# parse_clock_timestamp hands the supervisor an OFFSET-AWARE exchange-local
# datetime (fromisoformat over the vendor's "...-04:00"), so the clock rule is
# exercised here with the same kind of value it sees in production.
ET = timezone(timedelta(hours=-4))
BEFORE_CUTOFF = datetime(2026, 8, 27, 11, 0, tzinfo=ET)  # hours of room left
AT_CUTOFF = datetime(2026, 8, 27, 15, 20, tzinfo=ET)  # exactly the backstop cutoff
PAST_CUTOFF = datetime(2026, 8, 27, 15, 45, tzinfo=ET)
JUST_BEFORE_CUTOFF = datetime(2026, 8, 27, 15, 19, tzinfo=ET)


def occ(cp: str, strike: float, expiry: str = TODAY, root: str = "SPY") -> str:
    return f"{root}{expiry}{cp}{round(strike * 1000):08d}"


@dataclass
class Book:
    """One ledger entry plus the position/quote state the supervisor reads."""

    entry: dict
    qty: dict[str, float]
    quotes: dict[str, dict] = field(default_factory=dict)
    short_leg: str = ""
    long_leg: str = ""

    def classify(self, now: datetime = BEFORE_CUTOFF) -> tuple[str | None, str]:
        return classify_exit(self.entry, now, self.qty, self.quotes)


def _book(short_leg: str, long_leg: str, structure: str, limit_price,
          short_ask: float | None, long_bid: float | None) -> Book:
    """Assemble a two-leg book. Only the short ASK and long BID drive the rules.

    The other side of each quote is filled in a nickel away so the rows look
    like real quotes and so a rule that reached for the wrong side of the
    market would read a visibly different number.
    """
    quotes: dict[str, dict] = {}
    if short_ask is not None:
        quotes[short_leg] = {"bp": round(max(short_ask - 0.05, 0.01), 4), "ap": short_ask}
    if long_bid is not None:
        quotes[long_leg] = {"bp": long_bid, "ap": round(long_bid + 0.05, 4)}
    entry = {
        "client_order_id": f"t-{structure}",
        "legs": [short_leg, long_leg],
        "structure": structure,
        "limit_price": limit_price,
    }
    return Book(
        entry=entry,
        qty={short_leg: -1.0, long_leg: 1.0},
        quotes=quotes,
        short_leg=short_leg,
        long_leg=long_leg,
    )


def credit_book(*, short_ask: float | None = 1.00, long_bid: float | None = 0.40,
                expiry: str = TODAY, limit_price="-1.00",
                structure: str = "credit_vertical") -> Book:
    """Short the 645 call, long the 650 wing: buyback = short ASK - long BID."""
    return _book(occ("C", 645.0, expiry), occ("C", 650.0, expiry),
                 structure, limit_price, short_ask, long_bid)


def debit_book(*, long_bid: float | None = 2.00, short_ask: float | None = 1.00,
               expiry: str = TODAY, limit_price="1.00",
               structure: str = "debit_vertical") -> Book:
    """Long the 790 call, short the 795: value = long BID - short ASK.

    Same leg roles as the live ledger's `hack-bookcap-probe-1` row, which is a
    debit vertical whose limit_price arrives as the string "0.05".
    """
    return _book(occ("C", 795.0, expiry), occ("C", 790.0, expiry),
                 structure, limit_price, short_ask, long_bid)


# --- structure sets --------------------------------------------------------


def test_value_managed_is_exactly_credit_plus_debit():
    assert VALUE_MANAGED_STRUCTURES == CREDIT_STRUCTURES | DEBIT_STRUCTURES
    assert CREDIT_STRUCTURES.isdisjoint(DEBIT_STRUCTURES)


def test_long_single_is_not_value_managed():
    """Charter §4's debit rule speaks of verticals; a naked long stays the
    agent's to exit. If that ruling is ever revisited, this is the test to
    change deliberately rather than discover."""
    assert "long_single" not in VALUE_MANAGED_STRUCTURES


# --- entry_credit / entry_debit --------------------------------------------


@pytest.mark.parametrize(
    "limit_price, credit, debit",
    [
        pytest.param("-1.00", 1.00, None, id="string-credit"),
        pytest.param(-1.25, 1.25, None, id="float-credit"),
        pytest.param("0.05", None, 0.05, id="string-debit-live-ledger-row"),
        pytest.param(2.5, None, 2.5, id="float-debit"),
        pytest.param("0", None, None, id="zero"),
        pytest.param(0.0, None, None, id="zero-float"),
        pytest.param(None, None, None, id="null"),
        pytest.param("", None, None, id="empty-string"),
        pytest.param("not-a-price", None, None, id="unparseable"),
        pytest.param([], None, None, id="wrong-type"),
    ],
)
def test_entry_price_readers(limit_price, credit, debit):
    entry = {"limit_price": limit_price}
    assert entry_credit(entry) == credit
    assert entry_debit(entry) == debit


def test_entry_price_readers_without_the_field():
    assert entry_credit({}) is None
    assert entry_debit({}) is None


# --- credit structures: the pre-existing behavior, pinned ------------------


@pytest.mark.parametrize(
    "short_ask, long_bid, rule, fragment",
    [
        # credit = 1.00; buyback = short ASK - long BID.
        pytest.param(1.50, 0.50, None, "inside the exit band", id="mid-band"),
        pytest.param(1.00, 0.50, "TAKE_PROFIT", "50% of the credit captured",
                     id="take-profit-exactly-half"),
        pytest.param(0.60, 0.20, "TAKE_PROFIT", "60% of the credit captured",
                     id="take-profit-past-half"),
        pytest.param(2.50, 0.50, "VALUE_STOP", "reached 2.00x the credit",
                     id="value-stop-exactly-2x"),
        pytest.param(3.00, 0.50, "VALUE_STOP", "reached 2.50x the credit",
                     id="value-stop-past-2x"),
        pytest.param(1.05, 0.50, None, "inside the exit band",
                     id="just-inside-take-profit"),
        pytest.param(2.45, 0.50, None, "inside the exit band",
                     id="just-inside-value-stop"),
    ],
)
def test_credit_vertical_bands(short_ask, long_bid, rule, fragment):
    got, reason = credit_book(short_ask=short_ask, long_bid=long_bid).classify()
    assert got == rule
    assert fragment in reason
    assert "credit 1.00" in reason


@pytest.mark.parametrize("structure", sorted(CREDIT_STRUCTURES))
def test_every_credit_structure_reaches_the_value_rules(structure):
    """Set membership, not shape: the arithmetic is leg-count agnostic, so a
    two-leg stand-in exercises the condor's routing as well as the vertical's."""
    got, reason = credit_book(short_ask=3.00, long_bid=0.50, structure=structure).classify()
    assert got == "VALUE_STOP"
    assert "credit 1.00" in reason


# --- debit verticals: charter §4, amended 2026-08-27 -----------------------


@pytest.mark.parametrize(
    "long_bid, short_ask, rule, fragment",
    [
        # debit = 1.00; value = long BID - short ASK.
        pytest.param(2.00, 1.00, None, "inside the exit band", id="mid-band"),
        pytest.param(3.00, 1.00, "TAKE_PROFIT", "reached 2.00x the debit",
                     id="take-profit-exactly-2x"),
        pytest.param(3.50, 1.00, "TAKE_PROFIT", "reached 2.50x the debit",
                     id="take-profit-past-2x"),
        pytest.param(1.50, 1.00, "VALUE_STOP", "fell to 0.50x the debit",
                     id="value-stop-exactly-half"),
        pytest.param(0.60, 0.50, "VALUE_STOP", "fell to 0.10x the debit",
                     id="value-stop-past-half"),
        pytest.param(1.00, 2.00, "VALUE_STOP", "fell to -1.00x the debit",
                     id="value-stop-spread-worth-less-than-nothing"),
        pytest.param(2.95, 1.00, None, "inside the exit band",
                     id="just-inside-take-profit"),
        pytest.param(1.55, 1.00, None, "inside the exit band",
                     id="just-inside-value-stop"),
    ],
)
def test_debit_vertical_bands(long_bid, short_ask, rule, fragment):
    got, reason = debit_book(long_bid=long_bid, short_ask=short_ask).classify()
    assert got == rule
    assert fragment in reason
    assert "debit 1.00" in reason


@pytest.mark.parametrize(
    "limit_price, long_bid, short_ask, rule",
    [
        # The live ledger row: 5c debit, so 10c is the target and 2.5c the stop.
        pytest.param("0.05", 0.20, 0.02, "TAKE_PROFIT", id="string-debit-take-profit"),
        pytest.param("0.05", 0.03, 0.01, "VALUE_STOP", id="string-debit-value-stop"),
        pytest.param("0.05", 0.09, 0.02, None, id="string-debit-inside-band"),
        pytest.param(0.05, 0.20, 0.02, "TAKE_PROFIT", id="float-debit-take-profit"),
    ],
)
def test_debit_limit_price_arrives_as_a_string(limit_price, long_bid, short_ask, rule):
    got, _ = debit_book(limit_price=limit_price, long_bid=long_bid,
                        short_ask=short_ask).classify()
    assert got == rule


def test_debit_value_is_priced_against_us():
    """The long leg sells at the BID and the short buys back at the ASK.

    This book quotes 1.00/1.05 on the long and 0.01/0.05 on the short against
    a 0.50 debit. Taking the favorable side of each (sell the long at 1.05, buy
    the short back at 0.01) values it at 1.04 and trips the take-profit; priced
    against us it is worth 0.95 and does not.
    """
    got, reason = debit_book(limit_price="0.50", long_bid=1.00, short_ask=0.05).classify()
    assert got is None
    assert "value 0.95" in reason
    assert "inside the exit band" in reason


# --- exits stored at entry: charter §4, made structural 2026-08-27 ---------
# "The supervisor enforces the stored numbers and never re-derives them from
# whatever the rules say later." Every test below is written so the stored
# thresholds and the constant-derived ones disagree, because a test where they
# agree cannot tell which one fired.


def stamp(book: Book, **fields) -> Book:
    """Write exit fields onto a book's ledger row, as the shim's gate does."""
    book.entry.update(fields)
    return book


@pytest.mark.parametrize(
    "fields, expected",
    [
        pytest.param({"exit_tp_value": 3.50, "exit_stop_value": 1.00}, (3.50, 1.00), id="floats"),
        pytest.param({"exit_tp_value": "3.50", "exit_stop_value": "1.00"}, (3.50, 1.00),
                     id="strings-as-the-ledger-writes-them"),
        pytest.param({"exit_tp_value": 3, "exit_stop_value": 1}, (3.0, 1.0), id="ints"),
        # Every way a row can fail to carry a usable pair reads as "no stored
        # exits" and takes the constants, never a half-stored band.
        pytest.param({}, None, id="legacy-row-no-fields"),
        pytest.param({"exit_tp_value": 3.50}, None, id="take-profit-only"),
        pytest.param({"exit_stop_value": 1.00}, None, id="stop-only"),
        pytest.param({"exit_tp_value": 3.50, "exit_stop_value": 0.0}, None, id="zero-stop"),
        pytest.param({"exit_tp_value": 0.0, "exit_stop_value": 1.00}, None, id="zero-take-profit"),
        pytest.param({"exit_tp_value": -3.50, "exit_stop_value": 1.00}, None, id="negative"),
        pytest.param({"exit_tp_value": None, "exit_stop_value": 1.00}, None, id="null"),
        pytest.param({"exit_tp_value": "junk", "exit_stop_value": "1.00"}, None, id="unparseable"),
        pytest.param({"exit_tp_value": "", "exit_stop_value": "1.00"}, None, id="empty-string"),
        pytest.param({"exit_tp_value": [], "exit_stop_value": 1.00}, None, id="wrong-type"),
        pytest.param({"exit_tp_value": "nan", "exit_stop_value": 1.00}, None, id="nan"),
    ],
)
def test_stored_exits_reader(fields, expected):
    assert stored_exits(dict(fields)) == expected


@pytest.mark.parametrize(
    "long_bid, short_ask, rule",
    [
        # Stored tp 1.75 / stop 0.30 against constants that would say 2.00/0.50.
        # value 1.80: over the stored target, under the constant one.
        pytest.param(2.80, 1.00, "TAKE_PROFIT", id="stored-target-fires-where-constant-would-not"),
        # value 0.40: above the stored stop, below the constant one.
        pytest.param(1.40, 1.00, None, id="stored-stop-holds-where-constant-would-fire"),
        pytest.param(1.25, 1.00, "VALUE_STOP", id="stored-stop-fires"),
        pytest.param(2.70, 1.00, None, id="inside-the-stored-band"),
    ],
)
def test_debit_branch_prefers_the_stored_values(long_bid, short_ask, rule):
    book = stamp(debit_book(long_bid=long_bid, short_ask=short_ask),
                 exit_tp_value=1.75, exit_stop_value=0.30)
    got, reason = book.classify()
    assert got == rule
    assert "exits stamped at entry tp 1.75 / stop 0.30" in reason


@pytest.mark.parametrize(
    "short_ask, long_bid, rule",
    [
        # Stored tp 0.70 / stop 1.50 against constants that would say 0.50/2.00.
        # Both are buyback costs: cheap is a take-profit, expensive is a stop.
        pytest.param(1.10, 0.50, "TAKE_PROFIT", id="stored-target-fires-where-constant-would-not"),
        pytest.param(2.10, 0.50, "VALUE_STOP", id="stored-stop-fires-where-constant-would-not"),
        pytest.param(1.40, 0.50, None, id="inside-the-stored-band"),
    ],
)
def test_credit_branch_prefers_the_stored_values(short_ask, long_bid, rule):
    book = stamp(credit_book(short_ask=short_ask, long_bid=long_bid),
                 exit_tp_value=0.70, exit_stop_value=1.50)
    got, reason = book.classify()
    assert got == rule
    assert "exits stamped at entry tp 0.70 / stop 1.50" in reason


@pytest.mark.parametrize("book_factory, long_kw, short_kw",
                         [pytest.param(credit_book, "long_bid", "short_ask", id="credit"),
                          pytest.param(debit_book, "long_bid", "short_ask", id="debit")])
@pytest.mark.parametrize(
    "fields",
    [
        pytest.param({}, id="legacy-row"),
        pytest.param({"exit_tp_value": 1.75}, id="half-stamped"),
        pytest.param({"exit_tp_value": "junk", "exit_stop_value": "0.30"}, id="unparseable"),
        pytest.param({"exit_tp_value": 0.0, "exit_stop_value": 0.30}, id="non-positive"),
    ],
)
def test_unusable_stored_values_fall_back_to_the_constants(book_factory, long_kw, short_kw, fields):
    """Byte-for-byte identical to the pre-stamping behaviour, decision and
    reason alike. Rows opened before the gate stamped exits are the ones this
    protects, and charter §4 forbids re-litigating them."""
    quotes = {long_kw: 0.50, short_kw: 2.50}
    baseline = book_factory(**quotes).classify()
    got = stamp(book_factory(**quotes), **fields).classify()
    assert got == baseline
    assert "exits stamped at entry" not in got[1]


# A quote of 0.00 reads as a missing quote (buyback_cost refuses a
# non-positive price), so the short leg is parked on a real quarter here. Both
# it and the bids below are exact in binary, which keeps the boundary cases
# testing the comparison rather than the float representation.
SHORT_ASK = 0.25


@pytest.mark.parametrize(
    "long_bid, rule",
    [
        # A 2.50 debit on a 5-wide vertical: the gate stamps tp 3.75, which is
        # half of the 2.50 maximum profit, and stop 1.25. Only the target moved
        # in the re-anchoring — half the debit was already the stop — so the
        # stop cases here pin continuity rather than a change.
        pytest.param(4.05, "TAKE_PROFIT", id="over-the-half-of-max-profit-target"),
        pytest.param(4.00, "TAKE_PROFIT", id="exactly-the-target"),
        pytest.param(3.95, None, id="just-under-the-target"),
        pytest.param(1.55, None, id="just-over-the-stop"),
        pytest.param(1.50, "VALUE_STOP", id="exactly-the-stop"),
    ],
)
def test_the_new_debit_formula_classifies_from_the_stored_values(long_bid, rule):
    book = stamp(debit_book(limit_price="2.50", long_bid=long_bid, short_ask=SHORT_ASK),
                 exit_tp_value=3.75, exit_stop_value=1.25)
    got, _ = book.classify()
    assert got == rule


def test_stored_target_is_reachable_where_the_old_constant_never_was():
    """Why §4 was re-anchored the evening of 2026-08-27.

    A 3.00 debit on a 5-wide vertical could never take profit under the old
    constant: 2x the debit is 6.00, above the spread's own 5.00 ceiling, so the
    rule was unreachable by construction. The stored target of 4.00 — half of
    maximum profit — sits inside the band and fires on a spread worth 4.25.
    """
    quotes = {"limit_price": "3.00", "long_bid": 4.50, "short_ask": SHORT_ASK}
    assert debit_book(**quotes).classify()[0] is None  # the unreachable constant
    got, reason = stamp(debit_book(**quotes), exit_tp_value=4.00,
                        exit_stop_value=1.50).classify()
    assert got == "TAKE_PROFIT"
    assert "exits stamped at entry tp 4.00 / stop 1.50" in reason


@pytest.mark.parametrize("book_factory, fields", [
    pytest.param(debit_book, {"exit_tp_value": 0.01, "exit_stop_value": 99.0}, id="debit"),
    pytest.param(credit_book, {"exit_tp_value": 99.0, "exit_stop_value": 0.01}, id="credit"),
])
def test_the_clock_still_outranks_stored_values(book_factory, fields):
    """Stored exits move the value band, never the precedence. §4's same-day
    clock is settled before either value branch is consulted."""
    got, reason = stamp(book_factory(), **fields).classify(PAST_CUTOFF)
    assert got == "CLOCK"
    assert "expire today" in reason


@pytest.mark.parametrize("book_factory, word", [
    pytest.param(debit_book, "debit", id="debit"),
    pytest.param(credit_book, "credit", id="credit"),
])
def test_stored_values_do_not_rescue_a_row_with_no_usable_entry_price(book_factory, word):
    """A row whose limit_price is unreadable gets the clock rule only, stamped
    exits or not. The stored thresholds are enforceable on their own, but a row
    that corrupt is not one to start closing positions on, and the decision
    text an audit reads is anchored on the entry price."""
    book = stamp(book_factory(limit_price="junk"), exit_tp_value=0.01, exit_stop_value=0.01)
    got, reason = book.classify()
    assert got is None
    assert f"no usable entry {word}" in reason


# --- unusable ledger prices: no exit fires, and the reason says why --------


@pytest.mark.parametrize(
    "book_factory, limit_price, expected_word",
    [
        pytest.param(credit_book, "0.75", "credit", id="credit-entry-with-a-debit-price"),
        pytest.param(credit_book, "0", "credit", id="credit-entry-zero"),
        pytest.param(credit_book, None, "credit", id="credit-entry-null"),
        pytest.param(credit_book, "junk", "credit", id="credit-entry-unparseable"),
        pytest.param(debit_book, "-0.75", "debit", id="debit-entry-with-a-credit-price"),
        pytest.param(debit_book, "0", "debit", id="debit-entry-zero"),
        pytest.param(debit_book, None, "debit", id="debit-entry-null"),
        pytest.param(debit_book, "junk", "debit", id="debit-entry-unparseable"),
    ],
)
def test_unusable_limit_price_falls_to_the_clock(book_factory, limit_price, expected_word):
    book = book_factory(limit_price=limit_price)
    got, reason = book.classify()
    assert got is None
    assert f"no usable entry {expected_word}" in reason
    assert f"limit_price={limit_price!r}" in reason
    assert "clock rule only" in reason


def test_unusable_limit_price_still_loses_to_the_clock():
    book = debit_book(limit_price="junk")
    got, reason = book.classify(PAST_CUTOFF)
    assert got == "CLOCK"
    assert "expire today" in reason


def test_missing_limit_price_field():
    book = debit_book()
    del book.entry["limit_price"]
    got, reason = book.classify()
    assert got is None
    assert "no usable entry debit" in reason


# --- quote failures: abstain, never exit on missing information ------------


def _drop(book: Book, symbol: str) -> Book:
    book.quotes.pop(symbol, None)
    return book


def _corrupt(book: Book, symbol: str, side: str, value) -> Book:
    book.quotes[symbol][side] = value
    return book


@pytest.mark.parametrize("book_factory", [credit_book, debit_book],
                         ids=["credit", "debit"])
@pytest.mark.parametrize(
    "damage",
    [
        pytest.param(lambda b: Book(b.entry, b.qty, {}, b.short_leg, b.long_leg),
                     id="no-quotes-at-all"),
        pytest.param(lambda b: _drop(b, b.short_leg), id="short-leg-row-missing"),
        pytest.param(lambda b: _drop(b, b.long_leg), id="long-leg-row-missing"),
        pytest.param(lambda b: _corrupt(b, b.short_leg, "ap", 0), id="short-ask-zero"),
        pytest.param(lambda b: _corrupt(b, b.long_leg, "bp", -1.0), id="long-bid-negative"),
        pytest.param(lambda b: _corrupt(b, b.short_leg, "ap", None), id="short-ask-null"),
        pytest.param(lambda b: _corrupt(b, b.long_leg, "bp", "1.20"), id="long-bid-a-string"),
    ],
)
def test_quote_failure_abstains_and_falls_to_the_clock(book_factory, damage):
    """A quote failure must never be an exit trigger.

    The supervisor closes real positions unattended; a missing row is a reason
    to wait for the next pass, not to unwind a position on no information.
    """
    got, reason = damage(book_factory()).classify()
    assert got is None
    assert "no usable quote" in reason
    assert "abstaining from the value rules" in reason


@pytest.mark.parametrize("book_factory", [credit_book, debit_book],
                         ids=["credit", "debit"])
def test_quote_failure_still_loses_to_the_clock(book_factory):
    book = book_factory()
    book.quotes.clear()
    got, reason = book.classify(PAST_CUTOFF)
    assert got == "CLOCK"
    assert "past the 15:20 backstop cutoff" in reason


# --- precedence: the clock outranks both value rules -----------------------


@pytest.mark.parametrize(
    "book, would_fire",
    [
        pytest.param(credit_book(short_ask=0.60, long_bid=0.20), "TAKE_PROFIT",
                     id="credit-take-profit"),
        pytest.param(credit_book(short_ask=3.00, long_bid=0.50), "VALUE_STOP",
                     id="credit-value-stop"),
        pytest.param(debit_book(long_bid=3.50, short_ask=1.00), "TAKE_PROFIT",
                     id="debit-take-profit"),
        pytest.param(debit_book(long_bid=0.60, short_ask=0.50), "VALUE_STOP",
                     id="debit-value-stop"),
        pytest.param(credit_book(short_ask=1.50, long_bid=0.50), None,
                     id="credit-inside-band"),
        pytest.param(debit_book(long_bid=2.00, short_ask=1.00), None,
                     id="debit-inside-band"),
        pytest.param(credit_book(structure="long_single", limit_price="1.00"), None,
                     id="structure-left-to-the-agent"),
    ],
)
@pytest.mark.parametrize("now", [AT_CUTOFF, PAST_CUTOFF],
                         ids=["at-cutoff", "past-cutoff"])
def test_clock_outranks_everything(book, would_fire, now):
    assert book.classify()[0] == would_fire  # what would have fired before 15:20
    rule, reason = book.classify(now)
    assert rule == "CLOCK"
    assert "2 leg(s) expire today" in reason


@pytest.mark.parametrize(
    "book",
    [
        pytest.param(credit_book(short_ask=0.60, long_bid=0.20), id="credit"),
        pytest.param(debit_book(long_bid=3.50, short_ask=1.00), id="debit"),
    ],
)
def test_one_minute_before_the_cutoff_the_value_rules_still_govern(book):
    got, reason = book.classify(JUST_BEFORE_CUTOFF)
    assert got == "TAKE_PROFIT"
    assert "expires today, clock 15:19 ET is before 15:20" in reason


@pytest.mark.parametrize("book_factory", [credit_book, debit_book],
                         ids=["credit", "debit"])
def test_legs_expiring_another_day_never_trip_the_clock(book_factory):
    book = book_factory(expiry=TOMORROW)
    got, reason = book.classify(PAST_CUTOFF)
    assert got is None
    assert "no leg expires today" in reason


# --- structures the supervisor does not value-manage -----------------------


@pytest.mark.parametrize(
    "structure, shown",
    [
        pytest.param("long_single", "long_single", id="single-long-option"),
        pytest.param("butterfly", "butterfly", id="unrecognized-name"),
        pytest.param(None, "unrecorded", id="field-missing"),
        pytest.param("", "unrecorded", id="field-empty"),
    ],
)
def test_unmanaged_structures_are_left_to_the_agent(structure, shown):
    book = debit_book(structure=structure, long_bid=3.50, short_ask=1.00)
    if structure is None:
        del book.entry["structure"]
    got, reason = book.classify()
    assert got is None
    assert f"structure={shown} is not value-managed" in reason
    assert "Tactical exits belong to the agent" in reason


@pytest.mark.parametrize("book_factory", [credit_book, debit_book],
                         ids=["credit", "debit"])
def test_entry_with_no_legs_is_never_an_exit(book_factory):
    """A legless entry unwinds for zero, which both value branches would
    otherwise read as a filled take-profit. supervisor.py skips these before
    calling in, so this is belt-and-braces — but the arithmetic must not
    recommend closing a position the ledger cannot name."""
    book = book_factory()
    book.entry["legs"] = []
    got, reason = book.classify(PAST_CUTOFF)
    assert got is None
    assert "records no legs" in reason


# --- close_order and breach_pct --------------------------------------------


def test_close_order_puts_shorts_first():
    """Unwinding the long side first leaves a naked short mid-close."""
    short, long_ = occ("C", 645.0), occ("C", 650.0)
    qty = {short: -1.0, long_: 1.0}
    assert close_order([long_, short], qty) == [short, long_]
    assert close_order([short, long_], qty) == [short, long_]


def test_close_order_is_stable_when_qty_is_unknown():
    a, b = occ("C", 645.0), occ("C", 650.0)
    assert close_order([b, a], {}) == [a, b]


@pytest.mark.parametrize(
    "account, pct",
    [
        pytest.param({"equity": "97000", "last_equity": "100000"}, -0.03, id="breach"),
        pytest.param({"equity": 101000.0, "last_equity": 100000.0}, 0.01, id="up-day"),
        pytest.param({"equity": "100000"}, None, id="no-last-equity"),
        pytest.param({"equity": "x", "last_equity": "100000"}, None, id="unparseable"),
        pytest.param({"equity": "1", "last_equity": "0"}, None, id="zero-denominator"),
        pytest.param({}, None, id="empty"),
    ],
)
def test_breach_pct(account, pct):
    got = breach_pct(account)
    assert got is None if pct is None else got == pytest.approx(pct)
