"""Writes batch 24 (facts checked 2026-10-30): spaceuk career + 2 GD + 3 Roblox + 4 popular niches = #211-220.

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
# Channel had 166 subscribers on Oct 30, 2026, so "500 by Christmas" is a real goal.
def subline(name, credit, start=0.0):
    return L("Help a small creator hit 500 subs by Christmas!",
             CLIP(name, "SUBSCRIBE", "HELP US HIT 500 BY CHRISTMAS", start, credit, bs=150, ss=44))


GD_PRON.update({"spaceuk": "space U K", "paqoe": "pa-co", "Npesta": "N pesta", "Bianox": "Bee-a-nox", "Kenos": "Kee-nos",
                "Mvngo": "Mango", "Acheron": "Ack-er-on"})

# ============================================================ GEOMETRY DASH
SKC = "Clips: spaceuk; paqoe; Spaceuk Archive (YouTube)"
clip("gd24-sk-a.mp4", "https://www.youtube.com/watch?v=0CSFakL3Hl8", "*6:26-6:46", cut=0)
clip("gd24-sk-b.mp4", "https://www.youtube.com/watch?v=CC7zfHByLSk", "*1:00-1:20", cut=0, backup=["https://www.youtube.com/watch?v=7W5bZJY2IPI"])
clip("gd24-sk-c.mp4", "https://www.youtube.com/watch?v=I2RTFwn_zho", "*0:38-0:58", cut=0)
clip("gd24-sk-d.mp4", "https://www.youtube.com/watch?v=iS4bhiCOZGU", "*0:30-0:50", cut=0)
ep(211, "spaceuk-career", "spaceuk Faked Everything Then Came Back Legit", MIKE, "#7c4dff",
   {"font": MF + "BlackOpsOne-Regular.ttf", "size": 92, "fill": "#ffffff", "hi": "#b388ff", "stroke": 8},
   [L("He got caught faking almost every hard level. Now he's beating them for real.",
      CLIP("gd24-sk-a.mp4", "SPACEUK", "THE COMEBACK", 0, SKC)),
    L("Starting in 2020, spaceuk beat the hardest levels almost one a day.",
      CLIP("gd24-sk-b.mp4", "THE RISE", "SLAUGHTERHOUSE 'VERIFIED'", 0, SKC, ss=50)),
    L("In April 2023, paqoe exposed him. He'd faked almost every record with a bot.",
      CLIP("gd24-sk-c.mp4", "EXPOSED", "APRIL 2023", 0, SKC, bs=170)),
    L("He came back legit. In January, he beat Acheron after about 125,000 attempts.",
      CCOUNT("gd24-sk-a.mp4", 6.0, SKC, 125000, "LEGIT ATTEMPTS ON ACHERON", fmt="~{:,.0f}")),
    L("And now he's going back for Slaughterhouse, for real this time.",
      CLIP("gd24-sk-d.mp4", "SLAUGHTER-\nHOUSE", "FOR REAL THIS TIME", 0, SKC, bs=130)),
    ask("Should the community forgive him?", "FORGIVE\nHIM?", "gd24-sk-a.mp4", SKC),
    subline("gd24-sk-a.mp4", SKC, 3.0),
   ], pron=dict(GD_PRON), gd_player="spaceuk", **GDE)

ARC = "Clips: Zoink; TCD; Mr. Happy Junior (YouTube)"
clip("gd24-ar-a.mp4", "https://www.youtube.com/watch?v=FgjOM0ef1N8", "*1:08-1:28", cut=0)
clip("gd24-ar-b.mp4", "https://www.youtube.com/watch?v=DQsMd2-RMY8", "*14:44-15:04", cut=0)
clip("gd24-ar-c.mp4", "https://www.youtube.com/watch?v=OAYhKktcyUA", "*0:28-0:48", cut=0)
ep(212, "artemis-13-2-out-of-10", "Zoink Beat the Number 2 Level and Rated It 2 Out of 10", LIAM, "#00b0ff",
   {"font": MF + "RussoOne-Regular.ttf", "size": 92, "hi": "#80d8ff", "stroke": 8},
   [L("Zoink just beat the second hardest level in Geometry Dash, and he hated it.",
      CLIP("gd24-ar-a.mp4", "ARTEMIS 13", "VERIFIED", 0, ARC)),
    L("He verified Artemis 13 in September. It knocked Tidal Wave out of the top 5 after 3 years.",
      CLIP("gd24-ar-b.mp4", "#2 HARDEST", "TIDAL WAVE OUT OF TOP 5", 0, ARC, ss=48)),
    L("He almost had to drop it, after drama around the level's host. Then the level was handed to Mvngo, and he kept going.",
      CLIP("gd24-ar-c.mp4", "ALMOST\nDROPPED", "HOST DRAMA", 0, ARC)),
    L("His furthest death was 95 percent. And his review? 2 out of 10.",
      CLIP("gd24-ar-a.mp4", "ENJOYMENT:\n2/10", "- ZOINK", 6.0, ARC, bs=140)),
    ask("Would you grind a level you hate?", "GRIND A LEVEL\nYOU HATE?", "gd24-ar-a.mp4", ARC),
    subline("gd24-ar-a.mp4", ARC, 3.0),
   ], pron=dict(GD_PRON), gd_player="Zoink", **GDE)

KEC = "Clips: npesta's stream (Calypso); Kenos verified by npesta; Neiro (YouTube)"
clip("gd24-ke-a.mp4", "https://www.youtube.com/watch?v=TYU-G-MQ3dY", "*1:51-2:11", cut=0)
clip("gd24-ke-b.mp4", "https://www.youtube.com/watch?v=Bs1kVySdUtI", "*1:00-1:20", cut=0)
clip("gd24-ke-c.mp4", "https://www.youtube.com/watch?v=eTmaojkJ_3M", "*1:00-1:20", cut=0, backup=["https://www.youtube.com/watch?v=TfwUCuC6Z2I"])
ep(213, "kenos-135320", "Npesta Took 135,320 Attempts to Beat Kenos", FENRIR, "#ff3d00",
   {"font": MF + "Anton-Regular.ttf", "size": 104, "hi": "#ff9e80", "stroke": 8},
   [L("This is what 135,320 attempts feels like.",
      CLIP("gd24-ke-a.mp4", "KENOS", "VERIFIED", 0, KEC)),
    L("Kenos was hosted by Bianox, and Npesta spent 117 streams and over 300 hours verifying it.",
      CLIP("gd24-ke-b.mp4", "117\nSTREAMS", "300+ HOURS", 0, KEC)),
    L("He died at 90 percent, 88, and 87, twice.",
      CLIP("gd24-ke-b.mp4", "90% 88%\n87% 87%", "SO CLOSE", 6.0, KEC, bs=130)),
    L("In December 2019, he finally beat it, after 135,320 attempts.",
      CCOUNT("gd24-ke-c.mp4", 0, KEC, 135320, "ATTEMPTS")),
    ask("What's the most attempts you've ever spent on a level?", "YOUR MOST\nATTEMPTS?", "gd24-ke-a.mp4", KEC),
    subline("gd24-ke-a.mp4", KEC, 3.0),
   ], pron=dict(GD_PRON), gd_player="Npesta", **GDE)

# ============================================================ ROBLOX (live numbers, Oct 30)
BRC = "Clips: Backseat Rally (Roblox gameplay, YouTube)"
clip("rb24-br-a.mp4", "https://www.youtube.com/watch?v=VJS4UmLje1Q", "*3:00-3:20", cut=0, backup=["https://www.youtube.com/watch?v=jqlqSj1lnYA"])
clip("rb24-br-b.mp4", "https://www.youtube.com/watch?v=gMdtEmlNkzk", "*0:20-0:40", cut=0)
clip("rb24-br-c.mp4", "https://www.youtube.com/watch?v=o7aWLN16vgY", "*5:00-5:20", cut=0, backup=["https://www.youtube.com/watch?v=FigMPG-mrmE"])
ep(214, "backseat-rally", "In Backseat Rally You Cant See the Road", PUCK, "#ffab00",
   {"font": MF + "Bangers-Regular.ttf", "size": 120, "mode": "word", "fill": "#ffffff", "hi": "#ffd740", "cy": 1470},
   [L("In this Roblox racing game, you can't see the road. Your friend can.",
      CLIP("rb24-br-a.mp4", "BACKSEAT\nRALLY", "YOU CAN'T SEE THE ROAD", 0, BRC, ss=50)),
    L("Backseat Rally came out on October 5th. Your co-driver sees what's coming and calls out every turn.",
      CLIP("rb24-br-b.mp4", "TRUST YOUR\nCO-DRIVER", "OCTOBER 5", 0, BRC, bs=130)),
    L("7 cars, 5 stages, rain, mud and snow. Playing solo? A friend's avatar rides along as your AI co-driver.",
      CLIP("rb24-br-c.mp4", "RAIN. MUD.\nSNOW.", "7 CARS, 5 STAGES", 0, BRC, bs=130)),
    L("In less than 4 weeks, it got over 45 million visits.",
      CCOUNT("rb24-br-b.mp4", 6.0, BRC, 45546093, "VISITS", bs=140)),
    ask("Would you trust your friend to call the turns?", "TRUST YOUR\nFRIEND?", "rb24-br-a.mp4", BRC),
    subline("rb24-br-a.mp4", BRC, 3.0),
   ])

WDC = "Clips: What If Disasters (Roblox gameplay, YouTube)"
clip("rb24-wd-a.mp4", "https://www.youtube.com/watch?v=YO0VrLyregQ", "*3:00-3:20", cut=0, backup=["https://www.youtube.com/watch?v=UY4GKHY17F8"])
clip("rb24-wd-b.mp4", "https://www.youtube.com/watch?v=aDi1JoNPzvc", "*8:00-8:20", cut=0)
clip("rb24-wd-c.mp4", "https://www.youtube.com/watch?v=UxnDv2mNT6Y", "*5:00-5:20", cut=0)
ep(215, "what-if-disasters", "What If Disasters Lets You Survive a Black Hole", SARAH, "#651fff",
   {"font": MF + "BlackOpsOne-Regular.ttf", "size": 92, "fill": "#ffffff", "hi": "#b388ff", "stroke": 8},
   [L("What if a black hole flew past Earth? This Roblox game lets you find out.",
      CLIP("rb24-wd-a.mp4", "WHAT IF\nDISASTERS", "SURVIVE IT", 0, WDC)),
    L("What If Disasters came out on October 5th. Every round brings a new disaster on a new map.",
      CLIP("rb24-wd-b.mp4", "NEW DISASTER\nEVERY ROUND", "OCTOBER 5", 0, WDC, bs=120)),
    L("Like rain for 1,000 years, or all the water disappearing. Find somewhere safe, and try to survive.",
      CLIP("rb24-wd-c.mp4", "FIND\nSHELTER", "TRY TO SURVIVE", 0, WDC)),
    L("It already has over 11 million visits.",
      CCOUNT("rb24-wd-a.mp4", 6.0, WDC, 11732423, "VISITS IN 25 DAYS", bs=140)),
    ask("What disaster should they add next?", "NEXT\nDISASTER?", "rb24-wd-a.mp4", WDC),
    subline("rb24-wd-a.mp4", WDC, 3.0),
   ], mood="spooky")

FEC = "Clips: Fake an Egg (Roblox gameplay, YouTube)"
clip("rb24-fe-a.mp4", "https://www.youtube.com/watch?v=TQvBn1Bea7U", "*4:00-4:20", cut=0, backup=["https://www.youtube.com/watch?v=FYPLIvsh7vM"])
clip("rb24-fe-b.mp4", "https://www.youtube.com/watch?v=E3Iepf_U_U0", "*3:00-3:20", cut=0, backup=["https://www.youtube.com/watch?v=ErnfL23tjyk"])
clip("rb24-fe-c.mp4", "https://www.youtube.com/watch?v=EWMQRi1QKgo", "*5:00-5:20", cut=0)
ep(216, "fake-an-egg", "In Fake an Egg the Egg Is a Player", HEART, "#ffd600",
   {"font": MF + "RussoOne-Regular.ttf", "size": 92, "hi": "#ffff00", "stroke": 8},
   [L("In this Roblox game, that egg might be a player.",
      CLIP("rb24-fe-a.mp4", "FAKE AN EGG", "NOT EVERY EGG IS REAL", 0, FEC)),
    L("Fake an Egg came out on October 4th. You disguise yourself as an egg, and wait for a victim.",
      CLIP("rb24-fe-b.mp4", "DISGUISE", "WAIT FOR A VICTIM", 0, FEC)),
    L("Then you steal their best pet, while they're not looking.",
      CLIP("rb24-fe-c.mp4", "STEAL\nTHEIR PET", "DON'T GET CAUGHT", 0, FEC)),
    L("It's under 4 weeks old, with almost 39 million visits.",
      CCOUNT("rb24-fe-a.mp4", 6.0, FEC, 38904782, "VISITS", bs=140)),
    ask("Would you fall for it?", "WOULD YOU\nFALL FOR IT?", "rb24-fe-a.mp4", FEC),
    subline("rb24-fe-a.mp4", FEC, 3.0),
   ])

# ============================================================ POPULAR NICHES (real clips only)
BKC = "Clips: Backrooms trailer, A24; Kane Pixels (YouTube)"
clip("tr24-bk-a.mp4", "https://www.youtube.com/watch?v=0HjdiohVOik", "*2:03-2:18", cut=0)
clip("tr24-bk-b.mp4", "https://www.youtube.com/watch?v=H4dGpz6cnHo", "*8:22-8:42", cut=0)
clip("tr24-bk-c.mp4", "https://www.youtube.com/watch?v=0HjdiohVOik", "*0:30-0:50", cut=0)
ep(217, "backrooms-a24", "The Backrooms Went From One Photo to A24s Biggest Opening", MIKE, "#ffd54f",
   {"font": MF + "Anton-Regular.ttf", "size": 104, "hi": "#ffe082", "stroke": 8},
   [L("It started as one creepy photo. Now it's A24's biggest opening ever.",
      CLIP("tr24-bk-c.mp4", "BACKROOMS", "A24", 6.0, BKC)),
    L("In 2019, someone posted this empty yellow room on 4chan, and called it the Backrooms.",
      CLIP("tr24-bk-c.mp4", "ONE PHOTO", "MAY 2019", 0, BKC)),
    L("In 2022, teenage YouTuber Kane Parsons made this video. 97 million views.",
      CCOUNT("tr24-bk-b.mp4", 0, BKC, 97325058, "VIEWS")),
    L("A24 made it a movie, and it opened with 81 million dollars.",
      CLIP("tr24-bk-c.mp4", "$81 MILLION", "OPENING WEEKEND", 6.0, BKC)),
    ask("Would you survive the Backrooms?", "WOULD YOU\nSURVIVE?", "tr24-bk-c.mp4", BKC, 6.0),
    subline("tr24-bk-c.mp4", BKC, 9.0),
   ], pron={"A24": "A twenty four", "4chan": "four chan"}, prop_clip="tr24-bk-c.mp4", edition="BACKROOMS", mood="spooky")

HBC = "Clips: Brocraft stream (2010); SeaWattgaming; Lessons in Meme Culture (YouTube)"
clip("tr24-hb-a.mp4", "https://www.youtube.com/watch?v=5LXE-FKSv8c", "*0:00-0:23", cut=0, backup=["https://www.youtube.com/watch?v=WBC4gcklXNE"])
clip("tr24-hb-b.mp4", "https://www.youtube.com/watch?v=gO0bJlXEG5w", "*2:00-2:20", cut=0)
clip("tr24-hb-c.mp4", "https://www.youtube.com/watch?v=qYR3SNauEwI", "*0:30-0:50", cut=0)
ep(218, "herobrine-origin", "Where Herobrine Came From", LIAM, "#e0e0e0",
   {"font": MF + "BlackOpsOne-Regular.ttf", "size": 92, "fill": "#ffffff", "hi": "#ffffff", "stroke": 8},
   [L("This 2010 livestream helped start Minecraft's biggest legend.",
      CLIP("tr24-hb-a.mp4", "HEROBRINE", "2010", 3.0, HBC)),
    L("That year, someone posted on 4chan about a player with white eyes in their single player world, named Herobrine.",
      CLIP("tr24-hb-b.mp4", "WHITE EYES", "THE 4CHAN POST", 0, HBC)),
    L("Then streamers started faking their own sightings, live.",
      CLIP("tr24-hb-a.mp4", "FAKED\nLIVE", "THE STREAM HOAX", 0, HBC)),
    L("He was never actually in the game. But Mojang still jokes about removing him in update notes.",
      CLIP("tr24-hb-c.mp4", "NEVER\nREAL", "\"REMOVED HEROBRINE\"", 0, HBC)),
    ask("Did you ever believe in Herobrine?", "DID YOU\nBELIEVE?", "tr24-hb-a.mp4", HBC, 3.0),
    subline("tr24-hb-a.mp4", HBC, 6.0),
   ], pron={"Herobrine": "Hero brine", "4chan": "four chan", "Mojang": "Mo-jang"}, prop_clip="tr24-hb-b.mp4",
   edition="MINECRAFT", mood="spooky")

UPC = "Clips: pannenkoek2012; UncommentatedPannen (YouTube)"
clip("tr24-up-a.mp4", "https://www.youtube.com/watch?v=aNzTUdOHm9A", "*0:17-0:37", cut=0)
clip("tr24-up-b.mp4", "https://www.youtube.com/watch?v=X5cwuYFUUAY", "*0:04-0:24", cut=0)
clip("tr24-up-c.mp4", "https://www.youtube.com/watch?v=vj8DzA9y8ls", "*0:30-0:50", cut=0)
ep(219, "mario-64-upwarp", "Mario Flew Into the Air and Nobody Knows Why", SARAH, "#ff1744",
   {"font": MF + "RussoOne-Regular.ttf", "size": 92, "hi": "#ff8a80", "stroke": 8},
   [L("In 2013, Mario suddenly flew up into the air, and nobody knows why.",
      CLIP("tr24-up-a.mp4", "THE\nUPWARP", "SUPER MARIO 64", 0, UPC)),
    L("A streamer called DOTA_Teabag was playing Super Mario 64, when Mario warped up in Tick Tock Clock.",
      CLIP("tr24-up-a.mp4", "TICK TOCK\nCLOCK", "DOTA_TEABAG", 5.0, UPC, bs=130)),
    L("Pannenkoek found it matched one single bit changing in Mario's height, and offered 1,000 dollars to anyone who could recreate it.",
      CLIP("tr24-up-b.mp4", "ONE BIT", "$1,000 BOUNTY", 0, UPC, bs=180)),
    L("The famous theory is a cosmic ray from space. Others think it was a bad cartridge. It's never been proven.",
      CLIP("tr24-up-a.mp4", "COSMIC\nRAY?", "NEVER PROVEN", 9.0, UPC)),
    ask("Cosmic ray, or bad cartridge?", "COSMIC RAY OR\nCARTRIDGE?", "tr24-up-a.mp4", UPC),
    subline("tr24-up-a.mp4", UPC, 3.0),
   ], pron={"DOTA_Teabag": "Dota Teabag", "Pannenkoek": "Pan-uh-cook"}, prop_clip="tr24-up-b.mp4", edition="SUPER MARIO 64")

TPC = "Clips: Twitch Plays Pokemon (icymate; captain Crab; TheGamerFromMars, YouTube)"
clip("tr24-tp-a.mp4", "https://www.youtube.com/watch?v=8MTRwoY-oDQ", "*2:34-2:54", cut=0)
clip("tr24-tp-b.mp4", "https://www.youtube.com/watch?v=dEaLWXJC5Fg", "*0:00-0:20", cut=0)
clip("tr24-tp-c.mp4", "https://www.youtube.com/watch?v=hEKbfId5oHM", "*26:05-26:25", cut=0)
ep(220, "twitch-plays-pokemon", "1 Million People Played One Game of Pokemon", HEART, "#ffca28",
   {"font": MF + "Bangers-Regular.ttf", "size": 120, "mode": "word", "fill": "#ffffff", "hi": "#ffe57f", "cy": 1470},
   [L("In 2014, over a million people played one game of Pokémon, at the same time.",
      CLIP("tr24-tp-a.mp4", "TWITCH PLAYS\nPOKEMON", "1 GAME, 1 MILLION PLAYERS", 0, TPC, bs=120, ss=48)),
    L("Every chat message was a button press, and over 1.16 million people joined in.",
      CCOUNT("tr24-tp-c.mp4", 0, TPC, 1165140, "PLAYERS")),
    L("It was total chaos. Players kept checking the Helix Fossil, until it became their god, Lord Helix.",
      CLIP("tr24-tp-b.mp4", "LORD\nHELIX", "ALL HAIL", 0, TPC)),
    L("After 16 days, they actually beat Pokémon Red, and it won a Game Award.",
      CLIP("tr24-tp-a.mp4", "BEATEN", "16 DAYS", 6.0, TPC, bs=180)),
    ask("Could chat beat a game today?", "COULD CHAT\nDO IT TODAY?", "tr24-tp-a.mp4", TPC),
    subline("tr24-tp-a.mp4", TPC, 3.0),
   ], pron={"Pokémon": "Poke-ay-mon"}, prop_clip="tr24-tp-b.mp4", edition="POKEMON")

# ================================================================== write
paths = []
for e in RB:
    e = dict(preset="roblox", hdr="tag", **e)
    words = sum(len(l.get("say", l["t"]).split()) for l in e["lines"])
    p = os.path.join("episodes", "roblox", e["slug"] + ".json")
    json.dump(e, open(os.path.join(ROOT, p), "w"), indent=1, ensure_ascii=False)
    paths.append(p)
    print(e["slug"], len(e["lines"]), "lines", words, "words")
manifest = {"batch": 24, "note": "spaceuk, Artemis 13, Kenos, Backseat Rally, What If Disasters, Fake an Egg, Backrooms, Herobrine, Mario 64 upwarp, Twitch Plays Pokemon",
            "posting": "batch-24/posting.txt", "episodes": paths, "clips": CLIPS}
json.dump(manifest, open(os.path.join(ROOT, "batches", "batch-24.json"), "w"), indent=1)
print(len(CLIPS), "clips")
