# Universal Project Dossier Blueprint

Blueprint version: 1.0.0
Reference-analysis date: 2026-07-27

This document defines a domain-neutral project dossier for software, product,
business, brand, research, operational, and hybrid initiatives. It is complete
enough to create, audit, maintain, or resume a dossier without consulting the
reference repositories.

Evidence labels:

- **[Observed: CF]** Present in the Commerce Foundry reference.
- **[Observed: COE]** Present in the Cooper Online Enterprises reference.
- **[Observed: both]** Present in both references.
- **[Inferred]** Generalized from multiple observations.
- **[Recommended]** Introduced by this blueprint to close a reusable gap.

Reference paths use `CF:<path>` and `COE:<path>`. They are repository-relative;
no source-machine path is transferred to generated projects.

## 1. Executive summary

A project dossier is the maintained information system that explains what a
project is, what it is not, what outcome is intended, what currently exists,
why durable choices were made, what work remains, which constraints and gates
apply, what evidence supports a claim, and how work can resume safely.

The dossier is documentation. It does not grant permission, activate a plan,
approve a release, or prove implementation merely by describing it.

Primary audiences:

- project owners and decision-makers;
- implementers, operators, researchers, and reviewers;
- governance, security, privacy, legal, finance, and compliance specialists
  when their trigger applies;
- new maintainers receiving a handoff; and
- agents that need bounded, progressively disclosed context.

An effective dossier is:

- authoritative about where truth lives, not necessarily the sole container
  for every source;
- explicit about intended, observed, proposed, generated, and historical
  information states;
- traceable from source through requirement, evidence, finding, plan, and gate;
- maintainable because one artifact owns each mutable concern;
- progressively disclosed so orientation does not require loading history;
- versioned and supersession-aware;
- machine-readable where automation consumes the data;
- evidence-bounded and honest about freshness and limitations; and
- resumable by someone without oral context.

For humans, it prevents rediscovery, undocumented assumptions, conflicting
summaries, and unsafe handoff. For agents, it prevents authority laundering,
status inference, context overload, stale-evidence reliance, and loss of work
state across sessions.

## 2. Design principles

### 2.1 One owner per concern

**[Observed: both] [Recommended]** Assign one authoritative source to each
mutable fact. Summaries and generated views link to it; they do not redefine
it.

### 2.2 Authority is explicit and non-transitive

**[Observed: both]** A canonical document may define intended state without
granting permission to implement it. A plan may be correct without being
authorized. A passing report may be evidence without being approval.

Every entry point states its information role and authority limitation.

### 2.3 Separate information states

Keep these states distinct even when a Minimal profile combines them:

1. dossier interpretation and authority;
2. canonical intended state;
3. current observed state;
4. conformance assessment;
5. implementation or delivery plan;
6. risks, assumptions, issues, dependencies, and questions;
7. decisions;
8. source provenance;
9. validation and evidence;
10. handoff and resumption;
11. superseded or historical material; and
12. generated views.

### 2.4 Evidence is scoped, dated, and reproducible

Current-state and readiness claims identify subject version, observation time,
method, environment, result, and limitations. Stale evidence never overrides a
newer direct observation.

### 2.5 Provenance survives transformation

Every consequential source records identity, version or retrieval date,
classification, intended use, sensitivity, limitations, and freshness rule.
Derived artifacts link their source records.

### 2.6 Versioning and supersession preserve history

Accepted evidence and durable decisions are immutable or corrected with a
successor. A supersession record names the old artifact, replacement,
effective date, reason, migration impact, and retained-history location.

### 2.7 Progressive disclosure controls context

The dossier index and handoff pack stay compact. Readers load canonical,
current-state, plan, specialist models, evidence, or history only when the
task requires them. Large transcripts and historical narratives never
accumulate in the entry point.

### 2.8 Machine-readable mirrors have declared ownership

Each mirror states whether it is authoritative, generated from a human source,
or the source from which a human view is generated. Two independently edited
representations may not both claim authority.

### 2.9 Unknown is a valid state

Use `unknown`, `not_assessed`, `not_applicable`, and `gated` rather than
inventing facts or interpreting absence as failure.

## 3. Reference-dossier crosswalk

The references share a common information architecture but emphasize
different risks. CF contains a broad product/engineering dossier and a later
canonical v0.2 handoff. COE contains a more explicit authority, current-state,
conformance, plan, provenance, and integrity separation.

| Artifact family | Commerce Foundry evidence | COE evidence | Generalized interpretation |
|---|---|---|---|
| Entry and navigation | `CF:project-dossier/v0.2/README.md`; `CF:project-dossier/v0.2/HANDOFF_MANIFEST.md` | `COE:project-dossier/README.md`; `COE:project-dossier/handoff/START_HERE.md` | Compact index and resumable entry point |
| Authority and canonical map | `CF:project-dossier/v0.2/CANONICAL_SOURCE_MAP.md` | `COE:project-dossier/AUTHORITY.md`; `COE:project-dossier/CANONICAL_SOURCE_MAP.md` | Explicit interpretation and source ownership |
| Version and supersession | `CF:project-dossier/v0.2/SUPERSESSION_MAP.md`; `CF:project-dossier/v0.2/baseline/README.md` | `COE:project-dossier/MANIFEST.json`; `COE:project-dossier/CHECKSUMS.sha256` | Lifecycle, provenance, and point-in-time integrity |
| Project definition | `CF:project-dossier/docs/product/problem-statement.md`; `goals-and-non-goals.md`; `vision.md` | `COE:project-dossier/canonical/executive-project-definition.md` | Identity, problem, scope, outcomes, success |
| Requirements | `CF:project-dossier/docs/requirements/`; `requirements-traceability.md` | `COE:project-dossier/canonical/requirements-and-constraints.md`; `machine-readable/requirements.yaml` | Stable requirement definitions and traceability |
| Architecture/outcome model | `CF:project-dossier/docs/architecture/`; `docs/workflows/`; `docs/schemas/` | `COE:project-dossier/canonical/technical-architecture.md`; `business-and-brand-architecture.md` | Domain-neutral actors, components, flows, interfaces, invariants |
| Decisions | `CF:project-dossier/docs/architecture/adr/`; live `CF:.agent/decisions/` | `COE:project-dossier/registers/decisions.yaml`; live `COE:.agent/decisions/` | Durable accepted intent, preferably owned once |
| Current state | `CF:project-dossier/PROJECT_STATUS.md`; `v0.2/agent-handoff/current-implementation-status.md` | `COE:project-dossier/current-state/` | Dated observation, not target or plan |
| Conformance | `CF:project-dossier/v0.2/conformance/` | `COE:project-dossier/conformance/findings.yaml`; `initial-assessment.md` | Requirement-to-evidence gap assessment |
| Planning | `CF:project-dossier/docs/roadmaps/`; `v0.2/implementation-plan/` | `COE:project-dossier/implementation-plan/`; `plan.yaml` | Dependency-aware future sequence |
| Registers | `CF:project-dossier/docs/risks/risk-register.md`; `docs/knowledge/` | `COE:project-dossier/registers/` | Risks, assumptions, issues, dependencies, questions |
| Provenance/research | `CF:project-dossier/docs/research/`; dated provider verification files | `COE:project-dossier/provenance/` | Source identity, external-fact freshness, limitations |
| Validation/evidence | `CF:project-dossier/docs/testing/`; `evidence/` | `COE:project-dossier/validation/`; `COE:.agent/evidence/` | Reproducible checks and bounded evidence |
| Operations/recovery | `CF:project-dossier/docs/operations/` | Operational guidance distributed across COE plans and harness checklists | Conditional runbooks triggered by external effects |
| Machine-readable authority | YAML/JSON schemas and state machines under `CF:project-dossier/docs/` | `COE:project-dossier/machine-readable/path-authority.yaml` | Typed mirrors and path classification |

Direct equivalents include entry points, canonical requirements, current
state, plans, registers, validation, and handoff. Functional equivalents use
different structures for decisions, architecture, and evidence. CF uniquely
emphasizes detailed runtime, workflow, schema, and operations material. COE
uniquely emphasizes path-authority classification and generated integrity.

Apparent reference gaps that this blueprint closes:

- neither reference provides a portable universal artifact catalog schema;
- both need stronger automatic drift and freshness enforcement;
- both allow resumption summaries to grow;
- neither reference supplies a domain-neutral installation and migration
  package for arbitrary projects; and
- generated checksums in a repository-local trust boundary do not independently
  attest correctness or approval.

## 4. General artifact taxonomy

Classification:

- **Core** — expected in nearly every dossier.
- **Conditional** — required when a named trigger or risk is present.
- **Optional** — useful for complex coordination or higher assurance.

All artifacts use four-digit stable IDs. Record namespaces are globally unique
within the generated project.

### DOS-0001 — Dossier index

- Category/classification: navigation / Core
- Purpose: route readers through authoritative layers without restating them.
- Questions: Where do I start? What is current? Which profile applies?
- Audience/owner: everyone / dossier maintainer.
- Inputs: artifact catalog, authority map, current handoff pointers.
- Outputs: reading order and layer map.
- Format/authority: Markdown; navigation only.
- Dependencies: DOS-0002, DOS-0003, DOS-0004.
- Timing/cadence: create first; update when paths or entry points change.
- Validation: links resolve; current/high-profile directories are listed.
- Omit/combine: never omit; may combine with handoff only in a very small,
  single-session project if authority and current state remain distinct.
- Evidence: `CF:project-dossier/v0.2/README.md`;
  `COE:project-dossier/README.md`.

### DOS-0002 — Authority map

- Category/classification: governance / Core
- Purpose: define interpretation, precedence, information roles, and conflicts.
- Questions: Which source governs which concern? What cannot create permission?
- Audience/owner: all readers / project governance owner.
- Inputs: repository instructions, accepted decisions, source classifications.
- Outputs: authority rules consumed by navigation and validation.
- Format/authority: Markdown plus path-authority JSON; authoritative for dossier
  interpretation, never operating permission.
- Dependencies: DEC-0001, PRV-0001.
- Timing/cadence: create before content adoption; review on authority changes.
- Validation: every managed path classified; conflicts and historical material
  handled.
- Omit/combine: may combine with DOS-0003 in Minimal.
- Evidence: `COE:project-dossier/AUTHORITY.md`;
  `COE:project-dossier/machine-readable/path-authority.yaml`.

### DOS-0003 — Canonical-source map

- Category/classification: governance / Core
- Purpose: name the single owner for intended, current, plan, evidence, and
  lifecycle concerns.
- Questions: Where is the definition? Which mirrors are generated?
- Audience/owner: maintainers and agents / dossier maintainer.
- Inputs: artifact catalog and accepted ownership decisions.
- Outputs: source-of-truth lookup and change route.
- Format/authority: Markdown; authoritative for source ownership.
- Dependencies: DOS-0004, DEC-0001.
- Timing/cadence: create with first artifacts; update on ownership or path
  change.
- Validation: no concern has two independent authoritative owners.
- Omit/combine: may combine with DOS-0002 in Minimal.
- Evidence: `CF:project-dossier/v0.2/CANONICAL_SOURCE_MAP.md`;
  `COE:project-dossier/CANONICAL_SOURCE_MAP.md`.

### DOS-0004 — Artifact catalog

- Category/classification: inventory / Core
- Purpose: machine-readable inventory of artifact role, classification,
  ownership, cadence, sensitivity, and supersession.
- Questions: What belongs to the dossier? Who maintains it? Is it generated?
- Audience/owner: maintainers, validators, agents / dossier maintainer.
- Inputs: selected profile and project extensions.
- Outputs: navigation, path authority, drift checks, handoff.
- Format/authority: JSON; authoritative inventory metadata.
- Dependencies: DOS-0005, DOS-0006.
- Timing/cadence: generated initially; maintained on artifact/path changes.
- Validation: JSON Schema, unique IDs/paths, existing paths, full coverage.
- Omit/combine: never omit; Minimal may contain fewer entries.
- Evidence: inferred from both manifests; schema is a new recommendation.

### DOS-0005 — Generated manifest and integrity set

- Category/classification: generated / Core
- Purpose: point-in-time file inventory and fingerprints.
- Questions: Which bytes were checked? When? What scope was excluded?
- Audience/owner: reviewers and automation / refresh tool.
- Inputs: declared managed scope.
- Outputs: manifest, report, and optional checksums.
- Format/authority: JSON and checksum text; generated evidence only.
- Dependencies: DOS-0004, VAL-0001.
- Timing/cadence: refresh after managed changes and before handoff/release.
- Validation: exact scope, source fingerprint, generation ID, mutual
  consistency, freshness.
- Omit/combine: manifest required; checksums conditional on High Assurance.
- Evidence: `COE:project-dossier/MANIFEST.json`;
  `COE:project-dossier/CHECKSUMS.sha256`.

### DOS-0006 — Version and supersession ledger

- Category/classification: lifecycle / Core
- Purpose: identify dossier version and preserve replacement history.
- Questions: What is current? What changed? What does it supersede?
- Audience/owner: maintainers and auditors / dossier governance owner.
- Inputs: accepted changes and migration records.
- Outputs: semantic version, successor links, retained-history locations.
- Format/authority: Markdown version plus JSON ledger.
- Dependencies: DOS-0004, DEC-0001.
- Timing/cadence: create at initialization; update on semantic dossier change.
- Validation: no cycle, missing successor, or reused artifact ID.
- Omit/combine: version and empty supersession ledger remain Core.
- Evidence: `CF:project-dossier/v0.2/SUPERSESSION_MAP.md`; COE generated
  integrity and provenance.

### DEF-0001 — Executive project definition

- Category/classification: canonical target / Core
- Purpose: define identity, problem, outcomes, boundaries, audiences, ownership,
  and success.
- Questions: What is this project and explicitly not this project?
- Audience/owner: all stakeholders / project owner.
- Inputs: authoritative brief, accepted decisions, stakeholder evidence.
- Outputs: requirements, architecture/outcome model, success measures.
- Format/authority: Markdown; canonical target definition.
- Dependencies: PRV-0001, DEC-0001.
- Timing/cadence: early; review on strategy or scope change.
- Validation: scope is bounded; terms and measures are testable; unknowns named.
- Omit/combine: never omit; small projects may combine with REQ-0001 and
  ARC-0001.
- Evidence: CF product definition files; COE executive definition.

### REQ-0001 — Requirements and traceability

- Category/classification: canonical target / Core
- Purpose: own requirement wording, basis, status, owner, validation, and links.
- Questions: What must be true, why, and how will it be verified?
- Audience/owner: implementers, reviewers, owners / requirement owner.
- Inputs: definition, decisions, constraints, research, gates.
- Outputs: architecture, findings, plans, validation.
- Format/authority: Markdown plus authoritative JSON registry.
- Dependencies: DEF-0001, PRV-0001, DEC-0001.
- Timing/cadence: before conformance and planning; update through change control.
- Validation: stable IDs, basis, owner, method, evidence or remediation.
- Omit/combine: never omit; may combine prose with definition in Minimal.
- Evidence: both references' requirements and traceability material.

### ARC-0001 — Architecture or outcome model

- Category/classification: canonical target / Core
- Purpose: describe actors, components/workstreams, boundaries, flows,
  interfaces, states, and invariants.
- Questions: How should the intended system or outcome fit together?
- Audience/owner: implementers and reviewers / architecture or design owner.
- Inputs: definition, requirements, decisions, domain models.
- Outputs: plans, interfaces, validation criteria, operational models.
- Format/authority: Markdown, diagrams, and structured schemas where consumed.
- Dependencies: DEF-0001, REQ-0001, DEC-0001.
- Timing/cadence: before detailed implementation; update on accepted design
  changes.
- Validation: every component supports requirements; boundaries and failure
  behavior are explicit.
- Omit/combine: never omit; terminology becomes outcome/workstream model for
  non-software projects.
- Evidence: CF architecture/workflows/schemas; COE canonical architecture set.

### DEC-0001 — Decision records

- Category/classification: durable intent / Core
- Purpose: preserve why an accepted durable choice exists and its scope.
- Questions: What was decided, by whom/what authority, and what did it replace?
- Audience/owner: all future maintainers / decision owner.
- Inputs: alternatives, evidence, authority source.
- Outputs: canonical target, requirements, plans, supersession.
- Format/authority: Markdown records under `.agent/decisions/`; status-dependent.
- Dependencies: harness decision schema and lifecycle.
- Timing/cadence: when a durable choice is proposed or accepted.
- Validation: unique ID, valid status, authority source, successor semantics.
- Omit/combine: store is Core; no fabricated accepted record is generated.
- Evidence: both live `.agent/decisions/`; CF ADRs.

### GOV-0001 — Constraints, gates, and readiness criteria

- Category/classification: governance / Core
- Purpose: define non-functional constraints and objective gates.
- Questions: Which approvals, risks, evidence, and conditions block progression?
- Audience/owner: owners, reviewers, specialists / governance owner.
- Inputs: requirements, threat/risk analysis, specialist obligations.
- Outputs: plans, validation, handoff, release decisions.
- Format/authority: Markdown/JSON; canonical criteria, not approval.
- Dependencies: REQ-0001, REG-0001, VAL-0001.
- Timing/cadence: before gated work; review when risk or environment changes.
- Validation: gates have owner, inputs, pass criteria, evidence, expiry.
- Omit/combine: combine with requirements in Minimal; separate when any external
  or high-impact gate exists.
- Evidence: both references' approval/readiness checklists.

### CUR-0001 — Current-state baseline

- Category/classification: current state / Core
- Purpose: record dated, evidence-backed present reality.
- Questions: What exists, is absent, is unknown, or differs by environment?
- Audience/owner: all execution roles / current-state assessor.
- Inputs: direct inspection, commands, inventory, evidence.
- Outputs: findings, plans, handoff.
- Format/authority: Markdown and optional JSON; authoritative only for stated
  subject, time, and scope.
- Dependencies: VAL-0001, PRV-0001.
- Timing/cadence: initial assessment; refresh on material change or evidence
  expiry.
- Validation: date, subject fingerprint/version, method, environment,
  limitations, evidence links.
- Omit/combine: never omit.
- Evidence: both references' current-status and implementation assessments.

### CNF-0001 — Conformance and gap register

- Category/classification: conformance / Core
- Purpose: compare current evidence with canonical requirements.
- Questions: What conforms, is compatible, transitional, absent, or unassessed?
- Audience/owner: owners and implementers / assessor.
- Inputs: requirements, current state, evidence.
- Outputs: findings, remediation plans, readiness status.
- Format/authority: Markdown plus authoritative JSON findings.
- Dependencies: REQ-0001, CUR-0001, VAL-0001.
- Timing/cadence: after baseline; update when target or evidence changes.
- Validation: every finding links requirement and evidence; classifications are
  controlled.
- Omit/combine: never omit; an empty/not-assessed register is valid.
- Evidence: CF v0.2 conformance; COE conformance package.

### PLN-0001 — Dependency-aware plan

- Category/classification: planning / Core
- Purpose: define future work, dependencies, gates, owners, and acceptance.
- Questions: What remains, in what order, and what proves completion?
- Audience/owner: executors and owners / planning owner.
- Inputs: findings, requirements, registers, decisions, gates.
- Outputs: task intake, expected evidence, handoff priorities.
- Format/authority: Markdown plus authoritative JSON plan registry.
- Dependencies: CNF-0001, REG-0001, GOV-0001.
- Timing/cadence: after target/current comparison; update on dependency/status
  change.
- Validation: acyclic dependencies, valid refs, completion evidence.
- Omit/combine: plan entry point is Core; no accepted work is fabricated.
- Evidence: both references' roadmaps and implementation plans.

### REG-0001 — RAIDQ register

- Category/classification: unresolved state / Core
- Purpose: own risks, assumptions, issues, dependencies, and questions.
- Questions: What is uncertain, blocking, accepted, expired, or unresolved?
- Audience/owner: all roles / named item owners and register maintainer.
- Inputs: discovery, reviews, incidents, planning.
- Outputs: decisions, gates, plans, validation scope.
- Format/authority: Markdown plus authoritative JSON registry.
- Dependencies: PRV-0001, DEC-0001.
- Timing/cadence: create during discovery; review by item date and before gates.
- Validation: unique IDs, type/status, owner, impact, resolution condition.
- Omit/combine: never omit; empty register is valid.
- Evidence: both references' risk/open-question/knowledge stores.

### PRV-0001 — Source and provenance index

- Category/classification: provenance / Core
- Purpose: identify sources, versions, rights, sensitivity, freshness, and
  limitations.
- Questions: Where did this claim come from and may it still be relied upon?
- Audience/owner: all evidence consumers / source curator.
- Inputs: project records, external references, imported assets and methods.
- Outputs: requirements, decisions, research, evidence.
- Format/authority: Markdown plus authoritative JSON source index.
- Dependencies: DOS-0002.
- Timing/cadence: before consequential source use; refresh on expiry/version
  change.
- Validation: stable source ID, locator, observation date/version, use,
  limitations, sensitivity, rights/license where applicable.
- Omit/combine: never omit.
- Evidence: COE provenance package; CF dated provider research.

### VAL-0001 — Validation and evidence index

- Category/classification: evidence / Core
- Purpose: define validation commands and index bounded evidence.
- Questions: What was checked, on which subject, with what result and limits?
- Audience/owner: reviewers, operators, agents / validation owner.
- Inputs: requirements, gates, implementation/artifacts.
- Outputs: findings, readiness decisions, handoff.
- Format/authority: Markdown plus JSON evidence index and generated reports.
- Dependencies: REQ-0001, GOV-0001, PRV-0001.
- Timing/cadence: define with requirements; record evidence only after execution.
- Validation: reproducible command/method, exact fingerprint, time, environment,
  scope, result, limitations, freshness.
- Omit/combine: never omit; evidence may initially be empty.
- Evidence: both references' testing/validation/evidence layers.

### HOF-0001 — Handoff and resumption pack

- Category/classification: navigation / Core
- Purpose: provide a bounded current view and next safe action.
- Questions: What is active, blocked, fresh, and next?
- Audience/owner: incoming maintainer or agent / current task owner.
- Inputs: active tasks, accepted decisions, current evidence, registers.
- Outputs: reading order and resumption pointer.
- Format/authority: Markdown; derived navigation only.
- Dependencies: all current authoritative owners.
- Timing/cadence: before handoff and after active-state change.
- Validation: compact, link-based, no duplicated mutable facts, stale markers.
- Omit/combine: never omit for multi-session work; may merge with index only for
  truly single-session projects.
- Evidence: both references' handoff/resumption packages.

### Conditional and optional artifact types

| ID | Artifact | Class | Trigger | Owner/format | Validation/omission |
|---|---|---|---|---|---|
| MOD-0001 | Domain models, workflows, interfaces, schemas | Conditional | multiple entities, states, interfaces, suppliers, or handoffs | domain owner; Markdown/JSON/diagram | required refs and consistency; omit when ARC-0001 is sufficient |
| SEC-0001 | Security/privacy/legal/compliance model | Conditional | sensitive data, credentials, public claims, regulated activity, money, or external effects | qualified owners; Markdown/JSON/threat model | specialist review and control evidence; never infer conclusions |
| OPS-0001 | Operations/release/incident/recovery runbooks | Conditional | deployment, publication, ongoing service, or irreversible effects | operator; executable procedure plus Markdown | exercise evidence and rollback; omit before operations exist |
| RES-0001 | External-fact research | Conditional | mutable external facts affect decisions | researcher; Markdown/JSON source records | primary sources, retrieval date, contradiction and expiry |
| TRN-0001 | Transition and migration package | Conditional | established project, replacement, split/merge, or version upgrade | transition owner; Markdown/JSON crosswalk | compatibility, rollback, acceptance; omit for empty new project |
| HIS-0001 | Immutable historical baseline | Conditional | audit, release, regulated retention, or supersession needs | dossier custodian; frozen directory/manifest/checksum | immutability and successor links |
| DAT-0001 | Data classification and retention model | Conditional | personal, confidential, licensed, regulated, or production data | data owner; JSON/Markdown | classifications cover stores/flows; retention/deletion tested |
| SUP-0001 | Supply-chain and license inventory | Conditional | external code, models, content, datasets, vendors, or packages | supply-chain owner; SBOM/JSON | versions, licenses, provenance, vulnerability policy |
| EVA-0001 | Quality rubric and evaluation suite | Optional | repeated agent work or subjective/high-impact review | quality owner; Markdown/JSON/tests | versioned fixtures and scoring |
| CTX-0001 | Agent context packs | Optional | large dossier or specialist routing | dossier maintainer; Markdown | size budgets, source refs, no authority expansion |

## 5. Coverage profiles

Profiles are cumulative starting structures, not readiness levels.

### Minimal viable dossier

Appropriate for a new, small, low-risk project with one principal context.

Required artifacts:

- DOS-0001 through DOS-0006;
- DEF-0001, REQ-0001, ARC-0001, DEC-0001;
- GOV-0001 combined with requirements if desired;
- CUR-0001, CNF-0001, PLN-0001, REG-0001;
- PRV-0001, VAL-0001, HOF-0001.

Human-readable files may combine related concerns, but the artifact catalog
must preserve their distinct roles.

### Standard dossier

Default for active, multi-contributor, multi-session, or agent-assisted work.

Adds:

- authoritative JSON registries for requirements, findings, plans, RAIDQ,
  sources, evidence, path authority, and artifact catalog;
- explicit review cadence and owners;
- traceability and dependency validation;
- evidence and handoff maintenance checks; and
- project extensions when domain rules are consumed mechanically.

### High-assurance or agent-operable dossier

Appropriate when external effects, sensitive information, regulated work,
multiple environments, concurrent agents, long-lived handoff, audit, or
reproducibility applies.

Adds every triggered conditional artifact plus:

- generated manifest, checksums, source fingerprint, and freshness report;
- immutable baseline and supersession controls;
- recovery and interrupted-refresh tests;
- independent CI or protected validation where risk warrants;
- data, supply-chain, approval, and retention evidence; and
- context/evaluation packages for repeated agent work.

High Assurance is achieved only after its acceptance demonstrations pass.

## 6. Recommended directory structure

```text
project-dossier/
├── README.md
├── AUTHORITY.md
├── CANONICAL_SOURCE_MAP.md
├── ARTIFACT_CATALOG.json
├── MANIFEST.json                       # generated
├── CHECKSUMS.sha256                    # High Assurance, generated
├── VERSION.md
├── SUPERSESSION.json
├── canonical/
│   ├── executive-project-definition.md
│   ├── requirements-and-constraints.md
│   └── architecture-or-outcome-model.md
├── current-state/
├── conformance/
├── plans/
├── registers/
├── provenance/
├── evidence/
├── validation/
├── handoff/
├── machine-readable/
│   ├── requirements.json
│   ├── findings.json
│   ├── plan.json
│   ├── raidq.json
│   ├── sources.json
│   ├── evidence-index.json
│   └── path-authority.json             # generated from catalog
├── governance/                         # conditional
├── models/                             # conditional
├── operations/                         # conditional
├── research/                           # conditional
├── transition/                         # conditional
└── history/                            # conditional immutable records
```

Naming conventions:

- lower-kebab-case descriptive filenames;
- four-digit stable IDs inside records;
- one canonical owner for each mutable fact;
- `README.md` only as a directory entry point;
- `.json` for portable machine authority;
- Markdown for explanation;
- diagrams generated from a declared source where practical;
- generated files named and labeled as generated;
- no dates in canonical filenames unless the artifact is intentionally
  point-in-time evidence; and
- historical paths include version/fingerprint and explicit non-current banner.

## 7. Core artifact section outlines and schemas

Recommended concise outlines:

| Artifact | Required sections |
|---|---|
| DOS-0001 | purpose/boundary; reading order; current pointers; layer map; freshness |
| DOS-0002 | role; precedence; path classes; conflict rules; non-authority rules |
| DOS-0003 | concern-to-source table; mirror direction; change route; conflicts |
| DOS-0004 | schema/version; artifact entries; classifications; ownership; cadence |
| DOS-0005 | generation ID/time; scope/exclusions; file digests; limitations |
| DOS-0006 | current version; effective date; change summary; supersession records |
| DEF-0001 | identity; problem; intended outcome; in/out scope; audiences; owners; success |
| REQ-0001 | vocabulary; active/proposed requirements; constraints; traceability |
| ARC-0001 | context; actors; components/workstreams; boundaries; flows; states; failure behavior |
| DEC-0001 | context; options; decision; authority; consequences; validation; successor |
| GOV-0001 | constraints; gate catalog; approval sources; readiness criteria; exceptions |
| CUR-0001 | subject; time/environment; method; present/absent/unknown; evidence; limitations |
| CNF-0001 | method; classification; findings; coverage; unresolved assessment |
| PLN-0001 | objective; dependency graph; work items; gates; evidence; stop/rollback |
| REG-0001 | vocabularies; items; owners; impact; review/expiry; resolution |
| PRV-0001 | source classes; source records; rights/sensitivity; freshness; contradictions |
| VAL-0001 | commands/methods; evidence schema; results; limitations; freshness |
| HOF-0001 | current task; exact revision; recent evidence; blockers; next action; reading order |

Important structured field schemas are versioned under the generated
`.agent/schemas/` directory and validated by the harness. The artifact catalog
is authoritative metadata. Path authority is generated from it. Manifest,
checksums, and validation report are generated and never edited independently.
Human views generated from JSON state their source; authoritative Markdown
with a JSON mirror states that the mirror is generated.

## 8. Relationships and lifecycle

Primary flow:

```text
source/provenance
  → project definition
  → requirements and accepted decisions
  → architecture or outcome model
  → current-state evidence
  → conformance findings
  → dependency-aware plan and tasks
  → validation evidence and readiness gates
  → handoff/current state
  → supersession/history
```

Traceability rule:

```text
SRC → REQ → DEC/ARC/GOV → EVD/CUR → FIND → PLAN/TASK → EVD → GATE
```

Every active requirement has a basis, owner, validation method, current
assessment, and either satisfying evidence or planned remediation. Every
completed plan item links closure evidence. Every readiness gate names exact
requirements and evidence. Every handoff pointer resolves to a current owner.

Lifecycle:

1. Initialize authority, catalog, version, definition, and empty registers.
2. Adopt sources and record provenance.
3. Define proposed requirements and decisions; accept only through valid
   project authority.
4. Inspect current state independently of target material.
5. Assess conformance and create traceable plans.
6. Execute work through harness tasks.
7. Record evidence only after observation or execution.
8. Refresh generated integrity and handoff.
9. Supersede through successor records; archive immutable history when
   triggered.

## 9. Governance model

- Canonical authority: DOS-0002 and DOS-0003 define dossier interpretation;
  operating authority remains outside the dossier.
- Ownership: every catalog entry names an owner role and review cadence.
- Change control: canonical changes require source/decision basis, affected
  artifact list, traceability update, and validation.
- Versioning: semantic dossier version; breaking information-contract changes
  increment major version.
- Supersession: successor record, effective date, reason, migration, retained
  history, no silent deletion.
- Provenance: consequential claims link source IDs and limitations.
- Traceability: unique IDs and references validated repository-wide.
- Manifest/checksums: generated from declared scope; verified in the final
  read-only check; byte integrity only.
- Machine-readable mirrors: source direction declared and schema validated.
- Drift detection: catalog/path coverage, source fingerprint, stale evidence,
  broken links/refs, and duplicated authority fail validation.
- Periodic review: per change for affected records; monthly for active
  registers/evidence; quarterly for authority/recovery; per release for exact
  integrity.
- Human/agent handoff: compact, exact revision, current task, fresh evidence,
  blockers, next action, no secret values or implied approval.

## 10. Adoption checklist and quality gates

Creation sequence:

1. Read target-project instructions and inspect the repository.
2. Select the smallest profile justified by named triggers.
3. Generate transactionally into an empty new-project target, or produce a
   read-only adoption crosswalk for an established project.
4. Confirm artifact catalog and path-authority coverage.
5. Establish project definition, authority posture, source index, and owners.
6. Convert generated proposed baselines into project-specific records only
   from evidence or valid decisions.
7. Record current state from direct inspection.
8. Create requirements, findings, registers, and dependency-aware plan.
9. Configure project commands and triggered extensions.
10. Run strict structure, schema, traceability, lifecycle, integrity, and
    project checks.
11. Complete a real task through evidence, review, closure, and handoff.
12. Refresh generated integrity; run final read-only validation.

Objective quality gates:

- Completeness: every Core catalog type exists or has an explicit combined
  path; every conditional trigger is assessed.
- Consistency: one authority owner per concern; controlled statuses and schema
  versions; no contradictory mutable facts.
- Freshness: current evidence and generated reports match exact managed source.
- Traceability: every active requirement and completed plan item closes its
  required links.
- Authority: every path is classified; no dossier content grants permission.
- Navigability: all entry links resolve; High profile directories are listed.
- Resumability: an unfamiliar maintainer identifies current task, revision,
  evidence, blocker, and next action within ten minutes.
- Integrity: manifest/checksums/report share one generation ID and scope.
- Safety: no secret values, escaping errors, path traversal, or untrusted
  instruction expansion.
- Truthfulness: skipped checks, dirty/untracked/ignored scope, limitations, and
  external effects are disclosed.

## 11. Gaps and new recommendations

The following are **[Recommended]**, not observed universal conventions:

- Use strict JSON as the portable kernel format; permit YAML only through a
  pinned, duplicate-key-safe parser extension.
- Generate path authority from the authoritative artifact catalog.
- Validate identifiers and references across dossier and harness as one
  namespace.
- Treat project-source fingerprinting and dossier checksums as one integrity
  transaction.
- Use generation IDs to detect partial refreshes.
- Require an empty-target transactional generator for new projects and a
  separate read-only adoption planner for established projects.
- Package the bootstrap skill explicitly so future project agents can discover
  it.
- Protect high-assurance checks in independent CI or another trust boundary.
- Add data classification, supply-chain, cost/rate, concurrency, recovery, and
  evaluation extensions only when their triggers apply.

Unresolved universal limits:

- no dossier can establish legal, security, privacy, accessibility, financial,
  or production readiness without qualified project-specific evidence;
- external tool/platform authority cannot be created by repository files;
- domain correctness requires extensions and specialists;
- a generated skeleton is not an adopted dossier; and
- projects without a repository/filesystem require an adapted storage and
  instruction mechanism while preserving the same information contracts.
