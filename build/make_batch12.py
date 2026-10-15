"""Writes batch 12 (facts checked 2026-10-15): 10 Roblox videos (8-Bit Backstory #93-102), hook-first openers.
Picked from YouTube analytics: ~30 s Roblox videos with a number or twist up front perform best.
Openings name the game or a hook, never a year."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CTA = " Comment for which game we should review next! Follow for more!"
CTA_SUB = "COMMENT FOR WHICH GAME\nWE SHOULD REVIEW NEXT!"
MF = "../modern/fonts/"


def L(t, sc, say=None):
    d = {"t": t, "sc": sc}
    if say:
        d["say"] = say
    return d


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


def end(q, big, bg="party", ground="purple", **k):
    av_ = [{"p": [-1.8, 0.6], "a": "cheer", "c": "a"}, {"p": [0, 1.2], "a": "wave", "c": "g"}, {"p": [1.8, 0.6], "a": "cheer", "c": "b"}]
    return L(q + CTA, S(big, CTA_SUB, bg, ground, rays="#ffffff", ss=50, sgap=62, fx=["confetti"], av=av_, **k))


def crowd(n=25, appear=1.2):
    return {"n": n, "appear": appear}


def av(p, a="bob", c="a", **k):
    d = {"p": p, "a": a, "c": c}
    d.update(k)
    return d


RB = []
MIKE, SARAH = "am_michael", "af_sarah"


def ep(num, slug, name, target, accent, voice, speed, cap, lines, pron=None, **k):
    RB.append(dict(num=num, slug=f"{num}-{slug}", file=f"{num} {name}.mp4", target=target, accent=accent,
                   voice=voice, speed=speed, cap=cap, pron=pron or {}, lines=lines, **k))


# 93 Roblox removed features (longer story, am_michael like the top-performing oof video)
ep(93, "roblox-deleted-its-own-money", "Roblox Deleted Its Own Money", 48, "#ffd23c", MIKE, 1.1,
   {"font": MF + "RussoOne-Regular.ttf", "size": 84, "hi": "#ffd23c", "stroke": 8},
   [L("Roblox used to have two currencies. Then it deleted one.",
      opener("ROBLOX DELETED\nITS OWN MONEY", "THINGS ROBLOX REMOVED", "pop2-cat-keyboard.jpg", "A REAL CAT ON A KEYBOARD", "Photo: dougwoods, CC BY 2.0",
             bg="red", ground="stone", bs=96, ss=46, py=905, ph=400)),
    L("It was called Tix, short for tickets. It was removed in April 2016, because Roblox said two currencies confused new players.",
      S("TIX", "REMOVED APRIL 2016", "gold", "stone", rays="#ffffff", bs=200, fx=["coins"], ic=[{"n": "coin", "x": 860, "y": 820, "s": 150, "a": "shake"}])),
    L("In 2017, the official forums disappeared.",
      S("FORUMS", "GONE IN 2017", "night", "stone", bs=180, ic=[{"n": "question", "x": 860, "y": 820, "s": 140, "a": "float"}])),
    L("That October, you could no longer play without an account. Guest mode was gone.",
      S("NO MORE\nGUESTS", "OCTOBER 2017", "dark", "stone", bs=140, av=[av([0.0, 0.8], "idle", "a", face="o")])),
    L("Builders Club, the paid membership from 2007, was replaced by Roblox Premium in 2019.",
      S("BUILDERS\nCLUB", "2007 TO 2019", "mint", "stone", bs=140, props=[["tower", -1.6, -2.0], ["block", 1.4, -1.4]], av=[av([0.4, 0.8], "wave", "b", hat="#ffd23c")])),
    L("And in May 2026, Premium itself was replaced, by Roblox Plus.",
      S("PREMIUM\nIS NOW PLUS", "MAY 2026", "party", "purple", rays="#ffffff", bs=124, fx=["sparkle"])),
    L("Even the oof sound was removed in 2022, after a copyright dispute. But in July 2025, it came back.",
      S("OOF IS\nBACK!", "REMOVED 2022, BACK JULY 2025", "gold", "grass", rays="#ffffff", bs=150, ss=42, fx=["confetti"], av=[av([-1.0, 0.8], "cheer", "a"), av([1.0, 0.8], "jump", "e")])),
    end("What do you miss most?", "WHAT DO YOU\nMISS MOST?", bg="red", ground="stone"),
   ], pron={"Tix": "Ticks"})

# 94 Grow a Garden vs Fortnite
ep(94, "grow-a-garden-beat-fortnite", "Grow a Garden Beat Fortnite", 30, "#7cb342", SARAH, 1.04,
   {"font": MF + "Chewy-Regular.ttf", "size": 92, "upper": False, "stroke": 0, "fill": "#ffffff", "hi": "#fff59d", "box": "#2e7d32", "radius": 34},
   [L("A Roblox game about gardening beat Fortnite's all-time player record.",
      opener("IT BEAT\nFORTNITE", "GROW A GARDEN", "pop3-garden.jpg", "A REAL GARDEN", "Photo: Alabama Extension, CC0",
             bg="day", ground="grass", bs=130, ss=46, py=905, ph=400)),
    L("In late June 2025, Grow a Garden had 21.6 million people playing at once.",
      S(None, "PLAYING AT ONCE", "gold", "grass", rays="#ffffff", count={"to": 21.6, "fmt": "{:.1f} MILLION"}, bs=140, crowd=crowd(), fx=["confetti"])),
    L("Fortnite's record had been 15.2 million.",
      S("15.2 MILLION", "FORTNITE'S OLD RECORD", "night", "grass", bs=130, ic=[{"n": "trophy", "x": 860, "y": 820, "s": 140, "a": "shake"}])),
    L("It was made in just a few days, by a 16-year-old. Now it's run by a studio called Splitting Point.",
      S("MADE BY\nA 16-YEAR-OLD", "IN A FEW DAYS", "mint", "grass", bs=116, props=[["tree", -2.2, -2.4]], av=[av([0.4, 0.8], "wave", "c")])),
    L("The seed shop restocks every five minutes, so players keep coming back.",
      S("EVERY\n5 MINUTES", "NEW SEEDS", "sunset", "grass", bs=130, ic=[{"n": "clock", "x": 860, "y": 820, "s": 140, "a": "pulse"}], props=[["crate", -1.4, -1.2]])),
    end("What's your best crop?", "BEST\nCROP?", bg="day", ground="grass"),
   ], pron={"Fortnite": "Fort-nite"})

# 95 Lil Nas X concert
ep(95, "33-million-at-one-concert", "33 Million at One Roblox Concert", 31, "#ff4081", SARAH, 1.0,
   {"font": MF + "Bangers-Regular.ttf", "size": 136, "mode": "word", "fill": "#ffe0f0", "hi": "#ffe0f0", "cy": 1470},
   [L("Over 33 million people showed up to one concert, and it happened inside Roblox.",
      opener("33 MILLION\nAT ONE SHOW", "INSIDE ROBLOX", "pop3-pokemon-go-crowd.jpg", "A REAL CROWD", "Photo: Brian Miller, CC BY 2.0",
             bg="party", ground="purple", bs=120, ss=46, py=905, ph=400)),
    L("It was Lil Nas X, in November 2020, performing as a giant avatar.",
      S("LIL NAS X", "NOVEMBER 2020", "night", "purple", bs=150, props=[["tower", 0.0, -2.6, {"c": "#ff4081"}]], crowd=crowd(14, 0.4), fx=["sparkle"])),
    L("It was announced only four days before it started.",
      S("4 DAYS", "OF WARNING", "red", "purple", bc="#ffffff", bs=190, ic=[{"n": "calendar", "x": 860, "y": 820, "s": 140, "a": "shake"}])),
    L("He played a mix of his biggest songs, and he was there to promote a new one, Holiday.",
      S("HOLIDAY", "THE NEW SONG", "party", "purple", rays="#ffffff", bs=170, ic=[{"n": "star", "x": 860, "y": 820, "s": 140, "a": "spin"}])),
    L("At its peak, nearly a million people were watching at the same time. It became Roblox's most popular concert.",
      S(None, "WATCHING AT ONCE", "gold", "purple", rays="#ffffff", count={"to": 1, "fmt": "~{:.0f} MILLION"}, bs=150, crowd=crowd(), fx=["confetti"])),
    end("Who should play Roblox next?", "WHO PLAYS\nNEXT?", bg="party", ground="purple"),
   ], pron={"Nas": "Naz"})

# 96 John Doe
ep(96, "roblox-account-number-2", "Roblox Account Number 2", 38, "#ef5350", MIKE, 1.08,
   {"font": MF + "CrimsonText-Bold.ttf", "size": 100, "upper": False, "fill": "#f5f5f5", "hi": "#ef9a9a", "stroke": 6},
   [L("Roblox account number 2 was supposed to hack everyone. It never did.",
      opener("ACCOUNT #2:\nTHE 'HACKER'", "JOHN DOE", "pop4-hotel-hallway.jpg", "A REAL EMPTY HALLWAY", "Photo: cogdogblog, CC0",
             bg="dark", ground="dark", bs=110, ss=46, py=905, ph=400, vig=True)),
    L("John Doe and Jane Doe are user IDs 2 and 3. Roblox's founders made them on June 25, 2005, as test accounts.",
      S("IDS 2 & 3", "TEST ACCOUNTS, 2005", "night", "dark", bs=160, av=[av([-1.0, 0.8], "idle", "a"), av([1.0, 0.8], "idle", "g")], ic=[{"n": "code", "x": 860, "y": 800, "s": 130, "a": "float"}])),
    L("In 2017, a rumor spread that they would hack Roblox on March 18th.",
      S("MARCH 18", "THE RUMOR", "red", "dark", bc="#ffffff", bs=170, fx=["red"], vig=True, ic=[{"n": "alarm", "x": 860, "y": 820, "s": 150, "a": "shake"}])),
    L("Nothing happened. Roblox even posted on its blog to calm everyone down.",
      S("NOTHING\nHAPPENED", "ROBLOX POSTED ABOUT IT", "mint", "stone", bs=130, av=[av([0.0, 0.8], "wave", "b")])),
    L("A bug had let players add them as friends without permission. Roblox fixed it, and cleared their friend lists.",
      S("BUG FIXED", "FRIEND LISTS CLEARED", "night", "dark", bs=150, ic=[{"n": "shield", "x": 860, "y": 820, "s": 140, "a": "pulse"}])),
    end("Did you believe the rumor?", "DID YOU\nBELIEVE IT?", bg="dark", ground="dark"),
   ], mood="spooky")

# 97 Pressure
ep(97, "pressure", "Pressure", 31, "#26c6da", SARAH, 1.04,
   {"font": MF + "BlackOpsOne-Regular.ttf", "size": 90, "hi": "#4dd0e1", "stroke": 8},
   [L("In Pressure, the game tells you right away: you're expendable.",
      opener("YOU ARE\nEXPENDABLE", "PRESSURE", "pop7-factory.jpg", "A REAL ABANDONED FACILITY", "Photo: George A. Grant, NARA, public domain",
             bg="dark", ground="dark", bs=130, ss=46, py=905, ph=400, vig=True)),
    L("It's a Roblox horror game by Urbanshade: Hadal Division, and it came out in February 2023.",
      S("ROBLOX\nHORROR", "FEBRUARY 2023", "night", "dark", bs=140, av=[av([0.0, 0.8], "sneak", "a", face="o")], fx=["fireflies"])),
    L("It's inspired by games like Doors, Iron Lung, ULTRAKILL, and SCP: Containment Breach.",
      S("INSPIRED BY", "DOORS, IRON LUNG, ULTRAKILL, SCP", "red", "dark", bc="#ffffff", bs=150, ss=38, fx=["red"], vig=True)),
    L("It's still in alpha, but in March 2026, about 111,000 people played at once. Trackers count nearly half a billion visits.",
      S(None, "PLAYING AT ONCE, MARCH 2026", "gold", "dark", rays="#ffffff", count={"to": 111, "fmt": "{:.0f},000"}, bs=150, crowd=crowd(), fx=["confetti"])),
    end("Would you sign up?", "WOULD YOU\nSIGN UP?", bg="dark", ground="dark"),
   ], pron={"Urbanshade": "Urban-shade", "Hadal": "Hay-dal", "ULTRAKILL": "Ultra-kill", "SCP": "S C P"}, mood="spooky")

# 98 Anime Vanguards
ep(98, "anime-vanguards", "Anime Vanguards", 32, "#ab47bc", SARAH, 1.04,
   {"font": MF + "PermanentMarker-Regular.ttf", "size": 90, "upper": False, "hi": "#ce93d8", "stroke": 9},
   [L("Anime Vanguards turns anime fighters into tower defense.",
      opener("ANIME HEROES\nAS TOWERS", "ANIME VANGUARDS", "pop8-toysoldiers.jpg", "REAL TOY SOLDIERS", "Photo: Jcbutler, public domain",
             bg="sunset", ground="stone", bs=110, ss=46, py=905, ph=400)),
    L("You summon units from rotating banners, then place them to stop waves of enemies.",
      S("SUMMON.\nPLACE. DEFEND.", "WAVE AFTER WAVE", "night", "stone", bs=110, props=[["tower", -1.8, -1.8], ["tower", 1.8, -1.8]], av=[av([0.0, 1.0], "cheer", "e", hold="sword")], fx=["sparkle"])),
    L("It's made by a group called Kitawari, and it launched in January 2024.",
      S("KITAWARI", "JANUARY 2024", "mint", "stone", bs=160, ic=[{"n": "calendar", "x": 860, "y": 820, "s": 140, "a": "float"}])),
    L("Its biggest day came in October 2024, with about 171,000 players at once.",
      S(None, "PLAYING AT ONCE", "gold", "stone", rays="#ffffff", count={"to": 171, "fmt": "{:.0f},000"}, bs=150, crowd=crowd(), fx=["confetti"])),
    L("In March 2026, it even added a level editor. Trackers count about 2 billion visits.",
      S("LEVEL\nEDITOR", "ADDED MARCH 2026", "party", "purple", rays="#ffffff", bs=140, props=[["block", -1.4, -1.2], ["block", 0.0, -1.2], ["block", 1.4, -1.2]])),
    end("Who's your best unit?", "BEST\nUNIT?", bg="sunset", ground="stone"),
   ], pron={"Kitawari": "Kee-ta-wah-ree"})

# 99 The Hunt
ep(99, "the-hunt", "Roblox's Egg Hunt Vanished", 32, "#ffca28", SARAH, 1.04,
   {"font": MF + "TitanOne-Regular.ttf", "size": 80, "stroke": 0, "fill": "#3e2723", "hi": "#d84315", "box": "#ffd54f", "radius": 30},
   [L("Roblox held a giant egg hunt almost every year. Then it disappeared for four years.",
      opener("THE EGG HUNT\nVANISHED", "THEN IT CAME BACK", "pop8-vault.jpg", "A REAL VAULT DOOR", "Photo: Ammodramus, CC0",
             bg="mint", ground="grass", bs=110, ss=46, py=905, ph=400)),
    L("The platform-wide egg hunts started in April 2008, and ended in April 2020.",
      S("2008 TO\n2020", "THE OLD EGG HUNTS", "sunset", "grass", bs=130, ic=[{"n": "egg", "x": 540, "y": 780, "s": 190, "a": "float"}])),
    L("In March 2024, Roblox came back with The Hunt: First Edition, across more than 80 games.",
      S("80+ GAMES", "THE HUNT: FIRST EDITION", "party", "grass", rays="#ffffff", bs=160, crowd=crowd(16, 0.4), fx=["confetti"])),
    L("Finish challenges, earn badges, and badges unlocked items in the Infinite Vault.",
      S("INFINITE\nVAULT", "BADGES UNLOCK ITEMS", "night", "stone", bs=140, props=[["pedestal", 0.0, -0.6]], ic=[{"n": "egg_gold", "x": 540, "y": 760, "s": 170, "a": "pulse"}], fx=["sparkle"])),
    L("Some rare eggs traded for 1,000 Robux or more.",
      S("1,000+\nROBUX", "FOR ONE RARE EGG", "gold", "grass", rays="#ffffff", bs=140, fx=["coins"])),
    end("Did you finish The Hunt?", "DID YOU\nFINISH IT?", bg="mint", ground="grass"),
   ])

# 100 LuoBu
ep(100, "roblox-secret-china-version", "Roblox's Secret China Version", 30, "#e53935", MIKE, 1.08,
   {"font": MF + "Audiowide-Regular.ttf", "size": 76, "hi": "#ff8a80", "stroke": 7},
   [L("Roblox once had a separate version, just for China.",
      opener("ROBLOX'S\nOTHER VERSION", "LUOBU", "pop6-computer-lab.jpg", "A REAL COMPUTER LAB", "Photo: Todd Huffman, CC BY 2.0",
             bg="night", ground="stone", bs=116, ss=46, py=905, ph=400)),
    L("It was called LuoBu, made with an affiliate of Tencent, and it launched in July 2021.",
      S("LUOBU", "LAUNCHED JULY 2021", "red", "stone", bc="#ffffff", bs=180, ic=[{"n": "globe", "x": 860, "y": 820, "s": 150, "a": "spin"}])),
    L("Less than six months later, on December 8th, it was shut down and pulled from app stores.",
      S("SHUT DOWN", "DECEMBER 8, 2021", "dark", "stone", bs=150, vig=True, ic=[{"n": "alarm", "x": 860, "y": 820, "s": 140, "a": "shake"}])),
    L("Players who logged in saw a thank-you message for trying the test version. Roblox later said it was only ever meant as a test.",
      S("JUST A\nTEST?", "A THANK-YOU MESSAGE", "mint", "stone", bs=140, av=[av([0.0, 0.8], "wave", "a")])),
    end("Did you know about it?", "DID YOU\nKNOW?", bg="night", ground="stone"),
   ], pron={"LuoBu": "Lwo-boo", "Tencent": "Ten-sent"})

# 101 Bacon Hair
ep(101, "bacon-hair-real-name", "Bacon Hair's Real Name", 30, "#ff8a65", SARAH, 1.04,
   {"font": MF + "Chewy-Regular.ttf", "size": 100, "upper": False, "hi": "#ffab91", "stroke": 9},
   [L("Bacon Hair isn't its real name.",
      opener("IT'S NOT\nBACON HAIR", "ROBLOX'S DEFAULT LOOK", "pop5-pig.jpg", "A REAL PIG. NO BACON HERE.", "Photo: simon berger, CC0",
             bg="day", ground="grass", bs=130, ss=46, py=905, ph=400)),
    L("The real item is called Pal Hair. Players call it Bacon Hair, because it looks like strips of bacon.",
      S("PAL HAIR", "ITS REAL NAME", "mint", "grass", bs=170, av=[av([0.0, 0.8], "wave", "a", hat="#6d4c41")])),
    L("It arrived with Roblox's 2014 avatar revamp. Before that, new players started as a blocky yellow figure.",
      S("2014", "THE AVATAR REVAMP", "sunset", "grass", bs=200, av=[av([-1.0, 0.8], "idle", "g"), av([1.0, 0.8], "idle", "a", hat="#6d4c41")])),
    L("Now calling someone a bacon means they're new, and haven't customized their avatar yet.",
      S("\"BACON\"", "= A NEW PLAYER", "party", "purple", rays="#ffffff", bs=170, crowd=crowd(10, 0.4))),
    L("And no, it was never removed. You can still equip Pal Hair today.",
      S("STILL\nHERE", "EQUIP IT ANYTIME", "gold", "grass", rays="#ffffff", bs=150, fx=["sparkle"], av=[av([0.0, 0.8], "jump", "a", hat="#6d4c41")])),
    end("Were you ever a bacon?", "EVER BEEN\nA BACON?", bg="day", ground="grass"),
   ])

# 102 Ink Game
ep(102, "ink-game", "Ink Game", 30, "#ec407a", SARAH, 1.06,
   {"font": MF + "Anton-Regular.ttf", "size": 104, "hi": "#f06292", "stroke": 8},
   [L("In Ink Game, you can play the deadly games, or start a rebellion.",
      opener("SURVIVE.\nOR REBEL.", "INK GAME", "pop7-doll.jpg", "A REAL OLD DOLLHOUSE", "Photo: public domain",
             bg="red", ground="road", bs=130, ss=46, py=905, ph=400)),
    L("It's inspired by Squid Game, with mini-games like Red Light Green Light and Dalgona.",
      S("RED LIGHT\nGREEN LIGHT", "AND DALGONA", "red", "road", bc="#ffffff", bs=120, fx=["red"], av=[av([-1.2, 0.8], "run", "a", to=[0.0, 0.6]), av([1.2, 0.8], "idle", "e", face="o")])),
    L("There are three endings: Rebel, Final Fight, and Sky Squid Games.",
      S("3 ENDINGS", "REBEL, FINAL FIGHT, SKY", "night", "road", bs=160, ic=[{"n": "crown", "x": 860, "y": 820, "s": 140, "a": "float"}])),
    L("In September 2025, an update let you play as the guards. That month, about 514,000 people played at once.",
      S(None, "PLAYING AT ONCE, SEPT 2025", "gold", "road", rays="#ffffff", count={"to": 514, "fmt": "{:.0f},000"}, bs=150, crowd=crowd(), fx=["confetti"])),
    L("Trackers count over 3 billion visits.",
      S("3 BILLION+", "VISITS (PER TRACKERS)", "party", "road", rays="#ffffff", bs=150)),
    end("Which ending did you get?", "WHICH\nENDING?", bg="red", ground="road"),
   ], pron={"Dalgona": "Dal-go-na"})

# ================================================================== write
for e in RB:
    e = dict(preset="roblox", hdr="tag", **e)
    for l in e["lines"]:
        ph = l["sc"].get("photo")
        if ph and not os.path.exists(os.path.join(ROOT, "episodes", "assets", ph["img"])):
            print("  MISSING IMAGE", e["slug"], ph["img"])
    json.dump(e, open(os.path.join(ROOT, "episodes", "roblox", e["slug"] + ".json"), "w"), indent=1, ensure_ascii=False)
    print(e["slug"], len(e["lines"]), "lines", sum(len(l.get("say", l["t"]).split()) for l in e["lines"]), "words", "target", e["target"])
