# Octon Mini Velocity Implementation Program

This source-only plan tracks the bounded implementation work authorized for the
4.0.0 velocity program. It is not generated into projects, grants no permission,
and is not evidence that a target project is adopted or ready.

## Invariants shared by every workstream

- Dossier content remains documentation, never permission.
- Generated policy remains deny-by-default and non-authorizing.
- Mechanical writers may reference existing facts, authority, decisions, and
  evidence but may not create them.
- Every proposed mutation is previewable, content-addressed, fingerprint-bound,
  staged, validated, receipted, recoverable, and has no force bypass.
- `check` and every planning or diagnostic command remain read-only.
- Generated-integrity and project-check evidence writers remain explicit and
  separate.
- Stable IDs, profile choice, collaboration band, authority-bearing files, and
  external effects remain explicitly project-owned.

## Dependency-ordered workstreams

| Order | Workstream | Owner role | Depends on | Executable completion evidence |
|---:|---|---|---|---|
| 1 | PBV-10 profile and inventory manifest | Octon Mini source-contract maintainer | none | manifest/schema validation, derived generator and acceptance projections, criterion 15 reported |
| 2 | PBV-05 validation tiers and scale isolation | Harness validation maintainer | PBV-10 | bounded mutation fixtures, retained full-tree integration cases, 2k/20k benchmarks |
| 3 | PBV-09 diagnostics and profile correction | Harness diagnostics maintainer | PBV-10 | versioned JSON diagnostics, unchanged-tree doctor tests, explicit-profile negative tests |
| 4 | Shared proposal and transaction framework | Harness transaction maintainer | PBV-09 | plan/apply/receipt/rollback schemas plus stale, interruption, collision, and rollback mutations |
| 5 | PBV-01 lifecycle and derived state | Harness lifecycle maintainer | transaction framework | work commands, derived current state, focus source, lifecycle/recovery tests, migration |
| 6 | PBV-06 registry reconciliation | Dossier registry maintainer | transaction framework | add/rename/remove/combine/supersede plans and stable-ID mutation tests |
| 7 | PBV-11 checks and evidence lifecycle | Harness evidence maintainer | transaction framework | selective routing, full adoption verification, immutable archives, rebuilt current index |
| 8 | PBV-03 init and detector recipes | Bootstrap maintainer | lifecycle, diagnostics, transaction framework | interactive and scriptable init across profiles and archetypes |
| 9 | PBV-07 collaboration v2 and SCM trigger | Collaboration-contract maintainer | transaction framework, guided init | conditional evidence matrix, v1 migration, Git/non-Git fixtures |
| 10 | PBV-08 triggered domain packages | Extension-contract maintainer | manifest, transaction framework | trigger assessment, content-addressed installation, absence/non-applicability mutations |
| 11 | PBV-02 semantic adoption | Adoption maintainer | detectors, transaction framework | bounded inspection, exclusions, semantic plan, fingerprint-bound apply, archetype fixtures |
| 12 | PBV-04 live upgrades | Migration maintainer | adoption, transaction framework | three-way classification, safe apply, receipts, rollback refusal, cross-version fixtures |
| 13 | Compact representation layout | Dossier representation maintainer | registry reconciliation, upgrades | compact/separate selection, registry migration, ownership/lifecycle separation tests |

Owner roles identify the contract surface responsible for review; they are not
identities, principals, approvers, or standing authority.

## Common plan, apply, rollback, and diagnostic behavior

Planning reads instructions and target state, records bounded source evidence,
classifies conflicts and exclusions, and emits an immutable proposal with a
canonical digest. Applying requires that exact reviewed digest, verifies every
governing and per-path fingerprint, stages the full operation, validates the
stage, and writes an exact receipt. Rollback verifies post-apply hashes and
refuses any path changed since the receipt. Diagnostics group root causes and
dependent symptoms, identify the owning source, and distinguish derived-only
repair from project decisions or authorization gates.

## Validation boundary

Fast tests cover pure contracts and bounded mutations. Full-tree integration is
retained for fingerprint, symlink, ignored-file, host-metadata, refresh,
read-only, adoption, upgrade, and release boundaries. Human usability targets
require timed project exercises and are never inferred from structural tests.
