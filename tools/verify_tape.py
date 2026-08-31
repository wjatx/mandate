#!/usr/bin/env python3
"""Verify a published mandate audit tape. Standard library only, no secrets.

    python3 tools/verify_tape.py tape/audit.jsonl

The broker writes one record per brokered call: who asked, which tool and op,
what it decided, and what happened. Each record carries the SHA-256 of every
field of the record before it, so the file is a hash chain. Change a field,
drop a record, or reorder two, and every hash from that point on stops
matching.

WHAT THIS PROVES: the file is SELF-CONSISTENT. No record was edited, dropped,
or reordered in place.

WHAT IT DOES NOT PROVE: anything about tampering. Anyone who can write this
file can rewrite it whole and recompute every hash, and we hold the writer.
Calling a hash chain "tamper-evident" overstates it on its own; evidence
requires a witness we do not control, such as off-device append-only storage.
We have not built that. The claim we make is self-consistency and no more.

The chain is plain SHA-256 with no secret key, which is what makes this script
runnable by anyone. Verification needs no credential, no network, and nothing
from this repository except the tape itself.
"""

from __future__ import annotations

import hashlib
import json
import sys

GENESIS_PREV_HASH = "sha256:" + hashlib.sha256(b"").hexdigest()

# Fields the writer omits from the hash when they are null, so that records
# predating the receipt fields hash identically to ones that carry them.
RECEIPT_FIELDS = ("intentId", "storedCallDigest", "resultDigest")

# The exact field set the broker hashes, in the order it builds them. 'hash'
# is excluded: it is the output, not an input.
HASHED_FIELDS = (
    "seq", "ts", "principal", "tool", "op", "argsDigest", "decision",
    "reason", "envelopeHash", "approvedBy", "outcome", "error", "seed",
    "intentId", "storedCallDigest", "resultDigest", "prevHash",
)


def hash_record(record: dict) -> str:
    """Recompute a record's hash exactly as safe_agents.broker.audit does."""
    fields = {k: record.get(k) for k in HASHED_FIELDS}
    fields = {
        k: v for k, v in fields.items() if not (k in RECEIPT_FIELDS and v is None)
    }
    serialized = json.dumps(
        fields, sort_keys=True, separators=(",", ":"), default=str
    ).encode()
    return "sha256:" + hashlib.sha256(serialized).hexdigest()


def verify(path: str) -> int:
    try:
        with open(path, encoding="utf-8") as fh:
            records = [json.loads(line) for line in fh if line.strip()]
    except FileNotFoundError:
        print(f"FAIL: no tape at {path}")
        return 2
    except json.JSONDecodeError as exc:
        print(f"FAIL: {path} is not one JSON record per line: {exc}")
        return 2

    if not records:
        print(f"FAIL: {path} is empty")
        return 2

    expected_seq = records[0]["seq"]
    prev_hash = GENESIS_PREV_HASH if expected_seq == 0 else records[0]["prevHash"]
    if expected_seq != 0:
        print(f"note: tape starts at seq {expected_seq}, so this is a suffix of "
              f"the full chain; linkage is checked from there forward.")

    for record in records:
        seq = record.get("seq")
        if seq != expected_seq:
            print(f"FAIL: seq gap — expected {expected_seq}, found {seq}. "
                  f"A record was deleted or reordered.")
            return 1
        expected_seq += 1

        if record.get("prevHash") != prev_hash:
            print(f"FAIL: prevHash mismatch at seq={seq}. This record does not "
                  f"follow the one before it.")
            return 1

        computed = hash_record(record)
        if computed != record.get("hash"):
            print(f"FAIL: hash mismatch at seq={seq}. A field was modified "
                  f"after the record was written.")
            return 1
        prev_hash = record["hash"]

    first, last = records[0], records[-1]
    decisions: dict[str, int] = {}
    for r in records:
        decisions[r.get("decision", "?")] = decisions.get(r.get("decision", "?"), 0) + 1
    tally = ", ".join(f"{v} {k}" for k, v in sorted(decisions.items()))

    print(f"OK: {len(records)} records verify as an intact chain.")
    print(f"    {first['ts']}  ->  {last['ts']}")
    print(f"    decisions: {tally}")
    print(f"    final hash: {last['hash']}")
    print("    Proves SELF-CONSISTENCY only: no record was edited, dropped or")
    print("    reordered in place. Anyone who can write this file can rewrite it")
    print("    whole and recompute every hash, so this is not tamper-evidence.")
    return 0


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2
    return verify(argv[1])


if __name__ == "__main__":
    sys.exit(main(sys.argv))
