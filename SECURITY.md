# Security policy

## Supported versions

Braids is pre-release. Security fixes target the current development branch until a release policy is published.

## Reporting

Do not open a public issue containing an exploitable vulnerability, secret, or private project data. Use the private security-reporting channel of the repository host once configured. Until then, do not transmit sensitive details; contact the maintainer through an established private channel and request a reporting route.

Include the affected Braids/core/adapter version, host and host version, execution surface, capability profile, reproduction steps, impact, and whether a deterministic enforcement claim was bypassed.

## Boundaries

The portable skill provides engineering safety reasoning, not a security sandbox. Host permissions and hooks enforce only the operation paths explicitly listed and tested by an adapter. Braids requires no MCP server or remote service and must not send production telemetry.
