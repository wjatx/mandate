#!/usr/bin/env python3
"""Hand-rolled SVG for the mandate dashboard: chart, favicon, share card.

Stdlib only, no chart library. Split out of build_dashboard.py to keep that
file readable; it holds drawing, never data access.
"""

from __future__ import annotations

import html
import urllib.parse
from datetime import datetime, timezone

# Chart geometry. One series, so no legend: the section heading names it.
W, H = 960, 260
ML, MR, MT, MB = 78, 92, 14, 30
PW, PH = W - ML - MR, H - MT - MB
Y_PAD_FRACTION = 0.06  # of the value range, so a small move still has shape


def _esc(v) -> str:
    return html.escape("" if v is None else str(v))


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


def equity_curve_svg(stamps: list[str], values: list[float], aria: str) -> str:
    """Single-series line: 2px stroke, 10% wash, hairline grid, end label.

    Native SVG <title> on per-point hit bands gives the hover layer with no JS.
    """
    lo, hi = min(values), max(values)
    pad = max((hi - lo) * Y_PAD_FRACTION, 0.5)
    lo, hi = lo - pad, hi + pad
    n = len(values)
    decimals = 0 if (hi - lo) >= 50 else 2

    def x(i):
        return ML + (PW * i / (n - 1) if n > 1 else PW / 2)

    def y(v):
        return MT + PH - (v - lo) / (hi - lo) * PH

    pts = [(x(i), y(v)) for i, v in enumerate(values)]
    line = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    area = (f"M{pts[0][0]:.1f},{MT + PH:.1f} L" + line
            + f" L{pts[-1][0]:.1f},{MT + PH:.1f} Z")

    parts = [(f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" '
              f'aria-label="{_esc(aria)}">')]
    for t in nice_ticks(lo, hi):
        ty = y(t)
        parts.append(
            f'<line x1="{ML}" y1="{ty:.1f}" x2="{ML + PW}" y2="{ty:.1f}" '
            f'class="grid"/>'
            f'<text x="{ML - 10}" y="{ty + 4:.1f}" class="tick tick-y">'
            f'{t:,.{decimals}f}</text>'
        )
    parts.append(f'<line x1="{ML}" y1="{MT + PH}" x2="{ML + PW}" '
                 f'y2="{MT + PH}" class="axis"/>')
    parts.append(f'<path d="{area}" class="wash"/>')
    parts.append(f'<polyline points="{line}" class="line"/>')

    ex, ey = pts[-1]
    parts.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="4.5" class="dot"/>')
    parts.append(f'<text x="{ex + 12:.1f}" y="{ey + 4:.1f}" class="endlabel">'
                 f'{values[-1]:,.{decimals}f}</text>')

    band = PW / max(n - 1, 1)
    for i, (px, _) in enumerate(pts):
        parts.append(
            f'<rect x="{px - band / 2:.1f}" y="{MT}" width="{band:.2f}" '
            f'height="{PH}" class="hit"><title>{_esc(stamps[i])} · '
            f'{values[i]:,.2f}</title></rect>'
        )
    for i in dict.fromkeys((0, n // 2, n - 1)):
        anchor = "start" if i == 0 else ("end" if i == n - 1 else "middle")
        parts.append(
            f'<text x="{x(i):.1f}" y="{H - 8}" class="tick" '
            f'text-anchor="{anchor}">{_esc(stamps[i][:16])}</text>'
        )
    parts.append("</svg>")
    return "".join(parts)


def consumed_bar_svg(consumed: float, cap: float) -> str:
    """Thin bar: how much of a spread's stamped max loss is spent so far."""
    frac = 0.0 if cap <= 0 else max(0.0, min(1.0, consumed / cap))
    return (
        f'<svg class="bar" viewBox="0 0 200 6" preserveAspectRatio="none" '
        f'role="img" aria-label="{frac * 100:.0f} percent of max loss used.">'
        f'<rect x="0" y="0" width="200" height="6" rx="3" class="bar-bg"/>'
        f'<rect x="0" y="0" width="{frac * 200:.1f}" height="6" rx="3" '
        f'class="bar-fill"/></svg>'
    )


# --------------------------------------------------------------- identity

_FAVICON = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
    '<rect width="64" height="64" rx="14" fill="#12233a"/>'
    '<rect x="12" y="14" width="40" height="4" rx="2" fill="#7fb2ef"/>'
    '<rect x="12" y="26" width="40" height="4" rx="2" fill="#7fb2ef"/>'
    '<rect x="12" y="38" width="40" height="4" rx="2" fill="#7fb2ef"/>'
    '<rect x="27" y="8" width="10" height="48" rx="5" fill="#12233a"/>'
    '<rect x="29.5" y="10.5" width="5" height="43" rx="2.5" fill="#e8452c"/>'
    '</svg>'
)

# Data-URI favicon: no extra file to serve, no request, works on Pages.
FAVICON_DATA_URI = "data:image/svg+xml," + urllib.parse.quote(_FAVICON, safe="")


def og_card_svg(built: datetime | None = None) -> str:
    """1200x630 share card. Static copy only, so scraper caching cannot
    make it disagree with the live page."""
    stamp = (built or datetime.now(timezone.utc)).strftime("%Y-%m-%d")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" \
viewBox="0 0 1200 630" font-family="system-ui, -apple-system, 'Segoe UI', sans-serif">
<rect width="1200" height="630" fill="#12233a"/>
<rect x="0" y="0" width="1200" height="6" fill="#e8452c"/>
<text x="88" y="228" fill="#ffffff" font-size="104" font-weight="600" \
letter-spacing="-4">mandate</text>
<text x="88" y="300" fill="#7fb2ef" font-size="34" font-weight="500">\
an autonomous options agent under an enforced mandate</text>
<text x="88" y="386" fill="#c9d4e2" font-size="29">\
The agent holds no broker credential.</text>
<text x="88" y="428" fill="#c9d4e2" font-size="29">\
Every call is decided against a signed grant</text>
<text x="88" y="470" fill="#c9d4e2" font-size="29">\
and lands on a hash-chained tape.</text>
<rect x="88" y="524" width="88" height="4" fill="#e8452c"/>
<text x="88" y="576" fill="#8a97a8" font-size="23">\
Alpaca paper account · audit tape rebuilt {stamp}</text>
</svg>
"""
