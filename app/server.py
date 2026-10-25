"""SparkCart Studio - local control panel for the Shorts pipeline (stdlib only).

  python app/server.py            opens the app at http://127.0.0.1:8765

Everything runs on this PC: Docker/Postiz/ngrok start, clip download + cut, rendering, scheduling to Postiz.
Scripts (episode JSON + posting.txt + batches/batch-N.json) come from Claude in chat and arrive with "Update".
"""
import datetime as dt, glob, json, os, random, re, shutil, subprocess, sys, threading, time, urllib.request, uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from zoneinfo import ZoneInfo

APP = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(APP)
DATA = os.path.join(APP, "data")
BIN = os.path.join(APP, "bin")
WIN = os.name == "nt"
sys.path.insert(0, ROOT + "/tools")
sys.path.insert(0, APP)
os.environ["PATH"] = BIN + os.pathsep + os.environ.get("PATH", "")
os.makedirs(DATA, exist_ok=True)

DEFAULTS = {
    "timezone": "America/Toronto",
    "compose_dir": os.path.join(os.path.expanduser("~"), "postiz-docker-compose"),
    "postiz_url": "http://localhost:5000",
    "ngrok_url": "https://banking-amazingly-divided.ngrok-free.dev",
    "ngrok_cmd": "ngrok http 5000 --url=banking-amazingly-divided.ngrok-free.dev",
    "postiz_api_key": "",
    "youtube_id": "cmvfrmynt0001nk8tlnohlmd0",
    "clips_dir": r"Z:\claudeprojects\ffmpegclips" if WIN else os.path.join(ROOT, "build", "clips_dl"),
    "videos_dir": r"Z:\claudeprojects\roblox vids" if WIN else os.path.join(ROOT, "build", "videos_copy"),
    "start_time": "14:00", "gap_min": 25, "gap_max": 45, "comments": False,
    "parallel": max(1, (os.cpu_count() or 2) // 2),
}
LOCK = threading.Lock()


def cfg():
    p = os.path.join(DATA, "config.json")
    c = dict(DEFAULTS)
    if os.path.exists(p):
        c.update(json.load(open(p)))
    return c


def save_cfg(new):
    c = cfg()
    c.update({k: v for k, v in new.items() if k in DEFAULTS})
    json.dump(c, open(os.path.join(DATA, "config.json"), "w"), indent=1)
    return c


def state():
    p = os.path.join(DATA, "state.json")
    return json.load(open(p)) if os.path.exists(p) else {}


def set_state(key, val):
    with LOCK:
        s = state()
        s[key] = val
        json.dump(s, open(os.path.join(DATA, "state.json"), "w"), indent=1)


# ---------------------------------------------------------------- jobs
JOBS = {}


class Job:
    def __init__(self, name):
        self.id = uuid.uuid4().hex[:8]
        self.name, self.status, self.log, self.t0 = name, "running", [], time.time()
        JOBS[self.id] = self

    def say(self, line):
        self.log.append(str(line).rstrip())
        self.log = self.log[-400:]


def start_job(name, fn, *args):
    j = Job(name)

    def run():
        try:
            fn(j, *args)
            j.status = "failed" if j.status == "failed" else "done"
        except Exception as e:  # noqa
            j.say(f"ERROR: {e}")
            j.status = "failed"
    threading.Thread(target=run, daemon=True).start()
    return j


def run_cmd(job, cmd, cwd=None, env=None, shell=False):
    job.say("$ " + (cmd if isinstance(cmd, str) else " ".join(cmd)))
    p = subprocess.Popen(cmd, cwd=cwd, env=env, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         text=True, encoding="utf-8", errors="replace")
    for line in p.stdout:
        if line.strip():
            job.say(line)
    p.wait()
    if p.returncode:
        job.say(f"(exit {p.returncode})")
    return p.returncode


def quick(cmd, cwd=None, timeout=10):
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout, encoding="utf-8", errors="replace")
        return r.returncode, (r.stdout + r.stderr).strip()
    except Exception as e:  # noqa
        return 1, str(e)


def http_up(url, timeout=3):
    try:
        urllib.request.urlopen(url, timeout=timeout)
        return True
    except urllib.error.HTTPError:
        return True        # answered, so it's up
    except Exception:
        return False


# ---------------------------------------------------------------- status
def status():
    c = cfg()
    out = {}
    out["docker"] = quick(["docker", "info"], timeout=8)[0] == 0 if shutil.which("docker") else False
    names = quick(["docker", "ps", "--format", "{{.Names}}"])[1] if out["docker"] else ""
    out["postiz_containers"] = len([n for n in names.splitlines() if n.strip()])
    out["postiz"] = http_up(c["postiz_url"])
    try:
        t = json.load(urllib.request.urlopen("http://127.0.0.1:4040/api/tunnels", timeout=2))
        out["ngrok"] = bool(t.get("tunnels"))
    except Exception:
        out["ngrok"] = False
    out["ffmpeg"] = bool(shutil.which("ffmpeg"))
    out["ytdlp"] = bool(shutil.which("yt-dlp"))
    out["models"] = os.path.exists(ROOT + "/engine/models/kokoro.onnx") and os.path.exists(ROOT + "/engine/models/voices.bin")
    out["engine"] = quick([sys.executable, "-c", "import kokoro_onnx, num2words, PIL, numpy, soundfile"], timeout=30)[0] == 0
    out["api_key"] = bool(c["postiz_api_key"])
    return out


# ---------------------------------------------------------------- stack (Docker + Postiz + ngrok)
def docker_desktop_exe():
    for base in (os.environ.get("ProgramFiles", r"C:\Program Files"), r"C:\Program Files"):
        p = os.path.join(base, "Docker", "Docker", "Docker Desktop.exe")
        if os.path.exists(p):
            return p


def detached(cmd):
    kw = {"creationflags": 0x00000008 | 0x00000200} if WIN else {"start_new_session": True}
    subprocess.Popen(cmd, shell=isinstance(cmd, str), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                     stdin=subprocess.DEVNULL, **kw)


def job_start_stack(job):
    c = cfg()
    if quick(["docker", "info"], timeout=8)[0] != 0:
        exe = docker_desktop_exe()
        if not exe:
            job.say("Docker Desktop not found. Install it from docker.com, then press Start again.")
            job.status = "failed"
            return
        job.say("Starting Docker Desktop (can take a minute)...")
        detached([exe])
        for _ in range(60):
            time.sleep(3)
            if quick(["docker", "info"], timeout=8)[0] == 0:
                break
        else:
            job.say("Docker did not start in 3 minutes.")
            job.status = "failed"
            return
    job.say("Docker is running.")
    if os.path.isdir(c["compose_dir"]):
        if run_cmd(job, ["docker", "compose", "up", "-d"], cwd=c["compose_dir"]):
            job.status = "failed"
            return
    else:
        job.say(f"Postiz folder not found: {c['compose_dir']} (set it in Settings)")
        job.status = "failed"
        return
    try:
        json.load(urllib.request.urlopen("http://127.0.0.1:4040/api/tunnels", timeout=2))
        job.say("ngrok already running.")
    except Exception:
        if c["ngrok_cmd"] and shutil.which(c["ngrok_cmd"].split()[0]):
            job.say("Starting ngrok...")
            detached(c["ngrok_cmd"])
        else:
            job.say("ngrok not found; skipping (Postiz still works locally, YouTube links need ngrok).")
    job.say("Waiting for Postiz...")
    for _ in range(60):
        if http_up(c["postiz_url"]):
            job.say("Postiz is up.")
            return
        time.sleep(3)
    job.say("Postiz did not answer in 3 minutes.")
    job.status = "failed"


def job_stop_stack(job):
    c = cfg()
    run_cmd(job, ["docker", "compose", "stop"], cwd=c["compose_dir"])


# ---------------------------------------------------------------- batches
def video_for(num, bn=None):
    c = cfg()
    pats = [ROOT + "/build/out"]
    if bn:
        pats += [ROOT + f"/batch-{bn}", os.path.join(c["videos_dir"], f"batch-{bn}")]
    for d in pats:
        for f in sorted(glob.glob(os.path.join(d, f"{num} *.mp4"))):
            return f


def load_batches():
    out = []
    for f in sorted(glob.glob(ROOT + "/batches/batch-*.json"), key=lambda x: int(re.findall(r"batch-(\d+)", x)[0])):
        m = json.load(open(f))
        bn = m["batch"]
        eps = []
        for p in m["episodes"]:
            e = json.load(open(os.path.join(ROOT, p)))
            v = video_for(e["num"], bn)
            eps.append({"path": p, "num": e["num"], "title": e.get("file", e["slug"]).replace(".mp4", ""),
                        "voice": e.get("voice"), "target": e.get("target"), "rendered": bool(v)})
        clips = []
        for cl in m.get("clips", []):
            clips.append({**cl, "have": os.path.exists(f"{ROOT}/episodes/assets/{cl['name']}.mp4")})
        st = state().get(f"batch-{bn}", {})
        out.append({"batch": bn, "note": m.get("note", ""), "episodes": eps, "clips": clips,
                    "posting": m.get("posting", f"batch-{bn}/posting.txt"), "state": st})
    return out


def get_batch(bn):
    return next(b for b in load_batches() if b["batch"] == bn)


# ---------------------------------------------------------------- clips
def job_clips(job, bn, auto_render):
    c = cfg()
    b = get_batch(bn)
    raw, cut = os.path.join(c["clips_dir"], "raw"), os.path.join(c["clips_dir"], "cut")
    os.makedirs(raw, exist_ok=True)
    os.makedirs(cut, exist_ok=True)
    todo = [x for x in b["clips"] if not x["have"]]
    job.say(f"{len(todo)} clip(s) to get")
    for cl in todo:
        name = cl["name"]
        rawf = next(iter(glob.glob(os.path.join(raw, name + ".*"))), None)
        if not rawf:
            for url in [cl["url"]] + cl.get("backup", []):
                cmd = ["yt-dlp", "-f", "bv*[height<=1080]+ba/b", "--merge-output-format", "mp4", "-o",
                       os.path.join(raw, name + ".%(ext)s"), "--no-playlist", "--force-overwrites"]
                if cl.get("section"):
                    cmd += ["--download-sections", cl["section"]]
                run_cmd(job, cmd + [url])
                rawf = next(iter(glob.glob(os.path.join(raw, name + ".*"))), None)
                if rawf and os.path.getsize(rawf) > 50_000:
                    break
        if not rawf:
            job.say(f"FAILED to download {name}")
            job.status = "failed"
            continue
        out = os.path.join(cut, name + ".mp4")
        rc = run_cmd(job, ["ffmpeg", "-y", "-loglevel", "error", "-ss", str(cl.get("cut", 0)), "-t", str(cl.get("len", 13)),
                           "-i", rawf, "-an", "-vf", "scale=1280:-2,fps=30", "-c:v", "libx264", "-crf", "20", out])
        if rc == 0:
            shutil.copy(out, f"{ROOT}/episodes/assets/{name}.mp4")
            job.say(f"ready: {name}")
    if job.status == "failed":
        return
    job.say("All clips ready.")
    if auto_render:
        job_render(job, bn, None)


def clean_clips(bn):
    """Remove this batch's clip files from the repo assets and the download folder (they're temporary)."""
    c = cfg()
    for cl in get_batch(bn)["clips"]:
        for p in (f"{ROOT}/episodes/assets/{cl['name']}.mp4",):
            if os.path.exists(p):
                os.remove(p)
    for sub in ("raw", "cut"):
        shutil.rmtree(os.path.join(c["clips_dir"], sub), ignore_errors=True)


# ---------------------------------------------------------------- render
def job_render(job, bn, only):
    b = get_batch(bn)
    eps = [e for e in b["episodes"] if not e["rendered"] and (not only or e["num"] in only)]
    if not eps:
        job.say("Nothing to render.")
        return
    missing = [x["name"] for x in b["clips"] if not x["have"]]
    if missing:
        job.say("Clips missing: " + ", ".join(missing) + " - press Get clips first.")
        job.status = "failed"
        return
    c = cfg()
    os.makedirs(ROOT + "/build/out", exist_ok=True)
    pending, running = list(eps), []
    job.say(f"Rendering {len(eps)} video(s), {c['parallel']} at a time")
    while pending or running:
        while pending and len(running) < c["parallel"]:
            e = pending.pop(0)
            p = subprocess.Popen([sys.executable, ROOT + "/engine/render.py", os.path.join(ROOT, e["path"]), "--out", ROOT + "/build/out"],
                                 cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
            running.append((e, p, time.time()))
            job.say(f"start #{e['num']} {e['title']}")
        for e, p, t0 in list(running):
            if p.poll() is not None:
                out = p.stdout.read().strip().splitlines()
                job.say(f"{'done' if p.returncode == 0 else 'FAILED'} #{e['num']} in {int(time.time() - t0)}s" +
                        ("" if p.returncode == 0 else " :: " + " | ".join(out[-3:])))
                if p.returncode:
                    job.status = "failed"
                running.remove((e, p, t0))
        time.sleep(2)
    if job.status != "failed":
        job.say("All videos rendered.")


def job_publish(job, bn):
    """Copy finished videos (named with their length) to batch-N folders in the repo + the videos folder."""
    c = cfg()
    b = get_batch(bn)
    dst_repo, dst_pc = ROOT + f"/batch-{bn}", os.path.join(c["videos_dir"], f"batch-{bn}")
    dests = [dst_pc] + ([dst_repo] if os.path.isdir(dst_repo) else [])
    os.makedirs(dst_pc, exist_ok=True)
    for e in b["episodes"]:
        v = video_for(e["num"], bn)
        if not v:
            continue
        secs = probe_secs(v)
        name = os.path.basename(v)
        name = re.sub(r"\s*\(\d+s\)", "", name)[:-4] + f" ({round(secs)}s).mp4"
        for d in dests:
            if os.path.abspath(os.path.dirname(v)) != os.path.abspath(d) or os.path.basename(v) != name:
                shutil.copy(v, os.path.join(d, name))
        job.say(f"saved {name}")


def probe_secs(path):
    rc, o = quick(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], timeout=30)
    try:
        return float(o.splitlines()[-1])
    except Exception:
        return 0.0


# ---------------------------------------------------------------- schedule
def job_schedule(job, bn, start_local, gap, dry):
    import posting
    from postiz import Postiz
    c = cfg()
    b = get_batch(bn)
    eps = posting.parse(os.path.join(ROOT, b["posting"]))
    tz = ZoneInfo(c["timezone"])
    t = dt.datetime.strptime(start_local, "%Y-%m-%d %H:%M").replace(tzinfo=tz)
    rnd = random.Random()
    api = None if dry else Postiz(c["postiz_url"], c["postiz_api_key"])
    if not dry and not c["postiz_api_key"]:
        job.say("Add the Postiz API key in Settings first (Postiz > Settings > Developers > Public API).")
        job.status = "failed"
        return
    done = []
    for e in eps:
        num = e["FILE"].split(" ")[0]
        path = video_for(int(num), bn)
        if not path:
            job.say(f"No rendered video for #{num} - skipping")
            job.status = "failed"
            continue
        when = t.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:00Z")
        job.say(f"#{num} -> {t.strftime('%a %b %d %I:%M %p')} ({c['timezone']})")
        if not dry:
            media = api.upload(path)
            tags = [{"value": x.strip(), "label": x.strip()} for x in e["YT TAGS"].split(",") if x.strip()]
            settings = {"__type": "youtube", "title": e["YT TITLE"], **posting.YT_SETTINGS, "tags": tags}
            content = posting.html(e["YT DESCRIPTION"]) + f"<p>{e['YT HASHTAGS']}</p>"
            comment = posting.html(e["YT COMMENT"]) if c["comments"] and e.get("YT COMMENT") else None
            api.schedule(c["youtube_id"], when, content, media, settings, comment)
            done.append(num)
        t += dt.timedelta(minutes=rnd.randint(*gap))
    if not dry and job.status != "failed":
        set_state(f"batch-{bn}", {"scheduled": done, "at": dt.datetime.now().isoformat(timespec="minutes")})
        job.say(f"Scheduled {len(done)} post(s) to Postiz.")
        try:
            import topics
            topics.update()
        except Exception as ex:  # noqa
            job.say(f"(topic list not updated: {ex})")


def job_update(job):
    run_cmd(job, ["git", "pull", "--ff-only"], cwd=ROOT)


# ---------------------------------------------------------------- http
class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send(self, obj, code=200, ctype="application/json"):
        body = obj if isinstance(obj, bytes) else json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        p = self.path.split("?")[0]
        if p in ("/", "/index.html"):
            return self.send(open(APP + "/ui/index.html", "rb").read(), ctype="text/html; charset=utf-8")
        if p == "/api/status":
            return self.send(status())
        if p == "/api/config":
            c = cfg()
            c["postiz_api_key"] = "set" if c["postiz_api_key"] else ""
            return self.send(c)
        if p == "/api/batches":
            return self.send(load_batches())
        if p == "/api/jobs":
            return self.send([{"id": j.id, "name": j.name, "status": j.status, "log": j.log[-60:], "age": int(time.time() - j.t0)}
                              for j in sorted(JOBS.values(), key=lambda j: -j.t0)[:6]])
        self.send({"error": "not found"}, 404)

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        d = json.loads(self.rfile.read(n) or b"{}")
        p = self.path
        try:
            if p == "/api/config":
                if d.get("postiz_api_key") == "set":
                    d.pop("postiz_api_key")
                save_cfg(d)
                return self.send({"ok": True})
            if p == "/api/stack/start":
                return self.send({"job": start_job("Start Docker + Postiz", job_start_stack).id})
            if p == "/api/stack/stop":
                return self.send({"job": start_job("Stop Postiz", job_stop_stack).id})
            if p == "/api/update":
                return self.send({"job": start_job("Update from GitHub", job_update).id})
            if p == "/api/clips":
                return self.send({"job": start_job(f"Get clips, batch {d['batch']}", job_clips, d["batch"], d.get("render", True)).id})
            if p == "/api/render":
                return self.send({"job": start_job(f"Render batch {d['batch']}", job_render, d["batch"], d.get("only")).id})
            if p == "/api/publish":
                return self.send({"job": start_job(f"Save videos, batch {d['batch']}", job_publish, d["batch"]).id})
            if p == "/api/schedule":
                return self.send({"job": start_job(("Preview" if d.get("dry") else "Schedule") + f" batch {d['batch']}", job_schedule,
                                                   d["batch"], d["start"], (d["gap_min"], d["gap_max"]), d.get("dry", False)).id})
            if p == "/api/clean":
                clean_clips(d["batch"])
                return self.send({"ok": True})
        except StopIteration:
            return self.send({"error": "unknown batch"}, 404)
        self.send({"error": "not found"}, 404)


def main(port=8765):
    srv = ThreadingHTTPServer(("127.0.0.1", port), H)
    url = f"http://127.0.0.1:{port}"
    print("SparkCart Studio running at", url)
    if "--no-open" not in sys.argv:
        threading.Timer(1, lambda: open_window(url)).start()
    srv.serve_forever()


def open_window(url):
    import webbrowser
    if WIN:
        for exe in (r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
                    r"C:\Program Files\Google\Chrome\Application\chrome.exe"):
            if os.path.exists(exe):
                subprocess.Popen([exe, f"--app={url}", "--window-size=1100,800"])
                return
    webbrowser.open(url)


if __name__ == "__main__":
    main()
