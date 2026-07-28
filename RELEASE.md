# Release and Distribution

## Current release

- Blueprint version: `1.0.0`
- Harness kernel: `1.0.0`
- Extension API: `harness.extension.v1`
- Minimum runtime: Python `3.11`
- Canonical structured format: strict JSON

Version `1.0.0` is the stable domain-neutral kernel. Major versions may break
paths, schemas, IDs, lifecycle semantics, extension compatibility, or
migration behavior. Minor versions add backward-compatible artifacts or
checks. Patch versions correct behavior without changing accepted contracts.

## Release gate

Before tagging a release:

1. run `validate_blueprint.py`;
2. run `test_acceptance.py`;
3. run the skill-creator `quick_validate.py`;
4. confirm CI passes on the declared Python and OS matrix;
5. review the changelog and every migration from the previous release;
6. confirm generated Minimal, Standard, and High-Assurance snapshots contain
   no project facts, secrets, permissions, accepted decisions, or readiness
   claims;
7. commit the exact validated source; and
8. create an annotated `v<version>` tag on that commit.

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
portability, mutation resistance, and extension compatibility within the
declared validator scope. It does not certify a generated project's
implementation, security, privacy, accessibility, legal compliance,
operations, organizational approval, or readiness.
