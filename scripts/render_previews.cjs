#!/usr/bin/env node
const fs = require("fs/promises");
const path = require("path");
const { chromium } = require("playwright");

const root = path.resolve(__dirname, "..");
const publicDir = path.join(root, "public");
const previewDir = path.join(root, "previews");

const pages = [
  ["index.html", "home.png"],
  ["ghosts-of-bombay/index.html", "ghosts-of-bombay.png"],
  ["writing/index.html", "writing.png"],
  ["notebook/index.html", "notebook.png"],
];

async function htmlWithInlineCss(relativePath) {
  const htmlPath = path.join(publicDir, relativePath);
  const css = await fs.readFile(path.join(publicDir, "assets/site.css"), "utf8");
  const html = await fs.readFile(htmlPath, "utf8");
  return html.replace(
    '<link rel="stylesheet" href="/assets/site.css">',
    `<style>${css}</style>`
  );
}

async function main() {
  await fs.mkdir(previewDir, { recursive: true });
  const browser = await chromium.launch();
  try {
    const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
    for (const [source, output] of pages) {
      await page.setContent(await htmlWithInlineCss(source), {
        waitUntil: "load",
      });
      await page.screenshot({
        path: path.join(previewDir, output),
        fullPage: true,
      });
    }
  } finally {
    await browser.close();
  }
  console.log(`Rendered ${pages.length} previews into ${previewDir}`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
