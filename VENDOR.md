# VENDOR.md — Outlier Toolkit vendor sources

Vendored third-party repos for Outlier AI (Scale AI contributor platform) tooling.
All cloned `--depth 1` on 2026-09-19. Do not modify in place; re-vendor from upstream.

| dir | upstream | commit sha | upstream date | license | stars¹ |
|---|---|---|---|---|---|
| `vendor/EmptyQueue-Extension` | https://github.com/andreytakhtamirov/EmptyQueue-Extension | `b835f904d6e5f6fb1d495fbc77fd29e33465cd19` | 2025-01-24 | MIT | 3 |
| `vendor/OutlierProjectCheck` | https://github.com/Xh4H/OutlierProjectCheck | `7dcfa112284b0a8d9743731960a8129d08304b03` | 2025-03-02 | none declared | 1 |
| `vendor/Outlier-Tools` | https://github.com/FlintSH/Outlier-Tools | `da27828c8a45508e48d7e53ffa30bdebc4cef03a` | 2025-02-25 | MIT | 6 |
| `vendor/text-search-extension` | https://github.com/ahounain/text-search-extension | `8c77b722cdc8ba44502797e40b6485efcd58488e` | 2025-01-20 | none declared | 0 |
| `vendor/outlier-cli` | https://github.com/adbertram/cli-tools (sparse: `outlier/` + `_repo/skills/outlier-cli/`) | `e451ffae94590877fd014b00480688ab6b9181fa` | 2026-09-17 | MIT | 5 (parent repo) |

¹ star counts observed at vendoring time (2026-09-19).

Notes:
- `outlier-cli` is a sparse checkout of `adbertram/cli-tools` (83-tool monorepo); only the
  `outlier/` CLI package and its `_repo/skills/outlier-cli/` agent skill were taken.
- `Outlier-Tools` is archived/deprecated upstream (author hired by Scale AI, Jan 2025) but the
  repo remains public; kept for its Pay Analyzer earnings tooling.
- `Intizar-T/outlier` was evaluated and EXCLUDED: it is a QA test script with hardcoded
  credentials, not tooling.
