"""Posting helper for SparkCart batches.

  python3 tools/posting.py check <posting.txt>
      Parse the posting file and verify every block's character limits.

  python3 tools/posting.py urls <folder-in-repo>
      Print the public raw GitHub URL for every MP4 in that repo folder (for Postiz uploadFromUrlTool).

  python3 tools/posting.py schedule <posting.txt> <media.json> --start "2026-10-01 15:00" --tz America/Toronto
          [--gap 15 40] [--channels youtube tiktok] [--independent] [--seed N] [--out sched.json]
      Build the socialPost array for Postiz integrationSchedulePostTool.
      media.json maps each FILE name (or its leading number, e.g. "22") to the Postiz media path
      returned by uploadFromUrlTool.
      --gap MIN MAX     random minutes between posts (default 15 40)
      posting.txt may also hold YT COMMENT / TIKTOK COMMENT lines: a first comment posted by the channel
      under its own video (write a different one for every video; --no-comments leaves them out).
      --independent     YouTube and TikTok each get their own random timeline (default: TikTok
                        follows YouTube by a random 3-12 minutes for each video)
      Prints a readable timetable and writes the JSON (default build/sched.json).
"""
import argparse, datetime as dt, json, os, random, sys, urllib.parse
from zoneinfo import ZoneInfo

REPO = "Radicus-Boyer/sparkcart-media"
YOUTUBE_ID = "cmups58t40dreqw0yvi5zfyzi"   # SparkCart
TIKTOK_ID = "cmups5usr0dsdqw0ypxeny3k7"    # sparkcart.co
KEYS = ("FILE", "YT TITLE", "YT DESCRIPTION", "YT HASHTAGS", "YT TAGS", "TIKTOK TITLE", "TIKTOK CAPTION")
OPTIONAL = ("YT COMMENT", "TIKTOK COMMENT")   # first comment posted by the channel under its own video
LIMITS = {"YT TITLE": 100, "TIKTOK TITLE": 90, "TIKTOK CAPTION": 2200, "YT DESCRIPTION": 4800}

YT_SETTINGS = {"type": "public", "selfDeclaredMadeForKids": "no"}
TT_SETTINGS = {"privacy_level": "PUBLIC_TO_EVERYONE", "duet": True, "stitch": True, "comment": True,
               "autoAddMusic": "no", "brand_content_toggle": False, "brand_organic_toggle": False,
               "video_made_with_ai": False, "content_posting_method": "DIRECT_POST"}


def parse(path):
    blocks = [b for b in open(path, encoding="utf-8").read().split("\n=====\n") if "FILE:" in b]
    eps = []
    for b in blocks:
        d, key = {}, None
        for ln in b.strip().split("\n"):
            m = [k for k in KEYS + OPTIONAL if ln.startswith(k + ":")]
            if m:
                key = m[0]
                d[key] = ln.split(":", 1)[1].strip()
            elif key:
                d[key] += "\n" + ln
        eps.append(d)
    return eps


def check(path):
    bad = 0
    for e in parse(path):
        missing = [k for k in KEYS if not e.get(k)]
        over = [f"{k} {len(e[k])}/{n}" for k, n in LIMITS.items() if len(e.get(k, "")) > n]
        status = "OK" if not (missing or over) else "FIX: " + ", ".join(missing + over)
        bad += status != "OK"
        print(f"{e.get('FILE', '?'):45} {status}")
    print("all good" if not bad else f"{bad} block(s) need fixing")
    return bad


def urls(folder):
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for f in sorted(os.listdir(os.path.join(root, folder))):
        if f.endswith(".mp4"):
            print(f"https://raw.githubusercontent.com/{REPO}/main/{folder}/{urllib.parse.quote(f)}")


def html(text):
    return "".join(f"<p>{p.strip()}</p>" for p in text.split("\n") if p.strip())


def media_for(media, file):
    return media.get(file) or media.get(file.split(" ")[0])


def schedule(a):
    eps = parse(a.posting)
    media = json.load(open(a.media))
    rnd = random.Random(a.seed)
    tz = ZoneInfo(a.tz)
    start = dt.datetime.strptime(a.start, "%Y-%m-%d %H:%M").replace(tzinfo=tz)
    lo, hi = a.gap
    yt_t, tt_t = start, start + dt.timedelta(minutes=rnd.randint(3, 12))
    posts, rows = [], []
    for e in eps:
        path = media_for(media, e["FILE"])
        if not path:
            sys.exit(f"no media path for {e['FILE']}")
        row = [e["FILE"].rsplit(".", 1)[0]]
        if "youtube" in a.channels:
            tags = [{"value": t.strip(), "label": t.strip()} for t in e["YT TAGS"].split(",") if t.strip()]
            settings = [{"key": "title", "value": e["YT TITLE"]}] + [{"key": k, "value": v} for k, v in YT_SETTINGS.items()]
            settings.append({"key": "tags", "value": tags})
            posts.append({"integrationId": YOUTUBE_ID, "isPremium": False, "shortLink": False, "type": "schedule",
                          "date": yt_t.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:00Z"),
                          "postsAndComments": [{"content": html(e["YT DESCRIPTION"]) + f"<p>{e['YT HASHTAGS']}</p>", "attachments": [path]}]
                                              + ([{"content": html(e["YT COMMENT"]), "attachments": []}] if e.get("YT COMMENT") and not a.no_comments else []),
                          "settings": settings})
            row.append("YT " + yt_t.strftime("%a %I:%M %p"))
        if "tiktok" in a.channels:
            if not a.independent:
                tt_t = yt_t + dt.timedelta(minutes=rnd.randint(3, 12)) if "youtube" in a.channels else tt_t
            settings = [{"key": "title", "value": e["TIKTOK TITLE"]}] + [{"key": k, "value": v} for k, v in TT_SETTINGS.items()]
            posts.append({"integrationId": TIKTOK_ID, "isPremium": False, "shortLink": False, "type": "schedule",
                          "date": tt_t.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:00Z"),
                          "postsAndComments": [{"content": f"<p>{e['TIKTOK CAPTION']}</p>", "attachments": [path]}]
                                              + ([{"content": html(e["TIKTOK COMMENT"]), "attachments": []}] if e.get("TIKTOK COMMENT") and not a.no_comments else []),
                          "settings": settings})
            row.append("TT " + tt_t.strftime("%a %I:%M %p"))
            if a.independent or "youtube" not in a.channels:
                tt_t += dt.timedelta(minutes=rnd.randint(lo, hi))
        yt_t += dt.timedelta(minutes=rnd.randint(lo, hi))
        rows.append(" | ".join(row))
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump(posts, open(a.out, "w"), ensure_ascii=False)
    print(f"times in {a.tz}")
    print("\n".join(rows))
    print(f"{len(posts)} posts -> {a.out}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check"); c.add_argument("posting")
    u = sub.add_parser("urls"); u.add_argument("folder")
    s = sub.add_parser("schedule")
    s.add_argument("posting"); s.add_argument("media")
    s.add_argument("--start", required=True); s.add_argument("--tz", default="America/Mexico_City")
    s.add_argument("--gap", nargs=2, type=int, default=[15, 40])
    s.add_argument("--channels", nargs="+", default=["youtube", "tiktok"])
    s.add_argument("--independent", action="store_true")
    s.add_argument("--seed", type=int)
    s.add_argument("--no-comments", action="store_true", help="leave out the YT COMMENT / TIKTOK COMMENT first comments")
    s.add_argument("--out", default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "build", "sched.json"))
    a = ap.parse_args()
    if a.cmd == "check":
        sys.exit(1 if check(a.posting) else 0)
    if a.cmd == "urls":
        urls(a.folder)
    else:
        schedule(a)
