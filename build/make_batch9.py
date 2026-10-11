"""Writes batch 9 (facts checked 2026-10-11): 7 videos with varied lengths, looks, caption styles and voices.
Most Popular Games #43-47, 8-Bit Backstory #74 (NES look) and #75 (Roblox look). Openings name the game or a hook, never a year."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CTA = " Comment for which game we should review next! Follow for more!"
CTA_SUB = "COMMENT FOR WHICH GAME\nWE SHOULD REVIEW NEXT!"


def L(t, sc, say=None):
    d = {"t": t, "sc": sc}
    if say:
        d["say"] = say
    return d


# ------------------------------------------------------------------ popular helpers
def hook(img, big, label, credit, **k):
    return dict(kind="hook", img=img, big=big, label=label, credit=credit, **k)


def text(big, icon=None, sub=None, **k):
    d = dict(kind="text", big=big, **k)
    if icon:
        d["icon"] = icon
    if sub:
        d["sub"] = sub
    return d


def stat(val=None, label=None, sub=None, icon=None, num=None, **k):
    d = dict(kind="stat", **k)
    if num:
        d["num"] = num
    else:
        d["val"] = val
    for n, v in (("label", label), ("sub", sub), ("icon", icon)):
        if v:
            d[n] = v
    return d


def lst(items, head=None):
    return dict(kind="list", items=items, **({"head": head} if head else {}))


def photo(img, label, credit, **k):
    return dict(kind="photo", img=img, label=label, credit=credit, **k)


def vs(left, right):
    return dict(kind="vs", left=left, right=right)


def outro(q, question):
    return L(q + CTA, dict(kind="outro", question=question))


POP = []

# ------------------------------------------------------------------ 43 Flappy Bird (~40 s, pixel look, one-word captions, female voice)
POP.append(dict(num=43, theme="flappy", game="Flappy Bird", slug="43-flappy-bird", target=42, voice="af_heart", speed=1.08,
    pron={"Nguyen": "Win", "PewDiePie": "Pew Dee Pie"},
    lines=[
        L("Flappy Bird was made in about three days, and at its peak it earned around 50,000 dollars a day.",
          hook("pop9-pigeon.jpg", ["FLAPPY BIRD", "*$50,000 A DAY"], "A REAL BIRD, FLAPPING", "Photo: Thomas Quine, CC BY 2.0", size=96)),
        L("Dong Nguyen, a developer in Vietnam, built it in two to three days. It was first called Flap Flap.",
          text(["FLAP", "*FLAP"], "user", "the original name", size=150)),
        L("It flopped at first, until PewDiePie played it.",
          text(["THEN ONE", "*VIDEO"], "video", "PewDiePie played it")),
        L("In January 2014, it was the most downloaded app on the App Store.",
          stat("#1", "MOST DOWNLOADED APP", "January 2014", "download", size=220)),
        L("Then he tweeted he'd take it down in 22 hours, and he did. He said it had become too addictive.",
          stat("22 HRS", "UNTIL IT WAS GONE", "he called it too addictive", "clock", size=170)),
        L("Phones with it still installed were listed on eBay for thousands of dollars.",
          text(["$1,499+", "*PHONES"], "cart-shopping", "eBay listings, 2014", size=130)),
        outro("Did you ever beat your high score?", "BEAT YOUR HIGH SCORE?"),
    ]))

# ------------------------------------------------------------------ 44 Wii Sports (~57 s, clean white look, boxed sentence-case captions, British female voice)
POP.append(dict(num=44, theme="wiisports", game="Wii Sports", slug="44-wii-sports", target=60, voice="bf_emma", speed=1.1,
    pron={"Fils-Aime": "Fills Ah-may", "Iwata": "Ee-wata", "Miyamoto": "Mee-ya-moto", "Miis": "Mees"},
    lines=[
        L("Wii Sports is Nintendo's best-selling game ever, with over 82 million copies.",
          hook("pop9-wiistrap.jpg", ["Wii Sports", "*82 million copies"], "A REAL WII REMOTE STRAP", "Photo: Morgan from Montreal, CC BY 2.0", size=100)),
        L("It launched with the Wii in November 2006, and came free in the box almost everywhere except Japan and Korea.",
          text(["Free in", "*the box"], "gift", "everywhere but Japan and Korea")),
        L("There were five sports: tennis, baseball, bowling, golf, and boxing.",
          lst([["table-tennis-paddle-ball", "Tennis"], ["baseball", "Baseball"], ["bowling-ball", "Bowling"], ["golf-ball-tee", "Golf"], ["hand-fist", "Boxing"]], "5 sports")),
        L("Early on, it starred Mario characters, but players liked their own Miis better.",
          vs(["Before", "Mario", "early builds"], ["After", "Miis", "players' choice"])),
        L("Nintendo almost didn't bundle it. Reggie Fils-Aime convinced Miyamoto and Iwata.",
          text(["Almost", "*not bundled"], "handshake", "Reggie made the case")),
        L("Players swung so hard that remotes flew out of their hands, so Nintendo made the wrist straps almost twice as thick.",
          stat("2x", "thicker wrist straps", "after flying remotes", "hand", size=220)),
        L("Senior centers even started their own Wii bowling leagues. And it won six BAFTA awards in 2007.",
          lst([["users", "Senior bowling leagues"], ["trophy", "6 BAFTAs, 2007"]])),
        L("A tough opponent named Matt became a meme, and he came back as a secret boss in Switch Sports.",
          text(["Matt"], "user-ninja", "the meme, now a secret boss", size=200)),
        L("In 2023, it joined the World Video Game Hall of Fame.",
          text(["Hall of", "*Fame"], "award", "World Video Game Hall of Fame, 2023")),
        outro("What was your best sport?", "Your best sport?"),
    ]))

# ------------------------------------------------------------------ 45 Angry Birds (~72 s, comic look, big punchy captions, female voice)
POP.append(dict(num=45, theme="angry", game="Angry Birds", slug="45-angry-birds", target=86, voice="af_nicole", speed=1.12,
    pron={"Rovio": "Ro-vee-oh", "Jaakko": "Yak-ko", "Iisalo": "Ee-salo"},
    lines=[
        L("Before Angry Birds, Rovio had already made 51 games for other companies.",
          hook("pop9-slingshot.jpg", ["ANGRY BIRDS", "*GAME NUMBER 52"], "A REAL GIANT SLINGSHOT", "Photo: SSG B. Lashleyleidner, U.S. Army, PD", size=92)),
        L("By 2009, the studio could only afford to make one more game of its own.",
          text(["ONE LAST", "*SHOT"], "coins", "money for one game")),
        L("Designer Jaakko Iisalo drew some grumpy birds with angry eyebrows, and the team picked it before they even had the gameplay.",
          text(["ANGRY", "*EYEBROWS"], "pencil", "picked before the gameplay existed")),
        L("The slingshot idea was first rejected for being too obvious.",
          text(["TOO", "*OBVIOUS"], "ban", "the slingshot, at first")),
        L("And the pigs? People say they came from swine flu, but Iisalo says he drew them when he was ten.",
          vs(["MYTH", "FLU", "swine flu"], ["TRUTH", "AGE 10", "his childhood drawings"])),
        L("It launched on iPhone in December 2009, with 63 levels.",
          stat("63", "LEVELS AT LAUNCH", "December 2009", "mobile-screen", size=230)),
        L("It stayed number one on the paid App Store chart for 275 days, a record.",
          stat(num=[275, "{:.0f} DAYS"], label="AT #1 (RECORD)", icon="trophy")),
        L("By the end of 2010, it had 50 million downloads. On Android, the free version made about a million dollars a month from ads.",
          vs(["DOWNLOADS", "50M", "by end of 2010"], ["ADS", "$1M", "per month, Android"])),
        L("In 2019, the original was pulled from app stores, and fans started the hashtag Bring Back 2012.",
          text(["#BRING", "*BACK2012"], "hashtag", "after it vanished in 2019", size=120)),
        L("And this May, it entered the World Video Game Hall of Fame.",
          text(["HALL OF", "*FAME"], "award", "May 2026")),
        outro("Which bird was your favorite?", "FAVORITE BIRD?"),
    ]))

# ------------------------------------------------------------------ 46 Club Penguin (~64 s, icy look, boxed sentence-case captions, female voice)
POP.append(dict(num=46, theme="cpenguin", game="Club Penguin", slug="46-club-penguin", target=66, voice="af_bella", speed=1.1,
    pron={"Priebe": "Pree-bee", "Merrifield": "Merry-field", "Krysko": "Kris-ko", "Puffle": "Puffle"},
    lines=[
        L("Club Penguin started because three dads couldn't find a safe website for their kids.",
          hook("pop9-penguin.jpg", ["Club Penguin", "*Built by 3 dads"], "A REAL PENGUIN, MID-JUMP", "Photo: Christopher Michel, CC BY 2.0", size=100)),
        L("Lance Priebe, Lane Merrifield and Dave Krysko launched it in October 2005, with 15,000 users.",
          stat(num=[15000, "{:,.0f}"], label="Players on day one", sub="October 2005", icon="users")),
        L("They paid for it with their own credit, and kept 100 percent of the company.",
          text(["100%", "*theirs"], "piggy-bank", "no investors")),
        L("Less than two years later, Disney bought it for about 350 million dollars.",
          stat("$350M", "Disney buys it", "August 2007", "handshake", size=190)),
        L("About 70 of its 100 staff worked on keeping the game safe, and swearing could get you banned for 24 hours.",
          vs(["Staff", "70/100", "kept it safe"], ["Swearing", "24h", "auto ban"])),
        L("By 2013, it had over 200 million accounts. About 90 percent of players never paid, and there were no ads.",
          stat("200M+", "accounts", "by July 2013", "snowflake", size=190)),
        L("It shut down on March 30, 2017.",
          text(["Waddle", "*on"], "igloo", "March 30, 2017")),
        L("In the final hours, players raced to get banned as fast as possible. The record was under 40 seconds.",
          stat("<40 SEC", "fastest ban", "the last day", "stopwatch", size=170)),
        L("A fan-made copy, Club Penguin Rewritten, grew to over 11 million users, until police shut it down in 2022 after a request from Disney.",
          text(["Rewritten", "*11M users"], "shield", "shut down in 2022", size=120)),
        outro("What was your favorite Puffle?", "Favorite Puffle?"),
    ]))

# ------------------------------------------------------------------ 47 Goat Simulator (~45 s, chaos look, one-word handwritten captions, British male voice)
POP.append(dict(num=47, theme="goat", game="Goat Simulator", slug="47-goat-simulator", target=46, voice="bm_lewis", speed=1.05,
    pron={},
    lines=[
        L("Goat Simulator started as a joke, at a one-month game jam.",
          hook("pop9-goatroof.jpg", ["Goat Simulator", "*It was a joke"], "A REAL GOAT, ON A ROOF", "Photo: Tim Green, CC BY 2.0", size=96)),
        L("The goat model cost the team less than 20 dollars.",
          stat("<$20", "for the goat", "bought from a model store", "tag", size=220)),
        L("They only fixed bugs that crashed the game. Every other glitch stayed in, because it was hilarious.",
          text(["Bugs", "*stayed in"], "bug", "on purpose")),
        L("The alpha trailer passed a million YouTube views in two days.",
          stat("1M", "views in 2 days", "the alpha trailer", "video", size=240)),
        L("It launched on April Fools' Day 2014, and made back its budget within minutes.",
          text(["Paid off", "*in minutes"], "coins", "launched April 1st")),
        L("By 2016, it had made over 12 million dollars.",
          stat("$12M+", "earned", "by 2016", "chart-line", size=210)),
        L("The sequel is called Goat Simulator 3. There is no Goat Simulator 2.",
          vs(["Goat Sim 2", "?", "doesn't exist"], ["Goat Sim 3", "3", "2022"])),
        outro("What's the dumbest thing you did as the goat?", "Dumbest goat moment?"),
    ]))

# ================================================================== Roblox Edition
def S(big=None, sub=None, bg="day", ground="grass", **k):
    d = dict(bg=bg, ground=ground)
    if big:
        d["big"] = big
    if sub:
        d["sub"] = sub
    d.update(k)
    return d


def opener(big, sub, img, label, credit, bg="day", ground="grass", **k):
    ph = dict(img=img, label=label, credit=credit, y=k.pop("py", 800), h=k.pop("ph", 430))
    ph.update(k.pop("pk", {}))
    return S(big, sub, bg, ground, instant=True, by=310, photo=ph, **k)


def end(q, big, bg="party", **k):
    av = [{"p": [-1.8, 0.6], "a": "cheer", "c": "a"}, {"p": [0, 1.2], "a": "wave", "c": "g"}, {"p": [1.8, 0.6], "a": "cheer", "c": "b"}]
    return L(q + CTA, S(big, CTA_SUB, bg, "purple", rays="#ffffff", ss=50, sgap=62, fx=["confetti"], av=av, **k))


def crowd(n=25, appear=1.2):
    return {"n": n, "appear": appear}


RB = []

def av(p, a="bob", c="a", **k):
    d = {"p": p, "a": a, "c": c}
    d.update(k)
    return d

# ------------------------------------------------------------------ 75 IKEA on Roblox (30 s, blocky 3D look, female voice)
RB.append(dict(num=75, slug="75-ikea-on-roblox", file="75 IKEA on Roblox (30s).mp4", target=30, accent="#ffd23c", bpm=112, root=62, voice="af_sarah", speed=1.08,
    pron={"IKEA": "eye-kee-ah"},
    lines=[
        L("IKEA once paid real people real money to work in a Roblox store.",
          opener("IKEA ON\nROBLOX", "A REAL JOB. IN ROBLOX.", "pop9-meatballs.jpg", "REAL SWEDISH MEATBALLS", "Photo: Hakan Dahlstrom, CC BY 2.0",
                 bg="day", ground="wood", bs=116, ss=48, py=905, ph=400)),
        L("It was called The Co-Worker Game, and it opened in June 2024.",
          S("THE CO-WORKER\nGAME", "OPENED JUNE 2024", "mint", "wood", bs=104, props=[["house", -2.6, -2.6, {"c": "#1e5fb4"}]], av=[av([1.4, 1.0], "wave", "g", hat="#ffd23c")])),
        L("IKEA hired 10 players from the UK and Ireland, at 13 pounds 15 an hour. Applicants had to say which pixel IKEA furniture they'd be.",
          S("£13.15\nAN HOUR", "10 PLAYERS HIRED", "gold", "wood", rays="#ffffff", bs=130, fx=["coins"], av=[av([-1.0, 0.8], "cheer", "a"), av([1.0, 0.8], "cheer", "e")])),
        L("They served virtual meatballs, helped customers, and could even get promoted.",
          S("PROMOTED!", "IN A ROBLOX STORE", "party", "purple", rays="#ffffff", bs=170, props=[["crate", -1.8, -1.4]], av=[av([0.6, 0.8], "jump", "b", hat="#ffd23c")], fx=["confetti"])),
        end("Would you take that job?", "WOULD YOU\nTAKE IT?"),
    ]))

NES = dict(preset="nes", num=74, name="E.T. Burial", slug="etburial", theme="dark", voice="af_sky", speed=1.08,
    title_lines=["E.T.", "BURIED"], year_tag="ATARI 2600", music={"bpm": 120, "tr": -3, "seed": 74},
    pron={"Alamogordo": "Ala-mo-gordo", "Warshaw": "War-shaw"},
    lines=[
        {"say": "Atari once buried truckloads of video games in the New Mexico desert.", "scene": {"kind": "title", "prop": "photo", "args": {"file": "pop9-landfill.jpg", "rect": [14, 96, 166, 196], "label": "PHOTO: TAYLORHATMAKER CC BY"}}},
        {"say": "The most famous one was E.T., for the Atari 2600.", "scene": {"bg": "space", "head": "E.T.", "headsc": 5, "prop": "crt", "subs": ["ATARI 2600"]}, "cap": "The most famous one was E.T., for the Atari 2600."},
        {"say": "Its programmer, Howard Scott Warshaw, had only five weeks to make the whole game.", "scene": {"bg": "desk", "head": "5 WEEKS", "headsc": 4, "prop": "computer", "args": {"text": "E.T."}, "subs": ["TO MAKE IT ALL"]}},
        {"say": "Atari made five million cartridges, but only about one and a half million sold at first.", "scene": {"bg": "dark", "head": "5 MILLION MADE", "headsc": 2, "prop": "bignum", "args": {"n": 1.5, "fmt": "{:.1f}M", "unit": "SOLD AT FIRST"}}, "cap": "Atari made 5 million cartridges, but only about 1.5 million sold at first."},
        {"say": "Then in September 1983, trucks dumped Atari games at a landfill in Alamogordo, and covered them in concrete.", "scene": {"bg": "graveyard", "head": "BURIED", "headsc": 4, "prop": "none", "subs": ["ALAMOGORDO, NEW MEXICO", "UNDER CONCRETE"]}},
        {"say": "For years, people called it an urban legend.", "scene": {"bg": "dark", "head": "A LEGEND?", "headsc": 3, "prop": "quote", "args": {"text": "MILLIONS OF E.T. GAMES UNDER THE DESERT?"}}},
        {"say": "In April 2014, a film crew dug it up, in front of a crowd.", "scene": {"bg": "dark", "head": "THE 2014 DIG", "headsc": 2, "prop": "photo", "args": {"file": "pop9-landfill.jpg", "rect": [10, 70, 170, 190], "label": "TAYLORHATMAKER CC BY 2.0"}}},
        {"say": "They found about 1,300 cartridges, from 59 different games. Not millions of E.T.s.", "scene": {"bg": "dark", "head": "FOUND", "headsc": 3, "prop": "bignum", "args": {"n": 1300, "fmt": "{:,.0f}", "unit": "CARTRIDGES"}}},
        {"say": "Atari's own records said about 700,000 cartridges were buried in total.", "scene": {"bg": "dark", "head": "THE REAL NUMBER", "headsc": 2, "prop": "bignum", "args": {"n": 700, "fmt": "{:.0f}K", "unit": "BURIED"}}, "cap": "Atari's own records said about 700,000 cartridges were buried in total."},
        {"say": "The city sold them online, and one E.T. cartridge went for over fifteen hundred dollars. Another went to the Smithsonian.", "scene": {"bg": "space", "head": "SOLD!", "headsc": 3, "prop": "award", "args": {"n": "$1500", "text": "ONE E.T. CARTRIDGE"}}, "cap": "The city sold them online, and one E.T. cartridge went for over $1,500. Another went to the Smithsonian."},
        {"say": "Would you have dug for it? Comment for which game we should review next! Follow for more 8-Bit Backstory!", "scene": {"kind": "outro", "question": "WOULD YOU DIG FOR IT?", "ask": "COMMENT WHICH GAME TO REVIEW NEXT!", "prop": "none", "bg": "dark"}},
    ])

# ================================================================== write
ICONS = json.load(open(os.path.join(ROOT, "engine", "modern", "icons.json")))
NAMES = {43: "Flappy Bird", 44: "Wii Sports", 45: "Angry Birds", 46: "Club Penguin", 47: "Goat Simulator"}
os.makedirs(os.path.join(ROOT, "episodes", "popular"), exist_ok=True)
for ep in POP:
    ep = dict(preset="popular", hdr="tag", **ep)
    ep["file"] = f"{ep['num']:02d} - {NAMES[ep['num']]} ({ep['target']}s).mp4"
    slug = ep.pop("slug")
    for l in ep["lines"]:
        sc = l["sc"]
        for ic in [sc.get("icon")] + [i[0] for i in sc.get("items", [])]:
            if ic and ic not in ICONS:
                print("  MISSING ICON", slug, ic)
        if sc.get("img") and not os.path.exists(os.path.join(ROOT, "episodes", "assets", sc["img"])):
            print("  MISSING IMAGE", slug, sc["img"])
    json.dump(ep, open(os.path.join(ROOT, "episodes", "popular", slug + ".json"), "w"), indent=1, ensure_ascii=False)
    print(slug, len(ep["lines"]), "lines", sum(len(l.get("say", l["t"]).split()) for l in ep["lines"]), "words", "target", ep["target"])
for ep in RB:
    ep = dict(preset="roblox", hdr="tag", **ep)
    json.dump(ep, open(os.path.join(ROOT, "episodes", "roblox", ep["slug"] + ".json"), "w"), indent=1, ensure_ascii=False)
    print(ep["slug"], len(ep["lines"]), "lines", sum(len(l.get("say", l["t"]).split()) for l in ep["lines"]), "words", "target", ep["target"])

os.makedirs(os.path.join(ROOT, "episodes", "nes"), exist_ok=True)
NES["file"] = "74 ET Burial.mp4"
json.dump(NES, open(os.path.join(ROOT, "episodes", "nes", "74-et-burial.json"), "w"), indent=1, ensure_ascii=False)
print("74-et-burial", len(NES["lines"]), "lines", sum(len(l["say"].split()) for l in NES["lines"]), "words")
