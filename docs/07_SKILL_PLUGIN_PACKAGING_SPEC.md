# Skill and Plugin Packaging Specification

## Canonical source

`skills/braids/SKILL.md` is the portable orchestration entrypoint.

Recommended target:
- metadata: precise activation description;
- body: ideally 1500-3000 tokens, hard ceiling below the Agent Skills <5000-token recommendation;
- references: one level deep;
- scripts: deterministic helpers only.

## Proposed skill tree

```text
skills/braids/
├── SKILL.md
├── references/
│   ├── contract.md
│   ├── context.md
│   ├── system-model.md
│   ├── quality-scenarios.md
│   ├── risk-depth.md
│   ├── evidence-research.md
│   ├── reuse-dependencies.md
│   ├── security-user-harm.md
│   ├── performance-resources.md
│   ├── ux-developer-experience.md
│   ├── verification.md
│   ├── reporting.md
│   └── host-capabilities.md
└── scripts/
    ├── validate-braids
    └── inspect-capabilities
```

Reference files must be independently loadable. Avoid reference-to-reference chains.

## Portable Agent Plugin

Root:
- `plugin.json`
- `skills/braids/...`
- no mandatory `mcp.json` in v1

Agent Plugins v1 permits exactly Skills and MCP servers as portable component types. Host-specific components belong in client extension structures or separate adapter packaging.

## Description design

The description is the activation classifier.

Must include:
- what Braids does;
- when to invoke it;
- positive triggers: architecture, implementation planning, cross-module changes, reliability, performance, resource optimization, edge cases, fallbacks, integration, production readiness, audit, engineering review;
- negative boundaries: trivial spelling/comment/format-only edits unless explicitly requested.

Description quality must be evaluated independently from workflow quality.

## Scripts policy

Add a script only if:
- deterministic execution improves reliability;
- it saves significant repeated model reasoning;
- it is portable or adapter-scoped appropriately;
- dependencies are minimal and documented;
- failure behavior is explicit.

Do not turn Braids into a CLI framework prematurely.

## Assets policy

No decorative assets in the runtime skill.
Brand assets may exist at repository root/distribution metadata but should not enter model context.

**Implemented 2026-08-31.** The asset pack lives at `assets/` and is enforced, not merely documented: `scripts/validate.py` fails on any image outside `assets/`, apart from a single file an adapter may stage under `adapters/<host>/files/` for a host manifest that documents a logo field.

Only one host qualifies. Cursor documents a `logo` field taking a relative path, so its package carries the 256 px icon (59 KB). Claude Code 2.1.248 rejects both `icon` and `logo` as unknown fields under `plugin validate --strict`, in the plugin manifest and the marketplace manifest alike, so no asset is added there. Codex, Antigravity, OpenCode, Copilot, Cline and Windsurf packages carry no asset.

## Host adapter generation

Prefer generated or templated adapter manifests from a single metadata source to avoid:
- version drift;
- inconsistent descriptions;
- inconsistent licensing;
- outdated host capability claims.

## Versioning

Separate:
- Braids methodology version;
- portable package version;
- each host adapter compatibility version.

A host adapter may require a patch release without changing the core methodology.

## Distribution

Phase order:
1. source repository install/manual skill copy;
2. local plugin installs;
3. third-party/community marketplaces;
4. official marketplaces after conformance maturity.

Do not optimize for marketplace acceptance before behavioral quality is established.
