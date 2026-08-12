# Source Repository Git Workflow Assessment

This document applies only to the `project-blueprint` source repository. It is
not copied into generated projects and grants no permission. It records
accepted source-repository decision `SRC-DEC-0001`; release-history decision
`SRC-DEC-0002` is recorded in `RELEASE.md`. Neither decision transfers into
generated projects or creates authority for an individual Git, GitHub, or
release operation.

## SRC-DEC-0001 — Source Git and GitHub workflow

| Field | Accepted decision |
|---|---|
| Status | `accepted` |
| Authority | Explicit repository-owner approval on 2026-08-11 |
| Scope | This `project-blueprint` source repository only |
| Declared write-capable human maintainers | 1 |
| Independent review capacity | 0 (`not_established`) |
| Base workflow | `solo_hybrid` |
| Concurrent-work modifier | Use `concurrent_work` only while humans or agents are expected to write concurrently; it does not change the human team count |
| Integration method | `merge_commit` |
| Required peer approvals | 0 until eligible independent-review capacity is actually established |
| Hosted execution | Applied on 2026-08-11: expose only `merge_commit` and automatically delete merged head branches |
| Reassessment | By 2026-09-10 and immediately after any access, contributor, reviewer-capacity, or standing-concurrency change |
| Permission effect | None; workflow selection remains non-authorizing and every Git, GitHub, integration, cleanup, and release operation still requires current scope and authority |

Each material task uses a short-lived branch. Schema, template, validator,
migration, CI, workflow, policy, and release changes require a self-PR. A
self-PR records reviewability, validation, and known limitations; it is not
independent review.

The adopted PR integration method is `merge_commit`. Under separate owner
authority on 2026-08-11, hosted configuration was changed to expose only that
method and automatically delete merged head branches. Required peer approvals
remain zero until an eligible independent reviewer is actually available.

The repository must not be made public or moved to a higher GitHub plan solely
to obtain branch protection. If protection later becomes available for an
independent reason, first expose one stable aggregate validation context, then
consider requiring PRs and that check while disallowing force pushes and
deletion of the default branch.

## Assessment

| Field | Current assessment |
|---|---|
| Information role | Explicit repository-owner declaration plus direct local Git and read-only hosted GitHub observation |
| Observed on | 2026-08-11 |
| Reassess by | 2026-09-10, or immediately after an access, contributor, reviewer-capacity, or standing-concurrency change |
| Confidence | `confirmed` |
| Declared write-capable human maintainers | 1 |
| Observed write-capable human access | 1 |
| Active human contributors in the preceding 90 days | 1 |
| Human team band | `solo` |
| Independent review capacity | 0 (`not_established`) |
| Current implementation concurrency | One agent; no concurrent repository writer is expected for this post-release reconciliation |
| Standing post-task concurrency expectation | `not_assessed`; reassessment required |
| External contribution mode | `closed` (private and non-forking at observation time) |
| Adopted base workflow | `solo_hybrid` |
| Current modifier | None; `concurrent_work` is not selected for this task |
| Adoption status | `accepted` |
| Accepted decision reference | `SRC-DEC-0001` |
| Permission grant | `false` |

Read-only hosted observation found one write-capable human, one read-only
collaborator, no repository teams, no pending invitations, one human commit/PR
author, and no observed independent reviewer. Bots and automation were
excluded from the human counts; read-only access was not counted as a
developer. Activity does not erase dormant write authority, and access does
not prove intended responsibility or current availability. The completed
3.0.0 release-candidate task used three concurrent agents without increasing
the human team band. This post-release reconciliation has one agent and no
expected concurrent writer. Standing concurrency remains unknown and must be
reassessed rather than silently carried forward.

The repository is private and forking was disabled at observation time. The
observed source PRs used short-lived branches, CI, no hosted review, and merge
commits. The default branch remains unprotected; only the `merge_commit` method
is enabled; and automatic merged-head deletion is enabled. Detailed ruleset
inspection remains unavailable under the repository's hosted plan. The
explicit owner declaration and observed write access agree, so the current
human team band and workflow decision are `confirmed`. Hosted settings remain
dated observations rather than authority or proof of enforcement.

## Adopted workflow: `solo_hybrid`

The confirmed solo human band and accepted preference for reviewable
integration establish `solo_hybrid` as the base workflow for this source
repository. This post-release reconciliation has one agent and no expected
concurrent writer, so no `concurrent_work` modifier applies:

1. inspect the working tree, exact revision, applicable instructions, and
   current remote state;
2. use a short-lived task branch for a bounded change;
3. run the full applicable local validation before publication;
4. stage only reviewed paths and create intentional commits;
5. publish the required self-PR for material schema, template, validator,
   migration, CI, workflow, policy, or release changes with explicit current
   authority;
6. observe CI without treating availability as success or enforcement;
7. record self-review limitations and unresolved test gaps;
8. integrate only with `merge_commit` and only after current merge authority
   is supplied; and
9. remove only fully integrated local branches and separately authorized
   remote branches.

A self-PR records reviewability and limitations; it does not become independent
review, merge authority, or proof of branch protection.

The completed 3.0.0 release-candidate task used `concurrent_work` with disjoint
file ownership, a shared base revision, conflict detection, and explicit
handback rules. That modifier ended with the task. Future work must reassess
whether humans or agents are expected to write concurrently before selecting
it again. Coordination never grants edit authority.

Project risk remains separate. Sensitive, externally effective, or
high-consequence work may add stronger CI, self-review, or a separately
authorized qualified reviewer without changing the solo topology or
automatically selecting Standard or High Assurance.

## Local CI reconciliation

The source workflow is configured locally to validate:

- every pull request; and
- pushes to `main` only.

Superseded pull-request runs may be cancelled by a concurrency group scoped to
the workflow and PR number. Default-branch runs are not cancelled, preserving
post-integration and release evidence. The workflow retains read-only token
permissions, pinned action revisions, and the full operating-system/Python
matrix.

This local configuration does not prove that GitHub accepted or ran it. Before
this change, each update to the only observed open PR triggered duplicate full
matrices through both `push` and `pull_request`. Restricting ordinary push
validation to `main` removes that duplicate event path while retaining PR and
post-merge coverage.

## Applied hosted configuration

Under separate owner authority on 2026-08-11, the hosted settings selected by
`SRC-DEC-0001` were applied:

- only the adopted `merge_commit` integration method is exposed;
- merged head branches are automatically deleted; and
- no peer approval is required while eligible independent-review capacity is
  not established.

Do not make the repository public or move it to a higher GitHub plan solely to
obtain branch protection. If protection later becomes available for an
independent reason, first expose a stable aggregate validation context, then
consider requiring PRs and that check while disallowing default-branch force
pushes and deletion. No visibility, plan, protection, ruleset, collaborator,
or permission change accompanied the applied merge settings. These facts do
not authorize a later settings change or an individual merge.

## Release-state boundary

Accepted source release representation is governed by `SRC-DEC-0002` in
`RELEASE.md`. Version `1.0.1` is retained as an untagged, superseded source
milestone. The annotated `v2.0.0` tag was created on 2026-08-11 and targets
exactly `ef8f352ca32a7fbdf1131726263ff545cdd8b08a`; it was not backdated.
Version `3.0.0` was integrated at
`1af3c1f85cd17e2c840857ad720e1a27e874585a`, passed the full hosted `main`
matrix in run `31539907441`, and received an annotated `v3.0.0` tag on
2026-08-11. No GitHub Release exists. This workflow record does not authorize
moving either tag or creating a GitHub Release.

## Unsupported workflow families

This repository's blueprint does not support GitFlow, merge queues, release
trains, stacked-PR dependency trains, fork-first internal contribution,
multi-level CODEOWNERS approval, multiple mandatory approval stages,
dedicated release-manager handoffs, organization-wide ruleset orchestration,
multi-environment promotion pipelines, or enterprise issue/portfolio
governance. A team with more than five write-capable humans receives
`unsupported_team_size`; no enterprise fallback is selected.
