# Research Synthesis and Precedent Analysis

## Core conclusion

Braids should be developed as a **portable Agent Skill first**, packaged as an Agent Plugin where supported, and enhanced by host-specific adapters only when those adapters add real capability.

The source of truth must not be duplicated across Claude Code, Codex, Cursor, Antigravity, Copilot, Windsurf, OpenCode, and Cline.

## Precedent: Ponytail

Useful principle:
- focused engineering doctrine;
- reusable decision process;
- portable skill/plugin packaging;
- thin host adaptations.

Braids should borrow the structural idea, not the minimalism objective.

Braids differs because its objective is multi-dimensional and context-dependent: correctness, reliability, performance, resource use, security, compatibility, maintainability, operations, developer experience, deployment and user experience.

## Precedent: Superpowers

Useful principle:
- a software-development methodology can be expressed as reusable skills and activated across many harnesses;
- specialized skills can orchestrate a larger process.

Limitation for Braids:
- Braids should not begin as a large visible skill suite. More skills increase discovery metadata, routing ambiguity and maintenance surface. Internal references are cheaper until separate triggers are empirically justified.

## Precedent: Cline review-team

Useful principle:
- independent reviewers can cover different failure classes;
- review roles can be parallelized on capable hosts.

Adaptation:
- define abstract roles (`Scout`, `Challenger`, `Verifier`, `Implementer`) in Braids;
- map them to real subagents only at higher engineering depths and only on hosts that support safe delegation.

## Platform synthesis

### Portable
- `SKILL.md`
- supporting references/scripts/assets
- Agent Plugins `plugin.json`
- optional MCP server configuration

### Non-portable / adapter territory
- persistent rules/instructions
- hooks
- subagents
- commands
- permission models
- worktree/sandbox behavior
- LSP plugin configuration
- marketplace metadata
- UI variables and plugin-specific settings

## Architectural pattern

**Hexagonal/ports-and-adapters style**

Core:
- engineering methodology;
- state contracts;
- evidence semantics;
- risk/depth semantics;
- stop rules;
- output contract.

Ports:
- repository search;
- semantic code intelligence;
- web research;
- shell/build/test;
- profiling;
- security tooling;
- subagent delegation;
- user authorization;
- persistent guard activation.

Adapters:
- Claude Code
- Codex
- Cursor
- Antigravity
- Copilot
- Windsurf
- OpenCode
- Cline
- generic Agent Skills host

This prevents host API churn from contaminating the engineering methodology.
