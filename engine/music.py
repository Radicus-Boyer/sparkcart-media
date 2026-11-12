"""Original chiptune-pop music generator (square lead, triangle bass, noise drums)."""
import numpy as np

SR = 44100
PROGS = [[0, 7, 9, 5], [0, 5, 9, 7], [9, 5, 0, 7], [0, 9, 5, 7]]
MAJ = [0, 2, 4, 5, 7, 9, 11]


def sq(f, n, duty=0.25):
    t = np.arange(n) / SR
    return np.where((t * f) % 1.0 < duty, 1.0, -1.0)


def tri(f, n):
    t = np.arange(n) / SR
    return 2 * np.abs(2 * ((t * f) % 1.0) - 1) - 1


def env(n, a=0.005, r=0.08):
    e = np.ones(n)
    na, nr = int(a * SR), min(int(r * SR), n)
    if na:
        e[:na] = np.linspace(0, 1, na)
    e[-nr:] *= np.linspace(1, 0, nr)
    return e


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def make(seconds, seed=0, bpm=128, root=60, mood="happy"):
    if mood == "ambience":
        return ambience(seconds, seed)
    rng = np.random.default_rng(seed)
    prog = PROGS[seed % len(PROGS)]
    if mood == "spooky":
        prog = [9, 5, 4, 9]
    beat = 60.0 / bpm
    step = beat / 4
    n_total = int((seconds + 1) * SR)
    out = np.zeros(n_total)
    nstep = int(step * SR)
    steps = int(seconds / step) + 2
    # lead motif: 16 steps per bar, chosen per chord from chord tones
    motif = rng.integers(0, 3, 16)
    rest = rng.random(16) < 0.3
    for i in range(steps):
        bar = i // 16
        chord = prog[bar % 4]
        s0 = i * nstep
        if s0 >= n_total:
            break
        k = i % 16
        triad = [chord, chord + (3 if mood == "spooky" and chord == 9 else 4 if chord in (0, 5, 7) else 3), chord + 7]
        # lead
        if not rest[k] and bar >= 1:
            note = root + 12 + triad[motif[k]] + (12 if (k % 8 == 6 and bar % 2) else 0)
            n = int(nstep * 0.9)
            seg = sq(hz(note), n, 0.25 if mood != "spooky" else 0.125) * env(n, 0.003, 0.05) * 0.10
            out[s0:s0 + n] += seg[: max(0, n_total - s0)][:n]
        # arpeggio pad
        note = root + triad[i % 3]
        n = int(nstep * 0.8)
        seg = sq(hz(note), n, 0.5) * env(n, 0.002, 0.04) * 0.045
        out[s0:s0 + n] += seg[:n][: max(0, n_total - s0)]
        # bass on 8ths
        if k % 2 == 0:
            note = root - 24 + chord + (12 if k % 4 == 2 else 0)
            n = int(nstep * 1.8)
            seg = tri(hz(note), n) * env(n, 0.002, 0.05) * 0.22
            e = min(n, n_total - s0)
            out[s0:s0 + e] += seg[:e]
        # drums
        if bar >= 1 or k >= 12:
            if k % 8 == 0 or (mood != "spooky" and k == 10):
                n = int(0.16 * SR)
                t = np.arange(n) / SR
                kick = np.sin(2 * np.pi * (150 * t - 400 * t * t)) * np.exp(-t * 28) * 0.5
                e = min(n, n_total - s0)
                out[s0:s0 + e] += kick[:e]
            if k % 8 == 4:
                n = int(0.12 * SR)
                sn = rng.uniform(-1, 1, n) * np.exp(-np.arange(n) / SR * 30) * 0.22
                e = min(n, n_total - s0)
                out[s0:s0 + e] += sn[:e]
            if k % 2 == 1:
                n = int(0.03 * SR)
                hh = rng.uniform(-1, 1, n) * np.exp(-np.arange(n) / SR * 120) * 0.07
                e = min(n, n_total - s0)
                out[s0:s0 + e] += hh[:e]
    out = out[: int(seconds * SR)]
    fade = int(1.2 * SR)
    out[-fade:] *= np.linspace(1, 0, fade)
    out /= max(1e-6, np.max(np.abs(out)))
    return (out * 0.85).astype(np.float32)


def ambience(seconds, seed=0, root=45):
    """Dark horror ambience (batch 37, user Nov 12): detuned low drone, slow-swelling minor pad, filtered wind,
    a distant heartbeat every ~1.2s and an occasional high metallic ping. No melody, no drums."""
    rng = np.random.default_rng(seed)
    n = int((seconds + 1) * SR)
    t = np.arange(n) / SR
    f0 = hz(root - 12)
    drone = sum(np.sin(2 * np.pi * f0 * m * (1 + d) * t) / m for m, d in ((1, 0), (1, 0.004), (2, -0.003), (3, 0.002)))
    drone *= 0.55 + 0.45 * np.sin(2 * np.pi * t / 9.0)
    pad = sum(np.sin(2 * np.pi * hz(root + iv) * t + rng.uniform(0, 6)) for iv in (0, 3, 7, 13))
    pad *= (0.5 - 0.5 * np.cos(2 * np.pi * t / 14.0)) * 0.35
    w = rng.normal(0, 1, n)
    k = int(SR * 0.004)
    wind = np.convolve(w, np.ones(k) / k, mode="same")
    wind = np.convolve(wind, np.ones(k) / k, mode="same")
    wind *= (0.4 + 0.6 * np.abs(np.sin(2 * np.pi * t / 6.5 + 1.3))) * 6.0
    out = drone * 0.5 + pad + wind * 0.5
    beat = 1.2
    for b in np.arange(2.0, seconds, beat):
        for off, amp in ((0, 1.0), (0.22, 0.7)):
            s0 = int((b + off) * SR)
            m = int(0.18 * SR)
            tt = np.arange(m) / SR
            thump = np.sin(2 * np.pi * (55 - 30 * tt) * tt) * np.exp(-tt * 22) * amp * 0.9
            e = min(m, n - s0)
            if e > 0:
                out[s0:s0 + e] += thump[:e]
    for p0 in rng.uniform(3, max(4, seconds - 2), max(1, int(seconds / 9))):
        s0 = int(p0 * SR)
        m = int(2.5 * SR)
        tt = np.arange(m) / SR
        ping = np.sin(2 * np.pi * hz(root + 36 + int(rng.integers(0, 3))) * tt) * np.exp(-tt * 1.6) * 0.25
        e = min(m, n - s0)
        if e > 0:
            out[s0:s0 + e] += ping[:e]
    out = out[: int(seconds * SR)]
    fi, fo = int(0.6 * SR), int(1.2 * SR)
    out[:fi] *= np.linspace(0, 1, fi)
    out[-fo:] *= np.linspace(1, 0, fo)
    out /= max(1e-6, np.max(np.abs(out)))
    return (out * 0.85).astype(np.float32)
