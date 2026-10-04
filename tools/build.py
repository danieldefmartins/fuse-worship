#!/usr/bin/env python3
"""Build the static site: one real page per language plus sitemap.xml and robots.txt.

Edit site/template.html (layout) or site/content.json (all text, SEO titles and
descriptions), then run:  python3 tools/build.py
Commit the generated files; Cloudflare Pages serves them with no build step.
"""
import datetime
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = (ROOT / "site" / "template.html").read_text(encoding="utf-8")
CONTENT = json.loads((ROOT / "site" / "content.json").read_text(encoding="utf-8"))

SITE = CONTENT["site_url"].rstrip("/")
LANGS = CONTENT["languages"]
TODAY = datetime.date.today().isoformat()

# Fields that are not plain text placeholders in the template.
NON_TEMPLATE = {"path", "hreflang", "label", "schema_description"}


def url(path):
    return SITE + path


def hreflang_links():
    links = [f'<link rel="alternate" hreflang="{v["hreflang"]}" href="{url(v["path"])}">' for v in LANGS.values()]
    links.append(f'<link rel="alternate" hreflang="x-default" href="{url(LANGS["en"]["path"])}">')
    return "\n".join(links)


def json_ld(lang):
    data = {
        "@context": "https://schema.org",
        "@type": "MusicGroup",
        "name": "Fuse Worship",
        "url": url(LANGS[lang]["path"]),
        "logo": url("/favicon.svg"),
        "image": url("/assets/og-image.png"),
        "description": LANGS[lang]["schema_description"],
        "genre": ["Christian & Gospel", "Worship", "Children's Music"],
        "foundingDate": "2026",
        "knowsLanguage": [v["html_lang"] for v in LANGS.values()],
        "subOrganization": {"@type": "MusicGroup", "name": "Fuse Kids", "genre": "Children's Music"},
    }
    if CONTENT["same_as"]:
        data["sameAs"] = CONTENT["same_as"]
    # Escape "</" so the JSON can never close the <script> tag early.
    return json.dumps(data, ensure_ascii=False, indent=2).replace("</", "<\\/")


def render(lang):
    page = LANGS[lang]
    values = {k: html.escape(v) for k, v in page.items() if k not in NON_TEMPLATE}
    values.update({
        "site_url": SITE,
        "canonical": url(page["path"]),
        "home_path": page["path"],
        "year": str(datetime.date.today().year),
        "hreflang_links": hreflang_links(),
        "og_locale_alternates": "\n".join(
            f'<meta property="og:locale:alternate" content="{v["og_locale"]}">'
            for k, v in LANGS.items() if k != lang),
        "lang_links": "\n      ".join(
            f'<a href="{v["path"]}" hreflang="{v["hreflang"]}" lang="{v["html_lang"]}"'
            + (' aria-current="page"' if k == lang else "") + f'>{v["label"]}</a>'
            for k, v in LANGS.items()),
        "json_ld": json_ld(lang),
    })

    def sub(m):
        key = m.group(1)
        if key not in values:
            raise KeyError(f"{lang}: no value for {{{{{key}}}}}")
        return values[key]

    return re.sub(r"\{\{(\w+)\}\}", sub, TEMPLATE)


def main():
    for lang, page in LANGS.items():
        out = ROOT / page["path"].lstrip("/") / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(lang), encoding="utf-8")
        print("wrote", out.relative_to(ROOT))

    alternates = "".join(
        f'\n    <xhtml:link rel="alternate" hreflang="{v["hreflang"]}" href="{url(v["path"])}"/>' for v in LANGS.values())
    entries = "".join(
        f"\n  <url>\n    <loc>{url(v['path'])}</loc>\n    <lastmod>{TODAY}</lastmod>{alternates}\n  </url>"
        for v in LANGS.values())
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">'
        f"{entries}\n</urlset>\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\nDisallow: /site/\nDisallow: /tools/\nDisallow: /brand/\n\n"
        f"Sitemap: {url('/sitemap.xml')}\n", encoding="utf-8")
    print("wrote sitemap.xml, robots.txt")


if __name__ == "__main__":
    main()
