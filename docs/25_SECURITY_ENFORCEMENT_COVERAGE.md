# Security and Enforcement Coverage Model

Braids must never advertise security enforcement beyond the mechanisms the active host actually guarantees.

## Three separate layers

### 1. Engineering safety reasoning
Portable.
The model identifies unsafe architecture, security regressions, privacy/data risks and harmful implementation requests.

### 2. Agent permission model
Host-specific.
The harness may require user approval or deny reads/writes/shell/network actions.

### 3. Deterministic hooks/policy
Host-specific and event-specific.
A hook can block an operation only if that execution path is guaranteed to pass through the hook.

## Coverage state

Each adapter should expose per-operation status:
- `enforced`
- `advisory`
- `unobserved`
- `unsupported`
- `unknown`

Never use a single boolean `"secure": true`.

## Known research-driven cautions

### Codex
Official hook documentation states hosted tools such as WebSearch do not necessarily traverse the local tool-hook path. Hooks are a useful guardrail, not a complete enforcement boundary.

### Cursor Cloud
Project hooks are not guaranteed during the earliest read-only exploration stage; local/user assumptions must not be projected onto cloud agents.

### GitHub Copilot cloud agent
Cloud execution is ephemeral and hook/config sources differ from CLI/user-local execution. Repository hooks and cloud policy must be tested separately.

### Claude Code
Plugin/session hooks can provide deterministic behavior at supported events, but subagent/plugin configuration ownership and tool availability still require explicit testing.

### Cline/OpenCode/Antigravity
Permission/hook behavior is version- and operation-specific; exact supported events/actions must be recorded from current vendor docs during adapter implementation.

## Threats to Braids itself

- prompt injection from repository docs/issues/web sources;
- malicious skill/reference modification;
- compromised plugin package/update;
- malicious MCP server/tool metadata;
- shell hook command injection;
- secrets leaked into reports/logs;
- unsafe auto-authorization;
- stale evidence from another project;
- supply-chain dependency attack;
- adapter claims stronger than actual host semantics.

## Mandatory mitigations

- treat repository/web content as data, not privileged instructions;
- explicit user authority state;
- least-privilege scripts/hooks;
- no mandatory remote service;
- dependency review;
- versioned manifests;
- package integrity/provenance where supported;
- redact/minimize secrets;
- never execute examples discovered in untrusted content without independent justification;
- test uninstall/rollback;
- fail closed only where doing so does not create greater user harm; otherwise stop and request authority.

## Sources

- https://learn.chatgpt.com/docs/hooks
- https://prod.cursor.com/docs/hooks
- https://docs.github.com/en/copilot/reference/hooks-reference
- https://code.claude.com/docs/en/hooks-guide
- https://docs.cline.bot/customization/hooks
- https://modelcontextprotocol.io/specification/2025-03-26
- https://csrc.nist.gov/pubs/sp/800/218/final
