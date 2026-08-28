# mandate

An AI agent that trades options on an Alpaca paper account with no human in the
loop, built to show off a safety architecture rather than a strategy. The
strategy is a written charter ([CHARTER.md](CHARTER.md)) loaded at the start of
every run. Everything else is the wrapping: the agent never holds an API key
and never talks to the broker directly. Every call goes through a gateway that
serves only tools a human admitted through a two-key ceremony, checks every
order against dollar caps signed into a locked envelope, and writes every
request, grant, and refusal to an append-only audit tape.

Built for a trading hackathon on [safe-agents](https://github.com/wjatx/ptc-gal-reference).

NOTE: This project contains code that was written with AI.

## How a trading day runs

Scheduled `claude -p` runs wake the agent a few times a day. Each run reloads
the charter, reads the market through the gateway, and either acts inside its
caps or stands down with reasons on the record. Between runs, a deterministic
supervisor with no model in it holds the exits: it compares live position
values against the take-profit and stop values stamped into a ledger at entry,
and closes what the stored rules require. If the agent process dies, the
supervisor keeps running on its own timer under its own principal, whose
manifest contains no order-placing operation of any kind.

The order path itself is a defined-risk shim. The only acting operation the
agent can reach refuses any structure whose maximum loss is not computable,
any position over the per-position cap, and any order that would push the
book's total open risk over the book cap. The caps are enforced in the shim
and signed into the charter lock; changing the caps, the shim, the manifests,
or the charter without the re-key ceremony quarantines every trading grant
before the next run acts.

## The record, and its honest boundary

The live dashboard, rebuilt from the tape after each run, is at
[wjatx.github.io/mandate/dashboard](https://wjatx.github.io/mandate/dashboard/).

Two different guarantees back the record, and neither is "tamper-proof":

- The audit tape is a hash-chained, self-consistent record. Verification
  proves no record was edited, dropped, or reordered in place. It does not
  prove more: anyone who can write the file can rewrite it whole and recompute
  every hash. Stronger claims need off-device append-only storage, which this
  build does not use.
- The charter lock is tamper-evidence, not tamper-proofing. An editor who also
  holds the HMAC key can re-sign whatever they like. The point is that a
  change through any normal path either re-keys deliberately, leaving a
  signed and chained record of exactly what moved, or stops the next run.

## Reproducing it

Everything here runs against an Alpaca paper account. The floor is a Python
3.12 venv with `safe-agents[mcp]` installed from the tag this stack runs,
credentials in a broker-side secrets file the agent never reads, and the
bootstrap ceremony (snapshot, propose, ratify, seed, lock) run once before the
schedules arm. The run scripts and launchd schedules in [run/](run/) are the
exact ones the machine is on.

## License

MIT, copyright Wes Jackson. See [LICENSE](LICENSE).
