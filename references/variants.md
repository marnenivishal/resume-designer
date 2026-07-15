# Variants — region, industry, document class

Most resume advice online is written for one audience (mid-career US private sector)
and presented as universal. It isn't. Several rules below are **hard requirements**
where getting them wrong marks the applicant as an outsider — or breaks a submission
outright.

---

## 1. Pick the document class first

**This is the biggest branch, and it comes before styling.** The same person needs a
different *class* of document for different targets — not a restyle of one document.

| Class | Length | Nature | Template |
|---|---|---|---|
| **Resume** | 1–2 pp | selective, tailored, achievement bullets | `modern` / `classic` / `compact` |
| **Academic CV** | uncapped | comprehensive, citation-formatted, *includes references* | `academic` |
| **Structured form** | n/a | you fill *their* fields (USAJOBS builder, ERAS) | none — the form wins |

An academic CV is not "a long resume", and a resume is not "a trimmed CV". Converting
between them is a rewrite, not an edit.

---

## 2. Length is a lookup, not a constant `[ESTABLISHED]`

There is **no universal one-page rule** — it's a narrow US industry norm, not a global
default. The one-page rule is *unsupported* by the available evidence; note that the
largest experiment contradicting it was run by a company selling resume writing, so
the honest verdict is **"the one-page rule is unsupported"**, not "two pages win".

| Target | Cap |
|---|---|
| US, 0–7 yrs experience | **1 page** |
| US, 7+ yrs or advanced degree | 2 pages |
| US — consulting / finance / tech | **1 page** (industry norm is real here) |
| **US federal (USAJOBS)** | **2 pages, technically enforced** — see §4 |
| Canada, UK, Ireland, France, Netherlands | 2 |
| **Germany** | 2 (hard) |
| UK civil service | 2 (hard) |
| Switzerland | 3 (target 2) |
| Australia / New Zealand | 3 (target 2) |
| **Academic CV** | **uncapped** — length is dictated by content |

On a 2-page resume, **repeat the candidate's legal name at the top of page 2** — pages
get separated. (MIT career services checklist.)

---

## 3. Region — photo and personal data

### The US rule is evidentiary, not a ban `[ESTABLISHED]`

Commonly mis-stated. It is **not illegal** for a candidate to put a photo on a US
resume, and the EEOC does not categorically forbid employers from asking about age or
marital status. The mechanism is **evidentiary**: such data becomes evidence of
discriminatory intent if a claim is brought, so many employers discard resumes
containing it to protect themselves. The photo hurts you because of how the *employer*
must react to it.

It also hurts directly: a field experiment found including a photo **measurably harms
women**, while no-photo men are penalized relative to attractive men `[ESTABLISHED]`.
There is no version of this where a photo is a neutral choice in the US market.

### Street address: omit `[ESTABLISHED]`

Applicants with addresses **farther from the job get measurably fewer callbacks**.
Keep `City, State` so location-filtered searches still match; drop street and ZIP.
For remote roles use `Remote` or the target metro.

### Region table

Default OFF unless marked. `photo` includes any headshot frame.

| Region | Photo | DOB | Nationality | Marital | Notes |
|---|---|---|---|---|---|
| **US, Canada, UK, Ireland, Australia, NZ** | ✗ | ✗ | ✗ | ✗ | NZ's govt careers service says remove photos outright; Australia's own human-rights regulator asks for no photo/DOB |
| **Germany** (*Lebenslauf*) | common | common | — | — | photo still conventional despite AGG; signed+dated is traditional |
| **France** | common | common | — | — | 2 pp |
| **Netherlands, Nordics** | optional | optional | — | — | |
| **Switzerland** | **expected** | **expected** | **expected** | — | the major European exception; photo 45×65mm or 60×90mm, plus residence-permit type. Private-sector hiring discrimination is largely unsanctioned |
| **Japan** (*rirekisho*) | **expected** | **expected** | — | ✓ | a prescribed FORM, not a designed document — this skill's templates do not apply |
| **UAE / Gulf** | offered | offered | offered | ✗ | `[CONTESTED]` — the "photo + nationality expected" convention rests almost entirely on vendor sources, so offer these, never force them. **Never** religion |
| **India, Singapore** | ✗ | ✗ | ✗ | ✗ | follow the US/UK ruleset |

**GDPR (EU/UK):** personal data on a CV is processed by the employer; that's their
obligation, not the candidate's. It is not a reason to omit data the local convention
expects — but it *is* a reason never to include more than the convention requires.

> If a region expects a photo and the user wants one, say what the tradeoff is and let
> them decide. Do not silently override a local convention with a US default — and do
> not silently apply a photo to a US application either.

---

## 4. Industry

### US federal / USAJOBS — **the long-form era is over** `[ESTABLISHED]`

As of **27 September 2025**, OPM's Merit Hiring Plan caps federal resumes at **two
pages**, and **USAJOBS technically enforces it** — for uploaded, builder, and
profile-stored resumes alike, across Title 5 competitive and excepted service.

**Nearly every "federal resumes should be 3–7 pages" guide online is now wrong.** Do
not emit per-duty narratives, KSA essays, or exhaustive job history. Verify the
rendered page count.
Source: [OPM — Agency Guidance on the Two-Page Limit](https://www.opm.gov/policy-data-oversight/hiring-information/merit-hiring-plan-resources/agency-guidance-on-the-two-page-limit-on-resume-length/)

### Academic CV `[ESTABLISHED]`

- **No page cap.** ~2–4 pp for a grad student, 10+ for senior faculty. Length follows
  content; trimming it is the error.
- **All** publications, in a consistent citation style. Numbered, hanging indent.
- **Grants are a first-class scored section** — unlike any private-sector resume:
  `{Title}. {Funder}, {Grant #}. {Role: PI|Co-PI|Co-I}. ${amount}. {MM/YYYY–MM/YYYY}.`
  Separate *Funded* from *Submitted/Pending*.
- **Include references** — the opposite of the resume rule.
- Education carries dissertation title + advisor.
- Order: Contact → Education → Appointments → Publications → Grants → Teaching →
  Service → Awards.
- Use `academic`. Do **not** use `--fit`.

### Consulting (MBB) `[CONVENTION]`

Hard **1 page**. Fixed skeleton: **Education → Work Experience → Leadership /
Extracurriculars → Personal Interests**. Firms explicitly convert PhD/MD/JD academic
CVs down to this. Education leads *regardless of seniority* — the one legitimate case
where that's true for an experienced candidate.

`[CONTESTED]` The micro-rules circulating online (exact bullet counts, mandated
phrasing, specific fonts) are vendor folklore with no primary backing. Encode only
what the firms actually say: 1 page, the four sections, quantified problem-solving,
evidence of academic performance and leadership.

### Investment banking `[CONVENTION]`

1 page, austere, `classic`, no colour. Education first with GPA and test scores if
strong. Deal/transaction experience with sizes. Deviating from the expected template
is itself a negative signal in this market.

### Software / data / ML `[CONVENTION]`

`modern`, 1 page under ~10 yrs. Link a real GitHub with **3–5 documented projects** —
an unmaintained profile link is worse than none. Skills grouped, not rated. For ML,
show the problem and the measured result, not a framework list.

### Product management `[CONVENTION]`

Shipped outcomes tied to recognizable business metrics, plus evidence of discovery
work. Not a feature list.

### Design / UX `[CONVENTION]`

**The portfolio is the artifact that gets you hired; the resume routes to it.** Link it
in the contact line. The resume itself should still be single-column and parse-clean —
a designer whose resume can't be parsed reads as a designer who doesn't consider
constraints. Restraint here is a portfolio piece.

### Marketing `[CONTESTED]`

No documented industry-specific convention beyond generic quantification. Treat as
general industry; the differentiator is the numbers.

### Sales `[CONVENTION]`

Quota attainment, explicitly: `142% of $2.4M quota, FY24`. Ranking if strong. This is
the one field where the numbers essentially *are* the resume.

### Medicine, law, government `[CONVENTION]`

`classic`, conservative, ink-only. Licences/bar admissions near the top with numbers
and jurisdictions. Structured application systems (ERAS) override everything here.

---

## 5. Applying a variant

```yaml
config:
  template: classic
  page: a4            # letter | a4  — A4 outside the US/Canada
  max_pages: 2
  stage: senior       # or academic — drives section order
  labels:             # localise headings if writing in another language
    experience: Berufserfahrung
```

Set `page: a4` for every non-US/Canada target. Letter (8.5×11in) and A4 (210×297mm)
differ enough that a Letter-composed page prints wrong in Europe — a small tell that
reads as carelessness.
