# Project Blueprint Repository Instructions

These instructions apply to this repository only. Generated `AGENTS.md` files
belong to their target projects and must not inherit authority from this
repository.

## Start here

1. Read `README.md`.
2. Read `dossier/BLUEPRINT.md`, `harness/BLUEPRINT.md`, and
   `shared/GENERATION_CONTRACT.md` before changing shared behavior.
3. Read `skills/project-bootstrap/SKILL.md` before changing the Codex skill,
   generator, or scaffold assets.
4. Preserve the separation between dossier documentation and harness
   governance.

## Invariants

- Templates never contain real credentials, personal data, accepted owner
  decisions, or standing external-action authority.
- Generated harness policies start deny-by-default and explicitly state that
  they cannot create permission.
- Generated dossier material is documentation only.
- Existing target-project files are never overwritten by the generator.
- Generated projects are independent snapshots and record the blueprint
  version used.
- Machine-readable source files identify whether they are authoritative or
  generated.
- Stable artifact and record IDs are not silently reused or reassigned.

## Validation

After changing the skill, assets, scripts, profiles, or schemas, run:

```text
python3 skills/project-bootstrap/scripts/validate_blueprint.py
```

Also run the skill-creator `quick_validate.py` against
`skills/project-bootstrap` when `SKILL.md` or `agents/openai.yaml` changes.

Do not claim a generated project is ready merely because scaffolding or
structural validation succeeds.
