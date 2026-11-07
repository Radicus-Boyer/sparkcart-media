"""Writes batch 32 (facts checked 2026-11-07): 3 meme lore + 4 GD (Zoink plug last) + Fortnite Pirate Shop + Roblox copies + Say Cheese = #286-295.

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

# ---------------------------------------------------------------- 286 MEME: Snow Leopard Paws at You (Know Your Meme)
SLC = "Clips: Kuch Bhi Haat; fofobi (YouTube)"
clip("tr32-sl-a.mp4", "https://www.youtube.com/watch?v=Els3CVl_-cE", "*0:15-0:35", cut=0)
clip("tr32-sl-b.mp4", "https://www.youtube.com/watch?v=CETHQkNnlBM", "*1:00-1:20", cut=0)
clip("tr32-sl-c.mp4", "https://www.youtube.com/watch?v=fpVq9bvApwk", "*2:00-2:20", cut=0)
ep(286, "snow-leopard-paws-at-you", "The Snow Leopard Paws at You Meme Explained", HEART, "#b388ff", MCAP("#e1bee7"),
   [L("This snow leopard is all over your feed right now. And it is pawing at you.",
      CLIP("tr32-sl-a.mp4", "*PAWS\nAT YOU*", "THE SNOW LEOPARD MEME", 0, SLC, bs=140)),
    L("He's real. His name is Himmel, and he lives at a zoo in Japan.",
      CLIP("tr32-sl-b.mp4", "HE'S\nREAL", "HIMMEL - ISHIKAWA ZOO, JAPAN", 0, SLC, bs=150)),
    L("A visitor photographed him in 2024. Then in October 2026, someone used AI to give him the face of Mei Mei, a famous cat.",
      CLIP("tr32-sl-a.mp4", "+ AI CAT\nFACE", "MEI MEI THE CAT", 6.0, SLC, bs=140)),
    L("Add the words, paws at you, and it's a friend begging you to hop online.",
      CLIP("tr32-sl-c.mp4", "\"HOP\nONLINE\"", "", 0, SLC, bs=150)),
    L("One post got 1.4 million views in a day. Even Epic Games posted it.",
      CCOUNT("tr32-sl-a.mp4", 12.0, SLC, 1400000, "VIEWS IN ONE DAY", bs=140)),
    ask("Who keeps pawing at YOU to hop on?", "WHO PAWS\nAT YOU?", "tr32-sl-a.mp4", SLC),
    subline("tr32-sl-b.mp4", SLC, 8.0),
   ], pron={"Himmel": "Him-mel", "Mei Mei": "May May"}, edition="MEME LORE")

# ---------------------------------------------------------------- 287 MEME: The Last Dance trend (Know Your Meme)
LDC = "Clips: Torial; Memes ok; zoe. 0 (YouTube)"
clip("tr32-ld-a.mp4", "https://www.youtube.com/watch?v=-83fztV7Ix0", "*0:30-0:50", cut=0)
clip("tr32-ld-b.mp4", "https://www.youtube.com/watch?v=AJ1awkJrtJk", "*0:20-0:40", cut=0)
clip("tr32-ld-c.mp4", "https://www.youtube.com/watch?v=tZz3cFOwnKY", "*0:40-1:00", cut=0)
ep(287, "the-last-dance-trend", "The Last Dance Song Is From 2014", LIAM, "#ff4081", MCAP("#ff80ab"),
   [L("This song is everywhere on TikTok. It came out in 2014, and almost nobody heard it.",
      CLIP("tr32-ld-a.mp4", "\"THE LAST\nDANCE\"", "A SONG FROM 2014", 0, LDC, bs=140)),
    L("It's a Vocaloid track by a producer named MARETU, with a weird name. Fans just call it The Last Dance.",
      CLIP("tr32-ld-a.mp4", "FPD FF7\nBOTSU 8", "BY MARETU", 8.0, LDC, bs=140), say="It's a Vocaloid track by a producer named Mah-reh-too, with a weird name. Fans just call it The Last Dance."),
    L("In August, people started animating two characters dancing to it. Usually, saying goodbye forever.",
      CLIP("tr32-ld-b.mp4", "GOODBYE\nFOREVER", "THE ANIMATION TREND", 0, LDC, bs=150)),
    L("Then real people started doing the dance. One video got over 8 million views.",
      CCOUNT("tr32-ld-b.mp4", 8.0, LDC, 8600000, "VIEWS", bs=140)),
    L("Now there are English covers, and even Undertale cosplayers are doing it.",
      CLIP("tr32-ld-c.mp4", "ENGLISH\nCOVERS", "", 0, LDC, bs=150)),
    ask("Who would you do the last dance with?", "WHO WOULD\nYOU PICK?", "tr32-ld-a.mp4", LDC),
    subline("tr32-ld-c.mp4", LDC, 8.0),
   ], pron={"MARETU": "Mah-reh-too", "Vocaloid": "Vo-ka-loid"}, edition="MEME LORE")

# ---------------------------------------------------------------- 288 MEME: Randy Marsh "What's Up Brah?" (Know Your Meme)
RMC = "Clips: ConquerRecap; xCYMAx; Baix (YouTube)"
clip("tr32-rm-a.mp4", "https://www.youtube.com/watch?v=OdhjyxT95w8", "*0:05-0:25", cut=0)
clip("tr32-rm-b.mp4", "https://www.youtube.com/watch?v=WoudYNeVn5E", "*0:05-0:25", cut=0)
clip("tr32-rm-c.mp4", "https://www.youtube.com/watch?v=OdhjyxT95w8", "*0:45-1:05", cut=0)
ep(288, "randy-marsh-whats-up-brah", "Why Randy Marsh Is Fighting Every Villain", FENRIR, "#ffab00", MCAP("#ffd180"),
   [L("Randy Marsh is fighting every villain on the internet right now. And he always says the same thing.",
      CLIP("tr32-rm-a.mp4", "RANDY VS\nEVERYONE", "", 0, RMC, bs=140)),
    L("What's up, brah?",
      CLIP("tr32-rm-a.mp4", "\"WHAT'S UP\nBRAH?\"", "", 5.0, RMC, bs=150)),
    L("It's from a 2011 South Park episode called Broadway Bro Down.",
      CLIP("tr32-rm-b.mp4", "BROADWAY\nBRO DOWN", "SOUTH PARK - 2011", 0, RMC, bs=140)),
    L("Back in 2012, people put him next to Bane, like he was about to wrestle him.",
      CLIP("tr32-rm-c.mp4", "RANDY\nVS BANE", "THE 2012 MEME", 0, RMC, bs=150)),
    L("In October, TikTok brought it back. Now he's squaring up with Minecraft Steve, Omni-Man, and more. He never backs down.",
      CLIP("tr32-rm-c.mp4", "NEVER\nBACKS DOWN", "STEVE - OMNI-MAN - MORE", 8.0, RMC, bs=140)),
    ask("Who should Randy fight next?", "WHO'S\nNEXT?", "tr32-rm-a.mp4", RMC),
    subline("tr32-rm-a.mp4", RMC, 12.0),
   ], pron={"Omni-Man": "Omni Man"}, edition="MEME LORE")

# ---------------------------------------------------------------- 289 GD: Zoink beat GRIEF (wiki.gg, Nov 6 2026)
GRC = "Clips: Hao; Toogit; Yuric (YouTube)"
clip("gd32-gr-a.mp4", "https://www.youtube.com/watch?v=A-sK7146cK8", "*0:02-0:22", cut=0)
clip("gd32-gr-b.mp4", "https://www.youtube.com/watch?v=qUQZg6qd8SY", "*9:30-9:50", cut=0)
clip("gd32-gr-c.mp4", "https://www.youtube.com/watch?v=qUQZg6qd8SY", "*4:00-4:20", cut=0)
clip("gd32-gr-d.mp4", "https://www.youtube.com/watch?v=7892WirowY4", "*3:00-3:20", cut=0)
ep(289, "zoink-beat-grief", "Zoink Died at 98 Percent on GRIEF Then Beat It", MIKE, "#ff1744", GDCAP,
   [L("Zoink died at 98 percent on the hardest level in Geometry Dash. Two percent from history.",
      H("gd32-gr-a.mp4", "[98%] ZOINK\nON GRIEF", 0, GRC)),
    L("GRIEF is the new number one. Doggie spent two and a half years verifying it.",
      H("gd32-gr-c.mp4", "[TOP 1]\nGRIEF", 0, GRC)),
    L("On November 2nd, wPopoff beat it first. Zoink was stuck at 82 percent.",
      H("gd32-gr-c.mp4", "[FIRST VICTOR]\nWPOPOFF", 8.0, GRC)),
    L("Then came the 98. In the final monster.",
      H("gd32-gr-a.mp4", "[98%]\nTHE FINAL MONSTER", 6.0, GRC)),
    L("And on November 6th... he did it. About 37,000 attempts, and 67 hours of playtime.",
      HC("gd32-gr-b.mp4", 0, GRC, 37000, "GRIEF - ZOINK 100%")),
    ask("Who's better: Zoink or wPopoff?", "ZOINK OR\nWPOPOFF?", "gd32-gr-b.mp4", GRC, 8.0),
    subline("gd32-gr-d.mp4", GRC),
   ], pron=dict(GD_PRON), gd_player="Zoink", **GDE)

# ---------------------------------------------------------------- 290 GD: Green Bullet, 3 verifiers (wiki.gg)
GBC = "Clips: nickname; Viprin (YouTube)"
clip("gd32-gb-a.mp4", "https://www.youtube.com/watch?v=JG-qcvVkZFw", "*2:40-3:00", cut=0)
clip("gd32-gb-b.mp4", "https://www.youtube.com/watch?v=JG-qcvVkZFw", "*0:40-1:00", cut=0)
clip("gd32-gb-c.mp4", "https://www.youtube.com/watch?v=5pbCgDdA2mQ", "*1:00-1:20", cut=0)
ep(290, "green-bullet-three-verifiers", "Two Players Quit This Level Then the Third Took 105,000 Attempts", LIAM, "#00e676", GDCAP,
   [L("Two players quit this level. The third one beat it, after 105,000 attempts.",
      H("gd32-gb-a.mp4", "[3 VERIFIERS]\nGREEN BULLET", 0, GBC)),
    L("It's Green Bullet, built by Cherry Team, a group of more than ten creators.",
      H("gd32-gb-c.mp4", "[CHERRY TEAM]\nGREEN BULLET", 0, GBC)),
    L("SerVax was picked to verify it. He stepped down. Then Trick took over.",
      H("gd32-gb-b.mp4", "[QUIT]\nSERVAX - TRICK", 0, GBC)),
    L("Then a player called nickname took the job. He died at 89 percent.",
      H("gd32-gb-b.mp4", "[89%]\nNICKNAME", 8.0, GBC)),
    L("On June 16th, he finally verified it. It's now number 8 on the Demonlist.",
      HC("gd32-gb-a.mp4", 8.0, GBC, 105000, "GREEN BULLET - VERIFIED")),
    ask("Would you have quit too?", "WOULD YOU\nQUIT?", "gd32-gb-a.mp4", GBC),
    subline("gd32-gb-c.mp4", GBC, 8.0),
   ], pron=dict(GD_PRON, SerVax="Sir Vax"), gd_player="nickname", **GDE)

# ---------------------------------------------------------------- 291 GD: Antarctic Lights, 381,058 attempts (wiki.gg)
ALC = "Clips: Axinity; Newly Rated Extremes (YouTube)"
clip("gd32-al-a.mp4", "https://www.youtube.com/watch?v=Uue4ZRhVf-I", "*1:30-1:50", cut=0)
clip("gd32-al-b.mp4", "https://www.youtube.com/watch?v=_M3D5xP0w7c", "*1:30-1:50", cut=0)
clip("gd32-al-c.mp4", "https://www.youtube.com/watch?v=Ii25Ypw_Cjs", "*0:30-0:50", cut=0)
ep(291, "antarctic-lights-381058-attempts", "He Took 381,058 Attempts Then a Showcase Got the Views", PUCK, "#00e5ff", GDCAP,
   [L("This player spent 381,058 attempts on one level. Then someone else got the views.",
      H("gd32-al-a.mp4", "[381,058]\nANTARCTIC LIGHTS", 0, ALC)),
    L("It's Antarctic Lights. Most of it is wave, at quadruple speed.",
      H("gd32-al-c.mp4", "[4X SPEED]\nWAVE", 0, ALC)),
    L("Axinity grinded it for over a year. 70 percent. 85. 90. Then 92.",
      H("gd32-al-b.mp4", "[92%]\nVERIFYING", 0, ALC)),
    L("In July 2026, he verified it. It went in at number 8, the hardest Nine Circles level ever.",
      HC("gd32-al-a.mp4", 8.0, ALC, 381058, "ATTEMPTS - VERIFIED")),
    L("Then a showcase channel uploaded it with verified in the title. And people said it stole his views.",
      H("gd32-al-c.mp4", "[SHOWCASE]\n\"STOLE HIS VIEWS\"", 8.0, ALC)),
    ask("Are showcase channels fair?", "IS THAT\nFAIR?", "gd32-al-a.mp4", ALC),
    subline("gd32-al-b.mp4", ALC, 8.0),
   ], pron=dict(GD_PRON, Axinity="Ax-in-ity"), gd_player="Axinity", **GDE)

# ---------------------------------------------------------------- 292 FORTNITE: Pirate Shop Access + "dev hour" (Kotaku, Island Dispatch, Beebom, timesaver.gg)
FNC = "Clips: SypherPK; tmnglv; NOOB NOOB FRUIT (YouTube)"
clip("tr32-fn-a.mp4", "https://www.youtube.com/watch?v=NMPsjlNEF4o", "*0:20-0:40", cut=0)
clip("tr32-fn-b.mp4", "https://www.youtube.com/watch?v=EfYC0IOlR1c", "*1:00-1:20", cut=0)
clip("tr32-fn-c.mp4", "https://www.youtube.com/watch?v=8NIYlMaYMnc", "*0:15-0:35", cut=0)
clip("tr32-fn-d.mp4", "https://www.youtube.com/watch?v=Bph3jJW_79s", "*2:00-2:20", cut=0)
ep(292, "fortnite-pirate-shop-dev-hour", "Fortnite Pirate Shop Access and Dev Hour Explained", MIKE, "#ffd600",
   {"font": MF + "Bangers-Regular.ttf", "size": 120, "mode": "word", "fill": "#ffffff", "hi": "#ffff8d", "cy": 1470},
   [L("Fortnite hid one item that makes almost the whole Item Shop free. And Epic won't say how rare it is.",
      CLIP("tr32-fn-a.mp4", "A FREE\nITEM SHOP", "PIRATE SHOP ACCESS", 0, FNC, bs=140)),
    L("It's Pirate Shop Access. Any chest on Crossbones Isle can drop it.",
      CLIP("tr32-fn-d.mp4", "ANY CHEST", "CROSSBONES ISLE", 0, FNC, bs=150)),
    L("Find it, and you get two 14 day windows, one now and one in 2027, to claim V-Bucks items for free.",
      CLIP("tr32-fn-a.mp4", "2 x 14\nDAYS", "NOW + 2027", 8.0, FNC, bs=150)),
    L("Players are opening thousands of chests. One account with it was reportedly listed for 10,000 dollars.",
      CCOUNT("tr32-fn-b.mp4", 0, FNC, 10000, "REPORTED LISTING", fmt="${:,.0f}", bs=140)),
    L("So what's dev hour? A fan theory that Epic will boost the drop on November 19th, when GTA 6 comes out. Epic has not confirmed it.",
      CLIP("tr32-fn-c.mp4", "\"DEV HOUR\"", "FAN THEORY - NOT CONFIRMED", 0, FNC, bs=140)),
    L("What's real: Treasure Hours, with boosted chest rewards. And you have until December 15th to activate it.",
      CLIP("tr32-fn-c.mp4", "TREASURE\nHOURS", "ACTIVATE BY DEC 15", 8.0, FNC, bs=140)),
    ask("Have you found it yet?", "FOUND IT\nYET?", "tr32-fn-a.mp4", FNC),
    subline("tr32-fn-b.mp4", FNC, 8.0),
   ], pron={"V-Bucks": "V bucks", "GTA": "G T A"}, edition="FORTNITE")

# ---------------------------------------------------------------- 293 ROBLOX: devs copying small creators (Shane the Gamer, Windows Central, live Roblox numbers Nov 7)
CPC = "Clips: FoltynPlays; Ready To Wishlist; Navi (YouTube)"
clip("rb32-cp-a.mp4", "https://www.youtube.com/watch?v=3LHYoLyLCng", "*3:00-3:20", cut=0)
clip("rb32-cp-b.mp4", "https://www.youtube.com/watch?v=FfgehEpNhAc", "*0:03-0:23", cut=0)
clip("rb32-cp-c.mp4", "https://www.youtube.com/watch?v=pM6hQXByqUY", "*1:00-1:20", cut=0)
clip("rb32-cp-d.mp4", "https://www.youtube.com/watch?v=3LHYoLyLCng", "*8:00-8:20", cut=0)
ep(293, "roblox-copies-needle-in-a-haystack", "This Roblox Game Copied a Game That Isnt Even Out Yet", FENRIR, "#ff5252",
   {"font": MF + "Bangers-Regular.ttf", "size": 120, "mode": "word", "fill": "#ffffff", "hi": "#ff8a80", "cy": 1470},
   [L("This Roblox game got over 122 million visits, by copying a game that isn't even out yet.",
      CLIP("rb32-cp-a.mp4", "122 MILLION\nVISITS", "COPYING AN UNRELEASED GAME", 0, CPC, bs=120)),
    L("In August, a video of a game about finding one needle in a haystack got over 50 million views.",
      CLIP("rb32-cp-b.mp4", "THE\nORIGINAL", "NEEDLE IN A HAYSTACK SIMULATOR", 0, CPC, bs=150)),
    L("The real game still isn't out. But copies showed up right away, on Steam and on Roblox.",
      CLIP("rb32-cp-d.mp4", "COPIES\nEVERYWHERE", "STEAM + ROBLOX", 0, CPC, bs=150)),
    L("Search For The Needle came out on Roblox in August. Now it has over 122 million visits.",
      CCOUNT("rb32-cp-a.mp4", 8.0, CPC, 122520000, "VISITS", bs=130)),
    L("It happened before. When PEAK blew up, a Roblox copy called CLIFF got millions of visits. PEAK's devs said they'd rather you pirate their game.",
      CLIP("rb32-cp-c.mp4", "PEAK VS\nCLIFF", "\"RATHER YOU PIRATE IT\"", 0, CPC, bs=150)),
    L("So the real creator made a joke mode: find the original game in a pile of clones.",
      CLIP("rb32-cp-b.mp4", "FIND THE\nORIGINAL", "", 10.0, CPC, bs=150)),
    ask("Is copying a game ever okay?", "IS IT\nOKAY?", "rb32-cp-a.mp4", CPC),
   ], pron={"PEAK": "Peak", "CLIFF": "Cliff"})

# ---------------------------------------------------------------- 294 ROBLOX: Say Cheese! [STORY] (live Roblox numbers Nov 7)
SCC = "Clips: Roblox Master Guides; BrosClanYt (Roblox gameplay, YouTube)"
clip("rb32-sc-a.mp4", "https://www.youtube.com/watch?v=kyWrM9Bn1DA", "*2:00-2:20", cut=0, backup=["https://www.youtube.com/watch?v=QFtr97bUOxg"])
clip("rb32-sc-b.mp4", "https://www.youtube.com/watch?v=kyWrM9Bn1DA", "*10:00-10:20", cut=0)
clip("rb32-sc-c.mp4", "https://www.youtube.com/watch?v=kyWrM9Bn1DA", "*20:00-20:20", cut=0)
clip("rb32-sc-d.mp4", "https://www.youtube.com/watch?v=Rvln06xvWqk", "*3:00-3:20", cut=0)
ep(294, "say-cheese-story", "Say Cheese on Roblox Makes You Spread Panic", HEART, "#ffea00",
   {"font": MF + "Bangers-Regular.ttf", "size": 120, "mode": "word", "fill": "#ffffff", "hi": "#ffff8d", "cy": 1470},
   [L("This new fun game on Roblox makes you a reporter. And your job is to cause panic.",
      CLIP("rb32-sc-a.mp4", NEW, "YOUR JOB: CAUSE PANIC", 0, SCC, bs=110)),
    L("Big Media hires you to spread chaos in a peaceful park, so billions keep watching the news.",
      CLIP("rb32-sc-b.mp4", "BIG\nMEDIA", "NO MATTER THE COST", 0, SCC, bs=150)),
    L("It's a story game, and players have found 12 different endings.",
      CLIP("rb32-sc-c.mp4", "12\nENDINGS", "", 0, SCC, bs=160)),
    L("It came out on October 19th, and it already has over 17 million visits. And chapter 2 just dropped.",
      CCOUNT("rb32-sc-d.mp4", 0, SCC, 17600000, "VISITS - CHAPTER 2 OUT", bs=130)),
    ask("Would you do it, no matter the cost?", "WOULD\nYOU?", "rb32-sc-a.mp4", SCC),
   ])

# ---------------------------------------------------------------- 295 GD PLUG (posted LAST): Zoink's curse -> full Zoink story (long #3)
ZCC = "Clips: Zoink; random guy (YouTube)"
clip("gd32-zc-a.mp4", "https://www.youtube.com/watch?v=KIWapVa-Bxg", "*0:05-0:25", cut=0)
clip("gd32-zc-b.mp4", "https://www.youtube.com/watch?v=9fsZ014qB3s", "*3:30-3:50", cut=0)
clip("gd32-zc-c.mp4", "https://www.youtube.com/watch?v=9fsZ014qB3s", "*1:00-1:20", cut=0)
ZPOP = dict(img="zoink-long-thumb.jpg", len="FULL STORY", d=0.35, y=1175)
ep(295, "zoinks-curse-plug", "Four Players Died at 95 Percent on the Same Level", MIKE, "#2979ff", GDCAP,
   [L("Four of the best players in the world died at 95 percent on the same level. They call it Zoink's curse.",
      H("gd32-zc-a.mp4", "[95% x4]\nZOINK'S CURSE", 0, ZCC)),
    L("In 2023, Zoink was verifying Tidal Wave. He died at 95 percent.",
      H("gd32-zc-c.mp4", "[95%]\nTIDAL WAVE", 0, ZCC)),
    L("Later, wPopoff, Trick and Netermind all beat it. And all three had died at 95 too.",
      H("gd32-zc-a.mp4", "[95%]\nWPOPOFF - TRICK - NETERMIND", 8.0, ZCC, bs=64)),
    L("Zoink beat it on September 9th, 2023, with 25 fails past 73 percent.",
      HC("gd32-zc-b.mp4", 0, ZCC, 49534, "ATTEMPTS - TIDAL WAVE")),
    L("And that's one chapter. He verified seven of the fifteen hardest levels. The full Zoink story is on my channel.",
      H("gd32-zc-b.mp4", "[FULL STORY]\nON MY CHANNEL", 8.0, ZCC, popup=ZPOP)),
    ask("Is Zoink the best ever?", "THE BEST\nEVER?", "gd32-zc-a.mp4", ZCC),
    subline("gd32-zc-c.mp4", ZCC, 8.0),
   ], pron=dict(GD_PRON), gd_player="Zoink", **GDE)
RB[-1]["lines"][-2]["sc"]["popup"] = dict(ZPOP, d=0.0)

# ================================================================== write
paths = []
for e in RB:
    e = dict(preset="roblox", hdr="tag", **e)
    words = sum(len(l.get("say", l["t"]).split()) for l in e["lines"])
    p = os.path.join("episodes", "roblox", e["slug"] + ".json")
    json.dump(e, open(os.path.join(ROOT, p), "w"), indent=1, ensure_ascii=False)
    paths.append(p)
    print(e["slug"], len(e["lines"]), "lines", words, "words")
manifest = {"batch": 32, "note": "Snowmei, Last Dance, Randy brah, Zoink GRIEF, Green Bullet, Antarctic Lights, Fortnite Pirate Shop, Roblox copies, Say Cheese, Zoink plug",
            "posting": "Z:/claudeprojects/roblox vids/batch-32/posting.txt", "episodes": paths, "clips": CLIPS}
json.dump(manifest, open(os.path.join(ROOT, "batches", "batch-32.json"), "w"), indent=1)
print(len(CLIPS), "clips")
