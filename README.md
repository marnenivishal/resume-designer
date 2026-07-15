# resume-designer

A [Claude Code](https://claude.com/claude-code) skill that builds a typeset,
single-column, **parse-verified** resume from an editable YAML file.

It is opinionated, and the opinions are measured rather than inherited. Most resume
advice online is content marketing published by companies selling resume builders;
this skill tries to encode only what survives contact with evidence, and to say
plainly when the evidence is weak.

```bash
python scripts/build.py resume.yaml --format pdf,docx,txt --check
```

```
  wrote Maya_Ellison_Resume.pdf   (57,203 bytes)

  parse-back check  Maya_Ellison_Resume.pdf

  PASS  text-layer   1,901 chars extract cleanly across 1 page(s)
  PASS  fonts        all embedded/subset: SegoeUI-Bold, SegoeUI-Semibold, SegoeUI
  PASS  order        4 anchors extract in written order
  PASS  bleed        6 same-line pair(s), all record/metadata — merge harmlessly
  PASS  contact      email parses: maya.ellison@example.com
  PASS  headings     standard headings found: EXPERIENCE, EDUCATION, SKILLS…
  PASS  pages        1 page(s)

  clean — the text layer survives extraction intact
```

---

## What makes it different

**It verifies instead of claiming.** `ats_check.py` re-extracts the finished PDF the
way a parser does and proves the text layer is intact — reading order, no fabricated
lines, fonts genuinely embedded, contact details findable. Every other tool in this
space asserts "ATS-friendly!" as a marketing claim. This one shows its work, and
tells you when it fails.

**It's honest about ATS.** The famous *"75% of resumes are auto-rejected by bots"* is
unsupported folklore. PDFs are read fine by every mainstream system. There is no
portable "ATS score", and third-party resume scanners simulate nothing. ATS are
search tools operated by humans. See [`DESIGN.md § 7`](DESIGN.md).

**One source, many outputs.** `resume.yaml` → PDF (send this) · DOCX (when a posting
demands it) · TXT (paste into web forms) · HTML (preview).

---

## The finding that shaped the design

**PDF has no DOM.** Chrome emits glyphs in *visual* position order, so anything
side-by-side at the same height is merged into one line at extraction. Measured
across five layout strategies and two parser engines:

| Layout | Order | Unrelated blocks merged? |
|---|---|---|
| single column | correct in both | no |
| `column-count: 2` | **inverted** | no |
| flex sidebar (left/right) | **inverted** / ok | **yes** |
| CSS grid sidebar | **inverted** | **yes** |
| `<table>` two-cell | **inverted** | **yes** |
| main-first DOM, sidebar moved via CSS `order` | **inverted** | **yes** |

Three things fall out of that, each contradicting common advice:

1. **A sidebar doesn't "risk" parsing — it fabricates text.** A parser reads
   `Senior Engineer, Acme  Python, Go, Kubernetes`: a job title welded to a skills
   list. Correct *order* isn't sufficient.
2. **Tables are the worst performer**, not the safe choice.
3. **Fixing DOM order does nothing** — the DOM is gone by print time. The standard
   workaround does not work.

But side-by-side is *safe when the merged line is still true*, which is what rescues
the typography:

```
Senior Engineer, Acme      Mar 2021 – Present   ->  merges correctly  ✅
Languages   Go, Python, SQL                     ->  merges correctly  ✅
[SKILLS column] [EXPERIENCE column]             ->  fabricated line   ❌
```

So you can keep right-aligned tabular dates and label/value grids — the moves that
make a resume look typeset — and still emit a perfectly clean text stream. You don't
trade beauty for parseability. You trade *columns of unrelated content*.

Full evidence, including the font findings (variable fonts silently degrade Chrome's
PDF to Type3; Georgia's old-style figures make dates bounce), is in
**[`DESIGN.md`](DESIGN.md)**.

---

## Install

```bash
git clone https://github.com/marnenivishal/resume-designer
cp -r resume-designer ~/.claude/skills/          # personal, all projects
# or: cp -r resume-designer .claude/skills/      # one project
pip install pyyaml jinja2 python-docx pdfplumber pypdf
```

Needs Python 3.10+ and Chrome/Chromium/Edge (auto-detected; override with
`RESUME_CHROME=/path/to/chrome`).

Claude will invoke it automatically when you mention a resume. Or drive it directly:

```bash
python scripts/build.py examples/engineer.yaml --check   # build + verify
python scripts/ats_check.py Resume.pdf --show-text       # what a parser sees
python scripts/extract.py old_resume.pdf -o resume.yaml  # import an existing one
```

## Templates

| Template | For |
|---|---|
| `modern` | default — tech, product, marketing, general industry |
| `classic` | law, finance, government, medicine — ink only, no colour |
| `compact` | long histories that must fit |
| `academic` | academic CV — publications, grants; multi-page is *correct* here |

## Layout

```
SKILL.md              the workflow Claude follows
DESIGN.md             the design system + the evidence for every rule
assets/tokens.css     the numbers. change here, not in templates
assets/templates/     _base.html.j2 owns structure; variants restyle only
scripts/build.py      yaml -> pdf/docx/txt/html, content lint, --fit
scripts/ats_check.py  parse-back verification
scripts/extract.py    existing resume -> yaml
references/           content, variants (region/industry), review, rendering
tests/scenarios.py    75 scenarios, each built and parse-verified
```

Every rule in `DESIGN.md` carries an evidence grade: `[MEASURED]` (verified here,
reproducible), `[ESTABLISHED]` (primary source), `[CONVENTION]` (consensus, no proof),
`[CONTESTED]` (sources disagree), `[MYTH]` (false — not encoded).

## Non-negotiables

Single column · no skill bars or rating dots · no icons for contact details · no
photo for US/UK/CA/AU · standard section headings · one accent, ≤3 uses · all text
≥ 4.5:1 contrast.

And it will not invent employers, titles, dates, degrees, or metrics. It sharpens,
quantifies, and cuts — it does not fabricate. A resume that wins an interview it
can't survive is worse than no resume.

## Contributing

Add a template under `assets/templates/` extending `_base.html.j2`, override the
`style` block only, and run `tests/scenarios.py`. A variant that fails `bleed` is a
bug, not a variant — the structure is what keeps the document parse-clean, so
variants are deliberately unable to break it.

## License

MIT — see [LICENSE](LICENSE).
