"""Writes batch 26 (facts checked 2026-11-01): 5 Roblox + 4 GD + 1 meme (AI game merging) = #231-240.

Engine v2 format (user plan, Oct 27 2026), not a hard rule:
  1. HOOK   - the loudest / most dramatic real clip plays with its OWN sound for ~0.8s before the narrator talks
  2. STORY  - short backstory, one or two numbers max, no info overload
  3. ACTION - more real footage (one designed scene where a clip can't show it, e.g. the GD race bars)
  4. END    - a short question over the hook clip again (so the Short loops), no long like/subscribe card
Natural length (~20-25s): target 0 = no padding. No 'Next:' teasers. Clips: batches/batch-23.json (app downloads + cuts
them WITH audio now)."""

import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MF = "../modern/fonts/"
RB, CLIPS = [], []
MIKE, SARAH, HEART, FENRIR, LIAM, PUCK = "am_michael", "af_sarah", "af_heart", "am_fenrir", "am_liam", "am_puck"
ASK = "COMMENT BELOW"


def L(t, sc, say=None):
    d = {"t": t, "sc": sc}
    if say:
        d["say"] = say
    return d


def CLIP(name, big, sub, start, credit, **k):
    """Full-screen real clip (with its own sound) and the title over it."""
    k.setdefault("by", 300)
    k.setdefault("bs", 150)
    k.setdefault("ss", 56)
    d = dict(bg="night", ground="dark", full={"credit": credit, "clip": name, "start": start})
    if big:
        d["big"] = big
    if sub:
        d["sub"] = sub
    d.update(k)
    return d


def CCOUNT(name, start, credit, to, sub, fmt="{:,.0f}", **k):
    """A number counting up OVER a real clip (v2: no flat number cards)."""
    d = CLIP(name, None, sub, start, credit, bs=k.pop("bs", 170), **k)
    d["count"] = {"from": 0, "to": to, "fmt": fmt, "dur": 1.3}
    return d


def clip(name, url, section, cut=2, backup=None, ln=13):
    CLIPS.append({"name": name[:-4], "url": url, "backup": backup or [], "section": section, "cut": cut, "len": ln})


def ask(say, big, name, credit, start=0.0):
    """Ending: one question over the hook clip again, so the Short loops back into its first second."""
    return L(say, CLIP(name, big, ASK, start, credit, bs=140, ss=50))


def ep(num, slug, name, voice, accent, cap, lines, pron=None, **k):
    RB.append(dict(num=num, slug=f"{num}-{slug}", file=f"{num} {name}.mp4", target=0, accent=accent,
                   voice=voice, speed=1.06, cap=cap, pron=pron or {}, lines=lines,
                   lead=1.7, tail=0.5, clip_audio=True, **k))


GD_PRON = {"Demonlist": "Demon list", "Zoink": "Zoynk", "wPopoff": "W Pop off", "Cuatrocientos": "Kwatro-see-entos"}
GDE = dict(edition="GEOMETRY DASH", mood="spooky")

# ============================================================ ROBLOX (live numbers from Roblox, Oct 27)

# v2.1 (user, Oct 27): first ~1.7 s is ONLY the real clip's sound (no TTS), then a quick subscribe reminder after the question.
# Channel had ~170 subscribers on Oct 31, 2026, so "500 by Christmas" is still a real goal.
def subline(name, credit, start=0.0):
    return L("Help a small creator hit 500 subs by Christmas!",
             CLIP(name, "SUBSCRIBE", "HELP US HIT 500 BY CHRISTMAS", start, credit, bs=150, ss=44))


# Analytics (Nov 1): new Roblox games + GD attempt/drama stories win; old-internet lore and an image-only meme flopped,
# so this batch is 5 new Roblox games, 4 GD, and a gaming-tied meme trend with real video.
GD_PRON.update({"MindCap": "Mind Cap", "Zoink": "Zoynk", "spaceuk": "space U K", "Hqmy": "H Q M Y", "RobTop": "Rob Top",
                "meganeko": "meh-ga-neh-ko", "Demonlist": "Demon list", "Zodiac": "Zodiac"})

# ============================================================ ROBLOX (live numbers from Roblox, Nov 1)
TFC = "Clips: FoltynPlays; CaylusBlox (Roblox gameplay, YouTube)"
clip("rb26-tf-a.mp4", "https://www.youtube.com/watch?v=55cCOFQ6pzk", "*1:00-1:20", cut=0, backup=["https://www.youtube.com/watch?v=wzNIsJZpV8Q"])
clip("rb26-tf-b.mp4", "https://www.youtube.com/watch?v=55cCOFQ6pzk", "*5:00-5:20", cut=0)
clip("rb26-tf-c.mp4", "https://www.youtube.com/watch?v=D6wVp6vArzU", "*9:00-9:20", cut=0)
ep(231, "throw-food-for-animals", "In This Roblox Game You Throw Food to Catch Animals", PUCK, "#ffab00",
   {"font": MF + "Bangers-Regular.ttf", "size": 120, "mode": "word", "fill": "#ffffff", "hi": "#ffd740", "cy": 1470},
   [L("In this Roblox game, you throw food as far as you can, and see what comes running.",
      CLIP("rb26-tf-a.mp4", "THROW FOOD\nFOR ANIMALS", "AS FAR AS YOU CAN", 0, TFC, bs=120)),
    L("Every throw attracts animals. Catch them, and they make you money.",
      CLIP("rb26-tf-b.mp4", "CATCH\nTHEM", "THEY MAKE YOU MONEY", 0, TFC)),
    L("Buy better food for rarer animals, and do pull-ups to throw even further.",
      CLIP("rb26-tf-c.mp4", "PULL-UPS", "MORE THROW POWER", 0, TFC, bs=180)),
    L("It's about 6 weeks old, with almost 33 million visits.",
      CCOUNT("rb26-tf-b.mp4", 6.0, TFC, 32964686, "VISITS", bs=140)),
    ask("What animal would you throw food for?", "WHAT WOULD\nYOU CATCH?", "rb26-tf-a.mp4", TFC),
    subline("rb26-tf-a.mp4", TFC, 3.0),
   ])

CSC = "Clips: Bespecter; Radex Tips; ItzVexo (Roblox gameplay, YouTube)"
clip("rb26-cs-a.mp4", "https://www.youtube.com/watch?v=qfcUct1pKmU", "*0:30-0:50", cut=0, backup=["https://www.youtube.com/watch?v=4R9J3kARygA"])
clip("rb26-cs-b.mp4", "https://www.youtube.com/watch?v=qfcUct1pKmU", "*3:00-3:20", cut=0)
clip("rb26-cs-c.mp4", "https://www.youtube.com/watch?v=oEfL1e2QL84", "*6:00-6:20", cut=0, backup=["https://www.youtube.com/watch?v=4R9J3kARygA"])
ep(232, "criminal-simulator", "In Criminal Simulator You Pay Your Debt or Face the Sniper", FENRIR, "#ff1744",
   {"font": MF + "BlackOpsOne-Regular.ttf", "size": 92, "fill": "#ffffff", "hi": "#ff8a80", "stroke": 8},
   [L("In this Roblox game, if you don't pay your debt, a sniper comes for you.",
      CLIP("rb26-cs-a.mp4", "CRIMINAL\nSIMULATOR", "PAY UP", 0, CSC)),
    L("You and up to 3 friends rob the city at night. Sneak past the people living there.",
      CLIP("rb26-cs-b.mp4", "ROB THE\nCITY", "UP TO 4 PLAYERS", 0, CSC)),
    L("Outrun the police and their dogs, and sell your loot before the deadline.",
      CLIP("rb26-cs-c.mp4", "RUN", "POLICE AND DOGS", 0, CSC, bs=200)),
    L("It's still in alpha, and it already has over 7 million visits.",
      CCOUNT("rb26-cs-b.mp4", 6.0, CSC, 7166199, "VISITS", bs=140)),
    ask("Would you pay the debt, or run?", "PAY OR\nRUN?", "rb26-cs-a.mp4", CSC),
    subline("rb26-cs-a.mp4", CSC, 3.0),
   ], mood="spooky")

NRC = "Clips: Dxnny; NoobBlox (Roblox gameplay, YouTube)"
clip("rb26-nr-a.mp4", "https://www.youtube.com/watch?v=0l1dLXR97ZM", "*2:00-2:20", cut=0, backup=["https://www.youtube.com/watch?v=EYz2McCjNJY"])
clip("rb26-nr-b.mp4", "https://www.youtube.com/watch?v=0l1dLXR97ZM", "*8:00-8:20", cut=0)
clip("rb26-nr-c.mp4", "https://www.youtube.com/watch?v=EYz2McCjNJY", "*1:00-1:20", cut=0, backup=["https://www.youtube.com/watch?v=0rX-hhu92xM"])
ep(233, "night-rider", "In Night Rider the Highway Never Ends", LIAM, "#7c4dff",
   {"font": MF + "RussoOne-Regular.ttf", "size": 92, "hi": "#b388ff", "stroke": 8},
   [L("In this Roblox game, the highway never ends.",
      CLIP("rb26-nr-a.mp4", "NIGHT\nRIDER", "THE ENDLESS HIGHWAY", 0, NRC)),
    L("You ride a motorcycle through traffic, at crazy speeds. City, farms, factories, suburbs.",
      CLIP("rb26-nr-b.mp4", "CRAZY\nSPEEDS", "WEAVE THROUGH TRAFFIC", 0, NRC)),
    L("Pop wheelies, pull tricks, and watch out for the death wobble.",
      CLIP("rb26-nr-c.mp4", "DEATH\nWOBBLE", "DON'T CRASH", 0, NRC)),
    L("It's still in testing, and it's already over 8 million visits.",
      CCOUNT("rb26-nr-b.mp4", 6.0, NRC, 8245245, "VISITS", bs=140)),
    ask("How far could you ride?", "HOW FAR\nCOULD YOU GO?", "rb26-nr-a.mp4", NRC),
    subline("rb26-nr-a.mp4", NRC, 3.0),
   ], mood="spooky")

CMC = "Clips: OTTER ON ROBLOX; Sonoket Gaming (Roblox gameplay, YouTube)"
clip("rb26-cm-a.mp4", "https://www.youtube.com/watch?v=5tNfFioOF3c", "*3:00-3:20", cut=0, backup=["https://www.youtube.com/watch?v=ET1g1nYfyUE"])
clip("rb26-cm-b.mp4", "https://www.youtube.com/watch?v=5tNfFioOF3c", "*20:00-20:20", cut=0)
clip("rb26-cm-c.mp4", "https://www.youtube.com/watch?v=4C6poRImasE", "*1:00:00-1:00:20", cut=0, backup=["https://www.youtube.com/watch?v=ET1g1nYfyUE"])
ep(234, "clean-the-moon", "In This Roblox Game You Clean the Whole Moon", HEART, "#90caf9",
   {"font": MF + "Bangers-Regular.ttf", "size": 120, "mode": "word", "fill": "#ffffff", "hi": "#bbdefb", "cy": 1470},
   [L("In this Roblox game, your job is to clean the entire Moon.",
      CLIP("rb26-cm-a.mp4", "CLEAN THE\nMOON", "THE WHOLE THING", 0, CMC)),
    L("Grab a broom, and sweep up moon dust, space junk, and meteor rocks.",
      CLIP("rb26-cm-b.mp4", "SWEEP", "DUST, JUNK, METEORS", 0, CMC, bs=200)),
    L("Sell it, upgrade your moon boots, and unlock robots that clean the Moon for you.",
      CLIP("rb26-cm-c.mp4", "CLEANING\nROBOTS", "BUILD A MOON BASE", 0, CMC)),
    L("It came out in October, and it already has over 2 and a half million visits.",
      CCOUNT("rb26-cm-b.mp4", 6.0, CMC, 2591336, "VISITS", bs=140)),
    ask("Would you clean the Moon?", "WOULD YOU\nCLEAN IT?", "rb26-cm-a.mp4", CMC),
    subline("rb26-cm-a.mp4", CMC, 3.0),
   ])

BYC = "Clips: V1rtual; Osawh (Roblox gameplay, YouTube)"
clip("rb26-by-a.mp4", "https://www.youtube.com/watch?v=iQuy_I3qkHU", "*0:05-0:25", cut=0)
clip("rb26-by-b.mp4", "https://www.youtube.com/watch?v=SzV44XZX-8E", "*2:00-2:20", cut=0)
clip("rb26-by-c.mp4", "https://www.youtube.com/watch?v=rzx8nYsHrrA", "*4:00-4:20", cut=0, backup=["https://www.youtube.com/watch?v=MUl6OlLEZ4s"])
ep(235, "bey-rivals", "Bey Rivals Is a Spinning Top Battle Game on Roblox", MIKE, "#00e5ff",
   {"font": MF + "Anton-Regular.ttf", "size": 104, "hi": "#84ffff", "stroke": 8},
   [L("Remember spinning top battles? Now they're on Roblox.",
      CLIP("rb26-by-a.mp4", "BEY\nRIVALS", "LET IT RIP", 0, BYC)),
    L("In Bey Rivals, you launch your top into the arena, and battle other players.",
      CLIP("rb26-by-b.mp4", "BATTLE", "PLAYERS AND BOSSES", 0, BYC, bs=200)),
    L("Collect tops, customize them, upgrade them, and climb to the top of the leaderboard.",
      CLIP("rb26-by-c.mp4", "CUSTOMIZE", "BUILD THE BEST TOP", 0, BYC)),
    L("It came out in October, and it's almost at 8 million visits.",
      CCOUNT("rb26-by-b.mp4", 6.0, BYC, 7839901, "VISITS", bs=140)),
    ask("Did you have spinning tops as a kid?", "DID YOU\nHAVE ONE?", "rb26-by-a.mp4", BYC),
    subline("rb26-by-a.mp4", BYC, 3.0),
   ])

# ============================================================ GEOMETRY DASH (GD wiki + Dashword, Nov 1)
ORC = "Clips: Zoink (YouTube)"
clip("gd26-or-a.mp4", "https://www.youtube.com/watch?v=VVMRwjf9aPw", "*2:56-3:11", cut=0)
clip("gd26-or-b.mp4", "https://www.youtube.com/watch?v=QKcv8DkNPd0", "*3:52-4:12", cut=0)
clip("gd26-or-c.mp4", "https://www.youtube.com/watch?v=QKcv8DkNPd0", "*2:34-2:54", cut=0)
ep(236, "orbit-99-ball-pit", "Zoink Died at 99 Percent in a Ball Pit", MIKE, "#ff9100",
   {"font": MF + "Anton-Regular.ttf", "size": 104, "hi": "#ffd180", "stroke": 8},
   [L("He was one click from beating it. Then he hit the wrong orb.",
      CLIP("gd26-or-a.mp4", "ORBIT", "99%", 0, ORC)),
    L("ORBIT was meant for spaceuk, until he got caught hacking. So Zoink got it.",
      CLIP("gd26-or-c.mp4", "MEANT FOR\nSPACEUK", "THEN ZOINK GOT IT", 0, ORC, bs=130)),
    L("In January, he reached the very end, clicked the wrong orb, and got stuck in a ball pit. 99 percent.",
      CLIP("gd26-or-a.mp4", "THE BALL\nPIT", "99%", 4.0, ORC, bs=150)),
    L("12 days later, he beat it, after about 30,000 attempts. It became the first classic extreme demon rated Mythic.",
      CCOUNT("gd26-or-b.mp4", 0, ORC, 30000, "ATTEMPTS", fmt="~{:,.0f}")),
    ask("Would you have quit after 99 percent?", "QUIT AFTER\n99%?", "gd26-or-a.mp4", ORC),
    subline("gd26-or-a.mp4", ORC, 3.0),
   ], pron=dict(GD_PRON), gd_player="Zoink", **GDE)

EEC = "Clips: MindCap; Zoink (YouTube)"
clip("gd26-ee-a.mp4", "https://www.youtube.com/watch?v=KexrBfBCZJA", "*8:00-8:20", cut=0)
clip("gd26-ee-b.mp4", "https://www.youtube.com/watch?v=KexrBfBCZJA", "*6:28-6:48", cut=0)
clip("gd26-ee-c.mp4", "https://www.youtube.com/watch?v=ZyRmgwSh5tQ", "*19:05-19:25", cut=0)
ep(237, "every-end-29890", "Every End Kicked Two Old Number 1s Off the List", FENRIR, "#e040fb",
   {"font": MF + "BlackOpsOne-Regular.ttf", "size": 92, "fill": "#ffffff", "hi": "#ea80fc", "stroke": 8},
   [L("This level kicked two old number ones off the Demonlist.",
      CLIP("gd26-ee-a.mp4", "EVERY END", "VERIFIED", 0, EEC)),
    L("Every End is a MindCap collab. Two verifiers dropped it, so Hqmy took over.",
      CLIP("gd26-ee-b.mp4", "2 VERIFIERS\nDROPPED IT", "HQMY TOOK OVER", 0, EEC, bs=120)),
    L("In March 2025, he verified it, after about 29,890 attempts.",
      CCOUNT("gd26-ee-b.mp4", 6.0, EEC, 29890, "ATTEMPTS", fmt="~{:,.0f}")),
    L("It went into the top 5. Zodiac got pushed to the extended list, and Bloodlust to the legacy list.",
      CLIP("gd26-ee-c.mp4", "BYE\nZODIAC", "BYE BLOODLUST", 0, EEC)),
    ask("Which old top 1 do you miss most?", "WHICH TOP 1\nDO YOU MISS?", "gd26-ee-a.mp4", EEC),
    subline("gd26-ee-a.mp4", EEC, 3.0),
   ], pron=dict(GD_PRON), gd_player="Hqmy", **GDE)

MDC = "Clips: VortroxTwo; KampMiggy (YouTube)"
clip("gd26-md-a.mp4", "https://www.youtube.com/watch?v=W6z7c1OdUYw", "*0:04-0:24", cut=0)
clip("gd26-md-b.mp4", "https://www.youtube.com/watch?v=W6z7c1OdUYw", "*9:40-10:00", cut=0)
clip("gd26-md-c.mp4", "https://www.youtube.com/watch?v=wrX1q8rfnwc", "*0:30-0:50", cut=0)
ep(238, "gd-moderator-purge", "RobTop Removed Half of Geometry Dashs Moderators", LIAM, "#ffd600",
   {"font": MF + "RussoOne-Regular.ttf", "size": 92, "hi": "#ffff00", "stroke": 8},
   [L("Half of Geometry Dash's moderators got removed in one morning.",
      CLIP("gd26-md-a.mp4", "DEMOTED", "THE MOD PURGE", 0, MDC, bs=200)),
    L("In September, RobTop rebuilt the team, and 42 moderators were demoted. Most found out that same morning.",
      CCOUNT("gd26-md-c.mp4", 0, MDC, 42, "MODS DEMOTED")),
    L("Moderators are now called Rating Advisors. Applications are closed for good, and new ones won't be announced.",
      CLIP("gd26-md-b.mp4", "RATING\nADVISORS", "NO MORE APPLICATIONS", 0, MDC, bs=130)),
    L("RobTop said he wanted a smaller, clearer team. A lot of players weren't happy.",
      CLIP("gd26-md-a.mp4", "SMALLER\nTEAM", "PLAYERS WEREN'T HAPPY", 6.0, MDC, bs=140)),
    ask("Was RobTop right?", "WAS ROBTOP\nRIGHT?", "gd26-md-a.mp4", MDC),
    subline("gd26-md-a.mp4", MDC, 3.0),
   ], pron=dict(GD_PRON), gd_player="RobTop", **GDE)

UPD = "Clips: RobTop Games (2.209 trailer); Colours Gaming (YouTube)"
clip("gd26-up-a.mp4", "https://www.youtube.com/watch?v=gLlwslqKvQc", "*0:05-0:25", cut=0)
clip("gd26-up-b.mp4", "https://www.youtube.com/watch?v=YWR_h8jvUhE", "*6:58-7:18", cut=0)
clip("gd26-up-c.mp4", "https://www.youtube.com/watch?v=YWR_h8jvUhE", "*12:52-13:12", cut=0)
clip("gd26-up-d.mp4", "https://www.youtube.com/watch?v=gLlwslqKvQc", "*0:26-0:46", cut=0)
ep(239, "gd-2-209", "Geometry Dash Now Shows You Every Place You Died", SARAH, "#00e676",
   {"font": MF + "Bangers-Regular.ttf", "size": 120, "mode": "word", "fill": "#ffffff", "hi": "#69f0ae", "cy": 1470},
   [L("Geometry Dash can now show you every single place you died.",
      CLIP("gd26-up-a.mp4", "UPDATE\n2.209", "IT'S OUT", 0, UPD)),
    L("Update 2.209 came out on October 16th. Platformer levels finally save your progress.",
      CLIP("gd26-up-b.mp4", "PLATFORMER\nSAVES", "OCTOBER 16", 0, UPD, bs=120)),
    L("There's a death tracker, with markers on every spot you died. And you can set your own keybinds.",
      CLIP("gd26-up-c.mp4", "DEATH\nMARKERS", "EVERY. SINGLE. DEATH.", 0, UPD)),
    L("Plus group chats, emojis, and a new song by meganeko.",
      CLIP("gd26-up-d.mp4", "GROUP\nCHATS", "AND A NEW SONG", 0, UPD)),
    ask("What should the next update add?", "WHAT'S\nNEXT?", "gd26-up-a.mp4", UPD),
    subline("gd26-up-a.mp4", UPD, 3.0),
   ], pron=dict(GD_PRON), gd_player="RobTop", **GDE)

# ============================================================ MEME (Know Your Meme: AI Video Game Merging, Sept-Oct 2026)
AIC = "Clips: Tobyn Jacobs; chasm; Tanox; Chrispreds3 (YouTube)"
clip("tr26-ai-a.mp4", "https://www.youtube.com/watch?v=TmgAK5JjcDM", "*0:20-0:40", cut=0)
clip("tr26-ai-b.mp4", "https://www.youtube.com/watch?v=zRT3MyFwgu0", "*1:00-1:20", cut=0)
clip("tr26-ai-c.mp4", "https://www.youtube.com/watch?v=0-NM9HyaSt8", "*0:30-0:50", cut=0)
clip("tr26-ai-d.mp4", "https://www.youtube.com/watch?v=xkfIvE59AqA", "*2:00-2:20", cut=0, backup=["https://www.youtube.com/watch?v=LuityjCJ1Hg"])
ep(240, "ai-game-merging", "People Are Using AI to Merge Video Games", PUCK, "#ff4081",
   {"font": MF + "Bangers-Regular.ttf", "size": 120, "mode": "word", "fill": "#ffffff", "hi": "#ff80ab", "cy": 1470},
   [L("Someone put Minecraft inside Elden Ring, and AI did most of the work.",
      CLIP("tr26-ai-a.mp4", "MINECRAFT\nIN ELDEN RING", "MADE WITH AI", 0, AIC, bs=110)),
    L("In September, people started using AI to merge video games. It reads both games' code, and makes them run together.",
      CLIP("tr26-ai-b.mp4", "AI GAME\nMERGING", "THE NEW TREND", 0, AIC, bs=130)),
    L("Call of Duty with Minecraft. Skate tricks in Modern Warfare 2.",
      CLIP("tr26-ai-d.mp4", "COD +\nMINECRAFT", "WHY NOT", 0, AIC, bs=140)),
    L("Then someone put Mario 64 inside Elden Ring. Almost 3 million views, until it got taken down for copyright.",
      CLIP("tr26-ai-c.mp4", "MARIO IN\nELDEN RING", "TAKEN DOWN", 0, AIC, bs=130)),
    ask("What 2 games should be merged next?", "MERGE WHAT\nNEXT?", "tr26-ai-a.mp4", AIC),
    subline("tr26-ai-a.mp4", AIC, 3.0),
   ], pron={"Elden Ring": "Elden Ring"}, prop_clip="tr26-ai-b.mp4", edition="MEME LORE")

# ================================================================== write
paths = []
for e in RB:
    e = dict(preset="roblox", hdr="tag", **e)
    words = sum(len(l.get("say", l["t"]).split()) for l in e["lines"])
    p = os.path.join("episodes", "roblox", e["slug"] + ".json")
    json.dump(e, open(os.path.join(ROOT, p), "w"), indent=1, ensure_ascii=False)
    paths.append(p)
    print(e["slug"], len(e["lines"]), "lines", words, "words")
manifest = {"batch": 26, "note": "Throw Food For Animals, Criminal Simulator, Night Rider, Clean the Moon, Bey Rivals, ORBIT, Every End, GD mod purge, GD 2.209, AI game merging",
            "posting": "batch-26/posting.txt", "episodes": paths, "clips": CLIPS}
json.dump(manifest, open(os.path.join(ROOT, "batches", "batch-26.json"), "w"), indent=1)
print(len(CLIPS), "clips")
