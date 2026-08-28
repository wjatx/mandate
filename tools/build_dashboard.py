#!/usr/bin/env python3
"""Build the static mandate dashboard at docs/dashboard/index.html.

Operator-side tooling. This script holds Alpaca credentials because an operator
runs it; the agent never sees them and cannot run this script. The page it
emits is regenerated from the audit tape, not written by the agent.

Stdlib only. Every remote section degrades to an explicit "unavailable" note
rather than to fabricated data.
"""

from __future__ import annotations

import html
import json
import subprocess
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "dashboard" / "index.html"
AUDIT = ROOT / "state" / "audit.jsonl"
REFUSALS = ROOT / "state" / "shim_refusals.jsonl"
LEDGER = ROOT / "state" / "risk_ledger.json"
ENV_SH = ROOT / "state" / "env.sh"
SECRETS = Path.home() / ".secrets" / "alpaca.txt"

API = "https://paper-api.alpaca.markets"
START_EQUITY = 100_000.0
TIMEOUT = 20

# Palette: dataviz reference instance. Series slot 1 (blue) validated in both
# modes; status steps are fixed and always ship with a text label.
CSS_VARS = """
:root { color-scheme: light;
  --surface: #fcfcfb; --plane: #f9f9f7; --ink: #0b0b0b; --ink-2: #52514e;
  --muted: #898781; --grid: #e1e0d9; --axis: #c3c2b7; --up: #006300;
  --border: rgba(11,11,11,0.10); --series: #2a78d6; --wash: rgba(42,120,214,0.10);
  --deny-bg: rgba(208,59,59,0.055); }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  color-scheme: dark;
  --surface: #1a1a19; --plane: #0d0d0d; --ink: #fff; --ink-2: #c3c2b7;
  --muted: #898781; --grid: #2c2c2a; --axis: #383835; --up: #0ca30c;
  --border: rgba(255,255,255,0.10); --series: #3987e5; --wash: rgba(57,135,229,0.12);
  --deny-bg: rgba(208,59,59,0.14); } }
/* Status steps are fixed, never themed; each ships beside a text label. */
:root { --good: #0ca30c; --critical: #d03b3b; --down: #d03b3b; }
"""


# ---------------------------------------------------------------- utilities

def esc(v) -> str:
    return html.escape("" if v is None else str(v))


def fnum(v, default=None):
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def money(v, places=2) -> str:
    f = fnum(v)
    if f is None:
        return "—"
    return f"{'-' if f < 0 else ''}${abs(f):,.{places}f}"


def signed_money(v) -> str:
    f = fnum(v)
    if f is None:
        return "—"
    return f"{'+' if f >= 0 else '-'}${abs(f):,.2f}"


def short_digest(v) -> str:
    s = str(v or "")
    body = s.split(":", 1)[1] if s.startswith("sha256:") else s
    return body[:12] if body else "—"


def utc(ts) -> str:
    """Render an ISO-8601 or epoch timestamp as 'YYYY-MM-DD HH:MM:SS UTC'."""
    if ts in (None, ""):
        return "—"
    try:
        if isinstance(ts, (int, float)):
            dt = datetime.fromtimestamp(ts, timezone.utc)
        else:
            dt = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
            dt = dt.astimezone(timezone.utc)
    except (ValueError, OSError, OverflowError):
        return esc(ts)
    return dt.strftime("%Y-%m-%d %H:%M:%S UTC")


def read_jsonl(path: Path) -> tuple[list[dict], str | None]:
    if not path.exists():
        return [], f"{path.name} not present"
    rows, bad = [], 0
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except ValueError:
            bad += 1
    return rows, (f"{bad} unparseable line(s) skipped" if bad else None)


def read_ledger() -> list[dict]:
    try:
        raw = json.loads(LEDGER.read_text())
    except (OSError, ValueError):
        return []
    return [e for e in raw if isinstance(e, dict)] if isinstance(raw, list) else []


# -------------------------------------------------------------- data access

def load_keys() -> dict[str, str]:
    kv: dict[str, str] = {}
    for line in SECRETS.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        kv[k.strip()] = v.strip().strip('"').strip("'")
    return kv


def api_client():
    """Return a getter for the paper API, or None if keys are unreadable."""
    try:
        kv = load_keys()
        headers = {
            "APCA-API-KEY-ID": kv["ALPACA_KEY"],
            "APCA-API-SECRET-KEY": kv["ALPACA_SECRET"],
        }
    except (OSError, KeyError):
        return None

    def get(path: str):
        req = urllib.request.Request(API + path, headers=headers)
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.load(resp)

    return get


def fetch(get, path: str) -> tuple[object | None, str | None]:
    """Per-section fetch. Returns (payload, error-note); never raises."""
    if get is None:
        return None, "Alpaca credentials unavailable"
    try:
        return get(path), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code} from {path}"
    except (urllib.error.URLError, OSError, ValueError, TimeoutError) as e:
        return None, f"{type(e).__name__} from {path}"


def verify_tape() -> tuple[bool, str, str]:
    """Run the tape verifier; return (ok, verdict-line, captured tail)."""
    cmd = (
        f"source {ENV_SH} && "
        f"{ROOT}/.venv/bin/python -m safe_agents.broker.auditor.tape_cli "
        f"--path {AUDIT} --verify"
    )
    try:
        proc = subprocess.run(
            ["bash", "-c", cmd], cwd=ROOT, capture_output=True,
            text=True, timeout=120, check=False,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return False, f"verifier did not run ({type(e).__name__})", ""
    out = [ln.strip() for ln in (proc.stdout + proc.stderr).strip().splitlines()]
    # The verifier's own caveat paragraph also contains "CONSISTENT"; take the
    # short summary line ("CHAIN CONSISTENT — 28 records, seq 0..27") instead.
    verdict = next(
        (ln for ln in out if "CONSISTENT" in ln.upper() and len(ln) < 90),
        f"verifier exited {proc.returncode}",
    )
    return proc.returncode == 0, verdict, "\n".join(out[-6:])


# ------------------------------------------------------------- equity curve

def nice_ticks(lo: float, hi: float, count: int = 4) -> list[float]:
    span = hi - lo
    if span <= 0:
        return [lo]
    raw = span / count
    mag = 10 ** (len(f"{int(raw):d}") - 1) if raw >= 1 else 10 ** -2
    step = next((m * mag for m in (1, 2, 2.5, 5, 10) if m * mag >= raw), raw)
    first = (int(lo / step) + 1) * step
    ticks, t = [], first
    while t <= hi and len(ticks) <= count + 2:
        ticks.append(t)
        t += step
    return ticks


def equity_curve_svg(stamps: list, values: list[float]) -> str:
    """Single-series line: 2px stroke, 10% wash, hairline grid, end label.

    One series, so no legend box — the section heading names what is plotted.
    Native SVG <title> on per-point hit bands gives the hover layer with no JS.
    """
    w, h = 960, 260
    ml, mr, mt, mb = 68, 84, 14, 30
    pw, ph = w - ml - mr, h - mt - mb

    lo, hi = min(values), max(values)
    pad = max((hi - lo) * 0.10, abs(hi) * 0.0004, 0.5)
    lo, hi = lo - pad, hi + pad
    n = len(values)

    def x(i):
        return ml + (pw * i / (n - 1) if n > 1 else pw / 2)

    def y(v):
        return mt + ph - (v - lo) / (hi - lo) * ph

    pts = [(x(i), y(v)) for i, v in enumerate(values)]
    line = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    area = (f"M{pts[0][0]:.1f},{mt + ph:.1f} L" + line
            + f" L{pts[-1][0]:.1f},{mt + ph:.1f} Z")

    parts = [
        (
            f'<svg class="chart" viewBox="0 0 {w} {h}" role="img" '
            f'aria-label="Account equity over the past week, 15-minute marks.">'
        )
    ]
    for t in nice_ticks(lo, hi):
        ty = y(t)
        parts.append(
            f'<line x1="{ml}" y1="{ty:.1f}" x2="{ml + pw}" y2="{ty:.1f}" '
            f'class="grid"/>'
            f'<text x="{ml - 10}" y="{ty + 4:.1f}" class="tick tick-y">'
            f'{t:,.0f}</text>'
        )
    parts.append(
        f'<line x1="{ml}" y1="{mt + ph}" x2="{ml + pw}" y2="{mt + ph}" '
        f'class="axis"/>'
    )
    parts.append(f'<path d="{area}" class="wash"/>')
    parts.append(f'<polyline points="{line}" class="line"/>')

    ex, ey = pts[-1]
    parts.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="4.5" class="dot"/>')
    parts.append(
        f'<text x="{ex + 12:.1f}" y="{ey + 4:.1f}" class="endlabel">'
        f'{values[-1]:,.0f}</text>'
    )

    for i, (px, _) in enumerate(pts):
        band = pw / max(n - 1, 1)
        parts.append(
            f'<rect x="{px - band / 2:.1f}" y="{mt}" width="{band:.2f}" '
            f'height="{ph}" class="hit"><title>{esc(utc(stamps[i]))} · '
            f'{values[i]:,.2f}</title></rect>'
        )
    for i in (0, n // 2, n - 1):
        anchor = "start" if i == 0 else ("end" if i == n - 1 else "middle")
        parts.append(
            f'<text x="{x(i):.1f}" y="{h - 8}" class="tick" '
            f'text-anchor="{anchor}">{esc(utc(stamps[i])[:16])}</text>'
        )
    parts.append("</svg>")
    return "".join(parts)


# ------------------------------------------------------------------ render

def unavailable(note: str) -> str:
    return f'<p class="unavail">Unavailable — {esc(note)}. No data is shown.</p>'


def table(headers, rows, cls: str = "") -> str:
    """rows: (row-class, [cell-html, ...]) pairs. Cells are pre-escaped."""
    head = "".join(f"<th>{esc(h)}</th>" for h in headers)
    body = "".join(
        f'<tr class="{rc}">' + "".join(f"<td>{c}</td>" for c in cells) + "</tr>"
        for rc, cells in rows
    )
    return (f'<div class="scroll"><table class="{cls}"><thead><tr>{head}</tr>'
            f"</thead><tbody>{body}</tbody></table></div>")


def positions_section(positions, err, ledger) -> str:
    if err:
        return unavailable(err)
    if not positions:
        note = ""
        if ledger:
            note = (f'<p class="note">Risk ledger still tracks '
                    f"{len(ledger)} defined-risk entr"
                    f"{'y' if len(ledger) == 1 else 'ies'}; no matching "
                    "position is open at the broker.</p>")
        return '<p class="note">No open positions.</p>' + note
    by_leg = {leg: e for e in ledger for leg in (e.get("legs") or [])}
    rows = []
    for p in positions:
        entry = by_leg.get(p.get("symbol"))
        pl = fnum(p.get("unrealized_pl")) or 0.0
        rows.append(("", [
            esc(p.get("symbol")), esc(p.get("side")), esc(p.get("qty")),
            money(p.get("avg_entry_price")), money(p.get("current_price")),
            money(p.get("market_value")),
            (
                f'<span class="{"pos" if pl >= 0 else "neg"}">'
                f'{signed_money(p.get("unrealized_pl"))}</span>'
            ),
            money(entry.get("max_loss_usd")) if entry else "—",
        ]))
    return table(["Symbol", "Side", "Qty", "Avg entry", "Current", "Market value",
                  "Unrealized P&L", "Ledger max loss"], rows, "num")


def denies_section(records) -> str:
    denies = [r for r in records if r.get("decision") == "deny"]
    if not denies:
        return '<p class="note">No broker denies on the tape.</p>'
    rows = [("deny", [
        esc(r.get("seq")), utc(r.get("ts")),
        f'{esc(r.get("tool"))}.{esc(r.get("op"))}',
        '<span class="badge crit">denied</span>',
        f'<span class="reason">{esc(r.get("reason"))}</span>',
        f'<code>{esc(short_digest(r.get("argsDigest")))}</code>',
    ]) for r in reversed(denies)]
    return table(["Seq", "Timestamp", "Call", "Outcome", "Reason", "Args"], rows)


def shim_section(refusals, note) -> str:
    if not refusals:
        why = note or "no records"
        return (f'<p class="note">No defined-risk refusals recorded '
                f"({esc(why)}).</p>")
    rows = [("deny", [
        utc(r.get("refused_at")),
        f'<span class="reason">{esc(r.get("reason"))}</span>',
        esc(r.get("qty")), money(r.get("limit_price")),
        "<br>".join(esc(s) for s in (r.get("legs") or [])) or "—",
    ]) for r in reversed(refusals)]
    return table(["Refused at", "Reason", "Qty", "Limit", "Legs"], rows)


def log_section(records) -> str:
    rows = []
    for r in reversed(records):
        deny = r.get("decision") == "deny"
        pr = r.get("principal") or {}
        rows.append(("deny" if deny else "", [
            esc(r.get("seq")), utc(r.get("ts")),
            f'{esc(r.get("tool"))}.{esc(r.get("op"))}',
            f'{esc(pr.get("agentId"))} / {esc(pr.get("skill"))}',
            (
                f'<span class="badge {"crit" if deny else "ok"}">'
                f'{esc(r.get("decision"))} · {esc(r.get("outcome"))}</span>'
            ),
            f'<span class="reason">{esc(r.get("reason"))}</span>' if deny else "—",
            f'<code>{esc(short_digest(r.get("argsDigest")))}</code>',
        ]))
    return table(["Seq", "Timestamp", "Call", "Principal", "Decision",
                  "Reason", "Args"], rows)


def orders_section(orders, err) -> str:
    if err:
        return unavailable(err)
    if not orders:
        return '<p class="note">No recent orders.</p>'
    rows = []
    for o in orders:
        # Multi-leg orders carry no top-level symbol; the legs do.
        legs = o.get("legs") or []
        if o.get("symbol"):
            sym, side = esc(o.get("symbol")), esc(o.get("side"))
        else:
            sym = "<br>".join(f'{esc(l.get("side"))} {esc(l.get("symbol"))}'
                              for l in legs) or "—"
            side = esc(o.get("order_class")) or "—"
        rows.append(("", [
            sym, side, esc(o.get("type")), esc(o.get("qty")),
            esc(o.get("filled_qty")), money(o.get("filled_avg_price")),
            (
                f'<span class="badge {"ok" if o.get("status") == "filled" else "neutral"}">'
                f'{esc(o.get("status"))}</span>'
            ),
            utc(o.get("submitted_at")),
        ]))
    return table(["Symbol", "Side", "Type", "Qty", "Filled", "Fill price",
                  "Status", "Submitted"], rows, "num")


def build() -> str:
    records, _ = read_jsonl(AUDIT)
    refusals, refusal_note = read_jsonl(REFUSALS)
    ledger = read_ledger()
    chain_ok, verdict, _ = verify_tape()

    get = api_client()
    account, acct_err = fetch(get, "/v2/account")
    positions, pos_err = fetch(get, "/v2/positions")
    history, hist_err = fetch(get, "/v2/account/portfolio/history"
                                   "?period=1W&timeframe=15Min")
    orders, ord_err = fetch(get, "/v2/orders?status=all&limit=50")

    equity = fnum((account or {}).get("equity"))
    pl = None if equity is None else equity - START_EQUITY
    n_deny = sum(1 for r in records if r.get("decision") == "deny")
    n_refused = len(refusals)

    # Header figures
    if equity is None:
        hero = '<div class="hero">—</div>' + unavailable(acct_err or "no account data")
        tiles = ""
    else:
        cls = "pos" if pl >= 0 else "neg"
        hero = (f'<div class="hero">{money(equity)}</div>'
                f'<div class="hero-label">Account equity · Alpaca paper</div>')
        tiles = (
            f'<div class="tiles">'
            f'<div class="tile"><span class="tl">P&amp;L since $100,000 start</span>'
            f'<span class="tv {cls}">{signed_money(pl)}</span>'
            f'<span class="td">{pl / START_EQUITY * 100:+.3f}%</span></div>'
            f'<div class="tile"><span class="tl">Options buying power</span>'
            f'<span class="tv">{money((account or {}).get("options_buying_power"), 0)}</span>'
            f'<span class="td">Account {esc((account or {}).get("status"))}</span></div>'
            f'<div class="tile"><span class="tl">Brokered calls on tape</span>'
            f'<span class="tv">{len(records)}</span>'
            f'<span class="td">{n_deny} denied · {n_refused} refused at execution</span></div>'
            f"</div>"
        )

    verdict_cls = "ok" if chain_ok else "crit"
    chart = (unavailable(hist_err) if hist_err else "")
    if not hist_err:
        stamps = (history or {}).get("timestamp") or []
        vals = [v for v in ((history or {}).get("equity") or []) if v is not None]
        if len(vals) >= 2 and len(stamps) >= len(vals):
            chart = equity_curve_svg(stamps[:len(vals)], [float(v) for v in vals])
        else:
            chart = unavailable("portfolio history returned too few points")

    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>mandate — audit dashboard</title>
<style>{CSS_VARS}
* {{ box-sizing: border-box; }}
body {{ margin: 0; padding: 2rem 1.25rem 4rem; background: var(--plane); color: var(--ink);
  font: 15px/1.55 system-ui, -apple-system, "Segoe UI", sans-serif; }}
main, footer {{ max-width: 1080px; margin: 0 auto; }}
h1 {{ font-size: 2rem; margin: 0; letter-spacing: -0.02em; }}
h2 {{ font-size: 1.05rem; margin: 0 0 .2rem; letter-spacing: -0.01em; }}
.sub {{ color: var(--ink-2); margin: .25rem 0 1.5rem; }}
section {{ background: var(--surface); border: 1px solid var(--border); border-radius: 10px;
  padding: 1.25rem 1.35rem; margin: 1.1rem 0; }}
/* Hero figure: exactly one per view, in the same sans as everything else. */
.hero {{ font-size: 3.1rem; font-weight: 600; letter-spacing: -0.03em; line-height: 1.05; }}
.tiles {{ display: grid; gap: .9rem; margin-top: 1.35rem;
  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); }}
.tile {{ display: flex; flex-direction: column; gap: .1rem; padding-left: .8rem;
  border-left: 2px solid var(--border); }}
.tv {{ font-size: 1.5rem; font-weight: 600; letter-spacing: -0.02em; }}
.tl, .shead, .note, .unavail, .cap, .hero-label, footer {{ color: var(--ink-2); }}
.td, code, .tick {{ color: var(--muted); }}
.pos {{ color: var(--up); }} .neg, .reason {{ color: var(--down); }}
.reason {{ font-weight: 500; }}
.shead, .cap {{ font-size: .85rem; margin: 0 0 .9rem; }}
.tl, .td, .hero-label, .note, .unavail {{ font-size: .84rem; }}
.hero-label {{ margin-top: .15rem; }} .note, .unavail {{ margin: 0; }}
.unavail {{ border-left: 2px solid var(--muted); padding-left: .7rem; }}
.verdict {{ margin-top: 1.35rem; padding-top: 1rem; border-top: 1px solid var(--border);
  display: flex; flex-wrap: wrap; gap: .6rem 1.1rem; align-items: baseline; font-size: .88rem; }}
.badge {{ display: inline-block; padding: .08rem .5rem; border-radius: 999px; font-size: .76rem;
  font-weight: 600; border: 1px solid currentColor; white-space: nowrap; }}
.badge.ok {{ color: var(--good); }} .badge.crit {{ color: var(--critical); }}
.badge.neutral {{ color: var(--muted); }}
.chart {{ width: 100%; height: auto; display: block; }}
.grid {{ stroke: var(--grid); }} .axis {{ stroke: var(--axis); }}
.grid, .axis {{ stroke-width: 1; }}
.line {{ fill: none; stroke: var(--series); stroke-width: 2; stroke-linejoin: round;
  stroke-linecap: round; }}
.wash {{ fill: var(--wash); stroke: none; }} .hit {{ fill: transparent; }}
.dot {{ fill: var(--series); stroke: var(--surface); stroke-width: 2; }}
.tick {{ font-size: 11px; font-variant-numeric: tabular-nums; }}
.tick-y {{ text-anchor: end; }}
.endlabel {{ fill: var(--ink-2); font-size: 12px; font-weight: 600; }}
.scroll {{ overflow-x: auto; }}
table {{ border-collapse: collapse; width: 100%; font-size: .86rem; }}
th {{ text-align: left; font-weight: 600; color: var(--ink-2); font-size: .78rem;
  text-transform: uppercase; letter-spacing: .04em; padding: .4rem .6rem .45rem;
  white-space: nowrap; }}
td {{ padding: .45rem .6rem; vertical-align: top; }}
th, td {{ border-bottom: 1px solid var(--border); }}
tbody tr:last-child td {{ border-bottom: none; }}
table.num td:nth-child(n+3) {{ font-variant-numeric: tabular-nums; }}
tr.deny td {{ background: var(--deny-bg); }}
tr.deny td:first-child {{ box-shadow: inset 2px 0 0 var(--critical); }}
code {{ font: .8rem/1 ui-monospace, SFMono-Regular, Menlo, monospace; }}
.refusals {{ border-color: var(--critical); }} .refusals h2 {{ font-size: 1.2rem; }}
.split {{ margin-top: 1.3rem; }} .split h3 {{ font-size: .9rem; margin: 0 0 .15rem; }}
footer {{ margin-top: 2rem; font-size: .82rem; line-height: 1.6; padding-top: 1rem;
  border-top: 1px solid var(--border); }}
</style></head><body><main>

<section>
  <h1>mandate</h1>
  <p class="sub">an autonomous options agent under an enforced mandate</p>
  {hero}
  {tiles}
  <div class="verdict">
    <span><span class="badge {verdict_cls}">tape {"consistent" if chain_ok else "unverified"}</span></span>
    <span>{esc(verdict)}</span>
    <span>Generated {utc(datetime.now(timezone.utc))}</span>
  </div>
</section>

<section>
  <h2>Account equity</h2>
  <p class="shead">Past week, 15-minute marks from the broker's portfolio history,
    which reports to the dollar. The headline figure above is the live account value.</p>
  {chart}
</section>

<section class="refusals">
  <h2>Refusals</h2>
  <p class="shead">What the mandate stopped. {n_deny} call{"" if n_deny == 1 else "s"}
    denied at the broker; {n_refused} placement{"" if n_refused == 1 else "s"}
    refused at execution by the defined-risk shim.</p>
  <div class="split">
    <h3>Broker denies</h3>
    <p class="cap">The call never reached Alpaca. The manifest had no entry for it.</p>
    {denies_section(records)}
  </div>
  <div class="split">
    <h3>Defined-risk refusals</h3>
    <p class="cap">The broker allowed the call; the shim refused to place the order.
      These reach the tape as ordinary executed calls, so they are logged separately.</p>
    {shim_section(refusals, refusal_note)}
  </div>
</section>

<section>
  <h2>Open positions</h2>
  <p class="shead">Live from the paper account, joined to the risk ledger by leg symbol.</p>
  {positions_section(positions, pos_err, ledger)}
</section>

<section>
  <h2>Decision log</h2>
  <p class="shead">Every brokered call, newest first. {len(records)} records.</p>
  {log_section(records)}
</section>

<section>
  <h2>Recent orders</h2>
  <p class="shead">Last 50 orders at the broker, any status.</p>
  {orders_section(orders, ord_err)}
</section>

</main><footer>
<p>The audit chain is unkeyed SHA-256. Verification proves the tape is
<strong>self-consistent</strong> — no record was edited, dropped, or reordered in
place. It is not tamper-proof: anyone who can write the file can rewrite it whole
and recompute every hash. Tamper-evidence needs off-device append-only storage.</p>
<p>This page is regenerated from the audit tape; the agent cannot write this page.</p>
</footer></body></html>
"""


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build())
    print(f"wrote {OUT} ({OUT.stat().st_size:,} bytes)")
