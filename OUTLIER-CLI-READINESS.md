# Outlier Aether CLI — auth-readiness

Goal: `outlier-35-aether-mission-deadline` (goal_09fb101265d0). Mission "Get Started on Aether!" (up to $35) expires **2026-09-19 15:59 MDT**.
Prepared by lane-1 (visible contributor) 2026-09-19 ~04:05 MDT. Lane-2 is the accountable owner per fleet assignment.

## What is installed

- CLI: `outlier` via `uv tool install`, on PATH at `~/.local/bin/outlier` (awrawr-pc)
- Version: `outlier-cli version 0.1.0`
- Source: `/home/toxic/sovereign/projects/outlier-toolkit/vendor/outlier-cli/outlier` (vendored, MIT)
- Missing framework dep `_repo/cli-tools-shared` was fetched from the **pinned upstream commit** `e451ffae94590877fd014b00480688ab6b9181fa` (adbertram/cli-tools, matches VENDOR.md) and placed at `vendor/outlier-cli/_repo/cli-tools-shared`.

## Verified commands (all run on awrawr-pc 2026-09-19)

```bash
export PATH="$HOME/.local/bin:$PATH"
outlier --version            # outlier-cli version 0.1.0
outlier auth status          # JSON: authenticated=false, "Not authenticated. Run 'outlier auth login' to configure."
outlier auth login --help    # works
```

## Exact remaining user-only steps (Chris — nothing else blocks)

Outlier has **no password**. Auth is a passwordless emailed one-time link → persisted browser session cookie (`_jwt` on `.outlier.ai`). The CLI consumes it headlessly via the repo-owned `google` CLI reading Gmail, so the **Gmail mailbox must be accessible to the `google` CLI** (`google auth status` must pass for that mailbox).

1. Set the account email once:
   ```bash
   mkdir -p ~/.local/share/cli-tools/outlier
   echo 'ACCOUNT_EMAIL=<Chris's Outlier account email>' >> ~/.local/share/cli-tools/outlier/.env
   ```
2. Log in (fully non-interactive; mails a fresh link and consumes it from Gmail):
   ```bash
   outlier auth login
   ```
3. Confirm:
   ```bash
   outlier auth status --table
   outlier auth test
   ```
4. Then:
   ```bash
   outlier tasks list --table     # queued work assignments
   outlier queue status --table   # why the queue is empty, if it is
   ```

## Hard stops — deliberately NOT done

- Did not set `ACCOUNT_EMAIL` (Chris's account email was not confirmed; reading Gmail to find it was out of scope).
- Did not run `outlier auth login` (it mails a fresh sign-in link and reads Gmail — Chris's interactive/email surface).
- Did not touch Gmail, did not click/complete any screening step, did not create an account.
- `/home/toxic/.local/share/outlier-watch/cookies.json` (empty `[]`, created 03:52 MDT) was observed read-only and left untouched — appears to be lane-2's in-progress auth setup.

## Post-login

Once `outlier auth test` passes, the Aether mission claim + Live S2S screening remain Chris's interactive steps; the 14:00 MDT reminder cron still fires to confirm completion.
