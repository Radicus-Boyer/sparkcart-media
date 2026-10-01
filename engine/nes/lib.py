"""Shared pixel-art helpers: palette, 5x7 font, sprites, backgrounds."""
import math
import numpy as np
from PIL import Image, ImageDraw
W, H, S = 180, 320, 6
# ---------------- palette (NES-ish) ----------------
P = dict(blk=(0, 0, 0), wht=(252, 252, 252), gry=(124, 124, 124), lgry=(188, 188, 188),
         dgry=(60, 60, 60), red=(228, 0, 88), org=(248, 120, 88), yel=(248, 184, 0),
         lyel=(252, 224, 168), grn=(0, 184, 0), lgrn=(88, 216, 84), blu=(0, 88, 248),
         lblu=(60, 188, 252), cyn=(0, 232, 216), pur=(104, 68, 252), pnk=(248, 120, 248),
         brn=(172, 124, 0), dblu=(0, 0, 168), beige=(240, 208, 176), tan=(200, 160, 120),
         skin=(252, 188, 140), navy=(24, 16, 72), mag=(148, 0, 132))

# ---------------- 5x7 pixel font ----------------
G = {
 'A': ["01110","10001","10001","11111","10001","10001","10001"],
 'B': ["11110","10001","10001","11110","10001","10001","11110"],
 'C': ["01110","10001","10000","10000","10000","10001","01110"],
 'D': ["11110","10001","10001","10001","10001","10001","11110"],
 'E': ["11111","10000","10000","11110","10000","10000","11111"],
 'F': ["11111","10000","10000","11110","10000","10000","10000"],
 'G': ["01110","10001","10000","10111","10001","10001","01111"],
 'H': ["10001","10001","10001","11111","10001","10001","10001"],
 'I': ["01110","00100","00100","00100","00100","00100","01110"],
 'J': ["00111","00010","00010","00010","00010","10010","01100"],
 'K': ["10001","10010","10100","11000","10100","10010","10001"],
 'L': ["10000","10000","10000","10000","10000","10000","11111"],
 'M': ["10001","11011","10101","10101","10001","10001","10001"],
 'N': ["10001","11001","10101","10011","10001","10001","10001"],
 'O': ["01110","10001","10001","10001","10001","10001","01110"],
 'P': ["11110","10001","10001","11110","10000","10000","10000"],
 'Q': ["01110","10001","10001","10001","10101","10010","01101"],
 'R': ["11110","10001","10001","11110","10100","10010","10001"],
 'S': ["01111","10000","10000","01110","00001","00001","11110"],
 'T': ["11111","00100","00100","00100","00100","00100","00100"],
 'U': ["10001","10001","10001","10001","10001","10001","01110"],
 'V': ["10001","10001","10001","10001","10001","01010","00100"],
 'W': ["10001","10001","10001","10101","10101","10101","01010"],
 'X': ["10001","10001","01010","00100","01010","10001","10001"],
 'Y': ["10001","10001","01010","00100","00100","00100","00100"],
 'Z': ["11111","00001","00010","00100","01000","10000","11111"],
 '0': ["01110","10001","10011","10101","11001","10001","01110"],
 '1': ["00100","01100","00100","00100","00100","00100","01110"],
 '2': ["01110","10001","00001","00010","00100","01000","11111"],
 '3': ["11111","00010","00100","00010","00001","10001","01110"],
 '4': ["00010","00110","01010","10010","11111","00010","00010"],
 '5': ["11111","10000","11110","00001","00001","10001","01110"],
 '6': ["00110","01000","10000","11110","10001","10001","01110"],
 '7': ["11111","00001","00010","00100","01000","01000","01000"],
 '8': ["01110","10001","10001","01110","10001","10001","01110"],
 '9': ["01110","10001","10001","01111","00001","00010","01100"],
 '!': ["00100","00100","00100","00100","00100","00000","00100"],
 '?': ["01110","10001","00001","00010","00100","00000","00100"],
 '.': ["00000","00000","00000","00000","00000","01100","01100"],
 ',': ["00000","00000","00000","00000","01100","00100","01000"],
 "'": ["00100","00100","01000","00000","00000","00000","00000"],
 ':': ["00000","01100","01100","00000","01100","01100","00000"],
 '-': ["00000","00000","00000","11111","00000","00000","00000"],
 '/': ["00001","00010","00010","00100","01000","01000","10000"],
 '#': ["01010","01010","11111","01010","11111","01010","01010"],
 '+': ["00000","00100","00100","11111","00100","00100","00000"],
 '=': ["00000","00000","11111","00000","11111","00000","00000"],
 ' ': ["00000"] * 7,
}

def text_w(s, sc=1):
    return (len(s) * 6 - 1) * sc

def ptext(img, s, x, y, col, sc=1, shadow=None, center=False):
    px = img.load()
    if center:
        x = int(x - text_w(s, sc) / 2)
    for layer in ([(1, 1, shadow)] if shadow else []) + [(0, 0, col)]:
        ox, oy, c = layer
        cx = x
        for ch in s.upper():
            g = G.get(ch, G[' '])
            for r, row in enumerate(g):
                for k, v in enumerate(row):
                    if v == '1':
                        for a in range(sc):
                            for b in range(sc):
                                X, Y = cx + k * sc + a + ox * sc, y + r * sc + b + oy * sc
                                if 0 <= X < W and 0 <= Y < H:
                                    px[X, Y] = c
            cx += 6 * sc

# ---------------- sprites (original designs) ----------------
def sprite(rows, cmap):
    h, w = len(rows), max(len(r) for r in rows)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    px = im.load()
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch in cmap:
                px[x, y] = cmap[ch] + (255,)
    return im

SK_MAP = {'k': P['blk'], 's': P['skin'], 'h': P['red'], 'c': P['yel'], 'p': P['blu'],
          'w': P['wht'], 'b': P['brn'], 'g': P['gry'], 'm': P['lblu']}
SKATER = [  # 12 wide
    "....hhhh....",
    "...hhhhhh...",
    "...kssss....",
    "....ssss....",
    "....cccc....",
    "..sccccccs..",
    "..s.cccc.s..",
    "....cccc....",
    "....pppp....",
    "....pp.pp...",
    "...pp...pp..",
    "...kk...kk..",
    ".bbbbbbbbbb.",
    "..g......g..",
]
SKATER_CROUCH = [
    "............",
    "............",
    "....hhhh....",
    "...hhhhhh...",
    "...kssss....",
    "....ssss....",
    "..scccccs...",
    "..scccccs...",
    "....pppp....",
    "...pp..pp...",
    "...kk..kk...",
    "...kk..kk...",
    ".bbbbbbbbbb.",
    "..g......g..",
]
def punk(hair, shirt, pants=P['dgry']):
    m = dict(SK_MAP); m['h'] = hair; m['c'] = shirt; m['p'] = pants
    rows = [
        ".....hh.....",
        ".....hh.....",
        "....hhhh....",
        "...kssss....",
        "....ssss....",
        "..sccccccs..",
        "..s.cccc.s..",
        "....cccc....",
        "....pppp....",
        "....pp.pp...",
        "...pp...pp..",
        "...kk...kk..",
        ".bbbbbbbbbb.",
        "..g......g..",
    ]
    return sprite(rows, m)

sk_stand = sprite(SKATER, SK_MAP)
sk_crouch = sprite(SKATER_CROUCH, SK_MAP)
pete = punk(P['yel'], P['pnk'], P['lblu'])
eddie = punk(P['grn'], P['org'])
lester = punk(P['red'], P['blk'], P['navy'])

def paste(img, spr, x, y, flip=False, scale=1):
    if flip: spr = spr.transpose(Image.FLIP_LEFT_RIGHT)
    if scale != 1: spr = spr.resize((spr.width * scale, spr.height * scale), Image.NEAREST)
    img.alpha_composite(spr, (int(x), int(y)))

# ---------------- backgrounds ----------------
def sky(img, top, bot, y0=0, y1=None):
    d = ImageDraw.Draw(img)
    y1 = y1 or H
    bands = 8
    for i in range(bands):
        t = i / (bands - 1)
        c = tuple(int(top[j] + (bot[j] - top[j]) * t) for j in range(3))
        ya = y0 + (y1 - y0) * i // bands
        yb = y0 + (y1 - y0) * (i + 1) // bands
        d.rectangle([0, ya, W, yb], fill=c)

def skyline(img, ybase, col, t, speed=6, seed=1):
    d = ImageDraw.Draw(img)
    rng = np.random.default_rng(seed)
    blds = [(int(rng.integers(12, 26)), int(rng.integers(20, 70))) for _ in range(30)]
    total = sum(w for w, _ in blds)
    off = (t * speed) % total
    x = -off
    while x < W:
        for bw, bh in blds:
            d.rectangle([x, ybase - bh, x + bw - 2, ybase], fill=col)
            # windows
            for wy in range(ybase - bh + 4, ybase - 4, 6):
                for wx in range(int(x) + 3, int(x) + bw - 5, 5):
                    if (wx * 7 + wy * 3) % 11 < 4:
                        d.rectangle([wx, wy, wx + 1, wy + 2], fill=P['yel'])
            x += bw
            if x > W: break

def street(img, y, t, speed=60):
    d = ImageDraw.Draw(img)
    d.rectangle([0, y, W, y + 3], fill=P['lgry'])
    d.rectangle([0, y + 4, W, H], fill=P['dgry'])
    off = int(t * speed) % 24
    for x in range(-off, W, 24):
        d.rectangle([x, y + 16, x + 11, y + 17], fill=P['yel'])

def stars(img, t, seed=4):
    rng = np.random.default_rng(seed)
    px = img.load()
    for _ in range(40):
        x, y = int(rng.integers(0, W)), int(rng.integers(0, 150))
        if (int(t * 4) + x) % 5:
            px[x, y] = P['wht']

def box(img, x0, y0, x1, y1, fill, border=P['wht']):
    d = ImageDraw.Draw(img)
    d.rectangle([x0, y0, x1, y1], fill=border)
    d.rectangle([x0 + 1, y0 + 1, x1 - 1, y1 - 1], fill=fill)

def ease(x):
    x = min(max(x, 0), 1)
    return 1 - (1 - x) ** 3

