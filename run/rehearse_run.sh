#!/bin/bash
# Rehearsal run: a real decision run with the order-placing tools withheld.
#
# Usage: run/rehearse_run.sh "why we are rehearsing"
#
# The agent reads live market data through the gateway, declares its IV regime,
# reasons to a sized proposal under the charter currently in force, and then
# cannot place anything, because place_defined_risk_spread is not in its
# allowed-tools list for this invocation. The exit tools are withheld too: a
# rehearsal must not close a live position either.
#
# What this is for: finding out whether a freshly amended charter actually
# produces sane behavior, BEFORE the amended rules meet a live decision run on
# a trading morning. It answers "do these rules work together" without an order
# reaching the venue.
#
# What it is NOT: a substitute for the gate. Withholding a tool from the prompt
# is a harness-level restriction, not an enforcement one. The broker would still
# refuse anything out of grant; this simply means the agent never gets to ask.
# Never present a rehearsal as evidence that the enforcement surface works —
# that is what tools/refusal_drill.py is for, and it exercises the real path.
#
# The run's reasoning lands in this log like any other. It writes no orders, and
# because nothing is placed the risk ledger is untouched.
set -u
source "$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)/lib.sh"

WHY="${1:?usage: rehearse_run.sh \"why we are rehearsing\"}"

preflight

CODA="REHEARSAL RUN at $(ct_now) CT. Reason exactly as you would on a live \
decision run under the charter above: review the account, the positions and the \
market, declare your IV regime per section 3, and state the proposal you would \
place, with its structure, strikes, size and the dollar risk it carries. \
Then stop. The order-placing and position-closing tools are deliberately \
withheld from this invocation, so you cannot act and should not try. Reason \
about what you WOULD do at full size under the rules now in force. If the rules \
as written would leave you unable to act, say so plainly and name the rule that \
binds — that is the single most useful thing this rehearsal can tell the \
operator. Rehearsal context: ${WHY}"

log "=== REHEARSAL run starting (no open or exit tools) — ${WHY} ==="

charter_prompt "$CODA" | MCP_TIMEOUT=240000 claude -p --model "$AGENT_MODEL" \
  --mcp-config .mcp.json --strict-mcp-config \
  --allowedTools \
  "${BROKER_READ_TOOLS[@]}"
rc=$?

log "=== REHEARSAL complete (exit $rc); nothing was placed ==="

# Tape verification only. The dashboard and the record cross-check both assume a
# run that could act; a rehearsal has no ledger effect for them to check.
if verify_tape > /tmp/mandate-rehearsal-tape.$$ 2>&1; then
  log "postflight: tape still verifies."
else
  log "!! TAPE VERIFICATION FAILED AFTER THIS REHEARSAL — stop and look."
  sed 's/^/        | /' /tmp/mandate-rehearsal-tape.$$
fi
rm -f /tmp/mandate-rehearsal-tape.$$

exit "$rc"
