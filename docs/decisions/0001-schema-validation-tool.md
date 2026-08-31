# Schema validation tool

Date: 2026-08-31

## Decision

Keep Braids runtime dependency-free. Use the pinned `check-jsonschema` 0.38.0 tool only in isolated development/CI validation; keep basic source/reference/package checks in the Python standard-library validator.

## Evidence

JSON Schema Draft 2020-12 meta-validation and cross-file reference resolution are mature, non-trivial standards behavior. Reimplementing them locally would add more maintenance and correctness risk than an isolated development tool.

## Alternatives

- Write a partial JSON Schema engine: rejected as duplicated, fragile machinery.
- Add `jsonschema` as a runtime dependency: rejected because the portable skill does not execute schemas at runtime.

## Residual risk

Development/CI schema validation requires obtaining the pinned tool. Offline users can still use Braids and run the dependency-free structural validator, but cannot reproduce full meta-schema checks until the tool is cached or installed.
