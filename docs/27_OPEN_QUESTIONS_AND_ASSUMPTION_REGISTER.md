# Open Questions and Assumption Register

Research freeze date: 2026-08-31

This file separates **architectural decisions already frozen** from choices that should not be silently invented during implementation.

## Frozen — not open

- Product name: Braids.
- Core objective: right-sized engineering, not minimum/maximum code.
- Portable methodology: Agent Skills-compatible core.
- Packaging floor: Agent Plugins where supported; thin host adapters elsewhere.
- Progressive disclosure is mandatory.
- MCP is optional.
- Multi-agent execution is optional and depth-triggered.
- User-harm/security constraints are cross-cutting.
- No silent material assumptions.
- User retains final authority except where the host/platform itself refuses an unsafe/invalid operation.
- Research is targeted by value of information.
- External reuse gets a dependency/adoption gate.
- Verification is claim-driven.
- "No change required" is a successful outcome.
- Session state is ephemeral by default.
- Deterministic enforcement claims must be scoped to actual host coverage.

## Blocking product/release choices

### OQ-01 — License
**Status:** RESOLVED 2026-08-31 — MIT, chosen by the project owner.  
**Why it matters:** marketplace/package metadata, contributions, reuse.  
**Implementation:** `LICENSE` carries the MIT text, `braids.json.license` and `plugin.json.license` both read `MIT`, and `scripts/validate.py` fails if the two ever disagree.

### OQ-02 — Initial adapter release set
**Status:** partially resolved 2026-08-31 — all eight adapters are generated and schema-valid, but none is `supported`. Discovery and uninstall are directly exercised on the four hosts installed locally (Claude Code 2.1.248, Codex 0.150.1, OpenCode 1.18.23, Copilot CLI 1.0.82); Cursor, Antigravity, Cline and Windsurf are packaged from revalidated documentation with every host-side check recorded `not-exercised`.  
**Recommended reversible default:** build portable conformance harness first, then Claude Code + Codex + Cursor adapters because they exercise three different extension models. Add others only after core conformance is stable.  
**Do not treat recommendation as a user decision.**

### OQ-03 — Guard Mode default
**Status:** architecture says optional; default activation policy for public release must be frozen.  
**Safe development default:** Guard Mode OFF. Explicit/automatic skill activation only.

### OQ-04 — Telemetry
**Status:** metrics are defined, but collection/storage/product telemetry is not authorized.  
**Implementation rule:** evaluation harness may record local test metrics. Production plugin must not transmit telemetry without an explicit product/privacy decision.

### OQ-05 — Persistent reports
**Status:** session-local by default; exact CLI/user command for persisting an ADR/report is not frozen.  
**Implementation rule:** no hidden `.braids/` state.

### OQ-06 — Marketplace identity / signing / release accounts
**Status:** partially resolved 2026-08-31 — package identity is `Vyas Devgna <https://github.com/vyas-devgna>`, chosen by the project owner because Claude Code rejects a plugin manifest without `author` under `--strict` and a marketplace manifest without `owner` outright.  
**Still unresolved:** signing keys, marketplace accounts, and the published repository URL, which is currently an assumed `github.com/vyas-devgna/braids`.  
**Implementation rule:** release automation must support dry-run/local package validation without marketplace credentials. `python3 scripts/build_adapters.py --dist dist` satisfies this today.

### OQ-07 — Brand assets
**Status:** RESOLVED 2026-08-31 — final artwork delivered and vendored at `assets/` (mascot master and transparent at 3072 px, icon at 2048/1024/512/256 px, hero at 2560×1440, 17 MB total).  
**Implementation rule:** no engineering behavior may depend on brand assets. This is enforced: `scripts/validate.py` fails on any image outside `assets/`, and the only asset entering a package is the 256 px icon in the Cursor tree, for the one manifest field that documents a logo.  
**Note:** the pack ships no SVG. A future strict vector icon must be redrawn natively rather than auto-traced.

## Host facts that must be revalidated

The following are intentionally treated as versioned evidence, not timeless assumptions:
- manifest fields;
- skill directories;
- hook event names and coverage;
- marketplace validation commands;
- cloud-agent isolation/config behavior;
- subagent recursion and write isolation;
- token/context limits;
- permission schema.

Before implementing each adapter:
1. open current primary vendor docs;
2. update `research/<HOST>.md`;
3. update `matrices/host-capability-matrix.csv`;
4. add a dated ADR if the new host behavior changes architecture;
5. update host acceptance tests.

## Assumption rule

An implementer may choose a reversible implementation detail without asking only if:
- it does not change product behavior or safety;
- it does not create a new external dependency/trust boundary;
- it does not alter supported hosts;
- it does not materially change token cost;
- it can be replaced without migration burden.

Everything else belongs here or in an ADR.
