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
| `workbench/research/Website_Inspiration_Log.md` | Short table of reference sites and borrowable patterns | current |
| `workbench/research/Homepage_Intro_Research.md` | Working surface for homepage/about intro directions | working draft |
| `workbench/research/Visual_Direction_Research.md` | Working surface for type, color, layout, and visual references | working draft |
| `workbench/README.md` | Workbench boundary and map | current |
| `scripts/build_site.py` | Custom Python generator from source files to static output | working draft |
| `scripts/check_site.py` | Local generated-site link checker | working draft |
| `scripts/import_ghost_public.py` | Imports public Ghost posts/pages and images into local source files | working draft |
| `scripts/prepare_file_previews.py` | Creates standalone preview HTML files with CSS inlined | working draft |
| `scripts/prepare_github_pages.py` | Copies generated output into `docs/` for GitHub Pages | working draft |
| `scripts/render_previews.cjs` | Headless visual renderer for generated pages | working draft |

## Path chosen
This site currently uses a small custom static pipeline:

| Choice | Why |
| --- | --- |
| Local source files in `source/` | keeps writing and assets editable without a CMS |
| Custom Python builder | enough control for the current site without adopting Astro, Eleventy, or a larger framework yet |
| Public Ghost importer | preserves the old public archive and images from Ghost while moving the working copy local |
| Generated `docs/` output | lets GitHub Pages publish without GitHub Actions for the first version |
| GitHub Pages temporary URL | gives a safe preview before changing `rahulshankar.com` DNS in Squarespace |
| `workbench/` notes | keeps planning and inspiration close to the project without mixing them with source/build files |
| `public/` and `previews/` ignored | local outputs can be regenerated and should not clutter commits |

The likely next structural addition is `source/notes/` plus a generated `/notes/` index if Rahul wants a public notebook section for short observations.

## Information architecture
The current target navigation is:

| Section | Role |
| --- | --- |
| `Writing` | Longer essays and the migrated Ghost archive |
| `Notebook` | Shorter field notes, observations, travel notes, aesthetic notes, and public fragments from Fieldwork |
| `About` | Current intro, biography, and project orientation |

`A week in Beijing` is the first likely reclassification candidate: it reads more like a field note or travel note than a formal essay, so it should probably live in `Notebook` once that section exists.

## Current workflow
Run the builder from this folder:

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
- 2026-05-30: Added public Ghost content importer.
- 2026-05-30: Added intro and visual direction research surfaces.
- 2026-05-30: Moved planning and research notes into `workbench/` and documented the path choices.
