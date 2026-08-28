"""Charter lock — HMAC-signed pin of the enforcement and instruction surface.

The broker's envelope hash protects the caps *values* (a change quarantines
the grants), but nothing upstream measures the shim's *code* or the charter's
*prose* — a filesystem write could alter either silently. This tool closes
that gap at our floor: `write` records sha256 digests of the pinned files plus
the caps in force, signs the record with the broker HMAC key, and chains it
into an append-only re-key log with the old and new cap values side by side;
`verify` recomputes and refuses on any mismatch. The run preflight and the
supervisor call `verify` before acting.

Honest boundary: this is tamper-EVIDENCE, not tamper-proofing. An editor who
also holds the HMAC key can re-sign whatever they like; the point is that a
change through any normal path either re-keys deliberately (leaving a signed,
chained record of exactly what moved) or stops the next run.

Usage:
    charter_lock.py write --note "why"    # re-key: pin current state
    charter_lock.py verify                # exit 0 clean, 1 mismatch, 2 no lock
"""

from __future__ import annotations

import argparse
import hashlib
import hmac as hmac_mod
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOCK_PATH = ROOT / "state" / "charter.lock"
LOG_PATH = ROOT / "state" / "rekey-log.jsonl"
KEY_PATH = ROOT / "state" / "hmac.key"

# The surface a re-key attests: the risk gate's code, both manifests (caps,
# admitted tools, spawn commands), and the charter the model is prompted with.
# Orchestration scripts are deliberately out of scope — pinning everything
# breeds re-key fatigue, and the gate/instructions are where the money moves.
PINNED_FILES = [
    "shim/alpaca_shim.py",
    "shim/defined_risk.py",
    "manifest.yaml",
    "supervisor-manifest.yaml",
    "CHARTER.md",
]


def _sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _canonical(record: dict) -> bytes:
    return json.dumps(record, sort_keys=True, separators=(",", ":")).encode()


def _sign(record: dict) -> str:
    key = KEY_PATH.read_bytes().strip()
    return hmac_mod.new(key, _canonical(record), hashlib.sha256).hexdigest()


def _current_state() -> dict:
    import yaml

    sys.path.insert(0, str(ROOT / "shim"))
    from defined_risk import caps_from_manifest

    caps = caps_from_manifest(yaml.safe_load((ROOT / "manifest.yaml").read_text()))
    return {
        "files": {rel: _sha256(ROOT / rel) for rel in PINNED_FILES},
        "caps": {
            "max_loss_per_position_usd": caps.max_loss_per_position_usd,
            "max_total_open_risk_usd": caps.max_total_open_risk_usd,
        },
        "envelope_hash": caps.envelope_hash,
    }


def _read_lock() -> dict | None:
    try:
        return json.loads(LOCK_PATH.read_text())
    except (FileNotFoundError, ValueError):
        return None


def write(note: str) -> int:
    state = _current_state()
    previous = _read_lock()
    record = {
        "ts": datetime.now(UTC).isoformat(),
        "note": note,
        **state,
        "previous_caps": previous.get("caps") if previous else None,
        "prev": previous.get("hmac") if previous else None,
    }
    record["hmac"] = _sign({k: v for k, v in record.items() if k != "hmac"})
    LOCK_PATH.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    with LOG_PATH.open("a") as log:
        log.write(json.dumps(record, sort_keys=True) + "\n")
    old = record["previous_caps"] or {}
    for cap, new_value in record["caps"].items():
        old_value = old.get(cap)
        if old_value != new_value:
            print(f"[rekey] {cap}: {old_value} -> {new_value}")
        else:
            print(f"[rekey] {cap}: {new_value} (unchanged)")
    print(f"[rekey] envelope {record['envelope_hash']}")
    print(f"[rekey] lock written and chained ({LOCK_PATH.relative_to(ROOT)})")
    return 0


def verify() -> int:
    lock = _read_lock()
    if lock is None:
        print(
            "charter-lock: no lock at state/charter.lock — run bin/rekey.sh once "
            "to pin the current surface",
            file=sys.stderr,
        )
        return 2
    body = {k: v for k, v in lock.items() if k != "hmac"}
    if not hmac_mod.compare_digest(_sign(body), lock.get("hmac", "")):
        print("charter-lock: HMAC mismatch — the lock file itself was altered", file=sys.stderr)
        return 1
    state = _current_state()
    failures = []
    for rel, digest in state["files"].items():
        if lock["files"].get(rel) != digest:
            failures.append(f"{rel}: content differs from the signed lock")
    for absent in set(lock["files"]) - set(state["files"]):
        failures.append(f"{absent}: pinned but no longer present")
    if lock["envelope_hash"] != state["envelope_hash"]:
        failures.append(
            f"envelope hash {state['envelope_hash']} != signed {lock['envelope_hash']}"
        )
    if failures:
        for failure in failures:
            print(f"charter-lock: {failure}", file=sys.stderr)
        print(
            "charter-lock: the enforcement surface changed without a re-key. "
            "If deliberate, run bin/rekey.sh; if not, stop and investigate.",
            file=sys.stderr,
        )
        return 1
    print(
        f"charter-lock: verified — caps ${state['caps']['max_loss_per_position_usd']:,.0f}"
        f"/${state['caps']['max_total_open_risk_usd']:,.0f}, "
        f"{len(state['files'])} files pinned, signed {lock['ts']}"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    write_parser = sub.add_parser("write", help="re-key: pin and sign the current surface")
    write_parser.add_argument("--note", required=True, help="why this re-key happened")
    sub.add_parser("verify", help="check the surface against the signed lock")
    args = parser.parse_args()
    return write(args.note) if args.command == "write" else verify()


if __name__ == "__main__":
    sys.exit(main())
