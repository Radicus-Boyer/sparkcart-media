"""Long-form #1 (facts checked 2026-11-03): GRIEF, the #1 level - Doggie's 436,879 attempts and two 97% deaths.

Sources: geometrydash.wiki.gg/wiki/GRIEF + /wiki/Doggie, Doggie's verification video description (gB8slBPlOjc),
spilled.gg (Oct 5 + Sep 21 2026), Dexerto. Engine: engine/longform.py (16:9). Batch 101 = long-form slot.
Clip start times are seconds inside each CUT clip (the cut begins at the section start)."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIPS, LINES = [], []


def clip(name, url, section, ln):
    CLIPS.append({"name": name, "url": url, "backup": [], "section": section, "cut": 0, "len": ln, "w": 1920})


def S(c, start, credit, **k):
    return dict(clip=c + ".mp4", start=start, credit=credit, **k)


def L(t, sc, say=None):
    d = {"t": t, "sc": sc}
    if say:
        d["say"] = say
    LINES.append(d)


def BEAT(sec, sc):
    LINES.append({"t": "", "beat": sec, "sc": sc})


DG, IC, WP = "Doggie", "icedcave", "wPopoff"
clip("lf-97a", "https://www.youtube.com/watch?v=Emd2tWP2FkI", "*1:20-3:54", 154)   # 97% #1 (death ~44s in cut)
clip("lf-97b", "https://www.youtube.com/watch?v=_nv9UsomBi0", "*1:30-4:02", 152)   # 97% #2 (death ~37s in cut)
clip("lf-ver", "https://www.youtube.com/watch?v=gB8slBPlOjc", "*0:00-8:40", 520)   # verification
clip("lf-show", "https://www.youtube.com/watch?v=Wd0DIyujh2g", "*0:00-5:49", 349)  # official showcase
clip("lf-2023", "https://www.youtube.com/watch?v=bQXnREyaO34", "*0:00-2:55", 175)  # icedcave 2023 full
clip("lf-sh", "https://www.youtube.com/watch?v=kpcF1-QAHQc", "*0:00-2:27", 147)    # Doggie Slaughterhouse
clip("lf-osh", "https://www.youtube.com/watch?v=7W5bZJY2IPI", "*0:00-1:23", 83)    # icedcave Slaughterhouse
clip("lf-pr1", "https://www.youtube.com/watch?v=BEXg8TGfNPM", "*0:40-3:40", 180)   # progress report #1 (May 2024)
clip("lf-80", "https://www.youtube.com/watch?v=5gx07ZNiuJY", "*0:00-2:53", 173)
clip("lf-83", "https://www.youtube.com/watch?v=mp8TSHLoW8Q", "*0:00-3:03", 183)    # new best peak ~132s
clip("lf-84", "https://www.youtube.com/watch?v=VLqlssP1Dxw", "*0:00-2:45", 165)    # peak ~140s
clip("lf-hb", "https://www.youtube.com/watch?v=SI6OSbCWgrU", "*0:00-2:51", 171)    # hitboxes
clip("lf-cbf", "https://www.youtube.com/watch?v=cwE1-29-530", "*0:00-2:52", 172)   # GRIEF with clicks
clip("lf-wp", "https://www.youtube.com/watch?v=WhP4bRHTR8A", "*0:00-5:56", 356)    # wPopoff first victor
clip("lf-dr", "https://www.youtube.com/watch?v=0_e46M1PwwU", "*0:00-8:06", 486)    # Doggie reacts to wPopoff
clip("lf-ice", "https://www.youtube.com/watch?v=o6QLrB87jiU", "*0:00-3:24", 204)   # icedcave verified upload

# ---------------------------------------------------------------- cold open
BEAT(8.0, S("lf-97a", 79, DG))
L("Four hundred thirty-six thousand, eight hundred and seventy-nine attempts.", S("lf-ver", 329, DG, big="436,879", sub="ATTEMPTS"))
L("Over nine hundred hours of streams. Almost two and a half years of one player's life.", S("lf-ver", 100, DG, big="900+ HOURS"))
L("And twice, he made it to ninety-seven percent... and died.", S("lf-97b", 70, DG, big="97%", sub="TWICE", bc="#ff5252"))
L("This is the story of GRIEF, the hardest level in Geometry Dash, and Doggie, the player who refused to quit.", S("lf-show", 0, DG))
L("But to understand GRIEF, we have to go back to a level called Slaughterhouse.", S("lf-osh", 28, IC))

# ---------------------------------------------------------------- 1
L("In 2015, a creator named icedcave made an impossible level called Slaughterhouse. It was never meant to be beaten.",
  S("lf-osh", 36, IC, chapter="THE LEVEL THAT\nSTARTED IT ALL", chn=1))
L("Years later, icedcave hosted a real, beatable version. In December 2021, after 79,170 attempts, Doggie beat it, and it was the number one hardest level in the game.",
  S("lf-sh", 82, DG, big="79,170", sub="ATTEMPTS ON SLAUGHTERHOUSE"))
L("Another player had claimed to verify it first, but that run was later exposed as hacked. So Doggie's run is the one that counts.", S("lf-sh", 108, DG))
L("Right around then, icedcave had a new idea. A prequel to Slaughterhouse. His final attempt at bringing the level that made his name back to life. He called it GRIEF.",
  S("lf-2023", 8, IC, big="GRIEF"))
L("Doggie had always wanted to verify the hardest level in the game. When he saw GRIEF, he knew this was the one. He asked icedcave if he could verify it, and icedcave said yes.",
  S("lf-2023", 40, IC))
L("Quick explainer: before a level goes public, someone has to prove it's possible, by beating it from zero to one hundred in a single run. That's called verifying. And the creators usually can't do it themselves.",
  S("lf-show", 60, DG, big="VERIFYING", sub="0% TO 100% IN ONE RUN"))

# ---------------------------------------------------------------- 2
L("The layout was finished in April 2022, and a lot of people hated it.", S("lf-hb", 10, DG, chapter="BUILDING\nA MONSTER", chn=2))
L("Fourteen creators worked on the level. The decoration alone took sixteen months.", S("lf-show", 90, DG, big="14 CREATORS", sub="16 MONTHS OF DECORATION"))
L("In August 2023, it was finally shown off. Then the drama hit. One creator's part got replaced, there was a fight, and icedcave cancelled the whole level.",
  S("lf-2023", 75, IC, big="CANCELLED", bc="#ff5252"))
L("He brought it back. But then Doggie accidentally showed a link to the level file on stream, and an early version leaked to the public.", S("lf-2023", 110, IC, big="LEAKED"))
L("And then came the biggest problem of all. Update two point two.", S("lf-2023", 140, IC))

# ---------------------------------------------------------------- 3
L("Update 2.2 changed how the game reads your clicks. Inputs got checked at most 240 times a second.",
  S("lf-pr1", 27, DG, chapter="THE CLICK\nPROBLEM", chn=3), say="Update two point two changed how the game reads your clicks. Inputs got checked at most two hundred forty times a second.")
L("Doggie hated it. He told icedcave, straight up, that GRIEF was not being verified on 2.2 physics. The verification went on hold.",
  S("lf-pr1", 35, DG), say="Doggie hated it. He told iced cave, straight up, that GRIEF was not being verified on two point two physics. The verification went on hold.")
L("In April 2024, a mod called Click Between Frames came out. It registers your click at the exact moment you press, not on the next frame. Doggie chose to verify with it, and the community argued about it for months.",
  S("lf-pr1", 40, DG))
L("Then, in January 2026, RobTop added Click Between Frames to the real game. Argument over.", S("lf-cbf", 158, "Cast", big="ADDED TO\nTHE GAME", bs=100),
  say="Then, in January 2026, Rob Top added Click Between Frames to the real game. Argument over.")

# ---------------------------------------------------------------- 4
L("May 1st, 2024. Stream one. Doggie starts grinding GRIEF, live.", S("lf-pr1", 72, DG, chapter="STREAM ONE", chn=4))
L("GRIEF is almost three minutes long. That's huge for a top level. Every attempt is a three-minute test, where one mistake sends you back to zero.",
  S("lf-show", 140, DG, big="2:46", sub="ONE MISTAKE = BACK TO 0%"), say="GRIEF is almost three minutes long. That's huge for a top level. Every attempt is a three minute test, where one mistake sends you back to zero.")
L("By the end of the first month, he could already beat it in three pieces. Zero to 27. 25 to 66. And 65 to 100.",
  S("lf-pr1", 62, DG))
L("By November 2024, just six months in, he hit 80 percent. It looked like GRIEF would be done by Christmas.", S("lf-80", 124, DG, big="80%", sub="NOVEMBER 2024"))
L("It was not done by Christmas.", S("lf-80", 137, DG))

# ---------------------------------------------------------------- 5
L("The reason has a name. Greafer. It's the part from 65 to 75 percent, named after the creator who built it.", S("lf-hb", 110, DG, chapter="GREAFER", chn=5))
L("It's only ten seconds long. But it's a wave section at four times speed, up to eight clicks per second, and you can barely see where you're going. With two full minutes of the level already behind you.",
  S("lf-show", 111, DG, big="4X SPEED", sub="UP TO 8 CLICKS PER SECOND"))
L("Doggie died in this part over sixty times before he ever got past 80 percent.", S("lf-hb", 118, DG, big="60+ DEATHS"))
L("And then something worse set in. A mindblock. When you fail the same spot over and over, it stops being your hands. It's your head.", S("lf-80", 142, DG, big="MINDBLOCK", dark=0.15))
L("For most of 2025, he was stuck. In his own words, it became a question of if he could beat GRIEF, not when.", S("lf-80", 152, DG))
L("Then, on November 1st, 2025, after 342 days without a single new best...", S("lf-83", 112, DG, big="342 DAYS", sub="WITHOUT A NEW BEST"))
BEAT(9.0, S("lf-83", 131, DG))
L("83 percent. Just three more percent, but he said it almost felt like verifying a new top one.", S("lf-83", 141, DG, big="83%", bc="#69f0ae"))

# ---------------------------------------------------------------- 6
L("But there was one more wall. A three-second wave part right after it, called Tacos, named after its creator, GrenadeofTacos.",
  S("lf-show", 129, DG, chapter="TACOS", chn=6), say="But there was one more wall. A three second wave part right after it, called Tacos, named after its creator, Grenade of Tacos.")
L("That part is why it took six more months to get 84 percent, in May 2026.", S("lf-84", 119, DG, big="84%", sub="MAY 2026"))
BEAT(9.0, S("lf-84", 133, DG))
L("Now, finally, he could handle Greafer and Tacos from zero. The path to the end was clear. For real this time.", S("lf-show", 140, DG))

# ---------------------------------------------------------------- 7
L("June 14th, 2026. Stream 361. For the first time ever, Doggie gets through Tacos from zero.", S("lf-97a", 50, DG, chapter="NINETY-SEVEN", chn=7))
L("90 percent. 95. 96...", S("lf-97a", 69, DG, nocap=True), say="Ninety percent. Ninety five. Ninety six.")
BEAT(9.0, S("lf-97a", 78, DG))
L("97 percent. Three percent away from beating the hardest level in the game. And it's back to zero.", S("lf-97a", 88, DG, big="97%", bc="#ff5252"))
L("He uploaded the clip with one line in the description: the end is here.", S("lf-97a", 100, DG, big="\"the end is here.\"", bs=90))
L("Three months later. September 21st. Stream 390.", S("lf-97b", 48, DG, big="STREAM 390"))
BEAT(9.0, S("lf-97b", 68, DG))
L("97. Again. And in the same stream, he got a 91.", S("lf-97b", 79, DG, big="97% x2", bc="#ff5252"))
L("To show how rare these runs were: most attempts died in the first ten percent. In over four hundred thousand tries, he'd passed 75 percent only about forty times.",
  S("lf-show", 30, DG, big="~40 RUNS", sub="PAST 75% IN 400,000+ TRIES"))
L("But everyone could feel it. GRIEF was finally close.", S("lf-97b", 104, DG))

# ---------------------------------------------------------------- 8
L("October 4th, 2026. Stream 396. Attempt 436,879.", S("lf-ver", 30, DG, chapter="THE RUN", chn=8))
L("Greafer. Passed. Tacos. Passed.", S("lf-ver", 163, DG, nocap=True))
BEAT(14.0, S("lf-ver", 186, DG))
L("GRIEF. Verified. At nine fifty-one PM, with somewhere between forty and fifty thousand people watching live.", S("lf-ver", 214, DG, big="VERIFIED", bc="#69f0ae"),
  say="GRIEF. Verified. At nine fifty one PM, with somewhere between forty and fifty thousand people watching live.")
L("The verification video hit one million views in seven hours. So many people tried to download the level that players reported the servers going down.",
  S("lf-ice", 30, IC, big="1,000,000 VIEWS", sub="IN 7 HOURS"))
L("GRIEF went straight to number one on the Demonlist, replacing Society. It's the longest verification of any number one level, ever.",
  S("lf-ice", 70, IC, big="#1", sub="DEMONLIST"), say="GRIEF went straight to number one on the Demon list, replacing Society. It's the longest verification of any number one level, ever.")
L("Doggie wrote that GRIEF is the hardest thing he will ever do, and told anyone chasing something to never give up on their dreams.", S("lf-ver", 452, DG))

# ---------------------------------------------------------------- 9
L("Now the level is public, and the best players in the world are racing to beat it next.", S("lf-wp", 7, WP, chapter="THE FIRST\nVICTOR", chn=9))
L("And on November 2nd, wPopoff did it. The first victor, in 30,747 attempts.", S("lf-wp", 120, WP, big="30,747", sub="ATTEMPTS"),
  say="And on November second, W Pop off did it. The first victor, in 30,747 attempts.")
BEAT(10.0, S("lf-wp", 159, WP))
L("That's about fourteen times fewer attempts than Doggie. But that's how verifying works. The verifier has to figure out every part with no proof it's even possible. Everyone after him already knows it is.",
  S("lf-show", 60, DG, big="14x FEWER"))
L("And Doggie was watching, reacting live as someone else finished the level he gave two and a half years to.", S("lf-dr", 48, "MYKE [GD] / " + DG))
L("Players like Zoink are already at 82 percent. The race for second victor is on.", S("lf-show", 147, DG, big="NEXT?"),
  say="Players like Zoynk are already at eighty two percent. The race for second victor is on.")

# ---------------------------------------------------------------- outro
L("436,879 attempts. Two 97s. One perfect run.", S("lf-ver", 330, DG, big="436,879", sub="TWO 97s. ONE RUN."),
  say="Four hundred thirty-six thousand, eight hundred seventy-nine attempts. Two ninety-sevens. One perfect run.")
L("So be honest. Would you have kept going after the second 97? Tell me in the comments.", S("lf-97b", 70, DG, big="WOULD YOU\nKEEP GOING?", bs=110),
  say="So be honest. Would you have kept going after the second ninety-seven? Tell me in the comments.")
L("And if you liked this story, subscribe. Help a small creator hit 500 subs by Christmas!", S("lf-show", 158, DG, big="SUBSCRIBE", sub="HELP US HIT 500 BY CHRISTMAS"))

EP = {"preset": "long", "num": 1001, "slug": "1001-grief-long", "file": "1001 GRIEF - The Hardest Level in Geometry Dash.mp4",
      "title": "GRIEF: The 436,879-Attempt Story of Geometry Dash's Hardest Level", "voice": "am_michael", "speed": 1.0,
      "accent": "#ff5252", "mood": "spooky", "music_vol": 0.06, "clip_vol": 0.10,
      "pron": {"icedcave": "iced cave", "Greafer": "Gree-fer", "Doggie's": "Doggie's", "GRIEF": "Grief", "Demonlist": "Demon list",
               "wPopoff": "W Pop off", "Zoink": "Zoynk", "RobTop": "Rob Top"},
      "lines": LINES}

os.makedirs(os.path.join(ROOT, "episodes", "long"), exist_ok=True)
p = os.path.join("episodes", "long", EP["slug"] + ".json")
json.dump(EP, open(os.path.join(ROOT, p), "w"), indent=1, ensure_ascii=False)
words = sum(len(l.get("say", l["t"]).split()) for l in LINES)
print(len(LINES), "lines", words, "words ~", round(words / 150, 1), "min +", sum(l.get("beat", 0) for l in LINES), "s beats")
json.dump({"batch": 101, "note": "LONG-FORM #1: GRIEF (16:9)", "posting": "Z:/claudeprojects/roblox vids/batch-101/posting.txt",
           "episodes": [p], "clips": CLIPS}, open(os.path.join(ROOT, "batches", "batch-101.json"), "w"), indent=1)
print(len(CLIPS), "clips")
