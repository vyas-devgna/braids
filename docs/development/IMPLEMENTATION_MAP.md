# Braids implementation map

Date: 2026-08-31

## Authority

`docs/27_OPEN_QUESTIONS_AND_ASSUMPTION_REGISTER.md` controls frozen versus open decisions. Product semantics come from the PRD, architecture from `docs/04`, module contracts from `docs/05`, and release evidence from `docs/28` plus the acceptance specifications.

The development instruction accepts the dossier as the normative implementation baseline. It does not silently resolve open release choices: the license remains TBD, Guard Mode defaults off, telemetry stays local to evaluations, session state stays ephemeral, and marketplace signing is out of scope until credentials and identity are chosen.

## Requirement-to-delivery map

| Requirements | Owners | Deliverables | Evidence and gate |
|---|---|---|---|
| R-001–R-019, R-026, R-030 | M1–M15 | canonical `skills/braids/SKILL.md`, routed references, typed session contracts | kernel, repository, no-change, safety, optimization, scope, and claim-evidence fixtures; Gates A, C, D, G |
| R-020, R-022, R-027, R-029 | M0 + adapters | semantic capability schema, per-operation enforcement coverage, thin host adapters generated from canonical metadata | capability-removal, hook negative-path, adapter install/uninstall, and cross-host semantic conformance; Gates B, D, F, H |
| R-021, R-024, R-028 | progressive disclosure + M5/M6 | precise discovery metadata, compact kernel, shallow references, depth/research/delegation routing | trigger corpus, dormant/D0–D4 telemetry, research/no-research and single/subagent comparisons; Gates A, E |
| R-023, R-025 | packaging + state | dependency-free portable plugin with no MCP/server and no hidden persistent state | offline install/run, repository-cleanliness, disable/uninstall, and artifact-containment tests; Gates B, F, H |

FR-1–FR-18 and NFR-1–NFR-9 map through R-001–R-030 as recorded in `docs/28`. NFR-10 (model agnosticism) gains explicit cross-model/host fixture ownership during Milestone 3.

## Code and contract shape

- One semantic source: `skills/braids/`.
- Logical M0–M15 responsibilities remain prose/runtime contracts, not one class per module.
- JSON Schemas cover the contracts whose validation improves eval determinism: host capabilities, engineering contract, assumptions, system model, quality scenarios, risk, evidence, candidates, decision, verification claims, residual risks, session state, adapter metadata, eval cases/results, and telemetry.
- Python standard-library scripts provide package/reference/schema validation, capability inspection, eval normalization, adapter checks, and reproducible archive hashes. No runtime dependency, MCP server, database, or production telemetry.
- Adapters contain host metadata, installation/coverage documentation, and optional off-by-default Guard components. They do not copy or alter the kernel.

## Milestone status — 2026-08-31

| Milestone | State | Evidence |
|---|---|---|
| 0 Bootstrap | done | governance files, canonical metadata, MIT licence |
| 1 Portable kernel | done | `agentskills validate` clean; structural and safety-invariant tests |
| 2 Contracts and schemas | done | 17 Draft 2020-12 schemas, meta-validated in CI |
| 3 Evaluation harness | corpus done, small controls run | 100 cases, 60 balanced trigger prompts, 8 fixture families; no complete `--results` file exists |
| 4 Host adapters | packaged, not accepted | 8 adapters generated from one source; discovery and uninstall exercised on Claude Code, Codex, OpenCode and Copilot; all 8 remain `experimental` |
| 5 Guard Mode | deliberately not shipped | `docs/decisions/0003-no-guard-mode-in-0.1.0.md` |
| 6 Token/context | static budget done, per-run open | `scripts/measure_budget.py`; Claude Code 2.1.248 projected 870 always-on / ~3.9k for the 3.1.0 core invocation |
| 7 Security/adversarial | deterministic checks done, behaviour unrun | lifecycle-file and kernel-script gates in `validate.py`; adversarial corpus specified but ungraded |
| 8 Cross-host conformance | blocked | needs graded model runs on each host |
| 9 Release candidate | blocked on 3, 8 | `docs/29_KNOWN_LIMITATIONS.md` |

## Milestone gates

1. Bootstrap: governance files, canonical metadata, clean layout, local license placeholder.
2. Kernel/contracts: Agent Skill validation, bounded `SKILL.md`, routed references, D0–D4 and authority contracts.
3. Evals: executable trigger/kernel/adversarial/capability/no-change cases and traceability coverage.
4. Adapters: current primary-source revalidation followed by per-host acceptance; unsupported mechanics remain explicit.
5. Guard Mode: add only narrow tested enforcement; otherwise document advisory coverage.
6. Token/security/conformance: measured local telemetry, adversarial tests, identical semantic fixtures across supported adapters.
7. Release candidate: all local gates, reproducible artifacts, known limitations, and unresolved external-host/license gates reported rather than faked.

## Reversible conflict decisions

- Split Engineering Contract authority into decision authority and implementation authority.
- Add `unknown` and per-operation enforcement states instead of fabricating host capabilities.
- Use `residual_risks` as the canonical serialized field while retaining “Residual Risk Register” as the conceptual name.
- Keep risk/depth qualitative; fixtures assert reasons/properties, not a universal numeric score.
- Treat verification failure as a route back to the responsible context, decision, execution, or evidence stage.
- Include the existing baseline when reviewing; include “no change” in greenfield candidate sets only when viable.
- Record Tier 1 as a validation sequence, not an unsupported public-release promise.
