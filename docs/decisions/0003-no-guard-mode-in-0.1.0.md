# No Guard Mode, hooks or custom agents in 0.1.0

Date: 2026-08-31

## Decision

Every adapter ships the canonical skill and its packaging metadata only. No hooks, rules, custom agents, commands, LSP or MCP configuration is installed on any host. `guard_mode_default` is `false` everywhere and `scripts/build_adapters.py` rejects any other value.

## Evidence

`docs/22` fails an adapter that "claims enforcement that was not directly exercised", and `docs/25`/`docs/10` separate semantic safety reasoning from deterministic enforcement. Current primary-source revalidation shows the enforcement surface is full of holes that a shipped hook would have to be honest about:

- Claude Code 2.1.248 — `PreToolUse` denies only matched, directly tested tool paths; `EndConversation` skips Pre/PostToolUse; asynchronous and after-the-fact events do not block; plugin-declared agents do not own session hook, MCP or permission-mode configuration.
- Codex 0.150.1 — hooks need separate trust, hosted WebSearch is outside local hook coverage, `write_stdin` raises no second `PreToolUse`, background hooks cannot block, and parsed `prompt`/`agent` handlers are skipped.
- Cursor — cloud runs command hooks only, omits several local lifecycle events, excludes user hooks, and runs no hooks during initial read-only exploration; third-party Claude hook compatibility runs all matching sources by precedence, so a Braids hook could fire twice.
- Antigravity — hooks are command-only and operation-specific; Web and extension parity is undocumented.
- OpenCode — permission semantics differ between V1 and V2 config, and the last matching rule wins, so a shipped policy file written against the wrong version silently changes meaning.

A hook shipped against any of these would buy narrow, host-specific blocking while inviting exactly the enforcement over-claim the dossier forbids. Every adapter's `capabilities.json` therefore carries an empty `enforcement` array, and `build_adapters.py` rejects an `enforced` operation unless that adapter's `enforcement-truthfulness` check passes.

## Alternatives

- Ship a destructive-command `PreToolUse` hook on Claude Code and Codex: rejected for 0.1.0; its coverage would have to be tested per tool path per host before it could be described, and the untested paths would remain open while the README implied protection.
- Ship a tiny `AGENTS.md`/rule Guard Mode: rejected; persistent instructions cost context on every unrelated turn, which is the cost `docs/09` and `docs/24` exist to prevent.

## Residual risk

Braids on every supported host is advisory. It reasons about unsafe changes; it does not stop a tool call. `SECURITY.md` and each adapter README state this. Adding narrow enforcement later is additive: it needs a hook file, an `enforcement` entry naming the exact operation and surface, and an exercised `enforcement-truthfulness` result.
