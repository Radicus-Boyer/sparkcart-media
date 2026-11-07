"""Long-form #3 (facts checked 2026-11-07): Zoink - from a Bloodbath-to-Zodiac jump to second victor of GRIEF.

Sources: geometrydash.wiki.gg/wiki/Zoink (read Nov 7 2026), Pointercrate Demonlist API (top 15, Nov 7 2026).
Engine: engine/longform.py (16:9). Batch 103 = long-form slot. Clip start times are seconds inside each CUT clip."""
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


ZO, TG, HA, RG = "Zoink", "Toogit", "Hao", "random guy"
clip("lf3-grief", "https://www.youtube.com/watch?v=qUQZg6qd8SY", "*0:00-10:40", 640)   # Toogit: ZOINK BEAT GRIEF full clip
clip("lf3-98", "https://www.youtube.com/watch?v=A-sK7146cK8", "*0:00-0:24", 24)        # Hao: 98% on GRIEF
clip("lf3-zod", "https://www.youtube.com/watch?v=v1Gj1iRg3cY", "*0:00-3:44", 224)      # Zodiac (first list demon)
clip("lf3-slh", "https://www.youtube.com/watch?v=KaA6csT7Zo8", "*0:00-4:06", 246)      # Slaughterhouse first victor
clip("lf3-ach", "https://www.youtube.com/watch?v=sBKR6aUorzA", "*0:00-1:46", 106)      # Acheron verified
clip("lf3-av", "https://www.youtube.com/watch?v=16Zh8jssanc", "*0:00-1:20", 80)        # Avernus
clip("lf3-tod", "https://www.youtube.com/watch?v=LpS4JREhW98", "*0:00-2:18", 138)      # Tunnel of Despair verified
clip("lf3-tw", "https://www.youtube.com/watch?v=9fsZ014qB3s", "*0:00-4:05", 245)       # Tidal Wave verified
clip("lf3-95", "https://www.youtube.com/watch?v=KIWapVa-Bxg", "*0:00-2:48", 168)       # every Tidal Wave 95%
clip("lf3-ts2", "https://www.youtube.com/watch?v=CELNmHwln_c", "*0:00-2:43", 163)      # Thinking Space II verified
clip("lf3-orb", "https://www.youtube.com/watch?v=QKcv8DkNPd0", "*0:00-4:20", 260)      # ORBIT verified
clip("lf3-hel", "https://www.youtube.com/watch?v=gO1nQECPU2I", "*0:00-2:49", 169)      # Heliopolis 85%
clip("lf3-art", "https://www.youtube.com/watch?v=FgjOM0ef1N8", "*0:00-3:19", 199)      # Artemis 13 verified

# ---------------------------------------------------------------- cold open
BEAT(5.0, S("lf3-98", 2, HA))
L("98 percent. On the hardest level in Geometry Dash. Most players would break their keyboard.", S("lf3-98", 8, HA, big="98%", sub="GRIEF - THE NEW TOP 1", bc="#ff5252"))
L("Zoink just kept going. And on November 6th, 2026, he beat it.", S("lf3-grief", 560, TG, big="GRIEF 100%"))
BEAT(5.0, S("lf3-grief", 575, TG))
L("Today he is the number one player on the Demonlist. He has verified seven of the fifteen hardest levels in the game.", S("lf3-art", 150, ZO, big="7 OF THE\nTOP 15"))
L("This is the story of Zoink. How a player nobody knew skipped straight to the top, and stayed there.", S("lf3-tw", 200, ZO))

# ---------------------------------------------------------------- 1
L("Zoink is a player from the United States. He made his YouTube channel in 2018, but his first Geometry Dash video didn't come until December 2020.",
  S("lf3-zod", 10, ZO, chapter="THE JUMP", chn=1))
L("His first video was Cold Sweat, using speed hacks to play the wave part without sliding on the blocks.", S("lf3-zod", 25, ZO, big="COLD SWEAT", sub="DEC 2020"))
L("In March 2021, he verified a remake of Jumper called Bruhmper, on a secret account. That account doesn't even exist anymore.", S("lf3-zod", 30, ZO, big="BRUHMPER"))
L("In 2021, he started posting progress on Sonic Wave. 55 to 94. Then 75 percent.", S("lf3-zod", 40, ZO, big="SONIC WAVE", sub="75%"))
L("Then he tried something almost nobody does. His hardest level was Bloodbath. And he jumped straight to Zodiac.", S("lf3-zod", 70, ZO, big="BLOODBATH\n> ZODIAC"))
L("In June, he got 50 percent on it. Then he kept posting runs, month after month.", S("lf3-zod", 100, ZO, big="50%", sub="ZODIAC - JUNE 2021"))
L("On October 24th, 2021, he beat it. His first list demon was a former number one.", S("lf3-zod", 200, ZO, big="OCT 24, 2021", sub="ZODIAC"))
L("Three days later he beat WOW. In December, Sonic Wave. Nobody climbs that fast.", S("lf3-zod", 150, ZO, big="NOBODY\nCLIMBS THAT FAST"))

# ---------------------------------------------------------------- 2
L("Next, he went for the number one: Slaughterhouse.", S("lf3-slh", 20, ZO, chapter="FIRST VICTOR", chn=2))
L("On January 4th, 2022, he got 51 percent. And in the same month, he beat Cold Sweat, Calculator Core, and Bloodlust. On the side.", S("lf3-slh", 40, ZO, big="51%", sub="+ 3 DEMONS ON THE SIDE"))
L("He played it for four months. He died at 92. Then 93.", S("lf3-slh", 60, ZO, big="92%... 93%"))
BEAT(4.0, S("lf3-slh", 225, ZO))
L("And after 76,004 attempts, Zoink became the first player ever to beat Slaughterhouse.", S("lf3-slh", 232, ZO, big="76,004", sub="FIRST VICTOR - SLAUGHTERHOUSE"))
L("Right after that, he beat Tartarus, the number 4 level at the time, in just 13,909 attempts.", S("lf3-slh", 140, ZO, big="13,909", sub="TARTARUS"))

# ---------------------------------------------------------------- 3
L("Beating levels wasn't enough. Zoink started verifying them, which means beating them first, before anyone else has.", S("lf3-ach", 10, ZO, chapter="THREE TOP 1s", chn=3))
L("On August 23rd, 2022, he verified Acheron, after 72,808 attempts and a fail at 97 percent. It went straight to number one.", S("lf3-ach", 90, ZO, big="ACHERON", sub="72,808 ATTEMPTS"))
L("Along the way, he failed at 96 percent and had to take a break from it. But he came back.", S("lf3-ach", 50, ZO, big="96%"))
L("In January 2023, he passed spaceuk to become the top player on the Demonlist stats viewer. Months later, spaceuk was exposed as a cheater.", S("lf3-av", 10, ZO, big="PASSED\nSPACEUK"), say="In January 2023, he passed Space U K to become the top player on the Demon list stats viewer. Months later, Space U K was exposed as a cheater.")
L("In March, he verified his own buffed version of Avernus, in 27,732 attempts.", S("lf3-av", 60, ZO, big="AVERNUS", sub="27,732 ATTEMPTS"))
L("In April, he became only the second player ever to beat the entire main list, after nSwish.", S("lf3-tod", 20, ZO, big="THE WHOLE\nMAIN LIST"), say="In April, he became only the second player ever to beat the entire main list, after En swish.")
L("He also became the first victor of Deimos, fluking from 78 percent, and later verified the unnerfed version of Yatagarasu.", S("lf3-tod", 70, ZO, big="DEIMOS", sub="FIRST VICTOR"))
L("And in June, he verified Tunnel of Despair in about 12,000 attempts. But he said he was working on a secret project.", S("lf3-tod", 120, ZO, big="SECRET\nPROJECT"))

# ---------------------------------------------------------------- 4
L("The secret was Tidal Wave.", S("lf3-tw", 10, ZO, chapter="TIDAL WAVE", chn=4))
L("He revealed it on July 22nd, 2023, after struggling with it for two weeks.", S("lf3-tw", 30, ZO, big="JULY 22, 2023"))
L("It took him 25,000 attempts just to reach 50 percent. Around 39,000 attempts, he hit 90.", S("lf3-tw", 60, ZO, big="25,000", sub="JUST TO GET 50%"))
L("Then he died at 95 percent. Later, three of the next players to beat it, wPopoff, Trick and Netermind, all died at 95 too. People call it Zoink's curse.",
  S("lf3-95", 20, RG, big="ZOINK'S\nCURSE", sub="95% x4"), say="Then he died at 95 percent. Later, three of the next players to beat it, W Pop off, Trick and Neter-mind, all died at 95 too. People call it Zoink's curse.")
L("94. 93. 92. 91. 25 fails past 73 percent.", S("lf3-95", 90, RG, big="25 FAILS\nPAST 73%"))
BEAT(5.0, S("lf3-tw", 225, ZO))
L("On September 9th, 2023, after 49,534 attempts, Zoink verified Tidal Wave.", S("lf3-tw", 232, ZO, big="49,534", sub="TIDAL WAVE - VERIFIED"))
L("That made him the first player to verify three number one levels in a row.", S("lf3-tw", 160, ZO, big="3 TOP 1s\nIN A ROW"))

# ---------------------------------------------------------------- 5
L("After that, he took a break. In early 2024, he barely played.", S("lf3-ts2", 10, ZO, chapter="THE GRIND", chn=5))
L("Then he came back and verified Nullscapes, after more than 90,000 attempts and six months. He called it his hardest mental challenge.", S("lf3-ts2", 30, ZO, big="NULLSCAPES", sub="90,000+ ATTEMPTS"))
L("He became the first victor of Jigsaw in about 4,400 attempts. And he verified Ashley Wave Trials using a click mod, so it couldn't even be rated until RobTop added that feature to the game.", S("lf3-ts2", 60, ZO, big="CLICK BETWEEN\nFRAMES"))
L("On May 24th, 2025, after 80,000 attempts and 31 streams, he verified Thinking Space 2. It later became number one.", S("lf3-ts2", 140, ZO, big="THINKING\nSPACE II", sub="80,000 ATTEMPTS"))
L("He had 83 attempts that reached the ending. He later posted a compilation of the best moments, over an hour long.", S("lf3-ts2", 120, ZO, big="83 ENDING\nATTEMPTS"))
L("In August, he became the first victor of Amethyst, another future number one. 45,717 attempts.", S("lf3-ts2", 100, ZO, big="AMETHYST", sub="FIRST VICTOR"))
L("In November, he beat Flamewall. Cuatrocientos took 221,703 attempts to verify it. Zoink beat it in 11,745.", S("lf3-ts2", 150, ZO, big="11,745", sub="FLAMEWALL"), say="In November, he beat Flamewall. Kwatro-see-entos took 221,703 attempts to verify it. Zoink beat it in 11,745.")

# ---------------------------------------------------------------- 6
L("Then MindCap, a famous level creator, picked him to verify ORBIT.", S("lf3-orb", 20, ZO, chapter="ORBIT", chn=6), say="Then Mind Cap, a famous level creator, picked him to verify ORBIT.")
L("In January 2026, he almost beat it. His icon fell into the ball pit at the very end.", S("lf3-orb", 120, ZO, big="SO CLOSE"))
L("On February 10th, he verified it. About 30,000 attempts. He even buffed it on the way, from a top 15 level to number 5.", S("lf3-orb", 240, ZO, big="ORBIT", sub="BUFFED TO TOP 5"))
L("In March, he beat BOOBAWAMBA in 7,946 attempts. By far the fewest anyone has ever needed. That meant he had beaten the entire top 25.", S("lf3-orb", 200, ZO, big="7,946", sub="BOOBAWAMBA - WHOLE TOP 25"), say="In March, he beat Boo-ba-wam-ba in 7,946 attempts. By far the fewest anyone has ever needed. That meant he had beaten the entire top 25.")
L("MindCap put a 10,700 dollar bounty on his next level, Heliopolis. Within four days, Zoink could beat it in three runs.", S("lf3-hel", 30, ZO, big="$10,700", sub="BOUNTY - HELIOPOLIS"), say="Mind Cap put a ten thousand seven hundred dollar bounty on his next level, Heliopolis. Within four days, Zoink could beat it in three runs.")
L("A few days later, he did 37 to 100. Basically the whole level in two runs. In 25,581 attempts.", S("lf3-hel", 120, ZO, big="37-100", sub="HELIOPOLIS"))
L("He still found time for fun. He beat a GRIEF parody called GREFG, and a brainrot level called Tung Tung Sahurcles.", S("lf3-hel", 150, ZO, big="TUNG TUNG\nSAHURCLES"))
L("In July, he became the first victor of Society, a number one level. And in September, he verified Artemis 13, which is now number two.", S("lf3-art", 100, ZO, big="ARTEMIS 13", sub="NOW #2"))
L("Artemis 13 was verified before GRIEF, so for a moment in history, it was the hardest level in the game.", S("lf3-art", 160, ZO, big="RETRO\nTOP 1"))

# ---------------------------------------------------------------- 7
L("And then came GRIEF.", S("lf3-grief", 20, TG, chapter="GRIEF", chn=7))
L("Doggie spent two and a half years verifying it. It became the new number one, and every top player started racing to beat it first.", S("lf3-grief", 60, TG, big="THE RACE"))
L("Zoink started playing it on October 7th. On his 10th stream, he got a 21 to 100 run.", S("lf3-grief", 120, TG, big="21-100"))
L("He reached greafer's part three times. 68. 68 again. Then 72.", S("lf3-grief", 150, TG, big="68... 68... 72"))
L("In the next stream, he was the first player in the race to reach GrenadeofTacos's part, at 79 percent.", S("lf3-grief", 170, TG, big="79%"), say="In the next stream, he was the first player in the race to reach Grenade of Tacos's part, at 79 percent.")
L("On November 2nd, he tied his best of 82 percent. That same day, wPopoff beat GRIEF and won the race.", S("lf3-grief", 200, TG, big="WPOPOFF\nWINS"), say="On November second, he tied his best of 82 percent. That same day, W Pop off beat GRIEF and won the race.")
L("Zoink didn't stop. Four days later, he died at 98 percent. In the final monster.", S("lf3-98", 4, HA, big="98%", bc="#ff5252"))
BEAT(5.0, S("lf3-grief", 540, TG))
L("And then, on November 6th, after about 37,000 attempts and 67 hours, Zoink became the second player ever to beat GRIEF.", S("lf3-grief", 560, TG, big="SECOND VICTOR", sub="~37,000 ATTEMPTS - 67 HOURS"))
BEAT(5.0, S("lf3-grief", 580, TG))

# ---------------------------------------------------------------- outro
L("From a Bloodbath to Zodiac jump, to the top player on the Demonlist, with seven of the top fifteen verified.", S("lf3-tw", 238, ZO, big="BLOODBATH TO\nTHE TOP", bs=100))
L("So what do you think? Is Zoink the greatest Geometry Dash player of all time? Tell me in the comments.", S("lf3-grief", 600, TG, big="THE GREATEST\nEVER?", bs=110))
L("And if you liked this story, subscribe. Help a small creator hit 500 subs by Christmas!", S("lf3-art", 190, ZO, big="SUBSCRIBE", sub="HELP US HIT 500 BY CHRISTMAS"))

EP = {"preset": "long", "num": 1003, "slug": "1003-zoink-long", "file": "1003 Zoink - The Best Geometry Dash Player.mp4",
      "title": "Zoink: The Best Geometry Dash Player in the World", "voice": "am_michael", "speed": 1.0,
      "accent": "#2979ff", "mood": "spooky", "music_vol": 0.06, "clip_vol": 0.10,
      "pron": {"Zoink": "Zoynk", "Zoink's": "Zoynks", "Demonlist": "Demon list", "nSwish": "En swish", "wPopoff": "W Pop off", "Netermind": "Neter-mind",
               "MindCap": "Mind Cap", "spaceuk": "space U K", "Nullscapes": "Null scapes", "RobTop": "Rob Top"},
      "lines": LINES}

os.makedirs(os.path.join(ROOT, "episodes", "long"), exist_ok=True)
p = os.path.join("episodes", "long", EP["slug"] + ".json")
json.dump(EP, open(os.path.join(ROOT, p), "w"), indent=1, ensure_ascii=False)
words = sum(len(l.get("say", l["t"]).split()) for l in LINES)
print(len(LINES), "lines", words, "words ~", round(words / 150, 1), "min +", sum(l.get("beat", 0) for l in LINES), "s beats")
json.dump({"batch": 103, "note": "LONG-FORM #3: Zoink (16:9)", "posting": "Z:/claudeprojects/roblox vids/batch-103/posting.txt",
           "episodes": [p], "clips": CLIPS}, open(os.path.join(ROOT, "batches", "batch-103.json"), "w"), indent=1)
print(len(CLIPS), "clips")
