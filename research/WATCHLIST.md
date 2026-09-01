# Watchlist — standing intents (charter §6)

Maintained by the operator between decision runs. A decision run proposes WATCH items in its
record; the operator rules on each here. Only items under **Approved standing intents** are
executable, and only while unexpired. Everything here runs inside the charter's caps, slots,
per-run limits, and the broker's gate.

## Approved standing intents

- **WL-6** (run-0915 → approved with modification 2026-09-01 09:25 CT → **OPENED 2026-09-01
  09:48 CT by run-0945**): open a QQQ Sep 8
  volatility pair, a call debit vertical and a put debit vertical on the same underlying and
  expiry, as one §2 volatility thesis carrying Broadcom's Wednesday-evening report and Friday's
  payrolls print. Executable only while QQQ Sep 8 still measures Low at the acting run's own
  measurement. It consumes both of a run's opens and two slots per WL-2. Sizing, strike
  selection and the credit/debit arithmetic are the charter's, not named here.

  **EXECUTION.** The trigger measured true on this run's own reading. QQQ Sep 8 straddle-averaged
  ATM implied volatility at the 710 strike (call 14.44%, put 14.28%) is 14.36% against RV20 of
  17.31% computed through the 2026-08-31 close, a ratio of **0.830**: Low, and not close enough
  to the 1.00 edge to be ambiguous. The neighbouring strikes read 0.843 (709) and 0.816 (711),
  so the declaration does not turn on which strike is called ATM. Spot 710.18, quotes fresh to
  the minute, chain deep on every leg.

  Structure, both legs 7 DTE and inside §2's 2-to-7 band: a **717/722 call debit vertical, 30
  contracts at a $1.41 limit** ($4,230 max loss) and a **704/699 put debit vertical, 40 contracts
  at a $1.05 limit** ($4,200 max loss). The 30/40 ratio is delta-balancing rather than
  dollar-matching. The call spread carries +0.128 delta per contract and the put spread -0.094,
  so at 30 and 40 the pair opens within 0.1 delta of flat, which is what a volatility thesis
  taking no directional view should look like. Strikes were chosen on matched delta rather than
  matched distance, because QQQ's put skew makes the equidistant put the smaller delta: long 717
  call at 0.326 against long 704 put at -0.316, short 722 at 0.198 against short 699 at -0.222.
  The gate stamped both legs **vol_pair**, so each carries a take-profit (3.205 on the call, 3.025
  on the put) and no value stop, per §4 as amended 2026-08-29. Consumes both of this run's opens
  and two slots, 5 to 7 of 20; aggregate open risk moves $9,518 to $17,948 against the $85,000 cap.

  **Both orders were still resting unfilled at their mid-priced limits when this run ended**
  (status `new`, day orders). That is ordinary, and run-0845's spread rested about fifteen
  minutes before filling this morning, but it means the pair is authorized and working, not yet
  held. The next decision run confirms the fills and reprices any leg still resting; if a leg is
  never filled, the closing obligation below has nothing to attach to on that side.

  **MODIFICATION, and it is the condition of the approval: this pair is closed on Friday
  2026-09-04 regardless of value.** Any decision run on that day at or after 13:15 CT closes
  both legs at market; if none has by the 14:15 CT run, that run closes them. Basis: both
  catalysts the thesis names are spent by Friday morning, Monday 2026-09-07 is a market
  holiday, and a Sep 8 long-premium position held past Friday therefore pays three days of
  decay against no remaining event. This is a pre-registered close on WL-3's precedent, ruled
  in advance and risk-reducing, not a §4 re-litigation.

  Two limits on that close, recorded so nobody assumes otherwise. The supervisor does not
  enforce it: it enforces exits stamped at entry, and the §4 same-day clock only reaches legs
  expiring that day, so a Sep 8 position on Friday is untouched by it. The close therefore
  depends on a Friday decision run executing, and if Friday's runs fail the pair rides into the
  holiday weekend unmanaged. And the charter's ordinary exits still take precedence: if the
  take-profit fires first, the pair closes then and this clause never applies.

  The opening authorization expires 2026-09-01 close, and is now spent in any case: run-0945
  exercised it, so no further opening happens under WL-6 and any additional QQQ long-premium
  structure is a fresh proposal. The closing obligation does not expire; it attaches to whichever
  legs fill and binds through Friday. This item therefore stays under approved standing intents
  rather than moving to the ruled section, because the live part of it is the Friday close.

(none — WL-5 executed by run-0915; see below)

## Proposed, awaiting ruling

(none)

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
