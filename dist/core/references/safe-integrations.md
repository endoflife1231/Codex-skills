# Safe Integrations

The core distribution should remain predictable even when optional integrations are unavailable.

## Default rule

If an integration is optional, host-specific, paid, network-dependent, or potentially destructive, it must not be required for the core to work.

## What stays opt-in

- hooks
- browser automation that depends on extra setup
- external services and APIs
- deployment and publish flows
- Graphify installation and update flows
- package installs needed only for optional skills

## What the product should do instead

- check whether the dependency or CLI exists
- explain what is missing
- offer the optional path only when relevant
- degrade gracefully when the integration is absent

## Unsafe examples

Dangerous or host-specific command examples may exist in references for documentation value, but they should not appear in default-facing core policy as standard behavior.

Examples that require extra care:

- destructive file or git operations
- `curl | sh`
- hidden hook installation
- forced dependency removal or downgrades
- commands that publish data externally

## Why this improves the product

This filter does not reduce the power ceiling of the distribution. It improves the default experience by making the pack:

- cleaner
- more predictable
- easier to trust
- easier to support across environments

Optional power is still available, but it is activated deliberately instead of leaking into the default workflow.
