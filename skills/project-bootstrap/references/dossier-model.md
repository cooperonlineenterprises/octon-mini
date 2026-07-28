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

Use stable IDs and one definition source per concept. Prefer structured
requirements, findings, plans, sources, and evidence when the standard or
high-assurance profile applies.

`ARTIFACT_CATALOG.json` is generated from the blueprint artifact taxonomy.
`machine-readable/path-authority.json` is generated from that catalog and must
cover every dossier file. Manifests, checksums, and validation reports are
derived point-in-time evidence and never independently edited truth.
