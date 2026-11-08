"""Writes batch 33 (facts checked 2026-11-08): 4 meme lore + 3 GD (incl. Zoink long plug before 2:30) + 3 Roblox driving = #296-305.

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


# ---------------------------------------------------------------- 296 MEME: AI video game merging (KYM weekly roundup, Oct 9 2026)
AMC2 = "Clips: MrToucan Explains; Chrispreds3 (YouTube)"
clip("tr33-am-a.mp4", "https://www.youtube.com/watch?v=xkfIvE59AqA", "*5:00-5:20", cut=0)
clip("tr33-am-b.mp4", "https://www.youtube.com/watch?v=CVwrRn7COyc", "*1:00-1:20", cut=0)
clip("tr33-am-c.mp4", "https://www.youtube.com/watch?v=xkfIvE59AqA", "*12:00-12:20", cut=0)
ep(296, "ai-merging-video-games", "AI Is Merging Video Games Into One", LIAM, "#00e5ff", MCAP("#84ffff"),
   [L("Someone used AI to merge Call of Duty and Minecraft into one game. And people say you can actually play it.",
      CLIP("tr33-am-a.mp4", "COD +\nMINECRAFT", "ONE GAME?", 0, AMC2, bs=150)),
    L("It started on X, with a user who kept merging the Skate games with other games.",
      CLIP("tr33-am-b.mp4", "SKATE +\nEVERYTHING", "WHERE IT STARTED", 0, AMC2, bs=140)),
    L("Then he dropped Call of Duty mixed with Minecraft. And the internet lost it.",
      CLIP("tr33-am-c.mp4", "THE INTERNET\nLOST IT", "", 0, AMC2, bs=130)),
    L("It looks like an AI video. But it's supposedly a playable game.",
      CLIP("tr33-am-a.mp4", "PLAYABLE?", "", 7.0, AMC2, bs=150)),
    L("Now people are merging games old and new, and it's a little bit scary.",
      CLIP("tr33-am-c.mp4", "A LITTLE\nBIT SCARY", "", 7.0, AMC2, bs=140)),
    ask("Which two games should be merged next?", "WHICH TWO\nGAMES?", "tr33-am-a.mp4", AMC2),
    subline("tr33-am-b.mp4", AMC2, 8.0),
   ], edition="MEME LORE")

# ---------------------------------------------------------------- 297 MEME: Black Cat Clapping (KYM weekly roundup)
BCC = "Clips: Kitty POVs; flappy (YouTube)"
clip("tr33-bc-a.mp4", "https://www.youtube.com/watch?v=SsX8KDCKX1s", "*0:00-0:20", cut=0)
clip("tr33-bc-b.mp4", "https://www.youtube.com/watch?v=ww8kMw0FfUw", "*0:05-0:25", cut=0)
clip("tr33-bc-c.mp4", "https://www.youtube.com/watch?v=ww8kMw0FfUw", "*0:25-0:44", cut=0)
ep(297, "black-cat-clapping-meme", "Where the Clapping Cat Meme Came From", HEART, "#ffea00", MCAP("#ffff8d"),
   [L("This cat has human hands. And it will not stop clapping.",
      CLIP("tr33-bc-a.mp4", "HUMAN\nHANDS", "THE CLAPPING CAT", 0, BCC, bs=150)),
    L("It's from a comedy video by an Instagram creator. He gives his cat food, and the cat smiles, claps, and tries to shake his hand.",
      CLIP("tr33-bc-b.mp4", "IT TRIES TO\nSHAKE HANDS", "", 0, BCC, bs=130)),
    L("It's AI. And it got millions of views.",
      CCOUNT("tr33-bc-a.mp4", 7.0, BCC, 1000000, "VIEWS... AND COUNTING", fmt="{:,.0f}+", bs=130)),
    L("Now it's a green screen meme. The cat claps in the best and worst moments, like skipping class in a bathroom stall.",
      CLIP("tr33-bc-c.mp4", "BEST AND\nWORST MOMENTS", "", 0, BCC, bs=130)),
    ask("Is the clapping cat cute or cursed?", "CUTE OR\nCURSED?", "tr33-bc-a.mp4", BCC),
    subline("tr33-bc-c.mp4", BCC, 6.0),
   ], edition="MEME LORE")

# ---------------------------------------------------------------- 298 MEME: AI Rumpelstiltskin "Tip Toe" (KYM weekly roundup)
RPC2 = "Clips: Nunya Bizness; Official Dj.Solomo; Miss_Chiph (YouTube)"
clip("tr33-rp-a.mp4", "https://www.youtube.com/watch?v=jBpN6afe-ng", "*0:00-0:20", cut=0)
clip("tr33-rp-b.mp4", "https://www.youtube.com/watch?v=Qb91OznXzbg", "*0:02-0:22", cut=0)
clip("tr33-rp-c.mp4", "https://www.youtube.com/watch?v=Lg_1iR04Lcs", "*0:05-0:25", cut=0)
ep(298, "rumpelstiltskin-tip-toe-meme", "Why Rumpelstiltskin Is Tip Toeing in His Jordans", FENRIR, "#d500f9", MCAP("#ea80fc"),
   [L("Rumpelstiltskin is tip toeing in his Jordans. And it's making everyone uncomfortable.",
      CLIP("tr33-rp-a.mp4", "TIP TOEIN'", "IN HIS JORDANS", 0, RPC2, bs=150)),
    L("This isn't from a real movie. It's AI, made to look like an 80s fantasy film.",
      CLIP("tr33-rp-b.mp4", "100%\nAI", "AN 80s FANTASY THAT NEVER EXISTED", 0, RPC2, bs=150)),
    L("It was posted in August. Then in September, someone put it to a Riff Raff song, with a caption about taking too much melatonin.",
      CLIP("tr33-rp-a.mp4", "TOO MUCH\nMELATONIN", "+ RIFF RAFF", 6.0, RPC2, bs=140)),
    L("Now the dance means one thing: you're trolling. And people swap him with other characters.",
      CLIP("tr33-rp-c.mp4", "TROLL\nMODE", "", 0, RPC2, bs=150)),
    ask("Who should do the dance next?", "WHO'S\nNEXT?", "tr33-rp-a.mp4", RPC2),
    subline("tr33-rp-b.mp4", RPC2, 6.0),
   ], pron={"Rumpelstiltskin": "Rumple-stilt-skin"}, edition="MEME LORE")

# ---------------------------------------------------------------- 302 MEME: "You're Blatantly Just Not Me Nan" (KYM weekly roundup)
NNC = "Clips: MrTamozi; Meme Academy; Hypothetical Salam (YouTube)"
clip("tr33-nn-a.mp4", "https://www.youtube.com/watch?v=2DObGw2Czkg", "*0:05-0:25", cut=0)
clip("tr33-nn-b.mp4", "https://www.youtube.com/watch?v=-A8GSbr7K2g", "*0:20-0:40", cut=0)
clip("tr33-nn-c.mp4", "https://www.youtube.com/watch?v=7O8I-tHm8q8", "*0:10-0:30", cut=0)
ep(302, "blatantly-just-not-me-nan", "Youre Blatantly Just Not Me Nan Meme Explained", PUCK, "#ff6d00", MCAP("#ffab40"),
   [L("You're blatantly just not me nan.",
      CLIP("tr33-nn-a.mp4", "\"BLATANTLY\nNOT ME NAN\"", "", 0, NNC, bs=130)),
    L("It's from a skit. What if Little Red Riding Hood happened for real?",
      CLIP("tr33-nn-b.mp4", "LITTLE RED\nRIDING HOOD", "BUT REAL", 0, NNC, bs=130)),
    L("He walks into his nan's house, sees a wolf in her bed, and says it. That line went viral.",
      CLIP("tr33-nn-c.mp4", "A WOLF\nIN HER BED", "", 0, NNC, bs=140)),
    L("Now people put it over dogs dressed up as grandmas. Or anyone who's clearly an imposter.",
      CLIP("tr33-nn-b.mp4", "DOGS AS\nGRANDMAS", "", 7.0, NNC, bs=140)),
    ask("Who in your life is blatantly an imposter?", "WHO'S THE\nIMPOSTER?", "tr33-nn-a.mp4", NNC),
    subline("tr33-nn-c.mp4", NNC, 7.0),
   ], edition="MEME LORE")

# ---------------------------------------------------------------- 299 GD: Every End (wiki.gg)
EEC = "Clips: MindCap; TIAGC[GD] (YouTube)"
clip("gd33-ee-a.mp4", "https://www.youtube.com/watch?v=C7Umvy4VyDg", "*2:00-2:20", cut=0)
clip("gd33-ee-b.mp4", "https://www.youtube.com/watch?v=KexrBfBCZJA", "*7:40-8:00", cut=0)
clip("gd33-ee-c.mp4", "https://www.youtube.com/watch?v=8XtHnqwLakg", "*4:00-4:20", cut=0)
ep(299, "every-end-looks-like-2013", "This Level Looks Like 2013 But Its a Top 15 Demon", MIKE, "#ffc400", GDCAP,
   [L("This level looks like it's from 2013. It's one of the hardest levels in the game.",
      H("gd33-ee-a.mp4", "[TOP 15]\nEVERY END", 0, EEC)),
    L("Every End is only the cube, at normal speed. Old school 1.0 style.",
      H("gd33-ee-c.mp4", "[CUBE ONLY]\nNORMAL SPEED", 0, EEC)),
    L("But it has more objects than ORBIT. Because of the crazy background.",
      H("gd33-ee-a.mp4", "[MORE OBJECTS]\nTHAN ORBIT", 7.0, EEC)),
    L("Two verifiers dropped it. Then Hqmy took over and died at 79 percent.",
      H("gd33-ee-c.mp4", "[2 QUIT]\nHQMY - 79%", 7.0, EEC)),
    L("In March 2025, he verified it, after about 29,890 attempts.",
      HC("gd33-ee-b.mp4", 6.0, EEC, 29890, "EVERY END - VERIFIED")),
    ask("Old style or new style: which is harder?", "OLD OR\nNEW?", "gd33-ee-a.mp4", EEC),
    subline("gd33-ee-c.mp4", EEC, 4.0),
   ], pron=dict(GD_PRON, Hqmy="H Q M Y", MindCap="Mind Cap"), gd_player="Hqmy", **GDE)

# ---------------------------------------------------------------- 300 GD: The Bloop (wiki.gg)
BLC = "Clips: Zoink; Neiro (YouTube)"
clip("gd33-bl-a.mp4", "https://www.youtube.com/watch?v=Hio54AHPcbo", "*0:40-1:00", cut=0)
clip("gd33-bl-b.mp4", "https://www.youtube.com/watch?v=ROuXHSKEhHA", "*18:00-18:20", cut=0)
clip("gd33-bl-c.mp4", "https://www.youtube.com/watch?v=ROuXHSKEhHA", "*9:00-9:20", cut=0)
ep(300, "the-bloop-zoink-underrated", "Zoink Said This Level Was Top 75 Then It Went Top 10", LIAM, "#00b0ff", GDCAP,
   [L("Zoink said this level was maybe top 75. The Demonlist put it at number 10.",
      H("gd33-bl-a.mp4", "[TOP 75?]\nTHE BLOOP", 0, BLC)),
    L("It's The Bloop, built by murkkat and more than 20 creators.",
      H("gd33-bl-c.mp4", "[20+ CREATORS]\nMURKKAT", 0, BLC)),
    L("Zoink went from 28 percent to 71 in about a week. Then he buffed it.",
      H("gd33-bl-a.mp4", "[28% > 71%]\nIN A WEEK", 7.0, BLC)),
    L("83. 95. And on March 15th, 2026, he verified it.",
      H("gd33-bl-b.mp4", "[VERIFIED]\nMARCH 15, 2026", 0, BLC)),
    L("He guessed top 20 to 75. It was placed at number 10.",
      HC("gd33-bl-b.mp4", 7.0, BLC, 10, "DEMONLIST PLACEMENT", fmt="#{:,.0f}")),
    ask("Is Zoink just too good?", "TOO\nGOOD?", "gd33-bl-a.mp4", BLC),
    subline("gd33-bl-c.mp4", BLC, 4.0),
   ], pron=dict(GD_PRON, murkkat="murk cat"), gd_player="Zoink", **GDE)

# ---------------------------------------------------------------- 301 GD PLUG (posted BEFORE the 2:30 long video): Bloodbath -> Zodiac jump
ZDC = "Clips: Zoink (YouTube)"
clip("gd33-zd-a.mp4", "https://www.youtube.com/watch?v=v1Gj1iRg3cY", "*3:15-3:35", cut=0)
clip("gd33-zd-b.mp4", "https://www.youtube.com/watch?v=v1Gj1iRg3cY", "*1:00-1:20", cut=0)
clip("gd33-zd-c.mp4", "https://www.youtube.com/watch?v=Dsn3ce7HJ5I", "*2:00-2:20", cut=0)
ZPOP2 = dict(img="zoink-long-thumb.jpg", len="FULL STORY", d=0.35, y=1175)
ep(301, "zoink-zodiac-jump-plug", "Zoink Skipped Straight From Bloodbath to Zodiac", MIKE, "#2979ff", GDCAP,
   [L("His hardest level was Bloodbath. So he went straight for Zodiac. Almost nobody does that.",
      H("gd33-zd-a.mp4", "[BLOODBATH > ZODIAC]\nZOINK", 0, ZDC)),
    L("Zoink got 50 percent in June 2021. Then he kept grinding, month after month.",
      H("gd33-zd-b.mp4", "[50%]\nJUNE 2021", 0, ZDC)),
    L("On October 24th, 2021, he beat it. His first list demon was a former number one.",
      H("gd33-zd-a.mp4", "[100%]\nZODIAC", 6.0, ZDC)),
    L("Today he's the number one player in the world. And he just beat GRIEF.",
      H("gd33-zd-c.mp4", "[#1 PLAYER]\nGRIEF 100%", 0, ZDC)),
    L("The full Zoink story drops on my channel today at 2:30. Don't miss it.",
      H("gd33-zd-c.mp4", "[FULL STORY]\nTODAY 2:30 PM", 7.0, ZDC, popup=ZPOP2)),
    ask("Could you skip that many levels?", "COULD\nYOU?", "gd33-zd-a.mp4", ZDC),
    subline("gd33-zd-b.mp4", ZDC, 7.0),
   ], pron=dict(GD_PRON), gd_player="Zoink", **GDE)
RB[-1]["lines"][-2]["sc"]["popup"] = dict(ZPOP2, d=0.0)

# ---------------------------------------------------------------- ROBLOX driving (live Roblox numbers Nov 8) - driving/escape did best
def RCAP(hi):
    return {"font": MF + "Bangers-Regular.ttf", "size": 120, "mode": "word", "fill": "#ffffff", "hi": hi, "cy": 1470}

TRC = "Clips: Andy Plays; ProjectSupreme 2 (Roblox gameplay, YouTube)"
clip("rb33-tr-a.mp4", "https://www.youtube.com/watch?v=2aGKeyGzbL4", "*3:00-3:20", cut=0)
clip("rb33-tr-b.mp4", "https://www.youtube.com/watch?v=2aGKeyGzbL4", "*8:00-8:20", cut=0)
clip("rb33-tr-c.mp4", "https://www.youtube.com/watch?v=kdQVst-Xs0g", "*5:00-5:20", cut=0)
ep(303, "tesla-roadster-chase", "Steal the Roadster and Escape the Police on Roblox", FENRIR, "#ff1744", RCAP("#ff8a80"),
   [L("This new fun game on Roblox lets you steal a brand new Roadster, right off the showroom stage.",
      CLIP("rb33-tr-c.mp4", NEW, "STEAL IT OFF THE STAGE", 0, TRC, bs=110)),
    L("Then the police come for you.",
      CLIP("rb33-tr-b.mp4", "THE COPS\nARE COMING", "", 0, TRC, bs=150)),
    L("Weave through traffic on the highway, back roads and shortcuts, with cops on your tail.",
      CLIP("rb33-tr-c.mp4", "LOSE\nTHE COPS", "HIGHWAY - BACK ROADS - SHORTCUTS", 6.0, TRC, bs=150)),
    L("It came out on October 21st, and it already has over 19 million visits.",
      CCOUNT("rb33-tr-b.mp4", 7.0, TRC, 19608009, "VISITS", bs=130)),
    ask("Could you escape the cops?", "COULD YOU\nESCAPE?", "rb33-tr-c.mp4", TRC),
   ])

NRC = "Clips: ProjectSupreme 2; On1yMar (Roblox gameplay, YouTube)"
clip("rb33-nr-a.mp4", "https://www.youtube.com/watch?v=DWKpFUvmoec", "*3:00-3:20", cut=0)
clip("rb33-nr-b.mp4", "https://www.youtube.com/watch?v=DWKpFUvmoec", "*9:00-9:20", cut=0)
clip("rb33-nr-c.mp4", "https://www.youtube.com/watch?v=-daE8mzjNr0", "*2:00-2:20", cut=0)
ep(304, "night-rider", "Night Rider on Roblox Is an Endless Highway at Crazy Speed", MIKE, "#7c4dff", RCAP("#b388ff"),
   [L("This new fun game on Roblox puts you on a motorcycle, on a highway that never ends.",
      CLIP("rb33-nr-b.mp4", NEW, "THE HIGHWAY NEVER ENDS", 0, NRC, bs=110)),
    L("Swerve through traffic at crazy speeds, past the city, farms and suburbs.",
      CLIP("rb33-nr-c.mp4", "CRAZY\nSPEEDS", "", 0, NRC, bs=150)),
    L("Pop wheelies and do tricks. But watch out for the death wobble.",
      CLIP("rb33-nr-b.mp4", "DEATH\nWOBBLE", "", 6.0, NRC, bs=150)),
    L("It's still in testing, and it already has over 20 million visits.",
      CCOUNT("rb33-nr-a.mp4", 7.0, NRC, 20032070, "VISITS", bs=130)),
    ask("How far could you ride?", "HOW FAR?", "rb33-nr-b.mp4", NRC),
   ])

DTC = "Clips: ThunderClouds; KewlSqwad (Roblox gameplay, YouTube)"
clip("rb33-dt-a.mp4", "https://www.youtube.com/watch?v=3nzhPwk8pxc", "*2:00-2:20", cut=0)
clip("rb33-dt-b.mp4", "https://www.youtube.com/watch?v=3nzhPwk8pxc", "*6:00-6:20", cut=0)
clip("rb33-dt-c.mp4", "https://www.youtube.com/watch?v=IEwriGXf44o", "*2:00-2:20", cut=0)
ep(305, "can-you-pass-a-driving-test", "Can You Pass a Driving Test on Roblox", HEART, "#00e676", RCAP("#b9f6ca"),
   [L("This new fun game on Roblox makes you pass a real driving test. Most players fail.",
      CLIP("rb33-dt-a.mp4", NEW, "MOST PLAYERS FAIL", 0, DTC, bs=110)),
    L("A big town, with real traffic and real road rules.",
      CLIP("rb33-dt-b.mp4", "REAL\nROAD RULES", "", 0, DTC, bs=150)),
    L("Pass the test, get your license, then deliver pizzas and give lifts to earn cash.",
      CLIP("rb33-dt-c.mp4", "GET YOUR\nLICENSE", "THEN EARN CASH", 0, DTC, bs=150)),
    L("Work your way up to the hypercar on the roof. It already has over 10 million visits.",
      CCOUNT("rb33-dt-a.mp4", 7.0, DTC, 10848865, "VISITS", bs=130)),
    ask("Would you pass on your first try?", "FIRST\nTRY?", "rb33-dt-b.mp4", DTC),
   ])

# ================================================================== write
paths = []
for e in RB:
    e = dict(preset="roblox", hdr="tag", **e)
    words = sum(len(l.get("say", l["t"]).split()) for l in e["lines"])
    p = os.path.join("episodes", "roblox", e["slug"] + ".json")
    json.dump(e, open(os.path.join(ROOT, p), "w"), indent=1, ensure_ascii=False)
    paths.append(p)
    print(e["slug"], len(e["lines"]), "lines", words, "words")
manifest = {"batch": 33, "note": "AI game merging, clapping cat, Rumpelstiltskin, not me nan, Every End, The Bloop, Zoink plug, Roadster Chase, Night Rider, Driving Test",
            "posting": "Z:/claudeprojects/roblox vids/batch-33/posting.txt", "episodes": paths, "clips": CLIPS}
json.dump(manifest, open(os.path.join(ROOT, "batches", "batch-33.json"), "w"), indent=1)
print(len(CLIPS), "clips")
