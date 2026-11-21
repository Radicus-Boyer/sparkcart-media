"""Giggle Garden engine: drawing primitives, characters (Bunny, Chick, Froggy), text overlay helpers.
Rebuilt from claude/giggle-garden-video-process.md sections 4.1-4.4. 1080x1920, RGB numpy frames."""
import math, functools
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
SH = 4; MUL = 1 << SH
FONT = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
PALETTE = [(255,99,132),(255,170,51),(80,190,255),(140,220,90),(190,120,255),(255,214,70)]
YELLOW = (255,220,60); NAVY = (40,60,140); PINK = (255,105,150); WHITE = (255,255,255)

def _p(v): return int(round(v * MUL))

def ell(img, c, ax, color, ang=0, th=-1):
    ax = (max(1, _p(ax[0])), max(1, _p(ax[1])))
    cv2.ellipse(img, (_p(c[0]), _p(c[1])), ax, ang, 0, 360, color, th if th < 0 else max(1, int(th)), cv2.LINE_AA, SH)

def arc(img, c, ax, a0, a1, color, th, ang=0):
    cv2.ellipse(img, (_p(c[0]), _p(c[1])), (max(1,_p(ax[0])), max(1,_p(ax[1]))), ang, a0, a1, color, max(1,int(th)), cv2.LINE_AA, SH)

def circ(img, c, r, color, th=-1): ell(img, c, (r, r), color, 0, th)

def poly(img, pts, color, th=-1):
    p = np.array([[_p(x), _p(y)] for x, y in pts], np.int32)
    if th < 0: cv2.fillPoly(img, [p], color, cv2.LINE_AA, SH)
    else: cv2.polylines(img, [p], True, color, int(th), cv2.LINE_AA, SH)

def line(img, a, b, color, th):
    cv2.line(img, (_p(a[0]), _p(a[1])), (_p(b[0]), _p(b[1])), color, max(1, int(th)), cv2.LINE_AA, SH)

def rect(img, x0, y0, x1, y1, color):
    cv2.rectangle(img, (int(x0), int(y0)), (int(x1), int(y1)), color, -1)

def oell(img, c, ax, fill, out, ow=6, ang=0):
    """ellipse with soft thick outline"""
    ell(img, c, (ax[0] + ow, ax[1] + ow), out, ang); ell(img, c, ax, fill, ang)

def star_pts(cx, cy, r, rot=0, n=5, inner=0.45):
    pts = []
    for i in range(n * 2):
        a = rot + math.pi * i / n - math.pi / 2
        rr = r if i % 2 == 0 else r * inner
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return pts

def heart_pts(cx, cy, r):
    pts = []
    for i in range(40):
        t = 2 * math.pi * i / 40
        x = 16 * math.sin(t) ** 3; y = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
        pts.append((cx + x * r / 17, cy - y * r / 17))
    return pts

def gradient(top, bot, h=H):
    t = np.linspace(0, 1, h)[:, None]
    col = (np.array(top)[None, :] * (1 - t) + np.array(bot)[None, :] * t)
    return np.repeat(col[:, None, :], W, axis=1).astype(np.uint8)

def blend(img, x0, y0, x1, y1, color, a):
    x0, y0, x1, y1 = max(0,int(x0)), max(0,int(y0)), min(W,int(x1)), min(H,int(y1))
    if x1 <= x0 or y1 <= y0: return
    sub = img[y0:y1, x0:x1].astype(np.float32)
    img[y0:y1, x0:x1] = (sub * (1 - a) + np.array(color, np.float32) * a).astype(np.uint8)

# ------------------------------------------------------------------ characters
class Rig:
    def __init__(self, x, y, s, sx=1., sy=1., jump=0., t=0., mouth=0., blink=False, helmet=False, umbrella=False):
        self.__dict__.update(locals()); del self.__dict__['self']
    def P(self, lx, ly):
        return (self.x + lx * self.sx * self.s, self.y - self.jump + ly * self.sy * self.s)
    def A(self, ax, ay): return (ax * self.sx * self.s, ay * self.sy * self.s)
    def T(self, v): return max(1, v * self.s)

def shadow(img, x, y, s, jump):
    k = max(0.45, 1 - jump / 220)
    ell(img, (x, y + 6), (95 * s * k, 18 * s * k), (70, 140, 70))

def eyes(img, r, xs, y, rad):
    for ex in xs:
        if r.blink:
            arc(img, r.P(ex, y), r.A(rad, rad * 0.6), 200, 340, (40,30,55), r.T(7))
        else:
            ell(img, r.P(ex, y), r.A(rad, rad * 1.1), (40,30,55))
            circ(img, r.P(ex - rad*0.3, y - rad*0.4), r.T(rad * 0.33), WHITE)
            circ(img, r.P(ex + rad*0.3, y + rad*0.3), r.T(rad * 0.16), WHITE)

def mouth(img, r, c, w, closed_col):
    if r.mouth > 0.08:
        h = 8 + 34 * r.mouth
        ell(img, r.P(*c), r.A(w * 0.8, h * 0.5 + 6), (150,30,50))
        ell(img, r.P(c[0], c[1] + h * 0.3), r.A(w * 0.45, h * 0.22 + 3), (255,140,160))
        rect_c = r.P(c[0], c[1] - h * 0.5 - 2)
        ell(img, (rect_c[0], rect_c[1] + r.T(5)), r.A(w * 0.25, 5), WHITE)
    else:
        arc(img, r.P(c[0] - w*0.3, c[1] - 4), r.A(w*0.3, 12), 10, 170, closed_col, r.T(5))
        arc(img, r.P(c[0] + w*0.3, c[1] - 4), r.A(w*0.3, 12), 10, 170, closed_col, r.T(5))

def bunny(img, r):
    out = (125,115,150); body = (252,252,255); pinkin = (255,175,195)
    wig = math.sin(r.t * 5) * 8
    for side in (-1, 1):  # ears
        ang = side * 12 + wig * side
        oell(img, r.P(side * 48, -470), r.A(30, 92), body, out, r.T(6), ang)
        ell(img, r.P(side * 48, -462), r.A(15, 66), pinkin, ang)
    arm = math.sin(r.t * 6) * 25
    for side in (-1, 1):
        oell(img, r.P(side * 108, -175), r.A(24, 52), body, out, r.T(6), side * (35 + arm))
    for side in (-1, 1):
        oell(img, r.P(side * 52, -10), r.A(48, 24), body, out, r.T(6))
    oell(img, r.P(0, -130), r.A(112, 128), body, out, r.T(6))
    ell(img, r.P(0, -105), r.A(70, 78), (255,228,236))
    oell(img, r.P(0, -315), r.A(120, 104), body, out, r.T(6))
    eyes(img, r, (-44, 44), -330, 21)
    for side in (-1, 1): ell(img, r.P(side * 80, -282), r.A(19, 11), (255,170,190))
    ell(img, r.P(0, -296), r.A(11, 8), (255,130,160))
    mouth(img, r, (0, -268), 30, out)
    if r.helmet:
        ell(img, r.P(0, -320), r.A(165, 160), (230,245,255), 0, r.T(8))
        arc(img, r.P(-60, -380), r.A(60, 50), 200, 260, WHITE, r.T(10))
    if r.umbrella:
        hx, hy = r.P(130, -170)
        line(img, (hx, hy), (hx, hy - 330 * r.s), (110,80,60), 8 * r.s)
        top = (hx, hy - 330 * r.s)
        cv2.ellipse(img, (_p(top[0]), _p(top[1])), (_p(190*r.s), _p(110*r.s)), 0, 180, 360, (255,99,132), -1, cv2.LINE_AA, SH)
        for k in range(-2, 3):
            ell(img, (top[0] + k * 76 * r.s, top[1]), (38 * r.s, 14 * r.s), (255,99,132))

def chick(img, r):
    out = (200,150,30); body = (255,224,80); orange = (255,150,40)
    for side in (-1, 1):
        line(img, r.P(side*28, -20), r.P(side*28, 0), orange, r.T(8))
        ell(img, r.P(side*34, 2), r.A(26, 10), orange)
    flap = math.sin(r.t * 9) * 30
    for side in (-1, 1):
        oell(img, r.P(side * 92, -95), r.A(26, 48), body, out, r.T(5), side * (40 + flap))
    oell(img, r.P(0, -105), r.A(98, 100), body, out, r.T(6))
    ell(img, r.P(0, -75), r.A(62, 55), (255,243,180))
    for k, a in enumerate((-25, 0, 25)):
        oell(img, r.P(a * 0.8, -215), r.A(11, 30), body, out, r.T(4), a)
    eyes(img, r, (-32, 32), -135, 15)
    for side in (-1, 1): ell(img, r.P(side*58, -105), r.A(14, 8), (255,170,150))
    if r.mouth > 0.08:
        op = 6 + 22 * r.mouth
        poly(img, [r.P(-20, -110), r.P(20, -110), r.P(0, -110 - 16)], orange)
        poly(img, [r.P(-18, -106), r.P(18, -106), r.P(0, -106 + op)], (230,110,30))
    else:
        poly(img, [r.P(-20, -108), r.P(20, -108), r.P(0, -88)], orange)

def froggy(img, r):
    out = (60,140,60); body = (110,205,90)
    for side in (-1, 1):
        oell(img, r.P(side*70, -12), r.A(50, 20), body, out, r.T(5))
    oell(img, r.P(0, -85), r.A(118, 85), body, out, r.T(6))
    ell(img, r.P(0, -60), r.A(75, 50), (190,240,150))
    for side in (-1, 1):
        oell(img, r.P(side*52, -165), r.A(40, 40), body, out, r.T(5))
        ell(img, r.P(side*52, -168), r.A(28, 28), WHITE)
        if r.blink: arc(img, r.P(side*52, -168), r.A(20, 10), 200, 340, (40,30,55), r.T(6))
        else:
            circ(img, r.P(side*52, -165), r.T(14), (40,30,55)); circ(img, r.P(side*47, -170), r.T(5), WHITE)
    for side in (-1, 1): ell(img, r.P(side*82, -95), r.A(16, 9), (255,160,160))
    if r.mouth > 0.08:
        h = 6 + 26 * r.mouth
        ell(img, r.P(0, -100 + h*0.3), r.A(48, h*0.6 + 5), (150,30,50))
        ell(img, r.P(0, -98 + h*0.6), r.A(26, h*0.25 + 3), (255,140,160))
    else:
        arc(img, r.P(0, -112), r.A(52, 22), 15, 165, out, r.T(6))

# ------------------------------------------------------------------ text
@functools.lru_cache(maxsize=64)
def font(sz): return ImageFont.truetype(FONT, int(sz))

def text_w(s, sz, stroke=0):
    b = font(sz).getbbox(s, stroke_width=stroke); return b[2] - b[0]

def draw_text(d, xy, s, sz, fill, stroke_col, stroke, anchor="mm"):
    d.text(xy, s, font=font(sz), fill=fill, stroke_width=stroke, stroke_fill=stroke_col, anchor=anchor)

def brand_tag(d):
    s = "GIGGLE GARDEN"; sz = 40
    tw = text_w(s, sz, 7); x = W / 2 - tw / 2
    for i, ch in enumerate(s):
        if ch != ' ':
            d.text((x, 72), ch, font=font(sz), fill=PALETTE[i % 6], stroke_width=7, stroke_fill=WHITE, anchor="lm")
        x += text_w(ch, sz) + (0 if ch != ' ' else 4)

def title_pill(d, title):
    sz = 54
    while text_w(title, sz) > 900 and sz > 30: sz -= 2
    tw = text_w(title, sz); x0, x1 = W/2 - tw/2 - 40, W/2 + tw/2 + 40
    d.rounded_rectangle((x0, 120, x1, 212), radius=46, fill=PINK, outline=WHITE, width=7)
    draw_text(d, (W/2, 166), title, sz, WHITE, PINK, 0)

def ease_back(x):
    x = min(max(x, 0), 1); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2

def ease_out(x):
    x = min(max(x, 0), 1); return 1 - (1 - x) ** 3
