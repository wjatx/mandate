#!/bin/bash
# Calibration-cadence decision run (charter §6 calibration amendment).
# Fired by com.mandate.calibration.plist at the half-hour slots. The charter
# window is finite; outside it this wrapper refuses so a forgotten plist can
# never run an unauthorized cadence.
set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd)"

TODAY="$(TZ=America/Chicago date +%F)"
if [[ "$TODAY" > "2026-08-28" ]]; then
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] REFUSE: calibration cadence window (charter §6)" \
       "ended 2026-08-28; unload com.mandate.calibration or extend by ceremony."
  exit 0
fi

exec "$ROOT/run/decision_run.sh" "cal-$(TZ=America/Chicago date +%H%M)"
