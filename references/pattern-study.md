# Pattern study — 153 premium templates, counted

What the commercial and design-led market actually ships, surveyed rather than assumed,
and what this design system takes from it.

The point of counting is that resume design advice is mostly assertion. "Right-aligned
dates are the premium pattern" is the kind of claim that sounds right and dissolves on
contact with a tally — see §3.

---

## 1. Method, and its limits

**Corpus:** 153 distinct templates catalogued across 9 sources by 10 parallel research
agents (Nov 2025 – Jul 2026 galleries), plus direct visual inspection by the author of
Enhancv, Novorésumé, Kickresume, and Standard Resume.

| Source | Templates | Notes |
|---|---|---|
| Rezi | 28 | positions hardest on ATS |
| Kickresume | 22 | Zety **not fetchable** — 0 recorded rather than guessed |
| Enhancv | 21 | gallery-level only, no per-template pages |
| Resume.io | 18 | incl. `/ats`, `/two-column`, `/picture` category pages |
| Canva | 18 | |
| Adobe Express | 16 | |
| Figma Community | 14 | |
| Novorésumé | 12 | |
| Microsoft Create | 4 | JS SPA; **no template visually examined** |

### What this survey cannot tell you `[IMPORTANT]`

Read this before trusting any number below.

- **Most fetching returns markdown, which has no layout.** `heading_treatment` is
  null/unknown for ~38% of the corpus; `date_alignment` for ~44%. Those fields are
  **not reliable** and no conclusion here rests on them alone.
- **`false` mostly means "no evidence found", not "confirmed absent."** The Resume.io
  and Enhancv surveyors both flagged this explicitly and unprompted. Icon and
  skill-bar counts are therefore **floors, not totals** — the true numbers are higher.
- **Teal, Zety, and Behance/Dribbble were not fetchable.** Zero recorded rather than
  fabricated. The design-led gallery gap matters: Behance/Dribbble would almost
  certainly push the sidebar and photo counts **up**.
- **One agent caught its own tool hallucinating**, verbatim: *"DATA-INTEGRITY WARNING —
  one of my own tools fabricated layout data: my first WebFetch of the Rezi gallery
  confabulated…"* It discarded the result and re-fetched. Assume the rest of the
  corpus has some of this and treat single-source claims accordingly.

A survey that names its own holes is worth more than one that reports a clean 100.

---

## 2. What recurs

Counts across n=153 unless stated.

| Pattern | Count | Share |
|---|---|---|
| **Two-column (any)** | 86 | **56%** |
| — of which a true sidebar | 40 | 26% |
| — two-column content split | 28 | 18% |
| — hybrid | 18 | 12% |
| **Single column** | 33 | **22%** |
| Undetermined | 34 | 22% |
| **Photo** | 47+ | **38%+** |
| **Decorative icons** | 61+ | **50%+** (floor) |
| **Skill rating bars/dots/rings** | 21+ | **17%+** |
| **≤1 accent hue** | 83 | **67%** |

**Multi-column outnumbers single column roughly 2.6 : 1.** This is the market. The
design this system ships is a minority position, and that is a deliberate choice made
against a measurement, not an aesthetic preference.

### Design-led vs ATS-led sources diverge sharply

| | Sidebar-heavy | Skill bars | Photos |
|---|---|---|---|
| **Kickresume** (n=22) | 20/22 multi-col | **14/22** | **17/22** |
| **Adobe Express** (n=16) | **11/16 sidebar**, only 2 single | 2/16 | — |
| **Figma Community** (n=14) | 8/14 sidebar | **0/14 — extinct** | circular crops |
| **Novorésumé** (n=12) | **10/12 multi-col** | 4/12 | 6/12 |
| **Rezi** (n=28) | *"single-column is absolute"* | **0/28** | 1/28 |

The service that optimises hardest for parsing ships the layout this system ships.
The services that optimise for gallery appeal ship the opposite. That is the whole
story of the category in one table.

---

## 3. The claim that dissolved on counting

Earlier research (and most design blogs) told me:

> *"Right-aligned dates are the dominant premium pattern."*

The corpus says otherwise:

- **Adobe Express: 0 of 16** use right-aligned dates.
- **Canva:** dates cluster into *two* conventions — right-aligned **or** inline with
  the employer. Not one dominant.
- Corpus-wide: 18 right-aligned vs 31 left-under-title vs 30 inline — **with 44%
  undetermined**, so nobody should claim a winner.

**Consequence for this system:** right-aligned dates are a *legitimate* convention, not
*the* convention. Shipping only that was a gap. See §6.

---

## 4. Adopted — patterns the corpus supports and this system already does

| Pattern | Corpus evidence | Status |
|---|---|---|
| **One accent hue** | 83/153 (67%); Adobe **14/16**; Canva 12/18 use 0–1 | shipped: exactly one accent, ≤3 uses |
| **ALL-CAPS section headings + rule** | Novorésumé **12/12**; Canva "dominant heading treatment" | shipped: 9.5pt, +0.09em tracking, hairline rule |
| **Name largest, at top** | Canva: *"always the largest element and always at the top"* | shipped: 23pt (26pt banded), left or centred |
| **Restraint over decoration** | Figma: skill bars **0/14**, 0–1 hues | shipped: bars/dots/stars banned |
| **Single column** | Rezi **28/28**; Standard Resume's own copy: *"Recruiters love the one-column layout"* | shipped: the core rule |
| **Generous whitespace at the header** | recurring across sources | shipped: masthead + rule |

The header idiom — **large name, thin rule, single-line contact** — recurs across
essentially every source and is what this system's masthead already is.

---

## 5. Rejected — recurring patterns this system refuses

Honest about *why*, because the reasons are not equally strong.

| Pattern | Corpus | Refused because | Grade |
|---|---|---|---|
| Sidebar / two-column | **86/153 (56%)** | **Measured:** side-by-side blocks merge into fabricated lines at extraction. Reordering the DOM does not help. | `[MEASURED]` |
| Tables for layout | common in Word templates | **Measured:** worst performer of five strategies tested | `[MEASURED]` |
| Skill rating bars/rings | 21+/153; Kickresume 14/22 | Invented precision. Kickresume's `Pipeline` ships **"72% Teamwork", "85% Communication"** — against what scale? Invisible to parsers, and occupies space evidence should. Figma has already abandoned them (0/14). | `[CONVENTION]` |
| Decorative contact icons | **61+/153 (50%+)**; Novorésumé **12/12** | A glyph is not text. Novorésumé labels contact details as icons in **all 12** templates — no plain-text label anywhere. | `[CONVENTION]` |
| Photo | 47+/153 (38%+); Kickresume 17/22 | Legal exposure in US/UK/CA/AU; a field experiment found photos measurably harm women | `[ESTABLISHED]` |
| Full address / nationality | Kickresume `iMessage` ships **"Nationality: American"** + street address | PII leak; evidentiary discrimination risk in the US | `[ESTABLISHED]` |

> **The category's central dishonesty.** Services making the *loudest* ATS claims ship
> the layouts most likely to break parsing:
> - **Resume.io** contradicts itself inside one site: markets templates "created with
>   automated resume scanners in mind", ships one named **"Two Column ATS (Brussels)"**,
>   while its own `/ats` page says *"Use a single-column layout."*
> - **Enhancv** badges its whole catalogue ATS-friendly and asserts *"yes, even with pie
>   charts, icons, and modern two-column layouts."*
> - **Novorésumé**: *"all our resume templates are entirely ATS-friendly"* — 10/12 are
>   multi-column and 12/12 render contact as icon glyphs.
> - **Kickresume** puts templates **with photos** inside its own *ATS-friendly* category.
> - **Rezi** gets the layout right and still repeats the debunked *"75% of resumes are
>   rejected before a human ever sees them."*
> - **Canva and Adobe Express make no ATS claim at all.** They sell "captivating".
>   Honest by omission — and the only two in the set not asserting something unverified.

---

## 6. Missed — good patterns the corpus has and this system lacked

The most useful section. Two real gaps, both corpus-driven, both now closed:

1. **Inline dates.** Right-aligned is *a* convention, not *the* convention (§3 — Adobe
   0/16). Some content simply reads better with the date inline after the employer, and
   it is equally parse-safe (the merged line stays true either way). **Added:**
   `date_style: right | inline`.

2. **Skills as pill/tag chips.** Novorésumé's house pattern (**10/12**), also on Canva
   and Resume.io. Visually distinctive, and — unlike a sidebar — genuinely single-column
   safe, because pills are inline-flowing text that extracts as a plain comma run.
   **Added:** `skills_style: rows | pills`, verified to extract cleanly.

Considered and **not** taken:
- **Circular photo crops** (Figma's universal treatment) — the objection to photos is
  legal, not aesthetic; a nicer crop does not fix it.
- **Pill-shaped section headings**, gradient bands, sidebar skill clouds — decoration
  that buys nothing a parser or a reader can use.

---

## 7. Verdict

**Would this sit credibly beside the corpus?** Yes on typography, hierarchy, restraint,
and colour discipline — it matches or exceeds the median of what is sold, and the
`signature` full-bleed band gives it the "designed" register that the paid galleries
compete on.

**Where it loses, honestly:**
- **No photo option for markets that expect one** (Switzerland, Germany, Japan). Gated
  deliberately in `variants.md`, but a Swiss applicant is genuinely not served today.
- **No pictorial personality.** Canva and Behance sell delight; this sells evidence. For
  a graphic designer whose resume *is* the portfolio, the `portfolio` track exists — but
  it is one template, not a gallery.
- **Fewer skeletons than the big builders** (6 vs Resume.io's ~38 named designs). 107
  presets is more *looks*, but fewer distinct *structures* — by choice, since structure
  is what carries the parse-safety.

**Where it wins, and no template in the corpus does this:** it re-extracts the finished
PDF and shows you the text a parser sees, then tells you when it broke. 153 templates
were surveyed. **Not one of them verifies its own output.** Several assert
ATS-friendliness while shipping layouts that measurably fabricate lines.

The bar this system is trying to clear is not "looks as good as Enhancv." It is
"is true."
