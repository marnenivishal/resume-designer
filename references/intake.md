# Intake — what to ask

Ask what you need, then stop. An interrogation is not a service — most people give
up on a form before they finish it, and you can draft from far less than you think.

**Never invent a fact to fill a gap.** A missing number is a question; a fabricated
one is a lie the user discovers in an interview.

---

## Round 1 — the minimum to draft (ask together, once)

1. **Name**, and how to reach you: **email**, **phone**, **city + region**.
   *(Not a street address — see `variants.md`.)*
2. **Target role.** A title, or a link to a posting. This is the single most useful
   answer; everything downstream keys off it.
3. **Work history**: for each role — title, company, dates, and *what changed
   because you were there*.
4. **Education**: degree, institution, year.
5. Any **links** worth having: GitHub, portfolio, LinkedIn.

That is enough to build a real draft. Do it, show it, and iterate against something
concrete — people react far better to a draft than to a questionnaire.

## Round 2 — after they've seen a draft

Now the questions are specific and easy to answer, because there's a page to point at:

- "This bullet has no number. What was the scale — users, revenue, requests, headcount?"
- "You wrote *improved performance*. Improved from what, to what?"
- "What are you actually proud of here that isn't on this page?"
- "Which of these three roles matters most for the job you want?"

> The best material almost always arrives in round 2, in response to a draft. The
> question "what did you do?" gets a job description. The question "why is this
> bullet boring?" gets the truth.

---

## Context that changes the output

Ask only if not obvious from the above:

| Question | Why it matters |
|---|---|
| **Region** of the target job | photo/DOB/address rules, page cap, A4 vs Letter — several are legal-adjacent (`variants.md`) |
| **Industry** | consulting, finance, academia, US federal, design each have hard conventions |
| **Seniority** | drives section order and length |
| **Is this an academic CV?** | a different document class entirely, not a longer resume |
| **Any constraint?** | "must be one page", "they asked for DOCX" |

## Sensitive things — ask once, neutrally, and move on

If the dates imply one of these, ask plainly. Do not moralise, and do not pretend not
to have noticed:

- **A gap**: "There's a gap in 2020–21 — want to name it or use year-only dates?"
- **Short tenures**: "Were these contracts? Grouping them under one heading is
  accurate and reads better."
- **A career change**: "What's the thread you want the reader to see between these?"

All three are common and none is disqualifying (`content.md` § 4). Evasion reads
worse than the fact.

---

## Starting from an existing resume

Faster and more accurate than an interview — extract first, then ask round 2:

```bash
python scripts/extract.py old_resume.pdf -o resume.yaml
```

Then **read it back to the user** and let them correct it. Extraction from a PDF is
lossy by nature — that is the whole point of `DESIGN.md` § 2 — so verify rather than
assume. If their old resume had a sidebar, expect the extraction to be scrambled, and
say so: it's a live demonstration of why the new one won't have one.

## What not to ask

- Anything you can infer from a posting they linked.
- Their salary history. Never on a resume; illegal to ask in several US states.
- DOB, marital status, nationality, photo — unless the region genuinely expects it
  (`variants.md`), in which case say why you're asking.
- Which font they want. Offer a template; the type system is a considered whole, not
  a preference menu. If they have a real reason, honour it.
