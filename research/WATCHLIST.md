# Watchlist — standing intents (charter §6)

Maintained by the operator between decision runs. A decision run proposes WATCH items in its
record; the operator rules on each here. Only items under **Approved standing intents** are
executable, and only while unexpired. Everything here runs inside the charter's caps, slots,
per-run limits, and the broker's gate.

## Approved standing intents

(none — WL-5 executed by run-0915; see below)

## Proposed, awaiting ruling

- **WL-6** (run-0915, proposed 2026-09-01 09:20 CT): a QQQ **Sep 8 volatility pair** under §2's
  volatility-thesis shape — paired call and put debit verticals, no directional view. Requesting a
  ruling rather than acting on memo authority because WL-2 settled that a pair consumes both of a
  run's two opens, and this run had already spent one on WL-5; a later run today could execute it
  with both.

  Measured this run, which is the point of the item: the §7 memo's QQQ volatility thesis was
  explicitly flagged as *inferred from broad-market gauges, not from QQQ's own near-dated surface*,
  and asked for a measured reading to settle it. That reading is now taken. QQQ Sep 8 ATM straddle
  IV 14.74% (C/P both at the 709 strike, deltas 0.5016/-0.4984) against RV20 of 17.31% gives a
  ratio of **0.851 — Low regime**, confirming the memo's claim: implied sits below what QQQ has
  actually been realizing. The reading is not a band-edge case (710 gives 0.847, 711 gives 0.834;
  the nearest edge is 1.00).

  The thesis satisfies §2's volatility shape on every clause: dated macro events the position would
  carry (Broadcom after Wednesday's close, August payrolls Friday), both after entry and before a
  Sep 8 expiry; the position sits in the 2-7 DTE band at 7 DTE; measured IV in the low band. No
  directional view is taken or needed, which matters because the memo names none for QQQ.
  Falsified by the events passing, or by the regime leaving the low band.

  Strikes and debits deliberately not fixed here, per the WL-5 precedent that a number chosen at
  ruling time is stale by execution. Sizing would run inside §5 unchanged: each vertical at most
  $5,000, tactical-book headroom ample ($2,234 of the $60,000 sub-cap in use). Low regime does not
  halve size — that is the Mid income rule.

  Requested expiry if approved: 2026-09-01 close, since the Broadcom binary is Wednesday evening
  and the premium is cheapest before it.

## Ruled: rejected, expired, executed

- **WL-5** (run-0845 → approved with modification 2026-09-01 09:00 CT → **EXECUTED 2026-09-01
  09:18 CT by run-0915**): SPY **Sep 8 770/772 bear call**, 16 contracts, filled at $0.50 credit
  (short 770 @ 1.62, long 772 @ 1.12) for $800 collected against $2,400 max loss. The trigger
  measured true: SPY Sep 8 ATM straddle IV 10.38% against RV20 of 9.36% is a ratio of 1.109, inside
  Mid and not near either edge. Short delta 0.2720 sits inside the 0.20-0.30 band; credit/width of
  0.25 clears the Mid floor of one fifth with a quarter to spare; $2,400 is inside the half-size
  ceiling of $2,500. The strike guard did not bind, as anticipated in the approval: no Sep 8 leg
  existed to collide with. Gate stamped exits TP 0.25 and stop 1.00. Executable-once is now spent;
  any further SPY short-call structure is a fresh proposal.

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
