# Project Blueprint 4.0 Compatibility and Deprecation

## Supported snapshots

Generated projects are independent snapshots. Version 4.0 does not create a
runtime link to Blueprint source and does not rewrite 3.x projects
automatically. Existing 3.0/3.1 snapshots may continue using their own bundled
validators, subject to their recorded limitations.

Existing 4.0 snapshots and existing `pb init|adopt|upgrade plan` invocations
remain valid without guided setup. Legacy flags map to stable setup-question
IDs; they are not removed or silently defaulted.

## Migration

- 1.0.1→2.0.0 and 2.0.0→3.0.0 remain closed reference transformations with
  executable fixtures.
- 3.0.0→3.1.0 remains the recorded additive source migration.
- 3.1.0→4.0.0 requires reviewed inventory seeding followed by the live
  three-way upgrader. An unknown pristine hash, assessed collaboration v1,
  authority conflict, deletion/move, symlink, permission change, or modified
  project-owned/governance path cannot be auto-migrated.

## Changed defaults

- scripted generation without `--profile` now fails;
- interactive init proposes Minimal and requires confirmation;
- compact is the new-project physical layout default;
- current state is derived and operator intent moves to focus;
- Git and domain extensions are trigger-installed packages;
- Context Pack schema is trigger-installed rather than a High-Assurance
  universal file;
- routine generated tests expose `fast`, `integration`, and `release` tiers;
- primitive scaffolding runs structural plus fast bounded validation, while
  guided init, adoption, upgrade, and release gates retain release staging;
- evidence-complete work may close directly from an active state without
  status-only validating/review hops; and
- the source config advances to `project-blueprint.v3`, origin to inventory v2,
  collaboration to v2, and transaction receipts to v2.
- new snapshots include an empty decision-governance register and reusable
  workbook/review templates; accepted `DEC-####` semantics are unchanged, and
  a register acceptance uses an explicit reciprocal link rather than inferred
  historical correspondence;
- requirement and gate maturity assessment is optional and never inferred from
  existing structural evidence; and
- existing handoffs require reviewed checklist reconciliation rather than
  automatic replacement.
- new snapshots include one shared governed `work.finish` engine but retain a
  disabled, non-authorizing configuration and completion hook. Existing
  snapshots receive applicable pieces only through an explicit upgrade or
  pinned Git-package update; no update may silently adopt a workflow,
  provider, check, cleanup, eligible reviewer, command hook, or authorization
  policy. A package update updates only an already installed exact-pristine
  portfolio; the core engine and schema arrive through the reviewed Blueprint
  upgrade.
- guided setup is opt-in orchestration over the existing planners. Existing
  projects receive its CLI support and schemas only through an explicit
  Blueprint upgrade or skill-package update. The source question catalog is
  not projected into target authority, and new questions remain unanswered or
  deferred rather than receiving defaults.

## Deprecated entry points

Primitive scripts remain supported advanced interfaces during 4.x, but the
workflow-oriented `scripts/pb.py` and generated `./pb` are the documented
paths. Direct hand-editing of `.agent/state/current.json` is unsupported.
Direct copying of package directories or Git workflow files is unsupported
because it lacks content/decision/receipt binding.
Directly copying `pb_finish.py`, enabling its hook without a reviewed project
configuration, or treating a prior authorization as standing permission is
also unsupported.
Directly copying a setup session between targets, hand-editing its digest, or
treating an interview selection as accepted authority is unsupported.
The legacy read-only `validate.py --assess-collaboration` report remains a
compatibility diagnostic; new facts and workflow proposals use collaboration
plan/apply so evidence and changes are reviewable and receipted.

No deprecation authorizes deletion of a project-owned file or record. Moves,
representation changes, and stable-ID changes require explicit migration.
