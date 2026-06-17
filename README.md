# Personal Site

## Purpose
Explore and, if useful, build a more controlled replacement for Rahul's current Ghost-hosted personal site.

The emerging shape is a low-frequency living static site: not a paid membership business, not a frozen archive, and not a CMS-heavy publication workflow.

## Folder map
| Path | Role | Status |
| --- | --- | --- |
| `README.md` | Arena orientation and current migration thinking | current |
| `source/` | Local source files for pages, posts, notes, and assets | working draft |
| `scripts/` | Site builder, importers, link checks, and preview helpers | working draft |
| `raw/ghost-public/` | Raw public Ghost API exports used by the importer | reference |
| `docs/` | GitHub Pages-ready generated output | generated, tracked for publish |
| `public/` | Local generated static website output | generated, ignored |
| `previews/` | Generated preview inputs/screenshots for visual inspection | generated, ignored |
| `workbench/` | Planning, research, and decision notes for the site | working |
| `workbench/planning/Website_Migration_Notes.md` | Working notes for architecture, migration, and decisions | working draft |
| `workbench/planning/Initial_Launch_Plan.md` | First publish slice and GitHub Pages test path | current |
| `workbench/planning/Deployment_GitHub_Pages.md` | First deployment path and Squarespace DNS implications | working draft |
| `workbench/experiments/` | Site implementation experiments and prototypes | working |
| `workbench/research/Website_Inspiration_Log.md` | Short table of reference sites and borrowable patterns | current |
| `workbench/research/Homepage_Intro_Research.md` | Working surface for homepage/about intro directions | working draft |
| `workbench/research/Visual_Direction_Research.md` | Working surface for type, color, layout, and visual references | working draft |
| `workbench/README.md` | Workbench boundary and map | current |
| `scripts/build_site.py` | Custom Python generator from source files to static output | working draft |
| `scripts/check_site.py` | Local generated-site link checker | working draft |
| `scripts/import_ghost_public.py` | Imports public Ghost posts/pages and images into local source files | working draft |
| `scripts/prepare_file_previews.py` | Creates standalone preview HTML files with CSS inlined | working draft |
| `scripts/prepare_github_pages.py` | Copies generated output into `docs/` for GitHub Pages | working draft |
| `scripts/render_previews.cjs` | Older single-browser preview renderer for generated pages | candidate for replacement |

## Path chosen
This site currently uses a small custom static pipeline:

| Choice | Why |
| --- | --- |
| Local source files in `source/` | keeps writing and assets editable without a CMS |
| Custom Python builder | enough control for the current site without adopting Astro, Eleventy, or a larger framework yet |
| Public Ghost importer | preserves the old public archive and images from Ghost while moving the working copy local |
| Generated `docs/` output | lets GitHub Pages publish without GitHub Actions for the first version |
| GitHub Pages with custom domain | serves the tracked `docs/` output at `rahulshankar.com` |
| `workbench/` notes | keeps planning and inspiration close to the project without mixing them with source/build files |
| `public/` and `previews/` ignored | local outputs can be regenerated and should not clutter commits |

The site now has `source/notes/` plus a generated `/notebook/` index for short observations, travel notes, and public field notes.

## Information architecture
The current target navigation is:

| Section | Role |
| --- | --- |
| `Writing` | Longer essays and the migrated Ghost archive |
| `Notebook` | Shorter field notes, observations, travel notes, aesthetic notes, and public fragments from Fieldwork |
| `About` | Current intro, biography, and project orientation |

`A week in Beijing` now lives in `Notebook` while keeping its original `/beijing/` URL.

## Current workflow
The update path is:

`local source -> generated static site -> GitHub commit/push -> GitHub Pages -> rahulshankar.com`

GitHub is the publishing host, not the writing interface. The source of truth stays in this folder.

For a normal edit:

1. Change files under `source/`, `scripts/`, or `workbench/`.
2. Build the local site.
3. Preview and check the generated site.
4. Prepare `docs/`, which is the GitHub Pages output folder.
5. Review the Git diff.
6. Commit and push `main`.
7. GitHub Pages serves the updated `docs/` output at `rahulshankar.com`.

Small content/style changes can go straight to `main`. Larger experiments should use a branch or stay under `workbench/experiments/` until they are ready.

Assume parallel threads may be working in this folder. Before publishing, check for unrelated local work and stage only the files that belong to the current publish slice. Do not use `git add -A` or broad folder staging when untracked experiments are present. San Rafael and other field-note prototypes should stay local until they are explicitly promoted.

Run the local builder from this folder:

```sh
python3 scripts/build_site.py
```

Refresh public Ghost content:

```sh
python3 scripts/import_ghost_public.py
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

This builds `docs/` for the live custom domain, including `docs/CNAME` for `rahulshankar.com`.

Publish after review:

```sh
git status
git diff
git add path/to/changed-file
# If all modified tracked files belong to this publish slice, `git add -u` is acceptable.
git commit -m "Describe the site update"
git push origin main
```

GitHub Pages is configured to publish from the `main` branch and `/docs` folder.

Run repeatable browser checks and screenshots from the workspace root:

```sh
.tools/bin/fieldwork-ui check personal-site
```

This checks the generated site with Playwright across Chromium, Firefox, and WebKit at desktop and mobile viewport sizes. Screenshots and the latest JSON report are written to `automation/ui-testing/artifacts/personal-site/`.

Preview the generated site locally:

```sh
python3 -m http.server 8765 -d public
```

## Change log
- 2026-06-17: Added the local-to-GitHub-to-public-site update path and branch guidance.
- 2026-06-07: Added `workbench/experiments/` to the site folder map.
- 2026-06-06: Switched the recommended screenshot workflow to the workspace-level Playwright runner.
- 2026-05-30: Created the personal-site arena from the Fieldwork board candidate thread.
- 2026-05-30: Added the first custom static-site source tree and Python builder.
- 2026-05-30: Added a local site checker and GitHub Pages deployment note.
- 2026-05-30: Added a headless preview renderer for visual verification.
- 2026-05-30: Added standalone browser-preview file generation after automated screenshot routes were blocked.
- 2026-05-30: Added initial launch plan for GitHub Pages test publishing.
- 2026-05-30: Added native GitHub Pages `docs/` output preparation.
- 2026-05-30: Added a short website inspiration log.
- 2026-05-30: Added public Ghost content importer.
- 2026-05-30: Added intro and visual direction research surfaces.
- 2026-05-30: Moved planning and research notes into `workbench/` and documented the path choices.
- 2026-05-30: Added `Notebook` and moved `A week in Beijing` into `source/notes/`.
