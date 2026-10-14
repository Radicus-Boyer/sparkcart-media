"""Writes batch 11 (facts checked 2026-10-14): 6 Roblox videos (8-Bit Backstory #84-89, Roblox look) and
3 NES videos (#90-92, NES look). All voiced by af_sarah, 29-80 s, each with its own caption style.
Openings name the game or a hook, never a year."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CTA = " Comment for which game we should review next! Follow for more!"
CTA_SUB = "COMMENT FOR WHICH GAME\nWE SHOULD REVIEW NEXT!"
MF = "../modern/fonts/"


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


def opener(big, sub, img, label, credit, bg="day", ground="grass", **k):
    ph = dict(img=img, label=label, credit=credit, y=k.pop("py", 800), h=k.pop("ph", 430))
    ph.update(k.pop("pk", {}))
    return S(big, sub, bg, ground, instant=True, by=310, photo=ph, **k)


def end(q, big, bg="party", ground="purple", **k):
    av_ = [{"p": [-1.8, 0.6], "a": "cheer", "c": "a"}, {"p": [0, 1.2], "a": "wave", "c": "g"}, {"p": [1.8, 0.6], "a": "cheer", "c": "b"}]
    return L(q + CTA, S(big, CTA_SUB, bg, ground, rays="#ffffff", ss=50, sgap=62, fx=["confetti"], av=av_, **k))


def crowd(n=25, appear=1.2):
    return {"n": n, "appear": appear}


def av(p, a="bob", c="a", **k):
    d = {"p": p, "a": a, "c": c}
    d.update(k)
    return d

RB = []

# ------------------------------------------------------------------ 84 Blue Lock: Rivals (BlackOpsOne captions)
RB.append(dict(num=84, slug="84-blue-lock-rivals", file="84 Blue Lock Rivals.mp4", target=33, accent="#40c4ff", bpm=136, root=59,
    voice="af_sarah", speed=1.08,
    cap={"font": MF + "BlackOpsOne-Regular.ttf", "size": 92, "hi": "#40c4ff", "stroke": 8},
    pron={},
    lines=[
        L("Blue Lock: Rivals turned an anime about soccer strikers into one of Roblox's biggest sports games.",
          opener("BLUE LOCK:\nRIVALS", "ANIME SOCCER ON ROBLOX", "pop7-trophy.jpg", "A REAL SOCCER TEAM AND ITS CUP, 1931", "Photo: public domain",
                 bg="day", ground="grass", bs=110, ss=46, py=905, ph=400)),
        L("It's five against five, and every character has their own special abilities.",
          S("5 VS 5", "SPECIAL ABILITIES", "mint", "grass", bs=170, fx=["speed"], av=[av([-1.4, 0.8], "run", "a", to=[-0.2, 0.6]), av([1.2, 0.8], "jump", "e")])),
        L("It's a fan-made game, inspired by the anime Blue Lock, and it came out in July 2024.",
          S("FAN-MADE", "INSPIRED BY BLUE LOCK", "sunset", "grass", bs=150, ic=[{"n": "heart", "x": 860, "y": 830, "s": 140, "a": "pulse"}], av=[av([0.0, 0.8], "wave", "b")])),
        L("In April 2025, about 713,000 people were playing at the same time.",
          S(None, "PLAYING AT ONCE", "gold", "grass", rays="#ffffff", count={"to": 713, "fmt": "{:.0f},000"}, bs=140, crowd=crowd(), fx=["confetti"])),
        L("Trackers now count around 5 billion visits, and over 6 million favorites.",
          S("5 BILLION", "VISITS (PER TRACKERS)", "party", "grass", rays="#ffffff", bs=140, ic=[{"n": "star", "x": 860, "y": 830, "s": 140, "a": "spin"}])),
        end("Who's your favorite player?", "FAVORITE\nPLAYER?", bg="day", ground="grass"),
    ]))

# ------------------------------------------------------------------ 85 Theme Park Tycoon 2 (TitanOne, yellow box)
RB.append(dict(num=85, slug="85-theme-park-tycoon-2", file="85 Theme Park Tycoon 2.mp4", target=31, accent="#ffca28", bpm=120, root=62,
    voice="af_sarah", speed=1.0,
    cap={"font": MF + "TitanOne-Regular.ttf", "size": 80, "stroke": 0, "fill": "#3e2723", "hi": "#d84315", "box": "#ffd54f", "radius": 30},
    pron={"Den_S": "Den S"},
    lines=[
        L("Theme Park Tycoon 2 lets you build a whole theme park, from the ground up.",
          opener("THEME PARK\nTYCOON 2", "BUILD YOUR OWN PARK", "pop8-inflatable.jpg", "A REAL INFLATABLE PARK", "Photo: public domain",
                 bg="day", ground="grass", bs=110, ss=46, py=905, ph=400)),
        L("You get your own plot, and you can build alone, or with friends.",
          S("YOUR OWN\nPLOT", "SOLO OR WITH FRIENDS", "mint", "grass", bs=120, props=[["base", 0.0, -1.0]], av=[av([-1.4, 0.8], "wave", "a"), av([1.4, 0.8], "cheer", "c")])),
        L("Build rides, design your own roller coasters, and decorate with hundreds of scenery pieces.",
          S("DESIGN\nCOASTERS", "HUNDREDS OF SCENERY PIECES", "sunset", "grass", bs=124, ss=42, props=[["tower", -1.8, -2.0], ["tree", 1.8, -2.2], ["house", 0.2, -2.8]], fx=["sparkle"])),
        L("It's made by Den_S, and its biggest crowd ever came in July 2025, more than 13 years after it was published.",
          S("RECORD\nCROWD", "JULY 2025, 13+ YEARS LATER", "party", "grass", rays="#ffffff", bs=130, crowd=crowd(18, 0.6), fx=["confetti"])),
        L("Trackers count over 1.6 billion visits.",
          S(None, "VISITS (PER TRACKERS)", "gold", "grass", rays="#ffffff", count={"to": 1.6, "fmt": "{:.1f} BILLION"}, bs=140)),
        end("What's your best coaster called?", "BEST COASTER\nNAME?", bg="day", ground="grass"),
    ]))

# ------------------------------------------------------------------ 86 Funky Friday (Bangers, one word at a time, pink)
RB.append(dict(num=86, slug="86-funky-friday", file="86 Funky Friday.mp4", target=34, accent="#ff4081", bpm=150, root=60,
    voice="af_sarah", speed=1.1,
    cap={"font": MF + "Bangers-Regular.ttf", "size": 136, "mode": "word", "fill": "#ff80ab", "hi": "#ff80ab", "cy": 1470},
    pron={"Funkin'": "Funkin"},
    lines=[
        L("Funky Friday is a Roblox rhythm battle, where you hit arrows to the beat.",
          opener("FUNKY\nFRIDAY", "HIT THE ARROWS", "pop2-52nd-street.jpg", "A REAL MUSIC STREET, NEW YORK", "Photo: William P. Gottlieb, public domain",
                 bg="party", ground="purple", bs=130, ss=46, py=905, ph=400)),
        L("It's made by Lyte Interactive, and it's based on the indie game Friday Night Funkin'.",
          S("LYTE\nINTERACTIVE", "BASED ON FRIDAY NIGHT FUNKIN'", "night", "purple", bs=116, ss=40, av=[av([0.0, 0.8], "bob", "e")], ic=[{"n": "star", "x": 860, "y": 830, "s": 130, "a": "pulse"}])),
        L("Hit a note right on time, and you get a Sick. Miss the timing, and it's a Bad.",
          S("SICK!!", "OR BAD...", "red", "purple", bc="#ffffff", bs=190, fx=["speed"], av=[av([0.0, 0.8], "jump", "a")])),
        L("Hit it at the exact millisecond, and you get a special Fresh rating, with its own sound.",
          S("FRESH!", "THE EXACT MILLISECOND", "mint", "purple", bs=190, fx=["sparkle"], ic=[{"n": "bolt", "x": 860, "y": 820, "s": 150, "a": "flicker"}])),
        L("Battle other players, or play solo. Points buy new animations and emotes.",
          S("BATTLE!", "POINTS = NEW EMOTES", "party", "purple", rays="#ffffff", bs=170, av=[av([-1.2, 0.8], "cheer", "b"), av([1.2, 0.8], "cheer", "g")])),
        L("One song mod was in the game for only about ten minutes before it got removed.",
          S("10 MINUTES", "SHORTEST-LIVED SONG MOD", "dark", "purple", bs=150, ic=[{"n": "clock", "x": 860, "y": 820, "s": 150, "a": "shake"}])),
        L("Trackers count over 2 billion visits.",
          S(None, "VISITS (PER TRACKERS)", "gold", "purple", rays="#ffffff", count={"to": 2, "fmt": "{:.0f} BILLION+"}, bs=150, crowd=crowd(), fx=["confetti"])),
        end("What's your hardest song?", "HARDEST\nSONG?", bg="party", ground="purple"),
    ]))

# ------------------------------------------------------------------ 87 The Mimic (CrimsonText, sentence case, pale red)
RB.append(dict(num=87, slug="87-the-mimic", file="87 The Mimic.mp4", target=41, accent="#e57373", bpm=96, root=50, mood="spooky",
    voice="af_sarah", speed=1.0,
    cap={"font": MF + "CrimsonText-Bold.ttf", "size": 100, "upper": False, "fill": "#f5f5f5", "hi": "#ef9a9a", "stroke": 6},
    pron={"Yasu": "Yah-soo", "Isamu": "Ee-sah-moo", "Umibozu": "Oo-mee-bo-zoo", "yokai": "yo-kai", "Gashadokuro": "Gah-sha-doh-koo-roh"},
    lines=[
        L("The Mimic is a Roblox horror game built on real Japanese legends.",
          opener("THE MIMIC", "BUILT ON REAL LEGENDS", "pop4-hotel-hallway.jpg", "A REAL EMPTY HALLWAY", "Photo: cogdogblog, CC0",
                 bg="dark", ground="dark", bs=150, ss=46, vig=True)),
        L("The story is split into books, and each book has its own cast.",
          S("BOOKS", "EACH WITH ITS OWN STORY", "night", "dark", bs=170, fx=["fireflies"], ic=[{"n": "moon", "x": 860, "y": 800, "s": 140, "a": "float"}])),
        L("In Control, you play as Yasu, who's hunting a demon that cursed his family.",
          S("CONTROL", "YASU VS A DEMON", "red", "dark", bc="#ffffff", bs=160, fx=["red"], av=[av([0.0, 0.8], "sneak", "a", face="o")])),
        L("In Jealousy, Isamu searches for the truth about his brother, in a world ruled by the Umibozu.",
          S("JEALOUSY", "THE UMIBOZU'S WORLD", "night", "dark", bs=150, av=[av([-0.6, 0.8], "idle", "e", face="o")], ic=[{"n": "eye", "x": 860, "y": 800, "s": 150, "a": "pulse"}])),
        L("Along the way, you'll meet yokai from folklore, like the Gashadokuro, a giant skeleton.",
          S("YOKAI", "LIKE A GIANT SKELETON", "dark", "dark", bs=170, vig=True, fx=["fireflies"], props=[["tower", 1.8, -2.4, {"c": "#eceff1"}]])),
        L("Players compare its scares to horror games like P.T. and Until Dawn.",
          S("SCARY?", "COMPARED TO P.T. & UNTIL DAWN", "red", "dark", bc="#ffffff", bs=170, ss=40, fx=["red"], vig=True)),
        L("Trackers count about 1.3 billion visits, and 3.4 million favorites.",
          S(None, "VISITS (PER TRACKERS)", "night", "dark", count={"to": 1.3, "fmt": "{:.1f} BILLION"}, bs=150, crowd=crowd(14, 0.6))),
        end("Which book scared you most?", "SCARIEST\nBOOK?", bg="dark", ground="dark"),
    ]))

# ------------------------------------------------------------------ 88 Bubble Gum Simulator INFINITY (Chewy, pink box)
RB.append(dict(num=88, slug="88-bubble-gum-simulator-infinity", file="88 Bubble Gum Simulator Infinity.mp4", target=32, accent="#f48fb1", bpm=126, root=64,
    voice="af_sarah", speed=1.04,
    cap={"font": MF + "Chewy-Regular.ttf", "size": 92, "upper": False, "stroke": 0, "fill": "#ffffff", "hi": "#fff176", "box": "#ec407a", "radius": 40},
    pron={},
    lines=[
        L("Bubble Gum Simulator Infinity is all about blowing the biggest bubble you can.",
          opener("BUBBLE GUM\nSIMULATOR ∞", "BLOW. HATCH. REPEAT.", "pop5-puppy.jpg", "A REAL PET, NO EGG NEEDED", "Photo: lisaschaos, CC BY 2.0",
                 bg="mint", ground="grass", bs=104, ss=46, py=905, ph=400)),
        L("You blow gum, sell it for cash, then spend the cash on eggs that hatch pets.",
          S("HATCH\nPETS", "GUM = CASH = EGGS", "party", "grass", rays="#ffffff", bs=140, ic=[{"n": "egg", "x": 540, "y": 780, "s": 190, "a": "shake"}], fx=["coins"])),
        L("Pets go from Common to Legendary, across worlds like Twilight, Zen, and The Void.",
          S("COMMON TO\nLEGENDARY", "TWILIGHT, ZEN, THE VOID", "sunset", "grass", bs=110, ic=[{"n": "star", "x": 860, "y": 820, "s": 140, "a": "spin"}], av=[av([0.0, 0.8], "jump", "c")])),
        L("Some pets are Secret. In the Infinity Egg, the odds are one in forty million and one.",
          S("1 IN\n40,000,001", "SECRET PET ODDS", "night", "grass", bs=120, fx=["sparkle"], ic=[{"n": "egg_gold", "x": 540, "y": 790, "s": 180, "a": "pulse"}])),
        L("It's made by Rumble Studios, and trackers say about 380,000 people once played at the same time.",
          S(None, "PLAYING AT ONCE (PER TRACKERS)", "gold", "grass", rays="#ffffff", count={"to": 380, "fmt": "{:.0f},000"}, bs=140, ss=40, crowd=crowd(), fx=["confetti"])),
        end("What's your rarest pet?", "RAREST\nPET?", bg="mint", ground="grass"),
    ]))

# ------------------------------------------------------------------ 89 Driving Empire (Audiowide, cyan)
RB.append(dict(num=89, slug="89-driving-empire", file="89 Driving Empire.mp4", target=31, accent="#00e5ff", bpm=140, root=57,
    voice="af_sarah", speed=1.04,
    cap={"font": MF + "Audiowide-Regular.ttf", "size": 76, "hi": "#00e5ff", "stroke": 7},
    pron={"Voldex": "Vol-dex", "McLaren": "Mc-Laren"},
    lines=[
        L("Driving Empire lets you race real cars, from brands like Lamborghini and Porsche.",
          opener("DRIVING\nEMPIRE", "REAL CARS. REAL BRANDS.", "pop8-town.jpg", "REAL ROADS FROM ABOVE", "Photo: Serg Bataiev, CC0",
                 bg="sunset", ground="road", bs=124, ss=46, py=905, ph=400)),
        L("There are over 200 cars and boats, and you can customize them.",
          S("200+", "CARS AND BOATS", "day", "road", bs=190, props=[["car", -1.4, -0.8, {"c": "#ff1744"}], ["car", 1.2, -1.6, {"c": "#00b0ff"}]], fx=["speed"])),
        L("You can race, tune your ride, and join community events.",
          S("RACE.\nTUNE. CRUISE.", "COMMUNITY EVENTS TOO", "party", "road", rays="#ffffff", bs=110, props=[["car", 0.0, -0.8, {"c": "#76ff03"}]], fx=["sparkle"])),
        L("It came out in June 2019, and it's now made by Voldex, the same group that owns Brookhaven.",
          S("VOLDEX", "THEY ALSO OWN BROOKHAVEN", "mint", "road", bs=160, props=[["house", 1.8, -2.4]], av=[av([-0.8, 0.8], "wave", "a")])),
        L("This August, it hit its all-time record, about 90,000 players at once.",
          S(None, "PLAYING AT ONCE, AUG 2026", "gold", "road", rays="#ffffff", count={"to": 90, "fmt": "{:.0f},000"}, bs=150, crowd=crowd(), fx=["confetti"])),
        L("Trackers count over 3 billion visits.",
          S("3 BILLION+", "VISITS (PER TRACKERS)", "night", "road", bs=140, props=[["car", 0.0, -0.6, {"c": "#ffd600"}]], fx=["speed"])),
        end("What's your dream car?", "DREAM\nCAR?", bg="sunset", ground="road"),
    ]))

# ================================================================== NES
OUTRO = "Comment for which game we should review next! Follow for more 8-Bit Backstory!"


def outro_nes(q, question):
    return {"say": q + " " + OUTRO, "scene": {"kind": "outro", "question": question, "ask": "COMMENT WHICH GAME TO REVIEW NEXT!", "prop": "none", "bg": "dark"}}


NES = []
NES.append(dict(preset="nes", num=90, name="Final Fantasy", slug="finalfantasy", theme="dark", voice="af_sarah", speed=1.06,
    title_lines=["FINAL", "FANTASY"], year_tag="NES", music={"bpm": 112, "tr": -2, "seed": 90},
    pron={"Sakaguchi": "Sah-kah-goo-chee", "Uematsu": "Oo-eh-mah-tsu", "Gebelli": "Geh-belly", "Nasir": "Nah-seer"},
    lines=[
        {"say": "Final Fantasy was called Final for a reason. Or at least, that's the story.", "scene": {"kind": "title", "prop": "photo", "args": {"file": "pop6-cave.jpg", "rect": [14, 96, 166, 196], "label": "REAL CRYSTALS. PHOTO: PD"}}},
        {"say": "It was made by Square, and directed by Hironobu Sakaguchi.", "scene": {"bg": "desk", "head": "SQUARE", "headsc": 4, "prop": "computer", "args": {"text": "FF"}, "subs": ["DIR. SAKAGUCHI"]}},
        {"say": "Its working title was Fighting Fantasy, but that name already belonged to a series of gamebooks.", "scene": {"bg": "dark", "head": "TAKEN!", "headsc": 4, "prop": "quote", "args": {"text": "FIGHTING FANTASY? ALREADY TAKEN."}}},
        {"say": "Composer Nobuo Uematsu said Final meant Sakaguchi would quit if it flopped, and Square was facing possible bankruptcy.", "scene": {"bg": "city", "head": "LAST CHANCE?", "headsc": 2, "prop": "quote", "args": {"text": "IF IT FLOPS, I QUIT."}}},
        {"say": "Sakaguchi later said any word starting with F would have been fine.", "scene": {"bg": "dark", "head": "JUST AN F?", "headsc": 3, "prop": "quote", "args": {"text": "ANY F WORD WAS FINE."}}},
        {"say": "You pick four heroes at the start, from six classes, and you're stuck with them for the whole game.", "scene": {"bg": "dark", "head": "6 CLASSES", "headsc": 3, "prop": "list", "args": {"items": ["FIGHTER", "THIEF", "BLACK BELT", "RED MAGE", "WHITE MAGE", "BLACK MAGE"], "gap": 0.4}}},
        {"say": "Its programmer, Nasir Gebelli, even added a hidden sliding puzzle that was never in the plan.", "scene": {"bg": "lab", "head": "SECRET PUZZLE", "headsc": 2, "prop": "computer", "args": {"text": "15"}, "subs": ["NASIR GEBELLI"]}},
        {"say": "Square shipped 520,000 copies in Japan at first. By 1994, about 1.3 million had sold worldwide.", "scene": {"bg": "space", "head": "SOLD", "headsc": 3, "prop": "bignum", "args": {"n": 1.3, "fmt": "{:.1f}M", "unit": "BY 1994"}}, "cap": "Square shipped 520,000 copies in Japan at first. By 1994, about 1.3 million had sold worldwide."},
        {"say": "So it wasn't final at all. The series is still going today.", "scene": {"bg": "space", "head": "NOT FINAL!", "headsc": 3, "prop": "award", "args": {"n": "FF", "text": "STILL GOING"}}},
        outro_nes("Which Final Fantasy is your favorite?", "FAVORITE FINAL FANTASY?"),
    ]))
NES.append(dict(preset="nes", num=91, name="Excitebike", slug="excitebike", theme="dark", voice="af_sarah", speed=1.08,
    title_lines=["EXCITEBIKE"], year_tag="NES", music={"bpm": 150, "tr": 2, "seed": 91},
    pron={"Miyamoto": "Mee-ya-moto", "Famicom": "Fami-com"},
    lines=[
        {"say": "Excitebike let you build your own tracks, but most players could never save them.", "scene": {"kind": "title", "prop": "photo", "args": {"file": "pop8-parkour.jpg", "rect": [14, 96, 166, 196], "label": "REAL JUMP - PD"}}},
        {"say": "It was directed by Shigeru Miyamoto.", "scene": {"bg": "park", "head": "MIYAMOTO", "headsc": 3, "prop": "quote", "args": {"text": "DIRECTED BY SHIGERU MIYAMOTO."}}},
        {"say": "Hold B for turbo. But hold it too long, and your engine overheats.", "scene": {"bg": "city", "head": "OVERHEAT!", "headsc": 3, "prop": "quote", "args": {"text": "B = TURBO. TOO MUCH = OVERHEAT."}}},
        {"say": "Design mode let you build tracks from 19 kinds of hurdles.", "scene": {"bg": "grid", "head": "DESIGN MODE", "headsc": 2, "prop": "bignum", "args": {"n": 19, "fmt": "{:.0f}", "unit": "HURDLE TYPES"}}},
        {"say": "But saving them needed the Famicom Data Recorder, and that never came out outside Japan.", "scene": {"bg": "dark", "head": "NO SAVING", "headsc": 3, "prop": "quote", "args": {"text": "DATA RECORDER: JAPAN ONLY."}}},
        {"say": "Its smooth scrolling engine was reused for Super Mario Bros.", "scene": {"bg": "sky", "head": "REUSED!", "headsc": 3, "prop": "quote", "args": {"text": "SAME ENGINE: SUPER MARIO BROS."}}},
        outro_nes("Did you ever overheat?", "EVER OVERHEAT?"),
    ]))
NES.append(dict(preset="nes", num=92, name="Kid Icarus", slug="kidicarus", theme="dark", voice="af_sarah", speed=1.06,
    title_lines=["KID ICARUS"], year_tag="NES", music={"bpm": 128, "tr": 1, "seed": 92},
    pron={"Palutena": "Pa-loo-tena", "Sakamoto": "Sah-kah-moto"},
    lines=[
        {"say": "Kid Icarus has a wizard who can turn you into an eggplant.", "scene": {"kind": "title", "prop": "photo", "args": {"file": "pop7-climb.jpg", "rect": [14, 96, 166, 196], "label": "APOUTSIAK CC BY 3.0"}}},
        {"say": "You play as Pit, an angel climbing up out of the Underworld.", "scene": {"bg": "sky", "head": "CLIMB UP", "headsc": 3, "prop": "quote", "args": {"text": "UP, UP, AND UP."}}},
        {"say": "Medusa has stolen three sacred treasures, and locked up the goddess Palutena.", "scene": {"bg": "dark", "head": "3 TREASURES", "headsc": 2, "prop": "list", "args": {"items": ["MIRROR SHIELD", "LIGHT ARROWS", "WINGS OF PEGASUS"]}}},
        {"say": "Monsters drop hearts, and hearts are the money you spend in shops.", "scene": {"bg": "dark", "head": "HEARTS = MONEY", "headsc": 2, "prop": "shop", "args": {"sign": "HEART SHOP"}}},
        {"say": "In Japan, it saved to a disk. On the NES cartridge, you got passwords instead.", "scene": {"bg": "desk", "head": "PASSWORDS", "headsc": 2, "prop": "quote", "args": {"text": "WRITE IT DOWN!"}}},
        {"say": "It was built by the same Nintendo team as Metroid, and Yoshio Sakamoto joined once Metroid was done.", "scene": {"bg": "space", "head": "METROID TEAM", "headsc": 2, "prop": "quote", "args": {"text": "SAME TEAM. SAME YEAR."}}},
        {"say": "It's famously hard, and there are five different endings.", "scene": {"bg": "dark", "head": "5 ENDINGS", "headsc": 3, "prop": "bignum", "args": {"n": 5, "fmt": "{:.0f}", "unit": "ENDINGS"}}},
        {"say": "Pit came back in Super Smash Bros. Brawl, and got a whole new game, Kid Icarus Uprising, in 2012.", "scene": {"bg": "space", "head": "PIT RETURNS", "headsc": 2, "prop": "award", "args": {"n": "3DS", "text": "UPRISING, 2012"}}},
        outro_nes("Did you ever get turned into an eggplant?", "EVER BEEN AN EGGPLANT?"),
    ]))

# ================================================================== write
for ep in RB:
    ep = dict(preset="roblox", hdr="tag", **ep)
    for l in ep["lines"]:
        ph = l["sc"].get("photo")
        if ph and not os.path.exists(os.path.join(ROOT, "episodes", "assets", ph["img"])):
            print("  MISSING IMAGE", ep["slug"], ph["img"])
    json.dump(ep, open(os.path.join(ROOT, "episodes", "roblox", ep["slug"] + ".json"), "w"), indent=1, ensure_ascii=False)
    print(ep["slug"], len(ep["lines"]), "lines", sum(len(l.get("say", l["t"]).split()) for l in ep["lines"]), "words", "target", ep["target"])

for ep in NES:
    ep["file"] = f"{ep['num']} {ep['name']}.mp4"
    fn = f"{ep['num']}-{ep['name'].lower().replace(' ', '-')}.json"
    json.dump(ep, open(os.path.join(ROOT, "episodes", "nes", fn), "w"), indent=1, ensure_ascii=False)
    print(fn, len(ep["lines"]), "lines", sum(len(l["say"].split()) for l in ep["lines"]), "words")
