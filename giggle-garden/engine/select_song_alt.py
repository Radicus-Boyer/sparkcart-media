"""Doc section 3: pick best take (Whisper base.en via sherpa-onnx) and compute line starts.
usage: python select_song.py songs.json gen_dir id mp3 [mp3 ...]      -> writes gen_dir/<id>_timing.json
       python select_song.py windows mp3 [step] [win]                 -> prints transcript windows (hand check, doc 3.3)"""
import sys, os, json, re, difflib
import numpy as np, librosa, sherpa_onnx

M = '/home/claude/gg/model/sherpa-onnx-whisper-base.en'
REC = sherpa_onnx.OfflineRecognizer.from_whisper(
    encoder=f'{M}/base.en-encoder.int8.onnx', decoder=f'{M}/base.en-decoder.int8.onnx',
    tokens=f'{M}/base.en-tokens.txt', language='en', task='transcribe', num_threads=2)
_cache = {}

def audio(path):
    if path not in _cache: _cache[path] = librosa.load(path, sr=16000, mono=True)[0]
    return _cache[path]

def tx(y, a, b):
    seg = y[int(a * 16000):int(b * 16000)]
    if len(seg) < 1600: return ''
    s = REC.create_stream(); s.accept_waveform(16000, seg.astype(np.float32)); REC.decode_stream(s)
    t = re.sub(r"\([^)]*\)|\[[^\]]*\]", " ", s.result.text.lower())
    return re.sub(r"[^a-z' ]", " ", t).split()

def words_of(text): return re.sub(r"[^a-z' ]", " ", text.lower()).split()

def quick(path, lyrics):
    y = audio(path); dur = len(y) / 16000; heard = []
    t = 0.0
    while t < dur - 2: heard += tx(y, t, t + 10); t += 8
    lw = words_of(' '.join(lyrics)); hc = {}
    for w in heard: hc[w] = hc.get(w, 0) + 1
    lc = {}
    for w in lw: lc[w] = lc.get(w, 0) + 1
    return sum(min(c, hc.get(w, 0)) for w, c in lc.items()) / max(1, len(lw))

def sim(a, b): return difflib.SequenceMatcher(None, a, b).ratio()

def align(path, lyrics):
    y = audio(path); dur = len(y) / 16000
    wins = []; t = 0.0
    while t < dur - 1.5: wins.append((t, tx(y, t, t + 3.0))); t += 0.5
    starts = []; sims = []; prev = -1.0
    for ln in lyrics:
        fw = words_of(ln)[:3]; best = None
        for t0, hw in wins:
            if t0 < prev + 0.3 or not hw: continue
            for k in range(0, max(1, len(hw) - len(fw) + 1)):
                sc = np.mean([sim(a, b) for a, b in zip(fw, hw[k:k + len(fw)])]) if hw[k:k + len(fw)] else 0
                if sc >= 0.62:
                    est = t0 + k * (3.0 / max(len(hw), 5))
                    if best is None or est < best[0] - 1e-9: best = (est, sc)
                    break
            if best is not None and t0 > best[0] + 1.0: break
        if best: starts.append(best[0]); sims.append(best[1]); prev = best[0] + 0.6
        else: starts.append(None); sims.append(0.0)
    # interpolate missing
    idx = [i for i, s in enumerate(starts) if s is not None]
    for i, s in enumerate(starts):
        if s is None:
            lo = max([j for j in idx if j < i], default=None); hi = min([j for j in idx if j > i], default=None)
            if lo is not None and hi is not None: starts[i] = starts[lo] + (starts[hi] - starts[lo]) * (i - lo) / (hi - lo)
            elif lo is not None: starts[i] = starts[lo] + 2.5 * (i - lo)
            else: starts[i] = 0.3 + 2.5 * i
    found = len(idx) / len(lyrics)
    return starts, float(np.mean(sims)), found

def beats_and_end(path):
    y, sr = librosa.load(path, sr=22050, mono=True)
    _, b = librosa.beat.beat_track(y=y, sr=sr); beats = librosa.frames_to_time(b, sr=sr).tolist()
    rms = librosa.feature.rms(y=y, hop_length=512)[0]; thr = 0.08 * rms.max()
    last = np.where(rms > thr)[0]; end = float(librosa.frames_to_time(last[-1], sr=sr, hop_length=512)) if len(last) else len(y) / sr
    return beats, end

if __name__ == '__main__':
    if sys.argv[1] == 'windows':
        p = sys.argv[2]; step = float(sys.argv[3]) if len(sys.argv) > 3 else 2; win = float(sys.argv[4]) if len(sys.argv) > 4 else 4
        y = audio(p); t = 0.0
        while t < len(y) / 16000 - 1: print(f'{t:5.1f}  ' + ' '.join(tx(y, t, t + win))); t += step
        sys.exit()
    sp, gd, sid, *mp3s = sys.argv[1:]
    song = {s['id']: s for s in json.load(open(sp))}[sid]
    lyrics = [l for v in song['verses'] for l in v['lines']]
    q = [(quick(m, lyrics), m) for m in mp3s]
    q.sort(reverse=True); print('quick', [(round(a, 2), os.path.basename(m)[:8]) for a, m in q])
    best = None
    for qs, m in q[:2]:
        starts, ms, found = align(m, lyrics); score = ms + 0.5 * found + qs
        print(os.path.basename(m)[:8], 'quick', round(qs, 2), 'sim', round(ms, 2), 'found', round(found, 2), 'score', round(score, 2), [round(s, 1) for s in starts])
        if best is None or score > best[0]: best = (score, qs, m, starts)
    score, qs, m, starts = best
    import subprocess; r = json.loads(subprocess.run(['python3', '/home/claude/gg/beats.py', m, str(song['bpm'])], capture_output=True, text=True).stdout); beats, end = r['beats'], r['end']
    json.dump(dict(mp3=m, quick=qs, score=score, starts=starts, beats=beats, audio_end=end), open(f'{gd}/{sid}_timing.json', 'w'))
    print('CHOSEN', m, 'end', round(end, 1))
