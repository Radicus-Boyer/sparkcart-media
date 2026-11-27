"""Beat grid without numba beat_track (it segfaults here): known BPM, phase picked from onset strength."""
import sys, json, numpy as np, librosa
path, bpm = sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else 100.0
y, sr = librosa.load(path, sr=22050, mono=True); hop = 512
oenv = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop); ft = hop / sr
# refine tempo around the requested BPM (+-6%) by comb score
best = None
for b in np.arange(bpm * 0.94, bpm * 1.06, 0.25):
    per = 60.0 / b
    for ph in np.arange(0, per, 0.01):
        ts = np.arange(ph, len(y) / sr, per); idx = (ts / ft).astype(int); idx = idx[idx < len(oenv)]
        sc = oenv[idx].mean()
        if best is None or sc > best[0]: best = (sc, b, ph)
_, b, ph = best; per = 60.0 / b
beats = np.arange(ph, len(y) / sr, per).tolist()
rms = librosa.feature.rms(y=y, hop_length=hop)[0]; last = np.where(rms > 0.08 * rms.max())[0]
end = float(last[-1] * ft) if len(last) else len(y) / sr
print(json.dumps(dict(beats=beats, end=end, bpm=float(b))))
