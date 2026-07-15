#!/usr/bin/env python3
"""Round-trip verification: read a finished resume PDF back the way a parser does.

Most "ATS checkers" score keywords against a job description and guess. This does
something narrower and actually verifiable: it re-extracts the PDF you just built
and proves the machine-readable layer is intact.

    python ats_check.py Resume.pdf --data resume.yaml

Checks
    text-layer      the PDF has real selectable text, not a picture of text
    fonts           fonts are embedded+subset, and no silent fallback happened
    order           sections extract in the order you wrote them
    bleed           no two unrelated blocks merged onto one extracted line
    contact         email / phone / links survive extraction
    headings        section headings are findable as text
    pages           page count matches intent

Why "bleed" matters (measured, not folklore): PDF has no DOM. Chrome emits text in
visual position order, so ANY two blocks sitting side by side at the same height get
interleaved into a single extracted line -- a job title welded to a skills list.
Fixing the DOM order does not fix it, because the DOM is gone by print time.
Same-line pairs that BELONG together (role left, dates right) merge harmlessly.

Exit codes: 0 = clean, 1 = warnings (with --strict), 2 = failures.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    sys.exit("error: missing dependency. Install with: pip install pdfplumber")
try:
    import pypdf
except ImportError:
    sys.exit("error: missing dependency. Install with: pip install pypdf")

RESET, RED, YEL, GRN, DIM = "\033[0m", "\033[31m", "\033[33m", "\033[32m", "\033[2m"
if not sys.stdout.isatty():
    RESET = RED = YEL = GRN = DIM = ""

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
PHONE_RE = re.compile(r"(\+?\d{1,3}[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}")
URL_RE = re.compile(r"(https?://|www\.)[\w./#?=-]+|\b[\w-]+\.(com|io|dev|org|net|me|ai)/[\w./#?=-]+")


class Report:
    def __init__(self) -> None:
        self.rows: list[tuple[str, str, str]] = []

    def add(self, level: str, check: str, msg: str) -> None:
        self.rows.append((level, check, msg))

    ok = lambda self, c, m: self.add("ok", c, m)
    warn = lambda self, c, m: self.add("warn", c, m)
    fail = lambda self, c, m: self.add("fail", c, m)

    def render(self) -> int:
        icons = {"ok": (GRN, "PASS"), "warn": (YEL, "WARN"), "fail": (RED, "FAIL")}
        for lvl, check, msg in self.rows:
            col, label = icons[lvl]
            print(f"  {col}{label:4s}{RESET}  {check:11s}  {msg}")
        n_fail = sum(1 for r in self.rows if r[0] == "fail")
        n_warn = sum(1 for r in self.rows if r[0] == "warn")
        print()
        if n_fail:
            print(f"{RED}{n_fail} failure(s){RESET}, {n_warn} warning(s)")
        elif n_warn:
            print(f"{YEL}{n_warn} warning(s){RESET} — readable, but review them")
        else:
            print(f"{GRN}clean — the text layer survives extraction intact{RESET}")
        return 2 if n_fail else (1 if n_warn else 0)


def load_expected(path: Path | None) -> dict | None:
    if not path:
        return None
    try:
        import yaml
    except ImportError:
        return None
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


# --------------------------------------------------------------------- checks

def check_text_layer(pdf_path: Path, rep: Report) -> str:
    """Distinguish 'no text layer' (a scan) from 'not much text' (a short resume).

    These are different failures and were conflated at first: a genuinely minimal
    resume -- a name and an email -- is short but perfectly machine-readable, and
    flagging it as a scan is noise that trains people to ignore the checker.
    A scan has ~no text AND a big image; a sparse resume has text and no image.
    """
    with pdfplumber.open(pdf_path) as pdf:
        pages = [(p.extract_text() or "") for p in pdf.pages]
        n_images = sum(len(p.images) for p in pdf.pages)
    text = "\n".join(pages)
    chars = len(text.strip())

    if chars < 20:
        rep.fail("text-layer", f"only {chars} chars extracted — there is effectively no text "
                               f"layer. A parser sees nothing.")
    elif n_images and chars < 200:
        rep.fail("text-layer", f"{chars} chars of text beside {n_images} image(s) — this looks "
                               f"like a scan. Text inside an image is invisible to a parser.")
    elif chars < 350:
        rep.warn("text-layer", f"only {chars} chars — the text layer is fine, but there is very "
                               f"little on the page. Thin content, not a technical problem.")
    else:
        rep.ok("text-layer", f"{chars:,} chars extract cleanly across {len(pages)} page(s)")

    if n_images:
        rep.warn("text-layer", f"{n_images} embedded image(s) — any text inside them is invisible "
                               f"to a parser")
    return text


def check_fonts(pdf_path: Path, rep: Report, intended: list[str] | None = None) -> None:
    reader = pypdf.PdfReader(str(pdf_path))
    seen: dict[str, bool] = {}
    type3 = 0
    for page in reader.pages:
        fonts = (page.get("/Resources") or {}).get("/Font") or {}
        for key in fonts:
            f = fonts[key].get_object()
            subtype = str(f.get("/Subtype", ""))
            descs = []
            if subtype == "/Type0":
                for df in f.get("/DescendantFonts") or []:
                    descs.append(df.get_object().get("/FontDescriptor"))
            else:
                descs.append(f.get("/FontDescriptor"))

            # A Type3 font has no BaseFont: its glyphs are drawing procedures, not
            # font data. Recover the real family name from the FontDescriptor.
            base = f.get("/BaseFont")
            if not base:
                for d in descs:
                    if d and d.get_object().get("/FontName"):
                        base = d.get_object()["/FontName"]
                        break
            base = str(base or "unnamed").lstrip("/")

            if subtype == "/Type3":
                type3 += 1
                # Type3 carries no FontFile by definition; the glyph procedures ARE
                # the embedded data, so it is self-contained but not real text.
                seen[base] = seen.get(base, True)
                continue

            emb = any(d and any(k in d.get_object() for k in ("/FontFile", "/FontFile2", "/FontFile3"))
                      for d in descs)
            seen[base] = seen.get(base, False) or emb

    if not seen:
        rep.warn("fonts", "no font resources found")
        return

    if type3:
        rep.warn("fonts", f"{type3} Type3 (vector-outline) font(s) — glyphs are drawn as "
                          f"procedures, not text. Extraction then depends entirely on the "
                          f"ToUnicode map. Prefer real embedded fonts; see DESIGN.md > Type3.")
    missing = [n for n, e in seen.items() if not e]
    if missing:
        rep.fail("fonts", f"NOT embedded: {', '.join(missing)} — will reflow on another machine")
    else:
        kind = "self-contained" if type3 else "embedded/subset"
        rep.ok("fonts", f"all {kind}: {', '.join(sorted(seen)[:6])}")

    # Silent fallback is the quiet killer: CSS asks for a font that isn't installed,
    # the browser substitutes without error, and the design silently degrades.
    if intended:
        got = " ".join(seen).lower()
        for want in intended:
            stem = re.split(r"[,\s]", want.strip().strip("'\""))[0].lower().replace(" ", "")
            if stem and stem not in ("serif", "sans-serif", "monospace") and stem not in got.replace(" ", ""):
                rep.warn("fonts", f"'{want}' was requested but is absent from the PDF — "
                                  f"the browser silently substituted. Install it or pick another.")


def big_gap_lines(pdf_path: Path, min_gap_pt: float = 28.0) -> list[tuple[int, str, str, float]]:
    """Find extracted lines containing a large horizontal blank gap.

    A big internal gap means two independent blocks landed on the same visual line.
    Returns (page_no, left_text, right_text, gap_width).
    """
    out = []
    with pdfplumber.open(pdf_path) as pdf:
        for pno, page in enumerate(pdf.pages, 1):
            words = page.extract_words(use_text_flow=False, keep_blank_chars=False)
            lines: dict[float, list[dict]] = {}
            for w in words:
                key = round(w["top"] / 3.0) * 3.0  # bucket by baseline (~3pt tolerance)
                lines.setdefault(key, []).append(w)
            for top, ws in sorted(lines.items()):
                ws.sort(key=lambda w: w["x0"])
                for i in range(len(ws) - 1):
                    gap = ws[i + 1]["x0"] - ws[i]["x1"]
                    if gap >= min_gap_pt:
                        left = " ".join(w["text"] for w in ws[: i + 1])
                        right = " ".join(w["text"] for w in ws[i + 1:])
                        out.append((pno, left, right, gap))
                        break
    return out


def check_bleed(pdf_path: Path, rep: Report, data: dict | None) -> None:
    """Flag side-by-side text that merges into a FALSE line.

    Measured behaviour: PDF text extraction merges anything sitting side by side at
    the same height into one line, and DOM order cannot prevent it (PDF has no DOM).
    So the question is never "is there a gap" -- it is "is the merged line still
    true?". Two cases are true by construction and must not be flagged:
        role   | its own dates    -> "Senior Engineer, Acme  Mar 2021 - Present"
        label  | its own values   -> "Languages  Go, Python, SQL"
    Anything else (a skills column beside an experience column) merges two unrelated
    records into a sentence that was never written, and IS a defect.
    """
    gaps = big_gap_lines(pdf_path)
    if not gaps:
        rep.ok("bleed", "no side-by-side text blocks — extraction order is unambiguous")
        return

    # Metadata reads "Mar 2021 - Present" or "Seattle, WA · Mar 2021 - Present", so
    # the date may not be at the start. Match anywhere, but keep the length bound:
    # a short right-hand run carrying a year is metadata; a long one is a column.
    date_like = re.compile(
        r"((19|20)\d{2}|present|current)", re.I)

    # Labels the author actually authored as label/value pairs. Anything matching is
    # a sanctioned pair, not a bleed.
    labels = set()
    for g in ((data or {}).get("skills") or []):
        if isinstance(g, dict) and g.get("group"):
            labels.add(str(g["group"]).strip().lower())

    # Links the author attached to a record (project URL, portfolio) are that
    # record's own metadata, exactly like its dates.
    link_like = re.compile(r"^(https?://|www\.)|^[\w-]+\.(com|io|dev|org|net|me|ai|co|gg)(/|$)", re.I)

    suspicious = []
    for pno, left, right, gap in gaps:
        l, r = left.strip(), right.strip()
        benign = False
        if len(r) < 46 and date_like.search(r):
            benign = True                                  # record | its dates
        elif len(r) < 60 and link_like.search(r):
            benign = True                                  # record | its link
        elif l.lower().rstrip(":") in labels:
            benign = True                                  # label  | its values
        if not benign:
            suspicious.append((pno, l, r, gap))

    if not suspicious:
        rep.ok("bleed", f"{len(gaps)} same-line pair(s), all record/metadata — merge harmlessly")
        return
    rep.fail("bleed", f"{len(suspicious)} line(s) merge unrelated blocks — a parser reads each of "
                      f"these as ONE line:")
    for pno, left, right, gap in suspicious[:4]:
        rep.add("fail", "", f"{DIM}p{pno}: “{left[:32]}” + {gap:.0f}pt gap + “{right[:32]}”{RESET}")


def expected_section_order(data: dict) -> list[str]:
    """Ask build.py what order it renders sections in, rather than assuming.

    Section order is career-stage dependent -- a new grad and an academic render
    education BEFORE experience. Hardcoding experience-then-education here made the
    checker report inversions on documents that were correct by design. The two
    scripts must agree, so derive it from the one source of truth.
    """
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from build import section_order  # noqa: PLC0415
        return section_order(data)
    except Exception:
        return ["experience", "projects", "education", "skills"]


def check_order(text: str, rep: Report, data: dict | None) -> None:
    if not data:
        rep.warn("order", "pass --data resume.yaml to verify extraction order")
        return
    flat = re.sub(r"\s+", " ", text)
    anchors: list[tuple[str, str]] = []
    name = (data.get("basics") or {}).get("name")
    if name:
        anchors.append(("name", name))
    for sec in expected_section_order(data):
        if sec == "experience":
            for job in (data.get("experience") or [])[:6]:
                if job.get("company"):
                    anchors.append(("experience", str(job["company"])))
        elif sec == "education":
            for e in (data.get("education") or [])[:3]:
                v = e.get("institution") or e.get("degree")
                if v:
                    anchors.append(("education", str(v)))

    found, missing = [], []
    for kind, a in anchors:
        i = flat.lower().find(str(a).lower()[:36])
        (found if i >= 0 else missing).append((kind, a, i))
    if missing:
        rep.fail("order", f"not extractable: {', '.join(a for _, a, _ in missing)}")
    inversions = [
        (found[i][1], found[i + 1][1])
        for i in range(len(found) - 1) if found[i][2] > found[i + 1][2]
    ]
    if inversions:
        rep.fail("order", f"{len(inversions)} inversion(s) — extracted out of written order: "
                          + "; ".join(f"“{a}” after “{b}”" for a, b in inversions[:3]))
    elif found:
        rep.ok("order", f"{len(found)} anchors extract in written order")


def check_contact(text: str, rep: Report, data: dict | None) -> None:
    flat = re.sub(r"[ \t]+", " ", text)
    email, phone = EMAIL_RE.search(flat), PHONE_RE.search(flat)
    if email:
        rep.ok("contact", f"email parses: {email.group(0)}")
    else:
        want = (data or {}).get("basics", {}).get("email")
        (rep.fail if want else rep.warn)("contact",
            "no email found by regex — the single most important field for a parser")
    if phone:
        rep.ok("contact", f"phone parses: {phone.group(0).strip()}")
    elif (data or {}).get("basics", {}).get("phone"):
        rep.warn("contact", "phone present in source but not regex-matchable after extraction")
    if data:
        for link in ((data.get("basics") or {}).get("links") or []):
            lbl = str(link.get("label") or link.get("url") or "")
            stem = re.sub(r"^(https?://)?(www\.)?", "", lbl).split("/")[0]
            if stem and stem.lower() not in flat.lower():
                rep.warn("contact", f"link '{lbl}' not found in extracted text")


def check_headings(text: str, rep: Report, data: dict | None) -> None:
    up = text.upper()
    standard = ["EXPERIENCE", "EDUCATION", "SKILLS", "PROJECTS", "SUMMARY",
                "CERTIFICATIONS", "PUBLICATIONS", "AWARDS", "EMPLOYMENT",
                "APPOINTMENTS", "RESEARCH", "TEACHING", "GRANTS"]
    present = [h for h in standard if h in up]
    if not present:
        # No headings because there are no sections is a content problem, not a
        # rendering defect. Only a real failure if the data HAS sections that did
        # not survive into the text.
        has_sections = bool(data and any(data.get(k) for k in
                            ("experience", "education", "skills", "projects")))
        if has_sections:
            rep.fail("headings", "the source has sections but no standard heading survived "
                                 "extraction — parsers key off these")
        else:
            rep.warn("headings", "no section headings — the resume has no sections at all. "
                                 "That is a content gap, not a parsing one.")
        return
    rep.ok("headings", f"standard headings found: {', '.join(present)}")
    if data:
        for job in (data.get("experience") or []):
            if job.get("company") and "EXPERIENCE" not in up and "EMPLOYMENT" not in up:
                rep.warn("headings", "experience entries exist but no EXPERIENCE heading")
                break


def check_pages(pdf_path: Path, rep: Report, data: dict | None) -> None:
    n = len(pypdf.PdfReader(str(pdf_path)).pages)
    want = ((data or {}).get("config") or {}).get("max_pages")
    if want and n > int(want):
        rep.fail("pages", f"{n} pages, but config.max_pages={want}")
    elif n > 2:
        rep.warn("pages", f"{n} pages — justify anything past 2 outside academia/federal")
    else:
        rep.ok("pages", f"{n} page(s)")


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify a resume PDF survives machine extraction.")
    ap.add_argument("pdf")
    ap.add_argument("--data", help="resume.yaml — enables order/contact/page verification")
    ap.add_argument("--strict", action="store_true", help="exit non-zero on warnings too")
    ap.add_argument("--show-text", action="store_true", help="dump exactly what a parser sees")
    a = ap.parse_args()

    pdf_path = Path(a.pdf).resolve()
    if not pdf_path.exists():
        sys.exit(f"error: no such file: {pdf_path}")
    data = load_expected(Path(a.data).resolve() if a.data else None)

    print(f"\n  {DIM}parse-back check{RESET}  {pdf_path.name}\n")
    rep = Report()
    text = check_text_layer(pdf_path, rep)
    intended = None
    if data:
        fam = (data.get("config") or {}).get("font_family")
        intended = [fam] if isinstance(fam, str) else fam
    check_fonts(pdf_path, rep, intended)
    check_order(text, rep, data)
    check_bleed(pdf_path, rep, data)
    check_contact(text, rep, data)
    check_headings(text, rep, data)
    check_pages(pdf_path, rep, data)
    code = rep.render()

    if a.show_text:
        print(f"\n{DIM}{'-'*66}\nexactly what a naive parser sees:\n{'-'*66}{RESET}")
        print(text)
    if code == 1 and not a.strict:
        return 0
    return code


if __name__ == "__main__":
    sys.exit(main())
