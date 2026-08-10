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
equivalent path/name candidates without reading their contents or writing.
Human or agent reconciliation is then a project-aware, authorized
implementation task that accepts equivalence only after content and authority
review.

## Origin and upgrade rules

The origin record contains:

- blueprint name and version;
- selected profile;
- generation date;
- target project name and slug;
- generated path inventory;
- generator and kernel versions;
- a transaction generation ID;
- an immutable initial-generation snapshot; and
- an append-only migration history.

The snapshot also records the harness kernel version and generator version
where available. This provenance is not a live dependency: later blueprint
changes cannot silently change a generated project's rules.

An upgrade is a new migration task. It must preserve `initial_generation`,
compare the current top-level version with the candidate blueprint, classify
deltas, preserve project-specific content, append a typed migration-history
record with authority and evidence references, and never replace accepted
target-project authority silently.

## Template variables

The initial generator supports:

- `PROJECT_NAME` (derived and Markdown-escaped for prose templates);
- `PROJECT_NAME_JSON` (derived with a standards-compliant JSON encoder);
- `PROJECT_SLUG`;
- `CREATED_DATE`;
- `BLUEPRINT_VERSION`;
- `HARNESS_KERNEL_VERSION` (the independently versioned harness-kernel
  compatibility axis);
- `PROFILE`;
- `HARNESS_REFRESH_COMMAND` and `HARNESS_REFRESH_WRITES` (derived from the
  selected profile, not supplied as project facts).

Unresolved or unknown template variables are validation failures.

## Harness generation requirements

Every profile generates the seven-file governance kernel, compact current
state, task and decision templates, a read-only validator, and positive and
negative tests. Larger profiles add operational records, project-extension
contracts, capability packages, and generated-integrity tooling.

The selected profile also defines a closed minimum operational-file
inventory. The generated validator rejects a missing required router, kernel
file, schema, script, state or store entry point, template, fixture, extension
registry, or capability-package baseline. Project-specific additions belong
inside the registered extension and capability namespaces; they do not make a
required baseline path optional. This harness-retention rule is separate from
the dossier artifact registry, whose assessed applicability and durable
omission records intentionally support combining or omitting dossier
representations.

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
- enforce the selected profile's minimum governed-file inventory and reject
  unregistered extension or capability roots; and
- label structural success as distinct from project readiness.

The generator may create initial empty stores and unassessed configuration. It
must not create an accepted decision, completed task, passing evidence record,
human approval, or readiness certification.

## Derived-file rules

Initial generation selects the profile-applicable artifact types and physical
representations from `dossier/artifact-types.json` and writes them to
`project-dossier/machine-readable/artifact-registry.json`. That project-local
registry becomes the authoritative source for artifact metadata in the
independent snapshot. It is not regenerated from the blueprint during ordinary
maintenance or upgrade.

`project-dossier/ARTIFACT_CATALOG.json` is a generated mirror of the
project-local registry.
`project-dossier/machine-readable/path-authority.json` is generated from the
same registry and its registered physical paths. The two files are sibling
mirrors; neither is the other's edit source. Shared JSON schemas are copied
into `.agent/schemas/` so every generated project is independently
validatable.

Every profile includes an explicit refresh command. Refresh first validates
non-derived sources, requires exact registry coverage for physical dossier
files, stages all applicable outputs, and only then replaces the derived set.
Minimal and Standard refresh the catalog, path-authority map, and manifest.
High Assurance additionally refreshes `project-dossier/CHECKSUMS.sha256` and
`.agent/generated/*`.

All refreshed outputs carry or are bound to one generation ID. Because
ordinary filesystems cannot atomically replace multiple files, the final
read-only check rejects any interrupted, partial, or mismatched set. Refresh
does not infer entries for unregistered files, rewrite the authoritative
registry, overwrite non-derived artifacts, or delete project sources.
Generated validation reports are closed machine-readable records scoped to
the checks actually performed before refresh. They distinguish `pass` from
`not_run`, enumerate failures and skips, disclose fingerprint and Git scope,
external effects, and limitations, and never convert structural success into
a readiness or authorization claim. The post-refresh exact-tree check is
reported by the refresh command's exit status rather than retroactively
claimed by the pre-refresh report.

## Extension boundary

The kernel is stable and domain-neutral. A registered extension must declare
its version, compatible kernel major version, confined config and validator
paths, owner, provenance, side effects, deprecation path, and
`authority_effect: restrictions_only`. Enabled validators return structured
JSON findings. Disabling an extension must require no kernel edit.
