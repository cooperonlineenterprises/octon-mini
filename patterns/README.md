# Domain-Neutral Architectural Pattern Catalog

This directory is a governed source-repository catalog. It is outside the
Project Blueprint runtime kernel and every generated profile inventory.
Catalog records are design knowledge, not instructions, permission, project
facts, accepted project decisions, implementations, or readiness evidence.

Authority: `SRC-DEC-0003`, `SRC-DEC-0005`, and `SRC-DEC-0006` in
`ARCHITECTURE_DECISIONS.md`.

## Information ownership

- `catalog.json` allocates stable `PAT-####` IDs and routes active records.
- `schemas/pattern-catalog.schema.json` validates the catalog envelope.
- `schemas/pattern-record.schema.json` validates individual pattern records.
- `records/` owns current catalog records.
- `architecture-proof/` contains the optional, source-only proof family.
- `fixtures/` contains executable conformance and failure examples.

An allocated or retired pattern ID is never silently reused or reassigned.
Rejected and deprecated records remain discoverable with their rationale.
Every record explicitly carries applicability and non-applicability triggers,
exclusions, supporting and contrary evidence, compatibility, migration,
limitations, successor disposition, operator burden, and non-authority flags.

## Lifecycle

The only lifecycle states and transitions are:

- initial allocation to `candidate`;
- `candidate` to `reviewed` or `rejected`;
- `reviewed` to `experimental`, `deprecated`, or `rejected`;
- `experimental` to `reviewed`, `recommended`, `deprecated`, or `rejected`;
- `recommended` to `experimental`, `stable`, `deprecated`, or `rejected`; and
- `stable` to `deprecated`.

Allowed backward movement is deliberately narrow: an `experimental` pattern
may return to `reviewed` when evidence is insufficient, and a `recommended`
pattern may return to `experimental` when broader validation is required.
`rejected` is terminal. `deprecated` is terminal and names a successor.

## Promotion rules

- `candidate` records a problem and source basis without endorsement.
- `reviewed` requires an explicit source architecture decision and complete
  applicability, exclusion, compatibility, burden, and proof fields.
- `experimental` requires a concrete adopter or exact proof subject. Catalog
  review alone cannot enter this state.
- `recommended` requires explicit architecture review and supporting evidence
  from at least two distinct independent projects. Usage count alone is not
  evidence.
- `stable` requires prior `recommended` status plus an explicit compatibility,
  migration, maintenance, and deprecation-support commitment.
- `deprecated` requires reason, successor, compatibility window, and migration
  guidance.
- `rejected` requires retained contrary evidence or rationale so the same
  proposal is not reopened without new evidence.

Every transition is append-only in `status_history` and names its
`SRC-DEC-####` decision. The repository validator checks legal transitions,
promotion gates, references, successors, stable allocations, and the absence
of catalog assets from generated inventories.

## Adoption boundary

Catalog status never changes a generated project. An adopter must inspect its
own facts, risks, authority, compatibility, and evidence and then make any
required project-owned decision. A catalog record always has:

```json
{
  "permission_grant": false,
  "automatic_generation": false,
  "automatic_adoption": false,
  "universal_kernel": false
}
```

The catalog itself cannot elevate a pattern into the kernel. Kernel admission
requires a separate versioned architecture decision and compatibility review.
