# Module Contracts and Session State

Logical modules are responsibilities, not mandatory files/processes/subagents.

## M0 Capability Negotiator
Input: host environment.
Output: `HostCapabilities`.
Must: report unavailable capability instead of fabricating it.
Must not: infer enforcement from host brand alone.

## M1 Engineering Contract
Input: user request + project facts.
Output: `EngineeringContract`, initial `AssumptionRegister`.
Contains: objective, scope, authority, maturity, supported environments, expected scale, distribution model, hard constraints, success criteria.

## M2 Progressive Context Acquisition
Input: contract + capabilities.
Output: bounded relevant context set.
Escalation: instructions → diff → files → search → references/callers → configs/tests → runtime/deployment → external context.
Stop: more context is unlikely to change candidate set/risk/verification.

## M3 System/Change-Surface Model
Output: relevant modules, public contracts, callers/callees, state, process/network/persistence/trust boundaries, deployment and user flows, blast radius.

## M4 Quality Scenario Compiler
For each relevant quality:
- source/stimulus;
- environment;
- artifact;
- expected response;
- measurable/observable response criterion.

Avoid: generic "robust/scalable/clean" labels without scenarios.

## M5 Risk/Depth Router
Factors: exposure, severity, propagation, probability, detectability, recoverability, reversibility, uncertainty, platform variance, security/privacy/data impact.
Output: D0-D4 plus reasons.
Do not collapse into one fake universal numeric score.

## M6 Evidence Manager
Output: `EvidenceLedger`.
Evidence classes: measured, observed, primary-documented, upstream-source, incident/issue, secondary, inferred, unknown.
Rule: source ranking is contextual; applicability matters more than prestige alone.

## M7 Reuse/Dependency Gate
Order: project → stdlib → native platform → installed capability → proven external OSS → custom.
New dependency analysis when material: necessity, authenticity, health, security, transitives, license, platform support, resource cost, integration cost, exit strategy.

## M8 Candidate Synthesizer
Always include current baseline when reviewing existing code.
Generate only materially distinct viable alternatives.
No arbitrary "three options" requirement.

## M9 Hard Constraint/User-Harm Gate
Cross-cutting invariants: user safety, security, privacy, data integrity, destructive operations, explicit compatibility, explicit functional requirements.
Output: candidate allowed/rejected plus safer closest alternative.

## M10 Trade-off/Lifecycle Analysis
Compare scenario benefit against total lifecycle burden.
Prefer Pareto elimination and structured evidence over arbitrary weighted scoring.

## M11 Decision Record
Chosen option, rejected alternatives, assumptions, evidence, fallbacks, interfaces, migration, rollback/recovery, resource expectations, residual risk.

## M12 Controlled Execution
Only authorized scope.
Smallest justified blast radius, not smallest diff.
No opportunistic unrelated refactor.

## M13 Claim-Driven Verification
Every material claim maps to evidence.
Examples:
- builds → build result
- behavior preserved → regression tests
- faster → benchmark/profile against baseline
- lower memory → measurement
- compatible → supported matrix or authoritative evidence
- fallback → failure injection
- secure against threat → relevant threat analysis + verification

## M14 Stop Controller
Done if:
- success criteria met;
- hard constraints met;
- claims sufficiently evidenced;
- material regressions absent;
- residual risks documented;
- further work has lower expected value than added burden.

## M15 Reporter
Default report:
1. verdict
2. what is right
3. what is wrong
4. evidence
5. trade-off
6. residual risk
7. next action

Keep concise unless user requests depth.
