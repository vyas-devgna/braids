# Portability Research — What Braids Can and Cannot Standardize

Research date: 2026-08-31

## Interoperability floor

The current portable floor is **Agent Skills** for methodology/instructions and **Agent Plugins v1** for distributable skills plus optional MCP servers.

Agent Plugins v1.0.0 intentionally standardizes only two component types:
1. Agent Skills
2. MCP server declarations

Rules, hooks, agents/subagents, commands, LSP declarations, permission systems, monitors and marketplace metadata remain client-specific extensions.

## Consequence for Braids

Braids must have exactly one semantic source of truth:
- the portable Braids skill;
- versioned reference modules;
- machine-readable state/evaluation contracts.

Host adapters are allowed to:
- expose commands;
- install tiny persistent Guard Mode rules;
- map logical roles to subagents;
- install narrow hooks;
- declare LSP/MCP integrations;
- package marketplace metadata.

Host adapters are **not** allowed to redefine the engineering method.

## Capability negotiation over host-name branching

Wrong:
`if host == "cursor": assume hooks + cloud VM + subagents`

Correct:
discover/declare:
- whether skill auto-invocation exists;
- which instructions are persistent;
- which hook events are covered;
- local/cloud/hosted execution surface;
- shell/read/write/network/browser availability;
- code-intelligence availability;
- isolation/worktree support;
- subagent support and cost;
- permission/enforcement semantics.

This makes Braids robust to product updates and partial environments.

## Semantic vs deterministic guarantees

Portable semantic guarantee:
- Braids can reason that a requested change is unsafe, unsupported or poorly engineered and recommend/choose a safer design within user authority.

Non-portable deterministic guarantee:
- a hook/permission system may block a specific operation before execution.

Documentation and reports must never collapse those two concepts.

## Progressive disclosure

Agent Skills specifies a three-stage model:
- small metadata at discovery;
- full SKILL.md on activation;
- resources on demand.

Braids should therefore treat context budget as architecture:
- main SKILL.md contains router and invariants;
- detailed doctrine goes to references;
- references stay focused and shallow;
- scripts perform deterministic work without forcing implementation details into the prompt.

## Sources

- https://agentskills.io/specification
- https://agentskills.io/skill-creation/optimizing-descriptions
- https://agent-plugins.org/specification
- https://prod.cursor.com/docs/reference/plugins
- https://docs.github.com/en/copilot/concepts/agents/about-plugins
