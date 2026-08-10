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
features in the bundled reference implementation. Projects may adopt an
equivalent validator in an existing pinned toolchain only after it passes the
same conformance fixtures. Extensions may add other formats only with a pinned
parser and a validated adapter. Generated command contracts use `python` to
mean the project environment's pinned Python 3.11+ interpreter; the CI matrix
provisions that launcher on every supported operating system.

Reference citations use repository aliases and are checked against
`shared/reference-evidence.json`, which records commit identity, authority
classification, dirty-state qualification, and selected content
fingerprints. That registry is blueprint provenance; it is never copied into a
generated project's dossier. For a dirty reference checkout, exact cited bytes
are fingerprinted while volatile counts of unrelated working-tree paths are
intentionally not treated as stable provenance.

## Choose a profile

- `minimal` — small, early, or low-risk initiatives needing the complete
  authority, definition, state, plan, validation, and handoff kernel.
- `standard` — the default for active multi-contributor work; adds structured
  traceability, evidence, reviews, events, artifacts, and extensions.
- `high-assurance` — agent-operable, sensitive, externally effective, or
  audit-oriented work; adds capabilities, reference extension validation,
  checksums, generated validation evidence, transition, history, and
  conditional approval, coordination, recovery, evaluation, and metrics
  contracts.

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

Every generated profile also includes a transactional maintenance command:

```text
python -B .agent/scripts/refresh.py --refresh
python -B .agent/scripts/validate.py --check
```

The project-local artifact registry remains authoritative; refresh derives the
catalog, path-authority map, and integrity manifest without inventing or
overwriting source artifacts. High Assurance includes checksums and generated
validation evidence in the same refresh transaction.

## Plan adoption for an existing project

Do not point the new-project generator at an established repository. Produce a
read-only reconciliation plan instead:

```text
python3 skills/project-bootstrap/scripts/plan_adoption.py \
  --target /absolute/path/to/existing-project \
  --profile standard
```

The planner reports exact collisions and conservative path/name candidates for
functional-equivalence review without reading file contents or modifying the
target. A candidate is not accepted as equivalent until its content and
authority are inspected. Adoption remains a separate, project-aware
implementation task that preserves existing authority and project-specific
content.

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
python3 skills/project-bootstrap/scripts/validate_skill_package.py
python3 skills/project-bootstrap/scripts/verify_reference_evidence.py
python3 skills/project-bootstrap/scripts/validate_blueprint.py
python3 skills/project-bootstrap/scripts/test_acceptance.py
```

The no-argument reference check validates the registry and every citation
against the recorded evidence. When the reference checkouts are available,
also verify their current commits and cited bytes explicitly:

```text
python3 skills/project-bootstrap/scripts/verify_reference_evidence.py \
  --reference-root CF=/absolute/path/to/commerce-foundry \
  --reference-root COE=/absolute/path/to/cooper-online-enterprises
```

When the skill entry or UI metadata changes, also run the skill-creator
`quick_validate.py` against `skills/project-bootstrap`. The
repository-contained metadata validator is the reproducible release check;
`quick_validate.py` is a compatibility check against the installed Codex
tooling. CI repeats the metadata, internal reference-registry/citation,
blueprint, and acceptance suites on supported Python runtimes and operating
systems; CI does not have the external reference checkouts.

See `RELEASE.md`, `CHANGELOG.md`, and `migrations/` for release and upgrade
rules.

## Adoption boundary

Generation transfers structure, schemas, vocabulary, and validation behavior;
never project facts, implementation state, decisions, permissions, approvals,
credentials, providers, legal conclusions, or readiness. Every target project
must inspect its own instructions and sources, adopt project-specific content
through valid authority, run real project checks, and disclose unknowns,
skipped checks, limitations, dirty state, and external effects.
