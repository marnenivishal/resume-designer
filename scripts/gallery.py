#!/usr/bin/env python3
"""Render every preset and build one browsable contact sheet.

    python scripts/gallery.py                      # all presets, sample data
    python scripts/gallery.py --data resume.yaml   # YOUR resume in every preset
    python scripts/gallery.py --filter material    # just one family
    python scripts/gallery.py --verify             # also parse-check every one

Output: <out>/index.html -- every preset as a live, scaled page you can click.

A list of preset names is useless for choosing. You pick a look by looking at it.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import html as htmllib
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
sys.path.insert(0, str(HERE))

SAMPLE = SKILL / "examples" / "engineer.yaml"


def build_one(name: str, data: Path, outdir: Path, verify: bool) -> dict:
    d = outdir / name
    d.mkdir(parents=True, exist_ok=True)
    fmts = "html,pdf" if verify else "html"
    r = subprocess.run(
        [sys.executable, str(HERE / "build.py"), str(data), "--preset", name,
         "--format", fmts, "--out", str(d), "--name", name, "--quiet"],
        capture_output=True, text=True, timeout=300)
    ok = (d / f"{name}.html").exists()
    res = {"name": name, "ok": ok, "err": (r.stderr or "")[-160:] if not ok else ""}
    if verify and (d / f"{name}.pdf").exists():
        c = subprocess.run([sys.executable, str(HERE / "ats_check.py"),
                            str(d / f"{name}.pdf"), "--data", str(data)],
                           capture_output=True, text=True, timeout=180)
        res["fails"] = [l.strip() for l in c.stdout.split("\n") if "FAIL" in l]
    return res


PAGE = """<!doctype html><meta charset="utf-8">
<title>resume-designer — {n} presets</title>
<style>
  :root {{ color-scheme: light dark; }}
  body {{ font: 14px/1.5 system-ui, -apple-system, "Segoe UI", sans-serif;
         margin: 0; padding: 32px; background: #f6f7f9; color: #16181d; }}
  @media (prefers-color-scheme: dark) {{
    body {{ background: #14161a; color: #e8eaed; }}
    .card {{ background: #1e2126 !important; border-color: #2c3138 !important; }}
    .frame {{ border-color: #2c3138 !important; }}
  }}
  header {{ max-width: 1400px; margin: 0 auto 28px; }}
  h1 {{ font-size: 24px; margin: 0 0 6px; letter-spacing: -0.01em; }}
  p.sub {{ margin: 0; opacity: .7; }}
  .filters {{ margin: 18px 0 0; display: flex; flex-wrap: wrap; gap: 6px; }}
  .filters button {{ font: inherit; font-size: 12px; padding: 4px 11px; border-radius: 99px;
    border: 1px solid #d6dae0; background: #fff; cursor: pointer; }}
  .filters button.on {{ background: #16181d; color: #fff; border-color: #16181d; }}
  .grid {{ max-width: 1400px; margin: 0 auto; display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 22px; }}
  .card {{ background: #fff; border: 1px solid #e3e6ea; border-radius: 10px;
    overflow: hidden; }}
  .frame {{ height: 340px; overflow: hidden; border-bottom: 1px solid #e3e6ea;
    position: relative; background: #fff; }}
  /* Scale a real Letter page (816px) down into the card. This is the actual
     rendered document, not a picture of one. */
  .frame iframe {{ width: 816px; height: 1056px; border: 0;
    transform: scale(.32); transform-origin: top left; position: absolute;
    top: 0; left: 50%; margin-left: -130px; pointer-events: none; }}
  .meta {{ padding: 10px 12px; }}
  .nm {{ font-weight: 600; font-size: 13px; }}
  .nt {{ font-size: 11px; opacity: .62; margin-top: 2px; line-height: 1.35; }}
  .bad {{ color: #b3261e; font-size: 11px; margin-top: 4px; }}
  a.open {{ font-size: 11px; text-decoration: none; opacity: .7; }}
  a.open:hover {{ opacity: 1; text-decoration: underline; }}
</style>
<header>
  <h1>{n} presets</h1>
  <p class="sub">Every one is the same tested, single-column, parse-safe structure —
     retuned across type, accent, heading treatment and density.
     Each tile is the real rendered document, scaled.</p>
  <div class="filters" id="f"></div>
</header>
<div class="grid" id="g">
{cards}
</div>
<script>
  const fams = [...new Set([...document.querySelectorAll('.card')].map(c => c.dataset.fam))];
  const f = document.getElementById('f');
  const mk = (label, fam) => {{
    const b = document.createElement('button');
    b.textContent = label; b.onclick = () => {{
      [...f.children].forEach(x => x.classList.remove('on')); b.classList.add('on');
      document.querySelectorAll('.card').forEach(c =>
        c.style.display = (!fam || c.dataset.fam === fam) ? '' : 'none');
    }};
    f.appendChild(b); return b;
  }};
  mk('all', null).classList.add('on');
  fams.forEach(x => mk(x, x));
</script>
"""

CARD = """  <div class="card" data-fam="{fam}">
    <div class="frame"><iframe src="{src}" loading="lazy" scrolling="no"></iframe></div>
    <div class="meta">
      <div class="nm">{name}</div>
      <div class="nt">{note}</div>{bad}
      <a class="open" href="{src}" target="_blank">open full size →</a>
    </div>
  </div>"""


def main() -> int:
    ap = argparse.ArgumentParser(description="Render every preset into one contact sheet.")
    ap.add_argument("--data", default=str(SAMPLE), help="resume.yaml to render (default: the example)")
    ap.add_argument("--out", default=None)
    ap.add_argument("--filter", default=None, help="substring match on preset name")
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--verify", action="store_true", help="also parse-check every preset")
    a = ap.parse_args()

    from build import load_presets
    presets = load_presets()
    if a.filter:
        presets = {k: v for k, v in presets.items() if a.filter in k}
    if not presets:
        sys.exit("error: no presets matched")

    data = Path(a.data).resolve()
    if not data.exists():
        sys.exit(f"error: no such file: {data}")
    outdir = Path(a.out).resolve() if a.out else (Path.cwd() / "gallery")
    outdir.mkdir(parents=True, exist_ok=True)

    print(f"rendering {len(presets)} presets -> {outdir}")
    results = []
    with cf.ThreadPoolExecutor(max_workers=a.jobs) as ex:
        futs = {ex.submit(build_one, n, data, outdir, a.verify): n for n in presets}
        for i, fut in enumerate(cf.as_completed(futs), 1):
            r = fut.result()
            results.append(r)
            mark = "ok " if r["ok"] and not r.get("fails") else "FAIL"
            print(f"  [{i:3d}/{len(presets)}] {mark} {r['name']}"
                  + (f"  {r['err']}" if r["err"] else "")
                  + (f"  {r['fails'][0][:60]}" if r.get("fails") else ""))

    by = {r["name"]: r for r in results}
    cards = []
    for name, p in presets.items():
        r = by.get(name, {})
        if not r.get("ok"):
            continue
        bad = ""
        if r.get("fails"):
            bad = f'<div class="bad">parse check: {len(r["fails"])} failure(s)</div>'
        cards.append(CARD.format(
            fam=name.split("-")[0], src=f"{name}/{name}.html",
            name=htmllib.escape(name),
            note=htmllib.escape((p.get("note") or "")),
            bad=bad))
    index = outdir / "index.html"
    index.write_text(PAGE.format(n=len(cards), cards="\n".join(cards)), encoding="utf-8")

    n_ok = sum(1 for r in results if r["ok"])
    n_bad = sum(1 for r in results if r.get("fails"))
    print(f"\n  {n_ok}/{len(results)} rendered" + (f", {n_bad} failed parse check" if a.verify else ""))
    print(f"  open: {index}")
    return 0 if n_ok == len(results) and not n_bad else 1


if __name__ == "__main__":
    sys.exit(main())
