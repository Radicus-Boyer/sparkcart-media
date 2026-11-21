"""Pick the best ACE-Step take and time the lyric lines (doc section 3).
usage: python select_song.py songs.json gen_dir model_dir [ids...]
gen/<id>.json = {"mp3": [paths...]}; writes gen/<id>_timing.json"""
import sys, os, json, re, difflib
import numpy as np, librosa, sherpa_onnx

def recognizer(md):
    return sherpa_onnx.OfflineRecognizer.from_whisper(
        encoder=f"{md}/base.en-encoder.int8.onnx", decoder=f"{md}/base.en-decoder.int8.onnx",
        tokens=f"{md}/base.en-tokens.txt", language="en", task="transcribe", num_threads=2)

def words(s): return re.findall(r"[a-z']+", s.lower())

def transcribe(rec, y, sr, t0, t1):
    seg = y[int(t0*sr):int(t1*sr)]
    if len(seg) < sr * 0.5: return ""
    st = rec.create_stream(); st.accept_waveform(sr, seg); rec.decode_stream(st)
    return re.sub(r"\([^)]*\)|\[[^\]]*\]", " ", st.result.text)

def windows(rec, y, sr, win, hop):
    dur = len(y) / sr; out = []; t = 0.0
    while t < dur - 0.5:
        out.append((t, words(transcribe(rec, y, sr, t, min(dur, t + win))))); t += hop
    return out

def quick_score(rec, y, sr, lyric_words):
    heard = []
    for _, w in windows(rec, y, sr, 10, 8): heard += w
    from collections import Counter
    L, Hc = Counter(lyric_words), Counter(heard)
    return sum(min(c, Hc[w]) for w, c in L.items()) / max(1, sum(L.values()))

def sim(a, b): return difflib.SequenceMatcher(None, a, b).ratio()

def align(rec, y, sr, lines):
    wins = windows(rec, y, sr, 3.0, 0.5); starts, sims = [], []; prev = -1.0
    for ln in lines:
        lw = words(ln)[:3]; best = None
        for t, ww in wins:
            if t < prev + 0.3 or len(ww) < 1: continue
            for i in range(len(ww)):
                cand = ww[i:i+len(lw)]
                if len(cand) < len(lw): break
                s = np.mean([sim(a, b) for a, b in zip(lw, cand)])
                if s >= 0.62:
                    est = t + i * (3.0 / max(len(ww), 5))
                    if best is None or est < best[0] - 1e-6: best = (est, s)
            if best is not None and t > best[0] + 3.0: break
        if best and (not starts or starts[-1] is None or best[0] >= (prev + 0.6)):
            starts.append(best[0]); sims.append(best[1]); prev = best[0]
        else:
            starts.append(None); sims.append(0.0)
    known = [i for i, s in enumerate(starts) if s is not None]
    for i, s in enumerate(starts):
        if s is None:
            lo = max([k for k in known if k < i], default=None); hi = min([k for k in known if k > i], default=None)
            if lo is not None and hi is not None: starts[i] = starts[lo] + (starts[hi] - starts[lo]) * (i - lo) / (hi - lo)
            elif lo is not None: starts[i] = starts[lo] + 2.5 * (i - lo)
            elif hi is not None: starts[i] = max(0.5, starts[hi] - 2.5 * (hi - i))
            else: starts[i] = 2.0 + 2.5 * i
    found = len(known) / len(lines)
    return starts, float(np.mean(sims)), found

def analyse(path):
    y22, sr22 = librosa.load(path, sr=22050, mono=True)
    _, bf = librosa.beat.beat_track(y=y22, sr=sr22)
    beats = librosa.frames_to_time(bf, sr=sr22).tolist()
    rms = librosa.feature.rms(y=y22)[0]; idx = np.where(rms > 0.08 * rms.max())[0]
    end = float(librosa.frames_to_time(idx[-1], sr=sr22)) if len(idx) else len(y22) / sr22
    return beats, end

def main():
    songs = {s['id']: s for s in json.load(open(sys.argv[1]))}; gd = sys.argv[2]; rec = recognizer(sys.argv[3])
    ids = sys.argv[4:] or list(songs)
    for sid in ids:
        s = songs[sid]; lines = [l for v in s['verses'] for l in v['lines']]; lw = words(' '.join(lines))
        takes = json.load(open(f"{gd}/{sid}.json"))['mp3']; scored = []
        for p in takes:
            y, sr = librosa.load(p, sr=16000, mono=True); q = quick_score(rec, y, sr, lw); scored.append((q, p))
            print(sid, os.path.basename(p), 'quick', round(q, 3), flush=True)
        scored.sort(reverse=True); best = None
        for q, p in scored[:2]:
            y, sr = librosa.load(p, sr=16000, mono=True); st, ms, fd = align(rec, y, sr, lines)
            score = ms + 0.5 * fd + q
            print(sid, os.path.basename(p), 'align', round(score, 3), [round(x, 2) for x in st], flush=True)
            if best is None or score > best[0]: best = (score, p, st, q)
        beats, end = analyse(best[1])
        json.dump({"mp3": best[1], "quick": best[3], "score": best[0], "starts": best[2], "beats": beats, "audio_end": end,
                   "all_quick": [[q, p] for q, p in scored]}, open(f"{gd}/{sid}_timing.json", "w"), indent=1)

def dump(path, md, win=4.0, hop=2.0):
    """print 4 s transcript windows every 2 s (doc 3.3 manual check)"""
    rec = recognizer(md); y, sr = librosa.load(path, sr=16000, mono=True)
    for t, ww in windows(rec, y, sr, win, hop): print(f"{t:5.1f}  {' '.join(ww)}")

if __name__ == "__main__":
    if sys.argv[1] == "dump": dump(sys.argv[2], sys.argv[3])
    else: main()
