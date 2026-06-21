#!/usr/bin/env python3
from __future__ import annotations

import json
import hashlib
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"
POSTS = SOURCE / "posts"
PAGES = SOURCE / "pages"
IMAGES = SOURCE / "assets" / "images" / "ghost"
RAW = ROOT.parent / "workbench" / "raw" / "ghost-public"

API = "https://rahul-shankar.ghost.io/ghost/api/content"
KEY = "efc942fd5b9d82e7d2bad2b3f3"


def fetch_json(url: str) -> dict:
    req = Request(url, headers={"User-Agent": "rahulshankar.com static-site importer"})
    with urlopen(req, timeout=30) as response:
        return json.load(response)


def fetch_bytes(url: str) -> bytes:
    req = Request(url, headers={"User-Agent": "rahulshankar.com static-site importer"})
    with urlopen(req, timeout=30) as response:
        return response.read()


def frontmatter_value(value: object) -> str:
    if value is None:
        return ""
    return str(value).replace("\n", " ").replace("\r", " ").strip()


def image_target(url: str) -> str | None:
    parsed = urlparse(url)
    if not parsed.scheme.startswith("http"):
        return None
    name = Path(parsed.path).name
    if not name:
        return None
    clean = re.sub(r"[^A-Za-z0-9._-]+", "-", name)
    prefix = hashlib.sha1(url.encode("utf-8")).hexdigest()[:10]
    return f"{prefix}-{clean}"


def localize_image(url: str, image_map: dict[str, str]) -> str:
    if not url or not url.startswith(("http://", "https://")):
        return url
    if url in image_map:
        return image_map[url]
    target_name = image_target(url)
    if target_name is None:
        return url
    IMAGES.mkdir(parents=True, exist_ok=True)
    target = IMAGES / target_name
    try:
        if not target.exists():
            target.write_bytes(fetch_bytes(url))
        local = f"/assets/images/ghost/{target_name}"
        image_map[url] = local
        return local
    except Exception as error:
        print(f"warning: failed to download image {url}: {error}", file=sys.stderr)
        return url


def rewrite_html_images(html: str, image_map: dict[str, str]) -> str:
    def normalize_external_href(match: re.Match[str]) -> str:
        quote = match.group(1)
        url = match.group(2)
        if re.match(r"^[A-Za-z0-9.-]+\.[A-Za-z]{2,}(/.*)?$", url):
            url = f"https://{url}"
        return f"href={quote}{url}{quote}"

    def replace_image_src(match: re.Match[str]) -> str:
        prefix = match.group(1)
        quote = match.group(2)
        url = match.group(3)
        return f"{prefix}{quote}{localize_image(url, image_map)}{quote}"

    def replace_srcset(match: re.Match[str]) -> str:
        quote = match.group(1)
        value = match.group(2)
        pieces = []
        for item in value.split(","):
            bits = item.strip().split()
            if not bits:
                continue
            bits[0] = localize_image(bits[0], image_map)
            pieces.append(" ".join(bits))
        return f"srcset={quote}{', '.join(pieces)}{quote}"

    html = re.sub(
        r"(<(?:img|source)\b[^>]*\bsrc=)(['\"])(https?://[^'\"]+)\2",
        replace_image_src,
        html,
    )
    html = re.sub(r"srcset=(['\"])([^'\"]+)\1", replace_srcset, html)
    html = re.sub(r"href=(['\"])([^/'\"#][^:'\"]+)\1", normalize_external_href, html)
    return html


def item_tags(item: dict) -> str:
    return ", ".join(tag.get("name", "") for tag in item.get("tags", []) if tag.get("name"))


def item_author(item: dict) -> str:
    authors = item.get("authors") or []
    return authors[0].get("name", "Rahul Shankar") if authors else "Rahul Shankar"


def write_item(item: dict, kind: str, image_map: dict[str, str]) -> None:
    target_dir = POSTS if kind == "post" else PAGES
    target_dir.mkdir(parents=True, exist_ok=True)
    html_body = rewrite_html_images(item.get("html") or "", image_map)
    hero = localize_image(item.get("feature_image") or "", image_map)

    meta = {
        "title": item.get("title", ""),
        "slug": item.get("slug", ""),
        "date": (item.get("published_at") or "")[:10],
        "updated": (item.get("updated_at") or "")[:10],
        "author": item_author(item),
        "topics": item_tags(item),
        "summary": item.get("excerpt") or item.get("custom_excerpt") or "",
        "template": "article" if kind == "post" else "page",
        "body_format": "html",
        "ghost_id": item.get("id", ""),
        "source_url": item.get("url", ""),
    }
    if hero:
        meta["hero_image"] = hero
    if item.get("feature_image_alt"):
        meta["hero_alt"] = item.get("feature_image_alt")
    if item.get("feature_image_caption"):
        meta["hero_caption"] = item.get("feature_image_caption")

    lines = ["---"]
    for key, value in meta.items():
        value = frontmatter_value(value)
        if value:
            lines.append(f"{key}: {value}")
    lines.extend(["---", "", html_body, ""])
    (target_dir / f"{item['slug']}.html").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    image_map: dict[str, str] = {}

    posts = fetch_json(f"{API}/posts/?key={KEY}&limit=all&include=tags,authors&formats=html,plaintext")
    pages = fetch_json(f"{API}/pages/?key={KEY}&limit=all&include=tags,authors&formats=html,plaintext")
    tags = fetch_json(f"{API}/tags/?key={KEY}&limit=all&include=count.posts")

    (RAW / "posts.json").write_text(json.dumps(posts, indent=2), encoding="utf-8")
    (RAW / "pages.json").write_text(json.dumps(pages, indent=2), encoding="utf-8")
    (RAW / "tags.json").write_text(json.dumps(tags, indent=2), encoding="utf-8")

    if IMAGES.exists():
        shutil.rmtree(IMAGES)
    IMAGES.mkdir(parents=True, exist_ok=True)

    for item in posts.get("posts", []):
        write_item(item, "post", image_map)
    for item in pages.get("pages", []):
        write_item(item, "page", image_map)

    (RAW / "image-map.json").write_text(
        json.dumps(image_map, indent=2, sort_keys=True), encoding="utf-8"
    )
    print(
        f"Imported {len(posts.get('posts', []))} posts, "
        f"{len(pages.get('pages', []))} pages, {len(image_map)} images."
    )


if __name__ == "__main__":
    main()
