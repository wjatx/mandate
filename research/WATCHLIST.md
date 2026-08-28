# Watchlist — standing intents (charter §6)

Maintained by the operator between decision runs. A decision run proposes WATCH items in its
record; the operator rules on each here. Only items under **Approved standing intents** are
executable, and only while unexpired. Everything here runs inside the charter's caps, slots,
per-run limits, and the broker's gate.

## Approved standing intents

- **WL-4** (cal-1345 → approved with modification 2026-08-28 14:12 CT): if QQQ trades
  above 718 while this intent stands, open a second QQQ Sep 4 bull call debit vertical,
  long strike nearest below spot at trigger, $5 wide, 4 contracts, total debit at most
  $2,500 — provided the QQQ regime still measures Low, a slot is free, and the thesis is
  unfalsified. MODIFICATION (netting guard, per cal-1335's precedent): neither strike may
  coincide with an existing ledger leg's strike on the same expiry and right; if the
  indicated strike would net against a book leg at the venue, shift the spread $1 further
  from it. Expires 2026-08-31 close; any extension toward the Sep 2 earnings binary waits
  on the weekend memo refresh.

- **WL-3** (cal-1325 → approved 2026-08-28 13:38 CT): thesis-falsification close. If QQQ
  trades below 706 before the Sep 4 close, close cal-1315's QQQ 717/722 bull call at
  market, whether or not the stored value stop (1.24) has triggered. Basis: 706 is the
  memo's own falsification level, cited at entry; this is a pre-registered invalidation
  condition ruled in advance, not an in-band discretionary close, and it only reduces
  risk. Executable by any acting run observing the trigger. Expires 2026-09-04 close.


## Proposed, awaiting ruling

(none)

## Ruled: rejected, expired, executed

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
