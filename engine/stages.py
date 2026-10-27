"""Topic stages for non-Roblox episodes (user rule, Oct 27 2026: no Roblox avatars/baseplates outside Roblox videos).

An episode sets "stage": "gd" | "meme" | "news". Every generated (non-clip) scene is then drawn here instead of the
isometric baseplate + blocky avatars. Scene keys still work on top: big/sub/count text, ic icons, fx, vig.

  gd    Geometry Dash level: scrolling blocks, spikes and ground, pulsing to the beat, with the player's real
        cube icon (sc["icon"] or ep["gd_icon"], a PNG in episodes/assets, e.g. "gdicon-zoink.png") jumping
        and spinning over spikes. sc["mode"]="ship" flies the ship icon (ep["gd_ship"]) through a corridor.
  meme  phone showing a still from the meme (ep["prop_clip"] frame or sc["prop"] image) with floating reactions.
  news  news desk: monitor with a still from the story, flashing BREAKING tag and a scrolling ticker (ep["ticker"]).
"""
import math, os, random, subprocess
import numpy as np
import gdicons
from PIL import Image, ImageDraw, ImageFilter

W, H = 1080, 1920
D = os.path.dirname(os.path.abspath(__file__)) + "/"
ASSETS = os.path.join(os.path.dirname(D.rstrip("/")), "episodes", "assets")
_cache = {}


def rgb(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def mix(a, b, k):
    return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))


def grad(top, bot):
    key = ("g", top, bot)
    if key not in _cache:
        a, b = np.array(top, np.float32), np.array(bot, np.float32)
        t = np.linspace(0, 1, H)[:, None]
        g = (a * (1 - t) + b * t).astype(np.uint8)
        _cache[key] = Image.fromarray(np.repeat(g[:, None, :], W, axis=1), "RGB").convert("RGBA")
    return _cache[key].copy()


def asset(name, size=None):
    key = ("a", name, size)
    if key not in _cache:
        p = os.path.join(ASSETS, name)
        im = Image.open(p).convert("RGBA") if os.path.exists(p) else None
        if im is not None and size:
            im = im.crop(im.getbbox() or (0, 0, im.width, im.height))
            k = size / max(im.width, im.height)
            im = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.LANCZOS)
        _cache[key] = im
    return _cache[key]


def clip_still(clip, work, t=1.0):
    """One frame from a clip in episodes/assets, cached as PNG in the work folder."""
    key = ("s", clip, t)
    if key not in _cache:
        src = os.path.join(ASSETS, clip)
        out = os.path.join(work, f"still_{clip}_{t}.png")
        if os.path.exists(src) and not os.path.exists(out):
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t), "-i", src, "-frames:v", "1", out])
        _cache[key] = Image.open(out).convert("RGBA") if os.path.exists(out) else None
    return _cache[key]


def fit(im, w, h):
    k = max(w / im.width, h / im.height)
    r = im.resize((int(im.width * k) + 1, int(im.height * k) + 1), Image.LANCZOS)
    x, y = (r.width - w) // 2, (r.height - h) // 2
    return r.crop((x, y, x + w, y + h))


def glow(img, layer, radius=18, strength=1.0):
    """Blur only the drawn area (much faster than blurring the whole 1080x1920 frame)."""
    bb = layer.getbbox()
    if not bb:
        return
    pad = radius * 3
    x0, y0 = max(0, bb[0] - pad), max(0, bb[1] - pad)
    x1, y1 = min(layer.width, bb[2] + pad), min(layer.height, bb[3] + pad)
    part = layer.crop((x0, y0, x1, y1))
    g = part.filter(ImageFilter.GaussianBlur(radius))
    if strength != 1:
        a = g.split()[3].point(lambda v: min(255, int(v * strength)))
        g.putalpha(a)
    img.alpha_composite(g, (x0, y0))
    img.alpha_composite(part, (x0, y0))


def default_cube(size, c1, c2):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    s = size
    d.rectangle([2, 2, s - 3, s - 3], fill=c1, outline=(0, 0, 0), width=max(3, s // 22))
    d.rectangle([s * 0.27, s * 0.27, s * 0.73, s * 0.73], fill=c2, outline=(0, 0, 0), width=max(3, s // 26))
    return im


def player_icon(sc, ep, form, size):
    """sc["icon"]/ep["gd_icon"] file, else the real icon of sc["player"]/ep["gd_player"] (fetched from GDBrowser)."""
    name = sc.get("icon") if form == "cube" else None
    name = name or (ep.get("gd_icon") if form == "cube" else ep.get("gd_" + form))
    if name:
        return asset(name, size)
    player = sc.get("player") or ep.get("gd_player")
    if player:
        p = gdicons.get(player, form)
        if p:
            return asset(os.path.basename(p), size)
    return None


# ============================================================ Geometry Dash
GD_GROUND = 1330          # y of the ground line
SPEED = 560               # px / s scroll speed
GAP = 520                 # px between obstacles
PX = 330                  # player x


def gd_stage(sc, lt, seed, ep, bpm):
    acc = rgb(sc.get("tint", ep.get("accent", "#00e5ff")))
    base = mix((6, 8, 24), acc, 0.18)
    img = grad(mix(base, (0, 0, 0), 0.35), mix(base, acc, 0.35))
    d = ImageDraw.Draw(img)
    beat = max(0.0, math.cos(2 * math.pi * lt * bpm / 60)) ** 4
    # parallax background squares
    rnd = random.Random(seed)
    for k in range(16):
        s = rnd.randint(90, 220)
        x0 = rnd.randint(0, W + 400)
        y0 = rnd.randint(250, GD_GROUND - 150)
        x = (x0 - lt * SPEED * 0.25) % (W + 400) - 200
        col = mix(base, acc, 0.25 + 0.15 * beat) + (90,)
        d.rectangle([x, y0, x + s, y0 + s], outline=col, width=5)
    # ground
    d.rectangle([0, GD_GROUND, W, H], fill=mix(base, acc, 0.22))
    for k in range(-1, 8):
        x = k * 220 - (lt * SPEED) % 220
        d.rectangle([x, GD_GROUND + 8, x + 210, GD_GROUND + 210], outline=mix(base, acc, 0.4), width=4)
    line = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(line).rectangle([0, GD_GROUND - 3, W, GD_GROUND + 3], fill=mix(acc, (255, 255, 255), 0.5 + 0.4 * beat) + (255,))
    glow(img, line, 14, 1.4)
    d = ImageDraw.Draw(img)
    if sc.get("race"):
        return gd_race(img, sc, lt, ep, acc, base, beat)
    mode = sc.get("mode") or ("cube", "ship", "wave")[seed % 3]
    if mode == "ship":
        return gd_ship(img, sc, lt, ep, acc, base, beat)
    if mode == "wave":
        return gd_wave(img, sc, lt, ep, acc, base, beat)
    # obstacles: spike pairs scrolling in, the player jumps each one
    wx = lt * SPEED
    first = int((wx - PX) // GAP) - 1
    for k in range(first, first + 5):
        X = k * GAP + GAP * 0.6
        x = X - wx + PX
        if -120 < x < W + 120:
            kind = (k * 7 + seed) % 3
            for j in range(2 if kind == 0 else 1):
                xx = x + j * 62
                d.polygon([(xx - 31, GD_GROUND), (xx + 31, GD_GROUND), (xx, GD_GROUND - 70)], fill=(10, 10, 14), outline=(255, 255, 255), width=4)
            if kind == 2:
                d.rectangle([x - 80, GD_GROUND - 260, x + 80, GD_GROUND - 200], fill=(10, 10, 14), outline=mix(acc, (255, 255, 255), 0.6), width=5)
    # player
    size = 132
    ic = player_icon(sc, ep, "cube", size)
    if ic is None:
        ic = default_cube(size, acc, mix(acc, (255, 255, 255), 0.6))
    ph = ((wx - GAP * 0.6 + GAP * 0.42) % GAP) / GAP          # 0..1 between obstacles; jump centred on each spike
    jumpw = 0.62
    if ph < jumpw:
        q = ph / jumpw
        hgt = 4 * 330 * q * (1 - q)
        rot = -180 * q
    else:
        hgt, rot = 0, 0
    y = GD_GROUND - size / 2 - hgt
    # trail
    tr = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    td = ImageDraw.Draw(tr)
    for i in range(10):
        tt = lt - i * 0.03
        p2 = (((tt * SPEED) - GAP * 0.6 + GAP * 0.42) % GAP) / GAP
        h2 = 4 * 330 * (p2 / jumpw) * (1 - p2 / jumpw) if p2 < jumpw else 0
        yy = GD_GROUND - size / 2 - h2 + 30
        xx = PX - i * 26 - 50
        a = int(200 * (1 - i / 10))
        r = 12 - i
        td.rectangle([xx - r, yy - r, xx + r, yy + r], fill=mix(acc, (255, 255, 255), 0.5) + (a,))
    img.alpha_composite(tr)
    rimg = ic.rotate(rot, resample=Image.BICUBIC, expand=True)
    gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gl.alpha_composite(rimg, (int(PX - rimg.width / 2), int(y - rimg.height / 2)))
    glow(img, gl, 10, 0.8 + 0.6 * beat)
    return img


def gd_ship(img, sc, lt, ep, acc, base, beat):
    d = ImageDraw.Draw(img)
    top = 520
    # corridor blocks top and bottom with saw-tooth gaps
    for k in range(-1, 10):
        x = k * 140 - (lt * SPEED) % 140
        h1 = 60 + 40 * math.sin((k + int(lt * SPEED // 140)) * 0.9)
        d.rectangle([x, top, x + 136, top + h1], fill=(10, 10, 14), outline=mix(acc, (255, 255, 255), 0.5), width=4)
    size = 170
    ic = player_icon(sc, ep, "ship", size)
    if ic is None:
        ic = default_cube(110, acc, mix(acc, (255, 255, 255), 0.6))
    y = (top + GD_GROUND) / 2 + 170 * math.sin(lt * 2.6)
    rot = -18 * math.cos(lt * 2.6)
    r = ic.rotate(rot, resample=Image.BICUBIC, expand=True)
    gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gl.alpha_composite(r, (int(PX - r.width / 2), int(y - r.height / 2)))
    glow(img, gl, 10, 0.8 + 0.6 * beat)
    return img


def gd_wave(img, sc, lt, ep, acc, base, beat):
    d = ImageDraw.Draw(img)
    top, bot = 560, GD_GROUND
    # sawtooth ceiling and floor
    for k in range(-1, 12):
        x = k * 110 - (lt * SPEED) % 110
        d.polygon([(x, top), (x + 110, top), (x + 55, top + 70)], fill=(10, 10, 14), outline=mix(acc, (255, 255, 255), 0.5))
        d.polygon([(x, bot), (x + 110, bot), (x + 55, bot - 70)], fill=(10, 10, 14), outline=mix(acc, (255, 255, 255), 0.5))
    mid, amp, per = (top + bot) / 2, 230, 0.55

    def wy(t):
        u = (t / per) % 2
        return mid - amp + 2 * amp * (u if u < 1 else 2 - u)
    pts = [(PX - (lt - t) * SPEED, wy(t)) for t in [lt - i * 0.02 for i in range(40)] if PX - (lt - t) * SPEED > -20]
    tr = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if len(pts) > 1:
        ImageDraw.Draw(tr).line(pts, fill=mix(acc, (255, 255, 255), 0.6) + (230,), width=16, joint="curve")
    glow(img, tr, 12, 1.2)
    size = 110
    ic = player_icon(sc, ep, "wave", size)
    if ic is None:
        ic = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        ImageDraw.Draw(ic).polygon([(10, 20), (size - 10, size / 2), (10, size - 20)], fill=acc, outline=(0, 0, 0), width=5)
    up = ((lt / per) % 2) < 1
    r = ic.rotate(-40 if up else 40, resample=Image.BICUBIC, expand=True)
    gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gl.alpha_composite(r, (int(PX - r.width / 2), int(wy(lt) - r.height / 2)))
    glow(img, gl, 8, 0.8 + 0.6 * beat)
    return img


# ============================================================ meme (phone + reactions)
def meme_stage(sc, lt, seed, ep, work, paste_icon):
    acc = rgb(ep.get("accent", "#00e676"))
    img = grad(mix((20, 10, 40), acc, 0.25), mix((60, 20, 90), acc, 0.45))
    d = ImageDraw.Draw(img)
    # phone
    pw, ph = 540, 880
    px, py = (W - pw) // 2, 560
    k = 1 + 0.02 * math.sin(lt * 2)
    still = None
    if sc.get("prop"):
        still = asset(sc["prop"])
    elif ep.get("prop_clip"):
        still = clip_still(ep["prop_clip"], work, sc.get("prop_t", 1.5))
    phone = Image.new("RGBA", (pw + 40, ph + 40), (0, 0, 0, 0))
    pd = ImageDraw.Draw(phone)
    pd.rounded_rectangle([0, 0, pw + 39, ph + 39], 70, fill=(18, 18, 22), outline=(240, 240, 240), width=6)
    if still is not None:
        scr = fit(still, pw - 20, ph - 20)
        m = Image.new("L", scr.size, 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, scr.width - 1, scr.height - 1], 52, fill=255)
        phone.paste(scr, (30, 30), m)
    else:
        pd.rounded_rectangle([30, 30, pw + 9, ph + 9], 52, fill=mix(acc, (0, 0, 0), 0.5))
    pd.rounded_rectangle([pw // 2 - 50, 44, pw // 2 + 90, 70], 13, fill=(0, 0, 0))
    phone = phone.resize((int(phone.width * k), int(phone.height * k)), Image.BICUBIC)
    img.alpha_composite(phone, (int(W / 2 - phone.width / 2), int(py + ph / 2 - phone.height / 2)))
    # side buttons (like / comment / share) with ticking counts
    for i, (n, base_n) in enumerate((("heart", 1.2e6), ("question", 48e3), ("bolt", 21e3))):
        cx, cy = W // 2 + pw // 2 - 40, py + ph - 330 + i * 120
        paste_icon(img, n, cx, cy, 78 + 8 * math.sin(lt * 4 + i))
    # floating reactions
    rnd = random.Random(seed)
    for j in range(14):
        t0 = rnd.uniform(0, 3)
        per = rnd.uniform(2.2, 3.4)
        u = ((lt + t0) % per) / per
        x = rnd.choice([rnd.uniform(60, px - 20), rnd.uniform(px + pw + 30, W - 60)])
        y = H - 300 - u * 1300
        paste_icon(img, rnd.choice(["heart", "fire", "eye", "star", "question"]), x + 30 * math.sin(u * 7 + j), y,
                   int(70 + 30 * rnd.random()), rot=int(20 * math.sin(u * 5 + j)), alpha=max(0, 1 - u ** 3))
    return img


# ============================================================ news desk
def news_stage(sc, lt, seed, ep, work, text_img, font):
    acc = rgb(ep.get("accent", "#2979ff"))
    img = grad((6, 10, 30), mix((10, 20, 60), acc, 0.35))
    d = ImageDraw.Draw(img)
    # moving light beams
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for i in range(5):
        x = (i * 300 + lt * 120) % (W + 600) - 300
        od.polygon([(x, 0), (x + 120, 0), (x + 520, H), (x + 300, H)], fill=acc + (22,))
    img.alpha_composite(ov)
    # monitor
    mw, mh = 920, 518
    mx, my = (W - mw) // 2, 690
    d.rounded_rectangle([mx - 16, my - 16, mx + mw + 16, my + mh + 16], 24, fill=(14, 14, 18), outline=(200, 205, 215), width=5)
    still = asset(sc["prop"]) if sc.get("prop") else (clip_still(ep["prop_clip"], work, sc.get("prop_t", 1.5)) if ep.get("prop_clip") else None)
    if still is not None:
        z = 1.0 + 0.06 * min(1, lt / 5)
        f = fit(still, int(mw * z), int(mh * z))
        f = f.crop(((f.width - mw) // 2, (f.height - mh) // 2, (f.width - mw) // 2 + mw, (f.height - mh) // 2 + mh))
        img.alpha_composite(f, (mx, my))
    else:
        d.rectangle([mx, my, mx + mw, my + mh], fill=mix(acc, (0, 0, 0), 0.6))
    # BREAKING tag
    if int(lt * 2.5) % 2 == 0 or lt < 0.4:
        tag = text_img("BREAKING", 54, (255, 255, 255), font, 0, 5000)
        d.rectangle([mx - 16, my - 16 - 84, mx - 16 + tag.width + 56, my - 16], fill=(220, 20, 40))
        img.alpha_composite(tag, (mx + 12, my - 16 - 84 + (84 - tag.height) // 2))
    # desk + ticker
    d.polygon([(0, 1236), (W, 1236), (W, 1300), (0, 1300)], fill=mix(acc, (0, 0, 0), 0.55))
    d.rectangle([0, 1300, W, 1380], fill=(220, 20, 40))
    tick = ep.get("ticker") or ep.get("file", "").replace(".mp4", "").split(" ", 1)[-1].upper()
    tim = text_img(("   •   ".join([tick] * 4)), 46, (255, 255, 255), font, 3, 20000)
    off = int((lt * 220) % max(1, tim.width // 4))
    img.alpha_composite(tim, (40 - off, 1300 + (80 - tim.height) // 2))
    return img


# ------------------------------------------------------------ race (v2, Oct 27 2026)
# sc["race"] = [{"player": "Zoink", "pct": 80, "col": "#ff5252"}, {"player": "wPopoff", "pct": 81}]
# Two lanes, each player's real cube icon riding a progress bar that fills to their best %, then shakes.
def _font(size):
    key = ("f", size)
    if key not in _cache:
        from PIL import ImageFont
        _cache[key] = ImageFont.truetype(os.path.join(D, "modern", "fonts", "Anton-Regular.ttf"), size)
    return _cache[key]


def gd_race(img, sc, lt, ep, acc, base, beat):
    racers = sc["race"]
    lanes = [760 + i * 330 for i in range(len(racers))]
    best = max(r["pct"] for r in racers)
    x0, x1 = 90, W - 90
    for i, (r, y) in enumerate(zip(racers, lanes)):
        col = rgb(r.get("col", ("#ff5252", "#40c4ff", "#69f0ae")[i % 3]))
        k = min(1.0, max(0.0, (lt - 0.15 * i) / 1.6))
        k = 1 - (1 - k) ** 3
        pct = r["pct"] * k
        bar = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        bd = ImageDraw.Draw(bar)
        bd.rounded_rectangle([x0, y - 34, x1, y + 34], 34, fill=(10, 10, 18, 220), outline=(255, 255, 255, 255), width=5)
        xe = x0 + (x1 - x0) * pct / 100
        if xe > x0 + 40:
            bd.rounded_rectangle([x0 + 8, y - 26, xe, y + 26], 26, fill=col + (255,))
        glow(img, bar, 12, 0.9 + (0.6 * beat if r["pct"] == best else 0.2))
        d = ImageDraw.Draw(img)
        # the 100% finish flag, nobody there yet
        for j in range(4):
            for q in range(2):
                c = (255, 255, 255) if (j + q) % 2 == 0 else (20, 20, 20)
                d.rectangle([x1 - 30 + q * 15, y - 110 + j * 15, x1 - 15 + q * 15, y - 95 + j * 15], fill=c)
        d.line([x1 - 30, y - 110, x1 - 30, y - 34], fill=(255, 255, 255), width=5)
        size = 120
        ic = player_icon({"player": r["player"]}, ep, "cube", size) or default_cube(size, col, mix(col, (255, 255, 255), 0.6))
        hop = abs(math.sin(lt * 7 + i)) * 26 if k < 1 else 0
        shake = (math.sin(lt * 60) * 6 if k >= 1 and r["pct"] == best else 0)
        rot = -90 * ((lt * 3 + i) % 1) if k < 1 else 0
        ri = ic.rotate(rot, resample=Image.BICUBIC, expand=True)
        cx = max(x0 + size / 2, xe) + shake
        img.alpha_composite(ri, (int(cx - ri.width / 2), int(y - 42 - size / 2 - hop - ri.height / 2)))
        f = _font(64)
        name = r["player"].upper()
        d.text((x0 + 6, y + 48), name, font=f, fill=(255, 255, 255), stroke_width=6, stroke_fill=(0, 0, 0))
        pt = f"{pct:.0f}%"
        tw = d.textlength(pt, font=_font(84))
        d.text((x1 - tw, y + 40), pt, font=_font(84), fill=col, stroke_width=7, stroke_fill=(0, 0, 0))
    return img
