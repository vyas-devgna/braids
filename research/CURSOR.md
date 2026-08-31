# Braids Host Research — Cursor

Research date: 2026-08-31  
Status: pre-development evidence record; recheck before adapter implementation.

## Manifest revalidation — 2026-08-31

Fetched from the current plugin reference during adapter implementation.

- Enhanced manifest lives at `.cursor-plugin/plugin.json`; only `name` is required (lowercase kebab-case, alphanumeric at both ends). No `$schema` is documented for this form.
- Optional fields: `description`, `version`, `author` (object with `name`), `homepage`, `repository`, `license`, `keywords`, `logo`, `rules`, `agents`, `skills`, `commands`, `hooks`, `mcpServers`, `variables`.
- Default discovery when a field is omitted: `skills/`, `rules/`, `agents/`, `commands/`, `hooks/hooks.json`, `mcp.json`.
- No local install/uninstall CLI is documented; local testing remains a directory under `~/.cursor/plugins/local` plus a reload.

## Implementation revalidation — 2026-08-31

Current official documentation confirms separate portable Agent Plugin and enhanced Cursor Plugin wrappers.

- Direct skills use project `.agents/skills/` or `.cursor/skills/`; user skills are not copied to Cloud Agents, remote SSH agents, or managed workers.
- Enhanced wrapper uses `.cursor-plugin/plugin.json` with default root `skills/`, `rules/`, `agents/`, `commands/`, `hooks/hooks.json`, and `mcp.json` discovery.
- Cloud supports only command hooks, omits several local lifecycle events, excludes user hooks, and has no hooks during initial read-only exploration.
- Third-party Claude hooks require explicit enablement; all matching sources run by precedence, so duplicate Braids registration must be tested.
- Official docs do not yet provide a complete plugin disable/uninstall contract. Initial local removal is folder deletion plus reload; marketplace lifecycle remains unknown until exercised.
- Initial adapter ships skill-only portable and enhanced wrappers; no rules, hooks, agents, commands, variables, or MCP.

## Two plugin formats

Cursor currently supports:
1. **Agent Plugins** — root `plugin.json`; portable skills and MCP servers.
2. **Cursor Plugins** — `.cursor-plugin/plugin.json`; adds Cursor-specific rules, agents, commands, hooks, and variables.

This is almost exactly the architecture Braids needs: a portable Agent Plugin floor plus a richer optional Cursor adapter.

## Skills and rules

Skills provide on-demand specialized capability. Rules provide persistent guidance. Braids should:
- put the actual methodology in the skill;
- use an extremely small optional rule only for Guard Mode;
- avoid duplicating methodology in both locations.

## Hooks

Cursor hooks are spawned processes communicating over stdio/JSON and can observe, block, or modify defined agent-loop events. They can gate risky operations, inspect edits, control subagent execution, or inject context.

Braids hooks should remain narrow:
- block clearly forbidden destructive paths;
- enforce explicit organization policy;
- trigger deterministic validation where inexpensive.

Do not make ordinary architecture decisions in hook scripts.

## Cloud agents

Cursor Cloud Agents execute in isolated remote environments. Host behavior differs from local IDE execution. In particular, project hooks do not necessarily cover the earliest read-only exploration stage. User-level local configuration also cannot be assumed present in cloud execution.

Therefore `HostCapabilities` needs execution-surface granularity:
`cursor-local`, `cursor-cloud`, or equivalent discovered behavior.

## Subagents

Subagents have separate contexts and can support parallel or isolated exploration/verification. Braids should use them only when D2+ work benefits from independent evidence or context isolation.

## Third-party compatibility

Cursor can load selected third-party configurations, including Claude Code hooks when enabled. Braids should not depend on this compatibility mode, but its build/test matrix should detect it to avoid duplicate hook execution.

## Local testing / marketplace

Cursor documents local plugin testing from `~/.cursor/plugins/local`. Marketplace plugins are Git-backed and reviewed. The official template should be used as the host-specific packaging baseline rather than inventing a layout.

## Braids adapter decision

**Canonical:** Agent Plugin compatible package.  
**Enhanced:** optional Cursor Plugin containing Guard rule, hooks, agents/commands.  
**Cloud:** treat hook/config assumptions separately from local IDE.

## Primary sources

- https://prod.cursor.com/docs/plugins
- https://prod.cursor.com/docs/reference/plugins
- https://prod.cursor.com/docs/skills
- https://prod.cursor.com/docs/hooks
- https://prod.cursor.com/docs/customize-cursor
- https://prod.cursor.com/docs/reference/third-party-hooks
- https://github.com/cursor/plugin-template
- https://cursor.com/docs/cloud-agent
- https://cursor.com/docs/subagents
- https://cursor.com/docs/reference/third-party-hooks
