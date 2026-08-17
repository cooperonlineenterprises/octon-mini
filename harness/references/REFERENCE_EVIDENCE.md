# Harness Reference Evidence

This record supports `harness/SPECIFICATION.md`. Paths are relative to the named
reference repository. Reference repositories are evidence only: their facts,
permissions, identities, decisions, and implementation state do not transfer
to generated projects. `CF:` identifies Commerce Foundry and `COE:` identifies
Cooper Online Enterprises; every following citation is repository-relative.

## Commerce Foundry

Representative observed patterns:

- root instruction and operating boundary: `CF:AGENTS.md`;
- harness entry and routing: `CF:AGENTS.md`,
  `CF:.agent/docs/OPERATING_MODEL.md`, and
  `CF:.agent/docs/DOCUMENTATION_TRUST.md`;
- deny-by-default policy: `CF:.agent/policies.yaml`;
- context precedence: `CF:.agent/context-rules.yaml`;
- typed schema and identifiers: `CF:.agent/schema.yaml`;
- task and artifact transitions: `CF:.agent/lifecycle.yaml`;
- declared tools and commands: `CF:.agent/tools.yaml`,
  `CF:.agent/validators.yaml`, and `CF:.agent/project.yaml`;
- durable tasks, decisions, evidence, reviews, events, checkpoints, and
  summaries: `CF:.agent/tasks/`, `CF:.agent/decisions/`,
  `CF:.agent/evidence/`, `CF:.agent/reviews/`,
  `CF:.agent/events/events.jsonl`,
  `CF:.agent/checkpoints/manifest.jsonl`, and
  `CF:.agent/summaries/`;
- executable checks and mutation fixtures:
  `CF:scripts/validate-local.sh`, `CF:scripts/strict_yaml.py`,
  `CF:tests/test_strict_yaml.py`,
  `CF:tests/test_status_consistency.py`, and
  `CF:tests/test_self_contained_runtime_policy.py`;
- routed capability example:
  `CF:.agents/skills/commerce-foundry-ux/`.

Transferable pattern: executable governance with local policy, controlled work
records, read-only checking, adversarial tests, and selectively loaded
capabilities.

Inspection qualification: Commerce Foundry's current canonical dossier target
is `CF:project-dossier/v0.2/`; the root Phase 0 dossier is historical
structural evidence. The `CF:.agents/skills/commerce-foundry-ux/` package was
untracked in a dirty working tree at inspection time, so it demonstrates an
active extension design rather than a stable committed baseline. Exact
inspection provenance and content fingerprints live in
`../../shared/reference-evidence.json`.

Non-transferable subject matter: project routes, product-specific statuses,
commands, services, accounts, active work, permissions, and recorded outcomes.

## Cooper Online Enterprises

Representative observed patterns:

- root instruction and scope: `COE:AGENTS.md`;
- harness governance and routing under `COE:.agent/`;
- canonical and path-authority mapping:
  `COE:project-dossier/AUTHORITY.md`,
  `COE:project-dossier/CANONICAL_SOURCE_MAP.md`, and
  `COE:project-dossier/machine-readable/path-authority.yaml`;
- typed traceability and registries under
  `COE:project-dossier/machine-readable/` and
  `COE:project-dossier/requirements/`;
- manifest, byte-integrity, provenance, and generated validation:
  `COE:project-dossier/MANIFEST.json`,
  `COE:project-dossier/CHECKSUMS.sha256`,
  `COE:project-dossier/provenance/`, and
  `COE:project-dossier/validation/`;
- explicit handoff routing:
  `COE:project-dossier/handoff/START_HERE.md`.

Transferable pattern: source authority classification, stable identifiers,
machine-readable traceability, byte-integrity records, provenance, validation,
and resumption guidance.

Inspection qualification: COE's dossier has generated inventory and
byte-integrity evidence but no dossier-level version/supersession ledger.
Manifest and checksum files therefore support integrity observations, not a
claim that COE implements dossier lifecycle governance.

Non-transferable subject matter: business entities, implementation claims,
providers, policies accepted by that project, and generated validation results.

## Synthesis boundary

Direct equivalents include root instruction routing, project policy/context,
controlled records, validation, and handoff. Functional equivalents include
Commerce Foundry's operational stores and COE's dossier traceability records:
they solve related provenance and resumability problems at different layers.

The extension compatibility contract, disable-without-kernel-change rule,
transactional generation/refresh protocol, strict JSON kernel,
alternate-runtime conformance contract, and cross-profile acceptance matrix
are recommendations introduced to make the specification portable and auditable.
They are not claimed as observed conventions in both sources.
