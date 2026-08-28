#!/bin/bash
# Re-key ceremony: the ONE sanctioned path for changing the enforcement
# surface (dollar caps, shim code, manifests, charter).
#
# What a re-key does, in order:
#   1. Shows the cap delta (signed lock -> manifest) and asks for confirmation.
#   2. Re-attests the grants under the new envelope hash (grants re-seed, both
#      principals) — until this step, the gateway quarantines every trading
#      grant at first exercise, which is the protection working.
#   3. Re-admits the shim's advertised tool set (snapshot -> bulk-propose ->
#      bulk-ratify), acknowledging the place_defined_risk_spread description
#      delta, which embeds the enforced caps and envelope hash on purpose.
#   4. Writes the HMAC-signed charter lock and chains a record with the old
#      and new cap values into state/rekey-log.jsonl.
#
# Usage: bin/rekey.sh "why this re-key happened"
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
NOTE="${1:?usage: bin/rekey.sh \"why this re-key happened\"}"
PY="$ROOT/.venv/bin/python"
SNAPSHOT="$(mktemp -t rekey-snapshot)"
trap 'rm -f "$SNAPSHOT"' EXIT

echo "== re-key: current vs signed =="
"$PY" - <<'EOF'
import json, sys, yaml
from pathlib import Path
sys.path.insert(0, "shim")
from defined_risk import caps_from_manifest

caps = caps_from_manifest(yaml.safe_load(Path("manifest.yaml").read_text()))
try:
    lock = json.loads(Path("state/charter.lock").read_text())
    old = lock["caps"]
except (FileNotFoundError, ValueError, KeyError):
    old = {}
    print("no existing lock — this is the first re-key")
for name, new in (
    ("max_loss_per_position_usd", caps.max_loss_per_position_usd),
    ("max_total_open_risk_usd", caps.max_total_open_risk_usd),
):
    was = old.get(name)
    marker = "->" if was != new else "=="
    print(f"  {name}: {was} {marker} {new}")
print(f"  envelope: {caps.envelope_hash}")
EOF

printf 'Type "rekey" to attest this surface: '
read -r CONFIRM
if [ "$CONFIRM" != "rekey" ]; then
  echo "aborted: confirmation not given" >&2
  exit 1
fi

# BROKER_LOCAL_IDENTITY names each half of the ceremony on the local store
# arm. One operator holds both halves here, and the store records exactly
# that — the honest local-solo posture the 2026-08-25 bring-up used.
echo "== grants re-seed (trading principal) =="
( source state/env.sh && BROKER_LOCAL_IDENTITY=maker \
  "$PY" -m safe_agents.broker.grants.commands re-seed )

echo "== grants re-seed (supervisor principal) =="
( source state/env-supervisor.sh && BROKER_LOCAL_IDENTITY=maker \
  "$PY" -m safe_agents.broker.grants.commands re-seed )

echo "== tool re-admission (snapshot -> propose -> ratify) =="
PROPOSE_OUT="$(mktemp -t rekey-propose)"
trap 'rm -f "$SNAPSHOT" "$PROPOSE_OUT"' EXIT
( source state/env.sh &&
  "$PY" -m safe_agents.broker.mcp.commands snapshot \
    --manifest manifest.yaml --server-id alpaca --out "$SNAPSHOT" &&
  BROKER_LOCAL_IDENTITY=maker "$PY" -m safe_agents.broker.mcp.commands bulk-propose \
    --manifest manifest.yaml --snapshot "$SNAPSHOT" --ttl-hours 1 ) | tee "$PROPOSE_OUT"

# An --acknowledge-description-change flag naming a tool with NO pending delta
# is refused by bulk-ratify (an unused ack would be a standing pre-approval),
# so the ack list is derived from what the propose diff actually flagged.
DRIFTED="$(awk '/^=== / {tool=$2} /status: DRIFT/ {print tool}' "$PROPOSE_OUT")"
if [ -z "$DRIFTED" ]; then
  echo "no drifted tools; skipping ratify (nothing pending)"
else
  ACK_FLAGS=()
  for tool in $DRIFTED; do
    ACK_FLAGS+=(--acknowledge-description-change "$tool")
  done
  ( source state/env.sh &&
    BROKER_LOCAL_IDENTITY=checker "$PY" -m safe_agents.broker.mcp.commands bulk-ratify \
      --manifest manifest.yaml --server-id alpaca --yes "${ACK_FLAGS[@]}" )
fi

echo "== charter lock =="
"$PY" tools/charter_lock.py write --note "$NOTE"

echo "re-key complete. The next run starts under the attested surface."
