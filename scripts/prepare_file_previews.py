#!/usr/bin/env python3
from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
PREVIEW_INPUT = ROOT / "previews" / "render-input"

PAGES = {
    "index.html": "home.html",
    "ghosts-of-bombay/index.html": "ghosts-of-bombay.html",
    "writing/index.html": "writing.html",
    "notebook/index.html": "notebook.html",
}


def inline_css(html: str, css: str) -> str:
    return html.replace(
        '<link rel="stylesheet" href="/assets/site.css">',
        f"<style>{css}</style>",
    )


def main() -> None:
    if not PUBLIC.exists():
        raise SystemExit("public/ does not exist. Run scripts/build_site.py first.")
    if PREVIEW_INPUT.exists():
        shutil.rmtree(PREVIEW_INPUT)
    PREVIEW_INPUT.mkdir(parents=True)

    css = (PUBLIC / "assets" / "site.css").read_text(encoding="utf-8")
    for source, target in PAGES.items():
        html = (PUBLIC / source).read_text(encoding="utf-8")
        (PREVIEW_INPUT / target).write_text(inline_css(html, css), encoding="utf-8")

    print(f"Prepared {len(PAGES)} standalone preview files in {PREVIEW_INPUT}")


if __name__ == "__main__":
    main()
