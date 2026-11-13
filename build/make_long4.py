"""Long-form #4 (facts checked 2026-11-12): The Low Taper Fade meme, start to "still massive".

Sources: knowyourmeme.com (Imagine If Ninja Got a Low Taper Fade; The Low Taper Fade Meme Is Still Massive; Ninja's "Massive";
Tfue High Taper Fade), dailydot.com, Rolling Stone (Jan 19 2024), Wikipedia (Temple fade). Script doc: claude.ai artifact
"The Complete Story of the Low Taper Fade Meme". Clip start times are seconds inside each CUT clip."""
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


ED, NJ, CL = "ericdoa", "Ninja", "clip pages"
clip("lf4-line", "https://www.youtube.com/watch?v=ok5XRYhgH9Q", "*0:00-0:16", 16)       # the line itself
clip("lf4-vod", "https://www.youtube.com/watch?v=jwA9RAvcxuw", "*23:30-27:30", 240)      # ericdoa 2-hour Twitch freestyle (vault re-upload)
clip("lf4-orig", "https://www.youtube.com/watch?v=zloi-MI3DuY", "*0:00-1:42", 102)       # Ninja got a low taper fade, original TikToks
clip("lf4-comp", "https://www.youtube.com/watch?v=jIdbfXDKGNE", "*0:00-2:24", 144)       # Ninja low taper fade compilation
clip("lf4-drag", "https://www.youtube.com/watch?v=ryNMM5pMPr0", "*0:00-0:18", 18)        # Ninja dragging the meme
clip("lf4-dragc", "https://www.youtube.com/watch?v=8-KJdIV3w6Q", "*0:00-6:00", 360)      # dragging edits compilation
clip("lf4-react", "https://www.youtube.com/watch?v=gygzu88OEAs", "*0:00-6:00", 360)      # Ninja reacts to low taper fade memes
clip("lf4-tfue", "https://www.youtube.com/watch?v=JhIcb3jvA94", "*0:00-0:52", 52)        # Ninja reacts to Tfue high taper fade memes
clip("lf4-mass", "https://www.youtube.com/watch?v=gDKDvS4W8k4", "*0:00-0:24", 24)        # "you know what else is massive"
clip("lf4-say", "https://www.youtube.com/watch?v=yqSkmtGQxR0", "*0:00-3:04", 184)        # Ninja saying low taper fade for 3 minutes

# ---------------------------------------------------------------- cold open
BEAT(4.0, S("lf4-line", 0, ED))
L("In January 2024, a singer sang one sentence on a Twitch stream.", S("lf4-vod", 30, ED, big="ONE\nSENTENCE"))
L("Eight days later, one of the biggest streamers on the planet walked into a barbershop because of it.", S("lf4-orig", 10, NJ, big="8 DAYS LATER"))
L("And then the internet did something even weirder. It turned the joke around, and made fun of him for loving it too much.", S("lf4-drag", 2, CL))
BEAT(4.0, S("lf4-drag", 6, CL))
L("So how does a haircut become one of the biggest memes of 2024? It starts somewhere nobody expected. In the middle of a sad song.", S("lf4-vod", 60, ED, big="IT STARTED\nSAD"))

# ---------------------------------------------------------------- 1 origin
L("Meet ericdoa. Real name Eric Lopez, a 21 year old hyperpop artist.", S("lf4-vod", 90, ED, chapter="THE LINE", chn=1), say="Meet Eric D O A. Real name Eric Lopez, a 21 year old hyperpop artist.")
L("On January 5th, 2024, he went live on Twitch and freestyled for about an hour.", S("lf4-vod", 110, ED, big="JAN 5, 2024", sub="TWITCH FREESTYLE"))
L("And this was not a joke stream. Right before the famous line, he was singing about his grandfather passing away.", S("lf4-vod", 140, ED, dark=0.35))
L("The stream was getting heavy. So, to stop himself from getting too emotional, he reached for the funniest thing he could think of.", S("lf4-vod", 170, ED))
L("And what he came up with was this.", S("lf4-vod", 200, ED, big="..."))
BEAT(5.0, S("lf4-line", 0, ED))
L("He later told B R Gaming that was the whole point. A way out of a moment that was getting too sad. Chat lost it.", S("lf4-vod", 215, ED), say="He later told B R Gaming that was the whole point. A way out of a moment that was getting too sad. Chat lost it.")
L("For almost a week, nothing happened. The YouTube upload got about 4,000 views.", S("lf4-vod", 225, ED, big="~4,000 VIEWS", sub="FIRST WEEK"))
L("Then on January 11th, a fan page called ericdoaclips posted just that one moment to TikTok.", S("lf4-line", 2, ED, big="JAN 11"), say="Then on January 11th, a fan page called Eric D O A clips posted just that one moment to TikTok.")
L("1.4 million views in a single day. Over 6 million in under a week.", S("lf4-line", 6, ED, big="1.4 MILLION", sub="IN ONE DAY"))
L("The line was simple. Imagine if Ninja got a low taper fade. Sung twice, like the saddest love song ever written.", S("lf4-line", 10, ED, big="SUNG TWICE"))

# ---------------------------------------------------------------- 2 explosion
L("The same day it blew up, people started doing what the internet does best. Making things up.", S("lf4-comp", 5, CL, chapter="THE EXPLOSION", chn=2))
L("One TikToker told everyone the song was by Frank Ocean. 240,000 people watched that in a day.", S("lf4-comp", 20, CL, big="\"FRANK OCEAN\"", sub="240K VIEWS"))
L("Others made slideshows. Normal photos of Ninja, then a dramatic reveal of a stranger with a fresh fade.", S("lf4-comp", 35, CL))
L("By January 12th it had turned into a prophecy. A Fortnite video showed a wall that said, Ninja with a low taper fade solves all world problems.", S("lf4-comp", 50, CL, big="SOLVES ALL\nWORLD PROBLEMS", sub="679K VIEWS IN A DAY"))
L("Why did it work? It's short. It's sung like a heartfelt ballad, about a haircut. And it asks you to imagine something, so everyone gets to make their own version.", S("lf4-comp", 65, CL))
L("Then the brands showed up. The Brooklyn Nets used the sound. NFL on CBS posted, prophecy fulfilled. Rolling Loud posted, imagine no more.", S("lf4-comp", 80, CL, big="THE BRANDS\nJOINED"))
L("ericdoa's own clip page even posted him reacting to the Brooklyn Nets using his audio.", S("lf4-comp", 95, CL), say="Eric D O A's own clip page even posted him reacting to the Brooklyn Nets using his audio.")
L("By January 19th, Rolling Stone had written a whole article about him, called Meet ericdoa, the reason why Ninja got a low taper fade.", S("lf4-vod", 180, ED, big="ROLLING STONE", sub="JAN 19, 2024"), say="By January 19th, Rolling Stone had written a whole article about him, called Meet Eric D O A, the reason why Ninja got a low taper fade.")
L("But there was one person everybody was waiting on.", S("lf4-orig", 2, NJ, big="NINJA?"))

# ---------------------------------------------------------------- 3 Ninja
L("On January 12th, Ninja posted his first reaction. And the next day, January 13th, he did it.", S("lf4-orig", 8, NJ, chapter="THE PROPHECY", chn=3))
L("He actually got the haircut.", S("lf4-orig", 20, NJ, big="HE DID IT"))
BEAT(5.0, S("lf4-orig", 24, NJ))
L("His reveal, set to ericdoa's sound, got 5.4 million views in three days.", S("lf4-orig", 40, NJ, big="5.4 MILLION", sub="IN 3 DAYS"), say="His reveal, set to Eric D O A's sound, got 5.4 million views in three days.")
L("The internet imagined it. Ninja made it real. Story over, right?", S("lf4-orig", 60, NJ, big="THE END?"))
L("The peak came the week of January 21st. By then it had escaped TikTok and Twitch, and people saw the line everywhere.", S("lf4-comp", 110, CL, big="PEAK WEEK", sub="JAN 21-27"))
L("Not even close. Because Ninja kept talking about it. On stream. Over and over.", S("lf4-say", 20, NJ))
BEAT(5.0, S("lf4-say", 40, NJ))

# ---------------------------------------------------------------- 4 still massive
L("January 30th. Only 17 days after the haircut. A TikToker posted a clip from Ninja's stream with one caption.", S("lf4-drag", 0, CL, chapter="STILL MASSIVE", chn=4))
L("Ninja is dragging the low taper fade at this point.", S("lf4-drag", 4, CL, big="\"NINJA IS DRAGGING\nTHE LOW TAPER FADE\""))
L("In the clip, Ninja sings low taper fade, and then says this. You know what's crazy? Is that that low taper fade meme is like, dude, it is still massive.", S("lf4-drag", 6, CL, big="\"IT IS STILL\nMASSIVE\""))
BEAT(6.0, S("lf4-drag", 8, CL))
L("And that's the funniest part of the whole story. The meme was a joke about Ninja. Then Ninja loved it so much that loving it became the new joke.", S("lf4-dragc", 20, CL, big="THE JOKE\nFLIPPED"))
L("That clip pulled about 4.3 million plays.", S("lf4-dragc", 40, CL, big="4.3 MILLION"))
L("TikTok ran with it. Edits showed Ninja still dragging the meme years in the future. As a baby. As different animals, in different lifetimes.", S("lf4-dragc", 70, CL, big="DIFFERENT\nLIFETIMES"))
L("People made AI voice versions of the whole speech.", S("lf4-dragc", 110, CL))
L("One edit even showed Ninja passing the haircut on to his pet bird.", S("lf4-dragc", 125, CL, big="EVEN\nTHE BIRD"))
BEAT(5.0, S("lf4-dragc", 140, CL))
L("And Ninja watched them. He even reacted to compilations of people making fun of him for it.", S("lf4-react", 60, NJ, big="NINJA\nREACTS"))
BEAT(5.0, S("lf4-react", 90, NJ))

# ---------------------------------------------------------------- 5 out of control
L("In June, someone tried to start a new one. Imagine if Tfue got a high taper fade.", S("lf4-tfue", 2, CL, chapter="OUT OF CONTROL", chn=5))
L("It flopped. For four months. Then in October, a video saying Tfue was dragging the high taper fade got 2.3 million views in two days.", S("lf4-tfue", 12, CL, big="2.3 MILLION", sub="TFUE HIGH TAPER FADE"))
L("A fake meme, about a fake meme, about a real meme.", S("lf4-tfue", 22, CL, big="A FAKE MEME\nABOUT A FAKE MEME"))
L("Then the word itself broke free.", S("lf4-mass", 0, CL, big="MASSIVE"))
BEAT(4.0, S("lf4-mass", 4, CL))
L("A you know what else is massive edit in November got 5.7 million views and 872,000 likes in two months.", S("lf4-mass", 10, CL, big="5.7 MILLION", sub="NOV 2024"))
L("By January 2025 there was a parody song, a locked in Ninja remix, and a fan art trend of cartoon characters giving each other low taper fades.", S("lf4-dragc", 200, CL, big="IT NEVER\nENDED"))
L("Starting in February 2024, artists redrew characters from games, anime and cartoons in a barbershop, giving and getting low taper fades. Nobody was safe.", S("lf4-comp", 130, CL, big="NOBODY\nWAS SAFE"))

# ---------------------------------------------------------------- 6 legacy
L("So why did this one stick, when most memes die in a week? Because it had three lives.", S("lf4-comp", 100, CL, chapter="THE LEGACY", chn=6))
L("A sincere line, sung in a sad moment. A creator who actually did what the internet asked. And a creator who loved it so much, he became the next joke.", S("lf4-orig", 70, NJ, big="3 LIVES"))
L("For ericdoa, it followed him everywhere. He's said that no matter what he posts, the comments say the same thing.", S("lf4-vod", 235, ED, big="IMAGINE IF..."), say="For Eric D O A, it followed him everywhere. He's said that no matter what he posts, the comments say the same thing.")
L("And for Ninja, it became part of who he is online. Not just the Fortnite guy. The low taper fade guy.", S("lf4-orig", 90, NJ, big="THE LOW\nTAPER FADE GUY"))
L("And the strangest part? Even this video is proof. Because, you know what's crazy?", S("lf4-say", 100, NJ))
BEAT(4.0, S("lf4-drag", 8, CL))
L("Which meme do you think is still massive? Tell me in the comments.", S("lf4-comp", 120, CL, big="STILL\nMASSIVE?", bs=110))
L("And if you liked this story, subscribe. Help a small creator hit 500 subs by Christmas!", S("lf4-line", 8, ED, big="SUBSCRIBE", sub="HELP US HIT 500 BY CHRISTMAS"))

EP = {"preset": "long", "num": 1004, "slug": "1004-low-taper-fade-long", "file": "1004 The Low Taper Fade Meme - The Complete Story.mp4",
      "title": "The Low Taper Fade Meme Is Still MASSIVE: The Complete Story", "voice": "am_michael", "speed": 1.02,
      "accent": "#ffb300", "mood": "happy", "music_vol": 0.06, "clip_vol": 0.10,
      "pron": {"ericdoa": "Eric D O A", "ericdoa's": "Eric D O A's", "Tfue": "Tee-fyoo", "Blevins": "Bleh-vins"},
      "lines": LINES}

os.makedirs(os.path.join(ROOT, "episodes", "long"), exist_ok=True)
p = os.path.join("episodes", "long", EP["slug"] + ".json")
json.dump(EP, open(os.path.join(ROOT, p), "w"), indent=1, ensure_ascii=False)
words = sum(len(l.get("say", l["t"]).split()) for l in LINES)
print(len(LINES), "lines", words, "words ~", round(words / 150, 1), "min +", sum(l.get("beat", 0) for l in LINES), "s beats")
json.dump({"batch": 104, "note": "LONG-FORM #4: Low Taper Fade (16:9)", "posting": "Z:/claudeprojects/roblox vids/batch-104/posting.txt",
           "episodes": [p], "clips": CLIPS}, open(os.path.join(ROOT, "batches", "batch-104.json"), "w"), indent=1)
print(len(CLIPS), "clips")
