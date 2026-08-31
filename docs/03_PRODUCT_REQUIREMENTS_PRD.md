# Product Requirements Document — Braids

## Product statement

Braids is an adaptive engineering-governance skill/plugin that makes AI coding agents reason like a system-aware engineer instead of optimizing for code volume or blindly applying best-practice checklists.

## Problem

Coding agents routinely fail in two opposite directions:

1. **Under-engineering:** locally elegant/simple changes ignore integration contracts, platform variance, fallback paths, security, user scale, process/network behavior, deployment or real-world failure modes.
2. **Over-engineering:** agents invent abstractions, services, frameworks, fallbacks, dependencies or optimization machinery that are not justified by the current requirement.

Users often cannot enumerate every relevant concern before asking an agent to work. The agent should discover and evaluate those concerns proportionally.

## Primary users

- beginners using agents as an embedded experienced engineer;
- competent developers seeking stronger architecture/review discipline;
- advanced engineers who want an adversarial second opinion;
- open-source maintainers reviewing contributions;
- teams using multiple coding-agent hosts.

Braids must not assume user expertise. Material ambiguity about authority or constraints must be resolved.

## Jobs to be done

- inspect an idea before code exists;
- review a proposed change;
- audit a subsystem/project;
- choose between implementation approaches;
- research platform/OSS precedents and failure history;
- implement an authorized engineering decision;
- verify claims about correctness/performance/reliability/security/UX;
- explain trade-offs concisely.

## Functional requirements

FR-1: Determine host capabilities without assuming brand-specific features.
FR-2: Build an Engineering Contract from user intent and discoverable project facts.
FR-3: Record material assumptions and resolve those whose falsity can change the decision.
FR-4: Acquire project context progressively and stop when additional context is low-value.
FR-5: Model the affected system/change surface, not only edited files.
FR-6: Convert relevant quality expectations into concrete scenarios.
FR-7: Determine engineering depth D0-D4 from risk, blast radius and uncertainty.
FR-8: Research externally only when evidence may materially change a decision.
FR-9: Prefer reuse before reinvention, but evaluate dependency lifecycle/supply-chain cost.
FR-10: Generate only materially distinct viable candidates.
FR-11: Reject candidates violating hard safety/integrity/explicit constraints.
FR-12: Compare remaining candidates by scenario value and lifecycle burden.
FR-13: Obtain authorization before material implementation when authority is not already delegated.
FR-14: Implement with the smallest justified blast radius.
FR-15: Map every material claim to suitable verification evidence.
FR-16: Stop when success criteria are satisfied and marginal engineering value is below marginal cost.
FR-17: Return a concise verdict: right, wrong, why, evidence, residual risks, next action.
FR-18: Operate in advisory-only mode where host enforcement is unavailable.

## Non-functional requirements

NFR-1 Portability: core behavior must not depend on a single host.
NFR-2 Context efficiency: progressive disclosure is mandatory.
NFR-3 No hidden network dependency: core skill remains useful offline.
NFR-4 No mandatory server: no backend or MCP required for v1.
NFR-5 Auditability: important recommendations identify evidence and assumptions.
NFR-6 Safety: deterministic guarantees are claimed only when actually enforced.
NFR-7 Reversibility: host adapters and optional guard mode must be removable without modifying user code.
NFR-8 Compatibility: graceful degradation on hosts missing subagents/hooks/LSP/web.
NFR-9 Concision: user-facing verdicts are short by default; detail is available on request.
NFR-10 Model agnosticism: methodology must not rely on hidden reasoning or a specific model family.

## Explicit non-goals

- IDE replacement
- static analyzer
- vulnerability scanner
- LSP implementation
- profiler
- dependency manager
- universal architecture generator
- automatic refactor daemon
- autonomous self-improvement without authorization
- mandatory multi-agent system

## Success definition

Braids succeeds if, across representative tasks, it:
- detects more material integration/risk issues than the baseline agent;
- introduces less unjustified complexity than a naive "enterprise best practices" prompt;
- produces fewer unsupported claims;
- causes fewer regressions/rework loops;
- maintains bounded context/tool overhead on low-risk tasks;
- behaves consistently across hosts despite different capability surfaces.
