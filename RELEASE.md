# Release and Distribution

## Current source version

- Blueprint version: `3.0.0`
- Harness kernel: `3.0.0`
- Extension API: `harness.extension.v1`
- Minimum runtime: Python `3.11`
- Canonical structured format: strict JSON

Version `3.0.0` is the current source target and is not represented as a
completed release until its exact integrated `main` revision passes hosted CI
and an annotated `v3.0.0` tag is created in a separately authorized release
phase. Accepted historical release representation is recorded by
`SRC-DEC-0002` below. At the 2026-08-11 observation, only `v1.0.0` existed
locally and remotely and no GitHub Releases existed. Major versions may break
paths, schemas, IDs, lifecycle semantics, extension compatibility, or migration
behavior. Minor versions add backward-compatible artifacts or checks. Patch
versions correct behavior without changing accepted contracts.

## SRC-DEC-0002 — Historical release representation

| Field | Accepted decision |
|---|---|
| Status | `accepted` |
| Authority | Explicit repository-owner approval on 2026-08-11 |
| Scope | Release representation for this `project-blueprint` source repository only |
| `1.0.1` | Untagged, superseded source milestone; preserve its content and migration compatibility, but do not create `v1.0.1` |
| `2.0.0` | Completed historical release; its selected but still-uncreated future annotated `v2.0.0` tag target is exactly `ef8f352ca32a7fbdf1131726263ff545cdd8b08a` |
| `3.0.0` | Unreleased source target until its exact integrated `main` revision passes hosted CI and is tagged under separate release authority |
| Permission effect | None; this decision records historical representation and a future target but does not authorize creating or pushing a tag or GitHub Release |

The `1.0.1` source milestone was committed as
`d94550a8acf57841eac9458897410391722beb4b` on 2026-08-10, correcting the
previous changelog date of 2026-07-27. It remains the compatibility source for
the `1.0.1` to `2.0.0` migration, but it is not a completed tagged release and
must not receive a `v1.0.1` tag.

Version `2.0.0` is a completed historical release. Its future annotated tag
must target exactly `ef8f352ca32a7fbdf1131726263ff545cdd8b08a`. The earlier
`c7bbbb6525d1135cd3acb3b64743240f5c00ec50` revision is excluded because its
hosted validation failed and two corrective commits followed it. The
`v2.0.0` tag has not been created. Any future annotation must disclose its
actual creation date and must not be backdated.

Version `3.0.0` remains untagged and unreleased. Neither this record nor the
release gate authorizes a tag, GitHub Release, merge, or hosted-setting change.

## Release gate

Before tagging a release:

1. run `validate_skill_package.py` and `verify_reference_evidence.py`;
   when the reference checkouts are available, rerun reference verification
   with an explicit `--reference-root ID=/absolute/path` for each registered
   repository and disclose any unavailable checkout;
2. run `validate_blueprint.py`;
3. run both `test_migration_1_0_1_to_2_0_0.py` and
   `test_migration_2_0_0_to_3_0_0.py`, and confirm valid transformation,
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
9. inspect generated profile snapshots: every profile must contain the same
   non-authorizing small-team workflow portfolio, Minimal must not inherit
   production controls, Standard must retain traceability and disabled
   extension entry points, and High Assurance must add unassessed
   trigger/control entry points;
10. confirm no generated profile contains project facts, collaborator
    identities, hosted settings, secrets, permissions, accepted decisions,
    configured hooks, passing evidence, providers, or readiness claims;
11. commit the exact validated source and publish its required self-PR under
    current authority;
12. after a separately authorized `merge_commit` integration, confirm the full
    hosted matrix passes on the exact integrated `main` revision; and
13. only with separate current release authority, create an annotated
    `v<version>` tag on that exact validated integrated revision.

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
