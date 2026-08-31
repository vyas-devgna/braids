# Contributing

Braids is developed against the frozen product, architecture, module, security, token, evaluation, and traceability contracts in this repository.

Before proposing a normative behavior, identify:

- the requirement or ADR it implements;
- the owning logical module;
- a positive conformance fixture;
- a negative or edge fixture where misuse is plausible;
- added context, dependency, tool, maintenance, and removal cost.

Keep the portable methodology in `skills/braids`. Host adapters must stay thin and capability-driven. Do not add mandatory MCP, persistent state, production telemetry, or runtime dependencies without an accepted decision record and evidence.

Run `python3 scripts/validate.py` and `python3 scripts/run_evals.py` before submitting changes. Do not include secrets, credentials, private fixtures, generated eval results, or unrelated refactors.
