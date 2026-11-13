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


# ============================================================ BATCH 38 (Nov 13): analytics - GD steady ~900-1,100; Minecraft/Mario ~550 (keep, user);
# Game Mysteries 2-parters flopped (35-134). User: cover top-trending YouTube gaming topics + keep Roblox + GD.
# Trending Nov 13: GTA 6 (Nov 19 launch), Fortnite Pirate Shop token, RIVALS Season 4 (tonight 9 PM ET), Survive Your Ideas.

# ---------------------------------------------------------------- 346 GD: Old Orochi (Pointercrate Nov 13)
OOC = "Clips: SeptaGon7; FlyksGMD (YouTube)"
clip("gd38-oo-a.mp4", "https://www.youtube.com/watch?v=YxtFAQtLYQY", "*0:50-1:10", cut=0)
clip("gd38-oo-b.mp4", "https://www.youtube.com/watch?v=YxtFAQtLYQY", "*1:50-2:10", cut=0)
clip("gd38-oo-c.mp4", "https://www.youtube.com/watch?v=fQVVwFZJIE0", "*0:40-1:00", cut=0)
ep(346, "old-orochi-only-one-person", "Only One Person Has Ever Beaten This Level", MIKE, "#ff1744", GDCAP,
   [L("This is the 17th hardest level in Geometry Dash. And only one person has ever beaten it.",
      H("gd38-oo-a.mp4", "[ONLY 1 PERSON]\nOLD OROCHI", 0, OOC)),
    L("It's called Old Orochi. Published by Platnuu.",
      H("gd38-oo-c.mp4", "[#17]\nDEMONLIST", 0, OOC)),
    L("Volumni verified it. And since then, nobody else has a single completion on the Demonlist.",
      H("gd38-oo-b.mp4", "[VERIFIED]\nVOLUMNI", 0, OOC)),
    L("Every other top player has tried. Zero victors.",
      HC("gd38-oo-a.mp4", 7.0, OOC, 0, "OTHER VICTORS")),
    ask("Who beats it next?", "WHO'S\nNEXT?", "gd38-oo-b.mp4", OOC, 7.0),
    subline("gd38-oo-c.mp4", OOC, 7.0),
   ], pron=dict(GD_PRON, Orochi="Oh-roh-chee", Volumni="Vol-oom-nee", Platnuu="Plat-noo"), gd_player="Volumni", **GDE)

# ---------------------------------------------------------------- 347 GD: KILLSTEALER (Pointercrate Nov 13)
KSC = "Clips: kloone (YouTube)"
clip("gd38-ks-a.mp4", "https://www.youtube.com/watch?v=uhH4oqWrsfo", "*6:00-6:20", cut=0)
clip("gd38-ks-b.mp4", "https://www.youtube.com/watch?v=uhH4oqWrsfo", "*7:30-7:50", cut=0)
clip("gd38-ks-c.mp4", "https://www.youtube.com/watch?v=mm5ue1n-cuQ", "*1:00-1:20", cut=0)
ep(347, "killstealer-only-3-people", "Only 3 People Have Ever Beaten This Level", FENRIR, "#d50000", GDCAP,
   [L("Only three people in the world have ever beaten this level.",
      H("gd38-ks-a.mp4", "[ONLY 3 PEOPLE]\nKILLSTEALER", 0, KSC)),
    L("It's called Killstealer. It's number 22 on the Demonlist.",
      H("gd38-ks-c.mp4", "[#22]\nDEMONLIST", 0, KSC)),
    L("kloone verified it. And it went in as a top 15 level.",
      H("gd38-ks-b.mp4", "[VERIFIED]\nKLOONE", 0, KSC)),
    L("Since then, only two more players have beaten it. zLevii, and Wain.",
      H("gd38-ks-a.mp4", "[ZLEVII]\n+ WAIN", 7.0, KSC)),
    ask("Could you be number 4?", "NUMBER\n4?", "gd38-ks-b.mp4", KSC, 7.0),
    subline("gd38-ks-c.mp4", KSC, 7.0),
   ], pron=dict(GD_PRON, kloone="Kloon", zLevii="Z Levy", Wain="Wayne", KILLSTEALER="Kill stealer"), gd_player="kloone", **GDE)

# ---------------------------------------------------------------- 348 GD: andromeda (Pointercrate Nov 13)
ANC = "Clips: Taiago; Neiro (YouTube)"
clip("gd38-an-a.mp4", "https://www.youtube.com/watch?v=mk3TDemdkC0", "*0:40-1:00", cut=0)
clip("gd38-an-b.mp4", "https://www.youtube.com/watch?v=mk3TDemdkC0", "*2:00-2:20", cut=0)
clip("gd38-an-c.mp4", "https://www.youtube.com/watch?v=fFtQxxepyDo", "*0:20-0:40", cut=0)
ep(348, "andromeda-top-5-to-21", "This Level Was Top 5 Now 29 People Have Beaten It", LIAM, "#7c4dff", GDCAP,
   [L("This level was one of the five hardest in Geometry Dash. Now 29 people have beaten it.",
      H("gd38-an-a.mp4", "[TOP 5]\nANDROMEDA", 0, ANC)),
    L("Andromeda was verified by Taiago. And it went straight into the top 5.",
      H("gd38-an-c.mp4", "[NEW TOP 5]\nTAIAGO", 0, ANC)),
    L("The first player to beat it after him? Zoink.",
      H("gd38-an-b.mp4", "[FIRST VICTOR]\nZOINK", 0, ANC)),
    L("Today it's number 21. With 29 victors on the Demonlist.",
      HC("gd38-an-b.mp4", 7.0, ANC, 29, "VICTORS - NOW #21")),
    ask("Should old top 5s still count as hard?", "STILL\nHARD?", "gd38-an-a.mp4", ANC, 7.0),
    subline("gd38-an-c.mp4", ANC, 7.0),
   ], pron=dict(GD_PRON, Taiago="Tie-ah-go"), gd_player="Taiago", **GDE)

# ---------------------------------------------------------------- 349 GD: Clubstep (wiki.gg)
CBC = "Clips: GuitarHeroStyles (YouTube)"
clip("gd38-cb-a.mp4", "https://www.youtube.com/watch?v=VInQkeec188", "*0:30-0:50", cut=0)
clip("gd38-cb-b.mp4", "https://www.youtube.com/watch?v=VInQkeec188", "*1:00-1:20", cut=0)
clip("gd38-cb-c.mp4", "https://www.youtube.com/watch?v=gok5ShDXxg4", "*0:40-1:00", cut=0)
ep(349, "clubstep-first-demon", "This Was the First Demon Ever in Geometry Dash", PUCK, "#00e676", GDCAP,
   [L("Before Bloodbath. Before Sonic Wave. This was the first demon in Geometry Dash.",
      H("gd38-cb-a.mp4", "[THE FIRST DEMON]\nCLUBSTEP", 0, CBC)),
    L("Clubstep is the 14th main level. And you can't even play it at first.",
      H("gd38-cb-b.mp4", "[LEVEL 14]\nLOCKED", 0, CBC)),
    L("You have to collect 10 secret coins just to unlock it.",
      HC("gd38-cb-c.mp4", 0, CBC, 10, "SECRET COINS TO UNLOCK")),
    L("Then it hits you with fake spikes, fading blocks and gravity flips. For a lot of players, it was their first demon ever.",
      H("gd38-cb-a.mp4", "[FAKE SPIKES]\nFIRST DEMON", 7.0, CBC)),
    ask("Was Clubstep your first demon?", "YOUR FIRST\nDEMON?", "gd38-cb-b.mp4", CBC, 7.0),
    subline("gd38-cb-c.mp4", CBC, 7.0),
   ], pron=dict(GD_PRON, Clubstep="Club step"), gd_player="RobTop", **GDE)

# ---------------------------------------------------------------- 350 ROBLOX: RIVALS Season 4 (Roblox event listing via Timesaver, Nov 13)
RVC = "Clips: RoBros; Mud (Roblox gameplay, YouTube)"
clip("rb38-rv-a.mp4", "https://www.youtube.com/watch?v=2ygXBCpvQX4", "*2:00-2:20", cut=0)
clip("rb38-rv-b.mp4", "https://www.youtube.com/watch?v=2ygXBCpvQX4", "*6:00-6:20", cut=0)
clip("rb38-rv-c.mp4", "https://www.youtube.com/watch?v=gh-L6GhXay4", "*5:00-5:20", cut=0)
ep(350, "rivals-season-4-tonight", "RIVALS Season 4 Starts Tonight", FENRIR, "#ff3d00", RCAP("#ffab91"),
   [L("RIVALS Season 4 starts tonight. And every rank is getting reset.",
      CLIP("rb38-rv-a.mp4", "SEASON 4\nTONIGHT", "RIVALS", 0, RVC, bs=150)),
    L("It's called The Standard Season. It starts Friday, November 13th, at 9 PM Eastern.",
      CLIP("rb38-rv-b.mp4", "THE STANDARD\nSEASON", "NOV 13 - 9 PM ET", 0, RVC, bs=140)),
    L("A new battle pass. A rank reset. Exclusive rewards. And changes to ranked.",
      CLIP("rb38-rv-c.mp4", "RANK\nRESET", "NEW BATTLE PASS", 0, RVC, bs=150)),
    L("In past updates, a free reward only went to players who joined in the first hour. So be there early.",
      CLIP("rb38-rv-a.mp4", "FIRST\nHOUR", "FREE REWARD", 7.0, RVC, bs=150)),
    ask("What rank are you going for?", "YOUR\nRANK?", "rb38-rv-b.mp4", RVC, 7.0),
   ], pron={"RIVALS": "Rivals", "Nosniy": "Noz-nee"})

# ---------------------------------------------------------------- 351 ROBLOX: Survive Your Ideas (Roblox API Nov 13)
SYC = "Clips: CaylusBlox; bunhat (Roblox gameplay, YouTube)"
clip("rb38-sy-a.mp4", "https://www.youtube.com/watch?v=mytlurN0Z4w", "*2:00-2:20", cut=0)
clip("rb38-sy-b.mp4", "https://www.youtube.com/watch?v=mytlurN0Z4w", "*6:00-6:20", cut=0)
clip("rb38-sy-c.mp4", "https://www.youtube.com/watch?v=NwdhA09eSQo", "*8:00-8:20", cut=0)
ep(351, "survive-your-ideas", "In This Roblox Game Every Word You Type Comes to Life", PUCK, "#00b0ff", RCAP("#80d8ff"),
   [L("This new fun game on Roblox makes every word you type come to life.",
      CLIP("rb38-sy-a.mp4", NEW, "SURVIVE YOUR IDEAS", 0, SYC, bs=130)),
    L("Every round, one random player types a word. Tsunami. Dinosaur. Nuke. And it happens.",
      CLIP("rb38-sy-b.mp4", "TYPE ANY\nWORD", "IT HAPPENS", 0, SYC, bs=150)),
    L("Then everyone has to survive it.",
      CLIP("rb38-sy-c.mp4", "SURVIVE", "", 0, SYC, bs=170)),
    L("It came out in October. It already has almost 75 million visits.",
      CCOUNT("rb38-sy-a.mp4", 7.0, SYC, 74875209, "VISITS", bs=120)),
    ask("What word would you type?", "YOUR\nWORD?", "rb38-sy-b.mp4", SYC, 7.0),
   ])

# ---------------------------------------------------------------- 352 TRENDING: GTA 6 police remember you (Extended Look, Aug 27 2026)
GTC = "Clips: TGG; Hollow (YouTube)"
clip("tr38-gt-a.mp4", "https://www.youtube.com/watch?v=FgJRIzc6LPw", "*1:00-1:20", cut=0)
clip("tr38-gt-b.mp4", "https://www.youtube.com/watch?v=FgJRIzc6LPw", "*4:00-4:20", cut=0)
clip("tr38-gt-c.mp4", "https://www.youtube.com/watch?v=wiW1mpHZb_Y", "*2:00-2:20", cut=0)
ep(352, "gta-6-police-remember-you", "In GTA 6 the Police Remember What You Wore", MIKE, "#ff4081",
   {"font": MF + "Bangers-Regular.ttf", "size": 120, "mode": "word", "fill": "#ffffff", "hi": "#ff80ab", "cy": 1470},
   [L("In GTA 6, the police remember what you were wearing.",
      CLIP("tr38-gt-c.mp4", "THEY\nREMEMBER", "GTA 6", 0, GTC, bs=150)),
    L("Rockstar showed it in a 26 minute gameplay video. Cops remember your clothes and your car.",
      CLIP("tr38-gt-b.mp4", "CLOTHES\n+ CAR", "26 MIN GAMEPLAY", 6.0, GTC, bs=150)),
    L("So to escape, you have to change your look. There's even a six star wanted level.",
      CLIP("tr38-gt-a.mp4", "6 STAR\nWANTED", "", 7.0, GTC, bs=150)),
    L("GTA 6 comes out November 19th. That's six days away.",
      CLIP("tr38-gt-a.mp4", "NOV 19", "6 DAYS", 7.0, GTC, bs=190)),
    ask("Are you buying it on day one?", "DAY\nONE?", "tr38-gt-c.mp4", GTC, 0.0),
    subline("tr38-gt-c.mp4", GTC, 7.0),
   ], edition="GAMING NEWS")

# ---------------------------------------------------------------- 353 TRENDING: Fortnite Pirate Shop token is shared with your squad
PSC = "Clips: Premfn; Osky (YouTube)"
clip("tr38-ps-a.mp4", "https://www.youtube.com/watch?v=ctd7HwxpbTg", "*5:00-5:20", cut=0)
clip("tr38-ps-b.mp4", "https://www.youtube.com/watch?v=ctd7HwxpbTg", "*10:00-10:20", cut=0)
clip("tr38-ps-c.mp4", "https://www.youtube.com/watch?v=kSGabojsC4I", "*6:00-6:20", cut=0)
ep(353, "fortnite-pirate-token-squad", "If Your Friend Finds This Fortnite Token You Get It Too", LIAM, "#ffd600",
   {"font": MF + "Bangers-Regular.ttf", "size": 120, "mode": "word", "fill": "#ffffff", "hi": "#fff59d", "cy": 1470},
   [L("If your friend finds this Fortnite token, you get it too.",
      CLIP("tr38-ps-a.mp4", "YOU GET\nIT TOO", "PIRATE SHOP TOKEN", 0, PSC, bs=150)),
    L("It's the Pirate Shop token. It makes the whole Item Shop free for 14 days.",
      CLIP("tr38-ps-b.mp4", "FREE SHOP", "14 DAYS", 0, PSC, bs=160)),
    L("And it's shared. If anyone in your party opens the chest, the whole squad gets it.",
      CLIP("tr38-ps-c.mp4", "WHOLE\nSQUAD", "", 0, PSC, bs=160)),
    L("So playing in a squad of four means four times the chances. You also get a second token for 2027.",
      CLIP("tr38-ps-a.mp4", "4X\nCHANCES", "+ A 2027 TOKEN", 7.0, PSC, bs=150)),
    ask("Who's in your squad?", "YOUR\nSQUAD?", "tr38-ps-b.mp4", PSC, 7.0),
    subline("tr38-ps-c.mp4", PSC, 7.0),
   ], edition="GAMING NEWS")

# ---------------------------------------------------------------- 354 MINECRAFT: title screen seed (r/Minecraft Jul 18 2020; Minecraft@Home)
TSC = "Clips: SalC1; Quiff (YouTube)"
clip("mc38-ts-a.mp4", "https://www.youtube.com/watch?v=GaRurhiK-Lk", "*1:00-1:20", cut=0)
clip("mc38-ts-b.mp4", "https://www.youtube.com/watch?v=GaRurhiK-Lk", "*5:00-5:20", cut=0)
clip("mc38-ts-c.mp4", "https://www.youtube.com/watch?v=-6ed0zOCZFA", "*1:00-1:20", cut=0)
ep(354, "minecraft-title-screen-seed", "Nobody Knew What World the Minecraft Title Screen Was", MIKE, "#66bb6a", RCAP("#b9f6ca"),
   [L("For years, nobody knew what world the Minecraft title screen was.",
      CLIP("mc38-ts-a.mp4", "WHAT\nWORLD?", "TITLE SCREEN", 0, TSC, bs=150)),
    L("That spinning background was used from Beta 1.8 all the way to 1.13.",
      CLIP("mc38-ts-b.mp4", "BETA 1.8\nTO 1.13", "", 0, TSC, bs=150)),
    L("In 2020, a group called Minecraft at Home threw thousands of computers at it.",
      CLIP("mc38-ts-c.mp4", "MINECRAFT\n@HOME", "2020", 0, TSC, bs=150)),
    L("Less than 24 hours later, on July 18th, they found it. About 93 days of computing, done in one day.",
      CLIP("mc38-ts-a.mp4", "FOUND", "JULY 18, 2020", 7.0, TSC, bs=170)),
    ask("Would you play on the title screen world?", "WOULD YOU\nPLAY IT?", "mc38-ts-b.mp4", TSC, 7.0),
   ], pron={"SalC1": "Sal C 1"}, edition="MINECRAFT")

# ---------------------------------------------------------------- 355 MEME: Low Taper Fade (plug for long-form #4)
LTC = "Clips: ericdoa; Ninja; clip pages (YouTube)"
clip("tr38-lt-a.mp4", "https://www.youtube.com/watch?v=ok5XRYhgH9Q", "*0:00-0:16", cut=0, ln=15)
clip("tr38-lt-b.mp4", "https://www.youtube.com/watch?v=zloi-MI3DuY", "*0:15-0:35", cut=0)
clip("tr38-lt-c.mp4", "https://www.youtube.com/watch?v=ryNMM5pMPr0", "*0:00-0:18", cut=0, ln=17)
ep(355, "low-taper-fade-sad-song", "The Low Taper Fade Meme Started in a Sad Song", PUCK, "#ffb300", MCAP("#ffe082"),
   [L("The low taper fade meme started in the middle of a sad song.",
      CLIP("tr38-lt-a.mp4", "IT STARTED\nSAD", "", 0, LTC, bs=150)),
    L("In January 2024, ericdoa was freestyling on Twitch. The stream got emotional. So he sang the funniest thing he could think of.",
      CLIP("tr38-lt-a.mp4", "JAN 5, 2024", "TWITCH", 6.0, LTC, bs=150),
      say="In January 2024, Eric D O A was freestyling on Twitch. The stream got emotional. So he sang the funniest thing he could think of."),
    L("Eight days later, Ninja actually got the haircut.",
      CLIP("tr38-lt-c.mp4", "HE DID IT", "JAN 13", 5.0, LTC, bs=160)),
    L("And then he kept calling the meme massive. For months.",
      CLIP("tr38-lt-c.mp4", "STILL\nMASSIVE", "", 10.0, LTC, bs=160)),
    ask("The full story is on my channel. Is it still massive?", "STILL\nMASSIVE?", "tr38-lt-a.mp4", LTC, 0.0),
   ], edition="MEME LORE")

# ================================================================== write
paths = []
for e in RB:
    e = dict(preset="roblox", hdr="tag", **e)
    words = sum(len(l.get("say", l["t"]).split()) for l in e["lines"])
    p = os.path.join("episodes", "roblox", e["slug"] + ".json")
    json.dump(e, open(os.path.join(ROOT, p), "w"), indent=1, ensure_ascii=False)
    paths.append(p)
    print(e["slug"], len(e["lines"]), "lines", words, "words")
manifest = {"batch": 38, "note": "Old Orochi, KILLSTEALER, andromeda, Clubstep, RIVALS S4, Survive Your Ideas, GTA 6 police, Pirate token squad, MC title screen, Low Taper Fade plug",
            "posting": "Z:/claudeprojects/roblox vids/batch-38/posting.txt", "episodes": paths, "clips": CLIPS}
json.dump(manifest, open(os.path.join(ROOT, "batches", "batch-38.json"), "w"), indent=1)
print(len(CLIPS), "clips")
