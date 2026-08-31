# Architecture Freeze — Braids v3

## Architecture decision

Braids will use a **host-neutral adaptive engineering kernel + ports/adapters integration architecture**.

<!-- diagram:01-braids-system-architecture -->
```mermaid
flowchart TB
    U["User task / idea / review / implementation"] --> HC

    subgraph PORT["Host integration layer"]
      HC["M0 Capability Negotiator<br/>detect actual host capabilities"]
      GA["Optional Guard Adapter<br/>persistent rule / hook only where supported"]
      HA["Thin Host Adapter<br/>maps portable roles to native features"]
    end

    HC --> EC
    HC --> HA
    HA --> GA

    subgraph CORE["Portable Braids Kernel"]
      EC["M1 Engineering Contract<br/>goal • authority • scope • scale • environments • success criteria"]
      CA["M2 Progressive Context Acquisition<br/>retrieve only decision-changing context"]
      SM["M3 System & Change-Surface Model<br/>modules • callers • state • trust • process/network/deploy boundaries"]
      QS["M4 Quality Scenario Compiler<br/>stimulus • environment • artifact • response • measurable criterion"]
      RR["M5 Risk / Engineering-Depth Router<br/>blast radius • severity • uncertainty • recoverability • reversibility"]
      EM["M6 Evidence Manager<br/>local evidence first; targeted external research"]
      DG["M7 Reuse / Dependency Gate<br/>existing → stdlib → platform → installed → proven OSS → custom"]
      CS["M8 Candidate Synthesizer<br/>baseline + genuinely distinct viable alternatives"]
      HG["M9 Hard Constraint / User-Harm Gate<br/>security • privacy • integrity • destructive safety • explicit compatibility"]
      TA["M10 Trade-off & Lifecycle Analysis<br/>quality value vs implementation/runtime/ops/maintenance burden"]
      DR["M11 Engineering Decision Record"]
      AUTH{"Implementation authorized?"}
      EX["M12 Controlled Execution<br/>smallest justified blast radius"]
      VE["M13 Claim-Driven Verification<br/>every material claim maps to evidence"]
      SC{"M14 Stop Controller<br/>requirements + evidence + acceptable residual risk?"}
      RP["M15 Concise Braids Verdict"]
    end

    EC --> CA --> SM --> QS --> RR --> EM --> DG --> CS --> HG --> TA --> DR --> AUTH
    AUTH -->|"no"| RP
    AUTH -->|"yes"| EX --> VE --> SC
    SC -->|"context missing"| CA
    SC -->|"evidence missing"| EM
    SC -->|"done"| RP

    subgraph STATE["Session Decision State"]
      ST["EngineeringContract • AssumptionRegister • HostCapabilities<br/>SystemModel • QualityScenarios • RiskRegister • EvidenceLedger<br/>CandidateSet • DecisionRecord • VerificationClaims • ResidualRiskRegister"]
    end

    ST -.-> EC
    ST -.-> SM
    ST -.-> EM
    ST -.-> TA
    ST -.-> VE

    subgraph TOOL["Existing host/dev tools"]
      TL["filesystem • git • grep/search • compiler • tests • LSP • debugger<br/>profiler • browser • CI • web • scanners • optional MCP"]
    end

    TL --> CA
    TL --> EM
    TL --> VE
```

## Layer 1 — Portable methodology

Delivered as Agent Skills-compatible content:
- compact `SKILL.md`;
- focused `references/`;
- deterministic helper `scripts/` only where they outperform LLM reasoning;
- optional `assets/` only for output templates.

The kernel has no hard dependency on MCP, hooks, subagents, LSP, web access or a server.

## Layer 2 — Capability abstraction

Before using optional behaviors, Braids establishes `HostCapabilities`.

Capabilities are semantic:
- persistent instruction available?
- hook interception available?
- shell?
- write access?
- web?
- LSP?
- isolated subagent?
- worktree/sandbox?
- policy/approval controls?

No core decision is written as `if host == Cursor`.

## Layer 3 — Host adapters

Adapters map semantic capabilities to host-native surfaces:
- Claude Code plugin components;
- Codex plugin/skills/hooks/AGENTS/subagents;
- Cursor Agent Plugin or Cursor Plugin features;
- Antigravity Skill/Rule/Workflow/plugin;
- Copilot plugin components;
- Windsurf Skill/Rule/Workflow;
- OpenCode skill/agent/permissions;
- Cline skill/rules/hooks.

## Layer 4 — Optional deterministic tooling

Only added when justified:
- validation scripts;
- manifest builders;
- conformance checks;
- host adapter generation;
- possibly an MCP server in a later release if a concrete cross-host deterministic need emerges.

## Runtime lifecycle

<!-- diagram:03-runtime-decision-flow -->
```mermaid
flowchart TD
    A["Task"] --> B{"Material requirement unknown?"}
    B -->|"yes, discoverable"| C["Inspect / research / test"]
    B -->|"yes, not discoverable"| D["Ask user"]
    B -->|"no"| E["Build minimum sufficient system model"]
    C --> E
    D --> E
    E --> F["Compile relevant quality scenarios"]
    F --> G["Classify engineering depth D0-D4"]
    G --> H{"Would external evidence materially change decision?"}
    H -->|"yes"| I["Targeted research"]
    H -->|"no"| J["Reuse/dependency gate"]
    I --> J
    J --> K["Generate baseline + viable candidates"]
    K --> L["Eliminate hard-constraint violations"]
    L --> M["Compare trade-offs / lifecycle burden"]
    M --> N["Decision"]
    N --> O{"Authorized to implement?"}
    O -->|"no"| P["Report"]
    O -->|"yes"| Q["Implement"]
    Q --> R["Verify material claims"]
    R --> S{"Stop criteria satisfied?"}
    S -->|"no"| E
    S -->|"yes"| P
```

1. Capability negotiation
2. Engineering contract
3. Progressive context acquisition
4. System/change-surface model
5. Quality scenarios
6. Risk/depth routing
7. Evidence/research
8. Reuse/dependency evaluation
9. Candidate generation
10. Hard constraints
11. Trade-offs/lifecycle burden
12. Decision record
13. authorization
14. controlled execution
15. claim-driven verification
16. stop controller
17. concise verdict

## Engineering depth

D0: trivial/local/reversible.
D1: routine bounded engineering.
D2: cross-module/platform-sensitive.
D3: security/data/performance/reliability/high-consequence.
D4: large-scale/irreversible/mission-critical.

Depth determines analysis/research/verification intensity, not line count.

## Architectural invariants

- No silent material assumptions.
- No external research without decision value.
- No dependency without adoption cost analysis when material.
- No claim of "faster", "safer", "compatible", "robust", etc. without corresponding evidence class.
- No automatic scope expansion.
- No deterministic safety claim without deterministic host enforcement.
- No mandatory persistence.
- No recursive self-improvement loop without authorization and a stop condition.
- Existing solution may be the correct answer; Braids must be able to recommend no change.

## Why this architecture is frozen

It matches the current ecosystem split: Agent Skills are broadly portable, while hooks/rules/agents/LSP remain host-specific. Agent Plugins v1 explicitly preserves that boundary. This architecture therefore minimizes duplication and survives host API churn better than separate implementations.
