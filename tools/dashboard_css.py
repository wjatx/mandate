"""Stylesheet for the mandate dashboard.

Split out of build_dashboard.py so the page CSS does not have to live inside
an f-string, where every brace needs doubling.
"""

# Palette: dataviz reference instance. Series slot 1 (blue) validated in both
# modes; status steps are fixed and always ship with a text label.
CSS = """
:root { color-scheme: light;
  --surface: #fcfcfb; --plane: #f9f9f7; --ink: #0b0b0b; --ink-2: #52514e;
  --muted: #898781; --grid: #e1e0d9; --axis: #c3c2b7; --up: #006300;
  --border: rgba(11,11,11,0.10); --series: #2a78d6; --wash: rgba(42,120,214,0.10);
  --deny-bg: rgba(208,59,59,0.055); --gate-bg: rgba(163,90,0,0.055);
  --warn: #8a4b00; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  color-scheme: dark;
  --surface: #1a1a19; --plane: #0d0d0d; --ink: #fff; --ink-2: #c3c2b7;
  --muted: #898781; --grid: #2c2c2a; --axis: #383835; --up: #0ca30c;
  --border: rgba(255,255,255,0.10); --series: #3987e5; --wash: rgba(57,135,229,0.12);
  --deny-bg: rgba(208,59,59,0.14); --gate-bg: rgba(224,160,48,0.12);
  --warn: #e0a030; } }
/* Status steps are fixed, never themed; each ships beside a text label. */
:root { --good: #0ca30c; --critical: #d03b3b; --down: #d03b3b; }
* { box-sizing: border-box; }
body { margin: 0; padding: 2rem 1.25rem 4rem; background: var(--plane); color: var(--ink);
  font: 15px/1.55 system-ui, -apple-system, "Segoe UI", sans-serif; }
main, footer { max-width: 1080px; margin: 0 auto; }
h1 { font-size: 2rem; margin: 0; letter-spacing: -0.02em; }
h2 { font-size: 1.05rem; margin: 0 0 .2rem; letter-spacing: -0.01em; }
.sub { color: var(--ink-2); margin: .25rem 0 0; max-width: 62ch; }
section { background: var(--surface); border: 1px solid var(--border); border-radius: 10px;
  padding: 1.25rem 1.35rem; margin: 1.1rem 0; }
/* Two hero figures, refusals first: the mandate is the claim, equity the evidence. */
.heroes { display: grid; gap: 1.5rem 2.4rem; margin-top: 1.6rem;
  grid-template-columns: repeat(auto-fit, minmax(290px, 1fr)); }
.heroblock { display: flex; flex-direction: column; }
.hero { font-size: 3.1rem; font-weight: 600; letter-spacing: -0.03em; line-height: 1.05; }
.hero-split { font-size: .88rem; margin-top: .5rem; font-weight: 500; }
.hero-note { margin: .3rem 0 0; max-width: 42ch; }
.tiles { display: grid; gap: .9rem; margin-top: 1.5rem; padding-top: 1.2rem;
  border-top: 1px solid var(--border);
  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); }
.tile { display: flex; flex-direction: column; gap: .1rem; padding-left: .8rem;
  border-left: 2px solid var(--border); }
.tv { font-size: 1.5rem; font-weight: 600; letter-spacing: -0.02em; }
.tl, .shead, .note, .unavail, .cap, .hero-label, .hero-note, footer { color: var(--ink-2); }
.td, code, .tick, .barcap { color: var(--muted); }
.pos { color: var(--up); } .neg, .reason { color: var(--down); }
.warn { color: var(--warn); } .reason, .warn { font-weight: 500; }
.shead, .cap { font-size: .85rem; margin: 0 0 .9rem; }
.cap:last-child { margin: .6rem 0 0; }
.tl, .td, .hero-label, .hero-note, .note, .unavail, .counts { font-size: .84rem; }
.hero-label { margin-top: .15rem; } .note, .unavail { margin: 0; }
.counts { margin: 0 0 .9rem; padding: .5rem .7rem; border-radius: 6px;
  background: var(--plane); border: 1px solid var(--border); }
.unavail { border-left: 2px solid var(--muted); padding-left: .7rem; }
.verdict { margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid var(--border);
  display: flex; flex-wrap: wrap; gap: .6rem 1.1rem; align-items: baseline; font-size: .88rem; }
.badge { display: inline-block; padding: .08rem .5rem; border-radius: 999px; font-size: .76rem;
  font-weight: 600; border: 1px solid currentColor; white-space: nowrap; }
.badge.ok { color: var(--good); } .badge.crit { color: var(--critical); }
.badge.gate { color: var(--warn); } .badge.neutral { color: var(--muted); }
.chart { width: 100%; height: auto; display: block; }
.grid { stroke: var(--grid); } .axis { stroke: var(--axis); }
.grid, .axis { stroke-width: 1; }
.line { fill: none; stroke: var(--series); stroke-width: 2; stroke-linejoin: round;
  stroke-linecap: round; }
.wash { fill: var(--wash); stroke: none; } .hit { fill: transparent; }
.dot { fill: var(--series); stroke: var(--surface); stroke-width: 2; }
.tick { font-size: 11px; font-variant-numeric: tabular-nums; }
.tick-y { text-anchor: end; }
.endlabel { fill: var(--ink-2); font-size: 12px; font-weight: 600; }
.cards { display: grid; gap: .9rem;
  grid-template-columns: repeat(auto-fit, minmax(310px, 1fr)); }
.card { border: 1px solid var(--border); border-radius: 8px; padding: .9rem 1rem;
  background: var(--plane); }
.card h3 { font-size: .97rem; margin: 0 0 .1rem; letter-spacing: -0.01em; }
.card-sub { font-size: .78rem; color: var(--muted); margin: 0 0 .75rem; }
.kv { display: grid; grid-template-columns: auto 1fr; gap: .22rem .9rem;
  margin: 0; font-size: .84rem; }
.kv dt { color: var(--ink-2); }
.kv dd { margin: 0; text-align: right; font-variant-numeric: tabular-nums; }
.bar { width: 100%; height: 6px; display: block; margin-top: .9rem; }
.bar-bg { fill: var(--grid); } .bar-fill { fill: var(--series); }
.barcap { font-size: .76rem; margin: .35rem 0 0; }
.scroll { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; font-size: .86rem; }
th { text-align: left; font-weight: 600; color: var(--ink-2); font-size: .78rem;
  text-transform: uppercase; letter-spacing: .04em; padding: .4rem .6rem .45rem;
  white-space: nowrap; }
td { padding: .45rem .6rem; vertical-align: top; }
th, td { border-bottom: 1px solid var(--border); }
tbody tr:last-child td { border-bottom: none; }
table.num td:nth-child(n+3) { font-variant-numeric: tabular-nums; }
tr.deny td { background: var(--deny-bg); }
tr.deny td:first-child { box-shadow: inset 2px 0 0 var(--critical); }
tr.gate td { background: var(--gate-bg); }
tr.gate td:first-child { box-shadow: inset 2px 0 0 var(--warn); }
code { font: .8rem/1 ui-monospace, SFMono-Regular, Menlo, monospace; }
details.reads { margin-top: 1.1rem; border-top: 1px solid var(--border); padding-top: .8rem; }
details.reads summary { cursor: pointer; color: var(--ink-2); font-size: .84rem; }
details.reads[open] summary { margin-bottom: .8rem; }
.refusals { border-color: var(--critical); } .refusals h2 { font-size: 1.2rem; }
.split { margin-top: 1.3rem; } .split h3 { font-size: .9rem; margin: 0 0 .15rem; }
footer { margin-top: 2rem; font-size: .82rem; line-height: 1.6; padding-top: 1rem;
  border-top: 1px solid var(--border); }
"""
