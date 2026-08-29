"""Unit tests for the postflight record cross-check.

Everything under test is a pure function over text: no logs on disk, no
ledger on disk, no clock. The two slips the tool exists to catch — a stale
open-risk total and a position attributed to a run id that owns no ledger
entry — each have a test that fails if the check stops firing, and the
conservative cases that must stay silent (an unlabelled row, a per-position
dollar amount, a flat book quoting $0) have tests too. A false positive here
is the failure mode that would get the tool ignored, so the silences are
asserted as deliberately as the flags.

Run: .venv/bin/python -m pytest tools/
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from xcheck_record import (
    Row,
    attainable_sums,
    check_log,
    check_risk_totals,
    check_rows,
    entry_strikes,
    latest_record,
    load_ledger,
    match_row,
    parse_occ,
    parse_rows,
    risk_lines,
    row_tags,
)

STAMP = "2026-08-29T20:00:00Z"

# A trimmed copy of the shape state/risk_ledger.json really holds, including
# the two entries whose client_order_id is null.
LEDGER = [
    {
        "client_order_id": "cal-1315-qqq-bullcall-717-722",
        "order_id": "8fd1b79e",
        "legs": ["QQQ260904C00717000", "QQQ260904C00722000"],
        "structure": "debit_vertical",
        "limit_price": "2.48",
        "max_loss_usd": 992.0,
        "exit_tp_value": 3.74,
        "exit_stop_value": 1.24,
        "placed_at": "2026-08-28T14:20:54-04:00",
    },
    {
        "client_order_id": "cal-1325-spy-vol-call-775-780",
        "order_id": "e6fa1faa",
        "legs": ["SPY260904C00775000", "SPY260904C00780000"],
        "structure": "debit_vertical",
        "limit_price": "1.30",
        "max_loss_usd": 780.0,
        "exit_tp_value": 3.15,
        "exit_stop_value": 0.65,
        "placed_at": "2026-08-28T14:27:42-04:00",
    },
    {
        "client_order_id": "cal-1325-spy-vol-put-763-758",
        "order_id": "d938fe29",
        "legs": ["SPY260904P00763000", "SPY260904P00758000"],
        "structure": "debit_vertical",
        "limit_price": "0.95",
        "max_loss_usd": 570.0,
        "exit_tp_value": 2.975,
        "exit_stop_value": 0.475,
        "placed_at": "2026-08-28T14:27:46-04:00",
    },
    {
        "client_order_id": None,
        "order_id": "83a27db5",
        "legs": ["QQQ260904C00721000", "QQQ260904C00726000"],
        "structure": "debit_vertical",
        "limit_price": "1.85",
        "max_loss_usd": 740.0,
        "exit_tp_value": 3.425,
        "exit_stop_value": 0.925,
        "placed_at": "2026-08-28T14:37:46-04:00",
    },
]
LEDGER_TOTAL = 992.0 + 780.0 + 570.0 + 740.0  # 3082.0

EXIT_TABLE = """\
| Position | Entry | Now | Stop | TP |
|---|---|---|---|---|
| QQQ 717/722 C (cal-1315) | 2.48 | 2.33 | 1.24 | 3.74 |
| QQQ 721/726 C (pair) | 1.85 | 1.75 | 0.925 | 3.425 |
"""


def record(body: str, marker: str = "[2026-08-28T19:35:01Z] === decision run 3 starting ===") -> str:
    return f"{marker}\n{body}\n"


# ------------------------------------------------------------------ extraction


def test_latest_record_takes_the_last_marker():
    text = (
        "noise\n"
        "[t] === decision run 1 starting ===\n"
        "first record\n"
        "[t] === decision run 2 starting ===\n"
        "second record\n"
    )
    assert latest_record(text) == "[t] === decision run 2 starting ===\nsecond record"


@pytest.mark.parametrize(
    "text",
    ["", "just some output\nwith no marker\n", "=== not a start line ===\n"],
    ids=["empty", "no-marker", "marker-without-starting"],
)
def test_latest_record_absent(text):
    assert latest_record(text) is None


@pytest.mark.parametrize(
    ("symbol", "expected"),
    [
        ("QQQ260904C00717000", ("QQQ", "C", 717.0)),
        ("SPY260904P00763000", ("SPY", "P", 763.0)),
        ("SPY260904C00775500", ("SPY", "C", 775.5)),
        ("not-a-symbol", None),
        ("QQQ260904X00717000", None),
    ],
)
def test_parse_occ(symbol, expected):
    assert parse_occ(symbol) == expected


def test_entry_strikes():
    assert entry_strikes(LEDGER[0]) == ("QQQ", frozenset({717.0, 722.0}))
    assert entry_strikes({"legs": []}) is None
    assert entry_strikes({"legs": ["QQQ260904C00717000", "SPY260904C00722000"]}) is None


# ------------------------------------------------------------------ table parsing


def test_parse_rows_reads_labels_and_stored_columns():
    rows = parse_rows(EXIT_TABLE)
    assert [row.label for row in rows] == ["QQQ 717/722 C (cal-1315)", "QQQ 721/726 C (pair)"]
    assert rows[0].values == {"entry": 2.48, "stop": 1.24, "tp": 3.74}


def test_parse_rows_ignores_live_columns():
    """"Now" has no stored counterpart, so it must never reach the comparison."""
    assert all("now" not in row.values for row in parse_rows(EXIT_TABLE))


def test_parse_rows_accepts_reordered_and_renamed_headers():
    table = """\
| Position | Take profit | Value (mid) | Stop |
|---|---|---|---|
| cal-1315 QQQ 717/722 bull call | 3.74 | 2.45 | 1.24 |
"""
    (row,) = parse_rows(table)
    assert row.values == {"tp": 3.74, "stop": 1.24}


@pytest.mark.parametrize(
    ("table", "reason"),
    [
        (
            "| Underlying | Spot | Regime |\n|---|---|---|\n| SPY | 768.95 | Low |\n",
            "no position column and nothing comparable",
        ),
        (
            "| Position | Verdict |\n|---|---|\n| QQQ 717/722 C | hold |\n",
            "position column but no stored value",
        ),
        (
            "| Position | Stop |\n| QQQ 717/722 C | 1.24 |\n",
            "no separator row, so not a table",
        ),
    ],
)
def test_parse_rows_skips_tables_it_cannot_read(table, reason):
    assert parse_rows(table) == [], reason


# ------------------------------------------------------------------ matching


@pytest.mark.parametrize(
    ("label", "expected", "how"),
    [
        ("QQQ 717/722 C (cal-1315)", 0, "parenthesized tag"),
        ("cal-1315 QQQ 717/722 bull call", 0, "bare run-id tag"),
        ("leg QQQ260904C00721000 / QQQ260904C00726000", 3, "OCC symbol"),
        ("QQQ 721/726 C (pair)", 3, "underlying and strike pair"),
        ("SPY 763/758 P (cal-1325)", 2, "ambiguous tag narrowed by strikes"),
        ("QQQ 999/998 C (pair)", None, "nothing identifiable"),
        ("some prose row", None, "no identifier at all"),
    ],
)
def test_match_row(label, expected, how):
    assert match_row(label, LEDGER) == expected, how


def test_row_tags_drops_short_noise():
    assert row_tags("QQQ 717/722 C (cal-1315) (x)") == ["cal-1315"]


# ------------------------------------------------------------------ row diffing


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ({"entry": 2.48, "stop": 1.24, "tp": 3.74}, []),
        ({"entry": 2.484, "stop": 1.244}, []),
        ({"tp": 3.80}, ["row 'QQQ 717/722 C (cal-1315)': TP 3.8 differs from stored 3.74"]),
        ({"stop": 1.30}, ["row 'QQQ 717/722 C (cal-1315)': Stop 1.3 differs from stored 1.24"]),
        ({"entry": 2.60}, ["row 'QQQ 717/722 C (cal-1315)': Entry 2.6 differs from stored 2.48"]),
    ],
    ids=["clean", "within-tolerance", "tp-drift", "stop-drift", "entry-drift"],
)
def test_check_rows_value_diffs(values, expected):
    checked, findings = check_rows([Row("QQQ 717/722 C (cal-1315)", values)], LEDGER)
    assert checked == 1
    assert findings == expected


def test_check_rows_skips_unidentifiable_rows_silently():
    checked, findings = check_rows([Row("some prose (pair)", {"stop": 9.99})], LEDGER)
    assert (checked, findings) == (0, [])


def test_check_rows_flags_a_run_id_that_owns_nothing():
    checked, findings = check_rows([Row("QQQ 999/998 C (cal-9999)", {"stop": 1.0})], LEDGER)
    assert checked == 0
    assert findings == [
        (
            "ORPHAN_REF row 'QQQ 999/998 C (cal-9999)': 'cal-9999' matches no ledger "
            "entry and the row resolves to none"
        )
    ]


def test_check_rows_flags_a_row_attributed_to_the_wrong_run():
    """The row's strikes are cal-1315's; the prose credits a run that owns no entry."""
    checked, findings = check_rows([Row("QQQ 717/722 C (cal-9999)", {"tp": 3.74})], LEDGER)
    assert checked == 1
    assert findings == [
        (
            "ORPHAN_REF row 'QQQ 717/722 C (cal-9999)': 'cal-9999' matches no ledger entry; "
            "the row's legs belong to cal-1315-qqq-bullcall-717-722"
        )
    ]


def test_check_rows_stays_quiet_when_the_entry_has_no_client_order_id():
    """Two real ledger entries carry a null id, so their tag cannot be contradicted."""
    checked, findings = check_rows([Row("cal-1335 QQQ 721/726 bull call", {"tp": 3.425})], LEDGER)
    assert (checked, findings) == (1, [])


# ------------------------------------------------------------------ risk totals


def test_attainable_sums_includes_the_empty_subset_and_the_total():
    sums = attainable_sums(LEDGER)
    assert 0.0 in sums
    assert LEDGER_TOTAL in sums
    assert 992.0 + 570.0 in sums


def test_risk_lines_ignores_this_tools_own_output():
    body = f"XCHECK|{STAMP}|MISMATCH|x.log|RISK_TOTAL: line quotes $9,874 open risk\n"
    assert risk_lines(body) == []


@pytest.mark.parametrize(
    ("line", "flagged", "why"),
    [
        (
            f"Open positions: 4, total defined risk ${LEDGER_TOTAL:,.0f} (cap $10,000).",
            False,
            "quotes the ledger total",
        ),
        (
            "Open risk stands at $9,874 across the book.",
            True,
            "stale total matching no subset",
        ),
        (
            "Total open risk $1,562 after the two QQQ legs.",
            False,
            "a subset sum is a truthful partial claim",
        ),
        (
            "The QQQ position carries $992 of defined risk.",
            False,
            "a single position's max loss",
        ),
        (
            "Equity $100,000, no open positions, open defined risk $0.",
            False,
            "the empty subset covers a flat book",
        ),
        (
            "Risk per position is capped at $2,500 by the manifest.",
            False,
            "no total or open-risk claim, so not our business",
        ),
    ],
    ids=["exact", "stale", "subset", "single", "flat", "cap-mention"],
)
def test_check_risk_totals(line, flagged, why):
    checked, findings = check_risk_totals(record(line), LEDGER)
    assert checked == 1
    assert bool(findings) is flagged, why


def test_check_risk_totals_reports_the_ledger_sum():
    _, (finding,) = check_risk_totals(record("Open risk stands at $9,874."), LEDGER)
    assert finding.startswith("RISK_TOTAL: line quotes $9,874 but the ledger sums to $3,082")


def test_one_correct_total_makes_the_record_consistent():
    """Any amount matching the ledger sum stands the record down; false positives cost trust."""
    body = f"Book risk ${LEDGER_TOTAL:,.0f} per ledger.\nEarlier this run open risk was $9,874."
    assert check_risk_totals(record(body), LEDGER) == (2, [])


# ------------------------------------------------------------------ reporting


def write_log(tmp_path: Path, body: str, name: str = "com.mandate.decision-3.out.log") -> Path:
    path = tmp_path / name
    path.write_text(body)
    return path


def test_check_log_clean_record(tmp_path):
    body = record(f"{EXIT_TABLE}\nTotal open risk ${LEDGER_TOTAL:,.0f} across 4 positions.")
    lines = check_log(write_log(tmp_path, body), LEDGER, STAMP)
    assert lines == [
        f"XCHECK|{STAMP}|OK|com.mandate.decision-3.out.log|2 row(s) checked, 1 risk line(s) checked"
    ]


def test_check_log_reports_every_finding(tmp_path):
    table = EXIT_TABLE.replace("| 2.48 | 2.33 | 1.24 | 3.74 |", "| 2.48 | 2.33 | 1.24 | 3.80 |")
    body = record(f"{table}\nTotal open risk $9,874 across 4 positions.")
    lines = check_log(write_log(tmp_path, body), LEDGER, STAMP)
    assert len(lines) == 2
    assert all(line.startswith(f"XCHECK|{STAMP}|MISMATCH|") for line in lines)
    assert "TP 3.8 differs from stored 3.74" in lines[0]
    assert "RISK_TOTAL" in lines[1]


@pytest.mark.parametrize(
    ("body", "detail"),
    [
        ("preflight OK, nothing else\n", "no run record found"),
        (record("The run opened nothing and printed no table."), "no table rows recognized"),
    ],
    ids=["no-record", "no-rows"],
)
def test_check_log_skips(tmp_path, body, detail):
    lines = check_log(write_log(tmp_path, body), LEDGER, STAMP)
    assert lines == [f"XCHECK|{STAMP}|SKIP|com.mandate.decision-3.out.log|{detail}"]


def test_check_log_absent_file_is_silent(tmp_path):
    assert check_log(tmp_path / "never-written.log", LEDGER, STAMP) == []


def test_load_ledger_errors(tmp_path):
    missing = tmp_path / "gone.json"
    assert load_ledger(missing) == ([], "ledger unreadable: No such file or directory")

    bad = tmp_path / "bad.json"
    bad.write_text("{not json")
    entries, error = load_ledger(bad)
    assert (entries, error.startswith("ledger unparseable:")) == ([], True)

    wrong = tmp_path / "wrong.json"
    wrong.write_text(json.dumps({"client_order_id": "cal-1315"}))
    assert load_ledger(wrong) == ([], "ledger is not a list of entries")


def test_load_ledger_reads_a_list(tmp_path):
    path = tmp_path / "risk_ledger.json"
    path.write_text(json.dumps(LEDGER))
    assert load_ledger(path) == (LEDGER, None)
