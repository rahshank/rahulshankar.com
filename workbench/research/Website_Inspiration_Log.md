# Website Inspiration Log

## Purpose
Keep a short reference table of sites worth borrowing from while building Rahul's static personal site.

## Sites
| Site | URL | What to Notice | Build / Hosting Clue | Possible Borrowing |
| --- | --- | --- | --- | --- |
| Ribbonfarm / VGR | https://ribbonfarm.com | Static archive with preserved corpus, custom generator, archive navigation, tags, series, and later AI/search layers. | Public dev log says WordPress exports were preserved, a custom Python generator builds static HTML, media lives on Cloudflare R2, and the site is hosted on Cloudflare Pages. | Own the corpus; generate static files; add richer archive/search layers only after the base site works. |
| Michael's Notebook | https://michaelnotebook.com | Pandoc-generated, text-first intellectual map with simple CSS and direct links. | Public HTML has `generator` set to Pandoc; response headers show GitHub Pages serving the static output. | Keep the first homepage spare, readable, and index-like. |
| Andy Matuschak | https://andymatuschak.org | Bespoke static-exported personal/project index with strong project grouping. | Public HTML exposes a Next.js static export (`nextExport`) served as static assets; headers show an Apache server. | Treat the homepage as a map of work, not a chronological blog feed. |
| Andy's working notes | https://notes.andymatuschak.org | Public interface over a private thinking system, with note links and stacked reading paths. | Public HTML embeds note JSON and loads a bundled JavaScript app from `/assets/main.js`; hosting headers suggest static/CDN delivery. | Possible later direction for Fieldwork-derived public notes, not the first launch. |
| Interconnected / Matt Webb | https://interconnected.org/home/2024/10/11/filtered | Old-web blog density plus a slow changing pastel page background. Sidebar links, RSS, dated posts, tags, follow-ups, related posts, recent posts, archive, and start-here paths all make the site feel lived-in. | Public page is plain server-rendered/static-looking HTML with Tachyons, a custom CSS file, Fathom analytics, RSS, Cloudflare, and a ten-minute CSS `@keyframes` background animation on `body.container.blog`. | Add simple durable navigation around posts; consider a slow theme-color cycle for notebook or field-note pages when it serves the mood rather than decoration. |
| Drew Coffman | https://drewcoffman.com | Simple personal homepage with a small persistent light/dark mode control. | Static-looking HTML/CSS/JS: the toggle changes a wrapper class, stores the choice in `localStorage`, and updates the icon in place. | Add a small day/night setting without changing the site into an app-like interface. |
| Current Rahul Ghost site | https://rahulshankar.com | Existing title/date/tag/article shape plus Ghost furniture we want to remove. | Public HTML reports Ghost 6.42 and loads Ghost Portal, member attribution, search, theme CSS, RSS, structured metadata, and Ghost-hosted media. | Preserve URLs, titles, dates, tags, excerpts, images, and article rhythm while dropping CMS/member/search scripts. |

## Change log
- 2026-06-16: Added Drew Coffman as the reference for a small persistent day/night setting.
- 2026-06-07: Updated Interconnected with the inspected CSS color-cycle clue.
- 2026-05-30: Added one-sentence build/hosting clues for each inspiration site.
- 2026-05-30: Created initial inspiration log and added VGR, Michael Nielsen, Andy Matuschak, Interconnected, and Rahul's current site.
