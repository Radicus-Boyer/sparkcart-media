"""Writes batch 22 (facts checked 2026-10-27): 4 Roblox + 4 GD + 1 meme + 1 Tarkov = #191-200.
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
HLC = "Clip: The Hollow (Roblox gameplay)"
clip("rb22-hl-a.mp4", "https://www.youtube.com/watch?v=iTjpQhV4_0U", "*3:00-3:20", backup=["https://www.youtube.com/watch?v=aDt4v0QR_wI"])
clip("rb22-hl-b.mp4", "https://www.youtube.com/watch?v=m9DRQTdF248", "*1:30-1:50", backup=["https://www.youtube.com/watch?v=Xhv5PySNsZo"])
ep(191, "the-hollow-roblox", "The Hollow Is Roblox's Own Horror Event", SARAH, "#ff6d00",
   {"font": MF + "BlackOpsOne-Regular.ttf", "size": 92, "fill": "#ffffff", "hi": "#ffab40", "stroke": 8},
   [L("Roblox itself made this horror game, and it's asking you not to go in.",
      CLIP("rb22-hl-a.mp4", "THE HOLLOW", "BY ROBLOX ITSELF", 0, HLC, bs=180)),
    L("The Hollow opened on October 22nd, made by Roblox Presents.",
      CLIP("rb22-hl-b.mp4", "OCTOBER 22", "ROBLOX PRESENTS", 0, HLC, bs=170)),
    L("Every night, it drops you somewhere new, and some creators are going in live.",
      S("A NEW PLACE\nEVERY NIGHT", "CREATORS GO IN LIVE", "night", "dark", bs=140, fx=["fireflies"], ic=ic("eye", "pulse"), av=[av([0.0, 0.8], "walk", "a")])),
    L("Quests here and in other Roblox games give you free avatar items.",
      CLIP("rb22-hl-a.mp4", "FREE ITEMS", "EVENT QUESTS", 6.0, HLC, bs=180)),
    L("It already has almost 97 million visits, and it ends on Halloween.",
      COUNT(96941754, "VISITS", bg="night", ground="dark", fx="sparkle")),
    end("Will you go in?", "WILL YOU\nGO IN?", bg="night", ground="dark"),
   ], mood="spooky")

ADC = "Clip: Anime Dice (Roblox gameplay)"
clip("rb22-ad-a.mp4", "https://www.youtube.com/watch?v=GDhRkgOBJkk", "*4:00-4:20", backup=["https://www.youtube.com/watch?v=3Otkov2a7cU"])
clip("rb22-ad-b.mp4", "https://www.youtube.com/watch?v=Rb6VIV7S5fY", "*2:00-2:20", backup=["https://www.youtube.com/watch?v=azzcvjCZ0CI"])
ep(192, "anime-dice-roblox", "Anime Dice Has 141 Million Visits in 2 Months", PUCK, "#e040fb",
   {"font": MF + "Bangers-Regular.ttf", "size": 120, "mode": "word", "fill": "#ffffff", "hi": "#ea80fc", "cy": 1470},
   [L("This Roblox game is only 2 months old, and it already has 141 million visits.",
      CLIP("rb22-ad-a.mp4", "ANIME DICE", "141 MILLION VISITS", 0, ADC, bs=180)),
    L("Anime Dice came out in August 2026, made by More and More Games.",
      CLIP("rb22-ad-b.mp4", "AUGUST 2026", "MORE & MORE GAMES", 0, ADC, bs=170)),
    L("You roll dice to reveal anime characters, then upgrade your dice for more luck.",
      S("ROLL THE\nDICE", "REVEAL ANIME HEROES", "party", "purple", bs=170, fx=["confetti"], ic=ic("star", "spin"), av=[av([0.0, 0.8], "jump", "a")])),
    L("You build the strongest team, and you even make money while you're offline.",
      CLIP("rb22-ad-a.mp4", "BEST TEAM", "MONEY WHILE OFFLINE", 6.0, ADC, bs=180)),
    L("And it has 733,000 likes, and only about 6,800 dislikes.",
      COUNT(733236, "LIKES", bg="party", ground="purple", fx="confetti")),
    end("What's your best unit?", "YOUR BEST\nUNIT?", bg="party", ground="purple"),
   ])

BSC = "Clip: Break and Steal an Egg (Roblox gameplay)"
clip("rb22-be-a.mp4", "https://www.youtube.com/watch?v=MtNnuhxs5jk", "*5:00-5:20", backup=["https://www.youtube.com/watch?v=Y0o2gqsKzK8"])
clip("rb22-be-b.mp4", "https://www.youtube.com/watch?v=v57NpCawzVU", "*3:00-3:20", backup=["https://www.youtube.com/watch?v=Y0o2gqsKzK8"])
ep(193, "break-and-steal-an-egg", "Break and Steal an Egg Has 270 Million Visits", LIAM, "#ffd600",
   {"font": MF + "RussoOne-Regular.ttf", "size": 92, "hi": "#ffff00", "stroke": 8},
   [L("Steal An Egg is the number 1 game on Roblox. So someone made Break and Steal an Egg.",
      CLIP("rb22-be-a.mp4", "BREAK AND\nSTEAL AN EGG", "INSPIRED BY THE #1 GAME", 0, BSC, bs=130)),
    L("It came out on September 5th, made by ILGames.",
      CLIP("rb22-be-b.mp4", "SEPTEMBER 5", "BY ILGAMES", 0, BSC, bs=180)),
    L("You smash eggs with a pickaxe, hatch rare animals, then steal them and escape the guards.",
      S("SMASH +\nSTEAL", "ESCAPE THE GUARDS", "day", "grass", bs=170, ic=ic("money", "shake"), av=[av([-1.2, 0.6], "run", "a"), av([1.2, 0.6], "run", "b")])),
    L("Then you upgrade your speed and your pickaxe to grab rarer eggs.",
      CLIP("rb22-be-a.mp4", "UPGRADE", "SPEED + PICKAXE", 6.0, BSC, bs=180)),
    L("In 7 weeks it got 270 million visits.",
      COUNT(270076427, "VISITS IN 7 WEEKS", bg="gold", ground="grass", fx="confetti", bs=140)),
    end("Steal An Egg or Break and Steal?", "WHICH EGG\nGAME?", bg="gold", ground="grass"),
   ], pron={"ILGames": "I L Games"})

HVC = "Clip: Huss Valley (Roblox gameplay)"
clip("rb22-hv-a.mp4", "https://www.youtube.com/watch?v=OGxOmFC4Wyw", "*4:00-4:20", backup=["https://www.youtube.com/watch?v=xgvSsNX-dZI"])
clip("rb22-hv-b.mp4", "https://www.youtube.com/watch?v=iHM5GpAI-tc", "*2:00-2:20", backup=["https://www.youtube.com/watch?v=1zlsh6nTqkQ"])
ep(194, "huss-valley-roblox", "Huss Valley Has 205 Million Visits", FENRIR, "#00e676",
   {"font": MF + "Anton-Regular.ttf", "size": 104, "hi": "#69f0ae", "stroke": 8},
   [L("One chaser. Everyone else runs. Get caught, and you become a chaser too.",
      CLIP("rb22-hv-a.mp4", "HUSS VALLEY", "RUN!", 0, HVC, bs=180)),
    L("Huss Valley came out on Roblox at the end of August 2026.",
      CLIP("rb22-hv-b.mp4", "AUGUST 2026", "HUSS VALLEY", 0, HVC, bs=170)),
    L("Every round, you have to make it across before the chasers get you. The last one standing wins.",
      S("LAST ONE\nSTANDING", "MAKE IT ACROSS", "day", "grass", bs=150, ic=ic("trophy", "float"), av=[av([-1.4, 0.6], "run", "a"), av([0.0, 0.8], "run", "b"), av([1.4, 0.6], "run", "c")])),
    L("For Halloween, it added a woods map with knives and new abilities.",
      CLIP("rb22-hv-b.mp4", "HALLOWEEN\nWOODS", "KNIVES + ABILITIES", 6.0, HVC, bs=150)),
    L("In 2 months, it reached 205 million visits.",
      COUNT(205743618, "VISITS", bg="day", ground="grass", fx="confetti")),
    end("Runner or chaser?", "RUNNER OR\nCHASER?", bg="day", ground="grass"),
   ], pron={"Huss": "Huss"})

# ============================================================ GEOMETRY DASH (stage "gd": real player icons, no Roblox avatars)
SCC = "Clips: Silent clubstep verified by paqoe; Vision's 100% (YouTube)"
clip("gd22-sc-a.mp4", "https://www.youtube.com/watch?v=GR4OMkS3SN8", "*0:45-1:00", cut=0)
clip("gd22-sc-b.mp4", "https://www.youtube.com/watch?v=EOr8hDyXDvQ", "*1:20-1:40", backup=["https://www.youtube.com/watch?v=GR4OMkS3SN8"])
ep(195, "silent-clubstep-race", "The Race to Beat the Impossible Level", MIKE, "#2979ff",
   {"font": MF + "SairaStencilOne-Regular.ttf", "size": 96, "fill": "#ffffff", "hi": "#82b1ff", "stroke": 8},
   [L("For years, everyone said this Geometry Dash level was impossible.",
      CLIP("gd22-sc-a.mp4", "SILENT\nCLUBSTEP", "\"IMPOSSIBLE\"", 0, SCC, bs=150)),
    L("Then in 2020, its creator fixed it with icedcave, and the best players raced to verify it first.",
      S("THE RACE", "WHO VERIFIES IT FIRST?", "night", "stone", bs=200, mode="cube", player="paqoe")),
    L("paqoe won. She verified it in July 2022, after about 138,000 attempts.",
      COUNT(138000, "PAQOE'S ATTEMPTS", fmt="~{:,.0f}", bg="night", ground="stone", mode="ship", player="paqoe")),
    L("Her premiere had 3,700 people watching live.",
      CLIP("gd22-sc-a.mp4", "3,700\nWATCHING", "THE PREMIERE", 6.0, SCC, bs=150)),
    L("Vision lost the race, but kept going, and beat it after 821,027 attempts.",
      CLIP("gd22-sc-b.mp4", "VISION", "821,027 ATTEMPTS", 0, SCC, bs=180)),
    end("Could you beat Silent Clubstep?", "COULD YOU\nBEAT IT?", bg="night", ground="stone"),
   ], pron=dict(GD_PRON, paqoe="pa-co", icedcave="iced cave", Clubstep="Club step"), gd_player="paqoe", **GDE)

CTC = "Clips: Cataclysm by Ggb0y; Riot's stream (YouTube)"
clip("gd22-ct-a.mp4", "https://www.youtube.com/watch?v=J90L73YOR3k", "*0:20-0:40", backup=["https://www.youtube.com/watch?v=gFU4ln-hcJY"])
clip("gd22-ct-b.mp4", "https://www.youtube.com/watch?v=2Q0CYSDFpKk", "*2:00-2:20", backup=["https://www.youtube.com/watch?v=xBdSwk-leAw"])
ep(196, "cataclysm-hacked", "Cataclysm Was Verified With Hacks", FENRIR, "#d50000",
   {"font": MF + "BlackOpsOne-Regular.ttf", "size": 92, "fill": "#ffffff", "hi": "#ff5252", "stroke": 8},
   [L("The most famous level in Geometry Dash was first beaten with hacks.",
      CLIP("gd22-ct-a.mp4", "CATACLYSM", "BEATEN WITH HACKS", 0, CTC, bs=180)),
    L("Ggb0y spent around 80,000 attempts on Cataclysm, couldn't beat it, and hack-verified it in January 2015.",
      COUNT(80088, "GGB0Y'S ATTEMPTS", bg="red", ground="dark", fx="red")),
    L("Cyclic was called the first real victor, until he admitted he hacked too.",
      S("CYCLIC\nCONFESSED", "THE FAKE FIRST VICTOR", "red", "dark", bc="#ffffff", bs=150, fx=["red"], ic=ic("alarm", "shake"), mode="wave", player="Cyclic")),
    L("So Giron became the first legit victor, in May 2015. Then Riot verified the 2.0 version on stream.",
      CLIP("gd22-ct-b.mp4", "RIOT", "VERIFIED ON STREAM", 0, CTC, bs=180)),
    L("It's still the second most liked Extreme Demon in the game.",
      CLIP("gd22-ct-a.mp4", "#2 MOST\nLIKED", "EXTREME DEMON", 6.0, CTC, bs=150)),
    end("Could you beat Cataclysm?", "COULD YOU\nBEAT IT?", bg="red", ground="dark"),
   ], pron=dict(GD_PRON, Ggb0y="G G boy", Giron="Hee-ron", Cataclysm="Cat-a-clism"), gd_player="Riot", **GDE)

SKC = "Clips: Sakupen Circles verified by Diamond; Trick's 100% (YouTube)"
clip("gd22-sk-a.mp4", "https://www.youtube.com/watch?v=ofG2mJi9kEA", "*0:20-0:40", backup=["https://www.youtube.com/watch?v=b66_Oe4Xo1w"])
clip("gd22-sk-b.mp4", "https://www.youtube.com/watch?v=zCJrhYTjqMo", "*0:30-0:50", backup=["https://www.youtube.com/watch?v=b66_Oe4Xo1w"])
ep(197, "sakupen-circles-1107185", "One Player Took 1,107,185 Attempts on Sakupen Circles", HEART, "#ff1744",
   {"font": MF + "RussoOne-Regular.ttf", "size": 92, "hi": "#ff8a80", "stroke": 8},
   [L("One player spent over a million attempts on this 1 minute level.",
      CLIP("gd22-sk-a.mp4", "SAKUPEN\nCIRCLES", "1 MILLION+ ATTEMPTS", 0, SKC, bs=150)),
    L("Sakupen Circles was verified by Diamond, in December 2021.",
      CLIP("gd22-sk-b.mp4", "DIAMOND", "DECEMBER 2021", 0, SKC, bs=180)),
    L("It was placed number 1 on the Demonlist, and it's still the hardest level under a minute long.",
      S("UNDER\n1 MINUTE", "THE HARDEST ONE", "red", "dark", bc="#ffffff", bs=170, fx=["red"], mode="wave", player="Diamond")),
    L("Most players need tens of thousands of attempts. But ezzzzka needed 1,107,185.",
      COUNT(1107185, "EZZZZKA'S ATTEMPTS", bg="red", ground="dark", fx="red", bs=150, mode="cube", player="ezzzzka")),
    L("That's more attempts than anyone has spent beating any level.",
      CLIP("gd22-sk-a.mp4", "A RECORD", "MOST ATTEMPTS EVER", 6.0, SKC, bs=180)),
    end("How many attempts would you need?", "HOW MANY\nATTEMPTS?", bg="red", ground="dark"),
   ], pron=dict(GD_PRON, Sakupen="Sa-koo-pen", ezzzzka="ez-ka"), gd_player="Diamond", **GDE)

SHC = "Clips: Sakupen Hell by Noobas, verified by TrusTa; Riot (YouTube)"
clip("gd22-sh-a.mp4", "https://www.youtube.com/watch?v=CtL_ayfNKPI", "*0:08-0:23", cut=0)
clip("gd22-sh-b.mp4", "https://www.youtube.com/watch?v=miOMwNG3HKs", "*0:15-0:35", backup=["https://www.youtube.com/watch?v=CtL_ayfNKPI"])
ep(198, "sakupen-hell-challenge", "Sakupen Hell Was Made to Beat Riot and Cyclic", LIAM, "#ff3d00",
   {"font": MF + "Anton-Regular.ttf", "size": 104, "hi": "#ff9e80", "stroke": 8},
   [L("This level was made as a challenge to the two best players in the game.",
      CLIP("gd22-sh-a.mp4", "SAKUPEN\nHELL", "A CHALLENGE", 0, SHC, bs=160)),
    L("Noobas made Sakupen Hell to challenge Riot and Cyclic, and openly hack-verified it in June 2015.",
      S("VS RIOT\n& CYCLIC", "OPENLY HACK-VERIFIED", "red", "dark", bc="#ffffff", bs=150, fx=["red"], mode="cube", player="Riot")),
    L("Then he deleted it, to start over as a legit player.",
      S("DELETED", "A FRESH START", "night", "stone", bs=200, mode="ship", player="Noobas")),
    L("Over a year later, TrusTa verified it for real, on livestream, in August 2016.",
      CLIP("gd22-sh-b.mp4", "TRUSTA", "AUGUST 2016", 0, SHC, bs=180)),
    L("It became the hardest level in the game, passing Bloodbath.",
      CLIP("gd22-sh-a.mp4", "NEW #1", "PASSED BLOODBATH", 6.0, SHC, bs=180)),
    end("Riot or Cyclic?", "RIOT OR\nCYCLIC?", bg="red", ground="dark"),
   ], pron=dict(GD_PRON, Sakupen="Sa-koo-pen", Noobas="Noo-bas", TrusTa="Trust-a"), gd_player="TrusTa", **GDE)

# ============================================================ MEME LORE (stage "meme")
WIC = "Clips: TikTok (@trevorlarcom, @290dan, @alexanderthegreat025)"
clip("ml22-wi-a.mp4", "https://www.tiktok.com/@trevorlarcom/video/7696693848453500173", None, 0,
     backup=["https://www.tiktok.com/@hyperstrides/video/7701058477937986838"])
clip("ml22-wi-b.mp4", "https://www.tiktok.com/@290dan/video/7699669699440725269", None, 0,
     backup=["https://www.tiktok.com/@timothy.haireth/video/7700026895466843406"])
clip("ml22-wi-c.mp4", "https://www.tiktok.com/@alexanderthegreat025/video/7700360138200321287", None, 0,
     backup=["https://www.tiktok.com/@zenzennyyyyz/video/7699897420347378952"])
ep(199, "and-then-i-walk-in", "Where And Then I Walk In Came From", PUCK, "#ffd740",
   {"font": MF + "Bangers-Regular.ttf", "size": 124, "mode": "word", "fill": "#ffffff", "hi": "#ffffff", "cy": 1470},
   [L("And then I walk in. Why is this guy in every comment section?",
      CLIP("ml22-wi-a.mp4", "AND THEN\nI WALK IN", "WHO IS HE?", 0, WIC, bs=150)),
    L("The meme is one photo of a guy posing like a model, with the words, and then I walk in.",
      S("ONE PHOTO", "\"AND THEN I WALK IN\"", "party", "purple", bs=200)),
    L("The joke is, no matter how good a post is, he walks in and steals the spotlight.",
      CLIP("ml22-wi-b.mp4", "HE STEALS\nTHE SHOW", "AURA", 0, WIC, bs=150)),
    L("TikTokers traced it to a creator called Model Alexander, and one origin video got 1.9 million views.",
      CLIP("ml22-wi-c.mp4", "MODEL\nALEXANDER", "THE ORIGIN", 0, WIC, bs=150)),
    L("Now he's even walking into Roblox comment sections.",
      COUNT(1.9, "VIEWS ON ONE ORIGIN VIDEO", fmt="{:.1f}M", bg="party", ground="purple", fx="confetti", bs=220)),
    end("Who walked in better?", "WHO WALKED\nIN BETTER?", bg="party", ground="purple"),
   ], prop_clip="ml22-wi-a.mp4", edition="MEME LORE")

# ============================================================ TRENDING (stage "news")
TKC = "Clips: Escape from Tarkov, Battlestate Games; LVNDMARK (YouTube)"
clip("tr22-tk-a.mp4", "https://www.youtube.com/watch?v=v7Gjb69XcP4", "*10:00-10:20", backup=["https://www.youtube.com/watch?v=dzD7nTUUyp8"])
clip("tr22-tk-b.mp4", "https://www.youtube.com/watch?v=OKh9HaTEUfk", "*0:40-1:00", backup=["https://www.youtube.com/watch?v=Dd3MSNfRZ68"])
ep(200, "tarkov-labs-scourge", "Tarkov's New Labs Boss Had Aimbot Guards", MIKE, "#ffab00",
   {"font": MF + "BlackOpsOne-Regular.ttf", "size": 92, "fill": "#ffffff", "hi": "#ffd740", "stroke": 8},
   [L("Escape from Tarkov just put a new boss in Labs, and players said his guards had aimbot.",
      CLIP("tr22-tk-b.mp4", "SCOURGE", "THE NEW LABS BOSS", 0, TKC, bs=180)),
    L("The Scourge Incursion started October 16th. Scourge led 4 guards, said to be Arena champions.",
      S("4 ARENA\nCHAMPIONS", "OCTOBER 16", "red", "dark", bc="#ffffff", bs=150, fx=["red"], ic=ic("crosshair", "pulse"))),
    L("They had tier 5 armor, spawned every raid, and pushed and flanked like real players.",
      CLIP("tr22-tk-b.mp4", "TIER 5\nARMOR", "100% SPAWN", 6.0, TKC, bs=150)),
    L("Four days later, Battlestate cut their health and their vision, and the event was extended to October 26th.",
      S("NERFED", "EXTENDED TO OCT 26", "night", "stone", bs=200, ic=ic("shield", "float"))),
    L("And now Nikita is teasing a zombie event in Labs, saying it's pretty big, with a surprise.",
      CLIP("tr22-tk-a.mp4", "ZOMBIE\nLABS?", "\"PRETTY BIG\"", 6.0, TKC, bs=150)),
    end("Did you fight Scourge?", "DID YOU FIGHT\nSCOURGE?", bg="night", ground="stone"),
   ], pron={"Nikita": "Ni-kee-ta", "Battlestate": "Battle state"}, prop_clip="tr22-tk-b.mp4",
   ticker="TARKOV: NEW LABS BOSS SCOURGE - ZOMBIE LABS EVENT TEASED", edition="ESCAPE FROM TARKOV", mood="spooky")

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
manifest = {"batch": 22, "note": "4 Roblox, 4 GD, and then I walk in, Tarkov Labs (Oct 27)", "posting": "batch-22/posting.txt",
            "episodes": paths, "clips": CLIPS}
json.dump(manifest, open(os.path.join(ROOT, "batches", "batch-22.json"), "w"), indent=1)
print(len(CLIPS), "clips")
