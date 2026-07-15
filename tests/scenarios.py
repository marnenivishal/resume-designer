#!/usr/bin/env python3
"""Scenario matrix: build many diverse resumes and verify every one.

    python tests/scenarios.py                 # full matrix
    python tests/scenarios.py --limit 12      # smoke subset
    python tests/scenarios.py --jobs 4        # parallelism (Chrome is the bottleneck)

Each scenario is built to PDF and then re-extracted and checked. A scenario passes
only if the text layer survives: correct order, no fabricated merged lines, fonts
really embedded, contact parseable, page count within intent.

The point is not "does it crash". The point is that the parse-safety property holds
across every shape of real human career -- no experience, 25 years of it, gaps,
publications, one name, non-Latin names, absurdly long titles.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import io
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
BUILD = SKILL / "scripts" / "build.py"
CHECK = SKILL / "scripts" / "ats_check.py"

# ---------------------------------------------------------------- content atoms

def job(role, company, start, end, bullets, location="Seattle, WA"):
    return {"role": role, "company": company, "start": start, "end": end,
            "location": location, "bullets": bullets}

B_ENG = [
    "Cut p99 checkout latency from 840ms to 190ms by replacing a synchronous fan-out with a batched read path.",
    "Migrated 240M ledger rows to partitioned Postgres with zero downtime over 6 weeks.",
    "Designed the idempotency layer that took duplicate-charge incidents from 4/quarter to 0.",
]
B_MGR = [
    "Grew the platform team from 4 to 14 engineers across two time zones; regretted attrition under 5%.",
    "Cut deploy lead time from 9 days to 4 hours by funding CI work the roadmap kept deferring.",
    "Ran the incident review process; repeat-cause incidents fell 60% in a year.",
]
B_SALES = [
    "Closed 142% of a $2.4M quota in FY24; ranked 3rd of 61 reps.",
    "Built the enterprise pipeline in EMEA from $0 to $8.1M in 18 months.",
    "Cut average sales cycle from 94 to 61 days by qualifying earlier.",
]
B_NURSE = [
    "Managed a 6-bed ICU assignment on night rotation; zero medication errors across 3 years.",
    "Precepted 11 new graduate nurses; 9 still on unit after two years.",
    "Led the sepsis-bundle compliance push that moved the unit from 71% to 96%.",
]
B_DESIGN = [
    "Redesigned onboarding; activation rose from 31% to 48% over two quarters.",
    "Built and maintained the 120-component design system used by all 6 product teams.",
    "Ran 40+ moderated usability sessions; findings killed a feature before it shipped.",
]
B_TEACH = [
    "Taught 5 sections of AP Biology (140 students); pass rate rose from 62% to 88% in three years.",
    "Wrote the district's lab-safety curriculum, since adopted by 11 schools.",
]
B_ACCT = [
    "Closed month-end in 4 days, down from 11, by automating the reconciliation workbook.",
    "Found and recovered $340k of duplicate vendor payments across FY22-23.",
]
B_JUNIOR = [
    "Built a Flask app that tracks intramural standings; 300 weekly users on campus.",
    "Automated the lab's data intake, saving roughly 6 hours a week of manual entry.",
]

EDU_BS = {"degree": "B.S. Computer Science", "institution": "University of Washington",
          "location": "Seattle, WA", "start": 2014, "end": 2018}
EDU_PHD = {"degree": "Ph.D. Molecular Biology", "institution": "Stanford University",
           "location": "Stanford, CA", "start": 2015, "end": 2021,
           "summary": "Dissertation: Chromatin remodeling in early development. Advisor: Prof. A. Rivera."}
EDU_MBA = {"degree": "M.B.A.", "institution": "Northwestern (Kellogg)",
           "location": "Evanston, IL", "start": 2016, "end": 2018}
EDU_HS = {"degree": "High School Diploma", "institution": "Lincoln High School",
          "location": "Portland, OR", "start": 2019, "end": 2023}

SK_ENG = [{"group": "Languages", "items": ["Go", "Python", "SQL", "TypeScript"]},
          {"group": "Infrastructure", "items": ["Postgres", "Kafka", "Kubernetes", "AWS"]}]
SK_DESIGN = [{"group": "Design", "items": ["Figma", "Prototyping", "Design systems"]},
             {"group": "Research", "items": ["Usability testing", "Interviewing"]}]
SK_CLIN = [{"group": "Clinical", "items": ["ACLS", "Ventilator management", "Triage"]}]

PUBS = [
    {"citation": "Rivera A., Chen L. Chromatin remodeling in early development.",
     "venue": "Cell", "year": 2021},
    {"citation": "Chen L., et al. A method for single-cell lineage tracing.",
     "venue": "Nature Methods", "year": 2020},
]


def R(name, headline, **kw):
    d = {
        "config": {"template": "modern", "page": "letter", "density": "normal",
                   "max_pages": 1, "accent": "#1F4E5F"},
        "basics": {"name": name, "headline": headline, "email": "candidate@example.com",
                   "phone": "(206) 555-0142", "location": "Seattle, WA",
                   "links": [{"label": "linkedin.com/in/candidate",
                              "url": "https://linkedin.com/in/candidate"}]},
    }
    cfg = kw.pop("config", {})
    d["config"].update(cfg)
    d.update(kw)
    return d


# ---------------------------------------------------------------- the matrix

def matrix() -> list[tuple[str, dict]]:
    S: list[tuple[str, dict]] = []
    add = lambda n, d: S.append((n, d))

    # --- career stages -------------------------------------------------------
    add("student-no-experience", R("Priya Raman", "Computer Science Student",
        education=[EDU_BS], projects=[{"name": "IntraTrack", "summary": "Intramural standings app.",
        "link": "github.com/priya/intratrack", "bullets": B_JUNIOR}], skills=SK_ENG))
    add("highschool-first-job", R("Danny Ortiz", "Seeking Part-Time Retail",
        education=[EDU_HS], skills=[{"group": "Skills", "items": ["POS systems", "Customer service"]}]))
    add("new-grad", R("Priya Raman", "Software Engineer",
        education=[EDU_BS], experience=[job("SWE Intern", "Globex", "2023-06", "2023-09", B_JUNIOR)],
        projects=[{"name": "IntraTrack", "summary": "Standings app.", "bullets": B_JUNIOR[:1]}],
        skills=SK_ENG))
    add("mid-engineer", R("Maya Ellison", "Backend Engineer",
        experience=[job("Engineer", "Northwind", "2021-03", "present", B_ENG),
                    job("Engineer", "Globex", "2018-06", "2021-03", B_ENG[:2], "Portland, OR")],
        education=[EDU_BS], skills=SK_ENG))
    add("senior-engineer", R("Maya Ellison", "Senior Backend Engineer — Distributed Systems",
        summary="Backend engineer with eight years on payments under hard latency budgets.",
        experience=[job("Senior Engineer", "Northwind", "2021-03", "present", B_ENG),
                    job("Engineer", "Globex", "2018-06", "2021-03", B_ENG[:2], "Portland, OR")],
        education=[EDU_BS], skills=SK_ENG,
        certifications=[{"name": "AWS Solutions Architect — Professional",
                         "issuer": "Amazon Web Services", "date": 2023}]))
    add("staff-engineer", R("Maya Ellison", "Staff Engineer",
        experience=[job("Staff Engineer", "Northwind", "2021-03", "present", B_ENG),
                    job("Senior Engineer", "Globex", "2017-06", "2021-03", B_ENG),
                    job("Engineer", "Initech", "2014-01", "2017-06", B_ENG[:2])],
        education=[EDU_BS], skills=SK_ENG, config={"max_pages": 2}))
    add("engineering-manager", R("Dana Whitfield", "Engineering Manager",
        experience=[job("Engineering Manager", "Northwind", "2020-01", "present", B_MGR),
                    job("Senior Engineer", "Globex", "2016-06", "2020-01", B_ENG[:2])],
        education=[EDU_BS], skills=SK_ENG))
    add("executive-cto", R("Dana Whitfield", "Chief Technology Officer",
        summary="Technology executive; scaled two engineering orgs through hypergrowth and one through a downturn.",
        experience=[job("CTO", "Northwind", "2019-01", "present", B_MGR),
                    job("VP Engineering", "Globex", "2014-06", "2019-01", B_MGR[:2]),
                    job("Director of Engineering", "Initech", "2010-01", "2014-06", B_MGR[:2])],
        education=[EDU_MBA, EDU_BS], config={"template": "classic", "max_pages": 2},
        awards=[{"name": "CTO of the Year", "issuer": "GeekWire", "year": 2022}]))
    add("career-changer", R("Sam Okoye", "Product Manager — formerly Critical Care RN",
        summary="Eight years in critical care, now building clinical software. I know what breaks at 3am because I was there.",
        experience=[job("Associate PM", "MedFlow", "2023-01", "present", B_DESIGN[:2]),
                    job("ICU Registered Nurse", "Harborview", "2015-06", "2022-12", B_NURSE)],
        education=[EDU_BS], skills=SK_CLIN))
    add("veteran-transition", R("Marcus Reed", "Operations Manager",
        summary="Twelve years leading logistics operations in the US Army; now applying it in private-sector supply chain.",
        experience=[job("Logistics NCO", "US Army", "2012-06", "2024-03", B_MGR[:2], "Fort Lewis, WA")],
        education=[EDU_BS], skills=[{"group": "Operations", "items": ["Supply chain", "Fleet"]}]))
    add("returning-after-break", R("Alice Nakamura", "Software Engineer",
        summary="Returning to engineering after three years of full-time caregiving.",
        experience=[job("Engineer", "Globex", "2015-06", "2021-03", B_ENG[:2])],
        education=[EDU_BS], skills=SK_ENG,
        custom_sections=[{"title": "Career Break", "items": ["Full-time caregiving, 2021–2024."]}]))

    # --- roles across industries --------------------------------------------
    roles = [
        ("data-scientist", "Data Scientist", B_ENG, SK_ENG),
        ("ml-engineer", "Machine Learning Engineer", B_ENG, SK_ENG),
        ("devops-engineer", "DevOps Engineer", B_ENG, SK_ENG),
        ("security-engineer", "Security Engineer", B_ENG, SK_ENG),
        ("qa-engineer", "QA Engineer", B_ENG, SK_ENG),
        ("mobile-engineer", "iOS Engineer", B_ENG, SK_ENG),
        ("product-manager", "Product Manager", B_DESIGN, SK_DESIGN),
        ("program-manager", "Technical Program Manager", B_MGR, SK_ENG),
        ("ux-designer", "UX Designer", B_DESIGN, SK_DESIGN),
        ("graphic-designer", "Graphic Designer", B_DESIGN, SK_DESIGN),
        ("sales-executive", "Enterprise Account Executive", B_SALES, None),
        ("marketing-manager", "Marketing Manager", B_DESIGN, None),
        ("recruiter", "Technical Recruiter", B_MGR, None),
        ("hr-manager", "HR Manager", B_MGR, None),
        ("accountant", "Senior Accountant", B_ACCT, None),
        ("financial-analyst", "Financial Analyst", B_ACCT, None),
        ("business-analyst", "Business Analyst", B_ACCT, None),
        ("operations-manager", "Operations Manager", B_MGR, None),
        ("supply-chain", "Supply Chain Manager", B_MGR, None),
        ("mechanical-engineer", "Mechanical Engineer", B_ENG, None),
        ("civil-engineer", "Civil Engineer", B_ENG, None),
        ("electrical-engineer", "Electrical Engineer", B_ENG, None),
        ("teacher", "High School Science Teacher", B_TEACH, None),
        ("nurse", "Critical Care Nurse", B_NURSE, SK_CLIN),
        ("pharmacist", "Clinical Pharmacist", B_NURSE, SK_CLIN),
        ("customer-support", "Customer Support Specialist", B_MGR, None),
        ("consultant", "Management Consultant", B_MGR, None),
        ("founder", "Founder", B_MGR, None),
        ("freelancer", "Independent Consultant", B_DESIGN, SK_DESIGN),
    ]
    for key, title, bullets, sk in roles:
        d = R("Jordan Avery", title,
              experience=[job(title, "Northwind", "2020-01", "present", bullets),
                          job(title, "Globex", "2017-01", "2020-01", bullets[:2], "Portland, OR")],
              education=[EDU_BS])
        if sk:
            d["skills"] = sk
        add(f"role-{key}", d)

    # --- templates x same content -------------------------------------------
    base_senior = dict(
        summary="Backend engineer with eight years on payments under hard latency budgets.",
        experience=[job("Senior Engineer", "Northwind", "2021-03", "present", B_ENG),
                    job("Engineer", "Globex", "2018-06", "2021-03", B_ENG[:2], "Portland, OR")],
        education=[EDU_BS], skills=SK_ENG)
    for t in ("modern", "classic", "compact", "signature"):
        add(f"template-{t}", R("Maya Ellison", "Senior Backend Engineer",
                               config={"template": t}, **base_senior))
    # signature's full-bleed band must survive a custom band colour and A4 geometry
    add("signature-custom-band", R("Maya Ellison", "Senior Backend Engineer",
        config={"template": "signature", "band": "#3B2E4A", "accent": "#3B2E4A"}, **base_senior))
    add("signature-a4", R("Maya Ellison", "Senior Backend Engineer",
        config={"template": "signature", "page": "a4"}, **base_senior))
    add("signature-two-page", R("Pat Delgado", "Principal Engineer",
        config={"template": "signature", "max_pages": 2},
        experience=[job(f"Engineer {i}", f"Company {i}", f"{2008+i*2}-01", f"{2010+i*2}-01",
                        B_ENG[:2]) for i in range(7)],
        education=[EDU_BS], skills=SK_ENG))
    add("template-academic", R("Dr. Lin Chen", "Postdoctoral Researcher",
        config={"template": "academic", "max_pages": 4, "stage": "academic"},
        education=[EDU_PHD],
        experience=[job("Postdoctoral Fellow", "UCSF", "2021-09", "present", B_ENG[:2], "San Francisco, CA")],
        publications=PUBS,
        awards=[{"name": "NIH F32 Postdoctoral Fellowship", "year": 2022}],
        skills=[{"group": "Methods", "items": ["scRNA-seq", "CRISPR", "Confocal imaging"]}]))

    # --- density / page / accent --------------------------------------------
    for d_ in ("tight", "normal", "airy"):
        add(f"density-{d_}", R("Maya Ellison", "Senior Backend Engineer",
                               config={"density": d_, "max_pages": 2}, **base_senior))
    add("page-a4", R("Maya Ellison", "Senior Backend Engineer",
                     config={"page": "a4"}, **base_senior))
    add("accent-none", R("Maya Ellison", "Senior Backend Engineer",
                         config={"template": "classic", "accent": "#16181D"}, **base_senior))
    add("accent-custom", R("Maya Ellison", "Senior Backend Engineer",
                           config={"accent": "#6B2737"}, **base_senior))

    # --- content pressure ----------------------------------------------------
    long_hist = [job(f"Engineer {i}", f"Company {i}", f"{2000+i*2}-01", f"{2002+i*2}-01",
                     B_ENG[:2]) for i in range(12)]
    add("very-long-history", R("Pat Delgado", "Principal Engineer",
        experience=long_hist, education=[EDU_BS], skills=SK_ENG, config={"max_pages": 2}))
    add("overflow-forces-fit", R("Pat Delgado", "Principal Engineer",
        experience=long_hist[:8], education=[EDU_BS], skills=SK_ENG, config={"max_pages": 1}))
    add("many-certifications", R("Chris Vale", "Cloud Architect",
        experience=[job("Architect", "Northwind", "2020-01", "present", B_ENG)],
        education=[EDU_BS],
        certifications=[{"name": f"Certification Number {i}", "issuer": "Vendor", "date": 2020+i%4}
                        for i in range(12)]))
    add("many-projects", R("Chris Vale", "Engineer",
        experience=[job("Engineer", "Northwind", "2020-01", "present", B_ENG[:1])],
        projects=[{"name": f"Project {i}", "summary": "A thing that does a thing.",
                   "link": f"github.com/chris/p{i}", "bullets": B_JUNIOR[:1]} for i in range(8)],
        education=[EDU_BS], config={"max_pages": 2}))
    add("many-publications", R("Dr. Lin Chen", "Research Scientist",
        config={"template": "academic", "max_pages": 6, "stage": "academic"},
        education=[EDU_PHD], publications=PUBS * 12))
    add("multiple-degrees", R("Dr. Sam Reyes", "Physician-Scientist",
        config={"template": "classic", "max_pages": 2},
        education=[EDU_PHD, EDU_MBA, EDU_BS],
        experience=[job("Attending Physician", "Harborview", "2021-07", "present", B_NURSE[:2])]))
    add("employment-gap", R("Alice Nakamura", "Software Engineer",
        experience=[job("Engineer", "Northwind", "2023-06", "present", B_ENG[:2]),
                    job("Engineer", "Globex", "2015-06", "2020-03", B_ENG[:2])],
        education=[EDU_BS], skills=SK_ENG))
    add("no-summary", R("Maya Ellison", "Senior Backend Engineer",
        experience=[job("Senior Engineer", "Northwind", "2021-03", "present", B_ENG)],
        education=[EDU_BS], skills=SK_ENG))
    add("no-skills-section", R("Maya Ellison", "Senior Backend Engineer",
        experience=[job("Senior Engineer", "Northwind", "2021-03", "present", B_ENG)],
        education=[EDU_BS]))
    add("no-education", R("Maya Ellison", "Self-Taught Engineer",
        experience=[job("Senior Engineer", "Northwind", "2021-03", "present", B_ENG)],
        skills=SK_ENG))
    add("custom-sections", R("Maya Ellison", "Engineer",
        experience=[job("Engineer", "Northwind", "2021-03", "present", B_ENG[:2])],
        education=[EDU_BS],
        custom_sections=[{"title": "Speaking", "items": ["KubeCon 2024 — Sharding Postgres in anger."]},
                         {"title": "Open Source", "items": ["Maintainer, pgshard (2.1k stars)."]}]))
    add("many-languages", R("Sofia Marchetti", "Localization Manager",
        experience=[job("Localization Manager", "Northwind", "2020-01", "present", B_MGR[:2])],
        education=[EDU_BS],
        custom_sections=[{"title": "Languages",
                          "items": ["Italian (native)", "English (fluent)", "German (fluent)",
                                    "Spanish (conversational)", "Japanese (basic)"]}]))
    add("portfolio-links", R("Robin Fields", "Product Designer",
        config={"template": "modern"},
        experience=[job("Product Designer", "Northwind", "2020-01", "present", B_DESIGN)],
        education=[EDU_BS], skills=SK_DESIGN))

    # --- adversarial / edge cases -------------------------------------------
    add("edge-one-word-name", R("Prince", "Recording Artist",
        experience=[job("Artist", "Paisley Park", "1978-01", "2016-04", B_DESIGN[:2])]))
    add("edge-very-long-name", R("Bartholomew Fitzwilliam-Montgomery III",
        "Senior Vice President of Strategic Partnerships and Business Development",
        experience=[job("SVP Strategic Partnerships and Business Development",
                        "Northwind Global Holdings International", "2020-01", "present", B_MGR[:2])],
        education=[EDU_MBA]))
    add("edge-unicode-name", R("Zoë Müller-Ødegård", "Инженер / Engineer",
        experience=[job("Engineer", "Nørthwind AS", "2020-01", "present",
                        ["Reduced latency 40% — measured across 12 régions."], "Oslo, Norway")],
        education=[EDU_BS], config={"page": "a4"}))
    add("edge-cjk-name", R("陳大文 Chen Da-Wen", "Software Engineer",
        experience=[job("Engineer", "Northwind", "2020-01", "present", B_ENG[:2], "Taipei, Taiwan")],
        education=[EDU_BS], config={"page": "a4"}))
    add("edge-no-phone", R("Maya Ellison", "Engineer",
        experience=[job("Engineer", "Northwind", "2021-03", "present", B_ENG[:2])],
        education=[EDU_BS]))
    add("edge-single-job-single-bullet", R("Sam Short", "Analyst",
        experience=[job("Analyst", "Northwind", "2023-01", "present", ["Did the analysis."])]))
    add("edge-long-bullets", R("Verbose Vince", "Engineer",
        experience=[job("Engineer", "Northwind", "2021-03", "present",
            ["Architected, implemented, deployed, monitored and iterated on a "
             "comprehensive distributed event-processing pipeline that ingested "
             "telemetry from 400 services across 12 regions while maintaining "
             "sub-second p99 latency and 99.99% availability throughout a full "
             "calendar year of continuous operation without a single sev1 incident."])],
        education=[EDU_BS]))
    add("edge-special-chars", R("Ann O'Brien-Smith", "R&D Engineer <Systems>",
        experience=[job("R&D Engineer", "AT&T / Bell Labs", "2020-01", "present",
            ["Improved throughput >40% & cut cost by ~$1.2M (FY23).",
             'Wrote the "golden path" doc; 100% of teams adopted it.'])],
        education=[EDU_BS]))
    add("edge-no-dates", R("Timeless Terry", "Consultant",
        experience=[{"role": "Consultant", "company": "Self-employed",
                     "bullets": ["Advised 14 startups on infrastructure."]}]))
    add("edge-present-only", R("Fresh Start", "Engineer",
        experience=[job("Engineer", "Northwind", "2024-06", "present", B_ENG[:1])]))
    add("edge-minimal", {"config": {"template": "modern", "max_pages": 1},
                         "basics": {"name": "Minimal Mike", "email": "mike@example.com"}})
    add("edge-year-only-dates", R("Yearly Yolanda", "Engineer",
        experience=[job("Engineer", "Northwind", "2021", "2024", B_ENG[:2])],
        education=[EDU_BS]))

    # --- corpus-driven axes (references/pattern-study.md) --------------------
    # Both were added because the 153-template survey showed the shipped system
    # lacked them. Both must survive parse-back like anything else -- a pattern
    # that is popular is not thereby safe.
    add("axis-date-inline", R("Maya Ellison", "Senior Backend Engineer",
        config={"date_style": "inline"}, **base_senior))
    add("axis-skills-pills", R("Maya Ellison", "Senior Backend Engineer",
        config={"skills_style": "pills"}, **base_senior))
    add("axis-both", R("Maya Ellison", "Senior Backend Engineer",
        config={"date_style": "inline", "skills_style": "pills"}, **base_senior))
    add("axis-pills-signature", R("Maya Ellison", "Senior Backend Engineer",
        config={"template": "signature", "skills_style": "pills",
                "date_style": "inline"}, **base_senior))

    # --- presets -------------------------------------------------------------
    # One per family. Rendering is not the bar -- a preset that renders but bleeds
    # is still broken, so every family gets parse-checked like anything else.
    # (gallery.py --verify covers all 107; this keeps the default suite quick.)
    for p in ("material-blue", "signature-teal", "modern-navy", "modern-bar-forest",
              "editorial-burgundy", "classic-ink", "compact-slate", "minimal-graphite",
              "executive-oxblood", "technical-cobalt", "warm-rust", "nordic-steel",
              "banded-navy"):
        d = R("Maya Ellison", "Senior Backend Engineer", config={"max_pages": 2},
              **base_senior)
        d["_preset"] = p
        add(f"preset-{p}", d)

    return S


# ---------------------------------------------------------------- runner

def run_one(item: tuple[str, dict], outdir: Path, fit: bool) -> dict:
    name, data = item
    import yaml
    d = outdir / name
    d.mkdir(parents=True, exist_ok=True)
    preset = data.pop("_preset", None)
    y = d / "resume.yaml"
    y.write_text(yaml.dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")

    cmd = [sys.executable, str(BUILD), str(y), "--format", "pdf,docx,txt",
           "--out", str(d), "--quiet"]
    if preset:
        cmd += ["--preset", preset]
    if fit:
        cmd.append("--fit")
    b = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if b.returncode != 0:
        return {"name": name, "status": "BUILD-FAIL",
                "detail": (b.stderr or b.stdout)[-400:]}

    pdfs = list(d.glob("*.pdf"))
    if not pdfs:
        return {"name": name, "status": "NO-PDF", "detail": (b.stderr or "")[-300:]}

    c = subprocess.run([sys.executable, str(CHECK), str(pdfs[0]), "--data", str(y)],
                       capture_output=True, text=True, timeout=180)
    out = c.stdout
    fails = [l.strip() for l in out.split("\n") if "FAIL" in l]
    warns = [l.strip() for l in out.split("\n") if "WARN" in l]
    docx_ok = bool(list(d.glob("*.docx")))
    txt_ok = bool(list(d.glob("*.txt")))
    return {
        "name": name,
        "status": "PASS" if not fails else "CHECK-FAIL",
        "fails": fails[:4],
        "warns": warns[:2],
        "docx": docx_ok, "txt": txt_ok,
        "lint": len([l for l in (b.stderr or "").split("\n") if l.strip().startswith("!")]),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--out", default=None)
    ap.add_argument("--fit", action="store_true", default=True)
    ap.add_argument("--filter", default=None, help="substring match on scenario name")
    a = ap.parse_args()

    S = matrix()
    if a.filter:
        S = [s for s in S if a.filter in s[0]]
    if a.limit:
        S = S[: a.limit]
    outdir = Path(a.out).resolve() if a.out else Path(tempfile.mkdtemp(prefix="resume_scen_"))
    print(f"scenarios: {len(S)}   jobs: {a.jobs}   out: {outdir}\n")

    results = []
    with cf.ThreadPoolExecutor(max_workers=a.jobs) as ex:
        futs = {ex.submit(run_one, s, outdir, a.fit): s[0] for s in S}
        for i, f in enumerate(cf.as_completed(futs), 1):
            try:
                r = f.result()
            except Exception as e:
                r = {"name": futs[f], "status": "ERROR", "detail": str(e)[:200]}
            results.append(r)
            icon = {"PASS": "ok  ", "CHECK-FAIL": "FAIL", "BUILD-FAIL": "BUILD",
                    "NO-PDF": "NOPDF", "ERROR": "ERR "}.get(r["status"], "?")
            extra = ""
            if r.get("fails"):
                extra = " | " + r["fails"][0][:80]
            elif r.get("detail"):
                extra = " | " + r["detail"].replace("\n", " ")[:80]
            print(f"  [{i:3d}/{len(S)}] {icon} {r['name']:34s}{extra}")

    results.sort(key=lambda r: r["name"])
    n_pass = sum(1 for r in results if r["status"] == "PASS")
    print(f"\n{'='*74}")
    print(f"  {n_pass}/{len(results)} passed")
    bad = [r for r in results if r["status"] != "PASS"]
    if bad:
        print(f"\n  failures:")
        for r in bad:
            print(f"    {r['name']}: {r['status']}")
            for fl in r.get("fails", [])[:3]:
                print(f"        {fl[:110]}")
            if r.get("detail"):
                print(f"        {r['detail'][:200]}")
    (outdir / "results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\n  results.json -> {outdir/'results.json'}")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
