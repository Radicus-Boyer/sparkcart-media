"""Real Geometry Dash player icons (cube / ship / wave ...) from GDBrowser, cached in episodes/assets as
gdicon-<player>-<form>.png. Fetched on first use (the PC has internet; the cloud box may not, then we fall back)."""
import json, os, urllib.parse, urllib.request

ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "episodes", "assets")
UA = {"User-Agent": "Mozilla/5.0 (SparkCart Studio)"}
_failed = set()


def path(player, form="cube"):
    return os.path.join(ASSETS, f"gdicon-{player.lower().replace(' ', '_')}-{form}.png")


def get(player, form="cube"):
    """Local PNG path for this player's icon in this form, downloading it if needed; None if unavailable."""
    p = path(player, form)
    if os.path.exists(p):
        return p
    if (player, form) in _failed:
        return None
    try:
        req = urllib.request.Request("https://gdbrowser.com/api/profile/" + urllib.parse.quote(player), headers=UA)
        prof = json.load(urllib.request.urlopen(req, timeout=15))
        icon_id = prof["icon"] if form == "cube" else prof[form]
        q = urllib.parse.urlencode({"form": form, "icon": icon_id, "col1": prof["col1"], "col2": prof["col2"],
                                    "glow": 1 if prof.get("glow") else 0, "size": "auto"})
        req = urllib.request.Request("https://gdbrowser.com/icon/icon?" + q, headers=UA)
        data = urllib.request.urlopen(req, timeout=15).read()
        if data[:4] != b"\x89PNG":
            raise ValueError("not a png")
        os.makedirs(ASSETS, exist_ok=True)
        open(p, "wb").write(data)
        print(f"  fetched GD {form} icon for {player}")
        return p
    except Exception as e:  # noqa
        print(f"  no GD {form} icon for {player}: {e}")
        _failed.add((player, form))
        return None


if __name__ == "__main__":
    import sys
    for name in sys.argv[1:]:
        for f in ("cube", "ship", "wave"):
            print(name, f, get(name, f))
