"""Writes batch 28 (facts checked 2026-11-03): 4 GD + 4 Roblox + Fortnite Pirate Shop odds + Jimothy = #251-260.

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


# v2.2 (user, Nov 3): mix 4 GD / 4 Roblox / 2 news-trend; first-second text sets up a question; search-first titles;
# pinned comment per video (posting.txt YT COMMENT); Roblox hooks open with "THIS NEW FUN GAME ON ROBLOX";
# clip sound only loud in the hook (engine clip_duck). Subscribe line kept on GD / news / meme, dropped on Roblox.
GD_PRON.update({"Demishio": "Deh-mee-shee-o", "Kyouki": "Kyoh-kee", "Vortrox": "Vor-trox", "OniLink": "Oni Link",
                "Zoink": "Zoynk", "wPopoff": "W Pop off", "Netermind": "Neter-mind", "Taiago": "Tie-ah-go",
                "Exen": "Ex-en", "ivyteal": "ivy teal", "Servax": "Sir Vax"})
NEW = "THIS NEW FUN\nGAME ON ROBLOX"

# ============================================================ GEOMETRY DASH (GD wiki, Nov 3)
KYC = "Clips: Demishio; Zoink (YouTube)"
clip("gd28-ky-a.mp4", "https://www.youtube.com/watch?v=KDa5c0CJTHs", "*2:08-2:28", cut=0)
clip("gd28-ky-b.mp4", "https://www.youtube.com/watch?v=GM-eInEOwFk", "*2:40-3:00", cut=0)
clip("gd28-ky-c.mp4", "https://www.youtube.com/watch?v=KDa5c0CJTHs", "*5:16-5:36", cut=0)
clip("gd28-ky-d.mp4", "https://www.youtube.com/watch?v=g8iCSlLx-xE", "*1:30-1:50", cut=0)
ep(251, "kyouki-501997", "Kyouki Took 501,997 Attempts", FENRIR, "#ff1744",
   {"font": MF + "Anton-Regular.ttf", "size": 104, "hi": "#ff8a80", "stroke": 8},
   [L("501,997 attempts, on a level one person made alone.",
      CLIP("gd28-ky-a.mp4", "501,997\nATTEMPTS?", "FOR ONE LEVEL", 0, KYC, bs=130)),
    L("Kyouki is a solo level by Demishio. He built every part of it himself, then set out to beat it.",
      CLIP("gd28-ky-c.mp4", "KYOUKI", "MADE BY ONE PERSON", 0, KYC)),
    L("He played it for 175 days. His worst death was at 97 percent.",
      CLIP("gd28-ky-b.mp4", "97%", "175 DAYS", 0, KYC, bs=200)),
    L("In November 2022, he finally beat it, after 501,997 attempts. It went in at number 3, the hardest solo level ever made.",
      CCOUNT("gd28-ky-d.mp4", 0, KYC, 501997, "ATTEMPTS")),
    ask("Could you spend 175 days on one level?", "175 DAYS ON\nONE LEVEL?", "gd28-ky-a.mp4", KYC),
    subline("gd28-ky-a.mp4", KYC, 3.0),
   ], pron=dict(GD_PRON), gd_player="Demishio", **GDE)

CXC = "Clips: Vortrox; VortroxTwo (YouTube)"
clip("gd28-cx-a.mp4", "https://www.youtube.com/watch?v=Cq1ysv-7-w0", "*1:20-1:40", cut=0)
clip("gd28-cx-b.mp4", "https://www.youtube.com/watch?v=B3sGQ2bhDU8", "*3:32-3:52", cut=0)
clip("gd28-cx-c.mp4", "https://www.youtube.com/watch?v=qUPPt5Eonss", "*10:00-10:20", cut=0)
ep(252, "cycles-x-53363", "Vortrox Turned an Easy Main Level Into an Extreme Demon", LIAM, "#00e676",
   {"font": MF + "RussoOne-Regular.ttf", "size": 92, "hi": "#69f0ae", "stroke": 8},
   [L("He took a main level from the original game, and made it one of the hardest levels ever.",
      CLIP("gd28-cx-a.mp4", "CYCLES...\nBUT WHY?", "CYCLES X", 0, CXC, bs=140)),
    L("Cycles X is Vortrox's super buffed remake of Cycles, part of his series turning main levels into extreme demons.",
      CLIP("gd28-cx-c.mp4", "SUPER\nBUFFED", "A MAIN LEVEL REMADE", 0, CXC, bs=150)),
    L("He died at 93 percent, then died at 93 again, in almost the exact same spot.",
      CLIP("gd28-cx-c.mp4", "93%\n93%", "SAME SPOT", 8.0, CXC, bs=150)),
    L("In July, after 64 live streams, he beat it, at 53,363 attempts.",
      CCOUNT("gd28-cx-b.mp4", 0, CXC, 53363, "ATTEMPTS")),
    ask("Which main level should get buffed next?", "WHICH LEVEL\nIS NEXT?", "gd28-cx-a.mp4", CXC),
    subline("gd28-cx-a.mp4", CXC, 3.0),
   ], pron=dict(GD_PRON), gd_player="Vortrox", **GDE)

TWC = "Clips: Zoink; Neiro; switched to (YouTube)"
clip("gd28-tw-a.mp4", "https://www.youtube.com/watch?v=9fsZ014qB3s", "*2:40-3:00", cut=0)
clip("gd28-tw-b.mp4", "https://www.youtube.com/watch?v=mgQL2xeviN8", "*0:30-0:50", cut=0)
clip("gd28-tw-c.mp4", "https://www.youtube.com/watch?v=Hy9DZ4NPLa0", "*0:20-0:40", cut=0)
ep(253, "tidal-wave-invalid", "Nobody Has Beaten the Real Tidal Wave", MIKE, "#2979ff",
   {"font": MF + "BlackOpsOne-Regular.ttf", "size": 92, "fill": "#ffffff", "hi": "#82b1ff", "stroke": 8},
   [L("Every player who beat Tidal Wave beat an older version. Not the one that's in the game.",
      CLIP("gd28-tw-a.mp4", "0 REAL\nVICTORS?", "TIDAL WAVE", 0, TWC, bs=120)),
    L("Zoink verified it in 2023, after 49,534 attempts, and it became the number 1 hardest level.",
      CCOUNT("gd28-tw-b.mp4", 0, TWC, 49534, "ATTEMPTS")),
    L("But when its creator, OniLink, moved the buffs over to the rated version, he added one more change.",
      CLIP("gd28-tw-c.mp4", "ONE MORE\nCHANGE", "ONILINK", 0, TWC, bs=150)),
    L("That made every win technically invalid. Zoink, Trick and wPopoff beat version 1. Four others beat version 2. Nobody has beaten version 3.",
      CLIP("gd28-tw-b.mp4", "VERSION 3:\nNOBODY", "TECHNICALLY INVALID", 6.0, TWC, bs=140)),
    ask("Should their wins still count?", "SHOULD IT\nCOUNT?", "gd28-tw-a.mp4", TWC),
    subline("gd28-tw-a.mp4", TWC, 3.0),
   ], pron=dict(GD_PRON), gd_player="Zoink", **GDE)

TDC = "Clips: Zoink; Neiro; Zallitz (YouTube)"
clip("gd28-td-a.mp4", "https://www.youtube.com/watch?v=LpS4JREhW98", "*1:55-2:15", cut=0)
clip("gd28-td-b.mp4", "https://www.youtube.com/watch?v=0GC5og7gVS0", "*0:40-1:00", cut=0)
clip("gd28-td-c.mp4", "https://www.youtube.com/watch?v=8uDmKz5HB2I", "*0:30-0:50", cut=0)
ep(254, "tunnel-of-despair-nerfed", "Tunnel of Despair Was Meant to Be Number 1 Then It Got Nerfed", SARAH, "#e53935",
   {"font": MF + "Anton-Regular.ttf", "size": 104, "hi": "#ff8a80", "stroke": 8},
   [L("This level was built to be the hardest in the game. Then it got nerfed.",
      CLIP("gd28-td-a.mp4", "BUILT FOR #1...\nTHEN NERFED?", "TUNNEL OF DESPAIR", 0, TDC, bs=110)),
    L("Tunnel of Despair is a collab by Exen and ivyteal. Grey and black, with red pulses, and a famously long wave part.",
      CLIP("gd28-td-b.mp4", "THE LONG\nWAVE", "EXEN AND IVYTEAL", 0, TDC, bs=150)),
    L("It was aimed at the top of the Demonlist. But Zoink verified it in a nerfed version, after about 12,000 attempts.",
      CCOUNT("gd28-td-b.mp4", 6.0, TDC, 12000, "ATTEMPTS", fmt="~{:,.0f}")),
    L("Every player who beat it since, beat the easier one.",
      CLIP("gd28-td-c.mp4", "THE EASIER\nONE", "EVERY VICTOR", 0, TDC, bs=150)),
    ask("Should levels ever get nerfed?", "NERF OR\nNO NERF?", "gd28-td-a.mp4", TDC),
    subline("gd28-td-a.mp4", TDC, 3.0),
   ], pron=dict(GD_PRON), gd_player="Zoink", **GDE)

# ============================================================ ROBLOX (live numbers, Nov 3) - "THIS NEW FUN GAME ON ROBLOX" hooks
DTC = "Clips: Zonko; MBT (Roblox gameplay, YouTube)"
clip("rb28-dt-a.mp4", "https://www.youtube.com/watch?v=6iViHXKCPkI", "*1:00-1:20", cut=0, backup=["https://www.youtube.com/watch?v=DvY7G3NtddE"])
clip("rb28-dt-b.mp4", "https://www.youtube.com/watch?v=6iViHXKCPkI", "*5:00-5:20", cut=0)
clip("rb28-dt-c.mp4", "https://www.youtube.com/watch?v=rwNKnHDAMGU", "*3:00-3:20", cut=0, backup=["https://www.youtube.com/watch?v=DvY7G3NtddE"])
ep(255, "can-you-pass-a-driving-test", "Can You Pass A Driving Test on Roblox", PUCK, "#ffd600",
   {"font": MF + "Bangers-Regular.ttf", "size": 120, "mode": "word", "fill": "#ffffff", "hi": "#ffff00", "cy": 1470},
   [L("This new fun game on Roblox makes you pass a driving test, before you're allowed to drive. Yes, really.",
      CLIP("rb28-dt-a.mp4", NEW, "YOU NEED A LICENSE", 0, DTC, bs=110)),
    L("Real traffic, real road rules. Pass the test, and you get your license.",
      CLIP("rb28-dt-b.mp4", "REAL ROAD\nRULES", "PASS THE TEST", 0, DTC, bs=140)),
    L("Then do driving jobs. Deliver pizzas, drive VIPs, haul trailers, and save up for the hypercar on the roof.",
      CLIP("rb28-dt-c.mp4", "THE HYPERCAR\nON THE ROOF", "DRIVING JOBS", 0, DTC, bs=120)),
    L("It came out in October, and it already has over 3 million visits.",
      CCOUNT("rb28-dt-b.mp4", 6.0, DTC, 3111139, "VISITS", bs=140)),
    ask("Would you pass the test?", "WOULD YOU\nPASS?", "rb28-dt-a.mp4", DTC),
   ])

MCT = "Clips: Electracy; GeekBlud (Roblox gameplay, YouTube)"
clip("rb28-mc-a.mp4", "https://www.youtube.com/watch?v=jgMztOy8LTM", "*0:00-0:20", cut=0)
clip("rb28-mc-b.mp4", "https://www.youtube.com/watch?v=cIMTQ6te-_k", "*0:00-0:20", cut=0)
clip("rb28-mc-c.mp4", "https://www.youtube.com/watch?v=tHpmOG9FIYk", "*1:00-1:20", cut=0, backup=["https://www.youtube.com/watch?v=WYS6yQ3ARyw"])
ep(256, "make-a-cartoon", "Make a Cartoon Lets You Animate on Roblox", HEART, "#00e5ff",
   {"font": MF + "Bangers-Regular.ttf", "size": 120, "mode": "word", "fill": "#ffffff", "hi": "#84ffff", "cy": 1470},
   [L("This new fun game on Roblox turns you into an animator.",
      CLIP("rb28-mc-a.mp4", NEW, "YOU'RE THE ANIMATOR", 0, MCT, bs=110)),
    L("In Make a Cartoon, you add stick figures, animals and props, then drag their joints to pose them.",
      CLIP("rb28-mc-b.mp4", "POSE\nTHEM", "DRAG THE JOINTS", 0, MCT, bs=150)),
    L("Add a frame, move them a little, and press play. Then share it in the gallery.",
      CLIP("rb28-mc-c.mp4", "PRESS\nPLAY", "FRAME BY FRAME", 0, MCT, bs=150)),
    L("It came out in October, and it has over 4 million visits.",
      CCOUNT("rb28-mc-b.mp4", 6.0, MCT, 4358225, "VISITS", bs=140)),
    ask("What would your first cartoon be?", "WHAT WOULD\nYOU MAKE?", "rb28-mc-a.mp4", MCT),
   ])

VEC = "Clips: FoltynPlays; Bax (Roblox gameplay, YouTube)"
clip("rb28-ve-a.mp4", "https://www.youtube.com/watch?v=HxtzSfhxkN4", "*1:00-1:20", cut=0, backup=["https://www.youtube.com/watch?v=i1B2V0oJTQk"])
clip("rb28-ve-b.mp4", "https://www.youtube.com/watch?v=HxtzSfhxkN4", "*6:00-6:20", cut=0)
clip("rb28-ve-c.mp4", "https://www.youtube.com/watch?v=7kOgArvGgAs", "*10:00-10:20", cut=0, backup=["https://www.youtube.com/watch?v=rnpg82ZenDM"])
ep(257, "plus-1-venom-evolution", "In Plus 1 Venom Evolution You Evolve Into a Giant Symbiote", FENRIR, "#212121",
   {"font": MF + "BlackOpsOne-Regular.ttf", "size": 92, "fill": "#ffffff", "hi": "#e0e0e0", "stroke": 8},
   [L("This new fun game on Roblox lets you grow into a giant black goo monster.",
      CLIP("rb28-ve-a.mp4", NEW, "BECOME THE MONSTER", 0, VEC, bs=110)),
    L("In Plus 1 Venom Evolution, you train, fight enemies, and clear stages to collect wins.",
      CLIP("rb28-ve-b.mp4", "TRAIN.\nFIGHT. WIN.", "+1 EVERY TIME", 0, VEC, bs=130)),
    L("Every win unlocks a new evolution, until you hit your max transformation.",
      CLIP("rb28-ve-c.mp4", "MAX\nFORM", "KEEP EVOLVING", 0, VEC, bs=170)),
    L("It came out in October, and it already has over 36 million visits.",
      CCOUNT("rb28-ve-b.mp4", 6.0, VEC, 36477842, "VISITS", bs=140)),
    ask("What would you evolve into?", "WHAT'S YOUR\nFINAL FORM?", "rb28-ve-a.mp4", VEC),
   ], mood="spooky")

AEC = "Clips: OrangeIsShorts; RussoPlays (Roblox gameplay, YouTube)"
clip("rb28-ae-a.mp4", "https://www.youtube.com/watch?v=GqlsNcj3KSo", "*2:00-2:20", cut=0, backup=["https://www.youtube.com/watch?v=FhneiwnsSB0"])
clip("rb28-ae-b.mp4", "https://www.youtube.com/watch?v=GqlsNcj3KSo", "*8:00-8:20", cut=0)
clip("rb28-ae-c.mp4", "https://www.youtube.com/watch?v=seJAZBsWYhQ", "*5:00-5:20", cut=0, backup=["https://www.youtube.com/watch?v=FhneiwnsSB0"])
ep(258, "plus-1-anime-eyes", "Plus 1 Anime Eyes Has Over 128 Eyes to Unlock", MIKE, "#d50000",
   {"font": MF + "Anton-Regular.ttf", "size": 104, "hi": "#ff8a80", "stroke": 8},
   [L("This new fun game on Roblox lets you collect anime eyes. Over 128 of them.",
      CLIP("rb28-ae-a.mp4", NEW, "128+ ANIME EYES", 0, AEC, bs=110)),
    L("Every click gives you plus one chakra. Train it up, and awaken stronger eyes.",
      CLIP("rb28-ae-b.mp4", "+1 CHAKRA", "EVERY CLICK", 0, AEC, bs=170)),
    L("Each eye has its own power. Then take them into fights against tougher bosses.",
      CLIP("rb28-ae-c.mp4", "BOSS\nFIGHTS", "EVERY EYE HAS A POWER", 0, AEC, bs=150)),
    L("It came out in October, and it has over 12 million visits.",
      CCOUNT("rb28-ae-b.mp4", 6.0, AEC, 12688033, "VISITS", bs=140)),
    ask("Which anime eyes would you pick?", "WHICH EYES\nWOULD YOU PICK?", "rb28-ae-a.mp4", AEC),
   ])

# ============================================================ NEWS: Fortnite Pirate Shop odds (user: include 1/700,000)
FPC = "Clips: Tomato; TRAIL-TT; TG Plays; EveryDay FN (YouTube)"
clip("tr28-fp-a.mp4", "https://www.youtube.com/watch?v=k8kqqifuIFo", "*18:40-19:00", cut=0, backup=["https://www.youtube.com/watch?v=dYefjgFNPZQ"])
clip("tr28-fp-b.mp4", "https://www.youtube.com/watch?v=DerAErpZ_Rk", "*0:00-0:20", cut=0)
clip("tr28-fp-c.mp4", "https://www.youtube.com/watch?v=dYefjgFNPZQ", "*3:00-3:20", cut=0)
clip("tr28-fp-d.mp4", "https://www.youtube.com/watch?v=mMx-mEasXsg", "*0:00-0:20", cut=0)
ep(259, "fortnite-pirate-shop-odds", "Your Odds of Finding the Fortnite Pirate Shop Token", MIKE, "#00b0ff",
   {"font": MF + "Bangers-Regular.ttf", "size": 120, "mode": "word", "fill": "#ffffff", "hi": "#80d8ff", "cy": 1470},
   [L("Your odds of finding Fortnite's free Item Shop token? About 1 in 700,000.",
      CLIP("tr28-fp-a.mp4", "1 IN\n700,000?", "PIRATE SHOP TOKEN", 0, FPC, bs=150)),
    L("The Pirate Shop token drops from Treasure Hunt chests. Find it, and anything you'd buy with V-Bucks is free for 14 days.",
      CLIP("tr28-fp-b.mp4", "14 DAYS\nFREE", "THE PIRATE SHOP", 0, FPC, bs=150)),
    L("1 in 700,000 is the first reported estimate. Epic hasn't shared the real odds.",
      CCOUNT("tr28-fp-d.mp4", 0, FPC, 700000, "CHESTS PER TOKEN", fmt="1 in {:,.0f}", bs=120)),
    L("Players say the best spot is The Chest, with about 34 buried chests. The event ends December 5th.",
      CLIP("tr28-fp-c.mp4", "THE CHEST", "34 BURIED CHESTS", 0, FPC, bs=180)),
    ask("Would you open 700,000 chests for it?", "700,000\nCHESTS?", "tr28-fp-a.mp4", FPC),
    subline("tr28-fp-a.mp4", FPC, 3.0),
   ], pron={"V-Bucks": "V Bucks"}, prop_clip="tr28-fp-b.mp4", edition="FORTNITE")

# ============================================================ GAMING MEME OF THE WEEK: Jimothy (Wikipedia)
JMC = "Clips: HAPP - Story; ViralHog; Casual Geographic; KTLA 5 (YouTube)"
clip("tr28-jm-a.mp4", "https://www.youtube.com/watch?v=hrR5u5gb38I", "*0:03-0:23", cut=0)
clip("tr28-jm-b.mp4", "https://www.youtube.com/watch?v=QXpCoMmoBbM", "*0:00-0:20", cut=0)
clip("tr28-jm-c.mp4", "https://www.youtube.com/watch?v=iVqdCEkw2-Y", "*2:25-2:45", cut=0)
clip("tr28-jm-d.mp4", "https://www.youtube.com/watch?v=V15O_crWU-s", "*0:10-0:30", cut=0)
ep(260, "jimothy-the-raccoon", "Jimothy the Raccoon Is in Video Games Now", PUCK, "#8d6e63",
   {"font": MF + "Bangers-Regular.ttf", "size": 120, "mode": "word", "fill": "#ffffff", "hi": "#ffcc80", "cy": 1470},
   [L("This is Jimothy, the round raccoon that broke the internet. And now he's in video games.",
      CLIP("tr28-jm-a.mp4", "WHO IS\nJIMOTHY?", "THE ROUND RACCOON", 0, JMC, bs=150)),
    L("In July, a woman in Seattle filmed him, and said he just looked like a Jimothy. Millions of views later, he was everywhere.",
      CLIP("tr28-jm-b.mp4", "SEATTLE", "JULY 2026", 0, JMC, bs=180)),
    L("Then gaming adopted him. Guild Wars 2 added him as a pet. Blizzard and RuneScape made tributes. There are Skyrim and Stardew Valley mods.",
      CLIP("tr28-jm-c.mp4", "GAMING\nADOPTED HIM", "GUILD WARS 2, SKYRIM, STARDEW", 0, JMC, bs=130, ss=42)),
    L("He even got an honorary degree, and his own night at a Mariners game.",
      CLIP("tr28-jm-d.mp4", "JIMOTHY\nNIGHT", "HONORARY DEGREE", 0, JMC, bs=150)),
    ask("What game should Jimothy be in next?", "WHICH GAME\nIS NEXT?", "tr28-jm-a.mp4", JMC),
    subline("tr28-jm-a.mp4", JMC, 3.0),
   ], pron={"Jimothy": "Jim-oh-thee"}, prop_clip="tr28-jm-b.mp4", edition="MEME LORE")

# ================================================================== write
paths = []
for e in RB:
    e = dict(preset="roblox", hdr="tag", **e)
    words = sum(len(l.get("say", l["t"]).split()) for l in e["lines"])
    p = os.path.join("episodes", "roblox", e["slug"] + ".json")
    json.dump(e, open(os.path.join(ROOT, p), "w"), indent=1, ensure_ascii=False)
    paths.append(p)
    print(e["slug"], len(e["lines"]), "lines", words, "words")
manifest = {"batch": 28, "note": "Kyouki, Cycles X, Tidal Wave invalid wins, Tunnel of Despair nerf, Driving Test, Make a Cartoon, +1 Venom Evolution, +1 Anime Eyes, Fortnite Pirate Shop odds, Jimothy",
            "posting": "Z:/claudeprojects/roblox vids/batch-28/posting.txt", "episodes": paths, "clips": CLIPS}
json.dump(manifest, open(os.path.join(ROOT, "batches", "batch-28.json"), "w"), indent=1)
print(len(CLIPS), "clips")
