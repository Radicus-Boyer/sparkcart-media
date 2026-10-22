"""Writes batch 17 (facts checked 2026-10-22): 4 Roblox + 3 Geometry Dash + 1 meme lore + 1 anime (8-Bit Backstory #143-151)."""

import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CTA = " Like and subscribe, and comment for which game we should review next!"
CTA_SUB = "COMMENT FOR WHICH GAME\nWE SHOULD REVIEW NEXT!"
MF = "../modern/fonts/"
MIKE, SARAH = "am_michael", "af_sarah"
RB = []


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


def F(big, sub, img=None, credit=None, clip=None, start=0, **k):
    """Full-screen real image / clip scene with the title over it."""
    fu = {"credit": credit}
    if clip:
        fu.update(clip=clip, start=start)
    else:
        fu["img"] = img
    for key in ("w", "cy", "mode", "crop", "h"):
        if key in k:
            fu[key] = k.pop(key)
    k.setdefault("by", 300)
    k.setdefault("bs", 120)
    k.setdefault("ss", 50)
    return S(big, sub, "night", "dark", full=fu, **k)


def RBX(game):
    return f"Image: {game} on Roblox"


def tease(text, big, img, credit, **k):
    return L(text + " Subscribe so you don't miss it.", F(big, "SUBSCRIBE SO YOU DON'T MISS IT", img, credit, bs=104, ss=40, **k))


def end(q, big, bg="party", ground="purple", **k):
    av_ = [{"p": [-1.8, 0.6], "a": "cheer", "c": "a"}, {"p": [0, 1.2], "a": "wave", "c": "g"}, {"p": [1.8, 0.6], "a": "cheer", "c": "b"}]
    ic = [{"n": "heart", "x": 170, "y": 700, "s": 130, "a": "pulse"}, {"n": "bolt", "x": 910, "y": 700, "s": 130, "a": "pulse"}]
    return L(q + CTA, S(big, CTA_SUB, bg, ground, rays="#ffffff", ss=50, sgap=62, fx=["confetti"], av=av_, ic=ic, **k))


def av(p, a="bob", c="a", **k):
    d = {"p": p, "a": a, "c": c}
    d.update(k)
    return d


def ep(num, slug, name, target, accent, voice, speed, cap, lines, pron=None, **k):
    RB.append(dict(num=num, slug=f"{num}-{slug}", file=f"{num} {name}.mp4", target=target, accent=accent,
                   voice=voice, speed=speed, cap=cap, pron=pron or {}, lines=lines, **k))


HEART, FENRIR, LIAM, PUCK = "af_heart", "am_fenrir", "am_liam", "am_puck"
BR_PRON = {"brainrot": "brain rot", "Brainrot": "Brain rot", "brainrots": "brain rots", "Brainrots": "Brain rots"}
GD_PRON = {"Acheron": "Ack-er-on", "Demonlist": "Demon list", "Zoink": "Zoynk", "ryamu": "rye-ah-moo", "Wolvez": "Wolves",
           "paqoe": "pa-co", "clubstep": "club step", "CairoX": "Cairo X", "DrCuber": "Doctor Cuber", "wPopoff": "W Popoff"}
ASSET = os.path.join(ROOT, "episodes", "assets")


def CLIP(name, big, sub, start, credit, fb_img=None, fb_credit=None, **k):
    """Real clip scene; until the clip exists, fall back to a still so the batch still renders."""
    if os.path.exists(os.path.join(ASSET, name)):
        return F(big, sub, clip=name, start=start, credit=credit, **k)
    if fb_img:
        return F(big, sub, fb_img, fb_credit or credit, **k)
    return S(big, sub, "night", "stone", vig=True, fx=["sparkle"], ic=[{"n": "star", "x": 860, "y": 820, "s": 150, "a": "spin"}],
             **{kk: v for kk, v in k.items() if kk in ("bs", "ss")})


GDE = dict(edition="GEOMETRY DASH", mood="spooky")
ML = dict(edition="MEME LORE")


# ============================================================ ROBLOX (posted first)
SK, SKC = "rb17-seek.mp4", "Clip: DOORS Seek chase (Roblox gameplay)"
ep(143, "who-is-seek-doors", "Who Is Seek in DOORS", 54, "#ff1744", MIKE, 1.06,
   {"font": MF + "CrimsonText-Bold.ttf", "size": 100, "upper": False, "fill": "#fff8e1", "hi": "#ff5252", "stroke": 6},
   [L("This is Seek, the monster in DOORS that never stops chasing you.",
      CLIP("rb17-seek-b.mp4", "WHO IS\nSEEK?", "DOORS", 0, SKC, "pop15-doors-seek.jpg", RBX("DOORS"), bs=140)),
    L("Seek hides as eyes on the walls. When the eyes start to multiply, a chase is coming.",
      CLIP("rb17-seek-a.mp4", "EYES ON\nTHE WALLS", "A CHASE IS COMING", 0, SKC, "pop15-doors-alarm.jpg", RBX("DOORS"), bs=130)),
    L("Then it bursts out of the floor as a tall black figure, and you have to run through room after room.",
      CLIP("rb17-seek-a.mp4", "RUN!", "ROOM AFTER ROOM", 3.0, SKC, "pop15-doors-rush.jpg", RBX("DOORS"), bs=200)),
    L("In The Mines, it chases you from Door 140, first on foot, then in a minecart over a giant ravine.",
      F("MINECART\nCHASE", "DOOR 140", "pop15-doors-alarm.jpg", RBX("DOORS"), bs=130)),
    L("At Door 200, you fight it at The Dam, where Seek turns into a giant blob of eyes.",
      S("THE DAM", "DOOR 200 BOSS", "red", "dark", bc="#ffffff", bs=180, fx=["red"], ic=[{"n": "eye", "x": 540, "y": 820, "s": 220, "a": "pulse"}])),
    L("And at the very end, Seek infects Queen Grumble, and its humanoid form crawls out. To be continued.",
      CLIP("rb17-seek-b.mp4", "TO BE\nCONTINUED", "SEEK'S REAL FORM", 5.0, SKC, "pop15-doors-lineup.jpg", RBX("DOORS"), bs=130)),
    tease("Next: the Roblox horror game that DOORS helped inspire.", "NEXT: PRESSURE", "pop17-pressure-logo.jpg", RBX("Pressure")),
    end("Is Seek the scariest monster?", "SCARIEST\nMONSTER?", bg="dark", ground="dark"),
   ], mood="spooky")

PR, PRC = "rb17-pressure.mp4", "Clip: Pressure (Roblox gameplay)"
ep(144, "pressure-roblox-horror", "Pressure Is Roblox's Deepest Horror Game", 43, "#2979ff", HEART, 1.04,
   {"font": MF + "SairaStencilOne-Regular.ttf", "size": 96, "fill": "#ffffff", "hi": "#82b1ff", "stroke": 8},
   [L("This Roblox horror game takes place at the bottom of the ocean.",
      CLIP("rb17-pressure-b.mp4", "THE BOTTOM\nOF THE OCEAN", "PRESSURE", 0, PRC, "pop17-pressure-logo.jpg", RBX("Pressure"), bs=124)),
    L("It's called Pressure, made by a group called Urbanshade: Hadal Division, and it came out in February 2023.",
      F("PRESSURE", "URBANSHADE: HADAL DIVISION", "pop17-pressure-logo.jpg", RBX("Pressure"), bs=150)),
    L("You escape a flooded underwater facility, room by room, while monsters hunt you down.",
      CLIP("rb17-pressure-a.mp4", "ESCAPE THE\nFACILITY", "ROOM BY ROOM", 0, PRC, "pop17-pressure-monster.jpg", RBX("Pressure"), bs=124)),
    L("It was inspired by Rooms, the same game that inspired DOORS.",
      F("INSPIRED\nBY ROOMS", "LIKE DOORS", "pop17-pressure-monster.jpg", RBX("Pressure"), bs=140)),
    L("It has over 492 million visits and 1.6 million favorites, and it peaked at 111,000 players at once in March 2026.",
      {"count": {"from": 0, "to": 492, "fmt": "{:.0f}M", "dur": 1.4}, "sub": "VISITS", "bg": "night", "ground": "stone", "bs": 220, "fx": ["sparkle"], "vig": True}),
    tease("Next: how much Roblox paid its creators last year.", "NEXT: $1 BILLION", "pop15-sab-dragon.jpg", RBX("Steal a Brainrot")),
    end("DOORS or Pressure?", "DOORS OR\nPRESSURE?", bg="dark", ground="dark"),
   ], mood="spooky")

ep(145, "roblox-paid-creators-1-billion", "ROBLOX Paid Creators 1 Billion", 43, "#00e676", LIAM, 1.06,
   {"font": MF + "Anton-Regular.ttf", "size": 104, "hi": "#69f0ae", "stroke": 8},
   [L("Roblox paid its game creators about one billion dollars in a single year.",
      F("$1 BILLION", "PAID TO CREATORS", "pop15-sab-dragon.jpg", RBX("Steal a Brainrot"), bs=170)),
    L("Creators earn Robux from their games, then swap them for real money through a program called DevEx.",
      S("ROBUX → $", "DEVEX", "gold", "grass", rays="#ffffff", bs=200, fx=["coins"], ic=[{"n": "money", "x": 860, "y": 820, "s": 160, "a": "spin"}],
        av=[av([0.0, 0.8], "cheer", "a")])),
    L("In 2025 that added up to around one billion dollars, up from 923 million the year before.",
      {"count": {"from": 0, "to": 923, "fmt": "${:.0f}M", "dur": 1.3}, "sub": "THE YEAR BEFORE", "bg": "mint", "ground": "grass", "bs": 200, "fx": ["coins"], "av": [{"p": [0.0, 0.8], "a": "jump", "c": "g"}]}),
    L("The top 1,000 creators made about 1.1 million dollars each, on average.",
      S("$1.1M EACH", "TOP 1,000 CREATORS", "party", "purple", rays="#ffffff", bs=160, fx=["confetti"],
        av=[av([-1.6, 0.6], "jump", "a"), av([0, 1.0], "cheer", "g"), av([1.6, 0.6], "jump", "b")])),
    L("And Roblox even raised the DevEx rate by 8.5 percent, so every Robux is now worth more cash.",
      S("+8.5%", "MORE CASH PER ROBUX", "gold", "grass", bs=220, fx=["coins"], ic=[{"n": "bolt", "x": 860, "y": 820, "s": 150, "a": "pulse"}], av=[av([-1.2, 0.6], "cheer", "a"), av([1.2, 0.6], "cheer", "b")])),
    tease("Next: the biggest Roblox games right now.", "NEXT: BIGGEST\nGAMES NOW", "pop15-egg-trex.jpg", RBX("Steal An Egg")),
    end("Would you make a Roblox game?", "WOULD YOU\nMAKE ONE?", bg="gold", ground="grass"),
   ], pron={"DevEx": "Dev Ex", "Robux": "Robucks"})

ep(146, "biggest-roblox-games-right-now", "The 5 Biggest ROBLOX Games Right Now", 42, "#ffca28", SARAH, 1.04,
   {"font": MF + "Chewy-Regular.ttf", "size": 104, "upper": False, "fill": "#ffffff", "hi": "#ffd54f", "stroke": 8},
   [L("These are the five biggest Roblox games right now, by players online this week.",
      F("TOP 5\nRIGHT NOW", "BY PLAYERS ONLINE", "pop15-egg-trex.jpg", RBX("Steal An Egg"), bs=130)),
    L("Number 5: 99 Nights in the Forest, with about 189,000 people playing.",
      S("#5 99 NIGHTS", "189,000 PLAYING", "night", "grass", bs=140, fx=["fireflies"], props=[["tree", -1.8, -1.8], ["tree", 1.8, -2.0]], av=[av([0.0, 0.8], "walk", "a")])),
    L("Number 4: Adopt Me, with about 207,000.",
      F("#4 ADOPT ME", "207,000 PLAYING", "pop15-adoptme.jpg", RBX("Adopt Me!"), bs=140)),
    L("Number 3: Brookhaven, with about 384,000, and almost 89 billion visits.",
      F("#3 BROOKHAVEN", "384,000 PLAYING", "pop15-brookhaven.jpg", RBX("Brookhaven RP"), bs=140)),
    L("Number 2: Murder Mystery 2, with about 702,000. It's twelve years old.",
      F("#2 MM2", "702,000 PLAYING", "pop16-mm2-halloween.jpg", RBX("Murder Mystery 2"), bs=150)),
    L("And number 1: Steal An Egg, with over one million people playing at the same time.",
      {"count": {"from": 0, "to": 1090158, "fmt": "{:,.0f}", "dur": 1.6}, "sub": "STEAL AN EGG #1", "bg": "party", "ground": "purple", "bs": 150, "fx": ["confetti"]}),
    tease("Next: the Geometry Dash level that was hacked.", "NEXT: THE HACKED\nTOP 1", "pop15-gd-20.jpg", "Clip: Doggie"),
    end("Which one do you play?", "WHICH ONE\nDO YOU PLAY?", bg="party", ground="purple"),
   ])

# ============================================================ GEOMETRY DASH
SL, SLC = "gd17-slaughter.mp4", "Clip: Doggie, Slaughterhouse"
ep(147, "doggie-slaughterhouse", "Doggie Beat Slaughterhouse", 46, "#ff1744", FENRIR, 1.06,
   {"font": MF + "BlackOpsOne-Regular.ttf", "size": 92, "fill": "#ffffff", "hi": "#ff5252", "stroke": 8},
   [L("Doggie beat this level, and only years later got credit as its real verifier.",
      CLIP("gd17-slaughter-end.mp4", "THE REAL\nVERIFIER", "SLAUGHTERHOUSE", 8.0, SLC, bs=130)),
    L("It's Slaughterhouse, built by icedcave and a team of creators, and it was number 1 on the Demonlist for 221 days.",
      CLIP("gd17-slaughter-mid.mp4", "#1 FOR\n221 DAYS", "BY ICEDCAVE", 0, SLC, bs=130)),
    L("Another player, spaceuk, claimed to verify it first, in October 2021.",
      CLIP("gd17-slaughter-mid.mp4", "SPACEUK\nCLAIMED IT", "OCTOBER 2021", 6.0, SLC, bs=130)),
    L("Doggie beat it on December 19th, 2021, after 79,170 attempts.",
      {"count": {"from": 0, "to": 79170, "fmt": "{:,.0f}", "dur": 1.6}, "sub": "ATTEMPTS", "bg": "red", "ground": "dark", "bc": "#ffffff", "bs": 170, "fx": ["red"], "vig": True}),
    L("Then in April 2023, spaceuk was exposed for hacking, so the verifier title went to Doggie.",
      CLIP("gd17-slaughter-end.mp4", "VERIFIER:\nDOGGIE", "APRIL 2023", 0, SLC, bs=130)),
    L("And Grief, the level Doggie verified this October, is a remake by the same creator.",
      F("GRIEF", "SAME CREATOR", "pop15-gd-66.jpg", "Clip: Doggie, GRIEF verification", bs=180)),
    tease("Next: how spaceuk got caught.", "NEXT: SPACEUK\nEXPOSED", "pop15-gd-20.jpg", "Clip: Doggie"),
    end("Doggie or Zoink?", "DOGGIE OR\nZOINK?", bg="red", ground="dark"),
   ], pron=dict(GD_PRON, spaceuk="space U K", icedcave="iced cave"), **GDE)

SU, SUC = "gd17-spaceuk.mp4", "Clip: spaceuk, Acheron"
ep(148, "spaceuk-exposed", "The Top Player Who Hacked Everything", 56, "#ffab00", MIKE, 1.06,
   {"font": MF + "RussoOne-Regular.ttf", "size": 92, "hi": "#ffd740", "stroke": 8},
   [L("He was the best Geometry Dash player in the world, until everyone found out he was hacking.",
      CLIP("gd17-spaceuk-a.mp4", "HE HACKED\nEVERYTHING", "SPACEUK", 0, SUC, bs=124)),
    L("spaceuk claimed huge levels like Slaughterhouse and Acheron, and won Best Player at the Geometry Dash Awards in 2021 and 2022.",
      CLIP("gd17-spaceuk-c.mp4", "BEST PLAYER\nX2", "2021 + 2022", 0, SUC, bs=124)),
    L("Then players noticed his click sounds didn't match what happened on screen.",
      CLIP("gd17-spaceuk-b.mp4", "CLICKS\nDIDN'T MATCH", "THE CLUE", 0, SUC, bs=124)),
    L("On April 25th, 2023, paqoe posted a video exposing him, showing a bot called zBot in his recordings, all the way back to 2021.",
      S("EXPOSED", "APRIL 25, 2023", "red", "dark", bc="#ffffff", bs=200, fx=["red"], ic=[{"n": "alarm", "x": 860, "y": 820, "s": 150, "a": "shake"}])),
    L("spaceuk admitted it. His records were removed, and titles went back to players like Doggie, Trick and Zoink.",
      CLIP("gd17-spaceuk-a.mp4", "RECORDS\nREMOVED", "TITLES RETURNED", 6.0, SUC, bs=124)),
    L("Since then he's played legit, and in January 2026 he really beat Acheron, after about 125,000 attempts.",
      CLIP("gd17-spaceuk-c.mp4", "LEGIT\nTHIS TIME", "ACHERON: ~125,000", 6.0, SUC, bs=124)),
    tease("Next: the level that stayed number 1 for 15 months.", "NEXT: #1 FOR\n15 MONTHS", "pop15-gd-47.jpg", "Clip: Doggie"),
    end("Should he be forgiven?", "FORGIVE\nHIM?", bg="red", ground="dark"),
   ], pron=dict(GD_PRON, spaceuk="space U K", zBot="Z bot"), **GDE)

TW, TWC = "gd17-tidalwave.mp4", "Clip: Zoink, Tidal Wave verification"
ep(149, "zoink-tidal-wave", "Tidal Wave Was Number 1 for 15 Months", 44, "#00e5ff", PUCK, 1.06,
   {"font": MF + "Audiowide-Regular.ttf", "size": 92, "fill": "#ffffff", "hi": "#18ffff", "stroke": 8},
   [L("This level stayed number 1 in Geometry Dash for 15 months, longer than any other.",
      CLIP("gd17-tw-end.mp4", "#1 FOR\n15 MONTHS", "TIDAL WAVE", 0, TWC, bs=124)),
    L("It's Tidal Wave, built by OniLink, and Zoink verified it on September 9th, 2023, after 49,534 attempts.",
      CLIP("gd17-tw-a.mp4", "49,534\nATTEMPTS", "ZOINK, SEPT 2023", 0, TWC, bs=124)),
    L("It has 200 frame perfect inputs, more than any other rated level.",
      CLIP("gd17-tw-b.mp4", "200 FRAME\nPERFECTS", "THE MOST EVER", 0, TWC, bs=124)),
    L("It's three minutes long, with over 220,000 objects.",
      CLIP("gd17-tw-a.mp4", "3 MINUTES", "220,134 OBJECTS", 6.0, TWC, bs=150)),
    L("It took over number 1 in February 2024, and held it until Amethyst passed it in June 2025.",
      F("471 DAYS\nAT #1", "FEB 2024 TO JUNE 2025", "pop15-gd-demonlist.jpg", "Image: Pointercrate Demonlist", bs=124, w=760, cy=1040, h=820)),
    L("Zoink's verification video has over 11 million views.",
      CLIP("gd17-tw-end.mp4", "11 MILLION\nVIEWS", "ZOINK'S VIDEO", 7.0, TWC, bs=124)),
    tease("Next: the meme that took over every school.", "NEXT: 6 7", "pop15-gd-66.jpg", "Clip: Doggie"),
    end("Could you beat Tidal Wave?", "COULD YOU\nBEAT IT?", bg="night", ground="stone"),
   ], pron=dict(GD_PRON, OniLink="Oni link"), **GDE)

# ============================================================ MEME LORE
ep(150, "six-seven-meme-origin", "Where 6 7 Came From", 44, "#ff4081", HEART, 1.04,
   {"font": MF + "Bangers-Regular.ttf", "size": 124, "mode": "word", "fill": "#ffffff", "hi": "#ffffff", "cy": 1470},
   [L("Six seven. Everyone says it, but where did it actually come from?",
      S("6 7", "WHERE DID IT COME FROM?", "party", "purple", rays="#ffffff", bs=280, fx=["confetti"],
        av=[av([-1.6, 0.6], "jump", "a"), av([0, 1.0], "cheer", "g"), av([1.6, 0.6], "jump", "b")])),
    L("It started with a rap song called Doot Doot, six seven, by Skrilla, officially released in February 2025.",
      S("DOOT DOOT", "SKRILLA, FEB 2025", "night", "stone", bs=180, fx=["sparkle"], ic=[{"n": "tv", "x": 860, "y": 820, "s": 150, "a": "pulse"}], av=[av([-1.2, 0.6], "jump", "a"), av([1.2, 0.6], "jump", "b")])),
    L("The line six seven blew up on TikTok, especially in basketball edits of LaMelo Ball, who is six foot seven.",
      S("6'7\"", "LAMELO BALL EDITS", "sunset", "grass", bs=240, av=[av([0.0, 0.8], "jump", "a")], ic=[{"n": "trophy", "x": 860, "y": 820, "s": 150, "a": "float"}])),
    L("What does it mean? Nobody knows. Skrilla said he never gave it a meaning, and he doesn't want to.",
      S("IT MEANS\nNOTHING", "ON PURPOSE", "red", "dark", bc="#ffffff", bs=170, fx=["red"], ic=[{"n": "question", "x": 860, "y": 820, "s": 160, "a": "spin"}], av=[av([0.0, 0.8], "wave", "g")])),
    L("And Dictionary.com picked six seven as its word of the year for 2025.",
      S("WORD OF\nTHE YEAR", "DICTIONARY.COM, 2025", "gold", "grass", rays="#ffffff", bs=170, fx=["confetti"], ic=[{"n": "crown", "x": 860, "y": 820, "s": 150, "a": "float"}], av=[av([-1.4, 0.6], "cheer", "a"), av([1.4, 0.6], "cheer", "b")])),
    L("Next: Cyberpunk Edgerunners 2 is finally out. Subscribe so you don't miss it.", S("NEXT:\nEDGERUNNERS 2", "SUBSCRIBE SO YOU DON'T MISS IT", "night", "stone", bs=124, ss=40, fx=["sparkle"], ic=[{"n": "tv", "x": 860, "y": 820, "s": 150, "a": "pulse"}], av=[av([0.0, 0.8], "run", "a")])),
    end("Six or seven?", "SIX OR\nSEVEN?", bg="party", ground="purple"),
   ], pron={"Skrilla": "Skrilla", "LaMelo": "La Melo"}, **ML)

ER, ERC = "an17-edgerunners2.mp4", "Clip: Cyberpunk: Edgerunners 2 trailer, Netflix"
ep(151, "cyberpunk-edgerunners-2-is-out", "Cyberpunk Edgerunners 2 Is Out", 58, "#ffea00", LIAM, 1.06,
   {"font": MF + "Oxanium[wght].ttf", "size": 96, "fill": "#ffffff", "hi": "#ffff00", "stroke": 8},
   [L("Cyberpunk Edgerunners 2 is finally out, and fans are split.",
      CLIP("an17-er-a.mp4", "EDGERUNNERS 2\nIS OUT", "FANS ARE SPLIT", 0, ERC, bs=110)),
    L("All 10 episodes dropped on Netflix on October 20th, made by Studio Trigger and CD Projekt Red.",
      CLIP("an17-er-b.mp4", "10 EPISODES", "OCTOBER 20", 0, ERC, bs=150)),
    L("It's a brand new crew, not a direct sequel. Roman, a young filmmaker. Talia, who joins the Maelstrom gang. Weak Kingsley, an old edgerunner. And D, a netrunner out for revenge.",
      CLIP("an17-er-c.mp4", "A NEW CREW", "NOT A DIRECT SEQUEL", 0, ERC, bs=150)),
    L("The opening song is 10:15 Saturday Night by The Cure.",
      CLIP("an17-er-a.mp4", "THE CURE", "THE OPENING SONG", 6.0, ERC, bs=150), say="The opening song is Ten Fifteen Saturday Night, by The Cure."),
    L("It debuted at number 1 on Netflix in the US. But on Rotten Tomatoes, critics gave it 78 percent and fans 60, way down from season 1's 100 and 95.",
      S("78% / 60%", "SEASON 1: 100% / 95%", "night", "stone", bs=170, vig=True, ic=[{"n": "tv", "x": 860, "y": 820, "s": 150, "a": "shake"}])),
    L("Reviews praise the animation and action, but say the cast is too big and the crew lacks chemistry.",
      CLIP("an17-er-b.mp4", "GREAT ACTION", "TOO MANY CHARACTERS?", 6.0, ERC, bs=140)),
    tease("Next: Roblox's scariest monster, Seek.", "NEXT: WHO IS\nSEEK?", "pop15-doors-seek.jpg", RBX("DOORS")),
    end("Better or worse than season 1?", "BETTER OR\nWORSE?", bg="night", ground="stone"),
   ], pron={"Edgerunners": "Edge runners", "Talia": "Tah-lia", "Maelstrom": "Male strom", "netrunner": "net runner"}, edition="ANIME", mood="spooky")


# ================================================================== write
for e in RB:
    e = dict(preset="roblox", hdr="tag", **e)
    for l in e["lines"]:
        sc = l["sc"]
        for m in [sc.get("photo"), sc.get("full")]:
            if m:
                f = m.get("img") or m.get("clip")
                if not os.path.exists(os.path.join(ROOT, "episodes", "assets", f)):
                    print("  MISSING", e["slug"], f)
    json.dump(e, open(os.path.join(ROOT, "episodes", "roblox", e["slug"] + ".json"), "w"), indent=1, ensure_ascii=False)
    print(e["slug"], len(e["lines"]), "lines", sum(len(l.get("say", l["t"]).split()) for l in e["lines"]), "words", "target", e["target"])
