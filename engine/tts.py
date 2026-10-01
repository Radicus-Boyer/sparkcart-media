"""Kokoro voice + text normalizer (years read as 'twenty twenty-six').
PRON = global pronunciation fixes; episodes can add their own with a "pron" map."""
import re, os
import numpy as np
from num2words import num2words

D = os.path.dirname(os.path.abspath(__file__)) + "/"
_k = None

PRON = {
    "+1": "plus one", "RIVALS": "Rivals", "ASMR": "A.S.M.R.", "NATO": "Nay-toe",
    "Wolfpaq": "Wolfpack", "Aidanleewolf": "Aidan Lee Wolf", "Voldex": "Vol-dex",
    "Ouw": "Ow", "Nosniy": "Noz-nee", "mygame43": "my game forty-three", "rip_indra": "rip indra",
    "NewFissy": "New Fissy", "Bethink": "Bee-think", "SecretVerse": "Secret Verse",
    "Nikilis": "Nick-ill-iss", "Nik's": "Nick's", "RP": "R.P.", "Blox": "Blocks", "Favourite": "Favorite",
    "collab": "collab", "Uplift": "Up-lift",
}


def normalize(t, extra=None):
    for a, b in {**PRON, **(extra or {})}.items():
        t = re.sub(r"(?<![\w])" + re.escape(a) + r"(?![\w])", b, t)
    t = re.sub(r"\d{1,3}(?:,\d{3})+", lambda m: num2words(int(m.group().replace(",", ""))), t)
    t = re.sub(r"\b(\d+)\.(\d+)\b", lambda m: num2words(float(m.group())), t)
    t = re.sub(r"\b(\d+)(st|nd|rd|th)\b", lambda m: num2words(int(m.group(1)), to="ordinal"), t)

    def num(m):
        n = int(m.group())
        if 1900 <= n <= 2099:
            return num2words(n, to="year")
        return num2words(n)
    t = re.sub(r"\b\d+\b", num, t)
    return t


def say(text, voice="am_michael", speed=1.15, extra=None):
    global _k
    if _k is None:
        from kokoro_onnx import Kokoro
        _k = Kokoro(D + "models/kokoro.onnx", D + "models/voices.bin")
    a, sr = _k.create(normalize(text, extra), voice=voice, speed=speed, lang="en-us")
    a = np.asarray(a, np.float32)
    idx = np.where(np.abs(a) > 0.012)[0]
    if len(idx):
        a = a[max(idx[0] - 240, 0): idx[-1] + 720]
    return a, sr


if __name__ == "__main__":
    for s in ["Ride A Pet came out in April 2026.", "The first game got 678 million visits.",
              "It struggled to pass 20,000 players at once.", "launched on September 18th, 2026",
              "At its peak, 14.2 million people", "+1 Speed Keyboard Escape", "20th Century Studios"]:
        print(normalize(s))
