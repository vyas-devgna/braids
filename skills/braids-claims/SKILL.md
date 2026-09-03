---
name: braids-claims
description: "Map every engineering claim to the evidence that would prove it, and mark what is unproven. Use for is this actually faster, prove it, what evidence do we have, can we say production-ready."
metadata:
  methodology-version: "3.1.0"
---

# Braids claim ledger

A claim without evidence proportional to it is a liability. This skill separates what is proven from what is merely believed, and says what would close each gap.

## Collect the claims

Gather every material assertion in scope — the PR description, commit messages, release notes, README, code comments, and anything asserted in conversation. A claim is material when someone would act differently if it were false.

Watch for the words that smuggle claims in: faster, optimized, secure, hardened, reliable, robust, scalable, compatible, backwards-compatible, production-ready, fixes the race, no longer leaks, handles failure.

## Map each to its evidence

| Claim | Evidence that settles it |
|---|---|
| builds | build or compiler result |
| behaviour preserved | targeted regression plus the broader relevant suite |
| integration works | contract, integration, or end-to-end evidence |
| faster / uses less memory | representative before-and-after measurement, with correctness held equal |
| fallback or recovery works | induced failure, then observed cleanup and retry |
| race fixed | concurrency or stress evidence, or a deterministic reproduction that now passes |
| secure against X | threat-specific reasoning plus a negative test for X |
| works on supported platforms | an executed matrix, or authoritative evidence with its limits stated |
| UX improved | observed interaction behaviour |
| clean install and upgrade | an isolated lifecycle exercise |

## Status every claim

Mark each `supported`, `unverified`, `contradicted`, or `not-applicable`. Record what the evidence actually covers and where it stops.

Two rules decide most cases. Passing tests support only the behaviour those tests exercise — a green suite is not evidence for a performance or security claim. And missing infrastructure leaves a claim `unverified`; it does not make it true by inference.

## Report

One row per claim: claim, status, evidence, what the evidence does not cover.

Then state plainly which claims must be removed or softened before this ships, and the cheapest experiment that would upgrade the most valuable `unverified` claim to `supported`. If a claim cannot be evidenced at acceptable cost, the honest move is to stop making it, not to weaken the word.
