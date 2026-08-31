# Pre-Development Freeze Checklist

Development of Braids should begin only after this checklist is deliberately accepted.

## Freeze evidence — 2026-08-31

The boxes below are the owner's to tick; they are approval decisions, not build outputs. This section records what each group can now be ticked *against*, so acceptance is made with the evidence in hand.

| Group | Evidence now available | Open |
|---|---|---|
| Product, Portable architecture, Runtime | `skills/braids/SKILL.md` and its eleven references implement the frozen contract; `tests/test_scripts.py::test_kernel_keeps_its_safety_invariants` guards the authority, capability and untrusted-evidence rules against silent removal | none |
| Token/context | `scripts/measure_budget.py` gates dormant, activated and worst-case cost against the `docs/24` ceilings; Claude Code 2.1.248 independently measured 778 always-on across seven skills against ~3.1k for the core skill on invoke | per-run metrics (rework ratio, research marginal value) need graded runs |
| Security | `docs/decisions/0003-no-guard-mode-in-0.1.0.md` records the semantic/deterministic split with per-host coverage holes; `scripts/validate.py` rejects any lifecycle or enforcement file in an adapter; uninstall is exercised on four hosts | prompt-injection *behaviour* is specified and covered by fixtures but not graded |
| Host readiness | all eight research documents carry a 2026-08-31 revalidation section; `matrices/host-capability-matrix.csv` carries the per-host caveat | OQ-02 initial release set is only partially resolved |
| Evaluation | 99 schema-valid cases, including 60 balanced trigger cases, across eight fixture families; `scripts/run_evals.py` provides grading and release thresholds | only small observed controls exist, so no full-suite pass rate is claimed |
| Repository/release | `docs/decisions/0002-generated-thin-adapters.md`; MIT licence resolved; CI validates package, skill, schemas, adapters, budget and evals; `python3 scripts/build_adapters.py --dist dist` reproduces every package offline | marketplace accounts and signing remain open under OQ-06 |

The one gate that no amount of packaging work can close is graded model behaviour. See `docs/29_KNOWN_LIMITATIONS.md`.

## Product
- [ ] Product definition approved.
- [ ] Non-goals approved.
- [ ] "right-sized engineering" decision objective approved.
- [ ] User-authority model approved.
- [ ] No-change verdict explicitly accepted as success.

## Portable architecture
- [ ] Agent Skills is accepted as the primary portable methodology format.
- [ ] Agent Plugins is accepted as the portable packaging floor where supported.
- [ ] MCP is optional, not mandatory.
- [ ] Host-specific rules/hooks/agents/LSP remain adapters.
- [ ] No host adapter may redefine core engineering semantics.

## Runtime
- [ ] Engineering Contract fields frozen.
- [ ] material-assumption policy frozen.
- [ ] context stopping condition frozen.
- [ ] D0-D4 engineering depth model frozen.
- [ ] quality scenario shape frozen.
- [ ] evidence hierarchy/policy frozen.
- [ ] dependency/reuse gate frozen.
- [ ] user-harm constraints frozen.
- [ ] lifecycle trade-off method frozen.
- [ ] implementation authorization boundary frozen.
- [ ] claim-driven verification rule frozen.
- [ ] stop condition frozen.

## Token/context
- [ ] progressive disclosure mandatory.
- [ ] dormant-context objective defined.
- [ ] reference loading rules defined.
- [ ] subagent/research escalation rules defined.
- [ ] telemetry schema can measure actual cost.

## Security
- [ ] threat model reviewed.
- [ ] semantic safety vs deterministic enforcement separated.
- [ ] per-host hook coverage represented explicitly.
- [ ] prompt-injection handling defined.
- [ ] no mandatory remote trust boundary.
- [ ] uninstall/rollback behavior specified.

## Host readiness
- [ ] Claude Code source research revalidated.
- [ ] Codex source research revalidated.
- [ ] Cursor source research revalidated.
- [ ] Antigravity source research revalidated.
- [ ] GitHub Copilot source research revalidated.
- [ ] Windsurf/Cascade source research revalidated.
- [ ] OpenCode source research revalidated.
- [ ] Cline source research revalidated.
- [ ] initial adapter priority agreed.

## Evaluation
- [ ] trigger eval dataset design approved.
- [ ] engineering conformance fixtures approved.
- [ ] adversarial/negative fixtures approved.
- [ ] host adapter acceptance tests approved.
- [ ] token/cost measurements approved.
- [ ] pass/fail release gates approved.
- [ ] held-out evaluation policy approved.

## Repository/release
- [ ] source-of-truth vs generated adapters defined.
- [ ] schemas validate.
- [ ] CI plan approved.
- [ ] versioning policy approved.
- [ ] license decision made.
- [ ] security disclosure policy prepared.
- [ ] contribution boundaries prepared.
- [ ] release package can be independently validated.

## Gate

**If a box materially affects architecture and is unresolved, do not start final implementation.**
A reversible low-level build detail may remain open if it cannot change the product contract or test strategy.
