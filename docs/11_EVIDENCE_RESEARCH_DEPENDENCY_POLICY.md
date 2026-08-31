# Evidence, Research and Dependency Policy

## Evidence ledger

Material claims should record:
- claim;
- evidence type;
- source;
- version/date;
- applicability;
- confidence;
- contradictions;
- unresolved uncertainty;
- decision affected.

## Preferred evidence ordering

Not a blind ranking, but default preference:
1. measured project evidence;
2. observed runtime/test behavior;
3. primary official documentation;
4. upstream source;
5. upstream issues/incidents;
6. comparable mature implementation;
7. standards/research;
8. reputable secondary material;
9. inference;
10. unknown.

Applicability outranks prestige. A real platform incident can be more relevant than generic documentation.

## External research triggers

Research when uncertainty concerns:
- platform behavior;
- networking/process semantics;
- compatibility;
- security;
- dependency maturity;
- unexplained failure modes;
- performance/resource claims;
- standards/protocol behavior;
- architecture precedent;
- deployment restrictions.

Skip external research when a local fact/test answers the question more directly.

## Open-source reuse workflow

1. Can existing project code solve it?
2. Can stdlib/native platform solve it?
3. Is an already-installed dependency sufficient?
4. Identify mature external candidates.
5. Evaluate necessity.
6. Verify authentic source.
7. Inspect maintenance/sustainability.
8. Inspect security posture and dependency tree when material.
9. Check license compatibility.
10. Check platform/resource/integration fit.
11. Define exit/replacement path.
12. Trial in isolation where useful.

## Code borrowing

If logic is adapted rather than imported:
- respect license;
- understand invariants/failure handling rather than copying snippets mechanically;
- retain relevant edge cases demonstrated by upstream history;
- cite origin where license/project convention requires it.

## Performance claims

No "optimized/faster/lighter" conclusion from code shape alone.
Require:
- bottleneck or target;
- representative workload;
- baseline;
- measurement;
- correctness equivalence;
- resource/latency trade-off.

## Research output discipline

Research notes are not user-facing by default.
The verdict should cite only decision-relevant evidence and uncertainty.
