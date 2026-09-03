---
name: braids-risk
description: "Adversarial pre-mortem: weakest assumption, partial failure, retry, concurrency, upgrade, scale, corrupt state, outage, attack path. Use for what could go wrong, red-team this, poke holes in this, what am I missing."
metadata:
  methodology-version: "3.1.0"
---

# Braids pre-mortem

Assume the change shipped and caused an incident. Work backwards to the cause. The job is to falsify the design, not to appreciate it.

## Interrogate

Ask only the questions the case can actually fail on, and answer each from the code rather than in general:

- **Weakest assumption** — which single belief, if wrong, invalidates the design? What established it: measurement, documentation, or habit?
- **Missed surface** — which caller, subclass, serialized format, config, or downstream consumer was not considered?
- **Partial failure** — it dies halfway. What is left behind, and can the system tell?
- **Retry** — the same operation runs twice. Is it idempotent, and what does the second run do?
- **Concurrency** — two run at once. What is shared, what is ordered by luck?
- **Upgrade and downgrade** — old code meets new data, and new code meets old data. Which direction breaks?
- **Scale** — 100× the input, connections, or file size. What degrades first, and does it degrade or collapse?
- **Corrupt state** — stored data is truncated, half-written, or from a version that no longer exists.
- **Dependency failure** — the service, package, or API is slow, down, rate-limited, or gone. What is the fallback, and has it run?
- **Attack path** — who benefits from breaking this, and what is the cheapest way in?

## Weigh, do not just enumerate

For each credible failure, state consequence, how it would be reached, whether it would be detected, and how recoverable it is. A rare failure with severe consequence and no detection outranks a likely one that is loud and cheap to fix.

Discard failures that need conditions the system cannot reach. A pre-mortem that lists everything is as useless as one that lists nothing.

## Report

Rank the surviving failure modes by consequence × reachability. For each: what happens, the condition that triggers it, and the smallest change that removes or contains it.

Say explicitly which failure you would fix before shipping and which you would accept and monitor. If the design holds up, say so and name the one assumption most worth verifying anyway.
