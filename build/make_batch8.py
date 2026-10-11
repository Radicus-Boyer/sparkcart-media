"""Writes batch 8 (facts checked 2026-10-11): 5 x 30 s (Roblox #67-71) and 5 x 70 s (Roblox #72-73, Most Popular Games #40-42).
Openings name the game or a hook, never a year."""
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

# ------------------------------------------------------------------ 40 Plants vs. Zombies (70 s)
POP.append(dict(num=40, theme="pvz", game="Plants vs. Zombies", slug="40-plants-vs-zombies", target=70,
    pron={"Zomboss": "Zom-boss", "Peggle": "Peggle", "PopCap": "Pop Cap", "Weedlings": "Weedlings"},
    lines=[
        L("Plants vs. Zombies was almost called Lawn of the Dead.",
          hook("pop8-field.jpg", ["PLANTS VS. ZOMBIES", "*LAWN OF THE DEAD?"], "REAL SUNFLOWERS IN A FIELD", "Photo: Summer Stock, CC0", size=84)),
        L("But zombie movie legend George A. Romero said no, so the name had to change.",
          text(["PERMISSION", "*DENIED"], "ban", "George A. Romero said no", size=124)),
        L("Before that, the enemies weren't even zombies. They were aliens, and the game was called Weedlings.",
          text(["WEEDLINGS"], "seedling", "the aliens version", size=140)),
        L("It was designed by George Fan, and took about three and a half years to make.",
          stat("3.5 YEARS", "TO MAKE", "designed by George Fan", "hourglass-half", size=160)),
        L("Crazy Dave is based on a real person Fan knew, and Fan does Dave's voice himself.",
          text(["CRAZY", "*DAVE"], "user", "voiced by the designer")),
        L("The Dancing Zombie was first based on Michael Jackson, but it was changed after his estate objected.",
          text(["DANCING", "*ZOMBIE"], "music", "redesigned after an objection")),
        L("Testers didn't understand why to collect sun, so the Sunflower's price was cut in half.",
          vs(["BEFORE", "FULL", "too expensive"], ["AFTER", "HALF", "sunflower price"])),
        L("It launched in May 2009, and became PopCap's fastest selling game ever, beating Bejeweled and Peggle.",
          lst([["trophy", "FASTEST-SELLING POPCAP GAME"], ["gem", "BEAT BEJEWELED"], ["star", "BEAT PEGGLE"]], "MAY 2009")),
        L("The iPhone version made over a million dollars in nine days.",
          stat("$1M+", "IN 9 DAYS", "the iPhone version", "coins", size=190)),
        L("In 2011, EA bought PopCap for 750 million dollars.",
          stat("$750M", "EA BUYS POPCAP", "July 2011", "briefcase", size=180)),
        L("The credits song, Zombies on Your Lawn, came out on April 1st, so lots of fans thought it was a joke.",
          text(["APRIL", "*FOOLS?"], "music", "\"Zombies on Your Lawn\" was real")),
        L("There are 49 plants and 26 zombies, and the team spent a whole month on the Dr. Zomboss fight.",
          vs(["PLANTS", "49", "types"], ["ZOMBIES", "26", "types"])),
        outro("What's your favorite plant?", "FAVORITE PLANT?"),
    ]))

# ------------------------------------------------------------------ 41 Tetris (70 s)
POP.append(dict(num=41, theme="tetris", game="Tetris", slug="41-tetris", target=70,
    pron={"Pajitnov": "Pa-zhit-nov", "Elektronika": "Elek-tronika", "Henk": "Henk"},
    lines=[
        L("Tetris has sold over 520 million copies, and it started on a Soviet computer.",
          hook("pop8-pajitnov.jpg", ["TETRIS", "*520 MILLION SOLD"], "ALEXEY PAJITNOV, ITS CREATOR", "Photo: Official GDC, CC BY 2.0", size=100)),
        L("Alexey Pajitnov made it on an Elektronika 60, reportedly in about three weeks.",
          stat("~3 WEEKS", "TO MAKE THE FIRST VERSION", "on an Elektronika 60", "hourglass-half", size=150)),
        L("The name mixes tetra, Greek for four, with tennis, his favorite sport.",
          vs(["TETRA", "4", "four blocks"], ["TENNIS", "+", "his favorite sport"])),
        L("Getting it out of the Soviet Union turned into a giant rights battle.",
          text(["RIGHTS", "*BATTLE"], "scale-balanced", "who owned Tetris?")),
        L("One businessman sold the Western rights before he even owned them.",
          text(["SOLD IT", "*FIRST"], "handshake", "before owning the rights")),
        L("In 1989, Henk Rogers showed up uninvited at the Soviet office, and won the Game Boy rights for Nintendo.",
          text(["UNINVITED"], "door-open", "Henk Rogers, Moscow, 1989", size=130)),
        L("That Game Boy version has sold 35 million copies.",
          stat(num=[35000000, "{:,.0f}"], label="GAME BOY COPIES", icon="gamepad")),
        L("Pajitnov didn't get his rights back until 1995, and The Tetris Company was formed in 1996.",
          lst([["user", "1995: RIGHTS RETURN"], ["building", "1996: THE TETRIS COMPANY"]])),
        L("Guinness calls it the most ported game ever, on at least 70 platforms.",
          stat("70+", "PLATFORMS", "Guinness: most ported game", "trophy", size=200)),
        L("The Tetris effect, seeing falling blocks when you close your eyes, got its name from a 1994 Wired article.",
          text(["THE TETRIS", "*EFFECT"], "eye", "named in Wired, 1994", size=120)),
        L("In 2019, Tetris 99 turned it into a 99 player battle royale.",
          text(["TETRIS", "*99"], "users", "a 99-player battle royale, 2019", size=140)),
        L("And in January 2024, a teenager became the first person to beat NES Tetris, by making the game crash.",
          text(["GAME", "*CRASHED"], "bomb", "NES Tetris, January 2024")),
        outro("What's your highest Tetris score?", "HIGHEST SCORE?"),
    ]))

# ------------------------------------------------------------------ 42 Fall Guys (70 s)
POP.append(dict(num=42, theme="fallguys", game="Fall Guys", slug="42-fall-guys", target=70,
    pron={"Mediatonic": "Media-tonic", "Takeshi's": "Ta-keshi's"},
    lines=[
        L("Fall Guys was pitched as a 100 player game, but 100 beans was just too chaotic.",
          hook("pop8-inflatable.jpg", ["FALL GUYS", "*100 BEANS WAS TOO MANY"], "A REAL INFLATABLE COURSE", "Photo: public domain", size=96)),
        L("So the team cut it to 60.",
          stat("60", "PLAYERS PER SHOW", "down from 100", "users", size=240)),
        L("It was made by Mediatonic, inspired by game shows like Takeshi's Castle and Total Wipeout, plus playground games like tag.",
          lst([["tv", "TAKESHI'S CASTLE"], ["water", "TOTAL WIPEOUT"], ["person-running", "PLAYGROUND TAG"]], "INSPIRED BY")),
        L("Before launch, it briefly became the most watched game on Twitch during its beta.",
          text(["#1 ON", "*TWITCH"], "video", "during the beta")),
        L("It launched in August 2020, and over 1.5 million people played in the first 24 hours.",
          stat(num=[1500000, "{:,.0f}+"], label="PLAYERS IN 24 HOURS", icon="chart-line")),
        L("Two million copies sold on Steam in under a week.",
          stat("2M", "STEAM COPIES", "in under a week", "cart-shopping", size=220)),
        L("It became the most downloaded PlayStation Plus monthly game ever.",
          text(["MOST", "*DOWNLOADED"], "download", "PlayStation Plus monthly game")),
        L("In its first month, it made an estimated 185 million dollars on PC. By December, it passed 11 million PC sales.",
          vs(["MONTH 1", "$185M", "estimated, PC"], ["DECEMBER", "11M", "PC sales"])),
        L("In March 2021, Epic Games, the makers of Fortnite, bought the studio.",
          text(["EPIC", "*BUYS IT"], "handshake", "March 2021")),
        L("Then in June 2022, Fall Guys went free to play, and came to Xbox and Switch.",
          text(["FREE TO", "*PLAY"], "gift", "June 2022")),
        L("In just two weeks, over 50 million people played.",
          stat("50M+", "PLAYERS IN 2 WEEKS", "after going free", "users", size=190)),
        L("Later, lobbies shrank again, from 60 to 40. And this January, Fall Guys even came to Fortnite, with a mode called Crown Jam.",
          lst([["users", "60 TO 40 PLAYERS"], ["crown", "CROWN JAM IN FORTNITE"]])),
        outro("Have you ever won a crown?", "EVER WON A CROWN?"),
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

# ------------------------------------------------------------------ 67 Brookhaven Part 2 (30 s)
RB.append(dict(num=67, slug="67-brookhaven-part-2", file="67 Brookhaven Part 2 (30s).mp4", target=30, accent="#66bb6a", bpm=122, root=60,
    pron={"Voldex": "Vol-dex"},
    lines=[
        L("Brookhaven is still the number one game on Roblox, and it's not even close.",
          opener("BROOKHAVEN\nPART 2", "STILL #1 ON ROBLOX", "pop8-town.jpg", "A REAL TOWN FROM ABOVE", "Photo: Serg Bataiev, CC0",
                 bg="day", ground="grass", bs=110, ss=48, py=905, ph=400)),
        L("Trackers count over 80 billion visits. Its biggest day came in July 2025, with about 1.2 million people playing at once.",
          S(None, "VISITS (PER TRACKERS)", "gold", "grass", rays="#ffffff", count={"to": 80, "fmt": "{:.0f} BILLION+"}, bs=130, crowd=crowd(), fx=["confetti"])),
        L("When Voldex bought it in February 2025, it had over 120 million players every month.",
          S("120 MILLION", "PLAYERS EVERY MONTH", "mint", "road", bs=124, props=[["house", -2.6, -2.6], ["car", 1.2, -0.6]], av=[av([1.6, 1.4], "wave", "b")])),
        L("That's more people than live in most countries.",
          S("BIGGER THAN\nMOST COUNTRIES", "120M MONTHLY PLAYERS", "sunset", "grass", bs=104, ss=46, ic=[{"n": "globe", "x": 860, "y": 830, "s": 150, "a": "spin"}], crowd=crowd(14, 0.6))),
        end("What's your Brookhaven house like?", "YOUR DREAM\nHOUSE?"),
    ]))

# ------------------------------------------------------------------ 68 Evade (30 s)
RB.append(dict(num=68, slug="68-evade", file="68 Evade (30s).mp4", target=30, accent="#ef5350", bpm=132, root=57, mood="spooky",
    pron={"nextbot": "next bot", "Nextbot": "Next bot"},
    lines=[
        L("In Evade, giant flat memes chase you through the map, and they get louder as they get close.",
          opener("EVADE", "RUN. DON'T LOOK BACK.", "pop8-parkour.jpg", "REAL-LIFE PARKOUR", "Photo: Danhje, public domain",
                 bg="dark", ground="dark", bs=150, vig=False)),
        L("It's based on the nextbot chase games from Garry's Mod. If a teammate goes down, you can run back and revive them.",
          S("REVIVE\nTHEM!", "IF YOU'RE BRAVE", "red", "dark", bc="#ffffff", bs=130, vig=True, fx=["red", "speed"],
            av=[av([-1.0, 0.8], "run", "a", to=[0.2, 0.8]), av([1.2, 1.0], "idle", "g", face="o")])),
        L("It launched in 2022, and one TikTok revive clip got over 8 million views in a week.",
          S("8 MILLION\nVIEWS", "ONE REVIVE CLIP, ONE WEEK", "party", "purple", rays="#ffffff", bs=124, ss=46, ic=[{"n": "tv", "x": 860, "y": 830, "s": 140, "a": "float"}], fx=["sparkle"])),
        L("Trackers now count over 8 billion visits.",
          S(None, "VISITS (PER TRACKERS)", "gold", "stone", rays="#ffffff", count={"to": 8, "fmt": "{:.0f} BILLION+"}, bs=140, crowd=crowd(), fx=["confetti"])),
        end("Do you go back for your teammates?", "GO BACK FOR\nTEAMMATES?", bg="arena"),
    ]))

# ------------------------------------------------------------------ 69 Fish It! (30 s)
RB.append(dict(num=69, slug="69-fish-it", file="69 Fish It (30s).mp4", target=30, accent="#4fc3f7", bpm=118, root=62,
    pron={"Atelier": "Atel-yay"},
    lines=[
        L("Fish It! turned fishing into one of the biggest games on Roblox.",
          opener("FISH IT!", "FISHING, BUT HUGE", "pop8-fishing.jpg", "A REAL FISHERMAN", "Photo: Jeff Attaway, CC BY 2.0",
                 bg="day", ground="wood", bs=150)),
        L("You cast, catch rare fish, upgrade your rod, and unlock new islands.",
          S("CAST.\nCATCH. UPGRADE.", "NEW ISLANDS TO UNLOCK", "mint", "wood", bs=104, ss=46, props=[["island", 0.0, -1.0], ["ship", 1.6, -0.4]], av=[av([-1.4, 1.0], "bob", "b")])),
        L("It was made by a group called Fish Atelier, and launched in October 2024.",
          S("FISH ATELIER", "OCTOBER 2024", "sunset", "wood", bs=130, av=[av([0.4, 0.6], "wave", "a")], ic=[{"n": "calendar", "x": 860, "y": 850, "s": 150, "a": "float"}])),
        L("Trackers count over 4 billion visits, and more than a million people once played at the same time. It's still in the top 15 on Roblox right now.",
          S(None, "VISITS (PER TRACKERS)", "gold", "wood", rays="#ffffff", count={"to": 4, "fmt": "{:.0f} BILLION+"}, bs=140, crowd=crowd(), fx=["confetti"])),
        end("What's your rarest catch?", "RAREST\nCATCH?"),
    ]))

# ------------------------------------------------------------------ 70 Tower Defense Simulator (30 s)
RB.append(dict(num=70, slug="70-tower-defense-simulator", file="70 Tower Defense Simulator (30s).mp4", target=30, accent="#ffca28", bpm=126, root=55,
    pron={"Paradoxum": "Para-dox-um"},
    lines=[
        L("Tower Defense Simulator just hit its biggest crowd ever, almost seven years after it launched.",
          opener("TOWER DEFENSE\nSIMULATOR", "RECORD CROWD, 7 YEARS LATER", "pop8-toysoldiers.jpg", "REAL TOY SOLDIERS", "Photo: Jcbutler, public domain",
                 bg="sunset", ground="stone", bs=100, ss=48, py=905, ph=400)),
        L("You and your team place towers along the path, earn cash every wave, and upgrade until you can take down the boss.",
          S("PLACE.\nUPGRADE. HOLD.", "TAKE DOWN THE BOSS", "arena", "stone", bs=110, props=[["tower", -2.0, -1.6], ["tower", 1.6, -2.2]],
            av=[av([0.0, 1.2], "run", "k", to=[1.4, 1.2], face="mean", s=0.6)], fx=["coins"])),
        L("It's made by Paradoxum Games, and trackers count over 4.6 billion visits.",
          S(None, "VISITS (PER TRACKERS)", "gold", "stone", rays="#ffffff", count={"to": 4.6, "fmt": "{:.1f} BILLION+"}, bs=130, crowd=crowd(), fx=["confetti"])),
        L("This September, trackers say about 104,000 people played at once.",
          S(None, "PLAYERS AT ONCE, SEPT 2026", "party", "purple", rays="#ffffff", count={"to": 104000, "fmt": "{:,.0f}"}, bs=140, crowd=crowd(20, 0.8))),
        end("What's your favorite tower?", "FAVORITE\nTOWER?", bg="arena"),
    ]))

# ------------------------------------------------------------------ 71 Sol's RNG (30 s)
RB.append(dict(num=71, slug="71-sols-rng", file="71 Sol's RNG (30s).mp4", target=30, accent="#b388ff", bpm=120, root=64,
    pron={"RNG": "R N G", "Sol's": "Sol's"},
    lines=[
        L("In Sol's RNG, the whole game is pressing roll, and hoping for luck.",
          opener("SOL'S RNG", "ROLL. PRAY. REPEAT.", "pop8-dice.jpg", "REAL DICE", "Photo: Schlurcher, CC BY 4.0",
                 bg="night", ground="purple", bs=140)),
        L("Every roll gives you an aura, and there are over 200 of them, some so rare most players will never see them.",
          S("200+ AURAS", "SOME YOU'LL NEVER SEE", "party", "purple", rays="#ffffff", bs=140, av=[av([0.0, 0.8], "cheer", "e")], fx=["sparkle"],
            ic=[{"n": "star", "x": 860, "y": 820, "s": 130, "a": "spin"}])),
        L("It's made by Sol's Studio, and trackers count over 1.7 billion visits.",
          S(None, "VISITS (PER TRACKERS)", "gold", "purple", rays="#ffffff", count={"to": 1.7, "fmt": "{:.1f} BILLION+"}, bs=130, crowd=crowd(), fx=["confetti"])),
        L("In April 2026, it hit its biggest crowd yet, about 156,000 players at once.",
          S(None, "PLAYERS AT ONCE, APRIL 2026", "night", "night", count={"to": 156000, "fmt": "{:,.0f}"}, bs=140, crowd=crowd(18, 0.8), fx=["sparkle"])),
        end("What's your rarest aura?", "RAREST\nAURA?"),
    ]))

# ------------------------------------------------------------------ 72 Phantom Forces (70 s)
RB.append(dict(num=72, slug="72-phantom-forces", file="72 Phantom Forces (70s).mp4", target=70, accent="#90a4ae", bpm=128, root=52,
    pron={"litozinnamon": "lito zinnamon", "StyLiS": "Stylis", "Robloxia": "Roblox-ia"},
    lines=[
        L("Phantom Forces is a Roblox shooter so detailed, it was built to feel like Battlefield.",
          opener("PHANTOM\nFORCES", "BATTLEFIELD, ON ROBLOX", "pop8-range.jpg", "REAL RIFLE TRAINING", "Photo: Spc. Ashley Webster, U.S. Army, public domain",
                 bg="sunset", ground="stone", bs=116, ss=48, py=905, ph=400)),
        L("It's made by StyLiS Studios, led by a developer called litozinnamon, who also made Call of Robloxia 5.",
          S("STYLIS\nSTUDIOS", "ALSO MADE CALL OF ROBLOXIA 5", "dark", "stone", bs=124, ss=44, av=[av([0.4, 0.6], "wave", "b")], ic=[{"n": "code", "x": 860, "y": 850, "s": 140, "a": "float"}])),
        L("The game started with a team of just three developers.",
          S("3 DEVS", "THAT'S THE WHOLE TEAM", "mint", "stone", bs=190, av=[av([-1.4, 0.8], "bob", "a"), av([0.0, 0.8], "bob", "b"), av([1.4, 0.8], "bob", "g")])),
        L("Its game page dates back to August 2015, and it's still being updated today.",
          S("SINCE 2015", "STILL GETTING UPDATES", "day", "stone", bs=170, ic=[{"n": "calendar", "x": 860, "y": 850, "s": 150, "a": "float"}], av=[av([0.4, 0.8], "idle", "w", hold="gun")])),
        L("Two teams, the Phantoms and the Ghosts, fight across modes like Team Deathmatch and Capture the Flag.",
          S("PHANTOMS\nVS GHOSTS", "TDM, CAPTURE THE FLAG & MORE", "arena", "stone", bs=124, ss=44,
            av=[av([-1.6, 0.8], "run", "b", to=[-0.6, 0.8], hold="gun"), av([1.6, 0.8], "run", "k", to=[0.6, 0.8], hold="gun", f="y")], fx=["speed"])),
        L("In Team Deathmatch, the first team to 200 kills wins.",
          S(None, "KILLS TO WIN", "red", "stone", bc="#ffffff", count={"to": 200, "fmt": "{:.0f}"}, bs=230, ic=[{"n": "crosshair", "x": 860, "y": 830, "s": 140, "a": "pulse"}])),
        L("You pick one of four classes: Assault, Scout, Support, or Recon.",
          S("4 CLASSES", "ASSAULT, SCOUT, SUPPORT, RECON", "night", "stone", bs=150, ss=42,
            av=[av([-2.0, 0.8], "idle", "a", hold="gun"), av([-0.7, 1.0], "idle", "b", hold="gun"), av([0.7, 1.0], "idle", "g", hold="gun"), av([2.0, 0.8], "idle", "k", hold="gun")])),
        L("And the armory is huge. There are over 200 guns, plus 48 melee weapons.",
          S("200+ GUNS", "+ 48 MELEE WEAPONS", "gold", "stone", rays="#ffffff", bs=170, props=[["crate", -1.8, -1.2], ["crate", 1.0, -2.0]],
            ic=[{"n": "gun", "x": 300, "y": 830, "s": 140, "a": "float"}, {"n": "sword", "x": 820, "y": 830, "s": 140, "a": "float"}])),
        L("Its maps include Desert Storm, Metro, and Crane Site, the very first map.",
          S("CRANE SITE", "THE VERY FIRST MAP", "sunset", "stone", bs=160, props=[["tower", -2.2, -2.0], ["block", 1.2, -1.4]], av=[av([0.4, 1.0], "sneak", "b", hold="gun")])),
        L("Some maps were made for events, like Ruins, built for the Ready Player One event in 2018.",
          S("RUINS", "READY PLAYER ONE EVENT, 2018", "forest", "stone", bs=200, ss=44, props=[["block", -1.8, -1.4], ["block", 1.4, -2.2]], fx=["fireflies"])),
        L("For April Fools 2016, the game renamed itself Aimbot Forces, and sold aimbot for 100 Robux.",
          S("AIMBOT\nFORCES", "APRIL FOOLS, 2016", "party", "purple", rays="#ffffff", bs=130, ic=[{"n": "crosshair", "x": 860, "y": 830, "s": 150, "a": "spin"}], fx=["confetti"])),
        L("Another year, every map was turned upside down.",
          S("UPSIDE\nDOWN", "APRIL FOOLS, 2017", "night", "stone", bs=150, ic=[{"n": "question", "x": 860, "y": 830, "s": 140, "a": "spin"}], av=[av([0.4, 0.8], "jump", "c", face="o")])),
        L("It won three Bloxy Awards, has around 6 million favorites, and trackers count about 1.8 billion visits.",
          S(None, "VISITS (PER TRACKERS)", "gold", "stone", rays="#ffffff", count={"to": 1.8, "fmt": "{:.1f} BILLION"}, bs=130, crowd=crowd(), props=[["trophy", 2.0, -1.8]], fx=["confetti"])),
        end("What's your main class?", "YOUR MAIN\nCLASS?", bg="arena"),
    ]))

# ------------------------------------------------------------------ 73 Roblox stealing games (70 s)
RB.append(dict(num=73, slug="73-stealing-games", file="73 Roblox Stealing Games (70s).mp4", target=70, accent="#ffca28", bpm=124, root=57,
    pron={"Romonitor": "Ro-monitor"},
    lines=[
        L("Why is every big Roblox game about stealing now?",
          opener("STEALING\nGAMES", "WHY IS EVERY HIT ABOUT STEALING?", "pop8-vault.jpg", "A REAL BANK VAULT DOOR", "Photo: Ammodramus, CC0",
                 bg="night", ground="stone", bs=116, ss=44, py=905, ph=400)),
        L("It started with Steal a Brainrot. You buy meme characters, they make money, and anyone can sneak in and steal them.",
          S("STEAL A\nBRAINROT", "WHERE IT STARTED", "party", "purple", rays="#ffffff", bs=124, props=[["base", 0.0, -1.4]],
            av=[av([-2.4, 1.2], "sneak", "k", to=[-0.6, 1.0], face="mean")], fx=["coins"])),
        L("Its creator bought the rights to an older game called Steal a Character, then improved it.",
          S("STEAL A\nCHARACTER", "THE GAME THAT INSPIRED IT", "sunset", "grass", bs=124, ss=44, av=[av([0.4, 0.6], "wave", "b")], ic=[{"n": "license", "x": 860, "y": 850, "s": 150, "a": "float"}])),
        L("As many as 24 million people played at once, and it's earned an estimated 64 million dollars.",
          S("$64 MILLION", "ESTIMATED EARNINGS (ROMONITOR)", "gold", "grass", rays="#ffffff", bs=130, ss=42, crowd=crowd(), fx=["coins"])),
        L("So everyone copied it. Bloomberg reported hundreds of brainrot games flooding Roblox.",
          S("HUNDREDS\nOF COPIES", "PER BLOOMBERG", "red", "stone", bc="#ffffff", bs=124, crowd=crowd(20, 0.5), ic=[{"n": "trade", "x": 860, "y": 820, "s": 140, "a": "spin"}])),
        L("Like Cut Grass for Brainrots, Survive Lava for Brainrots, and Sail for Brainrots.",
          S("___ FOR\nBRAINROTS", "GRASS, LAVA, SAILING...", "mint", "grass", bs=124, props=[["ship", 1.6, -0.6], ["tree", -2.4, -2.0]], av=[av([-0.4, 1.0], "run", "a", to=[0.8, 1.0])])),
        L("The developers fought back, with at least four lawsuits against copycat versions.",
          S("4+ LAWSUITS", "AGAINST COPYCATS", "dark", "stone", bs=150, ic=[{"n": "license", "x": 860, "y": 830, "s": 150, "a": "shake"}], av=[av([0.4, 0.8], "idle", "w", face="mean")])),
        L("Fortnite even removed its brainrot copies. Epic said popular genres are fine, but direct copying is not.",
          S("REMOVED\nFROM FORTNITE", "COPYING IS NOT ALLOWED", "night", "stone", bs=110, ss=44, ic=[{"n": "shield", "x": 860, "y": 830, "s": 150, "a": "pulse"}])),
        L("Then this year came Steal an Egg. You train on treadmills, grab eggs, and run them home before someone steals them.",
          S("STEAL AN\nEGG", "TRAIN. GRAB. RUN.", "day", "grass", bs=124, props=[["base", -2.2, -1.6]],
            av=[av([-0.4, 1.0], "run", "c", to=[1.4, 1.0])], ic=[{"n": "egg_gold", "x": 860, "y": 830, "s": 140, "a": "float"}], fx=["speed"])),
        L("Its treadmills had a giant screen called Reels, playing short videos while you ran.",
          S("REELS", "VIDEOS ON THE TREADMILL", "dark", "stone", bs=210, ic=[{"n": "tv", "x": 860, "y": 820, "s": 160, "a": "flicker"}], av=[av([0.0, 0.8], "run", "a")])),
        L("In August, Roblox made new rules for games that show endless video feeds to kids, and Steal an Egg removed Reels.",
          S("NEW RULES", "NO MORE ENDLESS FEEDS FOR KIDS", "red", "stone", bc="#ffffff", bs=170, ss=42, ic=[{"n": "shield", "x": 860, "y": 830, "s": 150, "a": "pulse"}])),
        L("Even after that, it had nearly 800,000 players at once.",
          S(None, "PLAYERS AT ONCE", "gold", "grass", rays="#ffffff", count={"to": 800000, "fmt": "~{:,.0f}"}, bs=130, crowd=crowd(), fx=["confetti"])),
        end("Stealer, or defender?", "STEALER OR\nDEFENDER?", bg="arena"),
    ]))

# ================================================================== write
ICONS = json.load(open(os.path.join(ROOT, "engine", "modern", "icons.json")))
NAMES = {40: "Plants vs. Zombies", 41: "Tetris", 42: "Fall Guys"}
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
