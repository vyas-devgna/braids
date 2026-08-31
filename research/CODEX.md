# Braids Host Research — Codex

Research date: 2026-08-31  
Status: pre-development evidence record; recheck before adapter implementation.

## Implementation revalidation — 2026-08-31

Revalidated against current official documentation and local Codex CLI 0.150.1 before adapter implementation.

- Standalone repository skill: `.agents/skills/braids/SKILL.md`; installable desktop/CLI wrapper: `.codex-plugin/plugin.json` with root `skills/`. The installable plugin is not supported by the Codex IDE extension; the standalone skill is.
- Local marketplace flow: `codex plugin marketplace add <root>`, `codex plugin list --available --json`, `codex plugin add braids@<marketplace> --json`, new session, and `codex plugin remove ... --json`. There is no documented `codex plugin validate` command.
- Hooks require separate trust. Hosted WebSearch is outside local hook coverage, `write_stdin` has no second PreToolUse, background hooks cannot block, and parsed `prompt`/`agent` handlers are currently skipped.
- Subagents have separate threads/contexts but inherit parent sandbox/approval; current docs do not promise filesystem/worktree isolation per spawned subagent.
- Initial adapter ships the canonical skill and installable wrapper only. Guard hooks and custom agents remain absent; Guard Mode stays off.

## Native extension surfaces

Codex supports Agent Skills, project/user instruction discovery through `AGENTS.md`, hooks, subagents, tools/MCP, and host execution surfaces. The portable Braids methodology should be delivered as an Agent Skill; project instruction files are suitable only for small activation/policy hints.

## Skill discovery and token behavior

Codex uses progressive skill disclosure: skill metadata is available for discovery, then full skill instructions are loaded when selected. Current Codex documentation also constrains the initial skill-list contribution to avoid crowding the model context.

**Observed 2026-08-31 on 0.150.1**, emitted as a turn item: `Skill descriptions were shortened to fit the skills context budget. Codex can still see every skill, but some descriptions are shorter. Disable unused skills or plugins to leave more room for the rest.` The description *is* Braids' activation classifier, so on a machine with many installed skills Codex may be selecting against a truncated version of it. Trigger measurements must therefore record how many skills were loaded, and a user seeing Braids under-trigger on Codex should disable unused plugins before concluding the description is wrong.

Braids consequence:
- keep the discovery description precise;
- keep the discovery description *short enough to survive truncation*, front-loading the decisive clauses;
- keep the core SKILL.md small;
- put architecture/security/performance/dependency/UX material in references;
- only load a reference when a routed task requires it.

## AGENTS.md

Codex discovers instructions hierarchically, with global/project/nested scopes. This makes `AGENTS.md` appropriate for an **optional Guard Mode activation rule**, not for the complete Braids playbook. Project overrides must be tested because nested instruction scope can change behavior.

## Hooks and enforcement boundary

Codex hooks cover important local tool paths, including shell and patch/tool flows, but official documentation explicitly notes that hosted tools such as WebSearch do not necessarily pass through the same local hook path.

Braids must therefore record hook coverage in `HostCapabilities` and never label Codex hooks a universal security/enforcement boundary. A result such as `deterministic_blocking=true` must be scoped to concrete intercepted operations.

Large hook-generated model context is also a cost risk. Hook output should be terse and preferably machine-decision-oriented.

## Subagents

Current Codex guidance favors subagents for read-heavy parallelism: repository exploration, test discovery, triage, research, independent analysis. Parallel write-heavy workflows introduce coordination/conflict costs and consume more tokens than comparable single-agent work.

Braids mapping:
- D0/D1: normally single agent.
- D2+: Scout may run separately.
- D3/D4: Challenger/Verifier may be isolated if the expected information gain justifies cost.
- parallel implementation is not the default.

## Adapter acceptance focus

Test:
- implicit and explicit skill activation;
- nested AGENTS.md interaction;
- hook coverage and non-coverage;
- local versus hosted tools;
- subagent context isolation;
- worktree/sandbox behavior where available;
- token overhead with Braids dormant and active.

## Braids adapter decision

**Use:** Agent Skill as canonical behavior.  
**Optional:** tiny `AGENTS.md` Guard Mode, hooks for narrow deterministic policies, subagents for read-heavy/falsification work.  
**Avoid:** assuming hooks intercept all actions or spawning a reviewer swarm for ordinary changes.

## Primary sources

- https://learn.chatgpt.com/docs/build-skills
- https://learn.chatgpt.com/docs/hooks
- https://learn.chatgpt.com/docs/agent-configuration/subagents
- https://learn.chatgpt.com/docs/agent-configuration/agents-md
- https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/skill-creator/SKILL.md
- https://developers.openai.com/plugins/build/skills
- https://developers.openai.com/plugins/build/plugins
- https://learn.chatgpt.com/docs/plugins
