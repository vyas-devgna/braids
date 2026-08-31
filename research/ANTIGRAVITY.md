# Braids Host Research — Google Antigravity

Research date: 2026-08-31  
Status: pre-development evidence record; recheck before adapter implementation.

## Manifest and path revalidation — 2026-08-31

Fetched from the current plugins, CLI plugins and IDE skills pages during adapter implementation.

- CLI manifest: root `plugin.json`, only `name` mandatory (pattern `^[a-zA-Z0-9-_]+$`); `description` optional; `$schema` optional with value `https://antigravity.google/schemas/v1/plugin.json`.
- Plugin layout: `plugin.json`, optional `mcp_config.json`, `hooks.json`, `skills/`, `agents/`, `rules/`.
- CLI lifecycle: `agy plugin install <path> | list | disable <name> | enable <name> | uninstall <name>`.
- IDE skills: workspace `<root>/.agents/skills/<name>/`, with legacy `.agent/skills` still honoured.
- **Documented conflict, unresolved:** global locations differ per page — IDE skills at `~/.gemini/antigravity/skills/`, plugins page at `~/.gemini/config/plugins/`, CLI plugins at `~/.gemini/antigravity-cli/plugins/`. The adapter therefore documents only the workspace path and claims no global installer.

## Implementation revalidation — 2026-08-31

Revalidated against current Antigravity 2.0/IDE and CLI documentation.

- Antigravity needs its own root `plugin.json`; the strict IDE/CLI intersection is `$schema`, `name`, and `description`. It is not the portable Agent Plugins manifest.
- IDE bundles use `skills/`, optional `rules/`, `mcp_config.json`, and `hooks.json`; CLI additionally documents `agents/` and supports `agy plugin list|install|disable|enable|uninstall`.
- Workspace `.agents/skills/braids/SKILL.md` is stable. Official global skill paths and one CLI skill-format page conflict, so no global direct-skill installer is claimed.
- Hooks are command-only and operation-specific. Web/extension parity is not documented, so those surfaces remain unknown.
- Initial adapter ships a strict plugin plus canonical skill only; no workflow, rules, hooks, agents, or MCP.

## Extensibility model

Antigravity currently exposes Agent Skills plus plugins that bundle skills, rules, MCP servers, and hooks. CLI plugin documentation additionally describes agents/background subagents and related configuration.

IDE workspace skills use `.agents/skills/<skill>/`; global skill locations are under the user's Gemini/Antigravity configuration. Plugin layouts use a root `plugin.json`.

## Skill behavior

Skills use progressive disclosure:
- name/description is visible for discovery;
- full instructions are loaded when relevant;
- supporting scripts/resources are used on demand.

Google's guidance emphasizes focused skills, clear descriptions, decision trees, and scripts as bounded tools rather than dumping executable details into prompt instructions.

This aligns directly with Braids' router + references architecture.

## Rules vs workflows vs skills

Antigravity distinguishes:
- **Rules** — persistent/model-decided guidance;
- **Skills** — reusable on-demand expertise;
- **Workflows** — explicit slash-invoked sequences.

Braids methodology belongs in a skill. Guard Mode may use a tiny rule. A workflow can be an optional explicit UX wrapper (`/braids-audit`) but must not become the canonical logic because Braids' path is adaptive rather than a fixed step list.

## Plugins, MCP and hooks

Plugins can group skills/rules/MCP/hooks. MCP is optional for Braids; add it only when a concrete deterministic cross-host capability cannot be supplied by existing tools. Hooks should be used for narrow enforceable policies, never assumed to represent all model activity.

## Adapter acceptance focus

Test:
- workspace/global skill discovery;
- model-decided and explicit invocation;
- rule interaction and precedence;
- plugin package discovery;
- hook behavior;
- IDE versus CLI differences;
- absence of optional MCP;
- token/context behavior when Braids is dormant.

## Braids adapter decision

**Use:** Agent Skill core.  
**Plugin:** thin Antigravity wrapper for distribution and optional rules/hooks.  
**Avoid:** encoding the adaptive engineering method as a fixed Workflow.

## Primary sources

- https://www.antigravity.google/docs/ide/skills/
- https://antigravity.google/docs/plugins/
- https://antigravity.google/docs/cli/plugins/
- https://www.antigravity.google/docs/ide/rules/
- https://www.antigravity.google/docs/ide/workflows/
- https://antigravity.google/docs/hooks/
- https://antigravity.google/docs/subagents/
