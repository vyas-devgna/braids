<p align="center">
  <img src="assets/hero/braids-hero.png" alt="Braids" width="760">
</p>

<h1 align="center">Braids</h1>

<p align="center">
  Adaptive engineering governance for AI coding agents.<br>
  <strong>Enough engineering for the real risk—no more, no less.</strong>
</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-2f6f63"></a>
  <a href="https://github.com/vyas-devgna/braids/actions/workflows/ci.yml"><img alt="Conformance" src="https://github.com/vyas-devgna/braids/actions/workflows/ci.yml/badge.svg"></a>
  <img alt="Status: experimental" src="https://img.shields.io/badge/status-experimental-c58b2b">
</p>

Braids helps coding agents choose the lowest total lifecycle burden that still satisfies the real requirements, quality scenarios, hard constraints, and acceptable residual risk. It rejects both under-engineering and architecture-for-show.

> Complexity is a cost. Require it to purchase scenario-linked value. “No change” is a valid result.

## Why Braids

| Ordinary agent tendency | Braids response |
|---|---|
| Treat every task as roughly equal | Routes work from **D0** local/mechanical to **D4** critical/irreversible |
| Optimize before finding a bottleneck | Requires a target and suitable evidence |
| Change the named file and miss callers | Expands context only when the change surface demands it |
| Add dependencies as shortcuts | Prices security, maintenance, transitives, portability, and exit cost |
| Call passing tests “production-ready” | Maps each material claim to the evidence that can prove it |
| Keep polishing after the task is solved | Stops when further work costs more than its expected value |

Braids is a portable [Agent Skill](skills/braids/SKILL.md), not a prompt demo or remote service. It has no runtime dependency, mandatory MCP server, production telemetry, or hidden project state.

## Install

### Claude Code

```sh
claude plugin marketplace add vyas-devgna/braids
claude plugin install braids@braids
```

Verify with `claude plugin details braids`.

### Codex CLI and desktop

```sh
codex plugin marketplace add https://github.com/vyas-devgna/braids
codex plugin add braids@braids --json
```

The Codex IDE extension does not load installable plugins. For the IDE, copy `skills/braids` to `<project>/.agents/skills/braids`.

### Other Agent Skills hosts

Copy `skills/braids` to the host’s documented project or user skill directory. Host-specific commands, limitations, and acceptance evidence live under [`adapters/`](adapters/).

## Use

Braids is selected automatically when the task involves architecture, security, auth, data integrity, failure handling, concurrency, performance, dependencies, deployment, cross-module impact, or evidence-sensitive claims.

Invoke it explicitly when you want certainty:

```text
Use Braids to review this migration plan and identify the smallest justified design.
```

```text
Use Braids before changing this authorization check. Preserve security and explain the minimum safe alternative.
```

The method progressively loads only the references relevant to the task. Claude Code 2.1.248 currently reports about **280 always-on tokens** and **2.8k tokens when invoked**.

## Engineering depth

| Depth | Typical work | Default treatment |
|---|---|---|
| D0 | Safe, local, reversible | Direct change; no research or delegation |
| D1 | Routine bounded change | Targeted context and checks |
| D2 | Cross-module or platform-sensitive | Explicit change-surface model and broader verification |
| D3 | Security, reliability, concurrency, measured performance | Threat/failure analysis and stronger evidence |
| D4 | Irreversible, mission-critical, hard to recover | Staged decision, migration, rollback, recovery |

## Status

Braids is usable today but remains **experimental**. It is advisory on every host: it reasons about unsafe changes but ships no hooks and enforces nothing. A clean Codex smoke run observed 3/3 expected activations and 1/1 expected dormancy; the complete 92-case behavioral suite is not yet graded.

Read the exact boundaries in [Known Limitations](docs/29_KNOWN_LIMITATIONS.md). A present adapter is not itself a support claim.

## Validate and develop

```sh
python3 scripts/validate.py
python3 scripts/run_evals.py --fixture-tests
python3 scripts/measure_budget.py
python3 -m unittest discover -s tests
python3 scripts/build_adapters.py --dist dist
```

The repository contains 92 evaluation cases, eight fixture families, Draft 2020-12 contracts, and eight thin host adapters generated from one semantic source of truth.

## Documentation

- [Documentation map](docs/00_INDEX.md)
- [Product requirements](docs/03_PRODUCT_REQUIREMENTS_PRD.md)
- [Architecture](docs/04_ARCHITECTURE_FREEZE.md)
- [Security threat model](docs/10_SECURITY_THREAT_MODEL.md)
- [Evaluation strategy](docs/12_EVALUATION_STRATEGY.md)
- [Requirements traceability](docs/28_REQUIREMENTS_TRACEABILITY_MATRIX.md)
- [Known limitations](docs/29_KNOWN_LIMITATIONS.md)
- [Host research](research/00_INDEX.md)

## Contributing and security

Contributions are welcome; read [CONTRIBUTING.md](CONTRIBUTING.md) before changing normative behavior. Report vulnerabilities privately through GitHub’s security advisory flow as described in [SECURITY.md](SECURITY.md).

Brand artwork and usage notes live in [`assets/`](assets/README.md). No runtime behavior depends on them.

## License

[MIT](LICENSE) © 2026 Vyas Devgna.
