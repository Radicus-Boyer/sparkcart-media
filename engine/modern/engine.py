"""'Most Popular Games of the Internet' renderer: motion-graphics Shorts with one visual theme per game.

usage:  python3 engine/modern/engine.py <episode.json> [sheet | frame N]
        (normally called through engine/render.py, which reads "preset": "popular")

Episode JSON: {"preset": "popular", "num": 1, "theme": "cs2", "game": "Counter-Strike 2", "file": "01 - Counter-Strike 2.mp4",
               "target": 70, "pron": {...}, "lines": [{"t": "caption text", "say": "optional spoken text", "sc": {scene}}]}
Scene kinds: title, text, stat, list, bars, photo, quote, timeline, vs, outro (see README.md).
"""
import hashlib, json, math, os, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw

D = os.path.dirname(os.path.abspath(__file__)) + "/"
ENG = os.path.dirname(D.rstrip("/")) + "/"
ROOT = os.path.dirname(ENG.rstrip("/")) + "/"
sys.path.insert(0, D)
sys.path.insert(0, ENG)
from gfx import *
from themes import THEMES, PM
import music2, tts

FPS = 30
WORK = ROOT + "build/work/popular/"
OUT = os.environ.get("POP_OUT", ROOT + "build/out/")
ASSETS = ROOT + "episodes/assets/"
SERIES = ("MOST POPULAR GAMES", "OF THE INTERNET")
CAP_Y = 1330      # caption centre: kept well above the YouTube / TikTok title and buttons
MID = 800         # vertical centre of the content area (430..1170)


# ============================================================ text in the theme's style
def case(th, s):
    return s.upper() if th["case"] == "upper" else s


def T(th, role, txt, size, maxw=None, cache=True, raw=False):
    f, w, fill, sr, sfill, sh, box = th["text"][role]
    if not raw:
        txt = case(th, txt)
    size = int(size)
    while True:
        shd = (int(size * sh[0]), int(size * sh[1]), sh[2]) if sh else None
        bx = (box, int(size * 0.22), int(size * 0.13)) if box else None
        im = text_img(txt, f, size, fill, int(round(size * sr)), sfill, w, shd, bx, cache=cache)
        if not maxw or im.width <= maxw or size <= 26:
            return im
        size = int(size * 0.94)


def fit_size(th, role, txt, size, maxw):
    f, w = th["text"][role][0], th["text"][role][1]
    txt = case(th, txt)
    while size > 26 and font(f, size, w).getlength(txt) > maxw:
        size = int(size * 0.95)
    return size


def wrapped(th, role, txt, size, maxw, maxlines=4):
    f, w = th["text"][role][0], th["text"][role][1]
    while True:
        lines = wrap(case(th, txt), lambda s: font(f, size, w).getlength(s), maxw)
        if len(lines) <= maxlines or size <= 40:
            return [T(th, role, ln, size, maxw, raw=True) for ln in lines]
        size = int(size * 0.92)


def I(th, name, size, role="acc"):
    f, w, fill, sr, sfill, sh, box = th["text"][role]
    if box:
        fill = box
    return icon_img(name, size, fill, int(round(size * sr * 0.7)), sfill)


# ============================================================ sprites
def S(im, cx, cy, t0=0.0, anim="pop", anchor="c"):
    return dict(im=im, x=cx, y=cy, t0=t0, anim=anim, anchor=anchor)


def draw_items(img, items, lt):
    for s in items:
        if callable(s):
            s(img, lt)
            continue
        t = lt - s["t0"]
        if t < 0:
            continue
        k = min(1.0, t / 0.24)
        if s["anim"] == "pop" and k < 1:
            paste(img, s["im"], s["x"], s["y"], max(0.05, back(k)), s["anchor"])
        elif s["anim"] == "slide" and k < 1:
            paste(img, s["im"], s["x"], s["y"] + (1 - ease(k)) * 46, 1.0, s["anchor"])
        else:
            paste(img, s["im"], s["x"], s["y"], 1.0, s["anchor"])


def stack(entries, cy=MID, gap=18):
    """entries: (image, t0, anim). Centres the column on cy."""
    total = sum(e[0].height for e in entries) + gap * (len(entries) - 1)
    y, out = cy - total / 2, []
    for im, t0, anim in entries:
        out.append(S(im, 540, y + im.height / 2, t0, anim))
        y += im.height + gap
    return out


def panel(th, w, h, cy=MID, kind="main", t0=0.0):
    return S(th["panel"](int(w), int(h), kind), 540, cy, t0, "slide")


# ============================================================ scenes
def sc_text(th, sc, dur, title=False):
    ent = []
    t = 0.0
    if sc.get("kicker"):
        ent.append((T(th, "small", sc["kicker"], 56, 940), 0.0, "slide"))
        t = 0.1
    if sc.get("icon"):
        ent.append((I(th, sc["icon"], sc.get("isize", 190)), t, "pop"))
        t += 0.12
    lines = sc.get("big", [])
    lines = [lines] if isinstance(lines, str) else lines
    size = sc.get("size", 176 if title else 138)
    for ln in lines:
        role = "big"
        if ln.startswith("*"):
            role, ln = "acc", ln[1:]
        ent.append((T(th, role, ln, size, 960), t, "pop"))
        t += sc.get("stagger", 0.22)
    if sc.get("sub"):
        for im in wrapped(th, "small", sc["sub"], 60, 920, 2):
            ent.append((im, t + 0.1, "slide"))
    return stack(ent, MID + 10, sc.get("gap", 14))


def sc_stat(th, sc, dur):
    icon, label, sub = sc.get("icon"), sc.get("label"), sc.get("sub")
    lab = wrapped(th, "psmall", label, 54, 840, 2) if label else []
    subs = wrapped(th, "pacc", sub, 62, 850, 2) if sub else []
    h = 610 + 62 * max(0, len(lab) - 1) + 70 * max(0, len(subs) - 1)
    items = [panel(th, 940, h)]
    y = MID - h / 2
    if icon:
        items.append(S(I(th, icon, 104, "pacc"), 540, y + 96, 0.05))
        y += 96
    for j, im in enumerate(lab):
        items.append(S(im, 540, y + 96 + j * 62, 0.1, "slide"))
    y += 62 * max(0, len(lab) - 1)
    ny = y + (270 if label else 190)
    if not sub:
        ny += 40
    if "num" in sc:
        to, fmt = sc["num"][0], sc["num"][1]
        size = fit_size(th, "pbig", fmt.format(to), sc.get("size", 230), 850)
        cd = sc.get("count", 1.1)

        def dyn(img, lt):
            k = ease((lt - 0.15) / cd)
            paste(img, T(th, "pbig", fmt.format(to * k), size, cache=k >= 1), 540, ny)
        items.append(dyn)
    else:
        items.append(S(T(th, "pbig", sc["val"], sc.get("size", 230), 850), 540, ny, 0.15))
    for j, im in enumerate(subs):
        items.append(S(im, 540, ny + 190 + j * 70, 0.5, "slide"))
    return items


def sc_list(th, sc, dur):
    rows = sc["items"]
    n = len(rows)
    rowh = 136 if n <= 3 else 120
    head = sc.get("head")
    top_pad = 126 if head else 44
    h = top_pad + n * rowh + 44
    top = MID - h / 2
    items = [panel(th, 940, h)]
    if head:
        items.append(S(T(th, "pacc", head, 64, 840), 540, top + 74, 0.05, "slide"))
    for j, (ic, txt) in enumerate(rows):
        y = top + top_pad + j * rowh + rowh / 2
        t0 = 0.2 + j * min(1.1, dur * 0.62 / max(1, n))
        items.append(S(I(th, ic, 66, "pacc"), 158, y, t0))
        items.append(S(T(th, "pbig", txt, 70, 730), 226, y, t0, "slide", "l"))
    return items


def sc_bars(th, sc, dur):
    rows = sc["rows"]            # [label, value, shown text]
    n = len(rows)
    head = sc.get("head")
    top_pad = 130 if head else 50
    rowh = 200
    h = top_pad + n * rowh + 30
    top = MID - h / 2
    items = [panel(th, 940, h)]
    if head:
        items.append(S(T(th, "pacc", head, 60, 840), 540, top + 76, 0.05, "slide"))
    vmax = max(r[1] for r in rows)
    acc, dim = rgb(th["text"]["pacc"][2]), rgb(th["text"]["psmall"][2])
    x0, bw = 130, 820
    bars = []
    for j, (label, v, shown) in enumerate(rows):
        y = top + top_pad + j * rowh
        t0 = 0.25 + j * 0.45
        items.append(S(T(th, "psmall", label, 50, 540), x0, y + 34, t0, "slide", "l"))
        val = T(th, "pbig", shown, 70, 330)
        items.append(S(val, x0 + bw - val.width / 2, y + 30, t0 + 0.55))
        bars.append((y + 78, t0, v / vmax, acc if j == 0 else dim))

    def dyn(img, lt):
        d = ImageDraw.Draw(img)
        for (y, t0, frac, col) in bars:
            k = ease((lt - t0) / 0.8)
            if k > 0:
                d.rectangle([x0, y, x0 + max(6, bw * frac * k), y + 74], fill=col)
    items.insert(1, dyn)
    return items


def sc_photo(th, sc, dur):
    path = ASSETS + sc["img"]
    label, credit = sc.get("label"), sc.get("credit")
    cy = MID + (24 if label else 0)
    if not os.path.exists(path):
        return [panel(th, 940, 560, cy), S(T(th, "pacc", "ADD IMAGE", 110, 800), 540, cy - 50), S(T(th, "psmall", sc["img"], 44, 840, raw=True), 540, cy + 70)]
    src = Image.open(path).convert("RGB")
    if sc.get("crop"):
        l, t, r, b = sc["crop"]
        src = src.crop((int(src.width * l), int(src.height * t), int(src.width * r), int(src.height * b)))
    a = src.width / src.height
    fw, fh = 960, 960 / a
    if fh > sc.get("maxh", 660):
        fh = sc.get("maxh", 660)
        fw = fh * a
    fw, fh = int(fw) // 2 * 2, int(fh) // 2 * 2
    Z = 1.14
    pre = src.resize((int(fw * Z), int(fh * Z)), Image.LANCZOS)
    fx, fy = sc.get("focus", [0.5, 0.5])
    col, bw = th["frame"]
    fr = Image.new("RGBA", (fw + 2 * bw + 8, fh + 2 * bw + 8), (0, 0, 0, 0))
    fd = ImageDraw.Draw(fr)
    fd.rectangle([0, 0, fr.width - 1, fr.height - 1], outline=(0, 0, 0, 200), width=4)
    fd.rectangle([4, 4, fr.width - 5, fr.height - 5], outline=rgb(col) + (255,), width=bw)

    def dyn(img, lt):
        k = ease(min(1.0, lt / max(0.5, dur)))
        s = 1.0 + (Z - 1.0) * k * 0.9
        cw, ch = pre.width / s, pre.height / s
        x0 = (pre.width - cw) * (0.5 + (fx - 0.5) * 2 * k)
        y0 = (pre.height - ch) * (0.5 + (fy - 0.5) * 2 * k)
        x0, y0 = min(max(0, x0), pre.width - cw), min(max(0, y0), pre.height - ch)
        im = pre.resize((fw, fh), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))
        img.paste(im, (540 - fw // 2, int(cy - fh / 2)))
        paste(img, fr, 540, cy)
    items = [dyn]
    if label:
        t = T(th, "pacc", label, 44, 860)
        pl = th["panel"](t.width + 44, 72, "tag")
        items.append(S(pl, 540, cy - fh / 2 - 66, 0.1, "slide"))
        items.append(S(t, 540, cy - fh / 2 - 66, 0.1, "slide"))
    if credit:
        t = text_img(credit, "BarlowCondensed-ExtraBold.ttf", 34, "#ffffff", 4, "#000000")
        items.append(S(t, 540, cy + fh / 2 + bw + 40, 0.0, "none"))
    return items


def sc_quote(th, sc, dur):
    lines = wrapped(th, "pbig", sc["quote"], sc.get("size", 82), 820, 5)
    lh = lines[0].height + 12
    h = 150 + len(lines) * lh + (90 if sc.get("by") else 30)
    top = MID - h / 2
    items = [panel(th, 940, h), S(I(th, "quote-left", 72, "pacc"), 150, top + 80, 0.05)]
    for j, im in enumerate(lines):
        items.append(S(im, 540, top + 150 + j * lh + lh / 2 - 20, 0.15 + j * 0.12, "slide"))
    if sc.get("by"):
        items.append(S(T(th, "psmall", sc["by"], 48, 820), 540, top + h - 62, 0.5, "slide"))
    return items


def sc_timeline(th, sc, dur):
    rows = sc["rows"]            # [year, text]
    n = len(rows)
    rowh = 150 if n <= 3 else 132
    h = 60 + n * rowh + 30
    top = MID - h / 2
    items = [panel(th, 940, h)]
    acc = rgb(th["text"]["pacc"][2])
    pts = []
    for j, (yr, txt) in enumerate(rows):
        y = top + 60 + j * rowh + rowh / 2 - 20
        t0 = 0.15 + j * min(0.9, dur * 0.6 / n)
        items.append(S(T(th, "pacc", str(yr), 84, 250), 150, y, t0, "pop", "l"))
        items.append(S(T(th, "pbig", txt, 58, 500), 440, y, t0 + 0.08, "slide", "l"))
        pts.append((y, t0))

    def dyn(img, lt):
        d = ImageDraw.Draw(img)
        for j, (y, t0) in enumerate(pts):
            if lt >= t0:
                d.ellipse([398 - 11, y - 11, 398 + 11, y + 11], fill=acc)
                if j:
                    d.line([(398, pts[j - 1][0]), (398, y)], fill=acc, width=5)
    items.insert(1, dyn)
    return items


def sc_vs(th, sc, dur):
    items = []
    for j, (label, val, sub) in enumerate((sc["left"], sc["right"])):
        cx = 262 if j == 0 else 818
        t0 = 0.1 + j * 0.5
        items.append(S(th["panel"](404, 520, "main"), cx, MID, t0, "slide"))
        items.append(S(T(th, "psmall", label, 46, 350), cx, MID - 170, t0 + 0.1, "slide"))
        items.append(S(T(th, "pbig" if j == 0 else "pacc", val, 150, 350), cx, MID - 10, t0 + 0.2))
        items.append(S(T(th, "psmall", sub, 44, 350), cx, MID + 160, t0 + 0.3, "slide"))
    items.append(S(T(th, "acc", "VS", 74), 540, MID, 0.7))
    return items


def sc_outro(th, sc, dur):
    """Question, then the 'comment which game next' card, then the follow button. "cta": "" hides the card."""
    cta = sc.get("cta", "COMMENT FOR WHICH GAME WE SHOULD REVIEW NEXT!")
    q = wrapped(th, "big", sc["question"], sc.get("size", 118), 950, 3 if cta else 4)
    qh = sum(im.height for im in q) + 16 * (len(q) - 1)
    t = T(th, "pacc", "FOLLOW FOR MORE", 74, 760)
    pl = th["panel"](t.width + 96, 132, "tag")
    if cta:
        cl = wrapped(th, "pbig", cta, 60, 780, 3)
        ch = sum(im.height for im in cl) + 10 * (len(cl) - 1)
        ic = I(th, "comment-dots", 84, "pacc")
        ph = ch + 70
        card = th["panel"](940, int(ph), "main")
        total = qh + 44 + ph + 44 + 132
    else:
        total = qh + 74 + 132
    top = max(412, MID - 20 - total / 2)
    items = stack([(im, 0.05 + j * 0.15, "pop") for j, im in enumerate(q)], top + qh / 2, 16)
    y = top + qh
    tc = min(max(0.9, dur * 0.28), 2.4)
    tf = min(max(tc + 0.8, dur * 0.72), tc + 3.2) if cta else 0.6
    if cta:
        cy = y + 44 + ph / 2
        items.append(S(card, 540, cy, tc, "slide"))
        items.append(S(ic, 540 - 470 + 88, cy, tc + 0.1, "pop"))
        items += stack([(im, tc + 0.12 + j * 0.1, "pop") for j, im in enumerate(cl)], cy, 10)
        for e in items[-len(cl):]:
            e["x"] = 540 + 62
        y = cy + ph / 2
        by = y + 44 + 66
    else:
        by = y + 74 + 66

    def dyn(img, lt):
        if lt < tf:
            return
        s = back(min(1.0, (lt - tf) / 0.3)) * (1 + 0.035 * math.sin(lt * 7))
        paste(img, pl, 540, by, s)
        paste(img, t, 540, by, s)
    items.append(dyn)
    return items


KINDS = {"title": lambda th, sc, d: sc_text(th, sc, d, True), "text": sc_text, "stat": sc_stat, "list": sc_list, "bars": sc_bars,
         "photo": sc_photo, "quote": sc_quote, "timeline": sc_timeline, "vs": sc_vs, "outro": sc_outro}


def header(th, ep):
    im = Image.new("RGBA", (W, 360), (0, 0, 0, 0))
    l1, l2 = T(th, "pbig", SERIES[0], 60, 780), T(th, "pacc", SERIES[1], 42, 780)
    pl = th["panel"](max(l1.width, l2.width) + 90, 138, "tag")
    im.alpha_composite(pl, (540 - pl.width // 2, 196 - pl.height // 2))
    im.alpha_composite(l1, (540 - l1.width // 2, 170 - l1.height // 2))
    im.alpha_composite(l2, (540 - l2.width // 2, 230 - l2.height // 2))
    tag = T(th, th.get("tag_role", "acc"), ep["game"], 50, 900)
    im.alpha_composite(tag, (540 - tag.width // 2, 312 - tag.height // 2))
    return im


# ============================================================ captions
def chunks_for(text):
    out, cur = [], []
    for w in text.split():
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
    tot, res, t = sum(wts), [], t0
    for w, k in zip(words, wts):
        dt = (t1 - t0) * k / tot
        res.append((w, t, t + dt))
        t += dt
    return res


def draw_caption(th, img, line, t0, t1, now):
    cs = th["cap"]
    wt, chs, idx = word_times(line, t0, t1), chunks_for(line), 0
    for ch in chs:
        seg = wt[idx: idx + len(ch)]
        start, end = seg[0][1], seg[-1][2]
        if start - 0.02 <= now < end + 0.25 or (ch is chs[-1] and now >= start):
            box = cs.get("box")
            sw = 0 if box else int(cs["size"] * 0.09)
            ims, curs = [], []
            for (w, a, b) in seg:
                cur = a <= now < b + (0.25 if (w, a, b) == seg[-1] else 0)
                ims.append(text_img(w.upper(), cs["font"], cs["size"], cs["hi"] if cur else cs["fill"], sw, cs["stroke"], cs.get("wght"), line=True))
                curs.append(cur)
            sp = int(cs["size"] * 0.24)
            tw = sum(i.width - 12 for i in ims) + sp * (len(ims) - 1)
            sc = min(1.0, 980 / max(1, tw))
            k = back(min(1.0, (now - start) / 0.16)) if now - start < 0.16 else 1.0
            if box:
                hh = ims[0].height * sc
                ImageDraw.Draw(img).rectangle([540 - tw * sc / 2 - 30, CAP_Y - hh / 2 - 6, 540 + tw * sc / 2 + 30, CAP_Y + hh / 2 + 6], fill=rgb(box))
            x = 540 - tw * sc / 2
            for im, cur in zip(ims, curs):
                paste(img, im, x + (im.width - 12) * sc / 2, CAP_Y, sc * (1.07 if cur else 1.0) * k)
                x += (im.width - 12 + sp) * sc
            return
        idx += len(ch)


# ============================================================ voice + audio
def synth_lines(ep, speed):
    sr, clips = 24000, []
    for ln in ep["lines"]:
        text = ln.get("say", ln["t"])
        key = hashlib.md5(f"{text}|{ep.get('voice', 'am_michael')}|{speed:.3f}|{json.dumps(ep.get('pron', {}), sort_keys=True)}".encode()).hexdigest()
        fn = WORK + key + ".npy"
        if os.path.exists(fn):
            a = np.load(fn)
        else:
            a, sr = tts.say(text, ep.get("voice", "am_michael"), speed, ep.get("pron"))
            np.save(fn, a)
        clips.append(a)
    return clips, sr


def build_voice(ep):
    target, speed = ep["target"], ep.get("speed", 1.12)
    gap, lead, tail = 0.16, 0.3, 1.2
    for _ in range(3):
        clips, sr = synth_lines(ep, speed)
        total = lead + sum(len(c) / sr for c in clips) + gap * (len(clips) - 1) + tail
        if total > target + 1.0 and speed < 1.32:
            speed = min(1.32, speed * total / (target + 0.3))
            continue
        break
    timing, parts, t = [], [np.zeros(int(sr * lead), np.float32)], lead
    for c in clips:
        timing.append([t, t + len(c) / sr])
        parts += [c, np.zeros(int(sr * gap), np.float32)]
        t += len(c) / sr + gap
    audio = np.concatenate(parts)
    end = t - gap + tail
    audio = np.concatenate([audio, np.zeros(max(0, int(end * sr) - len(audio)), np.float32)])
    audio = audio / np.max(np.abs(audio)) * 0.92
    write_wav(WORK + f"{ep['slug']}_voice.wav", audio, sr)
    return timing, end, speed


def write_wav(fn, a, sr):
    with wave.open(fn, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((np.clip(a, -1, 1) * 32767).astype(np.int16).tobytes())


def sfx_track(starts, end):
    sr = music2.SR
    a = np.zeros(int((end + 1) * sr), np.float32)
    for i, s in enumerate(starts[1:]):
        n = int(0.18 * sr)
        t = np.arange(n) / sr
        f = 320 + 700 * t / 0.18
        w = np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-t * 16) * 0.16
        nz = np.random.default_rng(i).uniform(-1, 1, n) * np.sin(np.pi * t / 0.18) ** 2 * 0.07
        p = int(max(0, s - 0.06) * sr)
        a[p:p + n] += (w + nz)[: len(a) - p]
    return a[: int(end * sr)]


# ============================================================ main
def render(ep, mode="video", arg=None):
    os.makedirs(WORK, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    th = THEMES[ep["theme"]]
    st = {"static": th["static"]()}
    timing, END, speed = build_voice(ep)
    NF = int(END * FPS)
    starts = [0.0] + [timing[i][0] - 0.08 for i in range(1, len(timing))]
    hdr = header(th, ep)
    flash = Image.new("RGB", (W, H), rgb(th["flash"]))
    cache = {}

    def scene(i):
        if i not in cache:
            cache.clear()
            nxt = starts[i + 1] if i + 1 < len(starts) else END
            sc = ep["lines"][i]["sc"]
            cache[i] = KINDS[sc.get("kind", "text")](th, sc, nxt - starts[i])
        return cache[i]

    def frame(fi):
        now = fi / FPS
        i = max(j for j in range(len(starts)) if starts[j] <= now)
        lt, prog = now - starts[i], now / END
        img = th["base"](now, prog, END, st) if "base" in th else st["static"].copy()
        th["dyn"](img, ImageDraw.Draw(img), now, prog, END, st)
        draw_items(img, scene(i), lt)
        img.paste(hdr, (0, 0), hdr)
        t0, t1 = timing[i]
        if now >= t0 - 0.05:
            draw_caption(th, img, ep["lines"][i]["t"], t0, t1, now)
        if i > 0 and lt < 0.12:
            img = Image.blend(img, flash, 0.5 * (1 - lt / 0.12))
        return img

    if mode == "frame":
        i = int(arg)
        frame(int((starts[i] + (timing[i][1] - starts[i]) * 0.7) * FPS)).save(WORK + f"frame_{ep['slug']}_{i}.png")
        print("frame", WORK + f"frame_{ep['slug']}_{i}.png")
        return
    if mode == "sheet":
        thumbs = [frame(int((starts[i] + (timing[i][1] - starts[i]) * 0.72) * FPS)).resize((270, 480), Image.LANCZOS) for i in range(len(ep["lines"]))]
        cols = min(8, len(thumbs))
        rows = math.ceil(len(thumbs) / cols)
        s = Image.new("RGB", (270 * cols, 480 * rows), (0, 0, 0))
        for k, t in enumerate(thumbs):
            s.paste(t, ((k % cols) * 270, (k // cols) * 480))
        s.save(WORK + f"sheet_{ep['slug']}.png")
        print("sheet", ep["slug"], f"{END:.1f}s speed {speed:.2f}")
        return

    vid = WORK + f"{ep['slug']}_video.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p", vid], stdin=subprocess.PIPE)
    for fi in range(NF):
        p.stdin.write(frame(fi).tobytes())
    p.stdin.close()
    p.wait()
    write_wav(WORK + f"{ep['slug']}_music.wav", music2.make(END, ep.get("music", ep["theme"]), ep["num"]), music2.SR)
    write_wav(WORK + f"{ep['slug']}_sfx.wav", sfx_track(starts, END), music2.SR)
    final = OUT + ep["file"]
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", WORK + f"{ep['slug']}_voice.wav", "-i", WORK + f"{ep['slug']}_music.wav",
                    "-i", WORK + f"{ep['slug']}_sfx.wav", "-filter_complex",
                    "[1:a]aresample=44100,volume=1.5,asplit=2[vo1][vo2];[2:a]volume=0.30[mu];"
                    "[mu][vo1]sidechaincompress=threshold=0.05:ratio=6:attack=20:release=300[md];"
                    "[md][vo2][3:a]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.95[aout]",
                    "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", final], check=True)
    print("done", final, f"{END:.1f}s speed {speed:.2f}")


if __name__ == "__main__":
    path = sys.argv[1]
    ep = json.load(open(path))
    ep.setdefault("slug", os.path.splitext(os.path.basename(path))[0])
    render(ep, sys.argv[2] if len(sys.argv) > 2 else "video", sys.argv[3] if len(sys.argv) > 3 else None)
