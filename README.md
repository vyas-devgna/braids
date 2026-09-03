<p align="center">
  <img src="https://raw.githubusercontent.com/vyas-devgna/braids/main/assets/hero/braids-hero.png" alt="Braids" width="760">
</p>

<h1 align="center">Braids</h1>

<p align="center">
  Safer changes from AI coding agents, without unnecessary ceremony.<br>
  <strong>Braids matches the work to the risk.</strong>
</p>

<p align="center">
  <a href="https://braids.vyasdevgna.online"><img alt="Site" src="https://img.shields.io/badge/site-braids.vyasdevgna.online-2f6f63"></a>
  <a href="https://github.com/vyas-devgna/braids/blob/main/LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-2f6f63"></a>
  <a href="https://github.com/vyas-devgna/braids/actions/workflows/ci.yml"><img alt="Conformance" src="https://github.com/vyas-devgna/braids/actions/workflows/ci.yml/badge.svg"></a>
  <img alt="Status: experimental" src="https://img.shields.io/badge/status-experimental-c58b2b">
</p>

Braids helps coding agents tell the difference between a harmless rename and a one-line change that could break authentication. Small, reversible work stays small. Risky work gets the checks, failure analysis, and evidence it deserves.

> Complexity is a cost. Require it to purchase scenario-linked value. “No change” is a valid result.

## What changes when Braids is installed?

| Without Braids | With Braids |
|---|---|
| Treat every task as roughly equal | Matches effort to consequence, from **D0** local/mechanical to **D4** critical/irreversible |
| Optimize before finding a bottleneck | Requires a target and suitable evidence |
| Change the named file and miss callers | Expands context only when the change surface demands it |
| Add dependencies as shortcuts | Prices security, maintenance, transitives, portability, and exit cost |
| Call passing tests “production-ready” | Maps each material claim to the evidence that can prove it |
| Keep polishing after the task is solved | Stops when further work costs more than its expected value |

Braids is a set of portable [Agent Skills](https://github.com/vyas-devgna/braids/blob/main/skills/braids/SKILL.md). It runs inside your coding agent: no remote service, mandatory MCP server, production telemetry, or hidden project state.

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

### Cursor

```sh
git clone https://github.com/vyas-devgna/braids ~/.cursor/plugins/local/braids
```

### Any other Agent Skills host

```sh
npx github:vyas-devgna/braids <host>          # opencode, cline, windsurf, copilot, antigravity, agents
npx github:vyas-devgna/braids opencode --user # install for you rather than this project
npx github:vyas-devgna/braids opencode --uninstall
```

The installer copies the skills into that host's documented skill directory. Run it with no host to see the list. For the published prerelease, use `npx braids-skill@next <host>`. Host-specific commands, limitations, and acceptance evidence live under [`adapters/`](https://github.com/vyas-devgna/braids/tree/main/adapters).

## Use

Braids selects itself on work involving architecture, security, auth, data integrity, failure handling, concurrency, performance, dependencies, deployment, cross-module impact, or evidence-sensitive claims. You can also call it directly.

| Skill | Slash command | Use it for |
|---|---|---|
| `braids` | `/braids` | The method. Right-sizes any change and holds claims to evidence. |
| `braids-review` | `/braids-review` | A diff, branch, or PR: what breaks, what is unproven, what costs more than it buys. On Claude Code, name it — the built-in `code-review` skill wins generic "review this" phrasing. |
| `braids-audit` | `/braids-audit` | A whole repository: ranked engineering-risk surface when there is no diff. |
| `braids-risk` | `/braids-risk` | Adversarial pre-mortem: assume it shipped and caused an incident. |
| `braids-claims` | `/braids-claims` | Claim ledger: every "faster" or "secure" mapped to the evidence for it. |
| `braids-depth` | `/braids-depth` | Set the implementation threshold, or ask why a task got its depth. |
| `braids-help` | `/braids-help` | Reference card. |

### How hard should it work?

Two dials. **Depth** (D0–D4) is routed from risk automatically. **Threshold** is yours:

```text
braids low     smallest change that works, obvious check only
braids high    production shape: failure paths, callers, regression tests  (default)
braids ultra   hostile cases too: partial failure, retry, concurrency, upgrade,
               scale, corrupt state, outage — plus evidence for every claim
```

Threshold caps effort; risk sets the floor on care. `low` is honoured without a lecture — except where the change would weaken security, authorization, privacy, data integrity, a destructive or irreversible operation, or a compatibility guarantee. There Braids names in one sentence what `low` would skip and does the smallest safe version. Threshold never changes what may be *claimed*: unverified stays unverified at every level.

```text
Use Braids to review this migration plan and identify the smallest justified design.
braids ultra — I am about to change how sessions are authorized.
braids low — just make this test pass, don't redesign anything.
```

### Cost

Braids loads only the references a task routes to. On 2026-09-03, Claude Code 2.1.248 projected **~870 tokens always-on** across all seven skills and **~3.9k when the 3.1.0 core skill fires**. These are host estimates, not measured runtime usage.

## Engineering depth

| Depth | Typical work | Default treatment |
|---|---|---|
| D0 | Safe, local, reversible | Direct change; no research or delegation |
| D1 | Routine bounded change | Targeted context and checks |
| D2 | Cross-module or platform-sensitive | Explicit change-surface model and broader verification |
| D3 | Security, reliability, concurrency, measured performance | Threat/failure analysis and stronger evidence |
| D4 | Irreversible, mission-critical, hard to recover | Staged decision, migration, rollback, recovery |

## Status

Braids is usable today but remains **experimental**. It is advisory on every host: it reasons about unsafe changes but ships no hooks and enforces nothing.

Small activation controls passed on **both** Claude Code 2.1.248 and Codex 0.150.1. Measuring two high-severity *kernel* cases at four runs each then showed the opposite of what those controls suggested: activation, not depth routing, was the weak half — Braids fired on 3/8 runs, and routed depth correctly whenever it did fire. Rewriting the skill description moved that to **7/8**, with the irreversible-migration case activating 4/4 and routing D4 4/4. One gap stays open: the unmeasured-claim case still self-reports a depth below the D3 floor even though its behaviour is right.

That is eight runs on two cases on one host — a directional signal, not a trigger rate. The 0.90/0.10 release thresholds remain unmet and unclaimed, the near-miss corpus has not been re-run against the new description, the complete 100-case suite is not yet graded, and the six focused skills added alongside the core have no graded runs yet. Method and scope limits: [`evals/results/README.md`](https://github.com/vyas-devgna/braids/blob/main/evals/results/README.md).

Read the exact boundaries in [Known Limitations](https://github.com/vyas-devgna/braids/blob/main/docs/29_KNOWN_LIMITATIONS.md). A present adapter is not itself a support claim.

## Validate and develop

```sh
python3 scripts/validate.py
python3 scripts/run_evals.py --fixture-tests
python3 scripts/measure_budget.py
python3 -m unittest discover -s tests
python3 scripts/build_adapters.py --dist dist
```

The repository contains 100 evaluation cases, eight fixture families, Draft 2020-12 contracts, and eight thin host adapters generated from one semantic source of truth.

## Documentation

- [Skills reference](https://github.com/vyas-devgna/braids/blob/main/docs/30_SKILLS_REFERENCE.md) — what each skill does and what it costs
- [Distribution](https://github.com/vyas-devgna/braids/blob/main/docs/31_DISTRIBUTION.md) — installing, releasing, and why Braids is not in a marketplace yet
- [Documentation map](https://github.com/vyas-devgna/braids/blob/main/docs/00_INDEX.md)
- [Product requirements](https://github.com/vyas-devgna/braids/blob/main/docs/03_PRODUCT_REQUIREMENTS_PRD.md)
- [Architecture](https://github.com/vyas-devgna/braids/blob/main/docs/04_ARCHITECTURE_FREEZE.md)
- [Security threat model](https://github.com/vyas-devgna/braids/blob/main/docs/10_SECURITY_THREAT_MODEL.md)
- [Evaluation strategy](https://github.com/vyas-devgna/braids/blob/main/docs/12_EVALUATION_STRATEGY.md)
- [Requirements traceability](https://github.com/vyas-devgna/braids/blob/main/docs/28_REQUIREMENTS_TRACEABILITY_MATRIX.md)
- [Known limitations](https://github.com/vyas-devgna/braids/blob/main/docs/29_KNOWN_LIMITATIONS.md)
- [Host research](https://github.com/vyas-devgna/braids/blob/main/research/00_INDEX.md)

## Contributing and security

Contributions are welcome; read [CONTRIBUTING.md](https://github.com/vyas-devgna/braids/blob/main/CONTRIBUTING.md) before changing normative behavior. Report vulnerabilities privately through GitHub’s security advisory flow as described in [SECURITY.md](https://github.com/vyas-devgna/braids/blob/main/SECURITY.md).

Brand artwork and usage notes live in [`assets/`](https://github.com/vyas-devgna/braids/blob/main/assets/README.md). No runtime behavior depends on them.

## License

[MIT](https://github.com/vyas-devgna/braids/blob/main/LICENSE) © 2026 Vyas Devgna.
