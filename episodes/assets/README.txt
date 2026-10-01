Drop your own images or short clips here (PNG, JPG, MP4, MOV, GIF) to show them inside an NES-preset scene.

In the episode JSON, use the "photo" prop on any line:

  {"say": "...", "scene": {"bg": "dark", "head": "THE BOX ART", "prop": "photo",
                           "args": {"file": "my-clip.mp4", "label": "OPTIONAL CAPTION"}}}

- Images are fitted inside a gold-framed box in the middle of the screen (full resolution, not pixelated).
- Clips play from the start for up to 8 seconds and loop; no sound is used.
- If the file is missing, the scene shows "ADD IMAGE: <name>" so you can see where it will go.
- Only add media you made yourself or have the rights to use.
