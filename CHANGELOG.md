# Changelog

All notable changes will be recorded here.

## [0.1.0-dev.2] - 2026-09-03

### Added
- **Diagnosis discipline in the kernel.** Reproduce before changing, locate where the invariant first breaks rather than where it surfaces, require that removing a cause removes the symptom, check sibling callers before patching the reported site, and treat a defect with no explained cause as at least D2. Covered by a new `K-DIAGNOSIS-ROOT-CAUSE` eval case; the corpus is now 100.
- **A real host capability probe.** `inspect_capabilities.py` now observes the host from environment markers, CI/container/sandbox/worktree isolation, actual writability, the code-intelligence tools on `PATH`, project instruction files, configured hook events, and the build and test commands the project offers. Every value carries the observation behind it; anything unobservable stays `unknown`, and `enforcement` stays empty by construction. Routed from `host-capabilities.md` and the kernel, which previously named no discovery tool at all.
- **Durability rule for long sessions.** After compaction, unresolved assumptions, unverified claims and residual risks are still open and get re-derived rather than trusted to a previous turn. No project state is written.
- **First graded run records**, in `evals/results/`, with a README stating what they support and what they do not.
- Installer safety: a provenance receipt with per-file hashes, `--force`, `--dry-run`, and unknown-flag rejection.
- Decision record 0004 (kernel description allowance).
- Six skills beside the core method — `braids-review`, `braids-audit`, `braids-risk`, `braids-claims`, `braids-depth`, `braids-help` — each a lens onto the same decision procedure, with matching `commands/*.toml` for slash invocation.
- Implementation threshold `low` / `high` / `ultra`. Threshold caps effort; risk sets the floor on care; neither changes what may be claimed.
- npm package `braids-skill` and `npx braids-skill@next <host>` for hosts with no plugin system, plus `--user` and `--uninstall`.
- Tag-gated release workflow that re-runs every gate and refuses to publish if the tag, `plugin.json` and `package.json` disagree.
- `docs/30_SKILLS_REFERENCE.md`, `docs/31_DISTRIBUTION.md`, issue templates and a PR template that asks what a change claims.
- Portable Agent Skill kernel, routed references, and dependency-free validation scripts.
- Machine-readable contracts, the initial 92-case evaluation corpus, and eight repository fixture families.
- Eight host adapters — Claude Code, Codex, Cursor, Antigravity, GitHub Copilot, OpenCode, Cline, Windsurf — generated from a single metadata source by `scripts/build_adapters.py`. No adapter carries Braids methodology or a second copy of the kernel.
- `scripts/measure_budget.py`, gating static context cost against the `docs/24` ceilings.
- `docs/29_KNOWN_LIMITATIONS.md`, the release-candidate honesty report.
- Decision records 0002 (generated thin adapters) and 0003 (no Guard Mode in 0.1.0).
- Brand asset pack at `assets/`, with a validator rule that fails on any image outside it. Only the Cursor package carries an asset — the 256 px icon for the `logo` field that manifest documents.

### Changed
- **Evidence integrity.** Host runs now verify fixture hashes before execution, install the complete skill set, derive host/package versions at runtime, treat judge failures as blocked, isolate temporary host state, and resist prompt injection in judge inputs. Release grading rejects stale hashes, duplicate records, mixed cohorts, and runs from older Braids versions.
- **Distribution correctness.** The Codex manifest now follows the current interface contract; generated root manifests are checked against adapter sources; CI validates every source and packaged skill; prereleases publish to npm's `next` tag through a provenance-enabled OIDC workflow with a bootstrap-token fallback for the first publication.
- **Installer lifecycle safety.** Partial installs return failure for automation, and uninstall includes clean skills recorded by older releases while rejecting receipt names that could escape the skill root.
- **Truthful failure behavior.** The landing page remains readable without JavaScript/CDN execution and no longer advertises unsupported security claims. Historical pre-development files no longer claim to be current release authority, and the stale checksum inventory was removed.
- **Methodology 3.1.0.** The skill description now activates on imperative phrasing, on stating what a change achieved, and on stored-data rewrites, format changes and irreversibility described operationally rather than as the keyword `migration`; calling a change small or quick no longer lowers it. Measured on Claude Code 2.1.248: activation on two high-severity kernel cases went from 3/8 to 7/8, and the irreversible-migration case from 2/4 to 4/4 with D4 routed every time.
- **`docs/29` diagnosis corrected.** It reported depth routing as the weak half from a four-case trigger-corpus smoke test. Measured against kernel cases, activation was the weak half and depth was right whenever Braids loaded.
- `run_host_evals.py` reads `core_version` and `adapter_version` from `braids.json` instead of hardcoding them beside it.
- `braids-review` describes what distinguishes it from a correctness-focused review, which it loses generic review phrasing to.
- `check_cases` reports a malformed corpus instead of raising.
- OQ-01 resolved: MIT licence, applied to `LICENSE`, `braids.json` and `plugin.json`, with a validator check that the two never diverge.
- OQ-06 partially resolved: package identity is `Vyas Devgna <https://github.com/vyas-devgna>`, required because Claude Code rejects a plugin manifest without `author` under `--strict` and a marketplace manifest without `owner`.
- Host research revalidated against current primary sources for all eight hosts; four against locally installed CLIs.
- The Codex-only `agents/openai.yaml` interface descriptor moved out of the portable kernel into the Codex adapter.
- Repository-root manifests make a GitHub clone directly installable on Claude Code, Codex, and Cursor.
- Skill discovery metadata now treats small trust-boundary and guarantee-weakening edits as risk-sensitive, while preserving mechanical-edit exclusions.
- Host evals now separate trigger measurement from decision-quality judging, reject host errors, support repeated/resumable runs, and pin the evaluated model.

- OQ-07 resolved: final mascot, icon and hero artwork vendored; no Braids behaviour depends on them.

- Seven skill-surface eval cases covering the added skills, including `low` threshold on a harmful change and `ultra` on a trivial one. The corpus is now 100 cases.

### Not yet true
- The 7/8 activation figure is eight runs on two cases on one host. It is not a trigger rate, and the 0.90/0.10 release thresholds remain unmet.
- The near-miss corpus has not been re-run against the new description, so the false-trigger rate is argued, not measured.
- `K-CLAIM-UNSUPPORTED` still self-reports a depth below the D3 floor its own behaviour satisfies.
- No adapter is `supported` or `tested`; all eight are `experimental`.
- Of the six added skills only `braids-review` has been exercised live; the other five have no graded runs.
- On Claude Code the built-in `code-review` skill wins generic review phrasing, so `braids-review` must be named explicitly there.
- A four-case Codex activation smoke exists; the complete trigger, depth, parity, injection-resistance, and cost suites remain ungraded.
- Braids is advisory on every host; it ships no enforcement.
