# Known Limitations

Version: 0.1.0-dev.2 · Date: 2026-08-31

This is the report `docs/16` requires before a release candidate. Every entry is something Braids does **not** currently support or has **not** currently proven. Nothing here is aspirational.

## The blocking gap: no complete graded model run

Every deterministic gate in this repository passes. None of them tests what Braids does inside a model.

The 92-case corpus, the 60 balanced trigger prompts, the eight fixture families and the grading thresholds in `scripts/run_evals.py` all exist and all validate. A four-case clean Codex activation control observed 3/3 expected activations and 1/1 expected dormancy. It is a smoke test, not the release suite. Claude Code was quota-blocked during the matching run, and the independent property/depth judge was therefore unavailable. Until complete observed runs are graded:

- **no trigger accuracy is claimed.** The 0.90 positive / 0.10 near-miss thresholds are enforced by the grader, not met by evidence.
- **no depth-routing accuracy is claimed.** D0–D4 classification is specified and fixtured, never measured.
- **no cross-host semantic parity is claimed.** `evals/cross-host/cases.jsonl` defines the comparison; the comparison has not been run.
- **no prompt-injection resistance is claimed.** `evals/adversarial/cases.jsonl` specifies the expected refusals; the model has not been put in front of them.

Consequence: **no adapter is `supported` and none is `tested`.** All eight are `experimental`. `scripts/build_adapters.py` enforces this — `status: supported` is rejected unless all ten `docs/22` acceptance checks pass, and `tested` is rejected unless discovery, activation and uninstall pass. Activation has only the Codex smoke evidence above; it does not pass the release gate.

Closing this gap needs graded runs on each host, which cost real model quota. That is a spend decision, not an engineering one.

## Enforcement

Braids is **advisory on every host**. It reasons about unsafe changes; it does not stop a tool call.

No adapter ships hooks, rules, custom agents, commands, LSP or MCP configuration. `guard_mode_default` is `false` everywhere and the builder rejects any other value. Every `capabilities.json` carries an empty `enforcement` array. The reasoning, with the per-host coverage holes that motivated it, is in `docs/decisions/0003-no-guard-mode-in-0.1.0.md`.

Do not read "Braids is installed" as "this operation class is blocked."

## Per-host state

Discovery and uninstall were exercised directly only where the host is installed in the development environment.

| Adapter | Host version exercised | Discovery | Uninstall | Notes |
|---|---|---|---|---|
| claude-code | 2.1.248 | pass | pass | `validate --strict` clean on both manifests; component inventory confirms 0 agents/hooks/MCP/LSP |
| codex | 0.150.1 | pass | pass | leaves an empty `~/.codex/plugins/cache/braids-local/` directory behind |
| opencode | 1.18.23 | pass | pass | `opencode debug skill` resolves the project skill; no config written |
| copilot | 1.0.82 | pass | pass | skill and `--plugin-dir` plugin forms both listed; removal needs the directory path |
| cursor | — | not-exercised | not-exercised | host not installed; packaged from revalidated docs |
| antigravity | — | not-exercised | not-exercised | host not installed; packaged from revalidated docs |
| cline | — | not-exercised | not-exercised | host not installed; packaged from revalidated docs |
| windsurf | — | not-exercised | not-exercised | host not installed; packaged from revalidated docs |

State survival across compaction and resume is `not-exercised` on **all eight**, including the four with installed hosts. Long-session retention of assumptions, decisions and unverified claims is specified and unmeasured.

## Host mechanics that remain unknown or hostile

- **Antigravity global paths conflict across three official pages** — IDE skills at `~/.gemini/antigravity/skills/`, plugins at `~/.gemini/config/plugins/`, CLI plugins at `~/.gemini/antigravity-cli/plugins/`. Only the workspace path is documented as stable; no global installer is offered.
- **Windsurf documentation now redirects to `docs.devin.ai`.** The product surface is moving. Revalidate before any release claim.
- **Cursor documents no plugin uninstall contract.** Local removal is folder deletion plus reload; marketplace lifecycle is unverified.
- **Cline global skills shadow same-named project skills**, so a stale global copy silently wins.
- **Cross-host skill directories leak.** OpenCode auto-loads `~/.claude/skills` and `~/.agents/skills`; Copilot reads `.claude/skills` and `.agents/skills`; Cline reads `.claude/skills`; Cascade reads `.agents/skills`. A Braids copy installed for one host can appear in another. `OPENCODE_DISABLE_EXTERNAL_SKILLS=1` suppresses this for OpenCode only. Conformance runs must control for it.
- **Copilot cloud is out of scope.** The ephemeral cloud agent inherits no local user plugins or skills. Only a `copilot-cli` profile exists; no cloud claim is made.
- **Cursor cloud is out of scope** for the same reason: user skill directories are not copied to Cloud Agents, remote SSH agents or managed workers.

## Measurement

`scripts/measure_budget.py` measures static context cost only, using a **chars/4 estimate, not a tokenizer**. Against the one host-authoritative number available — Claude Code 2.1.248 reporting 280 always-on and ~2.8k on-invoke — the estimator reads 215 and 2385. Treat the static estimate as a bound, not as a token count.

Everything in `docs/24` that depends on a run — tokens per accepted decision, rework ratio, subagent marginal value, research marginal value, single-agent versus subagent comparison, research versus no-research comparison — is unmeasured. No token-saving or cost-reduction claim is made anywhere in this repository.

## Open decisions

- **OQ-02** — initial adapter release set only partially resolved; all eight are built, none is releasable.
- **OQ-03** — Guard Mode default is `false` for development; the public-release policy is not frozen.
- **OQ-04** — telemetry stays local to evaluations; production telemetry is unauthorised and unimplemented.
- **OQ-05** — session state is ephemeral; no persistent-report command is frozen and no `.braids/` state is written.
- **OQ-06** — package identity is resolved (`Vyas Devgna`, `github.com/vyas-devgna`); signing keys, marketplace accounts, and the published repository URL are not. `homepage`/`repository` currently point at an assumed URL.

Resolved: **OQ-01** (MIT) and **OQ-07** (artwork delivered at `assets/`; no behaviour depends on it, and the rule is enforced by `scripts/validate.py` rather than only documented). The pack ships no SVG — a strict vector icon would need redrawing natively.

## What is genuinely proven

For balance, the claims this repository *can* support:

- The portable kernel is a valid Agent Skill (`agentskills validate`), stays under every structural ceiling, and keeps its safety invariants under test.
- The portable package is a valid Agent Plugins v1 manifest against the published schema.
- All eight adapter manifests and capability profiles validate against the repository's own Draft 2020-12 schemas.
- Every adapter package is reproducible offline from a single metadata source, with no second copy of the kernel anywhere.
- Four hosts install, list, disable and remove the generated packages, with residue enumerated.
- Progressive disclosure holds: dormant cost is roughly a twelfth of activated cost, measured independently by Claude Code.
- The 92-case corpus is complete, balanced, hash-pinned to its fixtures, and covers R-001–R-030 plus NFR-10.
