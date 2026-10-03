# sparkcart-media

Video engine, episode scripts and public video files for **SparkCart / 8-Bit Backstory** Shorts,
posted to YouTube and TikTok through Postiz.

```
engine/            the renderer: render.py (entry point + Roblox preset), art.py, music.py, tts.py, fonts/, setup.sh
engine/nes/        NES preset = the original 8-Bit Backstory engine (engine.py, lib.py, props2.py, music.py, tts.py)
episodes/nes/      episode scripts #1-20 (NES preset), re-renderable
episodes/roblox/   episode scripts #21-30 (Roblox Edition preset)
engine/modern/     'popular' preset = Most Popular Games of the Internet (engine.py, themes.py, gfx.py, music2.py, fonts/)
episodes/popular/  episode scripts for Most Popular Games of the Internet
episodes/assets/   real images used by photo scenes + CREDITS.txt (licence and source of every image)
popular-batch-1/   finished MP4s + posting.txt, Most Popular Games #1-10
tools/posting.py   posting.txt checker, raw-URL lister, Postiz schedule builder
roblox-edition/    finished MP4s + posting.txt (public links Postiz pulls from)
build/             renders and scratch files (git-ignored)
```

## Quick start (fresh workspace)

```bash
bash engine/setup.sh                                            # ffmpeg, espeak-ng, Python packages, voice model
python3 engine/render.py episodes/nes/01-skate-or-die.json --sheet   # contact sheet in build/work/nes/
python3 engine/render.py episodes/roblox/*.json                 # MP4s in build/out/
```

Rendering takes about 1 minute per 30 s video on 2 CPUs. Run two renders in parallel at most.

## Presets

| preset   | look | engine |
|----------|------|--------|
| `nes`    | the original 8-Bit Backstory look (#1-20): flat side-view pixel scenes on a 180x320 canvas scaled 6x with scanlines, 5x7 pixel font (yellow titles with red shadow), "8-BIT BACKSTORY #N" badge, year tag box, DejaVu Sans Bold captions, black question box + pink "FOLLOW FOR MORE" outro | `engine/nes/engine.py` |
| `roblox` | Roblox Edition (#21-30): smooth blocky-3D isometric scenes, studded baseplates, Luckiest Guy / Lilita One fonts, "ROBLOX EDITION" under the header | `engine/render.py` |

Both use the Kokoro AI voice (`am_michael`), word-highlighted captions, and an original chiptune
track that ducks under the voice. Videos are 1080x1920, 30 fps. `engine/render.py` is the single
entry point; it reads `"preset"` from the episode JSON and hands NES episodes to `engine/nes/engine.py`.

NES cover image (TikTok cover, 1080x1920 PNG in `build/out/covers/`):
`python3 engine/nes/engine.py episodes/nes/13-contra.json cover "THE CODE THAT GAVE YOU 30 LIVES"`

## Popular episode format (Most Popular Games of the Internet)

`"preset": "popular"`. Motion-graphics Shorts with one visual theme per game: fonts, colours, background, panels,
music and a small live counter all change with `theme`. No NES or Roblox look. The header always reads
"MOST POPULAR GAMES / OF THE INTERNET" plus the game name. Captions sit at y=1330 (well above the YouTube and
TikTok title and buttons); the bottom third of the frame is left empty on purpose.

```json
{"preset": "popular", "num": 1, "theme": "cs2", "game": "Counter-Strike 2", "file": "01 - Counter-Strike 2.mp4",
 "target": 70, "pron": {"Minh Le": "Min Lay"},
 "lines": [{"t": "caption and spoken text", "say": "optional different spoken text", "sc": {"kind": "stat", "...": "..."}}]}
```

Themes (in `engine/modern/themes.py`, music in `music2.py`): `cs2` tactical HUD, `dw9` ink and war banners,
`dota` arcane battle map, `pubg` drop-zone map with a shrinking circle, `wardogs` cash and concrete, `oni` ink wash,
`dawn` day/night cycle, `control` brutalist black/red, `wolv` comic book, `witcher` parchment map.
A new game needs a new theme: copy the closest one (static painter, per-frame layer, panel, text roles, caption style)
and add a music style with the same name. Keep all art original and generic: no logos, sprites or known characters.

Scene kinds (`sc.kind`):

| kind | keys |
|------|------|
| `title` / `text` | `big` (list of lines, `*` prefix = accent colour), `icon`, `kicker`, `sub`, `size` |
| `stat` | `val` or `num: [value, "{:,.0f}"]` (counts up), `label`, `sub`, `icon`, `size` |
| `list` | `items: [[icon, text], ...]`, `head` |
| `bars` | `rows: [[label, value, shown text], ...]`, `head` |
| `vs` | `left` and `right`: `[label, value, sub]` |
| `timeline` | `rows: [[year, text], ...]` |
| `quote` | `quote`, `by` |
| `photo` | `img` (file in `episodes/assets/`), `label`, `credit`, `crop: [l, t, r, b]` as fractions, `focus: [x, y]`, `maxh` |
| `outro` | `question` |

Icons are Font Awesome Free solid names (`engine/modern/icons.json`).
Length: about 85 words for 30 s, about 190 words for 70 s. Voice speed starts at 1.12 and rises (max 1.32) if the
script runs over `target`; keep it at 1.20 or lower by trimming text instead.

Real images: every video gets at least one `photo` scene. Use only public-domain, CC0 or CC BY files (Wikimedia
Commons is the easiest source: official publisher trailers uploaded under CC BY, esports event photos, real places
behind the game), put the credit in `credit`, list it in `episodes/assets/CREDITS.txt` and in the YouTube
description. No screenshots or box art without a free licence. The cloud workspace cannot download from
Wikimedia directly; images come in through the browser on the user's linked computer.

## NES episode format

Copy a file from `episodes/nes/` (they are all real, posted episodes) and change it.

```jsonc
{
  "preset": "nes",
  "num": 31, "name": "Zelda II",          // output "31 - Zelda II.mp4" (or set "file")
  "slug": "zelda2",                       // work-file name
  "theme": "grass",                       // default background for every line
  "title_lines": ["ZELDA II"],            // big title on the first scene (1-2 lines)
  "year_tag": "NES 1988",                 // red tag box under the title
  "music": {"bpm": 140, "tr": 0, "seed": 31},   // tempo, transpose (semitones), melody seed
  "speed": 1.2,                           // optional voice speed
  "pron": {"Arakawa": "Ara-kawa"},        // optional pronunciation fixes
  "lines": [
    {"say": "spoken text", "cap": "optional caption text if different (e.g. EA vs E.A.)",
     "scene": {"kind": "title", "prop": "map"}},
    {"say": "...", "scene": {"bg": "space", "head": "1987", "headsc": 4, "headcol": "yel",
                             "prop": "port", "args": {"label": "ZELDA"}, "subs": ["NINTENDO"]}},
    {"say": "Did you beat it? Follow for more 8-Bit Backstory!",
     "scene": {"kind": "outro", "question": "DID YOU BEAT IT?", "prop": "map", "bg": "grass"}}
  ]
}
```

Scene keys: `kind` (`title` first line, `outro` last line, otherwise a card), `bg`, `head` (big pixel
headline), `headsc` (size 2-4, default 3), `headcol`/`subcol` (palette name), `prop` + `args`, `subs`
(1-2 small lines that appear one after another).

Palette names: `blk wht gry lgry dgry red org yel lyel grn lgrn blu lblu cyn pur pnk brn dblu beige tan skin navy mag`.

Backgrounds: `city snow sky space lab grid park stage arcade desk castle jungle prison ring grass moscow planet`, plus `dark`.

Props (with example args):
`computer {"text": "SKATE"}`, `port {"label": "TITLE", "col": "blu"}` (cartridge into console), `limit`,
`list {"items": [...]}`, `joust`, `adventure`, `weapons`, `halfpipe {"sign": "..."}`, `shop {"son": true}`,
`arcade`, `spin`, `bees`, `skier`, `snowballs`, `players`, `notes`, `cloudbush`, `minus`, `crown`,
`sales {"n": 40, "unit": "MILLION+"}`, `swap {"frm": "A", "to": "B", "frmcol": "pnk", "tocol": "red", "at": 2.4}`,
`heights`, `dream`, `curtain`, `film`, `sketch`, `boxart`, `rocknroll`, `robot {"rename": true}`, `mail`,
`difficulty`, `clock`, `bricks`, `ship`, `doh`, `knob`, `tron`, `sprite {"who": "robot", "sc": 6}`,
`blocks {"crash": true}`, `handheld`, `tennis`, `gavel`, `goldcart {"label": "ZELDA"}`, `map`, `battery`,
`dungeon`, `code`, `lives`, `commandos`, `robotswap`, `prisonbreak`, `brawl`, `brothers {"vs": true}`, `toads`,
`tunnel`, `trophy`, `ducks`, `zapper`, `crt`, `laugh {"target": true}`, `boxers {"stats": true}`, `keypad`,
`nameswap {"frm": "A", "to": "B", "at": 2.0}`, `suit`, `password`, `alien`, `metro`, `whip`,
`credits {"names": [...]}`, `monsters {"items": [...]}`, `none`.

Episodes 31+ add (in `engine/nes/props3.py`): backgrounds `moon court underwater graveyard base town`, and props
`photo {"file": "x.png", "label": "..."}` (your own image or clip from `episodes/assets/`, see the README there),
`quote {"text": "...", "col": "yel", "sc": 2}` (typed text box), `bignum {"n": 1.67, "fmt": "{:.2f}", "unit": "MILLION SOLD"}`,
`award {"n": "4TH", "text": "..."}`, `shooter {"options": true}`, `powerbar`, `sneak {"alert": true}`, `parachute`,
`mainframe`, `dam {"rate": 8}`, `squad`, `hoop {"dunk": true}`, `speech {"text": "..."}`, `daynight`,
`villager {"text": "...", "lie": true}`, `graves {"items": [...]}`, `pogo`, `gems {"n": 10000000}`, `team {"n": 3, "label": "..."}`,
`robodog`, `slide`, `mystery {"q": "..."}`, `pad2 {"hot": "R", "text": "SUPER JUMP!"}`, `knight`, `loop {"text": "X2"}`,
`grapple {"nojump": true}`, `magazine {"title": "...", "issue": "...", "line": "..."}`, `crates {"partner": true}`, `citymap`.

The voice is cached between a `--sheet` preview and the full render as long as the script lines don't change.

A new game often needs one new prop: add it to `engine/nes/props3.py` (`extra_prop`) in the same
style: drawn with rectangles on the 180x320 canvas using palette colours, all original art.

## Roblox episode format

One JSON file per video.

```jsonc
{
  "preset": "roblox",              // Roblox Edition preset
  "num": 31,                       // episode number shown in the header
  "slug": "zelda",                 // optional, defaults to the file name
  "file": "31 Zelda (30s).mp4",    // output file name
  "target": 30,                    // target seconds (30 or 60). Voice speeds up (max 1.4x) if the script runs long
  "accent": "#f8b800",             // accent colour for header number, subtitles, VS
  "bpm": 132, "root": 60,          // music tempo and key (MIDI note). "mood": "spooky" for minor/horror
  "edition": "ROBLOX EDITION",     // optional override of the line under the header
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
