# Initial Launch Plan

## Purpose
Get a small static version of `rahulshankar.com` onto GitHub Pages without touching the live domain yet.

## First public slice
Publish enough to prove the pipeline:
- index page
- writing index
- migrated public Ghost posts and pages
- RSS feed
- shared CSS

Leave out:
- drafts and private/member-only content
- email signup
- member tracking
- custom search
- Squarespace DNS changes
- Ghost cancellation

## Current source pages
| Source | Public path | Role |
| --- | --- | --- |
| `source/pages/index.md` | `/` | spare personal homepage |
| `source/pages/about.html` | `/about/` | migrated Ghost about page |
| `source/posts/*.html` | post slugs | migrated public Ghost posts |

## Test publish path
1. Build locally.
2. Check internal links.
3. Prepare standalone preview files.
4. Prepare GitHub Pages output in `docs/`.
5. Create a GitHub repository.
6. Push this folder to the repository.
7. In GitHub Pages settings, publish from the `main` branch and `/docs` folder.
8. Review the temporary GitHub Pages URL.
9. Iterate on copy and style.
10. Only after review, decide whether to point `rahulshankar.com` at GitHub Pages from Squarespace DNS.

## Repository decision
Preferred first test: publish source and generated output together in one repository.

Reason: the source and pipeline should travel with the site from the beginning. If the repository later becomes public and we want to hide drafts/private notes, split source and output then.

For the first GitHub Pages test, use native Pages publishing from `/docs`. This avoids GitHub Actions and keeps the build local.

Track `docs/` in Git because GitHub Pages will serve it. Ignore `public/` because it is only the local build output used before copying into `docs/`.

## Open questions before live-domain switch
- Which GitHub account should own the repository?
- Should the temporary repository be public or private?
- Should the live site use `rahulshankar.com` or `www.rahulshankar.com` as canonical?
- Which DNS records are currently used for email?
- Should drafts, private/member-only content, or subscriber data be exported manually from Ghost admin?

## Change log
- 2026-05-30: Created the first launch plan for index, Ghosts of Bombay, and GitHub Pages testing.
- 2026-05-30: Chose `/docs` as the first GitHub Pages publish folder to avoid a remote build workflow.
