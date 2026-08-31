# Audit tapes

Every call the agent or the supervisor makes goes through a broker process that
holds the API keys. The broker decides each call against a signed grant and
writes one record here before returning. These two files are those records.

- `audit.jsonl` — 142 records written for the trading agent.
- `audit-supervisor.jsonl` — 276 records written for the exit supervisor,
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
   these land in `shim_refusals.jsonl` (3 records) instead.

`shim_refusals.jsonl` is **not hash-chained** and carries no integrity claim;
it is an ordinary log. We publish it because the chained tape alone would show
one refusal when the system actually made several, and showing the smaller
number would misrepresent the record in our own favour. Putting shim refusals
onto the chain is a known gap in the design, not a property of it.
