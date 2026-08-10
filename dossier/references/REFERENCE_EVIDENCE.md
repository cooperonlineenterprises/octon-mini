# Dossier Reference Evidence

This file classifies the evidence behind the reusable dossier model. It does
not make either reference repository a dependency or authority for generated
projects. Evidence labels and repository aliases are defined in
[`../BLUEPRINT.md`](../BLUEPRINT.md). Reproducible checkout identity, observed
role, authority classification, and dirty-state metadata live in the shared
[`reference-evidence.json`](../../shared/reference-evidence.json).

## Authority resolution

### Commerce Foundry

`CF:AGENTS.md` explicitly identifies `CF:project-dossier/v0.2/` as the current
canonical target-state dossier. Within that package:

- `CF:project-dossier/v0.2/CANONICAL_SOURCE_MAP.md` routes canonical,
  conformance, implementation-plan, transition, handoff, and historical
  concerns;
- `CF:project-dossier/v0.2/canonical/` is current intended-state authority;
- `CF:project-dossier/v0.2/conformance/` is maintained current-state
  assessment;
- `CF:project-dossier/v0.2/implementation-plan/` is future sequencing;
- `CF:project-dossier/v0.2/transition/` and
  `CF:project-dossier/v0.2/SUPERSESSION_MAP.md` govern the documented
  transition and supersession relationship; and
- `CF:project-dossier/v0.2/baseline/` is explicitly historical.

The Phase 0 material directly under `CF:project-dossier/` is a retained
historical baseline, even when cited below to demonstrate an artifact family
that is more detailed there. Such citations are marked **historical evidence**
and never treated as current CF authority.

### Cooper Online Enterprises

`COE:AGENTS.md`, `COE:project-dossier/AUTHORITY.md`, and
`COE:project-dossier/CANONICAL_SOURCE_MAP.md` distinguish:

- `COE:project-dossier/canonical/` and the named machine-readable stores as
  intended target;
- `COE:project-dossier/current-state/` as dated observation;
- `COE:project-dossier/conformance/` as evidence-based comparison;
- `COE:project-dossier/implementation-plan/` as planning;
- `COE:project-dossier/provenance/` as source history and limitations; and
- `COE:project-dossier/MANIFEST.json`,
  `COE:project-dossier/CHECKSUMS.sha256`, and
  `COE:project-dossier/validation/validation-report.json` as generated
  point-in-time evidence.

No direct COE dossier-version or supersession-ledger equivalent was observed.
Its manifest and checksums are therefore evidence for integrity—not functional
equivalents of CF’s supersession package.

## Current, high-value evidence

### Entry, authority, and lifecycle

- **[Observed: CF, current target]**
  `CF:project-dossier/v0.2/README.md`
- **[Observed: CF, current target]**
  `CF:project-dossier/v0.2/CANONICAL_SOURCE_MAP.md`
- **[Observed: CF, current lifecycle]**
  `CF:project-dossier/v0.2/SUPERSESSION_MAP.md`
- **[Observed: CF, historical baseline classification]**
  `CF:project-dossier/v0.2/baseline/README.md`
- **[Observed: COE, current navigation]**
  `COE:project-dossier/README.md`
- **[Observed: COE, current interpretation]**
  `COE:project-dossier/AUTHORITY.md`
- **[Observed: COE, current source routing]**
  `COE:project-dossier/CANONICAL_SOURCE_MAP.md`

### Definition, requirements, and models

- **[Observed: CF, current target]**
  `CF:project-dossier/v0.2/canonical/platform-definition.md`
- **[Observed: CF, current target]**
  `CF:project-dossier/v0.2/canonical/architecture.md`
- **[Observed: CF, current target]**
  `CF:project-dossier/v0.2/canonical/domain-data-model.md`
- **[Observed: CF, historical detail]**
  `CF:project-dossier/docs/requirements/requirements-traceability.md`
- **[Observed: COE, current target]**
  `COE:project-dossier/canonical/executive-project-definition.md`
- **[Observed: COE, current target]**
  `COE:project-dossier/canonical/requirements-and-constraints.md`
- **[Observed: COE, authoritative structured target]**
  `COE:project-dossier/machine-readable/requirements.yaml`
- **[Observed: COE, current target]**
  `COE:project-dossier/canonical/technical-architecture.md`

### Current state, conformance, plan, and registers

- **[Observed: CF, maintained current-state assessment]**
  `CF:project-dossier/v0.2/agent-handoff/current-implementation-status.md`
- **[Observed: CF, maintained conformance]**
  `CF:project-dossier/v0.2/conformance/README.md`
- **[Observed: CF, maintained planning]**
  `CF:project-dossier/v0.2/implementation-plan/dependency-roadmap.md`
- **[Observed: CF, maintained risk register]**
  `CF:project-dossier/v0.2/implementation-plan/risk-register.md`
- **[Observed: COE, current-state method and evidence]**
  `COE:project-dossier/current-state/repository-baseline.md`
- **[Observed: COE, authoritative findings]**
  `COE:project-dossier/conformance/findings.yaml`
- **[Observed: COE, authoritative plan]**
  `COE:project-dossier/implementation-plan/plan.yaml`
- **[Observed: COE, current registers]**
  `COE:project-dossier/registers/`

### Provenance, validation, integrity, and handoff

- **[Observed: CF, current external-fact verification]**
  `CF:project-dossier/v0.2/verification/verification-manifest.md`
- **[Observed: CF, current validation evidence]**
  `CF:project-dossier/v0.2/machine-readable/validation-report.json`
- **[Observed: CF, current handoff]**
  `CF:project-dossier/v0.2/agent-handoff/START_HERE.md`
- **[Observed: CF, current integrity]**
  `CF:project-dossier/v0.2/CHECKSUMS.md`
- **[Observed: COE, current provenance]**
  `COE:project-dossier/provenance/source-index.yaml`
- **[Observed: COE, generated integrity]**
  `COE:project-dossier/MANIFEST.json`
- **[Observed: COE, generated integrity]**
  `COE:project-dossier/CHECKSUMS.sha256`
- **[Observed: COE, generated validation evidence]**
  `COE:project-dossier/validation/validation-report.json`
- **[Observed: COE, current handoff]**
  `COE:project-dossier/handoff/START_HERE.md`

### Specialist and progressive-disclosure patterns

- **[Observed: CF, current specialist target]**
  `CF:project-dossier/v0.2/canonical/security-architecture.md`
- **[Observed: CF, current operations target]**
  `CF:project-dossier/v0.2/canonical/monitoring-lifecycle-model.md`
- **[Observed: CF, current evaluation pattern]**
  `CF:project-dossier/v0.2/agent-handoff/evaluations/task-quality-rubric.md`
- **[Observed: CF, current context-pack pattern]**
  `CF:project-dossier/v0.2/agent-handoff/context-packs/`
- **[Observed: COE, current specialist target]**
  `COE:project-dossier/canonical/security-privacy-legal.md`
- **[Observed: COE, current domain model]**
  `COE:project-dossier/canonical/portfolio-and-content-model.md`

## New recommendations

The three-level artifact identity model, authoritative project-local artifact
registry, derived catalog and path-authority views, trigger/applicability
records, profile-independent refresh, review-date semantics, strict JSON
kernel, and domain-neutral generator are **[Recommended]** additions. They are
not represented as conventions observed in both projects.

## Transfer boundary

Generated projects receive generalized structures, schemas, validation
patterns, and evidence vocabulary. They do not receive reference-project
facts, decisions, permissions, identities, implementation status, readiness,
credentials, endpoints, personal information, or history.
