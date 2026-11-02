"""Writes batch 27 (facts checked 2026-11-02): NNN meme lore + Fortnite Pirate Shop + 3 GD + 5 Roblox = #241-250.

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


GD_PRON.update({"Zoink": "Zoynk", "w3rty": "werty", "dovvin": "dovvin", "murkkat": "murk cat", "OddMod": "Odd Mod",
                "RobTop": "Rob Top", "xStep": "ex step"})

# ============================================================ MEME LORE: NNN (user: make it exceptionally funny, keep it clean)
NNC = "Clips: Bramozed; CarbonFlash; lincth0m (YouTube)"
clip("tr27-nn-a.mp4", "https://www.youtube.com/watch?v=GblvGhuRgHE", "*1:22-1:42", cut=0)
clip("tr27-nn-b.mp4", "https://www.youtube.com/watch?v=uhDpfolqn2Q", "*1:00-1:20", cut=0)
clip("tr27-nn-c.mp4", "https://www.youtube.com/watch?v=uhDpfolqn2Q", "*3:30-3:50", cut=0)
clip("tr27-nn-d.mp4", "https://www.youtube.com/watch?v=j5YpDusOS5o", "*0:12-0:32", cut=0)
ep(241, "no-nut-november", "No Nut November Is Harder Than Tidal Wave", PUCK, "#ff9100",
   {"font": MF + "Bangers-Regular.ttf", "size": 120, "mode": "word", "fill": "#ffffff", "hi": "#ffd180", "cy": 1470},
   [L("It's November 2nd, and some of you have already lost No Nut November.",
      CLIP("tr27-nn-a.mp4", "NO NUT\nNOVEMBER", "DAY 2", 0, NNC)),
    L("It started as an Urban Dictionary joke in 2011. The rules? For 30 days, you don't. That's it. That's the whole game.",
      CLIP("tr27-nn-a.mp4", "THE RULES", "YOU KNOW WHAT YOU DID", 4.0, NNC, bs=180)),
    L("By 2019, 52,000 men had joined the subreddit, holding each other accountable. Brothers in arms.",
      CCOUNT("tr27-nn-c.mp4", 4.0, NNC, 52000, "BROTHERS IN ARMS")),
    L("Scientists say it does basically nothing. Players say it's the hardest level ever made. Harder than Tidal Wave.",
      CLIP("tr27-nn-d.mp4", "HARDER THAN\nTIDAL WAVE", "EXTREME DEMON", 2.0, NNC, bs=120)),
    ask("What day are you on? Be honest.", "WHAT DAY\nARE YOU ON?", "tr27-nn-a.mp4", NNC),
    subline("tr27-nn-a.mp4", NNC, 3.0),
   ], pron={"NNN": "N N N"}, prop_clip="tr27-nn-a.mp4", edition="MEME LORE")

# ============================================================ FORTNITE: Pirate Shop (Dexerto / Shane the Gamer, Nov 1-2)
FNC = "Clips: Fortnite (Epic Games); Ali-A; Coldside (YouTube)"
clip("tr27-fn-a.mp4", "https://www.youtube.com/watch?v=kJj7hV20p0Y", "*0:00-0:20", cut=0, backup=["https://www.youtube.com/watch?v=RoUsl_Jurzg"])
clip("tr27-fn-b.mp4", "https://www.youtube.com/watch?v=rnjWNafJy8Q", "*0:30-0:50", cut=0)
clip("tr27-fn-c.mp4", "https://www.youtube.com/watch?v=3grl3jv3kAI", "*2:00-2:20", cut=0, backup=["https://www.youtube.com/watch?v=NMPsjlNEF4o"])
clip("tr27-fn-d.mp4", "https://www.youtube.com/watch?v=kJj7hV20p0Y", "*3:00-3:20", cut=0)
ep(242, "fortnite-pirate-shop", "This Fortnite Chest Makes the Whole Item Shop Free", MIKE, "#00b0ff",
   {"font": MF + "Bangers-Regular.ttf", "size": 120, "mode": "word", "fill": "#ffffff", "hi": "#80d8ff", "cy": 1470},
   [L("There's a chest in Fortnite that makes the entire Item Shop free.",
      CLIP("tr27-fn-a.mp4", "FREE ITEM\nSHOP", "FROM ONE CHEST", 0, FNC, bs=130)),
    L("It's called the Pirate Shop, and since November 1st, it can drop from chests in Battle Royale.",
      CLIP("tr27-fn-b.mp4", "THE PIRATE\nSHOP", "TREASURE HUNTERS", 0, FNC, bs=130)),
    L("Find it, and everything you'd buy with V-Bucks is free for 14 days. Twice. Once this year, once next year.",
      CLIP("tr27-fn-c.mp4", "14 DAYS\nFREE", "TWICE", 0, FNC, bs=150)),
    L("One player found it after about 150 chests, and it looked like a normal chest. Epic won't say how rare it is.",
      CCOUNT("tr27-fn-d.mp4", 0, FNC, 150, "CHESTS OPENED", fmt="~{:,.0f}")),
    ask("How many chests would you open?", "HOW MANY\nCHESTS?", "tr27-fn-a.mp4", FNC),
    subline("tr27-fn-a.mp4", FNC, 3.0),
   ], pron={"V-Bucks": "V Bucks"}, prop_clip="tr27-fn-b.mp4", edition="FORTNITE")

# ============================================================ GEOMETRY DASH (GD wiki, Nov 2)
AWC = "Clips: Zoink; Nexus (YouTube)"
clip("gd27-aw-a.mp4", "https://www.youtube.com/watch?v=aTxt76U3e2Q", "*2:12-2:32", cut=0)
clip("gd27-aw-b.mp4", "https://www.youtube.com/watch?v=aTxt76U3e2Q", "*1:00-1:20", cut=0)
clip("gd27-aw-c.mp4", "https://www.youtube.com/watch?v=KrdMngKSLKc", "*1:20-1:40", cut=0)
ep(243, "ashley-wave-trials", "This Level Stayed Unrated for a Year Because of a Mod", LIAM, "#ff1744",
   {"font": MF + "Anton-Regular.ttf", "size": 104, "hi": "#ff8a80", "stroke": 8},
   [L("This level stayed unrated for over a year, because of a mod.",
      CLIP("gd27-aw-a.mp4", "ASHLEY WAVE\nTRIALS", "VERIFIED", 0, AWC, bs=120)),
    L("Ashley Wave Trials is a wave level by OddMod, with speed changes all the way up to four times speed.",
      CLIP("gd27-aw-c.mp4", "4X SPEED", "THE WAVE GAUNTLET", 0, AWC, bs=180)),
    L("Zoink verified it in November 2024, after 13,677 attempts.",
      CCOUNT("gd27-aw-b.mp4", 0, AWC, 13677, "ATTEMPTS")),
    L("But he used a mod called Click Between Frames, so it stayed unrated. Until January, when the game added that feature itself.",
      CLIP("gd27-aw-b.mp4", "CLICK BETWEEN\nFRAMES", "RATED IN JANUARY 2026", 6.0, AWC, bs=110)),
    ask("Should mods count?", "SHOULD MODS\nCOUNT?", "gd27-aw-a.mp4", AWC),
    subline("gd27-aw-a.mp4", AWC, 3.0),
   ], pron=dict(GD_PRON), gd_player="Zoink", **GDE)

PNC = "Clips: w3rty (YouTube)"
clip("gd27-pn-a.mp4", "https://www.youtube.com/watch?v=nVHPFf13M-I", "*1:12-1:27", cut=0)
clip("gd27-pn-b.mp4", "https://www.youtube.com/watch?v=nVHPFf13M-I", "*0:40-1:00", cut=0)
clip("gd27-pn-c.mp4", "https://www.youtube.com/watch?v=wN80tDzbkkY", "*1:20-1:40", cut=0)
ep(244, "penumbral-12-days", "He Beat It in 12 Days the Next Guy Needed 50,000 Attempts", FENRIR, "#7c4dff",
   {"font": MF + "BlackOpsOne-Regular.ttf", "size": 92, "fill": "#ffffff", "hi": "#b388ff", "stroke": 8},
   [L("One player beat this level in 12 days. The next one needed 50,000 attempts.",
      CLIP("gd27-pn-a.mp4", "PENUMBRAL", "VERIFIED", 0, PNC)),
    L("Penumbral is a Cherry Team collab, and the hardest level ever made to the song xStep.",
      CLIP("gd27-pn-b.mp4", "XSTEP", "THE HARDEST XSTEP LEVEL", 0, PNC, bs=200)),
    L("w3rty verified it in just 12 days, and it was rated around top 10.",
      CLIP("gd27-pn-c.mp4", "12 DAYS", "W3RTY", 0, PNC, bs=200)),
    L("The first person to beat it after him was dovvin, after around 50,000 attempts.",
      CCOUNT("gd27-pn-b.mp4", 6.0, PNC, 50000, "ATTEMPTS", fmt="~{:,.0f}")),
    ask("12 days, or 50,000 attempts?", "12 DAYS OR\n50,000?", "gd27-pn-a.mp4", PNC),
    subline("gd27-pn-a.mp4", PNC, 3.0),
   ], pron=dict(GD_PRON), gd_player="w3rty", **GDE)

BLC = "Clips: Zoink (YouTube)"
clip("gd27-bl-a.mp4", "https://www.youtube.com/watch?v=ROuXHSKEhHA", "*17:58-18:18", cut=0)
clip("gd27-bl-b.mp4", "https://www.youtube.com/watch?v=ROuXHSKEhHA", "*16:21-16:41", cut=0)
clip("gd27-bl-c.mp4", "https://www.youtube.com/watch?v=ROuXHSKEhHA", "*17:25-17:45", cut=0)
ep(245, "the-bloop-buffed", "Zoink Made The Bloop Harder While Beating It", MIKE, "#00e5ff",
   {"font": MF + "RussoOne-Regular.ttf", "size": 92, "hi": "#84ffff", "stroke": 8},
   [L("He made this level harder, while he was still trying to beat it.",
      CLIP("gd27-bl-a.mp4", "THE BLOOP", "VERIFIED", 0, BLC)),
    L("The Bloop is a giant collab hosted by murkkat. Zoink started verifying it last November.",
      CLIP("gd27-bl-b.mp4", "ZOINK", "THE VERIFIER", 0, BLC, bs=200)),
    L("In February, he started from zero. 28 percent, then 42, 56, 71.",
      CLIP("gd27-bl-c.mp4", "28% 42%\n56% 71%", "FROM ZERO", 0, BLC, bs=130)),
    L("Then he started buffing it, making it even harder. 83, 95, and in March, verified.",
      CLIP("gd27-bl-a.mp4", "BUFFED\nIT", "THEN BEAT IT", 6.0, BLC, bs=170)),
    ask("Would you make a level harder before beating it?", "WOULD YOU\nBUFF IT?", "gd27-bl-a.mp4", BLC),
    subline("gd27-bl-a.mp4", BLC, 3.0),
   ], pron=dict(GD_PRON), gd_player="Zoink", **GDE)

# ============================================================ ROBLOX (live numbers from Roblox, Nov 2)
MCC = "Clips: Yazn; MBT (Roblox gameplay, YouTube)"
clip("rb27-mc-a.mp4", "https://www.youtube.com/watch?v=FF54UTOPmMM", "*1:00-1:20", cut=0, backup=["https://www.youtube.com/watch?v=jHl31RjBxBo"])
clip("rb27-mc-b.mp4", "https://www.youtube.com/watch?v=FF54UTOPmMM", "*6:00-6:20", cut=0)
clip("rb27-mc-c.mp4", "https://www.youtube.com/watch?v=jHl31RjBxBo", "*10:00-10:20", cut=0, backup=["https://www.youtube.com/watch?v=EevOgTo6k90"])
ep(246, "1m-clicks-to-escape", "In This Roblox Game You Click a Button 1 Million Times to Escape", PUCK, "#ff1744",
   {"font": MF + "Bangers-Regular.ttf", "size": 120, "mode": "word", "fill": "#ffffff", "hi": "#ff8a80", "cy": 1470},
   [L("In this Roblox game, the only way out is to click one button, a million times.",
      CLIP("rb27-mc-a.mp4", "1M CLICKS\nTO ESCAPE", "THE ONLY WAY OUT", 0, MCC, bs=130)),
    L("You signed up for a game show. Now you're locked in a white room, with a big red button.",
      CLIP("rb27-mc-b.mp4", "THE WHITE\nROOM", "ONE RED BUTTON", 0, MCC, bs=140)),
    L("Click it 1,000,000 times. Unlock upgrades, earn gems, and uncover the lore of who locked you in.",
      CCOUNT("rb27-mc-c.mp4", 0, MCC, 1000000, "CLICKS TO GO")),
    L("It already has over 1.3 million visits. Probably fewer clicks than you need.",
      CLIP("rb27-mc-a.mp4", "1.3 MILLION\nVISITS", "KEEP CLICKING", 6.0, MCC, bs=130)),
    ask("How long would it take you?", "HOW LONG\nFOR YOU?", "rb27-mc-a.mp4", MCC),
    subline("rb27-mc-a.mp4", MCC, 3.0),
   ])

TRC = "Clips: Game N Go; Roblox gameplay (YouTube)"
clip("rb27-tr-a.mp4", "https://www.youtube.com/watch?v=Nrf7lsPwFAo", "*1:00-1:20", cut=0, backup=["https://www.youtube.com/watch?v=FyGk8din8RM"])
clip("rb27-tr-b.mp4", "https://www.youtube.com/watch?v=Nrf7lsPwFAo", "*6:00-6:20", cut=0)
clip("rb27-tr-c.mp4", "https://www.youtube.com/watch?v=FyGk8din8RM", "*3:00-3:20", cut=0, backup=["https://www.youtube.com/watch?v=YU5P9hoIwWE"])
ep(247, "tesla-roadster-chase", "In This Roblox Game You Steal a Brand New Roadster", FENRIR, "#ff3d00",
   {"font": MF + "RussoOne-Regular.ttf", "size": 92, "hi": "#ff9e80", "stroke": 8},
   [L("In this Roblox game, you steal a brand new sports car right off the showroom stage.",
      CLIP("rb27-tr-a.mp4", "ROADSTER\nCHASE", "STEAL IT", 0, TRC)),
    L("Then the police show up. Escape through a big city, with highways, back roads and shortcuts.",
      CLIP("rb27-tr-b.mp4", "ESCAPE THE\nPOLICE", "HIGHWAYS AND SHORTCUTS", 0, TRC, bs=130)),
    L("Weave through traffic at crazy speeds, and don't get boxed in.",
      CLIP("rb27-tr-c.mp4", "DON'T GET\nCAUGHT", "WEAVE THROUGH TRAFFIC", 0, TRC, bs=140)),
    L("It came out in late October, and already has over 3.8 million visits.",
      CCOUNT("rb27-tr-b.mp4", 6.0, TRC, 3828424, "VISITS", bs=140)),
    ask("How long could you outrun the cops?", "HOW LONG\nCOULD YOU LAST?", "rb27-tr-a.mp4", TRC),
    subline("rb27-tr-a.mp4", TRC, 3.0),
   ])

PPC = "Clips: OTTER ON ROBLOX; DraculDaculDacul (Roblox gameplay, YouTube)"
clip("rb27-pp-a.mp4", "https://www.youtube.com/watch?v=7J7Ywaeb3lQ", "*2:00-2:20", cut=0, backup=["https://www.youtube.com/watch?v=X-dICXSsJ60"])
clip("rb27-pp-b.mp4", "https://www.youtube.com/watch?v=7J7Ywaeb3lQ", "*10:00-10:20", cut=0)
clip("rb27-pp-c.mp4", "https://www.youtube.com/watch?v=M4NidrTFHa8", "*20:00-20:20", cut=0, backup=["https://www.youtube.com/watch?v=1BJjLWZRaAI"])
ep(248, "punch-out-of-prison", "In This Roblox Game You Punch Your Way Out of Prison", LIAM, "#ff6d00",
   {"font": MF + "Anton-Regular.ttf", "size": 104, "hi": "#ffab40", "stroke": 8},
   [L("In this Roblox game, you escape prison with your bare hands.",
      CLIP("rb27-pp-a.mp4", "PUNCH OUT\nOF PRISON", "BARE HANDS", 0, PPC)),
    L("You and your friends are locked in a cell. Punch the walls, one cube at a time.",
      CLIP("rb27-pp-b.mp4", "CUBE BY\nCUBE", "BREAK THE WALL", 0, PPC, bs=150)),
    L("Escape once, and chapter 2 opens. Dig up a buried crate, and carry it to the gate.",
      CLIP("rb27-pp-c.mp4", "CHAPTER 2", "THE YARD", 0, PPC, bs=180)),
    L("It's about 2 weeks old, with over 2.3 million visits.",
      CCOUNT("rb27-pp-b.mp4", 6.0, PPC, 2373713, "VISITS", bs=140)),
    ask("Who would you break out with?", "WHO'S YOUR\nCELLMATE?", "rb27-pp-a.mp4", PPC),
    subline("rb27-pp-a.mp4", PPC, 3.0),
   ])

HUC = "Clips: UnoTwo; Imadumbo (Roblox gameplay, YouTube)"
clip("rb27-hu-a.mp4", "https://www.youtube.com/watch?v=tLUr8opXaT4", "*1:00-1:20", cut=0, backup=["https://www.youtube.com/watch?v=RQgmjLnIvmo"])
clip("rb27-hu-b.mp4", "https://www.youtube.com/watch?v=tLUr8opXaT4", "*6:00-6:20", cut=0)
clip("rb27-hu-c.mp4", "https://www.youtube.com/watch?v=RQgmjLnIvmo", "*3:00-3:20", cut=0, backup=["https://www.youtube.com/watch?v=p56gJeXt-m4"])
ep(249, "hush-they-can-hear", "In HUSH the Monsters Hunt by Sound", SARAH, "#9e9e9e",
   {"font": MF + "BlackOpsOne-Regular.ttf", "size": 92, "fill": "#ffffff", "hi": "#e0e0e0", "stroke": 8},
   [L("In this Roblox game, the monsters can't see you. But they can hear you.",
      CLIP("rb27-hu-a.mp4", "HUSH", "THEY CAN HEAR", 0, HUC)),
    L("Monsters took over the town. You crawl out of the sewers, after hiding for a long time.",
      CLIP("rb27-hu-b.mp4", "THE TOWN\nIS GONE", "OUT OF THE SEWERS", 0, HUC, bs=140)),
    L("Sneak into houses, the hospital, and the army camp. Loot, hotwire a car, and get out before they hear you.",
      CLIP("rb27-hu-c.mp4", "STAY\nQUIET", "LOOT AND GET OUT", 0, HUC, bs=170)),
    L("It's still in beta, and it already has over 9.7 million visits.",
      CCOUNT("rb27-hu-b.mp4", 6.0, HUC, 9707832, "VISITS", bs=140)),
    ask("Could you stay quiet?", "COULD YOU\nSTAY QUIET?", "rb27-hu-a.mp4", HUC),
    subline("rb27-hu-a.mp4", HUC, 3.0),
   ], mood="spooky")

CDC = "Clips: ToyTaanic; CR11MS0N (Roblox gameplay, YouTube)"
clip("rb27-cd-a.mp4", "https://www.youtube.com/watch?v=PYQWUhcPddw", "*1:00-1:20", cut=0)
clip("rb27-cd-b.mp4", "https://www.youtube.com/watch?v=PYQWUhcPddw", "*7:00-7:20", cut=0)
clip("rb27-cd-c.mp4", "https://www.youtube.com/watch?v=JVXwFXiRPuE", "*0:03-0:23", cut=0)
ep(250, "create-a-disaster", "In This Roblox Game You Are the Disaster", HEART, "#ffd600",
   {"font": MF + "Bangers-Regular.ttf", "size": 120, "mode": "word", "fill": "#ffffff", "hi": "#ffff00", "cy": 1470},
   [L("In this Roblox game, you don't survive the disaster. You are the disaster.",
      CLIP("rb27-cd-a.mp4", "CREATE A\nDISASTER", "BLOW IT ALL UP", 4.0, CDC)),
    L("Drop meteors, tornadoes, nukes, and black holes on the city, and earn cash for every disaster.",
      CLIP("rb27-cd-b.mp4", "METEORS.\nNUKES.", "BLACK HOLES", 0, CDC, bs=150)),
    L("Save up, and you can summon the Kraken, a giant kaiju, or a crashing space station.",
      CLIP("rb27-cd-c.mp4", "THE KRAKEN", "SUMMON IT", 0, CDC, bs=180)),
    L("It came out in October, and it already has over 6 million visits.",
      CCOUNT("rb27-cd-b.mp4", 6.0, CDC, 6086164, "VISITS", bs=140)),
    ask("What disaster would you drop first?", "WHAT WOULD\nYOU DROP?", "rb27-cd-a.mp4", CDC, 4.0),
    subline("rb27-cd-a.mp4", CDC, 8.0),
   ], pron={"kaiju": "kai-joo"})

# ================================================================== write
paths = []
for e in RB:
    e = dict(preset="roblox", hdr="tag", **e)
    words = sum(len(l.get("say", l["t"]).split()) for l in e["lines"])
    p = os.path.join("episodes", "roblox", e["slug"] + ".json")
    json.dump(e, open(os.path.join(ROOT, p), "w"), indent=1, ensure_ascii=False)
    paths.append(p)
    print(e["slug"], len(e["lines"]), "lines", words, "words")
manifest = {"batch": 27, "note": "No Nut November, Fortnite Pirate Shop, Ashley Wave Trials, Penumbral, The Bloop, 1M Clicks To Escape, Tesla Roadster Chase, Punch Out Of Prison, HUSH, Create A Disaster",
            "posting": "Z:/claudeprojects/roblox vids/batch-27/posting.txt", "episodes": paths, "clips": CLIPS}
json.dump(manifest, open(os.path.join(ROOT, "batches", "batch-27.json"), "w"), indent=1)
print(len(CLIPS), "clips")
