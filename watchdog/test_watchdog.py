"""Unit tests for the watchdog's detect/kill decision.

Every test runs against a temp repo root, and `run_cmd` — the watchdog's one
seam onto the process table — is replaced with a recorder. No launchctl and no
pkill ever runs here: these tests are written on a machine where the real jobs
may be loaded and a real trading day may be in progress.

What is asserted is the pair (exit code, commands attempted). An exit code
alone would not catch the worst possible bug in this file, which is killing
com.mandate.supervisor along with the decision jobs.

Run: .venv/bin/python -m pytest watchdog/
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import watchdog

ALARM_TS = "2026-08-27T14:00:00+00:00"
BEFORE = "2026-08-27T13:59:59.500000+00:00"
AFTER = "2026-08-27T14:15:33.777735+00:00"
REASON = "day P&L -3.20% breached the -3% circuit breaker"

BOOTOUTS = [f"gui/{watchdog.os.getuid()}/{label}" for label in watchdog.DECISION_JOBS]


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    (tmp_path / "state").mkdir()
    return tmp_path


@pytest.fixture
def calls(monkeypatch) -> list[list[str]]:
    """Replace the process-action choke point with a recorder."""
    recorded: list[list[str]] = []

    def fake_run_cmd(argv: list[str]) -> tuple[int, str]:
        recorded.append(list(argv))
        return 0, ""

    monkeypatch.setattr(watchdog, "run_cmd", fake_run_cmd)
    return recorded


def record(seq: int, ts: str, *, op="place_defined_risk_spread",
           agent="hackathon-dev", tool="alpaca", decision="allow") -> str:
    return json.dumps({
        "seq": seq,
        "ts": ts,
        "principal": {"agentId": agent, "skill": "options-trader",
                      "user": "wes", "tier": "B"},
        "tool": tool,
        "op": op,
        "decision": decision,
        "reason": None,
        "outcome": "executed",
    })


def write_tape(repo: Path, *lines: str) -> None:
    (repo / "state" / "audit.jsonl").write_text("".join(f"{ln}\n" for ln in lines))


def alarm(repo: Path, stamp: str = ALARM_TS, reason: str = REASON) -> None:
    (repo / "state" / "ALARM").write_text(f"{stamp}\n{reason}\n")


# --- cases that must NOT kill ----------------------------------------------


@pytest.mark.parametrize("name, tape", [
    ("no place records at all", [record(1, AFTER, op="get_option_chain")]),
    ("place record predates the ALARM", [record(2, BEFORE)]),
    ("post-ALARM place by a different agent", [record(3, AFTER, agent="alpaca-paper-drill")]),
    ("post-ALARM place through a different tool", [record(4, AFTER, tool="polygon")]),
    ("empty tape", []),
])
def test_armed_but_clean(repo, calls, name, tape):
    alarm(repo)
    write_tape(repo, *tape)
    assert watchdog.main(repo) == 0
    assert calls == [], name
    assert not (repo / "state" / "KILLED").exists()


def test_no_alarm_is_a_noop(repo, calls):
    """Not demoted, so nothing to escalate — even with a place record on the tape."""
    write_tape(repo, record(5, AFTER))
    assert watchdog.main(repo) == 0
    assert calls == []
    assert not (repo / "state" / "KILLED").exists()


def test_missing_tape_is_not_a_kill(repo, calls):
    """An absent tape is no evidence of a violation, so it must not manufacture one."""
    alarm(repo)
    assert watchdog.main(repo) == 0
    assert calls == []


# --- cases that must kill --------------------------------------------------


@pytest.mark.parametrize("decision", ["allow", "deny"])
def test_post_alarm_place_kills_regardless_of_decision(repo, calls, decision):
    """A denied ask is still an ask; asking at all post-demotion is the violation."""
    alarm(repo)
    write_tape(repo, record(70, BEFORE, op="get_option_chain"),
               record(83, AFTER, decision=decision))
    assert watchdog.main(repo) == 2

    booted = [c[2] for c in calls if c[:2] == ["launchctl", "bootout"]]
    assert booted == BOOTOUTS
    assert not any("supervisor" in c or "check" in c for c in booted)
    assert calls[-1] == ["pkill", "-f", watchdog.STRAGGLER_PATTERN]

    lines = (repo / "state" / "KILLED").read_text().splitlines()
    assert watchdog.parse_ts(lines[0]) is not None
    assert lines[1] == f"seq 83 place_defined_risk_spread {decision} {AFTER}"
    assert lines[-1] == REASON


def test_unparseable_alarm_timestamp_fails_toward_killing(repo, calls):
    """No usable cutoff means every place attempt counts, including old ones."""
    alarm(repo, stamp="not-a-timestamp")
    write_tape(repo, record(9, BEFORE))
    assert watchdog.main(repo) == 2
    assert [c[2] for c in calls if c[:2] == ["launchctl", "bootout"]] == BOOTOUTS
    assert "seq 9 " in (repo / "state" / "KILLED").read_text()


def test_malformed_tape_lines_are_skipped_not_fatal(repo, calls):
    alarm(repo)
    write_tape(repo, "{not json", "", "[]", record(84, AFTER), "}{")
    assert watchdog.main(repo) == 2
    assert "seq 84 " in (repo / "state" / "KILLED").read_text()


def test_bootout_failure_does_not_stop_the_sweep(repo, monkeypatch):
    """bootout fails when a job is not loaded; that is fine and must not abort."""
    recorded: list[list[str]] = []
    monkeypatch.setattr(watchdog, "run_cmd",
                        lambda argv: (recorded.append(list(argv)), (3, "no such process"))[1])
    alarm(repo)
    write_tape(repo, record(85, AFTER))
    assert watchdog.main(repo) == 2
    assert len(recorded) == len(watchdog.DECISION_JOBS) + 1
    assert (repo / "state" / "KILLED").exists()


# --- idempotence -----------------------------------------------------------


def test_existing_killed_file_blocks_a_second_kill(repo, calls):
    alarm(repo)
    write_tape(repo, record(86, AFTER))
    original = "2026-08-27T14:16:00+00:00\nseq 86 place_defined_risk_spread deny\n"
    (repo / "state" / "KILLED").write_text(original)
    assert watchdog.main(repo) == 3
    assert calls == []
    assert (repo / "state" / "KILLED").read_text() == original
