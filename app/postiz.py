"""Minimal Postiz public-API client (self-hosted). Needs the API key from Postiz > Settings > Developers."""
import json, mimetypes, os, urllib.request, uuid


class Postiz:
    def __init__(self, base, key):
        self.base = base.rstrip("/")          # e.g. http://localhost:5000  (the API lives under /api/public/v1)
        self.key = key

    def _req(self, method, path, body=None, headers=None, raw=None):
        h = {"Authorization": self.key, **(headers or {})}
        data = raw
        if body is not None:
            data = json.dumps(body).encode()
            h["Content-Type"] = "application/json"
        r = urllib.request.Request(f"{self.base}/api/public/v1{path}", data=data, method=method, headers=h)
        with urllib.request.urlopen(r, timeout=600) as resp:
            t = resp.read().decode() or "null"
        return json.loads(t)

    def integrations(self):
        return self._req("GET", "/integrations")

    def upload(self, path):
        b = uuid.uuid4().hex
        name = os.path.basename(path)
        ctype = mimetypes.guess_type(name)[0] or "application/octet-stream"
        head = (f"--{b}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{name}\"\r\n"
                f"Content-Type: {ctype}\r\n\r\n").encode()
        raw = head + open(path, "rb").read() + f"\r\n--{b}--\r\n".encode()
        return self._req("POST", "/upload", headers={"Content-Type": f"multipart/form-data; boundary={b}"}, raw=raw)

    def schedule(self, integration_id, date_utc, content, media, settings, comment=None):
        value = [{"content": content, "image": [media]}]
        if comment:
            value.append({"content": comment, "image": []})
        body = {"type": "schedule", "date": date_utc, "shortLink": False, "tags": [],
                "posts": [{"integration": {"id": integration_id}, "value": value, "settings": settings}]}
        return self._req("POST", "/posts", body)

    def posts(self, start, end):
        return self._req("GET", f"/posts?startDate={start}&endDate={end}")

    def delete(self, post_id):
        return self._req("DELETE", f"/posts/{post_id}")
