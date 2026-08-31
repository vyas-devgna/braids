# User, developer, and deployment effects

Load this reference when a change affects interaction behavior, accessibility, developer workflow, build/release, operations, migration, or deployment.

Trace the affected journey rather than treating backend/code shape as the whole system:

- end-user response, errors, recovery, responsiveness, accessibility and compatibility;
- developer setup, edit/test/debug cycle, local resources, CI time, and cognitive/maintenance burden;
- deployment prerequisites, configuration, secrets, rollout, observability, upgrade/downgrade, rollback and operator recovery.

Turn each material concern into an observable scenario. A runtime improvement that makes interaction less responsive, requires fragile mandatory tooling, or creates disproportionate deployment burden may lose on lifecycle value.

Verify behavior through the relevant interface: interaction/acceptance checks for UX, accessible semantics and keyboard/screen-reader behavior when changed, clean setup/build for developer experience, and clean install/upgrade/rollback/uninstall for deployment.
