# Project Agent Harness Blueprint

## 1. Purpose

A project agent harness is the repository-local operating system for safe,
resumable work by humans and agents. It routes instruction discovery, states
authority boundaries, defines record and lifecycle contracts, exposes
validation commands, and preserves evidence.

Its universal scope is a stable domain-neutral kernel with validated extension
points, not a claim that one project's policies or domain rules fit another.

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
| `.agent/project.json` | stable project profile and project command hooks |

`project.json` must not become a second status report. Mutable work status
belongs in tasks and `.agent/state/current.json`.

### Layer 3: capability packages

`.agents/agents/`, `.agents/skills/`, and `.agents/workflows/` define
specialist modes and reusable procedures. Each capability inherits the active
task's authority, may narrow it, and may never expand it.

Capability packages are conditional. Do not add named agents or skills until
a recurring job, quality boundary, or role-separation need justifies them.

### Layer 4: project profile and extensions

`.agent/project.json` declares stable repository facts and command hooks.
`.agent/extensions/` owns domain registries, build or release rules, and
project-specific validators.

An extension:

- declares a stable ID, schema version, compatibility range, owner, provenance,
  config, validator, side effects, and deprecation path;
- returns structured findings through the kernel interface;
- can add restrictions and checks;
- cannot weaken the kernel or grant authority; and
- can be disabled without changing kernel behavior.

### Layer 5: operational records and evidence

Tasks, decisions, evidence, reviews, events, artifacts, state, checkpoints,
and generated integrity make work resumable and auditable.

## 4. Architectural invariants

1. Higher-level instructions cannot be weakened by lower-level files.
2. A capability or extension cannot grant itself access.
3. Generated content is labeled derived, non-authoritative, and point-in-time.
4. `check` is read-only; `refresh` is the explicit writer.
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
│   ├── schemas/                       # local versioned schema snapshot
│   ├── decisions/
│   ├── tasks/
│   ├── evidence/                     # standard+
│   ├── reviews/                      # standard+
│   ├── events/                       # standard+
│   ├── artifacts/                    # standard, when durable outputs matter
│   ├── extensions/                   # standard+
│   ├── checkpoints/                  # high-assurance
│   ├── state/
│   │   ├── current.json
│   │   └── RESUME.md
│   ├── templates/
│   ├── generated/                    # high-assurance, derived only
│   ├── scripts/
│   │   ├── validate.py
│   │   └── refresh.py                # high-assurance
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
7. inspect executable/configured reality and fresh evidence;
8. load intended target and plans only as context; and
9. record material conflicts instead of choosing silently.

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

## 8. Record and state model

| Concern | Store | Mutability | Meaning |
|---|---|---|---|
| durable intent | `decisions/` | immutable plus successor | why a lasting choice exists |
| active work | `tasks/` | lifecycle updates | what is being done |
| observation | `evidence/` | immutable record | what was inspected or executed |
| review finding | `reviews/` | disposition updates | what a separate pass found |
| chronology | `events/` | append-only | meaningful transitions |
| current view | `state/current.json` | compact derived view | what to resume now |
| artifact metadata | `artifacts/registry.json` | lifecycle updates | provenance and promotion |
| generated integrity | `generated/` | regenerated | point-in-time inventory and results |

Each record declares `schema_version`, stable ID, purpose/title, scope,
authority source, owner/maintainer, inputs, outputs or links, side effects,
status, timestamps as applicable, validation, limitations, provenance, and
successor/deprecation fields where applicable.

### Task lifecycle

```text
proposed → ready → in_progress → validating → review → completed
                       ├──────────────→ blocked
                       └──────────────→ cancelled
completed → reopened
```

- `ready` requires scope, authority basis, acceptance criteria, and validation
  plan.
- `in_progress` requires an owner.
- `validating` requires an implementation or analysis result.
- `review` requires evidence or an explicit limitation.
- `completed` requires satisfied criteria, closure evidence, and disclosure of
  external effects and limitations.
- `blocked` names the missing fact or authority.
- `reopened` links the evidence that invalidated completion.

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

An agent is a constrained task mode. A skill packages a repeated method and
selectively loaded references. A workflow is a versioned state machine whose
transitions invoke policy checks and produce evidence. A tool record separates
availability from allowed operations. An extension adds domain data and
findings through a stable interface:

```python
def validate(context: ValidationContext) -> list[Finding]:
    ...
```

For concurrent agents, additionally require a task lease and expiry, shared
revision base, declared write ownership, handback contract, deterministic
conflict detection, cancellation behavior, and partial-result rules.

Imported capability packages record upstream source and exact version, license,
adopted files, local changes, exclusions, security review, trust class, and
update strategy. Mutable network content is never loaded as instruction.

## 10. Validation contract

Validation layers are:

1. bootstrap and runtime availability;
2. syntax and duplicate-key rejection;
3. schema version, ID, path, link, successor, and dependency integrity;
4. instruction scope and authority classification;
5. policy, secret, network, filesystem, and external-effect rules;
6. lifecycle and closure evidence;
7. project extensions and project build/test/lint checks;
8. generated manifest, fingerprint, checksum scope, and freshness;
9. positive and negative/mutation tests; and
10. recovery from stale reports, corrupted records, and interrupted refresh.

The command contract is:

```text
python3 -B .agent/scripts/validate.py --check
python3 -B -m unittest discover -s .agent/tests -p 'test_*.py'
python3 -B .agent/scripts/refresh.py --refresh       # high-assurance only
```

Projects may expose aliases such as `make harness-check`, but the authoritative
commands live in `.agent/validators.json`.

`check` must not write bytecode, caches, reports, indexes, timestamps, or
lockfiles. `refresh` validates sources first, writes derived files atomically,
and instructs the operator to run the final read-only check.

The portable scaffold validator uses only Python 3.11+ standard-library
features and validates strict JSON with duplicate-key rejection. JSON is the
canonical structured format in the domain-neutral kernel because its complete
grammar can be validated without borrowing another repository's environment.
An extension may use YAML only when it declares a pinned parser, validates in a
clean bootstrap, and converts findings through the kernel extension interface.

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
- valid and invalid fixtures with mutation tests; and
- dossier minimal profile.

Exit only when discovery and precedence are clear, analysis versus
implementation authority is explicit, a task lifecycle can be validated, a
forbidden policy mutation fails, and validation runs without an undeclared
environment.

### Standard

Use by default for active multi-contributor projects or monorepos. Add:

- evidence and review stores/templates;
- meaningful transition events;
- optional artifact registry;
- extension registry and project validator interface;
- task-closure checklist; and
- structured dossier traceability and evidence.

Exit when an unfamiliar maintainer can execute, validate, review, hand off,
and resume a real task without undocumented steps.

### High assurance or agent-operable

Use when agents operate across sessions, concurrent work or sensitive data is
possible, external effects exist, or audit/reproducibility matters. Add:

- constrained reviewer agent, routed review skill, and safe-change workflow;
- checkpoints and generated integrity;
- explicit refresh/check separation and content fingerprints;
- stronger dossier governance, transition, history, and supersession;
- CI/mutation/recovery guidance; and
- environment-specific approval and enforcement hooks.

The profile does not by itself create high assurance. Independent controls,
adoption decisions, project extensions, and demonstrated acceptance criteria
are still required.

## 12. Adoption and evolution

### Initial adoption

1. Inventory use cases, protected resources, data classes, and unacceptable
   effects.
2. Identify actual sandbox, Git, CI, secret, cloud, and human enforcement
   boundaries.
3. Choose read-only, per-task mutation, or standing reversible local posture.
4. Preview and generate the smallest justified profile.
5. Inspect the target repository and resolve every template sentinel from
   evidence or mark it explicitly not applicable with a reason.
6. Record the threat model and authority posture as the first project decision;
   never ship the example ID as accepted fact.
7. Configure project commands and extension ownership.
8. Run check and tests in a disposable clean checkout/worktree.
9. Complete one real task through closure and handoff.
10. Enable external or high-impact paths only through trusted current
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
4. Valid task transitions pass and invalid transitions fail clearly.
5. Each critical deny has a failing mutation.
6. A clean checkout runs the documented runtime and check.
7. Read-only validation leaves no tracked, untracked, ignored, cache, or
   timestamp change.
8. Managed-source changes invalidate stale generated evidence.
9. Synthetic credentials are detected and output is redacted.
10. A sample extension validates and can be disabled without kernel edits.
11. Another maintainer resumes interrupted work from compact state, task, and
    linked evidence within an agreed time.
12. Interrupted refresh and corrupted event recovery are exercised.
13. Harness and real project checks pass on the exact handed-off revision.
14. Final reporting states scope, failures, skipped checks, limitations, dirty
    state, and external effects without overclaiming.

Passing these criteria proves the harness is usable and testable. It does not
prove production safety, security, accessibility, legal compliance,
organizational approval, or suitability for every project.

## 15. Evidence crosswalk

| Reusable concern | Reference evidence | Blueprint treatment |
|---|---|---|
| Root instruction routing and local policy | **Observed — both** | Short root router plus root-to-leaf nested instruction validation |
| Deny-by-default action policy | **Observed — Commerce Foundry** | Core `policy.json`; declarative and explicitly non-authorizing |
| Typed records and lifecycle control | **Observed — both** | Stable four-digit IDs, schema validation, legal transitions, and closure gates |
| Path authority and canonical-source classification | **Observed — COE** | Dossier artifact catalog and generated path-authority mirror |
| Executable validation and mutation tests | **Observed — Commerce Foundry** | Portable read-only validator plus adversarial fixtures |
| Manifest, checksum, and generated evidence | **Observed — COE** | Transactional refresh with shared generation ID and freshness fingerprint |
| Domain-specific registries and policies | **Observed — both** | Restrictions-only extension API; never kernel constants |
| Extension compatibility and disable behavior | **Recommendation** | Versioned registry, confined paths, validator protocol, and disable test |
| Clean-runtime portability | **Inference** | Python 3.11+ standard library, strict JSON, CI runtime matrix |

## 16. Implementation and adoption checklist

1. Select a coverage profile from named coordination, risk, and assurance
   triggers.
2. Generate only into a nonexistent or empty directory; use the read-only
   adoption planner for an existing project.
3. Inspect `.project-blueprint-origin.json`, the artifact catalog, and all
   proposed or unassessed sentinels.
4. Read applicable project instructions and classify real authority sources.
5. Adopt project scope, commands, owners, and extension needs through accepted
   project decisions; generation supplies none of them.
6. Populate intended state, dated current state, findings, plan, risks,
   provenance, evidence, and handoff without collapsing their information
   states.
7. Run the read-only validator and its mutation tests.
8. For high assurance, run refresh, then rerun the final read-only check.
9. Demonstrate one real task lifecycle and a safe handoff.
10. Record remaining unknowns and limits; do not translate structural success
    into a readiness claim.

## 17. Validated guarantees and project-owned obligations

| The generated kernel validates | The target project must still decide or prove |
|---|---|
| syntax, duplicate keys, schema versions, IDs, links, and legal transitions | actual project facts, owners, requirements, and acceptance criteria |
| authority cannot be expanded by nested instructions or extensions | who may authorize specific local or external actions |
| check mode is read-only and refresh outputs are mutually consistent | whether configured commands and environments are appropriate |
| dossier path roles, traceability structure, and integrity metadata cohere | whether requirements are correct and evidence is substantively sufficient |
| extension compatibility, confinement, validator response, and disable behavior | which domain extensions are needed and who maintains them |
| generated evidence is fresh for its declared byte scope | implementation quality, safety, compliance, legal rights, or release readiness |

The universal claim ends at this boundary: the kernel, contracts, validators,
profiles, and extension points are domain-neutral; project content,
enforcement integrations, risk decisions, and readiness conclusions are
necessarily project-specific.
