# Project Agent Harness Blueprint

## 1. Purpose

A project agent harness is the repository-local operating system for safe,
resumable work by humans and agents. It routes instruction discovery, states
authority boundaries, defines record and lifecycle contracts, exposes
validation commands, and preserves evidence.

Its universal scope is a stable domain-neutral kernel with validated extension
points, not a claim that one project's policies or domain rules fit another.
The information and behavior contracts are runtime-neutral. The generated
snapshot supplies a Python 3.11+ standard-library reference implementation,
but a project may adopt an equivalent validator in its existing pinned
toolchain after that implementation passes the same conformance fixtures and
records a migration. A project must not add Python solely to imitate the
reference implementation when its governed toolchain can satisfy the contract.

The harness is subordinate to current user, platform, sandbox, tool, legal,
and applicable repository instructions. It cannot create permission. A tool,
plan, decision template, skill, generated report, or dossier statement is not
authorization.

A working harness enables a newcomer to determine:

- which instructions apply to a path;
- whether the request is analysis, implementation, or an external action;
- which project facts are stable and which work state is current;
- why durable choices were made;
- which checks and approvals apply;
- what evidence supports a claim;
- what remains blocked or unknown; and
- which planned work is dependency-ready without relying on timeline order;
  and
- how to resume work safely.

## 2. Design basis

Evidence labels used in this blueprint:

- **Observed — Commerce Foundry:** present in the Commerce Foundry reference
  implementation.
- **Observed — COE:** present in the Cooper Online Enterprises reference
  implementation.
- **Observed — both:** materially equivalent behavior exists in both.
- **Inference:** a reusable rule derived from one or both implementations.
- **Recommendation:** a new domain-neutral addition needed for portability,
  safety, or completeness.

Exact reference paths and the transfer boundary are recorded in
`harness/references/REFERENCE_EVIDENCE.md`. These labels distinguish evidence
from design judgment; they do not import either source project's facts or
authority.

The reusable model synthesizes two mature reference patterns:

- an operational harness with deny-by-default local execution, lifecycle
  records, executable policy checks, mutation tests, and routed skills; and
- an information-integrity harness with root-to-leaf scoping, typed IDs,
  path-authority classification, record templates, manifests, checksums, and
  generated validation evidence.

The synthesis is intentionally not a union of their files. The common
governance kernel is separated from project-specific extensions, optional
capability packages, and generated evidence.

The following are design inferences and recommendations:

- roles are constrained task modes, not independent principals;
- one authoritative store owns each mutable concern;
- current state, intended target, plans, permission, and evidence remain
  distinct;
- domain rules belong in extensions, not in kernel constants;
- validation and generation are separate operations;
- passing evidence is scoped and point-in-time;
- the safe path has one discoverable check command; and
- ceremony is added only for a named risk or coordination need.

## 3. Five-layer architecture

### Layer 1: instruction router

Root and nested `AGENTS.md` files tell an agent what to read, how path scoping
works, what closes work, and which actions require explicit current
authorization. They stay short enough to load routinely.

### Layer 2: governance kernel

The seven versioned files below are domain-neutral and have one responsibility
each:

| File | Authoritative concern |
|---|---|
| `.agent/policy.json` | permission classes, hard boundaries, and approval gates |
| `.agent/context.json` | precedence, trust classes, and conflict handling |
| `.agent/schema.json` | IDs, statuses, record versions, and compatibility |
| `.agent/lifecycle.json` | legal task, decision, and artifact transitions |
| `.agent/tools.json` | availability, allowed operations, constraints, and evidence |
| `.agent/validators.json` | named check, test, refresh, and closure commands |
| `.agent/project.json` | stable project profile, collaboration assessment, workflow adoption, and project command hooks |

`project.json` must not become a second status report. Mutable work status
belongs in tasks and `.agent/state/current.json`.

### Layer 3: capability packages

`.agents/agents/`, `.agents/skills/`, and `.agents/workflows/` define
specialist modes and reusable procedures. Each capability inherits the active
task's authority, may narrow it, and may never expand it.

Capability packages are conditional. Do not add named agents or skills until
a recurring job, quality boundary, or role-separation need justifies them.

### Layer 4: project profile and extensions

`.agent/project.json` declares stable repository facts, a current
privacy-minimized collaboration assessment, any adopted small-team workflow,
and command hooks.
`.agent/extensions/` owns domain registries, build or release rules, and
project-specific validators.

An extension:

- declares a stable ID, schema version, compatibility range, owner, provenance,
  trust class, config, validator, side effects, and deprecation/removal path;
- returns structured findings through the kernel interface;
- can add restrictions and checks;
- cannot weaken the kernel or grant authority; and
- can be disabled without changing kernel behavior.

Extension code is executable project code, not untrusted data. Enabling it
requires an accepted trust decision, least-privilege execution, a minimized
environment, and a read-only enforcement or before/after mutation check.

Standard and High Assurance include disabled, unassessed, tool-neutral
operations/observability and security/supply-chain packages. They validate
project-owned declarations and evidence links only. Their presence cannot
assert a provider, deployment, monitor, scanner, SBOM, signature, qualified
review, compliance conclusion, or production readiness.

The extension root is closed: only its README, registry, and roots named by
that registry are valid immediate children. Likewise, the capability root
contains only its README and the validated agent, workflow, and skill
namespaces. Project-specific behavior is added through those registries and
namespaces, not through unregistered governance files.

### Layer 5: operational records and evidence

Tasks, decisions, evidence, reviews, events, artifacts, state, checkpoints,
explicit target-project check evidence, and generated integrity make work
resumable and auditable.

## 4. Architectural invariants

1. Higher-level instructions cannot be weakened by lower-level files.
2. A capability or extension cannot grant itself access.
3. Generated content is labeled derived, non-authoritative, and point-in-time.
4. `check` is read-only; `refresh` is the explicit generated-integrity writer,
   and only the separately invoked project-check writer may execute configured
   hooks or append its declared evidence store.
5. The kernel contains no product names, routes, release IDs, or domain
   statuses.
6. Unknown safety-relevant statuses, IDs, tools, and extension types fail
   closed.
7. Durable accepted decisions use successors instead of silent rewrites.
8. Task records describe work; they do not authorize it.
9. Evidence never includes secret values and never claims more than the
   recorded check proves.
10. Generated projects are independent snapshots and do not inherit authority
    from this blueprint.
11. Every derived dossier or harness file has one project-local source and one
    discoverable regeneration command in every profile that enforces it.
12. A declared read-only command must either execute in an enforced no-write
    boundary or detect and report any mutation without claiming prevention.
13. Hard dependencies, satisfied gates, resolved structured blockers, and
    reciprocal plan/task links determine work readiness; dates never do.
14. Collaboration observations, workflow recommendations, and workflow records
    are non-authorizing; only a project-owned accepted decision may adopt a
    workflow, and it still cannot authorize an operation.
15. Human team size selects only the base collaboration workflow. It never
    selects an assurance profile or grants access, approval, review capacity,
    publication authority, or release authority.
16. More than five write-capable humans is explicitly unsupported and never
    falls through to an enterprise workflow.

## 5. Recommended directory structure

```text
.
├── AGENTS.md
├── .agent/
│   ├── START_HERE.md
│   ├── policy.json
│   ├── context.json
│   ├── schema.json
│   ├── lifecycle.json
│   ├── tools.json
│   ├── validators.json
│   ├── project.json
│   ├── workflows/
│   │   └── small-team-git.json        # provider-neutral, non-authorizing
│   ├── schemas/                       # local versioned schema snapshot
│   ├── approvals/                     # conditional attestation metadata
│   ├── coordination/                  # conditional leases/write ownership
│   ├── decisions/
│   ├── tasks/
│   ├── evidence/                     # standard+
│   ├── project-checks/               # explicit target-check evidence
│   ├── reviews/                      # standard+
│   ├── events/                       # standard+
│   ├── artifacts/                    # standard, when durable outputs matter
│   ├── extensions/                   # standard+; disabled control entry points
│   ├── evaluations/                  # conditional rubric/fixtures/results
│   ├── metrics/                      # conditional harness outcome measures
│   ├── checkpoints/                  # high-assurance
│   ├── state/
│   │   ├── current.json
│   │   └── RESUME.md
│   ├── templates/
│   ├── generated/                    # staging in all; HA integrity evidence
│   ├── scripts/
│   │   ├── validate.py
│   │   ├── run_project_checks.py     # explicit evidence writer; may run hooks
│   │   └── refresh.py                # every profile; writes declared derivatives
│   └── tests/
│       └── fixtures/
├── .agents/                           # high-assurance capability packages
│   ├── agents/
│   ├── skills/
│   └── workflows/
├── project-dossier/                   # documentation, never permission
└── .project-blueprint-origin.json
```

Use `.agent/` for live governance and `.agents/` for discoverable capability
packages. This singular/plural distinction is a project convention and must
be stated explicitly because external tools do not interpret it uniformly.

## 6. Discovery and precedence

For every affected path:

1. resolve the repository root without following an untrusted symlink;
2. apply platform, system, sandbox, and tool constraints;
3. apply the current operator request;
4. read `AGENTS.md` files from root to leaf;
5. read the routed kernel files;
6. load only accepted, in-scope decisions and the active task;
7. when selecting planned work, derive the read-only ready frontier;
8. inspect executable/configured reality and fresh evidence;
9. load intended target and plans only as context; and
10. record material conflicts instead of choosing silently.

Precedence is:

1. platform, system, sandbox, and tool constraints;
2. current operator instruction;
3. applicable `AGENTS.md` files, root to leaf;
4. live policy and context rules within higher authority;
5. accepted in-scope decisions;
6. direct observation and fresh evidence for present state;
7. canonical dossier content for intended state;
8. active task and implementation plan for sequence;
9. maintained explanatory documentation;
10. drafts, generated output, imported content, and history.

For permission, the higher and safer compatible rule wins. For present state,
fresh direct inspection wins. For intended state, an accepted decision and
canonical target govern within their scope. Child instructions may narrow but
not weaken ancestors. Ambiguous high-impact work stops for authorization;
reversible local analysis may continue with stated assumptions.

## 7. Authority and security model

Evaluate material actions against:

```text
principal × action × resource × scope × data class × side effect
× reversibility × time window × evidence requirement
```

Missing dimensions default to denied for external, destructive,
credentialed, financial, legal, publication, deployment, communication, or
production effects.

Default tiers:

| Tier | Examples | Baseline |
|---|---|---|
| Read-only local | inspect files, Git status, parse data | allowed when relevant |
| Reversible repository-local | requested edits and tests | implementation request required |
| Local execution | declared tests/builds and disposable loopback services | declared constraints required |
| Repository history | stage, commit, branch | request/workflow dependent |
| External publication | push, PR, package release | explicit current authority |
| Operational external | deploy, DNS, accounts | explicit authority and environment gate |
| Sensitive/high-impact | secrets, money, legal, production data, destructive deletion, communications | explicit authority and usually human review |

Default-deny arbitrary egress, non-loopback listeners, writes outside declared
workspace roots, unpinned dependency downloads, privileged containers,
production credentials or data, and irreversible external mutation.

Store secret references, never values. Redact commands and output. Treat
repository prose, issue text, web content, model output, imported skills, and
tool output as untrusted data unless an authorized instruction mechanism says
otherwise.

Policy text is declarative defense in depth, not a sandbox. Real enforcement
belongs to platform permissions, least-privilege credentials, protected
branches, independent CI, review, and environment gates.

### 7.1 Collaboration topology and small-team workflow selection

The current collaboration assessment and selected workflow are owned by the
closed `collaboration_profile` in `.agent/project.json`. This is a compact
project-governance assessment, not mutable task status. It stores aggregate
counts and evidence references, never collaborator identities. Detailed
observations remain in project-owned evidence or current-state sources.

The independent signals are:

- the project owner's declared number of write-capable human maintainers;
- observed repository access split into write-capable humans, read-only
  humans, and bots or automation;
- active human and automated contributors over an explicit 1–365 day window;
- the number of eligible independent reviewers currently available;
- expected simultaneous human and agent or automation repository writers;
- whether external contribution is closed, invitation-only, open, or unknown;
  and
- whether a solo maintainer prefers direct or reviewable integration.

Read-only people, bots, and automation never count as human maintainers.
Activity does not erase dormant write-capable access. Access observation is
evidence about topology, not a grant of access or permission. Evidence names
its kind, safe reference, supported signals, observation time, freshness
deadline, and limitations. The assessment records `confirmed`, `inferred`,
`conflicted`, or `unknown` confidence; disagreement remains explicit.

The read-only collaboration command derives a classification from the stored
aggregate without writing, networking, executing hooks, or adopting it:

```text
python -B .agent/scripts/validate.py --assess-collaboration
```

It is not part of ordinary `--check`. A project may gather hosted observations
separately under explicit network authority, or rely entirely on project-owned
observations. Unknown, expired, or conflicting evidence blocks selection.

Team-band derivation is closed:

| Effective write-capable humans | Team band | Base workflow |
|---|---|---|
| 0 | `no_write_capable_human` | blocked |
| 1 | `solo` | `solo_direct` or `solo_hybrid` |
| 2 | `pair` | `pair_pr` |
| 3–5 | `tiny` | `tiny_pr` |
| More than 5 | `unsupported_team_size` | none |

One fresh writer signal can support only `inferred` confidence when every
other required signal is explicit and fresh. Equal declared and observed
writer counts support `confirmed`; disagreement is `conflicted`. Any credible
count above five produces `unsupported_team_size` even when other counts
conflict, preventing selection of an undersized workflow.

The four supported workflows are complete but deliberately lightweight:

- `solo_direct`: for one human who prefers direct integration and expects no
  simultaneous writer. Inspect the revision and worktree, make a bounded
  change on the default branch, validate locally, stage and commit, publish
  only with explicit current authority, then observe CI. Substantial or
  high-risk work escalates to `solo_hybrid` and may add stronger risk controls.
- `solo_hybrid`: create and switch to a short-lived task branch, make the
  bounded change, validate, stage and commit, optionally publish a self-PR,
  observe CI, perform self-review with limitations, integrate using the one
  project-adopted method, and safely clean up the branch.
- `pair_pr`: create a short-lived task branch, validate and commit, publish a
  PR under current authority, observe CI, obtain one peer review when an
  eligible reviewer is available, integrate with the one adopted method, and
  safely clean up. If capacity is absent, record the limitation and block
  rather than fabricate an approval.
- `tiny_pr`: use the same short-lived branch, PR, CI, integration, and cleanup
  lifecycle for three to five humans. At most one peer approval may be
  required. Lightweight ownership guidance is optional and must address an
  observed coordination need; it never becomes a multi-level approval system.

Any supported band with simultaneous writers applies the `concurrent_work`
modifier. Each task uses its own branch or worktree, records a shared base
revision and declared write scope, detects conflicts deterministically, and
defines cancellation, handback, and partial-result behavior. Agents and
automation change only this modifier, never the human team band. A
High-Assurance coordination lease is an optional stronger realization when a
named risk warrants it; the modifier itself applies in every profile.

`.agent/workflows/small-team-git.json` is the provider-neutral, non-authorizing
workflow source. Every operation it uses resolves to the ordered catalogs in
`.agent/tools.json`. A recommendation does not adopt a workflow. Adoption
requires a resolving accepted project-owned `DEC-####`, but neither the
decision nor the workflow grants permission to edit, fetch, push, publish a
PR, replace history, create a release tag, or perform recovery.

Team size selects only the base workflow. Project risk independently adds
validation, review, protected enforcement, external-effect gates, or qualified
specialists. It never changes the team band and does not automatically select
Standard or High Assurance.

GitHub integration is optional. Repository-local contracts never imply a
provider, account, credential, reviewer, branch protection, required check,
environment, release, successful CI run, or hosted permission. Provider
publication remains an explicitly authorized external action.

The portfolio expressly excludes GitFlow with long-lived development/release/
hotfix branches, merge queues or batch integration, release trains, stacked-PR
dependency trains, fork-first internal contribution, multi-level CODEOWNERS
approval hierarchies, multiple mandatory approval stages, dedicated release
manager handoffs, organization-wide ruleset orchestration, multi-environment
promotion pipelines, and enterprise issue-triage or portfolio governance.
Simple PRs, CI, one-peer review, and risk-justified branch protection remain
valid small-team controls.

## 8. Record and state model

| Concern | Store | Mutability | Meaning |
|---|---|---|---|
| collaboration topology and adoption | `project.json` | reassessed project source plus accepted decision reference | which small-team workflow fits without creating permission |
| provider-neutral Git workflow | `workflows/small-team-git.json` | versioned kernel contract | complete supported steps and explicit enterprise exclusions |
| durable intent | `decisions/` | immutable plus successor | why a lasting choice exists |
| active work | `tasks/` | lifecycle updates | what is being done |
| observation | `evidence/` | immutable record | what was inspected or executed |
| review finding | `reviews/` | disposition updates | what a separate pass found |
| chronology | `events/` | append-only | meaningful transitions |
| approval attestation | `approvals/` | immutable plus revocation/successor | who attested to what, under which external authority |
| coordination lease | `coordination/` | expiring lifecycle | who owns a write scope and until when |
| current view | `state/current.json` | project-maintained compact operational index | what to resume now |
| artifact metadata | `artifacts/registry.json` | lifecycle updates | provenance and promotion |
| evaluation | `evaluations/` | versioned fixtures and results | whether repeated work meets a declared rubric |
| harness metric | `metrics/` | generated/observed series | whether the harness improves closure, safety, and resumption |
| generated integrity | `generated/` | regenerated | point-in-time inventory and results |

Each record declares `schema_version`, stable ID, purpose/title, scope,
authority source, owner/maintainer, inputs, outputs or links, side effects,
status, timestamps as applicable, validation, limitations, provenance, and
successor/deprecation fields where applicable.

Task `dependencies` are hard `TASK-####` prerequisites. `plan_item_refs` and
plan-item `task_refs` are reciprocal. `gate_refs` name structured readiness
gates, while `blocking_refs` name status-bearing task, plan, gate, decision, or
RAIDQ records. Free-text `blocked_by` explains impact but cannot by itself make
a blocked state machine-verifiable.

Approval records are evidence of an attestation received through a separately
authorized channel; they cannot manufacture that authority. They identify the
principal or role, action, resource/scope, constraints, validity window,
source reference, evidence fingerprint, revocation state, and successor.
Secret material and reusable credentials are never copied into the record.
`state/current.json` is a project-maintained source summary, not a generated
view and not an authorization channel. Its task, decision, evidence, and
external-authority references must resolve and remain status-consistent;
updates to owning records require a deliberate compaction update.

### Task lifecycle

```text
proposed → ready → in_progress → validating → review → completed
             │         ├──────────────→ blocked
             │         └──────────────→ cancelled
             └────────────────────────→ blocked
blocked → ready
completed → reopened → ready
```

- `ready` requires scope, authority basis, acceptance criteria, a validation
  plan, completed hard dependencies, passed or validly waived gates, resolved
  structured blockers, and reciprocal plan links.
- `in_progress` requires an owner.
- `validating` requires an implementation or analysis result.
- `review` requires evidence or an explicit limitation.
- `completed` requires satisfied criteria, closure evidence, and disclosure of
  external effects and limitations.
- `blocked` names the missing fact or authority and links at least one
  unresolved structured dependency, gate, blocker, or plan condition.
- `reopened` links the evidence that invalidated completion.

Entering or re-entering execution always passes through `ready`. If a completed
dependency reopens, a gate expires, or a blocker becomes active, affected
nonterminal downstream tasks move to `blocked`; downstream `completed` claims
become invalid until reassessed. The validator rejects task cycles and any
`ready`, execution, review, or completion state whose readiness conditions are
unsatisfied.

The ready frontier is a read-only derivation of eligible planned items and
tasks. It is not stored as authority or mutable status. Dependencies define a
partial order, so current operator direction or an accepted priority/value/risk
decision selects among multiple ready items. Creation/update dates, evidence
freshness, gate expiry, and genuine external deadlines remain useful time data
but never satisfy prerequisites or silently choose work. Frontier arrays use
stable identifier order only for deterministic display, never as priority.

### Decision lifecycle

Use `proposed`, `accepted`, `rejected`, `superseded`, and `deprecated`.
Changing the meaning of an accepted decision requires a successor that names
the superseded record.

### Artifact lifecycle

Where durable non-code outputs matter:

```text
scratch → draft → reviewed → approved → final → archived
```

The registry records source inputs and licenses, producer/tool version,
validation and review, data class, retention, destination, required approver,
fingerprint, and supersession. It stores metadata, not secret or duplicate
large content.

### Event and recovery discipline

Every event has a globally unique ID, monotonic sequence within its declared
stream, exact subject reference, timestamp, actor/source, kind, redaction
status, and evidence links. Validation rejects duplicate or decreasing
sequence values, unresolved subjects, invalid event kinds, and malformed
recovery records. Append-only corruption is recovered by preserving the
damaged bytes as evidence, creating a successor stream/checkpoint, and
recording the mapping; history is never silently rewritten.

### Context budgets

- root instructions: routinely readable;
- `state/current.json`: preferably under 100 lines;
- `state/RESUME.md`: preferably under two pages;
- active task: preferably under 200 lines;
- skill entry file: preferably under 300 lines with routed references; and
- events: one fact-focused record per meaningful transition.

History belongs in durable records, not in an ever-growing resumption summary.

## 9. Agent, skill, workflow, tool, and extension contracts

Every component declares:

- stable ID and schema version;
- purpose and scope;
- required inputs and produced outputs;
- authority source and `may_expand: false`;
- side-effect class;
- prohibited behavior;
- validation method;
- version and provenance;
- owner/maintainer; and
- deprecation or successor.

Agent and workflow records use strict, closed JSON contracts from
`harness-capability-records.schema.json`; arbitrary workflow state names are
represented as closed state records with validated references. Generated
capabilities start as `generated_unadopted_baseline` with
`permission_grant: false`, unassigned ownership, unassessed license/security
review, and explicit limitations. Adopting a capability requires a
project-specific accepted trust and authority decision referenced by
`adoption_decision_ref`; schema conformance cannot perform that adoption. A
skill's `SKILL.md` frontmatter contains only `name` and `description`;
version, trust, review, and update metadata belong in its separate closed JSON
provenance record.

Project-harness adoption uses `not_assessed`, `in_progress`, `adopted`, and
`superseded` consistently across the project, policy, context, and current
state. `adopted` and `superseded` retain the resolved accepted external-authority
decision as provenance; pre-adoption states keep the decision reference null.

Target-project test, lint, build, and closure hooks use a separate closed
three-state contract. `configured` requires an assigned owner, direct argv and
version argv using the same executable, timeout, evidence freshness, and
declared repository/external effects. `not_applicable` requires an owner and
substantive rationale.
`not_assessed` is permitted only before harness adoption. String commands and
shell interpreters with inline command flags are rejected; validation does not
silently reinterpret them.

An explicit project-check writer is the only generated command allowed to
execute configured hooks or append `.agent/project-checks/evidence.json`. It
records command/tool identity, executable fingerprint, exact source and Git
scope, environment, times, results, skips, limitations, declared effects, and
detected repository mutations. Mutation comparison is observation after
execution, not sandbox isolation. The read-only harness check only validates
this evidence and never executes project hooks or writes evidence.

An agent is a constrained task mode. A skill packages a repeated method and
selectively loaded references. A workflow is a versioned state machine whose
transitions invoke policy checks and produce evidence. A tool record separates
availability from allowed operations. An extension adds domain data and
findings through a stable interface:

```python
def validate(context: ValidationContext) -> list[Finding]:
    ...
```

The Git and hosted-change catalogs are ordered, closed, and fail unknown
operations. Every operation declares one or more effects from
`read_only_observation`, `local_reference_mutation`,
`working_tree_or_index_mutation`, `repository_history_mutation`,
`network_access`, `external_publication`, and `destructive_recovery`; its
authority class; whether it is a normal workflow step; and exact safeguards.
Authority classes are `allowed`, `task_scoped`,
`explicit_current_authorization`, `separate_release_authorization`,
`exceptional_current_authorization`, `destructive_current_authorization`, and
`prohibited`.

Composite `pull` is not modeled as harmless. Raw force-push is prohibited.
Exceptional history replacement is force-with-lease only, exact-ref scoped,
currently authorized, and confined to a non-default short-lived branch.
Release tags require separate release authority. Branch and worktree deletion
require safe-state evidence. Destructive recovery is never a normal workflow
step, and every workflow operation reference must resolve to the catalog.

For concurrent work in any profile, require a shared revision base, declared
write ownership, handback contract, deterministic conflict detection,
cancellation behavior, and partial-result rules. High Assurance may
additionally require a task lease and expiry when the project risk assessment
justifies mechanical coordination.

A coordination lease is not authority to edit. It only prevents two
authorized workers from silently claiming the same write scope. Lease
acquisition, renewal, expiry, cancellation, and handback are validated state
transitions, and abandoned partial results remain discoverable.

Imported capability packages record upstream source, exact version and
immutable source fingerprint, license, adopted files, local changes,
exclusions, security review, trust class, and update strategy. Mutable network
content is never loaded as instruction.

Capability and schema deprecations name both the first deprecated version and
the planned removal version. Removal requires a successor, migration fixture,
and evidence that no live references remain. Capability deprecation and
removal use the harness-kernel release axis; the capability package's own
version remains separate provenance.

## 10. Validation contract

Validation layers are:

1. bootstrap and runtime availability;
2. selected-profile operational-file inventory, syntax, and duplicate-key
   rejection;
3. schema version, ID, path, link, successor, dependency integrity, reciprocal
   plan/task links, and dependency-gated readiness;
4. instruction scope and authority classification;
5. policy, secret, network, filesystem, and external-effect rules;
6. lifecycle and closure evidence;
7. project extensions and project build/test/lint checks;
8. generated manifest, fingerprint, checksum scope, and freshness;
9. positive and negative/mutation tests; and
10. recovery from stale reports, corrupted records, and interrupted refresh.

The validator is modular even when distributed as one standard-library file.
Kernel, instruction, record, lifecycle, dossier, extension, integrity, and
project-command checks have separate interfaces and return structured
findings. A failure in one module must not silently disable unrelated checks.

The command contract is:

```text
python -B .agent/scripts/validate.py --check
python -B .agent/scripts/validate.py --ready-frontier
python -B -m unittest discover -s .agent/tests -p "test_*.py"
python -B .agent/scripts/refresh.py --refresh
```

Here `python` is the pinned Python 3.11+ interpreter selected by the project
environment, not an arbitrary ambient executable. The reference CI provisions
that launcher on every supported operating system. A project that uses another
launcher or runtime must adopt and validate an equivalent command contract
rather than editing only the displayed strings.

Projects may expose aliases such as `make harness-check`, but the authoritative
commands live in `.agent/validators.json`.

After project owners assess every hook and confirm authority for its declared
effects, configured target-project checks run only through the separately
explicit writer:

```text
python -B .agent/scripts/run_project_checks.py --write-evidence
```

The optional `--verify-adoption` mode also performs the explicit refresh write
and final read-only check. A configured hook declaring repository writes or
possible external effects additionally requires `--acknowledge-side-effects`;
that acknowledgement is not permission.

`check` must not write bytecode, caches, reports, indexes, timestamps, or
lockfiles or execute target-project hooks. It snapshots repository paths and
content before and after extension execution and fails if mutation is detected;
high-impact projects also enforce no-write execution outside the repository
trust boundary.
The source fingerprint excludes `.git`, whose internal metadata is not project
source. The mutation snapshot separately covers the `.git` pointer plus
critical HEAD, index, config, packed-ref, loose-ref, and hook paths for normal
repositories and linked worktrees; it is not a complete Git-object audit.
Every Git probe runs with `GIT_OPTIONAL_LOCKS=0`; this reduces incidental index
refreshes but does not turn Git or an untrusted extension into a sandbox.
`refresh` validates authoritative sources first, transactionally regenerates
the artifact catalog, path authority, manifest, and profile-specific integrity
outputs, and then runs the final read-only check.

High-Assurance generated validation reports are explicitly scoped to the
pre-refresh checks they record. Their closed contract contains one result for
each required check, failures, skips, environment and Git scope, external
effects, freshness rule, and limitations. A disabled extension is `not_run`,
never `pass`. The refresh command's final exit status reports the separate
post-refresh exact-tree check; neither result implies project readiness.

The portable reference validator uses only Python 3.11+ standard-library
features and validates strict JSON with duplicate-key rejection. JSON is the
canonical structured format in the domain-neutral kernel because its complete
grammar can be validated without borrowing another repository's environment.
An alternate validator is conforming only when it consumes the same schemas,
passes every valid/invalid/mutation/recovery fixture, preserves read-only and
redaction behavior, and records its runtime and version in
`.agent/validators.json`. An extension may use YAML only when it declares a
pinned parser, validates in a clean bootstrap, and converts findings through
the kernel extension interface.

Built-in secret detection combines named-assignment patterns for JSON, YAML,
dotenv, and common source syntax with high-confidence credential formats. It
scans UTF-8 text files up to its declared 4 MiB limit across tracked,
untracked, ignored, and generated paths, reports only locations/categories,
and never echoes candidate values. Binary, larger, encoded, or deliberately
obfuscated material requires an independently configured dedicated scanner in
CI when risk warrants. Heuristics are defense in depth, not proof that a
repository is secret-free.

Generated reports include tool and schema versions, source revision or content
fingerprint, dirty/untracked/ignored scope, time, environment, checks
performed, result, limitations, task/decision links, and freshness rule.
Checksums prove byte identity only—not authority, correctness, safety,
freshness, provenance, or legal rights.

## 11. Profiles

### Minimal viable

Use for small, early, or low-risk projects. Required:

- root router and seven-file kernel;
- decision and task stores plus templates;
- compact current state and resumption page;
- portable read-only validator;
- unassessed target-project hook contracts and a separately explicit evidence
  writer;
- the full provider-neutral small-team Git workflow portfolio and unassessed
  collaboration profile;
- project-local derivative source plus refresh command;
- valid and invalid fixtures with mutation tests; and
- dossier minimal profile.

The validator requires these operational entry points to remain present; a
project may extend them but cannot silently delete them and retain Minimal
conformance.

Exit only when discovery and precedence are clear, analysis versus
implementation authority is explicit, a task lifecycle can be validated, a
forbidden policy mutation fails, and validation runs without an undeclared
environment.

### Standard

Use when structured traceability, durable review evidence, project extensions,
or comparable coordination risks justify it. Add:

- evidence and review stores/templates;
- meaningful transition events;
- optional artifact registry;
- extension registry and project validator interface;
- disabled, unassessed operations/observability and security/supply-chain
  extension packages for deliberate project adoption;
- task-closure checklist; and
- structured dossier traceability, dependency readiness, ready-frontier
  derivation, and evidence.

The extension registry, both production-control extension entry points, and
Standard operational stores remain required even when disabled, empty, or
unadopted, so absence cannot silently disable their assessment.

Exit when an unfamiliar maintainer can execute, validate, review, hand off,
and resume a real task without undocumented steps.

### High assurance or agent-operable

Use when sensitive data, material external effects, protected enforcement,
long-lived agent operation, role separation, or audit/reproducibility needs
justify it. Add:

- constrained reviewer agent, routed review skill, and safe-change workflow;
- checkpoints and generated integrity;
- explicit refresh/check separation and content fingerprints;
- stronger dossier governance, transition, history, and supersession;
- conditional approval-attestation, coordination-lease, data-handling,
  incident/recovery, evaluation, and metrics contracts;
- CI/mutation/recovery guidance; and
- environment-specific approval and enforcement hooks.

Before the profile can be represented as adopted, every conditional and
optional artifact trigger must be assessed. Applicable controls require an
owner, active reviewed representation, and current resolving evidence;
`not_applicable` requires a dated, attributed rationale. The generated
production-control extensions remain disabled and unassessed until separately
adopted and trusted, and qualified security, privacy, compliance, legal, and
production conclusions remain outside automatic validation.

The governed capability and assurance-store entry points remain required.
Generated capability baselines may be deprecated or superseded through their
validated lifecycle, but must not simply disappear with their provenance and
dependency records.

The profile does not by itself create high assurance. Independent controls,
adoption decisions, project extensions, and demonstrated acceptance criteria
are still required.

All three profiles support `solo_direct`, `solo_hybrid`, `pair_pr`, `tiny_pr`,
and the `concurrent_work` modifier. Human count alone never selects Standard or
High Assurance, and concurrency alone does not require a coordination lease.

## 12. Adoption and evolution

### Initial adoption

1. Inventory use cases, protected resources, data classes, and unacceptable
   effects.
2. Identify actual sandbox, Git, CI, secret, cloud, and human enforcement
   boundaries.
3. Choose read-only, per-task mutation, or standing reversible local posture.
4. Assess collaboration from project-owned, fresh, privacy-minimized evidence;
   derive the team band and recommendation without granting permission. Adopt
   a supported workflow only through a separate accepted project decision.
5. Preview and generate the smallest risk-justified profile.
6. Inspect the target repository and resolve every template sentinel from
   evidence or mark it explicitly not applicable with a reason.
7. Record the threat model and authority posture as a project decision;
   never ship the example ID as accepted fact.
8. Assess every project command; configure applicable hooks with direct argv,
   owners, freshness, version probes, and declared effects, or record an owned
   `not_applicable` rationale.
9. Assess extension needs and ownership. Operations/observability and
   security/supply-chain packages remain disabled until a project trust
   decision and project-owned records justify deliberate adoption.
10. Assess conditional approval, coordination, data, recovery, evaluation, and
   metric triggers; record every omission with a reason and every applicable
   High-Assurance control with current evidence.
11. Run the read-only check and mutation tests in a disposable clean
    checkout/worktree; run configured project hooks only through the explicit
    evidence writer after confirming authority for declared effects.
12. Complete one real task through closure and handoff using the adopted
    small-team workflow and its concurrency modifier when applicable.
13. Enable external or high-impact paths only through trusted current
    authorization and independent enforcement.

### Evolution

- Every structured file declares a schema version.
- Compatible additions increment the compatible version; breaking changes
  require a new major version, migration, fixtures, and transition window.
- Accepted policy changes use successor decisions.
- Extensions declare core compatibility and deprecation fields.
- Generated projects upgrade through a project-specific migration; the
  blueprint never overwrites them.
- Remove redundant summaries and expired exceptions.
- Track useful outcome measures such as time-to-orientation, time-to-resume,
  invalid-transition rejection, stale-evidence detection, closure rework,
  exception age, and false-positive/false-negative findings. Metrics describe
  harness performance and never become readiness approval.

Recommended cadence:

- per change: affected schemas, references, lifecycle, and extensions;
- weekly during active work: current-state compaction and stale tasks;
- monthly: policy exceptions, dependencies, evidence age, and summary size;
- quarterly: clean bootstrap, mutation suite, recovery, and authority review;
- per release: exact fingerprint, limitations, and final read-only check.

## 13. Common failure modes

| Failure | Required response |
|---|---|
| documentation becomes permission | classify trust and allow permission only from declared channels |
| installed tool becomes authority | separate availability, permission, and enforcement |
| passing report is treated as current forever | bind it to fingerprints and freshness rules |
| validator borrows an ambient runtime | pin/bootstrap the supported toolchain |
| domain constants enter the kernel | move them to a registered extension |
| status is copied across files | assign one owner and generate views |
| summaries become histories | compact current state and retain durable records |
| checksums are treated as truth | state their byte-integrity limitation |
| role names become principals | inherit and narrow task authority |
| child instructions weaken root | validate root-to-leaf compatibility |
| check writes caches or reports | suppress writes and test an unchanged tree |
| repository validates its own trust root | add protected independent CI where risk warrants |
| old harnesses look live | archive, banner, and test discovery |
| ceremony exceeds value | require every artifact to mitigate a named risk |

## 14. Acceptance criteria

A harness is complete only when these demonstrations pass:

1. A newcomer discovers instructions, current work, and closure command without
   oral context.
2. A nested-path fixture applies root and child rules and rejects weakening.
3. Review-only work cannot mutate, and local implementation cannot publish.
4. Valid task transitions and dependency-ready progressions pass; cycles,
   incomplete predecessor execution, unresolved gates/blockers, broken
   reciprocal plan links, and invalid transitions fail clearly.
5. Each critical deny has a failing mutation.
6. A clean checkout runs the documented runtime and check.
7. Read-only validation leaves no tracked, untracked, ignored, cache, or
   timestamp change and never executes a target-project hook; the explicit
   project-check writer records truthful, fingerprint-bound outcomes and
   distinguishes failure, unavailable, skipped, and not-applicable states.
8. Managed-source changes invalidate stale generated evidence.
9. Synthetic credentials are detected and output is redacted.
10. A sample extension validates and can be disabled without kernel edits;
    both production-control extensions reject invalid, stale-evidence,
    broken-reference, and authority-expansion cases while remaining disabled
    and unassessed by default.
11. Another maintainer resumes interrupted work from compact state, task, and
    linked evidence within an agreed time.
12. Interrupted refresh and corrupted event recovery are exercised.
13. Harness and real project checks pass on the exact handed-off revision; an
    adopted High-Assurance harness has no unresolved conditional or optional
    trigger assessment.
14. Final reporting states scope, failures, skipped checks, limitations, dirty
    state, and external effects without overclaiming.
15. Fresh solo, pair, and tiny-team assessments select only the supported
    provider-neutral workflows; unknown, stale, conflicted, zero-writer, and
    over-five states fail safely; concurrency does not change human count;
    every workflow operation resolves; and enterprise workflow identifiers are
    absent or rejected.

Passing these criteria proves the harness is usable and testable. It does not
prove production safety, security, accessibility, legal compliance,
organizational approval, or suitability for every project.

Acceptance has two explicit gates:

| Gate | Criteria | Required evidence |
|---|---|---|
| Blueprint release automation | 2, 4–10, 12, and 15, plus structural portions of 1, 3, and 14 | cross-profile valid/invalid fixtures, collaboration and workflow matrices, operation-reference coverage, unchanged-tree checks, stale/partial refresh recovery, extension confinement, secret redaction |
| Target-project adoption | human portions of 1 and 3, plus 11, 13, and 14 | timed unfamiliar-maintainer exercise, actual platform enforcement, one real task/closure, exact project revision checks, truthful handoff report |

The release suite reports every criterion as `automated_pass`,
`project_demonstration_required`, or `not_exercised`; it may not summarize a
partial matrix as complete acceptance.

## 15. Evidence crosswalk

| Reusable concern | Reference evidence | Blueprint treatment |
|---|---|---|
| Root instruction routing and local policy | **Observed — both** | Short root router plus root-to-leaf nested instruction validation |
| Deny-by-default action policy | **Observed — Commerce Foundry** | Core `policy.json`; declarative and explicitly non-authorizing |
| Typed records and lifecycle control | **Observed — both** | Stable four-digit IDs, schema validation, legal transitions, and closure gates |
| Path authority and canonical-source classification | **Observed — COE** | Dossier artifact catalog and generated path-authority mirror |
| Executable validation and mutation tests | **Observed — Commerce Foundry** | `CF:scripts/validate-local.sh`, `CF:scripts/strict_yaml.py`, and `CF:tests/test_strict_yaml.py` inform the portable validator and adversarial fixtures |
| Manifest, checksum, and generated evidence | **Observed — COE** | Transactional refresh with shared generation ID and freshness fingerprint |
| Domain-specific registries and policies | **Observed — both** | Restrictions-only extension API; never kernel constants |
| Extension compatibility and disable behavior | **Recommendation** | Versioned registry, confined paths, validator protocol, and disable test |
| Clean-runtime portability | **Inference** | Strict JSON contracts, Python reference implementation, alternate-runtime conformance suite, CI runtime matrix |

## 16. Implementation and adoption checklist

1. Select a coverage profile from named coordination, risk, and assurance
   triggers.
2. Generate only into a nonexistent or empty directory; use the read-only
   adoption planner for an existing project.
3. Inspect `.project-blueprint-origin.json`, the artifact catalog, and all
   proposed or unassessed sentinels.
4. Read applicable project instructions and classify real authority sources.
5. Record fresh aggregate collaboration evidence, derive the team band, and
   adopt a supported workflow through an accepted project decision; do not
   treat the assessment or decision as operation authority.
6. Adopt project scope, commands, owners, and extension needs through accepted
   project decisions; generation supplies none of them.
7. Populate intended state, dated current state, findings, plan, risks,
   provenance, evidence, and handoff without collapsing their information
   states.
8. Build hard plan/task dependency graphs, reciprocal plan/task links,
   structured gates and blockers, then derive the ready frontier before
   selecting planned work. Use valid direction rather than dates to choose
   among independent ready items.
9. Register every dossier representation in the project-local artifact source;
   run refresh to derive catalog, path authority, and integrity outputs.
10. Run the read-only validator and its mutation/recovery tests.
11. Demonstrate one real dependency-gated task lifecycle through the adopted
    Git workflow and a safe handoff.
12. Record conditional trigger decisions, remaining unknowns, and limits; do
    not translate structural success
    into a readiness claim.

## 17. Automatically validated baseline and project-owned obligations

| Release automation validates | The target project must still decide or prove |
|---|---|
| syntax, duplicate keys, kernel/record schemas, schema-kind agreement, IDs, links, legal transitions, dependency cycles/readiness, and reciprocal plan/task links for declared stores | actual project facts, owners, requirements, acceptance criteria, and priority among independent ready items |
| closed collaboration bands, workflow mappings, freshness/conflict failures, review-capacity caps, operation references, and enterprise exclusions | actual maintainer topology, reviewer availability, workflow adoption, hosted settings, and permission for any Git or provider action |
| structured instruction and extension rules cannot declare authority expansion; prohibited mutations fail fixtures | who may authorize specific actions and whether the execution platform actually enforces the boundary |
| the core check writes nothing and executes no project hook; explicit project-check evidence is schema-valid, fingerprint-bound, and fresh; extension or hook mutation is detected after execution | whether configured commands and extension code are authorized and trustworthy, and whether an external sandbox or no-write boundary is required |
| project-local artifact source, derived catalog/path roles, traceability structure, and integrity metadata cohere | whether requirements are correct and evidence is substantively sufficient |
| extension compatibility, path confinement, typed validator response, unique IDs, trust declaration, disable behavior, and strict operations/security production-control record contracts | which domain extensions and controls apply, whether referenced external systems or reviewers actually exist, and who maintains or approves them |
| generated evidence is fresh for its declared byte scope | implementation quality, safety, compliance, legal rights, or release readiness |

The universal claim ends at this boundary: the kernel, contracts, validators,
profiles, and extension points are domain-neutral; project content,
enforcement integrations, risk decisions, and readiness conclusions are
necessarily project-specific.
