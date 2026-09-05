# mandate: one-page write-up

Written 2026-09-03 for the hackathon submission, which asked for a one-page write-up
covering AI logic, risk gates and Alpaca infrastructure but had no form field for it. It
describes the record through 2026-09-03. The final day is in the README.

mandate is an autonomous options-trading agent on an Alpaca paper account. The strategy
is a written charter. The safety lives outside the model: a broker gateway that serves
only human-admitted tools, dollar caps signed into a locked envelope, a deterministic
supervisor that holds exits between runs, and hash-chained audit tapes that record every
grant and every refusal. Built on safe-agents, an open-source library for this problem.

## AI logic

The charter is the prompt. Every scheduled run reloads it and applies it to the market
in front of it. One read-only research pass a day writes a memo with a directional
verdict for each admitted name, one of up, down, range-bound or two-sided, each with the
level or event that would falsify it. The memo is labelled data, not instructions, and
nothing in it can authorize a trade.

Decision runs fire every thirty minutes during the session. Each one measures the
volatility regime itself, as at-the-money implied volatility over twenty-day realized,
read on the expiry of the structure it is considering. The regime and the verdict together
pick the structure: credit verticals on a directional verdict, an iron condor on a
two-sided or range-bound one, a debit pair when the regime says premium is cheap. Sizing
follows the regime. A run that finds nothing allowable files an inaction request with its
reasons, and a human approves it. Runs propose watchlist items in their printed record; an
operator transcribes them, because the runs cannot write files.

## Risk gates

The agent never holds an API key. Every call goes through the gateway, which admits only
tools a human accepted through a two-key ceremony. The one order-placing operation is a
defined-risk shim that stands in for the vendor's raw order tool. It refuses any structure
whose maximum loss it cannot compute, any position over $5,000 of maximum loss, any order
that would push the book past $85,000, and any spread that would offset a held position.

The caps are data, not code. They ride the envelope hash in every grant, and an HMAC lock
pins the charter text, the shim source and both manifests. Changing any of them quarantines
every trading grant until the re-key ceremony runs. Between runs, a supervisor with no
model in it compares live values against exits stamped into a ledger at entry and closes
what the stored rules require. It runs under its own principal, whose manifest has no
order-placing operation. A circuit breaker demotes the agent's placing authority on a
threshold loss, and a watchdog kills scheduled runs after a demotion.

Prompt injection is cut structurally. The news tool is admitted but marked untrusted, so a
turn that reads it cannot place an order that turn. The acting runs are denied every
non-broker tool, so the watchlist and ledger they read as authority are files they cannot
edit.

## Alpaca infrastructure

Paper account, options only, no stock leg anywhere. The gateway wraps Alpaca's MCP
server: clock, calendar, quotes, bars, option chains and snapshots, positions, orders,
close-position, and the shim's spread placement as one multi-leg order. Multi-leg positions
cannot rest bracket orders at the venue, so the supervisor is the carry machinery. A
dashboard rebuilds from the tape after every run and publishes to GitHub Pages.

## What the record shows

The development stack's first day abstained on every run: a charter written before
observing the market held predicates the market could not satisfy, and the fix was to
measure for a day and ceremony the constants in. On the same stack the breaker fired at
its threshold, placing was demoted, and the supervisor kept closing. On 2026-08-31 an
upstream package release broke the broker connector for ninety minutes of market hours;
it cost nothing, because the agent and the supervisor share the connector and a dead
safety layer can only fail to take an exit, never permit an entry. On 2026-09-02 the
rules combined to "no" five runs in a row on a morning meant for deployment; the agent
found the gap in its own regime rule, filed it rather than using it, and the fix was
ratified and re-keyed after the close. On 2026-09-03 the first run under the fix priced
a condor on a two-sided verdict and six were on by the close, three runs died on
upstream model outages before any tool call, and the supervisor closed eight positions
at the open on their stamped stops with no model awake.

## Honest boundaries

The lock is tamper-evident, not tamper-proof; a holder of the key can re-sign. The tape
proves self-consistency, not tamper-evidence: anyone who can write the file can rewrite
it whole, and the verifier says so in its own output. Shim refusals land in an unchained
sidecar, published and labelled as such. The 0-7 DTE horizon
is fitted to the contest window; a real deployment would sell further out and add rolls,
which is a charter change and not an architecture change. The paper account is down on the
week. The claim is bounded loss with every decision on the record, not profit.

Repo: https://github.com/wjatx/mandate · Dashboard: https://wjatx.github.io/mandate/dashboard/
