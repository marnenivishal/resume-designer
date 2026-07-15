#!/usr/bin/env python3
"""Generate assets/presets.yaml -- the named looks.

    python scripts/gen_presets.py > ../assets/presets.yaml

Why generated rather than hand-written: a preset is a POINT IN A DESIGN SPACE, not
a document. The axes are

    skeleton   x  type pairing  x  accent  x  heading treatment  x  density

and the interesting looks are combinations of those, not bespoke files. 100 template
FILES would be 100 things to maintain and parse-test, and in practice the "100+
templates" on commercial sites are a handful of skeletons with colour swaps sold as
variety. This is the same variety, honestly labelled, and every preset inherits the
one tested structure -- so a preset physically cannot break parse-safety.

Every accent here is verified >= 4.5:1 on white at generation time. That check
matters: of 160 palette colours in a well-known UI palette set, 93 FAIL it. Screen
palettes assume large text or non-text use; a resume accent carries small heading
text and must clear AA on its own.
"""
from __future__ import annotations
import sys

def lum(h: str) -> float:
    h = h.lstrip("#")
    parts = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    f = lambda v: v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = map(f, parts)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def on_white(h: str) -> float:
    return 1.05 / (lum(h) + 0.05)

# --- accents -----------------------------------------------------------------
# Deep and desaturated by preference: survives greyscale printing (still a common
# fate) and reads as a considered choice rather than decoration.
ACCENTS = {
    # name            hex        family
    "teal":          "#1F4E5F",
    "navy":          "#1B3A5C",
    "slate":         "#33415C",
    "graphite":      "#2F3437",
    "ink":           "#16181D",
    "forest":        "#1E4634",
    "moss":          "#3A4A2F",
    "burgundy":      "#6B2737",
    "oxblood":       "#5C2231",
    "plum":          "#4A2C4D",
    "indigo":        "#33366B",
    "cobalt":        "#1A3E7A",
    "material-blue": "#0D47A1",   # Material Blue 900
    "material-teal": "#00695C",   # Material Teal 800
    "material-indigo":"#283593",  # Material Indigo 800
    "material-green":"#1B5E20",   # Material Green 900
    "material-grey": "#37474F",   # Material Blue Grey 800
    "material-deep-orange":"#BF360C",  # Deep Orange 900
    "material-purple":"#4A148C",  # Purple 900
    "material-brown":"#3E2723",   # Brown 900
    "rust":          "#7A3B1F",
    "bronze":        "#6B4423",
    "steel":         "#3D5266",
    "pine":          "#20453C",
}

# --- type pairings -----------------------------------------------------------
# Only static, widely-installed families. No variable fonts: measured, they make
# Chrome emit Type3 glyph procedures instead of real embedded text.
SERIF = '"Cambria", "Charter", "Bitstream Charter", "Palatino Linotype", Georgia, serif'
SANS  = '"Segoe UI", "Helvetica Neue", "Calibri", "Lato", Arial, sans-serif'
GEO   = '"Century Gothic", "Futura", "Avenir Next", "Segoe UI", "Helvetica Neue", Arial, sans-serif'

TYPE = {
    "sans":      {"body": SANS,  "head": SANS},
    "serif":     {"body": SERIF, "head": SERIF},
    "mixed":     {"body": SERIF, "head": SANS},   # serif body, sans headings
    "mixed-alt": {"body": SANS,  "head": SERIF},  # sans body, serif headings
    "geometric": {"body": SANS,  "head": GEO},
}

# --- families ----------------------------------------------------------------
# Each family is a coherent point of view, not a random combination.
FAMILIES = [
    dict(prefix="material", template="signature", type="geometric", density="normal",
         heading_style="thick", note="Google-flavoured: geometric headings, saturated band, generous rhythm",
         accents=["material-blue","material-teal","material-indigo","material-green",
                  "material-grey","material-deep-orange","material-purple","material-brown"]),
    dict(prefix="signature", template="signature", type="sans", density="normal",
         heading_style=None, note="Full-bleed colour masthead. The premium look, single column",
         accents=["teal","navy","slate","graphite","forest","burgundy","plum","indigo",
                  "cobalt","steel","pine","rust"]),
    dict(prefix="modern", template="modern", type="sans", density="normal",
         heading_style=None, note="Contemporary, restrained. The safe default",
         accents=["teal","navy","slate","graphite","forest","burgundy","indigo","cobalt",
                  "steel","bronze"]),
    dict(prefix="modern-bar", template="modern", type="sans", density="normal",
         heading_style="bar", note="Accent bar beside each heading rather than a rule",
         accents=["teal","navy","forest","burgundy","indigo","graphite"]),
    dict(prefix="editorial", template="modern", type="mixed", density="airy",
         heading_style=None, note="Serif body, sans headings, generous space. Reads like a journal",
         accents=["ink","graphite","burgundy","oxblood","forest","plum","bronze","navy"]),
    dict(prefix="classic", template="classic", type="serif", density="normal",
         heading_style=None, note="Centred small caps. Law, finance, government, medicine",
         accents=["ink","graphite","navy","burgundy","oxblood","forest","slate","bronze"]),
    dict(prefix="compact", template="compact", type="mixed", density="tight",
         heading_style=None, note="Long histories that must fit. Dense but still typeset",
         accents=["ink","teal","navy","graphite","slate","forest","burgundy","steel"]),
    dict(prefix="minimal", template="modern", type="sans", density="airy",
         heading_style="plain", note="No rules at all. Hierarchy from space and weight only",
         accents=["ink","graphite","slate","steel","navy","teal"]),
    dict(prefix="academic", template="academic", type="serif", density="normal",
         heading_style=None, note="Academic CV. Numbered publications, no page cap",
         accents=["ink","navy","graphite","forest","burgundy","plum"]),
    dict(prefix="executive", template="signature", type="mixed-alt", density="airy",
         heading_style=None, note="Senior roles. Dark band, serif headings, room to breathe",
         accents=["ink","graphite","navy","oxblood","plum","pine","steel","bronze"]),
    dict(prefix="technical", template="modern", type="sans", density="tight",
         heading_style="thick", note="Engineering. Dense, skills-forward, no ornament",
         accents=["teal","navy","graphite","cobalt","steel","moss","indigo","pine"]),
    dict(prefix="warm", template="modern", type="mixed", density="normal",
         heading_style=None, note="Warmer palette. Design, education, non-profit, healthcare",
         accents=["rust","bronze","burgundy","oxblood","moss","plum","material-brown"]),
    dict(prefix="nordic", template="modern", type="geometric", density="airy",
         heading_style="plain", note="Quiet and spacious. Muted accent, no rules, lots of air",
         accents=["steel","slate","pine","moss","graphite","teal"]),
    dict(prefix="banded", template="signature", type="serif", density="normal",
         heading_style="bar", note="Colour band with a serif body. Warm authority",
         accents=["oxblood","burgundy","bronze","pine","navy","ink"]),
]


def check_no_variable_fonts() -> list[str]:
    """Refuse to generate if any named font is a variable font, where installed.

    Not hypothetical: the first cut of GEO named "Bahnschrift", which is Microsoft's
    VARIABLE DIN. Chrome cannot reference a static face for a variation instance, so
    it emitted /Type3 glyph procedures for every heading across 16 presets -- tripping
    this project's own ats_check warning. tokens.css says "no VF is named here" and
    this file quietly broke that.

    A comment asking people to remember is not a control. This is.
    Fonts that are not installed locally are skipped (nothing to check).
    """
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        return []                      # fontTools optional; skip rather than block
    import glob, os, re
    names = set()
    for stack in (SERIF, SANS, GEO):
        for fam in re.findall(r'"([^"]+)"', stack):
            names.add(fam.lower().replace(" ", ""))
    problems = []
    for path in glob.glob(os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", "*.tt*")):
        base = os.path.basename(path).lower().replace(" ", "")
        try:
            f = TTFont(path, fontNumber=0, lazy=True)
        except Exception:
            continue
        if "fvar" not in f:
            continue
        try:
            fam = str(f["name"].getDebugName(1) or "").lower().replace(" ", "")
        except Exception:
            fam = ""
        for want in names:
            if want and (want == fam or want == base.rsplit(".", 1)[0]):
                problems.append(f"{f['name'].getDebugName(1)} (variable) is named in a stack")
    return problems


def main() -> int:
    bad = [(n, h, round(on_white(h), 2)) for n, h in ACCENTS.items() if on_white(h) < 4.5]
    if bad:
        print("FATAL: accents below 4.5:1 on white: " + repr(bad), file=sys.stderr)
        return 1

    vf = check_no_variable_fonts()
    if vf:
        print("FATAL: variable font in a type stack -> Chrome emits Type3 glyph "
              "procedures instead of real embedded text:\n  " + "\n  ".join(vf),
              file=sys.stderr)
        return 1

    out: list[str] = []
    out.append("# presets.yaml -- GENERATED by scripts/gen_presets.py. Do not hand-edit;")
    out.append("# regenerate instead. Each preset is a point in the design space")
    out.append("#   skeleton x type pairing x accent x heading treatment x density")
    out.append("# and inherits the one tested, parse-safe structure. A preset can retune")
    out.append("# the design; it cannot restructure the document, so it cannot break parsing.")
    out.append("#")
    out.append("# Every accent below is verified >=4.5:1 on white at generation time.")
    out.append("#")
    out.append("#   python scripts/build.py resume.yaml --preset material-blue")
    out.append("#   python scripts/build.py --list-presets")
    out.append("#   python scripts/gallery.py          # render every preset to one page")
    out.append("")
    out.append("presets:")

    count = 0
    for fam in FAMILIES:
        out.append(f"\n  # --- {fam['prefix']}: {fam['note']}")
        for a in fam["accents"]:
            hexv = ACCENTS[a]
            # Avoid stutter: "material-material-blue" -> "material-blue"
            short = a[len(fam["prefix"]) + 1:] if a.startswith(fam["prefix"] + "-") else a
            name = f"{fam['prefix']}-{short}"
            out.append(f"  {name}:")
            out.append(f"    template: {fam['template']}")
            out.append(f"    type: {fam['type']}")
            out.append(f"    density: {fam['density']}")
            out.append(f'    accent: "{hexv}"')
            if fam["template"] == "signature":
                out.append(f'    band: "{hexv}"')
            if fam.get("heading_style"):
                out.append(f"    heading_style: {fam['heading_style']}")
            # Quote the note: it contains ':' and ',' which are YAML structure.
            note = f"{fam['note']} ({short}, {on_white(hexv):.1f}:1 on white)"
            out.append(f'    note: "{note.replace(chr(34), chr(39))}"')
            count += 1

    print("\n".join(out))
    print(f"\n# {count} presets across {len(FAMILIES)} families.")
    print(f"# accents: {len(ACCENTS)} | type pairings: {len(TYPE)}", file=sys.stderr)
    print(f"# generated {count} presets", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
