# Octon Mini 4.0 Velocity Validation

This report records local, content-free implementation evidence for the 4.0
velocity program. It is not target-project evidence, an adoption decision,
permission, or a readiness claim. Wall-clock results are host-specific.

## Measurement boundary

- Date: 2026-08-16
- Host: local macOS workspace, APFS, Python 3.14.0
- External effects: none
- Repository payload: disposable generated snapshots and synthetic small text
  files only
- Human elapsed-time estimates: modeled ranges, clearly separated from measured
  command time
- Profiles: Minimal, Standard, High Assurance
- Layouts: compact and separated
- Collaboration: solo, pair, tiny; concurrency tested as a separate modifier

Structural conformance, harness adoption, and target-project readiness are
reported separately throughout. No test supplies real project facts,
specialist conclusions, credentials, publication, deployment, or production
effects.

## Acceptance targets

| Measure | 4.0 target | Boundary |
|---|---:|---|
| valid compact scaffold, profile p90 | `<10 s` | structural check plus bounded fast mutations |
| read-only check at 10k synthetic files, p90 | `<2 s` | full structural check; hooks never run |
| fast mutation tier at 0–20k payload files, p90 | `<10 s` | bounded governed baseline independent of payload size |
| stale plan or evidence | deterministic refusal | no target mutation |
| interrupted transaction | write-ahead planned postimages, resumable rollback, and idempotent finalization permit exact recovery or fail closed | no force bypass |
| detector, plan, doctor, resume, check | unchanged target tree | read-only contract |

Consequential guided init, adoption, upgrade, and release workflows stage the
release tier even though primitive scaffolding uses the bounded fast tier.

## Current benchmark evidence

The final three-sample Octon Mini 4.0.0 benchmark passed every enforced
threshold:

| Synthetic files | Refresh | Check p90 | Fast mutations p90 |
|---:|---:|---:|---:|
| 0 | 0.347 s | 0.200 s | 6.332 s |
| 2,000 | 1.057 s | 0.529 s | 6.512 s |
| 10,000 | 4.015 s | **1.876 s** | 6.982 s |
| 20,000 | 7.856 s | 3.615 s | 7.597 s |

Final compact scaffold p90:

| Profile | p90 | Target |
|---|---:|---:|
| Minimal | 6.907 s | pass (`<10 s`) |
| Standard | 7.813 s | pass (`<10 s`) |
| High Assurance | 9.624 s | pass (`<10 s`) |

The immediately preceding three-sample run identified one threshold miss
rather than being reclassified as success: High Assurance scaffold p90 was
10.442 s; Minimal was 7.526 s, Standard was 7.980 s, the 10k read-only check
was 1.952 s, and every bounded mutation sample remained below 10 s.

Profiling traced the High Assurance miss to copying the same isolated 139-file
governed baseline 75 times. The mutation suite now uses portable independent
copies that retain file contents, symlink identity, and modes without copying
timestamps or extended metadata that no harness contract consumes. It does
not use hardlinks or shared writable inodes, and all 93 fast-tier tests remain
in the scaffold gate. The fresh three-sample run above confirms the result
without changing a threshold or removing a safety check.

The bounded fast tier remained nearly flat from 0 to 20k synthetic payload
files. This replaces the prior full-tree mutation behavior observed during the
velocity audit, where a 2,071-file fixture took 28.48 s because repeated
mutation clones copied project payload.

A 10k-file routine work transaction measured 0.25 s to create its reviewed
plan and 10.59 s to stage, refresh, validate, apply, validate again, and receipt
the change. That cost is an explicit safety tradeoff of portable complete-tree
staging. It is acceptable as a current limitation, not a target for read-only
`check`; future optimization must preserve isolation and cannot use unsafe
hardlinks that could mutate the live tree through staged commands.

## Executable validation matrix

| Boundary | Cases | Executable evidence |
|---|---|---|
| profile/layout generation | 3 profiles × compact/separated | `validate_octon_mini.py` profile builds |
| guided setup | init/adopt/upgrade, conversational/TTY/flag equivalence, immutable resume, staleness, work-completion prerequisites, target no-write | `test_guided_setup.py` |
| guided creation | explicit Minimal, compact, solo facts, first task, plan/apply/resume | `test_velocity_workflows.py` |
| established adoption | dirty Git repository, low conflict apply, existing-byte preservation, exact collision refusal | `test_velocity_workflows.py`; `test_acceptance.py` |
| archetype detection | software/product, research, brand/non-software, operations/hybrid | `test_velocity_workflows.py` |
| collaboration | solo, pair, tiny, concurrent humans/agents, stale evidence | `test_velocity_workflows.py`; generated mutation suite |
| routine lifecycle | start, handoff, resume, direct evidence-bound close, reopen, rollback | generated release tests; `test_velocity_workflows.py` |
| concurrency safety | target-preimage conflict, instruction fingerprint, dirty tree, stable task allocation | transaction and velocity tests |
| hook configuration | shell-free argv, version probe, owner, side effects, selective routing, full adoption boundary | generated mutations; acceptance |
| evidence lifecycle | selected hook writes, immutable archive, current bounded index, stale evidence | generated mutations; acceptance |
| registry maintenance | discovery, add, rename, combine, supersede, omission, stable-ID refusal | generated mutations; acceptance |
| packages | Git, operations/observability, security/supply-chain, sample restriction, Context Pack schema; digest/decision/receipt binding | acceptance package matrix |
| live upgrade | reviewed 3.1 seed, three-way plan/review/apply, idempotence, rollback, changed-path refusal | `test_migration_3_1_0_to_4_0_0.py` |
| historical migrations | 1.0.1→2.0.0 and 2.0.0→3.0.0 valid/invalid/idempotence/rollback | migration fixture suites |
| recovery | invalid configuration, stale evidence, interrupted refresh, pending transaction, changed postimage | generated mutations; velocity and migration tests |
| scale | 0, 2k, 10k, 20k synthetic payload files | `benchmark_validation.py` |
| installer | collision-safe self-contained bundle and bundled source validation | `install_skill.py`; acceptance |

Sensitive or externally effective projects are exercised structurally through
High Assurance, conditional trigger contracts, package confinement, and
external-effect gates. Tests intentionally perform no credentialed, financial,
legal, publication, deployment, production, or destructive external action.

## Before-and-after touchpoint model

These are workflow models, not measured human studies. A command is a user-run
invocation; a manual input is a distinct semantic value; files touched counts
hand edits, not transaction-generated files. Ranges reflect project ambiguity.

| Journey | Commands before → after | Manual inputs before → after | Project-owned decisions before → after | Files hand-edited before → after | Human elapsed estimate before → after |
|---|---:|---:|---:|---:|---:|
| new solo project through first task | 5–8 → 2 + resume | 12–20 → 11–14 | 4–7 → 3–5 | 4–8 → 0 | 15–40 min → 3–8 min review plus ~20 s machine work |
| established low-conflict adoption | 7–12 → 2 + final checks | 15–30 → 6–12 | 6–12 → 4–8 | 8–20 → 0 | 30–120 min → 5–25 min review plus staged apply |
| routine task start | 3–5 → 2 | 8–12 → 8 | 2–4 → 2–4 | 2–4 → 0 | 3–10 min → 1–3 min review plus apply |
| task close and handoff | 4–7 → 2 | 8–16 → 7–12 | 3–6 → 3–6 | 3–6 → 0 | 5–20 min → 2–6 min review plus apply |
| resume interrupted work | 3–7 → 1 | 0–6 → 0 | 0–2 → 0–1 | 0–3 → 0 | 2–15 min → under 1 s command plus reading |
| configure one project hook | 3–6 → 2 | 8–14 → 7–10 | 3–6 → 3–6 | 2–5 → 0 | 10–30 min → 3–10 min review plus apply |
| recover interrupted apply | ad hoc → 2 | unknown → journal path + reviewed action | unknown → 1 | unknown → 0 | unbounded → diagnosis plus deterministic restore/refusal |
| live upgrade | manual diff/reconcile → proposal, review, plan, apply | 20+ → conflict-dependent | unchanged substantive decisions | many → 0 automatic paths | hours/days → review-dominated, machine staging in seconds/minutes |

Automation does not reduce substantive decisions by inventing answers. The
after model removes file synchronization, ID allocation, derived-state edits,
integrity maintenance, and command discovery while retaining risk/profile,
authority, applicability, trust, review, evidence, and external-effect gates.

## Failure and fallback behavior

| Failure | Automatic behavior | Required recovery |
|---|---|---|
| explicit profile absent | refuse scripted generation | select a risk profile; interactive may propose Minimal |
| existing target content | route new-project init to adoption | run semantic adoption plan |
| functional equivalent or authority collision | emit proposal and review requirements | reconcile or disposition every current ambiguity |
| changed instruction/evidence/target after plan | refuse apply | inspect change and re-plan |
| staged validation failure | restore/no target mutation | fix owned source or configuration and re-plan |
| interrupted live mutation | leave/write-ahead journal | exact recover; refuse independently changed paths |
| changed path after apply | refuse rollback | project-owned reconciliation or specialist recovery |
| stale collaboration or check evidence | withhold selection/adoption claim | gather current evidence explicitly |
| derived-only drift | doctor proposes exact repair digest | accept derived repair or run explicit refresh |
| project-owned invalid configuration | no automatic repair | owner decision and reviewed transaction |
| unknown legacy baseline | refuse seed/upgrade | supply reviewed old pristine hash or reconcile manually |

## Measurement plan

Every release candidate records JSON or table evidence for:

1. **Time to first valid scaffold:** three samples per profile, compact default,
   plus all-profile/all-layout conformance builds.
2. **Time to first meaningful task:** guided init plan/apply with an explicit
   first task; report machine time separately from review time.
3. **Established-project adoption:** low-conflict and authority-collision
   fixtures, inspected-file bounds, unchanged pre-apply tree, and apply time.
4. **Task setup and closure:** plan and apply times on small, 2k, 10k, and 20k
   trees; report staging separately when instrumentation is added.
5. **Resume:** command time, bytes/lines returned, exact revision availability,
   and unchanged-tree result.
6. **Manual touchpoints:** commands, distinct semantic inputs, project-owned
   decisions, and hand-edited files for scripted usability exercises.
7. **Validation runtime/recovery:** refresh, check p50/p90, fast/integration/
   release tiers, first actionable diagnostic, and successful recovery time.
8. **Automation success/fallback:** plans applied unchanged, stale plans,
   review-required proposals, automatic upgrade paths, manual conflicts, and
   rollback/recovery outcomes.
9. **False positives:** detector candidates rejected by reviewers, invalid
   collision classifications, irrelevant diagnostics, and package triggers
   assessed non-applicable.
10. **Maintenance burden:** authoritative manifest edits per release, duplicate
    representations detected, source/derived drift, fixture update count, and
    runtime regression.

Suggested release thresholds retain the current `<10 s` scaffold, `<2 s`
10k check, and `<10 s` fast mutation goals. A threshold change requires a
recorded architecture decision and must not conceal a regression.

## Risks, tradeoffs, and non-goals

- Complete portable transaction staging is slower at large file counts but
  preserves pre-write validation and rollback evidence. Unsafe shared-inode
  acceleration is explicitly rejected.
- Semantic detectors are bounded recipes, not complete project understanding;
  false negatives remain possible and candidates never self-adopt.
- Compact layout currently combines only the representation pair whose
  governance boundaries were reviewed as aligned. File-count reduction is not
  allowed to collapse semantic ownership.
- The dynamic 3.1 fixture validates migration mechanics but cannot prove every
  historical project has known pristine bytes. Real legacy baselines remain a
  review obligation.
- Human elapsed-time and unfamiliar-maintainer usability need repeated real
  project exercises; automation tests cannot establish them.
- Enterprise workflows, multi-level approvals, organization-wide governance,
  generic external-effect automation, credentials, deployment, publication,
  legal conclusions, and production readiness remain non-goals.

## Reproduction

```text
python3 -B skills/octon-mini-project-bootstrap/scripts/test_velocity_workflows.py
python3 -B skills/octon-mini-project-bootstrap/scripts/test_guided_setup.py
python3 -B skills/octon-mini-project-bootstrap/scripts/test_migration_3_1_0_to_4_0_0.py
python3 -B skills/octon-mini-project-bootstrap/scripts/validate_octon_mini.py
python3 -B skills/octon-mini-project-bootstrap/scripts/test_acceptance.py
python3 -B skills/octon-mini-project-bootstrap/scripts/benchmark_validation.py \
  --sizes 0 2000 10000 20000 --samples 3 --enforce
```

Preserve the command, exit status, stdout/stderr, elapsed time, current source
revision, dirty-state disclosure, and host limitations for any published
release evidence.
