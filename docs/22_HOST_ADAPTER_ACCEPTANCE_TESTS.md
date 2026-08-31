# Host Adapter Acceptance Tests

No host adapter is releaseable merely because its files install.

## Universal adapter contract

Each adapter must prove:

1. **Discovery**
   - Braids is visible/installable through the host's supported mechanism.
   - No undocumented path is required.

2. **Activation**
   - explicit invocation works;
   - relevant prompts activate the skill when host supports automatic skill selection;
   - near-miss prompts do not over-trigger.

3. **Portable semantic parity**
   - the same fixture produces materially equivalent Engineering Contract, risk depth, hard constraints, decision rationale and verification obligations across hosts.

4. **Progressive disclosure**
   - dormant Braids does not inject full reference material;
   - activated Braids loads only routed references.

5. **Authority**
   - reviewer mode does not write;
   - implementation mode requires the expected user authorization boundary;
   - no adapter silently escalates privileges.

6. **Tool/capability degradation**
   - missing web, LSP, hooks, subagents, sandbox or MCP causes graceful degradation rather than fabricated evidence.

7. **Enforcement truthfulness**
   - deterministic blocking claims are tested against every operation class claimed;
   - uncovered paths are documented.

8. **State survival**
   - long sessions/compaction/resume retain material assumptions, decision and unverified claims where the host exposes lifecycle support.

9. **Isolation**
   - when worktrees/sandboxes/subagents are used, writes cannot leak into unintended workspaces.

10. **Uninstall**
   - removing the adapter leaves no persistent rule/hook/server unexpectedly active.

## Per-host minimums

### Claude Code
- load via `--plugin-dir`;
- `/reload-plugins`;
- `claude plugin validate <plugin-path> --strict`;
- skill namespacing;
- each hook event independently exercised;
- custom-agent visibility;
- worktree path test if shipped.
- explicit negative tests for `EndConversation`, async/after-the-fact events, and shared worktree `.git`/approval state;
- disable/uninstall proves components inactive even if inert cache bytes remain.

### Codex
- standalone `.agents/skills` and installable `.codex-plugin` activation on their supported surfaces;
- marketplace list/add/remove JSON flow because no `codex plugin validate` command is documented;
- AGENTS.md scope/nesting;
- hook tests on supported local tool paths;
- explicit negative test proving hosted/non-hook path is not represented as covered;
- hook trust, `write_stdin` no-second-PreToolUse, and background/non-executed handler negatives;
- subagent token/cost comparison fixture.
- subagent context isolation must not be reported as filesystem/worktree isolation unless separately exercised.

### Cursor
- Agent Plugin format;
- enhanced Cursor Plugin format if shipped;
- local plugin directory;
- cloud/local capability split;
- early cloud read-only/hook assumption test;
- third-party hook duplication test if compatibility enabled.
- desktop, CLI and cloud capability profiles; marketplace disable/uninstall remains unsupported until directly exercised.

### Antigravity
- workspace/global skill;
- plugin manifest;
- rule/workflow distinction;
- hooks if shipped;
- IDE/CLI behavior documented separately.
- strict manifest intersection, workspace skill path, CLI disable/enable/uninstall, and explicit unknown global-skill/Web coverage.

### GitHub Copilot
- CLI install/use;
- cloud/repository execution;
- repository hook behavior;
- absence of local-user assumptions in cloud.

### Windsurf/Cascade
- fresh documentation revalidation first;
- skill activation;
- optional workflow alias only;
- no unsupported enforcement claim.

### OpenCode
- skill discovery;
- installed-version config schema detection;
- allow/ask/deny permission behavior;
- subagent limits;
- lazy reference loading.

### Cline
- skill loading;
- PreToolUse cancellation if used;
- compaction/resume state preservation;
- task completion/cancel lifecycle.

## Release threshold

An adapter fails release if:
- it changes Braids methodology to fit the host;
- it claims enforcement that was not directly exercised;
- it requires full-time context injection;
- it leaves stale configuration after uninstall;
- its result materially disagrees with portable conformance fixtures without a documented host capability reason.
