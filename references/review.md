# Review — the quality bar

Run this before delivering. Be adversarial: you are looking for reasons the document
fails, not confirmation that it's fine. A review that passes everything on the first
pass is a review that wasn't performed.

Work in this order — content first. **A beautifully typeset page of weak claims is
still a weak resume**, and no amount of tracking fixes it.

---

## 1. The 10-second test

Cover everything below the top third. Answer, out loud:

1. Who is this person?
2. What are they good at?
3. What level are they?

If any answer needs the lower two-thirds, the masthead + summary have failed. Fix
the headline first — it is the cheapest, highest-leverage line on the page.

## 2. Content

- [ ] Does **every** bullet lead with an outcome, not an activity?
      *"Migrated 240M rows with zero downtime"* — not *"Was involved in migration work."*
- [ ] Is every number **real**? If you cannot source it to something the user told
      you, cut it. Inventing metrics is the one unrecoverable failure.
- [ ] Any bullet that survives the "so what?" test three times? If *so what* still
      has an answer, that answer belongs in the bullet.
- [ ] Zero instances of: `responsible for`, `duties included`, `worked on`,
      `helped with`, `team player`, `results-driven`, `detail-oriented`,
      `passionate about`, `proven track record`.
- [ ] Does the summary say anything the bullets don't? If not, **delete it** — it is
      occupying the most valuable space on the page.
- [ ] Is the most relevant evidence for *this* role in the **first two bullets** of
      the most recent job? That is where attention actually goes.
- [ ] Consistent tense: present for the current role, past for everything else.
- [ ] No first-person pronouns. Implied `I`, never written.
- [ ] Are older/less relevant roles compressed to 1–2 bullets? Symmetry is not a
      goal; relevance is.

## 3. Structure

- [ ] Reverse-chronological within each section.
- [ ] Section order matches career stage — evidence first. Education above
      experience **only** for students/new grads and academic CVs.
- [ ] Standard headings. `Experience`, not `My Journey`.
- [ ] Dates complete and consistently formatted. Unexplained gaps > 6 months either
      addressed or made irrelevant by the framing.
- [ ] Every section earns its space. A `Skills` section listing `Microsoft Word`
      is negative signal.

## 4. Typography and layout

- [ ] Vertical rhythm consistent — every gap a multiple of the 3pt scale.
- [ ] No stranded heading at the foot of a page.
- [ ] No job entry split across a page break.
- [ ] No single-word last line (a bullet wrapping to one orphan word). Tighten the
      wording — do not tighten the tracking.
- [ ] Dates align exactly down the right edge. If they don't, tabular figures aren't
      applying — see `rendering.md`.
- [ ] Page 2 (if any) is at least ~1/3 full. A two-page resume with three lines on
      page 2 should be a one-page resume.
- [ ] Nothing clipped at the margins; no text overflow.
- [ ] Three weights maximum, two families maximum.

## 5. Machine readability

Run it. Do not eyeball it:

```bash
python scripts/ats_check.py Resume.pdf --data resume.yaml
```

- [ ] `bleed` passes — no fabricated merged lines.
- [ ] `order` passes — sections extract in written order.
- [ ] `contact` passes — email and phone survive extraction.
- [ ] `fonts` passes — really embedded, and the intended family was actually used.
- [ ] `pages` matches intent.

Then read what a parser actually sees:

```bash
python scripts/ats_check.py Resume.pdf --show-text
```

Read that output as prose. If a line reads as nonsense, a human reading the
extracted version — which happens more often than people think — sees the same
nonsense.

## 6. The credibility test

Put it beside a resume from a paid service. Ask honestly:

- [ ] Does this look **considered**, or **decorated**? Decoration reads as
      compensating for thin content.
- [ ] Would this look right printed in greyscale? (It often is.)
- [ ] Is there anything on the page whose only job is to look like design? Delete it.
- [ ] Does the accent colour appear **≤ 3 times**?
- [ ] If you removed every rule, colour, and font choice — would the content still
      win? If no, go back to §2. Design cannot rescue it.

## 7. Regional and legal

- [ ] No photo, DOB, marital status, or nationality for US/UK/CA/AU targets.
- [ ] No street address anywhere. City + region only.
- [ ] No `References available upon request`.
- [ ] For non-generic targets (EU, academia, US federal, IB), the conventions in
      `variants.md` were actually applied — several are hard requirements, not
      preferences.

---

## Reporting to the user

State what you verified and what you did not. If `ats_check` produced warnings,
show them — don't bury them. If content is thin because the user gave you thin
material, say so plainly and ask the specific question that would fix it:

> "Your Globex bullets have no numbers. What changed because you were there —
> traffic handled, cost, time saved, incidents avoided? One real figure there is
> worth more than the rest of this page."

Never claim "ATS-optimized" as a finished state. Say what is true: *the text layer
extracts cleanly, in order, with contact details intact* — and show the check output
that proves it.
