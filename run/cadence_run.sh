#!/bin/bash
# Half-hourly decision run (charter §6, 2026-08-31 cadence amendment).
#
# Fired by com.mandate.cadence.plist at twelve slots, 8:45 through 14:15 CT.
# The 14:45 slot is deliberately absent: that is the position-check run's, and
# two acting runs spawning gateways at the same minute would contend.
#
# Two guards, both fail-closed, so a forgotten plist can never run an
# unauthorized cadence: the amendment's window ends with the contest, and any
# firing outside the charter's stated hours refuses rather than acts.
set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd)"
LOG_TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

TODAY="$(TZ=America/Chicago date +%F)"
if [[ "$TODAY" > "2026-09-04" ]]; then
  echo "[$LOG_TS] REFUSE: the §6 half-hourly cadence window ended 2026-09-04." \
       "Unload com.mandate.cadence or extend it by ceremony."
  exit 0
fi

HHMM="$(TZ=America/Chicago date +%H%M)"
# 10# forces base ten: a zero-padded "0845" is octal-invalid without it.
if (( 10#$HHMM < 845 || 10#$HHMM > 1415 )); then
  echo "[$LOG_TS] REFUSE: $HHMM CT is outside the §6 cadence hours (0845-1415)."
  exit 0
fi

exec "$ROOT/run/decision_run.sh" "run-$HHMM"
