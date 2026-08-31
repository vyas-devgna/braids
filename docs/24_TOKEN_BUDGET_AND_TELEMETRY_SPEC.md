# Token / Context Budget and Telemetry Specification

Braids is intended to reduce total engineering waste, not minimize the first prompt at any cost. Token spend must nevertheless be observable and bounded.

## Architecture requirement

Progressive disclosure is mandatory.

The Agent Skills specification currently describes approximately:
- ~100 tokens of metadata per discovered skill;
- <5,000 tokens recommended for an activated SKILL.md;
- supporting resources loaded on demand;
- main SKILL.md recommended under 500 lines.

These are ecosystem guidance, not Braids guarantees and can change.

## Braids target budget

### Dormant
Only name/description metadata. No persistent full methodology.

### D0
Core routing only; normally no external reference module.

### D1
Core + one/few relevant references.

### D2
Selective system/evidence references and targeted research.

### D3/D4
Higher spend is permitted only when risk/uncertainty or expected avoided rework justifies it.

## Context-economy rules

1. Do not reread known files unless changed or evidence is stale.
2. Summarize discovered system facts into structured state rather than repeatedly carrying raw source.
3. Do not load every quality/security/performance reference.
4. Prefer deterministic scripts/tool output for mechanical facts.
5. Use subagents only when context isolation/information gain exceeds coordination and token cost.
6. Stop external research when further evidence is unlikely to alter candidate/risk/verification decisions.
7. Keep hook-generated model context terse; hooks should return decisions/identifiers rather than logs.
8. Cache nothing across projects unless provenance/scope is explicit.
9. Never claim token savings from unmeasured behavior.

## Metrics

Per run capture where the host exposes them:
- input/output tokens;
- skill activation count;
- reference files loaded;
- tool calls;
- research calls;
- subagent count;
- retry count;
- verification iterations;
- user clarifications;
- implementation rework;
- wall-clock latency;
- task success/defects in eval fixtures.

Derived metrics:
- context overhead while dormant;
- Braids analysis overhead;
- tokens per accepted decision;
- tokens per defect prevented (eval only);
- rework ratio;
- subagent marginal value;
- research marginal value.

## Optimization objective

A more expensive first pass is acceptable when controlled evaluation shows lower expected total cost through:
- fewer wrong implementations;
- fewer repeated agent attempts;
- fewer regression/fallback misses;
- lower debugging/rework;
- more accurate scope and verification.

Braids must never hide a large token increase behind a qualitative claim that it "probably prevents hallucinations."

## Host-specific cautions

Codex and other hosts impose their own skill-list/context limits and hook output behavior. Store these as adapter-version facts, not portable constants.

## Primary sources

- https://agentskills.io/specification
- https://learn.chatgpt.com/docs/build-skills
- https://learn.chatgpt.com/docs/hooks
- https://learn.chatgpt.com/docs/agent-configuration/subagents
- https://docs.cline.bot/customization/skills
