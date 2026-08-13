# Project Blueprint 4.0 Golden Paths

These paths minimize ceremony while preserving project facts, authority,
evidence, stable IDs, no-overwrite, and explicit external-effect gates. All
planning and inspection commands are read-only. Replace example inputs with
current project-owned values; do not copy them as facts.

## New solo project

One plan and one apply reach a valid scaffold and first meaningful task:

```text
python3 skills/project-bootstrap/scripts/pb.py init plan \
  --target /absolute/project \
  --project-name "Project" \
  --profile minimal \
  --layout compact \
  --writer-count 1 \
  --collaboration-source authority:<current-source> \
  --collaboration-observed-at <date-time> \
  --collaboration-expires-at <date-time> \
  --solo-integration-preference direct \
  --first-task-title <title> \
  --first-task-scope <scope> \
  --first-task-authority-basis authority:<scope-source> \
  --first-task-owner <owner-role> \
  --first-task-operator <operator-role> \
  --first-task-acceptance <criterion> \
  --first-task-validation <validation> \
  --first-task-next-action <action> \
  --output /absolute/project/.agent/transactions/plans/init.json

python3 skills/project-bootstrap/scripts/pb.py init apply \
  --target /absolute/project \
  --plan /absolute/project/.agent/transactions/plans/init.json \
  --accept-digest <reviewed-digest>

cd /absolute/project
./pb work resume
```

The plan separates detector observations, proposals, explicit decisions, and
gates. It configures no hook and adopts no workflow. Minimal is an explicit
choice. Apply stages refresh, check, and the complete release tier before
writing. Structural conformance passes; adoption and readiness remain
unassessed.

## Established solo project

```text
python3 skills/project-bootstrap/scripts/pb.py adopt plan \
  --target /absolute/project \
  --project-name "Project" \
  --profile minimal \
  --layout compact \
  --authority-source authority:<adoption-scope> \
  --output /absolute/project/.agent/transactions/proposals/adoption.json
```

If ambiguity exists, disposition every item in a proposal-digest-bound review
file, then create the transaction plan with `--proposal` and `--review`. Apply
the exact transaction digest. Confirm that pre-existing bytes are unchanged,
run `./pb check`, assess hooks and mandatory triggers, execute complete project
checks explicitly, and only then consider a separate adoption decision.

Low-conflict apply installs only absent paths, passes the release tier in
staging, and records adoption `in_progress`; it never marks the project ready.

## Pair or tiny team

Keep profile selection risk-based. Record only aggregate current facts:

```text
python3 skills/project-bootstrap/scripts/pb.py maintain collaboration plan \
  --target /absolute/project \
  --writer-count 2 \
  --source authority:<collaboration-source> \
  --observed-at <date-time> \
  --expires-at <date-time> \
  --independent-review-capacity yes \
  --output /absolute/project/.agent/transactions/plans/collaboration.json
```

For three to five writers, use the same flow with the actual count. The result
proposes `pair_pr` or `tiny_pr`; it adopts nothing. Add an accepted decision
reference only when the project owner adopts the workflow. If Git is selected,
install the pinned Git portfolio in a separate content-addressed transaction.

## Concurrent human, agent, or automation work

Add `--concurrent-humans` and `--concurrent-agents` only with current evidence.
This adds the `concurrent_work` modifier; it never changes human team band or
assurance. Use project-owned write-scope coordination when overlapping work is
possible. Resume and hand off through focus rather than editing derived state:

```text
./pb work handoff --task-id TASK-0001 \
  --next-action <action> \
  --summary <bounded-summary> \
  --operator <role> \
  --output .agent/transactions/plans/handoff.json
./pb work resume
```

## Routine task closure

```text
./pb work start --help
./pb transaction apply --plan <plan> --accept-digest <digest>

# Perform authorized work and create real evidence.

./pb work close TASK-0001 \
  --criteria-met \
  --implementation-result <result> \
  --review-evidence EVD-0001 \
  --closure-evidence EVD-0001 \
  --external-effects none \
  --next-action <action> \
  --operator <role> \
  --output .agent/transactions/plans/close.json
./pb transaction apply --plan <plan> --accept-digest <digest>
```

The close command records supplied claims and evidence references; it does not
prove sufficiency. Direct closure is mechanically supported once explicit
criteria/review/evidence/effects inputs are present, avoiding status-only
ceremony.

## Hooks and evidence

Run the detector read-only, review candidate argv and side effects, then
install configuration through `./pb maintain hooks plan|apply`. `./pb check`
never executes hooks. Run only selected authorized hooks:

```text
python -B .agent/scripts/run_project_checks.py \
  --write-evidence \
  --hook project_test
```

Use changed-scope routing for routine work and `--verify-adoption` for the full
boundary. Writing or external hooks require their explicit acknowledgment.

## Recovery

```text
./pb doctor
./pb transaction recover --pending <pending-journal>
./pb transaction rollback --receipt <applied-receipt>
```

Derived-only diagnosis may propose an exact repair digest. Invalid
configuration, stale evidence, ambiguous authority, or changed post-apply
paths require a project decision or re-plan; they are never force-repaired. A
surviving pending journal with an exact terminal receipt is finalized without
undoing the receipted result. Retry the same rollback receipt when its status
is `rollback_in_progress`.

## Upgrade

For a native inventory-v2 project, run `pb upgrade plan` directly. For 3.1.0,
follow `migrations/3.1.0-to-4.0.0.md`: inspect, supply an exact reviewed old
baseline, create a non-applied seed, classify the three-way proposal,
disposition every review path, then accept the exact transaction digest.

After apply, distinguish the outcomes:

- structural conformance: checked automatically;
- harness adoption: unchanged unless project owners separately update it;
- target-project readiness: not inferred and requires current project and
  specialist evidence.
