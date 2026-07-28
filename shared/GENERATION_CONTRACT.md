# Generation Contract

## Source and output roles

`project-blueprint` is the versioned reference and generator source. A target
project receives an independent snapshot containing:

- `AGENTS.md`;
- `.agent/`;
- `.agents/` for profiles that include capability packages;
- `project-dossier/`;
- `.project-blueprint-origin.json`.

Generated files do not remain linked to this repository.

## Non-transfer rules

Generation transfers structure, schemas, vocabulary, and validation patterns.
It does not transfer:

- project facts or implementation status;
- decisions or approvals;
- permissions or standing authorization;
- legal, privacy, security, or compliance conclusions;
- external accounts, credentials, URLs, vendors, or providers;
- source-project history or evidence.

The generated harness is an unadopted baseline. Its policy is deliberately
non-authorizing, project command hooks are unassessed, and generated reports
do not claim target-project readiness.

## Collision and mutation rules

New-project generation accepts only a nonexistent or empty target directory.
The generator resolves its complete intended output, renders it in a sibling
staging directory, validates the staged snapshot, and atomically places the
snapshot at the target. Validation failure leaves the target unchanged. It
must not offer an overwrite, force, or in-place merge mode.

Integration with an established repository starts with the separate read-only
`plan_adoption.py` inventory. That plan identifies collisions and functional
equivalents without writing. Human or agent reconciliation is then a
project-aware, authorized implementation task.

## Origin and upgrade rules

The origin record contains:

- blueprint name and version;
- selected profile;
- generation date;
- target project name and slug;
- generated path inventory.
- generator and kernel versions; and
- a transaction generation ID.

The snapshot also records the harness kernel version and generator version
where available. This provenance is not a live dependency: later blueprint
changes cannot silently change a generated project's rules.

An upgrade is a new migration task. It must compare the recorded version with
the candidate blueprint, classify deltas, preserve project-specific content,
and never replace accepted target-project authority silently.

## Template variables

The initial generator supports:

- `PROJECT_NAME` (derived and Markdown-escaped for prose templates);
- `PROJECT_NAME_JSON` (derived with a standards-compliant JSON encoder);
- `PROJECT_SLUG`;
- `CREATED_DATE`;
- `BLUEPRINT_VERSION`;
- `PROFILE`.
- `HARNESS_REFRESH_COMMAND` and `HARNESS_REFRESH_WRITES` (derived from the
  selected profile, not supplied as project facts).

Unresolved or unknown template variables are validation failures.

## Harness generation requirements

Every profile generates the seven-file governance kernel, compact current
state, task and decision templates, a read-only validator, and positive and
negative tests. Larger profiles add operational records, project-extension
contracts, capability packages, and generated-integrity tooling.

Canonical structured files are strict JSON. Every parser rejects duplicate
keys. YAML is allowed only inside a registered extension that declares and
bootstraps a pinned parser; YAML never becomes a hidden dependency of the
domain-neutral kernel.

The scaffold validator must:

- run without another repository's environment;
- require Python 3.11 or newer;
- use `--check` as a read-only operation;
- reject critical authority-policy mutations;
- validate all repository source paths by default, with only explicit,
  reasoned fingerprint exclusions;
- detect unresolved generation placeholders and redact obvious secret
  assignments;
- validate strict syntax, schemas, controlled IDs, references, lifecycle
  transitions, plan acyclicity, dossier traceability, nested instructions,
  extension compatibility, and path authority; and
- label structural success as distinct from project readiness.

The generator may create initial empty stores and unassessed configuration. It
must not create an accepted decision, completed task, passing evidence record,
human approval, or readiness certification.

## Derived-file rules

`project-dossier/ARTIFACT_CATALOG.json` is generated from
`dossier/artifact-types.json`. `project-dossier/machine-readable/path-authority.json`
is generated from that catalog and the selected profile. Shared JSON schemas
are copied into `.agent/schemas/` so every generated project is independently
validatable.

`project-dossier/MANIFEST.json`, `project-dossier/CHECKSUMS.sha256`, and
`.agent/generated/*` are point-in-time integrity outputs. High-assurance
refresh validates sources first and assigns one generation ID to the refreshed
set. Because ordinary filesystems cannot atomically replace multiple files,
the final read-only check rejects any interrupted, partial, or mismatched set.

## Extension boundary

The kernel is stable and domain-neutral. A registered extension must declare
its version, compatible kernel major version, confined config and validator
paths, owner, provenance, side effects, deprecation path, and
`authority_effect: restrictions_only`. Enabled validators return structured
JSON findings. Disabling an extension must require no kernel edit.
