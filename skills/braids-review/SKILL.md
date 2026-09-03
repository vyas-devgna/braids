---
name: braids-review
description: "Engineering review of a diff, branch, or pull request, ending in a merge verdict: what breaks, what the change asserts without evidence, what costs more than it buys, and the residual risk of merging. Use for review this change, review my PR, is this ready to merge, is this safe to ship, what did this miss. Adds claim and cost judgement to a correctness-focused review rather than repeating it. For a whole repo with no diff use braids-audit."
metadata:
  methodology-version: "3.1.0"
---

# Braids review

Review a change the way a responsible reviewer does: find what is wrong, what is unproven, and what is more engineering than the risk justifies. Use the `braids` skill for depth routing and the decision method; this skill fixes the review's shape.

## Scope the change

Establish the diff (`git diff`, `git diff main...HEAD`, or the named PR), then read enough to judge it: the changed hunks, the callers of every changed signature, the tests that cover them, and the public contract or config the change touches. Stop when more reading cannot change a finding.

If the diff is unavailable, say so and stop. Do not review a description of a change as if it were the change.

## Find the findings

Work through these in order, reporting only what the diff actually shows:

1. **Correctness** — wrong logic, off-by-one, inverted condition, unhandled `None`/empty/zero, mis-ordered operations.
2. **Missed surface** — callers, subclasses, serialized formats, config, migrations, and docs the change should have touched and did not.
3. **Failure and recovery** — partial failure, retry, idempotency, cleanup, timeout, cancellation, and what state survives a crash mid-operation.
4. **Concurrency** — shared state, ordering assumptions, and what two of these racing does.
5. **Trust boundary** — input validation, authz checks, injection, secrets, and anything the change removes or weakens.
6. **Compatibility** — stored data, API/ABI, supported platforms and versions, upgrade and downgrade.
7. **Cost** — abstraction with one implementation, dependency added for a few lines, work the change does not need.
8. **Unproven claims** — anything the change or its message asserts without evidence. Route these through `braids-claims` when there are several.

## Report

Lead with a verdict: merge, merge with the listed fixes, or do not merge. Then one line per finding, most damaging first:

`<severity> <file>:<line> — <what is wrong>. <what happens>. <smallest fix>.`

Severity is `bug` (wrong now), `risk` (wrong under a stated condition), `cost` (works, but buys less than it costs), or `unproven` (asserted without evidence).

Separate what you verified from what you inferred. If you did not run the tests, say the tests were not run. End with the residual risk a reviewer is accepting by merging. If the change is right, say so plainly and stop — a clean diff needs no invented findings.
