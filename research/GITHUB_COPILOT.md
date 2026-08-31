# Braids Host Research — GitHub Copilot

Research date: 2026-08-31  
Status: pre-development evidence record; recheck before adapter implementation.

## Implementation revalidation — 2026-08-31

Revalidated against local GitHub Copilot CLI 1.0.82.

- Skill discovery on the CLI surface: project `.github/skills/`, `.agents/skills/`, `.claude/skills/`; personal `~/.copilot/skills/` or `~/.agents/skills/`; plugin bundles; and directories registered with `copilot skill add`.
- `copilot skill add <dir>` writes an absolute path into `~/.copilot/settings.json` `skillDirectories`. `copilot skill remove` requires that directory path — the bare skill name is rejected.
- Plugins install from `plugin@marketplace`, `owner/repo`, `owner/repo:path`, or a git URL. `copilot --plugin-dir <dir>` loads a local plugin, and `copilot plugin list --plugin-dir <dir>` lists it without installing.
- `copilot plugins` inspects plugins, MCP servers, skills, instructions and language servers by kind and scope, with `--plugin` / `--skill` selectors on remove/enable/disable.
- `--add-dir` loads a directory's `.github/skills` and `.github/agents` as *trusted* configuration; that is a deliberate trust decision, not a default.
- The cloud agent still runs in an ephemeral environment that does not inherit local user plugins or skills, so `copilot-cli` and `copilot-cloud` remain separate profiles and the cloud profile is unexercised.

## Plugin surface

GitHub Copilot plugins can currently package:
- custom agents;
- skills;
- hooks;
- MCP server configuration;
- LSP server configuration.

A root `plugin.json` is the package identity. Plugins can be installed from marketplaces, repositories, or local paths depending on client.

## Important execution split: CLI vs cloud agent

Braids must treat Copilot CLI and Copilot cloud agent as different capability profiles.

The cloud agent runs in an ephemeral Linux environment and repository hook configuration is materially different from local CLI/user/plugin configuration. User-local plugins/configuration cannot simply be assumed to exist in cloud execution.

This is a textbook case for Braids' Capability Negotiator.

## Hooks

Copilot supports hook interception at defined lifecycle/tool events, but availability and scope vary by execution surface. Pre-tool behavior can deny some operations. Permission-request semantics are not identical across CLI and cloud.

Do not publish one blanket `copilotHooks=true`; represent capabilities at event/surface granularity.

## Skills and custom agents

Skills are the portable methodology layer. Custom agents are an optional way to map Challenger/Verifier roles, especially for larger repository/PR workflows. They are not required for the initial product.

## Distribution

Because Copilot plugins are packaged/distributed units, the Braids release process should validate:
- manifest/package schema;
- skill discovery;
- local CLI execution;
- repository-hosted/cloud behavior;
- absence of local user assumptions;
- hook policy behavior;
- marketplace/install path.

## Braids adapter decision

**Use:** portable skill/plugin core.  
**Optional:** Copilot agents, hooks, MCP/LSP declarations when they buy concrete capability.  
**Separate profiles:** `copilot-cli` and `copilot-cloud`.

## Primary sources

- https://docs.github.com/en/copilot/concepts/agents/about-plugins
- https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-creating
- https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference
- https://docs.github.com/en/copilot/reference/hooks-reference
- https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/use-hooks
