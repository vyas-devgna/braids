# Architecture Decision Records — Frozen Pre-Development Decisions

## ADR-001 Portable core = Agent Skill
Status: Accepted.
Reason: broad cross-host support and progressive disclosure.
Rejected: host-specific plugin as canonical source.

## ADR-002 Agent Plugin is distribution wrapper, not methodology
Status: Accepted.
Reason: v1 portable plugin standard only guarantees skills and MCP; methodology remains reusable independently.

## ADR-003 No mandatory MCP in v1
Status: Accepted.
Reason: no proven capability gap justifies extra trust/process/maintenance surface.

## ADR-004 One primary public Braids skill initially
Status: Accepted.
Reason: minimizes discovery/routing overhead and source drift.
Revisit when activation evals prove separate skills improve behavior.

## ADR-005 Host adapters use capability semantics
Status: Accepted.
Reason: same host can differ by local/cloud/version/policy; brand-based assumptions are brittle.

## ADR-006 No universal risk number
Status: Accepted.
Reason: heterogeneous severity/recoverability/uncertainty cannot be truthfully collapsed without domain calibration.

## ADR-007 Quality scenarios before trade-off on non-trivial work
Status: Accepted.
Reason: makes vague qualities testable and ATAM-like trade-off reasoning concrete.

## ADR-008 Security is cross-cutting
Status: Accepted.
Reason: SSDF-style integration; late safety gate is insufficient.

## ADR-009 Session state is ephemeral by default
Status: Accepted.
Reason: avoid polluting repositories and unnecessary persistence.
Persistent ADR/risk artifacts only when task warrants them.

## ADR-010 Evidence-led claims
Status: Accepted.
Reason: prevents model confidence from masquerading as measurement.

## ADR-011 Subagents are optional roles
Status: Accepted.
Reason: portability and token cost.
Roles may map to sequential passes on simpler hosts.

## ADR-012 Guard Mode is opt-in and tiny
Status: Accepted.
Reason: avoid persistent context bloat.

## ADR-013 "No change" is a valid successful verdict
Status: Accepted.
Reason: prevents ideology-driven rewrites.

## ADR-014 Token goal = minimum sufficient reasoning, not minimum tokens
Status: Accepted.
Reason: first-turn token savings can create larger rework cost.

## ADR-015 Tiered host validation
Status: Proposed/Accepted for initial development.
Tier 1: Claude Code, Codex, Cursor, Antigravity.
Tier 2: Copilot, Windsurf, OpenCode, Cline.
Reason: bound initial integration/testing surface without narrowing the portable architecture.
