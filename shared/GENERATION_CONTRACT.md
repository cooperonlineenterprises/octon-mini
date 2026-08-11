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
- collaborator identities, maintainer counts, access observations, activity,
  reviewer capacity, or hosted repository settings;
- decisions or approvals;
- permissions or standing authorization;
- legal, privacy, security, or compliance conclusions;
- external accounts, credentials, URLs, vendors, or providers;
- source-project history or evidence.

The generated harness is an unadopted baseline. Its policy is deliberately
non-authorizing, project command hooks are unassessed, and generated reports
do not claim target-project readiness.

Three states remain distinct throughout generation and validation:

1. structural blueprint conformance means the generated contracts are
   internally valid;
2. project-harness adoption means project owners have assessed the hooks,
   triggers, authority basis, and evidence required by the selected profile;
3. demonstrated target-project readiness requires current project-specific
   implementation, operational, specialist, and external evidence.

Neither of the first two states implies the third.

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

A breaking migration must also ship executable valid and invalid fixtures. Its
reference transformation or reconciler must preserve stable IDs and accepted
authority, require explicit classification when a legacy relationship is
ambiguous, reject mixed live schema authorities, retain the exact pre-migration
state as rollback evidence, validate the candidate result against the new
schemas, and produce no further change when applied a second time.

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
negative tests. It also generates a project-check evidence store, an explicit
project-check writer, an unassessed privacy-minimized collaboration profile,
and the same provider-neutral small-team Git workflow portfolio. The validator
exposes a full read-only check, a read-only ready-frontier derivation, and a
separately invoked read-only collaboration assessment; none executes project
hooks. The collaboration assessment reads stored aggregate observations and
writes nothing. Larger profiles add operational records, project-extension
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
  transitions, plan and task acyclicity, dependency-gated readiness,
  reciprocal plan/task links, structured blockers, dossier traceability,
  nested instructions, extension compatibility, and path authority;
- validate collaboration evidence, freshness, confidence, team-band and
  workflow-selection coherence without counting read-only people, bots,
  automation, or activity as write authority;
- reject unknown, stale, conflicting, no-writer, and over-five workflow
  selection failures safely, reject enterprise workflow identifiers, and
  require every workflow operation to resolve to the closed tool catalog;
- derive an unordered ready frontier only from completed hard dependencies,
  passed or validly waived gates, resolved structured blockers, reciprocal
  links, and populated readiness contracts;
- keep timeline fields outside the closed readiness contracts and never use
  dates when deriving or ordering the core ready frontier;
- enforce the selected profile's minimum governed-file inventory and reject
  unregistered extension or capability roots; and
- label structural success as distinct from project readiness.

The generator may create initial empty stores and unassessed configuration. It
must not create an accepted decision, completed task, passing evidence record,
human approval, or readiness certification. A generated empty ready frontier
does not establish project adoption or permission.

## Collaboration and Git workflow rules

Every generated profile begins with `assessment_status: not_assessed`, unknown
confidence and team band, null counts and times, empty evidence/conflicts, and
no workflow. This is the only transferable collaboration state. Templates
never contain current-blueprint collaborator facts, project identities,
reviewers, providers, hosted settings, or accepted workflow decisions.

The supported human bands are exactly one (`solo`), two (`pair`), and three to
five (`tiny`) write-capable humans. Zero is blocked; more than five is
`unsupported_team_size` and has no enterprise fallback. Bots, automation,
read-only access, and recent activity do not change the human band. Expected
simultaneous human or agent work may add `concurrent_work` without changing
human count.

The base portfolio is exactly `solo_direct`, `solo_hybrid`, `pair_pr`, and
`tiny_pr`. It is provider-neutral, non-authorizing, and available in every
profile. Unknown, expired, or conflicting evidence cannot silently select a
workflow. Adoption requires a resolving accepted project-owned decision, but
that decision grants no local mutation, network, publication, review,
integration, release, or destructive authority. Project risks may add controls
without changing the team band or automatically selecting an assurance
profile.

GitHub is an optional integration boundary. Generation does not imply an
account, provider, credential, reviewer, branch protection, required check,
environment, release, successful CI result, or hosted permission. Any hosted
observation is gathered separately through an explicit read-only network
action; any push or PR publication remains explicitly authorized external
mutation.

The generated portfolio excludes GitFlow, merge queues, release trains,
stacked-PR dependency trains, fork-first internal contribution, multi-level
CODEOWNERS approval, multiple mandatory approval stages, dedicated release
manager handoffs, organization-wide ruleset orchestration, multi-environment
promotion pipelines, and enterprise issue or portfolio governance.

## Project-command and adoption evidence rules

Each `project_test`, `project_lint`, `project_build`, and `project_closure`
hook is deliberately assessed as exactly one of:

- `not_assessed`, allowed only before project-harness adoption;
- `configured`, with an owner, nonempty argv-style command and version command,
  both using the same executable, declared side effects and write scope, and
  an evidence-freshness contract;
- `not_applicable`, with a named owner and nonempty project-specific rationale.

Commands are represented as argument arrays and executed without implicit
shell interpretation. Structural `--check` validates configuration and
existing evidence only. It must never execute a project hook, update evidence,
or reinterpret a configured command as permission.

The separately invoked project-check writer is an explicit mutating workflow.
It runs only configured hooks, records unavailable and not-applicable outcomes
without converting them to passes, and appends closed evidence containing the
exact argv and tool version, executable fingerprint, source revision or
fingerprint, environment, dirty/untracked/ignored scope, start and end time,
outcome, limitations, skipped checks, declared possible external effects,
explicitly unassessed observed external effects, and repository mutations.
Output content is hashed rather than retained when it could expose secrets.
Mutation comparison is detection, not sandbox isolation.

An adopted project requires coherent adoption status, a resolved accepted
externally grounded adoption decision, no adoption blockers, every command
hook assessed, and fresh source- and command-bound passing evidence for every
configured hook. An adopted High-Assurance project additionally requires all
Conditional and Optional dossier triggers to be assessed and every applicable
control to retain an active owner, representation, review state, and current
evidence references. These checks establish adoption conformance only; they
cannot certify specialist conclusions or production readiness.

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

Standard and High-Assurance snapshots may include tool-neutral production
control extensions for operations/observability and security/supply chain.
They start disabled and unassessed, validate only project-owned declarations
and evidence references, deny network and filesystem effects, and never claim
that a deployment, monitor, scanner, review, signing service, or external
platform exists or ran. Enabling either package before its project-level
adoption is complete fails closed; a `not_applicable` package remains disabled.
