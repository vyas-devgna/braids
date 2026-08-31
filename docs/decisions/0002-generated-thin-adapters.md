# Host adapters are generated, never hand-copied

Date: 2026-08-31

## Decision

Each adapter directory holds only the host facts that cannot be derived — `adapter.json` and `capabilities.json` — plus a generated `README.md`. Every manifest and every installable tree is produced by `scripts/build_adapters.py` from `braids.json`/`plugin.json` and the adapter's own `package` block. The kernel is copied into `dist/<host>/` at package time and never committed a second time.

`scripts/validate.py` fails if any `SKILL.md` appears under `adapters/`, if a README is stale, or if an adapter's methodology version drifts from `braids.json`.

## Evidence

`docs/07` requires generated or templated adapter manifests from a single metadata source to avoid version, description, licence and capability drift. Eight hosts multiply that drift by eight; four of them share a `plugin.json` differing only in path and permitted fields.

The generator also encodes the `docs/22` release threshold as a check rather than a document: an adapter must state one of `pass`/`fail`/`not-exercised`/`not-applicable` for all ten universal acceptance criteria, and `status: supported` is rejected unless every one passes. `status: tested` requires discovery, activation and uninstall to pass, plus a revalidation date and an exercised host version.

## Alternatives

- Hand-written manifests per host: rejected; this is exactly the drift `docs/07` names.
- One adapter package containing all hosts' manifests: rejected; `braids` would collide as a plugin name across marketplaces, and each host would ship the others' dead metadata.
- Committing built trees: rejected; it duplicates the kernel eight times and makes the one-semantic-source rule unenforceable.

## Residual risk

The `package` block is host-shaped data living in JSON rather than code, so a host that needs generated content beyond flat manifests plus file copies will need a generator change, not a data change. No host currently does.
