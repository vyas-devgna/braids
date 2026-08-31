# Braids skills reference

Seven skills. One method. Each skill is a lens onto the same decision procedure in `skills/braids/SKILL.md`; none of them redefines it.

> [!NOTE]
> On Claude Code, name `braids-review` explicitly — the built-in `code-review` skill wins generic "review this" phrasing. The core `braids` skill is unaffected: no built-in claims risk routing.

## Choosing one

| You have | Use |
|---|---|
| A diff, branch, or PR | `braids-review` |
| A repository and no diff | `braids-audit` |
| A design you want attacked | `braids-risk` |
| A claim you need to stand behind | `braids-claims` |
| Too much or too little ceremony | `braids-depth` |
| A task, and no strong opinion | `braids` — it routes itself |

## `braids`

The method. Establishes authority and host capabilities, resolves material assumptions from evidence rather than guessing, builds only the model the decision needs, routes depth from risk, applies the reuse gate, rejects candidates that violate a hard constraint, compares lifecycle burden, then maps every material claim to evidence before stopping.

Selected automatically on risky work. ~310 always-on tokens, ~3.1k when it fires.

## `braids-review`

Reviews an actual diff. Refuses to review a description of a change as if it were the change.

Covers correctness, missed surface (callers, subclasses, serialized formats, config, migrations), failure and recovery, concurrency, trust boundaries, compatibility, cost that buys nothing, and unproven claims. Reports `bug` / `risk` / `cost` / `unproven` with the smallest fix for each, separates verified from inferred, and ends with the residual risk of merging.

## `braids-audit`

Whole-repository survey, read-only. Bounds itself from entry points, trust boundaries, persistent state and the deploy surface, and states what it did not read — an audit that reads everything costs more than it returns.

Ranks by consequence × exposure, tie-broken by poor detectability and recoverability. Never by file size.

## `braids-risk`

Pre-mortem. Assumes the change shipped and caused an incident, then works backwards. Interrogates the weakest assumption, missed consumers, partial failure, retry and idempotency, concurrency, upgrade and downgrade, scale, corrupt stored state, dependency outage, and the cheapest attack path — answering each from the code rather than in general.

Discards failures the system cannot reach. A pre-mortem that lists everything is as useless as one that lists nothing.

## `braids-claims`

The claim ledger. Collects every material assertion from the diff, commit messages, PR description, release notes, README and the conversation, maps each to the evidence that would settle it, and marks it `supported`, `unverified`, `contradicted`, or `not-applicable`.

Two rules decide most cases: passing tests support only the behaviour those tests exercise, and missing infrastructure leaves a claim unverified rather than making it true.

## `braids-depth`

The two dials.

**Depth (D0–D4)** is routed from risk and is not negotiable by preference. **Threshold (`low` / `high` / `ultra`)** is the user's budget for effort.

| Threshold | Implement | Verify |
|---|---|---|
| `low` | Smallest change that works. No refactor, no new abstraction. | The obvious check. |
| `high` | Production shape: failure paths, edge cases, affected callers. | Regression tests plus the existing suite. |
| `ultra` | Hostile cases too, plus migration and rollback where state moves. | Evidence for every claim, plus independent challenge. |

Threshold caps effort; risk sets the floor on care. Where they conflict the floor wins and Braids says so — in one sentence, without a lecture. The floor is narrow on purpose: security, authorization, privacy, data integrity, destructive or irreversible operations, and explicit compatibility guarantees. Everything else yields to the user's budget.

`ultra` on a genuinely trivial change is also a failure. Rigour that cannot change the outcome is waste billed to the user.

## `braids-help`

Prints the reference card. Does no engineering work.

## Cost

Measured by `claude plugin details braids` on Claude Code 2.1.248:

| Skill | Always-on | On invoke |
|---|---|---|
| `braids` | ~310 | ~3.1k |
| `braids-review` | ~90 | ~800 |
| `braids-audit` | ~80 | ~810 |
| `braids-depth` | ~80 | ~1.2k |
| `braids-risk` | ~80 | ~700 |
| `braids-claims` | ~70 | ~760 |
| `braids-help` | ~60 | ~960 |
| **Total** | **~778** | — |

Always-on is paid every turn whether or not anything fires. `scripts/measure_budget.py` gates this: 250 tokens per skill, 1000 total, and the standing cost must stay well under a single activation.
