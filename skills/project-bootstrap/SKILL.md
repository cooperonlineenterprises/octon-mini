---
name: project-bootstrap
description: Create, audit, or upgrade a project-specific agent harness and project dossier from the versioned Project Blueprint. Use when Codex needs to initialize a new project repository, add governed agent-operating structure, create a canonical/current-state/conformance dossier, select a minimal, standard, or high-assurance profile, or plan a deliberate blueprint upgrade without overwriting existing project authority.
---

# Project Bootstrap

Build an independent project-specific snapshot. Transfer structure and
validation patterns, never facts, permissions, decisions, or readiness claims.

## Workflow

1. Read all applicable instructions in the target repository.
2. Inspect the target filesystem, source control, implementation, and existing
   documentation.
3. Read the relevant reference:
   - dossier work: `references/dossier-model.md`;
   - harness work: `references/harness-model.md`;
   - profile selection: `references/profile-selection.md`;
   - generation and upgrades: `references/generation-workflow.md`.
4. Choose the smallest profile that covers the target's real risks.
5. Branch by target:
   - new nonexistent or empty directory: preview with
     `scripts/scaffold_project.py --dry-run`, then generate;
   - established directory: run `scripts/plan_adoption.py` and use its
     read-only inventory to plan reconciliation.
6. Never force template content over existing authority. Generation is
   transactional and intentionally refuses a nonempty target.
7. For a new project, generate the independently validated snapshot.
8. Replace generic placeholders only from inspected evidence or valid
   project-specific decisions.
9. Configure the target project's threat model, authority posture, project
   command hooks, and only the extensions justified by actual risks.
10. Run the generated read-only harness check and mutation tests. For a
    high-assurance profile, refresh derived integrity and rerun the check.
11. Validate dossier paths, links, IDs, traceability, and information-state
    boundaries.
12. Report what remains unknown, unassessed, skipped, stale, or gated.

## Non-negotiable boundaries

- Treat the dossier as documentation, never a permission channel.
- Treat generated harness policy as non-authorizing and deny-by-default.
- Do not transfer accepted decisions, identities, credentials, external
  endpoints, implementation status, or evidence from the blueprint.
- Do not infer current implementation from canonical target material.
- Do not overwrite existing paths.
- Preserve unknowns explicitly rather than inventing project facts.
- Record the blueprint version and selected profile in the target project.
- Keep `.agent/` governance separate from optional `.agents/` capabilities.
- A capability inherits and may narrow task authority; it cannot expand it.
- Keep `check` read-only and use `refresh` as the only generated-integrity
  writer.
- Keep strict JSON as the kernel format. A non-JSON extension must pin and
  bootstrap its parser independently.
- Require Python 3.11 or newer.

## Commands

Run commands from the skill directory or use absolute paths.

Preview:

```text
python3 scripts/scaffold_project.py \
  --target /absolute/project/path \
  --project-name "Project Name" \
  --profile standard \
  --dry-run
```

Generate:

```text
python3 scripts/scaffold_project.py \
  --target /absolute/project/path \
  --project-name "Project Name" \
  --profile standard
```

Plan adoption for an established project:

```text
python3 scripts/plan_adoption.py \
  --target /absolute/project/path \
  --profile standard
```

Validate this blueprint repository:

```text
python3 scripts/validate_blueprint.py
python3 scripts/test_acceptance.py
```

Validate a generated target:

```text
python3 -B .agent/scripts/validate.py --check
python3 -B -m unittest discover -s .agent/tests -p 'test_*.py'
```

## Output contract

Deliver generated files as a self-contained snapshot. State the selected
profile, blueprint version, collisions avoided, validation performed, and
remaining project-specific adoption work. Structural success must not be
reported as project readiness.
