# AGENTS.md — instructions for AI coding agents

For Cursor, GitHub Copilot, Codex, Zed, Windsurf, Claude Code, Gemini CLI, Aider,
ChatGPT with a code interpreter, or any agent that can run a shell.

**You are here because someone wants a resume built, fixed, redesigned, or reviewed.**
This repo is a tool for doing that well. Read this file, then use the CLI. Do not
hand-write HTML or reimplement the layout — the templates encode measured constraints
you will break by hand.

---

## Setup

```bash
pip install -r requirements.txt          # pyyaml jinja2 pdfplumber pypdf python-docx
```
Needs Python 3.10+ and Chrome/Chromium/Edge (auto-detected; else set
`RESUME_CHROME=/path/to/chrome`).

## The whole interface

```bash
# 1. describe the person in YAML   (start from examples/engineer.yaml)
# 2. build
python scripts/build.py resume.yaml --format pdf,docx,txt --check

# 3. verify — this is not optional, see "The one rule" below
python scripts/ats_check.py Resume.pdf --data resume.yaml

# other things you'll want
python scripts/build.py --list-presets                    # 107 named looks
python scripts/build.py resume.yaml --preset material-blue
python scripts/build.py resume.yaml --fit                 # compress to max_pages
python scripts/extract.py old_resume.pdf -o resume.yaml   # import an existing resume
python scripts/ats_check.py Resume.pdf --show-text        # what a parser actually sees
python scripts/micro_qa.py Resume.html                    # runts, rhythm, alignment, margins
python scripts/gallery.py                                 # render every preset to one page
python tests/scenarios.py                                 # 92 scenarios, all parse-verified
```

Two checkers, two questions:
- `ats_check.py` — *does the machine read it?* (reading order, fonts, contact, bleed)
- `micro_qa.py` — *does it look like a competent person made it?* (single-word last
  lines, off-grid gaps, ragged date column, margins, half-empty pages)

`build.py` exits non-zero on error and prints a content lint to stderr. `ats_check.py`
exits 0 clean / 1 warnings / 2 failures.

## The one rule

**Run `ats_check.py` and report what it says. Never tell a user their resume is
"ATS-friendly" without it.** That claim is the single most common lie in this product
category. The checker re-extracts the finished PDF the way a parser does and proves —
or disproves — that the text layer survived. If it fails, fix it; don't ship it and
describe it as fine.

## What you must not do

- **Do not invent** employers, titles, dates, degrees, or metrics. Sharpen, quantify,
  reframe, cut — never fabricate. A resume that wins an interview it can't survive is
  worse than no resume. If asked for a fake credential, decline and offer the
  strongest truthful alternative.
- **Do not add a sidebar or two-column layout.** Measured: any two blocks side by side
  at the same height are merged into one line by PDF text extraction, producing lines
  the author never wrote (`Senior Engineer, Acme  Python, Go`). Reordering the DOM does
  not help — PDF has no DOM. Tables are the worst offender, not the safe choice.
- **Do not add skill rating bars, dots, or stars.** Invented precision, invisible to
  parsers, and they occupy the space evidence should. (Surveyed: 21+ of 153 commercial
  templates ship them; Kickresume's `Pipeline` asserts "72% Teamwork" — against what
  scale? Figma Community has already abandoned them: 0 of 14.)
- **Do not add icons for contact details or a photo** (US/UK/CA/AU).
- **Do not hard-code values** that `assets/tokens.css` defines.
- **Do not repeat the "75% of resumes are auto-rejected by bots" claim.** It traces to
  a vendor that went out of business in 2013 without publishing a study. See
  `DESIGN.md § 7` for what's actually true.

## Where things are

| Path | What |
|---|---|
| `DESIGN.md` | the design system + the evidence for every rule. **Read before changing design.** |
| `SKILL.md` | the end-to-end workflow (written for Claude, useful to any agent) |
| `assets/tokens.css` | every number. Change here, never in a template. |
| `assets/templates/` | `_base.html.j2` owns structure; variants override `style` only |
| `assets/presets.yaml` | 107 named looks. Generated — edit `scripts/gen_presets.py` |
| `references/content.md` | bullet formulas, banned phrases, gaps, career changes |
| `references/variants.md` | region + industry rules (several are legal-adjacent) |
| `references/review.md` | the quality bar. Run it before delivering. |
| `references/rendering.md` | PDF/font/Chrome internals when output looks wrong |
| `references/pattern-study.md` | what 153 surveyed commercial templates actually do, counted |
| `tests/scenarios.py` | 92 scenarios, each built and parse-verified |

## Editing this repo

- Add a template: extend `_base.html.j2`, override the `style` block **only**. The
  structure is what keeps the document parse-clean, so variants are deliberately
  unable to break it.
- Add a look: add to `scripts/gen_presets.py` and regenerate `assets/presets.yaml`.
  Accents must clear 4.5:1 on white — the generator enforces this. (For scale: 93 of
  160 colours in a well-known UI palette set fail that bar.)
- Always run `python tests/scenarios.py` before claiming done. A variant that fails
  `bleed` is a bug, not a variant.

## Evidence grades

`DESIGN.md` marks every rule: `[MEASURED]` (verified here, reproducible),
`[ESTABLISHED]` (primary source), `[CONVENTION]` (consensus, no proof),
`[CONTESTED]` (sources disagree — a default is chosen and stated), `[MYTH]` (false,
never encoded). **Respect the grades.** Do not restate a `[CONVENTION]` as fact, and
do not "fix" a `[CONTESTED]` default without reading the tradeoff.
