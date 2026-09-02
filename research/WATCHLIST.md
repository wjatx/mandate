# Watchlist — standing intents (charter §6)

Maintained by the operator between decision runs. A decision run proposes WATCH items in its
record; the operator rules on each here. Only items under **Approved standing intents** are
executable, and only while unexpired. Everything here runs inside the charter's caps, slots,
per-run limits, and the broker's gate.

## Approved standing intents

- **WL-13** (run-1345, proposed 2026-09-01 13:45 CT as "WL-12"; renumbered by the operator in
  transcription because run-1315 had already claimed the number — both proposals exist only in
  the run logs): if SPY trades back to 765 or higher and a Sep 8 call at 775 or above measures
  inside the 0.20-0.30 delta band with credit clearing the Mid floor at natural pricing, one
  bear call at half size, short strike 775 or above. The 775 floor keeps it collision-free and
  strictly above every held short. Expires 2026-09-02 close. APPROVED by Wes 2026-09-01 14:50 CT, with the full-deployment package; executable within every ordinary limit.

- **WL-12** (run-1315, proposed 2026-09-01 13:15 CT; transcribed from the run record by the
  operator 2026-09-01 13:55 CT — the run did not write it into this file): if the next §7
  research pass carries a SPY read that is up-or-sideways in the §2 sense, a decision run may
  open one SPY bull put spread at half size, subject to every ordinary limit and the collision
  check. Rationale as filed: the only admitted structure that would diversify the book's
  single-question concentration rather than deepen it. Expires 2026-09-04 close. APPROVED by Wes
  2026-09-01 14:50 CT, with the full-deployment package (commit 40b94ca); executable within every ordinary limit. Text corrected 2026-09-02 08:05 CT: the approval commit re-ordered this entry but left its status line unchanged.

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

- **WL-18** (run-1045, proposed 2026-09-02 10:45 CT): **IWM Sep 8 bear put debit vertical, gated
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

  > OPERATOR NOTE (2026-09-02 10:55 CT): REFERRED TO WES, not ruled. This item asks Wes to name a
  > §3 reading, and the session operator standing in does not create trading authority, so it
  > stays here awaiting his answer rather than being approved, rejected or routed. Its facts were
  > checked and hold (calendar, falsifier, cap, collisions). Not executable until Wes rules. Runs
  > should not re-file it; the question is in front of him with the trade priced.

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
## Ruled: rejected, expired, executed

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
