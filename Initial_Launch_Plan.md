# Initial Launch Plan

## Purpose
Get a small static version of `rahulshankar.com` onto GitHub Pages without touching the live domain yet.

## First public slice
Publish only enough to prove the pipeline:
- index page
- writing index
- `Ghosts of Bombay` article page
- RSS feed
- shared CSS

Leave out:
- full archive migration
- email signup
- member tracking
- custom search
- Squarespace DNS changes
- Ghost cancellation

## Current source pages
| Source | Public path | Role |
| --- | --- | --- |
| `source/pages/index.md` | `/` | spare personal homepage |
| `source/pages/about.md` | `/about/` | placeholder about page |
| `source/posts/ghosts-of-bombay.md` | `/ghosts-of-bombay/` | first article migration target |

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
- Should the full Ghosts of Bombay article be migrated by export, scrape, or manual source copy?

## Change log
- 2026-05-30: Created the first launch plan for index, Ghosts of Bombay, and GitHub Pages testing.
- 2026-05-30: Chose `/docs` as the first GitHub Pages publish folder to avoid a remote build workflow.
