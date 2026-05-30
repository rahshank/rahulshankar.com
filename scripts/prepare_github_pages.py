#!/usr/bin/env python3
from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
DOCS = ROOT / "docs"


def main() -> None:
    if not PUBLIC.exists():
        raise SystemExit("public/ does not exist. Run scripts/build_site.py first.")
    if DOCS.exists():
        shutil.rmtree(DOCS)
    shutil.copytree(PUBLIC, DOCS)
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    print(f"Prepared GitHub Pages output in {DOCS}")


if __name__ == "__main__":
    main()

