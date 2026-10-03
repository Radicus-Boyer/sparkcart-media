"""Drawing helpers for the 'popular' preset (1080x1920, Pillow)."""
import json, math, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

W, H = 1080, 1920
D = os.path.dirname(os.path.abspath(__file__)) + "/"
FD = D + "fonts/"
ICONS = json.load(open(D + "icons.json"))
_fonts, _txt = {}, {}


def rgb(c):
    if isinstance(c, (tuple, list)):
        return tuple(c)
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def mix(a, b, k):
    a, b = rgb(a), rgb(b)
    return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))


def ease(k):
    k = max(0.0, min(1.0, k))
    return k * k * (3 - 2 * k)


def back(k):
    """overshoot ease for pop-ins"""
    k = max(0.0, min(1.0, k))
    c = 1.70158
    return 1 + (c + 1) * (k - 1) ** 3 + c * (k - 1) ** 2


def font(name, size, wght=None):
    key = (name, int(size), wght)
    if key not in _fonts:
        f = ImageFont.truetype(FD + name, int(size))
        if wght:
            try:
                f.set_variation_by_axes([wght])
            except Exception:
                pass
        _fonts[key] = f
    return _fonts[key]


def text_img(txt, fname, size, fill, stroke=0, sfill="#000000", wght=None, shadow=None, box=None, line=False, cache=True):
    """RGBA image of one line of text. shadow=(dx,dy,color). box=(fill, padx, pady) draws a solid plate behind.
    line=True uses the font's full line height so separately rendered words share a baseline."""
    key = (txt, fname, int(size), fill, stroke, sfill, wght, shadow, box, line)
    if cache and key in _txt:
        return _txt[key]
    f = font(fname, size, wght)
    stroke = int(stroke)
    l, t, r, b = f.getbbox(txt, stroke_width=stroke)
    if line:
        asc, desc = f.getmetrics()
        t, b = -stroke, asc + desc + stroke
    sx = max(abs(shadow[0]), 0) if shadow else 0
    sy = max(abs(shadow[1]), 0) if shadow else 0
    px, py = (box[1], box[2]) if box else (6, 6)
    im = Image.new("RGBA", (int(r - l + 2 * px + sx), int(b - t + 2 * py + sy)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if box:
        d.rectangle([0, 0, im.width - 1 - sx, im.height - 1 - sy], fill=rgb(box[0]) + (255,))
    if shadow:
        sc = rgb(shadow[2]) + (255,)
        d.text((px - l + shadow[0], py - t + shadow[1]), txt, font=f, fill=sc, stroke_width=stroke, stroke_fill=sc)
    d.text((px - l, py - t), txt, font=f, fill=rgb(fill) + (255,), stroke_width=stroke, stroke_fill=rgb(sfill) + (255,))
    if cache:
        if len(_txt) > 600:
            _txt.clear()
        _txt[key] = im
    return im


def icon_img(name, size, fill, stroke=0, sfill="#000000", shadow=None):
    code = ICONS.get(name)
    if not code:
        raise KeyError(f"unknown icon '{name}'")
    return text_img(chr(int(code, 16)), "fa-solid-900.ttf", size, fill, stroke, sfill, None, shadow)


def paste(img, im, cx, cy, s=1.0, anchor="c"):
    """alpha-paste RGBA sprite on the RGB frame; (cx, cy) is the centre, or the left-middle when anchor='l'."""
    if s <= 0.02:
        return
    if abs(s - 1) > 0.012:
        im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BILINEAR)
    x = int(cx) if anchor == "l" else int(cx - im.width / 2)
    img.paste(im, (x, int(cy - im.height / 2)), im)


def wrap(txt, measure, max_w):
    """greedy word wrap; measure(text) -> pixel width"""
    lines, cur = [], ""
    for w in txt.split():
        t = (cur + " " + w).strip()
        if cur and measure(t) > max_w:
            lines.append(cur)
            cur = w
        else:
            cur = t
    if cur:
        lines.append(cur)
    return lines


# ------------------------------------------------------------ backgrounds
def vgrad(c1, c2):
    a, b = np.array(rgb(c1), np.float32), np.array(rgb(c2), np.float32)
    t = np.linspace(0, 1, H)[:, None]
    g = (a * (1 - t) + b * t).astype(np.uint8)
    return Image.fromarray(np.ascontiguousarray(np.repeat(g[:, None, :], W, 1)), "RGB")


def radial(cin, cout, cx, cy, r):
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.clip(np.hypot(xx - cx, yy - cy) / r, 0, 1)[..., None]
    a, b = np.array(rgb(cin), np.float32), np.array(rgb(cout), np.float32)
    return Image.fromarray((a * (1 - d) + b * d).astype(np.uint8), "RGB")


def grain(img, amt=8, seed=1, cell=1):
    rng = np.random.default_rng(seed)
    n = rng.integers(-amt, amt + 1, (H // cell + 1, W // cell + 1, 1))
    n = np.repeat(np.repeat(n, cell, 0), cell, 1)[:H, :W]
    return Image.fromarray(np.clip(np.asarray(img).astype(np.int16) + n, 0, 255).astype(np.uint8), "RGB")


def vignette(img, k=0.5, col=(0, 0, 0)):
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.clip(np.hypot((xx - W / 2) / (W * 0.75), (yy - H / 2) / (H * 0.75)), 0, 1)[..., None] ** 2 * k
    a = np.asarray(img).astype(np.float32)
    return Image.fromarray((a * (1 - d) + np.array(col, np.float32) * d).astype(np.uint8), "RGB")


def layer():
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def over(img, lay, blur=0):
    if blur:
        lay = lay.filter(ImageFilter.GaussianBlur(blur))
    img.paste(lay, (0, 0), lay)
    return img


def blobs(seed, n, cols, rmin, rmax, alpha, blur, box=(0, 0, W, H)):
    rnd = random.Random(seed)
    lay, d = layer()
    for _ in range(n):
        x, y, r = rnd.uniform(box[0], box[2]), rnd.uniform(box[1], box[3]), rnd.uniform(rmin, rmax)
        d.ellipse([x - r, y - r * rnd.uniform(0.6, 1.0), x + r, y + r * rnd.uniform(0.6, 1.0)], fill=rgb(rnd.choice(cols)) + (alpha,))
    return lay.filter(ImageFilter.GaussianBlur(blur))


def ridge(d, seed, y0, amp, col, step=60):
    """jagged mountain silhouette from y0 down to the bottom"""
    rnd = random.Random(seed)
    pts = [(0, H)]
    x = -step
    while x <= W + step:
        pts.append((x, y0 - rnd.uniform(0, amp)))
        x += rnd.uniform(step * 0.5, step * 1.3)
    pts.append((W, H))
    d.polygon(pts, fill=col)


def glow_sprite(col, size):
    yy, xx = np.mgrid[0:size, 0:size]
    d = np.clip(1 - np.hypot(xx - size / 2, yy - size / 2) / (size / 2), 0, 1)
    a = (d ** 1.6 * 255).astype(np.uint8)
    core = np.clip(d * 2.2 - 1.2, 0, 1)[..., None]
    c = np.array(rgb(col), np.float32)
    px = (c * (1 - core) + 255 * core).astype(np.uint8)
    return Image.fromarray(np.dstack([px, a]), "RGBA")
