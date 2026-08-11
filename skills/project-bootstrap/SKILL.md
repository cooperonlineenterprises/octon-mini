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
4. Assess collaboration separately from risk: record only aggregate,
   privacy-minimized human access, activity, review-capacity, concurrency, and
   contribution signals with evidence and freshness. Team size never selects
   the assurance profile or grants permission.
5. Choose the smallest profile that covers the target's real risks.
6. Branch by target:
   - new nonexistent or empty directory: preview with
     `scripts/scaffold_project.py --dry-run`, then generate;
   - established directory: run `scripts/plan_adoption.py` and use its
     read-only inventory to plan reconciliation.
7. Never force template content over existing authority. Generation is
   transactional and intentionally refuses a nonempty target.
8. For a new project, generate the independently validated snapshot.
9. Replace generic placeholders only from inspected evidence or valid
   project-specific decisions.
10. Configure the target project's threat model and authority posture. Assess
   every test, lint, build, and closure hook: use an owned shell-free argv
   contract with a same-executable version probe for applicable checks, or an
   owned, reasoned `not_applicable` assessment. Adopt only the restrictions-only
   extensions justified by actual risks; generated production-control entry
   points start disabled and unassessed.
11. Select only `solo_direct`, `solo_hybrid`, `pair_pr`, or `tiny_pr` from a
    fresh, non-conflicting assessment. Apply `concurrent_work` for simultaneous
    humans or agents without changing human team size. More than five writers
    is unsupported. Adopt a workflow only through a project-owned accepted
    decision; neither assessment nor adoption authorizes Git or GitHub actions.
12. For planned development, build hard plan/task dependencies, gates,
    structured blockers, and reciprocal plan/task links. Derive the read-only
    ready frontier before selecting work; dates never satisfy prerequisites or
    choose among independent ready items.
13. Run the generated read-only harness check and mutation tests. The check
    must not execute project hooks or write evidence. After confirming
    authority for declared side effects, run configured hooks only through the
    explicit project-check evidence writer. In every profile, refresh derived
    metadata and integrity after adopting or changing source artifacts, then
    rerun the check. High Assurance additionally refreshes checksums and
    generated validation evidence.
14. Validate dossier paths, links, IDs, traceability, dependency readiness,
    and information-state
    boundaries.
15. Before representing High Assurance as adopted, assess every conditional
    and optional trigger and link applicable controls to owners,
    representations, and current evidence.
16. Report what remains unknown, unassessed, skipped, stale, or gated. Keep
    demonstrated target-project readiness separate from harness adoption.

## Non-negotiable boundaries

- Treat the dossier as documentation, never a permission channel.
- Treat generated harness policy as non-authorizing and deny-by-default.
- Do not transfer accepted decisions, identities, credentials, external
  endpoints, implementation status, or evidence from the blueprint.
- Do not infer current implementation from canonical target material.
- Do not overwrite existing paths.
- Preserve unknowns explicitly rather than inventing project facts.
- Record the blueprint version and selected profile in the target project.
- Do not transfer collaborator identities, counts, hosted settings, workflow
  adoption, or evidence from this blueprint or another project.
- Keep the provider-neutral small-team workflow portfolio available in every
  profile; GitHub remains optional and enterprise workflows remain excluded.
- Keep `.agent/` governance separate from optional `.agents/` capabilities.
- A capability inherits and may narrow task authority; it cannot expand it.
- Keep `check` read-only and use `refresh` as the only generated-integrity
  writer. The separate project-check writer may append only its documented
  evidence store when explicitly invoked.
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
python -B .agent/scripts/validate.py --check
python -B .agent/scripts/validate.py --assess-collaboration
python -B .agent/scripts/validate.py --ready-frontier
python -B -m unittest discover -s .agent/tests -p "test_*.py"
```

After project owners have assessed every hook and confirmed current authority
for its declared effects, explicitly run configured target-project checks and
write scoped evidence:

```text
python -B .agent/scripts/run_project_checks.py --write-evidence
```

Add `--acknowledge-side-effects` only after reviewing hooks that declare
repository writes or possible external effects. Use `--verify-adoption` only
when the explicit evidence write, generated-integrity refresh, and final
read-only adoption check are all intended.

After any legitimate source or dossier-artifact change, update the
project-local artifact registry when physical dossier paths changed, then run:

```text
python -B .agent/scripts/refresh.py --refresh
python -B .agent/scripts/validate.py --check
```

## Output contract

Deliver generated files as a self-contained snapshot. State the selected
profile, blueprint version, collaboration assessment status, supported or
unsupported team band, workflow recommendation/adoption status, collisions
avoided, validation performed, and remaining project-specific adoption work.
Structural success must not be reported as project readiness or authority.
