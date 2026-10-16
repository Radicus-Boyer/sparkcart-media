"""Writes batch 13 (facts checked 2026-10-16): 10 Roblox videos (8-Bit Backstory #103-112), hook-first openers, 30-70 s.
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


# 103 The admin war
ep(103, "roblox-admin-war", "The Roblox Admin War", 33, "#ff7043", SARAH, 1.06,
   {"font": MF + "Bangers-Regular.ttf", "size": 128, "mode": "word", "fill": "#ffccbc", "hi": "#ffccbc", "cy": 1470},
   [L("Two Roblox games went to war, and it broke Roblox's all-time record.",
      opener("TWO GAMES\nWENT TO WAR", "STEAL A BRAINROT VS GROW A GARDEN", "pop7-joker.jpg", "TWO REAL JOKER CARDS", "Photo: Czlowiek Oddzielany Mechanicznie, CC0",
             bg="red", ground="stone", bs=116, ss=40, py=905, ph=400)),
    L("On August 23rd, 2025, Steal a Brainrot and Grow a Garden held a mock admin war.",
      S("ADMIN\nWAR", "AUGUST 23, 2025", "dark", "stone", bc="#ff7043", bs=160, fx=["red", "speed"], av=[av([-1.3, 0.8], "cheer", "a", hold="sword"), av([1.3, 0.8], "cheer", "e", hold="sword")])),
    L("Grow a Garden hit at least 22.3 million players at once.",
      S(None, "GROW A GARDEN", "mint", "grass", count={"to": 22.3, "fmt": "{:.1f} MILLION"}, bs=140, crowd=crowd(18, 0.4), props=[["tree", -2.4, -2.4]])),
    L("And all of Roblox hit 47.4 million at the same time, a new platform record.",
      S(None, "ON ROBLOX AT ONCE", "gold", "stone", rays="#ffffff", count={"to": 47.4, "fmt": "{:.1f} MILLION"}, bs=140, crowd=crowd(), fx=["confetti"])),
    L("Later, Steal a Brainrot became the only Roblox game ever to pass 25 million players at once.",
      S("25 MILLION+", "STEAL A BRAINROT, OCT 2025", "party", "purple", rays="#ffffff", bs=140, ic=[{"n": "crown", "x": 860, "y": 820, "s": 150, "a": "float"}], fx=["sparkle"])),
    end("Team Brainrot or team Garden?", "BRAINROT OR\nGARDEN?", bg="red", ground="stone"),
   ])

# 104 Bruno Mars Guinness record
ep(104, "bruno-mars-roblox-record", "Bruno Mars Broke a Record in Roblox", 38, "#ffd54f", SARAH, 1.04,
   {"font": MF + "TitanOne-Regular.ttf", "size": 80, "stroke": 0, "fill": "#212121", "hi": "#c62828", "box": "#ffd54f", "radius": 30},
   [L("A Roblox concert set a Guinness World Record, and it beat Fortnite's Travis Scott show.",
      opener("A GUINNESS\nRECORD", "IN A ROBLOX GAME", "pop3-bruno-mars.jpg", "THE REAL BRUNO MARS", "Photo: Brothers Le, CC BY 2.0",
             bg="party", ground="purple", bs=120, ss=46, py=905, ph=400)),
    L("On January 17th, 2026, Bruno Mars played a concert inside Steal a Brainrot.",
      S("BRUNO MARS", "INSIDE STEAL A BRAINROT", "night", "purple", bs=140, props=[["tower", 0.0, -2.6, {"c": "#ffd54f"}]], crowd=crowd(14, 0.4), fx=["sparkle"])),
    L("Guinness counted 12,862,161 people watching at once, the largest concert in a video game by a single artist.",
      S(None, "WATCHING AT ONCE", "gold", "purple", rays="#ffffff", count={"to": 12862161, "fmt": "{:,.0f}"}, bs=110, crowd=crowd(), fx=["confetti"])),
    L("Travis Scott's Fortnite show had held the record, with 12.3 million.",
      S("12.3 MILLION", "THE OLD RECORD", "dark", "stone", bs=130, ic=[{"n": "trophy", "x": 860, "y": 820, "s": 140, "a": "shake"}])),
    L("And his limited Brainrot, Brunito Marsito, was collected over 5 million times.",
      S("BRUNITO\nMARSITO", "5.4 MILLION COLLECTED", "mint", "purple", bs=130, ic=[{"n": "star", "x": 860, "y": 820, "s": 140, "a": "spin"}])),
    end("Who should play Roblox next?", "WHO PLAYS\nNEXT?", bg="party", ground="purple"),
   ], pron={"Marsito": "Mar-see-toe", "Brunito": "Broo-nee-toe"})

# 105 Headless Horseman
ep(105, "headless-31000-robux", "31,000 Robux for No Head", 30, "#ff9100", MIKE, 1.02,
   {"font": MF + "PermanentMarker-Regular.ttf", "size": 92, "upper": False, "hi": "#ffab40", "stroke": 9},
   [L("On Roblox, having no head costs 31,000 Robux.",
      opener("31,000 ROBUX\nFOR NO HEAD", "THE HEADLESS HORSEMAN", "pop-hunyad-castle.jpg", "A REAL OLD CASTLE", "Photo: Luke.ender, public domain",
             bg="night", ground="dark", bs=104, ss=46, py=905, ph=400)),
    L("It's the Headless Horseman bundle, and its main draw is an invisible head.",
      S("NO HEAD", "THAT'S THE WHOLE POINT", "dark", "dark", bs=170, vig=True, fx=["fireflies"], av=[av([0.0, 0.8], "idle", "a", face="o")])),
    L("The price has stayed at 31,000 Robux across Halloween after Halloween.",
      S("31,000", "ROBUX, EVERY YEAR", "gold", "dark", rays="#ffffff", bs=190, fx=["coins"])),
    L("That's why a headless avatar is one of the biggest flexes on Roblox.",
      S("THE BIGGEST\nFLEX", "ON ALL OF ROBLOX", "party", "purple", rays="#ffffff", bs=124, crowd=crowd(10, 0.4), fx=["sparkle"])),
    L("But you can only buy it around Halloween. Once the event ends, it leaves the shop.",
      S("HALLOWEEN\nONLY", "THEN IT'S GONE", "red", "dark", bc="#ffffff", bs=130, ic=[{"n": "moon", "x": 860, "y": 800, "s": 150, "a": "float"}], fx=["red"])),
    end("Would you pay for no head?", "WORTH\nIT?", bg="night", ground="dark"),
   ], mood="spooky")

# 106 CEO account #1
ep(106, "roblox-ceo-account-number-1", "The Roblox CEO Gave Away Account 1", 35, "#64b5f6", MIKE, 1.08,
   {"font": MF + "RussoOne-Regular.ttf", "size": 84, "hi": "#64b5f6", "stroke": 8},
   [L("Roblox's CEO used to own account number 1. Then he gave it away.",
      opener("HE GAVE AWAY\nACCOUNT #1", "ROBLOX'S CEO", "pop3-baszucki.jpg", "THE REAL DAVID BASZUCKI", "Photo: TechCrunch, CC BY 2.0",
             bg="day", ground="stone", bs=110, ss=46, py=905, ph=400)),
    L("David Baszucki co-founded Roblox with Erik Cassel. His account was created in July 2004.",
      S("JULY 2004", "ACCOUNT CREATED", "mint", "stone", bs=170, av=[av([0.0, 0.8], "wave", "b")], ic=[{"n": "calendar", "x": 860, "y": 820, "s": 140, "a": "float"}])),
    L("It started as user ID 1. But in 2007, it was swapped with the newest account on the site.",
      S("ID 1\nSWAPPED", "WITH A BRAND-NEW ACCOUNT", "party", "stone", rays="#ffffff", bs=140, ic=[{"n": "trade", "x": 860, "y": 820, "s": 150, "a": "spin"}])),
    L("He used to play as builderman, before switching to his real name.",
      S("BUILDERMAN", "HIS OLD ACCOUNT", "sunset", "stone", bs=140, av=[av([0.0, 0.8], "idle", "a", hat="#ff7043")])),
    L("And his profile still shows the wrong join date, because of a display bug.",
      S("WRONG\nJOIN DATE", "A DISPLAY BUG", "night", "stone", bs=140, ic=[{"n": "question", "x": 860, "y": 820, "s": 140, "a": "shake"}])),
    end("Would you have wanted account 1?", "WANT\nACCOUNT #1?", bg="day", ground="stone"),
   ], pron={"Baszucki": "Bah-zoo-key", "builderman": "builder man"})

# 107 DevEx
ep(107, "roblox-paid-15-billion", "Roblox Paid Game Makers $1.5 Billion", 33, "#66bb6a", SARAH, 1.04,
   {"font": MF + "Anton-Regular.ttf", "size": 104, "hi": "#a5d6a7", "stroke": 8},
   [L("In one year, Roblox paid its game creators over 1.5 billion dollars.",
      opener("$1.5 BILLION\nTO CREATORS", "IN ONE YEAR", "pop2-seamstress.jpg", "A REAL CREATOR AT WORK", "Photo: Kris Atomic, CC0",
             bg="gold", ground="grass", bs=110, ss=46, py=905, ph=400)),
    L("It happens through DevEx, where creators trade the Robux they earn for real money.",
      S("DEVEX", "ROBUX TO REAL MONEY", "mint", "grass", bs=180, fx=["coins"], ic=[{"n": "money", "x": 860, "y": 820, "s": 150, "a": "float"}])),
    L("That 1.5 billion was for 2025 alone.",
      S(None, "PAID OUT IN 2025", "gold", "grass", rays="#ffffff", count={"to": 1.5, "fmt": "${:.1f} BILLION"}, bs=140, crowd=crowd(), fx=["confetti"])),
    L("In just the first three months of 2026, payouts hit 423 million dollars, up 50 percent.",
      S("$423M", "JAN TO MARCH 2026", "mint", "grass", bs=190, ic=[{"n": "money", "x": 860, "y": 820, "s": 150, "a": "pulse"}])),
    L("And from June 2026, the rate went up 42 percent, for some spending by verified adult players in the US.",
      S("+42%", "FOR SOME ADULT SPENDING", "party", "purple", rays="#ffffff", bs=200, av=[av([0.0, 0.8], "jump", "c")])),
    end("Would you make a Roblox game?", "WOULD YOU\nMAKE ONE?", bg="gold", ground="grass"),
   ], pron={"DevEx": "Dev Ex"})

# 108 Steal a Brainrot: Fortnite + movie
ep(108, "steal-a-brainrot-movie", "Steal a Brainrot Is Getting a Movie", 38, "#7e57c2", SARAH, 1.06,
   {"font": MF + "Chewy-Regular.ttf", "size": 96, "upper": False, "stroke": 0, "fill": "#ffffff", "hi": "#ffe082", "box": "#5e35b1", "radius": 36},
   [L("Steal a Brainrot is getting a movie. And Fortnite made its own version, with permission.",
      opener("IT'S GETTING\nA MOVIE", "STEAL A BRAINROT", "pop2-flip-the-frog.jpg", "A REAL 1930 CARTOON TITLE", "Photo: public domain",
             bg="party", ground="purple", bs=116, ss=46, py=905, ph=400)),
    L("It was made by SpyderSammy, and came out on May 16th, 2025.",
      S("SPYDERSAMMY", "MAY 16, 2025", "mint", "purple", bs=130, av=[av([0.0, 0.8], "wave", "a")], ic=[{"n": "calendar", "x": 860, "y": 820, "s": 140, "a": "float"}])),
    L("You buy brainrots off a conveyor belt, earn cash from them, and steal them from other players.",
      S("BUY. EARN.\nSTEAL.", "THE WHOLE LOOP", "sunset", "stone", bs=120, props=[["base", 0.0, -1.0]], av=[av([-1.4, 0.8], "sneak", "e", to=[-0.2, 0.4])])),
    L("In July 2025, Epic Games licensed it for Fortnite Creative, as Steal the Brainrot.",
      S("IN FORTNITE", "LICENSED, JULY 2025", "night", "purple", bs=140, ic=[{"n": "trade", "x": 860, "y": 820, "s": 150, "a": "spin"}])),
    L("Tung Tung Tung Sahur was pulled from the game in September 2025, after a licensing dispute. He came back on November 29th.",
      S("TUNG TUNG\nTUNG SAHUR", "REMOVED, THEN BACK", "red", "stone", bc="#ffffff", bs=120, av=[av([0.0, 0.8], "jump", "g")])),
    L("And a movie is now in development.",
      S("A MOVIE", "IN DEVELOPMENT", "gold", "purple", rays="#ffffff", bs=180, ic=[{"n": "clapper", "x": 860, "y": 820, "s": 150, "a": "pulse"}], fx=["confetti"])),
    end("Who should star in the movie?", "WHO STARS\nIN IT?", bg="party", ground="purple"),
   ], pron={"SpyderSammy": "Spider Sammy", "Sahur": "Sa-hoor", "brainrots": "brain rots", "Brainrot": "Brain rot", "brainrot": "brain rot"})

# 109 Plants & Brainrots
ep(109, "plants-and-brainrots", "4 Billion Visits in 9 Months", 31, "#9ccc65", SARAH, 1.0,
   {"font": MF + "BlackOpsOne-Regular.ttf", "size": 88, "hi": "#c5e1a5", "stroke": 8},
   [L("This Roblox game hit over 4 billion visits in under nine months.",
      opener("4 BILLION\nIN 9 MONTHS", "PLANTS & BRAINROTS", "pop8-field.jpg", "A REAL SUNFLOWER FIELD", "Photo: Summer Stock, CC0",
             bg="day", ground="grass", bs=116, ss=46, py=905, ph=400)),
    L("In Plants and Brainrots, you plant seeds, and your plants fight brainrots for you while you earn cash.",
      S("PLANTS VS\nBRAINROTS", "THEY FIGHT FOR YOU", "mint", "grass", bs=120, props=[["tree", -2.0, -2.0], ["tree", 2.0, -2.0]], av=[av([0.0, 0.8], "cheer", "c")], fx=["coins"])),
    L("You can play it on phones, tablets, PC and console.",
      S("PLAY\nANYWHERE", "PHONE, TABLET, PC, CONSOLE", "night", "grass", bs=130, ic=[{"n": "controller", "x": 860, "y": 820, "s": 140, "a": "float"}])),
    L("It's made by Splitting Point, the same studio that runs Grow a Garden.",
      S("SPLITTING\nPOINT", "ALSO RUNS GROW A GARDEN", "sunset", "grass", bs=130, ic=[{"n": "trophy", "x": 860, "y": 820, "s": 140, "a": "float"}])),
    L("It came out in August 2025, and by October, about 8.7 million people played at once.",
      S(None, "PLAYING AT ONCE", "gold", "grass", rays="#ffffff", count={"to": 8.7, "fmt": "{:.1f} MILLION"}, bs=140, crowd=crowd(), fx=["confetti"])),
    end("What's your best plant?", "BEST\nPLANT?", bg="day", ground="grass"),
   ], pron={"brainrots": "brain rots", "Brainrots": "Brain rots"})

# 110 Guests and Guest 666 (longer story)
ep(110, "guest-666", "The Evil Guest 666", 58, "#e53935", MIKE, 1.06,
   {"font": MF + "CrimsonText-Bold.ttf", "size": 100, "upper": False, "fill": "#f5f5f5", "hi": "#ef9a9a", "stroke": 6},
   [L("For years, Roblox kids whispered about Guest 666, a guest with admin powers in every game.",
      opener("THE EVIL\nGUEST", "GUEST 666", "pop5-alcatraz.jpg", "A REAL EMPTY CELL BLOCK", "Photo: Nonie, CC BY 2.0",
             bg="dark", ground="dark", bs=130, ss=46, py=905, ph=400, vig=True)),
    L("Guests were a trial mode, added in September 2008. You could play without an account.",
      S("GUESTS", "ADDED SEPTEMBER 2008", "night", "dark", bs=170, av=[av([-1.0, 0.8], "idle", "a"), av([1.0, 0.8], "idle", "a")])),
    L("But guests couldn't chat with friends, buy items, or save progress. And from 2016, they couldn't talk to anyone.",
      S("NO CHAT", "NO ITEMS, NO SAVES", "dark", "dark", bs=170, vig=True, ic=[{"n": "question", "x": 860, "y": 820, "s": 140, "a": "shake"}])),
    L("The rumor said Guest 666 showed up as An Evil Guest, and could control any game.",
      S("\"AN EVIL\nGUEST\"", "THE RUMOR", "red", "dark", bc="#ffffff", bs=130, fx=["red"], vig=True, av=[av([0.0, 0.8], "idle", "g", face="o")])),
    L("The truth? Guest numbers went from 0 to 9999, and players could edit their browser cookies to become 666.",
      S("A HOAX", "EDITED BROWSER COOKIES", "mint", "stone", bs=170, ic=[{"n": "code", "x": 860, "y": 820, "s": 140, "a": "float"}])),
    L("Guests were also used to troll players and dodge bans. So in October 2017, Roblox removed them.",
      S("REMOVED", "OCTOBER 2017", "night", "dark", bs=180, ic=[{"n": "alarm", "x": 860, "y": 820, "s": 140, "a": "shake"}])),
    L("The last ways to play as a guest were gone by November 2018.",
      S("GONE FOR\nGOOD", "NOVEMBER 2018", "dark", "dark", bs=140, vig=True, fx=["fireflies"])),
    end("Did you ever play as a guest?", "EVER BEEN\nA GUEST?", bg="dark", ground="dark"),
   ], mood="spooky")

# 111 Is brainrot dying?
ep(111, "is-brainrot-dying", "Is Brainrot Dying on Roblox", 37, "#26a69a", SARAH, 1.04,
   {"font": MF + "Audiowide-Regular.ttf", "size": 76, "hi": "#80cbc4", "stroke": 7},
   [L("Steal a Brainrot lost about 99 percent of its peak players. So is brainrot dead?",
      opener("IT LOST 99%\nOF ITS PLAYERS", "IS BRAINROT DYING?", "pop9-landfill.jpg", "A REAL LANDFILL DIG", "Photo: taylorhatmaker, CC BY 2.0",
             bg="night", ground="stone", bs=104, ss=46, py=905, ph=400)),
    L("At its peak in October 2025, Steal a Brainrot had over 25 million players at once.",
      S(None, "AT ITS PEAK", "gold", "stone", rays="#ffffff", count={"to": 25, "fmt": "{:.0f} MILLION+"}, bs=150, crowd=crowd(), fx=["confetti"])),
    L("Early this year, trackers had it at around 215,000.",
      S("~215,000", "EARLY 2026 (PER TRACKERS)", "dark", "stone", bs=150, crowd=crowd(4, 0.4))),
    L("But new brainrot games keep coming. Escape Tsunami for Brainrots briefly became Roblox's most-played game in January 2026.",
      S("NEW\nBRAINROTS", "STILL TOPPING THE CHARTS", "mint", "stone", bs=130, av=[av([-1.0, 0.8], "run", "a", to=[0.6, 0.6])], fx=["speed"])),
    L("Trackers say brainrot isn't dying. It's just turning into a normal Roblox genre.",
      S("NOT DEAD", "JUST NORMAL NOW", "party", "purple", rays="#ffffff", bs=170)),
    end("Is brainrot dead to you?", "DEAD OR\nALIVE?", bg="night", ground="stone"),
   ], pron={"brainrots": "brain rots", "Brainrots": "Brain rots", "Brainrot": "Brain rot", "brainrot": "brain rot"})

# 112 Escape Tsunami for Brainrots
ep(112, "escape-tsunami-for-brainrots", "5 Billion Visits in 4 Months", 31, "#29b6f6", SARAH, 1.04,
   {"font": MF + "RussoOne-Regular.ttf", "size": 84, "hi": "#4fc3f7", "stroke": 8, "cy": 1440},
   [L("This Roblox game passed 5 billion visits in about four months.",
      opener("5 BILLION\nIN 4 MONTHS", "ESCAPE TSUNAMI FOR BRAINROTS", "pop5-tornado.jpg", "A REAL STORM ROLLING IN", "Photo: NOAA, public domain",
             bg="day", ground="road", bs=116, ss=40, py=905, ph=400)),
    L("In Escape Tsunami for Brainrots, you outrun a giant wave while collecting brainrots for cash.",
      S("RUN!", "THE WAVE IS COMING", "red", "road", bc="#ffffff", bs=200, fx=["speed"], av=[av([-1.2, 0.8], "run", "a", to=[1.0, 0.6])])),
    L("You open Lucky Blocks, unlock new brainrots, and chase the legendary Infinity Brainrots.",
      S("LUCKY\nBLOCKS", "AND INFINITY BRAINROTS", "party", "road", rays="#ffffff", bs=140, props=[["block", 0.0, -1.0, {"c": "#ffd54f"}]], fx=["sparkle"])),
    L("It launched in December 2025, and in February 2026, over 4 million people played at once.",
      S(None, "PLAYING AT ONCE, FEB 2026", "gold", "road", rays="#ffffff", count={"to": 4, "fmt": "{:.0f} MILLION+"}, bs=150, crowd=crowd(), fx=["confetti"])),
    L("Trackers now count over 5 billion visits.",
      S("5 BILLION+", "VISITS (PER TRACKERS)", "party", "road", rays="#ffffff", bs=150)),
    end("How far did you make it?", "HOW FAR\nDID YOU GET?", bg="day", ground="road"),
   ], pron={"brainrots": "brain rots", "Brainrots": "Brain rots"})

# ================================================================== write
for e in RB:
    e = dict(preset="roblox", hdr="tag", **e)
    for l in e["lines"]:
        ph = l["sc"].get("photo")
        if ph and not os.path.exists(os.path.join(ROOT, "episodes", "assets", ph["img"])):
            print("  MISSING IMAGE", e["slug"], ph["img"])
    json.dump(e, open(os.path.join(ROOT, "episodes", "roblox", e["slug"] + ".json"), "w"), indent=1, ensure_ascii=False)
    print(e["slug"], len(e["lines"]), "lines", sum(len(l.get("say", l["t"]).split()) for l in e["lines"]), "words", "target", e["target"])
