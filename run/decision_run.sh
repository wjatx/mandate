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

charter_prompt "$CODA" | MCP_TIMEOUT=240000 claude -p \
  --mcp-config .mcp.json --strict-mcp-config \
  --allowedTools \
  "${BROKER_READ_TOOLS[@]}" \
  "${BROKER_EXIT_TOOLS[@]}" \
  "${BROKER_OPEN_TOOLS[@]}"
rc=$?

postflight "$rc"
exit "$rc"
