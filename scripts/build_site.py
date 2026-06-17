#!/usr/bin/env python3
from __future__ import annotations

import html
import os
import re
import shutil
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"
PUBLIC = ROOT / "public"
SITE_TITLE = "Rahul Shankar"
SITE_URL = "https://rahulshankar.com"
BASE_PATH = os.environ.get("SITE_BASE_PATH", "").strip("/")

THEME_BOOT_SCRIPT = """  <script>
    (function () {
      try {
        var savedTheme = localStorage.getItem("site-theme");
        var prefersNight = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
        document.documentElement.dataset.theme = savedTheme || (prefersNight ? "night" : "day");
      } catch (error) {
        document.documentElement.dataset.theme = "day";
      }
    })();
  </script>"""

THEME_CONTROL_SCRIPT = """  <script>
    (function () {
      var root = document.documentElement;
      var button = document.querySelector("[data-theme-toggle]");
      var icon = document.querySelector("[data-theme-toggle-icon]");
      var media = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;

      function applyTheme(theme, persist) {
        root.dataset.theme = theme;
        if (persist) {
          localStorage.setItem("site-theme", theme);
        }
        if (!button || !icon) {
          return;
        }
        var isNight = theme === "night";
        icon.textContent = isNight ? "☀" : "☾";
        button.setAttribute("aria-pressed", String(isNight));
        button.setAttribute("aria-label", isNight ? "Switch to daytime" : "Switch to nighttime");
        button.setAttribute("title", isNight ? "Switch to daytime" : "Switch to nighttime");
      }

      applyTheme(root.dataset.theme || "day", false);

      if (button) {
        button.addEventListener("click", function () {
          applyTheme(root.dataset.theme === "night" ? "day" : "night", true);
        });
      }

      if (media) {
        media.addEventListener("change", function (event) {
          if (!localStorage.getItem("site-theme")) {
            applyTheme(event.matches ? "night" : "day", false);
          }
        });
      }
    })();
  </script>"""


def site_path(path: str) -> str:
    if path.startswith(("http://", "https://", "mailto:", "#")):
        return path
    normalized = "/" + path.lstrip("/")
    if not BASE_PATH:
        return normalized
    return f"/{BASE_PATH}{normalized}"


def normalize_url(url: str) -> str:
    if url.startswith(("http://", "https://", "mailto:", "#")):
        return url
    if url.startswith("//"):
        return f"https:{url}"
    if BASE_PATH and url.startswith(f"/{BASE_PATH}/"):
        return url
    if re.match(r"^[A-Za-z0-9.-]+\.[A-Za-z]{2,}(/.*)?$", url):
        return f"https://{url}"
    if url.startswith("/"):
        return site_path(url)
    return url


def normalize_html_urls(html_text: str) -> str:
    def replace_attr(match: re.Match[str]) -> str:
        attr = match.group(1)
        quote = match.group(2)
        url = match.group(3)
        return f"{attr}={quote}{normalize_url(url)}{quote}"

    def replace_srcset(match: re.Match[str]) -> str:
        quote = match.group(1)
        value = match.group(2)
        pieces = []
        for item in value.split(","):
            bits = item.strip().split()
            if not bits:
                continue
            bits[0] = normalize_url(bits[0])
            pieces.append(" ".join(bits))
        return f"srcset={quote}{', '.join(pieces)}{quote}"

    html_text = re.sub(r"\b(href|src)=(['\"])([^'\"]+)\2", replace_attr, html_text)
    html_text = re.sub(r"\bsrcset=(['\"])([^'\"]+)\1", replace_srcset, html_text)
    return html_text


@dataclass
class Document:
    source_path: Path
    meta: Dict[str, str]
    body: str
    html_body: str

    @property
    def title(self) -> str:
        return self.meta.get("title", "Untitled")

    @property
    def slug(self) -> str:
        slug = self.meta.get("slug", self.source_path.stem).strip("/")
        return slug

    @property
    def url_path(self) -> str:
        return "/" if self.slug == "" else f"/{self.slug}/"


def parse_document(path: Path) -> Document:
    raw = path.read_text(encoding="utf-8")
    meta: Dict[str, str] = {}
    body = raw
    if raw.startswith("---\n"):
        _, frontmatter, body = raw.split("---\n", 2)
        for line in frontmatter.splitlines():
            if not line.strip() or line.strip().startswith("#"):
                continue
            if ":" not in line:
                raise ValueError(f"Invalid frontmatter line in {path}: {line}")
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip()
    body = body.strip()
    body_format = meta.get("body_format", "").lower()
    html_body = body if body_format == "html" or path.suffix == ".html" else markdown_to_html(body)
    html_body = normalize_html_urls(html_body)
    return Document(path, meta, body, html_body)


def markdown_to_html(markdown: str) -> str:
    blocks = re.split(r"\n\s*\n", markdown.strip()) if markdown.strip() else []
    rendered: List[str] = []
    for block in blocks:
        lines = block.splitlines()
        first = lines[0].strip()
        if first.startswith("## "):
            rendered.append(f"<h2>{inline(first[3:].strip())}</h2>")
        elif first.startswith("# "):
            rendered.append(f"<h1>{inline(first[2:].strip())}</h1>")
        elif first in {"---", "***"}:
            rendered.append("<hr>")
        elif all(line.strip().startswith("- ") for line in lines):
            items = "\n".join(
                f"<li>{inline(line.strip()[2:].strip())}</li>" for line in lines
            )
            rendered.append(f"<ul>\n{items}\n</ul>")
        elif all(re.match(r"^\d+\\.\\s+", line.strip()) for line in lines):
            cleaned = [re.sub(r"^\d+\\.\\s+", "", line.strip()) for line in lines]
            items = "\n".join(f"<li>{inline(item)}</li>" for item in cleaned)
            rendered.append(f"<ol>\n{items}\n</ol>")
        elif all(line.strip().startswith(">") for line in lines):
            quote = " ".join(line.strip().lstrip(">").strip() for line in lines)
            rendered.append(f"<blockquote><p>{inline(quote)}</p></blockquote>")
        else:
            paragraph = " ".join(line.strip() for line in lines)
            rendered.append(f"<p>{inline(paragraph)}</p>")
    return "\n".join(rendered)


def inline(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda m: f'<a href="{html.escape(site_path(m.group(2)), quote=True)}">{m.group(1)}</a>',
        escaped,
    )
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    return escaped


def page_shell(title: str, content: str, path: str = "/", description: str = "") -> str:
    full_title = SITE_TITLE if title == SITE_TITLE else f"{title} - {SITE_TITLE}"
    desc = html.escape(description or "Personal website of Rahul Shankar.", quote=True)
    canonical = f"{SITE_URL}{path}" if path != "/" else SITE_URL
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(full_title)}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{canonical}">
  <link rel="alternate" type="application/rss+xml" title="{SITE_TITLE}" href="{site_path("/rss.xml")}">
{THEME_BOOT_SCRIPT}
  <link rel="stylesheet" href="{site_path("/assets/site.css")}">
</head>
<body>
  <div class="site">
    <header class="masthead">
      <a class="brand" href="{site_path("/")}">Rahul Shankar</a>
      <div class="masthead-actions">
        <nav class="nav" aria-label="Primary">
          <a href="{site_path("/writing/")}">Writing</a>
          <a href="{site_path("/notebook/")}">Notebook</a>
          <a href="{site_path("/about/")}">About</a>
        </nav>
        <button class="theme-toggle" type="button" data-theme-toggle aria-pressed="false" aria-label="Switch to nighttime" title="Switch to nighttime">
          <span class="theme-toggle-icon" data-theme-toggle-icon aria-hidden="true">☾</span>
        </button>
      </div>
    </header>
    {content}
    <footer class="footer">Rahul Shankar</footer>
  </div>
{THEME_CONTROL_SCRIPT}
</body>
</html>
"""


def render_home(doc: Document, entries: List[Document]) -> str:
    content = f"""
<main>
  <h1>{html.escape(doc.title)}</h1>
  {doc.html_body}
</main>
"""
    return page_shell(doc.title, content, doc.url_path, doc.meta.get("summary", ""))


def render_page(doc: Document) -> str:
    content = f"""
<main>
  <h1>{html.escape(doc.title)}</h1>
  {doc.html_body}
</main>
"""
    return page_shell(doc.title, content, doc.url_path, doc.meta.get("summary", ""))


def render_article(doc: Document) -> str:
    topics = doc.meta.get("topics", "")
    meta_bits = [doc.meta.get("date", ""), topics]
    meta_line = " · ".join(bit for bit in meta_bits if bit)
    hero = ""
    if doc.meta.get("hero_image"):
        hero = (
            f'<img class="hero-image" src="{html.escape(site_path(doc.meta["hero_image"]), quote=True)}" '
            f'alt="{html.escape(doc.meta.get("hero_alt", doc.title), quote=True)}">'
        )
        if doc.meta.get("hero_caption"):
            hero += f'\n  <p class="caption">{html.escape(doc.meta["hero_caption"])}</p>'
    content = f"""
<article>
  <p class="meta">{html.escape(meta_line)}</p>
  <h1 class="article-title">{html.escape(doc.title)}</h1>
  {hero}
  {doc.html_body}
</article>
"""
    return page_shell(doc.title, content, doc.url_path, doc.meta.get("summary", ""))


def render_visual_note(doc: Document) -> str:
    topics = doc.meta.get("topics", "")
    meta_bits = [doc.meta.get("date", ""), topics]
    meta_line = " · ".join(bit for bit in meta_bits if bit)
    content = f"""
<article class="visual-note">
  <p class="meta">{html.escape(meta_line)}</p>
  <h1 class="article-title">{html.escape(doc.title)}</h1>
  {doc.html_body}
</article>
"""
    return page_shell(doc.title, content, doc.url_path, doc.meta.get("summary", ""))


def write_output(doc: Document, html_text: str) -> None:
    if doc.slug == "":
        out = PUBLIC / "index.html"
    else:
        out = PUBLIC / doc.slug / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html_text, encoding="utf-8")


def copy_assets() -> None:
    src = SOURCE / "assets"
    dst = PUBLIC / "assets"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def render_collection_index(
    title: str,
    slug: str,
    description: str,
    entries: List[Document],
) -> None:
    items = "\n".join(
        f'<li><a href="{site_path(entry.url_path)}">{html.escape(entry.title)}</a>'
        f' <span class="meta">{html.escape(entry.meta.get("date", ""))}</span>'
        f'<p>{html.escape(entry.meta.get("summary", ""))}</p></li>'
        for entry in sorted(entries, key=lambda item: item.meta.get("date", ""), reverse=True)
    )
    content = f"""
<main>
  <h1>{html.escape(title)}</h1>
  <ul>{items}</ul>
</main>
"""
    out = PUBLIC / slug / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        page_shell(title, content, f"/{slug}/", description),
        encoding="utf-8",
    )


def render_rss(entries: List[Document]) -> None:
    items = "\n".join(
        f"""  <item>
    <title>{html.escape(entry.title)}</title>
    <link>{SITE_URL}{entry.url_path}</link>
    <guid>{SITE_URL}{entry.url_path}</guid>
    <pubDate>{html.escape(entry.meta.get("date", ""))}</pubDate>
    <description>{html.escape(entry.meta.get("summary", ""))}</description>
  </item>"""
        for entry in sorted(entries, key=lambda item: item.meta.get("date", ""), reverse=True)
    )
    rss = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
  <title>{SITE_TITLE}</title>
  <link>{SITE_URL}</link>
  <description>Writing and projects by Rahul Shankar.</description>
  <lastBuildDate>{date.today().isoformat()}</lastBuildDate>
{items}
</channel>
</rss>
"""
    (PUBLIC / "rss.xml").write_text(rss, encoding="utf-8")


def load_documents(paths: Iterable[Path]) -> List[Document]:
    return [parse_document(path) for path in sorted(paths)]


def main() -> None:
    if PUBLIC.exists():
        shutil.rmtree(PUBLIC)
    PUBLIC.mkdir()
    copy_assets()

    pages = load_documents(
        list((SOURCE / "pages").glob("*.md")) + list((SOURCE / "pages").glob("*.html"))
    )
    posts = load_documents(
        list((SOURCE / "posts").glob("*.md")) + list((SOURCE / "posts").glob("*.html"))
    )
    notes = load_documents(
        list((SOURCE / "notes").glob("*.md")) + list((SOURCE / "notes").glob("*.html"))
    )
    entries = posts + notes

    for page in pages:
        template = page.meta.get("template", "page")
        if template == "home":
            html_text = render_home(page, entries)
        elif template == "visual_note":
            html_text = render_visual_note(page)
        else:
            html_text = render_page(page)
        write_output(page, html_text)

    for post in posts:
        write_output(post, render_visual_note(post) if post.meta.get("template") == "visual_note" else render_article(post))
    for note in notes:
        write_output(note, render_visual_note(note) if note.meta.get("template") == "visual_note" else render_article(note))

    render_collection_index("Writing", "writing", "Writing by Rahul Shankar.", posts)
    render_collection_index(
        "Notebook",
        "notebook",
        "Field notes, observations, and shorter public fragments by Rahul Shankar.",
        notes,
    )
    render_rss(entries)
    print(f"Built {len(pages)} pages, {len(posts)} posts, and {len(notes)} notes into {PUBLIC}")


if __name__ == "__main__":
    main()
