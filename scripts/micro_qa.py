#!/usr/bin/env python3
"""Micro typographic QA: the small things that make a document read as amateur.

    python scripts/micro_qa.py Resume.html
    python scripts/micro_qa.py out/*/Resume.html --json

ats_check.py asks "does the machine read it?". This asks "does it look like someone
competent made it?" -- the details a designer would flag in review and a test suite
normally cannot see:

    edge        content too close to (or past) the paper edge
    margins     left/right margins symmetric
    rhythm      every vertical gap on the 3pt spacing scale
    orphan      a heading stranded at the foot of a page
    runt        a line wrapping to leave a single-word last line
    empty       a page that is mostly blank (usually a content problem)
    dates       the right-aligned meta column actually aligns
    bullets     bullets share one left edge
    density     text is not crammed or drowning

Runs headless Chrome + CDP. No Playwright dependency; the browser is already
required for PDF output.

Exit: 0 clean, 1 warnings, 2 failures.
"""
from __future__ import annotations

import argparse
import base64
import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

# US Letter at 96dpi, the CSS pixel geometry Chrome lays out against.
PAGE_W, PAGE_H = 816, 1056

PROBE = r"""
(() => {
  const PAGE_W = 816, PAGE_H = 1056;
  const out = {issues: [], stats: {}};
  const add = (level, check, msg) => out.issues.push({level, check, msg});
  const txtEls = [...document.querySelectorAll('*')].filter(el =>
    [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()));

  // --- edge: nothing may touch or exceed the paper
  let minL = 1e9, maxR = -1e9;
  for (const el of txtEls) {
    const r = el.getBoundingClientRect();
    if (r.width === 0) continue;
    minL = Math.min(minL, r.left); maxR = Math.max(maxR, r.right);
    if (r.right > PAGE_W + 0.5 || r.left < -0.5)
      add('fail', 'edge', `overflows the page: "${el.textContent.trim().slice(0,32)}"`);
  }
  out.stats.leftMargin = Math.round(minL);
  out.stats.rightMargin = Math.round(PAGE_W - maxR);
  if (minL < 24) add('fail', 'edge', `content starts ${Math.round(minL)}px from the paper edge — reads as cramped`);
  if (PAGE_W - maxR < 24) add('fail', 'edge', `content ends ${Math.round(PAGE_W-maxR)}px from the right edge`);

  // --- margins: symmetric within 2px (asymmetry reads as a mistake)
  const asym = Math.abs(minL - (PAGE_W - maxR));
  out.stats.marginAsymmetry = Math.round(asym);
  if (asym > 2) add('warn', 'margins', `left ${Math.round(minL)}px vs right ${Math.round(PAGE_W-maxR)}px — ${Math.round(asym)}px asymmetric`);

  // --- rhythm: section gaps on the 3pt (=4px) scale
  const secs = [...document.querySelectorAll('section')];
  const gaps = [];
  for (let i = 1; i < secs.length; i++) {
    const prev = secs[i-1].getBoundingClientRect(), cur = secs[i].getBoundingClientRect();
    gaps.push(Math.round((cur.top - prev.bottom) * 100) / 100);
  }
  out.stats.sectionGaps = gaps;
  const offGrid = gaps.filter(g => Math.abs(g / 4 - Math.round(g / 4)) > 0.26);
  if (offGrid.length) add('warn', 'rhythm', `${offGrid.length} section gap(s) off the 3pt grid: ${offGrid.join(', ')}px`);
  const uniq = [...new Set(gaps.map(g => Math.round(g)))];
  if (uniq.length > 2) add('warn', 'rhythm', `section gaps inconsistent: ${uniq.join(', ')}px — should be one value`);

  // --- orphan: a heading must not be the last thing on a page
  for (const h of document.querySelectorAll('h2')) {
    const r = h.getBoundingClientRect();
    const posInPage = r.bottom % PAGE_H;
    if (posInPage > PAGE_H - 60 && r.bottom > PAGE_H)
      add('fail', 'orphan', `heading "${h.textContent.trim()}" is stranded at a page foot`);
  }

  // --- runt: a wrapped line ending in a single short word
  const runts = [];
  for (const li of document.querySelectorAll('li, p.prose, .entry-summary')) {
    const cs = getComputedStyle(li);
    const lh = parseFloat(cs.lineHeight) || 14;
    const lines = Math.round(li.getBoundingClientRect().height / lh);
    if (lines < 2) continue;
    const words = li.textContent.trim().split(/\s+/);
    // Re-measure the last word alone: if it sits on its own line, it's a runt.
    const probe = document.createElement('span');
    probe.style.cssText = `font:${cs.font};visibility:hidden;position:absolute;white-space:nowrap`;
    probe.textContent = words[words.length-1];
    document.body.appendChild(probe);
    const wLast = probe.getBoundingClientRect().width;
    probe.remove();
    const range = document.createRange();
    range.selectNodeContents(li);
    const rects = [...range.getClientRects()];
    if (rects.length) {
      const last = rects[rects.length-1];
      if (last.width <= wLast + 2 && words.length > 6)
        runts.push(`"…${words.slice(-3).join(' ')}"`);
    }
  }
  out.stats.runts = runts.length;
  if (runts.length) add('warn', 'runt', `${runts.length} line(s) end with a single-word last line: ${runts.slice(0,2).join(', ')} — reword, don't retrack`);

  // --- height only. NOT page count.
  // This used to derive pages and last-page fill from scrollHeight and it was simply
  // WRONG -- it reported "1 page, 4% fill" for a document Chrome paginates to 2 pages
  // with both pages 94% full. The DOM does not paginate; Chrome's print layout does,
  // and it accounts for break-inside/avoid, orphans and widows that the flow view
  // knows nothing about. references/rendering.md says exactly this and I built the
  // tool that ignores it. Page metrics now come from the PDF, in Python, below.
  out.stats.bodyHeight = document.body.scrollHeight;

  // --- dates: the right-aligned meta column must share one right edge
  const metas = [...document.querySelectorAll('.row > .meta')];
  const rights = metas.map(m => Math.round(m.getBoundingClientRect().right));
  const spread = rights.length ? Math.max(...rights) - Math.min(...rights) : 0;
  out.stats.dateRightSpread = spread;
  if (spread > 1) add('fail', 'dates', `right-aligned meta column is ragged by ${spread}px — tabular figures or flex is broken`);

  // --- bullets: one left edge
  const lis = [...document.querySelectorAll('li')];
  const lefts = lis.map(li => Math.round(li.getBoundingClientRect().left));
  const lspread = lefts.length ? Math.max(...lefts) - Math.min(...lefts) : 0;
  out.stats.bulletLeftSpread = lspread;
  if (lspread > 1) add('fail', 'bullets', `bullets do not share a left edge (${lspread}px spread)`);

  // --- density: leading and measure
  const body = getComputedStyle(document.body);
  const fs = parseFloat(body.fontSize), lh = parseFloat(body.lineHeight);
  out.stats.leadingRatio = Math.round((lh/fs)*100)/100;
  if (lh/fs < 1.15) add('warn', 'density', `leading ${(lh/fs).toFixed(2)} is tight for print`);
  if (lh/fs > 1.7)  add('warn', 'density', `leading ${(lh/fs).toFixed(2)} is loose — costs a page for nothing`);
  const p = document.querySelector('p.prose');
  if (p) {
    const chars = Math.round(p.getBoundingClientRect().width / (fs * 0.5));
    out.stats.proseMeasure = chars;
    if (chars > 96) add('warn', 'density', `prose measure ~${chars} chars — cap the summary`);
  }
  return out;
})()
"""


def find_chrome() -> str:
    from build import find_chrome as fc
    c = fc()
    if not c:
        sys.exit("error: no Chrome/Chromium/Edge found. Set RESUME_CHROME.")
    return c


def probe(html: Path, chrome: str) -> dict:
    """Run the probe via Chrome's headless dump-dom-less path: --run-all + CDP eval.

    Simplest portable trick: inject the probe into a copy of the page, have it write
    the JSON into the title, and read it back with --dump-dom.
    """
    src = html.read_text(encoding="utf-8")
    # Emulate the PRINTED page before measuring. @page{margin} applies only when
    # printing, so a browser window lays the document out with NO page margins --
    # measuring that reports "content starts 0px from the paper edge" for a document
    # whose printed margins are perfect. Reconstruct the page box from the same
    # tokens @page uses, so screen geometry == paper geometry.
    emulate = """<style id="__qa_page">
      html { background: #fff; }
      body {
        width: 8.5in;
        padding: var(--page-margin-y) var(--page-margin-x);
        margin: 0;
        box-sizing: border-box;
      }
    </style>"""
    inject = f"""<script>
      window.addEventListener('load', () => {{
        try {{ const r = {PROBE};
          document.title = "QA::" + JSON.stringify(r);
        }} catch (e) {{ document.title = "QA::" + JSON.stringify({{error: String(e)}}); }}
      }});
    </script>"""
    src = src.replace("</head>", emulate + "</head>", 1)
    tmp = html.parent / (html.stem + ".__qa.html")
    tmp.write_text(src.replace("</body>", inject + "</body>"), encoding="utf-8")
    udd = tempfile.mkdtemp(prefix="qa_")
    try:
        r = subprocess.run(
            [chrome, "--headless=new", "--disable-gpu", "--no-sandbox", "--no-first-run",
             "--no-default-browser-check", "--disable-extensions",
             f"--window-size={PAGE_W},{PAGE_H}", "--virtual-time-budget=4000",
             f"--user-data-dir={udd}", "--dump-dom", tmp.resolve().as_uri()],
            capture_output=True, text=True, timeout=120)
        dom = r.stdout
    finally:
        shutil.rmtree(udd, ignore_errors=True)
        tmp.unlink(missing_ok=True)
    i = dom.find("QA::")
    if i < 0:
        return {"issues": [{"level": "fail", "check": "probe", "msg": "probe did not run"}],
                "stats": {}}
    j = dom[i + 4: dom.find("</title>", i)]
    import html as _h
    try:
        return json.loads(_h.unescape(j))
    except Exception as e:
        return {"issues": [{"level": "fail", "check": "probe", "msg": f"bad probe output: {e}"}],
                "stats": {}}


def page_metrics(html: Path) -> list[dict]:
    """Real page metrics, from the sibling PDF. Never from the DOM.

    The DOM does not paginate -- Chrome's print layout does, honouring
    break-inside/avoid, orphans and widows that the flow view cannot see. Deriving a
    page count from scrollHeight produced "1 page, 4% full" for a document that is
    genuinely 2 pages at 94%. If there is no PDF beside the HTML, this reports
    nothing rather than guessing.
    """
    pdf = html.with_suffix(".pdf")
    if not pdf.exists():
        return []
    try:
        import pdfplumber
    except ImportError:
        return []
    out = []
    with pdfplumber.open(pdf) as doc:
        for i, p in enumerate(doc.pages, 1):
            objs = p.chars + p.rects
            bottom = max((o["bottom"] for o in objs), default=0)
            out.append({"page": i, "fill": bottom / p.height if p.height else 0,
                        "glyphs": len(p.chars)})
    return out


def check_pages(html: Path, rep: list) -> dict:
    pages = page_metrics(html)
    if not pages:
        return {}
    n = len(pages)
    last = pages[-1]
    st = {"pages": n, "lastPageFill": round(last["fill"] * 100)}
    if n > 1 and last["fill"] < 0.33:
        rep.append({"level": "warn", "check": "empty",
                    "msg": f"page {n} is only {round(last['fill']*100)}% full "
                           f"({last['glyphs']} glyphs) — cut to fit, or add substance"})
    elif n == 1 and last["fill"] < 0.55:
        rep.append({"level": "warn", "check": "empty",
                    "msg": f"page only {round(last['fill']*100)}% full — thin content, "
                           f"not a layout fault"})
    return st


def main() -> int:
    ap = argparse.ArgumentParser(description="Micro typographic QA on a rendered resume.")
    ap.add_argument("html", nargs="+", help="Resume.html file(s); globs ok")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true", help="warnings are failures too")
    a = ap.parse_args()

    files: list[Path] = []
    for pat in a.html:
        files += [Path(p) for p in glob.glob(pat)] or ([Path(pat)] if Path(pat).exists() else [])
    if not files:
        sys.exit("error: no HTML files matched")

    chrome = find_chrome()
    RESET, RED, YEL, GRN, DIM = "\033[0m", "\033[31m", "\033[33m", "\033[32m", "\033[2m"
    if not sys.stdout.isatty():
        RESET = RED = YEL = GRN = DIM = ""

    allres, worst = {}, 0
    for f in files:
        res = probe(f, chrome)
        # Page metrics come from the PDF, not the probe. See page_metrics().
        res["stats"].update(check_pages(f, res["issues"]))
        allres[str(f)] = res
        if a.json:
            continue
        st = res.get("stats", {})
        pg = (f"{st['pages']}pg, last {st['lastPageFill']}% full"
              if "pages" in st else "no PDF beside HTML — page metrics skipped")
        print(f"\n  {DIM}micro-qa{RESET}  {f.parent.name}/{f.name}")
        print(f"    {DIM}margins {st.get('leftMargin','?')}/{st.get('rightMargin','?')}px · "
              f"leading {st.get('leadingRatio','?')} · {pg} · "
              f"date-edge ±{st.get('dateRightSpread','?')}px · bullets ±{st.get('bulletLeftSpread','?')}px{RESET}")
        if not res["issues"]:
            print(f"    {GRN}PASS{RESET}  nothing to flag")
        for i in res["issues"]:
            col = RED if i["level"] == "fail" else YEL
            print(f"    {col}{i['level'].upper():4s}{RESET}  {i['check']:8s} {i['msg']}")
        worst = max(worst, 2 if any(i["level"] == "fail" for i in res["issues"])
                    else (1 if res["issues"] else 0))

    if a.json:
        print(json.dumps(allres, indent=2))
    return worst if (a.strict or worst == 2) else 0


if __name__ == "__main__":
    sys.exit(main())
