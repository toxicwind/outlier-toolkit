# outlier-toolkit

Community tooling for working Outlier AI (Scale AI) contributor missions more efficiently.
Outlier publishes no public API, so everything here drives the worker portal via browser
automation or in-browser page inspection.

## Vendored tools

- **EmptyQueue-Extension** (`vendor/EmptyQueue-Extension`, MIT) — Chrome extension that surfaces
  *why* your Outlier queue is empty (19 EQ reason tags) plus your review level per project.
  Details previously only visible via devtools.
- **OutlierProjectCheck** (`vendor/OutlierProjectCheck`) — Tampermonkey userscript that shows the
  task count on any `app.outlier.ai/projects/<id>` page (and the EQ reason when available),
  via Outlier's internal API.
- **Outlier-Tools** (`vendor/Outlier-Tools`, MIT, archived upstream) — Pay Analyzer: local,
  in-browser earnings visualization (total pay, hourly rate, project breakdown, pay-cycle
  search). All processing is client-side.
- **outlier-cli** (`vendor/outlier-cli`, MIT, sparse checkout of `adbertram/cli-tools`) — Python
  CLI for the Outlier worker portal: `outlier tasks list`, `outlier queue status`, passwordless
  magic-link login (reads the emailed link via Gmail), persistent browser profile.
- **text-search-extension** (`vendor/text-search-extension`) — generic Chromium auto-refresh +
  text-match page watcher; references `app.outlier.ai` — usable as a task-availability notifier.

## Sources / provenance

See [VENDOR.md](VENDOR.md) for upstream URLs, commit SHAs, licenses, and curation notes.

## Ideas for the missions angle

1. Port the OutlierProjectCheck task-count check into the `outlier-cli` flow (or a small
   headless poller) to page Chris the moment queued tasks appear for Live S2S / other projects.
2. EmptyQueue-Extension's EQ reason descriptions + outlier-cli's `queue status` give a
   machine-readable picture of queue state — feed into mission-availability alerting.
3. Outlier-Tools Pay Analyzer logic could be re-driven against current earnings pages for
   hourly-rate tracking across projects (upstream is archived, so fork it).
