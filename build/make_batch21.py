"""Writes batch 21 (facts checked 2026-10-26; Roblox numbers read live from Roblox's API on Oct 26):
4 Roblox + 4 Geometry Dash + 1 meme lore (code rot) + 1 trending (BioWare / Mass Effect) = #181-190.
No 'Next:' teasers. Clips come from batches/batch-21.json and are downloaded + rendered by SparkCart Studio on the PC."""

import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CTA = " Like and subscribe, and comment for which game we should review next!"
CTA_SUB = "COMMENT FOR WHICH GAME\nWE SHOULD REVIEW NEXT!"
MF = "../modern/fonts/"
RB, CLIPS = [], []
MIKE, SARAH, HEART, FENRIR, LIAM, PUCK = "am_michael", "af_sarah", "af_heart", "am_fenrir", "am_liam", "am_puck"


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


def CLIP(name, big, sub, start, credit, **k):
    """Full-screen real clip with the title over it (clip is fetched by the app before rendering)."""
    k.setdefault("by", 300)
    k.setdefault("bs", 120)
    k.setdefault("ss", 50)
    return S(big, sub, "night", "dark", full={"credit": credit, "clip": name, "start": start}, **k)


def clip(name, url, section=None, cut=2, backup=None):
    CLIPS.append({"name": name[:-4], "url": url, "backup": backup or [], "section": section, "cut": cut, "len": 13})


def COUNT(to, sub, fmt="{:,.0f}", bg="night", ground="stone", fx="sparkle", **k):
    d = {"count": {"from": 0, "to": to, "fmt": fmt, "dur": 1.5}, "sub": sub, "bg": bg, "ground": ground, "bs": 160, "fx": [fx]}
    if bg == "red":
        d.update(bc="#ffffff", vig=True)
    d.update(k)
    return d


def end(q, big, bg="party", ground="purple", **k):
    av_ = [{"p": [-1.8, 0.6], "a": "cheer", "c": "a"}, {"p": [0, 1.2], "a": "wave", "c": "g"}, {"p": [1.8, 0.6], "a": "cheer", "c": "b"}]
    ic = [{"n": "heart", "x": 170, "y": 700, "s": 130, "a": "pulse"}, {"n": "bolt", "x": 910, "y": 700, "s": 130, "a": "pulse"}]
    return L(q + CTA, S(big, CTA_SUB, bg, ground, rays="#ffffff", ss=50, sgap=62, fx=["confetti"], av=av_, ic=ic, **k))


def av(p, a="bob", c="a", **k):
    d = {"p": p, "a": a, "c": c}
    d.update(k)
    return d


def ic(n, a="float"):
    return [{"n": n, "x": 860, "y": 820, "s": 150, "a": a}]


def ep(num, slug, name, voice, accent, cap, lines, pron=None, **k):
    RB.append(dict(num=num, slug=f"{num}-{slug}", file=f"{num} {name}.mp4", target=0, accent=accent,
                   voice=voice, speed=1.04, cap=cap, pron=pron or {}, lines=lines, **k))


GD_PRON = {"Demonlist": "Demon list", "Zoink": "Zoynk", "BGram": "B Gram", "MindCap": "Mind Cap", "nSwish": "N Swish",
           "BoldStep": "Bold Step", "Exyl": "Ex-il", "Dils": "Dills", "thik": "thick", "Exen": "Ex-en", "ViperVenom95": "Viper Venom"}
GDE = dict(edition="GEOMETRY DASH", mood="spooky")

# ============================================================ ROBLOX
DSC = "Clip: DONT SPLASH (Roblox gameplay)"
clip("rb21-ds-a.mp4", "https://www.youtube.com/watch?v=xIXpJ38iS7o", "*2:00-2:20", backup=["https://www.youtube.com/watch?v=lkK3F6Md0JY"])
clip("rb21-ds-b.mp4", "https://www.youtube.com/watch?v=K2RZJqwQ138", "*4:00-4:20", backup=["https://www.youtube.com/watch?v=9SG2p7DbDms"])
ep(181, "dont-splash-roblox", "DONT SPLASH Is 9 Days Old With 87,000 Players", PUCK, "#00e5ff",
   {"font": MF + "BlackOpsOne-Regular.ttf", "size": 92, "fill": "#ffffff", "hi": "#84ffff", "stroke": 8},
   [L("This Roblox horror game is only 9 days old, and 87,000 people are playing it right now.",
      CLIP("rb21-ds-a.mp4", "DONT SPLASH", "9 DAYS OLD", 0, DSC, bs=170)),
    L("It's called DONT SPLASH, made by slo7th, and it came out on October 17th.",
      CLIP("rb21-ds-b.mp4", "BY SLO7TH", "OCTOBER 17, 2026", 0, DSC, bs=170)),
    L("It's inspired by the Poolrooms, the creepy, empty swimming pools from the backrooms.",
      S("THE\nPOOLROOMS", "THE INSPIRATION", "ocean", "water", bs=170, fx=["waves"], ic=ic("eye", "pulse"), av=[av([0.0, 0.8], "walk", "a")])),
    L("The game's only warning? Don't splash. It knows.",
      CLIP("rb21-ds-a.mp4", "IT KNOWS", "DON'T SPLASH", 6.0, DSC, bs=200)),
    L("In just over a week, it already has 46 million visits.",
      COUNT(46057769, "VISITS IN 9 DAYS", bg="red", ground="dark", fx="red")),
    end("Would you play it alone?", "WOULD YOU PLAY\nIT ALONE?", bg="night", ground="dark"),
   ], pron={"DONT": "Don't", "slo7th": "slow seventh", "Poolrooms": "Pool rooms"}, mood="spooky")

BAC = "Clip: Berry Avenue (Roblox gameplay)"
clip("rb21-ba-a.mp4", "https://www.youtube.com/watch?v=p-ZOEfA4qKc", "*3:00-3:20", backup=["https://www.youtube.com/watch?v=XoTt9iFlEYA"])
clip("rb21-ba-b.mp4", "https://www.youtube.com/watch?v=Blp8zbpYdUo", "*6:00-6:20", backup=["https://www.youtube.com/watch?v=mg1ow1ZYV6E"])
ep(182, "berry-avenue-roblox", "Berry Avenue Has Almost 9 Billion Visits", HEART, "#ff4081",
   {"font": MF + "Chewy-Regular.ttf", "size": 104, "upper": False, "fill": "#ffffff", "hi": "#ff80ab", "stroke": 8},
   [L("This Roblox town has been visited almost 9 billion times.",
      CLIP("rb21-ba-a.mp4", "BERRY\nAVENUE", "ALMOST 9 BILLION VISITS", 0, BAC, bs=170)),
    L("Berry Avenue is made by Amberry Games, and came out in January 2022.",
      CLIP("rb21-ba-b.mp4", "JANUARY\n2022", "BY AMBERRY GAMES", 0, BAC, bs=150)),
    L("You can go to high school, work at the grocery store, treat patients at the hospital, or rob the bank and get chased by the police.",
      S("PICK YOUR\nLIFE", "SCHOOL, JOBS, BANK ROBBERY", "day", "grass", bs=150, ic=ic("money", "shake"), av=[av([-1.2, 0.6], "run", "a"), av([1.2, 0.6], "run", "b")])),
    L("It has 3.7 million favorites, and once had over 200,000 players at once.",
      CLIP("rb21-ba-a.mp4", "200,000\nAT ONCE", "3.7 MILLION FAVORITES", 6.0, BAC, bs=150)),
    L("Total visits right now:",
      COUNT(8904490705, "VISITS", bg="party", ground="purple", fx="confetti", bs=130)),
    end("Berry Avenue or Brookhaven?", "BERRY OR\nBROOKHAVEN?", bg="party", ground="purple"),
   ], pron={"Amberry": "Am-berry"})

MVC = "Clip: Murderers VS Sheriffs Duels (Roblox gameplay)"
clip("rb21-mv-a.mp4", "https://www.youtube.com/watch?v=55ZxMWJsVIw", "*1:30-1:50", backup=["https://www.youtube.com/watch?v=XAFDWvnvL7w"])
clip("rb21-mv-b.mp4", "https://www.youtube.com/watch?v=XAFDWvnvL7w", "*0:40-0:55", cut=0)
ep(183, "murderers-vs-sheriffs", "Murderers VS Sheriffs Has Almost 2 Billion Visits", FENRIR, "#ff1744",
   {"font": MF + "Anton-Regular.ttf", "size": 104, "hi": "#ff5252", "stroke": 8},
   [L("Knives against guns. This Roblox duel game has almost 2 billion visits.",
      CLIP("rb21-mv-a.mp4", "MURDERERS\nVS SHERIFFS", "ALMOST 2 BILLION VISITS", 0, MVC, bs=130)),
    L("Murderers VS Sheriffs Duels came out in February 2025, made by the MVS Duels Community.",
      CLIP("rb21-mv-b.mp4", "FEBRUARY\n2025", "MVS DUELS COMMUNITY", 0, MVC, bs=150)),
    L("Murderers get knives, sheriffs get guns, and you fight in 1 versus 1, 2 versus 2, or 3 versus 3.",
      S("KNIFE\nVS GUN", "1V1, 2V2, 3V3", "red", "dark", bc="#ffffff", bs=170, fx=["red"], ic=ic("knife", "shake"), av=[av([-1.2, 0.6], "run", "a"), av([1.2, 0.6], "run", "b")])),
    L("Players call it a better MM2, because every round is a straight fight.",
      CLIP("rb21-mv-a.mp4", "BETTER\nTHAN MM2?", "EVERY ROUND IS A FIGHT", 6.0, MVC, bs=150)),
    L("And it has over 16 million favorites.",
      COUNT(16730897, "FAVORITES", bg="red", ground="dark", fx="red")),
    end("Murderer or sheriff?", "MURDERER OR\nSHERIFF?", bg="red", ground="dark"),
   ], pron={"MVS": "M V S", "VS": "versus", "MM2": "M M 2"})

ISC = "Clip: Illegal Soccer (Roblox gameplay)"
clip("rb21-is-a.mp4", "https://www.youtube.com/watch?v=rN8PDSyZn68", "*5:00-5:20", backup=["https://www.youtube.com/watch?v=vLZaYdQbpzU"])
clip("rb21-is-b.mp4", "https://www.youtube.com/watch?v=MtSsB7OYmi8", "*1:00-1:20", backup=["https://www.youtube.com/watch?v=hxCqfJmwoeE"])
ep(184, "illegal-soccer-roblox", "Illegal Soccer Is Soccer With Guns", LIAM, "#76ff03",
   {"font": MF + "RussoOne-Regular.ttf", "size": 92, "hi": "#b2ff59", "stroke": 8},
   [L("What if soccer had guns, jetpacks and no referees?",
      CLIP("rb21-is-a.mp4", "ILLEGAL\nSOCCER", "NO REFEREES", 0, ISC, bs=150)),
    L("That's Illegal Soccer, a Roblox game made by Repotted, that came out in May 2026.",
      CLIP("rb21-is-b.mp4", "BY REPOTTED", "MAY 2026", 0, ISC, bs=170)),
    L("You can kick, tackle and blow up the other team, use grappling hooks, and even shoot players while they dribble.",
      S("GUNS +\nJETPACKS", "+ GRAPPLING HOOKS", "day", "grass", bs=150, ic=ic("gun", "shake"), av=[av([-1.2, 0.6], "run", "a"), av([1.2, 0.6], "jump", "b")])),
    L("Watch out for oil spills, because you will slip.",
      CLIP("rb21-is-a.mp4", "OIL SPILLS", "YOU WILL SLIP", 6.0, ISC, bs=170)),
    L("In 5 months it got over 240 million visits.",
      COUNT(240505732, "VISITS", bg="day", ground="grass", fx="confetti")),
    end("Would you play it?", "WOULD YOU\nPLAY IT?", bg="day", ground="grass"),
   ])

# ============================================================ GEOMETRY DASH
LMC = "Clip: LIMBO by MindCap and more (YouTube)"
clip("gd21-lm-a.mp4", "https://www.youtube.com/watch?v=kXYMbaMVOZg", "*0:40-1:00", backup=["https://www.youtube.com/watch?v=dtKV9uSa5jQ"])
clip("gd21-lm-b.mp4", "https://www.youtube.com/watch?v=ryBbuH_SPbs", "*3:05-3:25", backup=["https://www.youtube.com/watch?v=X8lVZFTbP3E"])
ep(185, "limbo-109490", "LIMBO Took 109,490 Attempts", MIKE, "#651fff",
   {"font": MF + "SairaStencilOne-Regular.ttf", "size": 96, "fill": "#ffffff", "hi": "#b388ff", "stroke": 8},
   [L("This Geometry Dash level ends with a guessing game, and one wrong pick kills you.",
      CLIP("gd21-lm-a.mp4", "LIMBO", "THE MEMORY LEVEL", 0, LMC, bs=200)),
    L("LIMBO was hosted by MindCap, and BGram verified it in November 2022.",
      CLIP("gd21-lm-b.mp4", "BGRAM", "NOVEMBER 2022", 0, LMC, bs=170)),
    L("It took him 109,490 attempts.",
      COUNT(109490, "ATTEMPTS", bg="red", ground="dark", fx="red")),
    L("At the end, 8 keys shuffle like cups, and there are 40,320 ways to order them. Only one is right.",
      S("8 KEYS", "40,320 ORDERS, 1 IS RIGHT", "night", "stone", bs=200, fx=["sparkle"], ic=ic("key", "shake"), av=[av([0.0, 0.8], "jump", "a")])),
    L("Its showcase video now has over 32 million views.",
      CLIP("gd21-lm-a.mp4", "32 MILLION\nVIEWS", "THE SHOWCASE", 6.0, LMC, bs=150)),
    end("Could you remember the keys?", "COULD YOU\nREMEMBER?", bg="night", ground="stone"),
   ], pron=dict(GD_PRON, LIMBO="Limbo"), **GDE)

ADC = "Clip: Abyss of Darkness, verified by Cursed (YouTube)"
clip("gd21-ad-a.mp4", "https://www.youtube.com/watch?v=ejJkpqcMMCY", "*0:20-0:40", backup=["https://www.youtube.com/watch?v=Hzr7_PrgeqI"])
clip("gd21-ad-b.mp4", "https://www.youtube.com/watch?v=ejJkpqcMMCY", "*1:40-2:00", backup=["https://www.youtube.com/watch?v=Hzr7_PrgeqI"])
ep(186, "abyss-of-darkness-98", "Abyss of Darkness Broke a Player at 98%", SARAH, "#d50000",
   {"font": MF + "BlackOpsOne-Regular.ttf", "size": 92, "fill": "#ffffff", "hi": "#ff5252", "stroke": 8},
   [L("One player died at 98% on this level twice, then quit after about 200,000 attempts.",
      CLIP("gd21-ad-a.mp4", "ABYSS OF\nDARKNESS", "DIED AT 98%, TWICE", 0, ADC, bs=150)),
    L("Abyss of Darkness was made by Exen, but his 2018 verification was hacked, so everyone forgot about it.",
      S("HACKED", "EXEN, 2018", "red", "dark", bc="#ffffff", bs=200, fx=["red"], ic=ic("alarm", "shake"), av=[av([0.0, 0.8], "run", "a")])),
    L("Then in 2021, Dils thik hit 98%, two times, and gave up.",
      COUNT(98, "DILS THIK, TWICE", fmt="{:.0f}%", bg="red", ground="dark", fx="red", bs=220)),
    L("Finally, in April 2022, Cursed verified it, after 54,315 attempts.",
      CLIP("gd21-ad-b.mp4", "CURSED", "54,315 ATTEMPTS", 0, ADC, bs=180)),
    L("It became the number 1 hardest level in the game.",
      CLIP("gd21-ad-a.mp4", "#1 HARDEST", "JUNE 2022", 6.0, ADC, bs=170)),
    end("Would you quit at 98%?", "QUIT AT\n98%?", bg="red", ground="dark"),
   ], pron=GD_PRON, **GDE)

GLC = "Clip: The Golden by Bo and more (YouTube)"
clip("gd21-gl-a.mp4", "https://www.youtube.com/watch?v=wpS5PSHmji0", "*0:25-0:45", backup=["https://www.youtube.com/watch?v=fyKRPHKAss8"])
clip("gd21-gl-b.mp4", "https://www.youtube.com/watch?v=NkOOeh2ly4A", "*0:40-1:00", backup=["https://www.youtube.com/watch?v=fyKRPHKAss8"])
ep(187, "the-golden-52870", "The Golden Took 52,870 Attempts", PUCK, "#ffab00",
   {"font": MF + "RussoOne-Regular.ttf", "size": 92, "hi": "#ffd740", "stroke": 8},
   [L("This level was so hard, it was passed between four top players before anyone beat it.",
      CLIP("gd21-gl-a.mp4", "THE GOLDEN", "4 PLAYERS TRIED", 0, GLC, bs=180)),
    L("The Golden was hosted by Bo. He tried to verify it, then passed it to Sky Jax, then Dolphy, then nSwish.",
      S("BO, SKY JAX,\nDOLPHY, NSWISH", "THE HANDOFFS", "gold", "grass", rays="#ffffff", bs=120, ic=ic("crown", "float"), av=[av([-1.2, 0.6], "run", "a"), av([1.2, 0.6], "run", "b")])),
    L("nSwish finally verified it in April 2020, after 52,870 attempts.",
      COUNT(52870, "NSWISH'S ATTEMPTS", bg="gold", ground="grass", fx="confetti")),
    L("It's full of fast wave parts in a dark jungle.",
      CLIP("gd21-gl-b.mp4", "WAVE\nJUNGLE", "TRIPLE SPEED", 0, GLC, bs=170)),
    L("It beat Tartarus and stayed number 1 for 105 days.",
      CLIP("gd21-gl-b.mp4", "#1 FOR\n105 DAYS", "OVER TARTARUS", 6.0, GLC, bs=150)),
    end("Could you beat The Golden?", "COULD YOU\nBEAT IT?", bg="gold", ground="grass"),
   ], pron=dict(GD_PRON, Bo="Bo", Dolphy="Dol-fee", Tartarus="Tar-ta-rus"), **GDE)

ERC = "Clip: Erebus, verified by BoldStep (YouTube)"
clip("gd21-er-a.mp4", "https://www.youtube.com/watch?v=8csWDx6C2YI", "*0:30-0:50", backup=["https://www.youtube.com/watch?v=RdUwTwoxHOw"])
clip("gd21-er-b.mp4", "https://www.youtube.com/watch?v=RdUwTwoxHOw", "*0:50-1:10", backup=["https://www.youtube.com/watch?v=7i7W7IAx5rA"])
ep(188, "erebus-44803", "Erebus Took 44,803 Attempts", FENRIR, "#00b0ff",
   {"font": MF + "Anton-Regular.ttf", "size": 104, "hi": "#80d8ff", "stroke": 8},
   [L("This level stayed on the Demonlist for 2,277 days, a record at the time.",
      CLIP("gd21-er-a.mp4", "EREBUS", "2,277 DAYS", 0, ERC, bs=200)),
    L("Erebus was made by Rustam and ILRELL, and BoldStep verified it in March 2017.",
      CLIP("gd21-er-b.mp4", "BOLDSTEP", "MARCH 2017", 0, ERC, bs=170)),
    L("It took him 44,803 attempts, over three months.",
      COUNT(44803, "ATTEMPTS", bg="red", ground="dark", fx="red")),
    L("He called the last part the dreaded ship. And some bugs even crash you.",
      CLIP("gd21-er-b.mp4", "THE DREADED\nSHIP", "81% TO 100%", 6.0, ERC, bs=140)),
    L("Later, Exyl beat it on a 60 hertz screen, in 68,498 attempts.",
      COUNT(68498, "EXYL ON 60HZ", bg="night", ground="stone", fx="sparkle")),
    end("Could you beat Erebus?", "COULD YOU\nBEAT IT?", bg="night", ground="stone"),
   ], pron=dict(GD_PRON, Erebus="Air-uh-bus", Rustam="Roo-stam", ILRELL="Ill-rell"), **GDE)

# ============================================================ MEME LORE
CRC = "Clips: TikTok, @diaryofawimpykidfan01, @planetaryequinox, @originally..gavin"
clip("ml21-cr-a.mp4", "https://www.tiktok.com/@diaryofawimpykidfan01/video/7696245612215356685", None, 0,
     backup=["https://www.tiktok.com/@ted.broome1/video/7697372713521794318"])
clip("ml21-cr-b.mp4", "https://www.tiktok.com/@planetaryequinox/video/7643145686371863839", None, 0,
     backup=["https://www.tiktok.com/@acherryblossomtree/video/7643551584290442518"])
clip("ml21-cr-c.mp4", "https://www.tiktok.com/@originally..gavin/video/7645766551240494354", None, 0,
     backup=["https://www.tiktok.com/@forgottenfuture1/video/7644967301451762966"])
ep(189, "code-rot-meme", "What Code Rot Actually Means", HEART, "#00e676",
   {"font": MF + "Bangers-Regular.ttf", "size": 124, "mode": "word", "fill": "#ffffff", "hi": "#ffffff", "cy": 1470},
   [L("Yep, it's code rotted, indeed. But what is code rot?",
      CLIP("ml21-cr-a.mp4", "CODE ROT", "YEP, IT'S CODE ROTTED", 0, CRC, bs=200)),
    L("Code rot is when a game gets old, the world around it updates, and it slowly starts to break.",
      S("CODE ROT", "OLD GAMES SLOWLY BREAK", "dark", "stone", bs=200, fx=["sparkle"], ic=ic("code", "shake"), av=[av([0.0, 0.8], "walk", "a")])),
    L("In May 2026, Royale High players noticed old apartments glitching, and Royale High blamed Roblox updates.",
      CLIP("ml21-cr-b.mp4", "ROYALE HIGH", "MAY 2026", 0, CRC, bs=170)),
    L("Then players found rot in old games everywhere. One clip of Camping got 1.8 million views.",
      CLIP("ml21-cr-c.mp4", "CAMPING", "1.8 MILLION VIEWS", 0, CRC, bs=180)),
    L("And in October, a TikTok Despicable Me filter started glitching, so everyone said, the filter is code rotted.",
      CLIP("ml21-cr-a.mp4", "THE GRU\nFILTER", "CODE ROTTED, INDEED", 6.0, CRC, bs=150)),
    end("What game has code rot?", "WHAT GAME HAS\nCODE ROT?", bg="dark", ground="stone"),
   ], pron={"Gru": "Groo"}, edition="MEME LORE", mood="spooky")

# ============================================================ TRENDING
MEC = "Clip: Mass Effect Legendary Edition trailers, EA / BioWare"
clip("tr21-me-a.mp4", "https://www.youtube.com/watch?v=n8i53TtQ6IQ", "*0:20-0:40", backup=["https://www.youtube.com/watch?v=UAScSKBDuno"])
clip("tr21-me-b.mp4", "https://www.youtube.com/watch?v=n8i53TtQ6IQ", "*1:05-1:25", backup=["https://www.youtube.com/watch?v=q0lVjqxF0C0"])
ep(190, "bioware-shut-down", "EA Shut Down BioWare and 207,000 Fans Want Mass Effect Saved", MIKE, "#2979ff",
   {"font": MF + "Oxanium[wght].ttf", "size": 96, "fill": "#ffffff", "hi": "#82b1ff", "stroke": 8},
   [L("EA just shut down BioWare, the studio behind Mass Effect.",
      CLIP("tr21-me-a.mp4", "BIOWARE\nSHUT DOWN", "OCTOBER 21, 2026", 0, MEC, bs=150)),
    L("On October 21st, EA announced about 400 layoffs, and the next Mass Effect game was cancelled.",
      S("MASS EFFECT 5\nCANCELLED", "ABOUT 400 LAYOFFS", "red", "dark", bc="#ffffff", bs=130, fx=["red"], ic=ic("alarm", "shake"), av=[av([0.0, 0.8], "walk", "a")])),
    L("One day later, a trailer for the cancelled game leaked online.",
      CLIP("tr21-me-b.mp4", "IT LEAKED", "ONE DAY LATER", 0, MEC, bs=200)),
    L("Now fans started a petition to save Mass Effect, and over 207,000 people signed it.",
      COUNT(207000, "SIGNATURES", fmt="{:,.0f}+", bg="space", ground="dark", fx="sparkle")),
    L("Even both voices of Commander Shepard, Jennifer Hale and Mark Meer, told fans to hold the line.",
      CLIP("tr21-me-a.mp4", "HOLD THE\nLINE", "BOTH SHEPARDS AGREE", 6.0, MEC, bs=150)),
    end("Should EA save Mass Effect?", "SAVE MASS\nEFFECT?", bg="space", ground="dark"),
   ], pron={"BioWare": "Bio-Ware", "Meer": "Meer", "EA": "E A"}, edition="TRENDING", mood="spooky")

# ================================================================== write
paths = []
for e in RB:
    e = dict(preset="roblox", hdr="tag", **e)
    words = sum(len(l.get("say", l["t"]).split()) for l in e["lines"])
    e["target"] = round(words / 2.72) + 1
    p = os.path.join("episodes", "roblox", e["slug"] + ".json")
    json.dump(e, open(os.path.join(ROOT, p), "w"), indent=1, ensure_ascii=False)
    paths.append(p)
    print(e["slug"], len(e["lines"]), "lines", words, "words")
manifest = {"batch": 21, "note": "4 Roblox, 4 GD, code rot, BioWare (Oct 26)", "posting": "batch-21/posting.txt",
            "episodes": paths, "clips": CLIPS}
json.dump(manifest, open(os.path.join(ROOT, "batches", "batch-21.json"), "w"), indent=1)
print(len(CLIPS), "clips")
