# Personal Site

## Purpose
Explore and, if useful, build a more controlled replacement for Rahul's current Ghost-hosted personal site.

The emerging shape is a low-frequency living static site: not a paid membership business, not a frozen archive, and not a CMS-heavy publication workflow.

## Folder map
| Path | Role | Status |
| --- | --- | --- |
| `README.md` | Arena orientation and current migration thinking | current |
| `Website_Migration_Notes.md` | Working notes for architecture, migration, and decisions | working draft |
| `Website_Inspiration_Log.md` | Short table of reference sites and borrowable patterns | current |
| `Initial_Launch_Plan.md` | First publish slice and GitHub Pages test path | current |
| `Deployment_GitHub_Pages.md` | First deployment path and Squarespace DNS implications | working draft |
| `source/` | Local source files for pages, posts, and assets | working draft |
| `scripts/build_site.py` | Custom Python generator from source files to static output | working draft |
| `scripts/check_site.py` | Local generated-site link checker | working draft |
| `scripts/prepare_file_previews.py` | Creates standalone preview HTML files with CSS inlined | working draft |
| `scripts/prepare_github_pages.py` | Copies generated output into `docs/` for GitHub Pages | working draft |
| `scripts/render_previews.cjs` | Headless visual renderer for generated pages | working draft |
| `public/` | Local generated static website output | generated, ignored |
| `docs/` | GitHub Pages-ready generated output | generated, track for publish |
| `previews/` | Generated preview inputs/screenshots for visual inspection | generated |

## Current workflow
Run the builder from this folder:

```sh
python3 scripts/build_site.py
```

Check the generated site:

```sh
python3 scripts/check_site.py
```

Prepare standalone browser-preview files:

```sh
python3 scripts/prepare_file_previews.py
```

Prepare GitHub Pages output:

```sh
python3 scripts/prepare_github_pages.py
```

This builds `docs/` with the temporary GitHub Pages base path `/rahulshankar.com`. For the final custom-domain deployment, rebuild without `SITE_BASE_PATH`.

Render screenshots for visual inspection:

```sh
NODE_PATH=/Users/rahulshankar/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules /Users/rahulshankar/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node scripts/render_previews.cjs
```

Preview the generated site locally:

```sh
python3 -m http.server 8765 -d public
```

## Change log
- 2026-05-30: Created the personal-site arena from the Fieldwork board candidate thread.
- 2026-05-30: Added the first custom static-site source tree and Python builder.
- 2026-05-30: Added a local site checker and GitHub Pages deployment note.
- 2026-05-30: Added a headless preview renderer for visual verification.
- 2026-05-30: Added standalone browser-preview file generation after automated screenshot routes were blocked.
- 2026-05-30: Added initial launch plan for GitHub Pages test publishing.
- 2026-05-30: Added native GitHub Pages `docs/` output preparation.
- 2026-05-30: Added a short website inspiration log.
