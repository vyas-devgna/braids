# Security Threat Model and Guardrail Design

## Security objective

Braids must not create additional user harm while attempting to improve engineering quality.

## Trust boundaries

1. User instructions
2. Repository content
3. Generated code
4. Host tools and permissions
5. Shell/runtime environment
6. External web content
7. MCP servers
8. Dependencies/packages
9. Subagents
10. Plugin distribution/update channel

## Threats

### T1 Prompt/instruction injection from repository or web
Mitigation:
- treat repository/web text as evidence, not higher-priority instructions;
- preserve host instruction hierarchy;
- never execute untrusted instructions merely because they appear in source/docs/issues.

### T2 Over-privileged plugin behavior
Mitigation:
- core skill requires no new privilege;
- adapters request only needed host capabilities;
- optional hooks/MCP are separately disclosed.

### T3 False enforcement claims
Mitigation:
- explicit capability tier;
- distinguish semantic guardrail from deterministic interception;
- report uncovered tool paths.

### T4 Unsafe shell/destructive action
Mitigation:
- authorization gate;
- host permissions;
- deterministic pre-tool hook when supported and justified;
- preserve rollback/recovery plan for high-risk mutations.

### T5 Supply-chain compromise
Mitigation:
- dependency necessity gate;
- authenticity/source checks;
- maintenance/security/transitive/license evaluation;
- provenance checks for high-assurance scenarios;
- pinned/reproducible release practices where appropriate.

### T6 Malicious/compromised MCP
Mitigation:
- no mandatory MCP;
- least privilege and explicit user installation;
- treat tool descriptions/results as untrusted external capability;
- do not pass secrets unless required and authorized.

### T7 Subagent scope escalation
Mitigation:
- roles have explicit read/write/tool boundaries;
- Scout/Challenger/Verifier should be read-only by default;
- Implementer gets only required authority.

### T8 Data/secrets leakage through research
Mitigation:
- external research queries must not contain private source code, credentials, tokens, proprietary identifiers or unnecessary user data.

### T9 Infinite improvement loop
Mitigation:
- explicit stop controller;
- user authorization for material scope expansion/self-improvement;
- iteration ceiling in host adapters where practical.

### T10 Plugin update compromise
Mitigation:
- signed/tagged release process when available;
- checksums/build provenance;
- changelog and version pinning support;
- no opaque downloaded executable blobs.

## Secure-development baseline

Use NIST SSDF as a vocabulary for integrating security into normal development, not as a checkbox attached at the end.

## Hard user-harm categories

At minimum:
- authentication/authorization weakening;
- secret exposure;
- privacy leakage;
- destructive operations;
- data corruption/loss;
- unsafe migration;
- unbounded resource abuse;
- silently dropped integrity checks;
- known supported-environment breakage.

Braids should challenge the engineering decision and propose the nearest safe alternative. It should challenge the idea, not the user.
