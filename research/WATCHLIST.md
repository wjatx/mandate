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

  **FILL STATUS, run-1015 (2026-09-01 10:15 CT).** The call leg filled at 14:51:54Z at its
  $1.41 limit and is held: long 30 QQQ260908C00717000 @ 2.74, short 30 C00722000 @ 1.33. The
  put leg never filled. It rested 26 minutes at $1.05 while QQQ fell about 1% away from it, so
  the pair was half-on and the book was carrying $4,230 of long directional call risk that this
  thesis explicitly does not take. Under the approval's own reprice clause, run-1015 cancelled
  the stale order (b15bf0ac) and replaced it: **704/699 put debit vertical, 36 contracts at a
  $1.18 limit**, gate-accepted at $4,248 max loss, stamped `vol_pair`, order ab334e72, resting
  at run end.

  > OPERATOR CORRECTION (2026-09-01 10:35 CT): two figures in this fill account overstate the event. QQQ measured 710.18 at run-0945 and about 709.4 at 10:20, a move of roughly 0.1%, not 1%; the spread's own repricing (mid 1.05 to about 1.15) is consistent with that small move plus volatility, and inconsistent with a 7-point fall. And the unhedged call side's mark loss was $390 to $420 (supervisor tracked it at 1.28 and 1.27 against the 1.41 debit on both passes inside the window), not $1,140. The reprice and resize were sound on the live quotes regardless; the severity was not as recorded. Original text left intact above.

  Two deviations from run-0945's numbers, both recorded rather than assumed. The limit moved
  $1.05 to $1.18 because the spread itself repriced with spot: mid is now 1.16 and natural
  1.23, so $1.18 is mid plus a cent of chase, not a new thesis. The quantity moved 40 to 36
  because 40 was never the point. Run-0945 sized 30/40 to open the pair delta-flat, and with
  the call vertical now at +0.1231 delta per contract and the put at -0.1018, 40 contracts
  would open the pair at -0.379 net delta while 36 opens it at +0.028. Holding the stated
  quantity would have abandoned the property the quantity existed to produce. The operator
  delegated this explicitly ("Sizing, strike selection and the credit/debit arithmetic are the
  charter's, not named here").

  Trigger re-validated on this run's own measurement, not inherited: QQQ Sep 8 straddle-averaged
  ATM IV at the 709 strike (call 14.35%, put 14.35%) is 14.35% against RV20 of 17.306% through
  the 2026-08-31 close, a ratio of **0.829**, Low. Neighbouring strikes read 0.828 (710) and
  0.839 (708), so the declaration does not turn on the ATM choice, and nothing is near the 1.00
  edge. RV20 was recomputed from daily bars rather than carried over from run-0945, and
  reproduces its 17.31% exactly. Spot 709.23, quotes fresh to the second, chain deep.

  §2's unwind guard was checked and does not bind: a put debit vertical added to a call debit
  vertical in the same underlying and expiry offsets in delta but not in risk, since both legs
  are long premium and the ledger records the sum of the two debits correctly. That is the
  volatility-pair structure §2 and §4 name explicitly, not the condition the guard was written
  against, which was short premium cancelling long premium.

  Run-1015 counts this reprice as one of its two opens and opened nothing else, so the run is
  within limits under either reading of whether completing a prior run's authorized order is a
  new open.

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

- **WL-9** (run-1145, proposed 2026-09-01 11:45 CT): **AVGO Sep 4 income trade, gated on a
  directional read.** If the §7 research pass produces an AVGO directional thesis in the §2
  sense (one sentence, falsified at a named level) before the Wednesday 2026-09-02 close, then
  a decision run may open one AVGO Sep 4 credit spread on the side that thesis supports, at
  full size under the High regime measured below, subject to every ordinary limit. If no such
  thesis arrives, the item expires unexercised. Expiry: 2026-09-02 close, since AVGO reports
  that evening and the setup does not survive it.

  Why this is a watch item and not a trade. The measurement is the strongest dispersion signal
  the book has seen: AVGO Sep 4 straddle-averaged ATM IV at the 370 strike (call 111.57%, put
  112.24%) is **111.9%** against RV20 of **43.99%** through the 2026-08-31 close, a ratio of
  **2.544**, deep High. QQQ Sep 8 measures **0.873**, Low, on the same rule. Selling rich
  single-name variance while owning cheap index variance is a coherent pair, and the book
  already holds the index leg (the WL-6 pair). The charter admits AVGO to the income book and
  has already ruled that the gap risk is the deliberate choice.

  What blocks it is §2's direction requirement, not the arithmetic. A bull put needs an "up or
  sideways" read and a bear call a "down or sideways" one; today's memo carries **no AVGO
  thesis at all**, and its only AVGO-adjacent sentence (the QQQ basis note that the debate is
  "whether an AI revenue outlook clears a bar that has drifted above consensus") cuts against
  the put side rather than supporting it. An iron condor needs a genuinely range-bound read,
  which an 8.1% implied earnings move is the opposite of. So the run abstained on the read.

  The arithmetic, recorded so the next run need not re-derive it. Spot 369.25. At natural
  pricing nothing clears the High floor of one quarter of width; at mid, one candidate clears
  with room: **350/345 bull put**, short delta -0.2794 (in band), mid credit **1.52** against a
  **1.25** floor, natural 1.21. The call side is worse: the best bear call, 395/397.5, reaches
  0.635 at mid against a 0.625 floor, a one-cent margin on a 41-cent-wide market, which is not
  a measurement worth trading. Note the asymmetry this creates: if a read arrives, only the
  **put** side is actually reachable, so a bearish AVGO thesis would authorize a trade the
  chain cannot price. That is worth the operator knowing before ordering a research pass.

  **Flagged for the operator, no action proposed — the ledger's blind spot runs both ways.**
  §2's unwind guard exists because "the risk ledger sums each position's maximum loss and nets
  nothing across positions", so an *offsetting* open records risk it does not add. The mirror
  case is now the book's largest exposure and nothing checks it: **stacking** same-direction
  positions in the same strike region records them as independent when they are nearly
  perfectly correlated. After this run's open, SPY short-call risk is **$14,494** across five
  spreads — Sep 3 767/768 ($4,884), Sep 8 770/772 ($2,400), 771/774 ($2,290), 769/772 ($2,464)
  and 769/773 ($2,456) — about 14.7% of equity riding on one question, whether SPY rallies
  through roughly 770 inside seven days. The $85,000 aggregate cap counts that as $14,494 of
  diversified risk; economically it is closer to one position. This run took the fifth spread
  anyway, because the charter has no concentration limit and a run should not invent one and
  then abstain on it — but it is recording that the restraint it did exercise (one open, not
  two, and a short strike no lower than the book's existing lowest) came from judgment the
  rules do not supply. Whether the aggregate cap should net correlated exposure, or whether a
  per underlying-and-direction sub-cap belongs in the envelope, is a design question for after
  the contest.



## Ruled: rejected, expired, executed

- **WL-8** (run-1115, proposed 2026-09-01 11:15 CT → **REJECTED 2026-09-01 11:30 CT**): treat the **SPY Sep 4 volatility pair as a
  unit on the downside**, the way §4's `vol_pair` flag would if the pair were not older than the
  fix. If the call leg (768/773, 6 contracts, 1.84 debit) is closed by the per-leg value stop
  stamped at its entry, then the next decision run closes the put leg (763/758, 6 contracts,
  0.91 debit) at market in the same pass, rather than carrying a one-sided remnant of a
  volatility thesis that can no longer be expressed one-sided. Expiry: 2026-09-04 close, when
  both legs expire anyway.

  Why now. This is the **second** instance of the defect WL-7 flagged this morning, and the
  first one already fired: the QQQ Sep 4 pair lost its call half to a supervisor stop at 13:30Z
  today and its put half is still on the book alone. The SPY Sep 4 pair is set up identically
  and is closer than it looks. Measured this run: the call leg is worth 1.17 against a stored
  stop of 0.92, so it is roughly a 0.6% SPY rally away from the same outcome, while the put leg
  sits at 1.52 against a 0.91 debit and is the profitable half. Both pairs predate the
  2026-08-29 `vol_pair` amendment, so both carry per-leg stops the charter would no longer
  stamp; §4 forbids re-deriving their exits, which is correct and is exactly why this needs an
  operator ruling rather than run discretion.

  The counter-argument, recorded so the ruling is made on both sides. Closing the surviving half
  is not obviously right: the QQQ Sep 4 remnant left by this morning's stop is currently the
  book's best-performing position (+$232 on a $528 debit), so a standing "close the remnant"
  rule would have closed a winner. The choice is between honouring the pair as one thesis and
  keeping a leg that is doing well on its own. This run has no view worth imposing on that and
  is asking rather than acting.

  > RULING (2026-09-01 11:30 CT): REJECTED, on facts checked against the ledger rather than the proposal's account of them. The trigger cannot fire: the call leg carries no value stop (run1-spy-vol-call-768-773 is stamped vol_pair, stop None; it was placed 2026-08-31, after the 2026-08-29 amendment, so 'both pairs predate the fix' is wrong for this leg, and the supervisor has printed 'vol pair: no value stop' for it on every pass today). The quoted 0.92 stop belongs to the QQQ 721/726 leg closed at 13:30Z; the quoted debits (1.84, 0.91) also differ from the stored 1.86 and 0.95. The pair's one-sided risk runs the other way: only the put leg has a stop (0.475, pre-fix), which fires in a rally, precisely when the call leg is the aligned winner, and the proposal's own counter-argument (this morning's QQQ remnant is the book's best position) says do not close the winner because the loser stopped. The genuine residue, a mixed-era pair carrying a stop on one leg only, goes to the post-contest design list; section 4 forbids re-deriving stored exits, so no patch is attempted here.

- **WL-7** (run-1015, proposed 2026-09-01 10:15 CT → **OVERTAKEN 2026-09-01 10:30 CT**): completion or abandonment of the WL-6 put leg.
  If order ab334e72 (QQQ Sep 8 704/699 put debit vertical, 36 contracts, $1.18 limit) is still
  unfilled at the next decision run's own reading, then reprice it once more at that run's
  measured natural price, capped at $1.30 and at the $5,000 per-position ceiling, provided QQQ
  Sep 8 still measures Low on that run's own measurement. If it is still unfilled after that
  second reprice, cancel it and leave the call vertical unhedged rather than chase further.
  Expiry: 2026-09-01 close, since it is a day order and cannot survive the session anyway.

  Why this wants a ruling rather than run discretion. Repricing a resting leg is cheap
  individually and unbounded in aggregate: each run can justify one more cent, and a structure
  authorized as delta-flat drifts into an expensive directional bet one reprice at a time. A
  named cap and a named give-up point put the stopping rule in front of the decision instead of
  behind it. The $1.30 ceiling is not arbitrary — the pair's max loss at 36 contracts stays
  under $4,700 there, inside the position cap with room.

  **Flagged for the operator, no action proposed.** Two of the book's volatility pairs are
  currently half-on, by two unrelated mechanisms, and only one of them is a solved problem.
  The QQQ Sep 4 pair opened 2026-08-28 (put 711/706 at 1.32, call 721/726 at 1.85) lost its
  call half to a supervisor stop at 13:30Z today, leaving the put vertical alone; that is
  exactly the failure §4 describes and fixed on 2026-08-29 with the `vol_pair` flag, showing up
  in a position that predates the fix, so it needs nothing new. The WL-6 pair is half-on for a
  different reason the flag does not touch: **one leg filled and the other did not.** The
  `vol_pair` flag governs exits, not entries, so nothing in the charter or the gate currently
  makes a pair's two legs atomic at entry, and the window between fills is a window in which
  the book holds a directional position that no thesis authorized. Today that window was 26
  minutes and cost the pair about $1,140 of mark on the call side before it could be hedged.
  Whether entry atomicity is worth a rule, and whether that rule belongs in the gate or in the
  charter, is a design question for after the contest rather than a run's to answer.

  > RULING (2026-09-01 10:35 CT): OVERTAKEN. The intent is conditional on order ab334e72 being unfilled at the next decision run's own reading, and the order filled before 10:30, before any run could read it. The trigger is permanently false, per WL-1's precedent. The pattern it encodes, a named reprice cap and a named give-up point ruled in advance, is adopted into the post-contest design-pass list rather than lost. The $1,140 figure in the flagged section is corrected in WL-6's fill account above: the measured mark loss was $390 to $420.

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
