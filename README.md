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

**It's honest about ATS — and gets the threat model right.** The famous *"75% of
resumes are auto-rejected by bots"* traces to Preptel, a vendor that went out of
business in 2013 without ever publishing a study. No mainstream ATS auto-rejects on
formatting or fonts; PDFs parse fine everywhere; there is no portable "ATS score".

But the folk model is upside down in a more interesting way. **Total parse failure is
the *benign* outcome** — Greenhouse documents a fallback where a human types your
details in. **The real risk is a silent partial mis-parse**: your dates shift, a
*phantom employment gap* appears in the structured record, and ~48–50% of employers
automatically screen out gaps over six months (HBS/Accenture *Hidden Workers*, 2021,
n=8,720). No human, no fallback, no notification.

So the machine that hurts you reads **content, not typography**. That's precisely why
this tool verifies that your employers, dates and degrees extract *correctly* —
rather than scoring your keywords. See [`DESIGN.md § 7`](DESIGN.md).

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

## 107 looks, 6 skeletons

```bash
python scripts/build.py --list-presets
python scripts/build.py resume.yaml --preset material-blue
python scripts/gallery.py          # render every preset into one browsable page
```

A preset is a point in the design space — **skeleton × type pairing × accent ×
heading treatment × density** — not a file. That's deliberate: 107 template *files*
would be 107 things to maintain and parse-test, and the "100+ templates" on
commercial sites are a handful of skeletons with colour swaps sold as variety. This
is the same variety, honestly labelled, and every preset inherits the one tested
structure — so a preset **cannot** break parse-safety, only retune the look.

Families: `material` `signature` `modern` `editorial` `classic` `compact` `minimal`
`academic` `executive` `technical` `warm` `nordic` `banded`.

Every accent is verified ≥4.5:1 on white at generation time. Worth knowing: of 160
colours in a well-known UI palette set, **93 fail that bar** — screen palettes assume
large text, while a resume accent carries small heading text.

## Templates

| Template | For |
|---|---|
| `modern` | default — tech, product, marketing, general industry |
| `signature` | the premium look — full-bleed colour masthead, reversed-out name, no sidebar |
| `classic` | law, finance, government, medicine — ink only, no colour |
| `compact` | long histories that must fit |
| `academic` | academic CV — publications, grants; multi-page is *correct* here |
| `mono` | monospace headings — tabular by construction; 1 of 177 surveyed does this |
| `portfolio` | design specimen for a folio/site — **not** an application document |

## What the market actually ships

[`references/pattern-study.md`](references/pattern-study.md) surveys **177 real
templates** across Behance/Dribbble, Rezi, Kickresume, Enhancv, Resume.io, Canva, Adobe
Express, Figma Community, Novorésumé, Standard Resume and Microsoft Create — counted
from per-record fields, over stated denominators (35 have unknown columns; 71 have no
observable date field — rates over the full 177 would understate everything):

| | |
|---|---|
| Two-column | **80/142 known = 56%** (single: 25%) |
| One accent hue | **122/154 = 79%** |
| Skill rating bars | **32/177 = 18%** — and **31 of the 32 have no scale** |
| Right-aligned dates | **21/105 = 20%** — a minority convention |
| Name largest & at top · ALL-CAPS heading + rule | **zero counterexamples in 177** |

The interesting part is the contradiction. **Resume.io** ships a template named
*"Two Column ATS"* while its own `/ats` page says *"Use a single-column layout."*
**Enhancv** badges its whole catalogue ATS-friendly and claims *"yes, even with pie
charts, icons, and modern two-column layouts."* **Novorésumé** says *"entirely
ATS-friendly"* — 10 of 12 are multi-column and 12 of 12 render contact details as icon
glyphs. **Rezi**, which optimises hardest for parsing, agrees with the measurement
(*"single-column… read linearly"*) and still repeats the debunked 75% myth.

**Canva and Adobe Express make no ATS claim at all.** They sell "captivating" — the
only two in the set not asserting something unverified.

Of 177 templates surveyed, **not one verifies its own output.**

**The study changed this tool five ways** — the most useful thing it did was find faults:

- **A shipped defect.** The org-drop rule ran *per record*, so one long job title could
  put two date conventions in one document — the exact fault the survey holds against
  Canva's *Minimalist White and Grey*. Now document-scoped.
- **A character threshold can't be paper-independent** (A4 is 6mm narrower). Now 55/58.
- **The icon ban was overbroad.** Rezi — the most parse-serious vendor — ships contact
  glyphs on 20/20. The real rule is *never let an icon **replace** text*; beside text
  it's harmless. Novorésumé's 12/12 icon-only contact is the actual defect.
- **`date_style: inline`** — right-aligned is *a* convention, not *the* one (Adobe 0/15,
  Novorésumé 0/12, Kickresume 0/22 — 49 templates, no date rail).
- **`monogram` and `mono-head`** — the corpus's only honest answer to "what goes where
  the photo isn't", and the one type track that is tabular *by construction*.

And one point it earned for this tool: two sources mention fonts at all, **zero mention
figure style**. This is the only artifact in the corpus that noticed Georgia's old-style
figures make a date rail bounce — *which is exactly why the sources without tabular
figures ship no date rail.* They didn't fail to think of it; they lacked the prerequisite.

## Works with any AI tool

The interface is a CLI, so anything that can run a shell can drive it.

| Tool | Reads |
|---|---|
| Cursor, Copilot, Codex, Zed, Windsurf, Aider, ChatGPT | `AGENTS.md` |
| Cursor (rules) | `.cursor/rules/resume-designer.mdc` |
| Claude Code | `SKILL.md` (auto-activates), `CLAUDE.md` |
| Humans | this file |

All of them point at `AGENTS.md` rather than restating it, so they can't drift apart.

## Layout

```
AGENTS.md             instructions for any AI agent — the canonical one
SKILL.md              the workflow Claude follows
DESIGN.md             the design system + the evidence for every rule
assets/tokens.css     the numbers. change here, not in templates
assets/templates/     _base.html.j2 owns structure; variants restyle only
scripts/build.py      yaml -> pdf/docx/txt/html, content lint, --fit
scripts/ats_check.py  parse-back verification — does the machine read it?
scripts/micro_qa.py   typographic QA — runts, rhythm, alignment, margins
scripts/extract.py    existing resume -> yaml
scripts/gallery.py    render every preset into one contact sheet
assets/presets.yaml   113 named looks (generated by scripts/gen_presets.py)
references/           content, variants, review, rendering, pattern-study
tests/scenarios.py    92 scenarios, each built and parse-verified
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
