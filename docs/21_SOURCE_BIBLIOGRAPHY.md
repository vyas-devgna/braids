# Source Bibliography

Research date: **2026-08-31**

1. **Agent Skills Specification** — https://agentskills.io/specification
   - Used for: Portable SKILL.md format; progressive disclosure; ~100-token metadata, <5000-token recommended instructions, resources on demand; validation.

2. **Optimizing Skill Descriptions** — https://agentskills.io/skill-creation/optimizing-descriptions
   - Used for: Skill descriptions are the primary activation signal; trigger precision must be tested.

3. **Agent Plugins Specification v1.0.0** — https://agent-plugins.org/specification
   - Used for: Portable plugin.json package; exactly two portable v1 component types: Agent Skills and MCP servers; client extensions are vendor-specific.

4. **Agent Plugins Home** — https://agent-plugins.org/
   - Used for: Vendor-neutral packaging rationale and interoperability floor.

5. **Claude Code Plugins** — https://code.claude.com/docs/en/plugins
   - Used for: Claude plugin structure, local development via --plugin-dir, reload, namespacing and distribution.

6. **Claude Code Plugins Reference** — https://code.claude.com/docs/en/plugins-reference
   - Used for: Skills, agents, hooks, MCP, LSP, monitors, executable paths, plugin caching and validation.

7. **Claude Code Extension Overview** — https://code.claude.com/docs/en/features-overview
   - Used for: When to use persistent instructions, skills, subagents, hooks, MCP, plugins.

8. **Claude Code Hooks Guide** — https://code.claude.com/docs/en/hooks-guide
   - Used for: Deterministic hooks versus judgment-based model behavior; scopes and enforcement.

9. **Claude Code Marketplace Guide** — https://code.claude.com/docs/en/plugin-marketplaces
   - Used for: Marketplace layout, validation, local distribution and update model.

10. **Codex Skills** — https://learn.chatgpt.com/docs/build-skills
   - Used for: Codex skill authoring, progressive disclosure, skill packaging and activation.

11. **Codex Hooks** — https://learn.chatgpt.com/docs/hooks
   - Used for: Codex hook lifecycle and limits.

12. **Codex Subagents** — https://learn.chatgpt.com/docs/agent-configuration/subagents
   - Used for: Subagent delegation, isolation and coordination considerations.

13. **Codex AGENTS.md** — https://learn.chatgpt.com/docs/agent-configuration/agents-md
   - Used for: Persistent project-scoped agent instructions.

14. **Cursor Plugins** — https://prod.cursor.com/docs/plugins
   - Used for: Agent Plugin and Cursor Plugin support, local plugin development and marketplace.

15. **Cursor Plugin Reference** — https://prod.cursor.com/docs/reference/plugins
   - Used for: Cursor-specific rules, agents, commands, hooks, variables in addition to portable skills/MCP.

16. **Cursor Hooks** — https://prod.cursor.com/docs/hooks
   - Used for: Hooks can observe, block, or modify agent behavior.

17. **Cursor Agent Skills** — https://prod.cursor.com/docs/skills
   - Used for: Agent Skills discovery, automatic/manual activation, progressive loading.

18. **Google Antigravity Skills** — https://www.antigravity.google/docs/ide/skills/
   - Used for: Agent Skills support and workspace/global skill locations.

19. **Google Antigravity Skill Codelab** — https://codelabs.developers.google.com/getting-started-with-antigravity-skills?hl=en
   - Used for: Skills as on-demand capability extensions with scripts/resources.

20. **Google Antigravity Rules** — https://www.antigravity.google/docs/ide/rules/
   - Used for: Persistent and model-decided rules, scope and character limits.

21. **Google Antigravity Workflows** — https://www.antigravity.google/docs/ide/workflows/
   - Used for: Explicit slash-invoked sequential workflows; distinct from rules/skills.

22. **GitHub Copilot Plugins** — https://docs.github.com/en/copilot/concepts/agents/about-plugins
   - Used for: Plugin components: agents, skills, hooks, MCP and LSP.

23. **Windsurf Cascade Skills** — https://docs.devin.ai/desktop/cascade/skills
   - Used for: On-demand skills in Cascade.

24. **Windsurf Cascade Workflows** — https://docs.devin.ai/desktop/cascade/workflows
   - Used for: Manual workflow invocation and workflow semantics.

25. **OpenCode Skills** — https://opencode.ai/docs/skills
   - Used for: Agent Skills discovery, scopes and skill permissions.

26. **OpenCode Agents** — https://opencode.ai/docs/agents/
   - Used for: Agent permissions and task/subagent permission model.

27. **Cline Skills** — https://docs.cline.bot/customization/skills
   - Used for: Progressive loading, token model, skill locations and trigger guidance.

28. **Cline Hooks** — https://docs.cline.bot/customization/hooks
   - Used for: Lifecycle hooks including PreToolUse cancellation and context compaction hooks.

29. **Cline Skills Repository** — https://github.com/cline/skills
   - Used for: Cross-host skill portability and multi-reviewer precedent.

30. **Ponytail Repository** — https://github.com/DietrichGebert/ponytail
   - Used for: Reference precedent for a cross-host coding methodology skill/plugin and host adapters.

31. **Superpowers Repository** — https://github.com/obra/superpowers
   - Used for: Precedent for multi-skill software-development methodology distributed across many coding-agent harnesses.

32. **OpenAI Codex Skill Creator** — https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/skill-creator/SKILL.md
   - Used for: Skill construction workflow, progressive disclosure patterns, validation and forward testing.

33. **Cursor Plugin Template** — https://github.com/cursor/plugin-template
   - Used for: Official plugin repository layout and validation precedent.

34. **CMU SEI ATAM** — https://www.sei.cmu.edu/library/the-architecture-tradeoff-analysis-method/
   - Used for: Architecture trade-off analysis across competing quality attributes.

35. **CMU SEI ATAM 2026 Overview** — https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-atam/
   - Used for: Current SEI architecture evaluation overview.

36. **NIST SSDF 1.1** — https://csrc.nist.gov/pubs/sp/800/218/final
   - Used for: Security integrated into the SDLC.

37. **NIST SSDF 1.2 Draft** — https://csrc.nist.gov/pubs/sp/800/218/r1/ipd
   - Used for: 2025 draft update emphasizing secure and reliable development/delivery/improvement.

38. **OpenSSF OSS Evaluation Guide** — https://best.openssf.org/Concise-Guide-for-Evaluating-Open-Source-Software.html
   - Used for: Dependency necessity, authenticity, sustainability, security and practical testing.

39. **OpenSSF Secure Development Guide** — https://best.openssf.org/Concise-Guide-for-Developing-More-Secure-Software.html
   - Used for: Secure development and negative testing guidance.

40. **SLSA Provenance** — https://slsa.dev/spec/v1.2/provenance
   - Used for: Verifiable build/source provenance for supply-chain decisions.

41. **Model Context Protocol Specification** — https://modelcontextprotocol.io/specification/2025-03-26
   - Used for: MCP trust, consent, authorization and tool-execution security considerations.

42. **Language Server Protocol** — https://microsoft.github.io/language-server-protocol/
   - Used for: Reusable semantic code intelligence.

43. **Tree-sitter** — https://tree-sitter.github.io/tree-sitter/
   - Used for: Incremental, error-tolerant structural parsing.

44. **CodeQL Data Flow** — https://codeql.github.com/docs/codeql-language-guides/analyzing-data-flow-in-javascript-and-typescript/
   - Used for: Local/global data-flow trade-offs and analysis cost.


## Additional host-integration sources used in the research freeze

45. **Cursor Customization Overview** — https://prod.cursor.com/docs/customize-cursor
   - Used for: Current composable extension surface and relationship among plugins, rules, skills, subagents and hooks.

46. **Cursor Third-Party Hooks** — https://prod.cursor.com/docs/reference/third-party-hooks
   - Used for: Claude Code hook compatibility and duplicate/precedence concerns.

47. **Google Antigravity Plugins** — https://antigravity.google/docs/plugins/
   - Used for: IDE plugin structure (`plugin.json`, skills, rules, MCP, hooks) and workspace/global discovery.

48. **Google Antigravity CLI Plugins & Skills** — https://antigravity.google/docs/cli/plugins/
   - Used for: CLI plugin structure, skills, agents, hooks and MCP surface.

49. **GitHub Copilot Hooks Reference** — https://docs.github.com/en/copilot/reference/hooks-reference
   - Used for: CLI versus cloud hook/config differences and deterministic-policy limits.

50. **GitHub Copilot Plugin Creation** — https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-creating
   - Used for: Authoring/installing plugin packages.

51. **GitHub Copilot CLI Plugin Reference** — https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference
   - Used for: Plugin manifest/package reference.

52. **OpenCode Skills v2** — https://opencode.ai/v2/docs/skills
   - Used for: Current lazy skill body/supporting-file behavior.

53. **OpenCode Permissions v2** — https://opencode.ai/v2/docs/permissions
   - Used for: Version-sensitive granular action/resource permissions.

54. **OpenCode Agents v2** — https://opencode.ai/v2/docs/agents
   - Used for: Current primary/subagent capability model and delegation boundaries.

## Evidence register

`../matrices/research-evidence-register.csv` maps the research source class to the concrete Braids architectural decision it supports. This makes it possible to refresh fast-moving host facts independently from the stable engineering-methodology sources.


## Source policy

Primary/vendor documentation was preferred for current platform mechanics. Public repositories were used for architecture precedent, not as normative host specifications. Older architecture/security standards were used for stable engineering methodology, while host/plugin facts were checked against current documentation.

## Important freshness note

Host extension APIs are fast-moving. Before implementation of each adapter, its referenced primary documentation must be rechecked and the adapter capability contract updated if necessary. The portable Agent Skills and Agent Plugins specifications should be treated as the interoperability baseline until superseded.
