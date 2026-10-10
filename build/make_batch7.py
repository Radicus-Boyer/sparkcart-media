"""Writes batch 7 (facts checked 2026-10-10): 5 x 70 s and 5 x 30 s.
Roblox Edition #62-66 and Most Popular Games of the Internet #35-39. Openings name the game or a hook, never a year."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CTA = " Comment for which game we should review next! Follow for more!"
CTA_SUB = "COMMENT FOR WHICH GAME\nWE SHOULD REVIEW NEXT!"


def L(t, sc, say=None):
    d = {"t": t, "sc": sc}
    if say:
        d["say"] = say
    return d


# ------------------------------------------------------------------ popular helpers
def hook(img, big, label, credit, **k):
    return dict(kind="hook", img=img, big=big, label=label, credit=credit, **k)


def text(big, icon=None, sub=None, **k):
    d = dict(kind="text", big=big, **k)
    if icon:
        d["icon"] = icon
    if sub:
        d["sub"] = sub
    return d


def stat(val=None, label=None, sub=None, icon=None, num=None, **k):
    d = dict(kind="stat", **k)
    if num:
        d["num"] = num
    else:
        d["val"] = val
    for n, v in (("label", label), ("sub", sub), ("icon", icon)):
        if v:
            d[n] = v
    return d


def lst(items, head=None):
    return dict(kind="list", items=items, **({"head": head} if head else {}))


def photo(img, label, credit, **k):
    return dict(kind="photo", img=img, label=label, credit=credit, **k)


def vs(left, right):
    return dict(kind="vs", left=left, right=right)


def outro(q, question):
    return L(q + CTA, dict(kind="outro", question=question))


POP = []

# ------------------------------------------------------------------ 35 Balatro (70 s)
POP.append(dict(num=35, theme="balatro", game="Balatro", slug="35-balatro", target=70,
    pron={"Balatro": "Bal-a-tro", "LocalThunk": "Local Thunk", "Saskatchewan": "Saskatchewan", "Northernlion": "Northern Lion", "Fiverr": "Fiver"},
    lines=[
        L("Balatro was made by one anonymous developer, and it got nominated for Game of the Year.",
          hook("pop7-joker.jpg", ["BALATRO", "*ONE ANONYMOUS DEV"], "REAL JOKER CARDS", "Photo: Czlowiek Oddzielany Mechanicznie, CC0", size=96)),
        L("He goes by LocalThunk, and he's from Saskatchewan, Canada.",
          text(["LOCAL", "*THUNK"], "user-secret", "Saskatchewan, Canada")),
        L("It started in 2021 as an online version of a card game called Big Two.",
          text(["BIG TWO"], "dice", "a Cantonese card game", size=150)),
        L("Then he watched Northernlion stream Luck Be a Landlord, and turned it into a roguelike deckbuilder.",
          text(["ROGUELIKE", "*DECKBUILDER"], "video", "inspired by a Northernlion stream", size=110)),
        L("You play poker hands to score chips times mult, and collect Jokers that break the rules.",
          vs(["CHIPS", "BLUE", "from your poker hand"], ["MULT", "RED", "boosted by Jokers"])),
        L("It was almost called Joker Poker. Balatro is Latin for jester.",
          text(["JOKER", "*POKER?"], "face-laugh-squint", "balatro = Latin for jester")),
        L("He quit his job about a year before release, and found the composer on Fiverr.",
          lst([["briefcase", "QUIT HIS JOB"], ["music", "COMPOSER FROM FIVERR"]], "ALL IN")),
        L("It made over a million dollars in its first eight hours.",
          stat("$1M+", "IN 8 HOURS", "launch day, February 2024", "coins", size=190)),
        L("It sold a million copies in a month, and over five million by January 2025.",
          stat(num=[5000000, "{:,.0f}+"], label="COPIES BY JANUARY 2025", icon="chart-line")),
        L("At The Game Awards, it won three awards, and was the first solo project ever nominated for Game of the Year.",
          lst([["trophy", "BEST INDEPENDENT GAME"], ["star", "BEST DEBUT INDIE"], ["gamepad", "BEST MOBILE GAME"]], "3 GAME AWARDS")),
        L("One ratings board once gave it an 18 plus rating for gambling imagery. It was lowered after an appeal.",
          text(["RATED 18+", "*FOR CARDS"], "ban", "PEGI, later lowered to 12", size=124)),
        L("And in endless mode, around ante 39, the score you need gets so big the game just shows NaN. Not a number.",
          text(["NaN"], "infinity", "ante 39: the numbers break", size=220),
          say="And in endless mode, around ante thirty nine, the score you need gets so big the game just shows N, A, N. Not a number."),
        outro("What's your best Joker?", "BEST JOKER?"),
    ]))

# ------------------------------------------------------------------ 36 Peak (70 s)
POP.append(dict(num=36, theme="peak", game="Peak", slug="36-peak", target=70,
    pron={"Landfall": "Land fall", "bbno$": "baby no money"},
    lines=[
        L("Peak started as a one month game jam, and sold over ten million copies.",
          hook("pop7-climb.jpg", ["PEAK", "*10 MILLION CLIMBERS"], "A REAL SUMMIT RIDGE", "Photo: Apoutsiak, CC BY 3.0", size=96)),
        L("You and up to three friends are Scouts, stranded after a plane crash. The only way out is up.",
          text(["THE ONLY", "*WAY IS UP"], "person-hiking", "stranded after a plane crash")),
        L("You climb a huge mountain, while managing a stamina bar.",
          text(["STAMINA"], "bolt", "your most important resource", size=150)),
        L("Hunger, injuries, weight, poison and cold all shrink your stamina.",
          lst([["utensils", "HUNGER"], ["heart-crack", "INJURIES"], ["skull", "POISON"], ["snowflake", "COLD"]], "WHAT DRAINS IT")),
        L("There are six biomes, and the mountain changes every 24 hours.",
          stat("24 HRS", "NEW MOUNTAIN", "six biomes to climb", "mountain", size=170)),
        L("Climb too far ahead of your group, and the Scoutmaster shows up.",
          text(["THE", "*SCOUTMASTER"], "eye", "don't leave your friends behind", size=120)),
        L("It was made by two studios, Aggro Crab and Landfall, during a game jam in South Korea.",
          text(["2 STUDIOS", "*1 GAME JAM"], "users", "Aggro Crab + Landfall, in South Korea", size=120)),
        L("It launched in June 2025, and sold 100,000 copies in 24 hours.",
          stat(num=[100000, "{:,.0f}"], label="COPIES IN 24 HOURS", icon="cart-shopping")),
        L("A million in the first week. Five million in the first month.",
          lst([["chart-line", "1M: FIRST WEEK"], ["chart-line", "5M: FIRST MONTH"]], "THEN IT EXPLODED")),
        L("By mid August, it passed ten million.",
          stat("10M+", "COPIES SOLD", "by mid-August 2025", "trophy", size=190)),
        L("It won Best Multiplayer Game at the Golden Joysticks, and Better With Friends at the Steam Awards.",
          lst([["trophy", "BEST MULTIPLAYER GAME"], ["users", "BETTER WITH FRIENDS"]], "AWARDS")),
        L("Streamers loved it too. It won Stream Game of the Year at The Streamer Awards.",
          text(["STREAM GAME", "*OF THE YEAR"], "video", "The Streamer Awards", size=110)),
        L("It even had an in-game concert with bbno$, and a Fortnite bundle. Then this August, The Final Ascent update arrived.",
          lst([["music", "BBNO$ CONCERT"], ["gamepad", "FORTNITE BUNDLE"], ["flag-checkered", "THE FINAL ASCENT"]]),
          say="It even had an in-game concert with baby no money, and a Fortnite bundle. Then this August, The Final Ascent update arrived."),
        outro("Did you ever reach the top?", "REACHED THE TOP?"),
    ]))

# ------------------------------------------------------------------ 37 Lethal Company (70 s)
POP.append(dict(num=37, theme="lethal", game="Lethal Company", slug="37-lethal-company", target=70,
    pron={"Zeekerss": "Zeekers"},
    lines=[
        L("Lethal Company is a horror game about the worst job in the universe.",
          hook("pop7-factory.jpg", ["LETHAL COMPANY", "*THE WORST JOB EVER"], "A REAL ABANDONED MILL", "Photo: George A. Grant, NARA, public domain", size=86)),
        L("You and up to three coworkers fly to abandoned moons, collecting scrap for the Company.",
          text(["COLLECT", "*SCRAP"], "rocket", "on abandoned moons")),
        L("Every three days, you have to hit a profit quota. Miss it, and you get ejected into space.",
          text(["MAKE QUOTA", "*OR ELSE"], "dollar-sign", "every three days", size=120)),
        L("And get back to the ship before midnight, or autopilot leaves without you.",
          text(["BACK BY", "*MIDNIGHT"], "clock", "or the ship leaves")),
        L("Voice chat is proximity based, so if you wander off, nobody hears you scream.",
          text(["NOBODY", "*HEARS YOU"], "headset", "proximity voice chat")),
        L("The monsters include the Thumper, the Jester, and the Bracken, which snaps your neck, and runs if you spot it.",
          lst([["ghost", "THE THUMPER"], ["mask", "THE JESTER"], ["eye", "THE BRACKEN"]], "WATCH OUT FOR")),
        L("It was made by Zeekerss, who used to make Roblox games.",
          text(["ZEEKERSS"], "user", "a former Roblox developer", size=140)),
        L("Development was supposed to take six months.",
          stat("6 MONTHS", "THE ORIGINAL PLAN", "it took a lot longer", "hourglass-half", size=150)),
        L("It came out in early access in October 2023, and hit 100,000 players at once on Steam in November.",
          stat(num=[100000, "{:,.0f}"], label="PLAYERS AT ONCE ON STEAM", icon="users")),
        L("By January, it had sold an estimated ten million copies.",
          stat("10M", "COPIES (ESTIMATED)", "by January 2024", "chart-line", size=200)),
        L("It won Steam's Better With Friends award, and Stream Game of the Year at The Streamer Awards.",
          lst([["users", "BETTER WITH FRIENDS"], ["video", "STREAM GAME OF THE YEAR"]], "AWARDS")),
        L("It also won Best Early Access Game at the Golden Joysticks.",
          text(["BEST EARLY", "*ACCESS GAME"], "trophy", "Golden Joystick Awards", size=110)),
        L("Then in 2024, the Employee from Lethal Company came to Fortnite.",
          text(["THE", "*EMPLOYEE"], "gamepad", "in Fortnite, June 2024")),
        outro("Have you ever made quota?", "MADE QUOTA?"),
    ]))

# ------------------------------------------------------------------ 38 R.E.P.O. (30 s)
POP.append(dict(num=38, theme="repo", game="R.E.P.O.", slug="38-repo", target=30,
    pron={"R.E.P.O.": "Repo", "Semibots": "Semi bots", "Semiwork": "Semi work"},
    lines=[
        L("In R.E.P.O., you're a little robot, carrying priceless valuables past monsters.",
          hook("pop7-vases.jpg", ["R.E.P.O.", "*DON'T BREAK IT"], "REAL ANTIQUE VASES", "Photo: The Met, public domain", size=100),
          say="In Repo, you're a little robot, carrying priceless valuables past monsters."),
        L("Up to six players are Semibots. Get valuables to the extraction point without breaking them, and earn surplus to spend on upgrades.",
          text(["DON'T", "*BREAK IT"], "robot", "up to 6 Semibots")),
        L("R.E.P.O. stands for Retrieve, Extract, and Profit Operation.",
          lst([["box", "RETRIEVE"], ["truck", "EXTRACT"], ["coins", "PROFIT"]], "R.E.P.O. ="),
          say="Repo stands for Retrieve, Extract, and Profit Operation."),
        L("It was made by Semiwork, and hit 230,000 players at once on its first weekend.",
          stat(num=[230000, "{:,.0f}"], label="PLAYERS AT ONCE", sub="first weekend", icon="users")),
        L("It even topped Steam's sales charts for a week.",
          text(["#1 ON", "*STEAM"], "trophy", "top-grossing paid game, March 2025")),
        outro("What's the worst thing you broke?", "WORST THING YOU BROKE?"),
    ]))

# ------------------------------------------------------------------ 39 Baldi's Basics (30 s)
POP.append(dict(num=39, theme="baldi", game="Baldi's Basics", slug="39-baldis-basics", target=30,
    pron={"McGonigal": "Mc-Gonna-gull", "Markiplier": "Mark-iplier"},
    lines=[
        L("Baldi's Basics looks like a 90s learning game, but it's actually a horror game.",
          hook("pop7-school.jpg", ["BALDI'S BASICS", "*IT'S A HORROR GAME"], "A REAL OLD CLASSROOM", "Photo: State Library of Queensland, public domain", size=88)),
        L("Collect seven notebooks and escape, while Baldi asks you math questions.",
          text(["7", "*NOTEBOOKS"], "book", "then escape", size=150)),
        L("Get one wrong, and he gets faster, smacking his ruler as he comes for you.",
          text(["WRONG", "*ANSWER"], "ruler", "he gets faster", size=140)),
        L("It was made by Micah McGonigal for a game jam, where it placed second.",
          text(["2ND PLACE"], "award", "Meta Game Jam", size=130)),
        L("Markiplier's video of it got over a million views in a day.",
          stat("1.2M", "VIEWS IN 24 HOURS", "Markiplier's video", "video", size=190)),
        outro("Did you ever beat Baldi?", "DID YOU BEAT BALDI?"),
    ]))

# ================================================================== Roblox Edition
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


def end(q, big, bg="party", **k):
    av = [{"p": [-1.8, 0.6], "a": "cheer", "c": "a"}, {"p": [0, 1.2], "a": "wave", "c": "g"}, {"p": [1.8, 0.6], "a": "cheer", "c": "b"}]
    return L(q + CTA, S(big, CTA_SUB, bg, "purple", rays="#ffffff", ss=50, sgap=62, fx=["confetti"], av=av, **k))


def crowd(n=25, appear=1.2):
    return {"n": n, "appear": appear}


RB = []

def av(p, a="bob", c="a", **k):
    d = {"p": p, "a": a, "c": c}
    d.update(k)
    return d

# ------------------------------------------------------------------ 62 Animal Hospital (70 s)
RB.append(dict(num=62, slug="62-animal-hospital", file="62 Animal Hospital (70s).mp4", target=70, accent="#4dd0e1", bpm=108, root=57, mood="spooky",
    pron={"Harlow": "Har-low", "RDC": "R D C"},
    lines=[
        L("Animal Hospital is a Roblox horror game. You work the night shift at a vet, and some patients aren't animals.",
          opener("ANIMAL\nHOSPITAL", "SOME PATIENTS AREN'T ANIMALS", "pop7-vet.jpg", "A REAL CAT AT A REAL VET", "Photo: Kathy Eastwood, public domain",
                 bg="dark", ground="stone", bs=116, ss=48, py=905, ph=400, vig=False)),
        L("Up to four players work together. You treat patients, and check every visitor at the front desk.",
          S("NIGHT SHIFT", "UP TO 4 PLAYERS", "night", "stone", bs=140, props=[["house", -2.6, -2.6, {"c": "#e0f7fa"}]],
            av=[av([-1.0, 0.8], "bob", "a", hat="#ffffff"), av([1.0, 0.8], "bob", "g", hat="#ffffff")], pets=[{"k": "cat", "p": [0.0, 1.4], "a": "hop", "c": "#ffffff", "s": 0.7}])),
        L("If a visitor looks wrong, you reject them. Let an anomaly in, and things get bad fast.",
          S("ADMIT OR\nREJECT?", "SPOT THE ANOMALY", "dark", "dark", bs=124, vig=True, fx=["red"],
            av=[av([-1.2, 0.8], "idle", "c", face="o"), av([1.2, 0.8], "idle", "k", face="mean")], ic=[{"n": "question", "x": 540, "y": 760, "s": 130, "a": "pulse"}])),
        L("You also have to drink coffee to keep your sanity up.",
          S("COFFEE =\nSANITY", "DON'T SKIP IT", "sunset", "wood", bs=130, av=[av([0.4, 0.8], "bob", "b")], ic=[{"n": "clock", "x": 860, "y": 850, "s": 140, "a": "pulse"}])),
        L("You can be a doctor, a nurse, a surgeon, or even a secret agent.",
          S("PICK A CLASS", "DOCTOR, NURSE, SURGEON, AGENT", "mint", "stone", bs=130, ss=44,
            av=[av([-2.0, 0.8], "wave", "a", hat="#ffffff"), av([-0.6, 1.0], "bob", "d"), av([0.8, 1.0], "bob", "g"), av([2.0, 0.8], "idle", "k", hat="#212121")])),
        L("One monster, the Stalker, disguises itself as a patient at check-in. Just looking at it drains your sanity.",
          S("THE STALKER", "DON'T LOOK AT IT", "red", "dark", bc="#ffffff", bs=150, vig=True, fx=["red"],
            av=[av([0.0, 0.8], "sneak", "k", face="mean", s=0.7)], ic=[{"n": "eye", "x": 860, "y": 840, "s": 140, "a": "flicker"}])),
        L("At the end of the night, Dr. Harlow grades your shift.",
          S("DR. HARLOW", "GRADES YOUR SHIFT", "day", "stone", bs=150, av=[av([0.4, 0.8], "idle", "w", hat="#ffffff")], ic=[{"n": "star", "x": 860, "y": 840, "s": 140, "a": "spin"}])),
        L("And fans love the Head Nurse, a white cat who's all over fan art.",
          S("HEAD NURSE", "A WHITE CAT. FAN FAVORITE.", "party", "purple", rays="#ffffff", bs=140, ss=46,
            pets=[{"k": "cat", "p": [0.4, 0.6], "a": "hop", "c": "#ffffff", "s": 1.0}], ic=[{"n": "heart", "x": 860, "y": 820, "s": 130, "a": "pulse"}], fx=["sparkle"])),
        L("It came out in May 2026, from Animal Anomaly. Updates drop almost every two weeks.",
          S("ANIMAL\nANOMALY", "UPDATES EVERY ~2 WEEKS", "sunset", "grass", bs=124, ss=46, av=[av([0.4, 0.6], "wave", "b")], ic=[{"n": "calendar", "x": 860, "y": 850, "s": 150, "a": "float"}])),
        L("The July update added Liz, a fired journalist who knows the truth about the outbreak.",
          S("LIZ", "SHE KNOWS THE TRUTH", "night", "night", bs=220, av=[av([0.4, 0.8], "idle", "e")], ic=[{"n": "tv", "x": 860, "y": 840, "s": 140, "a": "flicker"}])),
        L("After that, over 1.2 million people played at the same time.",
          S(None, "PLAYERS AT ONCE", "gold", "stone", rays="#ffffff", count={"to": 1.2, "fmt": "{:.1f} MILLION"}, bs=130, crowd=crowd(), fx=["confetti"])),
        L("A TikTok of the characters dancing got 9.4 million views. Trackers count over 2.4 billion visits.",
          S(None, "VISITS (PER TRACKERS)", "party", "purple", rays="#ffffff", count={"to": 2.4, "fmt": "{:.1f} BILLION+"}, bs=124, crowd=crowd(20, 0.8),
            ic=[{"n": "tv", "x": 860, "y": 800, "s": 130, "a": "float"}])),
        L("At RDC 2026, it won four awards, more than any other game that night.",
          S("4 AWARDS", "MOST OF THE NIGHT, RDC 2026", "gold", "grass", rays="#ffffff", bs=170, ss=46, props=[["trophy", 0.0, -1.0]], fx=["confetti"])),
        end("Would you let this patient in?", "WOULD YOU LET\nTHEM IN?", bg="arena"),
    ]))

# ------------------------------------------------------------------ 63 Roblox Innovation Awards (70 s)
RB.append(dict(num=63, slug="63-innovation-awards", file="63 Roblox Innovation Awards 2026 (70s).mp4", target=70, accent="#ffca28", bpm=126, root=60,
    pron={"Nosniy": "Noz-nee", "Valkenheim": "Valken-heim", "RDC": "R D C", "UGC": "U G C", "TTK": "T T K"},
    lines=[
        L("The Roblox Innovation Awards just crowned this year's best games, and one brand new game swept the night.",
          opener("INNOVATION\nAWARDS", "WHO WON THIS YEAR?", "pop7-trophy.jpg", "A REAL OLD TROPHY", "Photo: public domain",
                 bg="gold", ground="purple", bs=110, ss=48, py=905, ph=400)),
        L("The awards were handed out at RDC 2026, Roblox's big developer conference.",
          S("RDC 2026", "ROBLOX DEVELOPERS CONFERENCE", "arena", "purple", bs=170, ss=44, crowd=crowd(16, 0.8), fx=["sparkle"])),
        L("The biggest winner was Animal Hospital, with four awards, including Best New Game and People's Choice.",
          S("ANIMAL\nHOSPITAL", "4 AWARDS. THE BIG WINNER.", "gold", "grass", rays="#ffffff", bs=124, ss=46, props=[["trophy", 0.0, -1.2]],
            pets=[{"k": "cat", "p": [1.6, 1.2], "a": "hop", "c": "#ffffff", "s": 0.6}], fx=["confetti"])),
        L("It also took Best Innovation in Creative Direction, and the Builderman Award.",
          S("BUILDERMAN\nAWARD", "+ CREATIVE DIRECTION", "party", "purple", rays="#ffffff", bs=120, ic=[{"n": "crown", "x": 860, "y": 840, "s": 150, "a": "float"}])),
        L("RIVALS won Best Shooter, and its studio, Nosniy Games, won Best Studio.",
          S("RIVALS", "BEST SHOOTER + BEST STUDIO", "arena", "stone", bs=190, ss=46, av=[av([-1.2, 0.8], "idle", "b", hold="gun"), av([1.2, 0.8], "idle", "k", hold="gun")],
            ic=[{"n": "crosshair", "x": 540, "y": 780, "s": 120, "a": "pulse"}])),
        L("DOORS won Best Use of Audio.",
          S("DOORS", "BEST USE OF AUDIO", "dark", "wood", bs=200, vig=True, av=[av([0.4, 0.8], "sneak", "c", face="o")], ic=[{"n": "eye", "x": 860, "y": 840, "s": 140, "a": "flicker"}])),
        L("99 Nights in the Forest won Best Survival, and Jujutsu Shenanigans won Best Action.",
          S("99 NIGHTS", "BEST SURVIVAL", "forest", "forest", bs=170, fx=["fireflies"], props=[["tree", -2.4, -2.0], ["tree", 2.2, -2.4]], av=[av([0.0, 0.8], "idle", "a")])),
        L("Mini War won Best Strategy, and Piggy Intercity won Best RPG.",
          S("MINI WAR\n+ PIGGY", "STRATEGY + RPG", "sunset", "stone", bs=124, av=[av([-1.0, 0.8], "run", "b", to=[0.0, 0.8], hold="sword"), av([1.2, 0.8], "idle", "w")])),
        L("FIFA Super Soccer won Best Sports, and TTK won Best Innovation in Tech.",
          S("BEST SPORTS", "FIFA SUPER SOCCER", "day", "grass", bs=150, ic=[{"n": "globe", "x": 860, "y": 840, "s": 140, "a": "spin"}], av=[av([-0.6, 0.8], "run", "a", to=[0.6, 0.8])])),
        L("Finish the Word won Best Puzzle, and plus one Speed Keyboard Escape won Best Party and Casual.",
          S("+1 SPEED\nKEYBOARD ESCAPE", "BEST PARTY & CASUAL", "party", "purple", bs=100, ss=46, fx=["speed"], av=[av([-1.6, 0.8], "run", "g", to=[1.6, 0.8])])),
        L("Steal a Brainrot's GOAT collab won Best Innovation in a Branded Game.",
          S("STEAL A\nBRAINROT", "BEST BRANDED GAME", "gold", "purple", rays="#ffffff", bs=124, av=[av([0.4, 0.8], "sneak", "k")], ic=[{"n": "trophy", "x": 860, "y": 840, "s": 140, "a": "pulse"}])),
        L("And Natural Disaster Survival, one of the oldest games on the list, won Best Classic.",
          S("BEST CLASSIC", "NATURAL DISASTER SURVIVAL", "sunset", "grass", bs=150, ss=44, props=[["house", -2.4, -2.4]], ic=[{"n": "bolt", "x": 860, "y": 820, "s": 140, "a": "shake"}])),
        L("Creators won too. Valkenheim won Best UGC Creator, and Laughability won Best Video Star.",
          S("CREATORS\nWON TOO", "VALKENHEIM + LAUGHABILITY", "mint", "grass", bs=124, ss=44, av=[av([-1.0, 0.8], "cheer", "d"), av([1.0, 0.8], "cheer", "e")],
            ic=[{"n": "clapper", "x": 860, "y": 820, "s": 130, "a": "float"}])),
        end("Which game got robbed?", "WHICH GAME\nGOT ROBBED?", bg="arena"),
    ]))

# ------------------------------------------------------------------ 64 Blade Ball (30 s)
RB.append(dict(num=64, slug="64-blade-ball", file="64 Blade Ball (30s).mp4", target=30, accent="#ef5350", bpm=140, root=55,
    pron={"Wiggity": "Wig-it-ee"},
    lines=[
        L("Blade Ball is dodgeball, but the ball is trying to kill you.",
          opener("BLADE BALL", "DODGEBALL, BUT DEADLY", "pop7-dodge.jpg", "REAL-LIFE DODGEBALL", "Photo: U.S. Navy, public domain",
                 bg="arena", ground="stone", bs=130)),
        L("The ball targets one player at a time. Parry at the right moment to send it at someone else, and it gets faster every hit.",
          S("PARRY!", "IT GETS FASTER EVERY HIT", "arena", "stone", bs=200, fx=["speed"],
            av=[av([-1.4, 0.8], "idle", "b", hold="sword"), av([1.4, 0.8], "idle", "k", hold="sword")], ic=[{"n": "bolt", "x": 540, "y": 780, "s": 130, "a": "shake"}])),
        L("It was made by Wiggity, and hit one billion visits in just 62 days, beating Piggy's record.",
          S(None, "DAYS TO 1 BILLION VISITS", "gold", "stone", rays="#ffffff", count={"to": 62, "fmt": "{:.0f} DAYS"}, bs=170, crowd=crowd(), fx=["confetti"])),
        L("In October 2023, only Blox Fruits and Brookhaven were bigger.",
          S("#3 ON\nROBLOX", "OCTOBER 2023", "party", "purple", rays="#ffffff", bs=150, props=[["pedestal", 0.0, -0.6]], ic=[{"n": "trophy", "x": 860, "y": 830, "s": 140, "a": "float"}])),
        end("Have you ever won a round?", "EVER WON\nA ROUND?", bg="arena"),
    ]))

# ------------------------------------------------------------------ 65 Hide and Seek Extreme (30 s)
RB.append(dict(num=65, slug="65-hide-and-seek-extreme", file="65 Hide and Seek Extreme (30s).mp4", target=30, accent="#ffa726", bpm=124, root=60,
    pron={"Tim7775": "Tim seventy seven seventy five"},
    lines=[
        L("In Hide and Seek Extreme, you're the size of a toy, hiding in a giant house.",
          opener("HIDE AND SEEK\nEXTREME", "YOU'RE THE SIZE OF A TOY", "pop7-doll.jpg", "A REAL 1600s DOLL HOUSE", "Photo: public domain",
                 bg="day", ground="wood", bs=100, ss=48, py=905, ph=400)),
        L("One random player is It, and gets a special power to find everyone else.",
          S("YOU'RE IT", "WITH A SPECIAL POWER", "red", "wood", bc="#ffffff", bs=190, av=[av([0.0, 0.8], "run", "k", to=[1.4, 0.8], face="mean")], ic=[{"n": "eye", "x": 860, "y": 830, "s": 140, "a": "pulse"}])),
        L("Hiders can even taunt It, which is brave, or a really bad idea.",
          S("TAUNT!", "BRAVE OR DUMB?", "party", "wood", bs=200, props=[["crate", -1.8, -1.2]], av=[av([1.0, 0.8], "jump", "g")], ic=[{"n": "question", "x": 860, "y": 830, "s": 130, "a": "shake"}])),
        L("It was made by Tim7775, and critics praised the creative maps and how easy it is to jump in.",
          S("TIM7775", "CREATIVE MAPS. EASY TO PLAY.", "mint", "wood", bs=150, ss=46, av=[av([0.4, 0.6], "wave", "b")], ic=[{"n": "star", "x": 860, "y": 840, "s": 140, "a": "spin"}])),
        end("Hider, or seeker?", "HIDER OR\nSEEKER?"),
    ]))

# ------------------------------------------------------------------ 66 Royale High (30 s)
RB.append(dict(num=66, slug="66-royale-high", file="66 Royale High (30s).mp4", target=30, accent="#f48fb1", bpm=118, root=64,
    pron={"Callmehbob": "Call me bob"},
    lines=[
        L("Royale High is a Roblox school where you dress up as royalty, or a magical creature.",
          opener("ROYALE HIGH", "A SCHOOL FOR ROYALTY", "pop7-castle.jpg", "A REAL CASTLE", "Photo: Wilfredor, CC0",
                 bg="party", ground="purple", bs=130)),
        L("It's a role play game set in a fantasy school, with classes, dances, and huge outfits.",
          S("FANTASY\nSCHOOL", "CLASSES, DANCES, OUTFITS", "mint", "purple", bs=130, ss=46,
            av=[av([-1.2, 0.8], "wave", "d", hat="#ffd54f"), av([1.2, 0.8], "cheer", "e", hat="#f48fb1")], fx=["sparkle"])),
        L("It was made by Callmehbob, and launched in 2017.",
          S("CALLMEHBOB", "LAUNCHED 2017", "sunset", "grass", bs=130, av=[av([0.4, 0.6], "wave", "b")], ic=[{"n": "crown", "x": 860, "y": 840, "s": 140, "a": "float"}])),
        L("By October 2022, it had over 8.2 billion visits. That makes it one of the biggest role play games on Roblox.",
          S(None, "VISITS BY OCTOBER 2022", "gold", "purple", rays="#ffffff", count={"to": 8.2, "fmt": "{:.1f} BILLION"}, bs=130, crowd=crowd(), fx=["confetti"])),
        end("What's your dream outfit?", "DREAM\nOUTFIT?"),
    ]))

# ================================================================== write
ICONS = json.load(open(os.path.join(ROOT, "engine", "modern", "icons.json")))
NAMES = {35: "Balatro", 36: "Peak", 37: "Lethal Company", 38: "R.E.P.O.", 39: "Baldi's Basics"}
os.makedirs(os.path.join(ROOT, "episodes", "popular"), exist_ok=True)
for ep in POP:
    ep = dict(preset="popular", hdr="tag", **ep)
    ep["file"] = f"{ep['num']:02d} - {NAMES[ep['num']]} ({ep['target']}s).mp4"
    slug = ep.pop("slug")
    for l in ep["lines"]:
        sc = l["sc"]
        for ic in [sc.get("icon")] + [i[0] for i in sc.get("items", [])]:
            if ic and ic not in ICONS:
                print("  MISSING ICON", slug, ic)
        if sc.get("img") and not os.path.exists(os.path.join(ROOT, "episodes", "assets", sc["img"])):
            print("  MISSING IMAGE", slug, sc["img"])
    json.dump(ep, open(os.path.join(ROOT, "episodes", "popular", slug + ".json"), "w"), indent=1, ensure_ascii=False)
    print(slug, len(ep["lines"]), "lines", sum(len(l.get("say", l["t"]).split()) for l in ep["lines"]), "words", "target", ep["target"])
for ep in RB:
    ep = dict(preset="roblox", hdr="tag", **ep)
    json.dump(ep, open(os.path.join(ROOT, "episodes", "roblox", ep["slug"] + ".json"), "w"), indent=1, ensure_ascii=False)
    print(ep["slug"], len(ep["lines"]), "lines", sum(len(l.get("say", l["t"]).split()) for l in ep["lines"]), "words", "target", ep["target"])
