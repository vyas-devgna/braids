# Kernel description allowance

Date: 2026-09-03

## Decision

Give the `braids` kernel skill its own metadata ceiling of 280 estimator tokens, separate from the 250 that continues to bind the six satellite skills. Leave the `metadata_tokens` total at 1000, which is the constraint that actually protects the user.

## Evidence

Measured runs on Claude Code 2.1.248, methodology 3.0.0, four repetitions per case:

| Case | Expected depth | Activated | Depth when it activated |
|---|---|---|---|
| `K-CLAIM-UNSUPPORTED` | D3 | 1/4 | D1 |
| `K-D4-IRREVERSIBLE` | D4 | 2/4 | D4, D4 |

Activation on these two high-severity decision cases was **3/8**. The prior record in `docs/29` reported 3/3 activation and blamed depth routing; that measurement came from the trigger corpus, whose prompts ask for judgement ("Review whether this monolith should be split"). The kernel cases are imperatives that describe a dangerous operation without naming it ("Replace every stored state file in place…"). Braids missed those, and where it did load it routed D4 correctly both times. The weak half is activation, not depth.

The description is the activation classifier. Fixing it required clauses the old wording did not carry: direct instructions still qualify, calling a change small or quick does not lower it, stated outcomes are claims, and stored-data rewrites and irreversibility described operationally rather than as the keyword `migration`. Those clauses do not fit in 250 estimator tokens.

The per-skill ceiling was a proxy for the real cost, which is the sum paid on every turn. That sum is 728 of 1000 with the longer description. The proxy had become binding in the wrong place: it was rationing the one description whose accuracy decides whether the other 3.5k tokens are ever loaded at all.

## Alternatives

- **Trim trigger keywords to fit 250**: rejected. It trades measured activation coverage on high-severity cases for adherence to a proxy, and the keyword list could not be shortened without re-measuring 30 positive trigger cases to show nothing was lost.
- **Move the new clauses into `SKILL.md`'s body**: rejected. The body is only read after activation, and activation is the step that was failing.
- **Raise the ceiling for every skill**: rejected. Only the kernel carries the classifier; the satellites are correctly held to 250, and the gate should keep catching drift in them.

## Residual risk

The extra clauses could raise the near-miss false-trigger rate. They are written as modifiers on operations that are already triggers ("a direct instruction still qualifies") rather than as new triggers, and the 30 near-miss prompts in `evals/trigger/cases.jsonl` are text, formatting and explanation tasks that none of the new clauses touch. That reasoning is argued, not measured: the near-miss corpus has not been re-run against the new description, so the false-trigger rate remains unverified.

The estimator is `chars/4`, not a tokenizer, and `docs/29` records it reading roughly 30% low against the one host-authoritative measurement available. The 280 figure inherits that error. It bounds drift; it is not a token count.
