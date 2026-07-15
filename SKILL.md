---
name: resume-designer
description: >
  Create, design, rewrite, review, tailor, or critique a resume or CV, and export it
  to PDF, DOCX, or plain text. Use this skill whenever the user mentions a resume,
  résumé, CV, curriculum vitae, cover letter pairing, job application, "my
  experience for a role", ATS or applicant tracking systems, resume templates or
  formatting, making a resume one page, tailoring a resume to a job description or
  posting, resume bullet points, or asks to make a resume look professional,
  premium, modern, or ATS-friendly. Also use when the user shares an existing
  resume file (PDF/DOCX/YAML) and wants feedback, a redesign, or an export. Produces
  a typeset, single-column, parse-verified document from an editable YAML source.
---

# Resume Designer

Produce a resume that survives both readers: the parser that sees only a text
stream, and the human who spends seconds on it.

**Do not hand-write HTML for a resume.** Write YAML, use the templates, verify the
output. The templates encode measured constraints that are easy to break by hand.

## Scope

This skill handles resume/CV content, design, and export (PDF/DOCX/TXT/HTML), plus
tailoring to a job posting and critique of an existing resume.

It does **not** handle: submitting applications, impersonating a real person,
fabricating employment history, credentials, or metrics, or writing content
designed to deceive an employer. See Integrity below.

## Workflow

### 1. Gather the material

Read `references/intake.md` for the full question set. Never invent facts to fill a
gap — ask. Minimum viable: name, contact, target role, work history with dates, and
one outcome per role.

If the user supplies an existing resume, extract it first:
```bash
python scripts/extract.py old_resume.pdf -o resume.yaml   # PDF/DOCX -> editable YAML
```

### 2. Establish context before designing

Three answers change the output. Ask if unclear:

- **Target role and seniority** — drives section order and length.
- **Region** — photo/DOB/address rules differ and some are legal issues.
  See `references/variants.md`.
- **Industry** — finance, academia, US federal, and design each have hard,
  non-obvious conventions. See `references/variants.md`.

### 3. Write the content

Content decides outcomes; design only decides whether the content gets read.
Full rules in `references/content.md`. The essentials:

- **X-Y-Z**: *Accomplished X, as measured by Y, by doing Z.* Outcome first.
- **Quantify** what can be honestly quantified. Never invent a number.
- Cut: `responsible for`, `duties included`, `team player`, `results-driven`,
  `detail-oriented`, `passionate about`.
- 3–5 bullets for recent roles, 1–2 for older ones. Relevance, not symmetry.

### 4. Choose a template

| Template | Use for |
|---|---|
| `modern` | default — tech, product, marketing, general industry |
| `signature` | when it must look designed — full-bleed colour masthead, still single-column |
| `classic` | law, finance, government, medicine, conservative corporates |
| `compact` | long histories that must fit; dense but still typeset |
| `academic` | academic CV — publications, grants, teaching; multi-page is correct |

### 5. Build

```bash
python scripts/build.py resume.yaml --format pdf,docx,txt --check
```

`--check` runs the parse-back verification. Formats: `pdf` (default; send this),
`docx` (when a posting demands it, or a recruiter wants to edit), `txt` (paste into
web forms), `html` (preview/debug).

### 6. Verify — do not skip

```bash
python scripts/ats_check.py Resume.pdf --data resume.yaml
```

This re-extracts the finished PDF the way a parser does and proves the text layer is
intact: reading order, no fabricated merged lines, fonts really embedded, contact
info regex-findable, headings present, page count.

**Treat `FAIL` as blocking.** Report results honestly — never tell the user a resume
is "ATS-optimized" without having run this.

To see exactly what a parser sees:
```bash
python scripts/ats_check.py Resume.pdf --show-text
```

### 7. Review against the quality bar

Read `references/review.md` and apply it critically. If a check fails, fix and
rebuild. Iterate — the first draft is never the deliverable.

The 10-second test: cover everything but the top third. Can you say who this person
is and what they're good at? If not, the masthead and summary have failed.

## Tailoring to a job posting

Mirror the posting's actual vocabulary where it is **honestly true** of the
candidate — if they say "observability" and the user wrote "monitoring", and the
work is the same, use theirs.

Do this because **a recruiter searches those words**, not because a robot scores
you. Reorder bullets to lead with relevant evidence; drop irrelevant ones.

Never add a skill the user does not have. That is not tailoring, it is lying, and
it fails at the interview.

## Non-negotiable design rules

Enforced by `assets/tokens.css` and measured in `DESIGN.md`:

1. **Single column.** Measured: sidebars, CSS columns, grids, and tables all merge
   unrelated text into fabricated lines at extraction. Fixing DOM order does **not**
   help — PDF has no DOM. Side-by-side is allowed only when both sides belong to the
   same record (role + its dates, label + its values).
2. **No skill bars, dots, or star ratings.** Invented precision, invisible to
   parsers, occupies the space evidence should.
3. **No icons for contact details, no photo** (US/UK/CA/AU), **no text in images.**
4. **Standard section headings.** `Experience`, not `Where I've Made Impact`.
5. **One accent colour**, three uses maximum. All text ≥ 4.5:1 contrast.
6. Never hard-code a value `tokens.css` defines.

## Honesty about ATS

Say what's true, and get the threat model right — the folk version is upside down.

- **No mainstream ATS auto-rejects on formatting, fonts, or file type.** No vendor
  documents such a mechanism. PDFs parse fine everywhere.
- The **"75% auto-rejected by bots"** figure traces to Preptel, a vendor that went
  out of business in 2013 without publishing a study. There is no portable "ATS
  score", and third-party resume scanners simulate nothing.
- **Total parse failure is the benign case** — Greenhouse documents a manual-entry
  fallback where a human types the fields in.
- **The real risk is a silent partial mis-parse**: dates shift or a role drops → a
  *phantom employment gap* appears in the structured record → and automated screening
  on **content** is real and documented (~48–50% of employers auto-screen gaps over
  six months; HBS/Accenture *Hidden Workers*, 2021). No human, no fallback.

So the machine that hurts you reads **content, not typography**. That is exactly why
`ats_check.py` verifies that employers, dates, and degrees extract *correctly* —
not why your font is safe. Do not sell the user fear. See `DESIGN.md` § 7.

## Integrity

Write the strongest **honest** version of the user's history. Sharpen, quantify,
reframe, and cut — never invent employers, titles, dates, degrees, or metrics. If
the user asks for a fabricated credential, decline and offer the strongest truthful
alternative. A resume that wins an interview it can't survive is worse than no
resume.

## Reference map

| File | Read when |
|---|---|
| `DESIGN.md` | changing design, or you want the evidence behind a rule |
| `references/intake.md` | starting from scratch — the question set |
| `references/content.md` | writing bullets, summaries, handling gaps |
| `references/variants.md` | region or industry is anything but generic US |
| `references/review.md` | before delivering — the quality bar |
| `references/rendering.md` | PDF/print/font internals, debugging output |
