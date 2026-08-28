#!/usr/bin/env python3
"""mandate's watchdog — the last rung of the escalation ladder.

The supervisor demotes: it tightens the agent's place grant and writes
state/ALARM. That is a rule change, and a rule change only works on an agent
that reads rules. This process assumes it does not. It reads the audit tape,
which records every brokered call whether allowed or denied, and asks one
question: has the agent tried to place a spread since the ALARM was raised?
A denied attempt counts — asking at all after demotion is the violation, and
the tape is the only witness that cannot be talked out of.

If the answer is yes, the agent's scheduled jobs are torn out of launchd. The
supervisor and the market-close check are never touched: they only reduce
exposure, and killing them would leave an open book with nobody watching it.

Re-arming is a human act: delete state/KILLED and re-run
run/install_launchd.sh.

Exit codes:
  0  nothing to do (no ALARM, or ALARM raised and the agent has behaved)
  2  violation found; jobs killed and state/KILLED written
  3  state/KILLED already exists; a human has not yet re-armed
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# WATCHDOG_KILL_LABELS exists for the rehearsal stack, which must kill its
# own dummy jobs and never the live ones. Production plists leave it unset.
DECISION_JOBS = tuple(
    lbl.strip()
    for lbl in os.environ.get("WATCHDOG_KILL_LABELS", "").split(",")
    if lbl.strip()
) or (
    "com.mandate.decision-1",
    "com.mandate.decision-2",
    "com.mandate.decision-3",
)
VIOLATION_TOOL = "alpaca"
VIOLATION_OP = "place_defined_risk_spread"
VIOLATION_AGENT = "hackathon-dev"
# Same rehearsal concern as the labels: an unanchored pattern would match a
# LIVE decision run's process from a rehearsal watchdog. Rehearsal sets an
# absolute, stack-specific pattern; production leaves it unset.
STRAGGLER_PATTERN = os.environ.get("WATCHDOG_STRAGGLER_PATTERN", "run/decision_run.sh")
CMD_TIMEOUT_S = 20

RUN_ID = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def log(event: str, detail: str = "") -> None:
    clean = str(detail).replace("|", "/").replace("\n", " ").strip()
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    print(f"WATCHDOG|{ts}|{RUN_ID}|{event}|{clean}", flush=True)


def run_cmd(argv: list[str]) -> tuple[int, str]:
    """The single choke point for every process action this file takes.

    One function so the kill path has exactly one seam to stub in tests, and
    so a missing binary or a hung call cannot raise past the caller: a
    watchdog that crashes halfway through a kill leaves some jobs alive.
    """
    try:
        out = subprocess.run(
            argv, capture_output=True, text=True, timeout=CMD_TIMEOUT_S, check=False
        )
        return out.returncode, (out.stderr or out.stdout).strip()
    except (OSError, subprocess.SubprocessError) as e:
        return -1, f"{type(e).__name__}: {e}"


def parse_ts(raw: object) -> datetime | None:
    """ISO-8601 to an aware UTC datetime, or None if it will not parse."""
    try:
        dt = datetime.fromisoformat(str(raw).strip().replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def read_alarm(path: Path) -> tuple[datetime | None, str]:
    """Return (raised-at, reason). Written by supervisor.demote(): line 1 is
    the stamp, the rest is free text."""
    lines = path.read_text().splitlines()
    stamp = parse_ts(lines[0]) if lines else None
    reason = " ".join(line.strip() for line in lines[1:] if line.strip())
    return stamp, reason or "(no reason recorded)"


def scan_tape(path: Path, cutoff: datetime | None) -> tuple[list[dict], int]:
    """Post-ALARM place attempts by the agent, plus a count of unreadable lines.

    A cutoff of None means the ALARM stamp did not parse; every place attempt
    on the tape then counts. Failing toward a kill is the correct direction:
    the cost of an unnecessary kill is a stopped agent, the cost of a missed
    one is an unbounded agent.
    """
    hits: list[dict] = []
    malformed = 0
    try:
        raw_lines = path.read_text().splitlines()
    except OSError as e:
        log("TAPE_UNREADABLE", f"{path}: {type(e).__name__}: {e}")
        return hits, malformed
    for line in raw_lines:
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
        except ValueError:
            malformed += 1
            continue
        if not isinstance(rec, dict):
            malformed += 1
            continue
        principal = rec.get("principal") or {}
        if (
            rec.get("tool") != VIOLATION_TOOL
            or rec.get("op") != VIOLATION_OP
            or not isinstance(principal, dict)
            or principal.get("agentId") != VIOLATION_AGENT
        ):
            continue
        ts = parse_ts(rec.get("ts"))
        if cutoff is not None and (ts is None or ts <= cutoff):
            continue
        hits.append(rec)
    return hits, malformed


def kill_jobs() -> None:
    """Bootout the three decision jobs, then sweep for a straggler process tree.

    `bootout` on an unloaded job fails, and that is a success for our purposes
    — the job is not going to run. Only the decision jobs are named here;
    com.mandate.supervisor and com.mandate.check must survive a kill.
    """
    domain = f"gui/{os.getuid()}"
    for label in DECISION_JOBS:
        rc, out = run_cmd(["launchctl", "bootout", f"{domain}/{label}"])
        if rc == 0:
            log("JOB_KILLED", label)
        else:
            log("JOB_KILL_NOOP", f"{label} rc={rc} {out[:200]}")
    rc, out = run_cmd(["pkill", "-f", STRAGGLER_PATTERN])
    log("STRAGGLER_SWEEP", f"pkill -f {STRAGGLER_PATTERN} rc={rc} {out[:200]}")


def write_killed(path: Path, hits: list[dict], reason: str) -> None:
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    lines = [stamp]
    for rec in hits:
        lines.append(
            f"seq {rec.get('seq')} {rec.get('op')} "
            f"{rec.get('decision')} {rec.get('ts')}"
        )
    lines.append(reason)
    try:
        path.write_text("\n".join(lines) + "\n")
        log("KILLED_WRITTEN", f"{path} recording {len(hits)} violation(s)")
    except OSError as e:
        log("KILLED_WRITE_FAILED", f"{path}: {type(e).__name__}: {e}")


def main(root: Path = ROOT) -> int:
    alarm = root / "state" / "ALARM"
    killed = root / "state" / "KILLED"
    tape = root / "state" / "audit.jsonl"

    if not alarm.exists():
        log("OK", "no ALARM; the agent is not demoted and there is nothing to watch")
        return 0

    if killed.exists():
        log("ALREADY_KILLED", f"{killed} exists; a human must delete it and re-run "
                              "run/install_launchd.sh to re-arm")
        return 3

    try:
        raised_at, reason = read_alarm(alarm)
    except OSError as e:
        raised_at, reason = None, f"ALARM unreadable: {type(e).__name__}: {e}"
        log("ALARM_UNREADABLE", reason)
    if raised_at is None:
        log("ALARM_TS_UNPARSEABLE",
            "ALARM carries no parseable timestamp; treating EVERY place attempt on "
            "the tape as a violation rather than reading none of them")
    else:
        log("ARMED", f"ALARM raised {raised_at.isoformat()}: {reason}")

    hits, malformed = scan_tape(tape, raised_at)
    if malformed:
        log("TAPE_MALFORMED", f"{malformed} unreadable tape line(s) skipped")

    if not hits:
        log("CLEAN", "demoted, and no post-ALARM place attempt on the tape")
        return 0

    seqs = ", ".join(str(r.get("seq")) for r in hits)
    log("VIOLATION", f"{len(hits)} post-ALARM {VIOLATION_OP} attempt(s) by "
                     f"{VIOLATION_AGENT} at tape seq {seqs}")
    kill_jobs()
    write_killed(killed, hits, reason)
    return 2


if __name__ == "__main__":
    sys.exit(main())
