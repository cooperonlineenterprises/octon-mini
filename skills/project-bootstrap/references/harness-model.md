# Harness Model

Read the first available harness definition:

- source checkout: `../../../harness/BLUEPRINT.md`;
- installed bundle: `../assets/blueprint-source/harness/BLUEPRINT.md`.

## Required layers

Generate the smallest justified profile around:

1. short root instruction routing;
2. the seven-file `.agent/` governance kernel;
3. project profile and extension contracts;
4. operational records and compact current state; and
5. optional `.agents/` capability packages and generated integrity.

The harness is project-local and subordinate to higher authority. Generated
policy remains non-authorizing and deny-by-default. Do not transfer
permissions, accepted decisions, current status, evidence, identities,
endpoints, or domain constants from this blueprint or another project.

## Information owners

- permission boundary: `.agent/policy.json`;
- precedence and trust: `.agent/context.json`;
- IDs and statuses: `.agent/schema.json`;
- state transitions: `.agent/lifecycle.json`;
- tool contracts: `.agent/tools.json`;
- commands and checks: `.agent/validators.json`;
- stable project hooks: `.agent/project.json`;
- active work: `.agent/tasks/`;
- durable intent: `.agent/decisions/`;
- direct observation: `.agent/evidence/`;
- concise resumption: `.agent/state/`; and
- generated integrity: `.agent/generated/`, always non-authoritative.

The kernel uses strict JSON with duplicate-key rejection and a local schema
snapshot. Domain behavior enters only through a registered,
restrictions-only extension that declares compatibility, confined paths,
provenance, side effects, and a structured validator.

## Adoption boundary

Scaffolding proves only that the baseline files were generated consistently.
Target-project adoption must inspect actual scope and risks, resolve or
explicitly classify sentinels, record the authority posture, configure real
commands, run read-only checks and mutation tests in a clean environment, and
complete a real task lifecycle.
