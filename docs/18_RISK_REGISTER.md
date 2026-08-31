# Pre-Development Risk Register

| ID | Risk | Consequence | Mitigation | Gate |
|---|---|---|---|---|
| R1 | Braids becomes a mega-prompt | context cost, worse reasoning | progressive disclosure, strict kernel size | A/E |
| R2 | Over-triggering | wastes tokens, annoys users | dedicated trigger evals, negative cases | E |
| R3 | Under-triggering | misses value | description optimization corpus | C |
| R4 | Architecture overengineering | Braids violates itself | no mandatory MCP/db/subagents; feature evidence rule | C/E |
| R5 | Host API churn | broken integrations | host-neutral core, adapter versioning | F |
| R6 | False safety guarantee | user harm | capability tiers, enforcement coverage statement | D |
| R7 | Research hallucination | incorrect architecture | evidence ledger, primary-source preference | C/D |
| R8 | Research leaks private data | security/privacy harm | query sanitization and no project secrets externally | D |
| R9 | Dependency sprawl | attack/maintenance surface | core dependency-free target, OpenSSF gate | D/E |
| R10 | Multi-agent token explosion | cost/latency | depth-triggered delegation only | E |
| R11 | Reviewer groupthink | missed failures | independent Challenger mandate on high depth | C |
| R12 | Endless improvement loop | cost/scope creep | stop controller + authorization | C/E |
| R13 | User loses control | distrust/unsafe writes | explicit authority contract | D |
| R14 | Too many public subskills | routing/maintenance tax | one primary skill until eval evidence | A/E |
| R15 | Vague quality language | non-testable advice | scenario compiler | C |
| R16 | Fake numeric scoring | pseudo-precision | structured/Pareto trade-off, measurements only where meaningful | C |
| R17 | "Reuse" imports bad dependency | supply chain/compat issue | dependency adoption/exit gate | D |
| R18 | Marketplace packaging drives architecture | vendor lock-in | portable core first | F |
| R19 | Model-specific behavior | inconsistent portability | multi-model/host evals and explicit capability constraints | F |
| R20 | Correct current code gets needless rewrite | user harm/maintenance | no-change fixtures and stop gate | C/E |
