# Engineering contract and assumptions

Load this reference when authority, requirements, constraints, or material unknowns affect the decision.

## Contract

Capture only relevant fields:

- objective and observable success criteria;
- in-scope and out-of-scope behavior;
- decision authority: review, advise, recommend-and-wait, or delegated decision;
- implementation authority: none, constrained, or full within the stated task;
- project maturity and distribution model;
- supported environments and compatibility floor;
- scale, exposure, data sensitivity, and recovery expectations;
- hard functional, safety, legal, operational, and resource constraints.

User permission to inspect or advise is not permission to write. Permission to implement a task is not permission to expand its product scope, publish, deploy, contact third parties, transmit private data, or install persistent governance.

## Assumption register

For each decision-relevant unknown, record:

- statement;
- status: stated, observed, documented, inferred, accepted, or unknown;
- material if false;
- evidence or resolution;
- decision effect if wrong.

Resolve material assumptions through project evidence, environment inspection, current primary sources, then user clarification. State rather than hide any material unknown that remains.

Harmless reversible details may be chosen without interruption when they do not change product behavior, safety, supported hosts, external trust/dependencies, token cost, or migration burden.

## Authority stop

In review/advice mode, return the decision and evidence without edits. In constrained implementation, reject scope expansion. If a harmful option fails the safety gate, explain the closest safe option; a host may deterministically block only a path its tested policy covers.
