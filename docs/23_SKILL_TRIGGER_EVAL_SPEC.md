# Braids Skill Trigger Evaluation Specification

Braids has value only if it activates for engineering-judgment tasks without becoming an expensive always-on reflex.

## Dataset

Maintain at least four partitions:
- training prompts;
- validation prompts;
- fresh holdout prompts;
- host-specific regression prompts.

Each partition contains:
- should-trigger;
- should-not-trigger;
- conditional/ambiguous prompts where invocation depends on project context.

## Positive categories

Examples must cover:
- architecture/refactoring decisions;
- cross-module behavior;
- performance optimization;
- reliability/fallback questions;
- platform compatibility;
- dependency/reuse decisions;
- security-sensitive changes;
- implementation requests with architectural consequences;
- project audits;
- claims such as "make this production ready".

## Near-miss negatives

Important negatives include:
- typo fix;
- deterministic rename;
- simple explanation of existing code;
- formatting-only task;
- one-line syntax question;
- user explicitly requests no engineering review and task is safe/local;
- document-only edits unrelated to software behavior.

## Evaluation method

Agent Skills guidance recommends realistic positive/negative prompts, repeated runs because triggering is nondeterministic, and train/validation separation.

Initial Braids protocol:
- >= 30 positive, >= 30 near-miss negative prompts per portable suite;
- >= 10 host-specific prompts per adapter;
- 3 runs per prompt for development;
- 5 runs for release candidate;
- fixed validation split;
- new holdout set for each major description rewrite.

Record:
`triggered`, `trigger_latency`, `references_loaded`, `estimated_context_cost`, `host`, `version`, `model`, `result`.

## Success targets for first release

These are project gates, not universal scientific thresholds:
- validation positive trigger rate >= 0.90;
- near-miss false-trigger rate <= 0.10;
- no catastrophic false negative in security/data-integrity D3 fixtures;
- no broad description hack that materially increases false positives;
- cross-host description can differ only where host metadata semantics require it; intent scope must remain equivalent.

## Anti-overfitting rule

Never add a phrase solely because one eval prompt contains that phrase. Revise the semantic boundary and rerun validation/holdout.

## Primary source

https://agentskills.io/skill-creation/optimizing-descriptions
