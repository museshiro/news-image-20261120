#!/usr/bin/env python3
"""Draw the front page for Friday 20 November 2026 as a single PNG.

One image summing up the world's news of 20 November 2026: a newspaper
front page drawn programmatically with PIL, so every word is crisp and
legible. Run: python3 draw_frontpage.py  ->  writes entry.png (1024x1024).
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (17, 17, 17)
RED = (178, 34, 34)
BLUE = (30, 70, 130)
TEAL = (14, 110, 110)
GREY = (90, 90, 90)
LIGHT_LINE = (150, 145, 130)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines that fit `width` px."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, lines, fnt, fill=INK, leading=None, align="left"):
    x, y = xy
    lh = leading or int(fnt.size * 1.22)
    for ln in lines:
        if align == "center":
            draw.text((x - draw.textlength(ln, font=fnt) / 2, y), ln, font=fnt, fill=fill)
        else:
            draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def rule(draw, x0, y, x1, w=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=w)


# ---------------------------------------------------------------- hero art
def draw_kyiv(draw, x0, y0, w, h):
    """Night skyline over the Dnipro: bridges, missile trails, blasts."""
    # sky gradient
    for i in range(h):
        t = i / h
        r = int(11 + (18 - 11) * t)
        g = int(30 + (50 - 30) * t)
        b = int(58 + (94 - 58) * t)
        draw.line([(x0, y0 + i), (x0 + w, y0 + i)], fill=(r, g, b))
    # stars
    import random
    rnd = random.Random(20261120)
    for _ in range(60):
        sx = x0 + rnd.randint(4, w - 4)
        sy = y0 + rnd.randint(4, int(h * 0.45))
        draw.ellipse([sx, sy, sx + 2, sy + 2], fill=(220, 225, 240))
    # moon
    draw.ellipse([x0 + w - 92, y0 + 16, x0 + w - 52, y0 + 56], fill=(235, 230, 200))
    # skyline silhouettes (dark towers with lit windows)
    base = y0 + int(h * 0.62)
    sil = (10, 18, 34)
    towers = [(0, 150, 90), (95, 60, 130), (150, 100, 70), (215, 55, 150),
              (265, 110, 60), (330, 70, 120), (395, 120, 85), (470, 60, 140),
              (525, 95, 75), (585, 55, 130), (640, 105, 80), (700, 70, 120),
              (765, 115, 65), (830, 60, 135), (885, 95, 80), (930, 70, 110)]
    for tx, tw, th in towers:
        draw.rectangle([x0 + tx, base - th, x0 + tx + tw, base], fill=sil)
        for wy in range(base - th + 10, base - 8, 16):
            for wx in range(x0 + tx + 8, x0 + tx + tw - 8, 16):
                if rnd.random() < 0.35:
                    draw.rectangle([wx, wy, wx + 4, wy + 6], fill=(255, 200, 90))
    # river
    draw.rectangle([x0, base, x0 + w, y0 + h], fill=(16, 42, 74))
    for ry in range(base + 10, y0 + h - 6, 12):
        draw.line([(x0 + 20, ry), (x0 + w - 20, ry)], fill=(40, 80, 130), width=2)
    # three bridges across the river (deck + arch + pillars)
    for bx, blen in [(60, 260), (380, 300), (700, 240)]:
        by = base + 26
        draw.line([(x0 + bx, by), (x0 + bx + blen, by)], fill=(200, 205, 215), width=5)
        draw.arc([x0 + bx + 20, by - 34, x0 + bx + blen - 20, by + 20],
                 180, 360, fill=(200, 205, 215), width=4)
        for px in (bx + 30, bx + blen // 2, bx + blen - 30):
            draw.line([(x0 + px, by), (x0 + px, by + 34)], fill=(200, 205, 215), width=4)
    # missile trails (white arcs) with orange heads
    for (sx, sy, ex, ey) in [(120, 8, 300, 150), (520, 4, 660, 140), (820, 10, 700, 170)]:
        pts = []
        for t_i in range(21):
            t = t_i / 20
            pts.append((x0 + sx + (ex - sx) * t,
                        y0 + sy + (ey - sy) * t - 26 * math.sin(math.pi * t)))
        draw.line(pts, fill=(255, 255, 255), width=3)
        draw.ellipse([x0 + ex - 5, y0 + ey - 5, x0 + ex + 5, y0 + ey + 5],
                     fill=(255, 170, 40))
    # explosion bursts
    for cx, cy, rr in [(300, 150, 26), (660, 140, 30), (700, 170, 22)]:
        for k in range(12):
            ang = k * math.pi / 6
            ex = x0 + cx + rr * math.cos(ang)
            ey = y0 + cy + rr * 0.7 * math.sin(ang)
            draw.line([(x0 + cx, y0 + cy), (ex, ey)], fill=(255, 140, 30), width=5)
        draw.ellipse([x0 + cx - 12, y0 + cy - 12, x0 + cx + 12, y0 + cy + 12],
                     fill=(255, 200, 60))
        draw.ellipse([x0 + cx - 5, y0 + cy - 5, x0 + cx + 5, y0 + cy + 5],
                     fill=(255, 240, 160))
    # smoke puffs
    for cx, cy, rr in [(330, 120, 16), (690, 110, 18)]:
        draw.ellipse([x0 + cx - rr, y0 + cy - rr // 2, x0 + cx + rr, y0 + cy + rr // 2],
                     fill=(120, 125, 135))


# ------------------------------------------------------------ panel art
def draw_cyclone(draw, x0, y0, w, h):
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(178, 214, 228))
    # coastline
    draw.polygon([(x0 + int(w * 0.62), y0), (x0 + w, y0), (x0 + w, y0 + h),
                  (x0 + int(w * 0.55), y0 + h)], fill=(226, 205, 160))
    draw.line([(x0 + int(w * 0.62), y0), (x0 + int(w * 0.55), y0 + h)],
              fill=(90, 120, 90), width=3)
    # spiral storm
    cx, cy = x0 + int(w * 0.32), y0 + int(h * 0.55)
    for arm in range(3):
        pts = []
        for t_i in range(40):
            t = t_i / 39
            ang = arm * 2.1 + t * 4.6
            r = 6 + t * 34
            pts.append((cx + r * math.cos(ang), cy + r * 0.55 * math.sin(ang)))
        draw.line(pts, fill=(255, 255, 255), width=6)
    draw.ellipse([cx - 9, cy - 7, cx + 9, cy + 7], fill=(30, 70, 130))
    draw.text((x0 + int(w * 0.66), y0 + 8), "ODISHA", font=font(SANS_B, 15), fill=INK)
    draw.text((x0 + int(w * 0.66), y0 + 28), "INDIA", font=font(SANS_B, 15), fill=INK)


def draw_summit(draw, x0, y0, w, h):
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(232, 228, 218))
    # table
    draw.rectangle([x0, y0 + int(h * 0.72), x0 + w, y0 + h], fill=(120, 70, 50))
    # three flags on poles: US, RU, CN
    fw, fh = 62, 40
    specs = [
        ("us", (30, 90, 160)),   # canton blue, stripes drawn below
        ("ru", None),
        ("cn", (200, 30, 30)),
    ]
    xs = [x0 + 18, x0 + 112, x0 + 206]
    for (kind, col), fx in zip(specs, xs):
        fy = y0 + 12
        draw.line([(fx + fw // 2, fy), (fx + fw // 2, y0 + int(h * 0.72))],
                  fill=(90, 90, 90), width=3)
        if kind == "us":
            for s in range(7):
                draw.rectangle([fx, fy + s * 6, fx + fw, fy + s * 6 + 3],
                               fill=(178, 34, 34) if s % 2 == 0 else (255, 255, 255))
            draw.rectangle([fx, fy, fx + 26, fy + 22], fill=(30, 60, 130))
        elif kind == "ru":
            for s, c in enumerate([(255, 255, 255), (30, 70, 160), (200, 30, 30)]):
                draw.rectangle([fx, fy + s * 14, fx + fw, fy + (s + 1) * 14], fill=c)
        else:
            draw.rectangle([fx, fy, fx + fw, fy + fh], fill=(200, 30, 30))
            for sx, sy in [(fx + 8, fy + 6), (fx + 20, fy + 4), (fx + 24, fy + 12),
                           (fx + 20, fy + 20), (fx + 8, fy + 18)]:
                draw.ellipse([sx, sy, sx + 5, sy + 5], fill=(255, 220, 60))
    draw.text((x0 + 12, y0 + h - 22), "SHENZHEN  •  CHINA", font=font(SANS_B, 13), fill=(255, 255, 255))


def draw_markets(draw, x0, y0, w, h):
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(18, 24, 30))
    # grid
    for gy in range(y0 + 12, y0 + h - 8, 16):
        draw.line([(x0 + 8, gy), (x0 + w - 8, gy)], fill=(45, 55, 65), width=1)
    # falling red line
    pts = [(x0 + 12, y0 + 14), (x0 + 60, y0 + 22), (x0 + 100, y0 + 18),
           (x0 + 150, y0 + 40), (x0 + 195, y0 + 34), (x0 + 245, y0 + 58),
           (x0 + w - 14, y0 + h - 16)]
    draw.line(pts, fill=(255, 70, 60), width=5)
    draw.polygon([(x0 + w - 26, y0 + h - 28), (x0 + w - 8, y0 + h - 28),
                  (x0 + w - 14, y0 + h - 8)], fill=(255, 70, 60))
    draw.text((x0 + 12, y0 + h - 34), "NIKKEI -5%", font=font(SANS_B, 18), fill=(255, 255, 255))


def draw_cop(draw, x0, y0, w, h):
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(214, 232, 214))
    cx, cy, r = x0 + 62, y0 + h // 2, 34
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(60, 130, 200))
    draw.ellipse([cx - 18, cy - 22, cx + 2, cy - 2], fill=(90, 170, 90))
    draw.ellipse([cx - 2, cy + 6, cx + 20, cy + 24], fill=(90, 170, 90))
    # clock = overtime
    ccx, ccy, cr = x0 + 200, y0 + h // 2, 32
    draw.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr], fill=(255, 255, 255),
                 outline=INK, width=3)
    draw.line([(ccx, ccy), (ccx, ccy - 20)], fill=INK, width=3)
    draw.line([(ccx, ccy), (ccx + 14, ccy + 8)], fill=INK, width=3)


def draw_ukeu(draw, x0, y0, w, h):
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(226, 232, 240))
    # UK flag (simplified Union Jack)
    fx, fy, fw, fh = x0 + 16, y0 + 14, 110, 58
    draw.rectangle([fx, fy, fx + fw, fy + fh], fill=(30, 60, 130))
    draw.line([(fx, fy), (fx + fw, fy + fh)], fill=(255, 255, 255), width=10)
    draw.line([(fx + fw, fy), (fx, fy + fh)], fill=(255, 255, 255), width=10)
    draw.line([(fx + fw // 2, fy), (fx + fw // 2, fy + fh)], fill=(255, 255, 255), width=16)
    draw.line([(fx, fy + fh // 2), (fx + fw, fy + fh // 2)], fill=(255, 255, 255), width=16)
    draw.line([(fx + fw // 2, fy), (fx + fw // 2, fy + fh)], fill=(200, 30, 30), width=8)
    draw.line([(fx, fy + fh // 2), (fx + fw, fy + fh // 2)], fill=(200, 30, 30), width=8)
    # EU flag
    ex, ey, ew, eh = x0 + 152, y0 + 14, 110, 58
    draw.rectangle([ex, ey, ex + ew, ey + eh], fill=(20, 50, 140))
    for k in range(12):
        ang = k * math.pi / 6 - math.pi / 2
        sx = ex + ew // 2 + 20 * math.cos(ang)
        sy = ey + eh // 2 + 16 * math.sin(ang)
        draw.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 220, 60))


def draw_gulf(draw, x0, y0, w, h):
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(250, 225, 190))
    # PIF-style tower
    tx = x0 + 40
    draw.polygon([(tx, y0 + h), (tx, y0 + 14), (tx + 34, y0 + 4),
                  (tx + 68, y0 + 14), (tx + 68, y0 + h)], fill=(60, 70, 90))
    for wy in range(y0 + 22, y0 + h - 10, 14):
        for wx in range(tx + 8, tx + 60, 14):
            draw.rectangle([wx, wy, wx + 6, wy + 6], fill=(255, 210, 120))
    # missile streak + smoke
    draw.line([(x0 + 150, y0 + 12), (x0 + 230, y0 + 46)], fill=(200, 40, 30), width=4)
    draw.ellipse([x0 + 226, y0 + 42, x0 + 238, y0 + 54], fill=(255, 150, 40))
    draw.ellipse([x0 + 150, y0 + 8, x0 + 176, y0 + 26], fill=(150, 150, 150))
    # sea
    draw.rectangle([x0, y0 + h - 16, x0 + w, y0 + h], fill=(30, 90, 140))
    draw.text((x0 + 130, y0 + h - 38), "RED SEA", font=font(SANS_B, 14), fill=INK)


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28  # margin
    X1 = W - M

    # masthead
    y = 18
    f_mast = font(SERIF_B, 62)
    d.text((W // 2, y), "THE WORLD IN ONE DAY", font=f_mast, fill=INK, anchor="ma")
    y += 74
    rule(d, M, y, X1, 3, RED)
    y += 10
    d.text((W // 2, y), "FRIDAY  20  NOVEMBER  2026", font=font(SANS_B, 26),
           fill=INK, anchor="ma")
    y += 40
    rule(d, M, y, X1, 2, INK)
    y += 8
    d.text((W // 2, y), "19 STORIES  •  6 REGIONS  —  THE DAY'S WORLD NEWS IN ONE PAGE",
           font=font(SANS_B, 15), fill=GREY, anchor="ma")
    y += 26

    # ---- hero: Kyiv (art rendered on its own canvas so nothing overflows)
    hero_y, hero_h, art_h = y, 280, 150
    d.rectangle([M, hero_y, X1, hero_y + hero_h], outline=INK, width=2)
    art = Image.new("RGB", (X1 - M - 4, art_h))
    draw_kyiv(ImageDraw.Draw(art), 0, 0, X1 - M - 4, art_h)
    img.paste(art, (M + 2, hero_y + 2))
    ty = hero_y + art_h + 4
    d.text((M + 14, ty), "UKRAINE  •  LEAD STORY", font=font(SANS_B, 14), fill=RED)
    ty += 20
    head = "RUSSIA'S BIGGEST BARRAGE OF THE WAR HITS KYIV"
    d.text((M + 14, ty), head, font=font(SERIF_B, 33), fill=INK)
    ty += 44
    deck = ("400+ drones and 110 missiles — 27 of them ballistic — strike overnight. "
            "Three bridges across the Dnipro are damaged, 8 people killed, power cut "
            "across the capital. A Russian missile lands in Poland; NATO jets scramble.")
    for ln in wrap(d, deck, font(SANS, 17), X1 - M - 28):
        d.text((M + 14, ty), ln, font=font(SANS, 17), fill=INK)
        ty += 22
    y = hero_y + hero_h + 12

    # ---- six panels, two rows of three
    panels = [
        ("ASIA", "CYCLONE AKVAN MAKES LANDFALL",
         "Storm crosses the coast near Gopalpur, Odisha. 300,000 moved to safety.",
         draw_cyclone, RED),
        ("DIPLOMACY", "SHENZHEN SUMMIT: TRUMP, PUTIN, XI",
         "The three leaders issue a joint declaration in China. Hours later, "
         "Kyiv is hit.", draw_summit, BLUE),
        ("MARKETS", "AI SELL-OFF: ANTHROPIC -9%",
         "Shares fall on day two after the record $81bn IPO. Nikkei -5%; the "
         "Nasdaq wipes out its 2026 gains.", draw_markets, RED),
        ("CLIMATE", "COP31 RUNS INTO OVERTIME",
         "Talks in Antalya pass their Friday deadline with no deal. The draft "
         "text drops all mention of fossil fuels.", draw_cop, TEAL),
        ("EUROPE", "UK-EU RESET: BIGGEST DEAL SINCE BREXIT",
         "Food trade, youth mobility for 100,000 a year and linked carbon "
         "markets agreed in Brussels.", draw_ukeu, BLUE),
        ("MIDDLE EAST", "GULF ESCALATION: HODEIDAH STRUCK",
         "Saudi-led coalition hits the port as Houthis threaten Red Sea ports "
         "and airlines.", draw_gulf, RED),
    ]
    pw = (X1 - M - 16) // 3
    ph = 182
    for row in range(2):
        for col in range(3):
            i = row * 3 + col
            kicker, title, deck, art, colr = panels[i]
            px = M + col * (pw + 8)
            py = y + row * (ph + 10)
            d.rectangle([px, py, px + pw, py + ph], outline=INK, width=1)
            art(d, px + 1, py + 1, pw - 2, 72)
            ty = py + 78
            d.text((px + 10, ty), kicker, font=font(SANS_B, 13), fill=colr)
            ty += 18
            for ln in wrap(d, title, font(SANS_B, 18), pw - 20):
                d.text((px + 10, ty), ln, font=font(SANS_B, 18), fill=INK)
                ty += 22
            for ln in wrap(d, deck, font(SANS, 14), pw - 20):
                d.text((px + 10, ty), ln, font=font(SANS, 14), fill=(40, 40, 40))
                ty += 18
    y = y + 2 * ph + 10 + 12

    # ---- ticker: more from the day
    rule(d, M, y, X1, 2, INK)
    y += 8
    d.text((M, y), "MORE FROM THE DAY", font=font(SANS_B, 15), fill=RED)
    y += 24
    more = [
        "US Senate passes the permitting bill 62-33",
        "Haiti police kill 34 in a gang raid; two soldiers die in a blast",
        "Kerch Bridge rail traffic resumes after Ukraine's strikes",
        "Ukraine hits a Druzhba oil pumping station in Tatarstan",
        "Britain pledges 1,000 long-range drones for Ukraine",
        "Trump: a decision on new Iran strikes can wait until 2027",
        "Estonia to close its border with Russia from 1 December",
        "Gold falls nearly 4%; Bitcoin drops below $59,000",
        "YouTube agrees in principle to pay $3bn to school districts",
        "Gaza floods swamp tents; the EU presses Israel on aid access",
        "African nations demand climate finance at COP31",
        "UN chief race deadlocked after a ninth straw poll",
    ]
    col_w = (X1 - M - 20) // 2
    f_t = font(SANS, 13)
    for i, item in enumerate(more):
        cx = M + (i % 2) * (col_w + 20)
        cy = y + (i // 2) * 18
        d.text((cx, cy), "•  " + item, font=f_t, fill=INK)
    y = y + 6 * 18 + 8

    # ---- footer
    rule(d, M, y, X1, 1, LIGHT_LINE)
    y += 7
    d.text((W // 2, y), "Friday 20 November 2026  •  Sources: Reuters, CNN, ISW, India Meteorological Dept.",
           font=font(SANS, 12), fill=GREY, anchor="ma")

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
