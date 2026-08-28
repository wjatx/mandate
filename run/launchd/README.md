# launchd jobs

Seven plists. `run/install_launchd.sh` installs and loads the six standing
jobs; nothing else should. The calibration job is temporary, loaded by hand,
and refuses to run outside its charter window.

| Label | When (CT, weekdays) | Runs |
|---|---|---|
| `com.mandate.decision-1` | 09:15 | `run/decision_run.sh 1` |
| `com.mandate.decision-2` | 12:00 | `run/decision_run.sh 2` |
| `com.mandate.decision-3` | 14:15 | `run/decision_run.sh 3` |
| `com.mandate.check` | 14:45 | `run/check_run.sh` |
| `com.mandate.supervisor` | every 15 min, 08:30–15:00 | `supervisor/supervisor.py` |
| `com.mandate.watchdog` | every 3 min (StartInterval) | `watchdog/watchdog.py` |
| `com.mandate.calibration` | :15/:45 slots, 08:45–11:45 | `run/calibration_run.sh` (temporary; self-expires 2026-08-28) |

The watchdog is the one deliberate exception to the StartCalendarInterval
argument below: its pass is two local file reads with no gateway spawn, so
around-the-clock wakes cost nothing, and a fixed 3-minute interval is the
point — the kill must not wait for market hours.

## Why StartCalendarInterval and not StartInterval

The supervisor plist carries 145 explicit calendar entries (29 times × 5
weekdays) instead of `StartInterval: 900` plus a market-hours guard in the
script. That is more XML, and it is the right trade:

- `StartInterval` fires around the clock. The supervisor would wake at 3 a.m.
  and on Sundays, and each wake spawns a broker gateway which spawns the
  vendor MCP server which calls Alpaca — a real cost for a guaranteed no-op.
- With `StartInterval`, the actual schedule lives in a conditional inside the
  script, where it is invisible to `launchctl list` and has to be correct.
  With calendar entries the schedule is declarative: what launchd is going to
  do is what the plist says, and it can be audited without reading Python.
- launchd handles DST for calendar entries. A wall-clock guard in the script
  would have to.

The cost of being wrong is asymmetric in the usual direction: an extra 3 a.m.
wake is wasted money, a missed 14:30 pass is an unmanaged position.

## Local time

launchd calendar entries are **local** time, and these encode CT. The host is
on `America/Chicago`; `install_launchd.sh` refuses to install if it is not.

## Known: the window runs past the close

RESOLVED 2026-08-25: the original 15:30 CT check-run time was an ET/CT slip (it would have landed after the 15:00 CT close). Times are now decision-3 at 14:15 CT, check run at 14:45 CT, supervisor window 08:30-15:00 CT - every run inside the session. Charter section 6 was updated to match.

## Kill switch

`touch state/ALARM` stops both run scripts at their preflight without
unloading anything. The supervisor deliberately keeps running — exits must
keep working while the agent is demoted.
