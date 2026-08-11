# Changelog

All notable blueprint contract changes are recorded here. Project-specific
snapshots do not upgrade automatically.

## 3.0.0 — Unreleased

Small-team Git and provider-neutral change-integration workflows for one to
five write-capable humans.

This unreleased source change also records accepted source-only decisions
`SRC-DEC-0001` and `SRC-DEC-0002`. They do not become generated-project
defaults and create no permission.

### Added

- a privacy-minimizing, evidence-dated collaboration profile that separates
  declared authority, observed access, activity, review capacity, concurrent
  writers, and external contribution mode without storing identities or
  granting permission;
- closed `solo_direct`, `solo_hybrid`, `pair_pr`, and `tiny_pr` workflow
  contracts plus a cross-profile `concurrent_work` modifier and an explicit
  `unsupported_team_size` result above five write-capable humans;
- a provider-neutral semantic Git and hosted-change operation catalog with
  distinct effect and authority classes, safe cleanup, conflict, tag, and
  force-with-lease boundaries, and fail-closed unknown operations;
- read-only collaboration assessment reporting, generated mutation coverage,
  and all-profile acceptance tests for topology, freshness, non-authorization,
  workflow completeness, and enterprise-workflow exclusion; and
- an executable, idempotent `2.0.0` to `3.0.0` reference migration that seeds
  an unknown collaboration state without inferring people or adopting a
  workflow.

### Changed

- assurance-profile selection now depends on project risk and control needs,
  not contributor count; team size selects only the base collaboration
  workflow;
- generated projects include the same complete small-team portfolio in every
  profile while GitHub-specific adoption remains optional and inactive;
- source CI validates feature work through `pull_request` and validates
  `push` only on `main`, with cancellation limited to superseded PR runs; and
- the blueprint, generator, harness kernel, project, tools, and validator
  contracts advance to their 3.0.0/v3-or-v2 forms.

### Migration note

This is a breaking change. Generated 2.0.0 snapshots remain independent.
Project-specific migration must preserve existing authority and decisions,
reassess collaboration from current project-owned evidence, and adopt a base
workflow through a separate accepted decision. Structural migration alone
does not establish readiness, permission, or a suitable workflow.

## 2.0.0 — 2026-08-10

Dependency-gated development progression for the domain-neutral kernel.

Under accepted source decision `SRC-DEC-0002`, `2.0.0` is a completed
historical release. Its selected but still-uncreated future annotated
`v2.0.0` tag target is exactly
`ef8f352ca32a7fbdf1131726263ff545cdd8b08a`. This changelog does not claim
that the tag already exists.

### Added

- task and plan v2 records with typed hard dependencies, structured gate and
  blocker references, and reciprocal plan-item/execution-task links;
- a deterministic, read-only `--ready-frontier` command that reports eligible
  plan items and tasks without granting authority or assigning priority;
- task dependency-cycle detection and status checks that reject execution,
  review, or completion while hard predecessors, gates, blockers, or linked
  plan conditions are unsatisfied;
- plan progression checks that require linked tasks and evidence for
  completion and reject inconsistent reciprocal links or task status;
- adversarial coverage for cycles, incomplete predecessors, gates, blockers,
  reciprocal links, reopened dependencies, and ready-frontier derivation; and
- executable, idempotent `1.0.1` to `2.0.0` migration fixtures that preserve
  stable IDs and authority, retain exact rollback evidence, and fail closed on
  ambiguous or mixed live authority;
- strict three-state target-project test, lint, build, and closure hooks plus
  an explicit shell-free project-check evidence writer;
- adoption conformance that requires assessed hooks and current matching
  evidence, and prevents adopted High-Assurance projects from retaining
  unresolved conditional or optional triggers; and
- optional, independently adoptable operations/observability and
  security/supply-chain extension contracts with strict schemas, validators,
  freshness/reference checks, and adversarial fixtures.

### Changed

- entering or re-entering execution now passes through `ready`; `blocked` and
  `reopened` tasks transition to `ready` rather than directly to
  `in_progress`;
- the ready gate now requires satisfied dependencies and gates, resolved
  structured blockers, and coherent plan links in addition to scope,
  authority, acceptance criteria, and validation planning;
- planning explicitly treats dependencies as a partial order. Current operator
  direction or an accepted priority/value/risk decision selects among
  independent ready items; dates remain provenance, freshness, expiry, or
  genuine external constraints and never determine readiness or priority; and
- structural conformance, project-harness adoption, and demonstrated
  target-project readiness are reported as distinct conclusions; read-only
  validation never runs target-project hooks or creates execution evidence;
- Standard and High Assurance contain disabled, unassessed production-control
  entry points, while Minimal remains free of those controls; and
- the harness kernel, generator, validator, dossier baseline, task record, plan
  store, lifecycle, project-command, and validator contracts advance to their
  2.0.0/v2 forms.

### Migration note

This is a breaking change. Generated `1.0.1` projects remain independent and
must use a project-specific migration; do not copy v2 kernel, validator, task,
plan, project-command, or evidence files over live project authority. The
reference migrator validates a closed representative bundle; it is not an
in-place target-project upgrader and does not run project commands.

## 1.0.1 — 2026-08-10

Historical status correction under `SRC-DEC-0002`: this version was committed
as `d94550a8acf57841eac9458897410391722beb4b` on 2026-08-10 and is retained
as an untagged, superseded source milestone rather than a completed tagged
release. Its content and migration compatibility remain supported; no
`v1.0.1` tag is to be created.

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
