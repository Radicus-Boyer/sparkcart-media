"""Writes batch 25 (facts checked 2026-10-31): 3 GD + 3 Roblox + Tarkov zombies + trending meme + 2 lore = #221-230.

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


GD_PRON.update({"Axinity": "Ax-in-ity", "declan": "deck-lan", "BOOBAWAMBA": "Boo-ba-wam-ba", "EastShark": "East Shark",
                "akunakun": "a-koo-na-koon", "Zoink": "Zoynk", "SerVax": "Sir Vax", "MinAY": "Min A Y",
                "nickname": "nickname", "Demonlist": "Demon list"})

# ============================================================ GEOMETRY DASH (pointercrate + GD wiki, Oct 31)
ALC = "Clips: Axinity; Newly Rated Extremes (YouTube)"
clip("gd25-al-a.mp4", "https://www.youtube.com/watch?v=Uue4ZRhVf-I", "*1:33-1:53", cut=0)
clip("gd25-al-b.mp4", "https://www.youtube.com/watch?v=Uue4ZRhVf-I", "*0:50-1:10", cut=0)
clip("gd25-al-c.mp4", "https://www.youtube.com/watch?v=Ii25Ypw_Cjs", "*0:14-0:34", cut=0)
clip("gd25-al-d.mp4", "https://www.youtube.com/watch?v=_M3D5xP0w7c", "*0:50-1:10", cut=0)
ep(221, "antarctic-lights-381058", "Axinity Took 381,058 Attempts on a 1 Minute Level", FENRIR, "#40c4ff",
   {"font": MF + "Anton-Regular.ttf", "size": 104, "hi": "#80d8ff", "stroke": 8},
   [L("This level is only one minute long. It took 381,058 attempts.",
      CLIP("gd25-al-a.mp4", "ANTARCTIC\nLIGHTS", "VERIFIED", 0, ALC)),
    L("Antarctic Lights is a harder remake of Arctic Lights, with wave gaps so tight they're measured in frames.",
      CLIP("gd25-al-c.mp4", "FRAME\nPERFECT", "ARCTIC LIGHTS, BUT HARDER", 0, ALC, ss=50)),
    L("Axinity started posting progress in 2024. Two years later, he died at 92 percent.",
      CLIP("gd25-al-d.mp4", "92%", "SO CLOSE", 0, ALC, bs=200)),
    L("In July, he finally beat it, after 381,058 attempts. It went straight into the top 10.",
      CCOUNT("gd25-al-b.mp4", 0, ALC, 381058, "ATTEMPTS")),
    ask("Would you spend 2 years on one minute?", "2 YEARS FOR\n1 MINUTE?", "gd25-al-a.mp4", ALC),
    subline("gd25-al-a.mp4", ALC, 3.0),
   ], pron=dict(GD_PRON), gd_player="Axinity", **GDE)

BWC = "Clips: EastShark1; Zoink (YouTube)"
clip("gd25-bw-a.mp4", "https://www.youtube.com/watch?v=20fYiqLAo_E", "*2:38-2:58", cut=0)
clip("gd25-bw-b.mp4", "https://www.youtube.com/watch?v=20fYiqLAo_E", "*1:58-2:18", cut=0)
clip("gd25-bw-c.mp4", "https://www.youtube.com/watch?v=DXV7CVkos7I", "*34:44-35:04", cut=0)
ep(222, "boobawamba-175282", "EastShark Took 175,282 Attempts on a Level You Cant See", LIAM, "#76ff03",
   {"font": MF + "RussoOne-Regular.ttf", "size": 92, "hi": "#ccff90", "stroke": 8},
   [L("In this level, you can barely see where you're going.",
      CLIP("gd25-bw-a.mp4", "BOOBAWAMBA", "VERIFIED", 0, BWC)),
    L("BOOBAWAMBA is all green and grey, so you can't tell what's coming. You have to memorize it.",
      CLIP("gd25-bw-b.mp4", "MEMORY\nLEVEL", "YOU CAN'T SEE IT", 0, BWC)),
    L("EastShark verified it in October 2024, after 175,282 attempts.",
      CCOUNT("gd25-bw-b.mp4", 6.0, BWC, 175282, "ATTEMPTS")),
    L("It's still the hardest memory level in the game. Then in April, Zoink beat it, and said it went so fast it was kinda crazy.",
      CLIP("gd25-bw-c.mp4", "ZOINK", "\"KINDA CRAZY\"", 0, BWC)),
    ask("Could you beat a level you can't see?", "COULD YOU\nSEE IT?", "gd25-bw-a.mp4", BWC),
    subline("gd25-bw-a.mp4", BWC, 3.0),
   ], pron=dict(GD_PRON), gd_player="EastShark", **GDE)

GBC = "Clips: nickname; Neiro; Geometry Dash news (YouTube)"
clip("gd25-gb-a.mp4", "https://www.youtube.com/watch?v=JG-qcvVkZFw", "*2:50-3:10", cut=0)
clip("gd25-gb-b.mp4", "https://www.youtube.com/watch?v=zfTqKYeqhTo", "*0:50-1:10", cut=0)
clip("gd25-gb-c.mp4", "https://www.youtube.com/watch?v=GTt1PNe4xho", "*0:20-0:40", cut=0)
clip("gd25-gb-d.mp4", "https://www.youtube.com/watch?v=B7vl5z-jqtE", "*1:20-1:40", cut=0)
ep(223, "green-bullet-3-verifiers", "Two Verifiers Quit Green Bullet Then nickname Beat It", MIKE, "#00e676",
   {"font": MF + "BlackOpsOne-Regular.ttf", "size": 92, "fill": "#ffffff", "hi": "#69f0ae", "stroke": 8},
   [L("Two players gave up on this level. The third one beat it.",
      CLIP("gd25-gb-a.mp4", "GREEN\nBULLET", "VERIFIED", 0, GBC)),
    L("Green Bullet is a giant collab by Cherry Team. Its first verifier, SerVax, stepped down. The next one refused to verify it.",
      CLIP("gd25-gb-c.mp4", "2 VERIFIERS\nQUIT", "THE DRAMA", 0, GBC, bs=130)),
    L("So nickname took over. After nearly a year, he died at 89 percent.",
      CLIP("gd25-gb-d.mp4", "89%", "NICKNAME", 0, GBC, bs=200)),
    L("In June, he finally verified it, after about 105,000 attempts. It's now a top 10 level.",
      CCOUNT("gd25-gb-b.mp4", 0, GBC, 105000, "ATTEMPTS", fmt="~{:,.0f}")),
    ask("Would you have quit too?", "WOULD YOU\nQUIT?", "gd25-gb-a.mp4", GBC),
    subline("gd25-gb-a.mp4", GBC, 3.0),
   ], pron=dict(GD_PRON), gd_player="nickname", **GDE)

# ============================================================ ROBLOX (live numbers from Roblox, Oct 31)
SAC = "Clips: +1 Spider Arm (Roblox gameplay, YouTube)"
clip("rb25-sa-a.mp4", "https://www.youtube.com/watch?v=CfjIxRi4qU4", "*1:00-1:20", cut=0, backup=["https://www.youtube.com/watch?v=XkWXiurjbeo"])
clip("rb25-sa-b.mp4", "https://www.youtube.com/watch?v=CfjIxRi4qU4", "*5:00-5:20", cut=0)
clip("rb25-sa-c.mp4", "https://www.youtube.com/watch?v=XkWXiurjbeo", "*2:00-2:20", cut=0, backup=["https://www.youtube.com/watch?v=UkC045Az8Q4"])
ep(224, "plus-1-spider-arm", "In This Roblox Game You Ride a Giant Spider Arm", PUCK, "#ff6d00",
   {"font": MF + "Bangers-Regular.ttf", "size": 120, "mode": "word", "fill": "#ffffff", "hi": "#ffab40", "cy": 1470},
   [L("In this Roblox game, a giant spider arm climbs for you.",
      CLIP("rb25-sa-a.mp4", "+1 SPIDER\nARM", "CLIMB ANYTHING", 0, SAC, bs=130)),
    L("You ride a mechanical spider that walks, climbs walls, and hangs under ceilings.",
      CLIP("rb25-sa-b.mp4", "CLIMB\nWALLS", "HANG FROM CEILINGS", 0, SAC)),
    L("Train to get plus one arm. More arms means more speed and more grip. But watch your grip, or you fall.",
      CLIP("rb25-sa-c.mp4", "+1 ARM", "MORE SPEED, MORE GRIP", 0, SAC, bs=180)),
    L("It's less than 2 weeks old, with over 8 million visits.",
      CCOUNT("rb25-sa-b.mp4", 6.0, SAC, 8269265, "VISITS", bs=140)),
    ask("How many arms would you get?", "HOW MANY\nARMS?", "rb25-sa-a.mp4", SAC),
    subline("rb25-sa-a.mp4", SAC, 3.0),
   ])

SCC = "Clips: Say Cheese! (Roblox gameplay: Roblox Master Gamer; Zac Worthy, YouTube)"
clip("rb25-sc-a.mp4", "https://www.youtube.com/watch?v=kyWrM9Bn1DA", "*2:00-2:20", cut=0, backup=["https://www.youtube.com/watch?v=--6IOnM6qH4"])
clip("rb25-sc-b.mp4", "https://www.youtube.com/watch?v=kyWrM9Bn1DA", "*10:00-10:20", cut=0)
clip("rb25-sc-c.mp4", "https://www.youtube.com/watch?v=--6IOnM6qH4", "*5:00-5:20", cut=0)
ep(225, "say-cheese", "In Say Cheese Your Photos Start a Riot", SARAH, "#e040fb",
   {"font": MF + "RussoOne-Regular.ttf", "size": 92, "hi": "#ea80fc", "stroke": 8},
   [L("In this Roblox game, your photos can start a riot.",
      CLIP("rb25-sc-a.mp4", "SAY\nCHEESE!", "YOU'RE ON CAMERA", 0, SCC)),
    L("You're a journalist hired by Big Media. Your job is to spread panic, so everyone keeps watching the news.",
      CLIP("rb25-sc-b.mp4", "BIG MEDIA", "SPREAD PANIC", 0, SCC)),
    L("It's based on a 2016 browser game by Nicky Case. Will you wreck the park, or try to bring hope? There are 12 endings.",
      CLIP("rb25-sc-c.mp4", "12\nENDINGS", "THE CHOICE IS YOURS", 0, SCC, bs=170)),
    L("It's less than 2 weeks old, with over 5 million visits.",
      CCOUNT("rb25-sc-a.mp4", 6.0, SCC, 5112560, "VISITS", bs=140)),
    ask("Would you spread panic, or hope?", "PANIC OR\nHOPE?", "rb25-sc-a.mp4", SCC),
    subline("rb25-sc-a.mp4", SCC, 3.0),
   ], pron={"Nicky": "Nicky"}, mood="spooky")

BEC = "Clips: Bug Evolution (Roblox gameplay: Bax; JelloYT, YouTube)"
clip("rb25-be-a.mp4", "https://www.youtube.com/watch?v=NKPQejjYbkQ", "*3:00-3:20", cut=0)
clip("rb25-be-b.mp4", "https://www.youtube.com/watch?v=NKPQejjYbkQ", "*12:00-12:20", cut=0)
clip("rb25-be-c.mp4", "https://www.youtube.com/watch?v=9pgArp2WrNI", "*5:00-5:20", cut=0)
ep(226, "bug-evolution", "In Bug Evolution You Start as a Tiny Spider", HEART, "#8bc34a",
   {"font": MF + "Bangers-Regular.ttf", "size": 120, "mode": "word", "fill": "#ffffff", "hi": "#ccff90", "cy": 1470},
   [L("In this Roblox game, you start as a tiny spider.",
      CLIP("rb25-be-a.mp4", "BUG\nEVOLUTION", "START TINY", 0, BEC)),
    L("Eat, grow, and evolve into over 30 insects. Flies, moths, grasshoppers, tarantulas.",
      CLIP("rb25-be-c.mp4", "30+\nINSECTS", "EAT AND EVOLVE", 0, BEC)),
    L("And at the top, giant prehistoric beasts.",
      CLIP("rb25-be-b.mp4", "PREHISTORIC\nBEASTS", "THE FINAL FORM", 0, BEC, bs=120)),
    L("It came out this month, and it already has over 6 million visits.",
      CCOUNT("rb25-be-b.mp4", 6.0, BEC, 6825950, "VISITS", bs=140)),
    ask("What bug would you evolve into?", "WHAT BUG\nWOULD YOU BE?", "rb25-be-a.mp4", BEC),
    subline("rb25-be-a.mp4", BEC, 3.0),
   ], mood="spooky")

# ============================================================ TARKOV ZOMBIES (user request, Oct 31)
TKC = "Clips: Glorious_E; VeryBadSCAV; EIRE_Gaz (YouTube)"
clip("tr25-tk-a.mp4", "https://www.youtube.com/watch?v=Abn3UT3tA3k", "*2:00-2:20", cut=0)
clip("tr25-tk-b.mp4", "https://www.youtube.com/watch?v=LxarqL48MUA", "*4:00-4:20", cut=0)
clip("tr25-tk-c.mp4", "https://www.youtube.com/watch?v=LxarqL48MUA", "*12:00-12:20", cut=0)
clip("tr25-tk-d.mp4", "https://www.youtube.com/watch?v=Z8Kp6FannzQ", "*1:30-1:50", cut=0)
ep(227, "tarkov-zombies-2026", "Zombies Are Back in Tarkov", FENRIR, "#c6ff00",
   {"font": MF + "BlackOpsOne-Regular.ttf", "size": 92, "fill": "#ffffff", "hi": "#eeff41", "stroke": 8},
   [L("Zombies are back in Escape from Tarkov, and this time it's worse.",
      CLIP("tr25-tk-a.mp4", "TARKOV\nZOMBIES", "THE OUTBREAK", 0, TKC)),
    L("The Halloween event started on October 29th. The infected are on every map, and some of them shoot back.",
      CLIP("tr25-tk-b.mp4", "EVERY MAP", "FAST, SLOW, RANGED", 0, TKC)),
    L("Tagilla is back as a zombie, with a scythe. And there are infected Black Division soldiers too.",
      CLIP("tr25-tk-c.mp4", "ZOMBIE\nTAGILLA", "NOW WITH A SCYTHE", 0, TKC)),
    L("Labs and Factory are now outbreak zones. Small groups only, and no insurance. Your job? Find the vaccine.",
      CLIP("tr25-tk-d.mp4", "NO\nINSURANCE", "FIND THE VACCINE", 0, TKC)),
    ask("Would you go into Labs right now?", "WOULD YOU\nGO IN?", "tr25-tk-a.mp4", TKC),
    subline("tr25-tk-a.mp4", TKC, 3.0),
   ], pron={"Tarkov": "Tar-kov", "Tagilla": "Ta-gee-la"}, prop_clip="tr25-tk-b.mp4", edition="TARKOV", mood="spooky")

# ============================================================ TRENDING MEME (Know Your Meme, Oct 2026)
HIC = "Clips: MrToucan Explains; Uriah Sachs; dumb alt account; EVIL sjtcfal (YouTube)"
clip("tr25-hi-a.mp4", "https://www.youtube.com/watch?v=x5WbmxMqWsU", "*0:00-0:16", cut=0)
clip("tr25-hi-b.mp4", "https://www.youtube.com/watch?v=GlSy4tNmRng", "*0:10-0:30", cut=0)
clip("tr25-hi-c.mp4", "https://www.youtube.com/watch?v=l8YIf93uwZE", "*0:20-0:40", cut=0)
clip("tr25-hi-d.mp4", "https://www.youtube.com/watch?v=yu_fnvjFY40", "*0:00-0:18", cut=0)
ep(228, "scientists-reveal-the-hi", "Where Scientists Reveal the Hi Came From", PUCK, "#ff9100",
   {"font": MF + "Bangers-Regular.ttf", "size": 120, "mode": "word", "fill": "#ffffff", "hi": "#ffd180", "cy": 1470},
   [L("Scientists reveal the hi. But what does it actually mean?",
      CLIP("tr25-hi-a.mp4", "SCIENTISTS\nREVEAL THE HI", "THE MEME", 0, HIC, bs=110)),
    L("It started with a real BBC article in 2025, about why ginger cats are ginger.",
      CLIP("tr25-hi-b.mp4", "A REAL\nBBC ARTICLE", "WHY GINGER CATS ARE GINGER", 0, HIC, bs=130, ss=44)),
    L("A Redditor captioned the cat, Scientists reveal the secret. Then in May, someone changed one word, to hi.",
      CLIP("tr25-hi-c.mp4", "SECRET\nTO HI", "ONE WORD", 0, HIC)),
    L("It means nothing. That's the joke. And in October, it took over Instagram and TikTok.",
      CLIP("tr25-hi-d.mp4", "IT MEANS\nNOTHING", "THAT'S THE JOKE", 0, HIC, bs=130)),
    ask("What should scientists reveal next?", "WHAT SHOULD\nTHEY REVEAL?", "tr25-hi-a.mp4", HIC),
    subline("tr25-hi-a.mp4", HIC, 3.0),
   ], pron={"BBC": "B B C"}, prop_clip="tr25-hi-b.mp4", edition="MEME LORE")

# ============================================================ LORE
SLC = "Clips: PewDiePie; Marble Hornets; TheRemster (YouTube)"
clip("tr25-sl-a.mp4", "https://www.youtube.com/watch?v=OZMBG4Pn3Sg", "*1:38-1:58", cut=0)
clip("tr25-sl-b.mp4", "https://www.youtube.com/watch?v=Gjp_z3CIxNo", "*9:01-9:21", cut=0)
clip("tr25-sl-c.mp4", "https://www.youtube.com/watch?v=Bn59FJ4HrmU", "*0:25-0:45", cut=0)
clip("tr25-sl-d.mp4", "https://www.youtube.com/watch?v=OZMBG4Pn3Sg", "*6:05-6:25", cut=0)
ep(229, "slender-man-origin", "Where Slender Man Came From", MIKE, "#eeeeee",
   {"font": MF + "BlackOpsOne-Regular.ttf", "size": 92, "fill": "#ffffff", "hi": "#ffffff", "stroke": 8},
   [L("This scream got 14 million views. But Slender Man started as a Photoshop contest.",
      CLIP("tr25-sl-a.mp4", "SLENDER\nMAN", "THE ORIGIN", 3.5, SLC)),
    L("In June 2009, a forum asked for creepy edited photos. Eric Knudsen added a tall, faceless man behind some kids.",
      CLIP("tr25-sl-b.mp4", "ONE\nPHOTOSHOP", "JUNE 2009", 0, SLC)),
    L("That same year, a YouTube series called Marble Hornets turned him into a found footage horror story.",
      CLIP("tr25-sl-c.mp4", "MARBLE\nHORNETS", "2009", 0, SLC)),
    L("Then in 2012, the game Slender came out. So many people tried to download it, the website crashed.",
      CLIP("tr25-sl-d.mp4", "SLENDER:\nTHE GAME", "THE SITE CRASHED", 0, SLC, bs=130)),
    ask("Did Slender ever scare you?", "DID IT\nSCARE YOU?", "tr25-sl-a.mp4", SLC, 3.5),
    subline("tr25-sl-a.mp4", SLC, 6.0),
   ], pron={"Knudsen": "Noodsen"}, prop_clip="tr25-sl-b.mp4", edition="SLENDER", mood="spooky")

PKC = "Clips: SalC1; Minecraft@Home (YouTube)"
clip("tr25-pk-a.mp4", "https://www.youtube.com/watch?v=ea6py9q46QU", "*9:34-9:54", cut=0)
clip("tr25-pk-b.mp4", "https://www.youtube.com/watch?v=88By1e1N9es", "*0:20-0:40", cut=0)
clip("tr25-pk-c.mp4", "https://www.youtube.com/watch?v=ea6py9q46QU", "*1:00-1:20", cut=0)
ep(230, "pack-png-seed", "It Took 3,700 People to Find This Minecraft Picture", LIAM, "#4caf50",
   {"font": MF + "RussoOne-Regular.ttf", "size": 92, "hi": "#b9f6ca", "stroke": 8},
   [L("This tiny picture was in Minecraft for 10 years. Nobody knew where it was taken.",
      CLIP("tr25-pk-a.mp4", "PACK.PNG", "THE MINECRAFT MYSTERY", 0, PKC)),
    L("It's called pack.png, the default resource pack icon. A real Minecraft world, but which one?",
      CLIP("tr25-pk-c.mp4", "WHICH\nWORLD?", "128 BY 128 PIXELS", 0, PKC)),
    L("In 2020, SalC1 made a video about it, and the hunt began. Thousands of volunteers lent their computers to search every seed.",
      CCOUNT("tr25-pk-b.mp4", 0, PKC, 3700, "VOLUNTEERS", fmt="~{:,.0f}")),
    L("In September, they found it, in one of the very last seeds they searched.",
      CLIP("tr25-pk-a.mp4", "FOUND", "SEPTEMBER 2020", 6.0, PKC, bs=180)),
    ask("What Minecraft mystery should we cover next?", "NEXT\nMYSTERY?", "tr25-pk-a.mp4", PKC),
    subline("tr25-pk-a.mp4", PKC, 3.0),
   ], pron={"SalC1": "Sal C 1", "pack.png": "pack dot P N G"}, prop_clip="tr25-pk-b.mp4", edition="MINECRAFT")

# ================================================================== write
paths = []
for e in RB:
    e = dict(preset="roblox", hdr="tag", **e)
    words = sum(len(l.get("say", l["t"]).split()) for l in e["lines"])
    p = os.path.join("episodes", "roblox", e["slug"] + ".json")
    json.dump(e, open(os.path.join(ROOT, p), "w"), indent=1, ensure_ascii=False)
    paths.append(p)
    print(e["slug"], len(e["lines"]), "lines", words, "words")
manifest = {"batch": 25, "note": "Antarctic Lights, BOOBAWAMBA, Green Bullet, +1 Spider Arm, Say Cheese, Bug Evolution, Tarkov zombies, Scientists Reveal the Hi, Slender Man, pack.png",
            "posting": "batch-25/posting.txt", "episodes": paths, "clips": CLIPS}
json.dump(manifest, open(os.path.join(ROOT, "batches", "batch-25.json"), "w"), indent=1)
print(len(CLIPS), "clips")
