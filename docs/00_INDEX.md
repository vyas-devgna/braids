# Braids Pre-Development / Pre-Testing Dossier

Research freeze date: **2026-08-31**

This package is the pre-implementation source of truth for Braids. It contains the research record, product requirements, frozen architecture, module/state contracts, host integration designs, packaging rules, token/context policy, security model, evidence policy, evaluation methodology, pre-test plan, acceptance gates, repository/release design, and implementation handoff.

## Start here

1. `research/00_INDEX.md` — current host/ecosystem research.
2. `docs/02_RESEARCH_SYNTHESIS_AND_PRECEDENTS.md` — conclusions from research.
3. `docs/03_PRODUCT_REQUIREMENTS_PRD.md` — product contract.
4. `docs/04_ARCHITECTURE_FREEZE.md` — architecture to implement.
5. `docs/05_MODULE_CONTRACTS_AND_STATE.md` — runtime/module boundaries.
6. `docs/06_HOST_PLATFORM_INTEGRATION_SPEC.md` — integration strategy.
7. `docs/07_SKILL_PLUGIN_PACKAGING_SPEC.md` — portable packaging.
8. `docs/10_SECURITY_THREAT_MODEL.md` — security/trust boundaries.
9. `docs/12_EVALUATION_STRATEGY.md` — how Braids itself will be judged.
10. `docs/13_PRE_TEST_PLAN.md` — test plan before implementation.
11. `docs/22_HOST_ADAPTER_ACCEPTANCE_TESTS.md` — host-specific acceptance.
12. `docs/23_SKILL_TRIGGER_EVAL_SPEC.md` — activation quality.
13. `docs/24_TOKEN_BUDGET_AND_TELEMETRY_SPEC.md` — context/token economics.
14. `docs/25_SECURITY_ENFORCEMENT_COVERAGE.md` — enforcement truthfulness.
15. `docs/26_PREDEVELOPMENT_FREEZE_CHECKLIST.md` — final Gate 0.
16. `docs/27_OPEN_QUESTIONS_AND_ASSUMPTION_REGISTER.md` — decisions implementation must not invent.
17. `docs/28_REQUIREMENTS_TRACEABILITY_MATRIX.md` — requirement → module → evaluation traceability.

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
