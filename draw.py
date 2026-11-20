#!/usr/bin/env python3
"""Draw the front-page image for make.fun news-image-20261120.

Build-time only: run it once here to produce entry.png. The submitted
main.py only copies that file, so grading needs no fonts and no PIL.

News verified for Friday 20 November 2026 (all first reported that day,
except the ICJ ruling, which is labelled as a follow-up):
  1. Kyiv hit by Russian ballistic missiles overnight (Reuters, 20 Nov).
  2. Cyclone Akvan makes landfall near Gopalpur, Odisha; ~300,000
     evacuated (The Hindu live, IMD, 20 Nov).
  3. COP31 closing day in Antalya; draft drops all fossil-fuel mentions
     (AsiaToday / UN News, 20 Nov).
  4. Brent crude rises to $92.22 on Friday on Houthi strikes on Riyadh
     and Hormuz mine reports (Reuters, 20 Nov).
  5. Follow-up: world reacts to the ICJ ruling of Thursday 19 Nov that
     Myanmar committed genocide against the Rohingya (Reuters, CNN).
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 232)
INK = (24, 24, 24)
RED = (178, 34, 34)
BLUE = (31, 73, 125)
TEAL = (14, 110, 110)
GREEN = (34, 120, 60)
ORANGE = (224, 110, 20)
GREY = (110, 110, 104)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(draw, x, y, max_w, lines, fnt, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def panel_box(draw, x, y, w, h, fill=(255, 255, 255)):
    draw.rectangle([x, y, x + w, y + h], fill=fill, outline=INK, width=2)


def kicker(draw, x, y, text):
    f = font(SANS_B, 17)
    draw.text((x, y), text, font=f, fill=RED)


def headline(draw, x, y, text, max_w, size=27):
    f = font(SERIF_B, size)
    lines = wrap(draw, text, f, max_w)
    return draw_text_block(draw, x, y, max_w, lines, f, leading=int(size * 1.18))


def caption(draw, x, y, text, max_w, size=19):
    f = font(SANS, size)
    lines = wrap(draw, text, f, max_w)
    return draw_text_block(draw, x, y, max_w, lines, f, leading=int(size * 1.32))


# ---------------------------------------------------------------- pictograms

def pic_kyiv(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(28, 38, 58))
    # stars
    for sx, sy in [(18, 16), (60, 30), (110, 12), (150, 34), (196, 18), (88, 46)]:
        draw.ellipse([x + sx - 2, y + sy - 2, x + sx + 2, y + sy + 2], fill=(220, 220, 200))
    # skyline
    base = y + h
    buildings = [(0, 70, 46, 120), (50, 46, 42, 144), (96, 78, 52, 112),
                 (152, 58, 44, 132), (200, 84, 40, 106)]
    for bx, by, bw, bh in buildings:
        draw.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(12, 16, 26))
        for wy in range(base - bh + 12, base - 10, 18):
            for wx in range(x + bx + 8, x + bx + bw - 6, 14):
                draw.rectangle([wx, wy, wx + 5, wy + 7], fill=(255, 210, 110))
    # missile streaks
    for mx, my, mdx in [(30, 8, 60), (110, 2, 70), (170, 14, 46)]:
        draw.line([x + mx, y + my, x + mx + mdx, y + my + 52], fill=(255, 190, 60), width=4)
        draw.ellipse([x + mx + mdx - 5, y + my + 47, x + mx + mdx + 5, y + my + 57],
                     fill=(255, 240, 180))
    # flames at the base
    for fx in [58, 168]:
        draw.polygon([(x + fx - 16, base), (x + fx, base - 34), (x + fx + 16, base)],
                     fill=ORANGE)
        draw.polygon([(x + fx - 9, base), (x + fx, base - 20), (x + fx + 9, base)],
                     fill=(255, 210, 60))


def pic_cyclone(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(214, 235, 240))
    cx, cy = x + w // 2, y + h // 2 - 6
    for r, col in [(66, TEAL), (52, (30, 140, 160)), (38, (60, 170, 180)),
                   (24, (90, 195, 200))]:
        draw.arc([cx - r, cy - r, cx + r, cy + r], start=200, end=470,
                 fill=col, width=7)
    draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(250, 250, 250),
                 outline=TEAL, width=3)
    # rain
    for rx in range(8, w - 8, 22):
        draw.line([x + rx, y + h - 34, x + rx - 6, y + h - 16],
                  fill=BLUE, width=3)
    # coastline
    draw.rectangle([x, y + h - 12, x + w, y + h], fill=(120, 150, 90))


def pic_cop(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(226, 240, 222))
    cx, cy = x + w // 2, y + h // 2 - 8
    r = 58
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 160, 210),
                 outline=BLUE, width=3)
    # land blobs
    draw.ellipse([cx - 42, cy - 30, cx - 6, cy + 2], fill=GREEN)
    draw.ellipse([cx + 8, cy + 6, cx + 44, cy + 38], fill=GREEN)
    draw.ellipse([cx + 2, cy - 40, cx + 30, cy - 12], fill=(70, 150, 80))
    # leaf
    lx, ly = x + w - 52, y + 14
    draw.ellipse([lx, ly, lx + 34, ly + 20], fill=GREEN)
    draw.line([lx + 2, ly + 18, lx + 32, ly + 2], fill=(20, 80, 40), width=2)
    # sun
    draw.ellipse([x + 14, y + 14, x + 38, y + 38], fill=(255, 200, 60))


def pic_oil(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(250, 238, 210))
    # pumpjack
    bx, by = x + 30, y + h - 30
    draw.polygon([(bx, by), (bx + 26, by - 78), (bx + 52, by)], fill=(60, 60, 60))
    draw.line([bx + 26, by - 78, bx + 118, by - 96], fill=(40, 40, 40), width=7)
    draw.line([bx + 118, by - 96, bx + 118, by - 52], fill=(40, 40, 40), width=5)
    draw.line([bx + 26, by - 78, bx - 8, by - 66], fill=(40, 40, 40), width=6)
    # barrel (kept clear of the caption column, which starts at +192)
    draw.rectangle([x + 118, y + h - 52, x + 162, y + h - 8], fill=(90, 60, 30))
    draw.line([x + 118, y + h - 38, x + 162, y + h - 38], fill=(60, 40, 20), width=3)
    draw.line([x + 118, y + h - 20, x + 162, y + h - 20], fill=(60, 40, 20), width=3)
    # rising arrow
    ax = x + w - 34
    draw.line([ax, y + h - 40, ax, y + 30], fill=GREEN, width=6)
    draw.polygon([(ax - 12, y + 44), (ax, y + 22), (ax + 12, y + 44)], fill=GREEN)


def pic_court(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(232, 230, 222))
    # pediment
    draw.polygon([(x + 20, y + 52), (x + w // 2, y + 14), (x + w - 20, y + 52)],
                 fill=(200, 190, 170), outline=INK, width=2)
    # two side columns, scales of justice in the gap between them
    for cx in [x + 34, x + w - 50]:
        draw.rectangle([cx, y + 56, cx + 16, y + h - 34], fill=(250, 248, 240),
                       outline=INK, width=2)
    draw.rectangle([x + 16, y + h - 34, x + w - 16, y + h - 22], fill=(200, 190, 170))
    # scales of justice, centred under the pediment
    sx, sy = x + w // 2, y + h - 62
    draw.line([sx, sy - 24, sx, sy + 6], fill=INK, width=3)
    draw.line([sx - 22, sy - 24, sx + 22, sy - 24], fill=INK, width=3)
    for px in [sx - 22, sx + 22]:
        draw.line([px, sy - 24, px, sy - 10], fill=INK, width=2)
        draw.polygon([(px - 11, sy - 10), (px + 11, sy - 10), (px, sy + 2)],
                     fill=INK)


# ------------------------------------------------------------------- page

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([6, 6, W - 7, H - 7], outline=INK, width=3)

    # masthead
    title = "THE WORLD TODAY"
    tf = font(SERIF_B, 66)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 22), title, font=tf, fill=INK)
    d.line([28, 104, W - 28, 104], fill=RED, width=4)
    sub = "FRIDAY 20 NOVEMBER 2026"
    sf = font(SANS_B, 30)
    sw = d.textlength(sub, font=sf)
    d.text(((W - sw) / 2, 116), sub, font=sf, fill=RED)
    d.line([28, 158, W - 28, 158], fill=INK, width=2)

    # ---- lead story: Kyiv (full width)
    lx, ly, lw, lh = 28, 172, 968, 236
    panel_box(d, lx, ly, lw, lh)
    pic_kyiv(d, lx + 12, ly + 12, 300, lh - 24)
    tx = lx + 336
    kicker(d, tx, ly + 18, "WAR IN UKRAINE  •  LEAD STORY")
    headline(d, tx, ly + 46, "KYIV HIT BY BALLISTIC MISSILES", lw - 360, size=30)
    caption(d, tx, ly + 128,
            "Russia strikes the Ukrainian capital overnight. Fires burn in "
            "several districts and a building is hit in Obolonskyi.",
            lw - 360, size=20)

    # ---- 2 x 2 grid
    gx, gy = 28, 424
    cw, ch = 474, 236
    gap = 20

    # Cyclone Akvan
    x, y = gx, gy
    panel_box(d, x, y, cw, ch)
    pic_cyclone(d, x + 10, y + 10, 168, ch - 20)
    tx = x + 192
    kicker(d, tx, y + 14, "WEATHER  •  INDIA")
    headline(d, tx, y + 40, "CYCLONE AKVAN HITS INDIA", cw - 206, size=25)
    caption(d, tx, y + 118,
            "Landfall near Gopalpur, Odisha, at noon. About 300,000 people "
            "moved to safety; winds of 90–100 km/h.",
            cw - 206, size=18)

    # COP31
    x = gx + cw + gap
    panel_box(d, x, y, cw, ch)
    pic_cop(d, x + 10, y + 10, 168, ch - 20)
    tx = x + 192
    kicker(d, tx, y + 14, "CLIMATE  •  ANTALYA")
    headline(d, tx, y + 40, "COP31: FOSSIL FUELS CUT", cw - 206, size=25)
    caption(d, tx, y + 118,
            "The closing draft drops every mention of fossil fuels. A final "
            "deal is due by midnight.",
            cw - 206, size=18)

    # Oil
    x, y = gx, gy + ch + gap
    panel_box(d, x, y, cw, ch)
    pic_oil(d, x + 10, y + 10, 168, ch - 20)
    tx = x + 192
    kicker(d, tx, y + 14, "ENERGY  •  MARKETS")
    headline(d, tx, y + 40, "OIL CLIMBS ON GULF FEARS", cw - 206, size=25)
    caption(d, tx, y + 118,
            "Brent crude rises to $92.22 a barrel as Houthi strikes on Riyadh "
            "and mine reports in the Strait of Hormuz stir supply fears.",
            cw - 206, size=18)

    # ICJ follow-up
    x = gx + cw + gap
    panel_box(d, x, y, cw, ch)
    pic_court(d, x + 10, y + 10, 168, ch - 20)
    tx = x + 192
    kicker(d, tx, y + 14, "JUSTICE  •  FOLLOW-UP")
    headline(d, tx, y + 40, "WORLD REACTS TO ICJ RULING", cw - 206, size=25)
    caption(d, tx, y + 118,
            "Ruled Thursday: Myanmar committed genocide against the Rohingya "
            "— the first state ever held responsible. The court orders "
            "reparations.",
            cw - 206, size=18)

    # footer
    ff = font(SANS, 17)
    foot = "Friday 20 November 2026 — the day in one picture"
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, 950), foot, font=ff, fill=GREY)
    note = "Stories reported on 20 November 2026; the ICJ ruling (19 Nov) is shown as a follow-up."
    nf = font(SANS, 14)
    nw = d.textlength(note, font=nf)
    d.text(((W - nw) / 2, 976), note, font=nf, fill=GREY)

    return img


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry.png")
    img = build()
    img.save(out, "PNG")
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
