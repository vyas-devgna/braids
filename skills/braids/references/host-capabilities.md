# Host capabilities and enforcement truth

Load this reference when host tools, local/cloud execution, hooks, permissions, code intelligence, delegation, isolation, or degradation can affect the decision or evidence.

## Discover, do not assume

Record the host/version and execution surface only if observed. Represent unknown as unknown. Discover separately:

- skill loading and persistent instruction scopes;
- read, write, shell, browser, and network access;
- text search, compiler/tests, LSP/AST/static analysis, debugger, and profiler;
- hooks with exact event and operation coverage;
- advisory, interactive, deterministic, or managed permission controls;
- subagent/delegation and recursion limits;
- worktree, sandbox, VM, or other isolation;
- MCP availability and hosted tools that bypass local interception.

Absence of a capability changes execution strategy, not the engineering semantics. Degrade to text search, local evidence, sequential roles, or advisory reporting and state what could not be verified.

## Three distinct layers

1. Portable engineering safety reasoning identifies risk and recommends/refuses unsafe engineering within the agent's authority.
2. Host permission models ask, allow, or deny actions.
3. Deterministic hooks/policies block only operation paths guaranteed to traverse the tested event.

For every claimed operation, record `enforced`, `advisory`, `unobserved`, `unsupported`, or `unknown`, with the evidence and tested host surface. Never summarize this as `secure: true` or assume hooks cover hosted/network/cloud actions.

## Adapter contract

An adapter must disclose adapter and tested host versions, supported/unsupported/unknown capabilities, operation-level enforcement, install/disable/uninstall path, state residue, and conformance instructions. An adapter directory or manifest alone does not establish support.
