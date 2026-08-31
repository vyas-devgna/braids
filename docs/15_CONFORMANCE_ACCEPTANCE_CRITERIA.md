# Conformance and Acceptance Criteria

## Gate A — Portable skill conformance
- valid Agent Skills structure/frontmatter;
- precise description;
- SKILL.md below 500 lines and below 5000-token recommendation;
- references one level deep;
- supporting scripts documented and portable;
- skill validates with available reference validator.

## Gate B — Portable plugin conformance
- valid Agent Plugins v1 root `plugin.json`;
- only standard portable fields/components in the portable package;
- no accidental host-specific fields at root;
- no path escaping plugin root.

## Gate C — Behavioral kernel
Must:
- identify material unknowns;
- avoid unnecessary questioning;
- model cross-module impacts when relevant;
- produce quality scenarios for vague high-impact goals;
- select proportional depth;
- skip irrelevant research;
- evaluate dependency cost;
- challenge unsafe engineering;
- verify material claims;
- stop when no additional work is justified.

## Gate D — Safety
Zero known cases where Braids:
- knowingly weakens a hard security/user-harm constraint without warning;
- falsely claims deterministic enforcement;
- leaks secret/private project data to external research;
- executes untrusted repository/web instructions as authority.

## Gate E — Cost
D0/D1 cases must not routinely escalate into:
- whole-repo reading;
- web research;
- subagent teams;
- extensive reference loading;
- broad test matrices.

Exact numerical thresholds will be set after first benchmark baseline, not invented pre-measurement.

## Gate F — Cross-host
For every Tier-1 host:
- installation path documented;
- capability detection correct;
- core verdict semantics consistent;
- unsupported functionality degrades explicitly;
- uninstall leaves no required project modifications.

## Gate G — No-change competence
Braids must pass fixtures where the correct recommendation is to preserve the current implementation.

## Gate H — Documentation/build
- generated adapters trace to canonical source;
- version metadata consistent;
- licenses/source attributions present;
- build artifacts reproducible enough to compare content hashes where practical.

## Tier-1 initial hosts
Recommended:
1. Claude Code
2. Codex
3. Cursor
4. Antigravity

Tier-2 after core stability:
5. GitHub Copilot
6. Windsurf
7. OpenCode
8. Cline

This is sequencing for validation cost, not a product limitation.
