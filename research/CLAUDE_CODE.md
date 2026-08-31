# Braids Host Research — Claude Code

Research date: 2026-08-31  
Status: pre-development evidence record; recheck before adapter implementation.

## Implementation revalidation — 2026-08-31

Revalidated against current official documentation and local Claude Code 2.1.248 before adapter implementation.

- Installable wrapper: `.claude-plugin/plugin.json`; components remain at plugin root (`skills/`, optional `agents/`, `hooks/hooks.json`, `.mcp.json`, `.lsp.json`). Plugin-root `CLAUDE.md` is not loaded.
- Local gate: `claude plugin validate <path> --strict`, then `claude --plugin-dir <path>`; `/reload-plugins` reloads changes.
- `PreToolUse` can deny only matched/tested tool paths. `EndConversation` skips Pre/PostToolUse; asynchronous and after-the-fact events are not blocking guarantees.
- Plugin agents ignore agent-declared hooks, MCP servers, and permission mode. Session/plugin hooks still apply. Worktrees isolate working files but share `.git`, project plugins, and approvals.
- Disable/uninstall must prove components are no longer loaded; inert cache versions can remain for about 14 days.
- Initial adapter therefore ships the canonical skill wrapper only. Guard hooks and agents remain absent until their marginal value and exact coverage are tested.

## Skill selection competes with built-ins — observed 2026-08-31

Claude Code ships built-in skills (`code-review`, `debug`, `simplify`, `run`, and others). A plugin skill competes with them by description alone, and a built-in whose *name* matches the user's phrasing tends to win: "Review the last commit" selected the built-in `code-review` over `braids-review`. The core `braids` skill does auto-activate on risk-shaped prompts, because no built-in claims that territory.

Consequence for the adapter: skills that overlap a built-in's name should be documented as explicitly invoked on this host rather than advertised as automatic.

## Native extension surfaces

Claude Code currently supports standalone `.claude/` configuration and distributable plugins. A plugin can contain:
- `skills/<name>/SKILL.md`
- `agents/`
- `hooks/hooks.json`
- `.mcp.json`
- `.lsp.json`
- `monitors/`
- optional root `settings.json`
- optional `.claude-plugin/plugin.json`

Plugin skills are namespaced. The official development path supports direct local loading with `claude --plugin-dir ./plugin`, live reloading with `/reload-plugins`, validation with `claude plugin validate`, and marketplace distribution.

## Skill discovery and context behavior

Agent Skills are model-invoked based primarily on skill metadata/description. Detailed instructions and supporting references should be progressively disclosed. Claude also supports manual-only skills (`disable-model-invocation: true`), which is useful for explicit Braids modes that should not auto-trigger.

Persistent `CLAUDE.md`/settings are appropriate only for a tiny optional Braids Guard Mode. The full Braids methodology must not be placed in persistent project instructions because it would consume context on unrelated turns.

## Hooks and enforcement

Hooks are useful for deterministic policy around defined lifecycle/tool events. They should be treated as an adapter capability rather than part of Braids' portable semantic kernel.

Braids should distinguish:
- semantic safety: model evaluates whether a design is unsafe or harmful;
- deterministic policy: a host hook blocks a known class of dangerous operation.

Do not imply that semantic review or hooks make Claude Code a complete security boundary.

## Subagents and isolation

Claude Code supports custom subagents and worktree isolation. Braids may map logical roles to:
- Scout — read-only discovery/research
- Challenger — falsification/adversarial review
- Verifier — claim verification
- Implementer — write path after user authority is resolved

These must remain optional. Low-risk tasks should stay single-agent. Plugin-shipped agents have security-related limitations: plugin agent definitions do not own all session-level hook/MCP/permission configuration, so enforcement must remain at the plugin/session layer.

## LSP / semantic code intelligence

Claude plugins can configure LSP servers. Braids should use an already available language server before introducing a new parser/indexer. Custom LSP packaging is justified only for unsupported languages or a concrete semantic capability gap.

## Local development and release

Recommended adapter workflow:
1. author the portable Braids skill first;
2. create Claude-specific plugin wrapper;
3. load with `--plugin-dir`;
4. test skill trigger/non-trigger cases;
5. test every hook independently;
6. test subagents and worktree behavior separately;
7. run `claude plugin validate --strict` before release;
8. test install from the same packaging path users will use;
9. submit only after cross-host core conformance passes.

## Braids adapter decision

**Use:** portable SKILL.md + thin Claude plugin adapter.  
**Optional:** Guard Mode, hooks, Scout/Challenger/Verifier agents, LSP integration.  
**Avoid:** making Claude-specific constructs part of the core decision protocol.

## Primary sources

- https://code.claude.com/docs/en/plugins
- https://code.claude.com/docs/en/plugins-reference
- https://code.claude.com/docs/en/skills
- https://code.claude.com/docs/en/hooks-guide
- https://code.claude.com/docs/en/sub-agents
- https://code.claude.com/docs/en/worktrees
- https://code.claude.com/docs/en/plugin-marketplaces
- https://code.claude.com/docs/en/memory
- https://code.claude.com/docs/en/discover-plugins
