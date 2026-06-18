#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"


def target_for_href(href: str) -> Path | None:
    parsed = urlparse(href)
    if parsed.scheme or parsed.netloc or href.startswith("#") or href.startswith("mailto:"):
        return None
    href_path = parsed.path
    if not href_path:
        return None
    if href_path.startswith("/"):
        path = PUBLIC / href_path.lstrip("/")
    else:
        path = PUBLIC / href_path
    if href_path.endswith("/"):
        return path / "index.html"
    if path.suffix:
        return path
    return path / "index.html"


def main() -> int:
    if not PUBLIC.exists():
        print("public/ does not exist. Run scripts/build_site.py first.")
        return 1

    problems = []
    for html_path in PUBLIC.rglob("*.html"):
        text = html_path.read_text(encoding="utf-8")
        for href in re.findall(r'href="([^"]+)"', text):
            target = target_for_href(href)
            if target is not None and not target.exists():
                problems.append((html_path.relative_to(PUBLIC), href, target.relative_to(PUBLIC)))

    if problems:
        print("Broken internal links:")
        for source, href, target in problems:
            print(f"- {source}: {href} -> missing {target}")
        return 1

    print("Site check passed: no broken internal links found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
