# Watchlist — standing intents (charter §6)

Maintained by the operator between decision runs. A decision run proposes WATCH items in its
record; the operator rules on each here. Only items under **Approved standing intents** are
executable, and only while unexpired. Everything here runs inside the charter's caps, slots,
per-run limits, and the broker's gate.

## Approved standing intents

- **WL-5** (run-0845 → approved 2026-09-01 09:00 CT): if a later run today measures SPY Sep 8
  still inside the Mid band, sell a SPY Sep 8 bear call vertical, short strike inside the
  0.20-0.30 delta band, half size (max loss at most $2,500), credit floor one fifth of the
  width per §2's Mid-regime rule. Executable once; a second short-call structure in SPY beyond
  this one is a fresh proposal.

  MODIFICATION (strike guard): neither strike may coincide with an existing ledger leg's strike
  at the same expiry and right; if the indicated strike would, shift the spread $1 further from
  it.

  On the collision the proposing run flagged: the Sep 4 pair's 768 and 773 are a different
  expiry. The defined-risk gate computes worst case over same-expiry groups
  (`shim/defined_risk.py:481`, and its refusal text names "the {root} {expiry} book"), and
  distinct expiries are distinct contracts at the venue, so they neither net nor group with a
  Sep 8 structure. The guard above therefore constrains nothing today and binds only if a Sep 8
  position is opened first, which a later run could do. Strikes are chosen by the delta rule,
  not named here, because naming them at 09:00 would fix a number the run must measure at
  execution.

  Expires 2026-09-01 close.

## Proposed, awaiting ruling

(none)

## Ruled: rejected, expired, executed

- **WL-3** (cal-1325 → approved 2026-08-28 13:38 CT → **OVERTAKEN 2026-09-01 08:30 CT**): the
  thesis-falsification close of cal-1315's QQQ 717/722 bull call below 706. The supervisor's
  first pass of the day closed that position on its stored value stop before QQQ reached the
  trigger: value 0.74 against a 2.48 debit (0.30x) versus the stop stamped at entry of 1.24,
  both legs closed shorts-first. The intent's action target no longer exists and its trigger
  can no longer do anything, so it is recorded overtaken rather than expired. The reasoning
  behind it stands and is worth keeping: 706 was the memo's own falsification level, cited at
  entry, and pre-registering the invalidation is what kept the position from being closed
  discretionarily in-band over the weekend. That the value stop arrived first is the exit
  precedence in §4 working as written, clock then value stop then take-profit.

- **WL-4** (cal-1345 → approved with modification 2026-08-28 14:12 CT → **EXPIRED 2026-08-31
  close**): the second QQQ Sep 4 bull call debit vertical above 718. The intent ran its full
  term and the 718 trigger never fired while it stood. It was deliberately left unedited
  through Monday so post 2's untouched-inputs claim stayed true, and is recorded as expired
  here on 2026-09-01 before the day's first decision run. Not executable. By the entry's own
  extension clause, any successor aimed at the Sep 2 earnings binary is a fresh proposal
  needing its own ruling; it does not revive on WL-4's terms.

- **WL-1** (cal-1315 → approved 13:25 CT → **OVERTAKEN 2026-08-28 13:32 CT**): the SPY
  Sep 4 volatility pair the intent authorized was opened directly by cal-1325 on its own
  §2 memo authority (that run's prompt predated the approval, and each run may act on the
  memo without a standing intent). The setup is expressed; the trigger is permanently
  false; a second pair would be duplication, not the intent. The approval's learning-rate
  ruling and the §4 exit-anchor question for the weekend review stand as recorded.

- **WL-2** (cal-1315 → ruled 2026-08-28 13:25 CT): position counting for paired verticals.
  CONFIRMED as the run read it: each spread is one position; a volatility pair consumes two
  slots and both of a run's two opens. War-room precedent is uniform (run 6's QQQ pair and
  cal-1115's SPY pair were each recorded as 2 of 2 per-run opens). A pair therefore cannot
  share a run with a directional open.
