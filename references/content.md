# Content — writing the words

Design decides whether the content gets read. Content decides whether it works.
This is where resumes are actually won, and where most of the effort should go.

---

## 1. The bullet

### The formula `[ESTABLISHED]`

Google's X-Y-Z, from Laszlo Bock (*Work Rules!*, and his own hiring guidance):

> **Accomplished [X], as measured by [Y], by doing [Z].**

The order is the point. **Outcome first**, because the reader may not finish the
line. The mechanism (`by doing Z`) is the least interesting part and goes last —
it's what most people lead with.

```
✗  Was responsible for migrating our database to a new Postgres cluster.
       activity, no outcome, dead opener, no scale

~  Migrated our database to partitioned Postgres.
       outcome-shaped, but: how big? did it work? who cares?

✓  Migrated 240M ledger rows to partitioned Postgres with zero downtime and
   no reconciliation breaks, over 6 weeks.
       scale (240M) + result (zero downtime) + constraint (6 weeks)
```

### The "so what?" ladder

Ask *so what?* until it stops having an answer. The last answer is the bullet.

```
"I rewrote the checkout service."          so what?
"It got faster."                           so what?
"p99 went 840ms -> 190ms."                 so what?
"We stopped losing the enterprise deal."   <- THIS is the bullet.

✓  Cut p99 checkout latency 840ms -> 190ms by replacing a synchronous fan-out
   with a batched read path, unblocking a $12M/yr enterprise contract.
```

Most people stop at rung 1. Stopping at rung 4 is the whole job.

### Quantification `[CONVENTION]`

Reach for: scale (rows, users, req/s, $, headcount), change (%, before → after),
time (shipped in N weeks, sustained N years), risk (incidents, downtime).

**When you have no number** — and this is common and fine — use a *verifiable
qualitative fact* instead of inventing one:

```
✓  Still running unmodified four years later.
✓  Adopted by all six product teams without a mandate.
✓  The runbook I wrote is still what oncall uses.
```

> **Never invent a metric.** `build.py` warns on bullets with no digit — that is a
> prompt to think, not an instruction to fabricate. A made-up number is the one
> failure that cannot be recovered: it dies in the interview, with your credibility.

### Openers

Cut these. They describe a job description, not a person:

`responsible for` · `duties included` · `worked on` · `helped with` ·
`assisted with` · `tasked with` · `in charge of` · `participated in`

Lead with a verb that implies a result: *Cut, Shipped, Rebuilt, Migrated, Reduced,
Grew, Automated, Eliminated, Negotiated, Recovered, Consolidated, Unblocked.*

Avoid inflation you can't defend: you *led* it if you were accountable for the
outcome; otherwise you *built*, *drove*, or *contributed to*. Interviewers probe
exactly here.

### Clichés `[CONVENTION]`

Every one is a claim with no evidence. Show it or cut it:

`team player` · `results-driven` · `self-starter` · `go-getter` · `synergy` ·
`think outside the box` · `hard-working` · `detail-oriented` ·
`proven track record` · `dynamic professional` · `passionate about`

> "Detail-oriented" in a resume with an inconsistent date format is worse than
> saying nothing. Let the document be the evidence.

### Length

1–2 lines. 3 is the hard ceiling. A bullet that wraps to a 3rd line for one orphan
word must be reworded — never fixed by tightening tracking.

3–5 bullets for recent/relevant roles, 1–2 for older ones. **Relevance, not
symmetry.** A 2010 job does not deserve equal weight because it looks balanced.

---

## 2. The summary

**Default: omit it.** `[CONTESTED]`

Sources genuinely disagree. The test that resolves it: *does it say anything the
bullets cannot?* If it restates them, it is a tax on the most valuable space on the
page. Keep it only when it carries information that has nowhere else to live:

- a **career change** (why a nurse is applying to product management)
- an **unusual combination** (securities law + distributed systems)
- **seniority framing** a list of jobs won't convey
- a **relocation** or context the dates would otherwise make confusing

2–3 lines. No first person. Never an "Objective" — an objective states what *you*
want, on a document whose entire job is stating what you *offer*.

```
✗  Objective: Seeking a challenging position at a dynamic company where I can
   leverage my skills and grow professionally.
       says nothing; about you; three clichés

✓  Backend engineer, eight years on payments and order-matching under hard
   latency budgets. I like the unglamorous parts: correctness under partial
   failure, and systems observable enough to debug at 3am.
       specific, opinionated, unmistakably a person
```

---

## 3. Headline

The line under the name. Highest-leverage real estate on the page — it answers
"what is this?" before the reader decides whether to keep reading.

```
✗  Experienced Professional
✗  Software Engineer                    (true, but it's the whole job market)
✓  Senior Backend Engineer — Distributed Systems
✓  Product Manager — 0→1 Marketplaces
✓  RN, Critical Care — 8 yrs ICU
```

Match the target role's vocabulary when honestly true.

---

## 4. Hard situations

Handle plainly. Every one of these is common; none is disqualifying. Evasion reads
worse than the fact.

| Situation | Approach |
|---|---|
| **Employment gap** | See the note below — this one has real evidence behind it. Use years (`2019 – 2021`) not months where that is honestly accurate. For a long gap, name it in one neutral line: `Career break — caregiving, 2020–2022`. Recruiters see thousands; the evasion reads worse than the gap. |
| **Career change** | Lead with a summary (this is what it's *for*). Reframe past work in the target's vocabulary — real transferable outcomes, not invented ones. Consider putting a relevant project *above* unrelated experience. |
| **Short tenures** | Don't hide them. Group contract work under one heading: `Independent Consultant, 2019–2022` with clients as bullets. That's accurate and reads as intent, not churn. |
| **Promotions at one company** | One company block, roles nested beneath. Shows growth and saves space. Two separate blocks reads as two jobs. |
| **Laid off** | Nothing on the resume. It's not a resume topic. |
| **Overqualified / long career** | Cut to the last ~15 years. Older roles compress to one `Earlier: Title, Company; Title, Company` line. Dropping the 1998 dates is not dishonest — it's editing. |
| **No experience (student)** | Projects and coursework ARE evidence. A real project with a real outcome beats an empty `Experience` heading. Order: education → projects → any work at all. |
| **Contract/freelance** | Group under one banner with a date range; list notable clients/outcomes as bullets. |
| **Returning after a break** | Lead with a summary framing the return. List the break neutrally. Any recent upskilling goes near the top. |

### The gap rule is the one with real evidence behind it `[ESTABLISHED]`

Most advice in this table is convention. This one isn't, and it's worth knowing why
the date format matters more than it looks:

- **~48–50% of employers automatically screen out resumes showing an employment gap
  over six months** — over 90% use their system to filter or rank at all. Candidates
  *"fall out of the candidate pool, having never been assessed by a human being."*
  (Harvard Business School / Accenture, *Hidden Workers: Untapped Talent*, 2021 —
  n=8,720 workers, 2,275 executives, US/UK/DE.)
- Gaps **causally** reduce callbacks, and **most of the decline happens within the
  first 8 months**. (Kroft, Lange & Notowidigdo, *QJE* 128(3) 2013 — ~12,000 resumes
  sent to ~3,000 postings. Scope: mid/low-skill US roles, pre-2013.)

Two things follow, and the second is the important one:

1. **Year-only dates are legitimate** when accurate. `2019 – 2021` is not a lie
   because you left in March and started in November; it is a coarser truth. Do not
   use it to conceal a two-year gap — that fails at the interview.
2. **This is why parse fidelity matters.** A mis-parsed date creates a *phantom* gap
   in the structured record, and a real, documented filter fires on it — with no
   human and no fallback. That is the actual mechanism behind "the ATS rejected me",
   and it has nothing to do with your font. Run `ats_check.py` and confirm the dates
   extract correctly. (`../DESIGN.md` § 7.)

---

## 5. Skills

Grouped label → values. Never bars, dots, or star ratings (see `DESIGN.md` § 4).

```yaml
skills:
  - group: Languages
    items: [Go, Python, SQL]
  - group: Infrastructure
    items: [Postgres, Kafka, Kubernetes]
```

Rules:
- List what you'd be **comfortable being interviewed on**. This section is a
  promise, and interviewers read it as one.
- No `Microsoft Word`, `Email`, `Internet Research` — negative signal.
- Don't list every technology you've touched. A 40-item skills list says you can't
  prioritise, and dilutes the ones that matter.
- Group by how a **reader** thinks, not by your mental model.

---

## 6. Tailoring to a posting

1. Pull the posting's actual **vocabulary** — the nouns for the work.
2. Where the user's real experience matches under a different word, **use theirs**
   (they say "observability", the user wrote "monitoring", same work → theirs).
3. **Reorder** so the relevant evidence is in the first two bullets of the most
   recent role.
4. **Cut** what doesn't serve this application. Ruthlessly.
5. Never add a skill the user doesn't have.

Do this because **a human recruiter searches those words** — not because a robot
scores you (see `DESIGN.md` § 7). The action is the same; the honest reason
produces better judgement about how far to take it.
