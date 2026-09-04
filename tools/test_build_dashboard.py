"""Unit tests for the dashboard's equity-series cleaning.

Pure functions over payload-shaped data: no broker, no clock, no disk. The
case that matters is the funding day, 2026-08-28, when the broker's 15-minute
series reported the opening balance plus the $100,000 funding journal for
every mark until the next session's open while its daily series said the
opening balance; the chart drew a step to $200,000 the account never had and
flattened the real week into a pixel. The silences matter as much: an
ordinary drawdown, even a bad one, must never be "corrected".

Run: .venv/bin/python -m pytest tools/
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_dashboard import (  # noqa: E402
    cash_journals,
    daily_marks,
    equity_series,
    strip_cash_journals,
)

DAY = 86_400
FRI, MON, TUE = 1_000_000, 1_000_000 + 3 * DAY, 1_000_000 + 4 * DAY
JOURNAL = [(FRI - DAY, 100_000.0)]
DAILY = [(FRI, 100_000.0), (MON, 99_459.0), (TUE, 93_195.0)]


@pytest.mark.parametrize("series, expected, fixed, why", [
    ([(FRI, 100_000.0), (FRI + 900, 200_000.0), (FRI + 1800, 199_722.8),
      (MON, 99_431.9)],
     [100_000.0, 100_000.0, 99_722.8, 99_431.9], 2,
     "funding-day marks carry the journal; the opening mark and Monday do not"),
    ([(MON, 100_000.0 - 291.0), (MON + 900, 100_000.0 - 694.0)],
     [99_709.0, 99_306.0], 0,
     "a P&L frame that is not off by a whole journal is untouched"),
    ([(MON, -291.0), (MON + 900, -694.0)],
     [99_709.0, 99_306.0], 2,
     "a P&L frame a whole journal LOW after the rebase is corrected upward"),
    ([(TUE, 85_445.0), (TUE + 900, 84_650.0)],
     [85_445.0, 84_650.0], 0,
     "an eight percent gap to the daily figure is a bad day, not a journal"),
    ([(TUE, 140_000.0)],
     [140_000.0], 0,
     "a gap that removing the journal would widen is left alone"),
])
def test_strip_cash_journals(series, expected, fixed, why):
    out, n = strip_cash_journals(series, JOURNAL, DAILY)
    assert [v for _, v in out] == pytest.approx(expected), why
    assert n == fixed, why
    assert [t for t, _ in out] == [t for t, _ in series], "stamps untouched"


@pytest.mark.parametrize("journals, daily", [
    ([], DAILY),
    (JOURNAL, []),
])
def test_strip_cash_journals_needs_both_references(journals, daily):
    series = [(FRI, 200_000.0)]
    assert strip_cash_journals(series, journals, daily) == (series, 0)


def test_journal_after_the_mark_does_not_apply():
    out, n = strip_cash_journals([(FRI, 200_000.0)], [(MON, 100_000.0)], DAILY)
    assert (out, n) == ([(FRI, 200_000.0)], 0)


def test_cash_journals_reads_dated_amounts_and_skips_the_rest():
    acts = [
        {"activity_type": "JNLC", "date": "2026-08-28", "net_amount": "100000"},
        {"activity_type": "FEE", "date": "2026-08-28", "net_amount": "-0.1"},
        {"activity_type": "JNLC", "date": "not a date", "net_amount": "5"},
        {"activity_type": "JNLC", "net_amount": "5"},
        {"activity_type": "JNLC", "date": "2026-08-29", "net_amount": None},
    ]
    out = cash_journals(acts)
    assert [a for _, a in out] == [100_000.0, -0.1]
    assert out[0][0] == 1_787_875_200.0  # 2026-08-28T00:00Z
    assert cash_journals(None) == []


def test_daily_marks_drops_broker_padding():
    hist = {"timestamp": [1, 2, 3], "equity": [0, "100000", 99770.0]}
    assert daily_marks(hist) == [(2, 100_000.0), (3, 99_770.0)]
    assert daily_marks("nonsense") == []


def test_equity_series_corrects_the_funding_day_and_says_so():
    # The captured 2026-09-03 shape in miniature: raw equity carries the
    # journal on the funding day; profit_loss is relative to the phantom
    # after the rebase, so the rebuilt candidate misses the live figure.
    history = {
        "base_value": 100_000.0,
        "timestamp": [FRI, FRI + 900, FRI + 1800, MON, MON + 900],
        "equity": [100_000.0, 200_000.0, 199_722.8, 99_431.9, 98_931.0],
        "profit_loss": [0.0, 100_000.0, 99_722.8, -100_568.1, -101_069.0],
    }
    stamps, values, note, err = equity_series(
        history, 98_900.0, journals=JOURNAL, daily=DAILY)
    assert err is None
    assert values == pytest.approx([100_000.0, 100_000.0, 99_722.8, 99_431.9, 98_931.0])
    assert max(values) < 150_000, "the phantom step is gone"
    # Both candidates agree once corrected, so the preferred rebuilt series is
    # chosen: two funding-day marks down, two post-rebase marks up.
    assert "Corrected: 4 marks" in note and "$100,000" in note


def test_equity_series_reports_an_unchecked_journal():
    history = {"base_value": 100_000.0, "timestamp": [FRI, MON],
               "equity": [100_000.0, 99_000.0], "profit_loss": [0.0, -1_000.0]}
    _, values, note, err = equity_series(
        history, 99_000.0, journal_note="Cash journals not checked (HTTP 500)")
    assert err is None and values == [100_000.0, 99_000.0]
    assert note == "Cash journals not checked (HTTP 500)"
