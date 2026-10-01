"""Chiptune backing track generator (original composition)."""
import sys, wave
import numpy as np

SR = 44100
BPM = float(sys.argv[3]) if len(sys.argv) > 3 else 150
TR = int(sys.argv[4]) if len(sys.argv) > 4 else 0
SEED = int(sys.argv[5]) if len(sys.argv) > 5 else 0
beat = 60 / BPM
dur = float(sys.argv[1]) if len(sys.argv) > 1 else 32
out = sys.argv[2] if len(sys.argv) > 2 else "music.wav"
N = int(SR * dur)
mix = np.zeros(N)

def note_hz(n):  # midi -> hz
    return 440 * 2 ** ((n + TR - 69) / 12)

def square(f, t, duty=0.25):
    return np.where((f * t) % 1 < duty, 1.0, -1.0)

def tri(f, t):
    return 2 * np.abs(2 * ((f * t) % 1) - 1) - 1

def add(sig, start, gain):
    s = int(start * SR)
    if s >= N: return
    e = min(N, s + len(sig))
    mix[s:e] += sig[: e - s] * gain

def env(n, a=0.005, r=0.08):
    t = np.arange(n) / SR
    e = np.minimum(1, t / a)
    tail = np.clip((n / SR - t) / r, 0, 1)
    return e * tail

# chords (root midi, minor/major triad), one bar each: Em C G D
PROGS = [[(52, [0, 3, 7]), (48, [0, 4, 7]), (55, [0, 4, 7]), (50, [0, 4, 7])],
         [(52, [0, 3, 7]), (50, [0, 4, 7]), (48, [0, 4, 7]), (47, [0, 4, 7])],
         [(48, [0, 4, 7]), (55, [0, 4, 7]), (57, [0, 3, 7]), (53, [0, 4, 7])],
         [(57, [0, 3, 7]), (53, [0, 4, 7]), (48, [0, 4, 7]), (55, [0, 4, 7])]]
prog = PROGS[SEED % 4]
bar = beat * 4
nbars = int(dur / bar) + 1
rng = np.random.default_rng(3)
noise_src = rng.uniform(-1, 1, SR)

# lead melody (two-bar phrases, 8th notes, in E minor) - original
_mel = [64, 67, 71, 67, 72, 71, 67, 64,  60, 64, 67, 72, 71, 67, 64, 62,
       67, 71, 74, 71, 79, 78, 74, 71,  66, 69, 74, 78, 76, 74, 71, 69]
mrng = np.random.default_rng(SEED)
mel = []
for b_ in range(4):
    r_, iv_ = prog[b_]
    pool = [r_ + 12 + x for x in iv_] + [r_ + 24 + x for x in iv_]
    if SEED:
        steps = list(mrng.choice(pool, 4)); mel += [steps[0], steps[1], steps[0], steps[2], steps[3], steps[2], steps[1], steps[0]]
    else:
        mel += _mel[b_ * 8:b_ * 8 + 8]

for b in range(nbars):
    root, tri_iv = prog[b % 4]
    t0 = b * bar
    # bass: 8th-note octave bounce (triangle)
    for i in range(8):
        n = root - 12 + (12 if i % 2 else 0)
        L = int(SR * beat / 2 * 0.9)
        t = np.arange(L) / SR
        add(tri(note_hz(n), t) * env(L, r=0.03), t0 + i * beat / 2, 0.30)
    # arpeggio (fast 16ths, thin square)
    for i in range(16):
        n = root + 12 + tri_iv[i % 3]
        L = int(SR * beat / 4 * 0.8)
        t = np.arange(L) / SR
        add(square(note_hz(n), t, 0.125) * env(L, r=0.02), t0 + i * beat / 4, 0.06)
    # lead from bar 2 on
    if b >= 2:
        phrase = mel[(b % 4) * 8:(b % 4) * 8 + 8]
        for i, n in enumerate(phrase):
            L = int(SR * beat / 2 * 0.85)
            t = np.arange(L) / SR
            vib = 1 + 0.004 * np.sin(2 * np.pi * 6 * t)
            add(square(note_hz(n) * vib, t, 0.25) * env(L, r=0.04), t0 + i * beat / 2, 0.11)
    # drums
    for q in range(4):
        tq = t0 + q * beat
        # kick on 1 and 3
        if q % 2 == 0:
            L = int(SR * 0.15); t = np.arange(L) / SR
            f = 150 * np.exp(-t * 30) + 45
            add(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 18), tq, 0.55)
        else:  # snare
            L = int(SR * 0.12); t = np.arange(L) / SR
            add(noise_src[:L] * np.exp(-t * 28), tq, 0.28)
        # hats on 8ths
        for h in range(2):
            L = int(SR * 0.03); t = np.arange(L) / SR
            add(noise_src[1000:1000 + L] * np.exp(-t * 120), tq + h * beat / 2, 0.10)

# fade out last 1.2s
fade = int(SR * 1.2)
mix[-fade:] *= np.linspace(1, 0, fade)
mix = mix / np.max(np.abs(mix)) * 0.8
with wave.open(out, "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes())
print("music ok", dur)
