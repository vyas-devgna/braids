# Pre-Test Plan

No Braids implementation should be called stable until this plan is executable.

## Test stages

### Stage 0 — Static package validation
- Agent Skills schema/frontmatter validation.
- Agent Plugin manifest validation.
- host-specific manifest validation.
- no broken relative references.
- no reference chain deeper than one level from SKILL.md.
- scripts executable and self-contained.
- no accidental secrets/binaries.

### Stage 1 — Trigger tests
Run positive, negative and ambiguous prompt corpus.
Tune description before tuning methodology.

### Stage 2 — Kernel unit-like scenario tests
Feed synthetic engineering cases where the expected behavior of each logical module is known:
- material assumption handling;
- D0-D4 routing;
- research gate;
- dependency gate;
- hard constraint rejection;
- stop condition.

These are behavior evals, not conventional unit tests unless deterministic scripts are involved.

### Stage 3 — Repository fixtures
Small script, medium application, monorepo, Windows-specific code, networking code, stateful/database code, UI application.

Use hidden defects and known-correct "do nothing" cases.

### Stage 4 — Baseline A/B
Same host/model/task:
- baseline;
- Braids.

Control temperature/reasoning settings where possible.
Repeat stochastic cases.

### Stage 5 — Host adapter conformance
Claude Code, Codex, Cursor, Antigravity, Copilot, Windsurf, OpenCode, Cline.
Validate installation, activation, capability detection, advisory/degraded behavior, uninstall.

### Stage 6 — Guardrail tests
Where hooks/permissions exist:
- verify covered events;
- verify uncovered paths are reported;
- verify malicious repository text cannot override Braids/system instructions;
- verify denial/approval UX.

### Stage 7 — Token/context stress
- many installed skills;
- long monorepo session;
- compaction;
- no-web environment;
- reference-load minimization;
- D0/D1 overhead.

### Stage 8 — Release candidate dogfood
Real open-source issues/PRs with retrospective ground truth where possible.
Human maintainers review Braids findings for usefulness/false positives.

## Test environments

- Linux primary development environment;
- Windows case fixtures for platform semantics;
- macOS where host availability requires it;
- local and cloud host modes where meaningfully different.

## Exit criteria

Defined in `15_CONFORMANCE_ACCEPTANCE_CRITERIA.md`.
