"""Blocky 3D (isometric) art library: boxes, avatars, creatures, props, icons, text. All original art."""
import math, os, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920
FD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts") + "/"
_fc = {}


def font(name, size):
    k = (name, size)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(FD + name, size)
    return _fc[k]


def rgb(c):
    if isinstance(c, tuple):
        return c
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def shade(c, f):
    r, g, b = rgb(c)
    if f <= 1:
        return (int(r * f), int(g * f), int(b * f))
    f -= 1
    return (int(r + (255 - r) * f), int(g + (255 - g) * f), int(b + (255 - b) * f))


def ease(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def pop(t, dur=0.3):
    """0->overshoot->1 scale curve for pop-in animations (t in seconds)."""
    if t <= 0:
        return 0.0
    x = min(t / dur, 1.0)
    return 1 + 0.18 * math.sin(x * math.pi) * (1 - x) * 2 - (1 - x) ** 3


# ===================================================== iso boxes
class Iso:
    def __init__(s, cx=540, cy=1060, u=56):
        s.cx, s.cy, s.u = cx, cy, u

    def p(s, x, y, z):
        return (s.cx + (x - y) * s.u * 0.866, s.cy + (x + y) * s.u * 0.5 - z * s.u)


def box_faces(iso, x, y, z, w, d, h):
    P = iso.p
    top = [P(x, y, z + h), P(x + w, y, z + h), P(x + w, y + d, z + h), P(x, y + d, z + h)]
    fx = [P(x + w, y, z), P(x + w, y + d, z), P(x + w, y + d, z + h), P(x + w, y, z + h)]
    fy = [P(x, y + d, z), P(x + w, y + d, z), P(x + w, y + d, z + h), P(x, y + d, z + h)]
    return top, fx, fy


def draw_box(dr, iso, b, ol=3):
    x, y, z, w, d, h, c = b[:7]
    top, fx, fy = box_faces(iso, x, y, z, w, d, h)
    oc = shade(c, 0.35)
    dr.polygon(fy, fill=shade(c, 0.64), outline=oc)
    dr.polygon(fx, fill=shade(c, 0.82), outline=oc)
    dr.polygon(top, fill=shade(c, 1.08), outline=oc)
    if ol > 1:
        for poly in (fy, fx, top):
            dr.line(poly + [poly[0]], fill=oc, width=ol, joint="curve")


def depth(b):
    x, y, z, w, d, h = b[:6]
    return (x + w / 2) + (y + d / 2) + z * 0.02


def draw_boxes(dr, iso, boxes, ol=3):
    for b in sorted(boxes, key=depth):
        draw_box(dr, iso, b, ol)
        if len(b) > 7 and b[7]:
            b[7](dr, iso, b)


def face_point(iso, b, side, u, v):
    x, y, z, w, d, h = b[:6]
    if side == "x":
        return iso.p(x + w, y + u * d, z + v * h)
    return iso.p(x + u * w, y + d, z + v * h)


def make_face(side, style="smile"):
    def f(dr, iso, b):
        e = iso.u * b[5] * 0.13
        if style == "glow":
            for u in (0.28, 0.72):
                px, py = face_point(iso, b, side, u, 0.6)
                dr.ellipse([px - e * 1.6, py - e * 1.6, px + e * 1.6, py + e * 1.6], fill=(255, 40, 40))
                dr.ellipse([px - e * 0.7, py - e * 0.7, px + e * 0.7, py + e * 0.7], fill=(255, 220, 200))
            return
        col = (25, 25, 25)
        for u in (0.3, 0.7):
            px, py = face_point(iso, b, side, u, 0.62)
            dr.ellipse([px - e * 0.55, py - e, px + e * 0.55, py + e], fill=col)
        if style == "smile":
            pts = [face_point(iso, b, side, 0.25 + 0.5 * i / 6, 0.34 - 0.1 * math.sin(math.pi * i / 6)) for i in range(7)]
            dr.line(pts, fill=col, width=max(3, int(e * 0.5)), joint="curve")
        elif style == "o":
            px, py = face_point(iso, b, side, 0.5, 0.28)
            dr.ellipse([px - e * 0.6, py - e * 0.7, px + e * 0.6, py + e * 0.7], fill=col)
        elif style == "mean":
            for u0, u1, v0, v1 in ((0.18, 0.42, 0.85, 0.76), (0.82, 0.58, 0.85, 0.76)):
                dr.line([face_point(iso, b, side, u0, v0), face_point(iso, b, side, u1, v1)], fill=col, width=max(3, int(e * 0.5)))
            dr.line([face_point(iso, b, side, 0.32, 0.3), face_point(iso, b, side, 0.68, 0.3)], fill=col, width=max(3, int(e * 0.5)))
    return f


# ===================================================== models (avatars & creatures)
SKINS = ["#f1c27d", "#e0ac69", "#c68642", "#8d5524", "#ffdbac", "#f5cd30"]
SHIRTS = ["#e53935", "#1e88e5", "#43a047", "#8e24aa", "#fb8c00", "#00acc1", "#f4511e", "#3949ab", "#ec407a", "#fdd835"]
PANTS = ["#263238", "#3e2723", "#1a237e", "#37474f", "#4e342e", "#212121"]


def place(parts, x, y, z, s, facing):
    """parts in local (forward f, side s, up z) -> world boxes."""
    out = []
    for p in parts:
        f, sd, zz, lf, ls, h, c = p[:7]
        extra = p[7] if len(p) > 7 else None
        if facing == "x":
            b = [x + f * s, y + sd * s, z + zz * s, lf * s, ls * s, h * s, c]
        else:  # facing +y : forward along y, side along x (mirrored so side keeps order)
            b = [x + sd * s, y + f * s, z + zz * s, ls * s, lf * s, h * s, c]
        if extra:
            b.append(extra)
        out.append(b)
    return out


def avatar_parts(t, anim, skin, shirt, pants, hat=None, face="smile"):
    sw = 0.0
    up = 0.0
    arm_up = 0.0
    if anim in ("walk", "run", "sneak"):
        k = 9 if anim == "run" else 6 if anim == "walk" else 4
        sw = math.sin(t * k) * (0.45 if anim == "run" else 0.3)
        up = abs(math.sin(t * k)) * (0.18 if anim == "run" else 0.08)
    elif anim == "bob":
        up = abs(math.sin(t * 4)) * 0.12
    elif anim == "jump":
        up = max(0, math.sin(t * 5)) * 1.2
    elif anim == "wave":
        arm_up = 1
        up = abs(math.sin(t * 3)) * 0.05
    elif anim == "cheer":
        arm_up = 2
        up = max(0, math.sin(t * 6)) * 0.5
    z0 = up
    P = []
    # legs (side 0..1 and 1..2)
    P.append((0 + sw * (1 if anim != "idle" else 0), 0, z0, 1, 0.98, 2, pants))
    P.append((0 - sw, 1.02, z0, 1, 0.98, 2, pants))
    P.append((0, 0, z0 + 2, 1, 2, 2, shirt))
    # arms
    aL = (0 - sw * 0.8, -1, z0 + 2, 1, 1, 2, skin)
    aR = (0 + sw * 0.8, 2, z0 + 2, 1, 1, 2, skin)
    if arm_up >= 1:
        aL = (0, -1, z0 + 3.6, 1, 1, 2, skin)
    if arm_up >= 2:
        aR = (0, 2, z0 + 3.6, 1, 1, 2, skin)
    P += [aL, aR]
    P.append((-0.1, 0.4, z0 + 4, 1.2, 1.2, 1.2, skin, "HEAD"))
    if hat:
        P.append((-0.15, 0.35, z0 + 5.2, 1.3, 1.3, 0.35, hat))
    return P, face


def creature_parts(kind, t, col, anim):
    up = 0.0
    sw = 0.0
    if anim in ("walk", "run"):
        sw = math.sin(t * (10 if anim == "run" else 6)) * 0.25
        up = abs(math.sin(t * 10)) * 0.1
    elif anim == "bob":
        up = abs(math.sin(t * 4)) * 0.1
    P = []
    if kind in ("dog", "cat", "fox"):
        legc = shade(col, 0.85)
        for f, s in ((0.1, 0.05), (1.3, 0.05), (0.1, 0.65), (1.3, 0.65)):
            P.append((f + (sw if s < 0.5 else -sw), s, 0, 0.35, 0.35, 0.7, legc))
        P.append((0, 0, 0.7 + up, 1.9, 1.0, 0.85, col))
        P.append((1.55, 0.05, 1.25 + up, 0.95, 0.9, 0.85, col, "HEAD"))
        ear = shade(col, 0.7)
        if kind == "dog":
            P.append((1.75, -0.05, 1.7 + up, 0.3, 0.2, 0.45, ear))
            P.append((1.75, 0.85, 1.7 + up, 0.3, 0.2, 0.45, ear))
        else:
            P.append((1.8, 0.1, 2.1 + up, 0.25, 0.25, 0.35, ear))
            P.append((1.8, 0.65, 2.1 + up, 0.25, 0.25, 0.35, ear))
        P.append((-0.45, 0.38, 1.25 + up + sw * 0.4, 0.5, 0.25, 0.25, ear))
        return P, 1.55 + up, "smile"
    if kind == "dragon":
        legc = shade(col, 0.8)
        for f, s in ((0.2, 0.0), (1.6, 0.0), (0.2, 0.9), (1.6, 0.9)):
            P.append((f + (sw if s < 0.5 else -sw), s, 0, 0.45, 0.4, 0.8, legc))
        P.append((0, 0, 0.8 + up, 2.4, 1.3, 1.0, col))
        P.append((2.0, 0.15, 1.6 + up, 1.1, 1.0, 1.0, col, "HEAD"))
        P.append((2.2, 0.2, 2.6 + up, 0.25, 0.25, 0.4, "#ffe082"))
        P.append((2.2, 0.85, 2.6 + up, 0.25, 0.25, 0.4, "#ffe082"))
        flap = math.sin(t * 7) * 0.4
        P.append((0.6, -1.4, 1.6 + up + flap, 1.2, 1.4, 0.15, shade(col, 1.25)))
        P.append((0.6, 1.3, 1.6 + up + flap, 1.2, 1.4, 0.15, shade(col, 1.25)))
        P.append((-0.8, 0.45, 1.1 + up, 0.8, 0.4, 0.35, col))
        return P, 1.8 + up, "smile"
    if kind == "deer":
        legc = shade(col, 0.75)
        for f, s in ((0.15, 0.05), (1.45, 0.05), (0.15, 0.7), (1.45, 0.7)):
            P.append((f, s, 0, 0.3, 0.3, 1.7, legc))
        P.append((0, 0, 1.7 + up, 2.0, 1.05, 1.0, col))
        P.append((1.6, 0.25, 2.5 + up, 0.5, 0.55, 1.2, col))
        P.append((1.7, 0.05, 3.5 + up, 1.0, 0.95, 0.9, col, "HEAD"))
        ant = "#d7ccc8"
        for s in (0.05, 0.8):
            P.append((1.9, s, 4.4 + up, 0.15, 0.15, 1.1, ant))
            P.append((1.6, s, 5.0 + up, 0.7, 0.15, 0.15, ant))
            P.append((1.6, s, 5.0 + up, 0.15, 0.15, 0.6, ant))
        return P, 0, "glow"
    raise ValueError(kind)


def model_boxes(parts, face_style, x, y, z, s, facing):
    out = []
    for p in place(parts, x, y, z, s, facing):
        if len(p) > 7 and p[7] == "HEAD":
            p[7] = make_face(facing, face_style)
        out.append(p)
    return out


def avatar(x, y, z=0, t=0, anim="idle", colors=("#f1c27d", "#e53935", "#263238"), facing="x", s=0.42, hat=None, face="smile"):
    parts, fs = avatar_parts(t, anim, colors[0], colors[1], colors[2], hat, face)
    # center the avatar footprint on (x,y)
    if facing == "x":
        return model_boxes(parts, fs, x - 0.5 * s, y - 1.0 * s, z, s, facing)
    return model_boxes(parts, fs, x - 1.0 * s, y - 0.5 * s, z, s, facing)


def creature(kind, x, y, z=0, t=0, anim="idle", col="#ffb74d", facing="x", s=0.6):
    parts, back, fs = creature_parts(kind, t, col, anim)
    if facing == "x":
        return model_boxes(parts, fs, x - 0.95 * s, y - 0.5 * s, z, s, facing), back * s
    return model_boxes(parts, fs, x - 0.5 * s, y - 0.95 * s, z, s, facing), back * s


# ===================================================== props
def P_house(x, y, o):
    col = o.get("c", "#ffe0b2")
    roof = o.get("r", "#d84315")
    g = "#9be7ff"
    return [
        [x, y, 0, 3, 3, 2.4, col],
        [x + 3, y + 1.1, 0, 0.08, 0.8, 1.4, "#6d4c41"],
        [x + 3, y + 0.25, 1.2, 0.08, 0.6, 0.7, g], [x + 3, y + 2.15, 1.2, 0.08, 0.6, 0.7, g],
        [x + 0.4, y + 3, 1.2, 0.8, 0.08, 0.7, g], [x + 1.8, y + 3, 1.2, 0.8, 0.08, 0.7, g],
        [x - 0.25, y - 0.25, 2.4, 3.5, 3.5, 0.4, roof],
        [x + 0.3, y + 0.3, 2.8, 2.4, 2.4, 0.4, shade(roof, 1.1)],
        [x + 0.85, y + 0.85, 3.2, 1.3, 1.3, 0.4, roof],
    ]


def P_tree(x, y, o):
    lf = o.get("c", "#2e7d32")
    s = o.get("s", 1.0)
    return [
        [x + 0.75 * s, y + 0.75 * s, 0, 0.5 * s, 0.5 * s, 1.2 * s, "#795548"],
        [x, y, 1.2 * s, 2 * s, 2 * s, 1 * s, lf],
        [x + 0.3 * s, y + 0.3 * s, 2.2 * s, 1.4 * s, 1.4 * s, 0.9 * s, shade(lf, 1.12)],
        [x + 0.6 * s, y + 0.6 * s, 3.1 * s, 0.8 * s, 0.8 * s, 0.7 * s, lf],
    ]


def P_car(x, y, o):
    c = o.get("c", "#e53935")
    return [
        [x + 0.3, y + 1.25, 0, 0.6, 0.12, 0.5, "#212121"], [x + 1.8, y + 1.25, 0, 0.6, 0.12, 0.5, "#212121"],
        [x, y, 0.25, 2.7, 1.3, 0.6, c],
        [x + 0.6, y + 0.1, 0.85, 1.3, 1.1, 0.55, "#b3e5fc"],
        [x + 2.7, y + 0.15, 0.45, 0.05, 0.3, 0.2, "#fff59d"], [x + 2.7, y + 0.85, 0.45, 0.05, 0.3, 0.2, "#fff59d"],
    ]


def P_treadmill(x, y, o):
    return [
        [x, y, 0, 1.4, 3.2, 0.35, "#37474f"],
        [x + 0.1, y + 0.2, 0.35, 1.2, 2.9, 0.05, "#1b1b1b"],
        [x, y + 3.0, 0.35, 0.15, 0.15, 1.5, "#90a4ae"], [x + 1.25, y + 3.0, 0.35, 0.15, 0.15, 1.5, "#90a4ae"],
        [x, y + 2.9, 1.85, 1.4, 0.4, 0.25, o.get("c", "#ff5252")],
    ]


def P_campfire(x, y, o):
    return [
        [x, y + 0.55, 0, 1.6, 0.4, 0.35, "#6d4c41"], [x + 0.6, y, 0, 0.4, 1.6, 0.35, "#5d4037"],
        [x - 0.4, y - 0.4, 0, 0.4, 0.4, 0.3, "#78909c"], [x + 1.6, y + 1.5, 0, 0.4, 0.4, 0.3, "#78909c"],
        [x + 1.7, y - 0.3, 0, 0.35, 0.35, 0.25, "#78909c"], [x - 0.4, y + 1.6, 0, 0.35, 0.35, 0.25, "#78909c"],
    ]


def P_ship(x, y, o):
    a = o.get("c", "#e53935")
    return [
        [x, y, 0, 4.4, 1.7, 0.9, "#8d6e63"], [x, y, 0.9, 4.4, 1.7, 0.18, "#5d4037"],
        [x + 3.6, y + 0.3, 0.2, 1.2, 1.1, 0.7, "#8d6e63"],
        [x + 0.3, y + 0.35, 1.08, 1.2, 1.0, 0.8, "#a1887f"],
        [x + 2.3, y + 0.75, 1.08, 0.22, 0.22, 3.4, "#4e342e"],
        [x + 2.6, y - 0.2, 1.9, 0.1, 2.1, 2.1, "#fafafa"],
        [x + 2.3, y + 0.75, 4.48, 0.1, 0.9, 0.5, a],
    ]


def P_island(x, y, o):
    return [
        [x, y, 0, 3.2, 3.2, 0.5, "#f4d58d"],
        [x + 1.4, y + 1.4, 0.5, 0.4, 0.4, 1.0, "#8d6e63"], [x + 1.5, y + 1.5, 1.5, 0.4, 0.4, 1.0, "#8d6e63"],
        [x + 0.5, y + 1.5, 2.5, 2.4, 0.5, 0.2, "#43a047"], [x + 1.5, y + 0.5, 2.5, 0.5, 2.4, 0.2, "#388e3c"],
    ]


def P_trophy(x, y, o):
    g = "#ffc107"
    return [
        [x, y, 0, 1.8, 1.8, 0.5, "#5d4037"], [x + 0.7, y + 0.7, 0.5, 0.4, 0.4, 0.7, g],
        [x + 0.25, y + 0.25, 1.2, 1.3, 1.3, 1.2, g], [x + 0.05, y + 0.65, 1.7, 0.2, 0.5, 0.5, g],
        [x + 0.65, y + 0.05, 1.7, 0.5, 0.2, 0.5, g],
    ]


def P_crate(x, y, o):
    s = o.get("s", 1.4)
    return [[x, y, o.get("z", 0), s, s, s, o.get("c", "#a1887f")]]


def P_base(x, y, o):
    c = o.get("c", "#42a5f5")
    w = o.get("w", 3.4)
    return [
        [x, y, 0, w, w, 0.15, shade(c, 1.2)],
        [x, y, 0.15, w, 0.25, 0.7, c], [x, y, 0.15, 0.25, w, 0.7, c],
        [x + w - 0.25, y + 0.25, 0.15, 0.25, w - 0.25, 0.7, c], [x + 0.25, y + w - 0.25, 0.15, w - 0.5, 0.25, 0.7, c],
    ]


def P_pedestal(x, y, o):
    return [[x, y, 0, 1.6, 1.6, 1.3, o.get("c", "#455a64")], [x - 0.1, y - 0.1, 1.3, 1.8, 1.8, 0.2, "#90a4ae"]]


def P_block(x, y, o):
    return [[x, y, o.get("z", 0), o.get("w", 1), o.get("d", 1), o.get("h", 1), o.get("c", "#9e9e9e")]]


def P_tower(x, y, o):
    c = o.get("c", "#7e57c2")
    return [[x, y, 0, 2, 2, 4, c], [x - 0.2, y - 0.2, 4, 2.4, 2.4, 0.4, shade(c, 1.2)], [x + 0.6, y + 0.6, 4.4, 0.8, 0.8, 1.2, "#ffd54f"]]


PROPS = {"house": P_house, "tree": P_tree, "car": P_car, "treadmill": P_treadmill, "campfire": P_campfire,
         "ship": P_ship, "island": P_island, "trophy": P_trophy, "crate": P_crate, "base": P_base,
         "pedestal": P_pedestal, "block": P_block, "tower": P_tower}


def keyboard_boxes(t, x0, y0, cols, rows, hot=None, rgbk=True):
    out = []
    for r in range(rows):
        for c in range(cols):
            x, y = x0 + c * 1.0, y0 + r * 1.0
            down = 0
            if hot is not None and abs(x + 0.45 - hot[0]) < 0.75 and abs(y + 0.45 - hot[1]) < 0.75:
                down = 0.2
            if rgbk and (r * 3 + c) % 4 == 0:
                hue = ((c * 40 + r * 25 + t * 120) % 360) / 360.0
                import colorsys
                cc = tuple(int(v * 255) for v in colorsys.hsv_to_rgb(hue, 0.55, 1.0))
            else:
                cc = (236, 239, 241)
            out.append([x + 0.05, y + 0.05, 0.4 - down, 0.9, 0.9, 0.35, cc])
    return out


# ===================================================== icons (2D stickers)
_ic = {}


def _star(d, cx, cy, r1, r2, n=5, rot=-90, fill=(255, 213, 79)):
    pts = []
    for i in range(n * 2):
        r = r1 if i % 2 == 0 else r2
        a = math.radians(rot + i * 180 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill, outline=(60, 40, 0), width=6)


def _draw_icon(name, arg=None):
    S = 256
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    K = (30, 30, 30)
    if name in ("egg", "egg_gold", "egg_blue", "egg_purple", "egg_red"):
        col = {"egg": (250, 245, 230), "egg_gold": (255, 202, 40), "egg_blue": (79, 195, 247),
               "egg_purple": (171, 71, 188), "egg_red": (239, 83, 80)}[name]
        d.ellipse([58, 28, 198, 236], fill=col, outline=K, width=8)
        sp = shade(col, 0.75)
        for (a, b, r) in ((100, 90, 16), (150, 140, 20), (105, 175, 14), (160, 70, 11)):
            d.ellipse([a - r, b - r, a + r, b + r], fill=sp)
        d.ellipse([80, 55, 108, 100], fill=(255, 255, 255, 170))
    elif name == "coin":
        d.ellipse([28, 28, 228, 228], fill=(255, 193, 7), outline=(120, 80, 0), width=10)
        d.ellipse([60, 60, 196, 196], outline=(230, 160, 0), width=8)
        _star(d, 128, 132, 50, 22, fill=(255, 236, 130))
    elif name == "star":
        _star(d, 128, 136, 115, 50)
    elif name == "heart":
        d.ellipse([28, 50, 134, 156], fill=(239, 83, 80))
        d.ellipse([122, 50, 228, 156], fill=(239, 83, 80))
        d.polygon([(34, 120), (222, 120), (128, 232)], fill=(239, 83, 80))
    elif name == "paw":
        c = (255, 255, 255)
        d.ellipse([70, 110, 186, 216], fill=c, outline=K, width=7)
        for (a, b) in ((52, 70), (98, 38), (158, 38), (204, 70)):
            d.ellipse([a - 24, b - 28, a + 24, b + 28], fill=c, outline=K, width=7)
    elif name == "fruit":
        c = arg or (156, 39, 176)
        d.ellipse([34, 56, 222, 240], fill=c, outline=K, width=8)
        d.ellipse([70, 90, 112, 140], fill=(255, 255, 255, 150))
        d.rectangle([120, 20, 136, 66], fill=(93, 64, 55))
        d.polygon([(136, 40), (210, 18), (176, 70)], fill=(76, 175, 80), outline=K)
    elif name == "sword":
        d.polygon([(60, 196), (196, 36), (214, 42), (220, 60), (78, 214)], fill=(207, 216, 220), outline=K, width=6)
        d.line([(80, 192), (205, 50)], fill=(255, 255, 255), width=5)
        d.polygon([(30, 182), (74, 226), (92, 208), (48, 164)], fill=(255, 202, 40), outline=K, width=6)
        d.polygon([(10, 226), (30, 246), (60, 214), (40, 196)], fill=(121, 85, 72), outline=K, width=6)
    elif name == "knife":
        d.polygon([(70, 186), (200, 40), (222, 30), (214, 56), (92, 206)], fill=(224, 224, 224), outline=K, width=6)
        d.polygon([(30, 214), (52, 236), (96, 196), (74, 174)], fill=(121, 85, 72), outline=K, width=6)
    elif name == "gun":
        c = (66, 66, 66)
        d.rectangle([40, 80, 220, 130], fill=c, outline=K, width=6)
        d.polygon([(70, 126), (120, 126), (104, 220), (54, 220)], fill=(93, 64, 55), outline=K, width=6)
        d.rectangle([200, 70, 216, 82], fill=c)
        d.ellipse([110, 130, 150, 170], outline=K, width=6)
    elif name == "scythe":
        d.line([(70, 236), (150, 36)], fill=(33, 33, 33), width=16)
        d.arc([30, 10, 250, 190], 195, 325, fill=K, width=50)
        d.arc([36, 16, 244, 184], 197, 323, fill=(38, 198, 218), width=38)
        d.ellipse([132, 20, 168, 56], fill=(129, 212, 250), outline=K, width=5)
    elif name == "trophy":
        g = (255, 193, 7)
        d.rectangle([84, 200, 172, 236], fill=(93, 64, 55), outline=K, width=6)
        d.rectangle([116, 150, 140, 200], fill=g, outline=K, width=6)
        d.pieslice([56, 10, 200, 170], 0, 180, fill=g, outline=K, width=6)
        d.rectangle([56, 24, 200, 90], fill=g)
        d.line([(56, 24), (200, 24)], fill=K, width=6)
        d.arc([20, 30, 90, 110], 90, 270, fill=K, width=12)
        d.arc([166, 30, 236, 110], 270, 90, fill=K, width=12)
        _star(d, 128, 74, 30, 13, fill=(255, 245, 157))
    elif name == "calendar":
        d.rounded_rectangle([30, 46, 226, 230], 22, fill=(255, 255, 255), outline=K, width=8)
        d.rounded_rectangle([30, 46, 226, 100], 22, fill=(229, 57, 53), outline=K, width=8)
        for a in (80, 176):
            d.rounded_rectangle([a - 10, 22, a + 10, 72], 8, fill=(97, 97, 97))
        for r in range(3):
            for c in range(4):
                x0, y0 = 54 + c * 42, 116 + r * 36
                d.rectangle([x0, y0, x0 + 26, y0 + 22], fill=(189, 189, 189) if (r, c) != (1, 2) else (255, 193, 7))
    elif name == "fire":
        d.polygon([(128, 8), (200, 120), (210, 180), (128, 246), (46, 180), (60, 110)], fill=(255, 111, 0))
        d.polygon([(128, 70), (170, 150), (172, 196), (128, 236), (84, 196), (92, 150)], fill=(255, 202, 40))
        d.polygon([(128, 140), (150, 190), (128, 226), (106, 190)], fill=(255, 249, 196))
    elif name == "alarm":
        d.rectangle([50, 200, 206, 236], fill=(66, 66, 66), outline=K, width=6)
        d.pieslice([60, 60, 196, 340], 180, 360, fill=(244, 67, 54), outline=K, width=6)
        d.rectangle([60, 196, 196, 204], fill=K)
        d.ellipse([92, 100, 124, 140], fill=(255, 205, 210))
        for a in (-150, -120, -60, -30):
            r = math.radians(a)
            d.line([(128 + 110 * math.cos(r), 150 + 110 * math.sin(r)), (128 + 140 * math.cos(r), 150 + 140 * math.sin(r))], fill=(255, 235, 59), width=10)
    elif name == "question":
        d.ellipse([20, 20, 236, 236], fill=(255, 193, 7), outline=K, width=8)
        f = font("LuckiestGuy.ttf", 170)
        d.text((128, 146), "?", font=f, fill=(255, 255, 255), anchor="mm", stroke_width=8, stroke_fill=K)
    elif name == "steps":
        for (a, b, r) in ((80, 190, 0), (170, 120, 1), (90, 60, 0)):
            d.ellipse([a - 28, b - 40, a + 28, b + 32], fill=(255, 255, 255), outline=K, width=5)
            d.ellipse([a - 18, b - 70, a + 18, b - 44], fill=(255, 255, 255), outline=K, width=5)
    elif name == "clapper":
        d.rectangle([28, 100, 228, 230], fill=(33, 33, 33), outline=(255, 255, 255), width=6)
        d.polygon([(28, 60), (220, 22), (228, 66), (36, 104)], fill=(33, 33, 33), outline=(255, 255, 255), width=6)
        for i in range(4):
            x = 60 + i * 44
            d.polygon([(x, 54 - i * 8), (x + 22, 50 - i * 8), (x + 12, 98 - i * 8), (x - 10, 102 - i * 8)], fill=(255, 255, 255))
        d.rectangle([28, 100, 228, 120], fill=(255, 255, 255))
    elif name == "crosshair":
        c = (255, 82, 82)
        d.ellipse([40, 40, 216, 216], outline=c, width=14)
        for (a, b, c2, e) in ((128, 10, 128, 90), (128, 166, 128, 246), (10, 128, 90, 128), (166, 128, 246, 128)):
            d.line([(a, b), (c2, e)], fill=c, width=14)
        d.ellipse([116, 116, 140, 140], fill=c)
    elif name == "rocket":
        d.polygon([(128, 10), (176, 80), (176, 180), (80, 180), (80, 80)], fill=(236, 239, 241), outline=K, width=6)
        d.ellipse([104, 80, 152, 128], fill=(79, 195, 247), outline=K, width=6)
        d.polygon([(80, 140), (40, 200), (80, 190)], fill=(229, 57, 53), outline=K, width=5)
        d.polygon([(176, 140), (216, 200), (176, 190)], fill=(229, 57, 53), outline=K, width=5)
        d.polygon([(96, 184), (160, 184), (128, 250)], fill=(255, 152, 0))
    elif name == "planet":
        d.ellipse([50, 50, 206, 206], fill=(126, 87, 194), outline=K, width=6)
        d.ellipse([10, 110, 246, 160], outline=(255, 213, 79), width=10)
        d.ellipse([80, 80, 120, 110], fill=(179, 157, 219))
    elif name == "key":
        d.rounded_rectangle([24, 30, 232, 226], 26, fill=(120, 144, 156), outline=K, width=7)
        d.rounded_rectangle([44, 40, 212, 190], 22, fill=(236, 239, 241), outline=K, width=5)
        f = font("LuckiestGuy.ttf", 100)
        d.text((128, 122), arg or "W", font=f, fill=(55, 71, 79), anchor="mm")
    elif name == "bolt":
        d.polygon([(150, 6), (50, 140), (118, 140), (96, 250), (206, 104), (138, 104)], fill=(255, 235, 59), outline=K, width=7)
    elif name == "money":
        d.rounded_rectangle([14, 60, 242, 196], 16, fill=(102, 187, 106), outline=K, width=7)
        d.ellipse([88, 88, 168, 168], fill=(165, 214, 167), outline=K, width=5)
        f = font("LuckiestGuy.ttf", 70)
        d.text((128, 132), "$", font=f, fill=(27, 94, 32), anchor="mm")
    elif name == "shield":
        d.polygon([(128, 14), (226, 50), (210, 160), (128, 244), (46, 160), (30, 50)], fill=(66, 165, 245), outline=K, width=8)
        d.polygon([(128, 40), (200, 66), (190, 152), (128, 214)], fill=(144, 202, 249))
    elif name == "crown":
        d.polygon([(26, 200), (26, 70), (80, 130), (128, 46), (176, 130), (230, 70), (230, 200)], fill=(255, 193, 7), outline=K, width=7)
        for x in (70, 128, 186):
            d.ellipse([x - 14, 150, x + 14, 178], fill=(229, 57, 53))
    elif name == "moon":
        d.ellipse([30, 30, 226, 226], fill=(255, 245, 157))
        for (a, b, r) in ((90, 100, 22), (150, 160, 30), (160, 80, 14)):
            d.ellipse([a - r, b - r, a + r, b + r], fill=(240, 220, 120))
    elif name == "code":
        d.rounded_rectangle([16, 30, 240, 190], 16, fill=(38, 50, 56), outline=K, width=7)
        d.rectangle([34, 48, 222, 172], fill=(21, 101, 192))
        f = font("LuckiestGuy.ttf", 64)
        d.text((128, 112), "</>", font=f, fill=(255, 255, 255), anchor="mm")
        d.rectangle([108, 190, 148, 226], fill=(96, 125, 139))
        d.rectangle([70, 222, 186, 238], fill=(96, 125, 139))
    elif name == "trade":
        d.polygon([(20, 80), (170, 80), (170, 40), (236, 100), (170, 160), (170, 120), (20, 120)], fill=(102, 187, 106), outline=K, width=6)
        d.polygon([(236, 160), (86, 160), (86, 120), (20, 180), (86, 240), (86, 200), (236, 200)], fill=(66, 165, 245), outline=K, width=6)
    elif name == "license":
        d.rounded_rectangle([14, 50, 242, 206], 18, fill=(255, 255, 255), outline=K, width=7)
        d.rectangle([34, 74, 104, 160], fill=(144, 202, 249))
        for y in (86, 116, 146):
            d.rectangle([122, y, 220, y + 12], fill=(189, 189, 189))
        d.ellipse([170, 150, 236, 216], fill=(76, 175, 80), outline=K, width=5)
        d.line([(184, 182), (200, 198), (224, 166)], fill=(255, 255, 255), width=9)
    elif name == "rock":
        d.polygon([(30, 200), (50, 110), (110, 60), (180, 70), (230, 140), (220, 210)], fill=(158, 158, 158), outline=K, width=7)
        for x in (100, 160):
            d.ellipse([x - 24, 110, x + 24, 158], fill=(255, 255, 255), outline=K, width=5)
            d.ellipse([x - 8, 128, x + 10, 150], fill=K)
    elif name == "bottle":
        d.rounded_rectangle([76, 80, 180, 240], 26, fill=(255, 255, 255), outline=K, width=7)
        d.rectangle([84, 150, 172, 232], fill=(255, 224, 178))
        d.rectangle([90, 54, 166, 86], fill=(244, 143, 177), outline=K, width=6)
        d.ellipse([110, 10, 146, 62], fill=(255, 204, 128), outline=K, width=6)
    elif name == "eye":
        d.ellipse([10, 60, 246, 196], fill=(255, 255, 255), outline=K, width=8)
        d.ellipse([88, 76, 168, 180], fill=(244, 67, 54))
        d.ellipse([112, 104, 144, 152], fill=K)
    elif name == "globe":
        d.ellipse([20, 20, 236, 236], fill=(41, 182, 246), outline=K, width=7)
        d.polygon([(60, 70), (120, 50), (130, 110), (80, 130)], fill=(102, 187, 106))
        d.polygon([(140, 140), (200, 120), (190, 200), (150, 210)], fill=(102, 187, 106))
    elif name == "clock":
        d.ellipse([20, 20, 236, 236], fill=(255, 255, 255), outline=K, width=9)
        d.line([(128, 128), (128, 60)], fill=K, width=12)
        d.line([(128, 128), (180, 150)], fill=K, width=12)
    elif name == "cartridge":
        c = arg or (120, 120, 120)
        d.polygon([(40, 30), (216, 30), (216, 200), (196, 230), (60, 230), (40, 200)], fill=c, outline=K, width=8)
        d.rectangle([66, 56, 190, 150], fill=(230, 230, 230), outline=K, width=5)
        d.rectangle([76, 66, 180, 110], fill=(229, 57, 53))
        for x in range(70, 190, 18):
            d.rectangle([x, 196, x + 9, 230], fill=shade(c, 0.6))
    elif name == "controller":
        d.rounded_rectangle([10, 70, 246, 190], 18, fill=(190, 190, 190), outline=K, width=8)
        d.rectangle([24, 84, 232, 176], fill=(40, 40, 40))
        d.rectangle([44, 116, 104, 136], fill=(200, 200, 200)); d.rectangle([64, 96, 84, 156], fill=(200, 200, 200))
        d.rectangle([116, 124, 134, 132], fill=(200, 200, 200)); d.rectangle([140, 124, 158, 132], fill=(200, 200, 200))
        d.ellipse([170, 112, 196, 138], fill=(229, 57, 53)); d.ellipse([204, 112, 230, 138], fill=(229, 57, 53))
    elif name == "tv":
        d.rounded_rectangle([20, 40, 236, 210], 20, fill=(121, 85, 72), outline=K, width=8)
        d.rounded_rectangle([40, 60, 186, 190], 16, fill=(30, 60, 90), outline=K, width=5)
        d.ellipse([200, 80, 222, 102], fill=(255, 202, 40)); d.ellipse([200, 120, 222, 142], fill=(255, 202, 40))
        d.line([(90, 40), (60, 6)], fill=K, width=6); d.line([(140, 40), (170, 6)], fill=K, width=6)
        d.rectangle([60, 210, 90, 236], fill=K); d.rectangle([166, 210, 196, 236], fill=K)
    elif name == "skateboard":
        d.rounded_rectangle([14, 100, 242, 140], 20, fill=(229, 57, 53), outline=K, width=7)
        for x in (60, 196):
            d.ellipse([x - 24, 136, x + 24, 184], fill=(255, 235, 59), outline=K, width=6)
    elif name == "arcade":
        d.polygon([(60, 10), (196, 10), (210, 246), (46, 246)], fill=(57, 73, 171), outline=K, width=8)
        d.rectangle([76, 40, 180, 130], fill=(20, 20, 20), outline=K, width=5)
        d.rectangle([86, 50, 170, 120], fill=(0, 230, 118))
        d.rectangle([60, 140, 196, 170], fill=(255, 202, 40), outline=K, width=5)
        d.ellipse([84, 146, 104, 166], fill=(229, 57, 53)); d.ellipse([150, 146, 170, 166], fill=(33, 150, 243))
    elif name == "bar":
        pass
    else:
        raise ValueError(name)
    return im


def icon(name, size, arg=None):
    k = (name, size, arg)
    if k not in _ic:
        im = _draw_icon(name, arg)
        a = im.split()[3]
        ol = a.filter(ImageFilter.MaxFilter(17))
        base = Image.new("RGBA", im.size, (0, 0, 0, 0))
        sh = Image.new("RGBA", im.size, (0, 0, 0, 110))
        base.paste(sh, (6, 10), ol)
        white = Image.new("RGBA", im.size, (255, 255, 255, 255))
        base.paste(white, (0, 0), ol)
        base.alpha_composite(im)
        pad = Image.new("RGBA", (300, 300), (0, 0, 0, 0))
        pad.alpha_composite(base, (22, 22))
        _ic[k] = pad.resize((size, size), Image.LANCZOS)
    return _ic[k]


def paste_icon(img, name, cx, cy, size, rot=0, arg=None, alpha=1.0):
    if size < 4:
        return
    if isinstance(arg, list):
        arg = tuple(arg)
    im = icon(name, int(size), arg)
    if rot:
        im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 1:
        a = im.split()[3].point(lambda v: int(v * alpha))
        im = im.copy()
        im.putalpha(a)
    img.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


# ===================================================== text
_tc = {}


def text_img(txt, size, fill, fname="LuckiestGuy.ttf", stroke=10, maxw=980):
    k = (txt, size, fill, fname, stroke, maxw)
    if k in _tc:
        return _tc[k]
    f = font(fname, size)
    while True:
        bb = f.getbbox(txt, stroke_width=stroke)
        if bb[2] - bb[0] <= maxw or size < 30:
            break
        size -= 4
        f = font(fname, size)
    w, h = bb[2] - bb[0] + 20, bb[3] - bb[1] + 30
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.text((10 - bb[0] + 6, 12 - bb[1] + 9), txt, font=f, fill=(0, 0, 0, 160), stroke_width=stroke, stroke_fill=(0, 0, 0, 160))
    d.text((10 - bb[0], 12 - bb[1]), txt, font=f, fill=fill, stroke_width=stroke, stroke_fill=(20, 20, 30))
    _tc[k] = im
    return im


def paste_center(img, im, cx, cy, scale=1.0):
    if scale <= 0.02:
        return
    if abs(scale - 1) > 0.01:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BILINEAR)
    img.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))
