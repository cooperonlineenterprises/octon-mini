# Project Blueprint

Project Blueprint is a reusable, versioned source for creating and operating a
project-specific agent harness and project dossier across software, product,
business, brand, research, operations, and hybrid work.

The generated systems remain separate:

- the **harness** defines repository-local guidance, deny-by-default authority
  boundaries, work records, automation contracts, and validation;
- the **dossier** documents definition, intended and observed state,
  conformance, plans, provenance, evidence, and handoff.

A dossier is never permission. Generated policy cannot create authority, and
automation cannot invent facts, owners, identities, decisions, approvals,
evidence, stable IDs, adoption, or readiness.

## What 4.0 changes

Version 4.0 makes the universal kernel thinner and ordinary operation faster:

- one authoritative profile/layout/package/inventory/acceptance manifest;
- one workflow-oriented `pb` command inventory projected into every snapshot;
- one catalog-driven, resumable, non-authorizing setup interview feeding the
  existing digest-bound initialization, adoption, and upgrade planners;
- read-only semantic detection and diagnosis;
- fully derived current state plus a small authoritative focus source;
- selective project checks and bounded immutable evidence history;
- one opt-in, provider-neutral, digest-bound and resumable small-team
  work-completion engine;
- trigger-installed Git, operations/observability, security/supply-chain,
  sample restriction, and optional-schema packages;
- compact physical dossier representation by default, with separated layout
  still supported; and
- fast, integration, and release validation tiers plus scale benchmarks.

Decision governance extends the existing decision concern with one
project-owned `DREG-####` register, gate-first trade-off review, compatibility
findings, read-only assurance, and a minimum closure graph. Recommendations,
owner selections, and accepted `DEC-####` authority remain distinct; scores
cannot compensate for a failed gate or conceal an evidence gap. See
`docs/DECISION_GOVERNANCE.md`.

Repository-local transactions are staged, validated, instruction- and
path-fingerprint-bound, receipted, and exactly recoverable. External Git and
provider effects cannot be rolled back atomically; governed work completion
records monotonic progress and resumes or fixes forward. There is no global
force mode.

## Independent selection axes

Choose each axis for its own reason:

| Axis | Values | Select from |
|---|---|---|
| assurance | Minimal, Standard, High Assurance | project risk and control needs |
| collaboration | solo, pair, tiny | 1, 2, or 3–5 write-capable humans |
| concurrency | `concurrent_work` or none | simultaneous human/agent/automation work |
| layout | compact or separated | representation ownership/lifecycle/review needs |

Minimal is the interactive recommendation, never a silent non-interactive
default. Missing, stale, or conflicting collaboration evidence selects no
workflow. A workflow proposal becomes adopted only through an accepted
project-owned decision. Team size never selects assurance.

## Repository layout

| Path | Role |
|---|---|
| `dossier/` | dossier blueprint, artifact taxonomy, reference evidence |
| `harness/` | harness architecture and acceptance contracts |
| `shared/` | generation contract, source manifests, schemas |
| `patterns/` | source-only pattern catalog and Architecture Proof assets |
| `skills/project-bootstrap/` | skill, templates, detectors, packages, scripts, fixtures |
| `migrations/` | version-to-version migration guidance |
| `docs/GOLDEN_PATHS.md` | verified operating paths |
| `docs/COMPATIBILITY.md` | v4 compatibility, migration, and deprecation boundary |
| `docs/DECISION_GOVERNANCE.md` | authoritative decision, review, maturity, handoff, and read-only assurance practice |
| `docs/GUIDED_SETUP.md` | canonical setup interview, session, authority, staleness, and migration practice |
| `VELOCITY_VALIDATION.md` | benchmarks, touchpoints, validation matrix |

Strict JSON and Python 3.11+ keep the generated kernel portable and
duplicate-key rejecting. Extensions may add formats only with a pinned parser
and validated adapter.

## New project

An AI agent or TTY can first run the shared setup interview. Question
generation is target-read-only; the optional session output is explicit and
must be outside the target:

```text
python3 skills/project-bootstrap/scripts/pb.py init setup \
  --target /absolute/path/to/new-project \
  --output /absolute/review-area/setup-01.json

# Supply a digest-bound answer batch, or use --tty, and write a successor.
python3 skills/project-bootstrap/scripts/pb.py init setup \
  --target /absolute/path/to/new-project \
  --session /absolute/review-area/setup-01.json \
  --answers /absolute/review-area/answers-01.json \
  --output /absolute/review-area/setup-02.json
```

The interview asks only unresolved, dependency-eligible questions, normally
one to three at a time. It preserves observations, inferences,
recommendations, owner selections, accepted-authority references, unknowns,
deferrals, and runtime authorization as different information roles. No
answer is preselected, and setup never stores secrets or grants permission.
See `docs/GUIDED_SETUP.md`.

Plan without changing the target:

```text
python3 skills/project-bootstrap/scripts/pb.py init plan \
  --target /absolute/path/to/new-project \
  --project-name "Example Project" \
  --profile minimal \
  --layout compact \
  --output /absolute/path/to/new-project/.agent/transactions/plans/init.json
```

After a session reaches `ready_for_plan`, the same existing planner accepts
`--setup-session /absolute/review-area/setup-02.json` instead of duplicate
setup flags. The plan binds the exact session digest and bytes. Apply
revalidates the session, target, instructions, plan digest, and ordinary
transaction preconditions.

Review the observations, inferences, explicit decisions, authorization gates,
exact operations, validation, rollback, and digest. Then apply that digest:

```text
python3 skills/project-bootstrap/scripts/pb.py init apply \
  --target /absolute/path/to/new-project \
  --plan /absolute/path/to/new-project/.agent/transactions/plans/init.json \
  --accept-digest <reviewed-digest>
```

Interactive `pb init` proposes Minimal and asks for confirmation. Scripted use
must pass `--profile`. An explicitly supplied first task is created in the
same candidate only when all task semantics are supplied. The full release
tier passes in staging before the target is written.

The primitive `scaffold_project.py` remains available for advanced generation
diagnostics and `--dry-run`. Generation uses
`shared/source-contracts/profile-manifest.json`; unreviewed source additions
are ignored and diagnosed, while unsafe paths, output collisions, forbidden
destinations, and missing required inputs fail closed.

## Established project

Use content-aware adoption rather than the empty-project generator:

```text
python3 skills/project-bootstrap/scripts/pb.py adopt plan --help
```

Use `pb adopt setup` before planning when a guided interview is desired. It
does not replace the bounded semantic proposal/review contract; proposal-bound
collision and functional-equivalence dispositions remain authoritative.

Default inspection is bounded to 200 allowlisted text/config files, 256 KiB
each, and 4 MiB total. It excludes secrets, `.env*`, private keys, symlinks,
binaries, ignored/generated/vendor/dependency/build/coverage content, and
sensitivity-marked paths. It retains hashes and matched semantic vocabulary,
not project content.

The proposal distinguishes confirmed collisions, likely functional
equivalents, authority conflicts, safe and reviewed additions, unresolved
project facts, hook candidates, and ambiguity. Functional equivalence and
authority preservation always require proposal-bound review. Apply preserves
all established content, runs the release tier in staging, and leaves harness
adoption `in_progress`.

## Routine project operation

Every generated snapshot includes `./pb`:

```text
./pb work start --help
./pb work close --help
./pb work handoff --help
./pb work resume
./pb work finish plan
./pb check
./pb doctor
./pb maintain registry plan
./pb maintain hooks plan --help
./pb maintain collaboration plan --help
./pb maintain refresh --apply
```

Work automation allocates stable IDs and synchronizes legal transitions,
reciprocal plan links, focus, derived current state, and handoff pointers. The
operator still owns task purpose, scope, authority basis, acceptance criteria,
priority, substantive review, closure claims, evidence, and external-effect
authorization.

`work finish` is generated disabled and becomes usable only after explicit
project adoption of its existing small-team workflow, repository, provider,
check, eligible peer reviewers where applicable, exact read-only completion
command hook, and cleanup inputs. `plan` performs no writes, refresh,
fetch, hosted query, or receipt update. `apply` reconstructs the plan from the
completed task's exact completion contract, accepts only its reviewed digest,
and requires current task-scoped authorization for the exact external
operation list. `resume` observes completed effects before acting so a partial
run does not duplicate commits, PRs, merges, pushes, or deletes. Pair and tiny
teams require a real approval by another eligible developer; agent or
self-review never counts. See the installed small-team workflow README for the
configuration and receipt contract.

`./pb check` is read-only and never runs hooks. Configure each test, lint,
build, and closure hook with shell-free argv, owner, rationale, version probe,
freshness, and side effects—or explicitly assess it `not_applicable`. Run hooks
only through the separate explicit evidence writer:

```text
python -B .agent/scripts/run_project_checks.py --write-evidence
```

Use `--hook`, changed-scope routing, and `--acknowledge-side-effects` as their
contracts require. `--verify-adoption` runs the complete configured hook set,
refresh, and final read-only check. Current evidence is bounded; prior records
move to immutable date-partitioned archives with successor relationships.

## Collaboration, SCM, and domain packages

Collaboration v2 requires evidence only for facts used by the result, while
every used fact has source, observation time, expiry, and limitations. It
stores no identities. Concurrent work is a modifier. Assurance remains
unchanged.

The kernel contains a compact SCM trigger and pinned package digest, not the
full Git portfolio. Detection proposes Git without selecting it. An accepted
decision triggers a transactional, content-addressed installation:

```text
python3 skills/project-bootstrap/scripts/pb.py maintain package plan --help
```

Domain-trigger absence never means `not_applicable`. Applicable packages
require explicit owner, accepted trust decision, pinned version/digest, exact
installed-content digest, and a successful transaction receipt. Extensions are
installed disabled; readiness and enablement remain separate.

## Recovery and upgrades

`./pb doctor` emits versioned codes with root cause, owning authority source,
dependent symptoms, safe next action, and repair class. It is read-only unless
an exact derived-only repair digest is explicitly accepted.

```text
./pb transaction recover --pending <journal>
./pb transaction rollback --receipt <receipt>
```

Recovery restores only exact preimages or finalizes an exact terminal receipt.
Rollback durably marks its in-progress state, resumes after interruption, and
refuses a path changed independently. Stale plans, evidence, instructions, or
target bytes require re-planning.

Live upgrade is a three-way comparison of recorded old baselines, current
project, and candidate Blueprint:

```text
python3 skills/project-bootstrap/scripts/pb.py upgrade plan --help
```

`pb upgrade setup` uses the same session engine. Every nonautomatic path still
requires one exact disposition in the existing proposal-bound upgrade review;
the session references that review rather than duplicating it.

Only exact-pristine non-authoritative implementation assets, safe additions,
and derived regeneration are automatic. Instructions, policy, project config,
workflow adoption, dossier sources/registries, records, current facts, stable
IDs, deletions/moves, permissions, symlinks, and modified content require
explicit review. For 3.1→4.0, first create the reviewed legacy inventory seed
described in `migrations/3.1.0-to-4.0.0.md`. Structural upgrade does not imply
harness adoption or project readiness.

## Validate, benchmark, and install

```text
python3 skills/project-bootstrap/scripts/validate_skill_package.py
python3 skills/project-bootstrap/scripts/verify_reference_evidence.py
python3 skills/project-bootstrap/scripts/validate_source_contracts.py
python3 skills/project-bootstrap/scripts/test_architectural_patterns.py
python3 -B skills/project-bootstrap/scripts/test_migration_1_0_1_to_2_0_0.py
python3 -B skills/project-bootstrap/scripts/test_migration_2_0_0_to_3_0_0.py
python3 -B skills/project-bootstrap/scripts/test_migration_3_1_0_to_4_0_0.py
python3 -B skills/project-bootstrap/scripts/test_velocity_workflows.py
python3 skills/project-bootstrap/scripts/validate_blueprint.py
python3 skills/project-bootstrap/scripts/test_acceptance.py
python3 skills/project-bootstrap/scripts/benchmark_validation.py --enforce
```

The skill installer is collision-safe, bundles an independent source snapshot,
and validates it before placement:

```text
python3 skills/project-bootstrap/scripts/install_skill.py --dry-run
```

When `SKILL.md` or `agents/openai.yaml` changes, also run the installed
skill-creator `quick_validate.py`. See `RELEASE.md`, `CHANGELOG.md`,
`docs/GOLDEN_PATHS.md`, and `VELOCITY_VALIDATION.md` for verified details and
limitations.

## Claim boundary

Generation transfers structure, schemas, vocabulary, and validation behavior;
never implementation state, decisions, permission, approvals, credentials,
providers, legal conclusions, or readiness. Report structural conformance,
harness adoption, and target-project readiness separately, including unknowns,
skipped work, stale evidence, dirty state, limitations, and external effects.
