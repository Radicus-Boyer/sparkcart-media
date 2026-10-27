"""Writes batch 23 (facts checked 2026-10-27): 2 Roblox + 2 GD + 1 meme + 5 mainstream gaming = #201-210.

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
                   lead=0.8, tail=0.6, clip_audio=True, **k))


GD_PRON = {"Demonlist": "Demon list", "Zoink": "Zoynk", "wPopoff": "W Pop off", "Cuatrocientos": "Kwatro-see-entos"}
GDE = dict(edition="GEOMETRY DASH", mood="spooky")

# ============================================================ ROBLOX (live numbers from Roblox, Oct 27)
RRC = "Clips: Ragdoll Reality (Roblox gameplay, YouTube)"
clip("rb23-rr-a.mp4", "https://www.youtube.com/watch?v=7whZLVq5kGg", "*0:20-0:40", backup=["https://www.youtube.com/watch?v=vgR2t1p2o-c"])
clip("rb23-rr-b.mp4", "https://www.youtube.com/watch?v=Px_b_stPLCI", "*4:00-4:20", backup=["https://www.youtube.com/watch?v=gj7EBw9IMlc"])
clip("rb23-rr-c.mp4", "https://www.youtube.com/watch?v=G4J99kmjye8", "*0:40-1:00", backup=["https://www.youtube.com/watch?v=854qj154pWM"])
ep(201, "ragdoll-reality", "Ragdoll Reality Is 2 Weeks Old With 17 Million Visits", FENRIR, "#ff1744",
   {"font": MF + "Anton-Regular.ttf", "size": 104, "hi": "#ff8a80", "stroke": 8},
   [L("In this Roblox game, every hit lands exactly where you aim.",
      CLIP("rb23-rr-a.mp4", "RAGDOLL\nREALITY", "EVERY HIT IS REAL", 0, RRC)),
    L("Ragdoll Reality came out on October 13th. Shoot a leg, and the dummy limps. Hit an arm, and it dangles.",
      CLIP("rb23-rr-b.mp4", "REAL\nPHYSICS", "2 WEEKS OLD", 0, RRC)),
    L("And for Halloween, dummies you throw in the graveyard come back as zombies.",
      CLIP("rb23-rr-c.mp4", "ZOMBIE\nUPDATE", "SURVIVE THE HORDE", 0, RRC)),
    L("In 2 weeks, it got over 17 million visits.",
      CCOUNT("rb23-rr-b.mp4", 6.0, RRC, 17345568, "VISITS IN 2 WEEKS")),
    ask("What's the first weapon you're grabbing?", "FIRST\nWEAPON?", "rb23-rr-a.mp4", RRC),
   ], mood="spooky")

BUC = "Clips: Bike Universe (Roblox gameplay, YouTube)"
clip("rb23-bu-a.mp4", "https://www.youtube.com/watch?v=AslzO7dEIBU", "*3:00-3:20", backup=["https://www.youtube.com/watch?v=AQtzq6GovRg"])
clip("rb23-bu-b.mp4", "https://www.youtube.com/watch?v=RxpADLMyMgg", "*2:00-2:20", backup=["https://www.youtube.com/watch?v=F3r_oMMjxr0"])
ep(202, "bike-universe", "Bike Universe Got 35 Million Visits in a Month", LIAM, "#00e5ff",
   {"font": MF + "RussoOne-Regular.ttf", "size": 92, "hi": "#84ffff", "stroke": 8},
   [L("This Roblox game pays you to pull wheelies.",
      CLIP("rb23-bu-a.mp4", "BIKE\nUNIVERSE", "WHEELIES = MONEY", 0, BUC)),
    L("Bike Universe came out on September 27th. You earn money from riding, wheelies and tricks.",
      CLIP("rb23-bu-b.mp4", "TRICKS\nPAY", "SEPTEMBER 27", 0, BUC)),
    L("Then you collect dirt bikes, electric bikes and pedal bikes, tune them, and race your friends.",
      CLIP("rb23-bu-a.mp4", "DIRT. ELECTRIC.\nPEDAL.", "TUNE + RACE", 6.0, BUC, bs=120)),
    L("One month in, it has over 35 million visits.",
      CCOUNT("rb23-bu-b.mp4", 6.0, BUC, 35675299, "VISITS IN 1 MONTH")),
    ask("Dirt bike or electric?", "DIRT OR\nELECTRIC?", "rb23-bu-a.mp4", BUC),
   ])

# ============================================================ GEOMETRY DASH (stage "gd": real player icons)
GRC = "Clips: Doggie, Zoink, wPopoff; Creative Destruction; DashWire (YouTube)"
clip("gd23-gr-a.mp4", "https://www.youtube.com/watch?v=qw91o5kZkJQ", "*0:05-0:25", backup=["https://www.youtube.com/watch?v=wjP5-gXMcsw"])
clip("gd23-gr-b.mp4", "https://www.youtube.com/watch?v=Emd2tWP2FkI", "*2:35-2:55", backup=["https://www.youtube.com/watch?v=_nv9UsomBi0"])
clip("gd23-gr-c.mp4", "https://www.youtube.com/watch?v=Mo5v4RiaKuw", "*1:00-1:20", backup=["https://www.youtube.com/watch?v=ysbFAzForrc"])
ep(203, "grief-first-victor-race", "The Race to Be the First to Beat Grief", MIKE, "#ff1744",
   {"font": MF + "BlackOpsOne-Regular.ttf", "size": 92, "fill": "#ffffff", "hi": "#ff8a80", "stroke": 8},
   [L("Only one person has beaten the hardest level in Geometry Dash. Two more are racing to be next.",
      CLIP("gd23-gr-a.mp4", "GRIEF", "THE #1 HARDEST LEVEL", 0, GRC)),
    L("Doggie verified Grief on October 6th, after over 436,000 attempts.",
      CCOUNT("gd23-gr-b.mp4", 0, GRC, 436000, "DOGGIE'S ATTEMPTS", fmt="{:,.0f}+")),
    L("Nobody else has beaten it yet. But Zoink just hit 80 percent, and wPopoff hit 81.",
      dict(big="THE RACE", sub="FIRST VICTOR?", bs=150, by=300, race=[
          {"player": "Zoink", "pct": 80, "col": "#ff5252"}, {"player": "wPopoff", "pct": 81, "col": "#40c4ff"}])),
    L("Their best runs are almost frame for frame.",
      CLIP("gd23-gr-c.mp4", "80% VS 81%", "SIDE BY SIDE", 0, GRC, bs=130)),
    ask("Who beats it first, Zoink or wPopoff?", "ZOINK OR\nWPOPOFF?", "gd23-gr-a.mp4", GRC),
   ], pron=dict(GD_PRON), gd_player="Doggie", **GDE)

FWC = "Clips: Flamewall by Narwall & more, verified by Cuatrocientos (YouTube)"
clip("gd23-fw-a.mp4", "https://www.youtube.com/watch?v=x4Io4zkWVRw", "*9:18-9:38", backup=["https://www.youtube.com/watch?v=VqCSvBYK6wM"])
clip("gd23-fw-b.mp4", "https://www.youtube.com/watch?v=1gZEJI-2yQQ", "*6:58-7:18", backup=["https://www.youtube.com/watch?v=h_i8yS8nXvw"])
clip("gd23-fw-c.mp4", "https://www.youtube.com/watch?v=gwNYGFmo_WY", "*6:25-6:45", backup=["https://www.youtube.com/watch?v=wZbqwUv5NI8"])
ep(204, "flamewall-221703", "Flamewall Took 221,703 Attempts", FENRIR, "#ff6d00",
   {"font": MF + "Anton-Regular.ttf", "size": 104, "hi": "#ffab40", "stroke": 8},
   [L("This is what 221,703 attempts sounds like.",
      CLIP("gd23-fw-a.mp4", "FLAMEWALL", "VERIFIED", 0, FWC)),
    L("Cuatrocientos spent over 221,000 attempts verifying Flamewall, one of the hardest levels in Geometry Dash.",
      CCOUNT("gd23-fw-c.mp4", 0, FWC, 221703, "ATTEMPTS")),
    L("He died at 99 percent. Twice.",
      CLIP("gd23-fw-b.mp4", "99%", "TWICE", 0, FWC, bs=220)),
    L("Then in September 2025 he finally beat it, and it went in at number 2 on the Demonlist.",
      dict(big="TOP 2", sub="SEPTEMBER 2025", bs=200, by=300, mode="ship", player="Cuatrocientos", fx=["sparkle"])),
    ask("Would you have quit at 99?", "QUIT AT\n99%?", "gd23-fw-a.mp4", FWC),
   ], pron=dict(GD_PRON, Flamewall="Flame wall"), gd_player="Cuatrocientos", **GDE)

# ============================================================ MEME LORE (stage "meme")
SDC = "Clips: Star Wars: Galactic Racer (YouTube)"
clip("ml23-sd-a.mp4", "https://www.youtube.com/watch?v=Hv8U7YcJHAA", "*0:00-0:20", cut=0, backup=["https://www.youtube.com/watch?v=67dmM5UM-AQ"])
clip("ml23-sd-b.mp4", "https://www.youtube.com/watch?v=udF8djozQek", "*0:00-0:20", cut=0, backup=["https://www.youtube.com/watch?v=1sdegC3R1Vw"])
clip("ml23-sd-c.mp4", "https://www.youtube.com/watch?v=Ju9wvY_dIW4", "*2:00-2:20", backup=["https://www.youtube.com/watch?v=X7BaeEKcYTg"])
ep(205, "scrib-doon", "Where Scrib Doon Came From", PUCK, "#ffd740",
   {"font": MF + "Bangers-Regular.ttf", "size": 124, "mode": "word", "fill": "#ffffff", "hi": "#ffe57f", "cy": 1470},
   [L("Scrib doon. Why is everyone saying it?",
      CLIP("ml23-sd-a.mp4", "SCRIB\nDOON", "WHAT DOES IT MEAN?", 0, SDC)),
    L("It comes from Biddy Blas, an alien racer in Star Wars Galactic Racer, which came out on October 6th.",
      CLIP("ml23-sd-b.mp4", "BIDDY\nBLAS", "STAR WARS: GALACTIC RACER", 0, SDC, ss=46)),
    L("Before a race, he tells you his name, and says, write it down. In his language, that's scrib doon.",
      CLIP("ml23-sd-c.mp4", "\"WRITE IT\nDOWN\"", "= SCRIB DOON", 0, SDC, bs=130)),
    L("Players loved the delivery, and one clip of it has over 700,000 views.",
      CCOUNT("ml23-sd-a.mp4", 6.0, SDC, 711679, "VIEWS ON ONE CLIP")),
    ask("Did you write it down?", "DID YOU\nSCRIB DOON?", "ml23-sd-a.mp4", SDC),
   ], pron={"Biddy": "Biddy", "Blas": "Blahss", "Scrib": "Scrib", "doon": "doon"}, prop_clip="ml23-sd-a.mp4",
   edition="MEME LORE")

# ============================================================ MAINSTREAM GAMING (stage "news", but every scene is a real clip)
NFC = "Clips: Niftski, Super Mario Bros. Any% 4:54.332; TAS comparison by Reflect (YouTube)"
clip("tr23-nf-a.mp4", "https://www.youtube.com/watch?v=jeyjmJkhLb0", "*7:58-8:18", backup=["https://www.youtube.com/watch?v=VbNI9Ws3WKQ"])
clip("tr23-nf-b.mp4", "https://www.youtube.com/watch?v=jeyjmJkhLb0", "*5:13-5:33")
clip("tr23-nf-c.mp4", "https://www.youtube.com/watch?v=LbOGuC3_R2Y", "*1:00-1:20", backup=["https://www.youtube.com/watch?v=i2jj1RLVOas"])
ep(206, "niftski-4-frames", "Niftski Is 4 Frames From a Perfect Mario Run", HEART, "#ff3d00",
   {"font": MF + "RussoOne-Regular.ttf", "size": 92, "hi": "#ff9e80", "stroke": 8},
   [L("This is the fastest anyone has ever beaten Super Mario Bros.",
      CLIP("tr23-nf-a.mp4", "4:54.332", "WORLD RECORD", 0, NFC, bs=170)),
    L("Niftski set it in August: 4 minutes, 54.332 seconds.",
      CLIP("tr23-nf-b.mp4", "NIFTSKI", "AUGUST 13, 2026", 0, NFC)),
    L("The best run thought possible is 4:54.265. He's just 4 frames off. That's about a fifteenth of a second.",
      CLIP("tr23-nf-c.mp4", "4 FRAMES", "FROM PERFECT", 0, NFC, bs=180),
      say="The best run thought possible is 4 54 point 2 6 5. He's just 4 frames off. That's about a fifteenth of a second."),
    L("And right now, he's live streaming attempts to tie it.",
      CLIP("tr23-nf-b.mp4", "GOING FOR\nPERFECT", "LIVE ON STREAM", 6.0, NFC, bs=130)),
    ask("Can a human ever get a perfect run?", "PERFECT\nPOSSIBLE?", "tr23-nf-a.mp4", NFC),
   ], pron={"Niftski": "Nift-ski"}, prop_clip="tr23-nf-b.mp4", ticker="SUPER MARIO BROS. ANY% WORLD RECORD: 4:54.332",
   edition="SUPER MARIO BROS")

MCC = "Clips: skycrab1, Minecraft 6:39 world record; Couriway (YouTube)"
clip("tr23-mc-a.mp4", "https://www.youtube.com/watch?v=NemhyWVAY68", "*6:38-6:58", backup=["https://www.youtube.com/watch?v=ZflXGH-5Sks"])
clip("tr23-mc-b.mp4", "https://www.youtube.com/watch?v=NemhyWVAY68", "*0:00-0:20", cut=0)
clip("tr23-mc-c.mp4", "https://www.youtube.com/watch?v=84Y1dXrfP8A", "*7:20-7:40", backup=["https://www.youtube.com/watch?v=1LQ93_Hb2Io"])
ep(207, "minecraft-6-39", "Someone Beat Minecraft in 6 Minutes 39 Seconds", LIAM, "#76ff03",
   {"font": MF + "Anton-Regular.ttf", "size": 104, "hi": "#ccff90", "stroke": 8},
   [L("This player beat Minecraft faster than you can cook dinner.",
      CLIP("tr23-mc-a.mp4", "6:39", "MINECRAFT BEATEN", 0, MCC, bs=220)),
    L("Skycrab, from Norway, set the random seed world record in July: 6 minutes, 39 seconds.",
      CLIP("tr23-mc-b.mp4", "SKYCRAB", "JULY 27, 2026", 0, MCC)),
    L("New world, no glitches. Find a portal, the stronghold, then kill the Ender Dragon.",
      CLIP("tr23-mc-a.mp4", "NO\nGLITCHES", "RANDOM SEED", 5.0, MCC, bs=150)),
    L("His record video has over 1.5 million views.",
      CCOUNT("tr23-mc-c.mp4", 0, MCC, 1541552, "VIEWS")),
    ask("How long would it take you?", "YOUR\nTIME?", "tr23-mc-a.mp4", MCC),
   ], pron={"Skycrab": "Sky crab"}, prop_clip="tr23-mc-b.mp4", ticker="MINECRAFT ANY% RANDOM SEED WORLD RECORD: 6:39.813",
   edition="MINECRAFT")

TTC = "Clips: Blue Scuti; aGameScout; NBC News (YouTube)"
clip("tr23-tt-a.mp4", "https://www.youtube.com/watch?v=GuJ5UuknsHU", "*14:58-15:18", backup=["https://www.youtube.com/watch?v=J9oVQ43j22g"])
clip("tr23-tt-b.mp4", "https://www.youtube.com/watch?v=GuJ5UuknsHU", "*11:08-11:28")
clip("tr23-tt-c.mp4", "https://www.youtube.com/watch?v=dS_8CZy8DbI", "*0:35-0:55", backup=["https://www.youtube.com/watch?v=_hVACOeb7OA"])
ep(208, "blue-scuti-beat-tetris", "A 13 Year Old Was the First Person to Beat Tetris", SARAH, "#2979ff",
   {"font": MF + "BlackOpsOne-Regular.ttf", "size": 92, "fill": "#ffffff", "hi": "#82b1ff", "stroke": 8},
   [L("This is the moment a 13 year old beat Tetris.",
      CLIP("tr23-tt-a.mp4", "TETRIS\nBEATEN", "THE GAME CRASHED", 0, TTC)),
    L("NES Tetris came out in 1989. For 34 years, no human could beat it.",
      CLIP("tr23-tt-b.mp4", "34 YEARS", "NO HUMAN DID IT", 0, TTC, bs=180)),
    L("Then in December 2023, Blue Scuti played so far that the game froze at level 157. That's how you beat it.",
      CCOUNT("tr23-tt-b.mp4", 6.0, TTC, 157, "LEVEL THE GAME CRASHED")),
    L("He even got to meet the creator of Tetris.",
      CLIP("tr23-tt-c.mp4", "BLUE\nSCUTI", "MET THE CREATOR", 0, TTC)),
    ask("What game would you beat first?", "WHICH GAME\nWOULD YOU BEAT?", "tr23-tt-a.mp4", TTC),
   ], pron={"Scuti": "Scoot-ee"}, prop_clip="tr23-tt-b.mp4", ticker="NES TETRIS: FIRST HUMAN TO BEAT THE GAME", edition="TETRIS")

G6C = "Clips: Grand Theft Auto VI trailers, Rockstar Games (YouTube)"
clip("tr23-g6-a.mp4", "https://www.youtube.com/watch?v=VQRLujxTm3c", "*1:06-1:26")
clip("tr23-g6-b.mp4", "https://www.youtube.com/watch?v=Qqzj-j4qk0E", "*0:20-0:40", backup=["https://www.youtube.com/watch?v=oFwB6gZLRmc"])
clip("tr23-g6-c.mp4", "https://www.youtube.com/watch?v=tJbzMqJGH4k", "*5:00-5:20")
ep(209, "gta-6-launch-trailer", "GTA 6's Launch Trailer Is Out", MIKE, "#ff4081",
   {"font": MF + "Anton-Regular.ttf", "size": 104, "hi": "#ff80ab", "stroke": 8},
   [L("GTA 6 is 22 days away, and the launch trailer is finally out.",
      CLIP("tr23-g6-a.mp4", "GTA 6", "22 DAYS LEFT", 0, G6C, bs=200)),
    L("Rockstar dropped it on October 15th. The game comes out on November 19th.",
      CLIP("tr23-g6-b.mp4", "NOVEMBER 19", "LAUNCH TRAILER", 0, G6C)),
    L("Trailer 2 alone has over 185 million views on YouTube.",
      CCOUNT("tr23-g6-a.mp4", 6.0, G6C, 185787294, "VIEWS ON TRAILER 2", bs=140)),
    L("And Rockstar's 26 minute gameplay look got 33 million more.",
      CLIP("tr23-g6-c.mp4", "33 MILLION", "26 MIN GAMEPLAY", 0, G6C)),
    ask("Are you playing on day one?", "DAY ONE?", "tr23-g6-a.mp4", G6C),
   ], pron={"Rockstar": "Rock star"}, prop_clip="tr23-g6-b.mp4", ticker="GTA 6 RELEASES NOVEMBER 19, 2026", edition="GTA 6")

FNC = "Clips: Fortnitemares 2026 trailers, Epic Games; SinX6 (YouTube)"
clip("tr23-fn-a.mp4", "https://www.youtube.com/watch?v=tIkemvVEpSA", "*0:00-0:20", cut=0)
clip("tr23-fn-b.mp4", "https://www.youtube.com/watch?v=7qQFLL_DJ7Q", "*0:15-0:35", backup=["https://www.youtube.com/watch?v=5lddZVFmxaw"])
clip("tr23-fn-c.mp4", "https://www.youtube.com/watch?v=NN9JgTLWIKE", "*0:40-1:00", backup=["https://www.youtube.com/watch?v=tymP2iDiwPo"])
ep(210, "fortnitemares-freddy", "Freddy Krueger and FNAF Are in Fortnite", FENRIR, "#ff6d00",
   {"font": MF + "BlackOpsOne-Regular.ttf", "size": 92, "fill": "#ffffff", "hi": "#ffab40", "stroke": 8},
   [L("Freddy Krueger is a boss in Fortnite right now.",
      CLIP("tr23-fn-a.mp4", "FREDDY\nKRUEGER", "IN FORTNITE", 0, FNC)),
    L("Fortnitemares started October 1st. Freddy guards a new spot, Nightmare Neighborhood.",
      CLIP("tr23-fn-b.mp4", "NIGHTMARE\nNEIGHBORHOOD", "FORTNITEMARES 2026", 0, FNC, bs=120)),
    L("And at Freddy Fazbear's Pizzeria, you can beat the Five Nights at Freddy's animatronics, then become them.",
      CLIP("tr23-fn-c.mp4", "BECOME\nFOXY", "FNAF BOSSES", 0, FNC)),
    L("You can even use Freddy Krueger's claws. But it all ends on November 1st.",
      CLIP("tr23-fn-b.mp4", "ENDS\nNOV 1", "FREDDY'S CLAWS", 6.0, FNC)),
    ask("Which Freddy is scarier?", "WHICH FREDDY\nIS SCARIER?", "tr23-fn-a.mp4", FNC),
   ], prop_clip="tr23-fn-b.mp4", ticker="FORTNITEMARES 2026 ENDS NOVEMBER 1", edition="FORTNITE", mood="spooky")

# ================================================================== write
paths = []
for e in RB:
    e = dict(preset="roblox", hdr="tag", **e)
    words = sum(len(l.get("say", l["t"]).split()) for l in e["lines"])
    p = os.path.join("episodes", "roblox", e["slug"] + ".json")
    json.dump(e, open(os.path.join(ROOT, p), "w"), indent=1, ensure_ascii=False)
    paths.append(p)
    print(e["slug"], len(e["lines"]), "lines", words, "words", f"~{words / 2.75 + 1.4:.0f}s")
manifest = {"batch": 23, "note": "v2 format: 2 Roblox, 2 GD, Scrib Doon, Mario WR, Minecraft WR, Tetris, GTA 6, Fortnitemares (Oct 28)",
            "posting": "batch-23/posting.txt", "episodes": paths, "clips": CLIPS}
json.dump(manifest, open(os.path.join(ROOT, "batches", "batch-23.json"), "w"), indent=1)
print(len(CLIPS), "clips")
