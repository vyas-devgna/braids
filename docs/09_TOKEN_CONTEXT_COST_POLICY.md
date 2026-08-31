# Token, Context and Cost Policy

## Research basis

Agent Skills uses progressive disclosure: approximately 100-token metadata at discovery, full instructions only on activation, and references/resources only when required. The specification recommends <5000 tokens for the skill body and <500 lines. Cline documents the same three-level model. Codex similarly uses skill discovery metadata and loads full content after selection.

## Product objective

Braids should optimize **total engineering cost**, not raw token count.

A task that needs 20% more analysis but prevents a failed architecture/rewrite can reduce total cost. Conversely, loading every architecture/security/performance reference for a local rename is waste.

## Token architecture

### Level A — discovery
Only name + description.

Target: concise enough for reliable routing; do not stuff methodology into the description.

### Level B — kernel
Load `SKILL.md` after activation.

Target: 1500-3000 tokens.
Hard design ceiling: <5000 tokens.

Contains only:
- operating principles;
- depth router;
- module sequence;
- conditions for loading references;
- stop/report rules.

### Level C — references
Load only matched domain files:
- security only for relevant trust/user-harm concerns;
- performance only for performance/resource claims;
- dependency reference only when dependency/reuse decisions exist;
- host capability reference only when native capability affects execution;
- verification reference only to select relevant evidence.

### Level D — external project/research context
Acquire progressively.

Stop when additional information is unlikely to change:
- candidate set;
- risk depth;
- hard constraints;
- chosen approach;
- verification strategy.

## Subagent policy

Subagents consume separate contexts and often more total tokens.

Use only if:
- independence materially improves falsification/verification;
- parallel read-heavy research saves latency;
- work can be cleanly isolated.

Do not use for D0/D1 by default.

## External research policy

Research has a value-of-information gate:
`research if plausible new evidence can materially change the decision`

Otherwise skip.

## Concision policy

User-facing report defaults to:
- one verdict;
- 3-7 material findings;
- evidence/risks;
- next action.

Working detail stays internal/session state unless requested.

## Cost metrics for evals

Record:
- input tokens;
- output tokens;
- tool calls;
- external search calls;
- number of files read;
- number of reference modules loaded;
- subagents spawned;
- elapsed time where available;
- rework attempts.

Compare Braids against baseline on **total task completion cost**, not only first-turn tokens.

## Acceptance target

D0/D1 tasks: Braids overhead should remain small and bounded.
D2-D4 tasks: higher overhead is acceptable only when it improves defect/risk detection, decision quality or rework rate.

No fixed percentage is frozen before measurement.
