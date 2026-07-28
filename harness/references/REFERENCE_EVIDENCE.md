# Harness Reference Evidence

This record supports `harness/BLUEPRINT.md`. Paths are relative to the named
reference repository. Reference repositories are evidence only: their facts,
permissions, identities, decisions, and implementation state do not transfer
to generated projects.

## Commerce Foundry

Representative observed patterns:

- root instruction and operating boundary: `AGENTS.md`;
- harness entry and routing: `.agent/START_HERE.md`;
- deny-by-default policy: `.agent/policy.yaml`;
- context precedence: `.agent/context.yaml`;
- typed schema and identifiers: `.agent/schema.yaml`;
- task and artifact transitions: `.agent/lifecycle.yaml`;
- declared tools and commands: `.agent/tools.yaml`,
  `.agent/validators.yaml`, and `.agent/project.yaml`;
- durable tasks, decisions, evidence, reviews, and state: `.agent/tasks/`,
  `.agent/decisions/`, `.agent/evidence/`, `.agent/reviews/`, and
  `.agent/state/`;
- executable checks and mutation fixtures: `.agent/scripts/`,
  `.agent/tests/`, and their fixture directories;
- routed capability packages: `.agents/agents/`, `.agents/skills/`, and
  `.agents/workflows/`.

Transferable pattern: executable governance with local policy, controlled work
records, read-only checking, adversarial tests, and selectively loaded
capabilities.

Non-transferable subject matter: project routes, product-specific statuses,
commands, services, accounts, active work, permissions, and recorded outcomes.

## Cooper Online Enterprises

Representative observed patterns:

- root instruction and scope: `AGENTS.md`;
- harness governance and routing under `.agent/`;
- canonical and path-authority mapping:
  `project-dossier/AUTHORITY.md`,
  `project-dossier/CANONICAL_SOURCE_MAP.md`, and
  `project-dossier/machine-readable/path-authority.yaml`;
- typed traceability and registries under
  `project-dossier/machine-readable/` and
  `project-dossier/requirements/`;
- manifest, byte-integrity, provenance, and generated validation:
  `project-dossier/MANIFEST.json`, `project-dossier/CHECKSUMS.sha256`,
  `project-dossier/provenance/`, and `project-dossier/validation/`;
- explicit handoff routing: `project-dossier/handoff/START_HERE.md`.

Transferable pattern: source authority classification, stable identifiers,
machine-readable traceability, byte-integrity records, provenance, validation,
and resumption guidance.

Non-transferable subject matter: business entities, implementation claims,
providers, policies accepted by that project, and generated validation results.

## Synthesis boundary

Direct equivalents include root instruction routing, project policy/context,
controlled records, validation, and handoff. Functional equivalents include
Commerce Foundry's operational stores and COE's dossier traceability records:
they solve related provenance and resumability problems at different layers.

The extension compatibility contract, disable-without-kernel-change rule,
transactional generation/refresh protocol, Python runtime floor, strict JSON
kernel, and cross-profile acceptance matrix are recommendations introduced to
make the blueprint portable and auditable. They are not claimed as observed
conventions in both sources.
