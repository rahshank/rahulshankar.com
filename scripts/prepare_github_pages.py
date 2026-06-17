#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import sys
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
DOCS = ROOT / "docs"
BUILD = ROOT / "scripts" / "build_site.py"
CUSTOM_DOMAIN = os.environ.get("SITE_CUSTOM_DOMAIN", "rahulshankar.com").strip()
DEFAULT_BASE_PATH = "" if CUSTOM_DOMAIN else "rahulshankar.com"


def main() -> None:
    env = os.environ.copy()
    env["SITE_BASE_PATH"] = os.environ.get("SITE_BASE_PATH", DEFAULT_BASE_PATH).strip("/")
    subprocess.run([sys.executable, str(BUILD)], cwd=ROOT, env=env, check=True)
    if not PUBLIC.exists():
        raise SystemExit("public/ does not exist. Run scripts/build_site.py first.")
    if DOCS.exists():
        shutil.rmtree(DOCS)
    shutil.copytree(PUBLIC, DOCS)
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    if CUSTOM_DOMAIN:
        (DOCS / "CNAME").write_text(f"{CUSTOM_DOMAIN}\n", encoding="utf-8")
    subprocess.run([sys.executable, str(BUILD)], cwd=ROOT, check=True)
    print(f"Prepared GitHub Pages output in {DOCS}")


if __name__ == "__main__":
    main()
