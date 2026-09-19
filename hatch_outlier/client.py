"""Lightweight Outlier worker-portal client (plain HTTPS, no browser).

Replaces the playwright-bound vendor CLI with a stdlib-only HTTP client:
  1. POST /internal/login/outlier/magic-link {"email": ...}  -> emailed link
  2. POST /internal/login/outlier/magic-link-verify {"token": ...} -> _jwt cookie
  3. GET  /internal/v2/tasks/peek_queue with _jwt + X-CSRF-Token

Session cookies persist in a 0600 JSON jar outside the repo. Nothing here
touches the vendor tree; vendor/outlier_cli/parsers.py is reused for
normalization (imported read-only).
"""

from __future__ import annotations

import base64
import html
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from http.cookiejar import CookieJar, LWPCookieJar
from typing import Any, Dict, List, Optional

BASE = "https://app.outlier.ai"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36"}

STATE_DIR = os.environ.get(
    "OUTLIER_WATCH_STATE",
    os.path.expanduser("~/.local/share/outlier-watch"),
)
JAR_PATH = os.path.join(STATE_DIR, "cookies.json")
LAST_PATH = os.path.join(STATE_DIR, "last_check.json")

VERIFY_RE = re.compile(r"https://app\.outlier\.ai/login/verify\?[^\"'<>\\s]+")


class OutlierError(Exception):
    pass


def _state():
    os.makedirs(STATE_DIR, exist_ok=True)


def _jar() -> CookieJar:
    return CookieJar()


def _csrf(jar: CookieJar) -> str:
    for c in jar:
        if c.name == "_csrf":
            return c.value
    return ""


def _has_jwt(jar: CookieJar) -> bool:
    for c in jar:
        if c.name == "_jwt" and c.value:
            return True
    return False


def save_jar(jar: CookieJar) -> None:
    _state()
    data = []
    for c in jar:
        data.append(
            {
                "name": c.name,
                "value": c.value,
                "domain": c.domain,
                "path": c.path,
                "secure": bool(c.secure),
                "expires": c.expires,
            }
        )
    with open(JAR_PATH, "w") as f:
        json.dump(data, f)
    os.chmod(JAR_PATH, 0o600)


def load_jar() -> CookieJar:
    jar = _jar()
    if not os.path.exists(JAR_PATH):
        return jar
    try:
        with open(JAR_PATH) as f:
            data = json.load(f)
    except Exception:
        return jar
    now = int(time.time())
    for d in data:
        if d.get("expires") and d["expires"] < now:
            continue
        from http.cookiejar import Cookie

        jar.set_cookie(
            Cookie(
                version=0,
                name=d["name"],
                value=d["value"],
                port=None,
                port_specified=False,
                domain=d.get("domain", ".outlier.ai"),
                domain_specified=True,
                domain_initial_dot=d.get("domain", "").startswith("."),
                path=d.get("path", "/"),
                path_specified=True,
                secure=bool(d.get("secure")),
                expires=d.get("expires"),
                discard=False,
                comment=None,
                comment_url=None,
                rest={},
            )
        )
    return jar


def _req(jar: CookieJar, method: str, path: str, body: Any = None) -> Any:
    url = BASE + path
    data = None
    headers = dict(UA)
    if body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    csrf = _csrf(jar)
    if csrf:
        headers["X-CSRF-Token"] = csrf
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    try:
        resp = opener.open(req, timeout=30)
        raw = resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        raise OutlierError(f"{method} {path} -> HTTP {e.code}: {raw[:300]}")
    if not raw:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


def request_magic_link(jar: CookieJar, email: str) -> Dict[str, Any]:
    """Ask Outlier to email a sign-in link. Returns the raw API response."""
    return _req(jar, "POST", "/internal/login/outlier/magic-link", {"email": email})


def extract_token(verify_url: str) -> str:
    m = re.search(r"[?&]token=([^&]+)", verify_url)
    if not m:
        raise OutlierError(f"no token param in verify url: {verify_url[:80]}")
    return m.group(1)


def verify_token(jar: CookieJar, token: str) -> Dict[str, Any]:
    """Exchange a magic-link token for a session. Saves the jar on success."""
    out = _req(jar, "POST", "/internal/login/outlier/magic-link-verify", {"token": token})
    save_jar(jar)
    return out if isinstance(out, dict) else {"raw": str(out)[:200]}


def api_get(jar: CookieJar, path: str) -> Any:
    return _req(jar, "GET", path)


def authenticated(jar: CookieJar) -> bool:
    if not _has_jwt(jar):
        return False
    try:
        me = api_get(jar, "/internal/v2/tasks/peek_queue")
        return isinstance(me, dict)
    except OutlierError:
        return False


def peek_queue(jar: CookieJar) -> Dict[str, Any]:
    body = api_get(jar, "/internal/v2/tasks/peek_queue")
    if not isinstance(body, dict):
        raise OutlierError(f"peek_queue returned {type(body).__name__}")
    return body
