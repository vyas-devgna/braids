# Threshold and depth together

Load this when the user's requested effort and the change's actual risk disagree.

## The two dials

**Depth (D0–D4)** is routed from risk and is not negotiable by preference. **Threshold (low / high / ultra)** is the user's budget for effort. They are independent: a D3 change with `low` threshold is a real and common situation, not a contradiction.

## Resolving a conflict

Threshold sets a ceiling on effort. Risk sets a floor on care. When the ceiling is below the floor:

1. Do the smallest change that does not weaken a guarantee.
2. Say in one sentence what the risk is and what the requested threshold skipped.
3. Report honestly: name what was not checked rather than implying coverage.
4. If the user reaffirms the lower threshold after hearing that, do exactly what they asked and record the residual risk in the report.

The floor is narrow on purpose. It is security, authorization, privacy, data integrity, destructive or irreversible operations, and explicit compatibility guarantees—not general tidiness, coverage targets, or architectural taste. Everything else yields to the user's budget without argument.

## The opposite conflict

`ultra` on a genuinely trivial change is also a failure. Rigour that cannot change the outcome is waste billed to the user. Say that the change is D0, do it, and offer the deeper pass rather than performing it unasked.

## What never varies

Threshold changes how much work is done, never what is claimed about it. At any threshold: material claims carry evidence proportional to the claim, unverified stays unverified, and residual risk is stated rather than absorbed.
