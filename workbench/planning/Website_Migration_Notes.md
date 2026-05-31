# Website Migration Notes

## Purpose
Keep the personal website migration lightweight while the shape is still forming.

## Current intent
Rahul wants more control than Ghost provides, without taking on Ghost's editor and publication machinery. The site should remain updateable, but updates will likely be occasional rather than frequent.

The desired shape is a living static site:
- owned source files
- durable URLs
- simple publishing workflow
- low hosting and maintenance burden
- no paid membership system
- subscriber/member tracking kept separately at first
- minimal subscribed services
- Codex can do much of the conversion, maintenance, and publishing work that would otherwise justify a CMS

## VGR-inspired model
Venkatesh Rao's current ecosystem separates functions rather than forcing one site to do everything:
- simple personal landing page at `venkateshrao.com`
- current writing in Contraptions
- Ribbonfarm as a static archive with rich navigation
- search and AI layers added separately over the corpus
- project worlds such as Summer of Protocols and World Machines as distinct surfaces

For Rahul, the transferable idea is not to copy Ribbonfarm's archive exactly. It is to build an owned hub that can support a public writing archive and a few project worlds without needing a live CMS.

## VGR's static publishing pipeline
Confirmed from Ribbonfarm's public dev log:
- Source materials were exported from the old WordPress site: XML export, full media library, MySQL dump, and old theme files.
- Source materials were kept read-only.
- Editable copies became the working source.
- A custom Python static site generator, `build_site.py`, generated the site.
- Posts and pages were stored as `.html` files with YAML frontmatter plus the original HTML body.
- The pipeline was non-lossy: the archive kept old content intact rather than translating everything into a new writing format.
- Images were served separately from Cloudflare R2 at `media.ribbonfarm.com`.
- The static site was hosted on Cloudflare Pages by direct upload.
- The build was designed to be reproducible from source, with rebuild instructions in `CLAUDE.md`.
- The workflow was iterative AI-assisted sessions: build, review, fix, deploy.

For Rahul, the key transferable pattern is a custom reproducible pipeline, not the exact archive format.

## Desired Rahul pipeline
The desired pipeline is:

1. Rahul and Codex draft or revise a piece locally.
2. The piece lives as a durable source file in the Fieldwork/personal-site system.
3. A publish script converts it into website content with frontmatter, slug, tags, dates, and any needed assets.
4. A build script regenerates the static site.
5. A preview step checks the local site.
6. A deploy step publishes to `rahulshankar.com`.

This avoids a live CMS editor while keeping publishing easy enough for occasional updates.

## Minimal-services principle
Get as close to basic internet primitives as practical:
- a domain name
- static files
- DNS
- optional object storage for media if needed
- versioned local source files
- a deploy command

Avoid services whose main value is a UI layer that Rahul does not want to use often. If Codex can reliably perform the transformation or maintenance work, prefer local scripts and explicit files over a subscription CMS.

## Hosting dependency ladder
There is no truly service-free public website unless Rahul runs the server. The goal is to choose the smallest dependency that serves static files without owning the publishing workflow.

From least to most operational burden:
- Managed static host: Cloudflare Pages/Workers static assets, GitHub Pages, SourceHut Pages, Netlify. Easy, but still platform-dependent.
- Old-school shared web hosting: upload static files over SFTP/SCP/rsync-like workflow. Less "website builder," more basic file hosting.
- Object storage plus CDN: good for media/static assets, but custom-domain HTTPS can add complexity depending on provider.
- VPS with NGINX/OpenBSD httpd/Caddy: closest to first principles, but Rahul owns server updates, TLS, security, monitoring, and breakage.
- Home server: philosophically pure, practically annoying for uptime, ISP/router/TLS/security reasons.

Likely direction: start with custom local generator plus either old-school shared hosting or a managed static host with direct upload. Keep the site portable so the host can be swapped later.

## Domain situation
Rahul's domain was purchased through Squarespace. This does not require using Squarespace's website builder.

The domain setup has separable layers:
- Registrar: where `rahulshankar.com` is owned and renewed. Currently Squarespace.
- DNS: the records that point `rahulshankar.com` and `www.rahulshankar.com` to a host. Likely managed in Squarespace unless nameservers are moved.
- Host: the service that serves the static website files. Candidate: GitHub Pages, Cloudflare Pages, or old-school static hosting.
- Source/pipeline: local files and scripts in Fieldwork. This should remain independent of the host.

If using GitHub Pages, the custom domain can still be `rahulshankar.com` or `www.rahulshankar.com`; the `github.io` URL is only the default/underlying address. Squarespace DNS would need GitHub Pages records instead of Ghost/Squarespace website records.

Important caution: preserve any MX/TXT records used for email before changing DNS.

## Likely architecture
Build `rahulshankar.com` as a static site generated from local files.

Candidate stack:
- Custom Python generator as the first serious candidate
- Markdown or MDX for posts and pages
- Cloudflare Pages for hosting
- Ghost export as the migration source
- subscriber/member list as CSV or spreadsheet outside the site

## Site shape
Possible top-level areas:
- Writing: longer essays and migrated Ghost posts
- Notebook: short observations, field notes, travel notes, aesthetic notes, and public fragments from Fieldwork
- About: current intro, biography, and project orientation

This gives the site a useful distinction between finished essays and public notes. `A week in Beijing` is the first likely reclassification candidate because it functions more like a field note/travel note than a formal essay.

## First recreation target
Use `Ghosts of Bombay` as the first article-page test because it has the core ingredients:
- author/date/topic metadata
- title
- hero image with caption
- essay body
- blockquote
- previous/next issue links
- simple footer

The current Ghost page also includes sign-in/subscribe UI and "Powered by Ghost" furniture. The static version should omit Ghost-specific furniture and replace subscription with either nothing, a simple "updates" link, or a manually managed email/contact path.

The first prototype should prove:
- `rahulshankar.com` can have a clean intro/home page
- `/ghosts-of-bombay/` can render as a durable static article
- source files can be edited locally with Codex
- a build script can generate the public HTML
- the visual style can be personal and calm without becoming a site-builder template

## Bespoke-site references
Public inspection suggests a useful spectrum:

- Michael Nielsen's `michaelnotebook.com` is generated by Pandoc and served by GitHub Pages. It is basically an intellectual index: mostly text, links, tags, sections, and a small amount of CSS. It uses Google Analytics and an external Substack mailing-list link.
- Andy Matuschak's main site is a statically exported Next.js site: built React output, static assets, and an external mailing-list endpoint. It is bespoke in presentation, but the public site is still static output.
- Andy's working notes are a custom note environment. The HTML includes embedded JSON note data and loads a bundled JavaScript app from `/assets/main.js`; the note content is Markdown-like with custom wiki-link syntax. It is not just a blog, but a public interface over a thinking system.
- Rahul's current Ghost article pages are Ghost-generated HTML with Ghost theme CSS, Ghost Portal/members script, Ghost search, RSS, structured metadata, and media hosted on Ghost storage.

Takeaway: the people with bespoke sites are often not avoiding generated sites. They are avoiding generic authoring interfaces. Their public websites are still build artifacts from some private source/process.

Optional later layers:
- RSS
- lightweight search
- curated reading paths
- corpus map
- AI/search interface, only if the writing archive becomes large enough to deserve it

## Open decisions
- Should the first version use Astro, Eleventy, or a tiny custom generator?
- Should old Ghost posts be converted into Markdown/MDX or preserved as HTML-with-frontmatter?
- Should email signup be removed, replaced with a simple form, or pointed to a separate newsletter/list tool?
- Should `Ghosts of Bombay` be a project page, a topic page, or its own mini-site later?
- What should the authoring source format be for new posts: Markdown, MDX, HTML-with-frontmatter, or a simple structured note that the pipeline converts?
- Should existing migrated posts be reclassified manually into `Writing` and `Notebook`, starting with `A week in Beijing`?

## Change log
- 2026-05-30: Captured the low-frequency living static site direction.
- 2026-05-30: Added the custom publishing pipeline as the core project shape.
- 2026-05-30: Identified `Ghosts of Bombay` as the first static article recreation target.
- 2026-05-30: Added minimal-services hosting dependency ladder.
- 2026-05-30: Added public-code inspection notes for Michael Nielsen and Andy Matuschak reference sites.
- 2026-05-30: Captured Squarespace-owned domain implications for GitHub/Cloudflare static hosting.
- 2026-05-30: Added the first local build pipeline. The broader working principle moved to workspace `AGENTS.md`.
- 2026-05-30: Added GitHub Pages deployment notes and a local generated-site checker.
- 2026-05-30: Added a headless preview renderer after local server and in-app browser preview paths failed.
- 2026-05-30: Added standalone preview HTML generation as the fallback visual verification path.
- 2026-05-30: Captured target navigation as Writing / Notebook / About, with `A week in Beijing` as a likely Notebook item.
