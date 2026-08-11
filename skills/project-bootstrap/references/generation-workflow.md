# Generation and Upgrade Workflow

## New project

1. Confirm the target is nonexistent or empty and its parent exists.
2. Select a profile from project risk and assurance triggers, never from human
   team size.
3. Run the generator with `--dry-run`.
4. Review every intended path.
5. Generate transactionally; the staged snapshot must validate before the
   target appears.
6. Replace placeholders from project evidence.
7. Populate the collaboration profile only from project-owned aggregate
   evidence with observation and freshness times. Run the read-only assessment;
   unknown, stale, or conflicting evidence selects nothing.
8. Adopt only `solo_direct`, `solo_hybrid`, `pair_pr`, or `tiny_pr` through a
   project-owned accepted decision. Apply `concurrent_work` for simultaneous
   humans or agents without changing the human band. More than five human
   writers is unsupported, not an enterprise-workflow trigger.
9. Establish the threat model and record project decisions separately.
10. Assess every project check hook. Configure applicable hooks with shell-free
   argv, ownership, freshness, same-executable version probes, and declared
   side effects; use owned, reasoned `not_applicable` only where justified.
   Deliberately assess restrictions-only extensions without enabling any by
   generation alone.
11. Build hard task/plan dependencies, structured gates and blockers, and
   reciprocal plan/task links when adopting project plans. Run the read-only
   ready-frontier command before selecting planned work; use valid direction,
   never dates, to choose among independent eligible items.
12. Run the read-only harness check and mutation tests. It must not execute
    target-project hooks. After confirming authority for any declared effects,
    run configured hooks separately with
    `run_project_checks.py --write-evidence`; use `--verify-adoption` only when
    an explicit evidence write plus refresh is intended.
13. In every profile, refresh the artifact catalog, path-authority map, and
    manifest from the authoritative project-local artifact registry, then
    rerun the read-only check. High Assurance refreshes checksums and generated
    validation evidence in the same transaction.
14. Confirm the selected profile's required governed-file inventory is intact;
    dossier omissions remain a separate, registry-recorded applicability
    decision.
15. Require current, fingerprint-bound evidence for configured target-project
    checks and complete one real dependency-gated task lifecycle before
    treating the harness as adopted. Treat demonstrated product or production
    readiness as a further project-owned conclusion.

## Established project

Run `scripts/plan_adoption.py` first. It inventories exact path collisions and
project signals without writing. Then inspect functional equivalents,
crosswalk existing authority and content to the blueprint, and create an
authorized migration task. Preserve unrelated work, accepted decisions, stable
IDs, and existing authority. Do not infer maintainers from commit history,
reuse current-source collaborator facts, or treat an observed branch/PR habit
as an adopted workflow.

## Upgrade

Treat an upgrade as a project-specific transition:

1. read `.project-blueprint-origin.json`;
2. compare old and candidate blueprint versions;
3. classify changes as compatible, additive, transitional, or conflicting;
4. preserve project-specific content;
5. update through explicit decisions and migrations;
6. follow the applicable migration in source-checkout `../../../migrations/`
   or installed-bundle `../assets/blueprint-source/migrations/`, and regenerate
   only derived artifacts;
7. reconcile hard dependencies, structured blockers, gates, reciprocal
   plan/task links, and lifecycle readiness before preserving any active or
   completed status;
8. reconcile collaboration observations and any workflow decision explicitly;
   a major-version migration seeds unknown non-authorizing state and never
   invents maintainers or adopts a workflow;
9. run schema migration fixtures, harness mutation tests, the ready-frontier
   command, and project checks;
10. update the project-local artifact registry for every added, removed, or
   renamed dossier representation;
11. refresh derived metadata and integrity, validate, and record the new origin
   version.

For `1.0.1` to `2.0.0`, run the repository-contained
`scripts/test_migration_1_0_1_to_2_0_0.py` suite. The companion reconciler
accepts only a closed reference bundle, writes only to an explicit new output
path, retains exact noncurrent rollback evidence, and is idempotent. It never
executes a legacy or migrated project command and is not an in-place project
upgrade mechanism.

For `2.0.0` to `3.0.0`, use the corresponding executable migration suite. The
reconciler preserves project authority and rollback evidence, seeds the closed
collaboration profile as unknown, replaces only a pristine known Git contract,
and rejects ambiguous or adopted legacy policy rather than silently selecting
a workflow.

## Ordinary maintenance

`project-dossier/machine-readable/artifact-registry.json` is the authoritative
project-local source for artifact types and physical representations. Update
it in the same source change that adds, removes, renames, combines, or
supersedes a dossier artifact. Stable artifact-type and representation IDs are
not reassigned.

Then run:

```text
python -B .agent/scripts/refresh.py --refresh
python -B .agent/scripts/validate.py --check
python -B .agent/scripts/validate.py --assess-collaboration
python -B .agent/scripts/validate.py --ready-frontier
```

Refresh first validates non-derived sources, renders all profile-applicable
derived files into a staging directory, and only then replaces the declared
outputs. A shared generation ID makes an interrupted multi-file replacement
fail closed at the final read-only check. Refresh never invents metadata for an
unregistered path, silently removes a registry entry, or overwrites a
non-derived artifact. The collaboration assessment is a separate read-only
stdout report; it is not run by `--check` and cannot adopt a workflow.
