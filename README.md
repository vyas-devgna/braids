<p align="center"><img src="assets/hero/braids-hero.png" alt="Braids" width="720"></p>

# Braids

Braids is an adaptive engineering-governance skill for AI coding agents. It chooses the lowest total lifecycle burden that satisfies the real requirements, quality scenarios, hard constraints, and acceptable residual risk.

Braids is currently under pre-release development. The canonical behavior lives in `skills/braids`; host adapters may expose native packaging or optional guards but may not redefine that behavior.

## What it does

Braids scales its engineering depth from D0 (local and reversible) through D4 (critical or irreversible), acquires only decision-changing context, challenges unsafe or unsupported choices, evaluates reuse and dependencies, and links material claims to evidence. Review-only authority never permits writes. “No change” is a valid result.

## Portable use

Install or copy `skills/braids` into an Agent Skills-compatible host, or load this directory as an Agent Plugins v1 package. No MCP server, network service, runtime dependency, or production telemetry is required.

### Claude Code

```sh
claude plugin marketplace add vyas-devgna/braids
claude plugin install braids@braids
```

### Codex CLI and desktop

```sh
codex plugin marketplace add https://github.com/vyas-devgna/braids
codex plugin add braids@braids --json
```

The Codex IDE extension does not load installable plugins. For that surface, copy `skills/braids` to `<project>/.agents/skills/braids`.

Run local conformance checks with:

```sh
python3 scripts/validate.py         # package, skill, schema, adapter and secret invariants
python3 scripts/run_evals.py        # eval corpus integrity (add --fixture-tests for the fixtures)
python3 scripts/measure_budget.py   # static context budget against the docs/24 ceilings
python3 -m unittest discover -s tests
```

## Host adapters

Eight adapters are generated from one metadata source — no adapter contains Braids methodology or a second copy of the kernel:

```sh
python3 scripts/build_adapters.py --dist dist          # build every installable tree
python3 scripts/build_adapters.py --dist dist --only codex
```

Each `adapters/<host>/README.md` carries that host's install, disable and uninstall steps, its state against all ten `docs/22` acceptance checks, and its limitations.

**All eight adapters are `experimental`, and Braids is advisory on every host — it ships no hooks and enforces nothing.** Read [docs/29_KNOWN_LIMITATIONS.md](docs/29_KNOWN_LIMITATIONS.md) before relying on any of it.

Host support is claimed only in each adapter's tested capability record. A present adapter directory is not itself a support claim.

## Project status

- Methodology baseline: v3
- Package: 0.1.0 development series
- Guard Mode: off by default
- State: session-local by default
- License: MIT

The authoritative pre-development dossier remains in `docs/00_INDEX.md`, `research/00_INDEX.md`, and the root baseline artifacts.

## Brand assets

`assets/` holds the mascot, icon and hero artwork, with per-file usage notes in [assets/README.md](assets/README.md). They are repository and distribution material only: no Braids behaviour depends on them, `scripts/validate.py` rejects an image anywhere outside `assets/`, and no asset enters the runtime skill or model context. Only the Cursor package carries one — the 256 px icon, for the `logo` field that manifest documents.

## Licence

MIT. See [LICENSE](LICENSE).
