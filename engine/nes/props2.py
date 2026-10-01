"""Extra backgrounds and props for episodes 11-20 (all original pixel art)."""
import math
import numpy as np
from PIL import Image, ImageDraw
from lib import *
import __main__ as E   # engine helpers: cart, console, fit_lines, block, cloud, PERSON, ROBOT, BEE

TCOL = ['cyn', 'yel', 'pur', 'lgrn', 'red', 'blu', 'org']
SHAPES = [[(0, 0), (1, 0), (2, 0), (3, 0)], [(0, 0), (1, 0), (0, 1), (1, 1)], [(0, 0), (1, 0), (2, 0), (1, 1)],
          [(1, 0), (2, 0), (0, 1), (1, 1)], [(0, 0), (1, 0), (1, 1), (2, 1)], [(0, 0), (0, 1), (1, 1), (2, 1)],
          [(2, 0), (0, 1), (1, 1), (2, 1)]]

def blk(d, x, y, s, col):
    d.rectangle([x, y, x + s - 1, y + s - 1], fill=P[col])
    d.line([x, y, x + s - 1, y], fill=P['wht']); d.line([x, y, x, y + s - 1], fill=P['wht'])
    d.line([x, y + s - 1, x + s - 1, y + s - 1], fill=P['dgry']); d.line([x + s - 1, y, x + s - 1, y + s - 1], fill=P['dgry'])

def well(d, t, lt, x0, y0, cols=10, rows=14, s=8, crash=False):
    d.rectangle([x0 - 3, y0, x0 + cols * s + 2, y0 + rows * s + 2], fill=P['gry'])
    d.rectangle([x0, y0, x0 + cols * s - 1, y0 + rows * s - 1], fill=P['blk'])
    rng = np.random.default_rng(5)
    stack = 3 + int(lt * 1.2) % 4
    for r in range(stack):
        gap = int(rng.integers(0, cols))
        for c in range(cols):
            if c != gap:
                blk(d, x0 + c * s, y0 + (rows - 1 - r) * s, s, TCOL[(r + c) % 7])
    k = (lt * 0.9) % 1
    sh = SHAPES[int(lt * 0.9) % 7]; col = TCOL[int(lt * 0.9) % 7]
    py = int(k * (rows - stack - 2))
    for (cx, cy) in sh:
        blk(d, x0 + (4 + cx) * s, y0 + (py + cy) * s, s, col)
    if crash:
        rng2 = np.random.default_rng(int(t * 12))
        for _ in range(40):
            x = int(rng2.integers(x0, x0 + cols * s)); y = int(rng2.integers(y0, y0 + rows * s))
            d.rectangle([x, y, x + int(rng2.integers(2, 14)), y + 2], fill=P[TCOL[int(rng2.integers(0, 7))]])

def fighter(col, hair, pants=None, flip=False):
    rows = [
        "...hhhh.....",
        "..hhhhhh....",
        "..hssss.....",
        "...ssss.....",
        "..cccccc....",
        ".scccccss...",
        ".s.cccc.ss..",
        "...cccc.....",
        "...pppp.....",
        "...pp.pp....",
        "..pp...pp...",
        "..kk...kk..."]
    spr = sprite(rows, {'h': P[hair], 's': P['skin'], 'c': P[col], 'p': P[pants or 'navy'], 'k': P['blk']})
    return spr.transpose(Image.FLIP_LEFT_RIGHT) if flip else spr

def punch_pose(col, hair, flip=False, punch=False):
    rows = [
        "...hhhh.....",
        "..hhhhhh....",
        "..hssss.....",
        "...ssss.....",
        "..cccccc....",
        ".scccccsssss" if punch else ".scccccss...",
        ".s.cccc.....",
        "...cccc.....",
        "...pppp.....",
        "..pp..pp....",
        ".pp....pp...",
        ".kk....kk..."]
    spr = sprite(rows, {'h': P[hair], 's': P['skin'], 'c': P[col], 'p': P['navy'], 'k': P['blk']})
    return spr.transpose(Image.FLIP_LEFT_RIGHT) if flip else spr

TOAD = lambda col: sprite([
    "..gggg....",
    ".gwkgwkg..",
    ".gggggggg.",
    ".gggrrgg..",
    "..gggggg..",
    "gg.bbbb.gg",
    "gg.bbbb.gg",
    "...gggg...",
    "..gg..gg..",
    ".ggg..ggg."], {'g': P[col], 'w': P['wht'], 'k': P['blk'], 'r': P['red'], 'b': P['brn']})

DUCK = sprite([
    "......kk....",
    ".....kgwk...",
    ".....kggyy..",
    "..bb..kk....",
    ".bbbbbbbb...",
    "bbwwbbbbbb..",
    ".bbbbbbbb...",
    "..bb..bb...."], {'k': P['blk'], 'g': P['grn'], 'w': P['wht'], 'y': P['org'], 'b': P['brn']})

BAT = sprite(["k.....k", "kk.k.kk", "kkkkkkk", ".k...k."], {'k': P['blk']})

def extra_bg(img, name, t):
    d = ImageDraw.Draw(img)
    if name == "castle":
        sky(img, P['navy'], P['pur'])
        stars(img, t, 11)
        d.ellipse([118, 30, 162, 74], fill=P['lyel'])
        d.rectangle([20, 120, 150, 200], fill=P['blk'])
        for x in (20, 60, 100, 138):
            d.rectangle([x, 96, x + 12, 200], fill=P['blk'])
            d.polygon([(x - 3, 96), (x + 6, 80), (x + 15, 96)], fill=P['blk'])
        for x in range(26, 146, 14):
            if (x * 7 + int(t * 2)) % 5 < 2: d.rectangle([x, 150, x + 3, 156], fill=P['yel'])
        d.rectangle([0, 200, W, H], fill=P['dgry'])
        for i in range(4):
            bx = (i * 50 + t * 30) % (W + 20) - 10; by = 60 + i * 12 + math.sin(t * 5 + i) * 6
            paste(img, BAT, bx, by)
        return True
    if name == "jungle":
        sky(img, P['grn'], P['lgrn'])
        for i in range(8):
            x = i * 26 - 10
            d.rectangle([x + 10, 90, x + 14, 200], fill=P['brn'])
            d.ellipse([x - 6, 70, x + 30, 104], fill=P['grn'])
        d.rectangle([0, 200, W, H], fill=P['brn'])
        return True
    if name == "prison":
        d.rectangle([0, 0, W, H], fill=P['dgry'])
        for y in range(0, 200, 10):
            for x in range(-(y // 10 % 2) * 10, W, 20): d.rectangle([x, y, x + 18, y + 8], fill=P['gry'])
        d.rectangle([0, 200, W, H], fill=P['blk'])
        return True
    if name == "ring":
        d.rectangle([0, 0, W, H], fill=P['blk'])
        for i in range(30):
            x = (i * 37) % W; y = 20 + (i * 53) % 70
            if (int(t * 5) + i) % 7 == 0: d.rectangle([x, y, x + 2, y + 2], fill=P['wht'])
        d.polygon([(0, 200), (W, 200), (W, H), (0, H)], fill=P['lblu'])
        for y, c in ((150, 'red'), (165, 'wht'), (180, 'blu')): d.line([0, y, W, y], fill=P[c], width=2)
        d.rectangle([0, 140, 6, 200], fill=P['lgry']); d.rectangle([W - 7, 140, W, 200], fill=P['lgry'])
        return True
    if name == "grass":
        sky(img, P['lblu'], P['wht'])
        for i in range(6):
            x = i * 34 - 10
            d.rectangle([x + 12, 120, x + 16, 180], fill=P['brn']); d.ellipse([x, 90, x + 30, 130], fill=P['grn'])
        d.rectangle([0, 170, W, H], fill=P['lgrn'])
        for x in range(0, W, 6): d.polygon([(x, 172), (x + 3, 160), (x + 6, 172)], fill=P['grn'])
        return True
    if name == "moscow":
        sky(img, P['navy'], P['dblu']); stars(img, t, 13)
        d.rectangle([0, 200, W, H], fill=P['lgry'])
        for i, (x, w_, h) in enumerate([(10, 30, 70), (48, 22, 100), (78, 34, 60), (120, 26, 90), (150, 30, 50)]):
            d.rectangle([x, 200 - h, x + w_, 200], fill=P['pur'])
            d.ellipse([x + 2, 200 - h - 14, x + w_ - 2, 200 - h + 6], fill=[P['red'], P['grn'], P['yel'], P['lblu'], P['org']][i])
            d.polygon([(x + w_ // 2 - 1, 200 - h - 22), (x + w_ // 2 + 1, 200 - h - 22), (x + w_ // 2, 200 - h - 14)], fill=P['yel'])
        for i in range(50):
            x = int((i * 23 + math.sin(t + i) * 5) % W); y = int((i * 41 + t * 20) % 200)
            d.point([x, y], fill=P['wht'])
        return True
    if name == "planet":
        d.rectangle([0, 0, W, H], fill=P['blk'])
        stars(img, t, 17)
        d.rectangle([0, 190, W, H], fill=P['brn'])
        for x in range(0, W, 16):
            d.polygon([(x, 190), (x + 8, 150 + (x * 13) % 30), (x + 16, 190)], fill=P['mag'])
        d.ellipse([130, 110, 170, 150], fill=P['org']); d.ellipse([136, 116, 160, 140], fill=P['yel'])
        return True
    return False

def extra_prop(img, t, lt, name, a):
    d = ImageDraw.Draw(img)
    if name == "blocks":
        well(d, t, lt, 50, 70, crash=a.get("crash", False) and lt > 1.5)
        if a.get("crash") and lt > 1.5 and int(t * 6) % 2:
            box(img, 30, 118, 150, 142, P['red'], P['yel']); ptext(img, "CRASH!", 90, 124, P['wht'], 2, P['blk'], True)
    elif name == "handheld":
        d.rounded_rectangle([40, 70, 140, 190], 22, fill=P['cyn'], outline=P['blu'])
        d.rectangle([54, 72, 126, 132], fill=P['dgry'])
        d.rectangle([60, 78, 120, 126], fill=(140, 172, 40))
        k = (lt * 1.2) % 1
        for i, (cx, cy) in enumerate(SHAPES[int(lt * 1.2) % 7]):
            d.rectangle([84 + cx * 5, 80 + int(k * 36) + cy * 5, 88 + cx * 5, 84 + int(k * 36) + cy * 5], fill=(40, 70, 20))
        for x in range(60, 120, 5): d.rectangle([x, 121, x + 4, 125], fill=(40, 70, 20))
        d.rectangle([60, 150, 66, 168], fill=P['dgry']); d.rectangle([54, 156, 72, 162], fill=P['dgry'])
        d.ellipse([104, 150, 114, 160], fill=P['yel']); d.ellipse([116, 144, 126, 154], fill=P['red'])
    elif name == "tennis":
        ptext(img, "TETRA", 50, 90, P['cyn'], 2, P['blk'], True); ptext(img, "+", 90, 90, P['yel'], 2, P['blk'], True)
        ptext(img, "TENNIS", 132, 90, P['lgrn'], 2, P['blk'], True)
        ptext(img, "= 4", 50, 110, P['wht'], 1, None, True)
        y = 150 + abs(math.sin(t * 4)) * -30
        d.ellipse([124, y, 140, y + 16], fill=P['lgrn']); d.arc([124, y, 140, y + 16], 300, 60, fill=P['wht'])
        for i, (cx, cy) in enumerate(SHAPES[0]): blk(d, 30 + cx * 10, 150 + cy * 10, 10, 'cyn')
    elif name == "gavel":
        box(img, 30, 160, 150, 196, P['brn'], P['tan'])
        ang = -40 if int(lt * 2) % 2 == 0 and lt < 2 else 0
        g = Image.new("RGBA", (70, 30), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
        gd.rectangle([0, 0, 24, 18], fill=P['brn'] + (255,)); gd.rectangle([24, 7, 70, 11], fill=P['tan'] + (255,))
        g = g.rotate(ang, expand=True, center=(12, 9)); img.alpha_composite(g, (60, 120))
        ptext(img, "NINTENDO", 50, 80, P['red'], 1, P['wht'], True); ptext(img, "VS", 90, 80, P['yel'], 1, None, True)
        ptext(img, "TENGEN", 130, 80, P['lblu'], 1, P['wht'], True)
        if lt > 2.2: ptext(img, "NINTENDO WINS", 90, 100, P['yel'], 1, P['red'], True)
    elif name == "goldcart":
        E.cart(img, 70, 80, a.get("label", "GAME"), P['yel'])
        for i in range(5):
            ang = t * 2 + i * 1.3; r = 34 + (i % 2) * 8
            x, y = 90 + math.cos(ang) * r, 104 + math.sin(ang) * r
            if int(t * 6 + i) % 3: d.line([x - 3, y, x + 3, y], fill=P['yel']); d.line([x, y - 3, x, y + 3], fill=P['yel'])
    elif name == "map":
        for r in range(8):
            for c in range(16):
                x, y = 10 + c * 10, 64 + r * 16
                col = P['grn'] if (r * 7 + c * 3) % 5 else P['lgrn']
                if (r, c) in [(2, 11), (2, 12), (3, 11), (3, 12), (3, 13)]: col = P['lblu']
                if (r, c) in [(5, 3), (6, 3), (5, 4)]: col = P['brn']
                d.rectangle([x, y, x + 9, y + 15], fill=col)
        path = [(1, 7), (4, 7), (4, 4), (8, 4), (8, 2), (11, 2)]
        k = min(len(path) - 1.001, lt * 1.2); i = int(k); f = k - i
        px = path[i][0] + (path[i + 1][0] - path[i][0]) * f; py = path[i][1] + (path[i + 1][1] - path[i][1]) * f
        d.rectangle([10 + px * 10 + 2, 64 + py * 16 + 4, 10 + px * 10 + 7, 64 + py * 16 + 11], fill=P['org'])
        if lt > 3.5: ptext(img, "A HIDDEN LAKE!", 90, 110, P['wht'], 1, P['blk'], True)
    elif name == "battery":
        box(img, 55, 90, 125, 170, P['dgry'], P['lgry']); d.rectangle([80, 82, 100, 90], fill=P['lgry'])
        n = min(4, int(lt * 2.5))
        for i in range(n): d.rectangle([62, 158 - i * 18, 118, 172 - i * 18 - 4], fill=P['lgrn'])
        if lt > 1.8: box(img, 40, 180, 140, 196, P['blk'], P['yel']); ptext(img, "GAME SAVED", 90, 185, P['yel'], 1, None, True)
    elif name == "dungeon":
        for r in range(4):
            for c in range(5):
                x, y = 20 + c * 29, 70 + r * 30
                lit = ((r * 5 + c) * 3) % 17 < lt * 3
                d.rectangle([x, y, x + 25, y + 26], fill=P['blu'] if lit else P['navy'], outline=P['lblu'])
        if lt > 1.5: ptext(img, "QUEST 2", 90, 124, P['yel'], 2, P['red'], True)
    elif name == "code":
        seq = ["U", "U", "D", "D", "L", "R", "L", "R", "B", "A"]
        n = min(10, int(lt * 4))
        for i in range(10):
            x, y = 12 + (i % 5) * 32, 78 + (i // 5) * 36
            box(img, x, y, x + 26, y + 28, P['yel'] if i < n else P['dgry'], P['wht'] if i < n else P['gry'])
            s = seq[i]
            if s in "UDLR":
                cx, cy = x + 13, y + 14
                pts = {"U": [(cx, cy - 7), (cx - 7, cy + 5), (cx + 7, cy + 5)], "D": [(cx, cy + 7), (cx - 7, cy - 5), (cx + 7, cy - 5)],
                       "L": [(cx - 7, cy), (cx + 5, cy - 7), (cx + 5, cy + 7)], "R": [(cx + 7, cy), (cx - 5, cy - 7), (cx - 5, cy + 7)]}[s]
                d.polygon(pts, fill=P['blk'] if i < n else P['gry'])
            else:
                ptext(img, s, x + 14, y + 8, P['red'] if i < n else P['gry'], 2, None, True)
        if lt > 2.6: ptext(img, "+ START", 90, 156, P['wht'], 2, P['blk'], True)
    elif name == "lives":
        k = ease(min(1, max(0, (lt - 0.6) / 1.4))); n = int(3 + 27 * k)
        ptext(img, f"x{n}", 90, 84, P['yel'], 5, P['red'], True)
        ptext(img, "LIVES", 90, 130, P['wht'], 2, P['blk'], True)
        for i in range(min(30, n)):
            x, y = 14 + (i % 10) * 16, 152 + (i // 10) * 14
            d.rectangle([x, y, x + 8, y + 8], fill=P['red']); d.rectangle([x + 2, y + 2, x + 6, y + 6], fill=P['org'])
    elif name == "commandos":
        paste(img, fighter('lblu', 'yel', 'grn'), 34, 120, scale=4)
        paste(img, fighter('red', 'blk', 'grn', flip=True), 98, 120, scale=4)
        for i in range(3):
            k = ((lt * 2) + i * 0.33) % 1
            d.rectangle([80 - k * 70, 150, 82 - k * 70, 151], fill=P['yel'])
            d.rectangle([100 + k * 70, 150, 102 + k * 70, 151], fill=P['yel'])
    elif name == "robotswap":
        if lt < a.get("at", 1.6):
            paste(img, fighter('lblu', 'yel', 'grn'), 60, 110, scale=5)
        else:
            paste(img, E.ROBOT, 54, 118, scale=6)
            ptext(img, "PROBOTECTOR", 90, 84, P['lblu'], 2, P['blk'], True)
    elif name == "prisonbreak":
        k = min(1, max(0, (lt - 1.0) / 0.8))
        paste(img, fighter('org', 'brn'), 70, 128, scale=4)
        for i in range(6):
            x = 30 + i * 22; bend = int(math.sin(k * math.pi / 2) * (12 if i in (2, 3) else 0)) * (-1 if i == 2 else 1)
            d.line([x, 76, x + bend, 196], fill=P['lgry'], width=4)
        d.rectangle([24, 72, 156, 78], fill=P['gry']); d.rectangle([24, 196, 156, 200], fill=P['gry'])
    elif name == "brawl":
        hit = int(lt * 3) % 2
        paste(img, punch_pose('org', 'brn', punch=hit), 30, 130, scale=4)
        paste(img, fighter('grn', 'blk', flip=True), 104 + (6 if hit else 0), 130, scale=4)
        if hit:
            ptext(img, "POW!", 118, 100, P['yel'], 2, P['red'], True)
        d.polygon([(40, 106), (60, 100), (58, 104)], fill=P['lgry'])
    elif name == "brothers":
        paste(img, punch_pose('lblu', 'brn'), 20, 124, scale=4)
        paste(img, punch_pose('red', 'brn', flip=True), 112, 124, scale=4)
        ptext(img, "BILLY", 44, 100, P['lblu'], 1, P['blk'], True); ptext(img, "JIMMY", 136, 100, P['red'], 1, P['blk'], True)
        if a.get("vs") and lt > 1.2: ptext(img, "VS", 90, 150, P['yel'], 3, P['red'], True)
    elif name == "toads":
        for i, c in enumerate(['lgrn', 'grn', 'brn']):
            paste(img, TOAD(c), 14 + i * 56, 120 + int(abs(math.sin(t * 4 + i)) * -8), scale=4)
        for i, nm in enumerate(["RASH", "ZITZ", "PIMPLE"]):
            ptext(img, nm, 34 + i * 56, 170, P['wht'], 1, P['blk'], True)
    elif name == "tunnel":
        for i in range(12):
            z = ((i + lt * 6) % 12) / 12
            r = 8 + z * z * 100
            d.rectangle([90 - r, 130 - r * 0.6, 90 + r, 130 + r * 0.6], outline=P['pur'] if i % 2 else P['blu'])
        for i in range(3):
            z = ((lt * 1.5 + i * 0.33) % 1)
            w_ = 4 + z * 40; x = 90 + (i - 1) * z * 50
            d.rectangle([x - w_ / 2, 130 - w_ / 3, x + w_ / 2, 130 + w_ / 3], fill=P['org'])
        paste(img, TOAD('lgrn'), 76, 170, scale=2)
        d.rectangle([70, 190, 110, 194], fill=P['red'])
    elif name == "trophy":
        d.polygon([(66, 80), (114, 80), (108, 120), (72, 120)], fill=P['yel'])
        d.arc([54, 84, 76, 108], 90, 270, fill=P['yel'], width=3); d.arc([104, 84, 126, 108], 270, 90, fill=P['yel'], width=3)
        d.rectangle([84, 120, 96, 136], fill=P['org']); d.rectangle([70, 136, 110, 146], fill=P['brn'])
        ptext(img, "7", 90, 90, P['red'], 3, None, True)
        if int(t * 4) % 2: d.line([60, 72, 64, 76], fill=P['wht']); d.line([120, 72, 116, 76], fill=P['wht'])
        ptext(img, "AWARDS", 90, 160, P['wht'], 2, P['blk'], True)
    elif name == "ducks":
        for i in range(2):
            x = (lt * 40 + i * 70) % 200 - 20; y = 80 + i * 30 + math.sin(t * 6 + i) * 8
            paste(img, DUCK if int(t * 6) % 2 else DUCK.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.FLIP_TOP_BOTTOM), x, y, scale=2)
    elif name == "zapper":
        phase = lt % 2.4
        if 1.0 < phase < 1.35:
            d.rectangle([0, 0, W, 200], fill=P['blk'])
            if phase > 1.18: d.rectangle([98, 84, 126, 104], fill=P['wht'])
            ptext(img, "BLACK" if phase <= 1.18 else "WHITE BOX", 90, 150, P['yel'], 1, None, True)
        else:
            paste(img, DUCK, 100, 84, scale=2)
        # generic light gun
        d.polygon([(20, 170), (70, 160), (74, 170), (40, 178), (36, 196), (24, 196)], fill=P['gry'])
        d.rectangle([68, 160, 76, 166], fill=P['dgry'])
        if 0.9 < phase < 1.1: d.line([76, 162, 108, 100], fill=P['yel'])
    elif name == "crt":
        d.rounded_rectangle([30, 76, 150, 180], 10, fill=P['brn']); d.rounded_rectangle([40, 84, 128, 170], 12, fill=P['blk'])
        d.rectangle([48, 92, 120, 162], fill=P['blu'])
        paste(img, DUCK, 70, 116, scale=2)
        d.ellipse([134, 96, 144, 106], fill=P['gry']); d.ellipse([134, 116, 144, 126], fill=P['gry'])
        d.line([60, 76, 40, 56], fill=P['gry'], width=2); d.line([100, 76, 120, 56], fill=P['gry'], width=2)
        if lt > 1.6:
            d.rectangle([30, 184, 150, 198], fill=P['blk'])
            ptext(img, "TUBE TV ONLY", 90, 188, P['yel'], 1, None, True)
    elif name == "laugh":
        for i in range(3):
            if (lt * 3 + i) % 3 < 2:
                ptext(img, "HA", 44 + i * 44, 90 + int(math.sin(t * 8 + i) * 6), P['yel'], 3, P['red'], True)
        d.rectangle([0, 170, W, 200], fill=P['lgrn'])
        for x in range(0, W, 6): d.polygon([(x, 172), (x + 3, 150), (x + 6, 172)], fill=P['grn'])
        if a.get("target") and lt > 1.5:
            d.ellipse([70, 126, 110, 166], outline=P['red'], width=2); d.line([90, 120, 90, 172], fill=P['red']); d.line([64, 146, 116, 146], fill=P['red'])
    elif name == "boxers":
        hit = int(lt * 2.5) % 2
        paste(img, punch_pose('lblu', 'brn', punch=hit), 28, 112, scale=4)
        paste(img, punch_pose('red', 'blk', flip=True), 104 + (4 if hit else 0), 112, scale=4)
        for x, c in ((28, 'red'), (84, 'red')):
            pass
        if a.get("stats"):
            box(img, 10, 66, 170, 100, P['blk'], P['wht'])
            ptext(img, "LITTLE MAC", 90, 70, P['lgrn'], 1, None, True)
            ptext(img, "AGE 17  107 LBS", 90, 84, P['wht'], 1, None, True)
    elif name == "keypad":
        code = "0073735963"
        n = min(10, int(lt * 4.5))
        shown = code[:n]
        disp = (shown[:3] + " " + shown[3:6] + " " + shown[6:]).strip()
        box(img, 20, 70, 160, 94, P['blk'], P['lgrn'])
        ptext(img, disp, 90, 78, P['lgrn'], 2, None, True)
        for i, k in enumerate("123456789 0 "):
            if k == " ": continue
            x, y = 44 + (i % 3) * 34, 102 + (i // 3) * 24
            on = shown and shown[-1] == k and int(lt * 4.5) < 11
            box(img, x, y, x + 26, y + 18, P['yel'] if on else P['dgry'], P['wht'])
            ptext(img, k, x + 13, y + 6, P['blk'] if on else P['wht'], 1, None, True)
    elif name == "nameswap":
        at = a.get("at", 1.5)
        nm = a["to"] if lt > at else a["frm"]
        col = P[a.get("tocol", "yel")] if lt > at else P[a.get("frmcol", "red")]
        box(img, 20, 96, 160, 140, P['blk'], col)
        ptext(img, a.get("label", "FINAL BOSS"), 90, 102, P['wht'], 1, None, True)
        ptext(img, nm, 90, 118, col, 2, None, True)
        if lt < at and lt > at - 0.6 and int(t * 10) % 2:
            d.line([24, 126, 156, 126], fill=P['red'], width=2)
    elif name == "suit":
        k = min(1, max(0, (lt - 1.2) / 0.8))
        # generic space suit, helmet lifts off
        d.rounded_rectangle([64, 124, 116, 190], 8, fill=P['lgry'])
        d.rectangle([56, 130, 66, 170], fill=P['lgry']); d.rectangle([114, 130, 124, 170], fill=P['lgry'])
        d.rectangle([70, 150, 110, 156], fill=P['blu'])
        hy = 86 - k * 30
        if k > 0.3:
            d.ellipse([74, 96, 106, 128], fill=P['skin'])
            d.rectangle([72, 94, 108, 104], fill=P['org'] if False else P['brn'])
            d.polygon([(72, 100), (66, 132), (76, 130)], fill=P['brn']); d.polygon([(108, 100), (114, 132), (104, 130)], fill=P['brn'])
            d.rectangle([82, 110, 85, 113], fill=P['blk']); d.rectangle([95, 110, 98, 113], fill=P['blk'])
        d.ellipse([70, hy, 110, hy + 42], fill=P['wht'], outline=P['gry']); d.ellipse([76, hy + 12, 104, hy + 28], fill=P['blu'])
        if lt > 2.2: ptext(img, "SHE'S A WOMAN!", 90, 196, P['yel'], 1, P['red'], True)
    elif name == "password":
        txt = "JUSTIN BAILEY"
        n = min(len(txt), int(lt * 6))
        box(img, 10, 80, 170, 150, P['blk'], P['lblu'])
        ptext(img, "PASSWORD", 90, 88, P['lblu'], 1, None, True)
        ptext(img, txt[:n], 90, 110, P['wht'], 2, None, True)
        for i in range(24):
            x = 16 + (i % 12) * 13; y = 132 + (i // 12) * 8
            d.rectangle([x, y, x + 8, y + 4], fill=P['dgry'] if i >= n * 2 else P['lblu'])
    elif name == "alien":
        # a generic winged space creature silhouette + film frame
        d.rectangle([28, 70, 152, 170], fill=P['blk'], outline=P['wht'])
        for y in (74, 162):
            for x in range(32, 150, 12): d.rectangle([x, y, x + 6, y + 4], fill=P['wht'])
        wing = abs(math.sin(t * 5)) * 20
        d.polygon([(90, 100), (54, 96 - wing), (70, 126)], fill=P['pur']); d.polygon([(90, 100), (126, 96 - wing), (110, 126)], fill=P['pur'])
        d.ellipse([80, 96, 100, 140], fill=P['mag']); d.rectangle([86, 104, 88, 106], fill=P['yel']); d.rectangle([92, 104, 94, 106], fill=P['yel'])
        d.line([90, 140, 96, 156], fill=P['mag'], width=3)
    elif name == "metro":
        ptext(img, "METRO", 48, 96, P['lblu'], 2, P['blk'], True); ptext(img, "+", 90, 96, P['yel'], 2, None, True)
        ptext(img, "ANDROID", 136, 96, P['lgrn'], 2, P['blk'], True)
        # floating jellyfish-like creature (generic)
        y = 140 + math.sin(t * 3) * 6
        d.polygon([(70, y + 22), (78, y), (102, y), (110, y + 22)], fill=P['pnk'])
        d.rectangle([80, y + 8, 84, y + 12], fill=P['yel']); d.rectangle([96, y + 8, 100, y + 12], fill=P['yel'])
        for i in range(4): d.line([76 + i * 9, y + 24, 74 + i * 9, y + 36 + math.sin(t * 6 + i) * 3], fill=P['wht'], width=2)
    elif name == "whip":
        hero = fighter('brn', 'brn', 'brn')
        paste(img, hero, 30, 128, scale=4)
        k = (lt * 1.5) % 1
        ext = math.sin(min(1, k * 2) * math.pi) * 100
        pts = [(70, 150)]
        for i in range(1, 12):
            f = i / 11; pts.append((70 + ext * f, 150 - math.sin(f * math.pi) * 10 * (1 - k)))
        d.line(pts, fill=P['tan'], width=2)
        if ext > 80: d.rectangle([pts[-1][0] - 2, pts[-1][1] - 2, pts[-1][0] + 2, pts[-1][1] + 2], fill=P['yel'])
    elif name == "credits":
        names = a.get("names", [])
        off = lt * 22
        for i, nm in enumerate(names):
            y = 200 - off + i * 22
            if 60 < y < 196:
                ptext(img, nm, 90, int(y), P['wht'] if i % 2 == 0 else P['lyel'], 1, P['blk'], True)
        d.rectangle([0, 56, W, 64], fill=P['blk'])
    elif name == "monsters":
        items = a["items"]
        for i, e in enumerate(items):
            if lt > 0.3 + i * 0.5:
                y0 = 70 + i * 22
                box(img, 14, y0, W - 14, y0 + 18, P['blk'], P['pur'])
                ptext(img, e, 90, y0 + 6, P['wht'], 1, None, True)
    else:
        pass
