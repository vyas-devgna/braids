# Changelog

All notable changes will be recorded here.

## [Unreleased]

### Added
- Portable Agent Skill kernel, routed references, and dependency-free validation scripts.
- Machine-readable contracts, the 92-case evaluation corpus, and eight repository fixture families.
- Eight host adapters — Claude Code, Codex, Cursor, Antigravity, GitHub Copilot, OpenCode, Cline, Windsurf — generated from a single metadata source by `scripts/build_adapters.py`. No adapter carries Braids methodology or a second copy of the kernel.
- `scripts/measure_budget.py`, gating static context cost against the `docs/24` ceilings.
- `docs/29_KNOWN_LIMITATIONS.md`, the release-candidate honesty report.
- Decision records 0002 (generated thin adapters) and 0003 (no Guard Mode in 0.1.0).
- Brand asset pack at `assets/`, with a validator rule that fails on any image outside it. Only the Cursor package carries an asset — the 256 px icon for the `logo` field that manifest documents.

### Changed
- OQ-01 resolved: MIT licence, applied to `LICENSE`, `braids.json` and `plugin.json`, with a validator check that the two never diverge.
- OQ-06 partially resolved: package identity is `Vyas Devgna <https://github.com/vyas-devgna>`, required because Claude Code rejects a plugin manifest without `author` under `--strict` and a marketplace manifest without `owner`.
- Host research revalidated against current primary sources for all eight hosts; four against locally installed CLIs.
- The Codex-only `agents/openai.yaml` interface descriptor moved out of the portable kernel into the Codex adapter.

- OQ-07 resolved: final mascot, icon and hero artwork vendored; no Braids behaviour depends on them.

### Not yet true
- No adapter is `supported` or `tested`; all eight are `experimental`.
- No graded model runs exist, so no trigger, depth, parity, injection-resistance or token-saving claim is made.
- Braids is advisory on every host; it ships no enforcement.
