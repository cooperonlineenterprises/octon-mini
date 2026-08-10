# Generation and Upgrade Workflow

## New project

1. Confirm the target is nonexistent or empty and its parent exists.
2. Select a profile.
3. Run the generator with `--dry-run`.
4. Review every intended path.
5. Generate transactionally; the staged snapshot must validate before the
   target appears.
6. Replace placeholders from project evidence.
7. Establish the threat model and record project decisions separately.
8. Configure project commands and restrictions-only extensions.
9. Run the read-only harness check and mutation tests.
10. In every profile, refresh the artifact catalog, path-authority map, and
    manifest from the authoritative project-local artifact registry, then
    rerun the read-only check. High Assurance refreshes checksums and generated
    validation evidence in the same transaction.
11. Confirm the selected profile's required governed-file inventory is intact;
    dossier omissions remain a separate, registry-recorded applicability
    decision.
12. Run target-project validation and complete one real task lifecycle before
    treating the harness as adopted.

## Established project

Run `scripts/plan_adoption.py` first. It inventories exact path collisions and
project signals without writing. Then inspect functional equivalents,
crosswalk existing authority and content to the blueprint, and create an
authorized migration task. Preserve unrelated work, accepted decisions, stable
IDs, and existing authority.

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
7. run schema migration fixtures, harness mutation tests, and project checks;
8. update the project-local artifact registry for every added, removed, or
   renamed dossier representation;
9. refresh derived metadata and integrity, validate, and record the new origin
   version.

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
```

Refresh first validates non-derived sources, renders all profile-applicable
derived files into a staging directory, and only then replaces the declared
outputs. A shared generation ID makes an interrupted multi-file replacement
fail closed at the final read-only check. Refresh never invents metadata for an
unregistered path, silently removes a registry entry, or overwrites a
non-derived artifact.
