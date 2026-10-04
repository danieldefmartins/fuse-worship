# SEO plan: Fuse Worship

## Already in place (2026-10-04)
- **One real page per language:** `/` (EN), `/es/`, `/pt/`. Google indexes each language on its own page; there's no text swapped in by JavaScript.
- **hreflang links** between the 3 pages, with `x-default` pointing to EN, plus a **canonical URL** on each page.
- **Titles and meta descriptions per language**, written with each language's own search terms. Edit them in `site/content.json`.
- **Schema.org `MusicGroup` data (JSON-LD)** on every page: name, genres, languages, and Fuse Kids as a sub-group.
- **Open Graph and Twitter share tags** with `assets/og-image.png` (1200×630).
- **`sitemap.xml`** with language alternates, and **`robots.txt`** pointing to it.
- A fast static site with no framework, a mobile layout and real text.

## How to edit
1. Change text or SEO fields in `site/content.json`, or the layout in `site/template.html`.
2. Run `python3 tools/build.py`. It rewrites the 3 pages, `sitemap.xml` and `robots.txt`.
3. Commit and push; Cloudflare Pages deploys automatically.

## Profile links (do this as each profile goes live)
Add every official profile URL to `"same_as"` in `site/content.json`: Spotify, Apple Music, YouTube, Instagram, TikTok, Facebook. Google uses these links to connect the band's profiles into one "knowledge panel".

## Once the site is live (Daniel or Claude via Chrome)
1. **Google Search Console:**
   - add the `fuseworship.com` domain property; verification is a DNS TXT record, which is easy in Cloudflare;
   - submit `https://fuseworship.com/sitemap.xml`.
2. **Bing Webmaster Tools:** import the site from Search Console. This also covers DuckDuckGo and Yahoo.
3. **Cloudflare:**
   - make sure `www` redirects to the root domain (or the other way round), so there's one canonical host;
   - keep "Always Use HTTPS" on.
4. Test the pages with Google's Rich Results Test and a social share preview tool.

## Target search terms (starting list)
| EN | ES | PT-BR |
|---|---|---|
| worship songs for kids | canciones cristianas para niños | músicas gospel infantis |
| christian kids songs | alabanzas para niños | louvor infantil |
| bilingual worship songs | adoración en español | músicas de adoração |
| Spanish worship songs | alabanzas de adoración | louvores de adoração |
| Portuguese worship songs | música cristiana para la familia | música cristã para família |
| Psalm 23 song for kids | Salmo 23 canción para niños | Salmo 23 música infantil |

Song pages will target each song's own title and Bible reference, for example "Psalm 23 song for kids".

## Next growth steps
- **One page per song in each language** (`/songs/<slug>/`, `/es/canciones/<slug>/`, `/pt/musicas/<slug>/`), each with:
  - the full lyrics (pages with lyrics rank well);
  - the Bible reference;
  - the YouTube embed;
  - streaming links;
  - `MusicRecording` schema.
- **Pages for parents, churches and teachers:** kids' ministry ideas, "how to use these songs in Sunday school", printable lyric sheets.
- **Links from other sites:** church partners, kids' ministry blogs, and the YouTube and streaming profiles linking back to the site.
- **Keep each song's title and description the same** across the site, YouTube, Spotify and Apple Music.
