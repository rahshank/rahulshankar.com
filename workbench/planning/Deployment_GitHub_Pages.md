# GitHub Pages Deployment Notes

## Purpose
Capture the likely first deployment path for the custom static site while keeping the source pipeline local and portable.

## Working model
Use GitHub Pages as a static file host, not as the authoring system.

The source of truth remains:
- local source files in `source/`
- local scripts in `scripts/`
- generated output in `public/`
- raw public Ghost API exports in `raw/ghost-public/`

GitHub's role is to serve finished files. Squarespace's role is to keep owning/renewing the domain and managing DNS unless Rahul later moves the domain or nameservers.

## Custom domain
The public URL can still be `rahulshankar.com` or `www.rahulshankar.com`. The GitHub default URL, such as `username.github.io`, is only the underlying Pages address.

GitHub's docs say the custom domain should be configured in the repository's Pages settings before changing DNS. They also recommend verifying the custom domain to reduce takeover risk.

For an apex domain like `rahulshankar.com`, GitHub Pages uses these `A` records:

| Type | Host | Value |
| --- | --- | --- |
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |

For `www.rahulshankar.com`, GitHub Pages uses a `CNAME` record pointing to the GitHub Pages default domain, such as `username.github.io`.

## Squarespace implications
Because the domain was purchased through Squarespace:
- DNS changes happen in the Squarespace domain DNS settings unless nameservers are moved.
- Squarespace website-builder features are not required.
- Existing website records pointing to Ghost/Squarespace will eventually be replaced by GitHub Pages records.
- Email records must be preserved.

Do not delete MX records or email-related TXT/CNAME records unless intentionally changing email providers.

## First deployment sequence
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

For the temporary project URL `https://rahshank.github.io/rahulshankar.com/`, `docs/` is built with `SITE_BASE_PATH=rahulshankar.com`. Before switching to the live custom domain, rebuild `docs/` without the base path so root-relative links point to `rahulshankar.com`.

## Authentication path
Use the official GitHub CLI for the first push if it is available. If it is not installed globally, install a temporary local copy into `.tools/gh/` and keep `.tools/` out of Git.

This is preferred over pasting a token into chat because GitHub CLI supports a one-time browser/device authorization flow and then handles repository creation and pushing through Git's normal credential path.

## Sources
- GitHub Pages custom domains: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site
- Squarespace DNS warning about MX records: https://support.squarespace.com/hc/en-us/articles/205812378-Connecting-a-third-party-domain-to-your-Squarespace-site

## Change log
- 2026-05-30: Documented the temporary GitHub Pages base path.
- 2026-05-30: Created initial GitHub Pages deployment note.
