"""Original background music for the 'popular' preset: one mood per game theme.
Small step-sequencer: pad + bass + pluck/arp + drums, different scale, tempo and sounds per style."""
import numpy as np

SR = 44100
SCALES = {
    "minor": [0, 2, 3, 5, 7, 8, 10], "harm": [0, 2, 3, 5, 7, 8, 11], "dorian": [0, 2, 3, 5, 7, 9, 10],
    "phryg": [0, 1, 3, 5, 7, 8, 10], "penta": [0, 3, 5, 7, 10], "insen": [0, 1, 5, 7, 10],
    "major": [0, 2, 4, 5, 7, 9, 11], "cpenta": [0, 2, 4, 7, 9],
}

# steps per bar is always 16 (waltz styles use 12). Patterns: x = hit, . = rest.
STYLES = {
    # tense, ticking, tactical
    "cs2": dict(bpm=100, root=38, scale="minor", prog=[0, 0, 5, 3], pad=("saw", 0.10, 60), bass=("x..x..x.x..x..x.", "sq", 0.22),
                arp=("0...2...1...2...", "bell", 0.07, 2), kick="x.......x..x....", snare="....x.......x...", hat="x.x.x.x.x.x.x.xx", tick=True),
    # galloping war drums + pentatonic lead
    "dw9": dict(bpm=150, root=40, scale="penta", prog=[0, 3, 4, 0], pad=("saw", 0.07, 35), bass=("x.xxx.xxx.xxx.xx", "saw", 0.20),
                arp=("0.2.4.2.3.2.4.2.", "pluck", 0.12, 2), kick="x...x...x...x...", snare="....x.......x.x.", hat="..x...x...x...x.", boom="x...............", dist=True),
    # slow, epic, dark
    "dota": dict(bpm=84, root=36, scale="minor", prog=[0, 5, 3, 4], pad=("saw", 0.16, 90), bass=("x.......x.......", "sine", 0.30),
                 arp=("0..2..4..2..0.2.", "bell", 0.06, 2), kick="", snare="", hat="", boom="x.........x.....", choir=True),
    # military snare march + drone
    "pubg": dict(bpm=112, root=38, scale="dorian", prog=[0, 0, 3, 4], pad=("saw", 0.10, 70), bass=("x...x...x...x.x.", "sq", 0.20),
                 arp=("....0.......2...", "bell", 0.06, 2), kick="x.......x.......", snare="..xxx.x...xxx.xx", hat="", boom="x...............", roll=True),
    # gritty, driving
    "wardogs": dict(bpm=126, root=36, scale="phryg", prog=[0, 0, 1, 0], pad=("saw", 0.08, 40), bass=("x.x.xx.xx.x.xx.x", "saw", 0.24),
                    arp=("0...0..1....0...", "sq", 0.05, 2), kick="x...x...x...x...", snare="....x.......x...", hat="xxxxxxxxxxxxxxxx", dist=True),
    # koto-like plucks, taiko
    "oni": dict(bpm=78, root=38, scale="insen", prog=[0, 0, 3, 0], pad=("saw", 0.07, 110), bass=("x...............", "sine", 0.26),
                arp=("0.1.2..3.2.1.0..", "pluck", 0.20, 2), kick="", snare="", hat="", boom="x.....x...x.....", wood="....x.......x...",),
    # gothic waltz, organ
    "dawn": dict(bpm=96, root=37, scale="harm", prog=[0, 3, 4, 0], steps=12, pad=("sq", 0.09, 60), bass=("x...x...x...", "sine", 0.26),
                 arp=("0.2.4.2.4.2.", "bell", 0.08, 2), kick="x...........", snare="", hat="....x...x...", boom="", choir=True),
    # minimal, eerie
    "control": dict(bpm=92, root=34, scale="phryg", prog=[0, 0, 0, 1], pad=("sine", 0.14, 1), bass=("x.....x.x.......", "sine", 0.34),
                    arp=("4.......3.......", "bell", 0.10, 3), kick="x.........x.....", snare="........x.......", hat="..x...x...x...x.", glitch=True),
    # punchy rock riff
    "wolv": dict(bpm=140, root=40, scale="minor", prog=[0, 0, 5, 6], pad=("saw", 0.06, 30), bass=("xx.xx.xx.xx.xxxx", "saw", 0.22),
                 arp=("0..0..2.0..0..3.", "sq", 0.09, 1), kick="x..x..x.x..x..x.", snare="....x.......x...", hat="x.x.x.x.x.x.x.x.", dist=True),
    # folk lute + hand drum
    "witcher": dict(bpm=104, root=38, scale="dorian", prog=[0, 6, 3, 4], pad=("saw", 0.06, 80), bass=("x.....x.x.......", "sine", 0.24),
                    arp=("0.2.4.2.1.2.4.2.", "pluck", 0.20, 2), kick="x.....x...x.....", snare="", hat="", wood="....x..x....x.x.", ),
    # ethereal: choir, harp-like plucks
    "aion": dict(bpm=88, root=41, scale="dorian", prog=[0, 3, 5, 4], pad=("saw", 0.14, 100), bass=("x.......x.......", "sine", 0.26),
                 arp=("0.2.4.6.4.2.0.2.", "pluck", 0.16, 2), kick="", snare="", hat="", boom="x...............", choir=True),
    # noir: walking bass, brushed hats
    "deadlock": dict(bpm=104, root=36, scale="harm", prog=[0, 3, 4, 0], pad=("saw", 0.07, 70), bass=("x...x...x...x.x.", "sine", 0.34),
                     arp=("....0..2....3.1.", "bell", 0.09, 2), kick="x.......x.......", snare="", hat="x..xx..xx..xx..x", wood="....x.......x..."),
    # soaring, driving
    "ace": dict(bpm=146, root=38, scale="minor", prog=[0, 5, 2, 6], pad=("saw", 0.10, 45), bass=("x.x.x.x.x.x.x.x.", "saw", 0.20),
                arp=("0...2...4...2.4.", "sq", 0.10, 2), kick="x...x...x...x...", snare="....x.......x...", hat="..x...x...x...x.", dist=True),
    # cozy waltz
    "dress": dict(bpm=108, root=43, scale="major", prog=[0, 3, 4, 0], steps=12, pad=("tri", 0.08, 40), bass=("x...........", "sine", 0.26),
                  arp=("0...2.4.2.4.", "pluck", 0.20, 2), kick="", snare="", hat="....x...x...", wood="....x...x..."),
    # playful bongos
    "bongo": dict(bpm=118, root=45, scale="cpenta", prog=[0, 3, 0, 4], pad=("tri", 0.06, 30), bass=("x.....x.x.......", "sine", 0.26),
                  arp=("0.2.4...2.0.4.2.", "pluck", 0.18, 2), kick="x.......x.......", snare="", hat="", wood="x.xx.x.xx.x.xx.x"),
    # heavy and slow
    "gears": dict(bpm=76, root=33, scale="phryg", prog=[0, 0, 1, 0], pad=("saw", 0.12, 90), bass=("x.....x.x.....x.", "saw", 0.28),
                  arp=("0.......1.......", "bell", 0.07, 2), kick="x.......x..x....", snare="........x.......", hat="", boom="x.......x.......", dist=True),
    # synthwave
    "swr": dict(bpm=128, root=38, scale="dorian", prog=[0, 5, 3, 4], pad=("saw", 0.10, 50), bass=("x.xx.xx.x.xx.xx.", "sq", 0.20),
                arp=("0.2.4.6.4.2.4.6.", "sq", 0.07, 2), kick="x...x...x...x...", snare="....x.......x...", hat="..x...x...x...x."),
    # tense, military
    "mw4": dict(bpm=120, root=36, scale="minor", prog=[0, 0, 5, 6], pad=("saw", 0.10, 70), bass=("x..x..x.x..x..x.", "sq", 0.22),
                arp=("0.......2.......", "bell", 0.06, 2), kick="x.......x.x.....", snare="....x..x....x.xx", hat="", boom="x...............", tick=True, roll=True),
    # plucks, drums, grit
    "pbz": dict(bpm=98, root=38, scale="insen", prog=[0, 3, 0, 1], pad=("saw", 0.07, 80), bass=("x.....x...x.x...", "saw", 0.24),
                arp=("0.1.3.2.1.0.3.1.", "pluck", 0.18, 2), kick="x.........x.....", snare="", hat="", boom="x.......x.......", wood="....x.......x.x.", dist=True),
    # bouncy cartoon rag
    "dandy": dict(bpm=132, root=43, scale="major", prog=[0, 5, 3, 4], pad=("tri", 0.05, 30), bass=("x...x...x...x...", "sq", 0.18),
                  arp=("0.4.2.4.0.4.2.6.", "pluck", 0.16, 2), kick="x.......x.......", snare="....x.......x...", hat="..x...x...x...x.", wood="......x.......x."),
}


STYLES.update({
    # creepy music box
    "isaac": dict(STYLES["dandy"], bpm=96, root=38, scale="minor", prog=[0, 5, 3, 6]),
    # calm and open
    "mine": dict(STYLES["dress"], bpm=96, root=41, prog=[0, 4, 5, 3]),
    # handheld chiptune
    "poke": dict(STYLES["swr"], bpm=138, root=45, scale="major", prog=[0, 4, 5, 3]),
    # driving electro
    "ut": dict(STYLES["swr"], bpm=120, root=50, scale="minor", prog=[0, 5, 3, 4]),
    "subway": dict(STYLES["swr"], bpm=128, root=55, scale="major", prog=[0, 4, 5, 3]),
    "fnaf": dict(STYLES["dandy"], bpm=88, root=36, scale="minor", prog=[0, 3, 5, 6]),
    "gdash": dict(STYLES["swr"], bpm=140, root=40, scale="minor", prog=[0, 5, 2, 6]),
    # sneaky
    "among": dict(STYLES["mw4"], bpm=104, root=40, prog=[0, 0, 3, 4]),
})


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def osc(kind, f, n):
    t = np.arange(n) / SR
    ph = (t * f) % 1.0
    if kind == "sine":
        return np.sin(2 * np.pi * ph)
    if kind == "sq":
        return np.where(ph < 0.5, 1.0, -1.0)
    if kind == "tri":
        return 2 * np.abs(2 * ph - 1) - 1
    return 2 * ph - 1  # saw


def lp(x, k):
    if k <= 1:
        return x
    return np.convolve(x, np.ones(k) / k, mode="same")


def env(n, a, r):
    e = np.ones(n)
    na, nr = max(1, min(int(a * SR), n // 2)), max(1, min(int(r * SR), n))
    e[:na] = np.linspace(0, 1, na)
    e[-nr:] *= np.linspace(1, 0, nr)
    return e


def note_of(st, deg, octave=0):
    sc = SCALES[st["scale"]]
    return st["root"] + 12 * octave + sc[deg % len(sc)] + 12 * (deg // len(sc))


def add(out, s0, seg):
    if s0 >= len(out):
        return
    e = min(len(seg), len(out) - s0)
    out[s0:s0 + e] += seg[:e]


def make(seconds, style="cs2", seed=0):
    st = STYLES.get(style, STYLES["cs2"])
    rng = np.random.default_rng(seed)
    spb = st.get("steps", 16)
    step = 60.0 / st["bpm"] / 4
    ns = int(step * SR)
    total = int((seconds + 1) * SR)
    out = np.zeros(total)
    bars = int(seconds / (step * spb)) + 2
    pwave, pvol, plp = st["pad"]
    bpat, bwave, bvol = st["bass"]
    apat, awave, avol, aoct = st["arp"]
    for bar in range(bars):
        deg = st["prog"][bar % len(st["prog"])]
        b0 = bar * spb * ns
        if b0 >= total:
            break
        chord = [note_of(st, deg, 1), note_of(st, deg + 2, 1), note_of(st, deg + 4, 1)]
        # pad: sustained chord
        n = spb * ns
        pad = np.zeros(n)
        for m in chord:
            for det in (0.996, 1.004):
                pad += osc(pwave, hz(m) * det, n)
        if st.get("choir"):
            pad += osc("sine", hz(chord[0] + 12), n) * 1.5 * (1 + 0.3 * np.sin(2 * np.pi * 5 * np.arange(n) / SR))
        pad = lp(pad, plp) * env(n, 0.25, 0.35) * pvol / 6
        add(out, b0, pad)
        full = bar >= 1
        for k in range(spb):
            s0 = b0 + k * ns
            # bass
            if bpat[k % len(bpat)] == "x":
                n = int(ns * 1.7)
                seg = osc(bwave, hz(note_of(st, deg, 0)), n)
                if bwave != "sine":
                    seg = lp(seg, 24)
                if st.get("dist"):
                    seg = np.tanh(seg * 2.5)
                add(out, s0, seg * env(n, 0.004, 0.06) * bvol)
            # arp / lead
            c = apat[k % len(apat)]
            if c != "." and full:
                m = note_of(st, deg + 2 * int(c), aoct)
                if awave == "pluck":
                    n = int(0.9 * SR)
                    t = np.arange(n) / SR
                    seg = lp(osc("saw", hz(m), n) + 0.5 * osc("tri", hz(m) * 2, n), 10) * np.exp(-t * 5.5)
                elif awave == "bell":
                    n = int(1.2 * SR)
                    t = np.arange(n) / SR
                    seg = (osc("sine", hz(m), n) + 0.4 * osc("sine", hz(m) * 2.01, n) + 0.2 * osc("sine", hz(m) * 3.0, n)) * np.exp(-t * 4)
                else:
                    n = int(ns * 0.9)
                    seg = lp(osc("sq", hz(m), n), 6) * env(n, 0.003, 0.04)
                add(out, s0, seg * avol)
            # drums
            def hit(pat):
                p = st.get(pat, "")
                return bool(p) and p[k % len(p)] == "x"
            if hit("kick") and full:
                n = int(0.2 * SR)
                t = np.arange(n) / SR
                add(out, s0, np.sin(2 * np.pi * (120 * t - 260 * t * t)) * np.exp(-t * 22) * 0.55)
            if hit("boom"):
                n = int(0.9 * SR)
                t = np.arange(n) / SR
                add(out, s0, (np.sin(2 * np.pi * (70 * t - 18 * t * t)) + 0.3 * rng.uniform(-1, 1, n) * np.exp(-t * 40)) * np.exp(-t * 4.5) * 0.6)
            if hit("snare") and full:
                n = int(0.14 * SR)
                t = np.arange(n) / SR
                v = 0.2 if not st.get("roll") else 0.13 + 0.07 * (k % 4 == 0)
                add(out, s0, (rng.uniform(-1, 1, n) * 0.8 + np.sin(2 * np.pi * 190 * t) * 0.4) * np.exp(-t * 28) * v)
            if hit("hat") and full:
                n = int(0.035 * SR)
                seg = np.diff(rng.uniform(-1, 1, n + 1)) * np.exp(-np.arange(n) / SR * 110) * 0.05
                add(out, s0, seg)
            if hit("wood"):
                n = int(0.08 * SR)
                t = np.arange(n) / SR
                add(out, s0, np.sin(2 * np.pi * 820 * t) * np.exp(-t * 60) * 0.16)
            if st.get("tick") and k % 4 == 0:
                n = int(0.02 * SR)
                t = np.arange(n) / SR
                add(out, s0, np.sin(2 * np.pi * (1800 if k else 2400) * t) * np.exp(-t * 200) * 0.07)
            if st.get("glitch") and full and rng.random() < 0.06:
                n = int(0.05 * SR)
                add(out, s0, osc("sq", rng.choice([110, 220, 880]), n) * env(n, 0.001, 0.01) * 0.04)
    out = out[: int(seconds * SR)]
    fi, fo = int(0.4 * SR), int(1.4 * SR)
    out[:fi] *= np.linspace(0, 1, fi)
    out[-fo:] *= np.linspace(1, 0, fo)
    out /= max(1e-6, np.max(np.abs(out)))
    return (out * 0.85).astype(np.float32)


if __name__ == "__main__":
    import sys, wave
    for s in sys.argv[1:] or list(STYLES):
        a = make(12, s, 1)
        with wave.open(f"/tmp/music_{s}.wav", "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes((a * 32767).astype(np.int16).tobytes())
        print(s, len(a) / SR)
