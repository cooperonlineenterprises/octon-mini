# Dossier Model

Read the first available dossier definition:

- source checkout: `../../../dossier/BLUEPRINT.md`;
- installed bundle: `../assets/blueprint-source/dossier/BLUEPRINT.md`.

The essential rule is semantic separation:

- canonical target answers what should exist;
- current state answers what was observed;
- conformance compares the two;
- plans describe future work;
- evidence supports bounded claims;
- provenance describes source origin;
- handoff is a compact view;
- history is never current authority.

Use three explicit ID levels: conceptual artifact-type IDs, `REP-####`
physical-representation IDs, and schema-governed project record IDs. They are
unique within their typed namespace and never silently reused. Prefer
structured requirements, findings, plans, sources, and evidence when the
standard or high-assurance profile applies.

Treat plan `depends_on` edges as hard `PLAN-####` prerequisites. Derive the
ready frontier from completed predecessors, passed or validly waived gates,
resolved structured blockers, populated acceptance/evidence contracts, and
reciprocal plan/task links. Dates remain provenance, freshness, expiry, or
explicit external constraints and never determine readiness or priority.

`machine-readable/artifact-registry.json` is the authoritative project-local
metadata source, initially seeded from the blueprint taxonomy. Maintain
artifact types, representations, source direction, applicability, ownership,
and substantive review state there. `ARTIFACT_CATALOG.json` and
`machine-readable/path-authority.json` are generated mirrors and must cover
every dossier file. Manifests, checksums, and validation reports are derived
point-in-time evidence and never independently edited truth.

A generation date is provenance, not a review or observation. Conditional and
optional conceptual types begin `not_assessed`; physical entry-point presence
does not establish applicability. A `not_applicable` type remains in the
registry with its dated assessor/rationale even after its representation is
removed. `combined` is a representation state and requires multiple
required/applicable artifact-type IDs.
