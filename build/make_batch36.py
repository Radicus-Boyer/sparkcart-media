"""Writes batch 35 (facts checked 2026-11-10): 8 GD (every GD Short clears 1,000) + Blox Fruits + Wii bowling fail meme = #316-325.

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

# ===== shared helpers (from batch 31)


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

# ============================================================ GEOMETRY DASH - v3 "GD news" style (user, Nov 6):
# word-by-word captions in the middle of the screen (NimPop style) + a fixed [BRACKET] header up top (ReapaVON style).
GDCAP = {"font": "LuckiestGuy.ttf", "size": 124, "mode": "word", "fill": "#ffffff", "hi": "#ffffff", "cy": 1000, "stroke": 11}
def H(name, head, start, credit, sub=None, **k):
    """GD news scene: real clip full screen, small [BRACKET] header at the top, captions do the talking."""
    k.setdefault("by", 250); k.setdefault("bs", 74); k.setdefault("ss", 50)
    return CLIP(name, head, sub, start, credit, **k)
def HC(name, start, credit, to, head, fmt="{:,.0f}", **k):
    d = H(name, head, start, credit, **k); d["count"] = {"from": 0, "to": to, "fmt": fmt, "dur": 1.3}; d["bs"] = k.get("bs", 120); d["big"] = None
    d["sub"] = head; d["ss"] = 54
    return d


# ============================================================ BATCH 32 (user, Nov 7): channel left "5k view jail", so every Short
# must hold 60%+ retention: loud real-clip hook, a twist every few seconds, and an end question people WANT to answer.
# Mix: 3 meme lore (memes did 6x), 4 GD (incl. Zoink plug posted LAST of the day), Fortnite Pirate Shop, Roblox clones story, 1 Roblox game.
MEMECAP = {"font": MF + "Bangers-Regular.ttf", "size": 120, "mode": "word", "fill": "#ffffff", "hi": "#ffe57f", "cy": 1470}
def MCAP(hi):
    return dict(MEMECAP, hi=hi)




# ============================================================ BATCH 36 (Nov 10 night): analytics say GD stories are the steady winner
# (all 1,000+), old-Roblox big-number videos ~900, official-trailer / AI videos flop. No official trailers or music videos as clips.
def RCAP(hi):
    return {"font": MF + "Bangers-Regular.ttf", "size": 120, "mode": "word", "fill": "#ffffff", "hi": hi, "cy": 1470}

# ============================================================ BATCH 36 (Nov 10, night): polar bear Short = 16.7K views (6x everything else) because it opens
# on a creepy real sound. Mix (user: keep regular GD + Roblox): 4 GD, 4 old Roblox games, 2 polar-bear-sound memes.
# (Oliver Tree memes skipped: he died in a real helicopter crash in June 2026.)
PBCAP = {"font": MF + "Bangers-Regular.ttf", "size": 120, "mode": "word", "fill": "#ffffff", "hi": "#e0f7fa", "cy": 1470}

# ---------------------------------------------------------------- 326 GD: Silent Clubstep (wiki.gg)
SCC = "Clips: paqoe; fnm04 (YouTube)"
clip("gd36-sc-a.mp4", "https://www.youtube.com/watch?v=GR4OMkS3SN8", "*2:00-2:20", cut=0)
clip("gd36-sc-b.mp4", "https://www.youtube.com/watch?v=GR4OMkS3SN8", "*0:30-0:50", cut=0)
clip("gd36-sc-c.mp4", "https://www.youtube.com/watch?v=4VQzSID55lY", "*0:20-0:40", cut=0)
ep(326, "silent-clubstep-impossible", "This Level Was Called Humanly Impossible", MIKE, "#00e5ff", GDCAP,
   [L("For years, players said this level was humanly impossible.",
      H("gd36-sc-c.mp4", "[IMPOSSIBLE]\nSILENT CLUBSTEP", 0, SCC)),
    L("It's a silent remake of Clubstep. With a section players call the eight jumps of hell.",
      H("gd36-sc-b.mp4", "[8 JUMPS]\nOF HELL", 0, SCC)),
    L("In 2020 it got a nerf, which took out the timings only possible at high FPS.",
      H("gd36-sc-c.mp4", "[2020]\nNERFED", 7.0, SCC)),
    L("In July 2022, paqoe finally verified it.",
      H("gd36-sc-a.mp4", "[VERIFIED]\nJULY 2022", 0, SCC)),
    L("It took over 138,000 attempts.",
      HC("gd36-sc-a.mp4", 7.0, SCC, 138000, "ATTEMPTS - SILENT CLUBSTEP")),
    ask("Is it still impossible?", "STILL\nIMPOSSIBLE?", "gd36-sc-c.mp4", SCC),
    subline("gd36-sc-b.mp4", SCC, 7.0),
   ], pron=dict(GD_PRON, paqoe="Pack-oh", Clubstep="Club step"), gd_player="paqoe", **GDE)

# ---------------------------------------------------------------- 327 GD: Avernus (wiki.gg)
AVC = "Clips: Zoink; Diamond (YouTube)"
clip("gd36-av-a.mp4", "https://www.youtube.com/watch?v=16Zh8jssanc", "*0:30-0:50", cut=0)
clip("gd36-av-b.mp4", "https://www.youtube.com/watch?v=16Zh8jssanc", "*1:10-1:30", cut=0)
clip("gd36-av-c.mp4", "https://www.youtube.com/watch?v=oEFB-ZrhMmM", "*0:50-1:10", cut=0)
ep(327, "avernus-27732-vs-233986", "Zoink Beat This Level in 27,732 Attempts The Next Player Needed 233,986", FENRIR, "#ff5722", GDCAP,
   [L("Zoink beat this level in about 27,000 attempts. The next player to beat it needed over 233,000.",
      H("gd36-av-a.mp4", "[27,732 VS 233,986]\nAVERNUS", 0, AVC)),
    L("Avernus is known for fast waves, mode switches and brutal timings.",
      H("gd36-av-b.mp4", "[FAST WAVES]\nBRUTAL TIMINGS", 0, AVC)),
    L("Zoink verified it in March 2023. It became the hardest level in the game, passing Acheron.",
      H("gd36-av-a.mp4", "[#1]\nHARDEST LEVEL", 7.0, AVC)),
    L("Diamond was the second person to beat it. It took him 233,986 attempts.",
      HC("gd36-av-c.mp4", 0, AVC, 233986, "ATTEMPTS - DIAMOND")),
    L("Then wPopoff beat it in just six days.",
      H("gd36-av-c.mp4", "[6 DAYS]\nWPOPOFF", 7.0, AVC)),
    ask("How many attempts would you need?", "HOW MANY\nATTEMPTS?", "gd36-av-a.mp4", AVC),
    subline("gd36-av-b.mp4", AVC, 7.0),
   ], pron=dict(GD_PRON, Avernus="Uh-vern-us", Acheron="Ack-er-on"), gd_player="Zoink", **GDE)

# ---------------------------------------------------------------- 328 GD: Tunnel of Despair (wiki.gg)
TDC = "Clips: Zoink; Zallitz; Neiro (YouTube)"
clip("gd36-td-a.mp4", "https://www.youtube.com/watch?v=LpS4JREhW98", "*0:20-0:40", cut=0)
clip("gd36-td-b.mp4", "https://www.youtube.com/watch?v=LpS4JREhW98", "*1:30-1:50", cut=0)
clip("gd36-td-c.mp4", "https://www.youtube.com/watch?v=0GC5og7gVS0", "*0:40-1:00", cut=0)
ep(328, "tunnel-of-despair-nerfed", "It Was Built to Be the Hardest Level Then It Got Nerfed", LIAM, "#ff1744", GDCAP,
   [L("This level was built to top the Demonlist. Then it got nerfed.",
      H("gd36-td-a.mp4", "[NERFED]\nTUNNEL OF DESPAIR", 0, TDC)),
    L("It's grayscale, with red pulsing on every drop. And a wave section that will not end.",
      H("gd36-td-b.mp4", "[ENDLESS WAVE]\nGRAYSCALE + RED", 0, TDC)),
    L("Zoink verified it in June 2023. But only in a nerfed version.",
      H("gd36-td-c.mp4", "[JUNE 2023]\nVERIFIED", 0, TDC)),
    L("It took about 12,000 attempts.",
      HC("gd36-td-a.mp4", 7.0, TDC, 12000, "ATTEMPTS - NERFED")),
    ask("Should nerfed levels count?", "NERFS\nOK?", "gd36-td-b.mp4", TDC),
    subline("gd36-td-c.mp4", TDC, 7.0),
   ], pron=dict(GD_PRON, Zallitz="Zal-its"), gd_player="Zoink", **GDE)

# ---------------------------------------------------------------- 329 GD: Defeated Circles (wiki.gg)
DCC = "Clips: Zoink; Cosmo (YouTube)"
clip("gd36-dc-a.mp4", "https://www.youtube.com/watch?v=nU5AQPzd2YA", "*0:10-0:30", cut=0)
clip("gd36-dc-b.mp4", "https://www.youtube.com/watch?v=nU5AQPzd2YA", "*0:40-1:00", cut=0)
clip("gd36-dc-c.mp4", "https://www.youtube.com/watch?v=R8BMscOkTrA", "*0:20-0:40", cut=0)
ep(329, "defeated-circles-9000-attempts", "Zoink Beat the Top Nine Circles Level in 5 Days", PUCK, "#7c4dff", GDCAP,
   [L("Zoink beat the hardest Nine Circles level in just five days.",
      H("gd36-dc-c.mp4", "[5 DAYS]\nDEFEATED CIRCLES", 0, DCC)),
    L("Nine Circles is one of the most famous levels in Geometry Dash. This is a mega collab redecor of it.",
      H("gd36-dc-b.mp4", "[NINE CIRCLES]\nMEGA COLLAB", 0, DCC)),
    L("It was published by GXQ. And made by Galaxium and a huge team.",
      H("gd36-dc-a.mp4", "[GXQ]\nGALAXIUM", 0, DCC)),
    L("Zoink verified it in May 2025. After about 9,000 attempts.",
      HC("gd36-dc-a.mp4", 7.0, DCC, 9000, "ATTEMPTS - VERIFIED")),
    ask("Is Nine Circles the best level ever?", "BEST\nLEVEL?", "gd36-dc-c.mp4", DCC),
    subline("gd36-dc-b.mp4", DCC, 7.0),
   ], pron=dict(GD_PRON, Galaxium="Guh-lax-ee-um", GXQ="G X Q"), gd_player="Zoink", **GDE)

# ---------------------------------------------------------------- 330 ROBLOX: Build A Boat For Treasure (Roblox API Nov 10)
BBC = "Clips: Roblox gameplay (YouTube)"
clip("rb36-bb-a.mp4", "https://www.youtube.com/watch?v=GyvNDiRRjAI", "*3:00-3:20", cut=0)
clip("rb36-bb-b.mp4", "https://www.youtube.com/watch?v=ZGPhyrKWti0", "*5:00-5:20", cut=0)
clip("rb36-bb-c.mp4", "https://www.youtube.com/watch?v=IFRtw36RP9A", "*8:00-8:20", cut=0)
ep(330, "build-a-boat-5-billion", "This Roblox Game From 2016 Has Over 5 Billion Visits", MIKE, "#29b6f6", RCAP("#b3e5fc"),
   [L("This Roblox game came out in 2016. And it has over five billion visits.",
      CLIP("rb36-bb-a.mp4", "5 BILLION\nVISITS", "BUILD A BOAT", 0, BBC, bs=150)),
    L("It's Build A Boat For Treasure. You build a boat, then sail through dangerous waters to find treasure.",
      CLIP("rb36-bb-b.mp4", "BUILD A BOAT", "FOR TREASURE", 0, BBC, bs=150)),
    L("More than 8 million people have favorited it.",
      CCOUNT("rb36-bb-c.mp4", 0, BBC, 8570000, "FAVORITES", bs=130)),
    L("And almost 9,000 people were playing it when I checked.",
      CLIP("rb36-bb-a.mp4", "9,000\nPLAYING", "RIGHT NOW", 7.0, BBC, bs=150)),
    ask("What's the biggest boat you ever built?", "BIGGEST\nBOAT?", "rb36-bb-b.mp4", BBC, 7.0),
   ])

# ---------------------------------------------------------------- 331 ROBLOX: Epic Minigames
EMC = "Clips: Roblox gameplay (YouTube)"
clip("rb36-em-a.mp4", "https://www.youtube.com/watch?v=Lq2284-V9iM", "*2:00-2:20", cut=0)
clip("rb36-em-b.mp4", "https://www.youtube.com/watch?v=5v5wENuiF6g", "*3:00-3:20", cut=0)
clip("rb36-em-c.mp4", "https://www.youtube.com/watch?v=0ftp75jJ-Ec", "*10:00-10:20", cut=0)
ep(331, "epic-minigames-8-million-favorites", "This 2015 Roblox Game Has 8.6 Million Favorites", FENRIR, "#ffd600", RCAP("#fff59d"),
   [L("This Roblox game is 11 years old. And 8.6 million people have favorited it.",
      CLIP("rb36-em-a.mp4", "8.6 MILLION\nFAVORITES", "EPIC MINIGAMES", 0, EMC, bs=140)),
    L("Epic Minigames came out in 2015. Every round is a different minigame.",
      CLIP("rb36-em-b.mp4", "EVERY ROUND\nIS NEW", "2015", 0, EMC, bs=150)),
    L("It has over 2 billion visits.",
      CCOUNT("rb36-em-c.mp4", 0, EMC, 2363415872, "VISITS", bs=120)),
    L("And over 1,600 people were still playing it when I checked.",
      CLIP("rb36-em-a.mp4", "1,600+\nPLAYING", "RIGHT NOW", 7.0, EMC, bs=150)),
    ask("What's your favorite minigame?", "BEST\nMINIGAME?", "rb36-em-b.mp4", EMC, 7.0),
   ])

# ---------------------------------------------------------------- 332 ROBLOX: Mad City
MCC = "Clips: Roblox gameplay (YouTube)"
clip("rb36-mc-a.mp4", "https://www.youtube.com/watch?v=dQFe5StO6Og", "*1:00-1:20", cut=0)
clip("rb36-mc-b.mp4", "https://www.youtube.com/watch?v=dQFe5StO6Og", "*4:00-4:20", cut=0)
clip("rb36-mc-c.mp4", "https://www.youtube.com/watch?v=pV1cOMxueAI", "*3:00-3:20", cut=0)
ep(332, "mad-city-2-billion-visits-76-playing", "This Roblox Game Has 2.6 Billion Visits But 76 Players", LIAM, "#ff1744", RCAP("#ff8a80"),
   [L("This Roblox game has over two and a half billion visits. And only 76 people were playing it when I checked.",
      CLIP("rb36-mc-a.mp4", "76\nPLAYING", "MAD CITY", 0, MCC, bs=170)),
    L("Mad City came out in 2017. You pick a side. Criminal, or hero.",
      CLIP("rb36-mc-b.mp4", "CRIMINAL\nOR HERO", "2017", 0, MCC, bs=150)),
    L("It has 2.6 billion visits.",
      CCOUNT("rb36-mc-c.mp4", 0, MCC, 2615038411, "VISITS", bs=120)),
    L("And almost 6 million favorites.",
      CLIP("rb36-mc-a.mp4", "5.8 MILLION\nFAVORITES", "", 7.0, MCC, bs=140)),
    ask("Did you play Mad City?", "DID YOU\nPLAY IT?", "rb36-mc-b.mp4", MCC, 7.0),
   ])

# ---------------------------------------------------------------- 333 ROBLOX: Speed Run 4
SRC = "Clips: Roblox gameplay (YouTube)"
clip("rb36-sr-a.mp4", "https://www.youtube.com/watch?v=ms05cqLt7ao", "*2:00-2:20", cut=0)
clip("rb36-sr-b.mp4", "https://www.youtube.com/watch?v=ms05cqLt7ao", "*8:00-8:20", cut=0)
clip("rb36-sr-c.mp4", "https://www.youtube.com/watch?v=hDIa4GDdWKE", "*3:00-3:20", cut=0)
ep(333, "speed-run-4-from-2014", "This Roblox Game From 2014 Still Has 1.7 Billion Visits", PUCK, "#76ff03", RCAP("#ccff90"),
   [L("This Roblox game is from 2014. And it has almost two billion visits.",
      CLIP("rb36-sr-c.mp4", "FROM 2014", "SPEED RUN 4", 0, SRC, bs=160)),
    L("It's Speed Run 4. You race through levels as fast as you can.",
      CLIP("rb36-sr-a.mp4", "RACE\nTHE LEVELS", "SPEED RUN 4", 0, SRC, bs=150)),
    L("It has 1.7 billion visits.",
      CCOUNT("rb36-sr-b.mp4", 0, SRC, 1757127816, "VISITS", bs=120)),
    L("More than 4 million favorites. And 700 people were playing it when I checked.",
      CLIP("rb36-sr-a.mp4", "4.5 MILLION\nFAVORITES", "", 7.0, SRC, bs=140)),
    ask("Did you beat all 32 levels?", "ALL 32\nLEVELS?", "rb36-sr-c.mp4", SRC, 7.0),
   ])

# ---------------------------------------------------------------- 334 MEME: the polar bear's sound (Know Your Meme)
PBC = "Clips: polar bear 2026 meme videos (YouTube)"
clip("tr36-pb-a.mp4", "https://www.youtube.com/watch?v=G1e-hQaejNU", "*0:00-0:09", cut=0, ln=9)
clip("tr36-pb-b.mp4", "https://www.youtube.com/watch?v=gUuW3oXhAEQ", "*0:30-0:50", cut=0)
clip("tr36-pb-c.mp4", "https://www.youtube.com/watch?v=uf0Aw5Lg4HA", "*0:00-0:14", cut=0, ln=13)
ep(334, "polar-bear-sound-horror-game", "The Creepy Polar Bear Song Comes From a Horror Game", PUCK, "#80deea", PBCAP,
   [L("The creepy sound in the polar bear meme comes from a horror game.",
      CLIP("tr36-pb-a.mp4", "THE CREEPY\nSOUND", "", 0, PBC, bs=140)),
    L("It's called Cumbia Masonica. It came out in 2017, and it was used in the game Hello Charlotte, episode 3.",
      CLIP("tr36-pb-b.mp4", "CUMBIA\nMASONICA", "HELLO CHARLOTTE", 0, PBC, bs=140)),
    L("In September 2023, videos using it started spreading with the polar bear. It sounds like a girl repeating yo yo yo.",
      CLIP("tr36-pb-c.mp4", "YO YO YO", "", 0, PBC, bs=150)),
    L("Now every polar bear video has it.",
      CLIP("tr36-pb-b.mp4", "EVERY\nPOLAR BEAR", "", 7.0, PBC, bs=150)),
    ask("Did this song give you chills?", "CHILLS?", "tr36-pb-a.mp4", PBC),
    subline("tr36-pb-c.mp4", PBC, 6.0),
   ], pron={"Cumbia": "Koom-bee-uh", "Masonica": "Mah-sonn-ih-kuh"}, edition="MEME LORE")

# ---------------------------------------------------------------- 335 MEME: polar bear started in Russia (Know Your Meme)
PRC = "Clips: polar bear 2026 meme videos (YouTube)"
clip("tr36-pr-a.mp4", "https://www.youtube.com/watch?v=uf0Aw5Lg4HA", "*0:00-0:14", cut=0, ln=13)
clip("tr36-pr-b.mp4", "https://www.youtube.com/watch?v=AK-XhVnvP4U", "*0:20-0:40", cut=0)
clip("tr36-pr-c.mp4", "https://www.youtube.com/watch?v=G1e-hQaejNU", "*0:00-0:09", cut=0, ln=9)
ep(335, "polar-bear-started-in-russia", "The Polar Bear Meme Started in Russia in 2023", LIAM, "#4dd0e1", PBCAP,
   [L("It's November 2026. The polar bear meme was posted three years ago.",
      CLIP("tr36-pr-a.mp4", "IT'S NOVEMBER\n2026", "", 0, PRC, bs=140)),
    L("It started in Russia, in March 2023. A TikTok said, this is a November meme from 2026. You won't understand yet.",
      CLIP("tr36-pr-b.mp4", "MARCH\n2023", "RUSSIA", 0, PRC, bs=150)),
    L("The image is allegedly AI generated. A polar bear at night, holding itself up on two paws.",
      CLIP("tr36-pr-c.mp4", "ALLEGEDLY\nAI", "", 0, PRC, bs=150)),
    L("That first TikTok got about 3 million plays.",
      CCOUNT("tr36-pr-a.mp4", 0, PRC, 3100000, "PLAYS", fmt="{:,.0f}+", bs=140)),
    ask("Did you know about the polar bear in 2023?", "KNEW\nABOUT IT?", "tr36-pr-c.mp4", PRC),
    subline("tr36-pr-b.mp4", PRC, 7.0),
   ], pron={}, edition="MEME LORE")

# ================================================================== write
paths = []
for e in RB:
    e = dict(preset="roblox", hdr="tag", **e)
    words = sum(len(l.get("say", l["t"]).split()) for l in e["lines"])
    p = os.path.join("episodes", "roblox", e["slug"] + ".json")
    json.dump(e, open(os.path.join(ROOT, p), "w"), indent=1, ensure_ascii=False)
    paths.append(p)
    print(e["slug"], len(e["lines"]), "lines", words, "words")
manifest = {"batch": 36, "note": "Silent Clubstep, Avernus, Tunnel of Despair, Defeated Circles, Build A Boat, Epic Minigames, Mad City, Speed Run 4, polar bear sound, polar bear Russia",
            "posting": "Z:/claudeprojects/roblox vids/batch-36/posting.txt", "episodes": paths, "clips": CLIPS}
json.dump(manifest, open(os.path.join(ROOT, "batches", "batch-36.json"), "w"), indent=1)
print(len(CLIPS), "clips")
