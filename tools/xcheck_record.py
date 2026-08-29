#!/usr/bin/env python3
"""Cross-check each run's prose record against the stored risk ledger.

A decision run's last act is to print a record — an exit-check table, a book
risk total, a ruling request — into its launchd log. That prose is written by
the model from memory of its own reads, and twice it has drifted from
`state/risk_ledger.json`: a stale open-risk total quoted after the book had
changed, and a position attributed to a run id that owned no ledger entry.
Neither slip moved money; both would have misled the human reading the log.

This tool diffs the most recent record in each run log against the ledger and
prints one `XCHECK|...` line per finding. It is advisory and log-only: it never
places, closes, or amends anything, it writes no files, and it always exits 0
so postflight can call it without any chance of failing a trading run.

What it compares, and what it deliberately does not:

* Exit-check table rows are matched to ledger entries by run-id tag, then by
  OCC symbol, then by underlying and strike pair. Entry, Stop and TP cells are
  compared against `limit_price`, `exit_stop_value` and `exit_tp_value`. A
  "Now"/"Value"/"mid" column is live market data with no stored counterpart,
  so no unrecognized column is ever compared.
* A row that matches nothing is skipped in silence — records legitimately
  contain tables this tool has no business reading. The one exception is a row
  carrying a run-id-shaped tag (`cal-1315`, `run6`) that no ledger entry owns:
  that is the attribution slip, flagged as ORPHAN_REF. A row whose tag is
  unknown but which resolves by strikes to an entry with a null
  `client_order_id` is NOT flagged — several real entries carry no id, so the
  tag can be neither confirmed nor contradicted.
* Dollar amounts on lines mentioning risk are checked against the ledger's
  summed `max_loss_usd`. The check is deliberately loose: if any amount
  anywhere in the record's risk lines equals the ledger total, the record is
  called consistent and nothing is flagged. A line is flagged only when it
  claims a "total" or "open risk" and none of its amounts is the ledger total,
  a single position's max loss, or the sum of any subset of positions (the
  empty subset included, so a flat book's "$0" is fine). False positives here
  would train the reader to ignore the tool, which is worse than a missed one.

Honest limits: it reads the log, not the tape, so it can only catch prose that
contradicts the ledger, never prose that is merely wrong about the world. It
compares whatever record is last in each log, so running it by hand long after
a run will diff a stale record against a current ledger. Its own output lines
are skipped on re-reads so findings cannot cascade.

Run: .venv/bin/python tools/xcheck_record.py
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "state" / "risk_ledger.json"
LOG_DIR = ROOT / "state" / "logs"

# The research pass holds no positions and prints no exit table; checking it
# would only produce SKIP noise.
LOG_LABELS = ("decision-1", "decision-2", "decision-3", "check", "calibration")

PRICE_TOL = 0.005
RISK_TOL = 1.0
# Subset sums are 2**n; the real ledger holds six entries at most, and this cap
# keeps a pathological ledger from stalling postflight.
MAX_SUBSET_ENTRIES = 16
DETAIL_LINE_CHARS = 120

# Column headers we trust to name a stored value. Anything else in the table —
# "Now", "Value (mid)", "Verdict" — is ignored rather than guessed at.
POSITION_HEADERS = frozenset(
    {"position", "positions", "leg", "legs", "spread", "trade", "structure", "name"}
)
COLUMN_ROLES = {
    "entry": frozenset({"entry", "entry price", "entry value", "entry fill", "fill", "debit"}),
    "stop": frozenset({"stop", "stop value", "stop loss", "stop level"}),
    "tp": frozenset({"tp", "take profit", "take-profit", "tp value", "target", "profit target"}),
}
LEDGER_FIELD = {"entry": "limit_price", "stop": "exit_stop_value", "tp": "exit_tp_value"}
ROLE_LABEL = {"entry": "Entry", "stop": "Stop", "tp": "TP"}

OCC_RE = re.compile(r"\b([A-Z]{1,6})(\d{6})([CP])(\d{8})\b")
PAIR_RE = re.compile(r"\b([A-Z]{2,6})\s+(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)\b")
RUNID_RE = re.compile(r"\b(?:cal-\d{3,4}|run[-\s]?\d+)\b", re.IGNORECASE)
PAREN_RE = re.compile(r"\(([^)]*)\)")
DOLLAR_RE = re.compile(r"\$\s?([\d,]+(?:\.\d+)?)")
SEPARATOR_RE = re.compile(r":?-{2,}:?")
NUMBER_RE = re.compile(r"-?\d+(?:\.\d+)?")
MIN_TAG_CHARS = 4


@dataclass(frozen=True)
class Row:
    """One exit-check table row: its label cell and the stored values it claims."""

    label: str
    values: dict[str, float]


# ------------------------------------------------------------------ ledger


def load_ledger(path: Path = LEDGER) -> tuple[list[dict], str | None]:
    """Return (entries, error). A bad or absent ledger is an error, not a crash."""
    try:
        raw = json.loads(path.read_text())
    except OSError as exc:
        return [], f"ledger unreadable: {exc.strerror or exc}"
    except ValueError as exc:
        return [], f"ledger unparseable: {exc}"
    if not isinstance(raw, list):
        return [], "ledger is not a list of entries"
    return [entry for entry in raw if isinstance(entry, dict)], None


def parse_occ(symbol: str) -> tuple[str, str, float] | None:
    """Split an OCC option symbol into (underlying, right, strike-in-dollars)."""
    match = OCC_RE.fullmatch(symbol.strip())
    if match is None:
        return None
    return match.group(1), match.group(3), int(match.group(4)) / 1000.0


def entry_strikes(entry: dict) -> tuple[str, frozenset[float]] | None:
    """Return (underlying, strike set) when every leg parses and agrees on the root."""
    parsed = [parse_occ(leg) for leg in entry.get("legs") or []]
    if not parsed or any(p is None for p in parsed):
        return None
    roots = {p[0] for p in parsed}
    if len(roots) != 1:
        return None
    return roots.pop(), frozenset(p[2] for p in parsed)


# ------------------------------------------------------------------ records


def latest_record(text: str) -> str | None:
    """Everything from the last run-start marker to EOF, or None if there is none."""
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if "=== " in line and " starting" in line:
            start = index
    if start is None:
        return None
    return "\n".join(lines[start:])


def _split_row(line: str) -> list[str]:
    body = line.strip().removeprefix("|").removesuffix("|")
    return [cell.strip() for cell in body.split("|")]


def _is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(SEPARATOR_RE.fullmatch(cell.strip()) for cell in cells)


def _norm_header(cell: str) -> str:
    text = PAREN_RE.sub(" ", cell)
    text = re.sub(r"[*`_]", "", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def _cell_number(cell: str) -> float | None:
    match = NUMBER_RE.search(cell.replace(",", "").replace("$", ""))
    return float(match.group()) if match else None


def _table_blocks(record: str) -> list[list[str]]:
    blocks: list[list[str]] = []
    current: list[str] = []
    for line in record.splitlines():
        if line.strip().startswith("|"):
            current.append(line)
            continue
        if current:
            blocks.append(current)
            current = []
    if current:
        blocks.append(current)
    return blocks


def parse_rows(record: str) -> list[Row]:
    """Pull exit-check rows out of every markdown table the record prints.

    A table is read only when it names a position column and at least one
    column this tool can compare; the IV-regime and account tables runs also
    print carry neither and are passed over.
    """
    rows: list[Row] = []
    for block in _table_blocks(record):
        if len(block) < 3 or not _is_separator(_split_row(block[1])):
            continue
        headers = [_norm_header(cell) for cell in _split_row(block[0])]
        label_index = next(
            (i for i, header in enumerate(headers) if header in POSITION_HEADERS), None
        )
        roles = {
            i: role
            for i, header in enumerate(headers)
            for role, names in COLUMN_ROLES.items()
            if header in names
        }
        if label_index is None or not roles:
            continue
        for line in block[2:]:
            cells = _split_row(line)
            if len(cells) <= label_index or not cells[label_index]:
                continue
            values = {}
            for index, role in roles.items():
                number = _cell_number(cells[index]) if index < len(cells) else None
                if number is not None:
                    values[role] = number
            rows.append(Row(label=re.sub(r"[*`]", "", cells[label_index]).strip(), values=values))
    return rows


# ------------------------------------------------------------------ matching


def row_tags(label: str) -> list[str]:
    """Candidate identifiers in a row label: parenthesized text and run-id shapes."""
    tags = [text.strip() for text in PAREN_RE.findall(label)]
    tags += [match.group(0) for match in RUNID_RE.finditer(label)]
    seen, out = set(), []
    for tag in tags:
        key = tag.casefold()
        if len(key) >= MIN_TAG_CHARS and key not in seen:
            seen.add(key)
            out.append(tag)
    return out


def _tag_matches(tag: str, entry: dict) -> bool:
    cid = entry.get("client_order_id")
    return bool(cid) and cid.casefold().startswith(tag.casefold())


def match_row(label: str, entries: list[dict]) -> int | None:
    """Index of the ledger entry a row refers to, or None when it names none.

    Tag, OCC symbol and strike pair are tried in that order; a rule that
    narrows to several entries (two wings share a `cal-1325` prefix) is
    intersected with the next rule rather than guessed at.
    """
    tags = row_tags(label)
    by_tag = {i for i, entry in enumerate(entries) if any(_tag_matches(t, entry) for t in tags)}
    by_occ = {
        i
        for i, entry in enumerate(entries)
        if any(str(leg) in label for leg in entry.get("legs") or [])
    }
    by_strikes: set[int] = set()
    for pair in PAIR_RE.finditer(label):
        underlying = pair.group(1)
        strikes = frozenset({float(pair.group(2)), float(pair.group(3))})
        by_strikes |= {
            i for i, entry in enumerate(entries) if entry_strikes(entry) == (underlying, strikes)
        }

    candidates: set[int] | None = None
    for result in (by_tag, by_occ, by_strikes):
        if not result:
            continue
        if candidates is None:
            candidates = set(result)
        else:
            candidates = candidates & result or candidates
        if len(candidates) == 1:
            break
    return candidates.pop() if candidates and len(candidates) == 1 else None


def check_rows(rows: list[Row], entries: list[dict]) -> tuple[int, list[str]]:
    """Compare each recognized row against its ledger entry. Returns (checked, findings)."""
    findings: list[str] = []
    checked = 0
    for row in rows:
        tags = row_tags(row.label)
        run_tags = [tag for tag in tags if RUNID_RE.fullmatch(tag)]
        orphans = [
            tag for tag in run_tags if not any(_tag_matches(tag, entry) for entry in entries)
        ]
        index = match_row(row.label, entries)
        if index is None:
            for tag in orphans:
                findings.append(
                    f"ORPHAN_REF row '{row.label}': '{tag}' matches no ledger entry "
                    "and the row resolves to none"
                )
            continue
        checked += 1
        entry = entries[index]
        cid = entry.get("client_order_id")
        if orphans and cid and not any(_tag_matches(tag, entry) for tag in tags):
            findings.append(
                f"ORPHAN_REF row '{row.label}': '{orphans[0]}' matches no ledger entry; "
                f"the row's legs belong to {cid}"
            )
        for role, claimed in sorted(row.values.items()):
            stored = _stored_value(entry, role)
            if stored is None or abs(claimed - stored) <= PRICE_TOL:
                continue
            findings.append(
                f"row '{row.label}': {ROLE_LABEL[role]} {claimed:g} "
                f"differs from stored {stored:g}"
            )
    return checked, findings


def _stored_value(entry: dict, role: str) -> float | None:
    try:
        return float(entry[LEDGER_FIELD[role]])
    except (KeyError, TypeError, ValueError):
        return None


# ------------------------------------------------------------------ risk totals


def max_losses(entries: list[dict]) -> list[float]:
    """The `max_loss_usd` of every entry that carries a usable one."""
    losses = []
    for entry in entries:
        try:
            losses.append(float(entry["max_loss_usd"]))
        except (KeyError, TypeError, ValueError):
            continue
    return losses


def attainable_sums(entries: list[dict]) -> set[float]:
    """Every total a truthful sentence could quote: any subset of max losses, empty included."""
    losses = max_losses(entries)
    if len(losses) > MAX_SUBSET_ENTRIES:
        return {0.0, sum(losses), *losses}
    sums = {0.0}
    for loss in losses:
        sums |= {total + loss for total in sums}
    return sums


def risk_lines(record: str) -> list[str]:
    """Lines that mention risk and quote at least one dollar amount."""
    return [
        line
        for line in record.splitlines()
        if not line.startswith("XCHECK|") and "risk" in line.lower() and DOLLAR_RE.search(line)
    ]


def _amounts(line: str) -> list[float]:
    return [float(raw.replace(",", "")) for raw in DOLLAR_RE.findall(line)]


def check_risk_totals(record: str, entries: list[dict]) -> tuple[int, list[str]]:
    """Check quoted risk totals against the ledger. Returns (lines checked, findings)."""
    lines = risk_lines(record)
    if not lines:
        return 0, []
    total = sum(max_losses(entries))
    if any(abs(amount - total) <= RISK_TOL for line in lines for amount in _amounts(line)):
        return len(lines), []
    sums = attainable_sums(entries)
    findings = []
    for line in lines:
        low = line.lower()
        if "open risk" not in low and "total" not in low:
            continue
        amounts = _amounts(line)
        if any(abs(amount - candidate) <= RISK_TOL for amount in amounts for candidate in sums):
            continue
        quoted = ", ".join(_dollars(amount) for amount in amounts)
        findings.append(
            f"RISK_TOTAL: line quotes {quoted} but the ledger sums to {_dollars(total)} "
            f"across {len(entries)} entr{'y' if len(entries) == 1 else 'ies'}: "
            f"'{_clip(line)}'"
        )
    return len(lines), findings


def _dollars(amount: float) -> str:
    """Quote an amount back the way the record wrote it — cents only when it has them."""
    return f"${amount:,.0f}" if float(amount).is_integer() else f"${amount:,.2f}"


def _clip(line: str) -> str:
    text = line.strip()
    return text if len(text) <= DETAIL_LINE_CHARS else text[: DETAIL_LINE_CHARS - 3] + "..."


# ------------------------------------------------------------------ reporting


def check_log(path: Path, entries: list[dict], stamp: str) -> list[str]:
    """Report lines for one log file. An absent log is not worth a line."""
    name = path.name
    try:
        text = path.read_text(errors="replace")
    except OSError:
        return []
    record = latest_record(text)
    if record is None:
        return [f"XCHECK|{stamp}|SKIP|{name}|no run record found"]
    checked, findings = check_rows(parse_rows(record), entries)
    risk_checked, risk_findings = check_risk_totals(record, entries)
    findings += risk_findings
    if findings:
        return [f"XCHECK|{stamp}|MISMATCH|{name}|{finding}" for finding in findings]
    if not checked and not risk_checked:
        return [f"XCHECK|{stamp}|SKIP|{name}|no table rows recognized"]
    summary = f"{checked} row(s) checked, {risk_checked} risk line(s) checked"
    return [f"XCHECK|{stamp}|OK|{name}|{summary}"]


def main() -> int:
    stamp = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    entries, error = load_ledger()
    if error:
        print(f"XCHECK|{stamp}|SKIP|-|{error}")
        return 0
    for label in LOG_LABELS:
        for line in check_log(LOG_DIR / f"com.mandate.{label}.out.log", entries, stamp):
            print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
