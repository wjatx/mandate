#!/bin/sh
# Broker gateway launcher: sources the env floor, execs the gateway.
# stdout is the MCP protocol; ready banner on stderr.
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
. "$ROOT/state/env.sh"
exec "$ROOT/.venv/bin/python" -m safe_agents.broker.gateway
