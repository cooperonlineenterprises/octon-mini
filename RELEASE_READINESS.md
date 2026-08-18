# Octon Mini 4.0.0 Release-Readiness Checklist

## Status and authority boundary

This source-only checklist is subordinate to the release gate in `RELEASE.md`.
It records preparation and missing evidence; it is not an accepted decision,
release authorization, tag, GitHub Release, package publication, readiness
claim, or target-project adoption result.

Octon Mini `4.0.0` remains **Unreleased**. A local or feature-branch pass cannot
populate final integrated-`main` evidence. Every final field remains pending
until it is observed on the exact separately authorized integration result.

| Field | Current value |
|---|---|
| Checklist state | `in_progress`; no release conclusion |
| Stabilization branch | `chore/4-0-release-stabilization` |
| Branch base | `ad5676b8456013cb3436e86a4ffa26281ab6f63a` (`origin/main` observed 2026-08-17) |
| Final candidate SHA | `pending`; must be the exact validated integrated `main` revision |
| Final candidate dirty state | `pending`; record tracked, untracked, ignored, submodule, and worktree scope |
| External effects from preparation | No release, tag, package, settings, ruleset, collaborator, permission, push, PR, merge, or workflow-dispatch action is authorized by this checklist |

The previously integrated base SHA has a successful manually dispatched full
matrix in GitHub Actions run `32068714705` and a successful `main-smoke` run
`32067921143`. They are dated pre-branch baseline observations only. Any change
from this branch requires new PR and post-integration evidence.

## Evidence ledger

For every local command retain the exact command, subject revision, start/end
or elapsed time, exit status, output/report location, failures, skipped work,
dirty-state disclosure, environment, and limitations. Do not replace failed or
slow samples with reruns.

| Requirement | Status | Exact subject | Command/evidence location | Exit/result | Elapsed | Limitations |
|---|---|---|---|---|---|---|
| Source/skill package validation | `pending` | `<SHA>` | `<command and safe path>` | `<value>` | `<value>` | `<value>` |
| Reference-evidence verification | `pending` | `<SHA>` | `<command and safe path>` | `<value>` | `<value>` | `<unavailable reference checkouts disclosed>` |
| Source contracts and architectural patterns | `pending` | `<SHA>` | `<commands and safe paths>` | `<value>` | `<value>` | `<value>` |
| Launcher, velocity, guided-setup, work-completion, and acceptance suites | `pending` | `<SHA>` | `<commands and safe paths>` | `<value>` | `<value>` | `<value>` |
| Migration suites | `pending` | `<SHA>` | `<commands and safe paths>` | `<value>` | `<value>` | `<reviewed 3.1 seed boundary>` |
| Installed-skill validation | `pending` | `<SHA>` | `<fresh temporary destination and commands>` | `<value>` | `<value>` | `<value>` |
| Profile/layout matrix | `pending` | `<SHA>` | `<Minimal/Standard/High Assurance × compact/separated evidence>` | `<value>` | `<value>` | `<structural only>` |
| Benchmark protocol v2 | `pending` | `<SHA>` | `<all complete JSON reports, stderr, and exit statuses>` | `<value>` | `<value>` | `<host-specific; every failure retained>` |
| Real-project validation | `not_run` | `none` | `docs/REAL_PROJECT_VALIDATION.md` defines the method; no completed report is recorded | `unknown` | `unavailable` | Existing validation remains synthetic and modeled human time is not a human study |

## Benchmark evidence requirements

- [ ] Use benchmark protocol `octon-mini.project.validation-benchmark.v2`.
- [ ] Measure 0, 2,000, 10,000, and 20,000 synthetic payload files.
- [ ] Retain one operational cold-start proxy and ten warm samples per series.
- [ ] Preserve every sample, subprocess failure, threshold failure, stderr, host
      context, source revision, and dirty-state disclosure.
- [ ] Complete three independent enforced invocations before making a final
      performance claim.
- [ ] Treat 50,000-file evidence as informational only when run; do not invent a
      threshold.
- [ ] Record phase-isolation evidence separately from benchmark-v2 enforcement.
- [ ] Preserve complete-tree staging, read-only checks, exact rollback, and the
      rejection of hardlinks, shared writable inodes, metadata-only identity
      caches, unsafe under-invalidation, and partial staging.

## Release-gate reconciliation

The numbered authority and validation requirements remain in `RELEASE.md`.
This checklist records their evidence without redefining them.

- [ ] Exact changelog and migration review completed on the final candidate.
- [ ] No generated profile contains project facts, identities, hosted settings,
      secrets, permissions, accepted decisions, configured hooks, passing
      evidence, providers, or readiness claims.
- [ ] Decision-governance positive and negative coverage passes.
- [ ] Work-completion planning, authorization, review-independence,
      interruption, integration, synchronization, and cleanup matrices pass.
- [ ] Guided setup remains target-read-only and stale inputs fail closed.
- [ ] Installed-skill source, reference, profile, and acceptance validation
      passes from a fresh destination.
- [ ] Required self-PR is opened only under separate publication authority.
- [ ] Hosted PR check named `required` passes on the exact PR head SHA.
- [ ] Integration uses separately authorized `merge_commit`.
- [ ] The final integrated `main` SHA is recorded after integration, not inferred
      from the feature branch.
- [ ] A separately authorized manual `validate` dispatch passes all twelve
      Ubuntu/macOS/Windows × Python 3.11–3.14 jobs on that exact SHA.

### Hosted evidence fields

| Field | Value |
|---|---|
| PR number and head SHA | `pending` |
| Hosted `required` run/job | `pending` |
| Integrated `main` SHA | `pending` |
| Manual full-matrix run | `pending`; pre-branch run `32068714705` is baseline only |
| Matrix accounting | `pending`; require 12 successful jobs and disclose cancelled, skipped, or failed jobs |

## Known limitations and open evidence

- Real-project onboarding and workflow evidence is not yet recorded; current
  acceptance evidence is synthetic.
- Unfamiliar-operator timing is unavailable. Modeled touchpoint ranges are not
  measured usability results.
- The source repository retains `solo_hybrid`, self-review limitations, and
  independent-review capacity `0 (not_established)`. Agent or self-review does
  not become independent approval.
- Read-only checks and complete portable transaction staging can take several
  seconds on 20,000-plus-file trees. Existing 10,000-file and mutation
  thresholds remain unchanged; no 50,000-file threshold exists.
- Copy-on-write/reflink staging remains separately architecture-proof gated and
  is not authorized by this checklist.
- Resource accounting, bounded invalidation, reusable policy locks, corpus-use
  controls, and general external-effect infrastructure remain trigger-gated.
  Universal action, lifecycle, readiness, trust, and state enums remain
  rejected as global defaults.
- Structural validation cannot establish a generated project's implementation,
  security, privacy, accessibility, legal compliance, operations, production
  readiness, organizational approval, or efficacy.

## Separate owner choices — not supplied

These are independent external actions. None is bundled with another, and no
choice or authority is inferred from validation, public visibility, MIT-0
licensing, a commit, a PR, or this checklist.

| External action | Owner choice | Exact target/channel | Current authority |
|---|---|---|---|
| Create annotated `v4.0.0` tag | `not_supplied` | `pending exact integrated-main SHA` | `not_supplied` |
| Create GitHub Release | `not_supplied` | `pending tag/release notes/assets` | `not_supplied` |
| Publish package | `not_supplied`; may be explicitly `none` | `pending exact registry/channel/artifact` | `not_supplied` |

Do not remove `Unreleased`, create or move a tag, create a GitHub Release,
publish a package, push, open or merge a PR, change hosted settings, or dispatch
a hosted workflow from this checklist. A correction after a published tag uses
a new patch version; the published tag is never moved.
