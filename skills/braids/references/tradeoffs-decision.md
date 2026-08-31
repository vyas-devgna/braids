# Candidates, lifecycle trade-offs, and decision record

Load this reference for architecture choices, material alternatives, migrations, or decisions with competing quality/lifecycle effects.

## Candidate set

Include the current implementation when reviewing existing code. For greenfield work, include no implementation only when it is viable. Generate only materially distinct candidates that can satisfy the contract; do not manufacture three options for appearance.

Eliminate any candidate that fails hard safety, integrity, functionality, compatibility, or authority constraints. For the remainder:

1. eliminate candidates dominated across every relevant scenario and burden;
2. compare remaining scenario value and residual risk;
3. include implementation, runtime, operational, maintenance, dependency, migration, rollback, developer, deployment, and user burden;
4. choose the lowest total lifecycle burden that meets the real bar.

Use measurements where available. Do not assign arbitrary universal weights to unlike qualities or treat line count as value.

## Decision record

Record concisely:

- contract/objective and selected depth;
- chosen option and why it wins;
- rejected viable alternatives and decisive trade-off;
- material assumptions and evidence;
- affected interfaces and callers;
- failure, fallback and external-dependency behavior;
- migration, upgrade/downgrade, rollback and recovery when relevant;
- expected resource behavior;
- verification claims and missing evidence;
- residual risks and stop condition.

Keep the record session-local unless the user requests persistence or the task itself requires an ADR/migration artifact.
