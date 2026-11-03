"""Long-form (16:9, 1920x1080) renderer for SparkCart deep-dive videos.

usage:  python3 engine/longform.py episodes/long/<episode>.json [--sheet] [--out DIR]

Built for speed on long videos: every line is one ffmpeg pass (real clip, slow Ken Burns drift,
PNG overlays for titles + captions), then the segments are joined and the audio is mixed in numpy.

Episode JSON ("preset": "long"):
  title, file, slug, voice, speed, accent, pron, music_vol (0.07), mood ("spooky")
  lines: [{ "t": caption/voice text, "say": optional spoken text,
            "beat": seconds   -> no narration: the clip plays with its OWN sound at full volume
            "sc": { "clip": asset, "start": s, "vol": clip level under the voice (0.10),
                    "chapter": "TITLE" (+ "chn": 3)  -> chapter card over a darkened clip,
                    "big": "BIG TEXT", "sub": "smaller line", "credit": "Doggie",
                    "dark": 0.25 (extra darkening) } }]
"""
import argparse, hashlib, json, math, os, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import art
from art import font, rgb
import tts, music

D = os.path.dirname(os.path.abspath(__file__)) + "/"
ROOT = os.path.dirname(D.rstrip("/")) + "/"
WORK, OUT = ROOT + "build/work/long/", ROOT + "build/out/"
W, H, FPS, SR = 1920, 1080, 30, 44100
MF = D + "modern/fonts/"
CAP_FONT, TITLE_FONT = "Lilita.ttf", "LuckiestGuy.ttf"
GAP = 0.32


# ------------------------------------------------------------------ text pictures
def _txt(txt, size, fill, fname, stroke, maxw=1720):
    return art.text_img(txt, size, rgb(fill), fname, stroke, maxw)


def overlay_png(path, sc, accent):
    """Static overlay for one line: chapter card / big title / credit."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if sc.get("chapter"):
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, W, H], fill=(5, 5, 12, 120))
        if sc.get("chn"):
            t = _txt(f"CHAPTER {sc['chn']}", 54, accent, CAP_FONT, 6)
            art.paste_center(im, t, W / 2, 400)
        for i, line in enumerate(sc["chapter"].split("\n")):
            art.paste_center(im, _txt(line, 128, "#ffffff", TITLE_FONT, 10), W / 2, 530 + i * 140)
        d.rectangle([W / 2 - 160, 470 + 140 * len(sc["chapter"].split("\n")) + 20, W / 2 + 160,
                     470 + 140 * len(sc["chapter"].split("\n")) + 30], fill=rgb(accent) + (255,))
    y = sc.get("by", 170)
    if sc.get("big"):
        for i, line in enumerate(sc["big"].split("\n")):
            art.paste_center(im, _txt(line, sc.get("bs", 120), sc.get("bc", "#ffffff"), TITLE_FONT, 10), W / 2, y + i * (sc.get("bs", 120) + 14))
        y += (len(sc["big"].split("\n")) - 1) * (sc.get("bs", 120) + 14)
    if sc.get("sub"):
        art.paste_center(im, _txt(sc["sub"], sc.get("ss", 56), sc.get("subc", accent), CAP_FONT, 7), W / 2, y + sc.get("bs", 120) * 0.5 + 60)
    if sc.get("credit"):
        t = _txt("footage: " + sc["credit"], 30, "#ffffff", CAP_FONT, 4, 900)
        t = t.copy()
        t.putalpha(t.getchannel("A").point(lambda a: int(a * 0.75)))
        im.alpha_composite(t, (W - t.width - 30, 26))
    im.save(path)


def chunks(text):
    words = text.split()
    out, cur = [], []
    for w in words:
        if cur and (len(" ".join(cur + [w])) > 42 or len(cur) >= 8):
            out.append(cur)
            cur = []
        cur.append(w)
        if w[-1] in ".!?" and len(cur) >= 3 or (w[-1] in ",:;" and len(cur) >= 5):
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def word_weights(words):
    return [len(w) + 3 * sum(ch.isdigit() for ch in w) + (5 if w[-1] in ",.!?" else 0) + 2 for w in words]


def caption_pngs(prefix, text, t0, t1):
    """One PNG per caption chunk, timed across [t0, t1] (segment-local seconds)."""
    out = []
    words = text.split()
    if not words:
        return out
    wts = word_weights(words)
    tot, t, idx = sum(wts), t0, 0
    for k, ch in enumerate(chunks(text)):
        dt = (t1 - t0) * sum(wts[idx: idx + len(ch)]) / tot
        idx += len(ch)
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        tx = _txt(" ".join(ch), 66, "#ffffff", CAP_FONT, 7, 1700)
        d = ImageDraw.Draw(im)
        cy = 960
        d.rounded_rectangle([W / 2 - tx.width / 2 - 26, cy - tx.height / 2 - 2, W / 2 + tx.width / 2 + 26, cy + tx.height / 2 - 6], 22, fill=(0, 0, 0, 120))
        art.paste_center(im, tx, W / 2, cy)
        p = f"{prefix}_c{k}.png"
        im.save(p)
        out.append((p, t, t + dt))
        t += dt
    return out


# ------------------------------------------------------------------ voice
def synth(ep, ln):
    txt = ln.get("say", ln["t"])
    key = hashlib.md5(f"{txt}|{ep['voice']}|{ep['speed']:.3f}|{json.dumps(ep.get('pron', {}), sort_keys=True)}".encode()).hexdigest()
    fn = WORK + key + ".npy"
    if os.path.exists(fn):
        return np.load(fn), 24000
    a, sr = tts.say(txt, ep["voice"], ep["speed"], ep.get("pron"))
    np.save(fn, a)
    return a, sr


def resample(a, sr):
    if sr == SR:
        return a
    n = int(len(a) * SR / sr)
    return np.interp(np.linspace(0, len(a) - 1, n), np.arange(len(a)), a).astype(np.float32)


def clip_audio(fu, dur):
    r = subprocess.run(["ffmpeg", "-loglevel", "error", "-stream_loop", "-1", "-ss", str(fu.get("start", 0)), "-t", f"{dur + 0.05:.3f}",
                        "-i", ROOT + "episodes/assets/" + fu["clip"], "-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True)
    seg = np.frombuffer(r.stdout, np.float32).copy()
    if not len(seg):
        return seg
    rms = float(np.sqrt(np.mean(seg ** 2)))
    if rms > 1e-4:
        seg *= min(6.0, 0.12 / rms)
    seg = np.tanh(seg * 1.2) / 1.2
    f = min(len(seg) // 2, int(0.06 * SR))
    if f:
        seg[:f] *= np.linspace(0, 1, f)
        seg[-f:] *= np.linspace(1, 0, f)
    return seg


# ------------------------------------------------------------------ main
def render(ep, sheet=False):
    os.makedirs(WORK, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    ep.setdefault("voice", "am_michael")
    ep.setdefault("speed", 1.0)
    accent = ep.get("accent", "#ff5252")
    lines = ep["lines"]

    # 1. timeline: voiced lines last as long as their voice (+ gap); beats last "beat" seconds
    voices, starts, t = [], [], 0.0
    for ln in lines:
        starts.append(t)
        if ln.get("beat"):
            voices.append(None)
            t += float(ln["beat"])
        else:
            a, sr = synth(ep, ln)
            a = resample(a, sr)
            voices.append(a)
            t += 0.12 + len(a) / SR + GAP
    END = t + 1.0
    starts.append(END)
    print(f"timeline {END:.1f}s, {len(lines)} lines")
    # YouTube chapters (description timestamps): 0:00 intro + every chapter card
    chs = ["0:00 Intro"] + [f"{int(starts[i] // 60)}:{int(starts[i] % 60):02d} " + ln["sc"]["chapter"].replace("\n", " ").title()
                            for i, ln in enumerate(lines) if ln["sc"].get("chapter")]
    open(OUT + ep["slug"] + "_chapters.txt", "w", encoding="utf-8").write("\n".join(chs) + "\n")
    print("\n".join(chs))

    # 2. video segments
    segs = []
    for i, ln in enumerate(lines):
        sc = ln["sc"]
        f0, f1 = round(starts[i] * FPS), round(starts[i + 1] * FPS)
        n = f1 - f0
        dur = n / FPS
        pre = WORK + f"{ep['slug']}_{i:03d}"
        ov = pre + "_ov.png"
        overlay_png(ov, sc, accent)
        caps = [] if ln.get("beat") or sc.get("nocap") else caption_pngs(pre, ln["t"], 0.12, 0.12 + len(voices[i]) / SR)
        side = 1 if i % 2 == 0 else -1
        dark = sc.get("dark", 0.0) + (0.28 if sc.get("chapter") else 0.0)
        vf = (f"[0:v]fps={FPS},scale={W + 120}:{H + 68}:force_original_aspect_ratio=increase,"
              f"crop={W}:{H}:x='(iw-{W})/2+{side}*55*(t/{dur:.3f}-0.5)':y='(ih-{H})/2',setsar=1"
              + (f",eq=brightness=-{dark:.2f}" if dark else "") + "[b0];[b0][1:v]overlay=0:0[v0]")
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-stream_loop", "-1", "-ss", str(sc.get("start", 0)),
               "-i", ROOT + "episodes/assets/" + sc["clip"], "-loop", "1", "-i", ov]
        for k, (p, a, b) in enumerate(caps):
            cmd += ["-loop", "1", "-i", p]
            vf += f";[v{k}][{k + 2}:v]overlay=0:0:enable='between(t,{a:.3f},{b:.3f})'[v{k + 1}]"
        last = f"[v{len(caps)}]"
        if sheet:
            mid = dur * 0.5
            cmd += ["-filter_complex", vf, "-map", last, "-ss", f"{mid:.2f}", "-frames:v", "1", pre + "_sheet.png"]
        else:
            cmd += ["-filter_complex", vf, "-map", last, "-frames:v", str(n), "-an", "-c:v", "libx264", "-preset", "veryfast",
                    "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(FPS), pre + ".mp4"]
        subprocess.run(cmd, check=True)
        segs.append(pre + (".mp4" if not sheet else "_sheet.png"))
        if i % 10 == 0:
            print(f"  segment {i + 1}/{len(lines)}", flush=True)

    if sheet:
        cols, tw, th = 5, 384, 216
        s = Image.new("RGB", (tw * cols, th * math.ceil(len(segs) / cols)))
        for k, p in enumerate(segs):
            s.paste(Image.open(p).convert("RGB").resize((tw, th)), ((k % cols) * tw, (k // cols) * th))
        s.save(WORK + f"sheet_{ep['slug']}.png")
        print("sheet", WORK + f"sheet_{ep['slug']}.png")
        return

    lst = WORK + f"{ep['slug']}_list.txt"
    with open(lst, "w") as f:
        for p in segs:
            f.write(f"file '{p}'\n")
    vid = WORK + f"{ep['slug']}_video.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", vid], check=True)

    # 3. audio: voice + real clip sound (loud in beats, low under the voice) + quiet music
    N = int((END + 1) * SR)
    vo, ca = np.zeros(N, np.float32), np.zeros(N, np.float32)
    for i, ln in enumerate(lines):
        p = int(starts[i] * SR)
        dur = starts[i + 1] - starts[i]
        if voices[i] is not None:
            v = voices[i]
            q = p + int(0.12 * SR)
            vo[q:q + len(v)] += v[: N - q]
        seg = clip_audio(ln["sc"], dur)
        if len(seg):
            g = 1.0 if ln.get("beat") else ln["sc"].get("vol", ep.get("clip_vol", 0.10))
            ca[p:p + len(seg)] += seg[: N - p] * g
    vo = vo / (np.max(np.abs(vo)) or 1) * 0.9
    mus = music.make(END, seed=ep.get("num", 1), bpm=ep.get("bpm", 92), root=ep.get("root", 57), mood=ep.get("mood", "spooky"))
    mus = np.asarray(mus, np.float32)[:N]
    mus = np.pad(mus, (0, N - len(mus)))
    # duck music under the voice
    env = np.convolve(np.abs(vo), np.ones(4410) / 4410, mode="same")
    mus *= ep.get("music_vol", 0.07) * np.clip(1.0 - env * 6, 0.45, 1.0)
    mix = vo + ca * 0.85 + mus
    mix = np.tanh(mix * 1.1) / 1.1
    mix = mix / max(np.max(np.abs(mix)), 1e-6) * 0.95
    wav = WORK + f"{ep['slug']}_mix.wav"
    with wave.open(wav, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((mix[: int(END * SR)] * 32767).astype(np.int16).tobytes())
    final = OUT + ep["file"]
    # chapters also embedded in the MP4 (readable later with ffprobe -show_chapters from any copy)
    meta = WORK + f"{ep['slug']}_meta.txt"
    cps = [(0.0, "Intro")] + [(starts[i], ln["sc"]["chapter"].replace("\n", " ").title()) for i, ln in enumerate(lines) if ln["sc"].get("chapter")]
    with open(meta, "w", encoding="utf-8") as f:
        f.write(";FFMETADATA1\n")
        for k, (a, name) in enumerate(cps):
            b = cps[k + 1][0] if k + 1 < len(cps) else END
            f.write(f"[CHAPTER]\nTIMEBASE=1/1000\nSTART={int(a * 1000)}\nEND={int(b * 1000)}\ntitle={name}\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", wav, "-i", meta, "-map", "0:v", "-map", "1:a", "-map_chapters", "2",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", final], check=True)
    for p in segs:
        os.remove(p)
    print("done", final, f"{END:.1f}s")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--sheet", action="store_true")
    ap.add_argument("--out")
    a = ap.parse_args()
    if a.out:
        OUT = os.path.abspath(a.out) + "/"
    e = json.load(open(a.episode))
    e.setdefault("slug", os.path.splitext(os.path.basename(a.episode))[0])
    render(e, a.sheet)
