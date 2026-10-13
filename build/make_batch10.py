"""Writes batch 10 (facts checked 2026-10-13): 7 Roblox videos (8-Bit Backstory #76-82, Roblox look) and
1 non-Roblox video (#83 Pac-Man, NES look). All voiced by af_sarah (the IKEA voice), 29-80 s, each with its
own caption style. Openings name the game or a hook, never a year."""
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

# ------------------------------------------------------------------ 76 Jujutsu Shenanigans (~74 s, dark arena, one-word Bangers captions)
RB.append(dict(num=76, slug="76-jujutsu-shenanigans", file="76 Jujutsu Shenanigans.mp4", target=50, accent="#b388ff", bpm=138, root=57, mood="spooky",
    voice="af_sarah", speed=1.1,
    cap={"font": MF + "Bangers-Regular.ttf", "size": 128, "mode": "word", "hi": "#d1b3ff", "fill": "#d1b3ff", "cy": 1480},
    pron={"Jujutsu": "Joo-jit-soo", "Kaisen": "Kai-sen", "Tze's": "Zee's"},
    lines=[
        L("Jujutsu Shenanigans gives you 21 fighters, and every single one is free.",
          opener("JUJUTSU\nSHENANIGANS", "21 FIGHTERS. ALL FREE.", "pop6-sparring.jpg", "REAL MARTIAL ARTS SPARRING", "Photo: Carlos Saavedra, CC BY 2.0",
                 bg="arena", ground="dark", bs=104, ss=46, py=905, ph=400)),
        L("It's a battlegrounds game on Roblox, inspired by the anime Jujutsu Kaisen.",
          S("BATTLEGROUNDS", "INSPIRED BY JUJUTSU KAISEN", "dark", "stone", bs=110, ss=44, fx=["sparkle"],
            av=[av([-1.2, 0.8], "cheer", "a", hold="sword"), av([1.2, 0.8], "idle", "e", face="o")])),
        L("It's made by a group called Tze's Shenanigans.",
          S("TZE'S\nSHENANIGANS", "THE DEVELOPER", "night", "night", bs=116, av=[av([0.0, 0.8], "wave", "g")], ic=[{"n": "code", "x": 860, "y": 840, "s": 140, "a": "float"}])),
        L("Most fighting games make you buy characters. Here, you just pick one and go.",
          S("NO PAYWALL", "PICK ANY FIGHTER", "mint", "stone", bs=124, ic=[{"n": "money", "x": 220, "y": 840, "s": 140, "a": "shake"}],
            crowd=crowd(10, 0.4))),
        L("The maps are destructible, so a big hit can smash right through the walls.",
          S("SMASH\nTHE WALLS", "DESTRUCTIBLE MAPS", "red", "stone", bc="#ffffff", bs=124, fx=["red", "speed"],
            props=[["block", -1.6, -1.2], ["block", 1.4, -1.6], ["tower", 2.4, -2.6]], av=[av([-1.0, 1.0], "run", "a", to=[0.8, 0.6])])),
        L("In March 2026, the Disaster Plants update brought the roster to 21 characters, with 21 emotes too.",
          S("DISASTER\nPLANTS", "21 CHARACTERS, 21 EMOTES", "forest", "forest", bs=116, ss=44, props=[["tree", -2.4, -2.4], ["tree", 2.2, -2.2]], fx=["fireflies"],
            av=[av([-0.8, 0.8], "jump", "b"), av([0.8, 0.8], "cheer", "c")])),
        L("Two days later, around 338,000 people were playing at the same time.",
          S(None, "PLAYING AT ONCE", "gold", "stone", rays="#ffffff", count={"to": 338, "fmt": "{:.0f},000"}, bs=140, crowd=crowd(), fx=["confetti"])),
        L("Trackers now count over 4 billion visits, and more than a million and a half favorites.",
          S(None, "VISITS (PER TRACKERS)", "party", "purple", rays="#ffffff", count={"to": 4, "fmt": "{:.0f} BILLION+"}, bs=140,
            ic=[{"n": "heart", "x": 860, "y": 840, "s": 140, "a": "pulse"}])),
        L("It even won Best Action at this year's Roblox Innovation Awards.",
          S("BEST\nACTION", "ROBLOX INNOVATION AWARDS", "gold", "stone", rays="#ffffff", bs=130, props=[["pedestal", 0.0, -0.6]],
            ic=[{"n": "trophy", "x": 540, "y": 760, "s": 200, "a": "float"}], fx=["sparkle"])),
        L("And it's still one of the top ten games on Roblox right now.",
          S("TOP 10", "ON ROBLOX RIGHT NOW", "arena", "dark", bs=170, crowd=crowd(16, 0.4), fx=["speed"])),
        end("Who's your main?", "WHO'S YOUR\nMAIN?", bg="arena", ground="dark"),
    ]))

# ------------------------------------------------------------------ 77 Pilfering Pirates (~55 s, sunset sea, PirataOne captions)
RB.append(dict(num=77, slug="77-pilfering-pirates", file="77 Pilfering Pirates.mp4", target=37, accent="#ffb74d", bpm=124, root=60,
    voice="af_sarah", speed=1.08,
    cap={"font": MF + "PirataOne-Regular.ttf", "size": 112, "upper": False, "hi": "#ffcc66", "stroke": 8},
    pron={"Pseudosuper": "Sue-doe-super"},
    lines=[
        L("In Pilfering Pirates, four crews fight, and the last ship still floating wins.",
          opener("PILFERING\nPIRATES", "LAST SHIP FLOATING WINS", "pop5-paintball.jpg", "A REAL PAINTBALL GUN", "Photo: Ken Thomas, public domain",
                 bg="sunset", ground="wood", bs=110, ss=46, py=905, ph=400)),
        L("Each team crews its own pirate ship, and you can break the other team's cannons.",
          S("4 CREWS", "4 SHIPS", "day", "wood", bs=150, props=[["ship", -1.6, -1.4], ["ship", 1.6, -1.8, {"c": "#c62828"}]], av=[av([0.0, 1.0], "cheer", "a")])),
        L("You get eight tools, like a sword, a flintlock, a rocket launcher, a bomb, a plank, and even a paintball gun.",
          S("8 TOOLS", "SWORD, BOMB, PLANK...", "sunset", "wood", bs=150, av=[av([-1.0, 0.8], "idle", "a", hold="sword"), av([1.0, 0.8], "idle", "e", hold="gun")])),
        L("You can even fly a plane across to the enemy ship.",
          S("FLY OVER", "AND BOARD THEM", "day", "wood", bs=140, ic=[{"n": "rocket", "x": 540, "y": 760, "s": 180, "a": "float"}], props=[["ship", 1.8, -2.0]])),
        L("There's Deathmatch, first to 20 kills, Mega Ships, where boats are twice as big, and Infection, where you join whoever beat you.",
          S("GAME MODES", "DEATHMATCH, MEGA SHIPS, INFECTION", "night", "wood", bs=130, ss=40, props=[["ship", 0.0, -2.2]], fx=["sparkle"])),
        L("Wins earn gold, which buys new boats, planes and trails.",
          S("GOLD", "FOR BOATS, PLANES & TRAILS", "gold", "wood", rays="#ffffff", bs=170, ss=44, fx=["coins"], av=[av([0.0, 0.8], "jump", "b")])),
        L("It was made by Pseudosuper, and trackers count over a billion visits.",
          S(None, "VISITS (PER TRACKERS)", "party", "wood", rays="#ffffff", count={"to": 1.2, "fmt": "{:.1f} BILLION"}, bs=140, crowd=crowd(), fx=["confetti"])),
        end("Sword or rocket launcher?", "SWORD OR\nROCKET?", bg="sunset", ground="wood"),
    ]))

# ------------------------------------------------------------------ 78 Cart Ride Mayhem (~31 s, red alarm look, boxed captions)
RB.append(dict(num=78, slug="78-cart-ride-mayhem", file="78 Cart Ride Mayhem.mp4", target=31, accent="#ff5252", bpm=146, root=55,
    voice="af_sarah", speed=1.0,
    cap={"font": MF + "TitanOne-Regular.ttf", "size": 84, "stroke": 0, "fill": "#ffffff", "hi": "#ffeb3b", "box": "#d32f2f", "radius": 26},
    pron={},
    lines=[
        L("Cart Ride Mayhem takes the classic Roblox cart ride, and adds giant miniguns.",
          opener("CART RIDE\nMAYHEM", "NOW WITH MINIGUNS", "pop4-obstacle-tower.jpg", "A REAL OBSTACLE COURSE", "Photo: U.S. Air Force, public domain",
                 bg="red", ground="road", bs=110, ss=46, py=905, ph=400)),
        L("You ride through explosions, bumpy tracks, and giant skulls.",
          S("EXPLOSIONS!", "BUMPS. SKULLS. CHAOS.", "dark", "road", bc="#ff5252", bs=120, fx=["red", "speed"],
            props=[["car", -0.6, -0.4]], ic=[{"n": "bolt", "x": 860, "y": 820, "s": 150, "a": "shake"}])),
        L("Then you upgrade your cart with new wheels and panels for new powers.",
          S("UPGRADE\nYOUR CART", "WHEELS, PANELS, POWERS", "mint", "road", bs=110, props=[["car", 0.0, -0.6, {"c": "#ffca28"}]], av=[av([1.6, 0.8], "cheer", "a")])),
        L("It was made by Proggramer090, and it came out in July 2024. You can ride solo, or bring friends.",
          S("PROGGRAMER090", "JULY 2024", "sunset", "road", bs=104, av=[av([-0.8, 0.8], "wave", "a"), av([0.8, 0.8], "cheer", "c")], ic=[{"n": "calendar", "x": 860, "y": 840, "s": 140, "a": "float"}])),
        L("Private servers are free, and it updates every week.",
          S("FREE\nSERVERS", "UPDATES EVERY WEEK", "party", "road", rays="#ffffff", bs=130, fx=["confetti"])),
        end("How far did you make it?", "HOW FAR\nDID YOU GET?", bg="red", ground="road"),
    ]))

# ------------------------------------------------------------------ 79 Lumber Tycoon 2 (~64 s, forest, sentence-case Chewy captions)
RB.append(dict(num=79, slug="79-lumber-tycoon-2", file="79 Lumber Tycoon 2.mp4", target=60, accent="#8bc34a", bpm=108, root=62,
    voice="af_sarah", speed=1.06,
    cap={"font": MF + "Chewy-Regular.ttf", "size": 100, "upper": False, "hi": "#c5e1a5", "stroke": 9},
    pron={"Defaultio": "Dee-fault-ee-oh", "Lumberland": "Lumber-land"},
    lines=[
        L("Lumber Tycoon 2 is an old Roblox game that just hit its biggest crowd ever.",
          opener("LUMBER\nTYCOON 2", "BIGGER THAN EVER", "pop6-house.jpg", "A REAL HOUSE, BUILT FROM WOOD", "Photo: Tudor Washington Collins, Auckland Museum, CC BY 4.0",
                 bg="forest", ground="forest", bs=116, ss=46, py=905, ph=400)),
        L("It was made by Defaultio. You show up in Lumberland with an axe, and one goal.",
          S("LUMBERLAND", "BY DEFAULTIO", "day", "forest", bs=130, props=[["tree", -2.2, -2.2], ["tree", 2.0, -2.6], ["tree", 0.4, -3.0]], av=[av([0.0, 1.0], "wave", "b", hold="sword")])),
        L("Chop trees, sell the wood, and build your dream base.",
          S("CHOP. SELL.\nBUILD.", "THE WHOLE GAME", "mint", "wood", bs=110, props=[["crate", -1.6, -1.2], ["house", 1.8, -2.4]], fx=["coins"])),
        L("There are 21 kinds of wood, and planks sell for more than raw logs.",
          S("21 WOODS", "PLANKS BEAT LOGS", "sunset", "forest", bs=150, props=[["tree", -2.0, -2.2, {"c": "#e65100"}], ["tree", 2.0, -2.2, {"c": "#7b1fa2"}]])),
        L("Your base starts as a blueprint, and it only turns solid once you fill it with wood.",
          S("BLUEPRINTS", "FILL THEM WITH WOOD", "night", "wood", bs=130, props=[["base", 0.0, -1.2]], fx=["sparkle"])),
        L("Each server has eight plots of land, but only six players, so two plots are always empty.",
          S("8 PLOTS", "6 PLAYERS", "day", "grass", bs=150, props=[["block", -2.0, -1.6], ["block", 0.0, -1.6], ["block", 2.0, -1.6]], crowd=crowd(6, 0.4))),
        L("Roads lead from spawn to the mountainside, the docks, and a bridge to the Safari, the way into the snowy Taiga.",
          S("THE MAP", "MOUNTAINSIDE, DOCKS, SAFARI, TAIGA", "day", "road", bs=150, ss=38, props=[["tree", -2.4, -2.6], ["ship", 2.0, -2.0], ["tower", 0.2, -3.0]])),
        L("Leave your logs alone too long, and they disappear.",
          S("POOF!", "UNATTENDED LOGS VANISH", "night", "forest", bs=170, fx=["sparkle"], props=[["crate", 0.0, -0.8]], av=[av([1.4, 0.8], "idle", "a", face="o")])),
        L("And to send money to a friend, you need your own land, and an account at least a week old.",
          S("SEND MONEY", "LAND + 1 WEEK OLD ACCOUNT", "gold", "grass", rays="#ffffff", bs=130, ss=42, fx=["coins"], av=[av([-1.0, 0.8], "wave", "b"), av([1.0, 0.8], "cheer", "g")])),
        L("Trackers count over 1.3 billion visits and 4.7 million favorites.",
          S(None, "VISITS (PER TRACKERS)", "gold", "forest", rays="#ffffff", count={"to": 1.3, "fmt": "{:.1f} BILLION"}, bs=140, crowd=crowd(), fx=["confetti"])),
        L("And in September 2026, it hit an all-time high of about 34,000 players at once.",
          S("ALL-TIME\nHIGH!", "~34,000 AT ONCE, SEPT 2026", "party", "forest", rays="#ffffff", bs=130, ss=44, fx=["confetti"], av=[av([0.0, 0.8], "jump", "a")])),
        end("What's the best wood?", "BEST\nWOOD?", bg="forest", ground="forest"),
    ]))

# ------------------------------------------------------------------ 80 Dead Rails (~45 s, night desert, Anton captions, two-word chunks)
RB.append(dict(num=80, slug="80-dead-rails", file="80 Dead Rails.mp4", target=30, accent="#ffab40", bpm=132, root=55, mood="spooky",
    voice="af_sarah", speed=1.1,
    cap={"font": MF + "Anton-Regular.ttf", "size": 104, "hi": "#ffab40", "stroke": 8},
    pron={"RCM": "R C M"},
    lines=[
        L("Dead Rails puts you on a train, through a desert full of zombies.",
          opener("DEAD\nRAILS", "ALL ABOARD. DON'T STOP.", "pop5-subway-1973.jpg", "A REAL OLD TRAIN", "Photo: Erik Calonius, NARA, public domain",
                 bg="sunset", ground="road", bs=130, ss=46, py=905, ph=400)),
        L("The year is 1899, a zombie plague has spread, and the cure is somewhere in Mexico.",
          S("FIND\nTHE CURE", "1899, ZOMBIE PLAGUE", "night", "road", bs=130, fx=["fireflies"], av=[av([-1.0, 0.8], "idle", "a", hold="gun"), av([1.4, 1.0], "sneak", "e", face="o")])),
        L("You and your friends keep the train fueled, and fight off whatever climbs aboard.",
          S("KEEP IT\nMOVING", "FUEL IT. DEFEND IT.", "red", "road", bc="#ffffff", bs=124, fx=["red", "speed"], props=[["car", 0.0, -0.8, {"c": "#5d4037"}]])),
        L("It's made by RCM Games, and in April 2025, about 1.4 million people were playing at once.",
          S(None, "PLAYING AT ONCE (APRIL 2025)", "gold", "road", rays="#ffffff", count={"to": 1.4, "fmt": "{:.1f} MILLION"}, bs=140, ss=40, crowd=crowd(), fx=["confetti"])),
        L("Trackers count over 6 billion visits.",
          S(None, "VISITS (PER TRACKERS)", "dark", "road", count={"to": 6, "fmt": "{:.0f} BILLION+"}, bs=150)),
        end("Did you ever make it to Mexico?", "MADE IT TO\nMEXICO?", bg="sunset", ground="road"),
    ]))

# ------------------------------------------------------------------ 81 Volleyball Legends (~37 s, bright gym, RussoOne captions)
RB.append(dict(num=81, slug="81-volleyball-legends", file="81 Volleyball Legends.mp4", target=32, accent="#29b6f6", bpm=128, root=64,
    voice="af_sarah", speed=1.0,
    cap={"font": MF + "RussoOne-Regular.ttf", "size": 86, "hi": "#4fc3f7", "stroke": 8, "cy": 1440},
    pron={},
    lines=[
        L("Volleyball Legends turned a school gym sport into a Roblox hit.",
          opener("VOLLEYBALL\nLEGENDS", "SPIKE. BLOCK. DIVE.", "pop7-dodge.jpg", "A REAL GYM GAME", "Photo: U.S. Navy, public domain",
                 bg="mint", ground="wood", bs=108, ss=46, py=905, ph=400)),
        L("It's six against six. You bump, set, spike, block and dive.",
          S("6 VS 6", "BUMP, SET, SPIKE", "day", "wood", bs=170, av=[av([-1.4, 0.8], "jump", "a"), av([0.0, 1.0], "cheer", "b"), av([1.4, 0.8], "jump", "c")])),
        L("It came out in December 2024, and a year later, about 286,000 people played at once.",
          S(None, "PLAYING AT ONCE", "gold", "wood", rays="#ffffff", count={"to": 286, "fmt": "{:.0f},000"}, bs=140, crowd=crowd(), fx=["confetti"])),
        L("On PC, you click to bump or spike, press Q to set or block, and Control to dive.",
          S("CLICK. Q.\nCONTROL.", "SPIKE, SET, DIVE", "night", "wood", bs=110, ic=[{"n": "controller", "x": 860, "y": 840, "s": 140, "a": "pulse"}], av=[av([-0.6, 0.8], "jump", "e")])),
        L("It updates every Saturday, and trackers count over 3 billion visits.",
          S("3 BILLION+", "VISITS (PER TRACKERS)", "party", "wood", rays="#ffffff", bs=130, ic=[{"n": "calendar", "x": 860, "y": 840, "s": 140, "a": "float"}])),
        end("Spiker or setter?", "SPIKER OR\nSETTER?", bg="mint", ground="wood"),
    ]))

# ------------------------------------------------------------------ 82 BedWars (~52 s, castle gold, PermanentMarker captions)
RB.append(dict(num=82, slug="82-bedwars", file="82 BedWars.mp4", target=33, accent="#ef5350", bpm=134, root=58,
    voice="af_sarah", speed=1.08,
    cap={"font": MF + "PermanentMarker-Regular.ttf", "size": 92, "upper": False, "hi": "#ff8a80", "stroke": 9},
    pron={"BedWars": "Bed Wars", "SkyWars": "Sky Wars"},
    lines=[
        L("In BedWars, your bed is everything. Lose it, and you can't respawn.",
          opener("BEDWARS", "PROTECT THE BED", "pop7-castle.jpg", "A REAL CASTLE, BUILT TO DEFEND", "Photo: Wilfredor, CC0",
                 bg="day", ground="grass", bs=150, ss=46)),
        L("Each team guards its bed on an island, while trying to break everyone else's.",
          S("GUARD IT", "BREAK THEIRS", "mint", "stone", bs=150, props=[["island", -1.6, -1.6], ["island", 1.6, -2.2, {"c": "#e53935"}]], av=[av([0.0, 1.0], "idle", "a", hold="sword")])),
        L("It's made by Easy.gg, and it came out in 2021.",
          S("EASY.GG", "THE DEVELOPER", "sunset", "stone", bs=150, ic=[{"n": "code", "x": 860, "y": 840, "s": 140, "a": "float"}], av=[av([-0.6, 0.8], "wave", "g")])),
        L("Now there are over ten modes, like Lucky Block, SkyWars, and Infected.",
          S("10+ MODES", "LUCKY BLOCK, SKYWARS, INFECTED", "party", "purple", rays="#ffffff", bs=150, ss=40, props=[["block", -1.8, -1.4, {"c": "#ffd54f"}]], fx=["sparkle"])),
        L("Once your bed breaks, your next death is your last.",
          S("NO BED,\nNO RESPAWN", "ONE LIFE LEFT", "red", "stone", bc="#ffffff", bs=120, fx=["red"], av=[av([0.0, 0.8], "idle", "a", face="o")])),
        L("There's even a Creative mode, where you can build and script your own maps.",
          S("CREATIVE\nMODE", "BUILD AND SCRIPT", "mint", "grass", bs=124, props=[["block", -1.6, -1.2], ["block", -0.6, -1.2], ["tower", 1.6, -2.0]], ic=[{"n": "code", "x": 860, "y": 820, "s": 130, "a": "float"}])),
        L("Trackers count over 11 billion visits.",
          S(None, "VISITS (PER TRACKERS)", "gold", "stone", rays="#ffffff", count={"to": 11, "fmt": "{:.0f} BILLION+"}, bs=140, crowd=crowd(), fx=["confetti"])),
        L("And it still gets a new update every Friday.",
          S("EVERY\nFRIDAY", "A NEW UPDATE", "night", "stone", bs=140, ic=[{"n": "calendar", "x": 860, "y": 840, "s": 140, "a": "pulse"}], fx=["fireflies"])),
        end("Do you defend or rush?", "DEFEND OR\nRUSH?", bg="day", ground="grass"),
    ]))

# ------------------------------------------------------------------ 83 Pac-Man (~68 s, NES look, non-Roblox)
NES = dict(preset="nes", num=83, name="Pac-Man", slug="pacman", theme="dark", voice="af_sarah", speed=1.06,
    title_lines=["PAC-MAN"], year_tag="ARCADE", music={"bpm": 132, "tr": 0, "seed": 83},
    pron={"Iwatani": "Ee-wa-tani", "Namco": "Nam-co", "paku": "pah-koo"},
    lines=[
        {"say": "Pac-Man was partly inspired by a pizza, with one slice missing.", "scene": {"kind": "title", "prop": "photo", "args": {"file": "pop5-pizza.jpg", "rect": [14, 96, 166, 196], "label": "PHOTO: JEFFREYW CC BY 2.0"}}},
        {"say": "It was designed by Toru Iwatani at Namco, in Japan.", "scene": {"bg": "arcade", "head": "TORU IWATANI", "headsc": 2, "prop": "arcade", "subs": ["NAMCO, JAPAN"]}},
        {"say": "He wanted a game that wasn't about shooting, so he made it about eating.", "scene": {"bg": "dark", "head": "NO GUNS", "headsc": 3, "prop": "quote", "args": {"text": "EATING, NOT SHOOTING."}}},
        {"say": "In Japan, it was first called Puck Man, from paku paku, the sound of chomping.", "scene": {"bg": "arcade", "head": "PUCK MAN", "headsc": 3, "prop": "quote", "args": {"text": "PAKU PAKU = CHOMP CHOMP"}}},
        {"say": "In America, the name was changed, because people worried vandals would scratch the P into a different letter.", "scene": {"bg": "city", "head": "NAME CHANGE", "headsc": 2, "prop": "quote", "args": {"text": "PUCK MAN -> PAC-MAN"}}},
        {"say": "The four ghosts don't move the same way. One chases you, one tries to cut you off, and one just wanders.", "scene": {"bg": "dark", "head": "4 GHOSTS", "headsc": 3, "prop": "list", "args": {"items": ["CHASES YOU", "CUTS YOU OFF", "TEAMS UP", "WANDERS"]}}},
        {"say": "Guinness calls it the most successful coin-operated arcade game ever, with over 290,000 machines.", "scene": {"bg": "arcade", "head": "WORLD RECORD", "headsc": 2, "prop": "bignum", "args": {"n": 293822, "fmt": "{:,.0f}", "unit": "ARCADE MACHINES"}}, "cap": "Guinness calls it the most successful coin-operated arcade game ever, with over 290,000 machines."},
        {"say": "Level 256 can't be beaten. A bug fills half the screen with garbage.", "scene": {"bg": "grid", "head": "LEVEL 256", "headsc": 3, "prop": "quote", "args": {"text": "HALF THE SCREEN IS GARBAGE."}}},
        {"say": "So the highest possible score is 3,333,360. You have to eat every dot, fruit and ghost, without dying once.", "scene": {"bg": "dark", "head": "PERFECT SCORE", "headsc": 2, "prop": "bignum", "args": {"n": 3333360, "fmt": "{:,.0f}", "unit": "POINTS"}}, "cap": "So the highest possible score is 3,333,360. You have to eat every dot, fruit and ghost, without dying once."},
        {"say": "For its 30th birthday, Google made it a playable logo, the first one ever.", "scene": {"bg": "space", "head": "PLAYABLE LOGO", "headsc": 2, "prop": "award", "args": {"n": "30", "text": "YEARS OLD"}}},
        {"say": "What's your high score? Comment for which game we should review next! Follow for more 8-Bit Backstory!", "scene": {"kind": "outro", "question": "YOUR HIGH SCORE?", "ask": "COMMENT WHICH GAME TO REVIEW NEXT!", "prop": "none", "bg": "dark"}},
    ])

# ================================================================== write
for ep in RB:
    ep = dict(preset="roblox", hdr="tag", **ep)
    for l in ep["lines"]:
        ph = l["sc"].get("photo")
        if ph and not os.path.exists(os.path.join(ROOT, "episodes", "assets", ph["img"])):
            print("  MISSING IMAGE", ep["slug"], ph["img"])
    json.dump(ep, open(os.path.join(ROOT, "episodes", "roblox", ep["slug"] + ".json"), "w"), indent=1, ensure_ascii=False)
    print(ep["slug"], len(ep["lines"]), "lines", sum(len(l.get("say", l["t"]).split()) for l in ep["lines"]), "words", "target", ep["target"])

NES["file"] = "83 Pac-Man.mp4"
json.dump(NES, open(os.path.join(ROOT, "episodes", "nes", "83-pac-man.json"), "w"), indent=1, ensure_ascii=False)
print("83-pac-man", len(NES["lines"]), "lines", sum(len(l["say"].split()) for l in NES["lines"]), "words")
