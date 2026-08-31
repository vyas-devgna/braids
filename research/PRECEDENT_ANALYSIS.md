# Precedent Analysis — Coding-Agent Methodology Packages

Research date: 2026-08-31

Purpose: extract structural lessons without copying product ideology.

## Ponytail

Repository: https://github.com/DietrichGebert/ponytail

Useful precedent:
- a compact, memorable coding philosophy can be packaged for multiple coding-agent hosts;
- portable/shared instructions plus host-specific installation/adapters reduce drift;
- trace comments can preserve intentional ceilings/compromises where future maintainers need context;
- exemptions prevent the philosophy from damaging security/validation/accessibility and other protected behavior.

Braids adaptation:
- keep the portability/shared-core pattern;
- do not copy code minimization as the objective;
- use trace comments only for non-obvious intentional engineering compromises, not as generation watermarks.

## Superpowers

Repository: https://github.com/obra/superpowers

Useful precedent:
- broad software-development methodology can be decomposed into focused skills;
- orchestration/activation quality matters as much as individual instruction quality;
- cross-harness distribution is feasible but creates synchronization burden.

Braids adaptation:
- split detailed references only where triggers/evidence/verification differ;
- avoid creating a large skill zoo before trigger evals prove it is needed;
- generate adapters from one source of truth where practical.

## Cline public skills / review-team patterns

Repository: https://github.com/cline/skills

Useful precedent:
- review work can be decomposed into independent specialist perspectives;
- independent contexts can expose contradictions missed by a single narrative.

Braids adaptation:
- Challenger/Verifier are logical roles first;
- instantiate extra agents only when D2-D4 risk/uncertainty justifies token/coordination cost.

## Official skill-creator patterns

OpenAI sample:
https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/skill-creator/SKILL.md

Agent Skills description testing:
https://agentskills.io/skill-creation/optimizing-descriptions

Useful precedent:
- build skills from real task examples;
- progressive disclosure;
- forward evaluation;
- trigger-positive and near-miss negative cases;
- repeated runs because activation is nondeterministic;
- validation set separate from optimization set.

## Resulting Braids rule

**The package should remain small until evidence demonstrates that another module, agent, hook, server, or skill produces more engineering value than orchestration/context cost.**
