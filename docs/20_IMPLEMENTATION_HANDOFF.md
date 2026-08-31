# Implementation Handoff — Instructions for the Development Agent

## Objective

Implement Braids from the frozen pre-development dossier. Do not reinterpret the project as a generic code-review skill.

## Read first

1. PRD
2. Architecture Freeze
3. Module Contracts
4. Host Integration Spec
5. Packaging Spec
6. Token Policy
7. Security Threat Model
8. Evaluation Strategy
9. Acceptance Criteria
10. ADRs

## Mandatory development order

1. Build the portable Agent Skill only.
2. Validate skill structure and activation description.
3. Build trigger eval corpus/harness.
4. Implement reference modules progressively.
5. Add only deterministic helper scripts that demonstrate measurable value.
6. Run kernel behavior evals.
7. Implement Tier-1 adapters sequentially.
8. Add optional guards/subagent roles only after baseline measurements establish need.
9. Run cross-host conformance.
10. Package beta.

## Prohibited shortcuts

- Do not create a mandatory server/MCP/database.
- Do not duplicate core prompts into every adapter.
- Do not put the full methodology into persistent rules.
- Do not spawn multi-agent fleets by default.
- Do not claim token savings before measurement.
- Do not claim enforcement when only instructions exist.
- Do not use line count as engineering quality.
- Do not add architecture purely to appear production-grade.
- Do not skip negative/no-change eval cases.

## First implementation milestone

A valid `skills/braids/SKILL.md` plus references that:
- triggers correctly on the initial corpus;
- routes D0-D4 appropriately;
- produces a correct concise decision on synthetic fixtures;
- loads only relevant references;
- has no host-specific dependency.

No marketplace work is required for this milestone.

## Definition of development readiness

Development may begin only after Gate 0 in `16_DEVELOPMENT_PLAN_AND_GATES.md` is accepted.
