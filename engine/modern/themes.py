"""One visual theme per game for the 'popular' preset.

A theme = colours + fonts + a static background painter + a per-frame animated layer + a panel style.
All art is original and generic: no logos, no official sprites, no known characters.
Text role spec: (font file, weight, fill, stroke as a fraction of the size, stroke colour, shadow (dx, dy, colour) as fractions, box fill)
"""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from gfx import *

PM = 34  # margin kept around every panel image for shadows and ornaments
CX, CY = 540, 800  # centre of the content area


def _panel(w, h, fill, outline=None, ow=0, radius=0, shadow=None, soft=0):
    im = Image.new("RGBA", (w + 2 * PM, h + 2 * PM), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if shadow:
        dx, dy, col = shadow
        d.rounded_rectangle([PM + dx, PM + dy, PM + w + dx, PM + h + dy], radius, fill=col)
        if soft:
            im = im.filter(ImageFilter.GaussianBlur(soft))
            d = ImageDraw.Draw(im)
    d.rounded_rectangle([PM, PM, PM + w, PM + h], radius, fill=fill, outline=outline, width=ow)
    return im, d


def particles(n, seed):
    rnd = random.Random(seed)
    return [(rnd.random(), rnd.random(), rnd.random(), rnd.random()) for _ in range(n)]


# ================================================================ COUNTER-STRIKE 2: tactical HUD
def static_cs2():
    img = grain(vgrad("#0a0e13", "#1a2430"), 5)
    lay, d = layer()
    for x in range(0, W, 90):
        d.line([(x, 0), (x, H)], fill=(255, 255, 255, 10), width=1)
    for y in range(0, H, 90):
        d.line([(0, y), (W, y)], fill=(255, 255, 255, 10), width=1)
    for r, a in ((430, 50), (280, 30), (130, 22)):
        d.ellipse([CX - r, CY - r, CX + r, CY + r], outline=(245, 166, 35, a), width=3)
    for ang in range(0, 360, 90):
        c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        d.line([(CX + c * 445, CY + s * 445), (CX + c * 500, CY + s * 500)], fill=(245, 166, 35, 110), width=5)
    for (x, y, sx, sy) in ((40, 420, 1, 1), (1040, 420, -1, 1), (40, 1190, 1, -1), (1040, 1190, -1, -1)):
        d.line([(x, y), (x + 70 * sx, y)], fill=(245, 166, 35, 150), width=5)
        d.line([(x, y), (x, y + 70 * sy)], fill=(245, 166, 35, 150), width=5)
    return vignette(over(img, lay), 0.5)


def dyn_cs2(img, d, now, prog, end, S):
    a = now * 0.9
    for j in range(7):
        aa = a - j * 0.045
        d.line([(CX, CY), (CX + 430 * math.cos(aa), CY + 430 * math.sin(aa))], fill=mix("#c98a20", "#141c26", j / 7), width=3)
    rem = max(0, end - now)
    blink = int(now * 2) % 2 == 0
    paste(img, text_img(f"{int(rem) // 60}:{int(rem) % 60:02d}", "ChakraPetch-Bold.ttf", 46, "#f5a623" if blink or rem > 10 else "#ff4433"), 540, 372)
    d.ellipse([440, 364, 456, 380], fill=(255, 68, 51) if blink else (90, 30, 26))


def panel_cs2(w, h, kind="main"):
    im, d = _panel(w, h, (14, 20, 28, 238), (70, 86, 104, 255), 2)
    L = 20 if kind != "main" else 40
    for (x, y, sx, sy) in ((PM, PM, 1, 1), (PM + w, PM, -1, 1), (PM, PM + h, 1, -1), (PM + w, PM + h, -1, -1)):
        d.line([(x, y), (x + L * sx, y)], fill=(245, 166, 35), width=6)
        d.line([(x, y), (x, y + L * sy)], fill=(245, 166, 35), width=6)
    return im


# ================================================================ DYNASTY WARRIORS 9: ink and war banners
def static_dw9():
    img = grain(vgrad("#f0e4c4", "#dcc79a"), 9, 2, 2)
    lay, d = layer()
    d.ellipse([750, 395, 1010, 655], fill=(179, 38, 30, 150))
    over(img, lay, 2)
    for k, (y0, a) in enumerate(((1480, 46), (1600, 70), (1730, 110))):
        lay, d = layer()
        ridge(d, 11 + k, y0, 190, (40, 34, 30, a), 70)
        over(img, lay, 5 - k)
    lay, d = layer()
    for x0 in (0, W - 46):
        d.rectangle([x0, 0, x0 + 46, H], fill=(160, 28, 24, 255))
        d.line([(x0 + (40 if x0 == 0 else 5), 0), (x0 + (40 if x0 == 0 else 5), H)], fill=(201, 151, 43, 255), width=4)
    over(img, lay)
    return vignette(img, 0.35, (90, 60, 20))


def dyn_dw9(img, d, now, prog, end, S):
    for i, (a, b, c, e) in enumerate(S.setdefault("p", particles(18, 5))):
        y = (b * H + now * (120 + 140 * c)) % (H + 40) - 20
        x = 60 + a * 960 + math.sin(now * 1.3 + i) * 40
        r = 6 + 6 * e
        d.ellipse([x - r, y - r * 0.6, x + r, y + r * 0.6], fill=mix("#b3261e", "#e9a39c", e))
    paste(img, text_img(f"K.O. COUNT  {int(now * 23):04d}", "Cinzel[wght].ttf", 40, "#b3261e", wght=900), 540, 372)


def panel_dw9(w, h, kind="main"):
    im, d = _panel(w, h, (156, 28, 24, 248), (201, 151, 43, 255), 6, 0, (8, 10, (60, 20, 10, 90)))
    if kind == "main":
        d.rectangle([PM + 14, PM + 14, PM + w - 14, PM + h - 14], outline=(232, 190, 96, 255), width=2)
    return im


# ================================================================ DOTA 2: arcane battle map
def static_dota():
    img = radial("#4a0f12", "#070304", CX, 820, 1150)
    lay, d = layer()
    gold = (232, 181, 74, 44)
    d.line([(130, 1500), (950, 330)], fill=gold, width=12)
    d.line([(130, 1500), (130, 330), (950, 330)], fill=gold, width=12, joint="curve")
    d.line([(130, 1500), (950, 1500), (950, 330)], fill=gold, width=12, joint="curve")
    over(img, lay, 2)
    over(img, blobs(3, 1, ["#63c466"], 190, 191, 120, 60, (129, 1499, 131, 1501)))
    over(img, blobs(4, 1, ["#e0483c"], 190, 191, 130, 60, (949, 329, 951, 331)))
    return vignette(grain(img, 4), 0.55)


def dyn_dota(img, d, now, prog, end, S):
    for k in range(10):
        a0 = k * 36 + now * 7
        d.arc([CX - 500, CY - 500, CX + 500, CY + 500], a0, a0 + 20, fill=(96, 70, 32), width=4)
    for i, (a, b, c, e) in enumerate(S.setdefault("p", particles(30, 9))):
        y = H - ((b * H + now * (60 + 110 * c)) % (H + 40))
        x = a * W + math.sin(now * 0.9 + i * 1.7) * 50
        r = 2 + 4 * e
        d.ellipse([x - r, y - r, x + r, y + r], fill=mix("#ffb347", "#5a1a10", 0.2 + 0.6 * (1 - y / H)))
    paste(img, text_img(f"{int(now) // 60:02d}:{int(now) % 60:02d}", "Metamorphous-Regular.ttf", 40, "#e8b54a"), 540, 372)


def panel_dota(w, h, kind="main"):
    im, d = _panel(w, h, (18, 8, 10, 238), (200, 160, 80, 255), 3)
    if kind == "main":
        d.rectangle([PM + 12, PM + 12, PM + w - 12, PM + h - 12], outline=(96, 66, 30, 255), width=2)
        for (x, y) in ((PM, PM), (PM + w, PM), (PM, PM + h), (PM + w, PM + h)):
            d.regular_polygon((x, y, 14), 4, rotation=45, fill=(232, 181, 74))
    return im


# ================================================================ PUBG: drop zone map
def static_pubg():
    img = Image.new("RGB", (W, H), rgb("#6f7d55"))
    over(img, blobs(21, 26, ["#8c9a66", "#55633f", "#a39a6a", "#7b8a5a"], 120, 330, 150, 70))
    over(img, blobs(22, 3, ["#3f6f8f"], 300, 420, 235, 50, (-150, -200, 150, 200)))
    over(img, blobs(23, 3, ["#3f6f8f"], 300, 460, 235, 50, (950, 1650, 1250, 2000)))
    lay, d = layer()
    rnd = random.Random(8)
    for _ in range(7):
        pts = [(rnd.uniform(0, W), rnd.uniform(300, 1700))]
        for _ in range(4):
            pts.append((pts[-1][0] + rnd.uniform(-320, 320), pts[-1][1] + rnd.uniform(-260, 260)))
        d.line(pts, fill=(196, 184, 140, 150), width=5, joint="curve")
    for x in range(0, W + 1, 135):
        d.line([(x, 0), (x, H)], fill=(255, 255, 255, 46), width=2)
    for y in range(0, H + 1, 135):
        d.line([(0, y), (W, y)], fill=(255, 255, 255, 46), width=2)
    over(img, lay)
    return ImageEnhance.Brightness(grain(img, 6)).enhance(0.72)


def base_pubg(now, prog, end, S):
    if "blue" not in S:
        S["blue"] = Image.blend(S["static"], Image.new("RGB", (W, H), rgb("#1846b8")), 0.5)
    r = 800 - 440 * ease(prog)
    cx, cy = 540 + 60 * math.sin(prog * 2.2), 800 + 50 * prog
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    img = Image.composite(S["static"], S["blue"], m)
    ImageDraw.Draw(img).ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=5)
    return img


def dyn_pubg(img, d, now, prog, end, S):
    alive = max(1, int(round(100 - 99 * ease(prog))))
    paste(img, text_img(f"{alive} ALIVE", "BlackOpsOne-Regular.ttf", 42, "#f2a900", 4, "#11140c"), 540, 372)
    if now < 9:
        k = now / 9
        x, y = -80 + 1300 * k, 470 + 240 * k
        paste(img, icon_img("plane", 64, "#ffffff", 4, "#11140c"), x, y)


def panel_pubg(w, h, kind="main"):
    im, d = _panel(w, h, (20, 24, 16, 232), None, 0, 6, (0, 8, (0, 0, 0, 90)))
    d.rectangle([PM, PM, PM + w, PM + (14 if kind == "main" else 8)], fill=(242, 169, 0, 255))
    return im


# ================================================================ WARDOGS: cash and concrete
def static_wardogs():
    img = grain(vgrad("#2c2f31", "#151718"), 8, 3, 2)
    lay, d = layer()
    rnd = random.Random(4)
    for k in range(9):
        r = 140 + k * 95
        d.ellipse([300 - r * 1.2, 1050 - r, 300 + r * 1.2, 1050 + r * 0.9], outline=(255, 255, 255, 14), width=2)
        d.ellipse([900 - r, 420 - r * 0.8, 900 + r, 420 + r * 0.8], outline=(255, 255, 255, 10), width=2)
    for i, c in enumerate(("#2f6fd6", "#c8372d", "#3f9b4b")):
        d.rectangle([90 + i * 300, 404, 90 + (i + 1) * 300, 412], fill=rgb(c) + (255,))
    for x in range(-40, W + 40, 56):
        d.polygon([(x, 1206), (x + 28, 1206), (x + 48, 1186), (x + 20, 1186)], fill=(232, 190, 40, 210))
    over(img, lay)
    return vignette(img, 0.45)


def dyn_wardogs(img, d, now, prog, end, S):
    for i, (a, b, c, e) in enumerate(S.setdefault("p", particles(22, 3))):
        x = (a * W + now * (30 + 60 * c)) % (W + 20) - 10
        y = 420 + b * 760 + math.sin(now + i) * 14
        r = 1.5 + 2.5 * e
        d.ellipse([x - r, y - r, x + r, y + r], fill=(84, 88, 84))
    cash = 10000 + int(now * 431 + now * now * 37) // 50 * 50
    paste(img, text_img(f"${cash:,}", "Anton-Regular.ttf", 46, "#7ed957"), 540, 368)


def panel_wardogs(w, h, kind="main"):
    im, d = _panel(w, h, (30, 34, 30, 240), (92, 98, 90, 255), 2, 0, (0, 10, (0, 0, 0, 110)))
    if kind == "main":
        for i, c in enumerate(("#2f6fd6", "#c8372d", "#3f9b4b")):
            d.rectangle([PM, PM + i * h // 3, PM + 12, PM + (i + 1) * h // 3], fill=rgb(c) + (255,))
    return im


# ================================================================ ONIMUSHA: ink wash and souls
def static_oni():
    img = grain(vgrad("#f2ead8", "#e0d3b6"), 7, 5, 2)
    lay, d = layer()
    rnd = random.Random(6)
    for _ in range(260):
        x, y, a = rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(0, math.pi)
        L = rnd.uniform(10, 34)
        d.line([(x, y), (x + math.cos(a) * L, y + math.sin(a) * L)], fill=(120, 96, 60, 30), width=1)
    d.ellipse([90, 1360, 430, 1700], fill=(181, 34, 42, 235))
    over(img, lay)
    over(img, blobs(7, 9, ["#141210"], 90, 230, 46, 55, (-60, 900, 420, 1500)))
    over(img, blobs(8, 6, ["#141210"], 70, 190, 40, 50, (700, 1000, 1140, 1400)))
    for k, (y0, a) in enumerate(((1560, 60), (1700, 120))):
        lay, d = layer()
        ridge(d, 31 + k, y0, 230, (20, 18, 16, a), 90)
        over(img, lay, 6 - 3 * k)
    return vignette(img, 0.3, (60, 40, 20))


def dyn_oni(img, d, now, prog, end, S):
    if "orbs" not in S:
        S["orbs"] = [glow_sprite(c, s) for c in ("#d8262e", "#3b7bd8", "#e8b83a") for s in (54, 84)]
    for i, (a, b, c, e) in enumerate(S.setdefault("p", particles(13, 12))):
        k = (b + now * (0.05 + 0.06 * c)) % 1.0
        x0 = a * W
        x = x0 + (CX - x0) * k * 0.55 + math.sin(now * 1.4 + i) * 26
        y = 1500 - k * 1150
        paste(img, S["orbs"][i % 6], x, y)
    paste(img, text_img(f"Souls  {int(now * 9):03d}", "KaushanScript-Regular.ttf", 44, "#b5222a"), 540, 370)


def panel_oni(w, h, kind="main"):
    im, d = _panel(w, h, (18, 16, 15, 244))
    rnd = random.Random(w * 7 + h)
    n = (w + h) // 9
    for _ in range(n):
        side = rnd.choice("tblr")
        r = rnd.uniform(5, 15)
        if side in "tb":
            x, y = PM + rnd.uniform(0, w), PM + (0 if side == "t" else h)
        else:
            x, y = PM + (0 if side == "l" else w), PM + rnd.uniform(0, h)
        d.ellipse([x - r * 2.2, y - r, x + r * 2.2, y + r] if side in "tb" else [x - r, y - r * 2.2, x + r, y + r * 2.2], fill=(18, 16, 15, 244))
    if kind == "main":
        d.line([(PM + 26, PM + 22), (PM + w - 26, PM + 22)], fill=(181, 34, 42, 255), width=4)
    return im


# ================================================================ BLOOD OF DAWNWALKER: day and night
def _dawn(night):
    img = vgrad("#0d0508", "#4a0c16") if night else vgrad("#f6d58a", "#d9773f")
    lay, d = layer()
    if night:
        rnd = random.Random(2)
        for _ in range(120):
            x, y, r = rnd.uniform(0, W), rnd.uniform(0, 1200), rnd.choice([1, 1.5, 2, 2.5])
            d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 235, 220, rnd.randint(90, 230)))
    over(img, lay)
    over(img, blobs(1, 1, ["#ff3048" if night else "#fff3c4"], 230, 231, 150, 70, (799, 569, 801, 571)))
    lay, d = layer()
    d.ellipse([670, 440, 930, 700], fill=(200, 30, 46, 255) if night else (255, 244, 205, 255))
    if night:
        for (x, y, r) in ((740, 520, 26), (840, 600, 34), (790, 640, 16), (860, 500, 14)):
            d.ellipse([x - r, y - r, x + r, y + r], fill=(170, 22, 38, 255))
    over(img, lay, 1)
    for k, (y0, amp) in enumerate(((1330, 260), (1500, 200), (1680, 150))):
        lay, d = layer()
        dark = (10 + 4 * k, 3, 6, 255) if night else (92 - 26 * k, 44 - 12 * k, 30 - 8 * k, 255)
        ridge(d, 51 + k, y0, amp, dark, 80)
        over(img, lay, 1)
    lay, d = layer()
    rnd = random.Random(14)
    for _ in range(26):
        x, hgt = rnd.uniform(0, W), rnd.uniform(90, 190)
        col = (6, 2, 4, 255) if night else (40, 20, 14, 255)
        for j in range(3):
            ww = 46 - j * 12
            d.polygon([(x - ww, 1920 - j * hgt / 3), (x + ww, 1920 - j * hgt / 3), (x, 1920 - (j + 1.4) * hgt / 3)], fill=col)
    over(img, lay)
    return grain(img, 4)


def static_dawn():
    return _dawn(False)


def base_dawn(now, prog, end, S):
    if "night" not in S:
        S["night"] = _dawn(True)
    k = 0.5 - 0.5 * math.cos(2 * math.pi * now / 14)
    S["k"] = k
    return Image.blend(S["static"], S["night"], k)


def dyn_dawn(img, d, now, prog, end, S):
    k = S.get("k", 0)
    day = 30 - min(29, int(prog * 30))
    col = mix("#5a2408", "#ffcf5a", k)
    paste(img, icon_img("moon" if k > 0.5 else "sun", 40, col), 388, 372)
    paste(img, text_img(f"{day} days left", "PirataOne-Regular.ttf", 46, col), 560, 372)


def panel_dawn(w, h, kind="main"):
    im, d = _panel(w, h, (26, 10, 14, 234), (217, 164, 65, 255), 3, 22, (0, 10, (0, 0, 0, 100)))
    if kind == "main":
        d.regular_polygon((PM + w // 2, PM, 16), 4, rotation=45, fill=(217, 164, 65))
        d.regular_polygon((PM + w // 2, PM + h, 16), 4, rotation=45, fill=(190, 30, 46))
    return im


# ================================================================ CONTROL RESONANT: brutalist
def static_control():
    img = grain(Image.new("RGB", (W, H), rgb("#c9c6c0")), 7, 9, 3)
    lay, d = layer()
    for y in range(0, H, 168):
        d.line([(0, y), (W, y)], fill=(0, 0, 0, 26), width=2)
    for x in range(0, W, 270):
        d.line([(x, 0), (x, H)], fill=(0, 0, 0, 12), width=2)
    d.rectangle([0, 1520, W, H], fill=(8, 8, 8, 255))
    d.rectangle([0, 0, W, 96], fill=(8, 8, 8, 255))
    d.rectangle([0, 1506, W, 1520], fill=(228, 0, 43, 255))
    over(img, lay)
    return vignette(img, 0.25)


def dyn_control(img, d, now, prog, end, S):
    for i, (a, b, c, e) in enumerate(S.setdefault("p", particles(6, 17))):
        w_, h_ = 70 + 190 * a, 60 + 260 * b
        x = [-20, 930, 70, 860, -40, 980][i] + math.sin(now * (0.25 + 0.2 * c) + i) * 30
        y = 430 + i * 150 + math.sin(now * (0.3 + 0.25 * e) + i * 2) * 60
        d.rectangle([x, y, x + w_, y + h_], fill=(12, 12, 12))
    x = 60 + (now * 34) % 960
    d.rectangle([x, 96, x + 5, 420], fill=(228, 0, 43))
    s = 16 + 6 * math.sin(now * 3)
    d.rectangle([540 - s, 372 - s, 540 + s, 372 + s], fill=(228, 0, 43))


def panel_control(w, h, kind="main"):
    return _panel(w, h, (0, 0, 0, 255), None, 0, 0, (14, 14, (228, 0, 43, 255)))[0]


# ================================================================ MARVEL'S WOLVERINE: comic book
def static_wolv():
    img = Image.new("RGB", (W, H), rgb("#ffd500"))
    d = ImageDraw.Draw(img)
    for i in range(18):
        a0, a1 = math.radians(i * 20), math.radians(i * 20 + 10)
        d.polygon([(CX, CY), (CX + 2200 * math.cos(a0), CY + 2200 * math.sin(a0)), (CX + 2200 * math.cos(a1), CY + 2200 * math.sin(a1))], fill=rgb("#ffc400"))
    for yi, y in enumerate(range(0, H, 26)):
        for x in range(0 if yi % 2 else 13, W, 26):
            r = 1.5 + 8.5 * (math.hypot(x - CX, y - CY) / 1200) ** 1.4
            d.ellipse([x - r, y - r, x + r, y + r], fill=rgb("#f59a00"))
    d.polygon([(0, 1500), (W, 1380), (W, H), (0, H)], fill=rgb("#1f4fd8"))
    for yi, y in enumerate(range(1400, H, 30)):
        for x in range(0 if yi % 2 else 15, W, 30):
            if y > 1500 - (x / W) * 120 + 16:
                d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=rgb("#3b68e6"))
    d.line([(0, 1500), (W, 1380)], fill=(10, 10, 10), width=16)
    d.rectangle([0, 0, W - 1, H - 1], outline=(10, 10, 10), width=16)
    return img


def dyn_wolv(img, d, now, prog, end, S):
    for i, (a, b, c, e) in enumerate(S.setdefault("p", particles(9, 23))):
        k = (b + now * (0.5 + 0.5 * c)) % 1.0
        x = -200 + k * 1500
        y = 440 + a * 700 - k * 120
        L = 90 + 160 * e
        d.line([(x, y), (x + L, y - L * 0.11)], fill=(20, 20, 20), width=5 if e > 0.5 else 3)
    s = 1 + 0.06 * math.sin(now * 6)
    paste(img, icon_img("bolt", 52, "#e10600", 5, "#111111"), 540, 372, s)


def panel_wolv(w, h, kind="main"):
    return _panel(w, h, (255, 255, 255, 255), (12, 12, 12, 255), 9, 0, (14, 14, (12, 12, 12, 255)))[0]


# ================================================================ THE WITCHER 3: parchment map
def static_witcher():
    img = grain(vgrad("#decba2", "#c8b183"), 10, 13, 2)
    over(img, blobs(41, 14, ["#8a6a3a", "#a98a52"], 80, 260, 34, 60))
    lay, d = layer()
    ink = (74, 52, 30, 70)
    rnd = random.Random(19)
    for k in range(7):
        x, y, r = rnd.uniform(100, 980), rnd.uniform(450, 1700), rnd.uniform(120, 300)
        for j in range(3):
            rr = r - j * 34
            if rr > 30:
                d.arc([x - rr * 1.3, y - rr, x + rr * 1.3, y + rr], rnd.uniform(0, 200), rnd.uniform(220, 360), fill=ink, width=2)
    for _ in range(16):
        x, y = rnd.uniform(60, 1020), rnd.uniform(1250, 1850)
        d.line([(x - 22, y + 20), (x, y - 20), (x + 22, y + 20)], fill=(74, 52, 30, 110), width=3)
    cx, cy = 890, 1250
    for ang in range(0, 360, 45):
        L = 92 if ang % 90 == 0 else 54
        c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        d.line([(cx, cy), (cx + c * L, cy + s * L)], fill=(74, 52, 30, 150), width=3)
    d.ellipse([cx - 62, cy - 62, cx + 62, cy + 62], outline=(74, 52, 30, 150), width=3)
    pts = [(110 + i * 34, 1210 - 300 * math.sin(i / 26 * math.pi) - i * 9) for i in range(27)]
    for i in range(0, 26, 2):
        d.line([pts[i], pts[i + 1]], fill=(139, 26, 26, 150), width=4)
    over(img, lay)
    return vignette(img, 0.5, (70, 44, 16))


def dyn_witcher(img, d, now, prog, end, S):
    for i, (a, b, c, e) in enumerate(S.setdefault("p", particles(34, 29))):
        y = (b * H + now * (70 + 90 * c)) % (H + 20) - 10
        x = (a * W + math.sin(now * 0.8 + i) * 36 + now * 14) % W
        r = 2 + 3 * e
        d.ellipse([x - r, y - r, x + r, y + r], fill=mix("#fffaf0", "#d8c59c", 0.35 * e))
    paste(img, icon_img("feather-pointed", 40, "#8b1a1a"), 540, 372)


def panel_witcher(w, h, kind="main"):
    im, d = _panel(w, h, (241, 230, 198, 255), (122, 92, 52, 255), 3, 4, (8, 12, (40, 24, 8, 120)), 6)
    rnd = random.Random(w + h)
    for _ in range(24):
        x, y = PM + rnd.uniform(10, w - 10), PM + rnd.uniform(10, h - 10)
        r = rnd.uniform(8, 30)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(214, 196, 150, 60))
    if kind == "main":
        d.ellipse([PM + w // 2 - 15, PM - 4, PM + w // 2 + 15, PM + 26], fill=(150, 26, 26, 255), outline=(70, 10, 10, 255), width=3)
        im = im.rotate(0.8, resample=Image.BICUBIC)
    return im


# ================================================================ AION 2: wings and starlight
def _wing(d, cx, cy, side, col):
    for k in range(9):
        a = math.radians(-78 + k * 17)
        L = 520 - k * 30
        x2, y2 = cx + side * math.cos(a) * L, cy + math.sin(a) * L * 0.9
        w = 46 - k * 3
        d.polygon([(cx, cy - w / 2), (cx, cy + w / 2), (x2, y2)], fill=col)


def static_aion():
    img = vgrad("#0b0a2e", "#3a1f6e")
    over(img, blobs(61, 5, ["#f2c86b", "#8d6bff", "#3fb6ff"], 200, 420, 60, 110, (0, 300, W, 1300)))
    lay, d = layer()
    rnd = random.Random(7)
    for _ in range(170):
        x, y, r = rnd.uniform(0, W), rnd.uniform(0, H), rnd.choice([1, 1.5, 2, 3])
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 244, 214, rnd.randint(70, 220)))
    over(img, lay)
    lay, d = layer()
    _wing(d, 40, 1250, 1, (255, 255, 255, 34))
    _wing(d, 1040, 1250, -1, (255, 255, 255, 34))
    over(img, lay, 3)
    return vignette(img, 0.45)


def dyn_aion(img, d, now, prog, end, S):
    for i, (a, b, c, e) in enumerate(S.setdefault("p", particles(16, 61))):
        y = (b * H + now * (50 + 60 * c)) % (H + 40) - 20
        x = a * W + math.sin(now * 0.8 + i * 1.3) * 70
        w_, h_ = 16 + 10 * e, 5 + 3 * e
        d.ellipse([x - w_, y - h_, x + w_, y + h_], fill=mix("#ffffff", "#b9a8ff", e))
    left = 60 - int(now) % 60
    paste(img, icon_img("feather-pointed", 34, "#f2c86b"), 418, 372)
    paste(img, text_img(f"FLIGHT TIME 0:{left % 60:02d}", "Marcellus-Regular.ttf", 38, "#f2c86b"), 580, 372)


def panel_aion(w, h, kind="main"):
    im, d = _panel(w, h, (16, 12, 48, 232), (242, 200, 107, 255), 3, 18, (0, 10, (0, 0, 0, 110)))
    if kind == "main":
        d.rounded_rectangle([PM + 12, PM + 12, PM + w - 12, PM + h - 12], 12, outline=(141, 107, 255, 160), width=2)
        for x in (PM + w // 2 - 60, PM + w // 2, PM + w // 2 + 60):
            d.regular_polygon((x, PM, 9 if x != PM + w // 2 else 14), 4, rotation=45, fill=(242, 200, 107))
    return im


# ================================================================ DEADLOCK: occult noir city
def static_deadlock():
    img = vgrad("#04100f", "#12302b")
    over(img, blobs(71, 1, ["#5ff0c8"], 300, 301, 70, 120, (539, 699, 541, 701)))
    lay, d = layer()
    rnd = random.Random(12)
    x = -20
    while x < W:
        bw, bh = rnd.randint(90, 190), rnd.randint(380, 900)
        top = H - bh
        d.rectangle([x, top, x + bw, H], fill=(5, 12, 12, 255))
        if rnd.random() < 0.6:
            d.rectangle([x + bw * 0.3, top - 60, x + bw * 0.7, top], fill=(5, 12, 12, 255))
            d.line([(x + bw / 2, top - 60), (x + bw / 2, top - 150)], fill=(5, 12, 12, 255), width=6)
        for wy in range(int(top) + 30, H - 20, 46):
            for wx in range(int(x) + 16, int(x + bw) - 16, 30):
                if rnd.random() < 0.22:
                    d.rectangle([wx, wy, wx + 12, wy + 22], fill=(233, 161, 59, rnd.randint(110, 230)))
        x += bw + rnd.randint(4, 22)
    over(img, lay)
    return vignette(grain(img, 6, 4), 0.55)


def dyn_deadlock(img, d, now, prog, end, S):
    for i, (a, b, c, e) in enumerate(S.setdefault("p", particles(46, 33))):
        y = (b * H + now * (900 + 500 * c)) % (H + 60) - 30
        x = (a * (W + 300) - 150) - (y / H) * 120
        d.line([(x, y), (x - 6, y + 34 + 20 * e)], fill=(120, 170, 160), width=2)
    on = (int(now * 9) % 11) != 3
    col = "#e9a13b" if on else "#5c3f17"
    paste(img, icon_img("fire-flame-curved", 34, col), 414, 372)
    paste(img, text_img(f"SOULS {int(1200 + now * 317):,}", "Limelight-Regular.ttf", 38, col), 580, 372)


def panel_deadlock(w, h, kind="main"):
    im, d = _panel(w, h, (8, 16, 16, 240), (233, 161, 59, 255), 3, 0, (0, 12, (0, 0, 0, 120)))
    if kind == "main":
        d.rectangle([PM + 10, PM + 10, PM + w - 10, PM + h - 10], outline=(233, 161, 59, 120), width=1)
        for (x, y, sx, sy) in ((PM, PM, 1, 1), (PM + w, PM, -1, 1), (PM, PM + h, 1, -1), (PM + w, PM + h, -1, -1)):
            for k in range(3):
                d.rectangle([min(x, x + sx * (36 - k * 12)), min(y + sy * k * 8, y + sy * (k * 8 + 6)),
                             max(x, x + sx * (36 - k * 12)), max(y + sy * k * 8, y + sy * (k * 8 + 6))], fill=(233, 161, 59, 255))
    return im


# ================================================================ ACE COMBAT 8: sky and HUD
def static_ace():
    img = vgrad("#0a2a66", "#9fd0f5")
    over(img, blobs(81, 9, ["#ffffff"], 160, 380, 150, 70, (-100, 1250, W + 100, 1900)))
    over(img, blobs(82, 5, ["#ffffff", "#dcefff"], 120, 260, 90, 80, (-100, 500, W + 100, 1150)))
    over(img, blobs(83, 1, ["#fff6d0"], 200, 201, 170, 90, (859, 479, 861, 481)))
    return img


def base_ace(now, prog, end, S):
    if "cl" not in S:
        cl = blobs(84, 7, ["#ffffff"], 120, 260, 120, 60, (0, 900, W, 1500))
        S["cl"] = cl
    img = S["static"].copy()
    x = int((now * 38) % W)
    img.paste(S["cl"], (x, 0), S["cl"])
    img.paste(S["cl"], (x - W, 0), S["cl"])
    return img


def dyn_ace(img, d, now, prog, end, S):
    g = (124, 255, 107)
    for k in range(-3, 4):
        y = CY + k * 150 + math.sin(now * 0.7) * 40
        L = 70 if k else 150
        d.line([(60, y), (60 + L, y)], fill=g, width=3)
        d.line([(W - 60 - L, y), (W - 60, y)], fill=g, width=3)
    for (x, y, sx, sy) in ((36, 420, 1, 1), (1044, 420, -1, 1), (36, 1190, 1, -1), (1044, 1190, -1, -1)):
        d.line([(x, y), (x + 60 * sx, y)], fill=g, width=4)
        d.line([(x, y), (x, y + 60 * sy)], fill=g, width=4)
    k = (now % 11) / 11
    if k < 0.75:
        x, y = -80 + 1400 * (k / 0.75), 1240 - 160 * (k / 0.75)
        d.line([(x - 260, y + 30), (x - 20, y + 3)], fill=(255, 255, 255), width=5)
        paste(img, icon_img("jet-fighter", 58, "#f4f8ff", 4, "#0a2a66"), x, y)
    paste(img, text_img(f"SPD {1725 + int(60 * math.sin(now * 1.3))}   ALT {31250 + int(now * 77) % 900:,}", "Oxanium[wght].ttf", 36, "#7cff6b", 3, "#06203f", 700), 540, 372)


def panel_ace(w, h, kind="main"):
    im, d = _panel(w, h, (6, 22, 48, 222), (124, 255, 107, 255), 2, 10)
    if kind == "main":
        for (x, y, sx, sy) in ((PM, PM, 1, 1), (PM + w, PM, -1, 1), (PM, PM + h, 1, -1), (PM + w, PM + h, -1, -1)):
            d.line([(x + 18 * sx, y + 18 * sy), (x + 58 * sx, y + 18 * sy)], fill=(124, 255, 107), width=4)
            d.line([(x + 18 * sx, y + 18 * sy), (x + 18 * sx, y + 58 * sy)], fill=(124, 255, 107), width=4)
    return im


# ================================================================ DRESSMAKER: cozy sewing table
def static_dress():
    img = Image.new("RGB", (W, H), rgb("#f8efe2"))
    lay, d = layer()
    for x in range(0, W, 54):
        d.rectangle([x, 0, x + 27, H], fill=(236, 150, 178, 26))
    for y in range(0, H, 54):
        d.rectangle([0, y, W, y + 27], fill=(236, 150, 178, 26))
    over(img, lay)
    over(img, blobs(91, 6, ["#ffd1e0", "#cfe6d4", "#ffe6b3"], 160, 320, 110, 90))
    lay, d = layer()
    d.rectangle([0, 396, W, 426], fill=(255, 209, 77, 255))
    for i, x in enumerate(range(0, W, 18)):
        d.line([(x, 396), (x, 396 + (18 if i % 5 == 0 else 10))], fill=(60, 42, 53, 255), width=2)
    rnd = random.Random(5)
    for _ in range(11):
        x, y, r = rnd.uniform(60, 1020), rnd.uniform(1480, 1860), rnd.uniform(24, 44)
        col = rgb(rnd.choice(["#d6457a", "#6aa58a", "#f2b84b", "#5b8fd6"]))
        d.ellipse([x - r, y - r, x + r, y + r], fill=col + (255,), outline=(60, 42, 53, 255), width=3)
        for (dx, dy) in ((-0.3, -0.3), (0.3, -0.3), (-0.3, 0.3), (0.3, 0.3)):
            d.ellipse([x + dx * r - 4, y + dy * r - 4, x + dx * r + 4, y + dy * r + 4], fill=(60, 42, 53, 255))
    over(img, lay)
    return grain(img, 4, 2)


def dyn_dress(img, d, now, prog, end, S):
    y = 1212
    x_end = 40 + (now * 150) % 1000
    x = 40
    while x < x_end:
        d.line([(x, y), (min(x + 22, x_end), y)], fill=(214, 69, 122), width=6)
        x += 38
    d.line([(x_end, y), (x_end + 46, y - 46)], fill=(120, 120, 130), width=5)
    d.ellipse([x_end + 38, y - 56, x_end + 52, y - 42], outline=(120, 120, 130), width=3)
    paste(img, icon_img("scissors", 34, "#d6457a"), 430, 468 - 96)
    paste(img, text_img(f"Orders done: {int(now * 0.9) + 1}", "Nunito[wght].ttf", 38, "#3a2a35", wght=900), 580, 372)


def panel_dress(w, h, kind="main"):
    im, d = _panel(w, h, (255, 252, 246, 255), None, 0, 30, (0, 12, (120, 80, 90, 90)), 8)
    m = 14
    x0, y0, x1, y1 = PM + m, PM + m, PM + w - m, PM + h - m
    step = 30
    for x in range(int(x0) + 16, int(x1) - 16, step):
        d.line([(x, y0), (x + 16, y0)], fill=(214, 69, 122, 255), width=4)
        d.line([(x, y1), (x + 16, y1)], fill=(214, 69, 122, 255), width=4)
    if kind == "main":
        for y in range(int(y0) + 16, int(y1) - 16, step):
            d.line([(x0, y), (x0, y + 16)], fill=(214, 69, 122, 255), width=4)
            d.line([(x1, y), (x1, y + 16)], fill=(214, 69, 122, 255), width=4)
    return im


# ================================================================ BONGO CAT: desk doodle
def _paw(d, x, y, s, fill, out=(27, 27, 31, 255)):
    d.ellipse([x - 26 * s, y - 20 * s, x + 26 * s, y + 24 * s], fill=fill, outline=out, width=max(2, int(5 * s)))
    for dx in (-24, -8, 8, 24):
        d.ellipse([x + dx * s - 9 * s, y - 40 * s, x + dx * s + 9 * s, y - 20 * s], fill=fill, outline=out, width=max(2, int(4 * s)))


def static_bongo():
    img = vgrad("#ffffff", "#dff1ff")
    over(img, blobs(101, 7, ["#ffd9e6", "#fff2b8", "#cdeeff"], 150, 300, 150, 60))
    lay, d = layer()
    rnd = random.Random(3)
    for _ in range(16):
        _paw(d, rnd.uniform(60, 1020), rnd.uniform(1300, 1880), rnd.uniform(0.6, 1.1), (255, 190, 210, 120), (255, 150, 180, 150))
    over(img, lay)
    lay, d = layer()
    pts = [(x, 1214 + 5 * math.sin(x / 37)) for x in range(-10, W + 20, 12)]
    d.line(pts, fill=(27, 27, 31, 255), width=9, joint="curve")
    over(img, lay)
    return img


def dyn_bongo(img, d, now, prog, end, S):
    beat = now * 5.2
    for j, cx in enumerate((300, 780)):
        down = (int(beat) % 2 == j) and (beat % 1) < 0.55
        y = 1168 + (34 if down else 0)
        d.ellipse([cx - 62, y - 44, cx + 62, y + 52], fill=(255, 255, 255), outline=(27, 27, 31), width=9)
        if down:
            for k in (-1, 0, 1):
                d.line([(cx + k * 60, 1124), (cx + k * 82, 1086)], fill=(255, 93, 143), width=7)
    paste(img, icon_img("keyboard", 34, "#ff5d8f"), 400, 372)
    paste(img, text_img(f"Taps: {int(now * 173):,}", "Baloo2[wght].ttf", 40, "#1b1b1f", wght=800), 570, 372)


def panel_bongo(w, h, kind="main"):
    return _panel(w, h, (255, 255, 255, 255), (27, 27, 31, 255), 8, 34, (12, 14, (255, 93, 143, 255)))[0]


# ================================================================ GEARS OF WAR: E-DAY: ash and embers
def static_gears():
    img = vgrad("#0b0b0c", "#2a2523")
    over(img, blobs(111, 4, ["#c2410c", "#7c1d12"], 260, 460, 120, 130, (0, 1500, W, 2000)))
    lay, d = layer()
    for cx in (110, 300, 800, 990):
        top = 1080 + (cx * 7) % 260
        d.rectangle([cx - 38, top, cx + 38, H], fill=(14, 13, 13, 255))
        d.rectangle([cx - 54, top - 26, cx + 54, top], fill=(14, 13, 13, 255))
        for k in range(-2, 3):
            d.line([(cx + k * 15, top + 10), (cx + k * 15, H)], fill=(30, 28, 27, 255), width=3)
    d.pieslice([360, 1180, 720, 1540], 180, 360, fill=(14, 13, 13, 255))
    d.rectangle([340, 1360, 740, H], fill=(14, 13, 13, 255))
    d.polygon([(600, 1180), (720, 1360), (640, 1300)], fill=(42, 37, 35, 255))
    over(img, lay)
    over(img, blobs(112, 8, ["#555049"], 140, 300, 50, 80, (0, 300, W, 1300)))
    return vignette(grain(img, 9, 6, 2), 0.6)


def dyn_gears(img, d, now, prog, end, S):
    R, r2 = 470, 500
    for k in range(24):
        a = math.radians(k * 15 + now * 6)
        a2 = math.radians(k * 15 + 7 + now * 6)
        d.polygon([(CX + R * math.cos(a), CY + R * math.sin(a)), (CX + r2 * math.cos(a), CY + r2 * math.sin(a)),
                   (CX + r2 * math.cos(a2), CY + r2 * math.sin(a2)), (CX + R * math.cos(a2), CY + R * math.sin(a2))], fill=(70, 22, 20))
    d.ellipse([CX - R, CY - R, CX + R, CY + R], outline=(70, 22, 20), width=6)
    for i, (a, b, c, e) in enumerate(S.setdefault("p", particles(34, 44))):
        y = H - ((b * H + now * (120 + 220 * c)) % (H + 40))
        x = a * W + math.sin(now * 1.6 + i) * 40
        r = 2 + 3 * e
        d.ellipse([x - r, y - r, x + r, y + r], fill=mix("#ffb347", "#d1161c", (1 - y / H)))
    t = int(now)
    paste(img, text_img(f"E-DAY +00:{t // 60:02d}:{t % 60:02d}", "SairaStencilOne-Regular.ttf", 38, "#d1161c"), 540, 372)


def panel_gears(w, h, kind="main"):
    im, d = _panel(w, h, (36, 37, 38, 244), (12, 12, 12, 255), 6, 0, (0, 12, (0, 0, 0, 150)))
    d.rectangle([PM + 6, PM + 6, PM + w - 6, PM + (20 if kind == "main" else 14)], fill=(209, 22, 28, 255))
    if kind == "main":
        rnd = random.Random(w * 3 + h)
        for _ in range(26):
            x, y = PM + rnd.uniform(20, w - 20), PM + rnd.uniform(30, h - 20)
            L = rnd.uniform(12, 60)
            d.line([(x, y), (x + L, y + rnd.uniform(-5, 5))], fill=(70, 72, 74, 255), width=1)
        for (x, y) in ((PM + 22, PM + 40), (PM + w - 22, PM + 40), (PM + 22, PM + h - 22), (PM + w - 22, PM + h - 22)):
            d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=(92, 94, 96, 255), outline=(12, 12, 12, 255), width=2)
    return im


# ================================================================ STAR WARS: GALACTIC RACER: neon desert
HZ = 1215


def static_swr():
    top = vgrad("#170a3c", "#ff7a3d").resize((W, HZ))
    img = Image.new("RGB", (W, H), rgb("#1a0d14"))
    img.paste(top, (0, 0))
    lay, d = layer()
    d.ellipse([720, HZ - 330, 900, HZ - 150], fill=(255, 226, 170, 255))
    d.ellipse([880, HZ - 250, 990, HZ - 140], fill=(255, 190, 130, 255))
    over(img, lay, 2)
    lay, d = layer()
    for (x0, x1, hgt) in ((-40, 260, 150), (200, 420, 90), (820, 1120, 120)):
        d.polygon([(x0, HZ), (x0 + 40, HZ - hgt), (x1 - 50, HZ - hgt), (x1, HZ)], fill=(60, 22, 50, 255))
    d.rectangle([0, HZ, W, H], fill=(22, 10, 26, 255))
    for k in range(-9, 10):
        d.line([(540 + k * 16, HZ), (540 + k * 330, H)], fill=(41, 240, 255, 90), width=3)
    over(img, lay)
    return grain(img, 4)


def dyn_swr(img, d, now, prog, end, S):
    for j in range(9):
        k = ((j / 9) + now * 0.9) % 1.0
        y = HZ + (H - HZ) * k ** 2.2
        d.line([(0, y), (W, y)], fill=mix("#170a3c", "#29f0ff", 0.25 + 0.75 * k), width=max(1, int(1 + 5 * k)))
    for i, (a, b, c, e) in enumerate(S.setdefault("p", particles(14, 55))):
        k = (b + now * (0.9 + 0.9 * c)) % 1.0
        x = W - k * (W + 400)
        y = 440 + a * 720
        L = 120 + 260 * e
        d.line([(x, y), (x + L, y)], fill=mix("#ffffff", "#ff7a3d", e), width=3 if e > 0.5 else 2)
    paste(img, text_img(f"SPEED {742 + int(38 * math.sin(now * 2.1)) + int(now * 3)} KM/H", "Audiowide-Regular.ttf", 34, "#29f0ff", 3, "#170a3c"), 540, 372)


def panel_swr(w, h, kind="main"):
    im = Image.new("RGBA", (w + 2 * PM, h + 2 * PM), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = 34 if kind == "main" else 16
    pts = [(PM + c, PM), (PM + w, PM), (PM + w, PM + h - c), (PM + w - c, PM + h), (PM, PM + h), (PM, PM + c)]
    d.polygon(pts, fill=(20, 8, 44, 232))
    d.line(pts + [pts[0]], fill=(41, 240, 255, 255), width=4, joint="curve")
    if kind == "main":
        d.line([(PM + w - 150, PM + h - 10), (PM + w - c - 6, PM + h - 10)], fill=(255, 179, 71, 255), width=6)
    return im


# ================================================================ CALL OF DUTY: MODERN WARFARE 4: night vision
def static_mw4():
    img = radial("#0f3a1c", "#020804", CX, 820, 1050)
    lay, d = layer()
    rnd = random.Random(23)
    for _ in range(9):
        x, y, r = rnd.uniform(0, W), rnd.uniform(300, 1800), rnd.uniform(160, 420)
        for j in range(4):
            rr = r - j * 36
            if rr > 30:
                d.ellipse([x - rr * 1.3, y - rr, x + rr * 1.3, y + rr], outline=(109, 255, 143, 20), width=2)
    for r in (150, 300, 450):
        d.ellipse([CX - r, CY - r, CX + r, CY + r], outline=(109, 255, 143, 30), width=2)
    d.line([(CX - 500, CY), (CX + 500, CY)], fill=(109, 255, 143, 26), width=2)
    d.line([(CX, CY - 380), (CX, CY + 380)], fill=(109, 255, 143, 26), width=2)
    for y in range(0, H, 4):
        d.line([(0, y), (W, y)], fill=(0, 0, 0, 46), width=1)
    over(img, lay)
    return vignette(grain(img, 10, 8), 0.7)


def dyn_mw4(img, d, now, prog, end, S):
    y = int((now * 260) % (H + 200)) - 100
    for k in range(6):
        d.line([(0, y - k * 5), (W, y - k * 5)], fill=mix("#6dff8f", "#061a0c", 0.45 + k * 0.1), width=2)
    for (x, y0, sx, sy) in ((36, 420, 1, 1), (1044, 420, -1, 1), (36, 1190, 1, -1), (1044, 1190, -1, -1)):
        d.line([(x, y0), (x + 80 * sx, y0)], fill=(109, 255, 143), width=4)
        d.line([(x, y0), (x, y0 + 80 * sy)], fill=(109, 255, 143), width=4)
    if int(now * 2) % 2 == 0:
        d.ellipse([318, 362, 338, 382], fill=(255, 59, 48))
    t = int(now)
    paste(img, text_img(f"REC  37.5665 N  126.9780 E  00:{t % 60:02d}", "Teko[wght].ttf", 40, "#6dff8f", wght=600), 580, 374)


def panel_mw4(w, h, kind="main"):
    im, d = _panel(w, h, (3, 12, 6, 238), (109, 255, 143, 255), 2)
    if kind == "main":
        d.rectangle([PM, PM, PM + 150, PM + 10], fill=(109, 255, 143, 255))
        d.rectangle([PM + w - 60, PM + h - 10, PM + w, PM + h], fill=(109, 255, 143, 255))
    return im


# ================================================================ PHANTOM BLADE ZERO: ink and steel
def static_pbz():
    img = vgrad("#0a0d10", "#1e262c")
    over(img, blobs(121, 10, ["#000000"], 120, 300, 110, 60))
    lay, d = layer()
    for k in range(60):
        a0 = k * 6
        wdt = int(26 + 20 * math.sin(k * 0.21) + (10 if k % 7 == 0 else 0))
        d.arc([CX - 430, CY - 430, CX + 430, CY + 430], a0, a0 + 5.4 if k < 54 else a0 + 2, fill=(170, 26, 30, 210), width=max(6, wdt))
    over(img, lay, 2)
    lay, d = layer()
    rnd = random.Random(31)
    for _ in range(8):
        x = rnd.uniform(-200, W)
        d.line([(x, 1920), (x + 520, 300)], fill=(200, 215, 225, 16), width=rnd.choice([2, 3, 6]))
    over(img, lay)
    return vignette(grain(img, 7, 9), 0.6)


def dyn_pbz(img, d, now, prog, end, S):
    for i, (a, b, c, e) in enumerate(S.setdefault("p", particles(40, 66))):
        y = (b * H + now * (1000 + 600 * c)) % (H + 60) - 30
        x = a * (W + 200) - 100 + (y / H) * 90
        d.line([(x, y), (x + 5, y + 30 + 22 * e)], fill=(120, 140, 150), width=2)
    k = (now % 3.2) / 0.22
    if k < 1:
        x0 = -200 + 1500 * k
        d.line([(x0, 1250), (x0 + 420, 420)], fill=(240, 244, 248), width=int(10 * (1 - k)) + 2)
    days = max(1, 66 - int(prog * 65))
    paste(img, text_img(f"{days} DAYS LEFT", "Eczar[wght].ttf", 40, "#e02a2a", wght=800), 540, 372)


def panel_pbz(w, h, kind="main"):
    im, d = _panel(w, h, (8, 10, 12, 244))
    rnd = random.Random(w * 5 + h)
    for _ in range((w + h) // 10):
        side = rnd.choice("tb")
        x, y = PM + rnd.uniform(0, w), PM + (0 if side == "t" else h)
        r = rnd.uniform(4, 13)
        d.ellipse([x - r * 2.6, y - r, x + r * 2.6, y + r], fill=(8, 10, 12, 244))
    if kind == "main":
        d.line([(PM + 20, PM + 20), (PM + 20, PM + h - 20)], fill=(150, 170, 182, 255), width=2)
        d.rectangle([PM + w - 64, PM + 18, PM + w - 22, PM + 60], fill=(224, 42, 42, 255))
        d.rectangle([PM + w - 54, PM + 28, PM + w - 32, PM + 50], outline=(8, 10, 12, 255), width=3)
    return im


# ================================================================ DANDY'S WORLD: cartoon stage with a dark side
def static_dandy():
    img = vgrad("#8fe3d9", "#ffc1dc")
    lay, d = layer()
    for k, c in enumerate(("#ff6b8b", "#ffb347", "#ffe14d", "#7bd88f", "#6cb6ff", "#b28dff")):
        r = 1150 - k * 62
        d.pieslice([CX - r, 1260 - r, CX + r, 1260 + r], 180, 360, fill=rgb(c) + (120,))
    d.pieslice([CX - 770, 1260 - 770, CX + 770, 1260 + 770], 180, 360, fill=(255, 246, 228, 255))
    over(img, lay)
    lay, d = layer()
    sq = 90
    for iy, y in enumerate(range(1260, H, sq)):
        for ix, x in enumerate(range(0, W, sq)):
            d.rectangle([x, y, x + sq, y + sq], fill=(29, 26, 38, 255) if (ix + iy) % 2 else (255, 246, 228, 255))
    d.rectangle([0, 1250, W, 1264], fill=(29, 26, 38, 255))
    over(img, lay)
    return vignette(grain(img, 6, 11, 2), 0.62, (20, 8, 30))


def dyn_dandy(img, d, now, prog, end, S):
    rnd = random.Random(int(now * 12))
    for _ in range(3):
        x = rnd.uniform(0, W)
        d.line([(x, 0), (x + rnd.uniform(-6, 6), H)], fill=(255, 255, 255) if rnd.random() < 0.6 else (40, 30, 50), width=1)
    for i, (a, b, c, e) in enumerate(S.setdefault("p", particles(7, 77))):
        x = 80 + a * 920
        y = 520 + b * 560 + math.sin(now * (1.4 + c) + i) * 26
        paste(img, icon_img("star", int(30 + 26 * e), ["#ffe14d", "#ff6b8b", "#6cb6ff"][i % 3], 4, "#1d1a26"), x, y)
    floor = 1 + int(now / 3.2)
    paste(img, icon_img("elevator", 36, "#1d1a26"), 440, 372)
    paste(img, text_img(f"FLOOR {floor:02d}", "Chewy-Regular.ttf", 42, "#1d1a26"), 570, 372)


def panel_dandy(w, h, kind="main"):
    return _panel(w, h, (255, 246, 228, 255), (29, 26, 38, 255), 9, 40, (12, 14, (29, 26, 38, 255)))[0]


# ================================================================ registry
# ================================================================ THE BINDING OF ISAAC: basement floor and tears
def static_isaac():
    img = radial("#5e4838", "#1b130f", CX, 820, 1150)
    lay, d = layer()
    rnd = random.Random(66)
    for y in range(240, H, 150):
        off = 0 if (y // 150) % 2 else 80
        for x in range(-80 + off, W, 160):
            d.rounded_rectangle([x + 4, y + 4, x + 156, y + 146], 14, outline=(20, 12, 8, 64), width=5)
    for _ in range(30):
        x, y = rnd.uniform(40, 1040), rnd.uniform(280, 1880)
        pts = [(x, y)]
        for k in range(4):
            x += rnd.uniform(-40, 40)
            y += rnd.uniform(10, 40)
            pts.append((x, y))
        d.line(pts, fill=(15, 9, 6, 110), width=4, joint="curve")
    for _ in range(12):
        x, y, r = rnd.uniform(30, 1050), rnd.uniform(1420, 1880), rnd.uniform(18, 46)
        d.ellipse([x - r, y - r * 0.8, x + r, y + r * 0.8], fill=(92, 82, 76, 255), outline=(20, 13, 9, 255), width=5)
    over(img, lay)
    return vignette(grain(img, 9, 4), 0.85)


def dyn_isaac(img, d, now, prog, end, S):
    for (a, b, c, e) in particles(13, 9):
        x = 40 + a * 1000
        y = ((b + now * (0.10 + c * 0.12)) % 1.0) * (H + 200) - 100
        r = 9 + e * 9
        d.polygon([(x, y - r * 2.3), (x - r * 0.85, y - r * 0.4), (x + r * 0.85, y - r * 0.4)], fill=(124, 200, 255))
        d.ellipse([x - r, y - r, x + r, y + r], fill=(124, 200, 255), outline=(30, 60, 110), width=3)
    paste(img, text_img(f"ROOM {1 + int(now / 3.2)}", "PermanentMarker-Regular.ttf", 40, "#f3e6c8", 5, "#140d09"), 940, 198)


def panel_isaac(w, h, kind="main"):
    return _panel(w, h, (243, 230, 200, 255), (20, 13, 9, 255), 7, 22, (10, 12, (0, 0, 0, 120)))[0]


# ================================================================ MINECRAFT: blocky sky, grass and dirt
def static_mine():
    img = vgrad("#6fb0ff", "#cfe8ff")
    lay, d = layer()
    rnd = random.Random(64)
    for (x, y, sc) in ((60, 330, 1.0), (700, 300, 1.2), (380, 1120, 0.8)):
        for (dx, dy, w, h) in ((0, 0, 260, 60), (60, -60, 140, 60)):
            d.rectangle([x + dx * sc, y + dy * sc, x + (dx + w) * sc, y + (dy + h) * sc], fill=(255, 255, 255, 215))
    B = 90
    for gy in range(1440, H + B, B):
        row = (gy - 1440) // B
        base = (106, 170, 64) if row == 0 else ((134, 96, 67) if row < 4 else (128, 128, 128))
        for gx in range(0, W, B):
            k = rnd.uniform(0.9, 1.08)
            d.rectangle([gx, gy, gx + B, gy + B], fill=tuple(int(min(255, c * k)) for c in base) + (255,))
            for _ in range(7):
                px, py = gx + rnd.randrange(0, 76, 15), gy + rnd.randrange(0, 76, 15)
                kk = rnd.uniform(0.74, 1.18)
                d.rectangle([px, py, px + 14, py + 14], fill=tuple(int(min(255, c * kk)) for c in base) + (255,))
    over(img, lay)
    return img


def dyn_mine(img, d, now, prog, end, S):
    x = int((now * 30) % (W + 420)) - 320
    d.rectangle([x, 600, x + 240, 656], fill=(255, 255, 255))
    d.rectangle([x + 56, 544, x + 176, 600], fill=(255, 255, 255))
    paste(img, text_img(f"BLOCKS: {int(now * 41):,}", "PressStart2P-Regular.ttf", 24, "#ffffff", 5, "#1d2b12"), 900, 198)


def panel_mine(w, h, kind="main"):
    im, d = _panel(w, h, (198, 198, 198, 255), (38, 38, 38, 255), 6, 0, (10, 10, (0, 0, 0, 110)))
    d.line([(PM + 8, PM + h - 9), (PM + 8, PM + 8), (PM + w - 9, PM + 8)], fill=(255, 255, 255, 255), width=5)
    d.line([(PM + 8, PM + h - 9), (PM + w - 9, PM + h - 9), (PM + w - 9, PM + 8)], fill=(120, 120, 120, 255), width=5)
    return im


# ================================================================ POKEMON: handheld dot-matrix screen
def static_poke():
    img = Image.new("RGB", (W, H), rgb("#9bbc0f"))
    lay, d = layer()
    for y in range(0, H, 8):
        d.line([(0, y), (W, y)], fill=(48, 98, 48, 34), width=1)
    for x in range(0, W, 8):
        d.line([(x, 0), (x, H)], fill=(48, 98, 48, 34), width=1)
    rnd = random.Random(151)
    for gy in range(1452, H, 64):
        for gx in range(0, W, 64):
            if rnd.random() < 0.82:
                for k in range(3):
                    d.rectangle([gx + 8 + k * 18, gy + 24 - (k % 2) * 12, gx + 20 + k * 18, gy + 56], fill=(48, 98, 48, 255))
    d.rectangle([0, 1430, W, 1442], fill=(15, 56, 15, 255))
    over(img, lay)
    return img


def dyn_poke(img, d, now, prog, end, S):
    n = min(151, 1 + int(prog * 151))
    paste(img, text_img(f"SEEN {n}/151", "PressStart2P-Regular.ttf", 26, "#0f380f"), 900, 198)
    if int(now * 2) % 2 == 0:
        d.polygon([(1010, 1250), (1040, 1250), (1025, 1272)], fill=(15, 56, 15))


def panel_poke(w, h, kind="main"):
    im, d = _panel(w, h, (224, 248, 208, 255), (15, 56, 15, 255), 8, 18)
    if kind == "main":
        d.rounded_rectangle([PM + 16, PM + 16, PM + w - 16, PM + h - 16], 10, outline=(48, 98, 48, 255), width=4)
    return im


# ================================================================ GEOMETRY DASH: neon squares, a ground line and spikes
def static_gdash():
    img = vgrad("#0a58ff", "#5a1fd1")
    lay, d = layer()
    rnd = random.Random(22)
    for _ in range(28):
        sz = rnd.choice([120, 180, 240])
        x, y = rnd.randrange(-60, W, 60), rnd.randrange(240, 1500, 60)
        d.rectangle([x, y, x + sz, y + sz], outline=(255, 255, 255, 24), width=6)
    d.rectangle([0, 1640, W, H], fill=(8, 30, 130, 255))
    for x in range(0, W, 180):
        d.rectangle([x + 10, 1662, x + 170, 1822], outline=(255, 255, 255, 40), width=5)
    d.line([(0, 1640), (W, 1640)], fill=(255, 255, 255, 255), width=6)
    over(img, lay)
    return img


def dyn_gdash(img, d, now, prog, end, S):
    off = (now * 520) % 360
    for k in range(5):
        x = W + 100 - off - k * 360
        if k % 2 == 0:
            d.polygon([(x, 1637), (x + 45, 1552), (x + 90, 1637)], fill=(10, 10, 24), outline=(255, 255, 255))
        else:
            d.rectangle([x, 1550, x + 90, 1637], fill=(10, 10, 24), outline=(255, 255, 255), width=5)
    ph = ((off - 260 + 180) % 360) / 360
    y = 1637 - 45 - 4 * ph * (1 - ph) * 150
    d.rectangle([155, y - 45, 245, y + 45], fill=(125, 255, 60), outline=(10, 10, 24), width=7)
    d.polygon([(200, y - 22), (222, y), (200, y + 22), (178, y)], fill=(255, 255, 255), outline=(10, 10, 24))
    paste(img, text_img(f"ATTEMPT {1 + int(now / 2.4)}", "RussoOne-Regular.ttf", 38, "#ffffff", 5, "#06103a"), 900, 198)


def panel_gdash(w, h, kind="main"):
    im, d = _panel(w, h, (8, 20, 70, 238), (255, 255, 255, 255), 6, 18, (10, 12, (0, 0, 0, 110)))
    if kind == "main":
        d.rounded_rectangle([PM + 14, PM + 14, PM + w - 14, PM + h - 14], 10, outline=(125, 255, 60, 255), width=3)
    return im


# ================================================================ AMONG US: drifting stars and a task bar
def static_among():
    return vignette(vgrad("#070b1a", "#151c3a"), 0.5)


def dyn_among(img, d, now, prog, end, S):
    for (a, b, c, e) in particles(80, 5):
        x = ((a - now * (0.01 + c * 0.05)) % 1.0) * W
        y, r = b * H, 1.5 + e * 3
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255) if e > 0.3 else (160, 190, 255))
    d.rounded_rectangle([700, 180, 1044, 216], 8, fill=(20, 26, 50), outline=(255, 255, 255), width=4)
    d.rounded_rectangle([706, 186, 706 + int(332 * prog), 210], 5, fill=(74, 222, 96))
    paste(img, text_img("TASKS", "TitanOne-Regular.ttf", 30, "#ffffff", 4, "#000000"), 640, 198)


def panel_among(w, h, kind="main"):
    if kind == "tag":
        return _panel(w, h, (197, 17, 17, 255), (255, 255, 255, 255), 5, 20)[0]
    return _panel(w, h, (24, 30, 58, 240), (255, 255, 255, 255), 6, 28, (10, 12, (0, 0, 0, 120)))[0]


def roles(big, small, ink, acc, dim, ptext, pacc, pdim, stroke=0.0, sfill="#000000", shadow=None, wb=None, ws=None, box=None, accbox=None):
    return {
        "big": (big, wb, ink, stroke, sfill, shadow, box), "acc": (big, wb, acc, stroke, sfill, shadow, accbox),
        "small": (small, ws, dim, stroke * 0.8, sfill, None, None), "pbig": (big, wb, ptext, 0, sfill, None, None),
        "pacc": (big, wb, pacc, 0, sfill, None, None), "psmall": (small, ws, pdim, 0, sfill, None, None),
        "credit": (small, ws, dim, stroke * 0.8, sfill, None, None),
    }


THEMES = {
    "cs2": dict(case="upper", static=static_cs2, dyn=dyn_cs2, panel=panel_cs2, flash="#f5a623", frame=("#f5a623", 6),
                text=roles("Rajdhani-Bold.ttf", "Rajdhani-Bold.ttf", "#ffffff", "#f5a623", "#9fb0c3", "#ffffff", "#f5a623", "#8fa3b8", shadow=(0.035, 0.035, "#7a4d06")),
                cap=dict(font="Rajdhani-Bold.ttf", size=104, fill="#ffffff", hi="#f5a623", stroke="#05080b")),
    "dw9": dict(case="upper", static=static_dw9, dyn=dyn_dw9, panel=panel_dw9, flash="#b3261e", frame=("#9c1c18", 10),
                text=roles("Cinzel[wght].ttf", "Cinzel[wght].ttf", "#1c1410", "#b3261e", "#5a4630", "#fff3d6", "#ffd36b", "#f0cfa0", wb=900, ws=700),
                cap=dict(font="Cinzel[wght].ttf", wght=900, size=78, fill="#fff6e0", hi="#ffd36b", stroke="#2a0a06")),
    "dota": dict(case="upper", static=static_dota, dyn=dyn_dota, panel=panel_dota, flash="#e8b54a", frame=("#c8a050", 6),
                 text=roles("Metamorphous-Regular.ttf", "CrimsonText-Bold.ttf", "#f4e3b5", "#e8b54a", "#c79a55", "#f4e3b5", "#e8b54a", "#b0905c", stroke=0.035),
                 cap=dict(font="CrimsonText-Bold.ttf", size=98, fill="#fff3d6", hi="#ff6a4a", stroke="#0a0304")),
    "pubg": dict(case="upper", static=static_pubg, base=base_pubg, dyn=dyn_pubg, panel=panel_pubg, flash="#f2a900", frame=("#f2a900", 8),
                 text=roles("BlackOpsOne-Regular.ttf", "BarlowCondensed-ExtraBold.ttf", "#ffffff", "#f2a900", "#ffffff", "#ffffff", "#f2a900", "#cfcdb6", stroke=0.06, sfill="#11140c"),
                 cap=dict(font="BarlowCondensed-ExtraBold.ttf", size=112, fill="#ffffff", hi="#f2a900", stroke="#0d100a")),
    "wardogs": dict(case="upper", static=static_wardogs, dyn=dyn_wardogs, panel=panel_wardogs, flash="#7ed957", frame=("#7ed957", 6),
                    text=roles("Anton-Regular.ttf", "BarlowCondensed-ExtraBold.ttf", "#f2f2ee", "#7ed957", "#b9beb4", "#f2f2ee", "#7ed957", "#aab0a4", stroke=0.03, sfill="#0c0d0c"),
                    cap=dict(font="Anton-Regular.ttf", size=92, fill="#ffffff", hi="#7ed957", stroke="#070807")),
    "oni": dict(case="title", static=static_oni, dyn=dyn_oni, panel=panel_oni, flash="#b5222a", frame=("#141210", 10),
                text=roles("KaushanScript-Regular.ttf", "CrimsonText-Bold.ttf", "#14110f", "#b5222a", "#4a4038", "#f2ead8", "#ee5a55", "#cfc4ae"),
                cap=dict(font="CrimsonText-Bold.ttf", size=98, fill="#ffffff", hi="#ff5a54", stroke="#120c0a")),
    "dawn": dict(case="title", static=static_dawn, base=base_dawn, dyn=dyn_dawn, panel=panel_dawn, flash="#c81e2e", frame=("#d9a441", 6),
                 text=roles("PirataOne-Regular.ttf", "PirataOne-Regular.ttf", "#fff4dc", "#ffcf5a", "#fff4dc", "#fff4dc", "#f0b24a", "#d8b9a0", stroke=0.05, sfill="#1a0508"),
                 cap=dict(font="PirataOne-Regular.ttf", size=112, fill="#fff4dc", hi="#ff5a5a", stroke="#150406")),
    "control": dict(case="upper", static=static_control, dyn=dyn_control, panel=panel_control, flash="#e4002b", frame=("#000000", 12),
                    text=roles("ArchivoBlack-Regular.ttf", "ArchivoBlack-Regular.ttf", "#ffffff", "#ffffff", "#141414", "#ffffff", "#ff2d4f", "#c4c4c4", box="#000000", accbox="#e4002b"),
                    cap=dict(font="ArchivoBlack-Regular.ttf", size=78, fill="#ffffff", hi="#ff2d4f", stroke="#000000", box="#000000")),
    "wolv": dict(case="upper", tag_role="small", static=static_wolv, dyn=dyn_wolv, panel=panel_wolv, flash="#ffffff", frame=("#0c0c0c", 12),
                 text=roles("Bangers-Regular.ttf", "Bangers-Regular.ttf", "#ffffff", "#e10600", "#111111", "#111111", "#e10600", "#333333", stroke=0.07, sfill="#0c0c0c", shadow=(0.05, 0.05, "#1f4fd8")),
                 cap=dict(font="Bangers-Regular.ttf", size=108, fill="#ffffff", hi="#ffe100", stroke="#0c0c0c")),
    "witcher": dict(case="title", static=static_witcher, dyn=dyn_witcher, panel=panel_witcher, flash="#f1e6c6", frame=("#5a3c1c", 10),
                    text=roles("Almendra-Bold.ttf", "Almendra-Bold.ttf", "#2b1d12", "#8b1a1a", "#5b4630", "#2b1d12", "#8b1a1a", "#6b563c"),
                    cap=dict(font="Almendra-Bold.ttf", size=98, fill="#fff6e0", hi="#ffc94a", stroke="#24160a")),
}
THEMES.update({
    "aion": dict(case="upper", static=static_aion, dyn=dyn_aion, panel=panel_aion, flash="#f2c86b", frame=("#f2c86b", 6),
                 text=roles("Marcellus-Regular.ttf", "CrimsonText-Bold.ttf", "#fdf6e3", "#f2c86b", "#d9d2f2", "#fdf6e3", "#f2c86b", "#b9b3d9", stroke=0.03, sfill="#120a2a"),
                 cap=dict(font="Marcellus-Regular.ttf", size=96, fill="#ffffff", hi="#f2c86b", stroke="#120a2a")),
    "deadlock": dict(case="upper", static=static_deadlock, dyn=dyn_deadlock, panel=panel_deadlock, flash="#e9a13b", frame=("#e9a13b", 6),
                     text=roles("Limelight-Regular.ttf", "BarlowCondensed-ExtraBold.ttf", "#f3e9d2", "#e9a13b", "#b9d6cc", "#f3e9d2", "#e9a13b", "#8fb3a8", stroke=0.035, sfill="#020807"),
                     cap=dict(font="BarlowCondensed-ExtraBold.ttf", size=110, fill="#f3e9d2", hi="#5ff0c8", stroke="#06100f")),
    "ace": dict(case="upper", static=static_ace, base=base_ace, dyn=dyn_ace, panel=panel_ace, flash="#ffffff", frame=("#7cff6b", 5),
                text=roles("Oxanium[wght].ttf", "Oxanium[wght].ttf", "#ffffff", "#7cff6b", "#ffffff", "#ffffff", "#7cff6b", "#a9c8e8", stroke=0.05, sfill="#06203f", wb=800, ws=700),
                cap=dict(font="Oxanium[wght].ttf", wght=800, size=92, fill="#ffffff", hi="#7cff6b", stroke="#041326")),
    "dress": dict(case="title", static=static_dress, dyn=dyn_dress, panel=panel_dress, flash="#ffd1e0", frame=("#d6457a", 8),
                  text=roles("DMSerifDisplay-Regular.ttf", "Nunito[wght].ttf", "#3a2a35", "#d6457a", "#6a5460", "#3a2a35", "#d6457a", "#7a6470", ws=800),
                  cap=dict(font="Nunito[wght].ttf", wght=900, size=92, fill="#ffffff", hi="#ffd166", stroke="#3a2a35")),
    "bongo": dict(case="title", static=static_bongo, dyn=dyn_bongo, panel=panel_bongo, flash="#ffffff", frame=("#1b1b1f", 10),
                  text=roles("Baloo2[wght].ttf", "Baloo2[wght].ttf", "#1b1b1f", "#ff5d8f", "#4a4a55", "#1b1b1f", "#ff5d8f", "#55555f", wb=800, ws=700),
                  cap=dict(font="Baloo2[wght].ttf", wght=800, size=100, fill="#ffffff", hi="#ffd23f", stroke="#1b1b1f")),
    "gears": dict(case="upper", static=static_gears, dyn=dyn_gears, panel=panel_gears, flash="#d1161c", frame=("#d1161c", 8),
                  text=roles("SairaStencilOne-Regular.ttf", "BarlowCondensed-ExtraBold.ttf", "#e9e4dc", "#e5282d", "#c4bdb1", "#efeae2", "#ff3b30", "#a8a196", stroke=0.035, sfill="#050505"),
                  cap=dict(font="BarlowCondensed-ExtraBold.ttf", size=112, fill="#ffffff", hi="#ff3b30", stroke="#0a0a0a")),
    "swr": dict(case="upper", static=static_swr, dyn=dyn_swr, panel=panel_swr, flash="#ffb347", frame=("#29f0ff", 6),
                text=roles("Audiowide-Regular.ttf", "Rajdhani-Bold.ttf", "#ffffff", "#29f0ff", "#ffe2c8", "#ffffff", "#29f0ff", "#c9b8e8", stroke=0.05, sfill="#170a3c"),
                cap=dict(font="Rajdhani-Bold.ttf", size=108, fill="#ffffff", hi="#ffb347", stroke="#150828")),
    "mw4": dict(case="upper", static=static_mw4, dyn=dyn_mw4, panel=panel_mw4, flash="#6dff8f", frame=("#6dff8f", 5),
                text=roles("Teko[wght].ttf", "BarlowCondensed-ExtraBold.ttf", "#eafff0", "#6dff8f", "#9fdfaf", "#eafff0", "#6dff8f", "#7fbf8f", stroke=0.03, sfill="#020803", wb=700),
                cap=dict(font="Teko[wght].ttf", wght=700, size=128, fill="#ffffff", hi="#6dff8f", stroke="#020803")),
    "pbz": dict(case="upper", static=static_pbz, dyn=dyn_pbz, panel=panel_pbz, flash="#e02a2a", frame=("#e02a2a", 6),
                text=roles("Eczar[wght].ttf", "CrimsonText-Bold.ttf", "#f0ece4", "#ff3b33", "#aebfc8", "#f0ece4", "#ff4a3d", "#93a7b1", stroke=0.04, sfill="#000000", wb=800),
                cap=dict(font="Eczar[wght].ttf", wght=800, size=96, fill="#ffffff", hi="#ff4a3d", stroke="#050607")),
    "dandy": dict(case="upper", tag_role="small", static=static_dandy, dyn=dyn_dandy, panel=panel_dandy, flash="#ffffff", frame=("#1d1a26", 10),
                  text=roles("Chewy-Regular.ttf", "Nunito[wght].ttf", "#1d1a26", "#e8336d", "#2b2640", "#1d1a26", "#7a3cf0", "#4a4460", ws=900),
                  cap=dict(font="Chewy-Regular.ttf", size=104, fill="#ffffff", hi="#ffe14d", stroke="#1d1a26")),
})
# small-text and credit roles never get a stroke on themes whose backgrounds are light
for _n in ("dw9", "oni", "witcher", "wolv", "dress", "bongo", "dandy"):
    for _r in ("small", "credit"):
        t = THEMES[_n]["text"][_r]
        THEMES[_n]["text"][_r] = (t[0], t[1], t[2], 0, t[4], None, None)
# ================================================================ FIVE NIGHTS AT FREDDY'S: security camera feed
def static_fnaf():
    img = radial("#27302b", "#050706", CX, 900, 1250)
    lay, d = layer()
    for y in range(0, H, 6):
        d.line([(0, y), (W, y)], fill=(0, 0, 0, 70), width=2)
    for k, x in enumerate(range(0, W, 60)):
        for j in range(2):
            if (k + j) % 2 == 0:
                d.rectangle([x, 1790 + j * 60, x + 60, 1850 + j * 60], fill=(235, 235, 225, 60))
            else:
                d.rectangle([x, 1790 + j * 60, x + 60, 1850 + j * 60], fill=(0, 0, 0, 120))
    d.rectangle([18, 254, W - 18, H - 18], outline=(220, 230, 220, 70), width=4)
    over(img, lay)
    return vignette(grain(img, 16, 5), 0.9)


def dyn_fnaf(img, d, now, prog, end, S):
    rnd = random.Random(int(now * 14))
    for _ in range(7):
        y = rnd.randrange(260, H - 30)
        x = rnd.randrange(0, W - 300)
        d.line([(x, y), (x + rnd.randrange(120, 520), y)], fill=(150, 160, 152), width=rnd.choice([1, 2, 3]))
    band = int((now * 240) % (H + 300)) - 150
    for k in range(0, 46, 6):
        d.line([(0, band + k), (W, band + k)], fill=(60, 68, 63), width=2)
    if int(now * 1.6) % 2 == 0:
        d.ellipse([706, 182, 738, 214], fill=(255, 40, 40))
    hr = [12, 1, 2, 3, 4, 5, 6][min(6, int(prog * 6.999))]
    paste(img, text_img(f"{hr} AM", "ChakraPetch-Bold.ttf", 46, "#ffffff", 5, "#000000"), 900, 198)


def panel_fnaf(w, h, kind="main"):
    im, d = _panel(w, h, (12, 15, 13, 240), (214, 224, 214, 255), 5, 6, (10, 12, (0, 0, 0, 150)))
    if kind == "main":
        d.rectangle([PM + 12, PM + 12, PM + 44, PM + 16], fill=(255, 210, 63, 255))
        d.rectangle([PM + 12, PM + 12, PM + 16, PM + 44], fill=(255, 210, 63, 255))
        d.rectangle([PM + w - 44, PM + h - 16, PM + w - 12, PM + h - 12], fill=(255, 210, 63, 255))
        d.rectangle([PM + w - 16, PM + h - 44, PM + w - 12, PM + h - 12], fill=(255, 210, 63, 255))
    return im


# ================================================================ UNDERTALE: black void, battle box and a red soul
def _heart(d, x, y, r, fill):
    d.ellipse([x - r, y - r * 0.6, x, y + r * 0.4], fill=fill)
    d.ellipse([x, y - r * 0.6, x + r, y + r * 0.4], fill=fill)
    d.polygon([(x - r * 0.97, y), (x + r * 0.97, y), (x, y + r * 1.1)], fill=fill)


def static_ut():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    lay, d = layer()
    rnd = random.Random(7)
    for _ in range(70):
        x, y = rnd.uniform(0, W), rnd.uniform(240, H)
        d.rectangle([x, y, x + 4, y + 4], fill=(255, 255, 255, rnd.randint(40, 140)))
    d.rectangle([90, 1660, W - 90, 1870], outline=(255, 255, 255, 255), width=8)
    over(img, lay)
    return img


def dyn_ut(img, d, now, prog, end, S):
    x = 540 + 330 * math.sin(now * 1.3)
    y = 1765 + 50 * math.sin(now * 2.1)
    _heart(d, x, y, 26, (255, 0, 0))
    if int(now * 2) % 2 == 0:
        cx, cy = 980, 300
        d.polygon([(cx, cy - 26), (cx + 8, cy - 8), (cx + 26, cy), (cx + 8, cy + 8), (cx, cy + 26), (cx - 8, cy + 8), (cx - 26, cy), (cx - 8, cy - 8)], fill=(255, 255, 0))
    paste(img, text_img(f"LV {1 + int(prog * 19)}", "PressStart2P-Regular.ttf", 28, "#ffffff"), 910, 198)


def panel_ut(w, h, kind="main"):
    im, d = _panel(w, h, (0, 0, 0, 245), (255, 255, 255, 255), 7, 0)
    return im


# ================================================================ SUBWAY SURFERS: sunny tracks, graffiti wall and coins
def static_subway():
    img = vgrad("#4fc3ff", "#bfeaff")
    lay, d = layer()
    rnd = random.Random(12)
    cols = [(255, 92, 92, 120), (255, 196, 0, 120), (92, 220, 120, 120), (186, 104, 255, 120)]
    d.rectangle([0, 1180, W, 1560], fill=(196, 170, 150, 255))
    for k in range(16):
        x, y = rnd.uniform(-60, W), rnd.uniform(1200, 1500)
        d.ellipse([x, y, x + rnd.uniform(120, 260), y + rnd.uniform(50, 110)], fill=cols[k % 4])
    d.rectangle([0, 1560, W, H], fill=(120, 110, 104, 255))
    for x in (240, 540, 840):
        d.line([(x - 70, 1560), (x - 140, H)], fill=(220, 220, 225, 255), width=10)
        d.line([(x + 70, 1560), (x + 140, H)], fill=(220, 220, 225, 255), width=10)
    for y in range(1590, H, 60):
        d.rectangle([0, y, W, y + 14], fill=(90, 70, 60, 200))
    over(img, lay)
    return img


def dyn_subway(img, d, now, prog, end, S):
    for (a, b, c, e) in particles(9, 31):
        x = 120 + a * 840
        y = 1560 + ((b + now * (0.25 + c * 0.2)) % 1.0) * 360
        r = 16 + e * 8
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 205, 40), outline=(190, 120, 0), width=4)
    paste(img, text_img(f"COINS {int(prog * 999):03d}", "Bangers-Regular.ttf", 46, "#ffd23f", 5, "#1a1a2e"), 900, 198)


def panel_subway(w, h, kind="main"):
    im, d = _panel(w, h, (255, 255, 255, 245), (26, 26, 46, 255), 7, 26, (10, 12, (0, 0, 0, 90)))
    if kind == "main":
        d.rounded_rectangle([PM + 16, PM + h - 22, PM + w - 16, PM + h - 12], 4, fill=(255, 140, 0, 255))
    return im


# ================================================================ SILKSONG: misty grey-blue kingdom with drifting silk
def static_hk():
    img = radial("#3a4660", "#0b0f1a", CX, 700, 1300)
    lay, d = layer()
    rnd = random.Random(9)
    for k in range(9):
        x = rnd.uniform(0, W)
        d.line([(x, 0), (x + rnd.uniform(-80, 80), H)], fill=(220, 225, 240, 22), width=3)
    for x0 in range(-100, W, 140):
        h = rnd.uniform(160, 420)
        d.polygon([(x0, H), (x0 + 70, H - h), (x0 + 140, H)], fill=(8, 10, 18, 230))
    over(img, lay)
    return vignette(grain(img, 6, 2), 0.8)


def dyn_hk(img, d, now, prog, end, S):
    for (a, b, c, e) in particles(26, 41):
        x = (a * W + math.sin(now * 0.7 + b * 6) * 40) % W
        y = ((b - now * (0.02 + c * 0.03)) % 1.0) * H
        r = 2 + e * 4
        d.ellipse([x - r, y - r, x + r, y + r], fill=(235, 240, 255))
    paste(img, text_img(f"ROSARIES {int(prog * 999):03d}", "Cinzel[wght].ttf", 34, "#f1ece0", 4, "#0b0f1a", 800), 880, 198)


def panel_hk(w, h, kind="main"):
    im, d = _panel(w, h, (12, 16, 28, 238), (232, 228, 214, 255), 4, 10, (10, 12, (0, 0, 0, 140)))
    if kind == "main":
        d.line([(PM + 30, PM + 14), (PM + w - 30, PM + 14)], fill=(196, 40, 52, 255), width=4)
    return im


# ================================================================ TERRARIA: sky, grass, dirt and ore layers
def static_terra():
    img = vgrad("#5fa8ff", "#c9e6ff")
    lay, d = layer()
    rnd = random.Random(5)
    B = 36
    top = 1500
    for x in range(0, W, B):
        g = top + int(math.sin(x / 140) * 30) // B * B
        d.rectangle([x, g, x + B, g + B], fill=(76, 175, 80, 255))
        for y in range(g + B, H, B):
            c = (121, 85, 61, 255) if y < g + 6 * B else (90, 90, 96, 255)
            if rnd.random() < 0.06:
                c = rnd.choice([(255, 196, 0, 255), (64, 196, 255, 255), (180, 90, 255, 255)])
            d.rectangle([x, y, x + B - 2, y + B - 2], fill=c)
    over(img, lay)
    return img


def dyn_terra(img, d, now, prog, end, S):
    sx = 120 + prog * 840
    d.ellipse([sx - 50, 360 - 50, sx + 50, 360 + 50], fill=(255, 236, 120))
    for (a, b, c, e) in particles(5, 3):
        x = ((a + now * (0.02 + c * 0.02)) % 1.2) * W - 100
        y = 300 + b * 300
        d.ellipse([x, y, x + 160, y + 50], fill=(255, 255, 255))
        d.ellipse([x + 40, y - 30, x + 120, y + 40], fill=(255, 255, 255))
    paste(img, text_img(f"DEPTH {int(prog * 300)} FT", "ArchivoBlack-Regular.ttf", 34, "#ffffff", 5, "#1b2a10"), 880, 198)


def panel_terra(w, h, kind="main"):
    im, d = _panel(w, h, (34, 46, 92, 235), (14, 18, 40, 255), 6, 8, (10, 12, (0, 0, 0, 110)))
    if kind == "main":
        d.rectangle([PM + 8, PM + 8, PM + w - 8, PM + h - 8], outline=(110, 140, 220, 255), width=3)
    return im


# ================================================================ CUPHEAD: 1930s cartoon film, sepia, grain and flicker
def static_cup():
    img = radial("#f3dfb0", "#9c7a4a", CX, 900, 1200)
    lay, d = layer()
    for k in range(18):
        a = k / 18 * math.tau
        d.polygon([(CX, 900), (CX + math.cos(a) * 1600, 900 + math.sin(a) * 1600), (CX + math.cos(a + 0.17) * 1600, 900 + math.sin(a + 0.17) * 1600)], fill=(255, 240, 200, 40))
    over(img, lay)
    return vignette(grain(img, 14, 5), 1.0)


def dyn_cup(img, d, now, prog, end, S):
    rnd = random.Random(int(now * 12))
    for _ in range(3):
        x = rnd.randrange(0, W)
        d.line([(x, 0), (x + rnd.randrange(-6, 6), H)], fill=(70, 50, 30), width=rnd.choice([1, 2]))
    for _ in range(4):
        x, y, r = rnd.randrange(0, W), rnd.randrange(0, H), rnd.randrange(2, 6)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(40, 28, 16))
    paste(img, text_img(f"REEL {1 + int(prog * 9)}", "Limelight-Regular.ttf", 40, "#2a1a0c", 0, "#000000"), 900, 198)


def panel_cup(w, h, kind="main"):
    im, d = _panel(w, h, (250, 238, 210, 245), (42, 26, 12, 255), 7, 26, (10, 12, (60, 36, 10, 120)))
    if kind == "main":
        d.rounded_rectangle([PM + 14, PM + 14, PM + w - 14, PM + h - 14], 18, outline=(190, 40, 30, 255), width=3)
    return im


# ================================================================ STARDEW VALLEY: warm farm, fences and crops
def static_stardew():
    img = vgrad("#8fd3ff", "#ffe8b0")
    lay, d = layer()
    d.ellipse([-300, 1380, 700, 1800], fill=(120, 190, 80, 255))
    d.ellipse([400, 1360, 1500, 1820], fill=(104, 176, 70, 255))
    d.rectangle([0, 1600, W, H], fill=(150, 108, 64, 255))
    for y in range(1640, H, 70):
        for x in range(40, W, 90):
            d.rectangle([x, y, x + 50, y + 40], fill=(120, 84, 48, 255))
            d.polygon([(x + 25, y - 30), (x + 10, y + 5), (x + 40, y + 5)], fill=(92, 184, 74, 255))
    for x in range(0, W, 120):
        d.rectangle([x + 50, 1520, x + 66, 1610], fill=(196, 150, 96, 255))
    d.rectangle([0, 1540, W, 1556], fill=(196, 150, 96, 255))
    over(img, lay)
    return img


def dyn_stardew(img, d, now, prog, end, S):
    for (a, b, c, e) in particles(10, 17):
        x = ((a + now * (0.03 + c * 0.03)) % 1.1) * W - 50
        y = 300 + b * 1000 + math.sin(now * 3 + a * 9) * 20
        d.ellipse([x - 8, y - 5, x + 8, y + 5], fill=(255, 214, 120))
    day = ["SPRING", "SUMMER", "FALL", "WINTER"][min(3, int(prog * 3.999))]
    paste(img, text_img(f"{day} {1 + int(prog * 27) % 28}", "Chewy-Regular.ttf", 44, "#ffffff", 5, "#5a3a1a"), 880, 198)


def panel_stardew(w, h, kind="main"):
    im, d = _panel(w, h, (255, 226, 160, 248), (110, 60, 24, 255), 8, 14, (10, 12, (60, 30, 10, 110)))
    if kind == "main":
        d.rounded_rectangle([PM + 12, PM + 12, PM + w - 12, PM + h - 12], 10, outline=(200, 130, 60, 255), width=4)
    return im


# ================================================================ POPPY PLAYTIME: dark toy factory, conveyor and grabpack colors
def static_poppy():
    img = radial("#1d2a3c", "#05070c", CX, 900, 1250)
    lay, d = layer()
    for x in range(0, W, 180):
        d.rectangle([x + 20, 240, x + 40, H], fill=(30, 40, 56, 200))
    d.rectangle([0, 1640, W, 1700], fill=(40, 46, 60, 255))
    for x in range(0, W, 60):
        d.line([(x, 1640), (x + 30, 1700)], fill=(255, 196, 0, 120), width=8)
    over(img, lay)
    return vignette(grain(img, 10, 4), 0.95)


def dyn_poppy(img, d, now, prog, end, S):
    off = (now * 160) % 220
    for k in range(7):
        x = -120 + off + k * 220
        col = [(40, 120, 255), (230, 40, 50), (255, 196, 0)][k % 3]
        d.rounded_rectangle([x, 1560, x + 90, 1640], 14, fill=col, outline=(10, 10, 14), width=5)
    if int(now * 1.3) % 3:
        d.ellipse([90, 300, 110, 320], fill=(255, 60, 60))
    paste(img, text_img(f"TOYS {int(prog * 100)}%", "SairaStencilOne-Regular.ttf", 38, "#ffffff", 4, "#05070c"), 900, 198)


def panel_poppy(w, h, kind="main"):
    im, d = _panel(w, h, (14, 20, 32, 240), (60, 130, 255, 255), 6, 16, (10, 12, (0, 0, 0, 140)))
    if kind == "main":
        d.rounded_rectangle([PM + 10, PM + h - 20, PM + w - 10, PM + h - 10], 4, fill=(230, 40, 50, 255))
    return im


# control: floating black blocks drift behind the content, so small text sits on its own black plate
_t = THEMES["control"]["text"]["small"]
THEMES["control"]["text"]["small"] = (_t[0], _t[1], "#ffffff", 0, _t[4], None, "#000000")

THEMES.update({
    "isaac": dict(case="upper", static=static_isaac, dyn=dyn_isaac, panel=panel_isaac, flash="#7cc8ff", frame=("#f3e6c8", 8),
                  text=roles("PermanentMarker-Regular.ttf", "PatrickHand-Regular.ttf", "#f6ecd2", "#7cc8ff", "#ead9b6", "#1c130d", "#c22a2f", "#4e3c31", stroke=0.06, sfill="#140d09"),
                  cap=dict(font="PermanentMarker-Regular.ttf", size=92, fill="#ffffff", hi="#7cc8ff", stroke="#140d09")),
    "mine": dict(case="upper", static=static_mine, dyn=dyn_mine, panel=panel_mine, flash="#ffffff", tag_col="#7dff5c", frame=("#3b3b3b", 8),
                 text=roles("PressStart2P-Regular.ttf", "BarlowCondensed-ExtraBold.ttf", "#ffffff", "#ffe14d", "#ffffff", "#2a2a2a", "#2f7d1f", "#4a4a4a", stroke=0.09, sfill="#1d2b12"),
                 cap=dict(font="PressStart2P-Regular.ttf", size=60, gap=0.6, fill="#ffffff", hi="#ffe14d", stroke="#1d2b12")),
    "poke": dict(case="upper", static=static_poke, dyn=dyn_poke, panel=panel_poke, flash="#e0f8d0", tag_col="#9bbc0f", frame=("#0f380f", 10),
                 text=roles("PressStart2P-Regular.ttf", "PressStart2P-Regular.ttf", "#0f380f", "#d7ee8a", "#0f380f", "#0f380f", "#306230", "#306230", accbox="#0f380f"),
                 cap=dict(font="PressStart2P-Regular.ttf", size=62, gap=0.6, fill="#9bbc0f", hi="#ffffff", stroke="#0f380f", box="#0f380f")),
    "gdash": dict(case="upper", static=static_gdash, dyn=dyn_gdash, panel=panel_gdash, flash="#7dff3c", frame=("#ffffff", 8),
                  text=roles("RussoOne-Regular.ttf", "Rajdhani-Bold.ttf", "#ffffff", "#7dff3c", "#dfe8ff", "#ffffff", "#ffe14d", "#b9c8ff", stroke=0.06, sfill="#06103a"),
                  cap=dict(font="RussoOne-Regular.ttf", size=92, fill="#ffffff", hi="#7dff3c", stroke="#06103a")),
    "among": dict(case="upper", static=static_among, dyn=dyn_among, panel=panel_among, flash="#ff4d4d", frame=("#ffffff", 8),
                  text=roles("TitanOne-Regular.ttf", "Nunito[wght].ttf", "#ffffff", "#ff4d4d", "#c9d4ff", "#ffffff", "#ffe14d", "#aab6e8", stroke=0.07, sfill="#000000", ws=900),
                  cap=dict(font="TitanOne-Regular.ttf", size=94, fill="#ffffff", hi="#ff4d4d", stroke="#000000")),
})

THEMES.update({
    "fnaf": dict(case="upper", static=static_fnaf, dyn=dyn_fnaf, panel=panel_fnaf, flash="#ff4040", tag_col="#ffd23f", frame=("#d6e0d6", 6),
                 text=roles("Anton-Regular.ttf", "ChakraPetch-Bold.ttf", "#f4f4ec", "#ff4040", "#c9d2ca", "#f4f4ec", "#ffd23f", "#9aa59d", stroke=0.06, sfill="#000000"),
                 cap=dict(font="ChakraPetch-Bold.ttf", size=90, fill="#ffffff", hi="#ffd23f", stroke="#000000")),
})

THEMES.update({
    "ut": dict(case="upper", static=static_ut, dyn=dyn_ut, panel=panel_ut, flash="#ffff00", tag_col="#ffff00", frame=("#ffffff", 8),
               text=roles("PressStart2P-Regular.ttf", "PressStart2P-Regular.ttf", "#ffffff", "#ffff00", "#ffffff", "#ffffff", "#ffff00", "#bbbbbb"),
               cap=dict(font="PressStart2P-Regular.ttf", size=58, gap=0.6, fill="#ffffff", hi="#ffff00", stroke="#000000", box="#000000")),
    "subway": dict(case="upper", static=static_subway, dyn=dyn_subway, panel=panel_subway, flash="#ff8c00", tag_col="#ffd23f", frame=("#1a1a2e", 8),
                   text=roles("Bangers-Regular.ttf", "BarlowCondensed-ExtraBold.ttf", "#ffffff", "#ffd23f", "#ffffff", "#1a1a2e", "#ff6a00", "#4a4a5e", stroke=0.08, sfill="#1a1a2e"),
                   cap=dict(font="Bangers-Regular.ttf", size=100, fill="#ffffff", hi="#ffd23f", stroke="#1a1a2e")),
})

THEMES.update({
    "hk": dict(case="upper", static=static_hk, dyn=dyn_hk, panel=panel_hk, flash="#ffffff", tag_col="#e05060", frame=("#e8e4d6", 6),
               text=roles("Cinzel[wght].ttf", "Marcellus-Regular.ttf", "#f1ece0", "#e05060", "#cfd6e6", "#f1ece0", "#e05060", "#a9b2c6", stroke=0.04, sfill="#05070c", wb=800),
               cap=dict(font="Cinzel[wght].ttf", size=84, wght=800, fill="#ffffff", hi="#ff6b7a", stroke="#05070c")),
    "terra": dict(case="upper", static=static_terra, dyn=dyn_terra, panel=panel_terra, flash="#ffd23f", tag_col="#7dff5c", frame=("#0e1228", 8),
                  text=roles("ArchivoBlack-Regular.ttf", "Nunito[wght].ttf", "#ffffff", "#ffd23f", "#ffffff", "#ffffff", "#7dff5c", "#c4cdf0", stroke=0.08, sfill="#14182c", ws=900),
                  cap=dict(font="ArchivoBlack-Regular.ttf", size=86, fill="#ffffff", hi="#ffd23f", stroke="#14182c")),
    "cup": dict(case="upper", static=static_cup, dyn=dyn_cup, panel=panel_cup, flash="#fff4d6", tag_col="#ffd27a", frame=("#2a1a0c", 8),
                text=roles("Limelight-Regular.ttf", "CrimsonText-Bold.ttf", "#2a1a0c", "#c0281e", "#4a3420", "#2a1a0c", "#c0281e", "#6a5038", stroke=0.0),
                cap=dict(font="Limelight-Regular.ttf", size=88, fill="#2a1a0c", hi="#c0281e", stroke="#fff4d6")),
    "stardew": dict(case="upper", static=static_stardew, dyn=dyn_stardew, panel=panel_stardew, flash="#fff6d0", tag_col="#ffd27a", frame=("#6e3c18", 8),
                    text=roles("Chewy-Regular.ttf", "Baloo2[wght].ttf", "#ffffff", "#ffe066", "#fff6e0", "#5a3a1a", "#2e8b3a", "#7a5a3a", stroke=0.08, sfill="#5a3a1a", ws=800),
                    cap=dict(font="Chewy-Regular.ttf", size=96, fill="#ffffff", hi="#ffe066", stroke="#5a3a1a")),
    "poppy": dict(case="upper", static=static_poppy, dyn=dyn_poppy, panel=panel_poppy, flash="#3c82ff", tag_col="#ffc400", frame=("#3c82ff", 7),
                  text=roles("SairaStencilOne-Regular.ttf", "Rajdhani-Bold.ttf", "#ffffff", "#ffc400", "#c8d4ec", "#ffffff", "#ff4a50", "#9aa8c4", stroke=0.05, sfill="#05070c"),
                  cap=dict(font="SairaStencilOne-Regular.ttf", size=88, fill="#ffffff", hi="#ffc400", stroke="#05070c")),
})
