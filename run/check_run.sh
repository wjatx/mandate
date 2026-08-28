#!/bin/bash
# mandate 14:45 CT position-check run (charter §6; 15:45 ET, inside the session).
#
# This run reviews the book and closes what the exit rules require. It opens
# nothing — and it is not merely TOLD that. place_defined_risk_spread is left
# out of --allowedTools entirely, so "open no new positions" is a property of
# the surface rather than an instruction the model has to keep remembering.
# The prompt says it too; the two agree, and only one of them can be argued
# with. (The broker still gates the op regardless; this is the cheap outer
# layer, not the enforcement.)
set -u
source "$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)/lib.sh"

preflight

CODA="This is the 14:45 CT position-check run, the last run before the close. Open NO new positions. Review \
every open position against the charter's exits and close what the rules require."

log "=== position-check run starting ==="

charter_prompt "$CODA" | MCP_TIMEOUT=240000 claude -p \
  --mcp-config .mcp.json --strict-mcp-config \
  --allowedTools \
  "${BROKER_READ_TOOLS[@]}" \
  "${BROKER_EXIT_TOOLS[@]}"
rc=$?

postflight "$rc"
exit "$rc"
