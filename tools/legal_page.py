#!/usr/bin/env python3
"""Turns one of AOD+'s legal documents (Markdown, English then Italian) into a page of this site.

    python3 tools/legal_page.py privacy /path/to/privacy-policy.md   ->  aodplus/privacy/index.html
    python3 tools/legal_page.py terms   /path/to/terms-of-use.md     ->  aodplus/terms/index.html

The text is edited only in the aodplus-app repository (docs/); its tools/publish_legal.sh runs this and
pushes, and OVH deploys the push. Markdown is rendered by GitHub's API (`gh api markdown`, README style:
tables, no hard line breaks).
"""
import html
import pathlib
import re
import subprocess
import sys

SITE = pathlib.Path(__file__).resolve().parent.parent
PAGES = {
    "privacy": "AOD+ Privacy Policy",
    "terms": "AOD+ Terms of Use",
}
# Links between the two documents are relative .md files in the source repository.
LINKS = {"(privacy-policy.md)": "(/aodplus/privacy/)", "(terms-of-use.md)": "(/aodplus/terms/)"}


def render(markdown: str) -> str:
    out = subprocess.run(["gh", "api", "markdown", "-f", f"text={markdown}", "-f", "mode=markdown"],
                         check=True, capture_output=True, text=True).stdout
    # GitHub prefixes heading anchors with "user-content-"; plain ids read better in links.
    return out.replace('id="user-content-', 'id="').replace('href="#user-content-', 'href="#')


def main(kind: str, source: str) -> None:
    title = PAGES[kind]
    text = pathlib.Path(source).read_text()
    for old, new in LINKS.items():
        text = text.replace(old, new)
    # The file holds the English version, then the Italian one, each starting with a level-1 heading.
    parts = re.split(r"(?m)^(?=# )", text)
    english, italian = [p for p in parts if p.strip()]
    body = (f'<section id="en" lang="en">{render(english)}</section>\n'
            f'<section id="it" lang="it">{render(italian)}</section>')
    page = TEMPLATE.format(title=html.escape(title), body=body)
    out = SITE / "aodplus" / kind / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page)
    print(f"Wrote {out.relative_to(SITE)}")


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} · Kinetra</title>
  <meta name="color-scheme" content="light dark">
  <link rel="icon" href="/assets/mark.svg" type="image/svg+xml">
  <link rel="preload" href="/assets/fonts/roboto-flex.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/assets/brand.css">
  <link rel="stylesheet" href="/assets/style.css">
</head>
<body>
  <header class="top">
    <div class="wrap top-row">
      <a class="logo" href="/" aria-label="Kinetra home">
        <picture>
          <source srcset="/assets/logo-dark.svg" media="(prefers-color-scheme: dark)">
          <img src="/assets/logo-light.svg" alt="Kinetra" height="34">
        </picture>
      </a>
      <nav aria-label="Language">
        <a href="#en">English</a>
        <a href="#it" lang="it" class="nav-cta">Italiano</a>
      </nav>
    </div>
  </header>

  <main class="wrap doc">
{body}
  </main>

  <footer class="wrap foot">
    <div class="foot-row">
      <span>© 2026 Kinetra</span>
      <span class="foot-links">
        <a href="/aodplus/privacy/">AOD+ privacy</a>
        <a href="/aodplus/terms/">AOD+ terms</a>
      </span>
    </div>
  </footer>
</body>
</html>
"""

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in PAGES:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
