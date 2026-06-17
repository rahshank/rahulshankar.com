# GitHub Pages Deployment Notes

## Purpose
Keep the operational runbook for publishing `rahulshankar.com` from local static files through GitHub Pages.

This page is for deployment mechanics: the local build path, the tracked `docs/` output, GitHub Pages settings, custom-domain records, and the few recovery details that matter if the site stops resolving cleanly. Site voice, visual direction, content backlog, and experiments live elsewhere in `workbench/`.

## Working model
Use GitHub Pages as a static file host, not as the authoring system.

The source of truth remains:
- local source files in `source/`
- local scripts in `scripts/`
- local generated output in `public/`
- GitHub Pages output in `docs/`
- raw public Ghost API exports in `raw/ghost-public/`

GitHub's role is to serve finished files. Squarespace's role is to keep owning/renewing the domain and managing DNS unless Rahul later moves the domain or nameservers.

## Current update path
The live update path is:

1. Edit local source files in `source/`, supporting code in `scripts/`, or planning/research notes in `workbench/`.
2. Run `python3 scripts/build_site.py` to build `public/` for local preview.
3. Run `python3 scripts/check_site.py` and any relevant visual checks.
4. Run `python3 scripts/prepare_github_pages.py` to rebuild tracked `docs/` for `rahulshankar.com`.
5. Review with `git status` and `git diff`.
6. Commit the source changes plus generated `docs/` output.
7. Push `main` to `origin`.
8. GitHub Pages publishes from `main` and `/docs`.

Completion rule: for publishable site work, local build and local verification are interim states. A thread should end with the change live and checked on `rahulshankar.com`, or with a clear decision that the work is staying local for now.

The normal publish command sequence after review is:

```sh
git add path/to/changed-file
# If all modified tracked files belong to this publish slice, `git add -u` is acceptable.
git commit -m "Describe the site update"
git push origin main
```

This repo currently uses a simple `main`-branch publish model. Use a feature branch for larger visual experiments, risky generator changes, or anything Rahul wants to inspect without changing the live site. Keep exploratory code under `workbench/experiments/` until it is promoted.

Assume there may be parallel threads with local work in progress. Publishing should stage the current slice deliberately, not sweep in every changed or untracked file. Before committing:

1. Check `git status` for unrelated modified or untracked files.
2. Stage exact paths for the current slice.
3. Use `git add -u` only when every modified tracked file belongs in the publish.
4. Do not use `git add -A` when experiments, drafts, or generated prototype pages are present.

San Rafael is the current example: local `/san-rafael/` prototype files should remain unpublished until Rahul explicitly promotes that page.

## Custom domain
The public URL can still be `rahulshankar.com` or `www.rahulshankar.com`. The GitHub default URL, such as `username.github.io`, is only the underlying Pages address.

Current state: `rahulshankar.com` is the live custom domain for this GitHub Pages site. `docs/CNAME` should contain `rahulshankar.com`, and normal builds should use root-relative links.

GitHub's docs say the custom domain should be configured in the repository's Pages settings before changing DNS. They also recommend verifying the custom domain to reduce takeover risk.

For an apex domain like `rahulshankar.com`, GitHub Pages uses these `A` records:

| Type | Host | Value |
| --- | --- | --- |
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |

For `www.rahulshankar.com`, GitHub Pages uses a `CNAME` record pointing to the GitHub Pages default domain, such as `username.github.io`.

Original DNS check before cutover on 2026-06-06:

| Name | Current record | Meaning |
| --- | --- | --- |
| `rahulshankar.com` | A `178.128.137.126` | apex is not pointed at GitHub Pages |
| `www.rahulshankar.com` | CNAME `rahul-shankar.ghost.io.` | `www` is still pointed at Ghost |
| `rahulshankar.com` | no MX records returned | no visible apex mail routing from this DNS check, but preserve any email-related records visible in Squarespace |

## Squarespace implications
Because the domain was purchased through Squarespace:
- DNS changes happen in the Squarespace domain DNS settings unless nameservers are moved.
- Squarespace website-builder features are not required.
- Existing website records pointing to Ghost/Squarespace will eventually be replaced by GitHub Pages records.
- Email records must be preserved.

Do not delete MX records or email-related TXT/CNAME records unless intentionally changing email providers.

## Historical cutover path
The initial move from Ghost/Squarespace to GitHub Pages followed this sequence:

1. Build and inspect the local static site.
2. Create a GitHub repository for the site.
3. Store source files and generated output together for the first test.
4. Run `scripts/prepare_github_pages.py` to copy `public/` into `docs/`.
5. Configure GitHub Pages to publish from the `main` branch and `/docs` folder.
6. Review the temporary GitHub Pages URL.
7. Add the custom domain in GitHub Pages settings only after the temporary URL looks right.
8. Add or update Squarespace DNS records.
9. Wait for DNS and HTTPS to settle.
10. Only then consider cancelling Ghost/Squarespace website services.

For the temporary project URL `https://rahshank.github.io/rahulshankar.com/`, `docs/` was built with `SITE_BASE_PATH=rahulshankar.com`. The live custom-domain build uses root-relative paths and writes `docs/CNAME`.

The publish script now defaults to the live custom domain:

```sh
python3 scripts/prepare_github_pages.py
```

To intentionally prepare the old temporary GitHub Pages project URL, clear the custom domain and set the base path:

```sh
SITE_CUSTOM_DOMAIN= SITE_BASE_PATH=rahulshankar.com python3 scripts/prepare_github_pages.py
```

Do not use the temporary mode for normal publishing because `rahulshankar.com` is now the live site.

## Authentication path
Use the official GitHub CLI for the first push if it is available. If it is not installed globally, install a temporary local copy into `.tools/gh/` and keep `.tools/` out of Git.

This is preferred over pasting a token into chat because GitHub CLI supports a one-time browser/device authorization flow and then handles repository creation and pushing through Git's normal credential path.

## Sources
- GitHub Pages custom domains: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site
- Squarespace DNS warning about MX records: https://support.squarespace.com/hc/en-us/articles/205812378-Connecting-a-third-party-domain-to-your-Squarespace-site

## Change log
- 2026-06-17: Added the publishable-work completion rule so future threads do not treat local verification as done.
- 2026-06-17: Reframed the page as the live deployment runbook and moved the first-deployment material into historical cutover context.
- 2026-06-17: Added the current local-build-commit-push-GitHub Pages update path and branch guidance.
- 2026-05-30: Documented the temporary GitHub Pages base path.
- 2026-05-30: Created initial GitHub Pages deployment note.
