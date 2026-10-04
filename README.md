# Fuse Worship

The website and brand for **Fuse Worship** and **Fuse Kids**, a worship ministry led by Pastor Daniel Martins. All songs are in EN, ES and PT.

## Website (fuseworship.com, on Cloudflare Pages)
- Static pages are committed at the repo root: `index.html` (EN), `es/index.html` and `pt/index.html`, plus `sitemap.xml`, `robots.txt`, `favicon.svg` and `assets/`.
- **Cloudflare Pages settings:** leave the build command empty and set the output directory to `/`.
- **To edit:**
  - text and SEO go in `site/content.json`;
  - the layout goes in `site/template.html`;
  - then run `python3 tools/build.py`, and commit and push.
- `python3 tools/make_og_image.py` regenerates the share image; run it again after the final logo is chosen.
- See **SEO.md** for the SEO setup and next steps.

## Brand
- `brand/BRAND.md` holds the brief, and `brand/logo/` holds the logo work.
- **The logo is not final yet.** The site uses a placeholder "F + cyan flame" mark.

## Rules
- **Never commit audio or video masters.** This repo is public, and `.gitignore` blocks those files.
