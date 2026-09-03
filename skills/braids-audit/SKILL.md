---
name: braids-audit
description: "Whole-repository engineering audit with no diff: ranked risk surface, trust boundaries, failure gaps, dependency burden. Use for audit this repo, where is this risky, pre-launch check. For a diff use braids-review."
metadata:
  methodology-version: "3.1.0"
---

# Braids audit

Survey a whole codebase and rank where the engineering risk actually is. Use the `braids` skill for the decision method. An audit is read-only: report, do not repair, unless the user asks.

## Bound the survey first

An audit that reads everything costs more than it returns. Establish the entry points, the trust boundaries, the persistent state, and the deploy surface, then read outward from those. State what you did not read.

Start from evidence, not intuition: build files and dependency manifests, entry points and routes, auth and permission code, anything touching money, PII, credentials or migrations, then the modules with the most callers.

## Ranked risk surface

For each finding record consequence if it fires, exposure (who can reach it), detectability, and recoverability. Rank by consequence × exposure, tie-broken by poor detectability and poor recoverability — never by file size or line count.

Look for:

1. **Trust boundaries** — unvalidated external input, missing or inconsistent authz, injection paths, secrets in source or logs, unsafe deserialization.
2. **Data integrity** — non-atomic writes, missing transactions, unbounded migrations, no backup or restore path, corrupt-state handling.
3. **Failure and recovery** — no timeout, no retry budget, non-idempotent retries, no cleanup on partial failure, silent exception swallowing.
4. **Concurrency** — shared mutable state, check-then-act races, ordering assumptions across processes.
5. **Compatibility** — stored formats, public APIs, platform and version assumptions with no matrix behind them.
6. **Dependencies** — unmaintained, unpinned, heavy for what they do, license-incompatible, or replaceable by a few lines.
7. **Cost without value** — abstractions with one implementation, speculative configuration, layers that only forward calls.
8. **Unproven claims** — README or docs asserting fast, secure, reliable, or production-ready with nothing behind it.

## Report

Lead with the three things most worth fixing first and why. Then one line per finding, ranked:

`<rank> <area> <path> — <what is wrong>. <what it costs when it fires>. <smallest fix>.`

Close with: what you deliberately did not audit, what you could not determine without running the system, and the residual risk the owner is carrying today. If the repository is sound, say so and name the two things most worth watching. Do not manufacture findings to fill a report.
