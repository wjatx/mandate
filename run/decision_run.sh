#!/bin/bash
# mandate decision run. Usage: run/decision_run.sh <run-number>
#
# Three of these a day (charter §6). Each may open at most two new positions,
# and opening none is a successful run.
set -u
source "$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)/lib.sh"

RUN_N="${1:?usage: decision_run.sh <run-number>}"

preflight

CODA="This is decision run ${RUN_N} of the day at $(ct_now) CT. Review account, \
positions, and the market per the charter. You may open at most 2 new positions \
this run. A run that opens nothing is a successful run."

log "=== decision run ${RUN_N} starting ==="

# Upstream-outage retry (design item 32, first rung). Added 2026-09-03 after three
# consecutive quarter-hour firings died on "API Error: 529 Overloaded" before any
# tool call, while hand re-runs a few minutes later went through. A retry is safe
# only when the failed attempt touched nothing. The tape is append-only and every
# broker call appends a record, so an unchanged record count is the proof; the
# error text alone is not, because a 529 mid-run after an order would double-act.
# One retry, not a loop: two attempts plus the wait still fit inside the cadence
# interval's sentinel budget, and launchd skips a firing that overlaps rather than
# stacking it.
RETRY_WAIT_S="${RETRY_WAIT_S:-120}"
MAX_ATTEMPTS="${MAX_ATTEMPTS:-2}"
attempt=1
while :; do
  tape_before=$(wc -l < "$AGENT_TAPE" | tr -d " ")
  out="$(mktemp /tmp/mandate-run-out.XXXXXX)"
  charter_prompt "$CODA" | MCP_TIMEOUT=240000 claude -p --model "$AGENT_MODEL" \
    --mcp-config .mcp.json --strict-mcp-config \
    --disallowedTools "Edit,Write,NotebookEdit,Bash,Read,Glob,Grep,WebFetch,WebSearch,Agent,Task" \
    --allowedTools \
    "${BROKER_READ_TOOLS[@]}" \
    "${BROKER_EXIT_TOOLS[@]}" \
    "${BROKER_OPEN_TOOLS[@]}" > "$out" &
  AGENT_PID=$!
  # A hung agent would block every later run on this serialised schedule.
  timeout_sentinel "$AGENT_PID" &
  SENTINEL_PID=$!
  wait "$AGENT_PID"
  rc=$?
  kill "$SENTINEL_PID" 2>/dev/null || true
  cat "$out"
  tape_after=$(wc -l < "$AGENT_TAPE" | tr -d " ")
  if [ "$rc" -ne 0 ] && [ "$attempt" -lt "$MAX_ATTEMPTS" ] \
     && grep -q -E 'API Error: 5[0-9][0-9]|Overloaded' "$out" \
     && [ "$tape_before" -eq "$tape_after" ]; then
    log "RETRY: attempt ${attempt} died on an upstream API error before any broker call" \
        "(tape unchanged at ${tape_after} records); waiting ${RETRY_WAIT_S}s, then one more attempt."
    rm -f "$out"
    attempt=$((attempt + 1))
    sleep "$RETRY_WAIT_S"
    continue
  fi
  rm -f "$out"
  break
done

postflight "$rc"
exit "$rc"
