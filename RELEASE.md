# Release and Distribution

## Current development version

- Product and generator: Octon Mini `4.0.0` (unreleased)
- Bootstrap capability: Octon Mini Project Bootstrap
- Bootstrap skill ID: `octon-mini-project-bootstrap`
- Harness kernel: `4.0.0`
- Source license: MIT No Attribution (`MIT-0`)
- Compatibility: clean product, command, protocol, provenance, skill, and
  generated-path break with independent snapshots and reviewed cross-brand
  migration

Version `4.0.0` implements the source-only velocity program recorded in
`VELOCITY_ROADMAP.md`. It is not yet a completed release, tag, GitHub Release,
or target-project adoption decision. Existing snapshots remain independent and
are not updated automatically. Upgrade automation is limited to exact-pristine
non-authoritative implementation assets, safe additions, and explicit derived
regeneration; all authority-bearing or ambiguous paths require reviewed
dispositions and exact digest acceptance.

Octon Mini 4.0.0 is the breaking successor to Project Blueprint 3.x. `octon`
is the sole current command; no `pb` compatibility command exists. Upgrade is
an explicit reviewed Project Blueprint 3.x→Octon Mini 4.0.0 migration.

The GitHub repository rename to `cooperonlineenterprises/octon-mini` and the
local project-directory rename to `octon-mini` are complete. The repository is
currently public. Octon Mini 4.0.0 remains unreleased: no `v4.0.0` tag, GitHub
Release, or package publication has occurred.

Accepted source decision `SRC-DEC-0014` records this owner-directed identity
and clean-break migration. It created no external operational authority and did
not itself authorize the later repository rename, visibility change,
publication, or release. Recording the present observed state does not create
continuing authority for another external action.

Accepted source decision `SRC-DEC-0015` records the technical post-rebrand
audit remediation and the license input that was still unset at that time.
Accepted source decision `SRC-DEC-0016` separately records the later
owner-approved MIT-0 source license. Neither decision grants runtime permission,
release authority, publication authority, or repository-setting authority.

Accepted source decision `SRC-DEC-0013` narrowly permits the shared governed
small-team work-completion exception to the repository-local transaction
boundary. It creates no delivery authority for this repository or any target
project. The capability and automatic event hook are generated disabled;
external apply requires separate exact current task-scoped authorization and
uses resumable progress evidence rather than an atomic rollback claim.

## Current completed historical release

- Product: Project Blueprint `3.0.0`
- Harness kernel: `3.0.0`
- Extension API: `harness.extension.v1`
- Minimum runtime: Python `3.11`
- Canonical structured format: strict JSON

Project Blueprint version `3.0.0` is the current completed historical release.
Pull request #2 was
integrated with `merge_commit` at
`1af3c1f85cd17e2c840857ad720e1a27e874585a` on 2026-08-11. GitHub Actions run
`31539907441` then passed the complete 12-job matrix on that exact `main`
revision, and the annotated `v3.0.0` tag was created on that revision later the
same day. At this post-release reconciliation, annotated `v1.0.0`, `v2.0.0`,
and `v3.0.0` tags exist locally and remotely; no GitHub Release exists. Major
versions may break paths, schemas, IDs, lifecycle semantics, extension
compatibility, or migration behavior. Minor versions add backward-compatible
artifacts or checks. Patch versions correct behavior without changing accepted
contracts.

## SRC-DEC-0002 — Historical release representation

| Field | Accepted decision |
|---|---|
| Status | `accepted` |
| Authority | Explicit repository-owner approval on 2026-08-11 |
| Scope | Release representation for this `project-blueprint` source repository only |
| `1.0.1` | Untagged, superseded source milestone; preserve its content and migration compatibility, but do not create `v1.0.1` |
| `2.0.0` | Completed historical release; its annotated `v2.0.0` tag was created on 2026-08-11 and targets exactly `ef8f352ca32a7fbdf1131726263ff545cdd8b08a` |
| `3.0.0` | Completed release; its annotated `v3.0.0` tag was created on 2026-08-11 and targets exactly `1af3c1f85cd17e2c840857ad720e1a27e874585a` after the full hosted `main` matrix passed |
| Permission effect | None; this decision and record do not authorize moving a published tag, creating a GitHub Release, or performing a later release operation |

The `1.0.1` source milestone was committed as
`d94550a8acf57841eac9458897410391722beb4b` on 2026-08-10, correcting the
previous changelog date of 2026-07-27. It remains the compatibility source for
the `1.0.1` to `2.0.0` migration, but it is not a completed tagged release and
must not receive a `v1.0.1` tag.

Version `2.0.0` is a completed historical release. Its annotated tag was
created on 2026-08-11 and targets exactly
`ef8f352ca32a7fbdf1131726263ff545cdd8b08a`. The annotation records its actual
later creation date and the 2026-08-10 source milestone; it was not backdated.
The earlier `c7bbbb6525d1135cd3acb3b64743240f5c00ec50` revision remains excluded
because its hosted validation failed and two corrective commits followed it.

Project Blueprint version `3.0.0` is released. Its annotated tag targets the exact merge commit
`1af3c1f85cd17e2c840857ad720e1a27e874585a`, whose post-integration `main`
validation passed in GitHub Actions run `31539907441`. The tag was created on
2026-08-11 after that run completed. No GitHub Release was created. Neither
this record nor the release gate authorizes moving the tag, creating a GitHub
Release, merging a later change, or changing hosted settings.

## Release gate

Before tagging a release:

1. run `validate_skill_package.py` and `verify_reference_evidence.py`;
   when the reference checkouts are available, rerun reference verification
   with an explicit `--reference-root ID=/absolute/path` for each registered
   repository and disclose any unavailable checkout;
2. run `validate_octon_mini.py`;
3. run `test_migration_1_0_1_to_2_0_0.py`,
   `test_migration_2_0_0_to_3_0_0.py`, and
   `test_migration_3_1_0_to_4_0_0.py`, and confirm valid transformation,
   exact idempotence, reviewed legacy seeding, rollback evidence, and every
   fail-closed fixture;
4. run `test_benchmark_validation.py`, `test_octon_launchers.py`,
   `test_velocity_workflows.py`, `test_work_completion.py`,
   `test_guided_setup.py`, `test_acceptance.py`, and
   `benchmark_validation.py --enforce`; retain the host-specific benchmark
   report, every cold-start and warm sample, and every threshold failure;
5. install the skill into a fresh temporary destination, run the installed
   package, Octon Mini source, reference, and acceptance validators from that
   destination, and generate and check all three profiles in compact and
   separated layouts from the bundled source;
6. when available, run the skill-creator `quick_validate.py` as a compatibility
   check against the installed Codex tooling;
7. confirm the pull-request `required` gate passes; local success is not
   evidence that hosted CI passed;
8. review the changelog and every migration from the previous release;
9. inspect generated profile snapshots: every profile must contain the same
   non-authorizing collaboration/SCM/package triggers but no full Git or domain
   package payload; Minimal must not inherit production controls, Standard must
   retain traceability and trigger registries, and High Assurance must add its
   risk-justified governance stores without silently assessing any trigger;
10. confirm the decision-governance valid baseline and every negative mutation
    pass in source and self-contained installed-skill validation; verify
    reciprocal `DREG-####`/accepted `DEC-####` links, evidence-first unknowns,
    closure evidence, stale-register integrity detection, and no-write
    `./octon check` behavior without refreshing generated outputs;
11. confirm no generated profile contains project facts, collaborator
    identities, hosted settings, secrets, permissions, accepted decisions,
    configured hooks, passing evidence, providers, or readiness claims;
12. confirm work-completion planning preserves complete repository and Git
    fingerprints; all four workflows and concurrent handback pass their
    positive and negative matrices; stale digests, remote/check/PR/review/
    ownership mismatches block; every external-action interruption resumes
    without duplication; and integration/synchronization precede cleanup;
13. confirm setup question generation leaves the target unchanged; catalog,
    target, instruction, evidence, Octon Mini, and session staleness fail
    closed; AI, TTY, and legacy-flag inputs reconcile through stable question
    IDs; init/adopt/upgrade use their existing planners; and work-completion
    setup neither enables missing prerequisites nor creates authorization;
14. commit the exact validated source and publish its required self-PR under
    current authority;
15. after a separately authorized `merge_commit` integration, manually
    dispatch the `validate` workflow on the exact integrated `main` revision
    and confirm the full Python 3.11-3.14 and Ubuntu/macOS/Windows matrix
    passes; the automatic `main-smoke` check is not a substitute for this
    release gate; and
16. only with separate current release authority, create an annotated
    `v<version>` tag on that exact validated integrated revision.

Do not move a published version tag. A correction receives a new patch
version.

## Installation and provenance

`skills/octon-mini-project-bootstrap/scripts/install_skill.py` installs a
collision-safe,
self-contained personal skill snapshot with the required dossier taxonomy,
schemas, migrations, and release metadata. It smoke-tests that staged copy
before placement. Installed and generated snapshots record their source version
but do not track or execute later Octon Mini changes automatically. Upgrades
are migrations.

## Distribution license decision

The repository owner approved `KEEP_PUBLIC_WITH_LICENSE — MIT-0` and confirmed
the exact copyright line `Copyright 2026 Cooper Online Enterprises`. The public
Octon Mini source repository and its installed source bundle are distributed
under the canonical MIT No Attribution license, SPDX identifier `MIT-0`.

Public visibility, licensed source reuse, and an Octon Mini release are separate
facts. Octon Mini 4.0.0 remains unreleased, with no `v4.0.0` tag, GitHub Release,
or package publication. The generator does not copy the source `LICENSE` into a
target snapshot or choose a target project's overall license; that remains a
separate project-owned decision.

## Supported and unsupported claims

Release acceptance supports claims about structure, syntax, traceability,
portability, dependency progression, adoption conformance, migration behavior,
mutation resistance, and extension compatibility within the declared
validator scope. It does not certify a generated project's implementation,
security, privacy, accessibility, legal compliance, operations,
organizational approval, or readiness.
