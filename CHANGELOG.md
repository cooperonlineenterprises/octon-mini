# Changelog

All notable blueprint contract changes are recorded here. Project-specific
snapshots do not upgrade automatically.

## 1.0.1 — 2026-07-27

Release-blocker remediation for the stable domain-neutral kernel.

### Fixed

- every profile now has a supported transactional refresh path for catalogs,
  path authority, manifests, and profile-specific derived evidence;
- project-local dossier registration supports adding, removing, renaming, and
  superseding project artifacts without editing derived files;
- the dossier taxonomy separates conceptual artifact types, blueprint
  representations, and project artifact records and supplies self-contained
  schemas for their machine-readable forms;
- validator coverage now enforces declared lifecycle, record-reference,
  authority, gate, supersession, path-confinement, extension, redaction, and
  read-only boundaries rather than merely documenting them;
- generated validators enforce the selected profile's required governed-file
  inventory and reject missing, misplaced, or unknown live-governance
  material;
- `current.json` is a closed, project-maintained resumption index whose task,
  decision, evidence, external-authority, and adoption references must resolve
  and remain status-coherent; it cannot authorize work;
- task and artifact closure plus readiness gates require fresh, subject-bound
  passing evidence; waivers and approval-backed gates require current,
  externally sourced authority evidence that is neither revoked nor
  superseded;
- adoption planning reports conservative functional-equivalent candidates
  while remaining read-only and non-authorizing;
- generation transaction IDs are unpredictable and unique rather than
  deterministically derived;
- reference evidence has explicit provenance and authority classification, and
  citations are checked against that registry.

### Added

- conditional approval, coordination, recovery, evaluation, and metric
  contracts for projects whose risk triggers require them;
- closed agent, workflow, and skill-provenance JSON contracts with exact
  included-file provenance, pinned fingerprints for adopted imports, strict
  deprecation/removal rules, and adopted dependency-chain validation;
- traceable adoption-decision contracts: generated baselines remain null and
  unadopted, while adopted harnesses and capabilities resolve to accepted
  externally authoritative decisions;
- adversarial tests for catalog traversal, nested instructions, stale
  derivatives, malformed extensions, unsafe environment access, duplicate
  identifiers, invalid semantic versions, record references, and source-only
  validation;
- a `1.0.0` to `1.0.1` migration guide and reproducible repository-contained
  skill-package validation.

### Changed

- Python 3.11 remains the reference implementation, while an alternate pinned
  runtime is permitted only when it passes the published conformance fixtures;
- extension checks run with a least-privilege environment and detect persistent
  repository mutation; prevention still requires an external no-write boundary;
- validation reports are bounded to checks actually performed and explicitly
  disclose scope, result, failures, skipped checks, limitations, Git
  dirty-state assessment, and external effects; structural success does not
  imply project readiness.

## 1.0.0 — 2026-07-27

First stable domain-neutral kernel release.

### Added

- self-contained project dossier blueprint with evidence-labeled reference
  crosswalk, 4-digit artifact taxonomy, coverage profiles, core
  specifications, lifecycle, governance, adoption gates, and new
  recommendations;
- evidence-labeled 17-section harness blueprint and source-evidence record;
- strict JSON seven-file governance kernel and local schema snapshot;
- generated artifact catalog and per-file path-authority mirror;
- transactional new-project generation and read-only existing-project
  adoption planning;
- cross-record reference, transition, traceability, plan-DAG, nested
  instruction, extension, secret-redaction, checksum, and freshness
  validation;
- restrictions-only versioned extension API with a disable-safe reference
  extension;
- mutually consistent high-assurance refresh outputs with shared generation
  IDs;
- Minimal, Standard, and High-Assurance end-to-end and adversarial acceptance
  tests;
- migration, release, installation, and CI guidance.

### Changed

- canonical structured outputs moved from constrained YAML to strict JSON;
- stable dossier record and artifact identifiers use four numeric digits;
- generated dossier registries start empty and unadopted rather than seeding
  active or authoritative project claims;
- integrity fingerprints cover the whole repository by default.

### Removed

- direct in-place generation into existing repositories;
- regex-only constrained-YAML validation;
- disconnected high-assurance checksum refresh behavior.
