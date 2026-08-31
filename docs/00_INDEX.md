# Braids documentation

Research freeze date: **2026-08-31**

This dossier is the source of truth for Braids: product requirements, frozen architecture, module contracts, host integration, security, evidence policy, evaluation, release gates, and implementation records.

> Looking for installation and everyday use? Start with the [project README](../README.md). Looking for what is not yet proven? Read [Known Limitations](29_KNOWN_LIMITATIONS.md).

## Choose your path

| I want to… | Read |
|---|---|
| Understand the product | [Product requirements](03_PRODUCT_REQUIREMENTS_PRD.md) → [Architecture](04_ARCHITECTURE_FREEZE.md) |
| Implement or review the kernel | [Module contracts](05_MODULE_CONTRACTS_AND_STATE.md) → [Engineering decision method](08_ENGINEERING_DECISION_METHOD.md) |
| Integrate a host | [Host integration](06_HOST_PLATFORM_INTEGRATION_SPEC.md) → [Adapter acceptance tests](22_HOST_ADAPTER_ACCEPTANCE_TESTS.md) |
| Evaluate behavior | [Evaluation strategy](12_EVALUATION_STRATEGY.md) → [Trigger evals](23_SKILL_TRIGGER_EVAL_SPEC.md) |
| Review security | [Threat model](10_SECURITY_THREAT_MODEL.md) → [Enforcement coverage](25_SECURITY_ENFORCEMENT_COVERAGE.md) |
| Check release readiness | [Freeze checklist](26_PREDEVELOPMENT_FREEZE_CHECKLIST.md) → [Traceability](28_REQUIREMENTS_TRACEABILITY_MATRIX.md) → [Known limitations](29_KNOWN_LIMITATIONS.md) |
| Trace a design decision | [Decision records](decisions/) → [Implementation map](development/IMPLEMENTATION_MAP.md) |

## Start here

1. [Host and ecosystem research](../research/00_INDEX.md)
2. [Research synthesis](02_RESEARCH_SYNTHESIS_AND_PRECEDENTS.md)
3. [Product requirements](03_PRODUCT_REQUIREMENTS_PRD.md)
4. [Architecture freeze](04_ARCHITECTURE_FREEZE.md)
5. [Module contracts and state](05_MODULE_CONTRACTS_AND_STATE.md)
6. [Host integration](06_HOST_PLATFORM_INTEGRATION_SPEC.md)
7. [Skill and plugin packaging](07_SKILL_PLUGIN_PACKAGING_SPEC.md)
8. [Security threat model](10_SECURITY_THREAT_MODEL.md)
9. [Evaluation strategy](12_EVALUATION_STRATEGY.md)
10. [Pre-test plan](13_PRE_TEST_PLAN.md)
11. [Host adapter acceptance](22_HOST_ADAPTER_ACCEPTANCE_TESTS.md)
12. [Skill trigger evaluation](23_SKILL_TRIGGER_EVAL_SPEC.md)
13. [Token budget and telemetry](24_TOKEN_BUDGET_AND_TELEMETRY_SPEC.md)
14. [Security enforcement coverage](25_SECURITY_ENFORCEMENT_COVERAGE.md)
15. [Freeze checklist](26_PREDEVELOPMENT_FREEZE_CHECKLIST.md)
16. [Open questions and assumptions](27_OPEN_QUESTIONS_AND_ASSUMPTION_REGISTER.md)
17. [Requirements traceability](28_REQUIREMENTS_TRACEABILITY_MATRIX.md)

## Complete document set

### Research and requirements
- `docs/01_RESEARCH_METHOD_AND_WORKING_NOTES.md`
- `docs/02_RESEARCH_SYNTHESIS_AND_PRECEDENTS.md`
- `docs/03_PRODUCT_REQUIREMENTS_PRD.md`

### Architecture and engineering method
- `docs/04_ARCHITECTURE_FREEZE.md`
- `docs/05_MODULE_CONTRACTS_AND_STATE.md`
- `docs/06_HOST_PLATFORM_INTEGRATION_SPEC.md`
- `docs/07_SKILL_PLUGIN_PACKAGING_SPEC.md`
- `docs/08_ENGINEERING_DECISION_METHOD.md`
- `docs/09_TOKEN_CONTEXT_COST_POLICY.md`
- `docs/10_SECURITY_THREAT_MODEL.md`
- `docs/11_EVIDENCE_RESEARCH_DEPENDENCY_POLICY.md`

### Evaluation and pre-testing
- `docs/12_EVALUATION_STRATEGY.md`
- `docs/13_PRE_TEST_PLAN.md`
- `docs/14_EVAL_CASE_CATALOG.md`
- `docs/15_CONFORMANCE_ACCEPTANCE_CRITERIA.md`
- `docs/22_HOST_ADAPTER_ACCEPTANCE_TESTS.md`
- `docs/23_SKILL_TRIGGER_EVAL_SPEC.md`
- `docs/24_TOKEN_BUDGET_AND_TELEMETRY_SPEC.md`
- `docs/25_SECURITY_ENFORCEMENT_COVERAGE.md`

### Development/release readiness
- `docs/16_DEVELOPMENT_PLAN_AND_GATES.md`
- `docs/17_REPOSITORY_BUILD_RELEASE_PLAN.md`
- `docs/18_RISK_REGISTER.md`
- `docs/19_ARCHITECTURE_DECISION_RECORDS.md`
- `docs/20_IMPLEMENTATION_HANDOFF.md`
- `docs/21_SOURCE_BIBLIOGRAPHY.md`
- `docs/26_PREDEVELOPMENT_FREEZE_CHECKLIST.md`
- `docs/27_OPEN_QUESTIONS_AND_ASSUMPTION_REGISTER.md`
- `docs/28_REQUIREMENTS_TRACEABILITY_MATRIX.md`

### Host research
- `research/CLAUDE_CODE.md`
- `research/CODEX.md`
- `research/CURSOR.md`
- `research/ANTIGRAVITY.md`
- `research/GITHUB_COPILOT.md`
- `research/WINDSURF.md`
- `research/OPENCODE.md`
- `research/CLINE.md`
- `research/PORTABILITY_COMPARISON.md`
- `research/PRECEDENT_ANALYSIS.md`

### Implementation records
- `docs/29_KNOWN_LIMITATIONS.md`
- `docs/development/IMPLEMENTATION_MAP.md`
- `docs/decisions/*.md`
- `adapters/*/README.md`

### Machine-readable artifacts
- `ARCHITECTURE_BASELINE.json`
- `schemas/*.schema.json`
- `matrices/host-capability-matrix.csv`
- `matrices/research-evidence-register.csv`
- `diagrams/*.mmd`
- `PACKAGE_MANIFEST.json`

## Architecture freeze rule

The portable source of truth is the Braids engineering methodology and state/evaluation contracts. Host-specific hooks, rules, agents, permission systems, LSP/MCP declarations, marketplace metadata, and cloud/local behavior are adapters.

**Development should not begin until `26_PREDEVELOPMENT_FREEZE_CHECKLIST.md` is reviewed and accepted.**

Host extension APIs are fast-moving. The per-host research file must be rechecked against primary vendor documentation immediately before each adapter implementation.
