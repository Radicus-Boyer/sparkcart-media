"""Writes batch 20 (facts checked 2026-10-24): 3 Roblox + 4 Geometry Dash + 2 meme lore + 1 Modern Warfare 4 (#171-180). target 0 = auto from word count."""

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
RVC = "Clip: RIVALS (Roblox gameplay)"
ep(171, "rivals-roblox", "RIVALS Has Almost 19 Billion Visits", 0, "#ff1744", LIAM, 1.04,
   {"font": MF + "Anton-Regular.ttf", "size": 104, "hi": "#ff5252", "stroke": 8},
   [L("This Roblox shooter has almost 19 billion visits, and 95 million favorites.",
      CLIP("rb20-rv-a.mp4", "RIVALS", "19 BILLION VISITS", 0, RVC, "pop20-rivals-a.jpg", RBX("RIVALS"), bs=200)),
    L("RIVALS is made by Nosniy Games, and came out in June 2024.",
      F("JUNE 2024", "BY NOSNIY GAMES", "pop20-rivals-b.jpg", RBX("RIVALS"), bs=160)),
    L("You fight in duels, from 1 versus 1 up to 5 versus 5. First team to win 5 rounds wins.",
      CLIP("rb20-rv-b.mp4", "1V1 TO 5V5", "FIRST TO 5 ROUNDS", 0, RVC, "pop20-rivals-a.jpg", RBX("RIVALS"), bs=170)),
    L("At its peak, almost a million people were playing at once.",
      {"count": {"from": 0, "to": 967342, "fmt": "{:,.0f}", "dur": 1.6}, "sub": "PEAK PLAYERS", "bg": "red", "ground": "dark", "bc": "#ffffff", "bs": 150, "fx": ["red"], "vig": True}),
    L("It even won Best Shooter at the Roblox Innovation Awards.",
      CLIP("rb20-rv-a.mp4", "BEST\nSHOOTER", "ROBLOX AWARDS 2025", 6.0, RVC, "pop20-rivals-b.jpg", RBX("RIVALS"), bs=150)),
    tease("Next: the Roblox horror game full of creepy cartoon mascots.", "NEXT: DANDY'S\nWORLD", "pop20-dandy-a.jpg", RBX("Dandy's World")),
    end("What's your main weapon?", "YOUR MAIN\nWEAPON?", bg="red", ground="dark"),
   ], pron={"Nosniy": "Noz-nee", "RIVALS": "Rivals"})

DWC = "Clip: Dandy's World (Roblox gameplay)"
ep(172, "dandys-world-roblox", "Dandy's World Is Roblox's Creepiest Cartoon", 0, "#ffd600", HEART, 1.04,
   {"font": MF + "Chewy-Regular.ttf", "size": 104, "upper": False, "fill": "#ffffff", "hi": "#ffff00", "stroke": 8},
   [L("This cute cartoon flower is actually the villain of a Roblox horror game.",
      F("MEET DANDY", "DANDY'S WORLD", "pop20-dandy-a.jpg", RBX("Dandy's World"), bs=170)),
    L("Dandy's World is made by BlushCrunch Studio, and came out in January 2024.",
      CLIP("rb20-dw-a.mp4", "JANUARY\n2024", "BLUSHCRUNCH STUDIO", 0, DWC, "pop20-dandy-b.jpg", RBX("Dandy's World"), bs=150)),
    L("You team up as collectible cartoon Toons, each with their own stats and abilities.",
      F("COLLECT\nTOONS", "EACH ONE IS DIFFERENT", "pop20-dandy-b.jpg", RBX("Dandy's World"), bs=150)),
    L("Then you finish machines and go deeper into the Gardenview Center, while monsters chase you.",
      CLIP("rb20-dw-b.mp4", "GO DEEPER", "GARDENVIEW CENTER", 0, DWC, "pop20-dandy-a.jpg", RBX("Dandy's World"), bs=170)),
    L("In March 2026, it hit 607,000 players at once, and it now has 7.7 billion visits.",
      {"count": {"from": 0, "to": 607000, "fmt": "{:,.0f}", "dur": 1.5}, "sub": "PEAK PLAYERS", "bg": "party", "ground": "purple", "bs": 160, "fx": ["confetti"]}),
    L("Next: the Roblox fighting game that vanished overnight. Subscribe so you don't miss it.", S("NEXT: IT\nVANISHED", "SUBSCRIBE SO YOU DON'T MISS IT", "red", "dark", bc="#ffffff", bs=124, ss=40, fx=["red"], ic=[{"n": "alarm", "x": 860, "y": 820, "s": 150, "a": "shake"}], av=[av([0.0, 0.8], "run", "a")])),
    end("Who's your favorite Toon?", "FAVORITE\nTOON?", bg="party", ground="purple"),
   ], pron={"BlushCrunch": "Blush Crunch"}, mood="spooky")

JJC = "Clip: Jujutsu Shenanigans (Roblox gameplay)"
ep(173, "jujutsu-shenanigans-vanished", "The Roblox Game That Vanished Overnight", 0, "#7c4dff", PUCK, 1.04,
   {"font": MF + "BlackOpsOne-Regular.ttf", "size": 92, "fill": "#ffffff", "hi": "#b388ff", "stroke": 8},
   [L("One day in July 2025, one of Roblox's biggest fighting games just disappeared.",
      CLIP("rb20-jj-a.mp4", "IT VANISHED", "JULY 2025", 0, JJC, bs=170)),
    L("It's Jujutsu Shenanigans, a battlegrounds game made by Tze in 2022.",
      CLIP("rb20-jj-b.mp4", "JUJUTSU\nSHENANIGANS", "BY TZE, 2022", 0, JJC, bs=124)),
    L("On July 21st, it went offline with no warning, and players had no idea why.",
      S("OFFLINE", "JULY 21, 2025", "red", "dark", bc="#ffffff", bs=200, fx=["red"], ic=[{"n": "alarm", "x": 860, "y": 820, "s": 150, "a": "shake"}], av=[av([0.0, 0.8], "run", "a")])),
    L("Some said it was under review. But soon after, it came back online.",
      CLIP("rb20-jj-a.mp4", "IT CAME\nBACK", "UNDER REVIEW?", 6.0, JJC, bs=150)),
    L("Today it has over 7.7 billion visits, and almost 300,000 people playing right now.",
      {"count": {"from": 0, "to": 291657, "fmt": "{:,.0f}", "dur": 1.5}, "sub": "PLAYING RIGHT NOW", "bg": "night", "ground": "stone", "bs": 160, "fx": ["sparkle"], "av": [{"p": [-1.4, 0.6], "a": "jump", "c": "a"}, {"p": [1.4, 0.6], "a": "jump", "c": "b"}]}),
    tease("Next: the Geometry Dash player who verified 4 number 1 levels.", "NEXT: ZOINK", "pop15-gd-47.jpg", "Clip: Doggie"),
    end("Who's your main?", "WHO'S YOUR\nMAIN?", bg="night", ground="stone"),
   ], pron={"Tze": "Tsay"})

# ============================================================ GEOMETRY DASH
AVC = "Clip: Zoink, Avernus verification"
ep(174, "zoink-4-top-ones", "Zoink Verified 4 Number 1 Levels", 0, "#00e676", MIKE, 1.06,
   {"font": MF + "RussoOne-Regular.ttf", "size": 92, "hi": "#69f0ae", "stroke": 8},
   [L("Zoink has verified four number 1 levels, more than anyone else in Geometry Dash.",
      CLIP("gd20-av-a.mp4", "4 TOP 1s", "ZOINK", 0, AVC, bs=200)),
    L("First, Acheron, in August 2022, after 72,808 attempts.",
      {"count": {"from": 0, "to": 72808, "fmt": "{:,.0f}", "dur": 1.4}, "sub": "ACHERON", "bg": "red", "ground": "dark", "bc": "#ffffff", "bs": 170, "fx": ["red"], "vig": True}),
    L("Then Avernus, in March 2023.",
      CLIP("gd20-av-b.mp4", "AVERNUS", "MARCH 2023", 0, AVC, bs=180)),
    L("Then Tidal Wave, which stayed number 1 for 471 days.",
      S("TIDAL WAVE", "#1 FOR 471 DAYS", "night", "water", bs=160, fx=["waves"], ic=[{"n": "crown", "x": 860, "y": 820, "s": 150, "a": "float"}], av=[av([0.0, 0.8], "jump", "a")])),
    L("And Thinking Space 2, in May 2025, after 83,913 attempts.",
      {"count": {"from": 0, "to": 83913, "fmt": "{:,.0f}", "dur": 1.4}, "sub": "THINKING SPACE II", "bg": "night", "ground": "stone", "bs": 170, "fx": ["sparkle"]}),
    L("Nobody else has verified as many.",
      CLIP("gd20-av-a.mp4", "THE KING\nOF TOP 1s", "ZOINK", 6.0, AVC, bs=150)),
    tease("Next: the first level to take over 100,000 attempts.", "NEXT: BLOODLUST", "pop15-gd-20.jpg", "Clip: Doggie"),
    end("Zoink or Doggie?", "ZOINK OR\nDOGGIE?", bg="night", ground="stone"),
   ], pron=dict(GD_PRON, Avernus="Ah-ver-nus"), **GDE)

BLC = "Clip: Bloodlust by Knobbelboy and more (YouTube)"
ep(175, "bloodlust-121296", "Bloodlust Took 121,296 Attempts", 0, "#d50000", FENRIR, 1.06,
   {"font": MF + "BlackOpsOne-Regular.ttf", "size": 92, "fill": "#ffffff", "hi": "#ff5252", "stroke": 8},
   [L("This was the first Geometry Dash level to take over 100,000 attempts to verify.",
      CLIP("gd20-bl-a.mp4", "BLOODLUST", "100,000+ ATTEMPTS", 0, BLC, bs=180)),
    L("Bloodlust was hosted by Manix648, and verified by knobbelboy in February 2018.",
      CLIP("gd20-bl-b.mp4", "KNOBBELBOY", "FEBRUARY 2018", 0, BLC, bs=150)),
    L("It took him 121,296 attempts. That number is even the level's password.",
      {"count": {"from": 0, "to": 121296, "fmt": "{:,.0f}", "dur": 1.6}, "sub": "ALSO THE PASSWORD", "bg": "red", "ground": "dark", "bc": "#ffffff", "bs": 150, "fx": ["red"], "vig": True}),
    L("It was number 1 for over a year, until Zodiac in March 2019.",
      CLIP("gd20-bl-a.mp4", "#1 FOR\n383 DAYS", "UNTIL ZODIAC", 6.0, BLC, bs=150)),
    L("And its verification has over 12 million views, the most of any Demonlist verification on YouTube.",
      S("12 MILLION\nVIEWS", "MOST-VIEWED VERIFICATION", "gold", "grass", rays="#ffffff", bs=150, fx=["confetti"], ic=[{"n": "trophy", "x": 860, "y": 820, "s": 150, "a": "float"}], av=[av([0.0, 0.8], "cheer", "a")])),
    tease("Next: the number 1 level whose first verification was hacked.", "NEXT: ZODIAC", "pop15-gd-47.jpg", "Clip: Doggie"),
    end("Could you beat Bloodlust?", "COULD YOU\nBEAT IT?", bg="red", ground="dark"),
   ], pron=dict(GD_PRON, Manix648="Manix six four eight", knobbelboy="knobble boy"), **GDE)

ZDC = "Clip: Zodiac by Bianox and more (YouTube)"
ep(176, "zodiac-hacked-verification", "Zodiac's First Verification Was Hacked", 0, "#651fff", SARAH, 1.04,
   {"font": MF + "SairaStencilOne-Regular.ttf", "size": 96, "fill": "#ffffff", "hi": "#b388ff", "stroke": 8},
   [L("This number 1 level was first verified by a hacker.",
      CLIP("gd20-zd-a.mp4", "ZODIAC", "A HACKED VERIFY", 0, ZDC, bs=200)),
    L("Zodiac was hosted by Bianox, and first uploaded in January 2019.",
      CLIP("gd20-zd-b.mp4", "BY BIANOX", "JANUARY 2019", 0, ZDC, bs=170)),
    L("But the player who verified it, xander, later admitted he hacked it.",
      S("HE ADMITTED\nIT", "XANDER", "red", "dark", bc="#ffffff", bs=150, fx=["red"], ic=[{"n": "alarm", "x": 860, "y": 820, "s": 150, "a": "shake"}], av=[av([0.0, 0.8], "run", "a")])),
    L("So Technical verified it for real, in April 2019.",
      CLIP("gd20-zd-a.mp4", "TECHNICAL", "THE REAL VERIFY", 6.0, ZDC, bs=170)),
    L("It took the number 1 spot from Bloodlust, and held it for about 11 months, until Tartarus.",
      S("#1 FOR\n11 MONTHS", "UNTIL TARTARUS", "night", "stone", bs=150, fx=["sparkle"], ic=[{"n": "crown", "x": 860, "y": 820, "s": 150, "a": "float"}], av=[av([0.0, 0.8], "jump", "a")])),
    tease("Next: the secret top 1 that took 249,109 attempts.", "NEXT: NULLSCAPES", "pop15-gd-20.jpg", "Clip: Doggie"),
    end("Should hacked levels be removed?", "REMOVE\nHACKED LEVELS?", bg="night", ground="stone"),
   ], pron=dict(GD_PRON, Bianox="Bee-a-nox", xander="Zander"), **GDE)

NLC = "Clip: Nullscapes (YouTube)"
ep(177, "nullscapes-secret-top-1", "Nullscapes Took 249,109 Attempts to Beat", 0, "#00b0ff", LIAM, 1.06,
   {"font": MF + "RussoOne-Regular.ttf", "size": 92, "hi": "#80d8ff", "stroke": 8},
   [L("Players called this level the secret top 1, because nobody could beat it for over a year.",
      CLIP("gd20-nl-a.mp4", "SECRET\nTOP 1", "NULLSCAPES", 0, NLC, bs=170)),
    L("Nullscapes was made by Kiba, and Zoink verified it in September 2024, after over 90,000 attempts.",
      {"count": {"from": 0, "to": 90000, "fmt": "{:,.0f}+", "dur": 1.4}, "sub": "ZOINK'S ATTEMPTS", "bg": "night", "ground": "stone", "bs": 170, "fx": ["sparkle"]}),
    L("It's almost all robot mode, and it's the hardest robot level ever.",
      CLIP("gd20-nl-b.mp4", "ROBOT\nMODE", "THE HARDEST EVER", 0, NLC, bs=170)),
    L("Two players were even caught faking progress on it with bots.",
      S("FAKED\nPROGRESS", "CAUGHT", "red", "dark", bc="#ffffff", bs=170, fx=["red"], ic=[{"n": "code", "x": 860, "y": 820, "s": 150, "a": "shake"}], av=[av([0.0, 0.8], "run", "a")])),
    L("Finally, in October 2025, spookkd beat it, after 249,109 attempts.",
      {"count": {"from": 0, "to": 249109, "fmt": "{:,.0f}", "dur": 1.6}, "sub": "SPOOKKD'S ATTEMPTS", "bg": "party", "ground": "purple", "bs": 150, "fx": ["confetti"]}),
    L("Next: where Tung Tung Tung Sahur came from. Subscribe so you don't miss it.", S("NEXT: TUNG\nTUNG SAHUR", "SUBSCRIBE SO YOU DON'T MISS IT", "party", "purple", bs=124, ss=40, fx=["confetti"], av=[av([0.0, 0.8], "jump", "a")])),
    end("Could you beat Nullscapes?", "COULD YOU\nBEAT IT?", bg="night", ground="stone"),
   ], pron=dict(GD_PRON, Nullscapes="Null scapes", spookkd="spooked", Kiba="Kee-ba"), **GDE)

# ============================================================ MEME LORE
TGC = "Clip: Tung Tung Tung Sahur (YouTube)"
ep(178, "tung-tung-tung-sahur", "Where Tung Tung Tung Sahur Came From", 0, "#ff6d00", HEART, 1.04,
   {"font": MF + "Bangers-Regular.ttf", "size": 124, "mode": "word", "fill": "#ffffff", "hi": "#ffffff", "cy": 1470},
   [L("Tung Tung Tung Sahur. Everyone knows him, but where did he come from?",
      CLIP("ml20-tg-a.mp4", "TUNG TUNG\nTUNG SAHUR", "WHERE DID HE COME FROM?", 0, TGC, bs=150)),
    L("The first video was posted on TikTok on February 28th, 2025, during Ramadan.",
      S("FEB 28,\n2025", "THE FIRST VIDEO", "night", "stone", bs=170, fx=["sparkle"], ic=[{"n": "calendar", "x": 860, "y": 820, "s": 150, "a": "float"}], av=[av([0.0, 0.8], "walk", "a")])),
    L("Sahur is the meal Muslims eat before dawn during Ramadan. And tung tung tung is the sound of a drum, used in Indonesia to wake people up for it.",
      CLIP("ml20-tg-b.mp4", "SAHUR", "THE MEAL BEFORE DAWN", 0, TGC, bs=180)),
    L("The video got over 42 million views.",
      {"count": {"from": 0, "to": 42.5, "fmt": "{:.1f}M", "dur": 1.4}, "sub": "VIEWS", "bg": "party", "ground": "purple", "bs": 220, "fx": ["confetti"]}),
    L("Then it joined the Italian brainrot wave, with fan art and battles against Brr Brr Patapim.",
      S("VS BRR BRR\nPATAPIM", "THE BRAINROT WARS", "red", "dark", bc="#ffffff", bs=150, fx=["red"], av=[av([-1.2, 0.6], "jump", "a"), av([1.2, 0.6], "jump", "b")])),
    L("Next: the GTA meme that made Lamar a legend. Subscribe so you don't miss it.", S("NEXT: LAMAR\nROASTS FRANKLIN", "SUBSCRIBE SO YOU DON'T MISS IT", "sunset", "grass", bs=124, ss=40, ic=[{"n": "fire", "x": 860, "y": 820, "s": 150, "a": "pulse"}], av=[av([0.0, 0.8], "run", "a")])),
    end("Tung Tung or Patapim?", "TUNG TUNG OR\nPATAPIM?", bg="party", ground="purple"),
   ], pron={"Sahur": "Sa-hoor", "Patapim": "Pata-pim"}, **ML)

LMC = "Clip: Grand Theft Auto V, Rockstar Games"
ep(179, "lamar-roasts-franklin", "Why Lamar Roasting Franklin Became a Meme", 0, "#76ff03", PUCK, 1.04,
   {"font": MF + "Bangers-Regular.ttf", "size": 124, "mode": "word", "fill": "#ffffff", "hi": "#ffffff", "cy": 1470},
   [L("This GTA 5 cutscene became one of the biggest gaming memes ever.",
      CLIP("ml20-lm-a.mp4", "LAMAR ROASTS\nFRANKLIN", "GTA 5", 0, LMC, bs=140)),
    L("In it, Lamar roasts Franklin's haircut, nonstop, while Franklin just takes it.",
      CLIP("ml20-lm-b.mp4", "THE HAIRCUT", "ROASTED", 0, LMC, bs=180)),
    L("GTA 5 came out in 2013, but the meme only blew up in May 2020, with a remix using SpongeBob's text to speech voice.",
      S("MAY 2020", "THE SPONGEBOB REMIX", "gold", "grass", rays="#ffffff", bs=200, ic=[{"n": "tv", "x": 860, "y": 820, "s": 150, "a": "pulse"}], av=[av([0.0, 0.8], "jump", "a")])),
    L("Then the real voice actors, Slink Johnson and Shawn Fonteno, acted it out in real life.",
      CLIP("ml20-lm-a.mp4", "THE REAL\nACTORS", "SLINK + SHAWN", 6.0, LMC, bs=150)),
    L("And Rockstar even added a new roast to GTA Online.",
      S("ROAST 2.0", "GTA ONLINE", "night", "stone", bs=200, fx=["sparkle"], ic=[{"n": "fire", "x": 860, "y": 820, "s": 150, "a": "shake"}], av=[av([-1.2, 0.6], "cheer", "a"), av([1.2, 0.6], "cheer", "b")])),
    L("Next: Modern Warfare 4 is finally out. Subscribe so you don't miss it.", S("NEXT: MODERN\nWARFARE 4", "SUBSCRIBE SO YOU DON'T MISS IT", "night", "stone", bs=124, ss=40, ic=[{"n": "gun", "x": 860, "y": 820, "s": 150, "a": "pulse"}], av=[av([0.0, 0.8], "run", "a")])),
    end("Will Lamar be in GTA 6?", "LAMAR IN\nGTA 6?", bg="sunset", ground="grass"),
   ], pron={"Fonteno": "Fon-tay-no"}, **ML)

# ============================================================ TRENDING
MWC = "Clip: Call of Duty: Modern Warfare 4 trailer, Activision"
ep(180, "modern-warfare-4-out", "Modern Warfare 4 Is Out Now", 0, "#ffab00", FENRIR, 1.06,
   {"font": MF + "BlackOpsOne-Regular.ttf", "size": 92, "fill": "#ffffff", "hi": "#ffd740", "stroke": 8},
   [L("Call of Duty Modern Warfare 4 is finally out.",
      CLIP("tr20-mw-a.mp4", "MODERN\nWARFARE 4", "OUT NOW", 0, MWC, bs=170)),
    L("It launched on October 23rd, made by Infinity Ward.",
      CLIP("tr20-mw-b.mp4", "OCTOBER 23", "INFINITY WARD", 0, MWC, bs=170)),
    L("The campaign is about North Korea invading South Korea, with Price, Ghost and Gaz, and Mads Mikkelsen as a villain called the Archer.",
      CLIP("tr20-mw-c.mp4", "KOREA", "PRICE, GHOST, GAZ", 0, MWC, bs=200)),
    L("It's the first Call of Duty on Nintendo Switch 2 on day one.",
      S("SWITCH 2", "DAY ONE", "red", "dark", bc="#ffffff", bs=200, fx=["red"], ic=[{"n": "controller", "x": 860, "y": 820, "s": 150, "a": "float"}], av=[av([0.0, 0.8], "cheer", "a")])),
    L("DMZ is back too. But it won't come to Game Pass for at least a year.",
      CLIP("tr20-mw-b.mp4", "DMZ IS BACK", "NO GAME PASS YET", 6.0, MWC, bs=150)),
    tease("Next: the Roblox shooter with 19 billion visits.", "NEXT: RIVALS", "pop20-rivals-a.jpg", RBX("RIVALS")),
    end("Are you playing it?", "PLAYING IT?", bg="night", ground="stone"),
   ], pron={"Mikkelsen": "Mick-el-sen", "DMZ": "D M Z", "Gaz": "Gaz"}, edition="CALL OF DUTY", mood="spooky")

# ================================================================== write
for e in RB:
    e = dict(preset="roblox", hdr="tag", **e)
    if not e["target"]:
        e["target"] = round(sum(len(l.get("say", l["t"]).split()) for l in e["lines"]) / 2.72)
    for l in e["lines"]:
        sc = l["sc"]
        for m in [sc.get("photo"), sc.get("full")]:
            if m:
                f = m.get("img") or m.get("clip")
                if not os.path.exists(os.path.join(ROOT, "episodes", "assets", f)):
                    print("  MISSING", e["slug"], f)
    json.dump(e, open(os.path.join(ROOT, "episodes", "roblox", e["slug"] + ".json"), "w"), indent=1, ensure_ascii=False)
    print(e["slug"], len(e["lines"]), "lines", sum(len(l.get("say", l["t"]).split()) for l in e["lines"]), "words", "target", e["target"])
