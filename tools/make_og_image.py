#!/usr/bin/env python3
"""Make assets/og-image.png (1200x630), the preview shown when the site is shared.
Re-run after the final logo is chosen.  python3 tools/make_og_image.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
W, H = 1200, 630
INK, TEXT, CYAN, MUTED = (11, 13, 18), (255, 248, 240), (46, 224, 240), (169, 176, 190)

img = Image.new("RGB", (W, H), INK)

# Soft cyan glow behind the mark.
glow = Image.new("RGB", (W, H), INK)
ImageDraw.Draw(glow).ellipse((W / 2 - 330, -260, W / 2 + 330, 400), fill=(20, 70, 80))
img = Image.blend(img, glow.filter(ImageFilter.GaussianBlur(120)), 1.0)
d = ImageDraw.Draw(img)

# Placeholder "F + flame" mark, the same shapes as favicon.svg (64-unit grid).
s, ox, oy = 2.6, W / 2 - 31 * 2.6, 40
f = [(27, 12), (50, 12), (50, 21), (35, 21), (35, 27), (47, 27), (47, 36), (35, 36), (35, 52), (27, 52)]
d.polygon([(ox + x * s, oy + y * s) for x, y in f], fill=TEXT)
flame = [(23, 14), (16, 19), (13, 27), (17, 36), (20, 40), (22, 44), (22, 50), (25, 46), (26, 40), (24, 33),
         (20, 28), (20, 22)]
d.polygon([(ox + x * s, oy + y * s) for x, y in flame], fill=CYAN)


def font(size):
    for p in ("/System/Library/Fonts/Supplemental/Arial Black.ttf", "/Library/Fonts/Arial Black.ttf"):
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def centered(text, y, size, fill, spacing=0):
    fnt = font(size)
    widths = [d.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + spacing * (len(text) - 1)
    x = (W - total) / 2
    for ch, w in zip(text, widths):
        d.text((x, y), ch, font=fnt, fill=fill)
        x += w + spacing


centered("FUSE", 205, 150, TEXT, 6)
centered("WORSHIP", 385, 44, TEXT, 26)
centered("Ignite. Unite. Worship.", 478, 36, CYAN)
centered("EN  ·  ES  ·  PT", 548, 26, MUTED, 2)

out = ROOT / "assets" / "og-image.png"
out.parent.mkdir(exist_ok=True)
img.save(out, optimize=True)
print("wrote", out.relative_to(ROOT))
