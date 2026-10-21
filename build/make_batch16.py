"""Writes batch 16 (facts checked 2026-10-21): 4 Roblox + 4 Geometry Dash (real clips) + 2 meme lore (8-Bit Backstory #133-142).
GD and meme videos use real clips the user downloaded (episodes/assets/gd16-*, ml16-*); voices rotate every few videos."""

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


HEART, FENRIR, LIAM, PUCK = "af_heart", "am_fenrir", "am_liam", "am_puck"
BR_PRON = {"brainrot": "brain rot", "Brainrot": "Brain rot", "brainrots": "brain rots", "Brainrots": "Brain rots"}
GD_PRON = {"Acheron": "Ack-er-on", "Demonlist": "Demon list", "Zoink": "Zoynk", "ryamu": "rye-ah-moo", "Wolvez": "Wolves",
           "paqoe": "pa-co", "clubstep": "club step", "CairoX": "Cairo X", "DrCuber": "Doctor Cuber", "wPopoff": "W Popoff"}
ASSET = os.path.join(ROOT, "episodes", "assets")


def CLIP(name, big, sub, start, credit, fb_img=None, fb_credit=None, **k):
    """Real clip scene; until the clip exists, fall back to a still so the batch still renders."""
    if os.path.exists(os.path.join(ASSET, name)):
        return F(big, sub, clip=name, start=start, credit=credit, **k)
    if fb_img:
        return F(big, sub, fb_img, fb_credit or credit, **k)
    return S(big, sub, "night", "stone", vig=True, fx=["sparkle"], ic=[{"n": "star", "x": 860, "y": 820, "s": 150, "a": "spin"}],
             **{kk: v for kk, v in k.items() if kk in ("bs", "ss")})


# ============================================================ ROBLOX (posted first)
# 133 The OOF sound
ep(133, "roblox-oof-sound", "Why ROBLOX Deleted the OOF Sound", 56, "#ff7043", SARAH, 1.04,
   {"font": MF + "Bangers-Regular.ttf", "size": 120, "mode": "word", "fill": "#ffffff", "hi": "#ffffff", "cy": 1470},
   [L("Roblox deleted its famous oof sound, and then it came back.",
      F("THE OOF WAS\nDELETED", "...THEN IT CAME BACK", "pop16-crossroads.jpg", RBX("Classic: Crossroads"), bs=120)),
    L("The oof wasn't even made for Roblox. It came from a 2000 game called Messiah.",
      S("NOT MADE\nFOR ROBLOX", "FROM A 2000 GAME", "night", "stone", bs=140, vig=True,
        ic=[{"n": "question", "x": 860, "y": 800, "s": 150, "a": "spin"}], av=[av([0.0, 0.8], "run", "a")])),
    L("Roblox used it as the death sound from 2006, so every fall and every reset said oof.",
      S("OOF!", "THE DEATH SOUND SINCE 2006", "day", "grass", bs=240, fx=["confetti"],
        av=[av([-1.4, 0.6], "jump", "a"), av([0.4, 1.0], "run", "b"), av([1.8, 0.4], "cheer", "g")])),
    L("In 2019, composer Tommy Tallarico said he owned it.",
      S("\"I OWN IT\"", "2019 COPYRIGHT CLAIM", "red", "dark", bc="#ffffff", bs=150, fx=["red"], ic=[{"n": "license", "x": 860, "y": 820, "s": 150, "a": "shake"}])),
    L("A deal in 2020 turned oof into a paid sound, for 100 Robux.",
      {"count": {"from": 0, "to": 100, "fmt": "{:.0f} ROBUX", "dur": 1.2}, "sub": "TO USE THE OOF", "bg": "gold", "ground": "grass", "bs": 170, "fx": ["coins"]}),
    L("Then in July 2022, Roblox removed it over a licensing issue. The new sound got called a guttural grunt.",
      S("REMOVED", "JULY 2022", "dark", "dark", bs=220, vig=True, ic=[{"n": "alarm", "x": 860, "y": 820, "s": 150, "a": "shake"}],
        av=[av([0.0, 0.8], "bob", "b")])),
    L("But in July 2025, Roblox brought the original back for developers. Their post said: a comeback so good it hurts.",
      F("IT'S BACK!", "JULY 2025", "pop16-crossroads.jpg", RBX("Classic: Crossroads"), bs=170, mode="cover")),
    tease("Next: the Roblox game that's 12 years old and still number 2.", "NEXT: 12 YEARS\nAND STILL #2", "pop16-mm2-heroes.jpg", RBX("Murder Mystery 2")),
    end("Old oof or new oof?", "OLD OOF OR\nNEW OOF?", bg="party", ground="purple"),
   ], pron={"Tallarico": "Tal-a-ree-co", "Robux": "Robucks"})

# 134 Murder Mystery 2
ep(134, "murder-mystery-2-still-number-2", "Murder Mystery 2 Is 12 Years Old", 48, "#e53935", MIKE, 1.06,
   {"font": MF + "BlackOpsOne-Regular.ttf", "size": 92, "fill": "#ffffff", "hi": "#ff5252", "stroke": 8},
   [L("Murder Mystery 2 is twelve years old, and it's the second most played game on Roblox right now.",
      F("12 YEARS OLD\nSTILL #2", "MURDER MYSTERY 2", "pop16-mm2-halloween.jpg", RBX("Murder Mystery 2"), bs=116)),
    L("Every round, one player is the murderer, one is the sheriff, and everyone else is innocent.",
      S("MURDERER\nSHERIFF\nINNOCENT", "EVERY ROUND", "night", "stone", bs=110, vig=True,
        av=[av([-1.8, 0.6], "walk", "b", hold="knife"), av([0, 1.1], "bob", "a", hold="gun"), av([1.8, 0.6], "run", "g")])),
    L("If the sheriff dies, the gun drops, and any innocent can grab it.",
      F("THE GUN\nDROPS", "ANY INNOCENT CAN GRAB IT", "pop16-mm2-logo.jpg", RBX("Murder Mystery 2"), bs=130)),
    L("It was made by one developer, Nikilis, and came out in January 2014.",
      S("1 DEVELOPER", "NIKILIS, JANUARY 2014", "sunset", "grass", bs=140, ic=[{"n": "code", "x": 860, "y": 820, "s": 150, "a": "float"}])),
    L("It has over 24 billion visits, and this week more than 600,000 people were playing it at once.",
      {"count": {"from": 0, "to": 600000, "fmt": "{:,.0f}+", "dur": 1.5}, "sub": "PLAYING AT ONCE", "bg": "red", "ground": "dark", "bc": "#ffffff", "bs": 150, "fx": ["red"]}),
    L("Players still trade rare Godly knives, and the Halloween events bring new ones every year.",
      F("GODLY\nKNIVES", "HALLOWEEN EVENTS", "pop16-mm2-heroes.jpg", RBX("Murder Mystery 2"), bs=140)),
    tease("Next: how two developers made DOORS.", "NEXT: HOW DOORS\nWAS MADE", "pop15-doors-seek.jpg", RBX("DOORS")),
    end("Murderer, sheriff, or innocent?", "WHICH ROLE\nIS BEST?", bg="dark", ground="dark"),
   ], pron={"Nikilis": "Nick-ill-iss"}, mood="spooky")

# 135 DOORS was made by two developers
ep(135, "doors-made-by-two-devs", "DOORS Was Made by 2 Developers", 46, "#ffb300", HEART, 1.04,
   {"font": MF + "CrimsonText-Bold.ttf", "size": 100, "upper": False, "fill": "#fff8e1", "hi": "#ffca28", "stroke": 6},
   [L("DOORS, one of Roblox's scariest games, was made by just two developers.",
      F("MADE BY\n2 PEOPLE", "DOORS", "pop15-doors-seek.jpg", RBX("DOORS"), bs=130)),
    L("They're called LSPLASH and Red, and the game was based on another Roblox game called Rooms.",
      F("LSPLASH\n+ RED", "BASED ON ROOMS", "pop15-doors-lobby.jpg", RBX("DOORS"), bs=140)),
    L("It came out on August 10th, 2022, with one floor: The Hotel.",
      S("THE HOTEL", "AUGUST 10, 2022", "night", "stone", bs=160, vig=True,
        ic=[{"n": "key", "x": 860, "y": 820, "s": 140, "a": "spin"}], av=[av([0.0, 0.8], "walk", "a")])),
    L("The Hotel got a huge revamp in January 2023, and modifiers to make runs harder came that August.",
      F("REVAMPED", "JANUARY 2023", "pop15-doors-rush.jpg", RBX("DOORS"), bs=170)),
    L("An event called The Hunt added a secret floor, The Backdoor.",
      S("THE\nBACKDOOR", "ADDED IN THE HUNT", "dark", "dark", bs=150, vig=True, fx=["red"], ic=[{"n": "eye", "x": 540, "y": 820, "s": 200, "a": "pulse"}])),
    L("Then Floor 2, The Mines, finally arrived on August 30th, 2024.",
      F("FLOOR 2", "AUGUST 30, 2024", "pop15-doors-alarm.jpg", RBX("DOORS"), bs=180)),
    tease("Next: the day Roblox had 47 million people online.", "NEXT: 47 MILLION\nONLINE", "pop15-sab-dragon.jpg", RBX("Steal a Brainrot")),
    end("Hotel or Mines?", "HOTEL OR\nMINES?", bg="dark", ground="dark"),
   ], pron={"LSPLASH": "L splash"}, mood="spooky")

# 136 Roblox's biggest day ever
ep(136, "roblox-biggest-day-ever", "ROBLOX's Biggest Day Ever", 50, "#00e676", LIAM, 1.06,
   {"font": MF + "Anton-Regular.ttf", "size": 104, "hi": "#69f0ae", "stroke": 8},
   [L("This is the day 47 million people were on Roblox at the same time.",
      F("47 MILLION\nAT ONCE", "ROBLOX'S BIGGEST DAY", "pop15-sab-dragon.jpg", RBX("Steal a Brainrot"), bs=116)),
    L("It was August 23rd, 2025, and two games started a fake admin war.",
      S("ADMIN WAR", "AUGUST 23, 2025", "red", "dark", bc="#ffffff", bs=170, fx=["red"],
        av=[av([-1.6, 0.6], "cheer", "a", hold="sword"), av([1.6, 0.6], "cheer", "b", hold="sword")])),
    L("Steal a Brainrot against Grow a Garden. Grow a Garden hit at least 22.3 million players.",
      S("22.3 MILLION", "GROW A GARDEN", "day", "grass", bs=160, fx=["sparkle"], props=[["tree", -1.8, -1.8], ["tree", 1.8, -2.0]], av=[av([0.0, 0.8], "walk", "g")])),
    L("And all of Roblox hit 47.4 million at once, smashing the old record of about 32.7 million.",
      {"count": {"from": 0, "to": 47.4, "fmt": "{:.1f}M", "dur": 1.6}, "sub": "ON ROBLOX AT ONCE", "bg": "party", "ground": "purple", "bs": 220, "fx": ["confetti"]}),
    L("Then in September, Steal a Brainrot's Extinct Event pulled in 24 million on its own.",
      F("24 MILLION", "EXTINCT EVENT", "pop15-sab-chicken.jpg", RBX("Steal a Brainrot"), bs=170)),
    L("And in January 2026, a Bruno Mars concert in the game peaked at 12.8 million.",
      S("BRUNO MARS", "12.8 MILLION AT ONCE", "night", "stone", rays="#ffffff", bs=140, fx=["sparkle"],
        av=[av([0.0, 1.0], "cheer", "g"), av([-1.8, 0.4], "jump", "a"), av([1.8, 0.4], "jump", "b")])),
    tease("Next: Roblox deleted the oof sound, and then it came back.", "NEXT: THE OOF\nWAS DELETED", "pop16-crossroads.jpg", RBX("Classic: Crossroads")),
    end("Were you online that day?", "WERE YOU\nTHERE?", bg="party", ground="purple"),
   ], pron=BR_PRON)

# ============================================================ GEOMETRY DASH (real clips)
GDE = dict(edition="GEOMETRY DASH", mood="spooky")

# 137 Zoink verifies Acheron
ZA, ZAC = "gd16-acheron.mp4", "Clip: Zoink, Acheron verification"
ep(137, "zoink-verifies-acheron", "Zoink Verified Acheron", 58, "#ff1744", MIKE, 1.08,
   {"font": MF + "BlackOpsOne-Regular.ttf", "size": 92, "fill": "#ffffff", "hi": "#ff5252", "stroke": 8},
   [L("This is the run that made Acheron the hardest level in Geometry Dash.",
      CLIP("gd16-acheron-end.mp4", "THE HARDEST\nLEVEL", "ACHERON", 2.0, ZAC, bs=124)),
    L("Acheron was hosted by ryamu, with Riot as co-host, and a long list of builders.",
      CLIP("gd16-acheron-mid.mp4", "ACHERON", "HOSTED BY RYAMU", 0, ZAC, bs=150)),
    L("The first verifier, Wolvez, got all the way to 96 percent, then dropped it in April 2022 because of health problems.",
      CLIP("gd16-acheron-mid.mp4", "96% ...\nTHEN DROPPED", "WOLVEZ, APRIL 2022", 6.5, ZAC, bs=124)),
    L("So it became an open race. Zoink buffed his own version, fixed the hitboxes, and got to 91 percent.",
      CLIP("gd16-acheron-end.mp4", "OPEN RACE", "ZOINK: 91%", 0, ZAC, bs=150)),
    L("Then, in August 2022, after 72,808 attempts, he beat it.",
      {"count": {"from": 0, "to": 72808, "fmt": "{:,.0f}", "dur": 1.6}, "sub": "ATTEMPTS", "bg": "red", "ground": "dark", "bc": "#ffffff", "bs": 170, "fx": ["red"], "vig": True}),
    L("100 percent. Level verified.",
      CLIP("gd16-acheron-end.mp4", "VERIFIED!", "100%", 9.0, ZAC, bs=170)),
    L("It went in at number 2 on the Demonlist, and on October 7th, 2022, it was moved to number 1.",
      F("#1", "OCTOBER 7, 2022", "pop15-gd-demonlist.jpg", "Image: Pointercrate Demonlist", bs=200, w=760, cy=1040, h=820)),
    L("And the next player to beat it legit took 121,749 attempts. That was Doggie.",
      CLIP("gd16-acheron-mid.mp4", "NEXT: 121,749\nATTEMPTS", "DOGGIE", 3.0, ZAC, bs=124)),
    tease("Next: how Doggie beat Acheron.", "NEXT: DOGGIE\nVS ACHERON", "pop15-gd-47.jpg", "Clip: Doggie"),
    end("Could you beat Acheron?", "COULD YOU\nBEAT IT?", bg="red", ground="dark"),
   ], pron=GD_PRON, **GDE)

# 138 Zoink verifies Thinking Space II
TS, TSC = "gd16-ts2.mp4", "Clip: Zoink, Thinking Space II verification"
ep(138, "zoink-verifies-thinking-space-2", "Zoink Beat Thinking Space II", 50, "#00e5ff", FENRIR, 1.06,
   {"font": MF + "Audiowide-Regular.ttf", "size": 92, "fill": "#ffffff", "hi": "#18ffff", "stroke": 8},
   [L("This level was number 1 in Geometry Dash for nine months. This is the run that beat it.",
      CLIP("gd16-ts2-end.mp4", "#1 FOR 9\nMONTHS", "THINKING SPACE II", 0, TSC, bs=124)),
    L("It's Thinking Space II, hosted by DrCuber, CairoX and NineDice.",
      CLIP("gd16-ts2-mid.mp4", "THINKING\nSPACE II", "DRCUBER, CAIROX, NINEDICE", 0, TSC, bs=124)),
    L("It was nerfed to around top 15, then Zoink buffed it back up to a possible top 1.",
      CLIP("gd16-ts2-mid.mp4", "BUFFED\nBACK UP", "BY ZOINK", 6.0, TSC, bs=140)),
    L("He verified it on May 25th, 2025, after 83,913 attempts across 31 streams.",
      {"count": {"from": 0, "to": 83913, "fmt": "{:,.0f}", "dur": 1.6}, "sub": "ATTEMPTS, 31 STREAMS", "bg": "night", "ground": "stone", "bs": 170, "fx": ["sparkle"], "vig": True}),
    L("Along the way, he died 11 times after 90 percent.",
      CLIP("gd16-ts2-end.mp4", "11 DEATHS\nPAST 90%", "SO CLOSE", 5.0, TSC, bs=124)),
    L("It was placed number 1 on the Demonlist in September 2025, and stayed there until Society passed it in June 2026.",
      F("#1 UNTIL\nJUNE 2026", "THEN SOCIETY", "pop15-gd-demonlist.jpg", "Image: Pointercrate Demonlist", bs=124, w=760, cy=1040, h=820)),
    tease("Next: the level that used to be impossible.", "NEXT: ONCE\nIMPOSSIBLE", "pop15-gd-66.jpg", "Clip: Doggie"),
    end("Could you beat it?", "COULD YOU\nBEAT IT?", bg="night", ground="stone"),
   ], pron=GD_PRON, **GDE)

# 139 Silent clubstep
SC, SCC = "gd16-silent.mp4", "Clip: Doggie, Silent clubstep"
ep(139, "silent-clubstep-impossible", "The Level That Was Impossible", 56, "#b388ff", MIKE, 1.08,
   {"font": MF + "BlackOpsOne-Regular.ttf", "size": 92, "fill": "#ffffff", "hi": "#b388ff", "stroke": 8},
   [L("For years, this Geometry Dash level was called humanly impossible.",
      CLIP("gd16-silent-end.mp4", "HUMANLY\nIMPOSSIBLE", "SILENT CLUBSTEP", 0, SCC, bs=124)),
    L("It's Silent clubstep, a silent remake of Clubstep by Sailent.",
      CLIP("gd16-silent-mid.mp4", "SILENT\nCLUBSTEP", "BY SAILENT", 0, SCC, bs=140)),
    L("It has the 8 jumps of hell: eight tiny cube jumps, almost frame perfect.",
      CLIP("gd16-silent-mid.mp4", "8 JUMPS\nOF HELL", "ALMOST FRAME PERFECT", 6.0, SCC, bs=140)),
    L("A nerfed version was finally verified by paqoe in July 2022, after about 138,000 attempts.",
      {"count": {"from": 0, "to": 138000, "fmt": "{:,.0f}", "dur": 1.6}, "sub": "PAQOE'S ATTEMPTS", "bg": "night", "ground": "stone", "bs": 170, "fx": ["sparkle"], "vig": True}),
    L("Zoink beat it next, in just 22,199. Then Doggie, in March 2023, after 120,190.",
      CLIP("gd16-silent-end.mp4", "DOGGIE:\n120,190", "ZOINK: 22,199", 4.0, SCC, bs=130)),
    L("Doggie's furthest fail before that was only 75 percent.",
      CLIP("gd16-silent-end.mp4", "BEST FAIL:\n75%", "THEN 100%", 8.0, SCC, bs=130)),
    L("And one player, Vision, needed 821,027 attempts.",
      {"count": {"from": 0, "to": 821027, "fmt": "{:,.0f}", "dur": 1.8}, "sub": "VISION'S ATTEMPTS", "bg": "red", "ground": "dark", "bc": "#ffffff", "bs": 160, "fx": ["red"], "vig": True}),
    tease("Next: the run that made Acheron number 1.", "NEXT: ZOINK VS\nACHERON", "pop15-gd-20.jpg", "Clip: Doggie"),
    end("How many attempts would you need?", "HOW MANY\nATTEMPTS?", bg="night", ground="stone"),
   ], pron=GD_PRON, **GDE)

# 140 Doggie beats Acheron
DA, DAC = "gd16-doggie-acheron.mp4", "Clip: Doggie, Acheron"
ep(140, "doggie-beats-acheron", "Doggie Beat Acheron", 44, "#ff9100", PUCK, 1.06,
   {"font": MF + "RussoOne-Regular.ttf", "size": 92, "hi": "#ffab40", "stroke": 8},
   [L("Doggie took 121,749 attempts to beat this level.",
      CLIP("gd16-dacheron-end.mp4", "121,749\nATTEMPTS", "DOGGIE VS ACHERON", 0, DAC, bs=124)),
    L("It's Acheron, which was number 1 on the Demonlist, the hardest level in the game.",
      CLIP("gd16-dacheron-mid.mp4", "ACHERON", "#1 ON THE DEMONLIST", 0, DAC, bs=150)),
    L("Zoink verified it first, after 72,808 attempts.",
      CLIP("gd16-dacheron-mid.mp4", "ZOINK:\n72,808", "THE VERIFIER", 6.0, DAC, bs=140)),
    L("Doggie kept going, and on November 1st, 2022, he beat it.",
      CLIP("gd16-dacheron-end.mp4", "100%", "NOVEMBER 1, 2022", 6.0, DAC, bs=200)),
    L("He also found an easier way through a click at 35 percent, and every victor since has used it.",
      CLIP("gd16-dacheron-mid.mp4", "HIS TRICK\nAT 35%", "EVERYONE USES IT", 3.0, DAC, bs=130)),
    L("Four years later, he beat Grief, the new hardest level, in 436,879 attempts.",
      F("THEN GRIEF:\n436,879", "OCTOBER 2026", "pop15-gd-66.jpg", "Clip: Doggie, GRIEF verification", bs=124)),
    tease("Next: the level that took one player 821,027 attempts.", "NEXT: 821,027\nATTEMPTS", "pop15-gd-20.jpg", "Clip: Doggie"),
    end("Who's better, Doggie or Zoink?", "DOGGIE OR\nZOINK?", bg="red", ground="dark"),
   ], pron=GD_PRON, **GDE)

# ============================================================ MEME LORE
ML = dict(edition="MEME LORE")

# 141 Verity
VE, VEC = "ml16-verity.mp4", "Clip: Verity mod gameplay (YouTube)"
ep(141, "verity-meme-origin", "The Origin of Verity", 56, "#ffd600", HEART, 1.04,
   {"font": MF + "Chewy-Regular.ttf", "size": 104, "upper": False, "fill": "#ffffff", "hi": "#ffea00", "stroke": 8},
   [L("It's me, it's Verity. But where did this yellow smile actually come from?",
      CLIP("ml16-verity-a.mp4", "IT'S ME,\nIT'S VERITY", "THE ORIGIN", 0, VEC, bs=120)),
    L("Verity is from a Minecraft horror series by a YouTuber called ThatMob. It's officially called Something.",
      CLIP("ml16-verity-a.mp4", "MINECRAFT\nHORROR", "BY THATMOB", 5.0, VEC, bs=130)),
    L("It started on May 30th, 2026. A player installs a mysterious AI mod, and it summons Verity, a happy yellow sphere.",
      S("AN AI MOD", "MAY 30, 2026", "night", "stone", bs=170, vig=True, ic=[{"n": "code", "x": 860, "y": 820, "s": 150, "a": "float"}],
        av=[av([0.0, 0.8], "walk", "a")])),
    L("At first it helps you. Then it starts knowing things about your real life, and asking creepy questions.",
      CLIP("ml16-verity-b.mp4", "IT KNOWS\nTOO MUCH", "CREEPY QUESTIONS", 0, VEC, bs=130)),
    L("The first video reportedly got over 22 million views in about two months.",
      {"count": {"from": 0, "to": 22, "fmt": "{:.0f}M+", "dur": 1.3}, "sub": "VIEWS", "bg": "gold", "ground": "grass", "bs": 220, "fx": ["sparkle"]}),
    L("Then on July 10th, Horror Skunx dropped a song about Verity, with over 12 million views in a month. That's where it's me, it's Verity comes from.",
      S("THE SONG", "12 MILLION+ VIEWS", "party", "purple", rays="#ffffff", bs=170, fx=["confetti"],
        av=[av([-1.6, 0.6], "cheer", "a"), av([1.6, 0.6], "cheer", "b")])),
    tease("Next: the Fortnite and Yeat collab.", "NEXT: YEAT IN\nFORTNITE", "pop15-fn-festival.jpg", "Image: Epic Games"),
    end("Is Verity creepy or cute?", "CREEPY OR\nCUTE?", bg="gold", ground="grass"),
   ], pron={"ThatMob": "That Mob", "Skunx": "Skunks"}, mood="spooky", **ML)

# 142 Fortnite x Yeat
YE, YEC = "ml16-yeat.mp4", "Clip: Fortnite x Yeat trailer, Epic Games"
ep(142, "fortnite-yeat-collab", "Yeat Is in Fortnite", 50, "#d500f9", LIAM, 1.06,
   {"font": MF + "BarlowCondensed-ExtraBold.ttf", "size": 112, "fill": "#ffffff", "hi": "#ea80fc", "stroke": 8},
   [L("Yeat is now in Fortnite, and the collab is full of hidden secrets.",
      CLIP("ml16-yeat-a.mp4", "YEAT IN\nFORTNITE", "HIDDEN SECRETS", 0, YEC, "pop15-fn-festival.jpg", "Image: Epic Games", bs=130)),
    L("It dropped in the Item Shop on October 15th, 2026, with a trailer called Real Lyfe.",
      CLIP("ml16-yeat-b.mp4", "REAL LYFE", "OCTOBER 15, 2026", 0, YEC, "pop15-fn-br.jpg", "Image: Epic Games", bs=150)),
    L("You get two outfits with over 27 style combos, and his famous bell as a pickaxe.",
      S("27+ STYLES", "+ THE YEAT BELL PICKAXE", "party", "purple", rays="#ffffff", bs=150, fx=["sparkle"],
        av=[av([0.0, 1.0], "cheer", "g", hold="sword")])),
    L("One emote has you riding a tiny truck, and another is his one finger handshake.",
      S("TINY TRUCK\nEMOTE", "+ THE HANDSHAKE", "sunset", "grass", bs=130,
        av=[av([-1.4, 0.6], "wave", "a"), av([1.4, 0.6], "wave", "b")])),
    L("And there's unreleased music. Find Yeat in Battle Royale and collect his missing bells to unlock a song called HeliMan.",
      CLIP("ml16-yeat-a.mp4", "UNRELEASED\nMUSIC", "FIND YEAT'S BELLS", 6.0, YEC, "pop15-fn-festival.jpg", "Image: Epic Games", bs=130)),
    L("Three more secret songs unlock with codes hidden in the trailer.",
      S("3 SECRET\nSONGS", "CODES IN THE TRAILER", "night", "stone", bs=140, vig=True, ic=[{"n": "key", "x": 860, "y": 820, "s": 150, "a": "spin"}])),
    tease("Next: Doggie's 121,749 attempts on Acheron.", "NEXT: DOGGIE\nVS ACHERON", "pop15-gd-47.jpg", "Clip: Doggie"),
    end("Did you buy the Yeat skin?", "DID YOU\nBUY IT?", bg="party", ground="purple"),
   ], pron={"Yeat": "Yeet", "HeliMan": "Heli man", "Lyfe": "Life"}, **ML)

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
