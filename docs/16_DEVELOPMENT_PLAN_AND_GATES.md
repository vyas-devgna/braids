# Development Plan and Gates

## Gate 0 — Pre-development freeze
Required before code:
- PRD accepted.
- architecture accepted.
- module contracts accepted.
- host capability schema accepted.
- security threat model accepted.
- token/context policy accepted.
- eval corpus skeleton accepted.
- Tier-1 hosts chosen.

Output: tag dossier as architecture baseline.

## Phase 1 — Portable skill prototype
Build only:
- `SKILL.md`;
- core references;
- validator;
- trigger eval harness/data.

Do not build:
- MCP;
- hooks;
- subagents;
- marketplace packaging beyond minimum local install.

Gate 1:
- skill validates;
- trigger eval acceptable;
- D0-D3 synthetic kernel cases behave correctly;
- context load is bounded.

## Phase 2 — Deterministic support scripts
Add only proven needs:
- capability inspection;
- package/reference validation;
- eval normalization.

Gate 2:
- scripts reduce variance/cost;
- no unnecessary dependencies.

## Phase 3 — Tier-1 host adapters
Order:
1. Claude Code
2. Codex
3. Cursor
4. Antigravity

For each:
- install;
- invoke;
- capability mapping;
- local test;
- uninstall;
- conformance suite.

Gate 3:
- semantic parity across Tier-1.

## Phase 4 — Optional advanced features
Evaluate with evidence:
- Guard Mode.
- Scout/Challenger/Verifier subagents.
- host hooks.
- worktree isolation.
- host-native LSP integration instructions.

Only add if benchmarked benefits exceed token/complexity burden.

## Phase 5 — Tier-2 adapters
Copilot, Windsurf, OpenCode, Cline.

## Phase 6 — Release hardening
- security review;
- supply-chain review;
- packaging;
- documentation;
- marketplace-specific requirements;
- reproducibility;
- cross-platform install test.

## Phase 7 — Public beta
Collect:
- false activations;
- missed activations;
- bad recommendations;
- overengineering incidents;
- underengineering incidents;
- host adapter breakages;
- token complaints;
- maintainers' rejected/accepted findings.

## Phase 8 — v1.0
Requires conformance gates and no unresolved critical safety/architecture defects.

## Change discipline

A proposed Braids feature must state:
- problem;
- observed evidence;
- affected eval case;
- expected benefit;
- added context/tool/dependency/maintenance cost;
- rollback/removal plan.

This forces Braids development to obey Braids.
