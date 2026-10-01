"""Props and backgrounds for episodes 31+ (all original pixel art, drawn with rectangles on the 180x320 canvas).

Also holds the "photo" slot: a framed area that shows an image or short clip the channel owner supplies
(put the file in episodes/assets/ and reference it with {"prop": "photo", "args": {"file": "name.png"}}).
"""
import hashlib, math, os, subprocess
import numpy as np
from PIL import Image, ImageDraw
from lib import *
import props2
import __main__ as E   # engine helpers: cart, console, block, cloud, PERSON, ROBOT, fit_lines

ROOT = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../..") + "/"
ASSETS = ROOT + "episodes/assets/"
OVERLAYS = []          # filled per frame by the photo prop: (PIL image, (x0, y0, x1, y1) in low-res px)
_media = {}


G['$'] = ["00100", "01111", "10100", "01110", "00101", "11110", "00100"]
G['&'] = ["01100", "10010", "10100", "01000", "10101", "10010", "01101"]
G['('] = ["00010", "00100", "01000", "01000", "01000", "00100", "00010"]
G[')'] = ["01000", "00100", "00010", "00010", "00010", "00100", "01000"]
G['%'] = ["11001", "11010", "00010", "00100", "01000", "01011", "10011"]

# ------------------------------------------------------------------ sprites
SHIP = sprite([
    "..w.......",
    ".wwww.....",
    "rwwwwwwb..",
    "owwwwwwwwc",
    "rwwwwwwb..",
    ".wwww.....",
    "..w......."], {'w': P['wht'], 'b': P['lblu'], 'c': P['cyn'], 'r': P['red'], 'o': P['org']})
ENEMY = sprite([".rr.", "rkkr", "rrrr", "r..r"], {'r': P['red'], 'k': P['blk']})
KNIGHT = sprite([
    "...gggg.....",
    "..gggggg....",
    "..gkssk.....",
    "...gggg.....",
    "..llllll....",
    ".gllllllg...",
    ".g.llll.g...",
    "...llll.....",
    "...gggg.....",
    "...gg.gg....",
    "..gg...gg...",
    "..kk...kk..."], {'g': P['gry'], 'l': P['lgry'], 's': P['skin'], 'k': P['blk']})
DOGBOT = sprite([
    "........gg..",
    ".......gllg.",
    "g......glyg.",
    "gg.gggggllgo",
    ".ggllllllgg.",
    "..gllllllg..",
    "..gg....gg..",
    "..dd....dd.."], {'g': P['gry'], 'l': P['lgry'], 'y': P['yel'], 'o': P['org'], 'd': P['dgry']})
GHOST = sprite([".www.", "wkwkw", "wwwww", "wwwww", "w.w.w"], {'w': P['wht'], 'k': P['blk']})


def person(col, hair='brn', pants='navy', flip=False):
    return props2.fighter(col, hair, pants, flip)


def bubble(img, x0, y0, x1, y1, text, col='wht', tail=None, sc=1):
    d = ImageDraw.Draw(img)
    box(img, x0, y0, x1, y1, P['blk'], P[col])
    scl, lines = E.fit_lines(text, sc, 4, x1 - x0 - 8)
    y = y0 + ((y1 - y0) - len(lines) * (8 * scl + 2)) // 2 + 1
    for ln in lines:
        ptext(img, ln, (x0 + x1) // 2, y, P[col], scl, None, True); y += 8 * scl + 2
    if tail:
        d.polygon([(tail[0] - 4, y1), (tail[0] + 4, y1), tail], fill=P[col])


def controller(img, x, y, hot=None, label=None):
    d = ImageDraw.Draw(img)
    box(img, x, y, x + 70, y + 30, P['lgry'], P['gry'])
    d.rectangle([x + 3, y + 3, x + 67, y + 27], fill=P['dgry'])
    cx, cy = x + 16, y + 15
    for nm, (dx, dy) in {"L": (-7, 0), "R": (7, 0), "U": (0, -7), "D": (0, 7), "C": (0, 0)}.items():
        d.rectangle([cx + dx - 3, cy + dy - 3, cx + dx + 3, cy + dy + 3], fill=P['yel'] if nm == hot else P['blk'])
    d.rectangle([x + 30, y + 16, x + 36, y + 19], fill=P['gry']); d.rectangle([x + 39, y + 16, x + 45, y + 19], fill=P['gry'])
    for i, nm in enumerate("BA"):
        d.ellipse([x + 49 + i * 10, y + 11, x + 56 + i * 10, y + 18], fill=P['yel'] if nm == hot else P['red'])
    if label:
        ptext(img, label, x + 35, y - 10, P['wht'], 1, P['blk'], True)


# ------------------------------------------------------------------ backgrounds
def extra_bg(img, name, t):
    d = ImageDraw.Draw(img)
    if name == "moon":
        d.rectangle([0, 0, W, H], fill=P['blk'])
        stars(img, t, 21)
        d.ellipse([146, 118, 172, 144], fill=P['blu']); d.ellipse([152, 122, 164, 131], fill=P['lgrn'])   # a far-away planet
        d.rectangle([0, 196, W, H], fill=P['lgry'])
        for (x, r) in ((20, 10), (70, 6), (120, 12), (160, 7), (44, 5)):
            d.ellipse([x - r, 206 + (x % 30) - r // 2, x + r, 206 + (x % 30) + r // 2], fill=P['gry'])
        return True
    if name == "court":
        sky(img, P['navy'], P['pur'])
        for i in range(60):
            x = (i * 31) % W; y = 70 + (i * 17) % 60
            d.rectangle([x, y, x + 3, y + 4], fill=[P['red'], P['yel'], P['lblu'], P['wht']][(i + int(t * 3)) % 4])
        d.rectangle([0, 196, W, H], fill=P['org'])
        d.line([0, 196, W, 196], fill=P['wht'], width=2); d.arc([50, 206, 130, 260], 180, 360, fill=P['wht'], width=2)
        return True
    if name == "underwater":
        sky(img, P['dblu'], P['blu'])
        for x in range(0, W, 2):
            d.point([x, int(52 + math.sin(x / 9 + t * 3) * 3)], fill=P['lblu'])
        for i in range(7):
            bx = (i * 29 + 8) % W; by = 190 - ((t * 22 + i * 37) % 130)
            d.ellipse([bx, by, bx + 3, by + 3], outline=P['lblu'])
        d.rectangle([0, 196, W, H], fill=P['navy'])
        return True
    if name == "graveyard":
        sky(img, P['navy'], P['mag']); stars(img, t, 23)
        d.ellipse([20, 28, 56, 64], fill=P['lyel'])
        d.rectangle([0, 196, W, H], fill=P['dgry'])
        for x in (14, 60, 108, 150):
            d.rounded_rectangle([x, 172, x + 16, 198], 6, fill=P['gry']); d.line([x + 8, 178, x + 8, 190], fill=P['dgry']); d.line([x + 4, 182, x + 12, 182], fill=P['dgry'])
        return True
    if name == "base":
        d.rectangle([0, 0, W, H], fill=P['dgry'])
        for y in range(0, 196, 14):
            d.line([0, y, W, y], fill=P['gry'])
            for x in range((y // 14 % 2) * 12, W, 24): d.line([x, y, x, y + 14], fill=P['gry'])
        d.rectangle([0, 196, W, H], fill=P['blk']); d.line([0, 196, W, 196], fill=P['yel'])
        return True
    if name == "town":
        sky(img, P['org'], P['lyel'])
        for i, (x, w_, h) in enumerate([(4, 40, 60), (50, 34, 80), (90, 44, 56), (140, 36, 72)]):
            d.rectangle([x, 196 - h, x + w_, 196], fill=P['tan']); d.polygon([(x - 3, 196 - h), (x + w_ // 2, 180 - h), (x + w_ + 3, 196 - h)], fill=P['red'])
            d.rectangle([x + 6, 206 - h, x + 14, 216 - h], fill=P['navy']); d.rectangle([x + w_ - 14, 206 - h, x + w_ - 6, 216 - h], fill=P['navy'])
            d.rectangle([x + w_ // 2 - 5, 180, x + w_ // 2 + 5, 196], fill=P['brn'])
        d.rectangle([0, 196, W, H], fill=P['brn'])
        return True
    return False


# ------------------------------------------------------------------ media slot
def _load_media(fname):
    """Returns a list of RGBA frames (1 for an image, many for a clip), or None if the file is missing."""
    if fname in _media:
        return _media[fname]
    path = fname if os.path.isabs(fname) else ASSETS + fname
    frames = None
    if os.path.exists(path):
        if path.lower().endswith((".mp4", ".mov", ".webm", ".gif", ".mkv")):
            cache = ROOT + "build/work/nes/clip_" + hashlib.md5(path.encode()).hexdigest()[:10]
            if not os.path.isdir(cache):
                os.makedirs(cache)
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", path, "-t", "8", "-r", "30",
                                "-vf", "scale=840:-2", cache + "/%04d.jpg"], check=True)
            frames = [Image.open(cache + "/" + f).convert("RGBA") for f in sorted(os.listdir(cache))]
        else:
            frames = [Image.open(path).convert("RGBA")]
    _media[fname] = frames
    return frames


def photo(img, t, lt, a):
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = a.get("rect", [20, 62, 160, 192])
    box(img, x0 - 3, y0 - 3, x1 + 3, y1 + 3, P['blk'], P['yel'])
    frames = _load_media(a.get("file", ""))
    if not frames:
        ptext(img, "ADD IMAGE:", (x0 + x1) // 2, (y0 + y1) // 2 - 10, P['gry'], 1, None, True)
        ptext(img, os.path.basename(a.get("file", "?"))[:22], (x0 + x1) // 2, (y0 + y1) // 2 + 2, P['gry'], 1, None, True)
    else:
        OVERLAYS.append((frames[int(lt * 30) % len(frames)], (x0, y0, x1, y1)))
    if a.get("label"):
        box(img, x0, y1 - 12, x1, y1, P['blk'], P['blk'])
        ptext(img, a["label"], (x0 + x1) // 2, y1 - 9, P['yel'], 1, None, True)


def apply_overlays(frame):
    """Called by the engine after the 6x upscale: paste supplied media at full resolution."""
    for im, (x0, y0, x1, y1) in OVERLAYS:
        bw, bh = (x1 - x0) * S, (y1 - y0) * S
        k = min(bw / im.width, bh / im.height)
        im2 = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.LANCZOS)
        frame.paste(im2.convert("RGB"), (x0 * S + (bw - im2.width) // 2, y0 * S + (bh - im2.height) // 2))
    OVERLAYS.clear()
    return frame


# ------------------------------------------------------------------ props
def extra_prop(img, t, lt, name, a):
    d = ImageDraw.Draw(img)
    if name == "photo":
        photo(img, t, lt, a)
    elif name == "quote":          # in-game style text box, typed out
        txt = a["text"]; n = int(lt * a.get("cps", 16))
        y0 = a.get("y", 96)
        sc, lines = E.fit_lines(txt, a.get("sc", 2), 4, W - 36)
        h = len(lines) * (8 * sc + 2) + 14
        box(img, 10, y0, W - 10, y0 + h, P['blk'], P[a.get("col", "wht")])
        y = y0 + 8; used = 0
        for ln in lines:
            show = ln[:max(0, n - used)]; used += len(ln) + 1
            ptext(img, show, 90 - text_w(ln, sc) // 2, y, P[a.get("col", "wht")], sc); y += 8 * sc + 2
    elif name == "bignum":         # count-up number with unit (no coins)
        target = a["n"]; k = ease(min(1, lt / a.get("dur", 1.6))); v = target * k
        txt = a.get("fmt", "{:.0f}").format(v)
        sc = min(5, (W - 10) // (6 * len(a.get("fmt", "{:.0f}").format(target))))
        ptext(img, txt, 90, 92, P[a.get("col", "yel")], sc, P['red'], True)
        if a.get("unit"): E.block(img, a["unit"], 92 + 8 * sc + 8, P['wht'], 2, 2)
    elif name == "shooter":        # side-scrolling space shooter
        sx = 34 + math.sin(t * 1.3) * 10; sy = 126 + math.sin(t * 2.1) * 22
        for i in range(4):
            ex = W + 10 - ((lt * 55 + i * 50) % (W + 40)); ey = 84 + i * 26 + math.sin(t * 3 + i) * 8
            paste(img, ENEMY, ex, ey, scale=3)
        paste(img, SHIP, sx, sy, scale=3)
        for i in range(3):
            bx = sx + 34 + ((lt * 160 + i * 45) % 130)
            d.rectangle([bx, sy + 9, bx + 6, sy + 10], fill=P['yel'])
        if a.get("options"):
            for i in range(2):
                ox = sx - 14 - i * 14; oy = sy + 6 + math.sin(t * 2.1 - 0.5 * (i + 1)) * 6
                d.ellipse([ox, oy, ox + 9, oy + 9], fill=P['org'], outline=P['yel'])
    elif name == "powerbar":       # power-up meter that fills as you enter the code
        names = a.get("items", ["SPEED", "MISSILE", "DOUBLE", "LASER", "OPTION", "SHIELD"])
        on = a.get("on", [1, 4, 5]); n = int(max(0, lt - 0.8) * 3)
        for i, nm in enumerate(names):
            x = 6 + (i % 3) * 57; y = 84 + (i // 3) * 34
            lit = i in on and on.index(i) < n
            box(img, x, y, x + 54, y + 24, P['yel'] if lit else P['navy'], P['wht'] if lit else P['gry'])
            ptext(img, nm, x + 27, y + 9, P['blk'] if lit else P['gry'], 1, None, True)
        paste(img, SHIP, 76, 160 + int(math.sin(t * 3) * 3), scale=3)
        if n >= len(on):
            d.ellipse([70, 152, 112, 190], outline=P['cyn'], width=1)
    elif name == "sneak":          # soldier hiding under a box while a guard patrols
        gx = 120 + math.sin(lt * 1.2) * 34
        paste(img, person('grn', 'blk', 'grn', flip=math.cos(lt * 1.2) > 0), gx, 130, scale=4)
        bx = 22 + min(40, lt * 14)
        moving = lt < 2.9 and math.cos(lt * 1.2) < 0
        box(img, bx, 150 - (2 if moving and int(t * 8) % 2 else 0), bx + 44, 178, P['tan'], P['brn'])
        d.line([bx + 22, 151, bx + 22, 177], fill=P['brn']); d.rectangle([bx + 8, 160, bx + 18, 164], fill=P['brn'])
        if moving: d.rectangle([bx + 10, 178, bx + 16, 182], fill=P['blk']); d.rectangle([bx + 28, 178, bx + 34, 182], fill=P['blk'])
        if a.get("alert") and lt > 3.0 and int(t * 6) % 2:
            ptext(img, "!", gx + 24, 108, P['red'], 3, P['wht'], True)
        d.rectangle([0, 178, W, 180], fill=P['gry'])
    elif name == "parachute":      # jungle drop
        for i in range(3):
            k = min(1, max(0, (lt - i * 0.5) / 2.4)); x = 30 + i * 52; y = 40 + k * 110
            if k < 1:
                d.pieslice([x - 14, y - 22, x + 26, y + 10], 180, 360, fill=[P['wht'], P['yel'], P['org']][i])
                d.line([x - 13, y - 6, x + 6, y + 14], fill=P['wht']); d.line([x + 25, y - 6, x + 6, y + 14], fill=P['wht'])
            paste(img, person('grn', 'blk', 'grn'), x - 6, y + 8, scale=2)
    elif name == "mainframe":      # big blinking computer
        box(img, 30, 70, 150, 186, P['gry'], P['lgry'])
        for r in range(4):
            for c in range(6):
                on = (r * 7 + c * 5 + int(t * 5)) % 4 == 0
                d.rectangle([40 + c * 17, 80 + r * 14, 50 + c * 17, 88 + r * 14], fill=[P['red'], P['lgrn'], P['yel']][(r + c) % 3] if on else P['dgry'])
        for i in range(2):
            cx = 62 + i * 56; ang = t * 3 + i
            d.ellipse([cx - 14, 142, cx + 14, 170], fill=P['dgry'], outline=P['blk'])
            d.line([cx, 156, cx + 12 * math.cos(ang), 156 + 12 * math.sin(ang)], fill=P['lgry'], width=2)
        d.rectangle([40, 176, 140, 182], fill=P['blk'])
    elif name == "dam":            # underwater bomb hunt against the clock
        total = a.get("secs", 140); left = max(0, total - int(lt * a.get("rate", 24)))
        box(img, 52, 64, 128, 88, P['blk'], P['red'])
        ptext(img, f"{left // 60}:{left % 60:02d}", 90, 70, P['red'] if int(t * 4) % 2 or left > 30 else P['wht'], 2, None, True)
        for i in range(6):
            x = 10 + i * 30
            for s in range(8):
                yy = 196 - s * 8; xx = x + math.sin(t * 4 + s * 0.8 + i) * 4
                d.rectangle([xx, yy - 8, xx + 3, yy], fill=P['pnk'] if (s + int(t * 6)) % 3 else P['wht'])
        n = a.get("bombs", 8); done = min(n, int(lt * 1.2))
        for i in range(n):
            x = 14 + (i % 4) * 42; y = 104 + (i // 4) * 30
            c = P['lgrn'] if i < done else P['red']
            d.ellipse([x, y, x + 12, y + 12], fill=P['dgry'], outline=c); d.rectangle([x + 5, y - 4, x + 7, y], fill=c)
            if i >= done and int(t * 5 + i) % 2: d.point([x + 6, y - 5], fill=P['yel'])
        sw = person('grn', 'grn', 'grn').rotate(-70, expand=True, resample=Image.NEAREST)
        paste(img, sw, 20 + (lt * 22) % 130, 150 + math.sin(t * 3) * 6, scale=2)
    elif name == "squad":          # pick one of four heroes
        cols = a.get("cols", ['blu', 'red', 'pur', 'org']); sel = int(lt * 1.6) % len(cols)
        for i, c in enumerate(cols):
            x = 12 + i * 41
            box(img, x, 92, x + 34, 150, P['navy'] if i != sel else P['blk'], P[c] if i == sel else P['gry'])
            paste(img, person('grn', c, 'grn'), x + 5, 104 - (4 if i == sel else 0), scale=2)
            ptext(img, f"{i + 1}", x + 17, 136, P[c], 1, None, True)
        ptext(img, a.get("label", "PRESS START TO SWITCH"), 90, 164, P['yel'], 1, P['blk'], True)
    elif name == "hoop":           # basketball shot / dunk
        d.rectangle([150, 70, 156, 196], fill=P['lgry']); box(img, 120, 74, 152, 104, P['wht'], P['red'])
        d.rectangle([128, 104, 146, 106], fill=P['org'])
        for i in range(4): d.line([129 + i * 5, 106, 131 + i * 4, 120], fill=P['wht'])
        k = (lt * 0.7) % 1
        if a.get("dunk"):
            px_ = 20 + k * 96; py = 140 - math.sin(k * math.pi) * 54
            paste(img, person(a.get("col", "lgrn"), 'blk', 'wht'), px_, py, scale=3)
            d.ellipse([px_ + 30, py - 6, px_ + 42, py + 6], fill=P['org'], outline=P['brn'])
        else:
            paste(img, person(a.get("col", "lgrn"), 'blk', 'wht'), 20, 140, scale=3)
            bx = 50 + k * 86; by = 136 - math.sin(k * math.pi) * 70 + k * -30
            d.ellipse([bx - 6, by - 6, bx + 6, by + 6], fill=P['org'], outline=P['brn'])
            if a.get("corner"): ptext(img, "3 PTS", 44, 112, P['yel'], 1, P['blk'], True)
    elif name == "speech":         # a talking TV
        d.rounded_rectangle([44, 122, 136, 190], 8, fill=P['brn']); d.rectangle([52, 130, 114, 182], fill=P['blu'])
        d.ellipse([120, 136, 130, 146], fill=P['gry']); d.ellipse([120, 152, 130, 162], fill=P['gry'])
        for i in range(3):
            if int(t * 6) % 3 >= i: d.arc([108 + i * 8, 140 - i * 6, 128 + i * 10, 170 + i * 6], 300, 60, fill=P['yel'], width=1)
        if lt > 0.4: bubble(img, 12, 66, 168, 110, a.get("text", "HELLO!"), "yel", (80, 122), 2)
    elif name == "daynight":       # day turns to night
        k = min(1, lt / a.get("dur", 2.2))
        sun_y = 80 + k * 130; moon_y = 210 - k * 130
        ov = Image.new("RGBA", (W, 200), P['navy'] + (int(190 * k),)); img.alpha_composite(ov, (0, 0))
        if sun_y < 166: d.ellipse([34, sun_y, 62, sun_y + 28], fill=P['yel'])
        if moon_y < 166:
            d.ellipse([118, moon_y, 146, moon_y + 28], fill=P['lyel']); d.ellipse([126, moon_y - 2, 150, moon_y + 22], fill=P['navy'])
        d.rectangle([0, 196, W, 200], fill=P['brn'])
        paste(img, person('brn', 'brn', 'brn'), 78, 148, scale=4)
        if k >= 1:
            for i in range(2):
                gx = (10 + i * 120 + math.sin(t * 2 + i) * 8); paste(img, GHOST, gx, 150 + math.sin(t * 3 + i) * 5, scale=4)
    elif name == "villager":       # townsperson giving a (bad) hint
        paste(img, person('pur', 'gry', 'brn'), 30, 140, scale=4)
        paste(img, person('brn', 'brn', 'brn', flip=True), 110, 140, scale=4)
        bubble(img, 8, 66, 172, 124, a.get("text", "..."), a.get("col", "wht"), (54, 138), 1)
        if a.get("lie") and lt > 1.6:
            ptext(img, a.get("stamp", "A LIE!"), 126, 128, P['red'], 2, P['wht'], True)
    elif name == "graves":         # three endings
        labels = a.get("items", ["ENDING 1", "ENDING 2", "ENDING 3"])
        for i, lab in enumerate(labels):
            if lt > 0.3 + i * 0.6:
                x = 10 + i * 58
                d.rounded_rectangle([x, 96, x + 46, 170], 14, fill=P['gry']); d.rectangle([x, 150, x + 46, 170], fill=P['gry'])
                d.line([x + 23, 108, x + 23, 132], fill=P['dgry'], width=2); d.line([x + 14, 116, x + 32, 116], fill=P['dgry'], width=2)
                ptext(img, lab, x + 23, 176, P['wht'] if i < len(labels) - 1 else P['yel'], 1, P['blk'], True)
    elif name == "pogo":           # bouncing on a cane like a pogo stick
        k = (lt * 0.5) % 1; x = 10 + k * 150; hop = abs(math.sin(lt * 5)) * 40
        y = 150 - hop
        paste(img, person('blu', 'gry', 'red'), x - 12, y - 16, scale=3)
        d.line([x + 6, y + 20, x + 6, y + 44], fill=P['brn'], width=2); d.arc([x + 6, y + 12, x + 14, y + 22], 180, 360, fill=P['brn'], width=2)
        for i in range(3):
            ex = 40 + i * 50; squash = abs(x - ex) < 12 and hop < 12
            d.rectangle([ex - 8, 196 - (5 if squash else 12), ex + 8, 196], fill=P['grn']); d.rectangle([ex - 5, 196 - (4 if squash else 10), ex - 2, 196 - (2 if squash else 7)], fill=P['wht'])
        if hop < 6: ptext(img, "BOING!", x + 6, y - 30, P['yel'], 1, P['blk'], True)
    elif name == "gems":           # treasure pile + money counter
        k = ease(min(1, lt / 2.0)); v = int(a.get("n", 10000000) * k)
        ptext(img, "$" + f"{v:,}", 90, 72, P['lgrn'], 2, P['blk'], True)
        for i in range(int(k * 18)):
            x = 30 + (i * 23) % 120; y = 180 - (i // 6) * 14 - (i * 7) % 6
            c = [P['cyn'], P['red'], P['yel'], P['pnk']][i % 4]
            d.polygon([(x, y - 6), (x + 6, y), (x, y + 6), (x - 6, y)], fill=c); d.line([x - 3, y - 1, x, y - 4], fill=P['wht'])
    elif name == "team":           # dev team at their desks (robots = the Mega Man crew)
        for i in range(a.get("n", 3)):
            x = 16 + i * 54
            paste(img, E.ROBOT, x + 6, 112 + int(math.sin(t * 5 + i) * 2), scale=3)
            box(img, x, 150, x + 46, 176, P['beige'], P['tan']); d.rectangle([x + 8, 140, x + 38, 152], fill=P['dgry']); d.rectangle([x + 10, 142, x + 36, 150], fill=P['lblu'])
        if a.get("label"): ptext(img, a["label"], 90, 184, P['yel'], 1, P['blk'], True)
    elif name == "robodog":        # robot hero + robot dog helper
        paste(img, E.ROBOT, 24, 118, scale=4)
        dx = 96 + abs(math.sin(lt * 3)) * 10; mode = int(lt / 1.3) % 3
        if mode == 1:
            d.rectangle([dx + 4, 170, dx + 40, 176], fill=P['org'])
            for i in range(3): d.rectangle([dx + 8 + i * 12, 176, dx + 12 + i * 12, 180 + (int(t * 12) + i) % 3 * 2], fill=P['yel'])
        if mode == 2:
            d.ellipse([dx - 2, 130, dx + 50, 180], outline=P['lblu']); d.rectangle([dx + 40, 150, dx + 54, 156], fill=P['lgry'])
        paste(img, DOGBOT, dx, 140 - (14 if mode == 0 and int(t * 3) % 2 else 0), scale=4)
        ptext(img, a.get("modes", ["COIL", "JET", "MARINE"])[mode], dx + 24, 100, P['yel'], 2, P['blk'], True)
    elif name == "slide":          # sliding under a low gap
        d.rectangle([70, 60, 180, 160], fill=P['gry']); d.rectangle([0, 186, W, 196], fill=P['gry'])
        for y in range(60, 160, 12): d.line([70, y, 180, y], fill=P['dgry'])
        k = (lt * 0.6) % 1; x = -20 + k * 200
        rob = E.ROBOT if x < 40 else E.ROBOT.rotate(90, expand=True, resample=Image.NEAREST)
        paste(img, rob, x, 142 if x < 40 else 162, scale=2)
        if x >= 40:
            for i in range(4): d.line([x - 6 - i * 8, 180, x - 12 - i * 8, 180], fill=P['wht'])
    elif name == "mystery":        # masked rival with scarf and shield
        y = 96 + int(math.sin(t * 3) * 3)
        paste(img, E.ROBOT, 54, y, scale=6)
        d.rectangle([66, y + 10, 114, y + 20], fill=P['blk']); d.rectangle([70, y + 13, 110, y + 16], fill=P['red'])
        for i in range(3):
            d.rectangle([114 + i * 10, y + 34 + int(math.sin(t * 6 + i) * 3), 124 + i * 10, y + 40 + int(math.sin(t * 6 + i) * 3)], fill=P['yel'])
        box(img, 30, y + 34, 56, y + 66, P['red'], P['wht'])
        if lt > 1.0: ptext(img, a.get("q", "? ? ?"), 90, 72, P['pnk'], 2, P['blk'], True)
    elif name == "pad2":           # trick on the second controller
        controller(img, 8, 150, None, "PLAYER 1"); controller(img, 100, 150, a.get("hot", "R"), "PLAYER 2")
        if int(t * 4) % 2: d.rectangle([98, 148, 172, 182], outline=P['yel'])
        j = abs(math.sin(lt * 2.2)) * (20 if lt > 0.8 else 6)
        paste(img, E.ROBOT, 78, 112 - j, scale=2)
        if lt > 0.8:
            for i in range(3): d.line([74 + i * 14, 136 - i, 74 + i * 14, 142], fill=P['wht'])
        d.rectangle([0, 134, W, 136], fill=P['gry'])
        if lt > 0.8: ptext(img, a.get("text", "SUPER JUMP!"), 90, 64, P['yel'], 2, P['red'], True)
    elif name == "knight":         # one hit and the armour is gone
        hit = lt > a.get("at", 1.6)
        k = (lt * 0.9) % 1; fx = W - k * 150; fy = 136 + math.sin(t * 6) * 4
        if not hit or lt > a.get("at", 1.6) + 1.0: paste(img, GHOST, fx, fy, scale=3)
        if not hit:
            paste(img, KNIGHT, 38, 132, scale=4)
        else:
            paste(img, person('wht', 'brn', 'red'), 38, 132, scale=4)
            f = min(1, (lt - a.get("at", 1.6)) / 0.7)
            for i, (dx, dy) in enumerate([(-30, -40), (26, -46), (-18, -60), (34, -24)]):
                x = 60 + dx * f; y = 150 + dy * f + 70 * f * f
                d.rectangle([x, y, x + 8, y + 8], fill=P['lgry'], outline=P['gry'])
            ptext(img, a.get("text", "1 HIT = NO ARMOR"), 90, 84, P['red'], 1, P['wht'], True)
        d.rectangle([0, 180, W, 182], fill=P['gry'])
    elif name == "loop":           # "do it all again" arrow loop
        cx, cy, r = 90, 128, 40
        ang = (t * 160) % 360
        d.arc([cx - r, cy - r, cx + r, cy + r], ang, ang + 300, fill=P['yel'], width=4)
        hx = cx + r * math.cos(math.radians(ang + 300)); hy = cy + r * math.sin(math.radians(ang + 300))
        d.ellipse([hx - 5, hy - 5, hx + 5, hy + 5], fill=P['red'])
        ptext(img, a.get("text", "X2"), cx, cy - 12, P['wht'], 3, P['red'], True)
    elif name == "grapple":        # swinging on a wire arm: no jumping
        for x0 in (0, 124): d.rectangle([x0, 150, x0 + 56, 196], fill=P['gry']); d.rectangle([x0, 150, x0 + 56, 154], fill=P['lgry'])
        d.rectangle([0, 62, W, 70], fill=P['gry'])
        k = (lt * 0.45) % 1; ang = math.radians(60 - 120 * (0.5 - 0.5 * math.cos(k * math.pi)))
        ax, ay = 90, 70; L = 66
        px_ = ax - math.sin(ang) * L; py = ay + math.cos(ang) * L
        d.line([ax, ay, px_ + 14, py], fill=P['lblu'], width=2); d.rectangle([ax - 3, ay - 3, ax + 3, ay + 3], fill=P['yel'])
        paste(img, person('grn', 'red', 'grn'), px_, py - 4, scale=3)
        if a.get("nojump"):
            box(img, 60, 160, 120, 190, P['blk'], P['red'])
            ptext(img, "JUMP", 90, 166, P['gry'], 1, None, True); ptext(img, "NOPE", 90, 178, P['red'], 1, None, True)
    elif name == "magazine":       # a magazine cover
        box(img, 46, 66, 134, 186, P[a.get("col", "red")], P['wht'])
        ptext(img, a.get("title", "GAME MAG"), 90, 74, P['yel'], 1, P['blk'], True)
        d.rectangle([54, 90, 126, 150], fill=P['lblu'])
        paste(img, person('grn', 'red', 'grn'), 72, 100, scale=3)
        ptext(img, a.get("issue", "ISSUE 2"), 90, 158, P['wht'], 1, None, True)
        ptext(img, a.get("line", "COVER STORY"), 90, 172, P['yel'], 1, None, True)
    elif name == "crates":         # two players, one grabs a crate (or the other player) and throws
        k = (lt * 0.5) % 1
        p1 = person('red', 'brn', 'brn'); p2 = person('blu', 'brn', 'brn', flip=True)
        paste(img, p1, 24, 150, scale=3)
        if a.get("partner"):
            x = 40 + k * 110; y = 132 - math.sin(k * math.pi) * 46
            spun = p2.rotate(-k * 720, expand=True, resample=Image.NEAREST)
            paste(img, spun, x, y, scale=3)
            if int(t * 4) % 2: ptext(img, a.get("yell", "HEY!"), min(150, x + 20), y - 12, P['yel'], 1, P['blk'], True)
        else:
            paste(img, p2, 124, 150, scale=3)
            x = 46 + k * 84; y = 136 - math.sin(k * math.pi) * 40
            box(img, x, y, x + 20, y + 20, P['tan'], P['brn']); d.line([x, y, x + 20, y + 20], fill=P['brn']); d.line([x + 20, y, x, y + 20], fill=P['brn'])
        d.rectangle([0, 186, W, 188], fill=P['brn'])
        ptext(img, "P1", 40, 136, P['red'], 1, P['blk'], True)
    elif name == "citymap":        # pick-your-route level map
        nodes = a.get("nodes", [(24, 160), (60, 120), (60, 176), (100, 96), (104, 150), (144, 120), (150, 172), (160, 80)])
        links = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 4), (3, 5), (4, 5), (4, 6), (5, 7)]
        for a_, b_ in links: d.line([nodes[a_], nodes[b_]], fill=P['lyel'], width=2)
        cur = [0, 1, 4, 5, 7][int(lt * 1.4) % 5]
        for i, (x, y) in enumerate(nodes):
            box(img, x - 7, y - 7, x + 7, y + 7, P['red'] if i == cur else P['navy'], P['wht'])
            ptext(img, chr(65 + i), x, y - 3, P['wht'], 1, None, True)
        cx, cy = nodes[cur]
        if int(t * 4) % 2: d.rectangle([cx - 10, cy - 10, cx + 10, cy + 10], outline=P['yel'])
    elif name == "award":          # trophy with custom text
        d.polygon([(66, 80), (114, 80), (108, 120), (72, 120)], fill=P['yel'])
        d.arc([54, 84, 76, 108], 90, 270, fill=P['yel'], width=3); d.arc([104, 84, 126, 108], 270, 90, fill=P['yel'], width=3)
        d.rectangle([84, 120, 96, 136], fill=P['org']); d.rectangle([70, 136, 110, 146], fill=P['brn'])
        ptext(img, a.get("n", "1"), 90, 90, P['red'], 3 if len(a.get("n", "1")) < 3 else 2, None, True)
        if int(t * 4) % 2: d.line([60, 72, 64, 76], fill=P['wht']); d.line([120, 72, 116, 76], fill=P['wht'])
        if a.get("text"): E.block(img, a["text"], 156, P['wht'], 2, 2)
    else:
        return False
    return True
