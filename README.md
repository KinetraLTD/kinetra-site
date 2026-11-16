# kinetra.uk

The Kinetra website: one static page, no build step, no cookies, nothing loaded from third parties.

- `index.html`, `assets/`: the site. OVH web hosting pulls this repository on every push to `main`
  (Git association on the hosting's site folder), so pushing is publishing.
- `brand/`: logo sources. `python3 brand/make_logos.py` draws the options (wordmarks outlined from
  Roboto Flex, SIL OFL 1.1); `python3 brand/use_logo.py a-orbit|b-k|c-brackets` puts one into `assets/`.
  `brand/preview.html` compares them.
- `.htaccess` hides `brand/`, this file and `.git` from the web.

Kinetra is a trading name of Alterflow Ltd.
