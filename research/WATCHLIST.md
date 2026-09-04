# Watchlist — standing intents (charter §6)

Maintained by the operator between decision runs. A decision run proposes WATCH items in its
record; the operator rules on each here. Only items under **Approved standing intents** are
executable, and only while unexpired. Everything here runs inside the charter's caps, slots,
per-run limits, and the broker's gate.

## Approved standing intents

- **WL-39** (operator, filed 2026-09-04 10:09 CT → **RULED by Wes 2026-09-04 10:07 CT**): **the
  book is frozen at the submission deadline and closed flat at the 14:15 CT run.** The contest
  deadline was 10:00 CT. From this ruling no decision run opens any position: WL-26 is revoked
  below, the WL-27 order was cancelled at 10:08 CT unfilled, and WL-38 already bars anything else.
  The six remaining iron condors (SPY Sep 8, Sep 9, two Sep 10; IWM Sep 10 x2) are closed at
  market by the 14:15 CT decision run, all legs, shorts bought back before longs are sold; if that
  run does not fire or dies before acting, the 14:45 CT check run closes them, noting as WL-35 did
  that a check run acting on a watchlist ruling is untested. §4's ordinary exits and the supervisor
  take precedence if they fire first. Decision runs before 14:15 hold, reprice nothing, and record.

  > RULING (2026-09-04 10:07 CT, Wes): "yes, cancel and revoke, and option 1", in chat, choosing
  > a flat, finished book over holding to expiry under the supervisor. Grounds under safe > profit
  > > loss: nothing after today depends on the Mac staying awake across a holiday weekend, which
  > this morning's closed lid showed is a real dependency; the condors carry about +$1,765
  > unrealized at 10:05 CT and closing realizes it; and the judges read a book that stops changing
  > at the deadline. (Transcribed by the session operator.)

- **WL-36** (run-0846, proposed 2026-09-04 08:47 CT → **APPROVED by Wes 2026-09-04 09:33 CT**):
  **bring the three pre-registered Friday pair closes forward from 13:15 CT to the 09:45 CT run.**
  The WL-6 (QQQ Sep 8 717/722 C + 704/699 P), WL-28 (IWM Sep 8 297/300 C + 293/290 P) and WL-33
  (IWM Sep 9 297/300 C + 295/292 P) rulings each close their pair "at or after 13:15 CT" on the
  ground that the payrolls catalyst is spent by Friday morning and long premium held past it pays
  decay against nothing. run-0846 found that ground already true at 08:47: the print landed at
  07:30 CT and post-print implied volatility collapsed under realized on every index name. Marked
  at the run: QQQ +$498, IWM Sep 8 −$3,716, IWM Sep 9 −$910, total −$4,128 on $21,178 of debit.
  The run did not close them because the rulings authorize 13:15 and §4 forbids re-litigating
  stored exits, so it filed this on the WL-35 precedent. Names no new trade; strictly risk-reducing.

  > RULING (2026-09-04 09:33 CT, Wes): APPROVED ("approve WL-36, close them at 09:45", in chat).
  > The 09:45 CT decision run closes all six legs of the three pairs at market; if that run does
  > not fire or dies before acting, the next decision run does. Same two limits as WL-6, WL-28 and
  > WL-33: the supervisor will not enforce this, and §4's ordinary take-profit takes precedence if
  > it fires first. WL-26's "after the WL-6 fill" condition is measured against this close; its
  > other conditions and §3 still govern, and QQQ Sep 8 measured Low at 08:47. (Transcribed by
  > the session operator.)

  **EXECUTED by run-0945 (2026-09-04 09:45 CT).** All twelve legs closed at market between
  14:45:51Z and 14:45:59Z, the six shorts bought back first, then the six longs sold; a follow-up
  position read confirmed all gone. Realized **−$5,213 on $21,178 of debit** (QQQ 717/722 C +$2,970,
  704/699 P −$3,672; IWM Sep 8 297/300 C −$1,273, 293/290 P −$2,408; IWM Sep 9 297/300 C −$374,
  295/292 P −$456). The run records that the same legs marked −$4,128 at 08:47, so the 58 minutes
  between observation and execution cost about $1,085, and argues a pre-registered close should
  trigger on the condition the ruling names rather than a clock time chosen days earlier. Moves
  to the ruled section at the close. (Transcribed by the session operator.)

- **WL-25** (run-0845, flagged 2026-09-03 08:49 CT under §5 → **APPROVED by Wes 2026-09-03 09:05 CT** → **EXECUTED by run-0915 2026-09-03 09:25 CT**, order resting at run end):
  **a second SPY iron condor, at an expiry other than Sep 10.** run-0845 measured SPY Sep 10 at
  1.354 High on today's two-sided verdict, opened one condor (777/780 C, 761/758 P, 26 contracts at
  -1.08, order 58307908, resting `new` at run end) and declined a second at Sep 9 on its own judgment
  about correlated short-delta losses on consecutive days, flagging that restraint as the operator's
  to rule under §5 and noting WL-10 cuts against a run inventing a concentration rule. Deployment
  stood at $17,424 of $85,000.

  > RULING (2026-09-03 09:05 CT, Wes): APPROVED ("Free to take the second SPY condor - yes", in
  > chat). One additional SPY iron condor, at an expiry other than Sep 10, executable within every
  > ordinary limit on the executing run's own re-measurement: two-sided SPY verdict on today's memo,
  > High regime read on the structure's own expiry, both shorts inside the 0.20-0.30 band, total
  > credit clearing the High floor against the widest wing at natural, max loss under the
  > per-position cap, no leg collision and no offset with the Sep 10 condor or the Sep 4 pair. This
  > is one condor, not a rolling authorization. The Sep 10 order's fill or repricing is the run's
  > ordinary business and is not gated by this item. Expires 2026-09-03 close. (Transcribed by the
  > session operator.)

  > RECORD CORRECTION (2026-09-03 09:10 CT, operator): run-0845 also sold the 18 orphaned SPY Sep 8
  > 773 calls (order 28315bee, 1.60, +$1,608 realized) on the ground that "the supervisor enforces
  > stored exits so nothing would ever have closed them." That ground does not hold. The supervisor's
  > long-only fragment rule (written after the 2026-08-28 fill race) would have sold them on its
  > 09:00 CT pass; an operator dry run at 08:47 CT showed FRAGMENT_EXIT and WOULD_CLOSE for both
  > rows. The run marked the mechanism [inferred] and had no supervisor-log tool, so the error is
  > one of inference, not of reading. Outcome identical; the close at 08:58 CT beat the supervisor by
  > about a minute. Recorded because two closers acting on one fragment is design item 31.

  **EXECUTED, run-0915 (2026-09-03 09:19-09:25 CT, the slot's hand re-run after the 09:15 firing
  died on an upstream API 529 before any tool call).** Sep 9 chosen over Sep 8 on a collision
  ground: at spot 768.57 a Sep 8 condor's call short would land on 774 against the held Sep 8
  771/774 long, WL-11's leg collision. **SPY Sep 9 775/778 C + 762/759 P, 12 contracts at a 1.07
  credit limit, order `0e9a7e0b`, gate-accepted iron_condor at $2,316 max loss.** Regime Mid
  (1.2554 on Sep 9, neighbours 1.2933 / 1.2534, no edge crossed), so §2's two-sided condor sizes
  at half, and $2,500 single-side max loss bound the quantity rather than the $5,000 cap. Shorts
  at 0.2524 and -0.2393; Mid floor 0.60 against 1.04 at natural. Resting `pending_new` at run end;
  the 09:45 run confirms the fill or reprices. WL-25 is spent by this placement; repricing the same
  condor if unfilled is the run's ordinary business, as with the Sep 10 order below.

  Same run, outside this item: the Sep 10 condor (order 58307908, 26 at 1.08) had rested 21
  minutes while SPY rallied from about 765 to 768.57 and centred it, cutting the credit to 0.94
  natural; cancelled and replaced as **24 contracts at 1.00, order `73531c10`, $4,800**, quantity
  reduced so max loss stays under the cap at the lower credit. The run named the resulting shape
  plainly: SPY short calls at 771 (Sep 8), 775 (Sep 9) and 777 (Sep 10), a rally of about 1.1%
  through all three, netted by nothing in the ledger. Design item 20, now the book's shape.
  (Transcribed by the session operator from the run record.)

  **FILLED.** run-0945 read the orders: the Sep 9 condor filled at **1.08**, a cent better than its
  1.07 limit, and the Sep 10 condor filled at **1.00** for 24 contracts. The 09:30 supervisor pass
  counted 18 legs and manages both rows against stamped exits (Sep 9 tp 0.54 / stop 2.14; Sep 10 tp
  0.50 / stop 2.00). WL-25 is closed as executed. (Transcribed by the session operator.)

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

- **WL-40** (run-1015, proposed 2026-09-04 10:15 CT → **ROUTED TO THE DESIGN PASS 2026-09-04
  10:25 CT**, design item 38; **operator note: the stale row stands until the close**): **a hand
  cancel outside the gateway leaves a ledger row the gate cannot reconcile.** The risk ledger still
  carries `run-0904-0945-dia-0911-condor-539-541-529-527` at $2,376 for order `bb4b3f0e`, which the
  operator cancelled unfilled by direct broker API at 15:08:47Z under WL-39. Positions show no DIA
  leg and no order rests, so the gate reads deployment as $19,268 where the true figure is
  $16,892. Prior stale rows (WL-14) came from unfilled day orders the gateway itself placed; this
  one came from an action the gateway never saw. Under WL-39 no run opens anything today, so the
  overstatement cannot block or admit a trade; the operator leaves the ledger untouched rather
  than hand-edit the file the gate reads, and the row expires with the day order it names. Names
  no trade. (Transcribed by the session operator.)

- **WL-38** (run-0945, flagged 2026-09-04 09:50 CT under §5 → **RULED by Wes 2026-09-04 09:55 CT:
  the idle capital is ACCEPTED DELIBERATELY for the day**): **idle capital on the deadline day.** Closing the three pairs released $21,178 of debit; the book stands at
  $19,268 of $85,000 deployed with 13 free slots. The two ruled openings were WL-26 and WL-27; one
  is spent and the other is gated to the 10:15 run, so run-0945 had no third compliant opening to
  take. §5 makes undeployed equity an inaction the operator rules on. The cadence window ends with
  today and the post-Friday carry decision follows the 14:15 run. (Transcribed by the session
  operator.)

  > RULING (2026-09-04 09:55 CT, Wes): ACCEPTED as a deliberate inaction, not an omission
  > ("option 1", in chat, choosing acceptance over authorizing further deployment). The cadence
  > window ends with today; the only ruled openings are WL-26 and WL-27, and no new opening is
  > authorized for the rest of the cadence. Grounds under safe > profit > loss: every position
  > opened today is one the supervisor alone watches from Monday, and the post-Friday carry
  > decision after the 14:15 run is simpler with fewer of them. Runs may keep flagging idle
  > capital under §5; this ruling answers the flag for 2026-09-04. (Transcribed by the session
  > operator.)

- **WL-37** (run-0945, proposed 2026-09-04 09:50 CT → **ROUTED TO THE DESIGN PASS 2026-09-04
  09:58 CT**, design item 37): **the §7 memo now states a horizon, and no charter rule tests a
  structure's expiry against it.** Friday's memo gives DIA a five-day horizon through Sep 9 while
  WL-27 authorized a Sep 11 structure, with two dated events between them. run-0945 handled it by
  sizing down, a judgment the rules do not supply. Same shape as items 22 and 27, which pin which
  expiry supplies the regime's numerator; this asks whether the verdict reaches the expiry the
  structure uses. Names no trade. (Transcribed by the session operator.)

- **WL-35** (run-1415, proposed 2026-09-03 14:15 CT → **RULED 2026-09-03 14:28 CT, session operator
  under Wes's 12:03 CT delegation: the gap risk is ACCEPTED DELIBERATELY and the SPY condors are
  held; revocable by Wes before the 14:45 CT check run starts**): **the gap the stops cannot
  cover.** SPY 773.39 sits 0.21% under the nearest of four SPY short-call blocks (775 Sep 9, 777
  Sep 10, 778 Sep 8, 779 Sep 10), all inside the ~1% move the memo prices for Friday's 08:30 ET
  payrolls print. The four SPY condors collected $6,916 and carry $11,996 of ledger max loss; the
  2x value stops bound the loss near the credit in a continuous tape, and a gap on the open moves
  it toward the max-loss figure. The run asked for a decision with time attached, and noted that
  silence should not be read as oversight. The only executor able to act before the print is
  today's 14:45 check run; Friday's first decision run fires after the open.

  > RULING (2026-09-03 14:28 CT, session operator, delegated): HELD, as a deliberate acceptance
  > rather than an omission. Grounds under safe > profit > loss. Safe: every SPY condor is defined
  > risk inside the $5,000 per-position cap and the $85,000 book cap, and the gap case is the one
  > the 2026-09-02 §2 amendment chose on purpose ("gap risk over thin credit ... bounded per
  > position and per book by caps this package does not touch"), ratified by Wes at 11:24 CT that
  > day; the worst case on the four condors together is $11,996, about 14% of equity, with three
  > long-vol pairs ($21,809 of debit) on the other side of a large move in either direction.
  > Profit: closing all four now realizes about $1,300 against current marks and forfeits the
  > base case, in which a move inside the priced 1% leaves most of the $6,916 collected. Loss:
  > the tail beyond the stops is accepted, sized and recorded here. The operator declines to
  > substitute a lower risk tolerance for the one Wes ratified. Wes may reverse this by saying
  > "close WL-35" (all four) or naming the condors to close, before 14:45 CT; the ruling would
  > then direct the check run to close them at market, noting that the check run acting on a
  > watchlist ruling is untested. (Transcribed by the session operator.)

- **WL-34** (run-1345, proposed 2026-09-03 13:45 CT → **ROUTED TO THE DESIGN PASS 2026-09-03 13:55
  CT**, design item 36): **a resting debit leg that misses is invisible for thirty minutes.** The IWM
  Sep 9 put leg was priced at 0.92 (12:45), 0.94 (13:15) and 1.09 (13:45); the first two rested 27
  and 30 minutes unfilled on a moving tape and the third filled in 0.14 s. Entry atomicity (item 3)
  covers one leg filling and the other not; it does not cover a leg that simply misses, because
  nothing observes the miss until the next run. Measured cost: the put ran 0.92 to 1.05 filled
  across the hour while the call half sat unhedged. Names no trade. (Transcribed by the session
  operator.)

- **WL-33** (run-1245, proposed 2026-09-03 12:45 CT → **APPROVED 2026-09-03 12:55 CT, session
  operator ruling under Wes's 12:03 CT delegation, on WL-6's and WL-28's precedent**):
  **pre-registered Friday close of the IWM Sep 9 volatility pair opened by run-1245** (297/300 call
  debit vertical x22, order `29267f49`, limit 0.78; 295/292 put debit vertical x22, order
  `49ee68da`, limit 0.92; both `vol_pair`, resting `new` at run end). The catalyst is Friday's 08:30
  ET payrolls print; Monday Sep 7 is a holiday; the memo's next dated event (CPI, Sep 11) sits past
  a Sep 9 expiry.

  > RULING (2026-09-03 12:55 CT, session operator): APPROVED as filed. Any decision run on
  > 2026-09-04 at or after 13:15 CT closes both legs at market; if none has by the 14:15 CT run,
  > that run closes them. Same two limits as WL-6 and WL-28: the supervisor will not enforce this,
  > and §4's ordinary take-profit takes precedence if it fires first. If the pair has not filled by
  > the 13:15 run today, that run cancels or reprices it on its ordinary discretion; a half-filled
  > pair is the WL-6 case and the run treats it the same way. Wes may amend before 13:15 CT Friday.
  > (Transcribed by the session operator.)

  **HALF-ON, then completed by run-1315 (2026-09-03 13:15 CT).** The call leg (`29267f49`, 297/300
  x22) filled at 18:08:15Z at 0.78; the put leg (`49ee68da`) rested 24 minutes at mid unfilled.
  run-1315 cancelled it (confirmed 18:17:56Z, zero filled) and re-placed **295/292 put debit
  vertical x22 at 0.94 natural, order `5a6a8c4b`**, $2,068, stamped `vol_pair`, resting at run end;
  regime re-measured Low on Sep 9 at all three neighbouring strikes (0.9725; 0.9807 / 0.9666), so
  the WL-31 edge had resolved. Quantity held at 22 to open the completed pair at +0.09 net delta.
  Counted as one of the run's two opens on run-1015's WL-6 precedent. The vol-pair entry race has
  now fired twice, both times call-first (2026-09-01 WL-6/WL-7 and today); entry atomicity is still
  unbuilt. The Friday close ruled above binds on whichever legs are held. (Transcribed by the
  session operator.)

  **COMPLETED, run-1345 (2026-09-03 13:45 CT).** `5a6a8c4b` rested 27 minutes unfilled; cancelled
  (18:48:25Z, zero filled) and re-placed **295/292 put debit vertical x19 at 1.09, order `60eec834`,
  filled in 0.14 s at 1.05**, $2,071 max loss, `vol_pair`. Quantity 19 rather than 22 so the
  completed pair opens at +0.06 net delta on the deltas as they stood (WL-6 precedent, arithmetic
  delegated by the ruling). Regime Low at all three strikes (0.9608; 0.9588 / 0.9514). Both legs
  are now held and the Friday close binds on both. Operator read-back of the ledger row confirms the
  `vol_pair` stamp (see the ruling tape). (Transcribed by the session operator.)

- **WL-32** (run-1145, proposed 2026-09-03 11:45 CT → **APPROVED by Wes 2026-09-03 11:57 CT** → **SPENT by run-1215 12:18 CT**): **does the SPY concentration
  lift cover one SPY condor at Sep 8 or Sep 9, now that Sep 10 has gone regime-ambiguous?** Wes
  lifted WL-30 at 11:50 CT for one SPY Sep 10 condor, but run-1145 (in flight when the lift was
  written) measured SPY Sep 10 straddling the 1.30 edge (772 High 1.3070 / 773 Mid 1.2791), which
  §3's straddling rule turns into abstention, while Sep 8 (1.1212) and Sep 9 (1.2168) both read
  clean Mid. On Sep 9 the 778 call is a held long (WL-11 collision), so the in-band call shorts are
  779 (0.2503) and 780 (0.2125); the run priced the Sep 9 call side at 0.58 natural alone against a
  0.60 total-credit floor and did not price the put sides. One condor, half size under Mid, every
  ordinary limit on the executing run's own re-measurement. Expires 2026-09-03 close.
  (Transcribed by the session operator from the run record; the operator reads WL-30 as lifted for
  Sep 10 only and asks Wes whether the lift follows the clean surface.)

  > RULING (2026-09-03 11:57 CT, Wes): APPROVED ("WL-32 yes", in chat). WL-30's lift now reads: one
  > SPY iron condor at whichever of Sep 8, Sep 9 or Sep 10 measures a clean regime (no band edge
  > crossed between neighbouring strikes) at the executing run, executable from the 12:15 run on
  > its own re-measurement within every ordinary limit: two-sided SPY verdict, both shorts inside
  > the 0.20-0.30 band, total credit clearing the measured regime's floor against the widest wing
  > at natural, single-side max loss under the Mid two-sided half-size cap ($2,500) or the
  > per-position cap if the chosen surface measures High, no leg collision (the held Sep 9 778 call
  > is long) and no same-expiry offset. One condor across WL-30 and WL-32 together, not one per
  > expiry and not a rolling authorization. Expires 2026-09-03 close. (Transcribed by the session
  > operator.)

  **SPENT, run-1215 (2026-09-03 12:18 CT).** SPY Sep 10 measured clean again (1.2493 Mid at 773,
  neighbours 1.2825 / 1.2331), the 11:45 straddle having resolved because the RV20 denominator
  rolled rather than because implied moved. **SPY Sep 10 iron condor 779/782 C + 765/762 P, 13
  contracts, order `b0c624a7`, filled at 1.12** (shorts 0.2617 / -0.2330; credit 1.11 at natural
  against a 0.60 floor; max loss $2,444 under the $2,500 half-size cap; no collision with the held
  777/780/761/758). WL-30 and WL-32 are closed as executed. (Transcribed by the session operator.)

- **WL-30** (run-1115, proposed 2026-09-03 11:15 CT → held for Wes by the operator 11:25 CT → **LIFTED
  by Wes 2026-09-03 11:50 CT**, amended by WL-32 → **SPENT by run-1215 12:18 CT**, see WL-32): **lift the concentration restraint for one SPY Sep 10 iron
  condor, 779/782 C + 765/762 P** (Mid 1.2883 on Sep 10, no edge crossed; shorts 0.2729 / -0.2311;
  total credit about 1.15 at natural against a 0.60 floor; about 13 contracts, roughly $2,405 max
  loss at the Mid two-sided half-size cap; no collision with the held Sep 10 777/780/761/758). The
  run states plainly that the trade is charter-compliant and that it declined on judgment the rules
  do not supply: it would be the fourth SPY short-call block (775, 777, 778 held, 779 proposed,
  0.82% above spot) on a day the book has lost 7.95% on that correlation, the morning before a
  payrolls print the memo prices at about 1%. Expires 2026-09-03 close.

  > OPERATOR NOTE (2026-09-03 11:25 CT, session operator standing in): NOT LIFTED. Wes's 09:59 CT
  > delegation covers arming and where to stay; lifting a restraint that adds a fourth correlated
  > short-call block is trading authority, which stays with Wes. The run's own grounds for
  > declining are also the operator's. Wes lifted the equivalent restraint as WL-25 at 09:05 CT and
  > may lift this one by ruling before the close; a later run then executes it on its own
  > re-measurement within every ordinary limit. Notified by push at 11:25 CT.

  > RULING (2026-09-03 11:50 CT, Wes): LIFTED ("lift WL-30", in chat). One SPY Sep 10 iron condor,
  > executable by any decision run from 12:15 CT on its own re-measurement within every ordinary
  > limit: two-sided SPY verdict on today's memo, regime read on Sep 10 with no edge crossed, both
  > shorts inside the 0.20-0.30 band, total credit clearing the measured regime's floor against the
  > widest wing at natural, single-side max loss under the Mid two-sided half-size cap ($2,500) or
  > the per-position cap if Sep 10 measures High, no leg collision with the held Sep 10
  > 777/780/761/758 and no same-expiry offset. Strikes are the executing run's, not fixed at
  > 779/782 + 765/762. One condor, not a rolling authorization. Expires 2026-09-03 close. The 11:45
  > run was in flight when this was written and does not carry it. (Transcribed by the session
  > operator.)

  > AMENDED by WL-32 (Wes, 11:57 CT): the lift follows the clean surface, Sep 8, 9 or 10, one
  > condor in total.

- **WL-31** (run-1115, proposed 2026-09-03 11:15 CT → **ROUTED TO THE DESIGN PASS 2026-09-03 11:25
  CT**, evidence appended to design item 27): **the 1.00 Low/Mid edge is now the one that bites.**
  IWM Sep 9 at 11:15 read 1.0005 Mid at 295 and 0.9814 Low at 296 on one surface at one instant,
  so §3's straddling rule mandated abstention; run-1045 saw the same crossing at 10:45. Every prior
  instance sat at 1.30, where both labels say sell and only the floor moves; at 1.00 the labels
  instruct opposite trades. Names no trade. (Transcribed by the session operator.)

- **WL-28** (run-1015, proposed 2026-09-03 10:15 CT → **APPROVED 2026-09-03 10:30 CT, session
  operator standing in, on WL-6's precedent; Wes may reverse before it binds**): **pre-registered
  Friday close of the IWM Sep 8 volatility pair opened by run-1015** (297/300 call debit vertical
  x67, order `9e56c85a`, filled 0.61; 293/290 put debit vertical x86, order `2cc4081b`, filled
  0.57; both stamped `vol_pair`, TP 1.84 / 1.79, no value stop). The pair's catalyst is Friday's
  08:30 ET payrolls print and its window is spent by Friday afternoon; Monday Sep 7 is a holiday,
  so a Sep 8 long-premium position held past Friday pays three days of decay against no remaining
  event.

  > RULING (2026-09-03 10:30 CT, session operator standing in under the delegation Wes gave at
  > 09:59 CT): APPROVED as filed, the conservative direction, since the close only reduces
  > exposure and mirrors the WL-6 close Wes approved on 2026-09-01. Any decision run on
  > 2026-09-04 at or after 13:15 CT closes both legs at market; if none has by the 14:15 CT run,
  > that run closes them. Same two limits WL-6 recorded: the supervisor will not enforce this,
  > and §4's ordinary take-profit takes precedence if it fires first. Wes may withdraw or amend
  > this before 13:15 CT Friday. (Transcribed by the session operator.)

- **WL-29** (run-1015, proposed 2026-09-03 10:15 CT → **ROUTED TO THE DESIGN PASS 2026-09-03
  10:30 CT**, evidence appended to design items 20 and 26): **does §2's offset guard reach across
  expiries?** run-0845 declined selling QQQ premium at Sep 9/10 as offsetting-in-substance against
  the QQQ Sep 8 long pair (WL-26); run-1015 bought IWM Sep 8 premium while holding a short IWM Sep
  10 condor, the mirror image, on the ground that §3's per-expiry numerator reads Sep 8 at 0.95
  and Sep 10 at 1.05, so the charter's own instrument says buy one surface and sell the other. The
  run called that defensible and not a ruling. No trade is asked; the operator agrees it is the
  design pass's question and rules nothing here. (Transcribed by the session operator.)

- **WL-26** (run-0845, proposed 2026-09-03 08:49 CT → **REVOKED by Wes 2026-09-04 10:07 CT under
  WL-39, never executed: no QQQ condor is to be placed** → previously **APPROVED WITH CONDITIONS 2026-09-03 13:25 CT,
  session operator under Wes's 12:03 CT delegation**): **a QQQ iron condor once WL-6's mandated
  Friday close removes the offsetting objection.** The run declined QQQ premium today on substance:
  Sep 8 is entangled with the WL-6 long-vol pair, and selling QQQ premium at Sep 9 or 10 is
  offsetting-in-substance even though §2's guard binds only on same expiry (WL-22 established the
  operator reads these by substance). Not executable until ruled, and not before the WL-6 close
  lands on 2026-09-04 at or after 13:15 CT. Every ordinary limit applies on the executing run's own
  re-measurement. (Transcribed by the session operator from the run record.)

  > RULING (2026-09-03 13:25 CT, session operator, delegated): APPROVED WITH CONDITIONS. One QQQ
  > iron condor on 2026-09-04, executable only by a decision run that starts after the WL-6 close
  > has been confirmed filled on the orders read (both QQQ Sep 8 legs gone from the book), on
  > that run's own re-measurement within every ordinary limit: a two-sided or range-bound QQQ
  > verdict on Friday's memo (written after the 08:30 ET print), regime read on the structure's
  > own expiry with no band edge crossed, both shorts inside the 0.20-0.30 band, total credit
  > clearing the measured regime's floor at natural, sizing by regime under §2, no leg collision
  > and no same-expiry offset with anything still held. One condor, not rolling. Expires
  > 2026-09-04 close. Grounds under safe > profit > loss: the offsetting objection is the only
  > thing that closed QQQ today, and it lapses with the WL-6 close; the structure takes no side;
  > the caps and stamped exits bound it. Wes may withdraw or amend before it binds. (Transcribed
  > by the session operator.)

- **WL-27** (run-0845, proposed 2026-09-03 08:49 CT → **APPROVED WITH CONDITIONS 2026-09-03 13:25 CT,
  session operator under Wes's 12:03 CT delegation**): **a DIA iron condor on 2026-09-04, when Sep 11
  becomes 7 DTE and DIA enters the 2-7 DTE band for the first time.** Today DIA's only expiries in
  range are Sep 4 (1 DTE) and Sep 11 (8 DTE), so the run called it unplayable on a calendar artifact.
  Not executable until ruled; every ordinary limit applies on the executing run's own re-measurement,
  including a two-sided or range-bound DIA verdict on tomorrow's memo and a High reading on Sep 11.
  (Transcribed by the session operator from the run record.)

  > RULING (2026-09-03 13:25 CT, session operator, delegated): APPROVED WITH CONDITIONS. One DIA
  > Sep 11 iron condor on 2026-09-04, executable by any decision run from 08:45 CT on its own
  > re-measurement within every ordinary limit: Sep 11 measured at 7 DTE and inside §3's band, a
  > two-sided or range-bound DIA verdict on Friday's memo, regime High or Mid on Sep 11 with no
  > band edge crossed (sizing by regime under §2; Low forbids it), both shorts inside the 0.20-0.30
  > band, total credit clearing the measured floor at natural, no collision (the book holds no DIA
  > leg). One condor, not rolling. Expires 2026-09-04 close. Grounds: DIA has been closed all week
  > on a calendar artifact rather than a read, it is the one admitted name the book carries no
  > exposure in, so this diversifies rather than stacks, and the caps and stamped exits bound it.
  > Wes may withdraw or amend before it binds. (Transcribed by the session operator.)

  **EXECUTED by run-0945 (2026-09-04 09:45 CT), order resting at run end.** DIA Sep 11
  539/541 C + 529/527 P, 18 contracts, 0.68 credit limit, order `bb4b3f0e`, `iron_condor`,
  $2,376 max loss, resting `new` at 09:50 CT. Regime Mid (1.126; neighbours 1.130 / 1.111);
  shorts 0.2536 / −0.2485; natural credit 0.66 against a 0.40 floor; no DIA leg in the book.
  Sized as two-sided rather than range-bound: the memo's DIA verdict is range-bound but its
  stated horizon runs through Sep 9, and the memo says extending to Sep 11 brings in producer
  and consumer prices; §1 resolved the size toward the smaller. Deployment $19,268 of $85,000,
  7 of 20 slots. The order's fill or repricing is the 10:15 run's ordinary business. A first
  placement call at 14:48:56Z went out with empty arguments and failed input validation before
  the shim; it is on the tape as an executed call and produced no order (reported to
  ptc-gal-reference #7). (Transcribed by the session operator.)

  **CANCELLED unfilled by the operator at 10:08 CT (15:08:47Z) under WL-39**, zero contracts
  filled, by a direct broker API call under Wes's "yes, cancel" at 10:07 CT; this is a hand action
  outside the gateway and so is not on the agent tape, recorded here and on the rulings tape
  instead. WL-27 is closed out: no DIA condor is to be placed or re-priced. (Transcribed by the
  session operator.)

## Ruled: rejected, expired, executed

- **WL-21** (run-1215, proposed 2026-09-02 12:15 CT → **APPROVED by Wes 2026-09-02 12:27 CT, with the down-verdict condition** → **EXPIRED UNEXERCISED 2026-09-03 close**, measured false nine times, closest approach 0.24% short; the down-verdict condition failed all day on a two-sided IWM memo): **re-file of WL-19 for tomorrow, on the same
  trigger, written to survive tonight's ceremony either way.** WL-19 was approved by Wes at 12:03
  today and expires at today's close having never come within 0.9% of its trigger. This asks to
  carry the same conditional intent into 2026-09-03 rather than let a live, Wes-approved setup
  lapse for calendar reasons alone.

  Trigger, unchanged in substance from WL-19: if IWM trades to **296.00 or higher**, and the IWM
  Sep 8 **298** call measures inside §2's 0.20-0.30 delta band on the acting run's own reading, and
  a spread with short strike at **298 or above** clears the credit floor of the regime that run
  measures **at natural pricing**, then one IWM bear call, sized to the measured regime under §5,
  regime read on the structure's own expiry. Expires 2026-09-03 close.

  **Why it should carry, and why the shape is the right one.** The 298 short-strike floor is what
  makes this trade sound rather than merely legal, and that is worth stating plainly because
  WL-20's ruling put the floor's *status* to Wes tonight. A short call at 298 sits **outside** the
  measured expected move (IWM Sep 8 straddle-avg ATM IV 14.04%, six calendar days, so about
  ±1.80% or ±$5.28 from 293.34, reaching 298.6), whereas the 296/297 candidates the band actually
  admits sit **inside** it at roughly 0.5σ to 0.7σ. Selling a strike inside the expected move on
  the name whose own memo calls the upside its largest tail is the substantive ground the 09:24
  ruling used to reject WL-17, and that ground is independent of the falsifier question and of
  every §3 reading. So this item should carry **whichever way Wes rules on WL-20**: if the falsifier
  floor is withdrawn as a placement rule, the 298 floor still earns its place here on expected-move
  grounds alone, and this item should simply be read as adopting it voluntarily.

  Recorded caveat, unchanged from WL-19 and now stronger: the memo's bearish IWM thesis has gone the
  wrong way for a second session (290.57 Tuesday close → 293.34 now, +0.95%). It is not falsified,
  which needs a close above ~298, but a run measuring the trigger true is by construction acting
  after a further 0.9% rally against the thesis, and should confirm the thesis still stands before
  acting. The trigger's own strike floor largely enforces this.

  Not executable until ruled. Names one trade, inside every ordinary limit; no new authority is
  requested beyond extending an already-approved item by one day.

  > OPERATOR NOTE (2026-09-02 12:26 CT): REFERRED TO WES, not ruled; not executable until he
  > rules. A standing intent for tomorrow creates trading authority the session operator does
  > not hold. Checked and holds: same trigger and strike floor as WL-19, which Wes approved at
  > 12:03; no collision with the held IWM 293/290 and 292/289 bear puts (a bear call above
  > 298 shares no leg); the 298 floor sits outside the measured expected move, so the item
  > stands whichever way the WL-20 question is ruled. Recommendation: approve, with one added
  > condition the run itself half-states, that tomorrow's memo still carries a down verdict on
  > IWM at the time a run measures the trigger; a bear call against an up or two-sided verdict
  > is a different trade. Expires 2026-09-03 close as filed.

  > RULING (2026-09-02 12:27 CT, Wes): APPROVED with one condition ("approve WL-21 with the
  > down-verdict condition", in chat). Executable on 2026-09-03 within every ordinary limit on
  > the executing run's own re-measurement: IWM at 296 or higher; the Sep 8 298 call inside the
  > 0.20-0.30 band; a spread with its short at 298 or above clearing the measured regime's
  > credit floor at natural; regime read on the structure's own expiry; **and the 2026-09-03
  > memo's directional verdict on IWM is "down" at the time the run measures the trigger.** A
  > bear call against an up, range-bound or two-sided IWM verdict is not this item. Expires
  > 2026-09-03 close. (Transcribed by the session operator.)

  **MEASURED FALSE, run-0845 (2026-09-03 08:49 CT, the slot's hand re-run after the 08:45 firing
  died on an upstream API 529 before any tool call).** Three independent clauses fail: IWM quotes
  **294.93 x 294.96** against the 296.00 trigger; today's memo returns **two-sided** on IWM, not the
  "down" verdict the 12:27 condition requires, and the research pass runs once a day so that cannot
  change before the close; and IWM Sep 8 declares **Low** (0.966), where §3 forbids selling premium.
  Expires at today's close. (Transcribed by the session operator.)

  **MEASURED FALSE AGAIN, run-0915 (2026-09-03 09:25 CT), and permanently so:** IWM 294.33 x
  294.35 against 296.00; verdict two-sided; the item expires at today's close and no clause can
  turn true before then. (Transcribed by the session operator.)

  **MEASURED FALSE A THIRD TIME, run-0945 (2026-09-03 09:48 CT):** IWM 294.07 x 294.09 against
  296.00; verdict two-sided. The run's only IWM action was a Sep 10 condor (order `f005a174`, 12 at
  1.00, $2,400), a §2 two-sided structure and not this item. Spent at today's close. (Transcribed by
  the session operator.)

  **MEASURED FALSE A FOURTH TIME, run-1045 (2026-09-03 10:45 CT):** IWM 295.13 x 295.15 against
  296.00; verdict two-sided. Expires unexercised at today's close; the operator moves it to the
  ruled section at the close. (Transcribed by the session operator.)

  **MEASURED FALSE A SIXTH TIME, run-1215 (2026-09-03 12:18 CT):** IWM 294.91 x 294.92, 0.37% short
  of 296.00; verdict two-sided. (Transcribed by the session operator.)

  **MEASURED FALSE A FIFTH TIME, run-1115 (2026-09-03 11:15 CT):** IWM 295.03 x 295.05, 0.32% short
  of 296.00, the closest of the five readings; verdict two-sided. (Transcribed by the session
  operator.)

  **MEASURED FALSE A SEVENTH TIME, run-1315 (2026-09-03 13:15 CT):** IWM 295.26 x 295.29, 0.24%
  short of 296.00, the closest approach of the day; verdict two-sided. (Transcribed by the session
  operator.)

  **MEASURED FALSE AN EIGHTH TIME, run-1345 (2026-09-03 13:45 CT):** IWM 294.91 x 294.93, 0.36%
  short of 296.00; verdict two-sided. The 14:15 run is the last that can measure it. (Transcribed by
  the session operator.)

  **MEASURED FALSE A NINTH AND FINAL TIME, run-1415 (2026-09-03 14:15 CT):** IWM 294.91 x 294.92,
  0.37% short of 296.00; verdict two-sided. No later decision run exists today. **EXPIRES
  UNEXERCISED at today's close.** (Transcribed by the session operator.)

  > RECORD CORRECTION (2026-09-02 13:26 CT, from run-1315): the filing's ground that "a short
  > call at 298 sits outside the measured expected move ... reaching 298.6" does not hold on its
  > own numbers; 298 is below 298.6, so inside the move (about 0.88 sigma on run-1315's reading),
  > and at the 296 trigger the strike is only 0.68% away. The relative claim (298 is further out
  > than 296 or 297) and the falsifier-alignment ground stand, and the down-verdict condition Wes
  > attached is untouched. Wes approved at 12:27 on the filing as written; the approval stands
  > unless he says otherwise, and the correction is flagged to him. Original text left intact.

- **WL-9** (run-1145, proposed 2026-09-01 11:45 CT → **DEFERRED 2026-09-01 12:02 CT, awaiting an AVGO research thesis**): **AVGO Sep 4 income trade, gated on a
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




  > RULING (2026-09-01 12:02 CT): DEFERRED, per §6's third option, session operator standing in. The intent gates itself on a research pass supplying an AVGO thesis, and none exists; approving before the thesis would authorize a trade on arithmetic alone, which §2 forbids, and rejecting would discard measured chain work that stays useful tomorrow. It stands deferred until a memo carries an AVGO read or the Sep 4 expiry makes it moot. Not executable while deferred.

  **EXPIRES UNEXERCISED, noted by run-1415 (2026-09-02 14:15 CT).** The gate never opened. Today's
  §7 memo carries no AVGO section and no AVGO directional thesis, so the condition the deferral
  named — "until a memo carries an AVGO read" — was not met before the item's stated 2026-09-02
  close expiry, and AVGO reports after today's close, which is the event the setup was written not
  to survive. No run tested the arithmetic, because §2 blocks on the read regardless of it. The
  measured chain work in the filing above is left intact for whoever revisits the dispersion idea;
  the asymmetry it recorded (only the put side is reachable, so a bearish AVGO thesis would
  authorize a trade the chain cannot price) is the part worth carrying forward.

  > EXPIRED at the 2026-09-02 close, unexercised (ruled 14:40 CT). No memo carried an AVGO
  > thesis; AVGO reports after tonight's close and the setup does not survive it, as filed.

- **WL-19** (run-1145, proposed 2026-09-02 11:45 CT → **APPROVED by Wes 2026-09-02 12:03 CT**): **IWM Sep 8 bear call, gated on the 298
  strike entering the delta band.** This is the re-file path the 09:24 ruling explicitly left
  open, with the one condition that currently fails written as the trigger.

  Trigger: if IWM trades to **296.00 or higher**, and the IWM Sep 8 **298** call measures inside
  §2's 0.20-0.30 delta band on the acting run's own reading, and a spread with short strike at
  **298 or above** clears the credit floor of the regime that run measures **at natural pricing**,
  then one IWM bear call, sized to the measured regime under §5. Expires 2026-09-03 close.

  Why it is a watch item and not a trade. The direction is authorized: today's §7 memo carries a
  bearish IWM read, the only directional thesis across the four admitted names, and §2 admits a
  bear call on "down or sideways". The arithmetic is available: measured this run at spot 293.12,
  IWM Sep 8 **296/297 prices 0.24 natural / 0.27 mid against a Mid floor of 0.20**, clearing at
  both prices with the short at 0.2834 delta, in band. What blocks it is the 09:24 ruling, which
  requires the short strike at or above the thesis's own falsification level (~298) so that the
  position and the thesis fail together. 296 is below that level, which is the precise defect the
  ruling named when it rejected WL-17.

  **The band and the falsifier do not currently overlap, on either in-window expiry, measured this
  run.** Sep 8 call deltas: 296 **0.2834**, 297 **0.2143**, 298 **0.1592**, 299 **0.1123**. Sep 4:
  296 **0.2354**, 297 **0.1602**, 297.5 **0.1305**, 298 **0.1113**. The band sits at 296-297 and
  the falsifier at 298, so every compliant strike is below the falsifier and every strike at or
  above the falsifier is outside the band. No choice of §3 reading changes this, and it confirms
  run-1115's finding at a second measurement three hours later.

  Why the trigger is a **rally** rather than a decline, which reads backwards and is not. Delta at
  a fixed strike rises as spot rises. IWM must move **toward** 298 for the 298 call to enter the
  band. That is coherent rather than perverse: it is exactly the setup where selling the 298 call
  is both compliant and the right expression of the thesis, since the short strike then sits at
  the level the memo says the read dies at, and the credit improves as the trade gets closer to
  its own falsifier. A decline moves the item further out of reach and it simply expires.

  Recorded caveat: a rally to 296 is 1.0% against a two-to-three session bearish thesis that has
  already gone the wrong way today (IWM 290.57 at Tuesday's close, 293.12 now). A run measuring
  the trigger true should confirm the memo's thesis still stands (no close above ~298) before
  acting, which the trigger's own strike floor largely enforces.

  > OPERATOR NOTE (2026-09-02 11:58 CT): REFERRED TO WES, not ruled; not executable until he
  > rules. Approving a standing intent creates trading authority, which the session operator
  > standing in does not hold. Checked and holds: the trigger (IWM 296+, 298 in band, credit at
  > natural clearing the floor) is the 09:24 re-file path as written, the book holds only the
  > Sep 8 293/290 bear put in IWM so there is no leg collision, and the thesis and position fail
  > together at 298. Recommendation to Wes: approve as filed, expiring at today's close, since
  > tomorrow's memo replaces the verdict it rests on. Wes is travelling; if no ruling arrives
  > the item expires unexercised.

  > RULING (2026-09-02 12:03 CT, Wes): APPROVED as filed ("approve WL-19", in chat). Executable
  > within every ordinary limit on the executing run's own re-measurement: IWM at 296 or higher,
  > the 298 call inside the 0.20-0.30 band, credit clearing the regime's floor at natural, one
  > bear call with the short at 298 or above, regime read on the structure's own expiry under
  > reading 2. Expires 2026-09-02 close. (Transcribed by the session operator.)

  **MEASURED FALSE, run-1215 (2026-09-02 12:15 CT).** The gating clause fails at the first test:
  IWM quotes **293.33 x 293.35**, against a trigger of 296.00 or higher. The item does not fire and
  no further clause was tested for authorization purposes. Recorded anyway, because the shape the
  item was written around is unchanged three hours on: measured this run at spot 293.34, IWM Sep 8
  call deltas are 296 **0.3115**, 297 **0.2345**, 298 **0.1720**, 299 **0.1178**. The band still sits
  at 297 alone and the falsifier still sits at 298, so the two do not overlap — a third measurement
  confirming run-1115 and run-1145. Note the band has *narrowed* since 11:45 (296 has drifted from
  0.2834 up out of the band to 0.3115 as IWM rose), which is the mechanism WL-19's rally trigger
  anticipated, running in the direction that would eventually bring 298 in. IWM would need roughly
  another 0.9% to reach the trigger. The item expires at today's close unexercised unless a later
  run measures it true; see WL-21 for the re-file.

  **MEASURED FALSE A THIRD TIME, run-1345 (2026-09-02 13:45 CT).** IWM quotes **293.86 x 293.87**
  against a trigger of 296.00 or higher, about 0.72% short, so the gating clause fails and no further
  clause was tested for authorization purposes. Recorded additionally: **WL-22's 13:26 scope
  clarification reaches this item.** A bear call is a short-delta IWM structure, so even a true
  trigger would now require an explicit ruling from Wes before the 14:15 run could act on it. Expires
  at today's close; WL-21 carries the shape into tomorrow on Wes's 12:27 approval.

  **MEASURED FALSE A FOURTH AND FINAL TIME, run-1415 (2026-09-02 14:15 CT).** IWM quotes **294.22 x
  294.25** against a trigger of 296.00 or higher — **0.59% short, the closest it has come all day**,
  and rising steadily through every measurement (293.12 → 293.34 → 293.55 → 293.86 → 294.25). The
  gating clause fails, so no further clause was tested for authorization purposes. The item is
  **doubly blocked in any case**: WL-22's 13:26 scope clarification reaches a bear call as a
  short-delta IWM structure, so even a true trigger would have required an explicit ruling from Wes,
  and no such ruling arrived. This is the last decision run before expiry: **WL-19 expires at today's
  close unexercised.** WL-21 carries the shape into 2026-09-03 on Wes's 12:27 approval, with the
  down-verdict condition attached.

  **MEASURED FALSE AGAIN, run-1245 (2026-09-02 12:45 CT).** The gating clause still fails at the
  first test: IWM quotes **293.54 x 293.56**, against a trigger of 296.00 or higher. No further
  clause was tested for authorization purposes. Recorded because the shape is unchanged at a fourth
  measurement: at spot 293.55, IWM Sep 8 call deltas are 296 **0.3239**, 297 **0.2492**, 298
  **0.1784**, 299 0.1369. The band sits at 297 alone and the falsifier at 298, so the two still do
  not overlap. 296 has drifted further above the band (0.2834 at 11:45, 0.3115 at 12:15, 0.3239
  now), which is the rally mechanism WL-19 anticipated continuing to run, but IWM is still about
  0.8% short of the trigger with roughly two hours of session left. Expires at today's close unless
  a later run measures it true.

  > EXPIRED at the 2026-09-02 close, unexercised (ruled 14:40 CT). IWM's closest approach to the
  > 296 trigger was 294.25 at 14:15. WL-21 carries the same shape into tomorrow with Wes's
  > down-verdict condition.

- **WL-13** (run-1345, proposed 2026-09-01 13:45 CT as "WL-12"; renumbered by the operator in
  transcription because run-1315 had already claimed the number — both proposals exist only in
  the run logs): if SPY trades back to 765 or higher and a Sep 8 call at 775 or above measures
  inside the 0.20-0.30 delta band with credit clearing the Mid floor at natural pricing, one
  bear call at half size, short strike 775 or above. The 775 floor keeps it collision-free and
  strictly above every held short. Expires 2026-09-02 close. APPROVED by Wes 2026-09-01 14:50 CT, with the full-deployment package; executable within every ordinary limit.

  > RULING (2026-09-02 11:09 CT, Wes): STANDS to its expiry at today's close. Run-0945 flagged
  > that the trigger becomes satisfiable on a squeeze; Wes ruled "leave it". Runs measure it as
  > written and execute only if both clauses are true.

  **MEASURED FALSE, run-1115 (2026-09-02 11:18 CT).** The first clause is now true and the second
  is not, so the item does not fire. SPY quotes 765.47 × 765.50, above the 765 trigger for the
  first time since the item was written. But **no SPY Sep 8 call at 775 or above is inside the
  0.20-0.30 delta band**: 775 measures **0.1306**, and delta only falls from there (776 0.1103,
  777 0.0838, 778 0.0612, 780 0.0392). The band on the Sep 8 call side currently sits in the
  low 770s, which is where the book already holds shorts, and the 775 floor exists precisely to
  keep this item collision-free. Both clauses are required; the item stands unexercised to its
  expiry at today's close. Recorded for the operator: SPY Sep 8 declares **High** on the §3 ratio
  under reading 2 (straddle-averaged ATM IV 9.920% at the 765 strike against RV20 7.180%, ratio
  **1.382**), so had the delta clause fired, the applicable credit floor would have been the High
  one quarter of width rather than the Mid one fifth the item names — the charter's floor governs
  over the item's wording, and a run executing it should test against the regime it measures.

  **MEASURED FALSE AGAIN, run-1215 (2026-09-02 12:15 CT), now on BOTH clauses.** SPY has given back
  the move that made the first clause true at 11:18: it quotes **764.84 x 764.89**, below the 765
  trigger, so the item fails on the first clause and the second was already measured false an hour
  ago. Nothing to re-test. The item stands unexercised to its expiry at today's close, and on this
  run's reading it is very unlikely to fire in the remaining session: SPY would have to regain 765
  *and* the Sep 8 call band would have to migrate up to 775, which at 11:18 measured 0.1306 delta.

  **MEASURED FALSE A FOURTH TIME, run-1345 (2026-09-02 13:45 CT), on both clauses.** SPY quotes
  **764.67 x 764.72**, back below the 765 trigger, so the first clause fails again. The second fails
  by a wider margin than at any earlier measurement: SPY Sep 8 **775 measures 0.1066** delta, against
  0.1306 at 11:18 and 0.1159 at 12:45. The band has moved steadily *away* from 775 all day rather
  than toward it. With roughly 70 minutes of session left and one decision run remaining, the item
  cannot fire; it expires at today's close unexercised.

  **MEASURED FALSE A FIFTH AND FINAL TIME, run-1415 (2026-09-02 14:15 CT).** The first clause is
  true and the second is not, so the item does not fire, and this is the last decision run before
  its expiry: **WL-13 expires at today's close unexercised.** SPY quotes **765.28 x 765.30**, back
  above the 765 trigger. But **no SPY Sep 8 call at 775 or above is inside the 0.20-0.30 delta
  band**: 775 measures **0.1130**, 776 **0.0899**, 777 **0.0600**, 778 **0.0525**, 780 **0.0295**.
  Delta falls monotonically from 775 up, so no strike satisfying the item's own 775 floor can be in
  band at any price short of a violent rally.

  One correction to the run-1345 entry above, recorded rather than left standing: it states the band
  "has moved steadily *away* from 775 all day rather than toward it." The direction reversed in the
  final half hour — 775 read 0.1306 (11:18), 0.1159 (12:45), 0.1066 (13:45), **0.1130 now** — as SPY
  recovered 764.67 to 765.29. The magnitude conclusion is unaffected and was right: 0.1130 is not
  close to 0.20, and the 14:45 run opens nothing. Only the monotonic-drift claim was wrong.

  **MEASURED FALSE A THIRD TIME, run-1245 (2026-09-02 12:45 CT).** SPY has regained the 765 level it
  gave back at 12:15 — it quotes **765.19 x 765.22** — so the first clause is true again and the item
  turns entirely on the second, which fails by a wide margin. Measured this run, **no SPY Sep 8 call
  at 775 or above is inside the 0.20-0.30 delta band**, and the readings have moved further away
  since 11:18: 775 **0.1159** (was 0.1306), 776 **0.0932**, 777 **0.0672**, 778 **0.0586**, 779
  **0.0386**, 780 **0.0242**. The band has not migrated up toward 775; SPY's rally has been met by
  enough decay and vol compression on the Sep 8 call wing to leave 775 further out of band than it
  was ninety minutes ago. The item stands unexercised to its expiry at today's close, and on this
  run's reading it cannot fire in the remaining session.

  > EXPIRED at the 2026-09-02 close, unexercised (ruled 14:40 CT). The price clause was true on
  > and off from 09:45; the strike clause never was, since the Sep 8 775 call read 0.11 to 0.14
  > delta all day after the morning's implied-vol collapse.

- **WL-22** (run-1245, proposed 2026-09-02 12:45 CT → **GRANTED 2026-09-02 12:53 CT**, binding through the 14:15 run → **SPENT 2026-09-02 14:40 CT**): **an interim stop on IWM bear-put tranches
  for the remainder of today.** This asks the operator to bind this agent tighter than the charter
  does. It authorizes nothing and it names no new trade.

  Proposed rule, for the three remaining decision runs today (13:15, 13:45, 14:15 CT): **no further
  IWM Sep 8 bear put debit vertical is opened without an explicit operator ruling.** Nothing else
  changes; every other name and structure is governed as usual.

  Why this run is asking, having just taken the trade it wants stopped. The book held no IWM at
  09:30 and now holds three bear-put tranches — 293/290 (23c), 292/289 (31c) and this run's 294/291
  (21c) — **$7,300 of ledger max loss, 7.8% of equity, all on one 3-day directional read that
  resolves on Friday's payrolls print.** Each was individually legal and each will keep being legal:
  the memo's IWM thesis is the only directional read on the board, §3 declares Mid on IWM Sep 8, and
  §3's Mid tactical clause admits a half-size debit vertical. So the argument this run accepted at
  12:45 is available unchanged at 13:15, 13:45 and 14:15, and on today's pace the stack reaches five
  tranches and roughly $12,000 by the close without a single rule being bent. That is the design
  item 20 concentration gap producing an outcome, not a hypothetical.

  Why it is not a re-file of WL-10, which was routed to the design pass on 2026-09-01. WL-10 asked
  for a **standing** per-underlying-and-direction sub-cap and correctly stalled on the denominator
  question (max loss overstates a stopped book; credit collected is the honest measure for credit
  spreads). This asks for none of that. It names one underlying, one direction, one expiry, and
  three runs, and it needs no denominator because it is a count, not a dollar limit. The design
  question stays where it was routed.

  **The case against granting it, which the operator should weigh, because it is the case this run
  acted on.** The entry improved rather than deteriorated: IWM rose 1.03% today (290.57 close to
  293.55), so the same thesis is available at a cheaper debit and with more room before its own ~298
  falsifier than at 11:18, when this book bought the first tranche at a worse price. Declining now
  while having bought twice higher is inconsistent unless the reason is portfolio concentration
  rather than thesis quality — which is precisely why the ask is framed as a concentration stop and
  not as a doubt about the read. And the book is deployed at $30,012 of an $85,000 cap on the
  second-to-last trading day before the deadline, so §5's idle-capital clause pushes the other way.

  **Recorded caveat, the one that would make this run wrong.** The memo names its own strongest
  counter-evidence, this morning's 38,000 ADP print, and says that if Friday confirms the cooling
  "this is the index that recovers hardest". A three-tranche IWM bear-put stack is short exactly
  that tail, and it sits on top of a SPY short-call book that is also short delta. The loss is
  bounded — each tranche carries a §4 value stop at half its debit and the three together cannot
  lose more than $7,300 — but the correlation is real and the ledger nets none of it.

  Not executable; it names no trade. If the operator declines, this run's own restraint stands as
  the only limit: it took one open rather than two, and it will not be the run that adds a fourth.

  > RULING (2026-09-02 12:53 CT): GRANTED, session operator standing in. For the 13:15, 13:45 and
  > 14:15 runs today, **no further IWM Sep 8 bear put debit vertical is opened without an explicit
  > ruling from Wes.** Nothing else changes: every other name and structure is governed as usual,
  > the three held tranches stand under their stamped §4 exits, and WL-21 (tomorrow, the credit
  > side) is untouched. Grounds: a count-based stop on one name, one direction, one expiry, for
  > three runs is a tighter bind than the charter, which is the conservative direction the
  > standing-in delegation covers; $7,300 of one three-day read into Friday's print, on top of a
  > short-delta SPY book the ledger nets nothing against, is the design item 20 gap producing an
  > outcome, as the run says. The case against, which the run stated fairly (the entry improved,
  > and §5 pushes toward deployment), is real and is why this is a today-only stop and not a rule:
  > Wes can lift it with a word, and the design pass owns the standing answer. This ruling stays
  > under approved intents while it binds and moves to ruled at the close.

  > SCOPE CLARIFIED (2026-09-02 13:26 CT), on run-1315's question, session operator standing in:
  > the stop is read by its substance. For the 13:45 and 14:15 runs today, **no new IWM position
  > of any expiry or structure that adds to the memo's bearish IWM read** (bear put debit
  > vertical, bear call credit spread, or any short-delta structure on IWM) is opened without an
  > explicit ruling from Wes. This narrows the agent further, which is the delegation's direction.
  > WL-21 is tomorrow's and unaffected; the three held tranches stand under §4.

  > CLOSED (2026-09-02 14:40 CT): the stop bound the 13:15, 13:45 and 14:15 runs as written and
  > each abstained on IWM under it; no fourth tranche was opened. It does not carry to tomorrow;
  > the standing concentration question is design items 15 and 20.

- **WL-24** (run-1415, proposed 2026-09-02 14:15 CT → **ROUTED TO THE DESIGN PASS 2026-09-02 14:40 CT**, folded into design item 27): **SPY Sep 8 crossed the Mid/High boundary
  between two consecutive decision runs.** This is **evidence appended to design item 28's second
  finding and to item 27, not a new item**, and it names no trade. Filed because the crossing converts
  a near-miss into an observation, on the book's most-traded underlying, inside a single 30-minute
  decision interval — and because the neighbour check turned it into an ATM-strike finding too.

  **The measurement, this run's own.** RV20 was recomputed from daily bars through the 2026-09-01
  close rather than carried, and reproduces run-0845, run-0915, run-1045, run-1115 and run-1345
  exactly: SPY **7.180%**, QQQ **13.173%**, IWM **12.023%**, DIA **8.013%**. Straddle-averaged ATM
  IV, quotes fresh to the second, spot SPY 765.28 x 765.30:

  | name | expiry | DTE | straddle-avg ATM IV | ratio | regime |
  |---|---|---|---|---|---|
  | SPY | Sep 8 | 6 | 9.330% @765 (C 9.42 / P 9.24) | **1.2995** | **Mid — ambiguous, see below** |
  | QQQ | Sep 8 | 6 | 13.785% @708 (C 13.81 / P 13.76) | 1.0465 | Mid |
  | IWM | Sep 8 | 6 | 14.080% @294 (C 13.98 / P 14.18) | 1.1711 | Mid |
  | DIA | Sep 4 | 2 | 11.770% @530 (C 12.19 / P 11.35) | 1.4688 | High |

  **The finding, and it is two findings rather than one.** run-1345 measured SPY Sep 8 at **1.3057 —
  High** at 13:45 and flagged it as "inside 0.5% of the boundary," a third distinct route to the 1.30
  edge. Thirty minutes later the same underlying, the same expiry, the same estimator and the same
  strike read **1.2995 — Mid**, 0.04% the other side. Same book, same rule, opposite regime labels,
  one decision interval apart.

  **The sharper half: at a single instant, the label also depends on which strike is called ATM.**
  This run checked the neighbours — which the first draft of this item did not, and should have,
  precisely because a reading on an edge is where the ATM choice stops being cosmetic:

  | strike | call IV | put IV | straddle avg | ratio | regime |
  |---|---|---|---|---|---|
  | 764 | 9.59% | 9.46% | 9.525% | **1.3267** | **High** |
  | **765** (nearest, spot 765.29) | 9.42% | 9.24% | **9.330%** | **1.2995** | **Mid** |
  | 766 | 9.06% | 9.11% | 9.085% | 1.2654 | Mid |

  So the declaration turns on the ATM choice, at one instant, with no time passing at all: the strike
  one dollar below the money reads High and the nearest strike reads Mid. §3 pins its denominator's
  estimator and names neither its numerator's expiry (item 22) nor its numerator's **strike** (item
  27), and this is item 27 firing at the boundary rather than in the abstract. The drift is ordinary
  put skew, monotonic across the three strikes; nothing here is a data artifact.

  Taken together, §3's ambiguity rule plainly binds: SPY Sep 8 is **ambiguous** ("straddling a band
  edge ... still resolve to abstain"), and that is the handling this run applied. It cost nothing
  today only because SPY was independently closed on the read. On a day when the read is open, this
  same configuration decides whether a spread is legal at a one-quarter or a one-fifth floor, and
  two runs measuring the same market one strike apart would answer differently.

  Why it is worth recording rather than shrugging at. Items 22 and 23 concern *which expiry* supplies
  the numerator; this one turns on the **level of the ratio itself**, so neither would catch it, which
  is exactly what run-1345 said. What is new is that the instability is no longer hypothetical: the
  regime label on SPY was not stable across one cadence interval. The 2026-08-31 amendment pinned the
  RV estimator because "a rule that does not name its estimator is not deterministic"; a pinned
  estimator still yields a label that flips on a 0.05-vol-point move in the numerator when the ratio
  sits on an edge. Whether the fix is a hysteresis band, a rounding convention, or an explicit
  "straddle the edge → abstain" tolerance written into §3 rather than inferred from §1, is the design
  pass's call. **Nothing here asks for the bands to move.**

  **Second finding, flagged, no action proposed — the circuit breaker's denominator drifts with
  deployment.** §5 sets the breaker at -25% of the account and justifies the number against a book
  deployed near the $85,000 cap: "an ordinary day is now roughly plus or minus 7% and -25% fires at
  about three and a half times that." The book is deployed at **$30,012**, 35% of that cap. Today's
  account move is **-$7,432, -7.42%** (equity 92,679.90 against last_equity 100,111.95), which is
  **24.8% of the capital actually at risk** — and the breaker was never within sight of firing. Scaled
  to this deployment, the charter's own model puts an ordinary day near ±2.5% of account, so today ran
  about 3x ordinary while the breaker sat ~10x away rather than the ~3.5x its rationale intended. The
  breaker is a fixed fraction of equity; the exposure it is meant to guard varies by a factor of three
  as the book fills. This is the WL-10 denominator question in a second place, and the answer may
  simply be that the value stops are the real guard and the breaker is a backstop — but the ceremony
  should decide that on purpose rather than inherit it. Recorded, not proposed.

  Not executable; it names no trade.

  > RULING (2026-09-02 14:40 CT): ROUTED, session operator standing in, into design item 27
  > (which strike is ATM), filed at 13:26 from run-1315's SPY reading and now confirmed a second
  > time at a single instant: 764 reads 1.3267 High, 765 reads 1.2995 Mid. Change C of tonight's
  > package pins the strike nearest spot and treats neighbours crossing the edge as ambiguity, so
  > this case resolves to abstain from tomorrow; the pass decides whether that is the intended
  > frequency. Never named a trade; not executable.

- **WL-23** (run-1345, proposed 2026-09-02 13:45 CT → **ROUTED TO THE DESIGN PASS 2026-09-02 13:55 CT**, design item 28): **the §7 memo states its volatility theses in level terms while §3 reads volatility as a ratio, and today that mismatch closed the long-premium book on all four names.** Amendment candidate for tonight's ceremony, not an executable standing intent. It names no trade.

  **The measurement, this run's own, all four admitted names and every expiry inside §3's 2-to-7 DTE
  window.** RV20 recomputed from daily bars through the 2026-09-01 close, reproducing run-0845,
  run-0915, run-1045 and run-1115 exactly (SPY 7.180%, QQQ 13.173%, IWM 12.023%, DIA 8.013%).
  Straddle-averaged ATM IV, quotes fresh to the second:

  | name | expiry | DTE | straddle-avg ATM IV | ratio | regime |
  |---|---|---|---|---|---|
  | SPY | Sep 4 | 2 | 12.680% @765 | 1.766 | High |
  | SPY | Sep 8 | 6 | 9.375% @765 | **1.306** | High |
  | SPY | Sep 9 | 7 | 9.910% @765 | 1.380 | High |
  | QQQ | Sep 4 | 2 | 17.795% @708 | 1.351 | High |
  | QQQ | Sep 8 | 6 | 13.420% @708 | 1.019 | Mid |
  | QQQ | Sep 9 | 7 | 14.410% @708 | 1.094 | Mid |
  | IWM | Sep 4 | 2 | 19.090% @294 | 1.588 | High |
  | IWM | Sep 8 | 6 | 14.125% @294 | 1.175 | Mid |
  | DIA | Sep 4 | 2 | 11.675% @530 | 1.457 | High |

  **No admitted name reaches Low on any expiry in the window.** This run extended the search to
  **Sep 9 (7 DTE)**, which no earlier run today had measured, precisely because "no strike reaches
  Low" is a claim of absence and deserved a check rather than a restatement. It does not help: Sep 9
  reads *higher* than Sep 8 on both names carrying it (SPY 1.380 vs 1.306, QQQ 1.094 vs 1.019), so
  the term structure closes the gap rather than opening it. QQQ Sep 8 at the neighbouring 707 strike
  reads 1.038, so the Mid declaration does not turn on the ATM choice. DIA returned no Sep 8
  contracts on this run's query, so Sep 4 is its only in-window expiry.

  **The finding.** Today's memo calls near-dated implied volatility "cheap" on SPY, QQQ and IWM.
  §3 measures all three as rich: implied exceeds realized on every one of the nine readings above.
  These are not contradictory observations but two different measurements. The memo is reading the
  **level** — its SPY basis cites "the broad volatility gauge only around 16" — and §3 reads the
  **variance risk premium**. The 2026-08-31 amendment already adjudicated exactly this pair and chose
  the ratio, in terms that fit today without alteration: "the absolute bands read the level of
  implied volatility, and a premium seller earns implied minus realized ... The two rules gave
  opposite instructions and the absolute one could not see realized volatility at all."

  **Why this closed the book rather than merely reading oddly.** §2's volatility conviction shape
  requires that "measured IV sits in the low band" and is "falsified by ... the regime leaving the
  low band". A volatility thesis is therefore only expressible in a Low regime, and no name is in
  one. Two of the three cheap-vol theses are additionally falsified by their **own stated tests** on
  this run's numbers: QQQ's falsifier is "a measured reading of near-dated QQQ pricing shows the
  macro premium already carried" (1.019 to 1.351 across the window — carried), and IWM's is "a
  measured near-dated reading shows the event premium already present" (1.175 to 1.588 — present).
  SPY's stated falsifier is **not** met: it asks whether pricing "richens materially before Friday",
  and SPY Sep 8 has *cheapened*, 1.382 at 11:18 to 1.306 now. Yet SPY is unplayable anyway, because
  it reads High on all three of its expiries and §3's High row says sell premium. That is the
  sharpest form of the mismatch — a live, unfalsified memo thesis that the charter can never permit
  a run to act on — and neither document records that this is possible.

  **Proposed shape, offered as a direction rather than a preference.** The no-lean package's Change B
  fixed the memo's *directional* vocabulary by requiring one of four verdicts. The volatility side
  got no such treatment and wants the same thing: have the §7 pass state its volatility claim as a
  ratio against realized volatility computed with §3's own estimator, and return a verdict from a
  fixed set. Then (a) a run can test the thesis against the same number it declares the regime with,
  and (b) "cheap vol" and a High declaration cannot both be produced from one market. What matters
  more than the exact wording is that the memo and the charter stop measuring volatility with two
  different instruments and calling both of them volatility.

  **Second finding, flagged, no action proposed.** SPY Sep 8 reads **1.3057** against the Mid/High
  edge of 1.30 — inside 0.5% of the boundary, the closest any reading has come today. It changes
  nothing on this board: both regimes instruct sell premium, §5's Mid half-size rule was removed on
  2026-09-01 so the position cap is $5,000 either way, and SPY is blocked on the read regardless. It
  is recorded because it is a third distinct route to the boundary that design items 22 and 23
  concern, and this one turns on the **level of the ratio itself** rather than on which expiry
  supplies the numerator, so neither pending item would catch it.

  Not executable; it names no trade.

  > RULING (2026-09-02 13:55 CT): ROUTED TO THE DESIGN PASS as item 28 (the run wrote 27; 27 was
  > taken at 13:26 by the ATM-strike gap), session operator standing in. The finding is accepted:
  > the memo states volatility as a level and §3 reads it as a ratio, so a memo long-vol thesis
  > can be live and unfalsified while §3 forbids acting on it. The operator adds the other half:
  > that outcome is the charter's design, not only an interaction. §2's volatility shape requires
  > measured Low because buying premium is the one trade the book makes on the measurement rather
  > than on a read; the memo names the event, §3 says whether the premium is cheap. Change A of
  > tonight's package already makes the memo's vol opinion advisory on the income side; the
  > design pass decides whether the prompt should stop asking for a vol verdict it cannot act
  > on, or ask for one stated in §3's own terms. Never named a trade; not executable.

- **WL-20** (run-1145, proposed 2026-09-02 11:45 CT → **ROUTED TO THE DESIGN PASS 2026-09-02 11:58 CT**, design item 26; the ceremony question referred to Wes): **the band/falsifier gap survives tonight's
  ceremony.** Amendment candidate, not an executable standing intent. It names no trade.

  **First, a correction to this run's own initial framing, recorded rather than quietly dropped.**
  This item was drafted as a finding that §2's read requirement can veto every row of §3's table
  and did so today. That finding is **not new and is already ratified**: it is the evidence base
  of the no-lean package [read: ~/Code/alpaca-hackathon/drafts/AMENDMENT-s2-s3-s7-no-lean.md:18-27],
  whose Changes A and B Wes ratified at 11:24 CT today and which cites the identical combination
  ("Three names closed for five runs on that one combination"). The run opened the draft before
  filing rather than after, so the duplicate never reached the operator as a fresh finding. What
  follows is only the residue the package does not reach.

  **The residue.** The package fixes the *no-verdict* case: after Change A a two-sided or
  range-bound verdict admits a condor, and after Change B the memo must return one of four
  verdicts. Today's IWM is the other case, and it is untouched. IWM **has** a verdict — the memo's
  only directional read, bearish, falsified above roughly 298 — and Change A leaves a "down"
  verdict admitting exactly what it admits now, a bear call. That bear call is blocked by a
  mechanism neither Change A nor Change C addresses:

  **§2's 0.20-0.30 delta band and the 09:24 ruling's falsifier floor do not currently intersect on
  IWM, on either in-window expiry.** Measured this run at spot 293.12, Sep 8 call deltas 296
  **0.2834**, 297 **0.2143**, 298 **0.1592**, 299 **0.1123**; Sep 4 296 **0.2354**, 297 **0.1602**,
  298 **0.1113**. Every strike inside the band is below the falsifier; every strike at or above the
  falsifier is outside the band. The 09:24 ruling requires the short at or above the falsification
  level so that position and thesis fail together, which is sound and is why WL-17 was rejected —
  but combined with the band it means a **correct, live, unfalsified directional read produces no
  legal trade**, and it will keep doing so whenever a memo's falsifier sits more than roughly 1.5%
  out of the money. That is a rule interaction, not a market condition, and it is the same *shape*
  as the interaction the no-lean package was written to fix, one layer down.

  This run is not proposing a resolution and is explicitly not asking for the band to move; the
  package's own decision item leaves the band alone on the recommendation, and a run should not
  reopen that from underneath. What it asks is that the falsifier floor be recorded as a **rule**
  somewhere durable rather than living only in a rejection ruling, and that whoever writes it down
  price this interaction — because as an unwritten operator ruling it is currently invisible to
  §3, to the gate, and to the next run that measures a compliant-looking 296/297.

  **Second finding, flagged, no action proposed.** The package's item 3 (design item 24, SPY's
  delta band exhausted by held legs) still holds at 11:48, three hours after the 09:45 observation
  it was filed on, and it is sharper than recorded. SPY Sep 8 in-band shorts are 770 (0.2946), 771
  (0.2548) and 772 (0.2123). The book already holds 770 and 771 as shorts and **772 as a long**
  (27 contracts), so selling 772 is WL-11's leg collision. Of the spreads that clear the measured
  High floor of one quarter at natural pricing — 770/772 at 0.57 against 0.50, and 770/773 at 0.76
  against 0.75 — **both are identical-leg duplicates of ledger rows already open**
  (run-0915-spy-bearcall-770-772 and run-1215-spy-0908-770-773). So on today's board WL-14's
  identical-leg aggregation (design item 21) and WL-11's collision check (item 20's sibling) are
  not hypothetical: they are the only two things standing between the book and a further $4,800 of
  economically-identical SPY short-call risk, and today they bind through judgment rather than
  through the gate, exactly as WL-14 warned.

  > RULING (2026-09-02 11:58 CT): ROUTED TO THE DESIGN PASS as item 26, session operator
  > standing in, and the residue is owned here: the "short strike at or above the falsifier"
  > condition exists only because the 09:24 ruling attached it to WL-17's re-file path. It is
  > not a charter rule. Section 2's band and floor are the charter's placement rules, and a
  > bear call at 296/297 on a down verdict is legal under them as written; the falsifier
  > governs the thesis, the value stop governs the position. The operator standing in should
  > not have invented a placement rule the charter does not carry, for the same reason section
  > 1 tells a run not to. Whether to withdraw that condition tonight, so a down verdict on IWM
  > has a legal expression tomorrow, or to write the position-and-thesis-fail-together rule
  > into section 2 text, is put to Wes with the package. Never named a trade; not executable.

- **WL-12** (run-1315, proposed 2026-09-01 13:15 CT → **SPENT 2026-09-02 11:25 CT**, trigger measured absent on the pass it named; transcribed from the run record by the
  operator 2026-09-01 13:55 CT — the run did not write it into this file): if the next §7
  research pass carries a SPY read that is up-or-sideways in the §2 sense, a decision run may
  open one SPY bull put spread at half size, subject to every ordinary limit and the collision
  check. Rationale as filed: the only admitted structure that would diversify the book's
  single-question concentration rather than deepen it. Expires 2026-09-04 close. APPROVED by Wes
  2026-09-01 14:50 CT, with the full-deployment package (commit 40b94ca); executable within every ordinary limit. Text corrected 2026-09-02 08:05 CT: the approval commit re-ordered this entry but left its status line unchanged.

  **MEASURED FALSE, run-1115 (2026-09-02 11:18 CT), with a reading question for the operator.**
  Today's §7 memo opens its SPY section "Directional thesis: No thesis" and takes no view over the
  window, so there is no up-or-sideways read and the item does not fire. The question the run
  declines to answer alone: the trigger names "the **next** §7 research pass", and today's pass was
  that one, which would make the item already spent rather than live to its stated 2026-09-04
  expiry. The run treats it as live and simply unfired, which is the conservative reading, and
  flags the ambiguity rather than resolving it. It cannot fire again before tomorrow's pass in
  either reading.

  > RULING (2026-09-02 11:25 CT): SPENT, session operator standing in, on run-1115's reading.
  > The intent is gated on "the next §7 research pass" carrying an up-or-sideways SPY read.
  > That pass was today's 08:15 memo and it carried "No thesis" for SPY, so the trigger has
  > resolved false and the item has nothing left to wait for; its 2026-09-04 expiry was the
  > outer bound, not a promise to re-test on each later memo. Conservative direction: this
  > removes standing authority rather than extending it. Reversible by Wes: if he wants a SPY
  > bull put standing through Friday under the amended §2 verdict vocabulary, that is a fresh
  > approval on tomorrow's memo, not this item.

- **WL-18** (run-1045, proposed 2026-09-02 10:45 CT → **APPROVED by Wes 2026-09-02 11:09 CT**, §3 reading 2 named for the day → **EXECUTED 2026-09-02 11:18 CT by run-1115**; the opening authorization is spent, see the execution account at the end of this entry): **IWM Sep 8 bear put debit vertical, gated
  solely on Wes naming §3 reading 2.** This does not re-ask design item 22, and unlike WL-17 it
  proposes no interim rule of its own. It records that the pending numerator question is not only
  a credit-floor question, and names the one trade in the book's universe whose legality turns on
  nothing else.

  **What is new.** Item 22 was filed and routed as a *floor* problem: the two in-window readings
  set the credit floor at one quarter or one fifth, and WL-17 showed a candidate that cleared the
  stricter floor and so was legal either way. On the **debit** side the same ambiguity behaves
  differently, and worse. §3's High row instructs *sell premium*; §3's Mid row (as amended
  2026-09-01) permits the tactical book to *buy* a half-size debit vertical on a named-falsifier
  memo thesis. So for a debit vertical the two readings do not disagree about a floor, they
  disagree about whether the structure may be placed at all, and §3's closing sentence makes a
  strategy that contradicts its declared regime invalid. There is no "clears the stricter test"
  escape available here, because the stricter reading forbids the structure outright.

  **This run's own measurement**, RV20 12.023% through the 2026-09-01 close (recomputed from daily
  bars; reproduces run-0845 and run-0915 exactly), spot 292.80, quotes fresh to the second:

  | expiry | straddle-avg ATM IV @293 | ratio | regime |
  |---|---|---|---|
  | IWM Sep 4 (2 DTE) | 19.795% (C 20.24 / P 19.35) | **1.647** | High |
  | IWM Sep 8 (6 DTE) | 14.320% (C 14.07 / P 14.57) | **1.191** | Mid |

  Neighbouring strikes hold both readings (Sep 4: 1.659 @292.5, 1.683 @292; Sep 8: 1.208 @292), so
  neither declaration turns on the ATM choice. The straddle has now persisted across four
  measurements today and both sides have drifted *down* without converging (Sep 4 1.752 → 1.683 →
  1.647; Sep 8 1.256 → 1.202 → 1.191).

  **Why the credit side cannot substitute, measured rather than assumed.** The 09:24 ruling left a
  re-file path open for an IWM bear call at a short strike at or above the memo's ~298
  falsification level. That path is closed at this spot on both in-window expiries: IWM 298 measures
  **0.1038** delta on Sep 4 and **0.1540** on Sep 8, both outside §2's 0.20-0.30 band. So no choice
  of §3 reading makes a compliant IWM bear call exist today. The debit vertical is the only IWM
  structure the pending ruling actually unlocks.

  **The thesis is the memo's, unchanged and unfalsified.** Today's §7 memo carries a bearish IWM
  directional read — the trend break below the 50-day, wrong on a reclaim and close above roughly
  298 — and it is the only directional thesis in the memo across all four admitted names. IWM at
  292.80 sits well below 298, so the thesis stands. A bear put debit vertical is the §2 tactical
  structure for exactly this shape, and the position and the thesis fail together: if IWM rallies
  through 298 the vertical is worth zero and the thesis is falsified in the same move.

  **If approved under reading 2, the board as measured this run** (recorded so the executing run
  need not re-derive it; it re-measures before acting). Natural debit is ask(long) − bid(short):

  | structure | width | natural | mid | max profit at natural | qty at $2,500 | max loss |
  |---|---|---|---|---|---|---|
  | IWM Sep 8 **293/290** | 3.00 | **1.09** | 1.01 | 1.91 | 22 | $2,398 |
  | IWM Sep 8 292/289 | 3.00 | 0.88 | 0.85 | 2.12 | 28 | $2,464 |
  | IWM Sep 8 291/288 | 3.00 | 0.70 | 0.66 | 2.30 | 35 | $2,450 |
  | IWM Sep 8 293/288 | 5.00 | 1.44 | 1.38 | 3.56 | 17 | $2,448 |

  293/290 is the primary: it is long the ATM put, so it pays on the modest two-to-three session
  drift the memo actually describes, rather than needing a 0.6% decline just to reach its long
  strike. §3's Mid tactical clause caps max loss at **$2,500** by its own words; §5's 2026-09-01
  amendment removed the *income* half-size rule and does not reach this cap. §4 exits would be
  stamped TP 2.045 (debit plus half of width minus debit) and stop 0.545 (half the debit); this is
  a single directional vertical, not a pair, so it carries a value stop normally. No collision: the
  book holds no IWM leg at any strike or expiry, and 10 of 20 slots are free.

  **Three caveats recorded rather than glossed, since WL-17 was rejected for understating risk.**
  *Calendar:* today is Wednesday 2026-09-02; Sep 8 is Tuesday (Monday Sep 7 is a market holiday),
  and Friday's payrolls print lands 07:30 CT on Sep 4, **inside** the position's life. This
  position carries the event, deliberately — that is what long premium on a directional thesis into
  a dated binary means, and the loss is bounded at the debit, which is the reason this is the debit
  side rather than the credit side that the 09:24 ruling refused. *Adverse tail:* the memo names
  its own strongest counter-evidence, this morning's 38,000 ADP print, and says that if Friday
  confirms the cooling "this is the index that recovers hardest". The bet therefore has a large
  adverse tail at the event it carries; bounded at roughly $2,400, not unbounded, and that
  boundedness is the argument, not a claim that the tail is small. *Concentration:* the book already
  carries $12,000 of SPY short-call risk, which is short delta. This adds short delta. It deepens
  the book's directional tilt rather than diversifying it, which is the WL-10 concern (routed,
  design item 20) showing up in a second name.

  **What is being asked.** Either (a) Wes names reading 2 (the expiry the trade itself uses) as the
  §3 numerator rule, in which case a decision run may open one IWM Sep 8 bear put debit vertical at
  the §3 Mid half-size cap on its own re-measurement; or (b) he names reading 1 or 3, in which case
  IWM stays unplayable and this item expires unexercised. Not executable unless (a). Expiry:
  2026-09-03 close, since a Sep 8 entry later than Thursday is a materially different trade against
  a three-session thesis.

  **Second finding, flagged, no action proposed — item 22 is now firing on half the admitted
  universe.** QQQ straddles the same boundary on this run's measurement: Sep 4 straddle-averaged ATM
  IV 18.42% @709 → **1.398 High**, Sep 8 13.91% @709 → **1.056 Mid**, against RV20 of 13.173%. That
  is two of four admitted names straddling 1.30 in one session, after run-0915 recorded the same
  pair. One point of arithmetic the operator may find useful: from tomorrow, Sep 4 is 1 DTE and
  therefore falls out of §3's own 2-to-7 DTE window, leaving only post-payrolls expiries in the
  band, so today's straddles should resolve themselves without a ruling. That is why the ask above
  is scoped to today and tomorrow rather than to the ceremony's timetable — but the mechanism WL-15
  identified will recur on every event week, so item 22 still needs its answer.

  > RULING (2026-09-02 11:09 CT, Wes): APPROVED. Wes names **§3 reading 2**: the regime that
  > governs a structure is measured on the expiry the structure itself uses. This is an operator
  > ruling under the charter, recorded here and on the rulings tape, not a charter text change;
  > the numerator question still goes to the ceremony as design item 22, and this reading holds
  > for 2026-09-02 and 2026-09-03 (this item's expiry), after which the ceremony decides. It
  > applies to every admitted name, not only to this trade: a run declaring a regime for a Sep 8
  > structure reads the Sep 8 surface, and for a Sep 4 structure the Sep 4 surface. Under it, one
  > IWM Sep 8 bear put debit vertical may be opened by a decision run at the §3 Mid tactical cap
  > ($2,500 max loss), on the run's own re-measurement of regime, strikes and the memo's thesis
  > (IWM below ~298), subject to every ordinary limit and the collision check. The 09:24 credit-
  > side conditions are unchanged and still block an IWM bear call at this spot. Executable.
  > Expires 2026-09-03 close as filed. (Transcribed by the session operator from Wes's ruling
  > "reading 2", given in chat at 11:09 CT.)

  **EXECUTION (run-1115, 2026-09-02 11:18 CT).** Filled, at better than the limit. **IWM Sep 8
  293/290 bear put debit vertical, 23 contracts, order 7bf08eb9**, filled 16:18:14Z at a **1.03**
  average (long 293P @ 2.04, short 290P @ 1.01) against a 1.05 limit, so $2,369 was actually paid.
  The gate parsed it `debit_vertical` and stamped $2,415 of max loss at the limit price, with
  §4 exits **TP 2.025 / stop 0.525**; not a vol pair, so it carries a value stop normally. This
  is 1 of the run's 2 opens and takes the book to 11 of 20 slots.

  Every gate measured on this run's own reading, not inherited. **Regime, §3 reading 2 as ruled:**
  IWM Sep 8 straddle-averaged ATM IV at the 293 strike (call 14.58%, put 14.43%) is **14.505%**
  against RV20 of **12.023%** through the 2026-09-01 close, a ratio of **1.206 — Mid**. RV20 was
  recomputed from daily bars and reproduces run-0845, run-0915 and run-1045 exactly. Neighbouring
  strikes read 1.234 (292) and 1.162 (294), so the declaration does not turn on the ATM choice, and
  nothing sits near either edge. Spot 293.18, quotes fresh to the second, both legs deep (293P ask
  ×75, 290P bid ×284, against 23 contracts). **Sizing:** §3's Mid tactical clause caps max loss at
  $2,500; $2,415 is inside it. **Thesis:** the §7 memo's bearish IWM read, falsified on a reclaim
  and close above roughly 298; IWM at 293.18 is 1.6% below that, so it stands. **Collision and
  anti-offset:** the book held no IWM leg at any strike or expiry. **Book caps:** aggregate open
  risk $22,712 → $25,127 against $85,000; tactical book $10,712 → $13,127 against $60,000.

  Two things recorded rather than glossed, both moving against the trade since it was filed.
  IWM has risen intraday, 290.57 at yesterday's close and 292.80 when run-1045 measured it, to
  293.18 now, so the two-to-three session drift the memo describes has reversed today; the thesis
  is not falsified, which requires a close above ~298, but the run is buying it a day into a bounce
  and the priced debit is correspondingly lower (natural 1.049 now against 1.09 at 10:45). And the
  concentration caveat in the filing is now larger than it was: SPY has rallied to 765.5, the four
  SPY Sep 8 bear calls sit at 1.14x to 1.51x their credits, and this adds short delta to a book
  already leaning that way. That is design item 20, unchanged and still unruled.

- **WL-17** (run-0915, proposed 2026-09-02 09:15 CT → **REJECTED 2026-09-02 09:24 CT**, interim-rule question referred to Wes): **an interim expiry rule for §3's numerator,
  for the remainder of today only, with the trade it would authorize measured and attached.** This
  does not re-ask WL-15's question, which is routed to the ceremony as design item 22. It asks the
  narrower one the ceremony's timetable leaves open: what a run may do *today* while §3's gap
  stands. Filed knowing the operator ruled at 08:57 that a straddled boundary is ambiguous and §1
  resolves it toward abstention; this run followed that ruling and abstained. What is offered here
  is new measurement, not a re-argument.

  **What changed since run-0845.** That run measured an IWM **Sep 8** 296/297 bear call at 0.25 mid
  / 0.21 natural, clearing the Mid floor and failing the High one — so the regime choice decided its
  legality, and the run abstained. Measured this run at spot 293.32, the **Sep 4** board now carries
  a candidate that clears the **High** floor at **natural** pricing:

  | structure | short δ | width | natural | mid | High floor | Mid floor |
  |---|---|---|---|---|---|---|
  | IWM Sep 4 **296/297** | 0.2971 | 1.00 | **0.26** | 0.275 | 0.25 | 0.20 |
  | IWM Sep 4 296/297.5 | 0.2971 | 1.50 | 0.41 | 0.42 | 0.375 | 0.30 |
  | IWM Sep 8 297/299 | 0.2663 | 2.00 | 0.39 | 0.445 | 0.50 | 0.40 |
  | IWM Sep 8 297/298 | 0.2663 | 1.00 | 0.17 | 0.225 | 0.25 | 0.20 |

  The consequence worth the ruling: **Sep 4 296/297 needs no favourable pricing assumption and no
  favourable floor assumption.** It clears the stricter of the two floors at the worse of the two
  prices, with a short delta inside the 0.20-0.30 band. It is therefore legal under WL-15's proposed
  reading 1 (nearest expiry at or beyond 2 DTE — Sep 4, High) and under reading 2 (the expiry the
  trade itself uses — Sep 4, High), and blocked only under reading 3 (unanimity across the band).
  Two of the three readings the operator itself enumerated permit it; the strictest does not.

  **The regime measurement, this run's own, both in-window expiries, RV20 12.023% through the
  2026-09-01 close** (recomputed from daily bars, reproduces run-0845 exactly): IWM Sep 4
  straddle-averaged ATM IV 20.235% at the 293 strike → ratio **1.683 High**; Sep 8 14.455% at 293 →
  **1.202 Mid**. Neighbouring strikes hold the readings (Sep 4: 1.704 at 292.5, 1.647 at 294; Sep 8:
  1.243 at 292, 1.190 at 294), so neither declaration turns on the ATM choice, and Sep 8 has moved
  further from the boundary than it was at 08:45 (1.202 against 1.256). The straddle is stable, not
  a rounding artifact.

  **The read behind it is the memo's, not this run's.** Today's §7 memo carries a bearish IWM
  directional thesis — the trend break below the 50-day, falsified on a reclaim above roughly 298 —
  which is the "down or sideways" §2 requires for a bear call. It is the **only** directional read
  in today's memo across all four admitted names. A 296 short strike sits above the memo's own
  falsification level, so the position and the thesis fail together rather than separately.

  **If approved, sizing as the charter gives it** (High permits full size; the numbers are recorded
  so the executing run need not re-derive them, and it re-measures before acting): 67 contracts at a
  $0.26 credit is $4,958 max loss and $1,742 collected, inside the $5,000 cap. Stamped exits would be
  TP 0.13 and stop 0.52. No collision: the book holds no IWM leg at any strike or expiry.

  **Two caveats recorded rather than glossed.** The 296 call quotes 0.79 bid × **5** against 0.80 ask
  × 245 — the market is one cent wide, so a resting sell near 0.795 is realistic, but the displayed
  bid depth will not absorb 67 contracts at once and the executing run should expect to work the
  order rather than lift a bid. And this is a 2 DTE credit spread whose expiry sits one day before
  Friday's payrolls print, so the position expires *before* the event the memo names; that is
  deliberate and is the conservative side of the calendar, but it also means the elevated Sep 4
  premium being sold is event premium the position does not have to carry.

  **What is being asked, precisely.** Either (a) name an interim numerator rule for the rest of
  2026-09-02 — reading 1 or reading 2, both of which make this trade's regime declarable as High —
  or (b) confirm that reading 3 governs until the ceremony, in which case IWM stays unplayable today
  and this item expires unexercised. Not executable unless (a). Expiry: 2026-09-02 close, since a
  Sep 4 entry later than today is a different trade.

  **Second finding, flagged, no action proposed.** The same defect appeared today on a second name:
  **QQQ straddles the identical boundary**, Sep 4 straddle-averaged ATM IV 20.02% at the 708 strike
  → **1.520 High**, Sep 8 14.72% → **1.117 Mid**, against RV20 of 13.173%. Design item 22 is
  therefore not an IWM quirk; it fired on two of four admitted names within one session. Note also
  that QQQ Sep 8 read **0.830 Low** yesterday and reads Mid today, mostly because RV20 fell from
  17.31% to 13.17% as the estimator's window rolled off a large return — so the WL-6 volatility
  pair's Low-regime basis no longer holds. §4 forbids re-deriving a live position's exits and none is
  attempted; this is recorded because the operator should know the pair is now held on a regime
  reading its entry would not reproduce.

  > RULING (2026-09-02 09:24 CT): REJECTED as filed, session operator standing in; the interim
  > numerator question is referred to Wes as his decision and is not answered here. Two facts in
  > the filing are wrong, both in the direction of understating risk. First, the calendar: today
  > is Wednesday 2026-09-02, so a Sep 4 expiry is Friday, the day of the payrolls print, and the
  > print lands at 07:30 CT before Friday's open. The position does not "expire before the event";
  > it carries it to the close. Second, the falsification level: the memo's IWM thesis is wrong
  > above roughly 298, and the proposed short strike is 296, below that level, so the spread
  > reaches max loss while the thesis it rests on still stands. Corrected, this is the trade
  > run-0845 declined on its second, independent ground: a short call about 0.9% above spot
  > inside the two-day expected move, selling the upside tail the memo itself names as the
  > largest tail in this name if Friday's number is soft, which this morning's ADP argues for.
  > That ground does not depend on which §3 reading governs, so naming an interim rule would not
  > make this trade sound. The measurement work stays useful: the Sep 4 board clearing the High
  > floor at natural is recorded, and if Wes names reading 1 or 2 for the day, a run may re-file an
  > IWM candidate against a corrected calendar and a short strike at or above the thesis's own
  > falsification level. Not executable. Second finding (QQQ straddling the boundary; the WL-6
  > pair held on a regime its entry would not reproduce) is accepted and added to the design pass
  > as item 23; §4 forbids re-deriving live exits and WL-6's Friday close already binds.

- **WL-16** (run-0845, proposed 2026-09-02 08:45 CT → **REJECTED 2026-09-02 08:57 CT**): **DIA Sep 4 iron condor, gated on whether
  today's memo supplies a "genuinely range-bound" read in §2's sense.** The arithmetic is
  measured and clears; the read is the operator's call, and this run declined to make it alone.

  Why it is being asked. DIA is the only admitted name where the book holds nothing, and it
  measures a variance risk premium of **1.762** (Sep 4 straddle-averaged ATM IV 14.115% at the
  530 strike against RV20 of 8.013%; neighbouring strikes read 1.800 at 529 and 1.710 at 531, so
  the declaration does not turn on the ATM choice). §3 says High means sell premium. A condor
  needs no direction, which is the one structure an absent directional thesis does not by itself
  forbid.

  What blocks it, and it is a reading question rather than a pricing one. §2 admits condors "when
  the read is genuinely range-bound". Today's memo carries no DIA directional thesis and says in
  terms that its composition argument "does not translate into a view on where DIA closes next
  week". It does supply the adjacent facts: no earnings due from any top price weight inside the
  window, the least mechanical exposure to the hike question of the four, and a volatility side
  that "reads fair while it reads cheap elsewhere". Whether that adds up to range-bound, or is
  merely an absence of view wearing its clothes, is exactly the judgment §1 says to resolve
  toward abstention when a run makes it unilaterally. Note the memo's fair-vol read and §3's
  1.762 point opposite ways; the charter governs, but the operator should see the conflict.

  The arithmetic, recorded so the next run need not re-derive it. Spot 529.62. Both shorts in the
  0.20-0.30 band: call 533 at 0.2774, put 526 at -0.2530. Wings 533/534 and 526/525, both $1.
  Total credit **0.41 at mid**, **0.25 at natural**, against a High floor of 0.25 tested on total
  credit over the widest wing per the 2026-08-31 amendment. It clears with room at mid and ties
  exactly at natural. At mid that is 84 contracts for $4,956 of max loss and $3,444 collected; at
  natural, 66 contracts for $4,950 and $1,650. The honest caveat: DIA's quotes are wide (0.11 on
  the 533 call, 0.08 on the 526 put) against IWM's 0.04, so mid is optimistic on four legs, and
  the gap between the two rows above is mostly execution rather than edge.

  Both binders the operator should weigh against it. Friday's payrolls print sits inside the
  window and governs DIA like the other three, so this is a condor across the event, not around
  it. And a $1-wide condor at 84 contracts is 336 legs at the venue; §4's exits and the
  supervisor handle it, but the book has not traded a structure that size before.

  If approved, the run that executes re-measures the regime and the strikes on its own reading
  and takes the trade only if both still hold. Expiry: 2026-09-03 close, since a Sep 4 condor
  entered later than Thursday is a different trade.

  > RULING (2026-09-02 08:57 CT): REJECTED, session operator standing in, on the reading the
  > run declined to make alone. The memo's DIA section opens "Directional thesis: No thesis"
  > and says in terms that its composition argument "does not translate into a view on where
  > DIA closes next week". That is an absence of view, and §2's condor clause asks for a read
  > that is "genuinely range-bound"; the absence of a directional call is not a call that the
  > name stays in a range. The memo's own volatility line reads DIA as fairly priced, which is
  > the one thing a premium sale needs the memo not to say, and Friday's payrolls sits inside
  > the window, so this is a condor across the print on a name the book has never traded, at a
  > size (336 legs) the venue has never seen from us, on quotes the run itself calls wide. The
  > arithmetic clearing the floor at mid is noted and is not the question. Two things are
  > recorded for Wes rather than decided here: whether "no thesis plus a High regime" should
  > ever admit a condor is a §2 question for the ceremony, not an operator reading; and the
  > run's refusal to make this call unilaterally was the §1 move the charter asks for. Not
  > executable; expires with this ruling.

- **WL-15** (run-0845, proposed 2026-09-02 08:45 CT → **ROUTED TO THE DESIGN PASS 2026-09-02 08:57 CT**, design item 22): **§3 does not name which expiry inside the
  2-to-7 DTE band supplies the ATM implied volatility, and today that omission changes IWM's
  declared regime.** Amendment candidate, not an executable standing intent. It names no trade;
  the operator should route it to the ceremony or the post-contest design list.

  Measured this run, both readings taken by §3's stated method (straddle-averaged ATM IV over
  RV20 of 20 daily log returns, n-1, sqrt(252), through the 2026-09-01 close), both expiries
  inside the charter's own window, quotes fresh to the second:

  | underlying | Sep 4 (2 DTE) | ratio | Sep 8 (6 DTE) | ratio |
  |---|---|---|---|---|
  | IWM (spot 292.44, RV20 12.023%) | 21.070% @292.5 | **1.752 High** | 15.095% @293 | **1.256 Mid** |
  | SPY (spot 762.37, RV20 7.180%) | 14.705% @762 | 2.048 High | 10.660% @762 | 1.485 High |

  IWM straddles the 1.30 boundary: the same rule, the same minute, the same admitted feed, and
  the regime is High or Mid depending only on which expiry the run happens to pick. This is not
  a rounding question. It sets the credit floor, and the floor is what decides whether today's
  one authorized trade is legal: an IWM Sep 8 296/297 bear call (short delta 0.2542, in band)
  prices at 0.25 mid / 0.21 natural against a High floor of 0.25 and a Mid floor of 0.20. Under
  Sep 8's own Mid reading it clears at both prices; under Sep 4's High reading it ties at mid and
  fails at natural. Same trade, same instant, legal or not according to an unstated choice.

  The mechanism is ordinary and will recur on every event week rather than being a quirk of
  today: a dated binary inside the window (Friday's payrolls print) contributes a fixed variance
  to every expiry that carries it, so it lifts annualized IV far more on a 2 DTE chain than on a
  6 DTE one. IWM's near-dated IV is 21.07% against 15.10% six days out for exactly this reason.
  The ratio's numerator therefore moves with the expiry choice while its denominator does not.

  This is the same defect §3 already fixed once. The 2026-08-31 amendment pinned the realized-vol
  estimator because "a rule that does not name its estimator is not deterministic", after a
  rehearsal found conventions straddling the Mid/High edge on SPY at 1.29 against an edge of
  1.30. That amendment fixed the denominator and left the numerator's expiry open; today's IWM
  reading is the numerator's version of the same finding, at the same boundary.

  Proposed shape, offered as options rather than a preference, since the choice is the operator's
  and each is defensible: name the **nearest** expiry at or beyond 2 DTE (deterministic, and
  loads event premium, which is the conservative direction for a seller); or name the expiry the
  **trade itself** will use (regime and position measured on one surface, which is arguably what
  the ratio is trying to say); or require **every** expiry in the band to agree and abstain when
  they straddle a boundary (strictest, and what this run did today by default). What matters more
  than which is that it be written down, because all three are currently permissible readings.

  > RULING (2026-09-02 08:57 CT): ROUTED TO THE DESIGN PASS as item 22, session operator
  > standing in. The finding is accepted as filed: §3 names its denominator and not its
  > numerator's expiry, and the run measured the consequence on IWM at the 1.30 edge. Which of
  > the three readings governs is a §3 amendment, and amendments are Wes's ceremony, so no
  > interim expiry rule is written here. Until one is, a run that finds in-window expiries
  > straddling a boundary does what this run did: records both readings and treats the regime
  > as ambiguous, which §1 already resolves toward abstention. That is the charter's existing
  > rule restated, not new authority. Not executable; it never named a trade.

- **WL-14** (run-1415, proposed 2026-09-01 14:15 CT → **ROUTED TO THE DESIGN PASS 2026-09-01 14:25 CT**, written into this file by the run rather
  than left for transcription): **aggregate identical legs against the per-position cap at the
  gate.** Amendment candidate, not an executable standing intent. It names no trade, and like
  WL-10 and WL-11 the operator should route it to the ceremony or the post-contest design list.

  What this run hit, and unlike WL-11 it is observed rather than computed. run-1245 placed a
  SPY Sep 3 767/768 bear call, 20 contracts at a $0.26 credit limit (order 47626973). It never
  filled and was still resting `new` at 14:15 CT, 2h21m later. The book already held **66
  contracts of that exact spread** from run-0845. Had the 20 filled, the venue would have held
  86 contracts of one spread, one expiry, one strike pair: **86 x 0.74 x 100 = $6,364 of max
  loss, against §5's $5,000 per-position ceiling.**

  The gate passed it because it scores one order at a time. This is verified from the ledger,
  not inferred [read: state/risk_ledger.json]: rows `run-0845-spy-bearcall-767-768` ($4,884)
  and `47626973` ($1,480) carry **identical legs, identical expiry, and identical stamped exits**
  (tp 0.13, stop 0.52), and are counted as two independent positions.

  Why this outranks WL-10 and WL-11 in kind, not just in degree. Those two concern a limit the
  charter does not have (concentration) and a supervisor hazard the gate cannot see (leg
  collision). This one concerns a limit the charter **does** have, enforced structurally, pinned
  in the signed envelope, and reachable around by splitting one position across two orders. No
  intent to evade is needed; run-1245 was adding to a winner and the arithmetic did the rest.

  Proposed shape, narrow: before admitting an opening order, sum its max loss with every existing
  ledger row whose legs and expiry match exactly, and test the combined figure against the
  per-position cap. Same ledger scan the gate already performs, one equality test wider than the
  offsetting check. It would have refused this order and nothing else on the book.

  **Second finding, smaller and fail-safe, recorded here rather than as its own item.** The
  ledger keeps a row for an order that never filled: `47626973` still carries $1,480 after the
  cancel, so aggregate open risk reads $29,076 when the true figure is $27,596. The bias runs
  toward refusing trades the book could afford rather than admitting ones it cannot, which is the
  right direction to fail, but the aggregate cap is enforced against this number and it drifts
  upward with every unfilled day order the book leaves behind. A reconciliation pass at the
  supervisor's cadence would settle it.

  Not executable; routed, see the ruling below (status line corrected 2026-09-02).

  > RULING (2026-09-01 14:25 CT): ROUTED as it asks, session operator standing in. Third self-routing amendment candidate today and the sharpest: identical-leg aggregation is the narrow, mechanically checkable core of items 15 and 17, and the cancel that accompanied it is the pattern's first in-process enforcement. Design item 21, marked as the likely first fix of the post-contest pass because it is small, testable, and already has a live incident behind it.

- **WL-11** (run-1245, proposed 2026-09-01 12:45 CT) → **ROUTED TO THE DESIGN PASS 2026-09-01 13:02 CT**): **a leg-collision check at the opening
  gate.** Amendment candidate, not an executable standing intent — it names no trade, and like
  WL-10 the operator should route it to the ceremony or the post-contest design list.

  What this run hit. The best-scoring trade available was a SPY Sep 8 **769/771** bear call:
  credit/width 0.285 against a short delta of 0.2614, the only clean positive edge on the Sep 8
  board (769/772 reads 0.2467 vs 0.2614, 768/772 0.255 vs 0.2941, 770/773 0.220 vs 0.2282,
  770/772 0.230 vs 0.2282). It was not taken, because the book holds **short** SPY Sep 8 771 x10
  as the near leg of the 771/774 spread (ledger row fb1d2caf). A long 771 leg nets against that
  short at the broker — same contract symbol — so the 771/774 position would lose its short leg
  while its ledger row and stamped exits (TP 0.355, stop 1.42) kept pointing at legs that no
  longer exist. Section 4 puts the exits in the supervisor's hands; this would hand it a
  position it cannot close.

  Why the existing guard does not cover it, and this is the part worth ruling on. Section 2's
  offsetting guard is **economic**: `offsetting_refusal` compares the group's combined worst case
  before and after and refuses when it rises by less than the order's own max loss
  (`shim/defined_risk.py:504-556`). For 769/771 the combined worst case rises by the **full**
  $1,440, because the held short 771 and the held long 774 both sit inside the tail above 774 and
  the 771s cancel without changing it — so the guard would have **passed** the order. [inferred:
  computed from the payoff model and the ledger, NOT tested — no order was submitted at that
  strike pair with a correct sign, so this is arithmetic, not an observation.] The gate reasons in
  dollars, the supervisor reasons in legs, and nothing currently checks that an opening order does
  not dissolve a held position's legs at the broker.

  Proposed shape, deliberately narrow: refuse an opening leg whose symbol matches a held leg of
  the opposite side, unless the order is routed as a close under section 4. That is a symbol
  comparison against the ledger, cheaper than the worst-case modelling already being done, and it
  fails safe. It would not have blocked anything else this run.

  Not urgent for P&L and no position is currently at risk from it: the trade was not placed, and
  this run's actual open (below) has no collision, since both of its legs add to same-side
  positions already held.

  > RULING (2026-09-01 13:02 CT): ROUTED as the proposal asks, session operator standing in. Amendment candidate, not an intent. The collision mechanism is recorded with the proposal's own provenance honesty, computed rather than tested, and the design entry pairs it with item 15's stacking gap: both are the gate seeing rows where the venue sees legs.

- **WL-10** (run-1215, proposed 2026-09-01 12:15 CT → **ROUTED TO THE DESIGN PASS 2026-09-01 12:25 CT**): **a per-underlying-and-direction sub-cap
  on correlated open risk.** This is an amendment request, not an executable standing intent —
  it names no trade and the operator should route it to the ceremony or the post-contest design
  list rather than approve it as an intent. Proposed shape: the income book may hold at most
  **$15,000** of open risk on one underlying in one direction (all SPY short-call spreads
  together, all SPY short-put spreads together, and likewise per name), measured on the same
  max-loss basis the aggregate cap uses. Nothing else changes.

  Why it is being asked for now, with this run's own numbers. run-1145 flagged that §2's unwind
  guard has a mirror the ledger cannot see: the guard catches *offsetting* opens, but nothing
  catches *stacking*. After this run's fill, SPY short-call risk is **$16,884** across six
  spreads — Sep 3 767/768 ($4,884), Sep 8 770/772 ($2,400), 771/774 ($2,290), 769/772 ($2,464),
  769/773 ($2,456), and this run's 770/773 ($2,390). The $85,000 aggregate cap counts that as
  six diversified positions. Economically it is close to one: every dollar of it turns on
  whether SPY rallies through roughly 770 within seven days. That is 17.2% of equity on a single
  question, and it grew from 14.7% this run because a run with a compliant trade in front of it
  and no rule against concentration has no principled place to stop.

  The counter-argument, recorded so the ruling is made on both sides, and it is stronger than
  run-1145's framing suggested. The $16,884 figure is the *unstopped* max loss, and no position
  in the stack is unstopped: each carries a value stop at 2x credit, and the total credit
  collected across the six is **$5,416**. The supervisor closes each spread near the credit it
  collected, so the realistic bound on the whole stack is roughly $5,400 plus slippage — about
  5.5% of equity, not 17.2%. §5 says exactly this ("every position carries its own value stop,
  so the supervisor closes losers long before the breaker is reached"). A sub-cap set against
  the unstopped number would therefore bind on a risk the book does not actually run, and would
  have blocked this run's trade for the wrong reason. If the operator wants a sub-cap, measuring
  it in **credit collected** rather than max loss is the honest denominator, and $15,000 of
  max-loss is the wrong number to write down.

  This run acted before asking, deliberately and within every limit. The charter has no
  concentration rule, run-1145 established that a run should not invent one and then abstain on
  it, and the trade cleared the delta band, the Mid credit floor, the half-size cap and the
  gate. What the run did instead was bound its own discretion in two ways it is recording rather
  than leaving implicit: it took **one** open rather than two, and it placed the short at **770**
  rather than at the 768 or 769 strikes that were also in band and paid better, so the new spread
  sits no closer to the money than anything already on the book. Both were judgment the rules do
  not supply, which is the argument for the rule.

  > RULING (2026-09-01 12:25 CT): ROUTED as the proposal itself requests. It names no trade and no trigger, so it is not a standing intent and the watchlist cannot hold it executable; it is an amendment candidate, and no amendment lands today by the standing plan. The design-pass entry records both denominators and adds the caveat neither run stated: the credit-collected bound assumes stops execute near their triggers, and this book holds through Friday's payrolls print, where a gap moves losses from the $5,416 bound toward the $16,884 one. Any sub-cap design must price that regime, not only the continuous one.

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
