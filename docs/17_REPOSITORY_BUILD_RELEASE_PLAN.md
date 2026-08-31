# Repository, Build and Release Plan

## Proposed repository

```text
braids/
├── README.md
├── LICENSE
├── SECURITY.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── plugin.json                     # portable Agent Plugin manifest
├── skills/
│   └── braids/
│       ├── SKILL.md
│       ├── references/
│       └── scripts/
├── adapters/
│   ├── claude-code/
│   ├── codex/
│   ├── cursor/
│   ├── antigravity/
│   ├── copilot/
│   ├── windsurf/
│   ├── opencode/
│   └── cline/
├── schemas/
├── evals/
│   ├── trigger/
│   ├── kernel/
│   ├── repositories/
│   ├── adversarial/
│   └── cross-host/
├── fixtures/
├── scripts/
│   ├── validate/
│   ├── build-adapters/
│   └── run-evals/
├── docs/
│   ├── architecture/
│   ├── decisions/
│   └── development/
└── .github/
    └── workflows/
```

## Single source of truth

Core behavior exists only in `skills/braids`.
Adapters may:
- package it;
- add host-native activation;
- add host-native guards/delegation;
- expose UI/commands.

Adapters may not fork the methodology text.

## Build

Build step should:
1. validate skill;
2. validate portable manifest;
3. generate/check adapter metadata;
4. ensure versions align;
5. ensure no absolute/path-escaping references;
6. run static package/security checks;
7. produce per-host archives where useful;
8. emit manifest of hashes.

## CI before behavioral eval maturity

- formatting/lint for scripts;
- JSON/YAML/schema validation;
- shellcheck where applicable;
- unit tests for deterministic scripts;
- secret scanning;
- dependency audit if runtime dependencies exist;
- package conformance.

## Release channels

- `edge`: development snapshots.
- `beta`: conformance-complete, field testing.
- `stable`: accepted v1 quality threshold.

## Supply-chain policy

Prefer no runtime dependencies for the core skill.
If build tooling requires dependencies, keep them dev-only when possible.
Pin CI actions/tools appropriately.
Generate release artifacts from tagged source.

## Marketplace strategy

Do not create divergent marketplace repos unless a host requires them.
Prefer one canonical repository with platform manifests/adapters.
Official marketplace submissions occur only after local/community validation.

## Backward compatibility

Core skill behavior follows semantic versioning conceptually:
- patch: wording/eval fixes without intentional contract change;
- minor: additive behaviors/references/host capability;
- major: methodology/output contract changes.

Adapter compatibility versions can move independently.
