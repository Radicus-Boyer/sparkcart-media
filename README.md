# sparkcart-media

Video engine, episode scripts and public video files for **SparkCart / 8-Bit Backstory** Shorts,
posted to YouTube and TikTok through Postiz.

```
engine/            the renderer (render.py, art.py, music.py, tts.py, fonts/, setup.sh)
episodes/roblox/   episode scripts, Roblox Edition preset (#21-30)
episodes/nes/      episode scripts, NES preset (_sample-skate-or-die.json is the template)
tools/posting.py   posting.txt checker, raw-URL lister, Postiz schedule builder
roblox-edition/    finished MP4s + posting.txt (public links Postiz pulls from)
build/             renders and scratch files (git-ignored)
```

## Quick start (fresh workspace)

```bash
bash engine/setup.sh                                            # ffmpeg, espeak-ng, Python packages, voice model
python3 engine/render.py episodes/nes/_sample-skate-or-die.json --sheet   # contact sheet in build/work/
python3 engine/render.py episodes/roblox/*.json                 # MP4s in build/out/
```

Rendering takes about 1 minute per 30 s video on 2 CPUs. Run two renders in parallel at most.

## Presets

| preset   | look |
|----------|------|
| `roblox` | smooth blocky-3D isometric scenes, studded baseplates, Luckiest Guy / Lilita One fonts, "ROBLOX EDITION" under the header |
| `nes`    | the same scenes rendered as chunky pixel art snapped to the NES colour palette, Press Start 2P pixel font, no edition line |

Both use the Kokoro AI voice (`am_michael`), word-highlighted captions, and an original chiptune
track that ducks under the voice. Videos are 1080x1920, 30 fps.

## Episode format

One JSON file per video.

```jsonc
{
  "preset": "nes",                 // "roblox" or "nes"
  "num": 31,                       // episode number shown in the header
  "slug": "zelda",                 // optional, defaults to the file name
  "file": "31 Zelda (30s).mp4",    // output file name
  "target": 30,                    // target seconds (30 or 60). Voice speeds up (max 1.4x) if the script runs long
  "accent": "#f8b800",             // accent colour for header number, subtitles, VS
  "bpm": 132, "root": 60,          // music tempo and key (MIDI note). "mood": "spooky" for minor/horror
  "edition": "GAME BOY EDITION",   // optional override of the line under the header
  "pron": {"Nikilis": "Nick-ill-iss"},  // optional extra pronunciations for this episode
  "lines": [ { "t": "caption + spoken text", "say": "optional different spoken text", "sc": { ...scene... } } ]
}
```

Writing rules that make the series work: line 1 is a hook, then facts (one idea per line), last line
is a question for the comments. 30 s ≈ 6-8 lines, 60 s ≈ 10-12 lines. Years are spoken correctly
("nineteen eighty-eight"); numbers like 37.2 and 20,000 are read naturally.

### Scene keys (`sc`)

| key | meaning |
|-----|---------|
| `bg` | `day sunset night forest space dark arena party ocean gold mint red` or `split` (needs `vs`) |
| `rays` | colour of rotating sun rays behind the scene, e.g. `"#ffffff"` |
| `ground` | baseplate: `grass sand water dark stone night purple red snow road forest wood space`, `"none"`, or `{"c": "#hex", "w": 8, "d": 8}` |
| `big` | headline text (`\n` for two lines). `bs` size (default 130), `bc` colour, `by` y position (default 400) |
| `sub` | subtitle under the headline. `ss` size, `sc` colour (default accent) |
| `count` | animated counter instead of `big`: `{"to": 14.2, "fmt": "{:.1f} MILLION", "dur": 1.4}` |
| `vs` | `["LEFT", "RIGHT", "#leftbg", "#rightbg"]` with `"bg": "split"` |
| `props` | `[name, x, y, {options}]`. Names: `house tree car treadmill campfire ship island trophy crate base pedestal block tower`. World coordinates run about -4..4 |
| `av` | avatars: `{"p": [x, y], "to": [x, y], "a": "idle/bob/walk/run/sneak/jump/wave/cheer", "c": "a".."h","k","w" or [skin, shirt, pants], "f": "x"/"y" facing, "s": size, "hold": icon, "hat": "#hex", "face": "smile/o/mean", "d": delay}` |
| `pets` | creatures: `{"k": "dog/cat/fox/dragon/deer", "p", "to", "a": "bob/walk/run/hop", "c": "#hex", "s", "rider": avatar colour}` |
| `crowd` | `{"n": 25, "appear": 1.6, "area": [x0, y0, x1, y1], "s": 0.3}` a crowd that pops in |
| `keyboard` | `[x0, y0, cols, rows]` RGB keyboard floor |
| `ic` | 2D sticker icons: `{"n": name, "x", "y" or "w": [x, y, z], "s": size, "a": "float/spin/pulse/fall/fly/shake/flicker", "d": delay, "arg": colour or key letter}` |
| `fx` | list of `speed confetti fireflies sparkle coins waves red` |
| `vig` | dark vignette (true) |
| `bar9` | Common→Divine rarity bar |
| `travel` | seconds for `to` movement (default: whole line) |

Icons: `egg egg_gold egg_blue egg_purple egg_red coin star heart paw fruit sword knife gun scythe trophy
calendar fire alarm question steps clapper crosshair rocket planet key bolt money shield crown moon code
trade license rock bottle eye globe clock cartridge controller tv skateboard arcade`.

Always check a `--sheet` render before the full render: look for text overlapping characters and
props hidden behind each other.

## Posting

1. Put finished MP4s and a `posting.txt` in a folder here (e.g. `nes-batch-2/`), commit and push.
2. `python3 tools/posting.py check <folder>/posting.txt`
3. `python3 tools/posting.py urls <folder>` → give each URL to Postiz `uploadFromUrlTool`, collect the
   returned `path`s into a media JSON (`{"31": "https://uploads.postiz.com/...", ...}`).
4. `python3 tools/posting.py schedule <folder>/posting.txt media.json --start "YYYY-MM-DD HH:MM" --tz America/Toronto --gap 15 40 --independent`
5. Pass `build/sched.json` as `socialPost` to Postiz `integrationSchedulePostTool`, then verify with `postsListTool`.

posting.txt format (blocks separated by a line with only `=====`):

```
FILE: 31 Zelda (30s).mp4
YT TITLE: (max 100 chars, include #Shorts)
YT DESCRIPTION: facts, end question, "8-Bit Backstory #31. New episode every day. Follow for more 8-Bit Backstory!"
YT HASHTAGS: #Shorts ... #8BitBackstory
YT TAGS: comma, separated
TIKTOK TITLE: (max 90 chars)
TIKTOK CAPTION: hook + question + 3-5 hashtags incl. #8BitBackstory
```

All art in these videos is original. No official sprites, logos or gameplay are used.
