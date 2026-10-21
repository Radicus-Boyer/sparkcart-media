"""Assemble 2x2-grid Chrome screenshots (YouTube frames) into an mp4. usage: assemble.py out.mp4 fps file1 file2 ..."""
import sys, os, subprocess, tempfile
from PIL import Image
out, fps, files = sys.argv[1], float(sys.argv[2]), sys.argv[3:]
d = tempfile.mkdtemp()
n = 0
for f in files:
    im = Image.open(f).convert("RGB")
    W, H = im.size
    s = W / 1920
    ch = int(427 * s); cw = int(759 * s)
    for i in range(4):
        x, y = (i % 2) * cw, (i // 2) * ch
        im.crop((x + 1, y + 1, x + cw - 1, y + ch - 1)).resize((1280, 720), Image.LANCZOS).save(f"{d}/{n:05d}.png"); n += 1
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", f"{d}/%05d.png",
                "-vf", "minterpolate=fps=30:mi_mode=blend,format=yuv420p", "-c:v", "libx264", "-crf", "18", out], check=True)
print(out, n, "frames", n / fps, "s")
