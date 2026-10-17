"""Writes batch 14 (facts checked 2026-10-17): DOORS Part 2 + 9 Roblox videos (8-Bit Backstory #113-122), hook-first openers, 30-80 s.
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


# 113 DOORS part 2
ep(113, "doors-part-2", "DOORS Has a Secret Level", 45, "#ffb300", SARAH, 1.06,
   {"font": MF + "CrimsonText-Bold.ttf", "size": 100, "upper": False, "fill": "#fff8e1", "hi": "#ffca28", "stroke": 6},
   [L("DOORS has a secret level, hidden inside the game.",
      opener("DOORS HAS A\nSECRET LEVEL", "DOORS PART 2", "pop4-hotel-hallway.jpg", "A REAL HOTEL HALLWAY", "Photo: cogdogblog, CC0",
             bg="dark", ground="dark", bs=110, ss=46, py=905, ph=400, vig=True)),
    L("It came with the Hotel Plus update, on January 29th, 2023. The secret level is a new version of Rooms, the game that inspired DOORS.",
      S("HOTEL+", "JANUARY 29, 2023", "night", "dark", bs=180, fx=["fireflies"], ic=[{"n": "eye", "x": 860, "y": 800, "s": 150, "a": "pulse"}])),
    L("You earn knobs as money, and a shopkeeper named Jeff opens his store at door 52.",
      S("JEFF'S\nSHOP", "DOOR 52", "gold", "wood", rays="#ffffff", bs=150, props=[["crate", -1.6, -1.2]], av=[av([0.6, 0.8], "wave", "b", hat="#4e342e")], fx=["coins"])),
    L("You can even save one item in the Rift, and take it into a future run.",
      S("THE RIFT", "SAVE ONE ITEM", "party", "purple", rays="#ffffff", bs=180, fx=["sparkle"])),
    L("When you die, the Guiding Light shows up with hints, and points out important items.",
      S("GUIDING\nLIGHT", "HINTS AFTER YOU DIE", "mint", "stone", bs=150, ic=[{"n": "star", "x": 540, "y": 780, "s": 180, "a": "float"}])),
    L("In 2024, The Backdoor added a prequel run with a strict time limit. Then on August 30th, Floor 2 opened: The Mines.",
      S("THE MINES", "FLOOR 2, AUG 30 2024", "dark", "stone", bs=170, vig=True, props=[["tower", -1.8, -2.0, {"c": "#5d4037"}], ["crate", 1.4, -1.2]], av=[av([0.0, 0.8], "sneak", "a", face="o")])),
    L("And on April Fools, it turned into Super Hard Mode, and later a retro, Doom-style mode.",
      S("APRIL\nFOOLS", "SUPER HARD MODE + RETRO MODE", "red", "dark", bc="#ffffff", bs=150, ss=40, fx=["red"], av=[av([0.0, 0.8], "jump", "e")])),
    end("Have you beaten The Mines?", "BEATEN\nTHE MINES?", bg="dark", ground="dark"),
   ], mood="spooky")

# 114 Roblox blocked countries
ep(114, "roblox-blocked-countries", "Countries That Blocked Roblox", 51, "#ef5350", MIKE, 1.08,
   {"font": MF + "RussoOne-Regular.ttf", "size": 84, "hi": "#ff8a80", "stroke": 8},
   [L("Roblox is blocked in some countries right now, and in others, it got blocked, then came back.",
      opener("BLOCKED IN\nWHOLE COUNTRIES", "WHERE ROBLOX GOT BANNED", "pop7-school.jpg", "A REAL OLD CLASSROOM", "Photo: State Library of Queensland, public domain",
             bg="red", ground="stone", bs=104, ss=44, py=905, ph=400)),
    L("Turkey blocked it on August 7th, 2024, and the ban was still in place as of June 2026.",
      S("TURKEY", "BLOCKED AUGUST 2024", "night", "stone", bs=180, ic=[{"n": "globe", "x": 860, "y": 820, "s": 150, "a": "spin"}])),
    L("In 2025, Qatar, Kuwait, Algeria, Iraq, and others blocked it too. The main reason was child safety.",
      S("QATAR, KUWAIT,\nIRAQ, ALGERIA", "2025: CHILD SAFETY", "dark", "stone", bs=110, vig=True, ic=[{"n": "shield", "x": 860, "y": 820, "s": 140, "a": "pulse"}])),
    L("Kuwait lifted its ban a few months later, after Roblox agreed to turn off in-game chat there.",
      S("BACK IN\nKUWAIT", "CHAT TURNED OFF", "mint", "stone", bs=140, av=[av([0.0, 0.8], "wave", "a")])),
    L("Russia blocked it in December 2025, then unblocked it on June 10th, 2026, after Roblox agreed to age-restricted access.",
      S("RUSSIA", "BLOCKED, THEN BACK", "sunset", "stone", bs=180, ic=[{"n": "calendar", "x": 860, "y": 820, "s": 140, "a": "float"}])),
    L("And in 2026, Egypt blocked it, and Indonesia blocked it for players under 16.",
      S("EGYPT +\nINDONESIA", "2026", "night", "stone", bs=140, crowd=crowd(10, 0.4))),
    end("Is Roblox safe enough?", "SAFE\nENOUGH?", bg="red", ground="stone"),
   ])

# 115 Italian brainrot origin
ep(115, "where-brainrot-came-from", "Where Brainrot Came From", 46, "#26c6da", SARAH, 1.06,
   {"font": MF + "Bangers-Regular.ttf", "size": 128, "mode": "word", "fill": "#b2ebf2", "hi": "#b2ebf2", "cy": 1470},
   [L("Brainrot started with a shark wearing sneakers.",
      opener("A SHARK IN\nSNEAKERS", "WHERE BRAINROT CAME FROM", "pop9-goatroof.jpg", "A REAL GOAT ON A ROOF. NOT AI.", "Photo: Tim Green, CC BY 2.0",
             bg="day", ground="grass", bs=116, ss=44, py=905, ph=400)),
    L("Italian brainrot is AI-made creatures with fake Italian names, and it blew up on TikTok in early 2025.",
      S("AI CREATURES", "FAKE ITALIAN NAMES", "party", "purple", rays="#ffffff", bs=140, fx=["sparkle"], ic=[{"n": "tv", "x": 860, "y": 820, "s": 140, "a": "float"}])),
    L("Tralalero Tralala, a three-legged shark in Nike sneakers, is seen as the first one. One clip from January 2025 reportedly hit 7 million views.",
      S("TRALALERO\nTRALALA", "THE FIRST ONE", "mint", "grass", bs=120, crowd=crowd(12, 0.4))),
    L("Then came Tung Tung Tung Sahur, a log with a bat, which actually comes from Indonesia, plus Bombardiro Crocodilo and Ballerina Cappuccina.",
      S("TUNG TUNG\nTUNG SAHUR", "FROM INDONESIA", "sunset", "grass", bs=120, av=[av([0.0, 0.8], "jump", "g", hold="sword")])),
    L("It took over Roblox through Steal a Brainrot. And in April 2026, Tung Tung Tung Sahur and Ballerina Cappuccina came to Fortnite as skins.",
      S("IN FORTNITE", "APRIL 2026 SKINS", "gold", "grass", rays="#ffffff", bs=160, fx=["confetti"])),
    end("Who's your favorite brainrot?", "FAVORITE\nBRAINROT?", bg="day", ground="grass"),
   ], pron={"Tralalero": "Tra-la-leh-ro", "Tralala": "Tra-la-la", "Sahur": "Sa-hoor", "Bombardiro": "Bom-bar-dee-ro", "Crocodilo": "Cro-co-dee-lo", "Cappuccina": "Ca-poo-chee-na", "brainrot": "brain rot", "Brainrot": "Brain rot"})

# 116 Toilet Tower Defense
ep(116, "toilet-tower-defense", "6 Billion Visits for Toilets", 31, "#90a4ae", SARAH, 1.0,
   {"font": MF + "TitanOne-Regular.ttf", "size": 80, "stroke": 0, "fill": "#263238", "hi": "#c62828", "box": "#eceff1", "radius": 30},
   [L("A Roblox game about fighting toilets got over 6 billion visits.",
      opener("6 BILLION\nVISITS. TOILETS.", "TOILET TOWER DEFENSE", "pop6-teacup.jpg", "REAL FANCY PORCELAIN", "Photo: The Met, CC0",
             bg="mint", ground="stone", bs=110, ss=46, py=905, ph=400)),
    L("In Toilet Tower Defense, you place cameramen and other units to stop waves of invading toilets.",
      S("CAMERAMEN\nVS TOILETS", "WAVE AFTER WAVE", "party", "stone", rays="#ffffff", bs=120, props=[["tower", -1.8, -1.8], ["tower", 1.8, -1.8]], av=[av([0.0, 1.0], "cheer", "a", hold="gun")])),
    L("It came out in June 2023, made by Telanthric, and it has an Endless Mode where you just try to survive.",
      S("ENDLESS\nMODE", "SURVIVE AS LONG AS YOU CAN", "night", "stone", bs=140, ic=[{"n": "clock", "x": 860, "y": 820, "s": 140, "a": "pulse"}])),
    L("In October 2024, about 167,000 people played at once.",
      S(None, "PLAYING AT ONCE", "gold", "stone", rays="#ffffff", count={"to": 167, "fmt": "{:.0f},000"}, bs=150, crowd=crowd(), fx=["confetti"])),
    L("Trackers count about 1.5 million favorites.",
      S("1.5 MILLION", "FAVORITES (PER TRACKERS)", "party", "stone", rays="#ffffff", bs=140, ic=[{"n": "heart", "x": 860, "y": 820, "s": 140, "a": "pulse"}])),
    end("Who's your best unit?", "BEST\nUNIT?", bg="mint", ground="stone"),
   ], pron={"Telanthric": "Tel-an-thric"})

# 117 The Classic / Tix return
ep(117, "roblox-brought-back-tix", "Roblox Brought Back Tix", 34, "#ffd23c", MIKE, 1.06,
   {"font": MF + "Chewy-Regular.ttf", "size": 96, "upper": False, "hi": "#ffe082", "stroke": 9},
   [L("Roblox deleted Tix in 2016. Then, for one event, it brought them back.",
      opener("TIX CAME\nBACK", "THE CLASSIC", "pop8-dice.jpg", "REAL GAME DICE", "Photo: Schlurcher, CC BY 4.0",
             bg="gold", ground="grass", bs=130, ss=46, py=905, ph=400)),
    L("The event was called The Classic, in 2024, with 15 games and a hub full of old-school items.",
      S("THE CLASSIC", "15 GAMES", "mint", "grass", bs=150, crowd=crowd(12, 0.4), ic=[{"n": "trophy", "x": 860, "y": 820, "s": 140, "a": "float"}])),
    L("You earned Tix and spent them in the hub. A Rocket Launcher was 6 Tix, a Timebomb was 20, and Mom's Dog was 32.",
      S("6 TIX", "FOR A ROCKET LAUNCHER", "party", "grass", rays="#ffffff", bs=190, ic=[{"n": "rocket", "x": 860, "y": 820, "s": 150, "a": "float"}], fx=["coins"])),
    L("Players around the world filled a giant Tix Tower together, to unlock a hidden reward.",
      S("TIX\nTOWER", "FILLED BY EVERYONE", "night", "grass", bs=150, props=[["tower", 0.0, -1.8, {"c": "#ffd23c"}]], fx=["sparkle"])),
    end("Should Tix come back for good?", "BRING TIX\nBACK?", bg="gold", ground="grass"),
   ], pron={"Tix": "Ticks"})

# 118 Crossroads
ep(118, "crossroads-first-multiplayer", "Roblox's First Multiplayer Game", 32, "#8d6e63", MIKE, 1.06,
   {"font": MF + "PermanentMarker-Regular.ttf", "size": 92, "upper": False, "hi": "#ffcc80", "stroke": 9},
   [L("This is Roblox's very first multiplayer game, and you can still play it.",
      opener("ROBLOX'S\nFIRST GAME", "CROSSROADS", "pop7-castle.jpg", "A REAL CASTLE", "Photo: Wilfredor, CC0",
             bg="day", ground="grass", bs=120, ss=46, py=905, ph=400)),
    L("It's called Crossroads. A Roblox developer remembered the team playing it with the first outside player, in December 2006.",
      S("CROSSROADS", "DECEMBER 2006", "sunset", "grass", bs=150, av=[av([-1.0, 0.8], "wave", "a"), av([1.0, 0.8], "wave", "b")])),
    L("The original map had a castle built by Erik Cassel, and a white house and playground built by Builderman.",
      S("A CASTLE\n+ A HOUSE", "BUILT BY THE FOUNDERS", "mint", "grass", bs=130, props=[["tower", -1.8, -2.2], ["house", 1.8, -2.4, {"c": "#eeeeee"}]])),
    L("You fought with a slingshot and a rocket launcher, and the whole map could be blown apart.",
      S("BOOM!", "THE MAP BREAKS", "red", "stone", bc="#ffffff", bs=200, fx=["red", "speed"], props=[["block", -1.2, -1.2], ["block", 1.2, -1.6]], av=[av([0.0, 0.8], "cheer", "e", hold="gun")])),
    end("Have you played Crossroads?", "EVER\nPLAYED IT?", bg="day", ground="grass"),
   ])

# 119 Dominus Empyreus
ep(119, "dominus-69-million-robux", "A Hat Sold for 69 Million Robux", 35, "#7e57c2", SARAH, 1.04,
   {"font": MF + "Anton-Regular.ttf", "size": 104, "hi": "#b39ddb", "stroke": 8},
   [L("One Roblox hat sold for 69 million Robux.",
      opener("69 MILLION\nROBUX", "FOR ONE HAT", "pop7-trophy.jpg", "A REAL TROPHY CUP", "Photo: public domain",
             bg="night", ground="purple", bs=120, ss=46, py=905, ph=400)),
    L("It's the Dominus Empyreus, the very first Dominus. It came out on January 24th, 2010, for 13,337 Robux, and only 26 were made.",
      S("ONLY 26", "MADE IN 2010", "party", "purple", rays="#ffffff", bs=190, ic=[{"n": "crown", "x": 860, "y": 820, "s": 150, "a": "float"}])),
    L("On June 24th, 2022, one sold for 69 million Robux, a record for a legal Roblox sale.",
      S(None, "ROBUX, JUNE 2022", "gold", "purple", rays="#ffffff", count={"to": 69, "fmt": "{:.0f} MILLION"}, bs=150, fx=["coins", "confetti"])),
    L("Back in 2012, an April Fools glitch even showed its average price at over a billion Robux.",
      S("1 BILLION?", "AN APRIL FOOLS GLITCH", "red", "purple", bc="#ffffff", bs=160, ic=[{"n": "question", "x": 860, "y": 820, "s": 140, "a": "shake"}])),
    end("Would you buy a Dominus?", "WOULD YOU\nBUY ONE?", bg="night", ground="purple"),
   ], pron={"Dominus": "Dom-in-us", "Empyreus": "Em-peer-ee-us"})

# 120 Age checks
ep(120, "roblox-face-scan-to-chat", "Roblox Scans Your Face to Chat", 31, "#42a5f5", SARAH, 1.04,
   {"font": MF + "Audiowide-Regular.ttf", "size": 76, "hi": "#90caf9", "stroke": 7},
   [L("To chat on Roblox now, you have to let it guess your age from your face.",
      opener("A FACE SCAN\nTO CHAT", "ROBLOX AGE CHECKS", "pop6-computer-lab.jpg", "A REAL COMPUTER LAB", "Photo: Todd Huffman, CC BY 2.0",
             bg="night", ground="stone", bs=116, ss=46, py=905, ph=400)),
    L("It started rolling out worldwide in January 2026. Players 13 and up can use an ID instead.",
      S("JANUARY\n2026", "OR USE AN ID (13+)", "mint", "stone", bs=140, ic=[{"n": "eye", "x": 860, "y": 820, "s": 140, "a": "pulse"}])),
    L("Then you're put in an age group, from under 9 up to 21 plus, and you mostly chat with people your own age.",
      S("6 AGE\nGROUPS", "UNDER 9 TO 21+", "party", "stone", rays="#ffffff", bs=150, crowd=crowd(12, 0.4))),
    L("Roblox says the images are deleted right after the check. Kids under 9 have chat off, unless a parent says yes.",
      S("DELETED", "RIGHT AFTER THE CHECK", "dark", "stone", bs=170, ic=[{"n": "shield", "x": 860, "y": 820, "s": 140, "a": "float"}])),
    end("Good idea or too much?", "GOOD IDEA\nOR TOO MUCH?", bg="night", ground="stone"),
   ])

# 121 Grace
ep(121, "grace-roblox", "Grace", 31, "#ab47bc", SARAH, 1.04,
   {"font": MF + "BlackOpsOne-Regular.ttf", "size": 88, "hi": "#ce93d8", "stroke": 8},
   [L("In Grace, eight monsters hunt you, and the clock never stops.",
      opener("8 MONSTERS.\nONE TIMER.", "GRACE", "pop6-cave.jpg", "A REAL DARK CAVE", "Photo: Jtknowles, public domain",
             bg="dark", ground="dark", bs=116, ss=46, py=905, ph=400, vig=True)),
    L("It's a Roblox horror game inspired by DOORS and Rooms, but much faster. You slide, kick doors, and pull levers.",
      S("SLIDE. KICK.\nPULL.", "INSPIRED BY DOORS", "red", "dark", bc="#ffffff", bs=124, fx=["red", "speed"], av=[av([-1.2, 0.8], "run", "a", to=[0.8, 0.6])])),
    L("The monsters include Carnation, Dozer, Elkman, Goatman, and Sorrow, and each one catches you a different way.",
      S("8 MONSTERS", "EACH HUNTS DIFFERENTLY", "night", "dark", bs=160, vig=True, fx=["fireflies"], ic=[{"n": "eye", "x": 860, "y": 800, "s": 150, "a": "pulse"}])),
    L("It's free to play, with no Robux purchases needed.",
      S("FREE", "NO ROBUX NEEDED", "mint", "dark", bs=200, ic=[{"n": "coin", "x": 860, "y": 820, "s": 140, "a": "spin"}])),
    L("There's no difficulty setting. If the timer runs out, you start again.",
      S("TIME'S UP", "TRY AGAIN", "dark", "dark", bs=180, ic=[{"n": "alarm", "x": 860, "y": 820, "s": 150, "a": "shake"}])),
    end("Which monster got you first?", "WHO GOT\nYOU FIRST?", bg="dark", ground="dark"),
   ], mood="spooky")

# 122 Rooms
ep(122, "the-game-that-inspired-doors", "The Game That Inspired DOORS", 32, "#78909c", MIKE, 1.06,
   {"font": MF + "Anton-Regular.ttf", "size": 104, "hi": "#cfd8dc", "stroke": 8},
   [L("Before DOORS, there was Rooms. And without it, DOORS wouldn't exist.",
      opener("BEFORE DOORS,\nTHERE WAS ROOMS", "THE GAME THAT STARTED IT", "pop6-house.jpg", "A REAL OLD HOUSE", "Photo: Tudor Washington Collins, Auckland Museum, CC BY 4.0",
             bg="night", ground="stone", bs=104, ss=44, py=905, ph=400, vig=True)),
    L("Rooms was made by a creator called nicorocks5555, and it has monsters like A-60 and A-200.",
      S("A-60", "AND A-200", "red", "stone", bc="#ffffff", bs=200, fx=["red"], vig=True)),
    L("DOORS was heavily inspired by it, and DOORS getting huge made Rooms huge too. It also inspired Pressure.",
      S("DOORS +\nPRESSURE", "BOTH INSPIRED BY ROOMS", "night", "stone", bs=130, props=[["house", -1.8, -2.2], ["tower", 1.8, -2.0]])),
    L("DOORS even put a new version of Rooms inside its own game, as a secret level.",
      S("A SECRET\nLEVEL", "ROOMS, INSIDE DOORS", "party", "purple", rays="#ffffff", bs=140, fx=["sparkle"])),
    end("Rooms or DOORS?", "ROOMS OR\nDOORS?", bg="night", ground="stone"),
   ], pron={"nicorocks5555": "nico rocks five five five five", "A-60": "A sixty", "A-200": "A two hundred"}, mood="spooky")

# ================================================================== write
for e in RB:
    e = dict(preset="roblox", hdr="tag", **e)
    for l in e["lines"]:
        ph = l["sc"].get("photo")
        if ph and not os.path.exists(os.path.join(ROOT, "episodes", "assets", ph["img"])):
            print("  MISSING IMAGE", e["slug"], ph["img"])
    json.dump(e, open(os.path.join(ROOT, "episodes", "roblox", e["slug"] + ".json"), "w"), indent=1, ensure_ascii=False)
    print(e["slug"], len(e["lines"]), "lines", sum(len(l.get("say", l["t"]).split()) for l in e["lines"]), "words", "target", e["target"])
