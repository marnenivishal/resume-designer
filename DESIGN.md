# Design System — resume-designer

The rulebook behind every document this skill produces. `assets/tokens.css` is the
machine-readable half; this file is the *why*. If you change one, change the other.

Every rule carries an evidence grade. This matters more than usual here, because
resume advice is one of the most polluted information spaces on the internet:
the top search results are content marketing published by companies selling resume
builders, and they profit from making the machinery sound scarier and more
deterministic than it is.

| Grade | Meaning |
|---|---|
| `[MEASURED]` | Verified on this machine by experiment. Reproduce it yourself. |
| `[ESTABLISHED]` | Documented by a primary source or a real study. |
| `[CONVENTION]` | No hard proof; professional consensus. Follow unless there's reason not to. |
| `[CONTESTED]` | Credible sources disagree. A default is chosen and the tradeoff stated. |
| `[MYTH]` | Widely repeated, and false. Do not encode. |

---

## 1. The thesis

> **A resume is one document read twice: once by a parser that only sees a stream of
> text, and once by a human who spends seconds on it. Most templates optimise for a
> third reader who does not exist — the person admiring the layout.**

Almost every "premium" resume design fails the first reader to impress the third.
The central claim of this system is that **this tradeoff is mostly fake**. You can
have real typography — right-aligned tabular dates, true hierarchy, restrained
colour, generous rhythm — and still emit a perfectly clean text stream. What you
cannot have is **columns of unrelated content**. That is a much smaller sacrifice
than the "ATS-safe = ugly Word document" folklore implies.

---

## 2. Layout

### 2.1 Side-by-side content merges at extraction time `[MEASURED]`

This is the single most important finding in this system, and it is the reason the
layout looks the way it does.

**PDF has no DOM.** Chrome emits glyphs into the PDF content stream in *visual*
position order. Anything sitting side by side at the same height is therefore
interleaved into a single line when the text is extracted.

Measured across five layout strategies, two extraction engines (`pdfplumber`,
`pypdf`), identical content in each:

| Layout | Extraction order | Unrelated blocks merged? |
|---|---|---|
| single column | correct in both | no |
| `column-count: 2` | **inverted** in pdfplumber | no |
| flex sidebar (left) | **inverted** in both | **yes** |
| flex sidebar (right) | order ok | **yes** |
| CSS grid sidebar | **inverted** in both | **yes** |
| `<table>` two-cell | **inverted** in both | **yes** |
| flex, main first in DOM, sidebar moved left via `order` | **inverted** in both | **yes** |

Three conclusions, each load-bearing:

1. **A sidebar is not "risky", it is broken by construction.** `flexSideRight`
   extracted in the *right order* and was still wrong, because the lines
   interleaved: a parser read `Senior Engineer, Acme  Python, Go, Kubernetes` —
   a job title welded to a skills list. Order being correct is not sufficient.

2. **Tables are not the safe alternative.** `<table>` was among the worst. This
   directly contradicts the common "use tables, ATS likes tables" advice.

3. **Fixing DOM order does not fix it.** The `flexVisualSwap` case put the main
   column first in the DOM and only moved the sidebar left *visually* via CSS
   `order` — the standard suggested workaround. It changed nothing, because the
   DOM is gone by print time. **This workaround does not work. Do not reach for it.**

> Honest scope: this measures *naive* text extraction. Commercial parsers
> (Textkernel, Affinda, RChilli) do layout analysis and often recover columns
> correctly. The claim here is not "a sidebar gets you auto-rejected" — that is
> unknowable and mostly `[MYTH]`. The claim is narrower and certain: **a sidebar
> makes your text stream depend on the quality of a parser you cannot inspect,
> and buys you nothing a single column cannot deliver.**

### 2.2 The exception, and why it's safe `[MEASURED]`

Side-by-side is *fine* when the merged line is **still true**. Verified — both
engines, clean output:

```
Senior Engineer, Acme        Mar 2021 – Present   ->  "Senior Engineer, Acme Mar 2021 – Present"   ✅ true
Languages    Go, Python, SQL                      ->  "Languages Go, Python, SQL"                  ✅ true
[SKILLS col] [EXPERIENCE col]                     ->  "Senior Engineer, Acme Python, Go"           ❌ fabricated
```

**The rule:** pair a record with *its own* metadata. Never pair a section with a
different section.

This is what rescues the design. Right-aligned dates and label/value skill rows —
the two moves that make a resume look typeset rather than typed — are both on the
safe side of the line.

### 2.2.1 …but only if the left side fits on one line `[MEASURED]`

The rule above is necessary and **not sufficient**. The scenario suite caught this,
and it is subtle enough to be worth stating precisely.

If the left side of a `.row` **wraps**, the right-aligned meta stays on line 1 and
gets extracted *into the middle of the wrapped text*:

```
rendered:                                        extracted:
SVP Partnerships, Northwind    Seattle · 2020    "SVP Partnerships, Northwind Seattle · Jan 2020 – Present"
Global Holdings International                    "Global Holdings International"
```

A parser now reads the employer as **"Northwind Seattle, WA"**, with `Global Holdings
International` orphaned on its own line. The pair is still semantically related — so
the §2.2 rule is satisfied — but the *mechanics* of wrapping severed the company name
anyway.

**Fix:** when `role + ", " + company` exceeds ~58 characters, the company drops to its
own line, where nothing is right-aligned against it and nothing can be injected into
it. `_base.html.j2` does this for experience and education.

The general lesson: **the merged line must be true, AND the left side must be a single
line.** Two conditions, not one.

### 2.3 Page geometry

- Margins `0.62in × 0.72in` `[CONVENTION]`. Below ~0.5in reads cramped and risks
  clipping on consumer printers; above ~1in you are paying a line of content per
  side for whitespace that does no work.
- **One page** through roughly 10 years; two beyond that `[CONTESTED]`. Sources
  genuinely disagree and no rigorous study settles it. Default to one page because
  the cost of an unread second page exceeds the cost of a cut bullet. The **academic
  CV** is a real exception and is *expected* to be long.
- **US federal / USAJOBS is capped at two pages** `[ESTABLISHED]`, not long-form.
  OPM's Merit Hiring Plan imposed a two-page limit that **USAJOBS technically
  enforces as of 27 Sep 2025** — it applies to uploaded, builder, and profile-stored
  resumes alike. Nearly every "federal resumes run 3–7 pages" guide still online is
  now wrong. Do not follow them.
  <br>Source: [OPM — Agency Guidance on the Two-Page Limit](https://www.opm.gov/policy-data-oversight/hiring-information/merit-hiring-plan-resources/agency-guidance-on-the-two-page-limit-on-resume-length/)
- A heading must never be the last thing on a page (`break-after: avoid`), and a
  job entry should not split across pages (`break-inside: avoid-page`). A stranded
  heading is the most common way a resume reads as amateur.

### 2.4 Measure `[CONTESTED]`

The 45–75 characters-per-line rule governs **immersive** reading — paragraphs you
read start to finish. A 7.1in column at 10.5pt runs ~90 characters, over that limit.

This system accepts the wide measure for **bullets** (1–2 lines, scanned in bursts,
where the rule barely applies) and caps **continuous prose** — the summary — at
`--measure-prose: 6.1in`. Applying the book rule to a resume uniformly would force
either enormous margins or a second page, paying real content for a theoretical gain.

---

## 3. Typography

### 3.1 Figures are the font decision `[MEASURED]`

A resume is unusually dense in numbers — dates, percentages, headcounts, dollars.
So the property that matters most is one almost nobody checks: **figure style**.

Measured with `fontTools`, per-digit glyph bounds (em units):

| Font | Figures | Digit widths | Verdict |
|---|---|---|---|
| **Cambria** | lining | **1 distinct** | tabular natively — the default |
| Calibri | lining | 1–2 | fine, but it is the Word default look |
| Times New Roman | lining | uniform | fine, reads as "no choice made" |
| Segoe UI, Arial, Verdana, Palatino | lining | uniform | fine |
| **Georgia** | **old-style** | **9 distinct** | `6`/`8` rise to 0.71em, `3459` fall to −0.18em |
| Corbel, Candara, Constantia, Sitka | **old-style** | many | same problem |

**Georgia is a trap for resumes** — the most-recommended resume serif on the
internet. Its old-style figures make `2021–2025` visibly bounce above and below the
baseline. Beautiful in an essay; on a page that is one-fifth dates, it reads as
uneven. Same for Corbel/Candara/Constantia (the ClearType text fonts).

**Fix, verified:** every one of those fonts exposes `lnum` (lining) and `tnum`
(tabular) OpenType features, and **Chrome applies them when printing to PDF** —
proven by digit advance widths collapsing from 9 distinct to 2 with
`font-variant-numeric: lining-nums tabular-nums`.

So `tokens.css` sets that globally. It is the highest-value line in the file:
- old-style fonts stop bouncing;
- `tnum` gives every digit the same advance, so **right-aligned date columns align
  exactly** — the detail that separates typeset from typed.

Default stack leads with **Cambria** anyway: it is lining *and* tabular natively
(1 distinct width), so it does not depend on feature support at all. Belt and braces.

### 3.2 Never trust a font stack silently `[MEASURED]`

`Inter`, `Lato`, `Source Serif`, `Charter`, and `Garamond` were **not installed** on
the development machine. A template naming them renders in a fallback **with no
error**, and the design quietly collapses.

Therefore: stacks end in a generic family, lead with fonts that actually ship
(Cambria/Calibri/Georgia on Windows+Office, Charter/Helvetica on macOS), and
`ats_check.py` reads the **fonts actually embedded in the PDF** and warns when the
requested family is absent. Verify, don't hope.

### 3.3 Scale, weight, space

- Type scale: minor third (1.2) off a 10.5pt body, **deliberately compressed**.
- **Section headings are the same size as body text** (9.5pt). Hierarchy comes from
  weight + tracking + colour + a rule — not size. A resume that shouts every heading
  has no hierarchy, only noise.
- **Three weights, maximum** `[CONVENTION]`. More reads as indecision.
- Uppercase gets `+0.09em` tracking `[ESTABLISHED]` — capitals were never designed
  to sit adjacent; default spacing is tuned for mixed case.
- The 23pt name gets `−0.012em`: sidebearings are tuned for text sizes and look
  loose when scaled up.
- Leading 1.34 — tighter than web's 1.5, because the measure is short and the
  reader scans.
- **Spacing is a 3pt scale, no exceptions.** Consistent vertical rhythm is the
  entire trick behind "it just looks tidy". The eye reads rhythm as competence.

### 3.4 Type3 fonts `[MEASURED]`

Certain CSS makes Chrome emit `/Type3` fonts — each glyph a *drawing procedure*
rather than real font text. Extraction then depends entirely on the `ToUnicode` map
surviving. Prefer real `/Type0` + `FontFile2`. `ats_check.py` warns on Type3.
See `references/rendering.md` for the property that triggers it.

---

## 4. Colour

- **One accent, used three times at most** `[CONVENTION]`: headline, section
  headings, masthead rule. An accent that appears everywhere is not an accent.
- Body ink is `#16181D`, not `#000` — pure black on white halates slightly in print
  and reads harsh.
- Every text colour passes **WCAG AA 4.5:1** on white `[ESTABLISHED]`. `--c-faint`
  (3.2:1) is for **rules only** and must never carry text.
- Default accent is a deep desaturated teal (8.6:1). Deep and desaturated survives
  greyscale printing — still a common fate — and never reads as decoration.
- `classic` ships **ink-only**. In law/finance/government, restraint is the signal;
  colour reads as compensating for thin content.

**Skill rating bars, proficiency dots, and star ratings are banned** `[CONVENTION]`.
They encode a number you invented ("Python: 4/5") against no scale, they are
invisible to a parser, and they consume the space where evidence belongs. No
credible source defends them.

---

## 5. Content

Design cannot rescue weak content; this is where resumes are actually won.

- **Bullet formula** `[ESTABLISHED]` — Google's X-Y-Z (Laszlo Bock):
  *"Accomplished **X**, as measured by **Y**, by doing **Z**."*
  Lead with the outcome, not the activity.
- **Quantify** `[CONVENTION]`. Scale, %, time, money, volume. `build.py` warns on
  any bullet with no digit — a warning, not an error: some real achievements have no
  honest metric, and inventing one is worse than omitting it.
- **Banned openers** (`build.py` lints these): `responsible for`, `duties included`,
  `worked on`, `helped with`, `tasked with`. They describe a job description, not you.
- **Banned clichés**: `team player`, `results-driven`, `self-starter`, `synergy`,
  `detail-oriented`, `proven track record`, `passionate about`. Every one is a claim
  with no evidence. Show it or cut it.
- **Summary**: 2–3 lines, or omit `[CONTESTED]`. It earns its space only if it says
  something the bullets cannot. A summary restating the bullets is a tax on the
  most valuable real estate on the page.
- No `References available upon request` `[CONVENTION]` — assumed, and wastes a line.
- **No street address** `[ESTABLISHED]` — city + region is what matters; a full
  address leaks PII to every job board that resells your resume.
- No photo / DOB / marital status in the **US, UK, Canada, Australia**
  `[ESTABLISHED]` — they invite discrimination claims and many employers discard
  such resumes for legal hygiene. Expected in parts of the EU. See
  `references/variants.md`.

---

## 6. Anti-patterns

Refuse these, and say why:

| Anti-pattern | Why |
|---|---|
| Sidebar / two-column | `[MEASURED]` fabricates lines in the text stream (§2.1) |
| Tables for layout | `[MEASURED]` worst performer; the "ATS-safe" advice is backwards |
| Skill bars / dots / stars | invented precision, invisible to parsers, costs evidence space |
| Icon **replacing** a contact label | Novorésumé does this in 12/12 templates — the glyph carries the meaning and a parser gets nothing. An icon *beside* text (`✉ jane@x.com`) is harmless: Rezi, the most parse-serious vendor surveyed, ships them 20/20. The rule is **never replace text**, not **never decorate**. |
| Photo (US/UK/CA/AU) | legal exposure, zero signal |
| Text inside images | invisible to extraction |
| Headers/footers for contact | some parsers never read them; the page-1 masthead is free |
| Full street address | PII leak, no benefit |
| Creative section names | "Where I've Made Impact" defeats heading detection for nothing |
| More than 3 weights / 2 families | reads as indecision |
| Justified text | rivers of whitespace at this measure; rag right |

---

## 7. ATS: the correct threat model

The folk model is upside down, and getting it right changes what the design optimises
for.

### 7.1 Parse failure is the *benign* outcome `[ESTABLISHED]`

Greenhouse documents the fallback verbatim: *"If a resume fails to parse, you'll need
to manually input the candidate's details into the fields."* The document stays
attached and visible. **A total parse failure is loud and self-correcting — a human
types your details in.**

### 7.2 Silent partial mis-parse is the actual risk `[ESTABLISHED]`

> Dates shift, a role drops, a degree is missed → a **phantom employment gap** now
> exists in the structured record → and automated screening on *content* is real,
> documented, and common: **~48–50% of employers automatically screen out resumes
> showing an employment gap over six months**, and degree filters behave the same way.
> No human, no fallback, no notification.
>
> Source: Harvard Business School / Accenture, *Hidden Workers: Untapped Talent*
> (2021) — n=8,720 workers, 2,275 executives, US/UK/DE. Over 90% of employers use
> their system to filter or rank; candidates *"fall out of the candidate pool, having
> never been assessed by a human being."* Corroborated causally by Kroft, Lange &
> Notowidigdo, *QJE* 128(3) 2013 (~12,000 resumes): gaps reduce callbacks, with most
> of the decline inside the first 8 months.

So the machine that hurts you **reads content, not typography**. It doesn't reject
your font. It rejects the gap your mis-parsed dates invented.

This is why `ats_check.py` verifies *field-level fidelity* — that your employers,
dates, and degree extract correctly and in order — rather than scoring keywords.
**That check is the whole point.** It is not a nicety.

### 7.3 The upside is avoiding the zero, not scoring points `[ESTABLISHED]`

Well-formed input already parses at **>95% accuracy, ~0.5s median** (Textkernel
specs). The distribution is **bimodal**: you are either fine or you are in the zero
bucket (`ovIsImage`, `ovNoText`, `ovIsEncrypted`, `ovCorrupt`). And per Textkernel:
*"The vast majority of problems in parsing are not from processing the plain text,
but from conversion to plain text."*

Which is exactly the step this skill measures.

### 7.4 Myths — never encode, correct on contact `[MYTH]`

- **"75% of resumes are auto-rejected by ATS before a human sees them."** The origin
  is now traceable: **Preptel**, a resume-optimisation vendor that **went out of
  business in August 2013** without ever publishing a study, dataset, or method. The
  number drifts across retellings — 70%, 75%, 88% — which is diagnostic of folklore.
  A real statistic has one value and one method.
- **"PDFs can't be read by ATS."** False for every mainstream system. Greenhouse
  accepts `.doc/.docx/.pdf/.rtf/.txt` and states **no preference**.
- **"You need a keyword-match score above N."** No such universal gate exists, and
  third-party "ATS scanners" simulate no real ATS — there is no portable ATS score.
- **"No mainstream ATS auto-rejects on formatting, fonts, or file type"**, and no
  vendor documents such a mechanism.

The skill mirrors job-posting vocabulary because **a human recruiter searches those
words** — not because a robot is scoring you. Same action, honest reason.

### 7.5 Named parse-breakers, from the vendor `[ESTABLISHED]`

Greenhouse names these explicitly, which independently corroborates §2.1:

contact info **in a header, footer, or text box** · **columned layouts** · complex
tables · graphics/photos/word art · spaces between letters · resumes **over 2.5 MB**
(uploads accept 100 MB — the *parse* fails, silently) · abbreviated job titles
(`Sr. Account Exec` rather than `Senior Account Executive`) · company names missing
`Inc./Co./Ltd/LLC`.

---

## 8. Extending this system

1. Add a variant under `assets/templates/`, extending `_base.html.j2`.
2. Override the `style` block **only**. If you are overriding the `body` block to
   move content side by side, re-read §2.1 — the structure is what keeps the
   document parse-clean, so variants are deliberately unable to break it.
3. Never hard-code a number a token already defines.
4. Run `scripts/ats_check.py` on the output. A variant that fails `bleed` is not a
   variant, it is a bug.
