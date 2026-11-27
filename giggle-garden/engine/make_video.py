"""Render one Giggle Garden Short (doc 4.2, 4.4-4.6). 1080x1920 30 fps.
usage: python make_video.py songs.json gen_dir out_dir id [id...]   (needs gen/<id>_timing.json)
       python make_video.py sheet songs.json gen_dir out_dir id     (contact sheet only, doc 4.7)"""
import sys, os, json, math, re, random, subprocess
import numpy as np, cv2
from PIL import Image, ImageDraw
from multiprocessing import Pool
from engine import *
from scenes import background, anim

FPS = 30
COUNT = {'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9,'ten':10}
SHAPES = ('circle','square','star','triangle','heart')

def syl(w):
    w = re.sub(r"[^a-z]", "", w.lower())
    if not w: return 1
    if len(w) > 2 and w.endswith('e') and not w.endswith('le'): w = w[:-1]
    return max(1, len(re.findall(r"[aeiouy]+", w)))

def build_timeline(song, tm):
    lines = [l for v in song['verses'] for l in v['lines']]
    starts = tm['starts']
    sy = [sum(syl(w) for w in l.split()) for l in lines]
    rates = []
    for i in range(len(lines) - 1):
        rates.append((starts[i+1] - starts[i]) / max(1, sy[i]))
    rate = float(np.clip(np.median(rates) if rates else 0.35, 0.22, 0.6))
    L = []
    for i, ln in enumerate(lines):
        nxt = starts[i+1] - 0.12 if i + 1 < len(lines) else tm.get('audio_end', 1e9) - 1.0
        end = min(nxt, starts[i] + sy[i] * rate * 1.35 + 0.3)
        end = max(end, starts[i] + 0.6)
        ws = ln.split(); per = (end - starts[i]) / max(1, sy[i]); t = starts[i]; words = []; sylls = []
        for w in ws:
            n = syl(w); words.append((w, t, t + n * per))
            for k in range(n): sylls.append((t + k * per, per))
            t += n * per
        L.append(dict(text=ln, start=starts[i], end=end, words=words, sylls=sylls))
    # verse/scene index per line
    vi = [];
    for k, v in enumerate(song['verses']): vi += [k] * len(v['lines'])
    # line appear times
    for i, l in enumerate(L):
        l['appear'] = max(L[i-1]['end'] + 0.1, l['start'] - 0.8) if i else l['start'] - 0.8
    # scenes
    sc = []
    for k, v in enumerate(song['verses']):
        first = L[vi.index(k)]['start']; st = 0.0 if k == 0 else max(first - 0.55, sc[-1][0] + 1.0)
        sc.append((st, v['scene']))
    last_end = L[-1]['end']
    dur = min(last_end + 3.2, tm.get('audio_len', 999))
    return dict(lines=L, scenes=sc, vi=vi, beats=tm['beats'], yay=last_end + 0.35, dur=dur, title=song['title'],
                lullaby=song.get('style') == 'lullaby')

def scene_at(T, t):
    cur = T['scenes'][0]; idx = 0
    for i, s in enumerate(T['scenes']):
        if t >= s[0]: cur = s; idx = i
    return idx, cur

def beat_phase(beats, t, off=0.0):
    if len(beats) < 2: p = (t * 1.6) % 1; return p, int(t * 1.6)
    period = float(np.median(np.diff(beats)))
    tt = t - off * period
    i = int(np.searchsorted(beats, tt) - 1)
    if i < 0: return 0.0, 0
    if i >= len(beats) - 1:
        p = ((tt - beats[-1]) / period) % 1; return p, len(beats) - 1 + int((tt - beats[-1]) / period)
    return (tt - beats[i]) / (beats[i+1] - beats[i]), i

def mouth_open(T, t, scale=1.0):
    for l in T['lines']:
        if l['start'] - 0.05 <= t <= l['end'] + 0.1:
            for s0, ln in l['sylls']:
                Ls = min(0.9 * ln, 0.4); dt = t - s0
                if 0 <= dt < Ls: return scale * math.sin(math.pi * dt / Ls) ** 0.6
    return 0.0

def draw_chars(img, T, t, scene, close):
    beats = T['beats']
    lay = [('chick', 190, 1500, 0.6, 0.25, 55), ('froggy', 890, 1500, 0.6, 0.5, 55), ('bunny', 540, 1525, 0.9, 0.0, 85)]
    if close: lay = [('chick', 120, 1500, 0.55, 0.25, 55), ('froggy', 960, 1500, 0.55, 0.5, 55), ('bunny', 540, 1540, 1.08, 0.0, 85)]
    floaty = scene in ('space', 'underwater'); moon = scene == 'moon'
    for k, (nm, x, y, s, off, h) in enumerate(lay):
        p, _ = beat_phase(beats, t, off)
        if moon: h *= 1.8
        jump = h * 4 * p * (1 - p)
        if floaty: jump = 60 + 30 * math.sin(t * 1.5 + k)
        sy = 1 - 0.1 * math.cos(2 * math.pi * p); sx = 1 / sy ** 0.7
        if not floaty: shadow(img, x, y, s, jump)
        blink = ((t + k * 1.03) % 3.1) < 0.16
        m = mouth_open(T, t, 1.0 if nm == 'bunny' else 0.85)
        r = Rig(x, y, s, sx, sy, jump, t + k, m, blink,
                helmet=(nm == 'bunny' and scene in ('underwater', 'space', 'moon')),
                umbrella=(nm == 'bunny' and scene == 'rain'))
        {'bunny': bunny, 'chick': chick, 'froggy': froggy}[nm](img, r)

def pops(img, T, t):
    beats = T['beats']; rnd = random.Random(7)
    for i, b in enumerate(beats):
        dt = t - b
        if 0 <= dt < 1.1:
            r2 = random.Random(i)
            for k in range(2):
                x = r2.uniform(150, 930); y = 1150 - dt * 220 - r2.uniform(0, 80); s = 18 * (1 - dt / 1.1) + 6
                col = PALETTE[(i + k) % 6]
                if (i + k) % 2: poly(img, star_pts(x, y, s, dt * 2), col)
                else: poly(img, heart_pts(x, y, s), col)
    # music notes on every other syllable
    for l in T['lines']:
        for j, (s0, ln) in enumerate(l['sylls']):
            if j % 2: continue
            dt = t - s0
            if 0 <= dt < 1.2:
                x = 540 + 120 * math.sin(s0 * 7) + 30 * math.sin(dt * 5); y = 1050 - dt * 250
                col = PALETTE[j % 6]
                ell(img, (x, y), (16, 12), col, -20); line(img, (x + 14, y), (x + 14, y - 50), col, 5)
                line(img, (x + 14, y - 50), (x + 34, y - 38), col, 5)

def circle_wipe(cur, prev, p):
    if p >= 1: return cur
    r = 1300 * ease_out(p); out = prev.copy()
    mask = np.zeros((H, W), np.uint8); cv2.circle(mask, (540, 1100), int(r), 255, -1, cv2.LINE_AA)
    m = (mask[..., None] / 255.0)
    out = (cur * m + prev * (1 - m)).astype(np.uint8)
    cv2.circle(out, (540, 1100), int(r), (255, 255, 255), 14, cv2.LINE_AA)
    for k in range(12):
        a = k * math.pi / 6 + p * 4
        x = 540 + r * math.cos(a); y = 1100 + r * math.sin(a)
        if -50 < x < W + 50 and -50 < y < H + 50: poly(out, star_pts(x, y, 26, p * 6), PALETTE[k % 6])
    return out

def scene_frame(T, t, idx, name):
    img = background(name).copy()
    ctx = {'beats': T['beats'], 'beat_i': beat_phase(T['beats'], t)[1]}
    if name == 'launch':
        cw = [w[1] for l in T['lines'] for w in l['words'] if re.sub('[^a-z]', '', w[0].lower()) in COUNT]
        past = [c for c in cw if c <= t]; ctx['count_t'] = past[-1] if past else None
        lw = [w[1] for l in T['lines'] for w in l['words'] if re.sub('[^a-z]', '', w[0].lower()) in ('zoom', 'hooray')]
        ctx['lift_t'] = lw[0] if lw else None
    anim(name, img, t, ctx)
    draw_chars(img, T, t, name, close=(idx % 2 == 1))
    pops(img, T, t)
    return img

def wrap_rows(text, sz):
    if text_w(text, sz, 13) <= 1000: return [text]
    ws = text.split(); cands = []
    for i in range(1, len(ws)):
        a, b = ' '.join(ws[:i]), ' '.join(ws[i:]); m = max(text_w(a, sz, 13), text_w(b, sz, 13))
        cands.append((m, a.endswith(','), [a, b]))
    best = min(cands, key=lambda c: c[0])
    commas = [c for c in cands if c[1] and c[0] <= max(1000, best[0] * 1.12)]
    return min(commas, key=lambda c: c[0])[2] if commas else best[2]

def overlay(img, T, t):
    pil = Image.fromarray(img); d = ImageDraw.Draw(pil)
    brand_tag(d); title_pill(d, T['title'])
    L = T['lines']
    # title card
    if t < L[0]['start'] - 0.35:
        ws = T['title'].split(); half = (len(ws) + 1) // 2
        rows = [' '.join(ws[:half]), ' '.join(ws[half:])] if len(ws) > 1 else ws
        k = ease_back(t / 0.5); bob = 10 * math.sin(t * 3)
        for j, r in enumerate(rows):
            sz = 120
            while text_w(r, sz, 12) > 980: sz -= 4
            sz = max(10, int(sz * k))
            draw_text(d, (W/2, 560 + j * 150 + bob), r, sz, YELLOW, NAVY, 12)
    # lyric line
    cur = None
    for i, l in enumerate(L):
        nxt_app = L[i+1]['appear'] if i + 1 < len(L) else T['yay']
        if l['appear'] <= t < nxt_app: cur = l
    if cur is not None:
        sz = 108
        rows = wrap_rows(cur['text'], sz)
        while max(text_w(r, sz, 13) for r in rows) > 1000 and sz > 50: sz -= 4; rows = wrap_rows(cur['text'], sz)
        pop = ease_back((t - cur['appear']) / 0.3); szp = max(10, sz * (0.6 + 0.4 * pop))
        wi = 0; words = cur['words']
        y0 = 480 - (len(rows) - 1) * sz * 0.6
        for ri, row in enumerate(rows):
            rw = row.split(); widths = [text_w(w, szp, 13) for w in rw]; sp = text_w(' ', szp)
            tot = sum(widths) + sp * (len(rw) - 1); x = W/2 - tot/2; y = y0 + ri * sz * 1.2
            for j, w in enumerate(rw):
                ws = words[wi][1] if wi < len(words) else 1e9
                sung = t >= ws; dt = t - ws
                bounce = -18 * math.sin(math.pi * min(1, dt / 0.3)) if 0 <= dt < 0.3 else 0
                d.text((x, y + bounce), w, font=font(szp), fill=YELLOW if sung else WHITE, stroke_width=13, stroke_fill=NAVY, anchor="lm")
                x += widths[j] + sp; wi += 1
        # badges
        line_words = [re.sub('[^a-z]', '', w[0].lower()) for w in words]
        nums = [(COUNT[w], words[j][1]) for j, w in enumerate(line_words) if w in COUNT]
        badge_y = y0 + len(rows) * sz * 1.2 + 40
        if nums:
            n = len(nums); gap = 130; x0 = W/2 - (n - 1) * gap / 2
            for j, (v, ts) in enumerate(nums):
                if t >= ts:
                    k = ease_back((t - ts) / 0.3); r = 52 * k
                    if r > 2:
                        cx = x0 + j * gap
                        d.ellipse((cx - r - 6, badge_y - r - 6, cx + r + 6, badge_y + r + 6), fill=WHITE)
                        d.ellipse((cx - r, badge_y - r, cx + r, badge_y + r), fill=PALETTE[v % 6])
                        draw_text(d, (cx, badge_y), str(v), max(8, int(64 * k)), WHITE, NAVY, 5)
        shp = [(w, words[j][1]) for j, w in enumerate(line_words) if w.rstrip('s') in SHAPES]
        if shp and t >= shp[0][1]:
            nm = shp[0][0].rstrip('s'); k = ease_back((t - shp[0][1]) / 0.3); r = 70 * k; cx, cy = W/2, badge_y + (130 if nums else 0)
            col = PALETTE[SHAPES.index(nm) % 6]
            if r > 2:
                if nm == 'circle': d.ellipse((cx-r, cy-r, cx+r, cy+r), fill=col, outline=WHITE, width=8)
                elif nm == 'square': d.rectangle((cx-r, cy-r, cx+r, cy+r), fill=col, outline=WHITE, width=8)
                elif nm == 'triangle': d.polygon([(cx, cy-r), (cx+r, cy+r*0.8), (cx-r, cy+r*0.8)], fill=col, outline=WHITE, width=8)
                elif nm == 'star': d.polygon(star_pts(cx, cy, r), fill=col, outline=WHITE, width=8)
                else: d.polygon(heart_pts(cx, cy, r), fill=col, outline=WHITE, width=8)
    # ending
    if t >= T['yay']:
        k = ease_back((t - T['yay']) / 0.4); s = 'Goodnight!' if T['lullaby'] else 'Yay!'
        draw_text(d, (W/2, 600 + 12 * math.sin(t * 4)), s, max(10, int(170 * k)), YELLOW, NAVY, 14)
    return np.array(pil)

def confetti(img, T, t):
    if t < T['yay']: return
    dt = t - T['yay']; rnd = random.Random(11)
    for k in range(70):
        x = rnd.uniform(0, W) + 40 * math.sin(dt * 2 + k); y = -50 + (rnd.uniform(0, 600) + dt * (300 + k % 5 * 60))
        if y > H: continue
        if T['lullaby']: poly(img, star_pts(x, y, 14, dt + k), (255, 245, 180))
        else: rect(img, x, y, x + 16, y + 26, PALETTE[k % 6])


def hype(img, T, t):
    """Extra visual stimulation: beat zoom pulse, rainbow rings, twinkling sparkles, animated rainbow side stripes."""
    if os.environ.get('GG_HYPE', '1') != '1': return img
    p, bi = beat_phase(T['beats'], t)
    z = 1 + 0.04 * max(0.0, 1 - p * 3.0)
    if z > 1.001:
        M = np.array([[z, 0, 540 * (1 - z)], [0, z, 1100 * (1 - z)]], np.float32)
        img = cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    # rainbow rings from the bunny on each of the last two beats
    for k in range(2):
        b = bi - k
        if b < 0 or b >= len(T['beats']): continue
        dt = t - T['beats'][b]
        if 0 <= dt < 0.55:
            r = 90 + dt * 1100; th = max(1, int(16 * (1 - dt / 0.55)))
            cv2.circle(img, (540, 1250), int(r), PALETTE[b % 6][::-1] if False else PALETTE[b % 6], th, cv2.LINE_AA)
    # twinkling sparkles scattered around
    rnd = random.Random(5)
    for k in range(26):
        x = rnd.uniform(40, W - 40); y = rnd.uniform(260, 1450)
        s = 8 + 14 * abs(math.sin(t * 5 + k * 1.7))
        poly(img, star_pts(x, y, s, 0.3 * math.sin(t + k)), PALETTE[(k + bi) % 6])
    # animated rainbow stripes down both sides
    off = int(t * 9)
    for i in range(0, H, 80):
        col = PALETTE[((i // 80) + off) % 6]
        rect(img, 0, i, 18, i + 80, col); rect(img, W - 18, i, W, i + 80, col)
    return img

def render_frame(args):
    T, fi = args; t = fi / FPS
    idx, (st, name) = scene_at(T, t)
    img = scene_frame(T, t, idx, name)
    if idx > 0 and t - st < 0.5:
        prev = scene_frame(T, t, idx - 1, T['scenes'][idx - 1][1])
        img = circle_wipe(img, prev, (t - st) / 0.5)
    img = hype(img, T, t)
    confetti(img, T, t)
    return overlay(img, T, t).tobytes()

def load(songs_path, gd, sid):
    songs = {s['id']: s for s in json.load(open(songs_path))}
    tm = json.load(open(f"{gd}/{sid}_timing.json"))
    if 'audio_len' not in tm:
        out = subprocess.run(['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration', '-of', 'csv=p=0', tm['mp3']], capture_output=True, text=True).stdout
        tm['audio_len'] = float(out.strip() or 999)
    return songs[sid], tm

def render(songs_path, gd, od, sid):
    song, tm = load(songs_path, gd, sid); T = build_timeline(song, tm)
    n = int(T['dur'] * FPS); out = f"{od}/{sid}.mp4"; os.makedirs(od, exist_ok=True)
    fade0 = max(0, T['dur'] - 0.9)
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
           '-i', tm['mp3'], '-t', f"{T['dur']:.3f}", '-af', f"loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=out:st={fade0:.3f}:d=0.9", '-map', '0:v', '-map', '1:a',
           '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000',
           '-movflags', '+faststart', out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with Pool(int(os.environ.get('GG_PROCS', '2'))) as pool:
        for fr in pool.imap(render_frame, ((T, i) for i in range(n)), chunksize=4): p.stdin.write(fr)
    p.stdin.close(); p.wait(); print('rendered', out, round(T['dur'], 2), flush=True)

def sheet(songs_path, gd, od, sid):
    song, tm = load(songs_path, gd, sid); T = build_timeline(song, tm)
    ts = [l['start'] + 0.6 for l in T['lines']] + [T['dur'] - 0.1]
    ims = [cv2.resize(np.frombuffer(render_frame((T, int(t * FPS))), np.uint8).reshape(H, W, 3), (270, 480)) for t in ts]
    while len(ims) % 4: ims.append(np.zeros_like(ims[0]))
    rows = [np.hstack(ims[i:i+4]) for i in range(0, len(ims), 4)]
    os.makedirs(od, exist_ok=True); Image.fromarray(np.vstack(rows)).save(f"{od}/{sid}_sheet.jpg", quality=80)
    print('sheet', f"{od}/{sid}_sheet.jpg", [round(t, 2) for t in ts])

if __name__ == '__main__':
    if sys.argv[1] == 'sheet': sheet(*sys.argv[2:6])
    else:
        for sid in sys.argv[4:]: render(sys.argv[1], sys.argv[2], sys.argv[3], sid)
