"""8-Bit Backstory NES preset (the original engine behind episodes #1-20).

usage: python3 engine/nes/engine.py episodes/nes/<file>.json [sheet | cover "HOOK TEXT"]
Normally called through engine/render.py, which picks the preset from the episode JSON.
Output folder: $NES_OUT if set, else build/out/ in the repo.
"""
import json, math, subprocess, sys, wave, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
D = os.path.dirname(os.path.abspath(__file__)) + "/"
ROOT = os.path.abspath(D + "../..") + "/"
WORK = ROOT + "build/work/nes/"
os.makedirs(WORK, exist_ok=True)
sys.path.insert(0, D)
from lib import *          # palette P, font G, ptext, text_w, sprites, sky, skyline, street, stars, box, ease, paste
import tts
import props2

FPS = 30
spec = json.load(open(sys.argv[1]))
COVER = len(sys.argv) > 2 and sys.argv[2] == "cover"
SHEET = len(sys.argv) > 2 and sys.argv[2] in ("sheet", "cover")
OUT = (os.environ.get("NES_OUT") or ROOT + "build/out").rstrip("/") + "/"
os.makedirs(OUT, exist_ok=True)
slug = spec["slug"]

# ======================= voice =======================
def build_voice():
    sr, gap = 24000, 0.2
    parts = [np.zeros(int(sr * 0.25), np.float32)]
    t, timing = 0.25, []
    for ln in spec["lines"]:
        a = tts.say(ln["say"], spec.get("voice", "am_michael"), spec.get("speed", 1.2), spec.get("pron"))
        idx = np.where(np.abs(a) > 0.01)[0]
        a = a[max(idx[0] - 200, 0): idx[-1] + 600]
        timing.append([t, t + len(a) / sr])
        parts += [a, np.zeros(int(sr * gap), np.float32)]
        t += len(a) / sr + gap
    audio = np.concatenate(parts)
    audio = audio / np.max(np.abs(audio)) * 0.9
    with wave.open(WORK + f"work_{slug}_voice.wav", "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((audio * 32767).astype(np.int16).tobytes())
    return timing

tfile = WORK + f"work_{slug}_timing.json"
if SHEET and os.path.exists(tfile):
    timing = json.load(open(tfile))
else:
    timing = build_voice()
    json.dump(timing, open(tfile, "w"))
END = timing[-1][1] + 1.0
NF = int(END * FPS)

# ======================= text helpers =======================
def fit_lines(text, max_sc=3, max_lines=3, width=W - 8):
    words = text.upper().split()
    for sc in range(max_sc, 0, -1):
        maxc = (width + sc) // (6 * sc)
        lines, cur = [], ""
        ok = True
        for w_ in words:
            if len(w_) > maxc: ok = False; break
            tst = (cur + " " + w_).strip()
            if len(tst) <= maxc: cur = tst
            else: lines.append(cur); cur = w_
        lines.append(cur)
        if ok and len(lines) <= max_lines:
            return sc, lines
    return 1, [text.upper()[:29]]

def block(img, text, y, col, max_sc=3, max_lines=3, shadow=P['blk']):
    sc, lines = fit_lines(text, max_sc, max_lines)
    for ln in lines:
        ptext(img, ln, W // 2, y, col, sc, shadow, True)
        y += 8 * sc + 2
    return y

# ======================= extra sprites (all original) =======================
def rows_sprite(rows, cmap): return sprite(rows, cmap)
SKIER = sprite([
    "....hhhh....",
    "...hhhhhh...",
    "...kwwww....",
    "....ssss....",
    "....mmmm....",
    ".g.mmmmmm.g.",
    ".g.m.mm.m.g.",
    ".g..mmmm..g.",
    ".g..pppp..g.",
    ".g..pp.pp.g.",
    "...pp...pp..",
    "...kk...kk..",
    "wwwwwwwwwwww",
    "............"], SK_MAP)
ROBOT = sprite([
    "...gggggg...",
    "..gllllllg..",
    "..glyllylg..",
    "..gllllllg..",
    "...gggggg...",
    ".o.dddddd.o.",
    "oo.drddrd.oo",
    "o..dddddd..o",
    "...dd..dd...",
    "...dd..dd...",
    "..ggg..ggg.."], {'g': P['gry'], 'l': P['lgry'], 'y': P['yel'], 'd': P['dgry'],
                        'r': P['red'], 'o': P['org']})
SHOP = sprite([
    "....kkkk....",
    "...kkkkkk...",
    "...ssssss...",
    "..wwsswwss..",
    "..wksswkss..",
    "...ssssss...",
    "...ssrrss...",
    "....ssss....",
    "..rrrrrrrr..",
    ".srrrwwrrrs.",
    ".s.rrwwrr.s.",
    "...rrrrrr...",
    "...pppppp...",
    "...pp..pp..."], {**SK_MAP, 'r': P['grn'], 'p': P['brn']})
BEE = sprite([".ww.", "ykyk", "ykyk"], {'w': P['wht'], 'y': P['yel'], 'k': P['blk']})
PERSON = lambda col: sprite([".cc.", "cccc", ".cc.", "cccc", "cccc", "c..c"], {'c': col})

# ======================= backgrounds =======================
def bg(img, name, t):
    d = ImageDraw.Draw(img)
    if name == "city":
        sky(img, P['navy'], P['mag']); stars(img, t)
        d.ellipse([112, 100, 164, 152], fill=P['org'])
        for yy in range(112, 152, 6): d.rectangle([110, yy, 166, yy + 1], fill=P['mag'])
        skyline(img, 200, P['pur'], t, 8, 1); skyline(img, 200, P['navy'], t, 20, 2)
        street(img, 200, t, 90)
    elif name == "snow":
        sky(img, P['lblu'], P['wht'])
        for i, (x, h, c) in enumerate([(-20, 90, P['lgry']), (60, 120, P['wht']), (120, 80, P['lgry'])]):
            d.polygon([(x, 200), (x + 70, 200 - h), (x + 140, 200)], fill=c)
            d.polygon([(x + 55, 200 - h + 15), (x + 70, 200 - h), (x + 85, 200 - h + 15)], fill=P['wht'])
        d.rectangle([0, 200, W, H], fill=P['wht'])
        rng = np.random.default_rng(2)
        for _ in range(60):
            x0, y0, sp = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(15, 35)
            x = int((x0 + math.sin(t + y0) * 6) % W); y = int((y0 + t * sp) % H)
            d.point([x, y], fill=P['wht']) if y < 200 else d.point([x, y], fill=P['lgry'])
    elif name in ("sky", "plain"):
        sky(img, P['blu'], P['lblu'])
        for i in range(4 if name == "sky" else 0):
            x = int((i * 60 - t * 10) % (W + 60)) - 40
            cloud(img, x, 118 + (i % 2) * 26, P['wht'])
        d.ellipse([-40, 170, 90, 260], fill=P['grn']); d.ellipse([60, 180, 220, 280], fill=P['lgrn'])
        d.rectangle([0, 200, W, H], fill=P['brn'])
        for x in range(0, W, 12): d.rectangle([x, 200, x + 10, 203], fill=P['org'])
    elif name == "space":
        d.rectangle([0, 0, W, H], fill=P['blk'])
        rng = np.random.default_rng(9)
        for _ in range(90):
            x0, y0, z = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(5, 40)
            y = int((y0 + t * z) % H)
            d.point([int(x0), y], fill=P['wht'] if z > 20 else P['gry'])
        d.ellipse([124, 232, 176, 284], fill=P['pur']); d.ellipse([132, 240, 156, 264], fill=P['pnk'])
    elif name == "lab":
        d.rectangle([0, 0, W, H], fill=P['navy'])
        for x in range(0, W, 12): d.line([x, 0, x, H], fill=P['dblu'])
        for y in range(int(t * 10) % 12, H, 12): d.line([0, y, W, y], fill=P['dblu'])
    elif name == "grid":  # neon tron-style
        d.rectangle([0, 0, W, H], fill=P['blk'])
        hz = 150
        for i in range(-10, 11):
            d.line([W // 2 + i * 8, hz, W // 2 + i * 40, H], fill=P['cyn'])
        off = (t * 30) % 20
        y = hz
        k = 0
        while y < H:
            d.line([0, int(y), W, int(y)], fill=P['pur'])
            k += 1; y = hz + (k * 6 + off * k / 8) ** 1.3
        sky(img, P['blk'], P['mag'], 0, hz)
    elif name == "park":
        sky(img, P['lblu'], P['wht'])
        halfpipe(img, t)
    elif name == "stage":
        d.rectangle([0, 0, W, H], fill=P['blk'])
        d.rectangle([0, 200, W, H], fill=P['brn'])
        for x in range(0, W, 16): d.line([x, 200, x, H], fill=P['tan'])
        d.rectangle([0, 0, W, 14], fill=P['red'])
        for x in range(0, W, 10): d.rectangle([x, 14, x + 5, 20], fill=P['yel'])
    elif name == "arcade":
        d.rectangle([0, 0, W, H], fill=P['navy'])
        for i in range(0, H, 4):
            if (i // 4) % 2: d.line([0, i, W, i], fill=P['blk'])
        d.rectangle([0, 205, W, H], fill=P['dgry'])
        for x in range(0, W, 20):
            for y in range(205, H, 20):
                if ((x + y) // 20) % 2: d.rectangle([x, y, x + 19, y + 19], fill=P['gry'])
    elif name == "desk":
        sky(img, P['dblu'], P['blu'])
        d.rectangle([0, 190, W, H], fill=P['brn']); d.rectangle([0, 190, W, 193], fill=P['tan'])
    elif props2.extra_bg(img, name, t):
        pass
    else:  # dark
        sky(img, P['dgry'], P['blk'])

def cloud(img, x, y, col):
    d = ImageDraw.Draw(img)
    d.ellipse([x, y + 6, x + 22, y + 22], fill=col); d.ellipse([x + 12, y, x + 36, y + 22], fill=col)
    d.ellipse([x + 26, y + 6, x + 48, y + 22], fill=col)

def halfpipe(img, t, cx=90, base=230, r=60):
    d = ImageDraw.Draw(img)
    for x in range(W):
        dx = abs(x - cx)
        top = base if dx <= 30 else (base - (r - math.sqrt(max(0, r * r - (dx - 30) ** 2))) if dx <= 90 else base - r)
        d.line([x, int(top), x, H], fill=P['brn']); d.point([x, int(top)], fill=P['lyel'])

# ======================= props =======================
def cart(img, x, y, label, lcol):
    d = ImageDraw.Draw(img)
    box(img, x, y, x + 40, y + 46, P['gry'], P['dgry'])
    d.rectangle([x + 4, y + 6, x + 36, y + 30], fill=lcol)
    for i in range(4): d.rectangle([x + 6, y + 36 + i * 2, x + 34, y + 36 + i * 2], fill=P['dgry'])
    sc, lines = fit_lines(label, 1, 3, 30)
    yy = y + 18 - len(lines) * 4
    for ln in lines:
        ptext(img, ln, x + 20, yy, P['wht'], 1, P['blk'], True); yy += 8

def console(img, x, y):
    d = ImageDraw.Draw(img)
    box(img, x, y, x + 90, y + 40, P['lgry'], P['gry'])
    d.rectangle([x + 4, y + 26, x + 86, y + 36], fill=P['dgry'])
    d.rectangle([x + 20, y + 4, x + 70, y + 10], fill=P['blk'])
    d.rectangle([x + 8, y + 29, x + 14, y + 33], fill=P['red'])

def computer(img, t, lt, text):
    d = ImageDraw.Draw(img); mx = 40
    box(img, mx, 80, mx + 100, 160, P['beige'], P['tan'])
    d.rectangle([mx + 8, 88, mx + 92, 148], fill=P['lblu']); d.rectangle([mx + 12, 92, mx + 88, 144], fill=P['blu'])
    d.rectangle([mx + 40, 160, mx + 60, 170], fill=P['tan'])
    box(img, mx - 10, 172, mx + 110, 188, P['beige'], P['tan'])
    for r in range(3):
        for c in range(14): d.rectangle([mx - 6 + c * 8, 175 + r * 4, mx - 1 + c * 8, 177 + r * 4], fill=P['brn'])
    shown = int(lt * 14); y = 98
    for ln in ["READY.", f"LOAD '{text}'", "RUN"]:
        ptext(img, ln[:max(0, shown)], mx + 16, y, P['lblu']); shown -= len(ln) + 2; y += 10
    if int(t * 3) % 2: d.rectangle([mx + 16, y, mx + 20, y + 6], fill=P['lblu'])

def arcade_cab(img, t, x=50, y=70, screen="sky"):
    d = ImageDraw.Draw(img)
    d.polygon([(x, y), (x + 80, y), (x + 80, y + 130), (x, y + 130)], fill=P['pur'])
    d.rectangle([x + 4, y + 4, x + 76, y + 18], fill=P['blk'])
    ptext(img, "ARCADE", x + 40, y + 8, P['yel'] if int(t * 4) % 2 else P['org'], 1, None, True)
    d.rectangle([x + 8, y + 24, x + 72, y + 74], fill=P['blk'])
    d.rectangle([x + 10, y + 26, x + 70, y + 72], fill=P['dblu'])
    # tiny attract-mode: skater zooming
    sx = x + 10 + int((t * 30) % 60)
    d.rectangle([sx, y + 60, sx + 3, y + 66], fill=P['yel'])
    d.rectangle([x + 2, y + 80, x + 78, y + 96], fill=P['dgry'])
    d.rectangle([x + 18, y + 84, x + 22, y + 90], fill=P['red']); d.ellipse([x + 16, y + 80, x + 24, y + 86], fill=P['red'])
    for i in range(3): d.ellipse([x + 40 + i * 10, y + 85, x + 46 + i * 10, y + 91], fill=[P['yel'], P['grn'], P['lblu']][i])
    d.rectangle([x + 30, y + 104, x + 50, y + 112], fill=P['blk'])
    ptext(img, "25", x + 40, y + 105, P['org'], 1, None, True)

def ramp_skater(img, t):
    ph = math.sin(t * 2.6); x = 90 + ph * 70
    y = 230 - 14 - max(0, abs(x - 90) - 30) ** 2 / 60
    y = max(y, 230 - 74 - (18 if abs(ph) > 0.97 else 0))
    paste(img, sk_stand, x - 12, y - 14, flip=math.cos(t * 2.6) < 0, scale=2)

def prop(img, t, lt, name, a):
    d = ImageDraw.Draw(img)
    if name == "none": return
    if name == "computer": computer(img, t, lt, a.get("text", "GAME"))
    elif name == "port":   # cart slides into console
        cy = 56 + min(1, max(0, (lt - 0.4) / 1.0)) * 46
        cart(img, 70, int(cy), a.get("label", "GAME"), P[a.get("col", "red")]); console(img, 45, 140)
    elif name == "limit":
        n = min(6, int(lt * 3.2) + 1)
        for i in range(n):
            x = 12 + (i % 3) * 54; y = 70 + (i // 3) * 58; big = i == 5
            cart(img, x, y, "ULTRA" if big and lt > 2.0 else "KONAMI", P['org'] if big else P['blu'])
            if big and lt < 2.0:
                d.line([x, y, x + 40, y + 46], fill=P['red'], width=3); d.line([x + 40, y, x, y + 46], fill=P['red'], width=3)
    elif name == "list":
        items = a["items"]
        for i, e in enumerate(items):
            if lt > 0.3 + i * a.get("gap", 0.55):
                y0 = 72 + i * 16
                box(img, 8, y0 - 3, W - 8, y0 + 10, P['navy'], P['lblu'])
                ptext(img, f"{i+1}.{e}"[:28], 13, y0, P['wht'], 1)
    elif name == "joust":
        foes = [("POSER PETE", pete), ("AGGRO EDDIE", eddie), ("LESTER", lester)]
        idx = min(2, int(lt / 1.0)); nm, spr = foes[idx]; sc = 3 if idx == 2 else 2
        d.ellipse([10, 140, 170, 250], fill=P['lblu']); d.ellipse([18, 146, 162, 240], fill=P['cyn'])
        d.rectangle([10, 138, 170, 142], fill=P['wht'])
        x = 26 + math.sin(t * 3) * 4
        paste(img, sk_stand, x, 170, scale=2); paste(img, spr, 150 - 12 * sc, 198 - 14 * sc, flip=True, scale=sc)
        d.line([x + 20, 186, x + 50, 176], fill=P['brn'], width=2)
        ptext(img, "VS", W // 2, 76, P['red'], 3, P['wht'], True)
        ptext(img, nm, W // 2, 104, P['yel'] if idx == 2 else P['wht'], 2, P['blk'], True)
    elif name == "adventure":  # skater with paintball splats around town
        skyline(img, 190, P['pur'], t, 10, 3)
        d.rectangle([0, 190, W, 200], fill=P['lgry'])
        x = 30 + (lt * 25) % 120
        paste(img, sk_stand, x, 162, scale=2)
        for i in range(int(lt * 3)):
            sx, sy = (37 * i + 20) % 160 + 10, 90 + (53 * i) % 80
            c = [P['pnk'], P['lgrn'], P['yel'], P['cyn']][i % 4]
            d.ellipse([sx - 5, sy - 5, sx + 5, sy + 5], fill=c)
            for k in range(4): d.point([sx + int(8 * math.cos(k * 1.6 + i)), sy + int(8 * math.sin(k * 1.6 + i))], fill=c)
    elif name == "weapons":
        items = [("PAINTBALLS", P['pnk']), ("EGGS", P['wht']), ("FIRECRACKERS", P['red'])]
        for i, (nm, c) in enumerate(items):
            if lt > 0.3 + i * 0.6:
                y0 = 80 + i * 36
                box(img, 10, y0, W - 10, y0 + 28, P['blk'], c)
                if i == 0: d.ellipse([18, y0 + 8, 30, y0 + 20], fill=c)
                elif i == 1: d.ellipse([19, y0 + 6, 29, y0 + 22], fill=c)
                else:
                    d.rectangle([20, y0 + 6, 26, y0 + 22], fill=c)
                    if int(t * 8) % 2: d.point([23, y0 + 3], fill=P['yel'])
                ptext(img, nm, 38, y0 + 10, c, 2 if len(nm) < 11 else 1, None)
    elif name == "halfpipe":
        halfpipe(img, t); ramp_skater(img, t)
        if a.get("sign"):
            box(img, 40, 70, 140, 96, P['red'], P['yel'])
            ptext(img, a["sign"], 90, 79, P['wht'], 1, P['blk'], True)
    elif name == "shop":
        box(img, 20, 70, 160, 190, P['beige'], P['brn'])
        d.rectangle([20, 70, 160, 86], fill=P['red'])
        ptext(img, a.get("sign", "SKATE SHOP"), 90, 75, P['wht'], 1, None, True)
        for i in range(4):
            d.rectangle([30 + i * 34, 94, 32 + i * 34, 130], fill=P['brn'])
            d.rectangle([28 + i * 34, 94, 50 + i * 34, 97], fill=[P['red'], P['blu'], P['grn'], P['yel']][i])
        paste(img, SHOP, 66, 140 + int(math.sin(t * 4) * 1), scale=2) if lt % 1 < 0.9 else paste(img, SHOP, 66, 139, scale=2)
        if a.get("son"): paste(img, lester, 120, 162, scale=2)
    elif name == "arcade": arcade_cab(img, t)
    elif name == "spin":
        # skater spinning twice in the air: counter 0->720
        k = min(1, lt / 2.2); ang = 720 * k
        y = 170 - math.sin(k * math.pi) * 60
        spr = sk_stand.resize((24, 28), Image.NEAREST).rotate(-ang, expand=True, resample=Image.NEAREST)
        img.alpha_composite(spr, (int(90 - spr.width / 2), int(y - spr.height / 2)))
        d.rectangle([0, 196, W, 200], fill=P['lgry'])
        ptext(img, f"{int(ang)}", W // 2, 100 if y > 130 else 175, P['yel'], 3, P['red'], True)
    elif name == "bees":
        x = 150 - (lt * 40) % 180
        paste(img, sk_stand, x, 162, scale=2)
        for i in range(9):
            bx = x + 28 + i * 7 + math.sin(t * 9 + i) * 4
            by = 150 + math.cos(t * 7 + i * 1.3) * 18
            paste(img, BEE, bx, by, scale=2)
        if int(t * 4) % 2:
            box(img, 18, 80, 162, 112, P['red'], P['yel'])
            ptext(img, "SKATE OR DIE!", W // 2, 89, P['wht'], 2, P['blk'], True)
    elif name == "skier":
        d.polygon([(0, 110), (W, 200), (W, 210), (0, 120)], fill=P['wht'])
        k = (lt * 0.4) % 1
        x, y = k * 180 - 20, 110 + k * 90 - 28
        spr = SKIER.rotate(-27, expand=True, resample=Image.NEAREST)
        paste(img, spr, x, y, scale=2)
        for i in range(10):
            d.point([int(x - i * 4), int(y + 24 - i * 2)], fill=P['lgry'])
    elif name == "snowballs":
        paste(img, SKIER, 20, 158, scale=2); paste(img, pete, 128, 158, flip=True, scale=2)
        for i in range(4):
            k = ((lt * 1.2) + i * 0.25) % 1
            x = 44 + k * 84; y = 160 - math.sin(k * math.pi) * 40
            d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=P['wht'], outline=P['lgry'])
    elif name == "players":
        n = min(6, int(lt * 3) + 1)
        cols = [P['red'], P['blu'], P['grn'], P['yel'], P['pnk'], P['org']]
        for i in range(n):
            x = 14 + (i % 3) * 56; y = 80 + (i // 3) * 58
            paste(img, PERSON(cols[i]), x + 12, y, scale=4)
            ptext(img, f"P{i+1}", x + 20, y + 28, P['wht'], 1, P['blk'], True)
    elif name == "notes":
        for i in range(8):
            x = (i * 27 + t * 20) % (W + 20) - 10; y = 110 + math.sin(t * 3 + i) * 30
            c = [P['yel'], P['cyn'], P['pnk'], P['lgrn']][i % 4]
            d.ellipse([x, y + 8, x + 7, y + 13], fill=c); d.rectangle([x + 6, y - 4, x + 7, y + 10], fill=c)
            d.rectangle([x + 6, y - 4, x + 11, y - 2], fill=c)
        d.rectangle([60, 150, 120, 190], fill=P['dgry'])
        for i in range(7): d.rectangle([62 + i * 8, 152, 67 + i * 8, 188], fill=P['wht'])
        for i in range(6): d.rectangle([67 + i * 8, 152, 70 + i * 8, 172], fill=P['blk']) if i != 2 else None
    elif name == "cloudbush":
        k = ease(min(1, max(0, (lt - 0.8) / 1.6)))
        col = tuple(int(P['wht'][j] + (P['lgrn'][j] - P['wht'][j]) * k) for j in range(3))
        cloud(img, 20, 80, P['wht'])
        cloud(img, 110, int(80 + k * 100), col)
        d.rectangle([0, 200, W, H], fill=P['brn'])
        ptext(img, "=", W // 2, 90, P['yel'], 3, P['blk'], True)
    elif name == "minus":
        d.rectangle([0, 60, W, 200], fill=P['dblu'])
        for x in range(0, W, 2):
            y = 64 + math.sin(x / 8 + t * 3) * 3; d.point([x, int(y)], fill=P['lblu'])
        for i in range(5):
            bx = (i * 40 + 10) % W; by = 190 - ((t * 25 + i * 30) % 120)
            d.ellipse([bx, by, bx + 4, by + 4], outline=P['lblu'])
        ptext(img, "WORLD -1", W // 2, 110, P['wht'], 3, P['blk'], True)
        ang = (t * 180) % 360
        d.arc([70, 140, 110, 180], ang, ang + 290, fill=P['yel'], width=3)
    elif name == "crown":
        k = min(1, lt / 1.5)
        box(img, 30, 90, 150, 140, P['blk'], P['wht'])
        ptext(img, "LIVES X", 40, 111, P['wht'], 1)
        n = int(k * 12) if k < 1 else 10
        if lt > 1.7:
            d.polygon([(100, 122), (100, 104), (107, 112), (113, 100), (119, 112), (126, 104), (126, 122)], fill=P['yel'])
            d.rectangle([100, 122, 126, 126], fill=P['org'])
        else:
            ptext(img, str(n), 100, 108, P['wht'], 2)
    elif name == "sales":
        target = a["n"]; k = ease(min(1, lt / 1.8)); v = target * k
        ptext(img, (f"{v:.1f}" if target < 10 else f"{int(v)}"), W // 2, 90, P['yel'], 5, P['red'], True)
        ptext(img, a.get("unit", "MILLION"), W // 2, 136, P['wht'], 2, P['blk'], True)
        for i in range(int(k * 14)):
            cx, cy = 12 + (i % 7) * 24, 170 + (i // 7) * 12
            d.ellipse([cx, cy, cx + 10, cy + 10], fill=P['yel'], outline=P['org'])
    elif name == "swap":
        lab = a["to"] if lt > a.get("at", 1.8) else a["frm"]
        col = P[a.get("tocol", "red")] if lt > a.get("at", 1.8) else P[a.get("frmcol", "pnk")]
        sq = 1 - abs(math.sin(min(1, max(0, (lt - a.get("at", 1.8) + 0.3) / 0.6)) * math.pi))
        c = Image.new("RGBA", (41, 47), (0, 0, 0, 0))
        tmp = Image.new("RGBA", (W, H), (0, 0, 0, 0)); cart(tmp, 70, 80, lab, col)
        piece = tmp.crop((70, 80, 111, 127)).resize((max(2, int(41 * sq * 2)), 94), Image.NEAREST)
        img.alpha_composite(piece, (int(90 - piece.width / 2), 80))
    elif name == "heights":
        k = ease(min(1, lt / 1.2))
        a1 = PERSON(P['lgry']).resize((16, 24), Image.NEAREST); a2 = PERSON(P['gry']).resize((16, int(24 + 12 * k)), Image.NEAREST)
        paste(img, a1, 44, 190 - 24 * 3, scale=3); paste(img, a2, 100, 190 - a2.height * 3, scale=3)
        d.rectangle([0, 190, W, 193], fill=P['wht'])
        for y in range(110, 190, 10): d.line([22, y, 30, y], fill=P['yel'])
    elif name == "dream":
        d.rectangle([30, 160, 150, 190], fill=P['red']); d.rectangle([30, 150, 60, 170], fill=P['wht'])
        d.rectangle([26, 140, 32, 195], fill=P['brn']); d.rectangle([148, 155, 154, 195], fill=P['brn'])
        for i in range(3):
            if (t * 2 + i) % 3 < 2: ptext(img, "Z", 60 + i * 14, 132 - i * 12, P['wht'], 1 + i % 2)
        cloud(img, 90, 76, P['wht']); d.ellipse([84, 110, 92, 118], fill=P['wht']); d.ellipse([74, 122, 80, 128], fill=P['wht'])
        ptext(img, "?", 114, 84, P['pur'], 2)
    elif name == "curtain":
        k = ease(min(1, lt / 1.6)); w = int(92 * (1 - k))
        d.rectangle([20, 60, 160, 190], fill=P['lblu'])
        cloud(img, 60, 100, P['wht'])
        for side in (0, 1):
            x0 = 0 if side == 0 else W - w - 2
            d.rectangle([x0, 20, x0 + w + 2, 200], fill=P['red'])
            for x in range(x0, x0 + w + 2, 6): d.line([x, 20, x, 200], fill=P['mag'])
        d.rectangle([0, 20, W, 30], fill=P['mag'])
        for x in range(40, 150, 30): d.line([x, 30, x, 60 + (x % 20)], fill=P['lgry'])
    elif name == "film":
        d.rectangle([40, 90, 140, 170], fill=P['blk'], outline=P['wht'])
        ang = -20 if int(lt * 2) % 2 == 0 and lt < 1.5 else 0
        top = Image.new("RGBA", (100, 14), P['wht'] + (255,))
        td = ImageDraw.Draw(top)
        for x in range(0, 100, 14): td.polygon([(x, 0), (x + 7, 0), (x + 14, 14), (x + 7, 14)], fill=P['blk'] + (255,))
        top = top.rotate(ang, expand=True, center=(0, 14))
        img.alpha_composite(top, (40, 74))
        ptext(img, a.get("t1", "THE WIZARD"), 90, 112, P['wht'], 1, None, True)
        ptext(img, a.get("t2", "1989"), 90, 130, P['yel'], 2, None, True)
    elif name == "sketch":
        d.rectangle([35, 70, 145, 190], fill=P['wht'])
        for y in range(80, 190, 8): d.line([35, y, 145, y], fill=P['lblu'])
        d.line([44, 70, 44, 190], fill=P['red'])
        # doodle: body w/ 4 legs + head
        k = min(1, lt / 2)
        pts = [(70, 150), (120, 150), (120, 130), (70, 130), (70, 150)]
        for i in range(int(k * 4)): d.line([pts[i], pts[i + 1]], fill=P['blk'], width=2)
        if k > 0.5:
            for x in (74, 84, 106, 116): d.line([x, 150, x, 172], fill=P['blk'], width=2)
            d.line([70, 130, 64, 108], fill=P['blk'], width=2); d.ellipse([56, 94, 72, 110], outline=P['blk'], width=2)
        if lt > 2.2: ptext(img, "CENTAUR?!", 90, 76, P['red'], 2, None, True)
    elif name == "boxart":
        box(img, 45, 70, 135, 190, P['yel'], P['wht'])
        d.rectangle([52, 78, 128, 150], fill=P['pnk'])
        d.polygon([(80, 150), (86, 110), (96, 110), (102, 150)], fill=P['blu'])
        d.ellipse([84, 96, 98, 112], fill=P['skin']); d.rectangle([96, 118, 116, 122], fill=P['gry'])
        ptext(img, "??? MAN", 90, 160, P['blk'], 2, None, True)
        if lt > 1.5:
            ptext(img, "NOT IN GAME!", W // 2, 124, P['red'], 2, P['wht'], True)
    elif name == "rocknroll":
        paste(img, ROBOT, 30, 110, scale=3); paste(img, ROBOT, 114, 116, scale=3, flip=True)
        ptext(img, "ROCK", 48, 90, P['lblu'], 2, P['blk'], True); ptext(img, "ROLL", 132, 96, P['pnk'], 2, P['blk'], True)
        ptext(img, "+", 90, 140, P['yel'], 3, P['blk'], True)
    elif name == "robot":
        paste(img, ROBOT, 54, 90 + int(abs(math.sin(t * 4)) * -6), scale=6)
        if a.get("rename") and lt > 1.2:
            ptext(img, "ROCKMAN", 90, 72, P['gry'], 2, None, True); d.line([45, 76, 135, 76], fill=P['red'], width=2)
            ptext(img, "MEGA MAN", 90, 72 - 18, P['yel'], 2, P['blk'], True) if lt > 1.8 else None
    elif name == "mail":
        n = int(min(8370, 8370 * ease(min(1, lt / 2.5))))
        for i in range(min(28, n // 250)):
            x, y = 20 + (i * 37) % 140, 186 - (i // 7) * 9
            d.rectangle([x, y, x + 18, y + 8], fill=P['wht'], outline=P['gry']); d.line([x, y, x + 9, y + 5, x + 18, y], fill=P['gry'])
        k = (lt * 1.5) % 1
        d.rectangle([10 + k * 150, 128 + k * 20, 28 + k * 150, 136 + k * 20], fill=P['wht'])
        ptext(img, f"{n:,}", W // 2, 70, P['yel'], 4, P['red'], True)
        ptext(img, "DESIGNS", W // 2, 104, P['wht'], 2, P['blk'], True)
    elif name == "difficulty":
        sel = 0 if int(lt * 1.5) % 2 else 1
        for i, (nm, c) in enumerate([("NORMAL", P['lgrn']), ("DIFFICULT", P['red'])]):
            y0 = 90 + i * 40
            box(img, 20, y0, 160, y0 + 30, P['blk'], c if sel == i else P['gry'])
            ptext(img, nm, 90, y0 + 9, c if sel == i else P['gry'], 2, None, True)
        if lt > 1.0: ptext(img, "NEW IN THE USA!", W // 2, 176, P['yel'], 1, P['blk'], True)
    elif name == "clock":
        d.ellipse([50, 80, 130, 160], fill=P['wht'], outline=P['gry'], width=3)
        ang = t * 8
        d.line([90, 120, 90 + 30 * math.sin(ang), 120 - 30 * math.cos(ang)], fill=P['blk'], width=2)
        d.line([90, 120, 90 + 18 * math.sin(ang / 12), 120 - 18 * math.cos(ang / 12)], fill=P['red'], width=3)
        ptext(img, "20 HR DAYS", W // 2, 172, P['yel'], 2, P['blk'], True)
        paste(img, ROBOT, 140, 136, scale=2)
    elif name == "bricks":
        cols = [P['red'], P['yel'], P['lblu'], P['pnk'], P['lgrn'], P['org']]
        # simple self-playing brick breaker
        bxp = 90 + math.sin(t * 2.2) * 70; byp = 90 + abs(math.sin(t * 3.1)) * 90
        for r in range(6):
            for c in range(10):
                x, y = 6 + c * 17, 70 + r * 8
                gone = ((r * 10 + c) * 7919) % 97 < lt * 12
                if not gone: d.rectangle([x, y, x + 15, y + 6], fill=cols[r]); d.line([x, y + 6, x + 15, y + 6], fill=P['dgry'])
        px = bxp - 16
        d.rounded_rectangle([px, 190, px + 32, 196], 3, fill=P['lgry']); d.rectangle([px, 190, px + 4, 196], fill=P['red']); d.rectangle([px + 28, 190, px + 32, 196], fill=P['red'])
        d.ellipse([bxp - 2, 186 - byp + 90 - 3, bxp + 2, 186 - byp + 90 + 1], fill=P['wht'])
    elif name == "ship":
        k = min(1, lt / 2.0)
        d.ellipse([10, 60, 110, 110], fill=P['gry']); d.rectangle([30, 76, 100, 92], fill=P['dgry'])
        for i in range(4):
            if int(t * 6 + i) % 2: d.ellipse([20 + i * 20, 70 + (i % 2) * 20, 30 + i * 20, 80 + (i % 2) * 20], fill=P['org'])
        x, y = 60 + k * 70, 100 + k * 80
        d.rounded_rectangle([x - 16, y, x + 16, y + 6], 3, fill=P['lgry']); d.rectangle([x - 16, y, x - 12, y + 6], fill=P['red']); d.rectangle([x + 12, y, x + 16, y + 6], fill=P['red'])
        for i in range(3): d.point([int(x - i * 5 - 18), int(y + 3 - i * 5)], fill=P['cyn'])
        ptext(img, "VAUS", x, y + 12, P['cyn'], 1, None, True)
    elif name == "doh":
        r = 40 + math.sin(t * 2) * 3
        d.ellipse([90 - r, 130 - r, 90 + r, 130 + r], fill=P['mag'])
        d.ellipse([90 - r + 8, 130 - r + 8, 90 + r - 8, 130 + r - 8], fill=P['pur'])
        for ex in (74, 106): d.rectangle([ex - 6, 118, ex + 6, 124], fill=P['red'] if int(t * 3) % 2 else P['yel'])
        ptext(img, "? ? ?", 90, 140, P['pnk'], 1, None, True)
    elif name == "knob":
        box(img, 30, 100, 150, 170, P['lgry'], P['gry'])
        ang = t * 3
        d.ellipse([60, 110, 110, 160], fill=P['dgry']); d.ellipse([66, 116, 104, 154], fill=P['gry'])
        d.line([85, 135, 85 + 16 * math.cos(ang), 135 + 16 * math.sin(ang)], fill=P['red'], width=3)
        d.ellipse([122, 140, 138, 156], fill=P['red'])
        d.line([150, 135, 175, 110], fill=P['blk'], width=2)
    elif name == "tron":
        pass
    elif name == "sprite":
        spr = {"skater": sk_stand, "skier": SKIER, "robot": ROBOT, "lester": lester}[a["who"]]
        paste(img, spr, 90 - 6 * a.get("sc", 4), 110 + int(math.sin(t * 4) * 2), scale=a.get("sc", 4))
    else:
        props2.extra_prop(img, t, lt, name, a)

# ======================= scenes =======================
def scene(img, t, lt, sc, i):
    kind = sc.get("kind", "card")
    bg(img, sc.get("bg", spec["theme"]), t)
    if kind == "title":
        box(img, 22, 8, 158, 24, P['blk'], P['yel'])
        ptext(img, f"8-BIT BACKSTORY #{spec['num']}", W // 2, 13, P['yel'], 1, None, True)
        prop(img, t, lt, sc.get("prop", "none"), sc.get("args", {}))
        box(img, 22, 8, 158, 24, P['blk'], P['yel'])
        ptext(img, f"8-BIT BACKSTORY #{spec['num']}", W // 2, 13, P['yel'], 1, None, True)
        k = ease(lt / 0.5); ty = int(-40 + 74 * k)
        shake = int(2 * math.sin(lt * 40)) if lt < 0.6 else 0
        y = ty
        for j, ln in enumerate(spec["title_lines"]):
            s = min(5 if len(spec["title_lines"]) == 1 else 4, (W - 8) // (6 * len(ln)))
            ptext(img, ln, W // 2 + (shake if j % 2 else -shake), y, P['yel'] if j % 2 == 0 else P['wht'], s, P['red'], True)
            y += 8 * s + 4
        if spec.get("year_tag"):
            box(img, 60, 234, 120, 252, P['red'], P['wht'])
            ptext(img, spec["year_tag"], 90, 240, P['wht'], 1, None, True)
        return
    if kind == "outro":
        prop(img, t, lt, sc.get("prop", "none"), sc.get("args", {}))
        box(img, 8, 30, 172, 110, P['blk'], P['yel'])
        block(img, sc["question"], 44, P['wht'], 2, 3, None)
        if int(lt * 3) % 2 == 0 or lt > 1.0:
            box(img, 14, 208, 166, 250, P['red'], P['yel'])
            ptext(img, "FOLLOW FOR MORE", W // 2, 216, P['wht'], 1, None, True)
            ptext(img, "8-BIT BACKSTORY", W // 2, 232, P['yel'], 1, P['blk'], True)
        return
    # card
    prop(img, t, lt, sc.get("prop", "none"), sc.get("args", {}))
    if sc.get("head"):
        k = ease(lt / 0.35)
        block(img, sc["head"], int(-20 + 34 * k), P[sc.get("headcol", "yel")], sc.get("headsc", 3), 2, P['red'])
    y = 200
    for j, sub in enumerate(sc.get("subs", [])):
        if lt > 0.6 + j * 0.7:
            y = block(img, sub, y, P[sc.get("subcol", "wht")], 2, 1)
            y += 2

# ======================= captions =======================
FONT = ImageFont.truetype(D + "../fonts/DejaVuSans-Bold.ttf", 64)
def wrap(words, maxw):
    lines, cur = [], []
    for w_ in words:
        if FONT.getlength(" ".join(cur + [w_])) > maxw and cur: lines.append(cur); cur = [w_]
        else: cur.append(w_)
    if cur: lines.append(cur)
    return lines

def caption(frame, t):
    for (s, e), ln in zip(timing, spec["lines"]):
        if s - 0.05 <= t <= e + 0.15:
            words = ln.get("cap", ln["say"]).split()
            lens = np.array([len(w_) + 1 for w_ in words], float)
            cum = np.cumsum(lens) / lens.sum()
            cur = min(len(words) - 1, int(np.searchsorted(cum, (t - s) / (e - s))))
            chunk = cur // 4 * 4
            d = ImageDraw.Draw(frame); y = 1575; wi = chunk
            for row in wrap(words[chunk:chunk + 4], 980):
                x = (1080 - FONT.getlength(" ".join(row))) / 2
                for w_ in row:
                    d.text((x, y), w_, font=FONT, fill=(255, 214, 0) if wi == cur else (255, 255, 255),
                           stroke_width=8, stroke_fill=(0, 0, 0))
                    x += FONT.getlength(w_ + " "); wi += 1
                y += 84
            return

starts = [0.0] + [timing[i][0] - 0.1 for i in range(1, len(timing))]
def frame_at(t):
    i = max(j for j in range(len(starts)) if t >= starts[j])
    img = Image.new("RGBA", (W, H), P['blk'] + (255,))
    lt = t - starts[i]
    scene(img, t, lt, spec["lines"][i]["scene"], i)
    if lt < 0.2 and i > 0:
        d = ImageDraw.Draw(img); cov = int((1 - lt / 0.2) * 20)
        for yy in range(0, H, 20): d.rectangle([0, yy, W, yy + cov], fill=P['blk'])
    frame = img.convert("RGB").resize((W * S, H * S), Image.NEAREST)
    arr = np.asarray(frame).copy(); arr[::S] = (arr[::S] * 0.78).astype(np.uint8)
    frame = Image.fromarray(arr); caption(frame, t)
    return frame

if COVER:
    t = 2.5
    img = Image.new("RGBA", (W, H), P['blk'] + (255,))
    bg(img, spec["theme"], t)
    prop(img, t, 2.5, spec["lines"][0]["scene"].get("prop", "none"), spec["lines"][0]["scene"].get("args", {}))
    d = ImageDraw.Draw(img)
    # darken top band for title legibility
    band = Image.new("RGBA", (W, 96), (0, 0, 0, 150)); img.alpha_composite(band, (0, 0))
    box(img, 10, 8, 170, 26, P['blk'], P['yel'])
    ptext(img, "8-BIT BACKSTORY", 72, 14, P['yel'], 1, None, True)
    ptext(img, f"#{spec['num']}", 148, 13, P['red'], 1, None, True)
    y = 34
    for j, ln in enumerate(spec["title_lines"]):
        s_ = min(5 if len(spec["title_lines"]) == 1 else 4, (W - 8) // (6 * len(ln)))
        ptext(img, ln, W // 2, y, P['yel'] if j % 2 == 0 else P['wht'], s_, P['red'], True)
        y += 8 * s_ + 3
    hook = sys.argv[3] if len(sys.argv) > 3 else ""
    sc_, lines_ = fit_lines(hook, 3, 3, W - 20)
    hh = len(lines_) * (8 * sc_ + 2) + 12
    y0 = 300 - hh
    box(img, 6, y0, W - 6, 306, P['red'], P['yel'])
    yy = y0 + 7
    for ln in lines_:
        ptext(img, ln, W // 2, yy, P['wht'], sc_, P['blk'], True); yy += 8 * sc_ + 2
    frame = img.convert("RGB").resize((W * S, H * S), Image.NEAREST)
    os.makedirs(OUT + "covers", exist_ok=True)
    frame.save(OUT + f"covers/{spec['num']:02d} - {spec['name']} cover.png"); print("cover", slug); sys.exit()

if SHEET:
    ts = []
    for k, (s, e) in enumerate(timing):
        ts.append(min(e, s + 2.2))
    fr = [frame_at(t).resize((216, 384)) for t in ts]
    cols = 5; rows = (len(fr) + cols - 1) // cols
    sheet = Image.new("RGB", (216 * cols, 384 * rows))
    for k, im in enumerate(fr): sheet.paste(im, ((k % cols) * 216, (k // cols) * 384))
    sheet.save(WORK + f"sheet_{slug}.png"); print("sheet", slug); sys.exit()

vid = WORK + f"work_{slug}_video.mp4"
ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1080x1920",
                       "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "19",
                       "-pix_fmt", "yuv420p", vid], stdin=subprocess.PIPE)
for f in range(NF): ff.stdin.write(frame_at(f / FPS).tobytes())
ff.stdin.close(); ff.wait()
m = spec.get("music", {})
subprocess.run(["python3", D + "music.py", str(END), WORK + f"work_{slug}_music.wav",
                str(m.get("bpm", 150)), str(m.get("tr", 0)), str(m.get("seed", 0))], check=True)
final = OUT + spec.get("file", f"{spec['num']:02d} - {spec['name']}.mp4")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", WORK + f"work_{slug}_voice.wav",
                "-i", WORK + f"work_{slug}_music.wav", "-filter_complex",
                "[1:a]aresample=44100,apad,volume=1.6,asplit=2[vo1][vo2];[2:a]volume=0.35[mu];"
                "[mu][vo1]sidechaincompress=threshold=0.05:ratio=6:attack=20:release=300[md];"
                "[md][vo2]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[aout]",
                "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", final], check=True)
print("done", final, round(END, 1))
