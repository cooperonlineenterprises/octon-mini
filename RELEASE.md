# Release and Distribution

## Current release

- Blueprint version: `2.0.0`
- Harness kernel: `2.0.0`
- Extension API: `harness.extension.v1`
- Minimum runtime: Python `3.11`
- Canonical structured format: strict JSON

Version `2.0.0` is the current stable domain-neutral kernel. Major versions may break
paths, schemas, IDs, lifecycle semantics, extension compatibility, or
migration behavior. Minor versions add backward-compatible artifacts or
checks. Patch versions correct behavior without changing accepted contracts.

## Release gate

Before tagging a release:

1. run `validate_skill_package.py` and `verify_reference_evidence.py`;
   when the reference checkouts are available, rerun reference verification
   with an explicit `--reference-root ID=/absolute/path` for each registered
   repository and disclose any unavailable checkout;
2. run `validate_blueprint.py`;
3. run `test_migration_1_0_1_to_2_0_0.py` and confirm valid transformation,
   exact idempotence, rollback evidence, and every fail-closed fixture;
4. run `test_acceptance.py`;
5. install the skill into a fresh temporary destination, run the installed
   package, blueprint, reference, and acceptance validators from that
   destination, and generate and check all three profiles from the bundled
   source;
6. when available, run the skill-creator `quick_validate.py` as a compatibility
   check against the installed Codex tooling;
7. confirm CI passes on the declared Python and OS matrix; local success is
   not evidence that hosted CI passed;
8. review the changelog and every migration from the previous release;
9. inspect generated profile snapshots: Minimal must not inherit production
   controls, Standard must retain traceability and disabled extension entry
   points, and High Assurance must add unassessed trigger/control entry points;
10. confirm no generated profile contains project facts, secrets, permissions,
    accepted decisions, configured hooks, passing evidence, providers, or
    readiness claims;
11. commit the exact validated source; and
12. create an annotated `v<version>` tag on that commit.

Do not move a published version tag. A correction receives a new patch
version.

## Installation and provenance

`skills/project-bootstrap/scripts/install_skill.py` installs a collision-safe,
self-contained personal skill snapshot with the required dossier taxonomy,
schemas, migrations, and release metadata. It smoke-tests that staged copy
before placement. Installed and generated snapshots record their source version
but do not track or execute later blueprint changes automatically. Upgrades are
migrations.

## Distribution license decision

No public redistribution license is asserted by this repository blueprint.
Private/internal use is technically supported, but public distribution must
pause until the repository owner chooses and adds an appropriate license after
legal review. This is an explicit owner decision, not a missing technical
default; the generator never inserts a license into target projects.

## Supported and unsupported claims

Release acceptance supports claims about structure, syntax, traceability,
portability, dependency progression, adoption conformance, migration behavior,
mutation resistance, and extension compatibility within the declared
validator scope. It does not certify a generated project's implementation,
security, privacy, accessibility, legal compliance, operations,
organizational approval, or readiness.
