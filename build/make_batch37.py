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
                   **dict(dict(lead=1.7, tail=0.5, clip_audio=True), **k)))


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


# ============================================================ BATCH 37 (Nov 12): new lanes plan (user, Nov 12).
# 97.8% new viewers / 1% subscriber watch time -> named series + 2-part cliffhanger stories that send viewers to the channel page.
# GAME MYSTERIES: dark ambience bed (music.py "ambience"), Part 1 cuts off right at the reveal + "PART 2 ON MY PAGE" card,
# Part 2 is posted ~30 min BEFORE Part 1 so it's already on the page. Not used on GD.
MYCAP = {"font": MF + "Bangers-Regular.ttf", "size": 118, "mode": "word", "fill": "#ffffff", "hi": "#ff5252", "cy": 1470}
MYS = dict(edition="GAME MYSTERIES", mood="ambience", music_vol=0.45, clip_duck=0.18)
def part2(name, credit, start=0.0):
    """Cliffhanger ending: hard cut to the Part 2 card (the line before it stops mid-reveal)."""
    return L("Part 2 is on my page.", CLIP(name, "PART 2", "ON MY PAGE", start, credit, bs=190, ss=64))
def recap(say, name, head, credit, start=0.0):
    return L(say, H(name, head, start, credit))

# ---------------------------------------------------------------- 336 MYSTERY: Polybius part 1 (Wikipedia)
PBC = "Clips: Push Square; Nostalgia Nerd; Gaming Historian (YouTube)"
clip("my37-pb-a.mp4", "https://www.youtube.com/watch?v=XHhMcJHYtBU", "*1:00-1:20", cut=0)
clip("my37-pb-b.mp4", "https://www.youtube.com/watch?v=TD1MBrkfEM0", "*0:30-0:50", cut=0)
clip("my37-pb-c.mp4", "https://www.youtube.com/watch?v=4gLypLPTljg", "*1:00-1:20", cut=0)
clip("my37-pb-d.mp4", "https://www.youtube.com/watch?v=4gLypLPTljg", "*4:00-4:20", cut=0)
ep(336, "polybius-part-1", "The Arcade Game That Vanished in 1981 Part 1", FENRIR, "#ff1744", MYCAP,
   [L("In 1981, an arcade game showed up in Portland, Oregon. Then it vanished.",
      H("my37-pb-a.mp4", "[GAME MYSTERIES #1]\nPOLYBIUS", 0, PBC)),
    L("It was called Polybius. A black cabinet, with strange flashing shapes.",
      H("my37-pb-b.mp4", "[1981]\nPORTLAND, OREGON", 0, PBC)),
    L("Kids lined up to play it. Then the stories started. Seizures. Nightmares. Memory loss.",
      H("my37-pb-a.mp4", "[SEIZURES]\nNIGHTMARES", 7.0, PBC)),
    L("At night, men in black suits came to the machines. They didn't take the coins. They took data.",
      H("my37-pb-c.mp4", "[MEN IN BLACK]\nTOOK THE DATA", 0, PBC)),
    L("Within weeks, every machine was gone. No company. No record. Nothing.",
      H("my37-pb-d.mp4", "[GONE]\nNO RECORD", 0, PBC)),
    L("But in 1981, something real did happen at those arcades. And it started with",
      H("my37-pb-a.mp4", "[WHAT REALLY\nHAPPENED?]", 4.0, PBC)),
    part2("my37-pb-b.mp4", PBC, 7.0),
   ], pron={"Polybius": "Puh-libby-us"}, tail=0.3, **MYS)

# ---------------------------------------------------------------- 337 MYSTERY: Polybius part 2 (Wikipedia)
clip("my37-pb-e.mp4", "https://www.youtube.com/watch?v=4gLypLPTljg", "*5:30-5:50", cut=0)
ep(337, "polybius-part-2", "The Arcade Game That Vanished in 1981 Part 2", FENRIR, "#ff1744", MYCAP,
   [recap("Part 2. Polybius vanished. But real things happened in Portland in 1981.",
          "my37-pb-a.mp4", "[PART 2]\nPOLYBIUS", PBC),
    L("A teenager got a migraine playing Tempest, and was found passed out in a stranger's yard.",
      H("my37-pb-c.mp4", "[TEMPEST]\nPASSED OUT", 7.0, PBC)),
    L("Another kid played Asteroids for 28 hours straight for a record, and got sick.",
      HC("my37-pb-d.mp4", 7.0, PBC, 28, "HOURS OF ASTEROIDS")),
    L("Ten days later, the FBI raided Portland arcades. Agents watched the machines and wrote down high scores.",
      H("my37-pb-e.mp4", "[FBI RAIDS]\nPORTLAND", 0, PBC)),
    L("They were hunting illegal gambling machines. So the men in black were real. Just not who people thought.",
      H("my37-pb-e.mp4", "[THE MEN\nIN BLACK]", 7.0, PBC)),
    L("And Polybius? No 1980s newspaper ever mentioned it. The first trace is a website note around 2000. Anyone heard of this game?",
      H("my37-pb-b.mp4", "[NO RECORD]\nUNTIL 2000", 0, PBC)),
    ask("Do you think Polybius was real?", "REAL?", "my37-pb-a.mp4", PBC),
    subline("my37-pb-b.mp4", PBC, 7.0),
   ], pron={"Polybius": "Puh-libby-us"}, **MYS)

# ---------------------------------------------------------------- 338 MYSTERY: P.T. part 1 (Wikipedia)
PTC = "Clips: P.T. gameplay - Shirrako; Outstar; SVG (YouTube)"
clip("my37-pt-a.mp4", "https://www.youtube.com/watch?v=YbaTFXlBllI", "*2:00-2:20", cut=0)
clip("my37-pt-b.mp4", "https://www.youtube.com/watch?v=YbaTFXlBllI", "*8:00-8:20", cut=0)
clip("my37-pt-c.mp4", "https://www.youtube.com/watch?v=zNdKnJg9dEY", "*0:20-0:40", cut=0)
clip("my37-pt-d.mp4", "https://www.youtube.com/watch?v=zNdKnJg9dEY", "*1:30-1:50", cut=0)
ep(338, "pt-part-1", "The Scariest Free Game Was Made by a Studio That Didnt Exist Part 1", LIAM, "#b71c1c", MYCAP,
   [L("In 2014, a free horror game appeared on PlayStation. From a studio nobody had ever heard of.",
      H("my37-pt-a.mp4", "[GAME MYSTERIES #2]\nP.T.", 0, PTC)),
    L("It was called P.T. You walk down one hallway. Over and over. And every loop, something changes.",
      H("my37-pt-b.mp4", "[ONE HALLWAY]\nFOREVER", 0, PTC)),
    L("A radio talks about a family murder. A voice keeps repeating the same numbers.",
      H("my37-pt-a.mp4", "[204863]", 7.0, PTC)),
    L("And a ghost named Lisa follows you. If she catches you, you start over.",
      H("my37-pt-c.mp4", "[LISA]\nIS BEHIND YOU", 0, PTC)),
    L("The studio was called 7780s Studio. It didn't exist.",
      H("my37-pt-d.mp4", "[7780s STUDIO]\nDIDN'T EXIST", 0, PTC)),
    L("When players finally solved the last puzzle, they found out who really made it. It was",
      H("my37-pt-b.mp4", "[WHO MADE IT?]", 7.0, PTC)),
    part2("my37-pt-c.mp4", PTC, 7.0),
   ], pron={"P.T.": "P T", "7780s": "seventy seven eighty's"}, tail=0.3, **MYS)

# ---------------------------------------------------------------- 339 MYSTERY: P.T. part 2 (Wikipedia)
clip("my37-pt-e.mp4", "https://www.youtube.com/watch?v=YbaTFXlBllI", "*21:00-21:20", cut=0)
clip("my37-pt-f.mp4", "https://www.youtube.com/watch?v=0bGI3ut3vBg", "*1:00-1:20", cut=0)
ep(339, "pt-part-2", "The Scariest Free Game Was Made by a Studio That Didnt Exist Part 2", LIAM, "#b71c1c", MYCAP,
   [recap("Part 2. P.T. came from a fake studio. And the real answer shocked everyone.",
          "my37-pt-c.mp4", "[PART 2]\nP.T.", PTC),
    L("It was a teaser for a new Silent Hill game. Silent Hills. By Hideo Kojima and Guillermo del Toro, starring Norman Reedus.",
      H("my37-pt-e.mp4", "[SILENT HILLS]\nKOJIMA + DEL TORO", 0, PTC)),
    L("Over a million people downloaded it.",
      HC("my37-pt-a.mp4", 7.0, PTC, 1000000, "DOWNLOADS", fmt="{:,.0f}+")),
    L("Then in April 2015, Silent Hills was cancelled. And P.T. was pulled from the PlayStation Store.",
      H("my37-pt-f.mp4", "[CANCELLED]\nAPRIL 2015", 0, PTC)),
    L("Now you can't download it again. PS4s with P.T. still installed were listed on eBay for over 1,000 dollars.",
      H("my37-pt-d.mp4", "[$1,000+]\nFOR A PS4", 0, PTC)),
    ask("Would you play P.T. alone at night?", "ALONE?", "my37-pt-c.mp4", PTC),
    subline("my37-pt-b.mp4", PTC, 7.0),
   ], pron={"P.T.": "P T", "Kojima": "Ko-jee-ma", "Reedus": "Ree-dus"}, **MYS)

# ---------------------------------------------------------------- 340 ROBLOX MYSTERY: John Doe (Roblox wiki, Roblox blog via press)
JDC = "Clips: Roblox videos - RageElixir; BeepinHam (YouTube)"
clip("rb37-jd-a.mp4", "https://www.youtube.com/watch?v=e7FqUsrX4Vs", "*2:00-2:20", cut=0)
clip("rb37-jd-b.mp4", "https://www.youtube.com/watch?v=e7FqUsrX4Vs", "*8:00-8:20", cut=0)
clip("rb37-jd-c.mp4", "https://www.youtube.com/watch?v=Q0nujJ1g88E", "*0:00-0:20", cut=0)
ep(340, "john-doe-march-18", "This Roblox Account Was Supposed to Hack Roblox on March 18", PUCK, "#ff5252", MYCAP,
   [L("This Roblox account was last online on March 18th. And players thought he'd come back on that day to hack Roblox.",
      H("rb37-jd-c.mp4", "[GAME MYSTERIES]\nJOHN DOE", 0, JDC)),
    L("John Doe and Jane Doe are two of the oldest accounts on Roblox. John is user number 2.",
      H("rb37-jd-a.mp4", "[USER #2]\nJOHN DOE", 0, JDC)),
    L("In 2017, a rumor spread that they would hack Roblox on March 18. Clickbait videos made it huge.",
      H("rb37-jd-b.mp4", "[MARCH 18]\nTHE HACK", 0, JDC)),
    L("Players were scared to log in. Then March 18 came, and nothing happened.",
      H("rb37-jd-a.mp4", "[NOTHING\nHAPPENED]", 7.0, JDC)),
    L("The truth? Roblox's founders made them in 2005, as test accounts.",
      H("rb37-jd-b.mp4", "[2005]\nTEST ACCOUNTS", 7.0, JDC)),
    L("Every March 18, players still dress up like John and Jane Doe.",
      H("rb37-jd-c.mp4", "[EVERY\nMARCH 18]", 7.0, JDC)),
    ask("Were you scared of March 18?", "SCARED?", "rb37-jd-c.mp4", JDC),
   ], pron={"Baszucki": "Bah-zoo-key"}, edition="GAME MYSTERIES", mood="ambience", music_vol=0.4)

# ---------------------------------------------------------------- 341 MINECRAFT: pack.png seed (Reddit r/MinecraftAtHome, minecraft.wiki, PC Gamer)
PKC = "Clips: SalC1; 07 Archives (YouTube)"
clip("mc37-pk-a.mp4", "https://www.youtube.com/watch?v=ea6py9q46QU", "*1:00-1:20", cut=0)
clip("mc37-pk-b.mp4", "https://www.youtube.com/watch?v=ea6py9q46QU", "*6:00-6:20", cut=0)
clip("mc37-pk-c.mp4", "https://www.youtube.com/watch?v=fr4Iw74ZWxk", "*3:00-3:20", cut=0)
ep(341, "minecraft-pack-png-seed", "It Took 8 Months to Find Where This Minecraft Picture Was Taken", MIKE, "#66bb6a", RCAP("#b9f6ca"),
   [L("This picture has been in Minecraft for years. It took 8 months to find out where it was taken.",
      CLIP("mc37-pk-a.mp4", "8 MONTHS", "PACK.PNG", 0, PKC, bs=160)),
    L("It's called pack.png. The default pack icon. A screenshot from one old Minecraft world.",
      CLIP("mc37-pk-b.mp4", "PACK.PNG", "ONE SCREENSHOT", 0, PKC, bs=150)),
    L("In January 2020, the YouTuber SalC1 asked a simple question. What world is this? Seed hunters got to work.",
      CLIP("mc37-pk-c.mp4", "WHAT WORLD\nIS THIS?", "JANUARY 2020", 0, PKC, bs=140)),
    L("Checking every possible seed would take almost a year and a half of computing.",
      CLIP("mc37-pk-b.mp4", "1.5 YEARS", "OF COMPUTING", 7.0, PKC, bs=150)),
    L("On September 5th, 2020, the alarm went off. The seed was in the last 5 percent they checked.",
      CLIP("mc37-pk-a.mp4", "FOUND", "SEPTEMBER 5, 2020", 7.0, PKC, bs=170)),
    ask("Would you visit the pack.png world?", "WOULD YOU\nVISIT?", "mc37-pk-c.mp4", PKC, 7.0),
   ], pron={"SalC1": "Sal C 1", "pack.png": "pack P N G"}, edition="MINECRAFT")

# ---------------------------------------------------------------- 342 IMPOSSIBLE FEATS: half an A press (Wikipedia)
ABC = "Clips: pannenkoek2012 (YouTube)"
clip("im37-ab-a.mp4", "https://www.youtube.com/watch?v=kpk2tdsPh0A", "*2:00-2:20", cut=0)
clip("im37-ab-b.mp4", "https://www.youtube.com/watch?v=kpk2tdsPh0A", "*12:00-12:20", cut=0)
clip("im37-ab-c.mp4", "https://www.youtube.com/watch?v=X-zAWbM50JM", "*1:00-1:20", cut=0)
ep(342, "half-an-a-press", "This Mario Level Was Beaten With Half a Jump", PUCK, "#ffd600", RCAP("#fff59d"),
   [L("This Mario level was beaten with half a jump.",
      CLIP("im37-ab-c.mp4", "HALF\nA JUMP", "SUPER MARIO 64", 0, ABC, bs=170)),
    L("In Super Mario 64, pannenkoek2012 tries to beat levels pressing the jump button as few times as possible.",
      CLIP("im37-ab-a.mp4", "FEWEST\nJUMPS", "THE A BUTTON CHALLENGE", 0, ABC, bs=150)),
    L("In 2016 he beat Watch for Rolling Rocks in half an A press. He was already holding the button from the level before.",
      CLIP("im37-ab-b.mp4", "0.5 A\nPRESSES", "2016", 0, ABC, bs=150)),
    L("To do it, Mario builds up so much speed he moves through parallel universes. The first plan took over 14 hours.",
      CLIP("im37-ab-c.mp4", "PARALLEL\nUNIVERSES", "14+ HOURS", 7.0, ABC, bs=150)),
    L("Then in 2023, someone beat it with zero A presses.",
      CLIP("im37-ab-a.mp4", "ZERO", "2023", 7.0, ABC, bs=190)),
    ask("Could you beat Mario without jumping?", "NO\nJUMPING?", "im37-ab-b.mp4", ABC, 7.0),
    subline("im37-ab-c.mp4", ABC, 4.0),
   ], pron={"pannenkoek2012": "pannen cook twenty twelve"}, edition="IMPOSSIBLE FEATS")

# ---------------------------------------------------------------- 343 GD: Spectre (wiki.gg)
SPC = "Clips: PersonHuman42; Trick (YouTube)"
clip("gd37-sp-a.mp4", "https://www.youtube.com/watch?v=MzsSLKJrLSI", "*1:00-1:20", cut=0)
clip("gd37-sp-b.mp4", "https://www.youtube.com/watch?v=MzsSLKJrLSI", "*2:20-2:40", cut=0)
clip("gd37-sp-c.mp4", "https://www.youtube.com/watch?v=D0tp4U1sUWs", "*1:30-1:50", cut=0)
ep(343, "spectre-106017-vs-5582", "He Took 106,017 Attempts Then Someone Beat It in 5,582", MIKE, "#e040fb", GDCAP,
   [L("He took over 106,000 attempts to verify this level. Six days later, someone beat it in 5,582.",
      H("gd37-sp-b.mp4", "[106,017 VS 5,582]\nSPECTRE", 0, SPC)),
    L("Spectre is a giant mega collab. A spiritual successor to Zodiac. Rainbow colors and flow gameplay.",
      H("gd37-sp-a.mp4", "[RAINBOW]\nZODIAC SUCCESSOR", 0, SPC)),
    L("PersonHuman42 verified it in October 2024.",
      HC("gd37-sp-b.mp4", 7.0, SPC, 106017, "ATTEMPTS - VERIFIER")),
    L("Then Trick beat it six days later. In just 5,582 attempts.",
      HC("gd37-sp-c.mp4", 0, SPC, 5582, "ATTEMPTS - TRICK")),
    L("It went in at number 6 on the Demonlist.",
      H("gd37-sp-c.mp4", "[#6]\nDEMONLIST", 7.0, SPC)),
    ask("Who's more impressive?", "WHO'S\nBETTER?", "gd37-sp-b.mp4", SPC),
    subline("gd37-sp-a.mp4", SPC, 7.0),
   ], pron=dict(GD_PRON, PersonHuman42="Person Human forty two"), gd_player="PersonHuman42", **GDE)

# ---------------------------------------------------------------- 344 GD: Nine Circles (wiki.gg)
NCC = "Clips: Zobros; Nexus [GD] (YouTube)"
clip("gd37-nc-a.mp4", "https://www.youtube.com/watch?v=4WCgpSYz-ug", "*0:20-0:40", cut=0)
clip("gd37-nc-b.mp4", "https://www.youtube.com/watch?v=4WCgpSYz-ug", "*1:00-1:20", cut=0)
clip("gd37-nc-c.mp4", "https://www.youtube.com/watch?v=dOdPoU1ncOc", "*1:20-1:40", cut=0)
ep(344, "nine-circles-created-a-genre", "This Hard Demon Created a Whole New Type of Level", LIAM, "#ff4081", GDCAP,
   [L("This is only a Hard Demon. But it created a whole new type of level.",
      H("gd37-nc-b.mp4", "[HARD DEMON]\nNINE CIRCLES", 0, NCC)),
    L("Nine Circles, by Zobros. A super fast wave section, and strobing visuals.",
      H("gd37-nc-a.mp4", "[ZOBROS]\nFAST WAVE", 0, NCC)),
    L("Players remade it thousands of times. These became known as Nine Circles levels.",
      H("gd37-nc-c.mp4", "[THOUSANDS]\nOF REMAKES", 0, NCC)),
    L("Sonic Wave, Poltergeist, and Jawbreaker all came from it.",
      H("gd37-nc-b.mp4", "[SONIC WAVE]\nCAME FROM THIS", 7.0, NCC)),
    ask("What's the best Nine Circles level?", "BEST\nONE?", "gd37-nc-c.mp4", NCC, 7.0),
    subline("gd37-nc-a.mp4", NCC, 7.0),
   ], pron=dict(GD_PRON, Zobros="Zoh-bros"), gd_player="Zobros", **GDE)

# ---------------------------------------------------------------- 345 GD: Yatagarasu (wiki.gg)
YTC = "Clips: TrusTa; Vortex RBR (YouTube)"
clip("gd37-yt-a.mp4", "https://www.youtube.com/watch?v=KgGKx0pk_wo", "*1:30-1:50", cut=0)
clip("gd37-yt-b.mp4", "https://www.youtube.com/watch?v=KgGKx0pk_wo", "*5:00-5:20", cut=0)
clip("gd37-yt-c.mp4", "https://www.youtube.com/watch?v=AnlW9Z6aVrM", "*0:20-0:40", cut=0)
ep(345, "yatagarasu-new-difficulty", "This Level Was So Hard Geometry Dash Added a New Difficulty", FENRIR, "#ff6d00", GDCAP,
   [L("This level was so hard, Geometry Dash added a new difficulty three days later.",
      H("gd37-yt-b.mp4", "[NEW DIFFICULTY]\nYATAGARASU", 0, YTC)),
    L("Yatagarasu. A hell themed mega collab, named after a three legged crow from Japanese myth.",
      H("gd37-yt-a.mp4", "[3-LEGGED CROW]\nJAPANESE MYTH", 0, YTC)),
    L("TrusTa verified it on January 13, 2017. It went straight to number 1.",
      H("gd37-yt-c.mp4", "[#1]\nTRUSTA", 0, YTC)),
    L("Players said RobTop needed a harder rating. Three days later, update 2.1 added Extreme Demons.",
      H("gd37-yt-b.mp4", "[2.1]\nEXTREME DEMONS", 7.0, YTC)),
    ask("Should there be a rating harder than Extreme?", "HARDER\nTHAN EXTREME?", "gd37-yt-a.mp4", YTC, 7.0),
    subline("gd37-yt-c.mp4", YTC, 7.0),
   ], pron=dict(GD_PRON, Yatagarasu="Yah-tah-gah-rah-soo", TrusTa="Trust-uh", RobTop="Rob Top"), gd_player="TrusTa", **GDE)

# ================================================================== write
paths = []
for e in RB:
    e = dict(preset="roblox", hdr="tag", **e)
    words = sum(len(l.get("say", l["t"]).split()) for l in e["lines"])
    p = os.path.join("episodes", "roblox", e["slug"] + ".json")
    json.dump(e, open(os.path.join(ROOT, p), "w"), indent=1, ensure_ascii=False)
    paths.append(p)
    print(e["slug"], len(e["lines"]), "lines", words, "words")
manifest = {"batch": 37, "note": "Game Mysteries 2-parters (Polybius, P.T.), John Doe, pack.png, half A press, Spectre, Nine Circles, Yatagarasu",
            "posting": "Z:/claudeprojects/roblox vids/batch-37/posting.txt", "episodes": paths, "clips": CLIPS}
json.dump(manifest, open(os.path.join(ROOT, "batches", "batch-37.json"), "w"), indent=1)
print(len(CLIPS), "clips")
