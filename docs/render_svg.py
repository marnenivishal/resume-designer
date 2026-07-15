#!/usr/bin/env python3
"""Render the Excalidraw canvas to a standalone SVG for the README.

    python docs/render_svg.py why-single-column.svg

Why not the MCP's own export: that server runs in Docker, so its export writes
inside the container. This pulls the scene from the canvas API on localhost and
renders it here, producing a crisp, small, diffable SVG that GitHub displays
inline and that survives without the container.

Deliberately NOT a general Excalidraw renderer -- it handles exactly the element
types these diagrams use (rectangle, text, line, arrow). If a future diagram uses
ellipses or freedraw, extend it or screenshot instead.
"""
from __future__ import annotations
import json, sys, urllib.request
from xml.sax.saxutils import escape

API = "http://localhost:3000/api/elements"
FONTS = {
    2: "'Segoe UI', 'Helvetica Neue', Arial, sans-serif",
    3: "'Cascadia Code', Consolas, 'SF Mono', Menlo, monospace",
}
PAD = 24


def fetch() -> list[dict]:
    with urllib.request.urlopen(API, timeout=15) as r:
        j = json.loads(r.read().decode("utf-8"))
    return j if isinstance(j, list) else (j.get("elements") or j.get("data") or [])


def line_h(fs: float) -> float:
    return fs * 1.25


def bounds(els: list[dict]) -> tuple[float, float, float, float]:
    xs, ys, xe, ye = [], [], [], []
    for e in els:
        x, y = e.get("x", 0), e.get("y", 0)
        w, h = e.get("width", 0), e.get("height", 0)
        if e["type"] == "text":
            fs = e.get("fontSize", 16)
            lines = str(e.get("text", "")).split("\n")
            w = max((len(l) for l in lines), default=0) * fs * 0.55
            h = len(lines) * line_h(fs)
        xs.append(x); ys.append(y); xe.append(x + w); ye.append(y + h)
    return min(xs), min(ys), max(xe), max(ye)


def render(els: list[dict]) -> str:
    x0, y0, x1, y1 = bounds(els)
    W, H = (x1 - x0) + PAD * 2, (y1 - y0) + PAD * 2
    dx, dy = PAD - x0, PAD - y0
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" '
        f'viewBox="0 0 {W:.0f} {H:.0f}" font-family="{FONTS[2]}">',
        f'<rect width="{W:.0f}" height="{H:.0f}" fill="#ffffff"/>',
        # orient="auto" (not auto-start-reverse): wider renderer support, and these
        # arrows only ever point forwards.
        '<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" '
        'markerHeight="6" orient="auto" markerUnits="strokeWidth">'
        '<path d="M0,0 L10,5 L0,10 z" fill="#1e1e1e"/></marker></defs>',
    ]
    # shapes first, text last, so labels are never covered
    order = {"rectangle": 0, "line": 1, "arrow": 2, "text": 3}
    for e in sorted(els, key=lambda e: order.get(e["type"], 1)):
        t = e["type"]
        x, y = e.get("x", 0) + dx, e.get("y", 0) + dy
        stroke = e.get("strokeColor", "#1e1e1e")
        sw = e.get("strokeWidth", 1)
        op = e.get("opacity", 100) / 100
        dash = ""
        if e.get("strokeStyle") == "dashed": dash = ' stroke-dasharray="8 5"'
        elif e.get("strokeStyle") == "dotted": dash = ' stroke-dasharray="2 5" stroke-linecap="round"'

        if t == "rectangle":
            out.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{e.get("width",0):.1f}" '
                f'height="{e.get("height",0):.1f}" rx="6" fill="{e.get("backgroundColor","transparent")}" '
                f'fill-opacity="{op:.2f}" stroke="{stroke}" stroke-width="{sw}"{dash}/>')
        elif t in ("line", "arrow"):
            pts = e.get("points") or [[0, 0], [e.get("width", 0), e.get("height", 0)]]
            d = " ".join(f'{"M" if i==0 else "L"}{x+p[0]:.1f},{y+p[1]:.1f}' for i, p in enumerate(pts))
            marker = ' marker-end="url(#ah)"' if t == "arrow" else ""
            out.append(f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{sw}"'
                       f'{dash}{marker} opacity="{op:.2f}"/>')
        elif t == "text":
            fs = e.get("fontSize", 16)
            fam = FONTS.get(e.get("fontFamily", 2), FONTS[2])
            for i, ln in enumerate(str(e.get("text", "")).split("\n")):
                out.append(
                    f'<text x="{x:.1f}" y="{y + fs + i*line_h(fs):.1f}" font-size="{fs}" '
                    f'font-family="{fam}" fill="{stroke}" opacity="{op:.2f}" '
                    f'xml:space="preserve">{escape(ln)}</text>')
    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "diagram.svg"
    els = fetch()
    svg = render(els)
    import pathlib
    p = pathlib.Path(__file__).parent / name
    p.write_text(svg, encoding="utf-8")
    print(f"  {p}  ({len(els)} elements, {len(svg):,} bytes)")
