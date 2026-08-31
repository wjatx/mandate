#!/usr/bin/env python3
"""Publish the audit tapes so anyone can verify them.

    python3 tools/export_tape.py

Copies the broker's two hash-chained tapes out of state/ (which is gitignored,
because it also holds keys and ledgers) into tape/, which is committed. Writes
tape/README.md describing what the records are and how to check them.

Publishing is safe by construction rather than by redaction: the broker records
the SHA-256 DIGEST of each call's arguments and result, never the values. So a
record says "this principal asked for this op and the broker allowed it" without
carrying the order, the position, or anything else. Redacting would break the
chain; there is nothing here to redact.

The exporter refuses to publish a tape that does not verify, so a corrupted
file cannot be shipped by accident.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAPES = (
    ("state/audit.jsonl", "tape/audit.jsonl", "agent", "the trading agent"),
    (
        "state/audit-supervisor.jsonl",
        "tape/audit-supervisor.jsonl",
        "supervisor",
        "the deterministic exit supervisor",
    ),
)

# Not a chained tape: the defined-risk shim runs inside the admitted connector,
# so its refusals are tool-level results rather than broker decisions, and they
# land in this sidecar. Published alongside because otherwise the record shows
# only one of the refusals the system actually made.
SIDECAR = ("state/shim_refusals.jsonl", "tape/shim_refusals.jsonl")

README = """# Audit tapes

Every call the agent or the supervisor makes goes through a broker process that
holds the API keys. The broker decides each call against a signed grant and
writes one record here before returning. These two files are those records.

- `audit.jsonl` — {agent_n} records written for the trading agent.
- `audit-supervisor.jsonl` — {sup_n} records written for the exit supervisor,
  a separate principal with its own grant and no order-placing operation.

## Verify them yourself

```
python3 tools/verify_tape.py tape/audit.jsonl
python3 tools/verify_tape.py tape/audit-supervisor.jsonl
```

No credentials, no network, no dependencies beyond the Python standard library.
Each record carries the SHA-256 of every field of the record before it, so
editing a field, dropping a record, or reordering two makes every later hash
stop matching. The chain is unkeyed, which is what lets anyone check it.

**What that proves, exactly:** the file is self-consistent. Nothing was edited,
dropped, or reordered in place. **What it does not prove:** anything about
tampering. We hold the writer, so we could rewrite the whole file and recompute
every hash. Real tamper-evidence needs a witness we do not control, such as
off-device append-only storage. We have not built that, and we would rather
state the boundary than imply a guarantee the mechanism does not deliver.

## Why publishing these is safe

The broker stores the digest of each call's arguments and result, never the
values (`argsDigest`, `resultDigest`). A record shows who asked for which
operation and what was decided, and carries no order details, positions, or
secrets. Nothing is redacted, because redaction would break the chain and there
is nothing here that needs it.

## What to look for

`decision` is the broker's ruling on each call. The interesting ones are the
refusals: an operation absent from the manifest is refused because no entry for
it exists at all, a tool not granted to that principal is refused as
out-of-grant, and a grant whose envelope hash no longer matches is quarantined
until the re-key ceremony re-attests it.

## Two refusal layers, and why one is not on the tape

Refusals happen in two places, and only the first is on the chain.

1. **The broker gate** decides whether a call is allowed at all, and writes its
   ruling to the tape above. `no manifest entry for alpaca.place_stock_order`
   is this layer: the operation is structurally absent from the admitted
   surface.
2. **The defined-risk shim** runs *inside* the admitted connector and refuses
   orders whose maximum loss it cannot compute or that exceed a signed cap. To
   the broker this is a tool returning a result, not a decision it makes, so
   these land in `shim_refusals.jsonl` ({shim_n} records) instead.

`shim_refusals.jsonl` is **not hash-chained** and carries no integrity claim;
it is an ordinary log. We publish it because the chained tape alone would show
one refusal when the system actually made several, and showing the smaller
number would misrepresent the record in our own favour. Putting shim refusals
onto the chain is a known gap in the design, not a property of it.
"""


def verify(path: Path) -> bool:
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "verify_tape.py"), str(path)],
        capture_output=True,
        text=True,
    )
    sys.stdout.write(result.stdout)
    return result.returncode == 0


def main() -> int:
    out_dir = ROOT / "tape"
    out_dir.mkdir(exist_ok=True)
    counts = {}

    for src_rel, dst_rel, key, _desc in TAPES:
        src, dst = ROOT / src_rel, ROOT / dst_rel
        if not src.exists():
            print(f"FAIL: {src_rel} does not exist; nothing to export.")
            return 2
        if not verify(src):
            print(f"FAIL: {src_rel} does not verify; refusing to publish it.")
            return 1
        dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        counts[key] = sum(1 for line in dst.read_text().splitlines() if line.strip())
        print(f"exported {src_rel} -> {dst_rel}")

    src, dst = ROOT / SIDECAR[0], ROOT / SIDECAR[1]
    if src.exists():
        dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        counts["shim"] = sum(1 for line in dst.read_text().splitlines() if line.strip())
        print(f"exported {SIDECAR[0]} -> {SIDECAR[1]} (unchained sidecar)")
    else:
        counts["shim"] = 0
        print(f"note: {SIDECAR[0]} does not exist; no shim refusals to publish.")

    (out_dir / "README.md").write_text(
        README.format(
            agent_n=counts["agent"],
            sup_n=counts["supervisor"],
            shim_n=counts["shim"],
        ),
        encoding="utf-8",
    )
    print(f"wrote tape/README.md ({counts['agent']} agent, "
          f"{counts['supervisor']} supervisor, {counts['shim']} shim records)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
