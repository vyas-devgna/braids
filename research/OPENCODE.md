# Braids Host Research — OpenCode

Research date: 2026-08-31  
Status: pre-development evidence record; current docs include V2 behavior and should be treated as version-sensitive.

## Implementation revalidation — 2026-08-31

Revalidated against local OpenCode 1.18.23 and the host's own bundled configuration reference.

- Project skills: `.opencode/skill(s)/<name>/SKILL.md`. Global skills: `~/.config/opencode/skill(s)/<name>/SKILL.md`, explicitly **not** `~/.opencode/`.
- Extra roots register through `skills.paths` / `skills.urls` in `opencode.json`; unknown top-level config keys are rejected outright.
- OpenCode also auto-loads external skills from `~/.claude/skills` and `~/.agents/skills`. `OPENCODE_DISABLE_EXTERNAL_SKILLS=1` suppresses that scan, which matters for cross-host conformance runs.
- `opencode plugin <module>` installs a JavaScript plugin module, a different extension surface from skills. There is no skill plugin manifest, so the adapter ships a skill directory only.
- `opencode debug skill` lists every resolved skill with its location and is the deterministic discovery gate used by the adapter.
- Permission keys include `skill`; actions are `allow`/`ask`/`deny` and the **last** matching rule wins. Per-agent permission overrides the top level. No permission file is shipped, because the correct shape depends on the installed version.
- Config is read once at startup and is not hot-reloaded.

## Skills

OpenCode discovers skills from multiple compatible locations, including Agent Skills-style directories. At runtime it advertises permitted skill metadata and loads the body when the model invokes the skill. Supporting files remain unloaded until explicitly read.

This is an excellent fit for Braids' progressive disclosure design.

## Permissions

OpenCode exposes granular permissions around actions/resources. Current V2 syntax differs from V1, so adapter configuration must be generated/tested against the installed OpenCode version rather than copied blindly.

Braids can use permissions for deterministic user/project policy, but semantic architecture decisions remain in the skill.

## Agents

OpenCode supports primary and subagent profiles. Current built-in patterns include read-oriented exploration agents and general subagents with capability limits. The exact recursion/delegation rules are version-specific.

Braids can map Scout/Challenger/Verifier to OpenCode agents only for D2+ tasks where independent context is worth the cost.

## Adapter design

- canonical Braids skill in Agent Skills layout;
- optional project instructions for Guard Mode;
- optional permission policy examples, never silently installed;
- optional specialized subagents;
- no required MCP.

## Testing focus

- skill discovery across supported directories;
- explicit/automatic invocation;
- permission allow/ask/deny behavior;
- V1/V2 configuration mismatch detection;
- supporting-reference lazy loading;
- subagent capability isolation;
- no permanent host assumptions in the portable skill.

## Braids adapter decision

**Use:** skill-first, permission-aware adapter.  
**Avoid:** hardcoding old permission schema or assuming recursive subagent behavior.

## Primary sources

- https://opencode.ai/docs/skills
- https://opencode.ai/v2/docs/skills
- https://opencode.ai/v2/docs/permissions
- https://opencode.ai/v2/docs/agents
