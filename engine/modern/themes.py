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


# ================================================================ registry
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
# small-text and credit roles never get a stroke on themes whose backgrounds are light
for _n in ("dw9", "oni", "witcher", "wolv"):
    for _r in ("small", "credit"):
        t = THEMES[_n]["text"][_r]
        THEMES[_n]["text"][_r] = (t[0], t[1], t[2], 0, t[4], None, None)
# control: floating black blocks drift behind the content, so small text sits on its own black plate
_t = THEMES["control"]["text"]["small"]
THEMES["control"]["text"]["small"] = (_t[0], _t[1], "#ffffff", 0, _t[4], None, "#000000")
