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




# ============================================================ BATCH 35 (Nov 10): analytics say GD stories are the steady winner
# (all 1,000+), old-Roblox big-number videos ~900, official-trailer / AI videos flop. No official trailers or music videos as clips.
def RCAP(hi):
    return {"font": MF + "Bangers-Regular.ttf", "size": 120, "mode": "word", "fill": "#ffffff", "hi": hi, "cy": 1470}

# ---------------------------------------------------------------- 316 GD: Kyouki (wiki.gg)
KYC = "Clips: Demishio; Spaceuk Archive (YouTube)"
clip("gd35-ky-a.mp4", "https://www.youtube.com/watch?v=KDa5c0CJTHs", "*9:40-10:00", cut=0)
clip("gd35-ky-b.mp4", "https://www.youtube.com/watch?v=KDa5c0CJTHs", "*3:00-3:20", cut=0)
clip("gd35-ky-c.mp4", "https://www.youtube.com/watch?v=64x4gPO-0lw", "*1:00-1:20", cut=0)
ep(316, "kyouki-501997-attempts", "One Player Took 501,997 Attempts on a Level He Made Himself", MIKE, "#ff1744", GDCAP,
   [L("One player spent half a million attempts on a level he built all by himself.",
      H("gd35-ky-c.mp4", "[501,997]\nKYOUKI", 0, KYC)),
    L("Demishio made Kyouki solo. Every single part.",
      H("gd35-ky-b.mp4", "[100% SOLO]\nDEMISHIO", 0, KYC)),
    L("He played it for 175 days. He died at 97 percent.",
      H("gd35-ky-b.mp4", "[175 DAYS]\n97% DEATH", 7.0, KYC)),
    L("In November 2022, he finally verified it.",
      HC("gd35-ky-a.mp4", 0, KYC, 501997, "ATTEMPTS - KYOUKI")),
    L("It went in at number 3. The hardest solo level in Geometry Dash.",
      H("gd35-ky-a.mp4", "[#3]\nHARDEST SOLO LEVEL", 7.0, KYC)),
    ask("Could you play one level for 175 days?", "175\nDAYS?", "gd35-ky-c.mp4", KYC),
    subline("gd35-ky-b.mp4", KYC, 4.0),
   ], pron=dict(GD_PRON, Kyouki="Kyoh-kee", Demishio="Deh-mee-shee-o"), gd_player="Demishio", **GDE)

# ---------------------------------------------------------------- 317 GD: Subsuming Vortex (wiki.gg)
SVC = "Clips: Cursed; Neiro (YouTube)"
clip("gd35-sv-a.mp4", "https://www.youtube.com/watch?v=0eYG1ogJpIQ", "*4:00-4:20", cut=0)
clip("gd35-sv-b.mp4", "https://www.youtube.com/watch?v=0eYG1ogJpIQ", "*1:00-1:20", cut=0)
clip("gd35-sv-c.mp4", "https://www.youtube.com/watch?v=CLzkb9YMMEg", "*0:20-0:40", cut=0)
ep(317, "subsuming-vortex-made-as-a-joke", "This Level Was Made as a Joke Then Took 7 Years to Beat", LIAM, "#7c4dff", GDCAP,
   [L("This level was made as a joke in 2018. It took seven years for anyone to verify it.",
      H("gd35-sv-c.mp4", "[A JOKE]\nSUBSUMING VORTEX", 0, SVC)),
    L("Subsuming Vortex was made to make fun of all the generic Nine Circles top 1 levels.",
      H("gd35-sv-b.mp4", "[NINE CIRCLES]\nPARODY", 0, SVC)),
    L("Then it became the hardest impossible level on the impossible levels list.",
      H("gd35-sv-b.mp4", "[IMPOSSIBLE]\nTOP 1", 7.0, SVC)),
    L("Cursed crashed past 53 percent 296 times. His worst fail was 96.",
      HC("gd35-sv-c.mp4", 7.0, SVC, 296, "CRASHES PAST 53%")),
    L("On November 10th, 2025, after about 85,000 attempts, he verified it. Exactly one year ago.",
      H("gd35-sv-a.mp4", "[VERIFIED]\nNOV 10, 2025", 0, SVC)),
    ask("Is it still a joke?", "STILL A\nJOKE?", "gd35-sv-c.mp4", SVC),
    subline("gd35-sv-b.mp4", SVC, 4.0),
   ], pron=dict(GD_PRON), gd_player="Cursed", **GDE)

# ---------------------------------------------------------------- 318 GD: Penumbral (wiki.gg)
PNC = "Clips: w3rty; Arth GD (YouTube)"
clip("gd35-pn-a.mp4", "https://www.youtube.com/watch?v=nVHPFf13M-I", "*1:20-1:40", cut=0)
clip("gd35-pn-b.mp4", "https://www.youtube.com/watch?v=wN80tDzbkkY", "*1:00-1:20", cut=0)
clip("gd35-pn-c.mp4", "https://www.youtube.com/watch?v=8FK9FvEjPts", "*0:30-0:50", cut=0)
ep(318, "penumbral-verified-in-12-days", "He Verified a Top 10 Level in 12 Days", FENRIR, "#00e5ff", GDCAP,
   [L("Most top levels take months to verify. This player did a top 10 level in 12 days.",
      H("gd35-pn-c.mp4", "[12 DAYS]\nPENUMBRAL", 0, PNC)),
    L("It's Penumbral, verified by w3rty.",
      H("gd35-pn-b.mp4", "[VERIFYING]\nW3RTY", 0, PNC)),
    L("It was supposed to be around top 10. And it pushed Slaughterhouse out of the top 25, after four and a half years.",
      H("gd35-pn-c.mp4", "[GOODBYE]\nSLAUGHTERHOUSE", 6.0, PNC)),
    L("Twelve days. That's it.",
      HC("gd35-pn-a.mp4", 0, PNC, 12, "DAYS TO VERIFY")),
    ask("How long would it take you?", "HOW\nLONG?", "gd35-pn-a.mp4", PNC, 7.0),
    subline("gd35-pn-b.mp4", PNC, 7.0),
   ], pron=dict(GD_PRON, w3rty="wur-tee"), gd_player="w3rty", **GDE)

# ---------------------------------------------------------------- 319 GD: wPopoff's rise (wiki.gg)
WPC = "Clips: wPopoff; Toogit (YouTube)"
clip("gd35-wp-a.mp4", "https://www.youtube.com/watch?v=WhP4bRHTR8A", "*4:40-5:00", cut=0)
clip("gd35-wp-b.mp4", "https://www.youtube.com/watch?v=5SV7VnDdUTk", "*3:00-3:20", cut=0)
clip("gd35-wp-c.mp4", "https://www.youtube.com/watch?v=4lfkzz1VCbA", "*2:25-2:45", cut=0)
ep(319, "wpopoff-slaughterhouse-to-grief", "3 Years Ago His Hardest Was Slaughterhouse Now He Beat GRIEF First", MIKE, "#00e676", GDCAP,
   [L("Three years ago, his hardest level was Slaughterhouse. This month, he beat the hardest level in the game. First.",
      H("gd35-wp-a.mp4", "[FIRST VICTOR]\nGRIEF", 0, WPC)),
    L("wPopoff made his YouTube channel in October 2022.",
      H("gd35-wp-b.mp4", "[2022]\nWPOPOFF", 0, WPC)),
    L("In 2023, he beat Slaughterhouse, Acheron, and Kenos. Kenos took him just three days.",
      H("gd35-wp-b.mp4", "[3 DAYS]\nKENOS", 7.0, WPC)),
    L("Then he verified Amethyst and Society. Both became number one.",
      H("gd35-wp-c.mp4", "[2 TOP 1s]\nAMETHYST + SOCIETY", 0, WPC, bs=64)),
    L("And on November 2nd, he beat GRIEF before anyone else. He's now the number 2 player in the world.",
      H("gd35-wp-a.mp4", "[#2 PLAYER]\nIN THE WORLD", 7.0, WPC)),
    ask("wPopoff or Zoink?", "WPOPOFF OR\nZOINK?", "gd35-wp-a.mp4", WPC),
    subline("gd35-wp-c.mp4", WPC, 7.0),
   ], pron=dict(GD_PRON), gd_player="wPopoff", **GDE)

# ---------------------------------------------------------------- 320 GD: Slaughterhouse's fall (wiki.gg, Pointercrate Nov 10)
SHC2 = "Clips: Doggie; Spaceuk Archive; Toogit (YouTube)"
clip("gd35-sh-a.mp4", "https://www.youtube.com/watch?v=kpcF1-QAHQc", "*1:50-2:10", cut=0)
clip("gd35-sh-b.mp4", "https://www.youtube.com/watch?v=CC7zfHByLSk", "*1:30-1:50", cut=0)
clip("gd35-sh-c.mp4", "https://www.youtube.com/watch?v=qUQZg6qd8SY", "*2:50-3:10", cut=0)
ep(320, "slaughterhouse-number-1-to-40", "This Was the Hardest Level in Geometry Dash Now Its Number 40", HEART, "#ff5252", GDCAP,
   [L("This was the hardest level in Geometry Dash. Today, it's number 40.",
      H("gd35-sh-a.mp4", "[#1 > #40]\nSLAUGHTERHOUSE", 0, SHC2)),
    L("In 2021, spaceuk claimed the verification. It was later found out he hacked it.",
      H("gd35-sh-b.mp4", "[HACKED]\nSPACEUK", 0, SHC2)),
    L("So the title went to Doggie, who really beat it in December 2021. It was number one for most of 2022.",
      H("gd35-sh-a.mp4", "[REAL VERIFIER]\nDOGGIE", 7.0, SHC2)),
    L("Then newer levels kept pushing it down. Out of the top 20. Out of the top 25.",
      HC("gd35-sh-b.mp4", 7.0, SHC2, 40, "DEMONLIST - SLAUGHTERHOUSE", fmt="#{:,.0f}")),
    L("And the new number one? GRIEF. A remake of the 2015 Slaughterhouse. Verified by Doggie.",
      H("gd35-sh-c.mp4", "[NEW TOP 1]\nGRIEF", 0, SHC2)),
    ask("Is Slaughterhouse still hard to you?", "STILL\nHARD?", "gd35-sh-a.mp4", SHC2),
    subline("gd35-sh-c.mp4", SHC2, 7.0),
   ], pron=dict(GD_PRON, spaceuk="space U K"), gd_player="Doggie", **GDE)

# ---------------------------------------------------------------- 321 GD: Anathema (wiki.gg)
ANC = "Clips: Whizkid05; MrWafflz (YouTube)"
clip("gd35-an-a.mp4", "https://www.youtube.com/watch?v=_uKwmjHmySI", "*4:50-5:10", cut=0)
clip("gd35-an-b.mp4", "https://www.youtube.com/watch?v=_uKwmjHmySI", "*1:30-1:50", cut=0)
clip("gd35-an-c.mp4", "https://www.youtube.com/watch?v=LFcX3d1w8dk", "*0:30-0:50", cut=0)
ep(321, "anathema-6-years-to-make", "This Level Took 6 Years to Make and Got Cancelled", LIAM, "#e040fb", GDCAP,
   [L("This level took six years to make. It got cancelled along the way.",
      H("gd35-an-c.mp4", "[6 YEARS]\nANATHEMA", 0, ANC)),
    L("Anathema started in 2017. The host cancelled it, and it was handed to someone else.",
      H("gd35-an-b.mp4", "[CANCELLED]\n2017-2023", 0, ANC)),
    L("Then it came back, and got buffed way past its first top 20 difficulty. Some players hated that.",
      H("gd35-an-b.mp4", "[BUFFED]\nPAST TOP 20", 7.0, ANC)),
    L("Whizkid05 verified it. Today it's number 24 on the Demonlist.",
      HC("gd35-an-a.mp4", 0, ANC, 24, "DEMONLIST - ANATHEMA", fmt="#{:,.0f}")),
    ask("Was 6 years worth it?", "WORTH\nIT?", "gd35-an-c.mp4", ANC),
    subline("gd35-an-a.mp4", ANC, 7.0),
   ], pron=dict(GD_PRON, Anathema="Uh-nath-uh-muh", Whizkid05="Whiz kid oh five"), gd_player="Whizkid05", **GDE)

# ---------------------------------------------------------------- 322 GD: Ashley Wave Trials (wiki.gg)
AWC = "Clips: Zoink; Nexus [GD] (YouTube)"
clip("gd35-aw-a.mp4", "https://www.youtube.com/watch?v=aTxt76U3e2Q", "*2:00-2:20", cut=0)
clip("gd35-aw-b.mp4", "https://www.youtube.com/watch?v=aTxt76U3e2Q", "*0:30-0:50", cut=0)
clip("gd35-aw-c.mp4", "https://www.youtube.com/watch?v=KrdMngKSLKc", "*0:40-1:00", cut=0)
ep(322, "ashley-wave-trials-couldnt-be-rated", "Zoink Beat This Level but It Couldnt Be Rated", FENRIR, "#ff4081", GDCAP,
   [L("Zoink verified this level. And it still couldn't be rated.",
      H("gd35-aw-c.mp4", "[UNRATED]\nASHLEY WAVE TRIALS", 0, AWC)),
    L("Ashley Wave Trials started as an impossible wave level. With a cartoon girl watching you the whole time.",
      H("gd35-aw-b.mp4", "[IMPOSSIBLE]\nWAVE LEVEL", 0, AWC)),
    L("It sat in open verification with barely any progress. Until Zoink came back from a break in 2024.",
      H("gd35-aw-b.mp4", "[ZOINK]\nIS BACK", 7.0, AWC)),
    L("He verified it in November 2024, using a click mod. So it couldn't be rated until RobTop added that feature to the game.",
      HC("gd35-aw-a.mp4", 0, AWC, 13677, "ATTEMPTS - VERIFIED")),
    ask("Should mods be allowed?", "MODS\nOK?", "gd35-aw-c.mp4", AWC),
    subline("gd35-aw-a.mp4", AWC, 7.0),
   ], pron=dict(GD_PRON, RobTop="Rob Top"), gd_player="Zoink", **GDE)

# ---------------------------------------------------------------- 323 GD: Menace (wiki.gg)
MNC = "Clips: Whizkid05 (YouTube)"
clip("gd35-mn-a.mp4", "https://www.youtube.com/watch?v=nnkgghxxsEE", "*3:40-4:00", cut=0)
clip("gd35-mn-b.mp4", "https://www.youtube.com/watch?v=nnkgghxxsEE", "*1:00-1:20", cut=0)
clip("gd35-mn-c.mp4", "https://www.youtube.com/watch?v=-wyvgP0NJs0", "*1:00-1:20", cut=0)
ep(323, "menace-sequel-could-be-top-5", "The Sequel to This Level Could Be Top 5", MIKE, "#ffab00", GDCAP,
   [L("This level is already one of the 30 hardest. Its sequel could be top 5.",
      H("gd35-mn-b.mp4", "[TOP 30]\nMENACE", 0, MNC)),
    L("Menace was one of the first top demons built around update 2.2. Swing duals. Robot sections.",
      H("gd35-mn-c.mp4", "[2.2]\nSWING DUALS", 0, MNC)),
    L("Whizkid05 verified it after 45,000 attempts.",
      HC("gd35-mn-a.mp4", 0, MNC, 45000, "ATTEMPTS - MENACE")),
    L("Now there's a sequel called Glass Chapel. It's projected top 5.",
      H("gd35-mn-a.mp4", "[SEQUEL]\nGLASS CHAPEL", 7.0, MNC)),
    ask("Would you play the sequel?", "SEQUEL?", "gd35-mn-b.mp4", MNC),
    subline("gd35-mn-c.mp4", MNC, 7.0),
   ], pron=dict(GD_PRON, Whizkid05="Whiz kid oh five"), gd_player="Whizkid05", **GDE)

# ---------------------------------------------------------------- 324 ROBLOX: Blox Fruits used to be Blox Piece (Rowatcher; live Roblox numbers Nov 10)
BFC = "Clips: WinterKloudz; Gamer Robot (Roblox gameplay, YouTube)"
clip("rb35-bf-a.mp4", "https://www.youtube.com/watch?v=O51JbL6nA48", "*5:00-5:20", cut=0)
clip("rb35-bf-b.mp4", "https://www.youtube.com/watch?v=XgnzZEG_jQ8", "*1:00-1:20", cut=0)
clip("rb35-bf-c.mp4", "https://www.youtube.com/watch?v=z-i1pAF6FjE", "*1:00-1:20", cut=0)
ep(324, "blox-fruits-was-blox-piece", "Blox Fruits Used to Have a Different Name", FENRIR, "#ff9100", RCAP("#ffd180"),
   [L("One of the biggest Roblox games ever used to have a different name. And it had to change it.",
      CLIP("rb35-bf-a.mp4", "A DIFFERENT\nNAME", "BLOX FRUITS", 0, BFC, bs=140)),
    L("When it came out in January 2019, it was called Blox Piece. Inspired by One Piece.",
      CLIP("rb35-bf-b.mp4", "BLOX\nPIECE", "JANUARY 2019", 0, BFC, bs=150)),
    L("By the end of 2019, it was renamed Blox Fruits, reportedly because of copyright pressure.",
      CLIP("rb35-bf-b.mp4", "RENAMED", "DECEMBER 2019", 7.0, BFC, bs=160)),
    L("Today it has over 65 billion visits.",
      CCOUNT("rb35-bf-a.mp4", 7.0, BFC, 65408602949, "VISITS", bs=120)),
    L("And over 260,000 people were playing it when I checked.",
      CLIP("rb35-bf-c.mp4", "260,000+\nPLAYING", "", 0, BFC, bs=150)),
    ask("What's your favorite fruit?", "BEST\nFRUIT?", "rb35-bf-a.mp4", BFC),
   ])

# ---------------------------------------------------------------- 325 MEME: "Will he perform" fail audio (Know Your Meme)
WHC = "Clips: Hall Of Fail; Contendo (YouTube)"
clip("tr35-wh-a.mp4", "https://www.youtube.com/watch?v=60TyBx9Mw9k", "*0:05-0:25", cut=0)
clip("tr35-wh-b.mp4", "https://www.youtube.com/watch?v=4MHEbwsahos", "*0:05-0:25", cut=0)
clip("tr35-wh-c.mp4", "https://www.youtube.com/watch?v=60TyBx9Mw9k", "*0:20-0:40", cut=0)
ep(325, "will-he-perform-meme", "The Will He Perform Meme Started With Wii Sports", PUCK, "#76ff03",
   {"font": MF + "Bangers-Regular.ttf", "size": 120, "mode": "word", "fill": "#ffffff", "hi": "#ccff90", "cy": 1470},
   [L("Will he perform when he has money right in front of him? This meme started with Wii Sports.",
      CLIP("tr35-wh-a.mp4", "\"WILL HE\nPERFORM?\"", "", 0, WHC, bs=140)),
    L("The audio is from a song by the rapper Remble. In August, someone put it over a Wii Sports bowling fail.",
      CLIP("tr35-wh-b.mp4", "WII SPORTS\nBOWLING", "", 0, WHC, bs=140)),
    L("The player misses every single pin, at the very last second.",
      CLIP("tr35-wh-c.mp4", "MISSED\nEVERY PIN", "", 0, WHC, bs=150)),
    L("Now the sound has been used over 53,000 times, mostly for fails.",
      CCOUNT("tr35-wh-a.mp4", 7.0, WHC, 53000, "VIDEOS", fmt="{:,.0f}+", bs=140)),
    ask("Would you perform?", "WOULD YOU\nPERFORM?", "tr35-wh-b.mp4", WHC, 7.0),
    subline("tr35-wh-c.mp4", WHC, 7.0),
   ], pron={"Remble": "Rem-bull"}, edition="MEME LORE")

# ================================================================== write
paths = []
for e in RB:
    e = dict(preset="roblox", hdr="tag", **e)
    words = sum(len(l.get("say", l["t"]).split()) for l in e["lines"])
    p = os.path.join("episodes", "roblox", e["slug"] + ".json")
    json.dump(e, open(os.path.join(ROOT, p), "w"), indent=1, ensure_ascii=False)
    paths.append(p)
    print(e["slug"], len(e["lines"]), "lines", words, "words")
manifest = {"batch": 35, "note": "Kyouki, Subsuming Vortex, Penumbral, wPopoff, Slaughterhouse fall, Anathema, AWT, Menace, Blox Fruits, Will he perform",
            "posting": "Z:/claudeprojects/roblox vids/batch-35/posting.txt", "episodes": paths, "clips": CLIPS}
json.dump(manifest, open(os.path.join(ROOT, "batches", "batch-35.json"), "w"), indent=1)
print(len(CLIPS), "clips")
