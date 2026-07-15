# Pattern study — 177 premium templates, counted

What the commercial and design-led market actually ships, surveyed rather than
assumed, and what this design system takes from it.

The point of counting is that resume design advice is mostly assertion. *"Right-aligned
dates are the premium pattern"* is the kind of claim that sounds right and dissolves on
contact with a tally — see §3.

---

## 1. Method, and its limits

**Corpus:** 177 distinct templates catalogued across 10 source groups by parallel
research agents (2025–2026 galleries), plus direct visual inspection by the author of
Enhancv, Novorésumé, Kickresume and Standard Resume.

| Source | Templates |
|---|---|
| Behance / Dribbble (design-led) | 24 |
| Rezi | 20 |
| Kickresume | 22 |
| Enhancv | 21 |
| Resume.io | 18 |
| Canva | 18 |
| Adobe Express | 16 |
| Figma Community | 14 |
| Novorésumé | 12 |
| Standard Resume | 8 |
| Microsoft Create | 4 |
| **Teal, Zety** | **0 — Cloudflare 403 on every route; recorded zero rather than guessed** |

### Denominators, because they move the answer `[IMPORTANT]`

Read this before trusting any number below.

- **Most fetching returns markdown, which has no layout.** 35 of 177 templates have
  `columns: unknown`; 71 have no observable `date_alignment`; 23 have no
  `accent_colors`. **Rates computed over 177 understate every attribute** — so every
  rate here is quoted over its *observable subset*, with n stated.
- **`false` mostly means "no evidence found", not "confirmed absent."** The Resume.io
  and Enhancv surveyors flagged this themselves, unprompted. Icon and bar counts are
  **floors**.
- **Per-source prose miscounts its own records in at least six places.** Adobe's
  summary claims "11 of 16 sidebar" — its records say 9; Figma claims 8 of 14, records
  say 5; Behance claims 11 of 24 bars, records say 9. **Every count below is recomputed
  from the per-record fields, not the prose.** (An earlier version of this document
  quoted the prose. It was wrong.)
- **One agent caught its own tool fabricating layout data** — verbatim: *"DATA-INTEGRITY
  WARNING — one of my own tools fabricated layout data: my first WebFetch of the Rezi
  gallery confabulated…"* It discarded and re-fetched.

A survey that names its own holes is worth more than one reporting a clean 100.

---

## 2. What recurs

### 2.1 Structure (n=142 with known columns)

| Layout | n | % of known |
|---|---|---|
| **Two-column, any** (47 sidebar + 33 content-split) | **80** | **56%** |
| Single | **36** | 25% |
| Hybrid | 26 | 18% |

**Two-column is the majority of everything observable.** This system ships the 25%
position — deliberately, against a measurement, not a preference.

### 2.2 The two universals — zero counterexamples in 177

1. **The name is the largest element and sits at the top.** Canva: *"the single most
   invariant structure in the set"* (18/18). Behance: *"the largest element on the page
   in every single piece"* (24/24). Novorésumé 12/12.
2. **ALL-CAPS section heading + a delimiter rule.** *"Near-universal heading grammar"*
   (Behance), *"universal — 12 of 12"* (Novorésumé). Kickresume is the lone dissenter.

This system does both.

### 2.3 Chromatic restraint is near-total (n=154 scored)

| accent hues | n | % |
|---|---|---|
| 0 | 29 | 19% |
| 1 | 93 | 60% |
| **≤1** | **122** | **79%** |
| ≥3 | **4** | **2.6%** |

Three of the four maximalist outliers are **collections or self-branded personal CVs,
not products**. Maximalism is functionally extinct in shipped commercial work.

### 2.4 Skill bars are a legacy tail, not a norm — and 31 of 32 have no scale

**32/177 (18%)**, but 23 come from just two sources (Kickresume 14/22, Behance 9/24).
The modern cohort ships **zero**: Figma 0/14, Enhancv 0/21, Rezi 0/20, Standard Resume
0/8.

**Of the 32, exactly one has a scale** (Novorésumé *Tech*, with an axis tick). The other
31 are, in the corpus's words, *"unlabelled… no legend, no units, no baseline. Purely
decorative rhetoric."* Kickresume's `Pipeline` asserts **"72% Teamwork"** against
nothing at all.

### 2.5 Design-led vs ATS-led disagree on everything except type

| | Design-led (Behance+Figma) | ATS-led (Rezi+Standard) |
|---|---|---|
| single column | **8/37 (22%)** | **6/8 (75%)** |
| two-column any | 19/37 (51%) | 1/8 (13%) |
| photo | **21/38 (55%)** | **1/28 (4%)** |
| skill bars | **9/38 (24%)** | **0/28** |
| ≤1 accent | 25/38 (66%), max 6 | **28/28 (100%), max 1** |
| **icons** | **20/38 (53%)** | **20/28 (71%)** ← inversion |

Both ATS-led heterodoxies (a sidebar, a photo) belong to **Standard Resume — the source
that doesn't market on ATS at all.** Rezi, which does, ships 0 sidebars, 0 photos,
0 bars, ≤1 hue across 20 templates.

---

## 3. The claim that dissolved on counting

Earlier research told me: *"Right-aligned dates are the dominant premium pattern."*

| Convention | n | % of 105 observable |
|---|---|---|
| left-under-title | **42** | **40%** |
| inline | 34 | 32% |
| **right-aligned** | **21** | **20%** |
| sidebar | 8 | 8% |

Right-aligned is a **Canva + Rezi habit and nothing else**. **Adobe (0/15), Novorésumé
(0/12) and Kickresume (0/22) ship zero right-aligned dates between them — 49 templates,
no date rail.**

This system shipped only the 20% convention — the one that *needs a conditional*
(§5.1). `date_style: inline` was added because of this count.

> **The causal insight, and it is this system's best-earned point:** two sources mention
> fonts at all; **zero mention figure style.** This is the only artifact in the corpus
> that noticed Georgia's old-style figures make a date rail bounce — *which is precisely
> why the three sources with no tabular figures ship no date rail.* You cannot align a
> date column with proportional digits. They didn't fail to think of it; they lacked the
> prerequisite.

---

## 4. Adopted

| Shipped rule | Corpus evidence |
|---|---|
| ALL-CAPS headings + hairline rule | the corpus's #1 invariant |
| Name largest, at top | the corpus's #0 invariant — 0 counterexamples in 177 |
| One accent hue | 122/154 (79%) |
| **Accent on employer names** | Canva *Science and Engineering*: *"accent carries semantic weight rather than being purely decorative — **the sharpest use of a single hue in the sample**"* |
| **Words, not bars** | Behance *Resume Layout*: skills in words — *"**the single best decision in the whole survey and a direct rebuke to the bar convention**"* |
| Full-bleed masthead band | ~15–18 templates; resume.io's own /creative formula is *"a strong block of color at the top"*. **This is the corpus's most conventional premium gesture — not an invention.** |
| Static fonts, native tabular figures | **Zero corpus coverage.** Nothing else here noticed. |
| ≥4.5:1 contrast, greyscale survival, 3pt scale | **Zero corpus coverage.** No vendor mentions contrast, print, or a spacing scale. |

---

## 5. What the audit found wrong with *this* system

### 5.1 A shipped defect — fixed

The org-drop rule (`role + ", " + company` over ~58 chars → company to its own line) was
applied **per record**. A four-job resume could render three entries with a date rail and
the fourth as a two-line block: **two date conventions in one document** — exactly the
defect the survey holds against Canva's *Minimalist White and Grey*.

**Fixed:** promoted to **document scope**. If any record trips the limit, all records
adopt the dropped form. Consistency beats compactness.

### 5.2 The threshold was paper-independent, and can't be — fixed

A constant measured in *characters* cannot be paper-independent: A4 is 6mm narrower than
Letter. **Fixed:** 55 for A4, 58 for Letter.

### 5.3 The icon ban was overbroad — corrected

Shipped rule: *"no icons for contact details."* But **Rezi — the most parse-serious
vendor in the corpus — puts contact glyphs on 20 of 20 templates** while its own docs ban
columns, bars and percentages. The ATS camp out-decorates the design camp (71% vs 53%).

They are not wrong, and neither was the ban's *intent*. The distinction the rule missed:

- **Icon *replacing* text** — Novorésumé, 12/12, *no template labels contact as plain
  text*. The glyph carries the meaning. **This is the real defect.**
- **Icon *beside* text** — Rezi's pattern. `✉ jane@x.com` still regex-matches. Harmless
  decoration; earns nothing, breaks nothing.

**Corrected rule:** an icon must never *replace* text. Beside it, it is merely pointless.

### 5.4 Cambria reads as Word — acknowledged

Cambria is technically the best font decision here (static, native lining + tabular).
It is also **the default serif of Microsoft Word 2007–2010**. Standard Resume — the most
typographically disciplined source — reaches for IBM Plex Serif and EB Garamond instead.
**Added:** `mono-head` type pairing. Mono is lining + tabular **by construction** — zero
figure-style risk, a perfect date rail, and **1 of 177** templates differentiates on it
(Standard Resume *Keefer*), making it a differentiator rather than table stakes.

### 5.5 The monogram — adopted

The corpus's only honest answer to *"what goes where the photo isn't"*. Dribbble's
*John Doe monogram*: *"the **only piece in the survey to solve the photo problem rather
than indulge it, and worth stealing**"*. Standard Resume uses one as its signature.

It passes this system's own test: `ME Maya Ellison` — a merged line that stays true.
**Added:** `monogram: true`.

---

## 6. Rejected

| Pattern | Corpus | Refused because | Grade |
|---|---|---|---|
| Sidebar / two-column | **80/142 (56%)** | **Measured:** side-by-side blocks merge into fabricated lines; DOM order is not a lever in a PDF | `[MEASURED]` |
| Tables for layout | Microsoft Support: *"Many templates use tables to streamline the layout"* | **Measured:** worst of five strategies tested | `[MEASURED]` |
| Skill bars | 32/177; **31 of 32 have no scale** | Invented precision — "72% Teamwork" against what? Figma already abandoned them (0/14) | `[CONVENTION]` |
| Photo | 47+/177 | Legal exposure US/UK/CA/AU; a field experiment found photos measurably harm women | `[ESTABLISHED]` |
| Full address / nationality | Kickresume *iMessage* ships **"Nationality: American"** + street address | PII leak; evidentiary discrimination risk | `[ESTABLISHED]` |

> **The category's central dishonesty.** The loudest ATS claims come with the layouts
> most likely to break parsing:
> - **Resume.io** contradicts itself inside one site: ships **"Two Column ATS
>   (Brussels)"** while its own `/ats` page says *"Use a single-column layout."*
> - **Enhancv** badges its whole catalogue and asserts *"yes, even with pie charts,
>   icons, and modern two-column layouts."*
> - **Novorésumé**: *"entirely ATS-friendly"* — 10/12 multi-column, 12/12 icon-only contact.
> - **Kickresume** puts templates **with photos** inside its own ATS category.
> - **Rezi** gets the layout right and still repeats the debunked *"75% are rejected."*
> - **Canva and Adobe Express make no ATS claim at all.** They sell "captivating" — the
>   only two not asserting something unverified.

---

## 7. Verdict

**Matches or exceeds the corpus on:** both universals, colour discipline (79% cohort),
the corpus's single best-reviewed idea (words not bars), and typographic control nothing
else here attempts — contrast, greyscale survival, figure style, a spacing scale.

**Loses on, honestly:**
- **No photo for markets that expect one** (CH/DE/JP). Deliberate, but a Swiss applicant
  is genuinely not served.
- **Fewer skeletons** than the big builders (7 vs Resume.io's ~38 named designs). More
  *looks*, fewer *structures* — by choice, since structure carries the parse-safety.
- **The full-bleed band is conventional, not novel.** It is the corpus's standard premium
  gesture. This system does it correctly, not first.

**Wins on the only thing nobody else does:** it re-extracts the finished PDF and shows
you the text a parser sees, then tells you when it broke. **177 templates surveyed. Not
one verifies its own output.** Several assert ATS-friendliness while shipping layouts
that measurably fabricate lines.

The bar is not "looks as good as Enhancv." It is **"is true."**
