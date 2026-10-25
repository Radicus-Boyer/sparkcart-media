# SparkCart Studio

Windows control panel for the Shorts pipeline. Everything runs on your PC; scripts come from Claude in chat.

**Install:** run `SparkCart-Studio-Install.bat` once (installs Python, Git, ffmpeg, voice model, yt-dlp).
**Run:** double-click `app\SparkCart Studio.bat`.

Tabs: **Home** (one button for Docker + Postiz + ngrok, status lights, Update), **Batches** (get clips, render, save, schedule),
**New batch** (builds the request text you paste into chat), **Settings** (Postiz API key, folders, timezone).

## Batch manifest (written by Claude): `batches/batch-N.json`
```json
{"batch": 21, "note": "...", "posting": "batch-21/posting.txt",
 "episodes": ["episodes/roblox/181-name.json"],
 "clips": [{"name": "rb21-foo", "url": "https://youtube.com/watch?v=...", "backup": ["..."],
            "section": "*0:30-1:10", "cut": 5, "len": 13}]}
```
Get clips downloads each `section` with yt-dlp, cuts `len` seconds starting `cut` seconds in, copies it into `episodes/assets/`, then renders.
Clips are temporary: "Delete clips" removes them after the batch is rendered.

Postiz needs the API key (Postiz > Settings > Developers > Public API) saved in Settings.
