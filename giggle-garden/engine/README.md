# Giggle Garden engine
Rebuilt from claude/giggle-garden-video-process.md (sections 3-4).
- `select_song.py songs.json gen_dir whisper_model_dir [ids]` picks the best ACE-Step take, writes gen/<id>_timing.json. `select_song.py dump <mp3> <model>` prints 4 s windows every 2 s for the manual line-start check.
- `make_video.py songs.json gen_dir out_dir id...` renders 1080x1920 30 fps Shorts (loudnorm -14 LUFS for the NeonCity check). `make_video.py sheet songs.json gen_dir out_dir id` makes the contact sheet.
- `engine.py` (drawing, characters, text), `scenes.py` (scene library).
Whisper: sherpa-onnx-whisper-base.en from the k2-fsa GitHub release.
