# Requirements Traceability Matrix

Purpose: prevent the implementation from becoming "Braids-like" while silently omitting the actual product philosophy.

| ID | Product requirement | Architecture owner | Required evidence/evaluation |
|---|---|---|---|
| R-001 | Do not optimize for minimum or maximum code | M10 trade-off/lifecycle engine | Eval includes cases where shorter code loses and where longer code loses |
| R-002 | Engineering depth follows project/change risk, scope and uncertainty | M3/M5 | D0-D4 routing fixtures across tiny to monorepo-scale cases |
| R-003 | Understand wider modules/integration before local optimization when material | M2/M3 | Cross-module regression fixtures; missed-caller score |
| R-004 | No silent material assumptions | M1 + AssumptionRegister | Ambiguous requirement fixtures; count unresolved/material invented assumptions |
| R-005 | Research related implementations/edge cases when decision-relevant | M6 | Research-trigger and research-stop fixtures |
| R-006 | Reuse existing/proven work before rebuilding where lifecycle value is positive | M7 | Dependency-vs-local fixtures; OSS adoption evidence |
| R-007 | External dependency is not free complexity | M7/M10 | Supply-chain/maintenance/license/transitive tests |
| R-008 | Protect users from harm; security foremost | M9 cross-cutting + security policy | Security/data-integrity adversarial fixtures |
| R-009 | Challenge unsafe/wrong engineering, not the person | M15 reporting | Output-style eval: direct, reasoned, non-personal |
| R-010 | User chooses Braids authority level | M1/M11/M12 | Reviewer must not write; implement mode respects authorization |
| R-011 | Consider developer, development environment, deployment and end-user effects | M3/M4/M10 | Quality-scenario coverage fixtures |
| R-012 | Optimize only against evidence/target/bottleneck | M4/M6/M10 | Premature optimization rejection + measured bottleneck acceptance fixtures |
| R-013 | Rare failure significance scales with exposure/severity/recovery | M5 | Low-probability/high-population fixtures |
| R-014 | Avoid speculative future architecture | M10 | YAGNI/unused abstraction fixtures |
| R-015 | Do not add architecture merely because it appears sophisticated | M8/M10 | unnecessary service/layer fixtures |
| R-016 | Produce concise evidence-backed verdicts | M15 | Report length/coverage rubric |
| R-017 | Implement only after permitted; smallest justified blast radius | M12 | scope-creep and unrelated-refactor fixtures |
| R-018 | Verify material claims rather than trusting generated implementation | M13 | claim-to-evidence coverage metric |
| R-019 | Stop when further engineering has lower expected value | M14 | over-engineering/stop fixtures |
| R-020 | Portable across coding-agent hosts | M0 + adapters | cross-host semantic conformance suite |
| R-021 | Use only justified token/context budget | progressive loading + M5/M6 | dormant/active cost measurements |
| R-022 | Never describe advisory behavior as deterministic enforcement | M0/security coverage | host hook negative-path tests |
| R-023 | No mandatory MCP/server infrastructure | packaging architecture | install/run fixture without MCP |
| R-024 | No mandatory subagent swarm | M5/M12 | D0/D1 single-agent conformance |
| R-025 | Session-local state by default | state model | repository cleanliness/uninstall tests |
| R-026 | No-change is a valid engineering result | M14/M15 | correct-existing-implementation fixtures |
| R-027 | Host-specific features must not fork core methodology | build/adapters | generated/source parity and semantic fixture comparison |
| R-028 | Skill should trigger when useful and avoid trivial over-triggering | skill description | positive/near-miss trigger eval suite |
| R-029 | Braids must degrade gracefully when research/LSP/hooks/subagents unavailable | M0/M2/M6/M13 | capability-removal matrix |
| R-030 | Claims about performance/reliability/security/compatibility require appropriate evidence | M13 | unsupported-claim failure fixtures |

## Delivery status — 2026-08-31

Every R-001–R-030 requirement has eval coverage; `scripts/run_evals.py` fails if any is uncovered. Coverage is not the same as demonstrated behaviour. The split:

| Requirements | Deterministically demonstrated today | Still needs graded runs |
|---|---|---|
| R-020, R-023, R-025, R-027 | adapters generated from one metadata source with no duplicated kernel (`scripts/validate.py` rejects any `SKILL.md` under `adapters/`); packages install and uninstall with no MCP or server on four hosts; no `.braids/` state is written | cross-host *semantic* conformance (R-020, R-027) |
| R-021, R-024 | `scripts/measure_budget.py` bounds dormant, activated and worst-case cost; Claude Code 2.1.248 projected 870 always-on across seven skills against ~3.9k for the 3.1.0 core invocation; no adapter ships a subagent | measured runtime tokens per accepted decision, subagent marginal value |
| R-022, R-029 | every `capabilities.json` carries an empty `enforcement` array; `build_adapters.py` rejects an `enforced` operation without an exercised enforcement test, and `validate.py` rejects any lifecycle file in an adapter; no adapter declares an MCP, LSP or hook dependency | behaviour when a tool is removed mid-run |
| R-001–R-019, R-026, R-028, R-030 | specified in the kernel, fixtured in the corpus, and the safety-critical sentences are regression-guarded by `tests/test_scripts.py::test_kernel_keeps_its_safety_invariants` | all of it — these are model-behaviour requirements and no observed run has been graded |

No requirement is claimed as met on the strength of a passing packaging test. See `docs/29_KNOWN_LIMITATIONS.md`.

## Traceability release rule

Every new normative behavior added to the implementation must:
1. have a requirement/ADR owner;
2. identify its module contract;
3. have at least one positive conformance fixture;
4. have a negative/edge fixture when misuse is plausible;
5. update this matrix.

A feature without traceability is provisional and cannot become a release invariant.
