# Braids Engineering Decision Method

## Objective

Select the lowest total lifecycle burden among solutions that:
- satisfy real requirements;
- satisfy relevant quality scenarios;
- satisfy hard constraints;
- leave acceptable, explicit residual risk.

## Step 1 — establish contract

Resolve:
- desired outcome;
- permitted scope;
- decision authority;
- implementation authority;
- supported platforms/environments;
- scale/user exposure;
- project maturity;
- distribution model;
- success criteria.

Unknowns become assumptions. Resolve only material ones.

## Step 2 — model the affected system

Do not review only the edited file. Identify relevant contracts and boundaries:
- callers/callees;
- public APIs;
- state/persistence;
- process/thread/network boundaries;
- OS/runtime behavior;
- deployment;
- user journey;
- trust boundaries.

## Step 3 — compile scenarios

For relevant quality concerns, state:
`source -> stimulus -> environment -> artifact -> expected response -> response criterion`

This prevents vague "robust/performance/best practice" reasoning.

## Step 4 — route depth

Determine D0-D4 using risk/blast radius/uncertainty.

Important: low line count does not imply low depth.

## Step 5 — gather decision-changing evidence

Local implementation and tests first.
Use external docs/source/issues/benchmarks only when they can change architecture, risk, dependency or verification.

## Step 6 — reuse gate

Consider:
project capability -> stdlib -> platform -> installed dependency -> proven OSS -> custom implementation.

External code is accepted only if its lifecycle burden is lower after maintenance/security/license/integration/exit costs.

## Step 7 — candidate set

Include baseline plus materially distinct viable alternatives.
Do not create options for rhetorical completeness.

## Step 8 — hard constraints

Eliminate candidates that violate:
- user safety;
- security;
- privacy;
- data integrity;
- destructive-operation safety;
- explicit functionality;
- required compatibility.

## Step 9 — trade-offs

Evaluate only relevant dimensions:
- correctness
- reliability
- performance
- CPU/memory/I/O/network/storage
- maintainability
- operability/observability
- developer UX
- deployment UX
- end-user UX
- dependency/supply-chain burden
- migration/rollback burden
- future change cost

Do not reduce unlike qualities to arbitrary numeric weights unless project data supplies defensible measurements.

## Step 10 — decide and verify

Decision record states why the winner won and what evidence remains missing.
Implementation occurs only under delegated authority.
Verification targets material claims.
Stop on diminishing value.

## Canonical Braids principle

**Complexity is neither good nor bad. It is a cost that must purchase scenario-linked engineering value.**
