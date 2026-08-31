# Quality scenarios and engineering depth

Load this reference when requirements use vague qualities, risk is uncertain, or D0–D4 routing needs explicit reasons.

## Scenario compiler

For each relevant concern, state:

- source of stimulus;
- stimulus/event;
- environment and operating condition;
- affected artifact or user flow;
- expected response;
- measurable or observable criterion.

Example: “When the upstream times out after accepting a request, the worker retries without duplicating the operation, releases resources within the configured deadline, and records a diagnosable outcome.”

Use only qualities that can change the decision: correctness, reliability, latency/throughput, CPU/memory/I/O/network/storage, security/privacy/integrity, compatibility, maintainability, operability, developer/deployment UX, accessibility, and end-user behavior.

## Depth factors

Consider exposure, severity, propagation, likelihood, detectability, recoverability, reversibility, uncertainty, platform variance, security/privacy/data impact, and migration burden. Do not collapse them into a universal score.

- D0: local, safe, reversible, mechanically verified.
- D1: bounded routine engineering with known interfaces and recovery.
- D2: multiple consumers/boundaries, platform variance, meaningful integration uncertainty, or deployment behavior.
- D3: security/privacy/integrity, concurrency, reliability, measured performance/resource work, high exposure/severity, or difficult recovery.
- D4: critical/irreversible state, large migration, mission-critical operation, or unusually high uncertainty and blast radius.

Use fixture/project evidence to justify the exact depth. A small auth fix can be D3; a large compiler-covered rename can remain D1/D2.

## Escalation effects

Higher depth may require broader system context, failure scenarios, current primary research, independent challenge, staged execution, rollback/recovery, platform evidence, and stronger verification. It never automatically requires subagents, a dependency, a new service, or exhaustive analysis.
