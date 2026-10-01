"""8-Bit Backstory video renderer.

usage:  python3 engine/render.py episodes/<preset>/<episode>.json [--sheet] [--out DIR]

  --sheet   render a contact sheet (one frame per line) instead of the MP4, for a quick look
  --out     where finished MP4s go (default: build/out next to the repo root)

The episode JSON picks a preset ("roblox" or "nes"). See README.md for the episode format.
"""
import argparse, json, math, os, subprocess, sys, wave, hashlib, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art import *
import tts, music

D = os.path.dirname(os.path.abspath(__file__)) + "/"
ROOT = os.path.dirname(D.rstrip("/")) + "/"
FPS = 30
WORK, OUT = ROOT + "build/work/", ROOT + "build/out/"
ISO = Iso(540, 1085, 68)

# ------------------------------------------------------------------ presets
NES_PALETTE = ["#000000", "#fcfcfc", "#bcbcbc", "#7c7c7c", "#a4e4fc", "#3cbcfc", "#0078f8", "#0000fc",
               "#b8b8f8", "#6888fc", "#0058f8", "#0000bc", "#d8b8f8", "#9878f8", "#6844fc", "#4428bc",
               "#f8b8f8", "#f878f8", "#d800cc", "#940084", "#f8a4c0", "#f85898", "#e40058", "#a80020",
               "#f0d0b0", "#f87858", "#f83800", "#a81000", "#fce0a8", "#fca044", "#e45c10", "#881400",
               "#f8d878", "#f8b800", "#ac7c00", "#503000", "#d8f878", "#b8f818", "#00b800", "#007800",
               "#b8f8b8", "#58d854", "#00a800", "#006800", "#b8f8d8", "#58f898", "#00a844", "#005800",
               "#00fcfc", "#00e8d8", "#008888", "#004058", "#f8d8f8", "#787878"]

PRESETS = {
    # Roblox Edition: smooth blocky-3D look, chunky cartoon fonts, studded baseplates
    "roblox": {"title_font": "LuckiestGuy.ttf", "sub_font": "Lilita.ttf", "cap_font": "Lilita.ttf",
               "text_scale": 1.0, "cap_size": 92, "edition": "ROBLOX EDITION", "studs": True,
               "pixel": 0, "stroke": 1.0, "hdr_size": 58},
    # NES: the same scenes rendered as chunky pixel art in the NES colour palette, pixel font
    "nes": {"title_font": "PressStart2P.ttf", "sub_font": "PressStart2P.ttf", "cap_font": "PressStart2P.ttf",
            "text_scale": 0.52, "cap_size": 56, "edition": "", "studs": False,
            "pixel": 6, "stroke": 0.7, "hdr_size": 40},
}
ST = PRESETS["roblox"]
_PAL = None


def nes_pixelate(img):
    """Downscale, snap to the NES palette, upscale with hard pixels."""
    global _PAL
    k = ST["pixel"]
    if _PAL is None:
        flat = []
        for c in NES_PALETTE:
            flat += list(rgb(c))
        flat += flat[-3:] * (256 - len(NES_PALETTE))
        _PAL = Image.new("P", (1, 1))
        _PAL.putpalette(flat)
    small = img.convert("RGB").resize((W // k, H // k), Image.BOX)
    small = small.quantize(palette=_PAL, dither=Image.Dither.NONE).convert("RGB")
    return small.resize((W, H), Image.NEAREST).convert("RGBA")


def T(size):
    return max(10, int(size * ST["text_scale"]))


def SW(w):
    return max(2, int(w * ST["stroke"]))

PRESET = {  # avatar colour presets (skin, shirt, pants)
    "a": ("#f1c27d", "#e53935", "#263238"), "b": ("#8d5524", "#1e88e5", "#212121"),
    "c": ("#ffdbac", "#43a047", "#3e2723"), "d": ("#c68642", "#8e24aa", "#1a237e"),
    "e": ("#e0ac69", "#fb8c00", "#37474f"), "f": ("#f5cd30", "#00acc1", "#4e342e"),
    "g": ("#ffdbac", "#ec407a", "#263238"), "h": ("#8d5524", "#fdd835", "#3949ab"),
    "k": ("#e0ac69", "#212121", "#212121"), "w": ("#ffdbac", "#fafafa", "#90a4ae"),
}
GROUND = {"grass": "#5cb85c", "sand": "#f4d58d", "water": "#29b6f6", "dark": "#455a64", "stone": "#90a4ae",
          "night": "#2e7d32", "purple": "#7e57c2", "red": "#c62828", "snow": "#eceff1", "road": "#546e7a",
          "forest": "#33691e", "wood": "#a1887f", "space": "#3949ab"}
BG = {"day": ("#4fc3f7", "#d6f3ff"), "sunset": ("#ff7043", "#ffd180"), "night": ("#0b1033", "#2b3270"),
      "forest": ("#050b14", "#13263a"), "space": ("#05030f", "#2a0f5c"), "dark": ("#15151f", "#33334a"),
      "arena": ("#1a1030", "#4a1f5c"), "party": ("#7c4dff", "#ff80ab"), "ocean": ("#29b6f6", "#e1f5fe"),
      "gold": ("#ff8f00", "#ffe082"), "mint": ("#26a69a", "#b2dfdb"), "red": ("#b71c1c", "#ff8a65")}


def colors(c):
    if isinstance(c, str):
        return PRESET[c]
    return tuple(c)


# ============================================================ static layers
def grad(top, bot):
    a = np.array(rgb(top), np.float32)
    b = np.array(rgb(bot), np.float32)
    t = np.linspace(0, 1, H)[:, None]
    g = (a * (1 - t) + b * t).astype(np.uint8)
    g = np.repeat(g[:, None, :], W, axis=1)
    return Image.fromarray(g, "RGB").convert("RGBA")


def back_layer(sc, seed):
    mode = sc.get("bg", "day")
    if mode == "split":
        lc, rc = sc["vs"][2], sc["vs"][3]
        img = Image.new("RGBA", (W, H), rgb(lc) + (255,))
        d = ImageDraw.Draw(img)
        d.polygon([(640, 0), (W, 0), (W, H), (440, H)], fill=rgb(rc))
        d.line([(640, 0), (440, H)], fill=(255, 255, 255), width=14)
        return img
    top, bot = BG[mode]
    img = grad(top, bot)
    d = ImageDraw.Draw(img)
    rnd = random.Random(seed)
    if mode in ("night", "forest", "space", "arena", "dark"):
        for _ in range(140 if mode == "space" else 70):
            x, y, r = rnd.randint(0, W), rnd.randint(0, 1300), rnd.choice([1.5, 2, 2.5, 3])
            a = rnd.randint(120, 255)
            d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, a))
    if mode in ("night", "forest"):
        paste_icon(img, "moon", 930, 640, 120)
    if mode == "space":
        paste_icon(img, "planet", 150, 640, 170)
    if mode in ("day", "ocean", "party", "mint"):
        for (x, y, s) in ((150, 300, 1.0), (820, 250, 1.3), (520, 470, 0.8), (960, 620, 0.7)):
            for (dx, dy, w, h) in ((0, 0, 200, 60), (40, -36, 110, 60), (110, -20, 90, 50)):
                d.rounded_rectangle([x + dx * s, y + dy * s, x + (dx + w) * s, y + (dy + h) * s], int(22 * s), fill=(255, 255, 255, 235))
    if mode == "forest":
        for i in range(14):
            x = rnd.randint(-40, W)
            hgt = rnd.randint(380, 620)
            w = rnd.randint(90, 150)
            yb = 1240
            col = (8, 22, 30)
            for k in range(4):
                ww = w * (1 - k * 0.22)
                d.rectangle([x + (w - ww) / 2, yb - hgt * (k + 1) / 4 - 40, x + (w + ww) / 2, yb - hgt * k / 4], fill=col)
    if mode == "sunset":
        d.ellipse([380, 420, 700, 740], fill=(255, 236, 179, 200))
    return img


def ground_boxes(sc):
    g = sc.get("ground", "grass")
    if not g or g == "none":
        return []
    if isinstance(g, str):
        g = {"c": GROUND[g]}
    w, dd = g.get("w", 8), g.get("d", 8)
    return [[-w / 2, -dd / 2, -0.6, w, dd, 0.6, rgb(g["c"])]]


def front_layer(sc, seed):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    gb = ground_boxes(sc)
    if gb:
        draw_box(d, ISO, gb[0], 4)
        g = gb[0]
        studs = ST["studs"] and sc.get("ground", "grass") not in ("water", "road")
        if studs:
            sc_ = shade(g[6], 1.18)
            for i in range(int(g[3])):
                for j in range(int(g[4])):
                    x, y = g[0] + i + 0.5, g[1] + j + 0.5
                    px, py = ISO.p(x, y, 0)
                    d.ellipse([px - 13, py - 7, px + 13, py + 7], fill=sc_, outline=shade(g[6], 0.85), width=2)
        else:
            rnd = random.Random(seed)
            for _ in range(30):
                x, y = rnd.uniform(-3.8, 3.8), rnd.uniform(-3.8, 3.8)
                px, py = ISO.p(x, y, 0)
                d.line([(px - 22, py), (px + 22, py)], fill=(255, 255, 255, 140), width=4)
    boxes = []
    for pr in sc.get("props", []):
        name, x, y = pr[0], pr[1], pr[2]
        o = pr[3] if len(pr) > 3 else {}
        boxes += PROPS[name](x, y, o)
    draw_boxes(d, ISO, [[b[0], b[1], b[2], b[3], b[4], b[5], rgb(b[6]) if isinstance(b[6], str) else b[6]] for b in boxes])
    return img


VIG = None


def vignette():
    global VIG
    if VIG is None:
        m = Image.new("L", (W // 8, H // 8), 0)
        dd = ImageDraw.Draw(m)
        dd.ellipse([-W // 16, H // 16, W // 8 + W // 16, H // 8 - H // 32], fill=255)
        m = m.filter(ImageFilter.GaussianBlur(14)).resize((W, H))
        VIG = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        VIG.putalpha(m.point(lambda v: int((255 - v) * 0.55)))
    return VIG


# ============================================================ dynamic
def draw_rays(img, col, t):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    cx, cy = 540, 760
    c = rgb(col) + (70,)
    for i in range(14):
        a0 = math.radians(i * 360 / 14 + t * 12)
        a1 = a0 + math.radians(360 / 28)
        R = 1800
        d.polygon([(cx, cy), (cx + R * math.cos(a0), cy + R * math.sin(a0)), (cx + R * math.cos(a1), cy + R * math.sin(a1))], fill=c)
    img.alpha_composite(ov)


def lerp2(a, b, k):
    return (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k)


def world_dynamic(img, sc, lt, dur, seed):
    d = ImageDraw.Draw(img)
    boxes = []
    holds = []
    k = ease(lt / max(0.1, sc.get("travel", dur)))
    kb = sc.get("keyboard")
    hot = None
    for a in sc.get("av", []):
        p = a.get("p", (0, 0))
        pos = lerp2(p, a["to"], k) if "to" in a else p
        if kb and hot is None:
            hot = pos
    if kb:
        boxes += keyboard_boxes(lt, kb[0], kb[1], kb[2], kb[3], hot)
    for i, pe in enumerate(sc.get("pets", [])):
        p = pe.get("p", (0, 0))
        pos = lerp2(p, pe["to"], k) if "to" in pe else p
        dl = pe.get("d", 0)
        if lt < dl:
            continue
        hop = 0
        if pe.get("a") == "hop":
            hop = abs(math.sin((lt + i) * 5)) * 0.6
        bx, back = creature(pe["k"], pos[0], pos[1], pe.get("z", 0) + hop, lt + i, pe.get("a", "bob"), pe.get("c", "#ffb74d"), pe.get("f", "x"), pe.get("s", 0.75))
        boxes += bx
        if "rider" in pe:
            boxes += avatar(pos[0], pos[1], pe.get("z", 0) + hop + back, lt, "idle", colors(pe["rider"]), pe.get("f", "x"), pe.get("rs", 0.45))
    for i, a in enumerate(sc.get("av", [])):
        dl = a.get("d", 0)
        if lt < dl:
            continue
        p = a.get("p", (0, 0))
        pos = lerp2(p, a["to"], k) if "to" in a else p
        z = a.get("z", 0)
        if kb:
            z = 0.75
        anim = a.get("a", "bob")
        if "to" in a and k >= 0.999 and anim in ("walk", "run", "sneak"):
            anim = "bob"
        boxes += avatar(pos[0], pos[1], z, lt + i * 0.7, anim, colors(a.get("c", "a")), a.get("f", "x"), a.get("s", 0.55), a.get("hat"), a.get("face", "smile"))
        if a.get("hold"):
            holds.append((pos, z, a.get("s", 0.55), a["hold"], a.get("f", "x")))
    cr = sc.get("crowd")
    if cr:
        n = cr["n"]
        rnd = random.Random(seed + 7)
        x0, y0, x1, y1 = cr.get("area", (-3.2, -3.2, 3.2, 3.2))
        cols = int(math.ceil(math.sqrt(n)))
        for j in range(n):
            appear = cr.get("appear", 0) * j / n
            if lt < appear:
                continue
            gx, gy = j % cols, j // cols
            x = x0 + (x1 - x0) * (gx + 0.5) / cols + rnd.uniform(-0.15, 0.15)
            y = y0 + (y1 - y0) * (gy + 0.5) / cols + rnd.uniform(-0.15, 0.15)
            c = (rnd.choice(SKINS), rnd.choice(SHIRTS), rnd.choice(PANTS))
            boxes += avatar(x, y, 0, lt * 1.3 + j, cr.get("a", "jump" if j % 3 == 0 else "bob"), c, rnd.choice("xy"), cr.get("s", 0.3))
    draw_boxes(d, ISO, boxes)
    for (pos, z, s, name, f) in holds:
        if f == "x":
            px, py = ISO.p(pos[0] + 0.6 * s, pos[1] + 1.4 * s, z + 3.3 * s)
        else:
            px, py = ISO.p(pos[0] + 1.4 * s, pos[1] + 0.6 * s, z + 3.3 * s)
        paste_icon(img, name, px + 22, py, 130)


def draw_icons(img, sc, lt):
    for ic in sc.get("ic", []):
        dl = ic.get("d", 0)
        t = lt - dl
        if t < 0:
            continue
        a = ic.get("a", "float")
        x, y, s = ic.get("x", 540), ic.get("y", 600), ic.get("s", 180)
        if "w" in ic:
            x, y = ISO.p(*ic["w"])
        rot = ic.get("rot", 0)
        sc_ = pop(t)
        if a == "float":
            y += math.sin(t * 2.6 + x) * 14
        elif a == "spin":
            rot += math.sin(t * 3) * 14
            y += math.sin(t * 2.2) * 10
        elif a == "pulse":
            sc_ *= 1 + 0.08 * math.sin(t * 8)
        elif a == "fall":
            k = min(1, t / 0.5)
            y = -200 + (y + 200) * (1 - (1 - k) ** 2)
            sc_ = 1
        elif a == "fly":
            k = ease(t / ic.get("dur", 1.5))
            x, y = lerp2((x, y), ic["to"], k)
        elif a == "shake":
            x += math.sin(t * 40) * 6
            rot += math.sin(t * 30) * 6
        elif a == "flicker":
            sc_ = 1 + 0.08 * math.sin(t * 23) + 0.05 * math.sin(t * 37)
        paste_icon(img, ic["n"], x, y, s * sc_, rot, ic.get("arg"))


def draw_fx(img, sc, lt, seed):
    fx = sc.get("fx", [])
    if not fx:
        return
    d = ImageDraw.Draw(img)
    rnd = random.Random(seed)
    if "speed" in fx:
        for i in range(16):
            y = 700 + rnd.uniform(0, 600)
            L = rnd.uniform(120, 300)
            x = W + 100 - ((lt * rnd.uniform(1600, 2600) + rnd.uniform(0, W + 400)) % (W + 400))
            d.line([(x, y), (x + L, y)], fill=(255, 255, 255, 200), width=rnd.choice([4, 6, 8]))
    if "confetti" in fx:
        for i in range(60):
            x0 = rnd.uniform(0, W)
            sp = rnd.uniform(250, 520)
            y = (rnd.uniform(-H, 0) + lt * sp) % (H + 200) - 100
            x = x0 + math.sin(lt * 3 + i) * 30
            c = rgb(rnd.choice(SHIRTS))
            a = lt * 5 + i
            w, h = 22 * abs(math.cos(a)) + 4, 12
            d.rectangle([x - w / 2, y - h / 2, x + w / 2, y + h / 2], fill=c)
    if "fireflies" in fx:
        for i in range(26):
            x = (rnd.uniform(0, W) + math.sin(lt * 0.7 + i) * 60) % W
            y = rnd.uniform(500, 1400) + math.cos(lt * 0.9 + i * 2) * 40
            a = int(140 + 110 * math.sin(lt * 4 + i))
            r = 7
            d.ellipse([x - r * 2, y - r * 2, x + r * 2, y + r * 2], fill=(255, 241, 118, a // 4))
            d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 245, 157, a))
    if "sparkle" in fx:
        for i in range(10):
            x, y = rnd.uniform(80, W - 80), rnd.uniform(300, 1300)
            s = 60 * max(0, math.sin(lt * 3 + i * 1.7))
            paste_icon(img, "star", x, y, s)
    if "coins" in fx:
        for i in range(12):
            x = rnd.uniform(60, W - 60)
            y = (rnd.uniform(-H, 0) + lt * rnd.uniform(500, 800)) % (H + 300) - 150
            paste_icon(img, "coin", x, y, 90, (lt * 200 + i * 40) % 360)
    if "waves" in fx:
        for i in range(14):
            x0, y0 = rnd.uniform(-3.8, 3.8), rnd.uniform(-3.8, 3.8)
            px, py = ISO.p(x0, y0, 0)
            px += math.sin(lt * 2 + i) * 20
            d.arc([px - 30, py - 10, px + 30, py + 10], 200, 340, fill=(255, 255, 255, 220), width=5)
    if "red" in fx:
        a = int(35 + 30 * math.sin(lt * 8))
        ov = Image.new("RGBA", (W, H), (255, 0, 0, a))
        img.alpha_composite(ov)


def draw_bar9(img, lt):
    cols = ["#bdbdbd", "#66bb6a", "#42a5f5", "#ab47bc", "#ffa726", "#ef5350", "#ec407a", "#26c6da", "#fff176"]
    d = ImageDraw.Draw(img)
    x0, y0, bw, gap = 90, 610, 92, 8
    for i, c in enumerate(cols):
        t = lt - i * 0.12
        if t < 0:
            continue
        s = pop(t, 0.25)
        x = x0 + i * (bw + gap) + bw / 2
        hh = 70 * s
        d.rounded_rectangle([x - bw / 2, y0 - hh / 2, x + bw / 2, y0 + hh / 2], 14, fill=rgb(c), outline=(20, 20, 30), width=6)
    if lt > 0.3:
        paste_center(img, text_img("COMMON", T(46), (255, 255, 255), ST["sub_font"], SW(7)), 200, 690)
    if lt > 1.2:
        paste_center(img, text_img("DIVINE", T(46), (255, 241, 118), ST["sub_font"], SW(7)), 880, 690)


def draw_texts(img, sc, lt, ep):
    y = sc.get("by", 400)
    big = sc.get("big")
    if "count" in sc:
        c = sc["count"]
        k = ease(lt / c.get("dur", 1.4))
        v = c.get("from", 0) + (c["to"] - c.get("from", 0)) * k
        big = c["fmt"].format(v)
    if big:
        for i, line in enumerate(big.split("\n")):
            col = rgb(sc.get("bc", "#ffffff"))
            im = text_img(line, T(sc.get("bs", 130)), col, ST["title_font"], SW(10))
            s = pop(lt - 0.05 - i * 0.12, 0.32) if "count" not in sc else 1
            paste_center(img, im, 540, y + i * (T(sc.get("bs", 130)) + 18), s)
        y += (len(big.split("\n")) - 1) * (T(sc.get("bs", 130)) + 18)
    if sc.get("sub"):
        for i, line in enumerate(sc["sub"].split("\n")):
            im = text_img(line, T(sc.get("ss", 66)), rgb(sc.get("sc", ep["accent"])), ST["sub_font"], SW(9))
            paste_center(img, im, 540, y + 135 + i * 78, pop(lt - 0.35 - i * 0.1, 0.3))
    if "vs" in sc:
        l, r = sc["vs"][0], sc["vs"][1]
        paste_center(img, text_img(l, T(84), (255, 255, 255), ST["title_font"], SW(10), 460), 280, 420, pop(lt, 0.3))
        paste_center(img, text_img(r, T(84), (255, 255, 255), ST["title_font"], SW(10), 460), 800, 420, pop(lt - 0.15, 0.3))
        paste_center(img, text_img("VS", T(150), rgb(ep["accent"]), ST["title_font"], SW(10)), 540, 640, pop(lt - 0.3, 0.3) * (1 + 0.05 * math.sin(lt * 6)))


def header(ep):
    im = Image.new("RGBA", (W, 230), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    t1 = text_img("8-BIT BACKSTORY ", ST["hdr_size"], (255, 255, 255), ST["title_font"], SW(8))
    t2 = text_img(f"#{ep['num']}", ST["hdr_size"], rgb(ep["accent"]), ST["title_font"], SW(8))
    wtot = t1.width + t2.width - 6
    x = (W - wtot) // 2
    d.rounded_rectangle([x - 24, 84, x + wtot + 24, 170], 40, fill=(20, 20, 35, 190), outline=rgb(ep["accent"]), width=5)
    im.alpha_composite(t1, (x, 88))
    im.alpha_composite(t2, (x + t1.width - 6, 88))
    edition = ep.get("edition", ST["edition"])
    if edition:
        t3 = text_img(edition, T(36), rgb(ep["accent"]), ST["sub_font"], SW(6))
        im.alpha_composite(t3, ((W - t3.width) // 2, 170))
    return im


# ============================================================ captions
def chunks_for(text):
    words = text.split()
    out, cur = [], []
    for w in words:
        if cur and (len(" ".join(cur + [w])) > 20 or len(cur) >= 4):
            out.append(cur)
            cur = []
        cur.append(w)
        if w[-1] in ",.!?:" and len(cur) >= 2:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def word_times(text, t0, t1):
    words = text.split()
    wts = [len(w) + 3 * sum(ch.isdigit() for ch in w) + (4 if w[-1] in ",.!?" else 0) + 2 for w in words]
    tot = sum(wts)
    res, t = [], t0
    for w, k in zip(words, wts):
        dt = (t1 - t0) * k / tot
        res.append((w, t, t + dt))
        t += dt
    return res


def draw_caption(img, line, t0, t1, now):
    wt = word_times(line, t0, t1)
    chs = chunks_for(line)
    idx = 0
    for ch in chs:
        seg = wt[idx: idx + len(ch)]
        start, end = seg[0][1], seg[-1][2]
        if start - 0.02 <= now < end + 0.25 or (ch is chs[-1] and now >= start):
            parts = []
            for (w, a, b) in seg:
                cur = a <= now < b + (0.25 if (w, a, b) == seg[-1] else 0)
                parts.append((w.upper(), cur))
            sp = 26
            ims = [text_img(w, ST["cap_size"], (255, 230, 60) if cur else (255, 255, 255), ST["cap_font"], SW(9)) for w, cur in parts]
            tw = sum(i.width for i in ims) + sp * (len(ims) - 1) - 20 * len(ims)
            sc = min(1.0, 1000 / max(1, tw))
            x = 540 - tw * sc / 2
            k = pop(now - start, 0.18)
            for im, (w, cur) in zip(ims, parts):
                s = sc * (1.08 if cur else 1.0) * k
                paste_center(img, im, x + (im.width - 20) * sc / 2, 1500, s)
                x += (im.width - 20 + sp) * sc
            return
        idx += len(ch)


# ============================================================ voice
def synth_lines(ep, speed):
    sr = 24000
    clips = []
    for ln in ep["lines"]:
        key = hashlib.md5(f"{ln.get('say', ln['t'])}|{ep.get('voice','am_michael')}|{speed:.3f}|{json.dumps(ep.get('pron', {}), sort_keys=True)}".encode()).hexdigest()
        fn = WORK + key + ".npy"
        if os.path.exists(fn):
            a = np.load(fn)
        else:
            a, sr = tts.say(ln.get("say", ln["t"]), ep.get("voice", "am_michael"), speed, ep.get("pron"))
            np.save(fn, a)
        clips.append(a)
    return clips, sr


def build_voice(ep):
    target = ep["target"]
    speed = ep.get("speed", 1.12)
    gap, lead, tail = 0.16, 0.3, 1.2
    for _ in range(3):
        clips, sr = synth_lines(ep, speed)
        total = lead + sum(len(c) / sr for c in clips) + gap * (len(clips) - 1) + tail
        if total > target + 1.0 and speed < 1.4:
            speed = min(1.4, speed * total / (target + 0.3))
            continue
        break
    timing, parts, t = [], [np.zeros(int(sr * lead), np.float32)], lead
    for c in clips:
        timing.append([t, t + len(c) / sr])
        parts += [c, np.zeros(int(sr * gap), np.float32)]
        t += len(c) / sr + gap
    audio = np.concatenate(parts)
    end = max(t - gap + tail, target - 0.5 if total < target else 0)
    audio = np.concatenate([audio, np.zeros(max(0, int(end * sr) - len(audio)), np.float32)])
    audio = audio / np.max(np.abs(audio)) * 0.92
    with wave.open(WORK + f"{ep['slug']}_voice.wav", "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((audio * 32767).astype(np.int16).tobytes())
    return timing, end, speed


def write_wav(fn, a, sr):
    a = np.clip(a, -1, 1)
    with wave.open(fn, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((a * 32767).astype(np.int16).tobytes())


def sfx_track(starts, end):
    sr = music.SR
    a = np.zeros(int((end + 1) * sr), np.float32)
    for i, s in enumerate(starts[1:]):
        n = int(0.16 * sr)
        t = np.arange(n) / sr
        f = 500 + 900 * t / 0.16
        w = np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-t * 18) * 0.22
        nz = np.random.default_rng(i).uniform(-1, 1, n) * np.exp(-t * 30) * 0.05
        p = int(max(0, s - 0.05) * sr)
        a[p:p + n] += (w + nz)[: len(a) - p]
    return a[: int(end * sr)]


# ============================================================ main render
def render(ep, sheet=False):
    os.makedirs(WORK, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    timing, END, speed = build_voice(ep)
    NF = int(END * FPS)
    starts = [0.0] + [timing[i][0] - 0.08 for i in range(1, len(timing))]
    hdr = header(ep)
    layers = {}

    def get_layers(i):
        if i not in layers:
            sc = ep["lines"][i]["sc"]
            b = back_layer(sc, ep["num"] * 31 + i)
            f = front_layer(sc, ep["num"] * 31 + i)
            if not sc.get("rays"):
                b.alpha_composite(f)
                f = None
            layers.clear()
            layers[i] = (b, f)
        return layers[i]

    def frame(fi):
        now = fi / FPS
        i = max(j for j in range(len(starts)) if starts[j] <= now)
        sc = ep["lines"][i]["sc"]
        nxt = starts[i + 1] if i + 1 < len(starts) else END
        lt = now - starts[i]
        b, f = get_layers(i)
        img = b.copy()
        if sc.get("rays"):
            draw_rays(img, sc["rays"], now)
            img.alpha_composite(f)
        world_dynamic(img, sc, lt, nxt - starts[i], ep["num"] * 31 + i)
        draw_fx(img, sc, lt, ep["num"] * 13 + i)
        if sc.get("vig"):
            img.alpha_composite(vignette())
        if sc.get("bar9"):
            draw_bar9(img, lt)
        draw_icons(img, sc, lt)
        if ST["pixel"]:
            img = nes_pixelate(img)
        draw_texts(img, sc, lt, ep)
        img.alpha_composite(hdr, (0, 0))
        ln = ep["lines"][i]
        t0, t1 = timing[i]
        if now >= t0 - 0.05:
            draw_caption(img, ln["t"], t0, t1, now)
        if lt < 0.1 and i > 0:
            fl = Image.new("RGBA", (W, H), (255, 255, 255, int(150 * (1 - lt / 0.1))))
            img.alpha_composite(fl)
        return img

    if sheet:
        thumbs = []
        for i in range(len(ep["lines"])):
            mid = (timing[i][0] + timing[i][1]) / 2
            thumbs.append(frame(int(mid * FPS)).convert("RGB").resize((270, 480)))
        cols = 6
        rows = math.ceil(len(thumbs) / cols)
        s = Image.new("RGB", (270 * cols, 480 * rows), (0, 0, 0))
        for k, t in enumerate(thumbs):
            s.paste(t, ((k % cols) * 270, (k // cols) * 480))
        s.save(WORK + f"sheet_{ep['slug']}.png")
        print("sheet", ep["slug"], f"{END:.1f}s speed {speed:.2f}")
        return

    vid = WORK + f"{ep['slug']}_video.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
                          "-pix_fmt", "yuv420p", vid], stdin=subprocess.PIPE)
    for fi in range(NF):
        p.stdin.write(frame(fi).convert("RGB").tobytes())
    p.stdin.close()
    p.wait()
    mus = music.make(END, seed=ep["num"], bpm=ep.get("bpm", 128), root=ep.get("root", 60), mood=ep.get("mood", "happy"))
    write_wav(WORK + f"{ep['slug']}_music.wav", mus, music.SR)
    write_wav(WORK + f"{ep['slug']}_sfx.wav", sfx_track(starts, END), music.SR)
    final = OUT + ep["file"]
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", WORK + f"{ep['slug']}_voice.wav",
                    "-i", WORK + f"{ep['slug']}_music.wav", "-i", WORK + f"{ep['slug']}_sfx.wav", "-filter_complex",
                    "[1:a]aresample=44100,volume=1.5,asplit=2[vo1][vo2];[2:a]volume=0.30[mu];"
                    "[mu][vo1]sidechaincompress=threshold=0.05:ratio=6:attack=20:release=300[md];"
                    "[md][vo2][3:a]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.95[aout]",
                    "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", final], check=True)
    print("done", final, f"{END:.1f}s speed {speed:.2f}")


def load(path):
    global ST
    ep = json.load(open(path))
    ep.setdefault("slug", os.path.splitext(os.path.basename(path))[0])
    ST = PRESETS[ep.get("preset", "roblox")]
    return ep


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("episode", nargs="+", help="episode JSON file(s)")
    ap.add_argument("--sheet", action="store_true", help="contact sheet instead of MP4")
    ap.add_argument("--out", help="output folder for MP4s")
    a = ap.parse_args()
    if a.out:
        OUT = os.path.abspath(a.out) + "/"
    for path in a.episode:
        render(load(path), a.sheet)
