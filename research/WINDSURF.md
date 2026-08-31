# Braids Host Research — Windsurf / Cascade

Research date: 2026-08-31  
Status: pre-development evidence record; documentation currently resolves through the Cascade/Devin documentation surface and must be rechecked before implementation.

## Implementation revalidation — 2026-08-31

Revalidated against current official documentation. Windsurf is not installed in the development environment, so nothing here is exercised.

- `docs.windsurf.com` now redirects to `docs.devin.ai`. The product surface is moving; revalidate again before any release claim.
- Workspace skills: `.windsurf/skills/<name>/`. Global skills: `~/.codeium/windsurf/skills/<name>/`.
- Enterprise system-level skill directories exist and are read-only; the adapter never writes them.
- Cascade also reads `.agents/skills` and `~/.agents/skills`, and `.claude/skills` when Claude Code config reading is enabled, so a Braids copy installed for another host can appear here.
- Frontmatter requires `name` (lowercase, digits, hyphens) and `description`.
- No plugin manifest format is documented, so the adapter ships a skill directory only and claims no enforcement.

## Relevant concepts

Cascade documentation exposes skills and workflows as distinct customization mechanisms.

Skills are the appropriate Braids core because they provide reusable expertise/instructions with progressive/on-demand use. Workflows are explicit user-invoked sequences and are better suited to convenience commands than to Braids' dynamic decision routing.

Persistent rule/memory mechanisms should only be used for optional activation guidance.

## Architectural consequence

Do not design Braids around a host-specific workflow DSL. The Braids kernel must decide its path from:
- project scope;
- change surface;
- risk;
- uncertainty;
- available evidence.

A fixed workflow can call Braids but must not replace that runtime router.

## Adapter scope

Initial Windsurf/Cascade adapter should be intentionally minimal:
- portable Agent Skill where accepted;
- equivalent skill location/package mechanism;
- optional tiny persistent rule;
- no mandatory host-specific code.

Only add hooks/subagents/tool integrations after their current supported behavior is revalidated during the adapter implementation gate.

## Token policy

Keep the persistent component close to zero. Put all detailed engineering doctrine in the skill and references. Do not duplicate reference material into workflow instructions.

## Braids adapter decision

**Use:** skill-first integration.  
**Optional:** explicit workflows as aliases to review/audit modes.  
**Avoid:** asserting unverified enforcement guarantees.

## Primary sources

- https://docs.devin.ai/desktop/cascade/skills
- https://docs.devin.ai/desktop/cascade/workflows

## Freshness warning

This platform's documentation/product naming and extension surface are fast-moving. Gate H-WINDSURF-0 in the development plan requires a fresh vendor-doc recheck before any adapter code is committed.
