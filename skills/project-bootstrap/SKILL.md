---
name: project-bootstrap
description: Create, adopt, operate, recover, or upgrade a project-specific agent harness and project dossier from the versioned Project Blueprint. Use for guided or conversational setup interviews, new or established repositories, governed agent operation, compact or separated dossier layout, progressive solo/pair/tiny collaboration, transactional work lifecycle, validation, recovery, and deliberate Blueprint upgrades.
---

# Project Bootstrap

Build an independent project snapshot. Transfer structure and validators, never
facts, identities, permissions, accepted decisions, evidence, or readiness.

## Start

1. Read every applicable target-repository instruction.
2. Inspect source control, files, implementation, and existing documentation.
3. Read only the references needed for the task:
   - dossier: `references/dossier-model.md`;
   - harness: `references/harness-model.md`;
   - profile/layout/collaboration: `references/profile-selection.md`;
   - creation, adoption, maintenance, recovery, upgrade:
     `references/generation-workflow.md`;
   - conversational, TTY, or answer-file setup and resume:
     `references/guided-setup.md`.
4. Keep these axes independent:
   - Minimal, Standard, High Assurance: project risk and assurance;
   - solo, pair, tiny: one, two, or three-to-five write-capable humans;
   - `concurrent_work`: simultaneous humans, agents, or automation;
   - compact or separated: physical representation layout.

## Workflow

Use the source `scripts/pb.py` interface for bootstrap operations. Its
authoritative command inventory is projected to every generated
`.agent/commands.json`, where each command labels its bootstrap-source or
generated-project availability; primitive scripts remain advanced diagnostics.

- Guided setup: use `pb init|adopt|upgrade setup`. Determine mode from target
  evidence, stop on ambiguity, inspect read-only, and ask only unresolved
  dependency-eligible catalog questions—normally one to three at a time. State
  importance, choices, recommendation/rationale, allowed unknown or deferral,
  and blocked consequences without preselecting an answer. Keep observations,
  inferences, recommendations, selections, accepted-authority references,
  unknowns, deferrals, and runtime authorization distinct. Write a session only
  to an explicitly requested external path, use immutable successors, summarize
  before planning, and bind `--setup-session` into the existing planner.
- New project: `pb init plan|apply`. Non-interactive planning requires an
  explicit profile flag or a reviewed setup-session answer. Interactive
  `pb init` proposes Minimal and requires confirmation. Archetypes, hooks, and collaboration are proposals; create a
  first task only from explicitly supplied purpose, scope, authority,
  acceptance, ownership, validation, and next action.
- Established project: `pb adopt plan|apply`. Use the default bounded semantic
  inspection; review every functional equivalent or authority collision.
  Adoption apply never overwrites existing content and leaves adoption
  `in_progress`.
- Routine work: generated `pb work start|block|close|reopen|handoff|resume`.
  Lifecycle writers allocate IDs and synchronize mechanical links and derived
  state, but never invent scope, authority, criteria, review, evidence, or
  external-effect authorization.
- Governed completion: use `pb work finish plan|apply|resume` only after the
  project explicitly enables the shared engine and adopts the installed
  small-team Git workflow. Planning is read-only. Apply requires the exact
  digest, unchanged preconditions, and current task-scoped authorization for
  its exact external operations; external progress is resumable and cannot
  claim atomic rollback. The disabled-by-default completion event may dispatch
  only the exact read-only plan hook after successful task closure.
- Configuration: use `pb maintain hooks`, `pb maintain collaboration`,
  `pb maintain registry`, and source `pb maintain package` plan/apply flows.
  Package applicability, owner, trust decision, version, digest, and successful
  receipt evidence are mandatory.
- Validation: `pb check` is always read-only and never runs project hooks.
  `pb maintain refresh --apply` is the explicit generated-integrity writer.
  `.agent/scripts/run_project_checks.py --write-evidence` is the separately
  explicit hook/evidence writer.
- Recovery: use `pb doctor`, then exact `pb transaction recover` for a pending
  journal or `pb transaction rollback` for an unchanged applied receipt. Never
  add or simulate a force bypass.
- Upgrade: use the applicable migration guide and `pb upgrade plan|apply`.
  The 3.1→4.0 path first creates a reviewed legacy inventory seed. Automatic
  upgrade is limited to safe additions, exact-pristine non-authoritative
  implementation assets, and derived regeneration.

Every plan is non-authorizing and content-addressed. Repository-local mutation
plans are instruction- and path-fingerprint-bound, staged, validated,
receipted, and exactly recoverable. Governed external completion instead uses
monotonic evidence-backed receipts and safe resume or fix-forward. Stale or
ambiguous plans fail closed.

## Non-negotiable boundaries

- The dossier is documentation, never permission.
- Generated policy is deny-by-default and cannot create authority.
- Existing target paths are never silently overwritten.
- Stable IDs and authority ownership are never silently reassigned.
- Generated snapshots remain independent and versioned.
- `check`, detection, diagnosis, planning, and resume views are read-only.
- Guided question generation is target-read-only; session output is explicit,
  external to the target, non-authorizing, and secret-free.
- Generated-integrity and project-check evidence writes stay explicit and
  separate.
- External, destructive, credentialed, financial, legal, publication,
  deployment, communication, and production effects require explicit current
  authorization.
- Inferences remain sourced, timed, confidence-scored, limited, previewable,
  overridable, and recoverable.
- Structural conformance, harness adoption, and target-project readiness are
  separate claims.
- Trigger absence never means `not_applicable`.
- The Git portfolio is installed only when Git is explicitly selected; an
  uninstalled portfolio is not a runtime dependency.
- Generated work completion and its event hook start disabled. A completion
  event may automatically create only a read-only plan; it cannot apply.
- Require Python 3.11 or newer and strict JSON for the kernel.

## Commands

Run from the skill directory or use absolute paths.

```text
python3 scripts/pb.py init setup \
  --target /absolute/project/path \
  --output /absolute/review-area/setup-01.json

python3 scripts/pb.py init plan \
  --target /absolute/project/path \
  --project-name "Project Name" \
  --profile minimal \
  --layout compact \
  --output /absolute/project/path/.agent/transactions/plans/init.json

python3 scripts/pb.py init setup \
  --target /absolute/project/path \
  --session /absolute/review-area/setup-01.json \
  --record-plan /absolute/review-area/init-plan.json \
  --output /absolute/review-area/setup-02.json

python3 scripts/pb.py init apply \
  --target /absolute/project/path \
  --plan /absolute/project/path/.agent/transactions/plans/init.json \
  --accept-digest <reviewed-digest>

python3 scripts/pb.py adopt plan --help
python3 scripts/pb.py upgrade plan --help
python3 scripts/test_guided_setup.py
python3 scripts/validate_blueprint.py
python3 scripts/test_acceptance.py
```

Inside a generated project:

```text
./pb check
./pb work resume
./pb work finish plan
./pb doctor
python -B .agent/tests/test_validate.py --tier fast
```

## Output contract

Report the Blueprint version, profile, layout, collaboration assessment and
workflow-adoption status, setup-session digest/status, recommendations versus
selections versus accepted authority, unknowns/deferrals, exact plan/receipt
identity, collisions or deferred review, work-completion closure sequence,
validation tier run, rollback/recovery path, and remaining adoption or readiness
work. Never describe setup, structural success, or a selected option as
permission or readiness.
