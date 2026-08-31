# Claim-driven verification and stopping

Load this reference when implementation, release, or a material engineering claim needs an evidence plan.

## Claim ledger

For each claim record the claim, required evidence, current status (`unverified`, `supported`, `contradicted`, or `not-applicable`), evidence links/results, applicability, and residual uncertainty.

Typical mappings:

- builds → compiler/build result;
- behavior preserved → targeted regression plus broader relevant tests;
- integration works → contract/integration/end-to-end evidence;
- faster/less resource use → representative before/after measurement with correctness equivalence;
- fallback/recovery works → induced failure and cleanup/retry evidence;
- race fixed → concurrency/stress or deterministic reproduction evidence;
- secure against a threat → threat-specific analysis and negative/security checks;
- supported-platform compatibility → executed matrix or current authoritative evidence with limits;
- UX/accessibility improved → observed interaction and relevant accessibility checks;
- clean install/upgrade/uninstall → isolated lifecycle exercise.

Passing tests support only the behavior they exercise. Missing infrastructure means the claim remains unverified; it does not become true by inference.

## Failure routing

- Missing context or caller → context/system model.
- Invalid assumption or candidate → contract/candidate/trade-off decision.
- Implementation defect → controlled execution.
- Missing or weak proof → evidence/verification.
- New hard constraint or harm → safety gate and decision.

## Stop controller

Stop when success criteria and hard constraints are met, relevant material claims are supported, regressions are absent at the selected depth, residual risks are explicit and acceptable within authority, and the expected value of more work is below its added burden. Stop with “no change” when the baseline already wins.
