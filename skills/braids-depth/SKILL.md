---
name: braids-depth
description: "Set how hard Braids works: threshold low, high, or ultra, and engineering depth D0-D4. Use for braids low, braids high, braids ultra, keep it light, quick pass, go deep, be thorough, maximum rigour, production-grade."
metadata:
  methodology-version: "3.1.0"
---

# Braids intensity control

Two dials. **Depth** (D0–D4) is routed automatically from risk. **Threshold** (low / high / ultra) is the user's call about how much implementation effort to spend. Depth says how dangerous the change is; threshold says how much work to do about it.

## Implementation threshold

| Threshold | Implement | Verify | Stop when |
|---|---|---|---|
| **low** | Smallest change that works. No refactor, no new abstraction, no extra surface. | The obvious check: it runs, the direct case passes. | It works for the stated case. |
| **high** *(default)* | Production shape. Handle the failure paths and edge cases a reviewer would name. Touch the callers the change actually affects. | Regression tests for changed behaviour, plus the existing suite. | Behaviour is covered and callers are consistent. |
| **ultra** | Everything `high` does, plus the hostile cases: partial failure, retry, concurrency, upgrade and downgrade, scale, corrupt state, dependency outage. Migration and rollback where state moves. | Evidence proportional to every claim — induced failure, measurement, stress, threat-specific checks. Independent challenge of the chosen approach. | Every material claim has evidence and the residual risk is written down. |

Map informal phrasing on: "quick", "just make it work", "minimal", "don't gold-plate" → **low**. Nothing said → **high**. "be thorough", "go deep", "production-grade", "ultra", "treat as critical" → **ultra**.

Threshold controls effort, never honesty. At `low` you still say what you did not check; you do not claim it was verified.

## The one thing threshold cannot lower

A user asking for less work is making a legitimate call about their own time and risk. Take `low` when asked and do not lecture.

The exception is harm. When the change touches security, authorization, privacy, data integrity, a destructive or irreversible operation, or an explicit compatibility guarantee, `low` does not license shipping a weakened guarantee. State in one sentence what the risk is and what `low` would skip, then do the smallest *safe* version. If the user reaffirms after hearing that, do exactly what they asked and record the residual risk plainly.

So threshold sets a ceiling on effort, and risk sets a floor on care. Where they conflict, the floor wins and you say so.

## Engineering depth

Depth is routed from risk, not requested, and not from line count. A one-line auth change can be D3; a thousand-line mechanical rename is D0.

| Depth | Meaning | What it buys |
|---|---|---|
| D0 | Local, reversible, mechanically checkable | Direct work. No research, no delegation. |
| D1 | Routine bounded change with understood callers | Targeted context and the relevant checks. |
| D2 | Cross-module, platform-sensitive, uncertain integration | Explicit system model, quality scenarios, broader tests. |
| D3 | Security, privacy, data integrity, measured performance, concurrency | Threat and failure analysis, independent challenge, real evidence. |
| D4 | Large-scale, irreversible, mission-critical, hard to recover | Staged decision, migration and rollback, strongest evidence, explicit residual risk. |

Threshold and depth interact: `ultra` on a D0 rename is waste, and Braids should say so rather than perform rigour theatre. `low` on a D4 migration is the dangerous case above.

## Explaining a routing

When asked why a task got its depth, name the factors that decided it — severity, exposure, propagation, uncertainty, detectability, recoverability, reversibility, platform variance, user-harm potential — say which one dominated, and state what would move it a level either way.
