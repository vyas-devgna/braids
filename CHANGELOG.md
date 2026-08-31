# Changelog

All notable changes will be recorded here.

## [Unreleased]

### Added
- Six skills beside the core method — `braids-review`, `braids-audit`, `braids-risk`, `braids-claims`, `braids-depth`, `braids-help` — each a lens onto the same decision procedure, with matching `commands/*.toml` for slash invocation.
- Implementation threshold `low` / `high` / `ultra`. Threshold caps effort; risk sets the floor on care; neither changes what may be claimed.
- npm package `braids-skill` and `npx braids-skill <host>` for hosts with no plugin system, plus `--user` and `--uninstall`.
- Tag-gated release workflow that re-runs every gate and refuses to publish if the tag, `plugin.json` and `package.json` disagree.
- `docs/30_SKILLS_REFERENCE.md`, `docs/31_DISTRIBUTION.md`, issue templates and a PR template that asks what a change claims.
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
- Repository-root manifests make a GitHub clone directly installable on Claude Code, Codex, and Cursor.
- Skill discovery metadata now treats small trust-boundary and guarantee-weakening edits as risk-sensitive, while preserving mechanical-edit exclusions.
- Host evals now separate trigger measurement from decision-quality judging, reject host errors, support repeated/resumable runs, and pin the evaluated model.

- OQ-07 resolved: final mascot, icon and hero artwork vendored; no Braids behaviour depends on them.

### Not yet true
- No adapter is `supported` or `tested`; all eight are `experimental`.
- A four-case Codex activation smoke exists; the complete trigger, depth, parity, injection-resistance, and cost suites remain ungraded.
- Braids is advisory on every host; it ships no enforcement.
