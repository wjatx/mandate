#!/bin/bash
# Install mandate's seven launchd jobs. NOT run as part of any build — a human
# runs this deliberately, once, when the schedule should actually start.
#
#   run/install_launchd.sh            install and load
#   run/install_launchd.sh --unload   stop and remove
#
# The plists in run/launchd/ are the source of truth and are tracked; the
# copies under ~/Library/LaunchAgents are disposable.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd)"
SRC="$ROOT/run/launchd"
DEST="$HOME/Library/LaunchAgents"
JOBS=(
  com.mandate.research
  com.mandate.decision-1
  com.mandate.decision-2
  com.mandate.decision-3
  com.mandate.check
  com.mandate.supervisor
  com.mandate.watchdog
)

mkdir -p "$DEST" "$ROOT/state/logs"

if [ "${1:-}" = "--unload" ]; then
  for job in "${JOBS[@]}"; do
    launchctl unload "$DEST/$job.plist" 2>/dev/null || true
    rm -f "$DEST/$job.plist"
    echo "removed $job"
  done
  echo "All mandate jobs unloaded. The agent is no longer on a timer."
  exit 0
fi

# These schedules are LOCAL time and the charter's cadence is stated in CT, so
# the host must be on Central or every run fires at the wrong moment.
tz="$(readlink /etc/localtime | sed 's#.*/zoneinfo/##')"
if [ "$tz" != "America/Chicago" ]; then
  echo "REFUSING: launchd schedules are local time and these plists encode CT," >&2
  echo "          but this host is on '$tz'. Every run would fire at the wrong" >&2
  echo "          time. Set the host to America/Chicago or regenerate the plists." >&2
  exit 1
fi

for job in "${JOBS[@]}"; do
  plutil -lint "$SRC/$job.plist" > /dev/null
  cp "$SRC/$job.plist" "$DEST/$job.plist"
  launchctl unload "$DEST/$job.plist" 2>/dev/null || true
  launchctl load "$DEST/$job.plist"
  echo "loaded $job"
done

echo
echo "mandate is now on a timer. Logs: $ROOT/state/logs/"
echo "Stop everything with: run/install_launchd.sh --unload"
echo "Kill switch without unloading: touch $ROOT/state/ALARM"
