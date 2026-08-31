# Braids Host Research — Cline

Research date: 2026-08-31  
Status: pre-development evidence record; recheck before adapter implementation.

## Implementation revalidation — 2026-08-31

Revalidated against current official Cline documentation. Cline is not installed in the development environment, so nothing here is exercised.

- Project skills: `.cline/skills/`, `.clinerules/skills/`, `.claude/skills/`. Global skills: `~/.cline/skills/`.
- A global skill of the same name **takes precedence over** a project skill, so a stale global copy silently shadows a project install.
- Frontmatter requires `name` matching the directory and `description` of at most 1024 characters.
- Progressive disclosure is three-level: metadata at startup (~100 tokens per skill), instructions on trigger (under 5k tokens), resources on demand.
- Skills are managed from the Skills tab in the Cline panel; explicit invocation uses a slash command.
- No plugin manifest format is documented, so the adapter ships a skill directory only.

## Skill model

Cline supports skills with progressive disclosure and emphasizes keeping active skill instructions bounded while loading resources only when needed. This directly supports Braids' one-core-skill + focused references architecture.

## Hooks

Cline exposes lifecycle hooks such as task/session events, prompt events, pre/post tool use, and compaction. Pre-tool hooks can cancel operations.

Use hooks only for deterministic, narrow policies. Do not move architecture judgment into shell scripts or claim a hook protects operations it never sees.

Compaction events are particularly relevant to Braids: if a long engineering task compresses conversation context, the durable/session decision state must retain the Engineering Contract, material assumptions, chosen decision and unverified claims.

## Skills vs reviewer teams

The public Cline skill ecosystem includes precedents for review-oriented skills/multi-reviewer structures. Braids should learn the separation-of-concerns lesson without assuming that multiple reviewers are always cost-effective.

## Adapter design

- portable Braids skill;
- optional Cline hooks for policy/validation;
- preserve Braids state across context compaction;
- explicit integration tests for hook cancellation and post-tool verification;
- no mandatory external server.

## Token policy

Braids should exploit Cline's progressive skill loading:
- minimal discovery metadata;
- bounded core instructions;
- focused references;
- scripts used as black-box deterministic helpers where they save prompt tokens.

## Braids adapter decision

**Use:** portable skill + optional hooks.  
**Important:** test behavior around context compaction and task resumption.

## Primary sources

- https://docs.cline.bot/customization/skills
- https://docs.cline.bot/customization/hooks
- https://github.com/cline/skills
