"""Writes batch 15 (facts checked 2026-10-18): 8 Roblox + 1 Geometry Dash + 1 Fortnite (8-Bit Backstory #123-132).
New this batch: every hook is real gameplay / official game art (full-screen, Ken Burns), the Grief video uses Doggie's
real verification clip, every scene has camera motion (engine), and every video ends with a 'watch next' teaser +
subscribe/like + the comment CTA. Openings name the game or a hook, never a year."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CTA = " Like and subscribe, and comment for which game we should review next!"
CTA_SUB = "COMMENT FOR WHICH GAME\nWE SHOULD REVIEW NEXT!"
MF = "../modern/fonts/"
MIKE, SARAH = "am_michael", "af_sarah"
RB = []


def L(t, sc, say=None):
    d = {"t": t, "sc": sc}
    if say:
        d["say"] = say
    return d


def S(big=None, sub=None, bg="day", ground="grass", **k):
    d = dict(bg=bg, ground=ground)
    if big:
        d["big"] = big
    if sub:
        d["sub"] = sub
    d.update(k)
    return d


def F(big, sub, img=None, credit=None, clip=None, start=0, **k):
    """Full-screen real image / clip scene with the title over it."""
    fu = {"credit": credit}
    if clip:
        fu.update(clip=clip, start=start)
    else:
        fu["img"] = img
    for key in ("w", "cy", "mode", "crop", "h"):
        if key in k:
            fu[key] = k.pop(key)
    k.setdefault("by", 300)
    k.setdefault("bs", 120)
    k.setdefault("ss", 50)
    return S(big, sub, "night", "dark", full=fu, **k)


def RBX(game):
    return f"Image: {game} on Roblox"


def tease(text, big, img, credit, **k):
    return L(text + " Subscribe so you don't miss it.", F(big, "SUBSCRIBE SO YOU DON'T MISS IT", img, credit, bs=104, ss=40, **k))


def end(q, big, bg="party", ground="purple", **k):
    av_ = [{"p": [-1.8, 0.6], "a": "cheer", "c": "a"}, {"p": [0, 1.2], "a": "wave", "c": "g"}, {"p": [1.8, 0.6], "a": "cheer", "c": "b"}]
    ic = [{"n": "heart", "x": 170, "y": 700, "s": 130, "a": "pulse"}, {"n": "bolt", "x": 910, "y": 700, "s": 130, "a": "pulse"}]
    return L(q + CTA, S(big, CTA_SUB, bg, ground, rays="#ffffff", ss=50, sgap=62, fx=["confetti"], av=av_, ic=ic, **k))


def av(p, a="bob", c="a", **k):
    d = {"p": p, "a": a, "c": c}
    d.update(k)
    return d


def ep(num, slug, name, target, accent, voice, speed, cap, lines, pron=None, **k):
    RB.append(dict(num=num, slug=f"{num}-{slug}", file=f"{num} {name}.mp4", target=target, accent=accent,
                   voice=voice, speed=speed, cap=cap, pron=pron or {}, lines=lines, **k))


BR_PRON = {"brainrot": "brain rot", "Brainrot": "Brain rot", "brainrots": "brain rots", "Brainrots": "Brain rots",
           "Sahur": "Sa-hoor", "Obby": "Obbie"}

# 123 DOORS The Mines ending (70 s)
ep(123, "doors-the-mines-ending", "DOORS The Mines Ending", 70, "#ffb300", SARAH, 1.04,
   {"font": MF + "CrimsonText-Bold.ttf", "size": 100, "upper": False, "fill": "#fff8e1", "hi": "#ffca28", "stroke": 6},
   [L("The Mines in DOORS ends with Seek doing something nobody saw coming.",
      F("SEEK DID\nWHAT?!", "THE MINES ENDING", "pop15-doors-seek.jpg", RBX("DOORS"), bs=124)),
    L("The Mines is Floor 2. One hundred rooms, from Door 100 all the way down to Door 200, and you go down there because of Figure.",
      F("FLOOR 2", "DOORS 100 TO 200", "pop15-doors-lobby.jpg", RBX("DOORS"), bs=170)),
    L("Down there, Gloombats keep hurting you, so watch out for their Moth Eggs. And Giggle drops onto your face for up to 40 damage.",
      S("GLOOMBATS +\nGIGGLE", "UP TO 40 DAMAGE", "dark", "stone", bs=120, vig=True, fx=["red"], ic=[{"n": "moon", "x": 860, "y": 820, "s": 140, "a": "float"}])),
    L("From Door 150, Grumbles guard The Nest. Distract them with a Glowstick or a Bulklight, or they can kill you instantly.",
      S("GRUMBLES", "DOOR 150: THE NEST", "night", "stone", bs=170, vig=True,
        photo=dict(img="pop15-doors-lineup.jpg", label="REAL DOORS SCREENSHOT", credit=RBX("DOORS"), y=880, h=420), instant=True)),
    L("Seek chases you from Door 140, first on foot, then in a minecart over a giant ravine. And later, again, through the Sewage Pipes.",
      F("MINECART\nCHASE", "DOORS 140 TO 149", "pop15-doors-alarm.jpg", RBX("DOORS"), bs=124)),
    L("At Door 200 is The Dam, a boss fight against Seek as a giant blob of eyes.",
      S("DOOR 200", "THE DAM BOSS FIGHT", "red", "dark", bc="#ffffff", bs=180, fx=["red"], ic=[{"n": "eye", "x": 540, "y": 800, "s": 220, "a": "pulse"}])),
    L("Beat it, and you climb a ladder, through a sewer grate, and out into The Woods.",
      S("THE WOODS", "OUT OF THE SEWERS", "night", "grass", bs=170, fx=["fireflies"], props=[["tree", -1.8, -1.8], ["tree", 1.8, -2.0]], av=[av([0.0, 0.8], "sneak", "a")])),
    L("At a castle, Seek infects Queen Grumble, and Seek's humanoid form crawls out.",
      F("SEEK'S REAL\nFORM", "AT THE CASTLE", "pop15-doors-lineup.jpg", RBX("DOORS"), bs=124, mode="cover")),
    L("Then the screen says To Be Continued, and you unlock an achievement called See You Soon.",
      S("TO BE\nCONTINUED", "ACHIEVEMENT: SEE YOU SOON", "dark", "dark", bs=150, ss=44, vig=True, fx=["sparkle"])),
    L("Oh, and it pays 50 knobs, and the rarest room is a giant ladder room full of gold.",
      S("50 KNOBS", "+ THE RAREST ROOM", "gold", "stone", rays="#ffffff", bs=170, fx=["coins"])),
    tease("Next up: the biggest brainrot games on Roblox, ranked.", "NEXT: BRAINROT\nGAMES RANKED", "pop15-sab-chicken.jpg", RBX("Steal a Brainrot")),
    end("Did the ending scare you?", "DID IT\nSCARE YOU?", bg="dark", ground="dark"),
   ], mood="spooky")

# 124 Biggest brainrot games ranked (70 s)
ep(124, "biggest-brainrot-games-ranked", "The Biggest Brainrot Games on ROBLOX", 72, "#ff4081", MIKE, 1.12,
   {"font": MF + "Bangers-Regular.ttf", "size": 124, "mode": "word", "fill": "#ffffff", "hi": "#ffffff", "cy": 1470},
   [L("These are the five biggest brainrot games on Roblox, ranked by the most people playing at once.",
      F("TOP 5\nBRAINROT GAMES", "RANKED BY PEAK PLAYERS", "pop15-sab-chicken.jpg", RBX("Steal a Brainrot"), bs=112)),
    L("Number 5: Swing Obby for Brainrots. You swing across ropes and grab brainrots. It peaked around 256,000 players in March 2026.",
      F("#5 SWING OBBY", "256,000 PLAYERS", "pop15-swing.jpg", RBX("Swing Obby for Brainrots"), bs=110)),
    L("Number 4: Kick a Lucky Block, by No More Flops. Kick a block to roll brainrots, train your legs, and survive a tsunami. 1.7 million at once, in May 2026.",
      F("#4 KICK A\nLUCKY BLOCK", "1.7 MILLION PLAYERS", "pop15-kick-3.jpg", RBX("Kick a Lucky Block"), bs=110)),
    L("Number 3: Escape Tsunami for Brainrots. Outrun a giant wave while you collect brainrots. It hit 4.1 million in February 2026.",
      F("#3 ESCAPE\nTSUNAMI", "4.1 MILLION PLAYERS", "pop15-tsunami.jpg", RBX("Escape Tsunami for Brainrots"), bs=110)),
    L("Number 2: Plants and Brainrots. Your plants fight brainrots for you. 8.7 million at once, in October 2025.",
      F("#2 PLANTS &\nBRAINROTS", "8.7 MILLION PLAYERS", "pop15-plants.jpg", RBX("Plants & Brainrots"), bs=110)),
    L("And number 1: Steal a Brainrot. Over 25 million people playing at once, in October 2025.",
      F("#1 STEAL A\nBRAINROT", "25 MILLION AT ONCE", "pop15-sab-dragon.jpg", RBX("Steal a Brainrot"), bs=110)),
    L("That's about three times number 2, and almost a hundred times number 5.",
      S("100X", "NUMBER 1 VS NUMBER 5", "gold", "grass", rays="#ffffff", bs=220, fx=["confetti"], ic=[{"n": "crown", "x": 860, "y": 820, "s": 150, "a": "float"}])),
    L("It also has nearly 70 billion visits, the second most visited Roblox game ever.",
      {"count": {"from": 0, "to": 69.8, "fmt": "{:.1f}B", "dur": 1.6}, "sub": "VISITS", "bg": "party", "ground": "purple", "bs": 200, "fx": ["coins"]}),
    tease("Next: the game that took Steal a Brainrot's crown.", "NEXT: IT GOT\nDETHRONED", "pop15-egg-trex.jpg", RBX("Steal An Egg")),
    end("Which one's your favorite?", "YOUR\nFAVORITE?", bg="party", ground="purple"),
   ], pron=BR_PRON)

# 125 Roblox lost 29 million daily players
ep(125, "roblox-lost-29-million-players", "ROBLOX Lost 29 Million Daily Players", 38, "#ef5350", MIKE, 1.08,
   {"font": MF + "RussoOne-Regular.ttf", "size": 84, "hi": "#ff8a80", "stroke": 8},
   [L("Roblox has lost 29 million daily players in under a year.",
      F("29 MILLION\nGONE", "ROBLOX DAILY PLAYERS", "pop15-brookhaven.jpg", RBX("Brookhaven RP"), bs=124)),
    L("In the summer of 2025, a record 152 million people played Roblox every day.",
      {"count": {"from": 0, "to": 152, "fmt": "{:.0f}M", "dur": 1.4}, "sub": "PLAYED EVERY DAY", "bg": "gold", "ground": "grass", "bs": 220, "rays": "#ffffff"}),
    L("Then it dropped three times in a row, down to 123 million by mid 2026.",
      S("123M", "THREE DROPS IN A ROW", "night", "stone", bs=220, fx=["red"], ic=[{"n": "bar", "x": 860, "y": 820, "s": 140, "a": "shake"}])),
    L("Hours played fell from about 40 billion to 29 billion a quarter, and revenue came in under what Wall Street expected.",
      S("40B → 29B", "HOURS PLAYED", "dark", "stone", bs=150, vig=True, ic=[{"n": "clock", "x": 860, "y": 820, "s": 140, "a": "spin"}])),
    tease("Next up: Roblox's most visited games ever.", "NEXT: MOST\nVISITED EVER", "pop15-bloxfruits.jpg", RBX("Blox Fruits")),
    end("Is Roblox dying, or just cooling off?", "DYING OR\nCOOLING OFF?", bg="red", ground="stone"),
   ])

# 126 Tung Tung Tung Sahur kicked out
ep(126, "tung-tung-tung-sahur-kicked-out", "Tung Tung Tung Sahur Got Kicked Out", 36, "#ffb74d", SARAH, 1.04,
   {"font": MF + "TitanOne-Regular.ttf", "size": 80, "stroke": 0, "fill": "#3e2723", "hi": "#e65100", "box": "#fff3e0", "radius": 30},
   [L("Tung Tung Tung Sahur got kicked out of Steal a Brainrot.",
      F("TUNG TUNG\nKICKED OUT", "OF STEAL A BRAINROT", "pop15-sab-bumbatron.jpg", RBX("Steal a Brainrot"), bs=124)),
    L("He comes from Indonesia, where people drum before dawn during Ramadan to wake everyone up for the meal called sahur.",
      S("FROM\nINDONESIA", "SAHUR = PRE-DAWN MEAL", "sunset", "grass", bs=150, ic=[{"n": "moon", "x": 860, "y": 800, "s": 150, "a": "float"}])),
    L("In September 2025 he was pulled from the game over licensing, and two companies are still fighting over the copyright.",
      S("PULLED", "SEPTEMBER 2025: LICENSING", "dark", "stone", bs=200, vig=True, ic=[{"n": "license", "x": 860, "y": 820, "s": 150, "a": "shake"}])),
    L("Then on November 29th, 2025, he came back.",
      F("HE'S BACK", "NOVEMBER 29, 2025", "pop15-sab-chicken.jpg", RBX("Steal a Brainrot"), bs=160)),
    L("And in April 2026, he even became a Fortnite skin.",
      S("IN FORTNITE", "APRIL 2026", "gold", "grass", rays="#ffffff", bs=160, fx=["confetti"], av=[av([0.0, 0.8], "jump", "g", hold="sword")])),
    tease("Next: the biggest brainrot games on Roblox, ranked.", "NEXT: BRAINROT\nGAMES RANKED", "pop15-plants.jpg", RBX("Plants & Brainrots")),
    end("Is he the best brainrot?", "THE BEST\nBRAINROT?", bg="day", ground="grass"),
   ], pron=BR_PRON)

# 127 Steal An Egg dethroned Steal a Brainrot
ep(127, "steal-an-egg-dethroned-brainrot", "Steal a Brainrot Got Dethroned", 35, "#ffca28", SARAH, 1.04,
   {"font": MF + "Chewy-Regular.ttf", "size": 104, "upper": False, "fill": "#ffffff", "hi": "#ffd54f", "stroke": 8},
   [L("Steal a Brainrot just lost its crown, to a game about stealing eggs.",
      F("DETHRONED\nBY AN EGG", "STEAL AN EGG", "pop15-egg-snake.jpg", RBX("Steal An Egg"), bs=124)),
    L("From July to September 2026, Steal An Egg was the most visited game on Roblox, with 6 billion visits.",
      F("6 BILLION", "VISITS IN 3 MONTHS", "pop15-egg-trex.jpg", RBX("Steal An Egg"), bs=170)),
    L("It peaked at 14.2 million players at the same time.",
      {"count": {"from": 0, "to": 14.2, "fmt": "{:.1f}M", "dur": 1.3}, "sub": "PLAYING AT ONCE", "bg": "mint", "ground": "grass", "bs": 220, "fx": ["sparkle"]}),
    L("Murder Mystery 2 and Plus One Speed Keyboard Escape had about 4 billion each, and Steal a Brainrot fell to fifth, with 3 billion.",
      F("FELL TO #5", "STEAL A BRAINROT: 3B", "pop15-sab-dragon.jpg", RBX("Steal a Brainrot"), bs=150)),
    tease("Next: why Roblox lost 29 million daily players.", "NEXT: 29 MILLION\nPLAYERS GONE", "pop15-adoptme.jpg", RBX("Adopt Me!")),
    end("Egg or brainrot?", "EGG OR\nBRAINROT?", bg="day", ground="grass"),
   ], pron=BR_PRON)

# 128 Sell Lemons is not banned
ep(128, "sell-lemons-not-banned", "Sell Lemons Isn't Banned", 36, "#ffee58", SARAH, 1.04,
   {"font": MF + "Baloo2[wght].ttf", "size": 96, "fill": "#ffffff", "hi": "#fff176", "stroke": 8},
   [L("Sell Lemons didn't get banned, and it isn't 16 plus.",
      F("NOT BANNED", "SELL LEMONS", "pop15-lemons-logo.jpg", RBX("Sell Lemons"), bs=150)),
    L("A rumor said this Roblox game was now 16 plus, but its official rating is still Minimal.",
      S("RATED\nMINIMAL", "NOT 16+", "mint", "grass", bs=150, ic=[{"n": "shield", "x": 860, "y": 820, "s": 150, "a": "pulse"}])),
    L("You sell lemonade, upgrade your stand, and keep earning even while you're offline. It's by BloxByte Games, and came out in March 2025.",
      F("OFFLINE\nINCOME", "BLOXBYTE GAMES", "pop15-lemons-stand.jpg", RBX("Sell Lemons"), bs=124)),
    L("It peaked at about 229,000 players this July, and has over 481 million visits.",
      {"count": {"from": 0, "to": 481, "fmt": "{:.0f}M", "dur": 1.3}, "sub": "VISITS", "bg": "gold", "ground": "grass", "bs": 220, "fx": ["coins"]}),
    tease("Next: 1.7 million people kicking a block.", "NEXT: KICK A\nLUCKY BLOCK", "pop15-kick-1pct.jpg", RBX("Kick a Lucky Block")),
    end("Best lemon upgrade?", "BEST\nUPGRADE?", bg="gold", ground="grass"),
   ])

# 129 Kick a Lucky Block
ep(129, "kick-a-lucky-block", "1.7 Million Kicking a Block", 37, "#7c4dff", MIKE, 1.06,
   {"font": MF + "Anton-Regular.ttf", "size": 104, "hi": "#b388ff", "stroke": 8},
   [L("1.7 million people played a Roblox game about kicking a block.",
      F("1.7 MILLION\nKICKING A BLOCK", "KICK A LUCKY BLOCK", "pop15-kick-1pct.jpg", RBX("Kick a Lucky Block"), bs=108)),
    L("You kick a lucky block to roll brainrots, train your legs with weights, and try to survive a tsunami.",
      F("KICK TO\nROLL", "BRAINROTS + TSUNAMI", "pop15-kick-3.jpg", RBX("Kick a Lucky Block"), bs=140)),
    L("It's by No More Flops, came out in April 2026, and hit 1.7 million at once just a month later.",
      S("1 MONTH", "APRIL TO MAY 2026", "party", "purple", rays="#ffffff", bs=200, ic=[{"n": "rocket", "x": 860, "y": 820, "s": 150, "a": "float"}])),
    L("Trackers count 1.9 billion visits, and 26.7 million favorites.",
      {"count": {"from": 0, "to": 26.7, "fmt": "{:.1f}M", "dur": 1.3}, "sub": "FAVORITES", "bg": "night", "ground": "stone", "bs": 220, "fx": ["sparkle"]}),
    tease("Next: Roblox's most visited games of all time.", "NEXT: MOST\nVISITED EVER", "pop15-brookhaven.jpg", RBX("Brookhaven RP")),
    end("How far can you kick?", "HOW FAR\nCAN YOU KICK?", bg="party", ground="purple"),
   ], pron=BR_PRON)

# 130 Most visited Roblox games ever
ep(130, "most-visited-roblox-games", "ROBLOX's Most Visited Games Ever", 34, "#29b6f6", SARAH, 1.06,
   {"font": MF + "Rajdhani-Bold.ttf", "size": 104, "fill": "#ffffff", "hi": "#81d4fa", "stroke": 8},
   [L("These are the most visited Roblox games of all time.",
      F("MOST VISITED\nEVER", "TOP 5 ON ROBLOX", "pop15-brookhaven.jpg", RBX("Brookhaven RP"), bs=124)),
    L("Number 5: 99 Nights in the Forest, with 27 billion visits.",
      S("#5 99 NIGHTS", "27 BILLION", "night", "grass", bs=130, fx=["fireflies"], props=[["tree", -1.8, -1.8], ["tree", 1.8, -2.0]])),
    L("Number 4: Adopt Me, with 43.8 billion.",
      F("#4 ADOPT ME", "43.8 BILLION", "pop15-adoptme.jpg", RBX("Adopt Me!"), bs=130)),
    L("Number 3: Blox Fruits, with 62 billion.",
      F("#3 BLOX FRUITS", "62 BILLION", "pop15-bloxfruits.jpg", RBX("Blox Fruits"), bs=130)),
    L("Number 2: Steal a Brainrot, with nearly 70 billion, in only about a year.",
      F("#2 STEAL A\nBRAINROT", "69.8 BILLION", "pop15-sab-chicken.jpg", RBX("Steal a Brainrot"), bs=120)),
    L("And number 1: Brookhaven, with 83.4 billion visits.",
      F("#1 BROOKHAVEN", "83.4 BILLION", "pop15-brookhaven.jpg", RBX("Brookhaven RP"), bs=124, mode="cover")),
    tease("Next: the hardest Geometry Dash level ever beaten.", "NEXT: THE\nHARDEST LEVEL", "pop15-gd-66.jpg", "Clip: Doggie, GRIEF verification"),
    end("Which one have you played most?", "PLAYED\nTHE MOST?", bg="day", ground="grass"),
   ], pron=BR_PRON)

# 131 Geometry Dash: Doggie verifies Grief (70 s, real clip)
GD = "gd-grief-doggie.mp4"
GDC = "Clip: Doggie, GRIEF verification"
ep(131, "doggie-verifies-grief", "The Hardest Level in Geometry Dash", 72, "#e53935", MIKE, 1.1,
   {"font": MF + "BlackOpsOne-Regular.ttf", "size": 92, "fill": "#ffffff", "hi": "#ff5252", "stroke": 8},
   [L("This is the moment the hardest level in Geometry Dash got beaten, for the very first time.",
      F("THE HARDEST\nLEVEL EVER", "GRIEF, VERIFIED", clip=GD, start=13.5, credit=GDC, bs=124)),
    L("It's called Grief, and it's number 1 on the Demonlist, the ranking of the hardest levels in the game.",
      F("#1", "ON THE DEMONLIST", "pop15-gd-demonlist.jpg", "Image: Pointercrate Demonlist", bs=200, w=760, cy=1040, h=820)),
    L("Grief was built by GrenadeofTacos and others, published by icedcave, and it's the prequel to another famous level, Slaughterhouse.",
      F("A PREQUEL", "TO SLAUGHTERHOUSE", "pop15-gd-20.jpg", GDC, bs=150)),
    L("The player who beat it is Doggie. He started verifying it on May 1st, 2024.",
      F("DOGGIE", "STARTED MAY 1, 2024", "pop15-gd-47.jpg", GDC, bs=180)),
    L("It took him 436,879 attempts, over 396 streams, and about two years and five months.",
      {"count": {"from": 0, "to": 436879, "fmt": "{:,.0f}", "dur": 1.8}, "sub": "ATTEMPTS", "bg": "red", "ground": "dark", "bc": "#ffffff", "bs": 170, "fx": ["red"], "vig": True}),
    L("He reached 80 percent in November 2025, 84 percent in May 2026, then kept dying at 97 percent, again and again.",
      F("STUCK\nAT 97%", "AGAIN AND AGAIN", "pop15-gd-66.jpg", GDC, bs=150)),
    L("Then, on October 5th, 2026, he finally made it through.",
      F("OCTOBER 5,\n2026", "THE FINAL RUN", clip=GD, start=0, credit=GDC, bs=130)),
    L("100 percent. Level verified.",
      F("LEVEL\nVERIFIED!", "100%", clip=GD, start=17.5, credit=GDC, bs=150)),
    L("His old record was 121,749 attempts, on Acheron. Grief took more than three times that.",
      F("3X HIS OLD\nRECORD", "ACHERON: 121,749", clip=GD, start=23, credit=GDC, bs=124)),
    L("And so far, nobody else has beaten it.",
      F("NOBODY ELSE\nYET", "0 OTHER RECORDS", "pop15-gd-demonlist.jpg", "Image: Pointercrate Demonlist", bs=124, w=760, cy=1040, h=820)),
    tease("Next: Fortnite's Battle Royale was built in about two months.", "NEXT: BUILT IN\n2 MONTHS", "pop15-fn-br.jpg", "Image: Epic Games"),
    end("Could you beat Grief?", "COULD YOU\nBEAT IT?", bg="red", ground="dark"),
   ], pron={"GrenadeofTacos": "Grenade of Tacos", "icedcave": "iced cave", "Acheron": "Ack-er-on", "Demonlist": "Demon list"},
   edition="GEOMETRY DASH", mood="spooky")

# 132 Fortnite built in two months
ep(132, "fortnite-built-in-two-months", "Fortnite Was Built in 2 Months", 57, "#7e57c2", MIKE, 1.08,
   {"font": MF + "BarlowCondensed-ExtraBold.ttf", "size": 110, "fill": "#ffffff", "hi": "#b39ddb", "stroke": 8},
   [L("Fortnite's Battle Royale was built in about two months.",
      F("BUILT IN\n2 MONTHS", "FORTNITE BATTLE ROYALE", "pop15-fn-br.jpg", "Image: Epic Games", bs=130)),
    L("Fortnite grew out of an Epic Games game jam around 2011, and Save the World came out in early access in July 2017.",
      S("SAVE THE\nWORLD", "EARLY ACCESS, JULY 2017", "night", "stone", bs=150,
        photo=dict(img="pop15-fn-freddy.jpg", label="REAL FORTNITE SCREENSHOT", credit="Image: Epic Games", y=880, h=420), instant=True)),
    L("Then Epic made Battle Royale in about two months, and released it free in September 2017.",
      S("FREE", "SEPTEMBER 2017", "sunset", "grass", bs=220, rays="#ffffff", ic=[{"n": "rocket", "x": 860, "y": 820, "s": 150, "a": "float"}])),
    L("It hit 10 million players in two weeks, and 125 million by June 2018.",
      {"count": {"from": 0, "to": 125, "fmt": "{:.0f}M", "dur": 1.5}, "sub": "PLAYERS BY JUNE 2018", "bg": "party", "ground": "purple", "bs": 220, "fx": ["confetti"]}),
    L("It made 2.4 billion dollars in 2018 alone.",
      S("$2.4\nBILLION", "IN 2018 ALONE", "gold", "grass", rays="#ffffff", bs=170, fx=["coins"])),
    L("Then came Creative mode, a 30 million dollar World Cup in 2019, and a Travis Scott concert with 12.3 million players at once.",
      F("12.3 MILLION", "AT ONE CONCERT", "pop15-fn-festival.jpg", "Image: Epic Games", bs=140)),
    L("LEGO Fortnite arrived in December 2023, and in April 2026, Save the World finally became free.",
      F("LEGO +\nFREE STW", "2023 + 2026", "pop15-fn-lego.jpg", "Image: Epic Games", bs=140)),
    tease("Next: how DOORS The Mines really ends.", "NEXT: THE\nMINES ENDING", "pop15-doors-seek.jpg", RBX("DOORS")),
    end("Do you still play Fortnite?", "STILL\nPLAYING?", bg="party", ground="purple"),
   ], edition="FORTNITE")

# ================================================================== write
for e in RB:
    e = dict(preset="roblox", hdr="tag", **e)
    for l in e["lines"]:
        sc = l["sc"]
        for m in [sc.get("photo"), sc.get("full")]:
            if m:
                f = m.get("img") or m.get("clip")
                if not os.path.exists(os.path.join(ROOT, "episodes", "assets", f)):
                    print("  MISSING", e["slug"], f)
    json.dump(e, open(os.path.join(ROOT, "episodes", "roblox", e["slug"] + ".json"), "w"), indent=1, ensure_ascii=False)
    print(e["slug"], len(e["lines"]), "lines", sum(len(l.get("say", l["t"]).split()) for l in e["lines"]), "words", "target", e["target"])
