"""Keeps TOPICS_DONE.txt (every game/subject we've made a video about) up to date and checks new ideas for repeats.

  python3 tools/topics.py update                  rebuild TOPICS_DONE.txt from every rendered batch in the repo
  python3 tools/topics.py check "Doors" "Zoink"   list past videos that match each idea (exit code 1 if any match)
  python3 tools/topics.py check-batch build/make_batch21.py
                                                  check every new episode in a generator against past videos

posting.py runs `update` automatically after every schedule, so the list never falls behind.
"""

import argparse, glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "TOPICS_DONE.txt")
STOP = {"the", "a", "an", "of", "in", "on", "to", "is", "was", "for", "and", "it", "its", "it's", "how", "why", "this",
        "that", "from", "with", "at", "by", "got", "has", "are", "be", "who", "what", "where", "came", "number", "1",
        "roblox", "roblox's", "geometry", "dash", "game", "games", "level", "player", "players", "million", "billion",
        "took", "attempts", "times", "out", "now", "new", "every", "first", "most", "just", "again", "made", "really",
        "biggest", "part", "2", "3", "4", "5", "years", "old", "day", "days", "hit", "all", "your", "you", "people"}
NES_FIX = {"Castlevania Ii Simons Quest": "Castlevania II: Simon's Quest", "Pow": "P.O.W.", "Et Burial": "E.T. Burial",
           "Mike Tysons Punch Out": "Mike Tyson's Punch-Out!!", "Ghosts N Goblins": "Ghosts 'n Goblins",
           "Chip N Dale Rescue Rangers": "Chip 'n Dale Rescue Rangers", "Pac Man": "Pac-Man", "Skate Or Die": "Skate or Die",
           "Skate Or Die 2": "Skate or Die 2", "Ski Or Die": "Ski or Die", "The Legend Of Zelda": "The Legend of Zelda",
           "Ducktales": "DuckTales"}


def clean(f):
    return re.sub(r"\s*\(\d+s\)", "", os.path.splitext(f)[0]).strip()


def collect():
    nes, popular, history, roblox = [], [], set(), set()
    for j in sorted(glob.glob(os.path.join(ROOT, "episodes", "nes", "*.json"))):
        n, _, s = os.path.basename(j)[:-5].partition("-")
        t = s.replace("-", " ").title()
        nes.append((int(n), NES_FIX.get(t, t)))
    for d in ("popular-batch-1", "popular-batch-2"):
        for f in sorted(os.listdir(os.path.join(ROOT, d))):
            if f.endswith(".mp4"):
                n, _, s = clean(f).partition(" - ")
                popular.append((int(n), s))
    dirs = sorted(glob.glob(os.path.join(ROOT, "batch-*")), key=lambda x: int(x.rsplit("-", 1)[1])) + [os.path.join(ROOT, "roblox-edition")]
    for d in dirs:
        for f in os.listdir(d):
            if not f.endswith(".mp4"):
                continue
            c = clean(f)
            if " - " in c:
                n, _, s = c.partition(" - ")
                history.add((int(n), s))
            else:
                n, _, s = c.partition(" ")
                if n.isdigit():
                    roblox.add((int(n), s))
    return nes, popular, sorted(history), sorted(roblox)


def update():
    import datetime
    nes, popular, history, roblox = collect()
    out = [f"SPARKCART SHORTS - EVERYTHING WE'VE COVERED (auto-updated {datetime.date.today():%b %d, %Y})",
           "Check new ideas against this list to avoid repeats: python3 tools/topics.py check \"idea\"", ""]
    for title, rows in (("8-BIT BACKSTORY: NES / RETRO", nes), ("MOST POPULAR GAMES OF THE INTERNET (modern games)", popular),
                        ("POPULAR GAME HISTORIES", history), ("ROBLOX EDITION + GD / MEMES / TRENDING", roblox)):
        out.append(f"== {title} ==")
        out += [f"{n:>3}  {s}" for n, s in rows]
        out.append("")
    open(OUT, "w").write("\n".join(out))
    print(f"TOPICS_DONE.txt: {sum(map(len, (nes, popular, history, roblox)))} videos")


def words(s):
    return {w for w in re.findall(r"[a-z0-9+']+", s.lower()) if w not in STOP and len(w) > 2}


def matches(idea):
    nes, popular, history, roblox = collect()
    iw = words(idea)
    hits = []
    for n, s in nes + popular + history + roblox:
        if iw & words(s) or idea.lower() in s.lower():
            hits.append((n, s))
    return hits


def check(ideas):
    found = False
    for idea in ideas:
        hits = matches(idea)
        if hits:
            found = True
            print(f"! {idea}: already covered in " + "; ".join(f"#{n} {s}" for n, s in hits))
        else:
            print(f"  {idea}: new")
    return found


def check_batch(path):
    src = open(path).read()
    names = re.findall(r'ep\(\d+, "[^"]+", "([^"]+)"', src)
    return check(names)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("update")
    c = sub.add_parser("check"); c.add_argument("ideas", nargs="+")
    b = sub.add_parser("check-batch"); b.add_argument("generator")
    a = ap.parse_args()
    if a.cmd == "update":
        update()
    elif a.cmd == "check":
        sys.exit(1 if check(a.ideas) else 0)
    else:
        sys.exit(1 if check_batch(a.generator) else 0)
