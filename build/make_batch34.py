"""Writes batch 34 (facts checked 2026-11-09): 5 OLD famous Roblox games (user: searchable classics) + 4 GD + GTA 6 = #306-315.
Mega-viral bets: #306 MeepCity (16B visits, ~85 players) and #315 GTA 6 (212 GB preload).

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



# ============================================================ BATCH 34 (user, Nov 9): old famous Roblox games people search for,
# GD stories (steadiest 1,000-1,700 views), and one big gaming-news bet. No AI memes (they flopped).
def RCAP(hi):
    return {"font": MF + "Bangers-Regular.ttf", "size": 120, "mode": "word", "fill": "#ffffff", "hi": hi, "cy": 1470}
OLD = dict()   # old games: no "THIS NEW FUN GAME" hook

# ---------------------------------------------------------------- 306 ROBLOX: MeepCity (live Roblox numbers Nov 9 11:45 AM ET; progameguides)
MPC = "Clips: dreflame; Milo (Roblox gameplay, YouTube)"
clip("rb34-mp-a.mp4", "https://www.youtube.com/watch?v=zeTXtut-HJI", "*2:00-2:20", cut=0)
clip("rb34-mp-b.mp4", "https://www.youtube.com/watch?v=Y4U_BwCLxls", "*3:00-3:20", cut=0)
clip("rb34-mp-c.mp4", "https://www.youtube.com/watch?v=zeTXtut-HJI", "*5:00-5:20", cut=0)
ep(306, "meepcity-16-billion-visits-85-players", "This Roblox Game Has 16 Billion Visits and Almost Nobody Plays It", FENRIR, "#ff4081", RCAP("#ff80ab"),
   [L("This Roblox game has over 16 billion visits. When I checked, only 85 people were playing it.",
      CCOUNT("rb34-mp-a.mp4", 0, MPC, 16279507056, "VISITS - MEEPCITY", bs=120)),
    L("It's MeepCity. It came out in 2016, and for years it was one of the biggest games on Roblox.",
      CLIP("rb34-mp-b.mp4", "MEEPCITY", "ONE OF ROBLOX'S BIGGEST", 0, MPC, bs=150)),
    L("Then, in February 2022, its parties were removed. That same day, the whole game disappeared from Roblox for a few hours.",
      CLIP("rb34-mp-c.mp4", "PARTIES\nREMOVED", "FEB 16, 2022", 0, MPC, bs=150)),
    L("The creator went quiet. And the players slowly left.",
      CLIP("rb34-mp-a.mp4", "THE PLAYERS\nLEFT", "", 7.0, MPC, bs=140)),
    L("16 billion visits. 85 players.",
      CLIP("rb34-mp-c.mp4", "16 BILLION\nVS 85", "", 7.0, MPC, bs=140)),
    ask("Did you ever play MeepCity?", "DID YOU\nPLAY IT?", "rb34-mp-b.mp4", MPC),
    subline("rb34-mp-a.mp4", MPC, 4.0),
   ], pron={"MeepCity": "Meep City"})

# ---------------------------------------------------------------- 307 ROBLOX: Jailbreak (Guinness World Records; live Roblox numbers)
JBC = "Clips: Denis; KreekCraft; VeD_DeV (Roblox gameplay, YouTube)"
clip("rb34-jb-a.mp4", "https://www.youtube.com/watch?v=qky3ajONpt0", "*3:00-3:20", cut=0)
clip("rb34-jb-b.mp4", "https://www.youtube.com/watch?v=9hrz9_XVKwY", "*1:00-1:20", cut=0)
clip("rb34-jb-c.mp4", "https://www.youtube.com/watch?v=ZfxYx_SC7wc", "*20:00-20:20", cut=0)
ep(307, "jailbreak-guinness-record", "Jailbreak Has a Guinness World Record", MIKE, "#ff9100", RCAP("#ffd180"),
   [L("This Roblox game is in the Guinness World Records. And it was made by just two people.",
      CLIP("rb34-jb-a.mp4", "A WORLD\nRECORD", "MADE BY 2 PEOPLE", 0, JBC, bs=150)),
    L("It's Jailbreak. Cops versus robbers. Escape the prison, rob the bank, and drive away.",
      CLIP("rb34-jb-b.mp4", "COPS VS\nROBBERS", "", 0, JBC, bs=150)),
    L("In March 2020, it had over 3.3 million likes. The most likes for any game made in Roblox.",
      CCOUNT("rb34-jb-a.mp4", 7.0, JBC, 3373726, "LIKES - GUINNESS RECORD", bs=130)),
    L("Today it has over 8 billion visits. And people still break out of that prison every day.",
      CLIP("rb34-jb-c.mp4", "8 BILLION\nVISITS", "STILL PLAYED TODAY", 0, JBC, bs=140)),
    ask("Cop or criminal?", "COP OR\nCRIMINAL?", "rb34-jb-a.mp4", JBC),
    subline("rb34-jb-c.mp4", JBC, 7.0),
   ])

# ---------------------------------------------------------------- 308 ROBLOX: Brookhaven (Business Wire Feb 2025; live Roblox numbers)
BKC = "Clips: IBella; SKH GAMING (Roblox gameplay, YouTube)"
clip("rb34-bk-a.mp4", "https://www.youtube.com/watch?v=u8cs_KSSP3k", "*2:00-2:20", cut=0)
clip("rb34-bk-b.mp4", "https://www.youtube.com/watch?v=u8cs_KSSP3k", "*8:00-8:20", cut=0)
clip("rb34-bk-c.mp4", "https://www.youtube.com/watch?v=jRuSrlXN7gw", "*10:00-10:20", cut=0)
ep(308, "brookhaven-almost-90-billion", "Brookhaven Is About to Hit 90 Billion Visits", HEART, "#00e5ff", RCAP("#84ffff"),
   [L("The most visited game on Roblox is about to hit 90 billion visits.",
      CCOUNT("rb34-bk-a.mp4", 0, BKC, 89368300790, "VISITS - BROOKHAVEN", bs=120)),
    L("It's Brookhaven. It came out in April 2020, made by a creator called Wolfpaq.",
      CLIP("rb34-bk-c.mp4", "BROOKHAVEN", "BY WOLFPAQ - 2020", 6.0, BKC, bs=150)),
    L("In February 2025, Wolfpaq sold it to a company called Voldex. Back then it had about 60 billion visits.",
      CLIP("rb34-bk-c.mp4", "SOLD", "AT ~60 BILLION VISITS", 0, BKC, bs=160)),
    L("Since then? Almost 30 billion more. And right now, almost 400,000 people are playing it.",
      CLIP("rb34-bk-a.mp4", "+30 BILLION", "~400,000 PLAYING NOW", 7.0, BKC, bs=140)),
    ask("What's your house in Brookhaven?", "YOUR\nHOUSE?", "rb34-bk-a.mp4", BKC),
    subline("rb34-bk-c.mp4", BKC, 7.0),
   ], pron={"Wolfpaq": "Wolf pack", "Voldex": "Vol dex"})

# ---------------------------------------------------------------- 309 ROBLOX: Adopt Me (Wikipedia; live Roblox numbers)
AMC3 = "Clips: Alaska Violet; Cookie Cutter (Roblox gameplay, YouTube)"
clip("rb34-ad-a.mp4", "https://www.youtube.com/watch?v=yJ7mMhhnSOg", "*3:00-3:20", cut=0)
clip("rb34-ad-b.mp4", "https://www.youtube.com/watch?v=yJ7mMhhnSOg", "*10:00-10:20", cut=0)
clip("rb34-ad-c.mp4", "https://www.youtube.com/watch?v=zF2QIQJTjT8", "*2:00-2:20", cut=0)
ep(309, "adopt-me-1-92-million-players", "Adopt Me Once Had 1.92 Million Players at Once", LIAM, "#76ff03", RCAP("#ccff90"),
   [L("A Roblox game about adopting pets once had more players than the biggest game on Steam.",
      CLIP("rb34-ad-a.mp4", "BIGGER\nTHAN STEAM", "ADOPT ME!", 0, AMC3, bs=150)),
    L("In April 2020, Adopt Me hit 680,000 players. Three times more than the top game on Steam.",
      CCOUNT("rb34-ad-b.mp4", 0, AMC3, 680000, "PLAYERS - APRIL 2020", bs=130)),
    L("A year later, it hit its record. 1.92 million players at once.",
      CCOUNT("rb34-ad-c.mp4", 0, AMC3, 1920000, "PLAYERS AT ONCE - RECORD", bs=130)),
    L("One six year old in Australia spent 8,000 dollars on it, on an iPad.",
      CLIP("rb34-ad-a.mp4", "$8,000", "ONE 6-YEAR-OLD - AUSTRALIA", 7.0, AMC3, bs=170)),
    L("Today it has over 45 billion visits, and over 200,000 people still play it.",
      CLIP("rb34-ad-b.mp4", "45 BILLION\nVISITS", "200,000+ STILL PLAYING", 7.0, AMC3, bs=140)),
    ask("What's your best pet?", "BEST\nPET?", "rb34-ad-a.mp4", AMC3),
    subline("rb34-ad-c.mp4", AMC3, 7.0),
   ])

# ---------------------------------------------------------------- 310 ROBLOX: Crossroads (live Roblox numbers)
CRC = "Clips: Rob6304; Wurtel99; Roblox (YouTube)"
clip("rb34-cr-a.mp4", "https://www.youtube.com/watch?v=9x-CsTAspfE", "*1:00-1:20", cut=0)
clip("rb34-cr-b.mp4", "https://www.youtube.com/watch?v=RzRABRCzEno", "*2:00-2:20", cut=0)
clip("rb34-cr-c.mp4", "https://www.youtube.com/watch?v=tyRxtNBaK0Y", "*0:10-0:30", cut=0)
ep(310, "crossroads-2007-still-played", "This Roblox Game Is From 2007 and People Still Play It", PUCK, "#ffd600", RCAP("#ffff8d"),
   [L("This Roblox game was made in 2007, by Roblox itself. And people are still playing it.",
      CLIP("rb34-cr-a.mp4", "FROM\n2007", "MADE BY ROBLOX", 0, CRC, bs=150)),
    L("It's Crossroads. A sword fighting map from the very early days of Roblox.",
      CLIP("rb34-cr-c.mp4", "CROSSROADS", "", 0, CRC, bs=150)),
    L("It has almost 40 million visits.",
      CCOUNT("rb34-cr-b.mp4", 0, CRC, 39943413, "VISITS", bs=130)),
    L("When I checked, 14 people were in there. Still fighting, 19 years later.",
      CLIP("rb34-cr-a.mp4", "14 PLAYERS", "19 YEARS LATER", 7.0, CRC, bs=150)),
    ask("What's the oldest Roblox game you played?", "YOUR\nOLDEST?", "rb34-cr-b.mp4", CRC),
    subline("rb34-cr-c.mp4", CRC, 7.0),
   ])

# ---------------------------------------------------------------- 311 GD: BOOBAWAMBA (wiki.gg)
BBC = "Clips: EastShark1; Zoink (YouTube)"
clip("gd34-bb-a.mp4", "https://www.youtube.com/watch?v=20fYiqLAo_E", "*2:30-2:50", cut=0)
clip("gd34-bb-b.mp4", "https://www.youtube.com/watch?v=20fYiqLAo_E", "*0:40-1:00", cut=0)
clip("gd34-bb-c.mp4", "https://www.youtube.com/watch?v=DXV7CVkos7I", "*36:00-36:20", cut=0)
ep(311, "boobawamba-175282-attempts", "It Took 175,282 Attempts Then Zoink Did It in 7,946", MIKE, "#00e676", GDCAP,
   [L("It took one player 175,282 attempts to verify this level. Then Zoink beat it in 7,946.",
      H("gd34-bb-b.mp4", "[175,282]\nBOOBAWAMBA", 0, BBC)),
    L("It's BOOBAWAMBA. It's green and grey, so you can barely see what's coming.",
      H("gd34-bb-b.mp4", "[CAN'T SEE]\nGREEN + GREY", 6.0, BBC)),
    L("EastShark1 verified it in October 2024. Then nobody else beat it for over 430 days.",
      H("gd34-bb-a.mp4", "[430 DAYS]\nNO ONE BEAT IT", 0, BBC)),
    L("And in March 2026, Zoink did it. By far the fewest attempts ever.",
      HC("gd34-bb-c.mp4", 0, BBC, 7946, "ZOINK - ATTEMPTS")),
    ask("How is Zoink this good?", "HOW?!", "gd34-bb-b.mp4", BBC),
    subline("gd34-bb-c.mp4", BBC, 7.0),
   ], pron=dict(GD_PRON, BOOBAWAMBA="Boo-ba-wam-ba", EastShark1="East Shark one"), gd_player="EastShark1", **GDE)

# ---------------------------------------------------------------- 312 GD: Quanteuse processing (wiki.gg)
QPC = "Clips: Zoink; Nexus [GD] (YouTube)"
clip("gd34-qp-a.mp4", "https://www.youtube.com/watch?v=sRUO72zI2GQ", "*0:40-1:00", cut=0)
clip("gd34-qp-b.mp4", "https://www.youtube.com/watch?v=j5NC0u1Q91Q", "*17:00-17:20", cut=0)
clip("gd34-qp-c.mp4", "https://www.youtube.com/watch?v=sRUO72zI2GQ", "*1:20-1:40", cut=0)
ep(312, "quanteuse-processing-worst-level", "One of the Worst Levels of 2025 Is One of the Hardest", LIAM, "#ff5252", GDCAP,
   [L("This was ranked one of the worst extreme demons of 2025. It's also one of the hardest.",
      H("gd34-qp-a.mp4", "[WORST OF 2025]\nQUANTEUSE", 0, QPC)),
    L("Quanteuse processing is a joke remake of Quantum Processing. Made way harder.",
      H("gd34-qp-c.mp4", "[JOKE REMAKE]\nQUANTUM PROCESSING", 0, QPC, bs=64)),
    L("Zoink verified it. Then it sat unrated for almost a year, until he asked RobTop on stream.",
      H("gd34-qp-c.mp4", "[UNRATED]\nALMOST 1 YEAR", 6.0, QPC)),
    L("It went in at number 6, and kicked Silent Clubstep out of the top 10, after three and a half years.",
      HC("gd34-qp-a.mp4", 7.0, QPC, 6, "DEMONLIST PLACEMENT", fmt="#{:,.0f}")),
    ask("Bad level, or just hard?", "BAD OR\nHARD?", "gd34-qp-a.mp4", QPC),
    subline("gd34-qp-c.mp4", QPC, 7.0),
   ], pron=dict(GD_PRON, Quanteuse="Kwan-tuhz", RobTop="Rob Top"), gd_player="Zoink", **GDE)

# ---------------------------------------------------------------- 313 GD: Heliopolis, the cursed verification (wiki.gg)
HLC = "Clips: Nexus [GD]; MindCap; Zoink (YouTube)"
clip("gd34-hl-a.mp4", "https://www.youtube.com/watch?v=wvwZaW2xLiw", "*0:40-1:00", cut=0)
clip("gd34-hl-b.mp4", "https://www.youtube.com/watch?v=7yaKGl_2Dsw", "*1:20-1:40", cut=0)
clip("gd34-hl-c.mp4", "https://www.youtube.com/watch?v=gO1nQECPU2I", "*2:20-2:40", cut=0)
ep(313, "heliopolis-cursed-verification", "Five Players Tried to Verify This Level and None Finished", FENRIR, "#ffab00", GDCAP,
   [L("Five players have tried to verify this level. Not one of them has finished it.",
      H("gd34-hl-a.mp4", "[5 VERIFIERS]\nHELIOPOLIS", 0, HLC)),
    L("Heliopolis is a pure timing level by MindCap. Pablohh dropped it. Jif got kicked.",
      H("gd34-hl-b.mp4", "[DROPPED]\nPABLOHH - JIF", 0, HLC)),
    L("Thnnder spent over 108,000 attempts on it, then had to quit for health reasons.",
      HC("gd34-hl-b.mp4", 7.0, HLC, 108000, "THNNDER - ATTEMPTS")),
    L("MindCap put a 10,700 dollar bounty on it. Zoink's best is 85 percent.",
      H("gd34-hl-c.mp4", "[$10,700]\nZOINK 85%", 0, HLC)),
    ask("Is this level cursed?", "CURSED?", "gd34-hl-a.mp4", HLC),
    subline("gd34-hl-c.mp4", HLC, 7.0),
   ], pron=dict(GD_PRON, MindCap="Mind Cap", Pablohh="Pablo", Thnnder="Thunder", Heliopolis="Heel-ee-op-olis"), gd_player="Thnnder", **GDE)

# ---------------------------------------------------------------- 314 GD: Artemis 13 (wiki.gg, Pointercrate Nov 7)
ARC = "Clips: Zoink; gdclipsanddips (YouTube)"
clip("gd34-ar-a.mp4", "https://www.youtube.com/watch?v=FgjOM0ef1N8", "*2:50-3:10", cut=0)
clip("gd34-ar-b.mp4", "https://www.youtube.com/watch?v=FgjOM0ef1N8", "*1:00-1:20", cut=0)
clip("gd34-ar-c.mp4", "https://www.youtube.com/watch?v=vk7a0-VwpqM", "*0:40-1:00", cut=0)
ep(314, "artemis-13-nerfed-still-number-2", "Zoink Nerfed This Level and Its Still Number 2", MIKE, "#2979ff", GDCAP,
   [L("Zoink made this level easier. It's still the second hardest level in the game.",
      H("gd34-ar-a.mp4", "[NERFED]\nARTEMIS 13", 0, ARC)),
    L("Artemis 13 was supposed to be top 1 to 3. Zoink got to 79 percent.",
      H("gd34-ar-b.mp4", "[79%]\nVERIFYING", 0, ARC)),
    L("Then he reportedly nerfed it, to top 5 or 10 difficulty.",
      H("gd34-ar-b.mp4", "[NERF]\nTOP 5-10?", 7.0, ARC)),
    L("He verified it on September 9th, 2026. Today it sits at number 2.",
      HC("gd34-ar-a.mp4", 7.0, ARC, 2, "DEMONLIST - ARTEMIS 13", fmt="#{:,.0f}")),
    ask("Should he have nerfed it?", "NERF\nOR NOT?", "gd34-ar-c.mp4", ARC),
    subline("gd34-ar-c.mp4", ARC, 7.0),
   ], pron=dict(GD_PRON), gd_player="Zoink", **GDE)

# ---------------------------------------------------------------- 315 NEWS: GTA 6 preload / file size (Beebom, Shacknews: Rockstar-confirmed preload + up to 212 GB)
GTC = "Clips: Rockstar Games (official trailers)"
clip("tr34-gt-a.mp4", "https://www.youtube.com/watch?v=rz1B4B2yBZY", "*0:10-0:30", cut=0)
clip("tr34-gt-b.mp4", "https://www.youtube.com/watch?v=rz1B4B2yBZY", "*0:50-1:10", cut=0)
clip("tr34-gt-c.mp4", "https://www.youtube.com/watch?v=VQRLujxTm3c", "*1:30-1:50", cut=0)
ep(315, "gta-6-212-gb-preload", "GTA 6 Is So Big You Might Have to Delete Your Games", MIKE, "#ff4081",
   {"font": MF + "Bangers-Regular.ttf", "size": 120, "mode": "word", "fill": "#ffffff", "hi": "#ff80ab", "cy": 1470},
   [L("GTA 6 is so big, you might have to delete half your games to install it.",
      CLIP("tr34-gt-a.mp4", "DELETE YOUR\nGAMES", "GTA 6", 0, GTC, bs=130)),
    L("Rockstar says it's up to 212 gigabytes, depending on your console.",
      CCOUNT("tr34-gt-b.mp4", 0, GTC, 212, "GB - UP TO", fmt="{:,.0f} GB", bs=160)),
    L("Preloading starts this week, so it's ready the second it unlocks.",
      CLIP("tr34-gt-c.mp4", "PRELOAD\nTHIS WEEK", "", 0, GTC, bs=150)),
    L("And it comes out November 19th, on PS5 and Xbox Series X and S.",
      CLIP("tr34-gt-a.mp4", "NOVEMBER\n19", "PS5 - XBOX SERIES X|S", 7.0, GTC, bs=150)),
    ask("What are you deleting for GTA 6?", "WHAT ARE\nYOU DELETING?", "tr34-gt-b.mp4", GTC, 7.0),
    subline("tr34-gt-c.mp4", GTC, 7.0),
   ], pron={"GTA": "G T A", "PS5": "P S 5"}, edition="GTA 6")

# ================================================================== write
paths = []
for e in RB:
    e = dict(preset="roblox", hdr="tag", **e)
    words = sum(len(l.get("say", l["t"]).split()) for l in e["lines"])
    p = os.path.join("episodes", "roblox", e["slug"] + ".json")
    json.dump(e, open(os.path.join(ROOT, p), "w"), indent=1, ensure_ascii=False)
    paths.append(p)
    print(e["slug"], len(e["lines"]), "lines", words, "words")
manifest = {"batch": 34, "note": "MeepCity, Jailbreak, Brookhaven, Adopt Me, Crossroads, BOOBAWAMBA, Quanteuse, Heliopolis, Artemis 13, GTA 6",
            "posting": "Z:/claudeprojects/roblox vids/batch-34/posting.txt", "episodes": paths, "clips": CLIPS}
json.dump(manifest, open(os.path.join(ROOT, "batches", "batch-34.json"), "w"), indent=1)
print(len(CLIPS), "clips")
