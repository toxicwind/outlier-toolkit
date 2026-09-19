# outlier-watch

First-class, stdlib-only Outlier worker-portal watcher. Lives next to (never inside)
`vendor/`.

## How it works

Outlier has passwordless auth: `POST /internal/login/outlier/magic-link`
`{"email": ...}` emails a one-time link; opening it
`POST`s `/internal/login/outlier/magic-link-verify` `{"token": ...}` and sets the
`_jwt` session cookie (~3 day expiry). Authenticated reads are plain HTTPS:

- `GET /internal/v2/tasks/peek_queue` — the only "work available to me" signal.

Session cookies persist in `~/.local/share/outlier-watch/cookies.json` (mode 600,
gitignored, never committed). Queue normalization reuses
`vendor/outlier-cli/outlier/outlier_cli/parsers.py` read-only.

## Commands

```bash
# 1. request a sign-in link (emails the account)
python3 watch.py auth-request --email toxicwind@gmail.com
# 2. paste the emailed link
python3 watch.py auth-verify 'https://app.outlier.ai/login/verify?token=...'
# 3. check the queue
python3 watch.py check
```

`check` exits 0 with JSON `{ok, authenticated, queue, tasks, task_count}`;
exit 2 means not authenticated (re-run steps 1-2).

## Watch cron

`outlier-mail-watch` (platform scheduler, every 30 min) is the single watch
mechanism, no duplicates:

1. Gmail `from:outlier.ai` since last check, diffed against seen-state in
   `.state/gmail_seen.json` — surfaces only NEW emails (mission deadlines,
   screening steps, task availability). Delivers to main chat.
2. If `~/.local/share/outlier-watch/cookies.json` exists, also runs
   `watch.py check` and reports task_count / queue changes vs
   `.state/last_check.json`. Skipped silently until auth lands.
