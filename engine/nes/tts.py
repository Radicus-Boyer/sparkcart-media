"""Voice for the NES preset: Kokoro AI voice (am_michael) with the original year-reading fix
(1989 -> "nineteen eighty-nine"). Episodes can add a "pron" map of word -> spoken form."""
import os
import numpy as np
D = os.path.dirname(os.path.abspath(__file__)) + "/"
_k = None

import re
_ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()
_PLURAL = {"twenty": "twenties", "thirty": "thirties", "forty": "forties", "fifty": "fifties",
           "sixty": "sixties", "seventy": "seventies", "eighty": "eighties", "ninety": "nineties"}

def _two(n):
    if n < 20: return _ONES[n]
    t, o = divmod(n, 10)
    return _TENS[t] + ("" if o == 0 else "-" + _ONES[o])

def year_words(y, plural=False):
    """1989 -> nineteen eighty-nine, 1905 -> nineteen oh five, 2007 -> two thousand seven, 2023 -> twenty twenty-three"""
    hi, lo = divmod(y, 100)
    if 2000 <= y <= 2009:
        w = "two thousand" + ("" if lo == 0 else " " + _ONES[lo])
    elif lo == 0:
        w = _two(hi) + " hundred"
    elif lo < 10:
        w = _two(hi) + " oh " + _ONES[lo]
    else:
        w = _two(hi) + " " + _two(lo)
    if plural:
        last = w.split(" ")[-1]
        w = w[: -len(last)] + _PLURAL.get(last, last + "s")
    return w

def normalize(text):
    # years 1100-2099, not part of a longer number like 8,370 or 1.5
    text = re.sub(r"(?<![\d,.])(1[1-9]\d\d|20\d\d)(s?)(?![\d,]\d)",
                  lambda m: year_words(int(m.group(1)), m.group(2) == "s"), text)
    return text


def say(text, voice="am_michael", speed=1.2, pron=None):
    global _k
    if _k is None:
        from kokoro_onnx import Kokoro
        _k = Kokoro(D + "../models/kokoro.onnx", D + "../models/voices.bin")
    for a, b in (pron or {}).items():
        text = re.sub(r"(?<![\w])" + re.escape(a) + r"(?![\w])", b, text)
    audio, sr = _k.create(normalize(text), voice=voice, speed=speed, lang="en-us")
    return np.asarray(audio, np.float32).ravel()
