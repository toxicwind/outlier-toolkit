# Changelog

Auto-backfilled from git history 2026-11-02 (real commits only).

## 2026-10-30
- chore(eidos): apply bun-scaffold bunfig + infra drop-in env (qdrant/hindsight/kafka/redis) — eidos is the pare (3bdb09c)

## 2026-10-22
- rig(phase-b): add bin/run + bin/check + mise gate (self-test gate) (c71ab42)

## 2026-10-16
- snapshot: round-2 forward-commit 2026-10-16 (1547d1c)
- snapshot: forward-commit dirty worktree 2026-10-16 (pre weave-land) (a090410)

## 2026-09-29
- docs(readme): maximal README pass per readme-maximal skill (b242ba2)

## 2026-09-19
- outlier-cli: install readiness on awrawr-pc — add _repo/cli-tools-shared from pinned upstream e451ffae, CLI ve (aa929a7)
- gitignore: secret hygiene block (never commit credentials) (751f6f1)

## 2026-09-18
- watch.py: restore 100755 (xfer dropped exec bit) (7fe1c1e)
- watch.py: persist jar on auth-request, write LAST_PATH on check, single-shot queue read (57acf3e)
- README: outlier-mail-watch is the real cron (gmail + optional portal check) (b0393c9)
- hatch_outlier: stdlib-only portal client + watch.py + README (no browser, no vendor edits) (4cd80b5)
- vendor: flatten vendor trees (remove nested gitlinks, contents in-repo) (7ea42b4)
- vendor: Outlier AI contributor tooling (5 repos) + VENDOR.md manifest (19596e8)
