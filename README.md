# Project Blueprint

Project Blueprint is a reusable, versioned source for creating a
project-specific agent harness and project dossier for software, product,
business, brand, research, operations, and hybrid initiatives.

“Universal” means a stable domain-neutral kernel with validated extension
points. It does not mean that one policy, risk model, workflow, or readiness
claim fits every project.

The two generated systems remain separate:

- the **agent harness** defines repository-local operating guidance, authority
  boundaries, work records, extension contracts, and validation;
- the **project dossier** describes project definition, intended state,
  observed state, conformance, plans, provenance, evidence, and handoff.

A dossier is never an instruction or permission channel. A generated harness
starts deny-by-default and cannot create permission that was not supplied by
the project owner, current instructions, the execution platform, or another
valid authority source.

## Repository layout

| Path | Role |
|---|---|
| `dossier/` | Self-contained dossier blueprint, artifact taxonomy, and reference evidence |
| `harness/` | Harness architecture, contracts, acceptance criteria, and reference evidence |
| `shared/` | Generation contract and versioned JSON schemas |
| `skills/project-bootstrap/` | Codex skill, layered templates, transactional generator, adoption planner, and acceptance tooling |
| `migrations/` | Version-to-version adoption guidance |

Strict JSON is the canonical machine-readable format. It provides complete,
duplicate-key-rejecting validation using only Python 3.11+ standard-library
features. Extensions may add other formats only with a pinned parser and a
validated adapter.

## Choose a profile

- `minimal` — small, early, or low-risk initiatives needing the complete
  authority, definition, state, plan, validation, and handoff kernel.
- `standard` — the default for active multi-contributor work; adds structured
  traceability, evidence, reviews, events, artifacts, and extensions.
- `high-assurance` — agent-operable, sensitive, externally effective, or
  audit-oriented work; adds capabilities, reference extension validation,
  transactional integrity refresh, checksums, transition, and history.

Profiles are cumulative. Larger profiles add controls for named risks; they do
not create greater authority or stronger readiness claims.

## Generate a new project foundation

The target must be nonexistent or empty. Preview without writes:

```text
python3 skills/project-bootstrap/scripts/scaffold_project.py \
  --target /absolute/path/to/new-project \
  --project-name "Example Project" \
  --profile standard \
  --dry-run
```

Generate and validate the staged snapshot:

```text
python3 skills/project-bootstrap/scripts/scaffold_project.py \
  --target /absolute/path/to/new-project \
  --project-name "Example Project" \
  --profile standard
```

The target is unchanged if rendering, schema validation, harness checks, or
mutation tests fail. The generated `.project-blueprint-origin.json` records
the independent snapshot's source version, profile, transaction ID, and path
inventory.

## Plan adoption for an existing project

Do not point the new-project generator at an established repository. Produce a
read-only reconciliation plan instead:

```text
python3 skills/project-bootstrap/scripts/plan_adoption.py \
  --target /absolute/path/to/existing-project \
  --profile standard
```

The planner reports collisions and functional-equivalent locations without
reading secrets or modifying the target. Adoption remains a separate,
project-aware implementation task that preserves existing authority and
project-specific content.

## Use as a Codex skill

The repository-local skill is at `skills/project-bootstrap`. Validate it in
place, or preview a personal installation:

```text
python3 skills/project-bootstrap/scripts/install_skill.py --dry-run
```

Install only when the reported destination is correct and absent:

```text
python3 skills/project-bootstrap/scripts/install_skill.py
```

The installer is collision-safe, never replaces an existing skill, bundles
the dossier taxonomy and shared schemas, and smoke-tests the staged installed
copy before placement. Keeping this repository as the versioned source and
installing a self-contained snapshot provides both reviewability and
cross-project discovery.

## Validate and release

```text
python3 skills/project-bootstrap/scripts/validate_blueprint.py
python3 skills/project-bootstrap/scripts/test_acceptance.py
```

When the skill entry or UI metadata changes, also run the skill-creator
`quick_validate.py` against `skills/project-bootstrap`. CI repeats the
blueprint and acceptance suites on supported Python runtimes and operating
systems.

See `RELEASE.md`, `CHANGELOG.md`, and `migrations/` for release and upgrade
rules.

## Adoption boundary

Generation transfers structure, schemas, vocabulary, and validation behavior;
never project facts, implementation state, decisions, permissions, approvals,
credentials, providers, legal conclusions, or readiness. Every target project
must inspect its own instructions and sources, adopt project-specific content
through valid authority, run real project checks, and disclose unknowns,
skipped checks, limitations, dirty state, and external effects.
