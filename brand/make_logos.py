#!/usr/bin/env python3
"""Generates the Kinetra logo options as plain SVG (wordmarks outlined, no font needed).

Wordmarks use Roboto Flex (SIL Open Font License 1.1) from Android Studio's layoutlib.
Run: python3 brand/make_logos.py   ->  brand/<option>/{mark,lockup-light,lockup-dark}.svg
"""
import math
import pathlib

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

FONT = "/Applications/Android Studio.app/Contents/plugins/design-tools/resources/layoutlib/data/fonts/RobotoFlex-Regular.ttf"
OUT = pathlib.Path(__file__).parent

INK = "#14161C"
WHITE = "#FFFFFF"


def wordmark(text, wght, size, tracking=0.0, wdth=100, opsz=None):
    """Returns (svg path d, width) for text set at `size` px with baseline at y=0."""
    font = instantiateVariableFont(TTFont(FONT), {"wght": wght, "wdth": wdth, "opsz": opsz or size},
                                   inplace=False)
    upem = font["head"].unitsPerEm
    cmap, hmtx, glyphs = font.getBestCmap(), font["hmtx"], font.getGlyphSet()
    scale = size / upem
    pen = SVGPathPen(glyphs)
    x = 0.0
    for i, ch in enumerate(text):
        g = cmap[ord(ch)]
        glyphs[g].draw(TransformPen(pen, (scale, 0, 0, -scale, x, 0)))
        x += hmtx[g][0] * scale + (tracking * size if i < len(text) - 1 else 0)
    return pen.getCommands(), x


def arc(cx, cy, r, a0, a1):
    """SVG arc from angle a0 to a1 (degrees, clockwise from 3 o'clock, y down)."""
    p = lambda a: (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
    (x0, y0), (x1, y1) = p(a0), p(a1)
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return f"M{x0:.2f} {y0:.2f}A{r} {r} 0 {large} 1 {x1:.2f} {y1:.2f}"


# --- Marks: 64x64 artwork. `fg` is the colour that flips between light and dark backgrounds.
def mark_orbit(fg, accent):
    # A ring with a gap, and a dot travelling along it: always on, always moving.
    # The dot rides on the arc's end; the clear space ahead of it (to -13°) is ~5 units.
    return (f'<path d="{arc(32, 32, 22, -13, 290)}" fill="none" stroke="{fg}" stroke-width="8" '
            f'stroke-linecap="round"/>'
            f'<circle cx="{32 + 22 * math.cos(math.radians(-55)):.2f}" '
            f'cy="{32 + 22 * math.sin(math.radians(-55)):.2f}" r="7" fill="{accent}"/>')


def mark_k(fg, accent):
    # A rounded tile with a K whose arms come loose from the stem, like a forward step.
    return (f'<rect width="64" height="64" rx="16" fill="{accent}"/>'
            f'<path d="M21 17V47" stroke="{WHITE}" stroke-width="7.5" stroke-linecap="round"/>'
            f'<path d="M44 17 30.5 32 44 47" fill="none" stroke="{WHITE}" stroke-width="7.5" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def mark_brackets(fg, accent):
    # Evolution of today's brackets: ‹ • ›, code around a point of focus.
    return (f'<path d="M20 18 7 32l13 14M44 18l13 14-13 14" fill="none" stroke="{fg}" stroke-width="7" '
            f'stroke-linecap="round" stroke-linejoin="round"/>'
            f'<circle cx="32" cy="32" r="7.5" fill="{accent}"/>')


OPTIONS = {
    # name: (mark fn, accent, wordmark text, weight, tracking)
    "a-orbit": (mark_orbit, "#FFB020", "kinetra", 640, -0.01),
    "b-k": (mark_k, "#5B4CF5", "Kinetra", 560, -0.005),
    "c-brackets": (mark_brackets, "#F5BE2E", "KINETRA", 700, 0.14),
}


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" role="img" '
            f'aria-label="{title}"><title>{title}</title>{body}</svg>\n')


def build():
    for name, (mark, accent, text, wght, tracking) in OPTIONS.items():
        d = OUT / name
        d.mkdir(exist_ok=True)
        (d / "mark.svg").write_text(svg(64, 64, mark(INK, accent), "Kinetra"))
        (d / "mark-dark.svg").write_text(svg(64, 64, mark(WHITE, accent), "Kinetra"))
        size = 40 if text.isupper() else 44
        path, width = wordmark(text, wght, size, tracking)
        cap = size * 0.711  # Roboto Flex cap height ≈ 0.711 em: caps and ascenders centred on the mark
        baseline = 32 + cap / 2
        gap = 18
        total = 64 + gap + width
        for variant, fg in (("lockup-light", INK), ("lockup-dark", WHITE)):
            body = (mark(fg, accent) +
                    f'<path transform="translate({64 + gap} {baseline:.2f})" d="{path}" fill="{fg}"/>')
            (d / f"{variant}.svg").write_text(svg(total, 64, body, "Kinetra"))
        print(name, f"{total:.0f}x64")


if __name__ == "__main__":
    build()
