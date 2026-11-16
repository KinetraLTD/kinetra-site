#!/usr/bin/env python3
"""Puts one logo option into the site: python3 brand/use_logo.py a-orbit|b-k|c-brackets"""
import pathlib
import shutil
import sys

from make_logos import OPTIONS, build

BRAND = pathlib.Path(__file__).parent
ASSETS = BRAND.parent / "assets"

name = sys.argv[1] if len(sys.argv) > 1 else "a-orbit"
if name not in OPTIONS:
    sys.exit(f"Unknown option {name}; pick one of {', '.join(OPTIONS)}")
build()
for f in ("mark.svg", "mark-dark.svg", "lockup-light.svg", "lockup-dark.svg"):
    shutil.copy(BRAND / name / f, ASSETS / f.replace("lockup", "logo"))
accent = OPTIONS[name][1]
(ASSETS / "brand.css").write_text(f":root {{ --accent: {accent}; }}\n")
print(f"Site now uses {name} (accent {accent})")
