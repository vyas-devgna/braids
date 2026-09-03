---
name: braids-help
description: "Reference card for Braids: what each skill does, the low/high/ultra threshold, and how depth D0-D4 works. Use for braids help, braids commands, what can braids do."
metadata:
  methodology-version: "3.1.0"
---

# Braids reference card

Print this, adapted to what the user asked. Do not perform engineering work here.

## Skills

| Skill | Use it for |
|---|---|
| `braids` | The method itself. Right-sizes any change and holds claims to evidence. Selected automatically on risky work. |
| `braids-review` | A diff, branch, or PR. What breaks, what is unproven, what costs more than it buys. |
| `braids-audit` | A whole repository. Ranked engineering-risk surface when there is no diff. |
| `braids-depth` | Set the implementation threshold (`low`, `high`, `ultra`) or explain engineering depth. |
| `braids-claims` | Build the claim ledger. Every "faster", "secure", "compatible" mapped to the evidence that would prove it. |
| `braids-risk` | Adversarial pre-mortem. Weakest assumption, partial failure, retry, concurrency, upgrade, scale, attack path. |

## Implementation threshold

Say `braids low`, `braids high`, or `braids ultra` to set how much work Braids does.

| Threshold | Implement | Verify |
|---|---|---|
| `low` | Smallest change that works. No refactor, no new abstraction. | The obvious check. |
| `high` *(default)* | Production shape: failure paths, edge cases, affected callers. | Regression tests plus the existing suite. |
| `ultra` | Hostile cases too — partial failure, retry, concurrency, upgrade, scale, corrupt state, outage. Migration and rollback. | Evidence for every claim, plus independent challenge. |

Threshold caps effort; risk sets the floor on care. `low` is honoured without argument, except where the change would weaken security, authorization, privacy, data integrity, a destructive or irreversible operation, or a compatibility guarantee — there Braids names what `low` skips and does the smallest safe version. Threshold never changes what gets claimed.

## Depth

| Depth | Work | Treatment |
|---|---|---|
| D0 | Local, reversible, mechanically checkable | Do it. No research, no delegation. |
| D1 | Routine bounded change | Targeted context and relevant checks. |
| D2 | Cross-module, platform-sensitive, uncertain integration | System model, scenarios, broader tests. |
| D3 | Security, privacy, data integrity, measured performance, concurrency | Threat and failure analysis, independent challenge, real evidence. |
| D4 | Large-scale, irreversible, mission-critical | Staged decision, migration and rollback, strongest available evidence, explicit residual risk. |

Depth follows risk, never line count. A one-line auth change can be D3; a thousand-line mechanical rename is D0.

## Governing rule

Choose the lowest total lifecycle burden among options that satisfy the real requirements, quality scenarios, hard constraints, and acceptable residual risk. Complexity is a cost that must buy something. "No change" is a valid result.

## Note

Braids is advisory. It reasons about unsafe changes; it does not block tool calls. It ships no hooks and enforces nothing.
