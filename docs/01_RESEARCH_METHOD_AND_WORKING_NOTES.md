# Research Method and Working Notes

## Research objective

Determine how reusable AI-agent skills/plugins are currently authored, discovered, activated, packaged, integrated, secured, tested, distributed, and kept context-efficient across major coding-agent hosts; then use that evidence to define Braids before implementation.

## Method

Research was performed against current primary/vendor documentation where available, plus a small number of public open-source precedents. Every architectural conclusion was required to answer one of these questions:

1. What is portable across hosts?
2. What is host-specific?
3. What is deterministic versus model-judgment behavior?
4. What consumes persistent context?
5. What can be progressively loaded?
6. Which capabilities require hooks, subagents, LSP, MCP, shell, web, or isolation?
7. What failure/security boundaries appear when extending the agent?
8. How should the skill itself be tested for activation and behavioral quality?
9. What should Braids reuse rather than implement?

## Working conclusions

### W1 — Agent Skills is the portability floor

The Agent Skills specification defines a `SKILL.md` with optional `scripts/`, `references/`, and `assets/`. It explicitly uses progressive disclosure:
- metadata is loaded at startup (approximately 100 tokens),
- the skill body is loaded only after activation (<5000 tokens recommended),
- supporting resources are loaded as needed,
- the main skill is recommended to stay below 500 lines.

**Consequence:** Braids must be a compact orchestrating skill with detailed reasoning policies in focused references. A monolithic mega-prompt would contradict the dominant skill architecture and increase context cost.

Sources: Agent Skills Specification; Cline Skills; Codex Skill Creator.

### W2 — Portable plugins are intentionally narrow

Agent Plugins v1.0.0 defines exactly two portable component types: **skills and MCP servers**. Rules, hooks, agents, commands, LSP, permissions, distribution UX, and marketplace behavior remain client-specific.

**Consequence:** Braids needs one portable core plus thin host adapters. Host-specific behavior must never leak into the core contract.

Source: Agent Plugins Specification v1.0.0.

### W3 — MCP is optional infrastructure, not a default architecture

MCP is useful when Braids needs a capability not available through the host, but it adds a tool/process/trust/authorization surface. The MCP specification requires consent, authorization discipline, and careful treatment of tools.

**Consequence:** no Braids MCP server in v1 unless a concrete cross-host deterministic capability cannot be delivered through existing host tools.

### W4 — Hooks are useful enforcement, but not universally portable

Claude Code, Cursor, Cline, Codex, and Copilot expose hooks or related interception mechanisms, but event coverage and semantics differ.

**Consequence:** the kernel distinguishes **semantic guardrails** (reasoning and warnings) from **deterministic guardrails** (host hook/policy enforcement). Braids must never claim a deterministic guarantee on a host that cannot enforce it.

### W5 — Persistent rules are not the right place for the methodology

Persistent instructions such as AGENTS.md, Rules, CLAUDE.md, or equivalent are always or frequently loaded. Skills exist specifically to avoid loading full procedures on unrelated tasks.

**Consequence:** optional Guard Mode must be a tiny trigger/router rule, not the full Braids doctrine.

### W6 — Host-native code intelligence should be reused

LSP, repository search, git, compilers, tests, profilers, debuggers, scanners, and browser tools already exist.

**Consequence:** Braids must orchestrate these rather than build its own code index, parser, profiler, scanner, or test runner. Tree-sitter/CodeQL-like escalation is optional and evidence-driven.

### W7 — Large methodology frameworks validate modularity but expose orchestration tax

Ponytail demonstrates a focused methodology distributed across agent hosts. Superpowers demonstrates a broad multi-skill development methodology. Cline's review-team demonstrates specialized review lanes/subagents.

**Consequence:** Braids should expose one coherent primary skill at launch, with internal reference modules and optional subagent roles. Splitting into many public skills is deferred until activation/eval data proves it improves routing.

### W8 — Architecture evaluation should use scenarios and trade-offs, not slogans

ATAM exists because quality attributes conflict. Security, performance, availability, modifiability and other qualities cannot be maximized simultaneously.

**Consequence:** Braids converts vague requests such as "make it robust" into quality scenarios and compares candidate solutions against scenario-linked value and lifecycle burden.

### W9 — Security is cross-cutting

NIST SSDF treats secure software development as integrated into the SDLC rather than a final scanner step.

**Consequence:** user-harm/security constraints operate throughout context acquisition, dependency evaluation, candidate generation, implementation, and verification.

### W10 — Dependencies are outsourced complexity

OpenSSF recommends first deciding whether a dependency is necessary, then evaluating authenticity, maintenance, security, transitive impact and suitability.

**Consequence:** the reuse ladder cannot blindly prefer external OSS. New dependencies need an adoption/exit decision.

### W11 — Skill triggering itself is a product surface

Agent Skills documentation states that the skill description is the primary activation signal. Over-broad descriptions cause false activations; narrow descriptions cause misses.

**Consequence:** Braids needs a dedicated trigger evaluation set before behavioral testing.

## Research uncertainties deliberately retained

- Host plugin APIs change faster than the Agent Skills core. Adapters must be versioned independently.
- Some hosts expose overlapping functionality under different names. Capability detection must be semantic, not brand-name branching.
- Marketplace acceptance/review rules can change without affecting the portable architecture.
- Exact token costs vary by model/host. Braids should measure relative overhead in evals rather than promise fixed savings.
