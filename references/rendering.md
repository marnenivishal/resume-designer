# Rendering — PDF, print CSS, fonts

Everything here was measured on a real machine, not inferred from documentation.
Reproduce any of it with the scripts in `scripts/`.

---

## The pipeline

```
resume.yaml --(jinja2)--> HTML --(headless Chrome --print-to-pdf)--> PDF
```

Chrome is the renderer because it is the only engine that is (a) already installed
almost everywhere, (b) a genuinely good paged-media implementation, and (c) free.
WeasyPrint/wkhtmltopdf need installing; LaTeX is a different universe.

### Chrome invocation — three non-obvious requirements

```bash
chrome --headless=new --disable-gpu --no-pdf-header-footer \
       --user-data-dir=<UNIQUE TEMP DIR> \
       --print-to-pdf=<ABSOLUTE PATH> file:///<ABSOLUTE PATH>.html
```

1. **`--headless=new`.** Legacy `--headless` silently produces nothing on current
   builds — **exit code 0, no file**. Cost me a debugging cycle.
2. **`--print-to-pdf` must be an ABSOLUTE path.** A relative path also exits 0 and
   writes nothing.
3. **A unique `--user-data-dir` per invocation.** Sharing one makes concurrent or
   even *serial* runs block on the profile lock until they time out. This is the #1
   cause of "the build hangs".

Also: `--no-pdf-header-footer` removes Chrome's default URL/date furniture, which
otherwise prints on every page and looks like a mistake.

## Fonts

### Variable fonts degrade the PDF to Type3 `[MEASURED]`

The important one, and completely undocumented as far as I can tell:

| Font | PDF font subtype |
|---|---|
| `Segoe UI Variable Text` (VF) | **Type3** |
| `Sitka Text` (VF) | **Type3** |
| Segoe UI (static) | Type0 ✅ |
| Cambria, Calibri, Georgia | Type0 ✅ |

A **variable font makes Chrome emit `/Type3` fonts** — every glyph becomes a *drawing
procedure* (`/CharProcs`) instead of real embedded font text. Chrome must instantiate
a variation instance and apparently cannot reference a static embedded face.

Text still extracts, because Chrome writes a `ToUnicode` map — but extraction now
depends **entirely** on that map surviving. PDF/UA is explicit that embedding alone
does not make text extractable; it must also be Unicode-mapped. Real `/Type0` +
`FontFile2` needs no such luck.

So `tokens.css` names **no variable font**, and `Inter` is deliberately absent (it
usually ships as `InterVariable`). `ats_check.py` warns if a Type3 font appears.

> This bit me in my own tokens: the first `modern` stack led with
> `Segoe UI Variable Text` and silently produced Type3. Nothing errored. The only
> reason I caught it was reading the PDF back.

### Silent fallback `[MEASURED]`

`Inter`, `Lato`, `Source Serif`, `Charter`, `Garamond` were **not installed** on the
dev machine. CSS naming them renders a fallback **with no error**. Never trust the
stack — `ats_check.py` reads the fonts *actually embedded* and warns when the
requested family is missing.

### Figures `[MEASURED]`

Georgia, Corbel, Candara, Constantia, Sitka default to **old-style figures** (digits
that vary in height and descend below the baseline — Georgia's fall to −0.18em). On
a page full of dates this reads as uneven.

All of them expose `lnum`/`tnum`, and **Chrome applies them** — verified by digit
advance widths collapsing from 9 distinct to 2 under
`font-variant-numeric: lining-nums tabular-nums`. That line is in `tokens.css`
globally. `tnum` is why right-aligned dates align exactly.

Cambria leads the serif stack because it is lining + tabular **natively** (one
distinct digit width), depending on no feature support at all.

## Print CSS that actually works in Chrome

| Property | Works? |
|---|---|
| `@page { size: Letter/A4; margin: … }` | ✅ |
| `break-inside: avoid-page` / `page-break-inside` | ✅ |
| `break-after: avoid` on headings | ✅ |
| `orphans` / `widows` | ✅ (block text) |
| `print-color-adjust: exact` | ✅ — required, or backgrounds/rules drop |
| `@page { @bottom-center { content: counter(page) } }` | ⚠️ margin boxes are patchy; verify before relying |
| `position: fixed` repeating headers | ❌ |

## Debugging

```bash
# what a parser actually sees
python scripts/ats_check.py Resume.pdf --show-text

# is anything side-by-side that shouldn't be
python scripts/ats_check.py Resume.pdf --data resume.yaml

# inspect the HTML before Chrome touches it
python scripts/build.py resume.yaml --format html
```

**Page count is authoritative from the PDF, not the DOM.** Measuring
`document.body.scrollHeight` in a browser approximates the printed page and will
disagree with Chrome's own pagination. Count `pypdf` pages instead.

## Why not DOCX as the primary format

DOCX is generated (`python-docx`) but is deliberately **plainer** than the PDF: real
Word heading styles, no fine typography. It exists for the two cases that need it — a
posting that demands `.docx`, or a recruiter who wants to edit — and it is honest
about not being the designed artifact. PDF preserves the design and is read fine by
every mainstream ATS; that myth is addressed in `../DESIGN.md` § 7.
