#!/usr/bin/env python3
"""outlier-watch: queue/task watcher for Chris's Outlier account.

Subcommands:
  auth-request --email E     POST the magic-link request (emails E a sign-in link)
  auth-verify  <verify-url>  exchange the emailed link for a session (saves jar)
  check                     peek the queue, normalize, emit JSON to stdout

Exit codes: 0 ok, 2 not authenticated, 1 other error.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(
    0,
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "vendor", "outlier-cli", "outlier"),
)

from hatch_outlier import (  # noqa: E402
    OutlierError,
    authenticated,
    extract_token,
    load_jar,
    peek_queue,
    request_magic_link,
    save_jar,
    verify_token,
    LAST_PATH,
)

try:
    from outlier_cli.parsers import normalize_queue_status, normalize_task_rows
except Exception:
    normalize_queue_status = None
    normalize_task_rows = None


def cmd_auth_request(email: str) -> int:
    jar = load_jar()
    try:
        resp = request_magic_link(jar, email)
        save_jar(jar)  # persist pre-auth cookies (_csrf, etc.) for auth-verify
    except OutlierError as e:
        print(json.dumps({"ok": False, "error": str(e)}))
        return 1
    print(json.dumps({"ok": True, "response": resp, "note": "sign-in link emailed; fetch it from Gmail then run auth-verify"}))
    return 0


def cmd_auth_verify(url: str) -> int:
    jar = load_jar()
    try:
        token = extract_token(url)
        resp = verify_token(jar, token)
    except OutlierError as e:
        print(json.dumps({"ok": False, "error": str(e)}))
        return 1
    ok = authenticated(jar)
    print(json.dumps({"ok": ok, "response": resp if isinstance(resp, dict) else str(resp)[:200]}))
    return 0 if ok else 2


def cmd_check() -> int:
    jar = load_jar()
    try:
        raw = peek_queue(jar)  # single shot: 401/auth errors raise OutlierError
    except OutlierError as e:
        print(json.dumps({"ok": False, "authenticated": False, "error": str(e)}))
        return 2
    if normalize_queue_status and normalize_task_rows:
        status = normalize_queue_status(raw)
        tasks = normalize_task_rows(raw.get("assignments"))
    else:
        status = {"raw_keys": sorted(raw.keys())}
        tasks = raw.get("assignments") or []
    out = {
        "ok": True,
        "authenticated": True,
        "queue": status,
        "tasks": tasks,
        "task_count": len(tasks),
    }
    os.makedirs(os.path.dirname(LAST_PATH), exist_ok=True)
    with open(LAST_PATH, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(json.dumps(out, default=str))
    return 0


def main(argv) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 1
    cmd = argv[1]
    if cmd == "auth-request":
        email = argv[3] if len(argv) > 3 and argv[2] == "--email" else (argv[2] if len(argv) > 2 else None)
        if not email:
            print("usage: watch.py auth-request --email E")
            return 1
        return cmd_auth_request(email)
    if cmd == "auth-verify":
        if len(argv) < 3:
            print("usage: watch.py auth-verify <verify-url>")
            return 1
        return cmd_auth_verify(argv[2])
    if cmd == "check":
        return cmd_check()
    print(f"unknown command: {cmd}")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
