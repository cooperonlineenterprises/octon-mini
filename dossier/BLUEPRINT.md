# Universal Project Dossier Blueprint

Blueprint version: 3.1.0
Reference-analysis date: 2026-08-10

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

**[Observed: both] [Inferred]**
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

Use the following semantic roles to describe information without replacing an
artifact's own aggregate-specific status vocabulary:

| Role | Meaning and use boundary |
|---|---|
| `authoritative` | The declared source for a bounded concern; this is information authority only and does not grant action permission. |
| `observed` | A dated inspection of an exact subject, scope, method, and environment. |
| `inferred` | A conclusion derived from stated premises with uncertainty and limitations exposed. |
| `proposed` | A candidate fact, target, or decision that has not been accepted by its owner. |
| `derived` | A reproducible projection from named sources; it never writes authority back to those sources. |
| `historical` | Retained noncurrent material used for provenance, audit, or recovery. |
| `superseded` | Material replaced by a named successor and no longer current for its former purpose. |
| `stale` | Material whose freshness or validity boundary has elapsed and must not support a consequential current claim. |
| `unknown` | A fact that has not been established; it is not false, absent, or ready. |
| `intentionally_omitted` | Information deliberately excluded with a disclosed reason, scope, and consequence. |

These roles are a crosswalk, not a universal status enum, trust score,
readiness model, or lifecycle. An artifact can be an authoritative source whose
aggregate-specific status is `proposed`, for example. None of the roles grants
permission or establishes readiness by itself.

### 2.4 Evidence is scoped, dated, and reproducible

**[Observed: both] [Recommended]**
Current-state and readiness claims identify subject version, observation time,
method, environment, result, and limitations. Consequential evidence also
states what its result does not prove. Stale evidence never overrides a newer
direct observation.

### 2.5 Provenance survives transformation

**[Observed: both] [Recommended]**
Every consequential source records identity, version or retrieval date,
classification, intended use, sensitivity, limitations, and freshness rule.
Derived artifacts link their source records.

### 2.6 Versioning and supersession preserve history

**[Observed: CF] [Inferred]**
Accepted evidence and durable decisions are immutable or corrected with a
successor. A supersession record names the old artifact, replacement,
effective date, reason, migration impact, and retained-history location.

### 2.7 Progressive disclosure controls context

**[Observed: both] [Inferred]**
The dossier index and handoff pack stay compact. Readers load canonical,
current-state, plan, specialist models, evidence, or history only when the
task requires them. Large transcripts and historical narratives never
accumulate in the entry point.

### 2.8 Machine-readable mirrors have declared ownership

**[Observed: both] [Recommended]**
Each mirror states whether it is authoritative, generated from a human source,
or the source from which a human view is generated. Two independently edited
representations may not both claim authority.

### 2.9 Unknown is a valid state

**[Inferred] [Recommended]**
Use `unknown`, `not_assessed`, `not_applicable`, and `gated` rather than
inventing facts or interpreting absence as failure.

### 2.10 Collaboration topology remains harness governance

**[Recommended]** The dossier may provide dated, privacy-minimized evidence
about repository access, activity, reviewer capacity, concurrency, or external
contribution. The authoritative current collaboration assessment and any
adopted Git workflow belong in `.agent/project.json`, not in dossier prose.
Neither an observation nor a workflow decision grants repository permission.
Human team size selects only a base collaboration workflow; dossier and harness
profiles remain independently selected from project risk and assurance needs.

## 3. Reference-dossier crosswalk

The references share a common information architecture but emphasize
different risks. CF's root instructions identify
`CF:project-dossier/v0.2/` as the current canonical target; the Phase 0
material directly under `CF:project-dossier/` is a retained historical
baseline. COE contains a more
explicit authority, current-state, conformance, plan, provenance, and
integrity separation. Neither dossier is an instruction or permission channel.

| Artifact family | Commerce Foundry evidence | COE evidence | Generalized interpretation |
|---|---|---|---|
| Entry and navigation | `CF:project-dossier/v0.2/README.md`; `CF:project-dossier/v0.2/HANDOFF_MANIFEST.md` | `COE:project-dossier/README.md`; `COE:project-dossier/handoff/START_HERE.md` | Compact index and resumable entry point |
| Authority and canonical map | `CF:project-dossier/v0.2/CANONICAL_SOURCE_MAP.md` | `COE:project-dossier/AUTHORITY.md`; `COE:project-dossier/CANONICAL_SOURCE_MAP.md` | Explicit interpretation and source ownership |
| Version and supersession | `CF:project-dossier/v0.2/SUPERSESSION_MAP.md`; `CF:project-dossier/v0.2/baseline/README.md` | No direct dossier-version or supersession-ledger equivalent observed | Explicit lifecycle, replacement, and noncurrent history |
| Generated integrity | `CF:project-dossier/v0.2/CHECKSUMS.md`; `CF:project-dossier/v0.2/HANDOFF_MANIFEST.md` | `COE:project-dossier/MANIFEST.json`; `COE:project-dossier/CHECKSUMS.sha256` | Point-in-time inventory and byte identity, not supersession or authority |
| Project definition | `CF:project-dossier/v0.2/canonical/platform-definition.md`; `CF:project-dossier/v0.2/canonical/executive-summary.md` | `COE:project-dossier/canonical/executive-project-definition.md` | Identity, problem, scope, outcomes, success |
| Requirements | `CF:project-dossier/v0.2/dossier-v0.2/docs/requirements/functional-requirements.md`; `CF:project-dossier/v0.2/dossier-v0.2/docs/requirements/requirements-traceability.md` | `COE:project-dossier/canonical/requirements-and-constraints.md`; `COE:project-dossier/machine-readable/requirements.yaml` | Stable requirement definitions and traceability |
| Architecture/outcome model | `CF:project-dossier/v0.2/canonical/architecture.md`; `CF:project-dossier/v0.2/canonical/canonical-workflow.md`; `CF:project-dossier/v0.2/canonical/domain-data-model.md` | `COE:project-dossier/canonical/technical-architecture.md`; `COE:project-dossier/canonical/business-and-brand-architecture.md` | Domain-neutral actors, components, flows, interfaces, invariants |
| Decisions | `CF:project-dossier/v0.2/dossier-v0.2/docs/architecture/adr/`; live `CF:.agent/decisions/` | proposed dossier records at `COE:project-dossier/registers/decisions.yaml`; live status-dependent records at `COE:.agent/decisions/` | Durable accepted intent, preferably owned once |
| Current state | `CF:project-dossier/v0.2/agent-handoff/current-implementation-status.md`; `CF:project-dossier/v0.2/conformance/repository-inventory.md` | `COE:project-dossier/current-state/repository-baseline.md` | Dated observation, not target or plan |
| Conformance | `CF:project-dossier/v0.2/conformance/README.md`; `CF:project-dossier/v0.2/conformance/conformance-matrix.csv` | `COE:project-dossier/conformance/findings.yaml`; `COE:project-dossier/conformance/initial-assessment.md` | Requirement-to-evidence gap assessment |
| Planning | `CF:project-dossier/v0.2/implementation-plan/dependency-roadmap.md`; `CF:project-dossier/v0.2/implementation-plan/task-dependency-graph.md` | `COE:project-dossier/implementation-plan/dependency-graph.md`; `COE:project-dossier/implementation-plan/plan.yaml` | Dependency-aware future sequence |
| Registers | `CF:project-dossier/v0.2/implementation-plan/risk-register.md`; `CF:project-dossier/v0.2/implementation-plan/technical-debt-register.md` | `COE:project-dossier/registers/risks.yaml`; `COE:project-dossier/registers/open-questions.yaml` | Risks, assumptions, issues, dependencies, questions |
| Provenance/research | `CF:project-dossier/v0.2/verification/verification-manifest.md`; `CF:project-dossier/v0.2/verification/etsy-reverification-2026-07-23.md` | `COE:project-dossier/provenance/source-index.yaml`; `COE:project-dossier/provenance/reference-model-notes.md` | Source identity, external-fact freshness, limitations |
| Validation/evidence | `CF:project-dossier/v0.2/machine-readable/validation-report.json`; `CF:project-dossier/v0.2/dossier-v0.2/evidence/README.md` | `COE:project-dossier/validation/validation-report.json`; `COE:.agent/evidence/` | Reproducible checks and bounded evidence |
| Operations/recovery | `CF:project-dossier/v0.2/canonical/monitoring-lifecycle-model.md`; `CF:project-dossier/v0.2/implementation-plan/release-gates.md` | `COE:project-dossier/canonical/seo-analytics-and-operations.md`; `COE:project-dossier/implementation-plan/acceptance-gates.md` | Conditional runbooks and gates triggered by external effects |
| Machine-readable authority | `CF:project-dossier/v0.2/machine-readable/repository-path-authority.yaml`; `CF:project-dossier/v0.2/machine-readable/workflow-registry.yaml` | `COE:project-dossier/machine-readable/path-authority.yaml`; `COE:project-dossier/machine-readable/requirements.yaml` | Typed sources, mirrors, and path classification |

Direct equivalents include entry points, canonical requirements, current
state, plans, registers, validation, and handoff. Functional equivalents use
different structures for decisions, architecture, and evidence. CF uniquely
provides an explicit dossier supersession package and emphasizes detailed
runtime, workflow, schema, and operations material. COE uniquely emphasizes
path-authority classification and generated integrity. COE integrity files
are not treated as lifecycle or supersession equivalents.

Apparent reference gaps and the blueprint response:

- **[Recommended]** Neither reference provides a portable universal artifact
  registry/catalog schema.
- **[Inferred]** Both benefit from stronger automatic drift and freshness
  enforcement.
- **[Inferred]** Both demonstrate the risk of resumption summaries growing
  beyond a compact current view.
- **[Recommended]** Neither reference supplies a domain-neutral installation and migration
  package for arbitrary projects; and
- **[Inferred]** Generated checksums in a repository-local trust boundary do not independently
  attest correctness or approval.

## 4. General artifact taxonomy

Classification:

- **Core** — expected in nearly every dossier.
- **Conditional** — required when a named trigger or risk is present.
- **Optional** — useful for complex coordination or higher assurance.

### 4.1 Three-level identity model

Artifact identity has three explicit levels. IDs are unique and immutable
within their typed namespace; references name the namespace and ID rather than
assuming that a bare string is globally unambiguous.

1. **Conceptual artifact type** — a reusable information contract such as
   `REQ-0001` (requirements and traceability). These definitions are owned by
   `dossier/artifact-types.json` in this blueprint and copied into a generated
   project’s authoritative artifact registry.
2. **Physical representation** — a concrete path and edit direction identified
   only as `REP-####`. Several representations may implement one type; for
   example, explanatory Markdown and an authoritative structured record store.
   One representation may deliberately implement multiple conceptual types;
   `artifact_type_ids` records that combination without duplicating a path.
3. **Record instance** — a project fact, requirement, decision, finding, plan
   item, source, or evidence record. Record IDs follow the applicable record
   schema and lifecycle. They are not artifact-type or representation IDs.

The v1 source catalog used conceptual-looking IDs for physical paths. Version
1.0.1 retires that ambiguity: every old physical ID is preserved as
`legacy_v1_id` on its `REP-####` successor. A retired legacy ID is never
reassigned silently.

### 4.2 Registry, applicability, and review semantics

`project-dossier/machine-readable/artifact-registry.json` is the project-local
edit source for artifact metadata. `ARTIFACT_CATALOG.json` and
`machine-readable/path-authority.json` are generated mirrors. A maintainer
changes the registry and runs refresh; derived files are never edited
independently.

Conceptual type applicability is the durable trigger/omission decision.
Core types use `required`. Conditional and Optional types use `not_assessed`,
`applicable`, or `not_applicable`. A scaffold begins conditional/optional
types as `not_assessed`; physical entry-point presence does not mean the
trigger applies. `applicable` and `not_applicable` require `assessed_on`,
`assessed_by`, and an evidence-based rationale. Only a `not_applicable` type
may remain in the registry without a physical representation, preserving the
omission decision after its path is removed.

For an adopted High-Assurance harness, every Conditional and Optional type
must be assessed. An `applicable` type additionally links current `EVD-####`
records through `applicability.evidence_refs`, retains a named assessor and
owner role, and has an active reviewed representation. These links prove only
that the declared assessment has evidence; they do not certify the control,
specialist conclusion, or production readiness.

Representation applicability describes physical realization and additionally
supports `combined`. A combined representation requires at least two
`artifact_type_ids`, each referring to a required or applicable type, and a
rationale naming the sections and edit direction that keep the concerns
distinct inside one file.

Review state is separate from generation provenance. `generated_on` or
`scaffold_generated_on` records when structure was produced. A substantive
`last_reviewed_on` remains `null` until a named maintainer reviews project
content against stated evidence. Refreshing derived files never advances that
review date.

Representation roles and source directions are controlled by the registry.
`project_maintained_source*`, `authoritative_when_present`, and
`external_live_store_navigation` identify edit ownership;
`generated_from_artifact_registry` and `generated_from_managed_files` identify
derived outputs; `navigation_only` and
`derived_navigation_maintained_by_task_owner` cannot own mutable facts.

### 4.3 Complete artifact-type specifications

The following is the self-contained human-readable specification of every
conceptual type in the v2 machine source. A `CF:` or `COE:` locator is
**[Observed]** evidence from that reference; entries prefixed `Inferred:` or
`Recommended:` retain those explicit labels.

#### DOS-0001 — Dossier index

- **Category / classification:** navigation / core
- **Minimum profile:** minimal
- **Type applicability default:** required — Core artifact type for the selected profile. (`assessed_on`: null; `assessed_by`: null)
- **Purpose:** Route readers to authoritative layers without restating mutable content.
- **Questions it must answer:** Where do I start?; Which profile and information layers apply?;
  Where is current work summarized?
- **Intended audience:** all_project_participants, new_maintainers, agents
- **Expected owner or maintainer:** dossier_maintainer
- **Required inputs:** artifact_registry, authority_map, current_handoff_pointers
- **Outputs / downstream consumers:** all_dossier_readers, handoff_workflows
- **Recommended format:** Markdown
- **Source-of-truth expectations:** Navigation only; it links authoritative sources and never
  owns their mutable facts.
- **Dependencies and related artifacts:** DOS-0002, DOS-0003, DOS-0010
- **Creation timing:** Create first as the dossier entry point.
- **Update triggers:** artifact_path_change, profile_change, entry_point_change
- **Review cadence:** on_path_or_entry_point_change
- **Validation / quality checks:** links_resolve, all_active_layers_listed,
  no_duplicated_mutable_status
- **Inclusion triggers:** all_projects
- **Omission or combination:** Never omit. It may share a file with HOF-0001 only for truly
  single-session work if authority and state remain visibly separate.
- **Representative evidence:** `CF:project-dossier/v0.2/README.md`;
  `COE:project-dossier/README.md`

#### DOS-0002 — Authority and interpretation map

- **Category / classification:** governance / core
- **Minimum profile:** minimal
- **Type applicability default:** required — Core artifact type for the selected profile. (`assessed_on`: null; `assessed_by`: null)
- **Purpose:** Define dossier precedence, information roles, conflict handling, and the
  non-authorizing boundary.
- **Questions it must answer:** Which source governs each concern?; How are conflicts handled?;
  What cannot grant permission?
- **Intended audience:** all_project_participants, reviewers, agents
- **Expected owner or maintainer:** project_governance_owner
- **Required inputs:** applicable_repository_instructions, accepted_decisions,
  source_classifications
- **Outputs / downstream consumers:** canonical_source_map, validators, handoff
- **Recommended format:** Markdown
- **Source-of-truth expectations:** Authoritative only for interpreting dossier information;
  operating permission remains outside the dossier.
- **Dependencies and related artifacts:** DEC-0001, PRV-0001
- **Creation timing:** Create before project-specific dossier content is adopted.
- **Update triggers:** authority_change, information_role_change, conflict_discovered
- **Review cadence:** on_authority_change_and_quarterly_for_active_projects
- **Validation / quality checks:** non_authorizing_boundary_present, precedence_complete,
  conflict_rule_present
- **Inclusion triggers:** all_projects
- **Omission or combination:** Never omit as a concern; Minimal may combine it with DOS-0003
  under distinct headings.
- **Representative evidence:** `CF:project-dossier/v0.2/CANONICAL_SOURCE_MAP.md`;
  `COE:project-dossier/AUTHORITY.md`

#### DOS-0003 — Canonical-source map

- **Category / classification:** governance / core
- **Minimum profile:** minimal
- **Type applicability default:** required — Core artifact type for the selected profile. (`assessed_on`: null; `assessed_by`: null)
- **Purpose:** Name the single source owner and edit direction for every mutable concern.
- **Questions it must answer:** Where is each definition maintained?; Which view is generated?;
  How does profile choice change representation ownership?
- **Intended audience:** maintainers, reviewers, agents
- **Expected owner or maintainer:** dossier_maintainer
- **Required inputs:** artifact_registry, accepted_source_ownership_decisions
- **Outputs / downstream consumers:** navigation, drift_detection, change_control
- **Recommended format:** Markdown
- **Source-of-truth expectations:** Authoritative for concern-to-source routing; it does not
  duplicate the routed content.
- **Dependencies and related artifacts:** DOS-0002, DOS-0010
- **Creation timing:** Create with the first canonical and observed-state artifacts.
- **Update triggers:** source_owner_change, representation_added, source_direction_change
- **Review cadence:** on_source_owner_or_representation_change
- **Validation / quality checks:** one_edit_owner_per_concern, generated_direction_declared,
  all_active_stores_routed
- **Inclusion triggers:** all_projects
- **Omission or combination:** Never omit as a concern; Minimal may combine it with DOS-0002
  under distinct headings.
- **Representative evidence:** `CF:project-dossier/v0.2/CANONICAL_SOURCE_MAP.md`;
  `COE:project-dossier/CANONICAL_SOURCE_MAP.md`

#### DOS-0004 — Generated artifact catalog

- **Category / classification:** inventory / core
- **Minimum profile:** minimal
- **Type applicability default:** required — Core artifact type for the selected profile. (`assessed_on`: null; `assessed_by`: null)
- **Purpose:** Provide a normalized, machine-readable point-in-time view of the project-local
  artifact registry.
- **Questions it must answer:** Which type and representation records were cataloged?; From
  which registry generation was this view produced?
- **Intended audience:** validators, maintainers, agents
- **Expected owner or maintainer:** artifact_registry_refresh_tool
- **Required inputs:** DOS-0010
- **Outputs / downstream consumers:** navigation_checks, integrity_validation
- **Recommended format:** JSON
- **Source-of-truth expectations:** Generated non-authoritative mirror of DOS-0010; never edited
  independently.
- **Dependencies and related artifacts:** DOS-0010
- **Creation timing:** Generate after registry initialization and after every registry change.
- **Update triggers:** artifact_registry_change, integrity_refresh
- **Review cadence:** generated_on_registry_change
- **Validation / quality checks:** schema_valid, generation_id_matches_related_outputs,
  content_matches_registry
- **Inclusion triggers:** all_projects
- **Omission or combination:** Never omit from a generated dossier; consumers that can read
  DOS-0010 directly may ignore this view but must not edit it.
- **Representative evidence:** Recommended: portable normalized catalog inferred from both
  reference manifests

#### DOS-0005 — Generated manifest and integrity set

- **Category / classification:** integrity / core
- **Minimum profile:** minimal
- **Type applicability default:** required — Core artifact type for the selected profile. (`assessed_on`: null; `assessed_by`: null)
- **Purpose:** Record a point-in-time managed-file inventory and, when triggered, byte
  checksums.
- **Questions it must answer:** Which bytes and paths were checked?; What was excluded?; Are
  related integrity outputs from one refresh?
- **Intended audience:** reviewers, release_owners, automation
- **Expected owner or maintainer:** integrity_refresh_tool
- **Required inputs:** DOS-0010, declared_managed_scope
- **Outputs / downstream consumers:** freshness_checks, handoff, release_or_audit_evidence
- **Recommended format:** JSON, SHA-256 checksum text
- **Source-of-truth expectations:** Generated evidence only; proves scoped byte identity, not
  authority, correctness, approval, or readiness.
- **Dependencies and related artifacts:** DOS-0010, VAL-0001
- **Creation timing:** Generate at scaffold time and refresh after managed changes; checksums
  are High-Assurance or risk-triggered.
- **Update triggers:** managed_file_change, handoff, release_candidate, integrity_refresh
- **Review cadence:** after_managed_change_and_before_gated_handoff
- **Validation / quality checks:** scope_exact, generation_ids_match, fingerprint_fresh,
  checksum_set_complete_when_enabled
- **Inclusion triggers:** manifest_for_all_profiles, checksums_for_high_assurance_or_audit_need
- **Omission or combination:** The manifest is Core. Checksums may be omitted unless audit,
  release, immutable-baseline, or High-Assurance triggers apply.
- **Representative evidence:** `CF:project-dossier/v0.2/CHECKSUMS.md`;
  `COE:project-dossier/MANIFEST.json`; `COE:project-dossier/CHECKSUMS.sha256`

#### DOS-0006 — Dossier version record

- **Category / classification:** lifecycle / core
- **Minimum profile:** minimal
- **Type applicability default:** required — Core artifact type for the selected profile. (`assessed_on`: null; `assessed_by`: null)
- **Purpose:** Identify the dossier contract version, adoption state, effective date, and change
  basis.
- **Questions it must answer:** Which dossier version is current?; Was it merely generated or
  project-adopted?; What migration applies?
- **Intended audience:** maintainers, auditors, upgrade_tools
- **Expected owner or maintainer:** dossier_governance_owner
- **Required inputs:** accepted_dossier_changes, blueprint_origin, migration_records
- **Outputs / downstream consumers:** upgrade_planning, handoff, supersession
- **Recommended format:** Markdown
- **Source-of-truth expectations:** Project-maintained source for dossier version and adoption
  state.
- **Dependencies and related artifacts:** DOS-0007, DEC-0001
- **Creation timing:** Create at initialization; mark generated baseline as unadopted.
- **Update triggers:** dossier_contract_change, profile_change, adoption_or_upgrade
- **Review cadence:** on_semantic_dossier_change
- **Validation / quality checks:** semantic_version_valid, adoption_state_explicit,
  migration_link_present_when_required
- **Inclusion triggers:** all_projects
- **Omission or combination:** Never omit; it may be presented with the supersession ledger only
  if the machine-readable lifecycle record remains available.
- **Representative evidence:** `CF:project-dossier/v0.2/README.md`; Inferred: COE records
  point-in-time creation and generated integrity but has no direct dossier-version equivalent

#### DOS-0007 — Supersession ledger

- **Category / classification:** lifecycle / core
- **Minimum profile:** minimal
- **Type applicability default:** required — Core artifact type for the selected profile. (`assessed_on`: null; `assessed_by`: null)
- **Purpose:** Preserve explicit artifact replacements, effective dates, reasons, migrations,
  and retained history.
- **Questions it must answer:** What is no longer current?; What replaced it?; Where is history
  retained?
- **Intended audience:** maintainers, auditors, agents
- **Expected owner or maintainer:** dossier_governance_owner
- **Required inputs:** accepted_successor_change, artifact_registry, retention_decision
- **Outputs / downstream consumers:** authority_resolution, history, migration, handoff
- **Recommended format:** JSON
- **Source-of-truth expectations:** Authoritative project-local lifecycle record; changes append
  or correct through an explicit successor.
- **Dependencies and related artifacts:** DOS-0006, DOS-0010, DEC-0001
- **Creation timing:** Create empty at initialization; add a record before a superseded artifact
  is treated as noncurrent.
- **Update triggers:** artifact_superseded, artifact_split_or_merged, dossier_version_change
- **Review cadence:** on_supersession
- **Validation / quality checks:** no_cycles, successors_resolve, retained_location_resolves,
  ids_not_reused
- **Inclusion triggers:** all_projects
- **Omission or combination:** Never omit the empty ledger; it may remain empty until the first
  supersession.
- **Representative evidence:** `CF:project-dossier/v0.2/SUPERSESSION_MAP.md`; Recommended: COE
  has no direct dossier supersession ledger equivalent

#### DOS-0008 — Generated path-authority map

- **Category / classification:** governance / core
- **Minimum profile:** minimal
- **Type applicability default:** required — Core artifact type for the selected profile. (`assessed_on`: null; `assessed_by`: null)
- **Purpose:** Provide per-path information-state and authority classification derived from the
  registry.
- **Questions it must answer:** Which representation owns this path?; What information role and
  source direction apply?
- **Intended audience:** validators, agents, reviewers
- **Expected owner or maintainer:** artifact_registry_refresh_tool
- **Required inputs:** DOS-0010
- **Outputs / downstream consumers:** authority_checks, drift_detection, safe_context_loading
- **Recommended format:** JSON
- **Source-of-truth expectations:** Generated non-authoritative mirror; DOS-0010 owns
  representation metadata.
- **Dependencies and related artifacts:** DOS-0010
- **Creation timing:** Generate alongside the artifact catalog directly from the artifact
  registry.
- **Update triggers:** artifact_registry_change, integrity_refresh
- **Review cadence:** generated_on_registry_change
- **Validation / quality checks:** every_managed_dossier_path_covered_once,
  content_matches_registry, generation_id_matches_catalog
- **Inclusion triggers:** all_projects
- **Omission or combination:** Never omit from an agent-operable generated dossier;
  non-filesystem adaptations must provide an equivalent locator classification.
- **Representative evidence:**
  `CF:project-dossier/v0.2/machine-readable/repository-path-authority.yaml`;
  `COE:project-dossier/machine-readable/path-authority.yaml`

#### DOS-0010 — Project artifact registry

- **Category / classification:** inventory / core
- **Minimum profile:** minimal
- **Type applicability default:** required — Core artifact type for the selected profile. (`assessed_on`: null; `assessed_by`: null)
- **Purpose:** Own project-local artifact types, physical representations, applicability
  decisions, review state, and source direction.
- **Questions it must answer:** Which artifact types apply?; Which physical representations are
  active?; Who owns and reviews each one?
- **Intended audience:** dossier_maintainers, validators, agents
- **Expected owner or maintainer:** dossier_maintainer
- **Required inputs:** selected_profile, project_trigger_assessment,
  accepted_path_and_owner_changes
- **Outputs / downstream consumers:** DOS-0004, DOS-0008, DOS-0005, navigation, drift_detection
- **Recommended format:** JSON
- **Source-of-truth expectations:** Authoritative project-local metadata source seeded by
  generation and thereafter maintained explicitly; generated views never replace it.
- **Dependencies and related artifacts:** DOS-0002, DOS-0003
- **Creation timing:** Seed during scaffold generation before derived catalog and path-authority
  outputs.
- **Update triggers:** artifact_added_or_removed, path_change, applicability_assessment,
  owner_or_review_change, supersession
- **Review cadence:** on_artifact_change_and_quarterly_for_active_projects
- **Validation / quality checks:** type_ids_unique, representation_ids_unique,
  paths_confined_and_unique, references_resolve, applicability_and_review_semantics_valid
- **Inclusion triggers:** all_projects
- **Omission or combination:** Never omit. It is the edit source; DOS-0004 and DOS-0008 must be
  regenerated from it.
- **Representative evidence:** Recommended: closes the editable-registry and derived-catalog gap
  observed across both references

#### DEF-0001 — Executive project definition

- **Category / classification:** project_definition / core
- **Minimum profile:** minimal
- **Type applicability default:** required — Core artifact type for the selected profile. (`assessed_on`: null; `assessed_by`: null)
- **Purpose:** Define project identity, problem, intended outcomes, boundaries, audiences,
  ownership, and success.
- **Questions it must answer:** What is this project?; What is explicitly out of scope?; What
  outcomes and measures define success?
- **Intended audience:** all_stakeholders, maintainers, agents
- **Expected owner or maintainer:** project_owner
- **Required inputs:** authoritative_brief, accepted_scope_decisions, stakeholder_evidence
- **Outputs / downstream consumers:** requirements, architecture_or_outcome_model, planning,
  success_assessment
- **Recommended format:** Markdown
- **Source-of-truth expectations:** Canonical target definition; proposed or unknown content
  stays labeled.
- **Dependencies and related artifacts:** PRV-0001, DEC-0001
- **Creation timing:** Create during project framing before detailed requirements.
- **Update triggers:** strategy_change, scope_change, outcome_change, ownership_change
- **Review cadence:** on_strategy_or_scope_change_and_at_major_gates
- **Validation / quality checks:** scope_bounded, non_goals_present, success_measures_testable,
  unknowns_labeled
- **Inclusion triggers:** all_projects
- **Omission or combination:** Never omit; small projects may combine it with REQ-0001 and
  ARC-0001 under separate sections.
- **Representative evidence:** `CF:project-dossier/v0.2/canonical/platform-definition.md`;
  `COE:project-dossier/canonical/executive-project-definition.md`

#### REQ-0001 — Requirements and traceability system

- **Category / classification:** requirements / core
- **Minimum profile:** minimal
- **Type applicability default:** required — Core artifact type for the selected profile. (`assessed_on`: null; `assessed_by`: null)
- **Purpose:** Own requirement wording, basis, status, owner, validation method, and
  traceability.
- **Questions it must answer:** What must be true?; Why is it required?; How will it be verified
  and what currently satisfies it?
- **Intended audience:** owners, implementers, reviewers, agents
- **Expected owner or maintainer:** requirements_owner
- **Required inputs:** project_definition, accepted_decisions, constraints, provenance
- **Outputs / downstream consumers:** architecture, conformance, plans, validation, gates
- **Recommended format:** Markdown, JSON for Standard and High-Assurance record stores
- **Source-of-truth expectations:** Minimal owns records in Markdown; Standard and
  High-Assurance own individual records in JSON while Markdown owns vocabulary and explanation.
- **Dependencies and related artifacts:** DEF-0001, PRV-0001, DEC-0001
- **Creation timing:** Create before conformance assessment and implementation planning.
- **Update triggers:** requirement_proposed, decision_accepted, constraint_change,
  validation_method_change
- **Review cadence:** on_requirement_change_and_before_readiness_gates
- **Validation / quality checks:** stable_record_ids, basis_and_owner_present,
  status_controlled, validation_and_traceability_complete
- **Inclusion triggers:** all_projects
- **Omission or combination:** Never omit; prose may share DEF-0001 in Minimal, but requirement
  IDs and record ownership remain explicit.
- **Representative evidence:**
  `CF:project-dossier/v0.2/dossier-v0.2/docs/requirements/requirements-traceability.md`;
  `COE:project-dossier/machine-readable/requirements.yaml`;
  `COE:project-dossier/requirements/traceability.md`

#### ARC-0001 — Architecture or outcome model

- **Category / classification:** architecture_or_outcome / core
- **Minimum profile:** minimal
- **Type applicability default:** required — Core artifact type for the selected profile. (`assessed_on`: null; `assessed_by`: null)
- **Purpose:** Describe intended actors, components or workstreams, boundaries, flows,
  interfaces, states, and invariants.
- **Questions it must answer:** How should the intended system or outcome fit together?; Where
  are boundaries and failure modes?; Which requirements does each part support?
- **Intended audience:** implementers, designers, reviewers, operators
- **Expected owner or maintainer:** architecture_or_design_owner
- **Required inputs:** project_definition, requirements, accepted_decisions,
  domain_models_when_applicable
- **Outputs / downstream consumers:** plans, interfaces, validation, operations
- **Recommended format:** Markdown, diagram, JSON schema where mechanically consumed
- **Source-of-truth expectations:** Canonical intended structure; diagrams generated from
  another source are labeled derived.
- **Dependencies and related artifacts:** DEF-0001, REQ-0001, DEC-0001
- **Creation timing:** Create before detailed execution or implementation.
- **Update triggers:** accepted_design_change, boundary_change, workflow_change,
  failure_model_change
- **Review cadence:** on_accepted_design_change
- **Validation / quality checks:** requirements_coverage, boundaries_explicit,
  flows_and_failure_behavior_consistent, generated_diagrams_trace_source
- **Inclusion triggers:** all_projects
- **Omission or combination:** Never omit the concern; non-software projects use outcome,
  operating, service, or workstream terminology.
- **Representative evidence:** `CF:project-dossier/v0.2/canonical/architecture.md`;
  `COE:project-dossier/canonical/technical-architecture.md`;
  `COE:project-dossier/canonical/business-and-brand-architecture.md`

#### DEC-0001 — Durable decision records

- **Category / classification:** decisions / core
- **Minimum profile:** minimal
- **Type applicability default:** required — Core artifact type for the selected profile. (`assessed_on`: null; `assessed_by`: null)
- **Purpose:** Preserve the context, authority, alternatives, consequences, and successors of
  durable choices.
- **Questions it must answer:** What was decided?; Under which authority and scope?; What did it
  replace and how is it validated?
- **Intended audience:** future_maintainers, owners, reviewers, agents
- **Expected owner or maintainer:** decision_owner
- **Required inputs:** decision_context, alternatives, evidence, valid_authority_source
- **Outputs / downstream consumers:** canonical_target, requirements, plans, supersession
- **Recommended format:** Markdown records governed by the harness lifecycle
- **Source-of-truth expectations:** Status-dependent live decision store belongs in the harness;
  dossier summaries only link to it.
- **Dependencies and related artifacts:** none
- **Creation timing:** Create when a durable choice is proposed; acceptance requires valid
  project authority.
- **Update triggers:** decision_proposed, decision_status_change, decision_superseded
- **Review cadence:** on_durable_choice_or_invalidating_evidence
- **Validation / quality checks:** stable_ids, legal_status_transition,
  authority_source_present_for_acceptance, successor_semantics
- **Inclusion triggers:** all_projects
- **Omission or combination:** The store is Core; an empty store is valid and generation must
  not fabricate an accepted decision.
- **Representative evidence:** `CF:.agent/decisions/`; `COE:.agent/decisions/`;
  `CF:project-dossier/v0.2/dossier-v0.2/docs/architecture/adr/`

#### GOV-0001 — Constraints, quality gates, and readiness criteria

- **Category / classification:** governance / core
- **Minimum profile:** minimal
- **Type applicability default:** required — Core artifact type for the selected profile. (`assessed_on`: null; `assessed_by`: null)
- **Purpose:** Define constraints and objective evidence conditions for progression without
  recording approval itself.
- **Questions it must answer:** Which gates apply?; Who may decide them?; What exact evidence,
  expiry, and exception rules apply?
- **Intended audience:** owners, reviewers, specialists, operators
- **Expected owner or maintainer:** project_governance_owner
- **Required inputs:** requirements, risk_analysis, specialist_obligations, authority_sources
- **Outputs / downstream consumers:** plans, validation, handoff, readiness_decisions
- **Recommended format:** Markdown, JSON gate records
- **Source-of-truth expectations:** Criteria are canonical; generated proposed gates remain
  unadopted until project authority accepts them. Approval evidence is separate.
- **Dependencies and related artifacts:** REQ-0001, REG-0001, VAL-0001
- **Creation timing:** Create before any gated work or readiness claim.
- **Update triggers:** gate_added_or_changed, risk_change, environment_change, obligation_change
- **Review cadence:** on_gate_or_risk_change_and_before_gate_evaluation
- **Validation / quality checks:** owner_and_scope_present, pass_criteria_objective,
  required_evidence_and_expiry_present, approval_not_inferred
- **Inclusion triggers:** all_projects
- **Omission or combination:** Never omit the concern; Minimal may combine prose with
  requirements, but machine gate records remain separate when present.
- **Representative evidence:** `CF:project-dossier/v0.2/canonical/readiness-criteria.md`;
  `CF:project-dossier/v0.2/machine-readable/approval-gates.yaml`;
  `COE:project-dossier/canonical/readiness-criteria.md`

#### CUR-0001 — Current-state baseline

- **Category / classification:** current_state / core
- **Minimum profile:** minimal
- **Type applicability default:** required — Core artifact type for the selected profile. (`assessed_on`: null; `assessed_by`: null)
- **Purpose:** Record dated, evidence-backed present reality independently of intended state and
  plans.
- **Questions it must answer:** What exists, is absent, is unknown, or differs by environment?;
  What exact subject and method were inspected?
- **Intended audience:** owners, implementers, reviewers, agents
- **Expected owner or maintainer:** current_state_assessor
- **Required inputs:** direct_inspection, source_revision_or_subject_identity,
  executed_commands, evidence
- **Outputs / downstream consumers:** conformance, plans, handoff, risk_assessment
- **Recommended format:** Markdown, optional JSON observations
- **Source-of-truth expectations:** Authoritative only for the stated subject, scope,
  environment, method, and observation time.
- **Dependencies and related artifacts:** VAL-0001, PRV-0001
- **Creation timing:** Create after direct initial inspection, not from scaffold generation.
- **Update triggers:** material_implementation_change, environment_change, evidence_expiry,
  handoff
- **Review cadence:** on_material_change_or_evidence_expiry
- **Validation / quality checks:** observation_time_not_generation_time,
  subject_identity_present, method_and_limits_present, claims_link_evidence
- **Inclusion triggers:** all_projects
- **Omission or combination:** Never omit; before inspection, retain an explicit not_assessed
  state rather than a false dated baseline.
- **Representative evidence:**
  `CF:project-dossier/v0.2/agent-handoff/current-implementation-status.md`;
  `COE:project-dossier/current-state/repository-baseline.md`

#### CNF-0001 — Conformance and gap register

- **Category / classification:** conformance / core
- **Minimum profile:** minimal
- **Type applicability default:** required — Core artifact type for the selected profile. (`assessed_on`: null; `assessed_by`: null)
- **Purpose:** Compare current evidence with canonical requirements using controlled findings.
- **Questions it must answer:** What conforms, differs, is absent, or remains unassessed?; Which
  evidence and requirement support each classification?
- **Intended audience:** owners, implementers, reviewers, agents
- **Expected owner or maintainer:** conformance_assessor
- **Required inputs:** requirements, current_state, validation_evidence
- **Outputs / downstream consumers:** remediation_plans, risk_register, readiness_assessment
- **Recommended format:** Markdown, JSON for Standard and High-Assurance finding records
- **Source-of-truth expectations:** Minimal may own findings in Markdown; Standard and
  High-Assurance own finding records in JSON while Markdown owns method and summary.
- **Dependencies and related artifacts:** REQ-0001, CUR-0001, VAL-0001
- **Creation timing:** Create after the first current-state baseline.
- **Update triggers:** requirement_change, current_state_change, evidence_change,
  remediation_change
- **Review cadence:** on_target_or_evidence_change
- **Validation / quality checks:** finding_ids_stable, requirement_and_evidence_refs_resolve,
  classification_controlled, coverage_disclosed
- **Inclusion triggers:** all_projects
- **Omission or combination:** Never omit; an empty or not_assessed register is valid before
  evidence exists.
- **Representative evidence:** `CF:project-dossier/v0.2/conformance/README.md`;
  `COE:project-dossier/conformance/findings.yaml`

#### PLN-0001 — Dependency-aware implementation or delivery plan

- **Category / classification:** planning / core
- **Minimum profile:** minimal
- **Type applicability default:** required — Core artifact type for the selected profile. (`assessed_on`: null; `assessed_by`: null)
- **Purpose:** Define future work as a hard-dependency graph with gates, structured blockers,
  ownership, reciprocal execution-task links, rollback, and closure evidence.
- **Questions it must answer:** What remains?; Which work is dependency-ready now?; What proves
  completion and what stops or rolls back the work?
- **Intended audience:** executors, owners, reviewers, agents
- **Expected owner or maintainer:** planning_owner
- **Required inputs:** findings, requirements, registers, decisions, gates
- **Outputs / downstream consumers:** task_intake, validation, handoff, resource_coordination
- **Recommended format:** Markdown, JSON for Standard and High-Assurance plan-item records
- **Source-of-truth expectations:** Minimal may own plan items in Markdown; Standard and
  High-Assurance own plan-item records in JSON while Markdown owns method and summary.
- **Dependencies and related artifacts:** CNF-0001, REG-0001, GOV-0001
- **Creation timing:** Create after target/current comparison identifies real work.
- **Update triggers:** finding_change, dependency_change, gate_change, plan_status_change
- **Review cadence:** on_dependency_or_status_change
- **Validation / quality checks:** dependency_graph_acyclic, references_resolve,
  readiness_derived_from_completed_predecessors_passed_or_waived_gates_and_resolved_blockers,
  plan_task_links_reciprocal, completion_links_tasks_and_evidence, authority_not_implied,
  timeline_not_used_as_readiness_or_priority
- **Inclusion triggers:** all_projects
- **Omission or combination:** Never omit the planning entry point; an empty plan is valid and
  generation must not fabricate accepted work.
- **Representative evidence:**
  `CF:project-dossier/v0.2/implementation-plan/dependency-roadmap.md`;
  `COE:project-dossier/implementation-plan/plan.yaml`

#### REG-0001 — RAIDQ register

- **Category / classification:** unresolved_state / core
- **Minimum profile:** minimal
- **Type applicability default:** required — Core artifact type for the selected profile. (`assessed_on`: null; `assessed_by`: null)
- **Purpose:** Own risks, assumptions, issues, dependencies, and open questions with review and
  resolution conditions.
- **Questions it must answer:** What is uncertain, blocking, accepted, expired, or unresolved?;
  Who owns the next review or resolution?
- **Intended audience:** all_project_roles, owners, reviewers
- **Expected owner or maintainer:** register_maintainer
- **Required inputs:** discovery, reviews, incidents, planning
- **Outputs / downstream consumers:** decisions, gates, plans, validation_scope, handoff
- **Recommended format:** Markdown, JSON for Standard and High-Assurance records
- **Source-of-truth expectations:** Minimal may own items in Markdown; Standard and
  High-Assurance own item records in JSON while Markdown owns vocabulary and summary.
- **Dependencies and related artifacts:** PRV-0001, DEC-0001
- **Creation timing:** Create during discovery before silent assumptions accumulate.
- **Update triggers:** item_discovered, status_change, review_date_reached, resolution_evidence
- **Review cadence:** weekly_during_active_work_and_by_each_item_date
- **Validation / quality checks:** stable_ids, type_and_status_controlled,
  owner_and_impact_present, review_or_expiry_and_resolution_condition_present
- **Inclusion triggers:** all_projects
- **Omission or combination:** Never omit; an empty register is valid. Categories may share one
  store when IDs and vocabularies remain explicit.
- **Representative evidence:** `CF:project-dossier/v0.2/implementation-plan/risk-register.md`;
  `COE:project-dossier/registers/`

#### PRV-0001 — Source and provenance index

- **Category / classification:** provenance / core
- **Minimum profile:** minimal
- **Type applicability default:** required — Core artifact type for the selected profile. (`assessed_on`: null; `assessed_by`: null)
- **Purpose:** Identify sources, versions, retrieval or observation dates, rights, sensitivity,
  freshness, and limitations.
- **Questions it must answer:** Where did a consequential claim come from?; May it still be
  relied upon and used for this purpose?
- **Intended audience:** all_evidence_consumers, researchers, reviewers
- **Expected owner or maintainer:** source_curator
- **Required inputs:** project_sources, external_references, imported_assets, methods
- **Outputs / downstream consumers:** requirements, decisions, research, evidence, supply_chain
- **Recommended format:** Markdown, JSON for Standard and High-Assurance source records
- **Source-of-truth expectations:** Minimal may own source records in Markdown; Standard and
  High-Assurance own records in JSON while Markdown owns method and summary.
- **Dependencies and related artifacts:** DOS-0002
- **Creation timing:** Create before a consequential source is relied upon.
- **Update triggers:** source_added, source_version_change, source_expiry,
  rights_or_sensitivity_change, contradiction_found
- **Review cadence:** on_source_change_or_expiry
- **Validation / quality checks:** stable_source_id, locator_and_version_or_date_present,
  use_and_limits_present, freshness_and_rights_assessed_when_applicable
- **Inclusion triggers:** all_projects
- **Omission or combination:** Never omit; private or sensitive locators may be represented by
  safe references rather than exposed values.
- **Representative evidence:** `CF:project-dossier/v0.2/verification/verification-manifest.md`;
  `COE:project-dossier/provenance/source-index.yaml`

#### VAL-0001 — Validation and evidence system

- **Category / classification:** validation_and_evidence / core
- **Minimum profile:** minimal
- **Type applicability default:** required — Core artifact type for the selected profile. (`assessed_on`: null; `assessed_by`: null)
- **Purpose:** Define reproducible validation and index bounded evidence without converting a
  check result into approval.
- **Questions it must answer:** What was checked?; On which exact subject and environment?; What
  result, limitations, freshness rule, and explicit non-proven implications apply?
- **Intended audience:** reviewers, operators, owners, agents
- **Expected owner or maintainer:** validation_owner
- **Required inputs:** requirements, gates, implemented_or_produced_subject, provenance
- **Outputs / downstream consumers:** current_state, findings, readiness_decisions, handoff,
  integrity
- **Recommended format:** Markdown, JSON evidence metadata, generated reports
- **Source-of-truth expectations:** Validation procedure is maintained; executed evidence is
  immutable and scoped. Standard and High-Assurance index evidence metadata in JSON.
- **Dependencies and related artifacts:** REQ-0001, GOV-0001, PRV-0001
- **Creation timing:** Define methods with requirements; create evidence only after observation
  or execution.
- **Update triggers:** requirement_or_validator_change, evidence_recorded,
  evidence_expired_or_superseded
- **Review cadence:** on_validation_contract_or_evidence_change
- **Validation / quality checks:** method_reproducible, subject_fingerprint_present,
  time_environment_scope_result_and_limits_present, freshness_enforced,
  consequential_claims_name_non_proven_implications
- **Inclusion triggers:** all_projects
- **Omission or combination:** Never omit the validation entry point; the evidence index may be
  empty before checks run.
- **Representative evidence:**
  `CF:project-dossier/v0.2/machine-readable/validation-report.json`;
  `COE:project-dossier/validation/validation-report.json`

#### HOF-0001 — Handoff and resumption pack

- **Category / classification:** handoff / core
- **Minimum profile:** minimal
- **Type applicability default:** required — Core artifact type for the selected profile. (`assessed_on`: null; `assessed_by`: null)
- **Purpose:** Provide a bounded current view, exact revision, blockers, evidence pointers, and
  next safe action.
- **Questions it must answer:** What is active and blocked?; What evidence is fresh?; What
  should the next maintainer inspect or do first?
- **Intended audience:** incoming_maintainers, agents, reviewers
- **Expected owner or maintainer:** current_task_owner
- **Required inputs:** active_tasks, accepted_decisions, current_evidence, registers,
  exact_revision
- **Outputs / downstream consumers:** resumption, review, transition
- **Recommended format:** Markdown
- **Source-of-truth expectations:** Derived navigation only; links to mutable owners and never
  becomes a second status store.
- **Dependencies and related artifacts:** DEC-0001, CUR-0001, PLN-0001, REG-0001, VAL-0001
- **Creation timing:** Create before the first multi-session handoff.
- **Update triggers:** active_task_change, blocker_change, evidence_change, handoff
- **Review cadence:** before_every_handoff
- **Validation / quality checks:** compact_and_link_based, exact_revision_present,
  pointers_resolve, stale_or_unknown_state_disclosed
- **Inclusion triggers:** all_multi_session_projects, all_generated_profiles
- **Omission or combination:** Never omit for multi-session work; a truly single-session project
  may combine it with DOS-0001 while preserving separate state labels.
- **Representative evidence:** `CF:project-dossier/v0.2/agent-handoff/START_HERE.md`;
  `COE:project-dossier/handoff/START_HERE.md`

#### HOF-0002 — Adoption checklist

- **Category / classification:** handoff_and_adoption / core
- **Minimum profile:** minimal
- **Type applicability default:** required — Core artifact type for the selected profile. (`assessed_on`: null; `assessed_by`: null)
- **Purpose:** Track conversion of a generated structure into an adopted project dossier and
  harness without implying readiness.
- **Questions it must answer:** Which adoption steps are complete?; Which project facts, owners,
  checks, and extensions remain unresolved?
- **Intended audience:** project_owners, bootstrap_maintainers, reviewers
- **Expected owner or maintainer:** project_owner
- **Required inputs:** selected_profile, project_inspection, adoption_decisions,
  validation_results
- **Outputs / downstream consumers:** handoff, adoption_review, upgrade_planning
- **Recommended format:** Markdown checklist
- **Source-of-truth expectations:** Tracking aid only; checked boxes do not create authority or
  substantive evidence.
- **Dependencies and related artifacts:** DOS-0010, CUR-0001, VAL-0001
- **Creation timing:** Seed during generation and maintain through initial adoption or upgrade.
- **Update triggers:** adoption_progress, profile_change, upgrade
- **Review cadence:** during_adoption_and_before_adoption_closeout
- **Validation / quality checks:** all_profile_triggers_assessed, unknowns_and_skips_disclosed,
  real_project_checks_distinguished_from_structure
- **Inclusion triggers:** all_generated_or_upgraded_projects
- **Omission or combination:** May be archived after adoption is demonstrably complete; keep its
  outcome or successor in history when assurance requires.
- **Representative evidence:** `CF:project-dossier/v0.2/transition/adoption-checklist.md`;
  Recommended: generalized adoption gate

#### MOD-0001 — Domain models, workflows, interfaces, and schemas

- **Category / classification:** domain_model / conditional
- **Minimum profile:** high-assurance
- **Type applicability default:** not_assessed — Generation does not establish trigger applicability. (`assessed_on`: null; `assessed_by`: null)
- **Purpose:** Specify specialist entities, states, interfaces, handoffs, and controlled
  vocabularies beyond the core outcome model.
- **Questions it must answer:** Which domain concepts and transitions require precise
  contracts?; Where are interface and ownership boundaries?
- **Intended audience:** domain_owners, implementers, reviewers
- **Expected owner or maintainer:** domain_owner
- **Required inputs:** architecture_or_outcome_model, requirements, accepted_decisions
- **Outputs / downstream consumers:** implementation, validation, operations, extensions
- **Recommended format:** Markdown, JSON, diagram, schema
- **Source-of-truth expectations:** Each model declares its edit source; generated diagrams or
  mirrors point to that source.
- **Dependencies and related artifacts:** ARC-0001, REQ-0001, DEC-0001
- **Creation timing:** Create when domain complexity exceeds the core architecture or outcome
  model.
- **Update triggers:** entity_change, workflow_change, interface_change, vocabulary_change
- **Review cadence:** on_model_change
- **Validation / quality checks:** requirements_and_decision_refs_resolve,
  states_and_interfaces_consistent, source_direction_declared
- **Inclusion triggers:** multiple_entities_or_states, multiple_interfaces_or_suppliers,
  formal_handoffs
- **Omission or combination:** Omit when ARC-0001 answers all domain questions without
  ambiguity.
- **Representative evidence:** `CF:project-dossier/v0.2/canonical/domain-data-model.md`;
  `COE:project-dossier/canonical/portfolio-and-content-model.md`

#### SEC-0001 — Trust, security, privacy, legal, and compliance model

- **Category / classification:** specialist_governance / conditional
- **Minimum profile:** high-assurance
- **Type applicability default:** not_assessed — Generation does not establish trigger applicability. (`assessed_on`: null; `assessed_by`: null)
- **Purpose:** Define applicable trust boundaries, threats, controls, obligations, specialist
  gates, and residual risks.
- **Questions it must answer:** What sensitive or regulated interests exist?; Which qualified
  reviews and controls are required?; What remains unresolved?
- **Intended audience:** security_privacy_legal_or_compliance_owners, project_owners, reviewers
- **Expected owner or maintainer:** qualified_governance_owner
- **Required inputs:** data_and_effect_inventory, requirements, risk_register,
  applicable_obligations
- **Outputs / downstream consumers:** gates, architecture, operations, validation, handoff
- **Recommended format:** Markdown, threat_model, JSON control register
- **Source-of-truth expectations:** Canonical specialist criteria and models; no generated
  template establishes a qualified conclusion.
- **Dependencies and related artifacts:** GOV-0001, REG-0001, DAT-0001
- **Creation timing:** Create before handling sensitive data, credentials, regulated activity,
  public claims, money, or external effects.
- **Update triggers:** threat_or_obligation_change, data_flow_change, external_effect_change,
  incident
- **Review cadence:** on_risk_or_obligation_change_and_at_specialist_gate
- **Validation / quality checks:** qualified_owner_named, scope_and_controls_trace_requirements,
  residual_risks_and_exceptions_explicit, no_inferred_legal_conclusion
- **Inclusion triggers:** sensitive_data, credentials, regulated_activity, public_claims, money,
  external_effects
- **Omission or combination:** Omit only after triggers are explicitly assessed as not
  applicable; related low-risk criteria may be combined with GOV-0001.
- **Representative evidence:** `CF:project-dossier/v0.2/canonical/security-architecture.md`;
  `COE:project-dossier/canonical/security-privacy-legal.md`

#### OPS-0001 — Operations, release, incident, and recovery runbooks

- **Category / classification:** operations / conditional
- **Minimum profile:** high-assurance
- **Type applicability default:** not_assessed — Generation does not establish trigger applicability. (`assessed_on`: null; `assessed_by`: null)
- **Purpose:** Provide executable, exercised procedures for recurring operations and failure
  recovery.
- **Questions it must answer:** How is the outcome operated, released, rolled back, restored, or
  retired?; What evidence proves the procedure works?
- **Intended audience:** operators, release_owners, incident_responders, reviewers
- **Expected owner or maintainer:** operations_owner
- **Required inputs:** architecture, risk_model, environment_inventory, gates
- **Outputs / downstream consumers:** operational_execution, recovery_testing, handoff,
  readiness_assessment
- **Recommended format:** Markdown, executable_procedure, checklist
- **Source-of-truth expectations:** Project-maintained procedures; execution evidence is
  separate and dated.
- **Dependencies and related artifacts:** ARC-0001, GOV-0001, SEC-0001, VAL-0001
- **Creation timing:** Create before deployment, publication, ongoing service, operator handoff,
  or irreversible effect.
- **Update triggers:** deployment_model_change, incident, recovery_change, provider_change,
  retirement
- **Review cadence:** quarterly_and_per_release_or_material_change
- **Validation / quality checks:** owner_and_prerequisites_present,
  rollback_or_stop_path_present, exercise_evidence_fresh, secrets_not_embedded
- **Inclusion triggers:** deployment, publication, ongoing_service,
  external_or_irreversible_effect
- **Omission or combination:** Omit before operations exist; combine small related procedures
  only when owners, triggers, and evidence remain clear.
- **Representative evidence:**
  `CF:project-dossier/v0.2/canonical/monitoring-lifecycle-model.md`;
  `COE:project-dossier/canonical/seo-analytics-and-operations.md`

#### RES-0001 — External-fact research and verification

- **Category / classification:** research / conditional
- **Minimum profile:** high-assurance
- **Type applicability default:** not_assessed — Generation does not establish trigger applicability. (`assessed_on`: null; `assessed_by`: null)
- **Purpose:** Record mutable external facts, source comparison, contradictions, verdicts, and
  reverification deadlines.
- **Questions it must answer:** Which external facts affect decisions?; When and how were they
  verified?; When do they expire?
- **Intended audience:** researchers, decision_owners, reviewers
- **Expected owner or maintainer:** research_owner
- **Required inputs:** source_index, research_question, primary_sources
- **Outputs / downstream consumers:** decisions, requirements, risk_register, supply_chain
- **Recommended format:** Markdown, JSON source_and_verdict_records
- **Source-of-truth expectations:** Research records own bounded findings; source identity and
  freshness remain in provenance.
- **Dependencies and related artifacts:** PRV-0001, REG-0001
- **Creation timing:** Create before a mutable external fact drives a consequential choice.
- **Update triggers:** external_fact_used, source_changed_or_expired, contradiction_found
- **Review cadence:** by_recorded_reverification_deadline
- **Validation / quality checks:** primary_sources_preferred, retrieval_date_and_scope_present,
  contradictions_and_limits_disclosed, expiry_enforced
- **Inclusion triggers:** mutable_external_facts_affect_requirements_decisions_or_operations
- **Omission or combination:** Omit when no consequential mutable external fact is used; small
  research notes may live with provenance if conclusions and expiry remain explicit.
- **Representative evidence:**
  `CF:project-dossier/v0.2/verification/etsy-reverification-2026-07-23.md`;
  `COE:project-dossier/provenance/`

#### TRN-0001 — Transition and migration package

- **Category / classification:** transition / conditional
- **Minimum profile:** high-assurance
- **Type applicability default:** not_assessed — Generation does not establish trigger applicability. (`assessed_on`: null; `assessed_by`: null)
- **Purpose:** Control adoption, replacement, split, merge, and version migration without
  silently overwriting authority or history.
- **Questions it must answer:** What changes and what remains authoritative?; How is
  compatibility, rollback, and acceptance demonstrated?
- **Intended audience:** transition_owners, maintainers, reviewers, agents
- **Expected owner or maintainer:** transition_owner
- **Required inputs:** current_inventory, candidate_target, authority_delta,
  migration_constraints
- **Outputs / downstream consumers:** implementation_plan, supersession, history, handoff
- **Recommended format:** Markdown, JSON crosswalk
- **Source-of-truth expectations:** Project-maintained migration intent and crosswalk; execution
  evidence and accepted decisions remain separate.
- **Dependencies and related artifacts:** DOS-0007, CUR-0001, CNF-0001, PLN-0001
- **Creation timing:** Create before changing an established project, dossier, harness,
  architecture, or major version.
- **Update triggers:** existing_project_adoption, blueprint_upgrade, replacement, split_or_merge
- **Review cadence:** throughout_transition_and_at_acceptance
- **Validation / quality checks:** authority_delta_complete,
  path_and_concept_crosswalk_complete, rollback_present, supersession_verified
- **Inclusion triggers:** established_project_adoption, replacement, split_or_merge,
  major_version_upgrade
- **Omission or combination:** Omit for an empty new project with no predecessor.
- **Representative evidence:**
  `CF:project-dossier/v0.2/transition/DEVELOPMENT_TRANSITION_v0_1_TO_v0_2.md`; Recommended: no
  direct COE transition package equivalent

#### HIS-0001 — Immutable historical baseline

- **Category / classification:** history / conditional
- **Minimum profile:** high-assurance
- **Type applicability default:** not_assessed — Generation does not establish trigger applicability. (`assessed_on`: null; `assessed_by`: null)
- **Purpose:** Retain noncurrent evidence or baselines for audit, recovery, provenance, or
  regulated retention.
- **Questions it must answer:** What historical snapshot is retained?; Why and for how long?;
  Which current successor replaces it?
- **Intended audience:** auditors, maintainers, recovery_owners
- **Expected owner or maintainer:** dossier_custodian
- **Required inputs:** retention_decision, supersession_record, frozen_inventory
- **Outputs / downstream consumers:** audit, recovery, provenance, migration
- **Recommended format:** frozen_directory, manifest, checksum_set, Markdown index
- **Source-of-truth expectations:** Explicitly noncurrent immutable history; current authority
  always routes to a successor.
- **Dependencies and related artifacts:** DOS-0005, DOS-0007
- **Creation timing:** Create when a retained baseline or superseded evidence set is required.
- **Update triggers:** baseline_archived, artifact_superseded, retention_rule_change
- **Review cadence:** on_archive_or_retention_event
- **Validation / quality checks:** noncurrent_banner_present, manifest_and_checksum_scope_exact,
  successor_link_resolves, retention_rule_recorded
- **Inclusion triggers:** audit_or_regulatory_retention, release_baseline, recovery_need,
  supersession_history
- **Omission or combination:** Omit when version control and ordinary supersession records fully
  satisfy retention and recovery needs.
- **Representative evidence:** `CF:project-dossier/v0.2/baseline/README.md`; Recommended: COE
  generated integrity is current evidence, not a historical-baseline equivalent

#### DAT-0001 — Data classification, lifecycle, and retention model

- **Category / classification:** data_governance / conditional
- **Minimum profile:** high-assurance
- **Type applicability default:** not_assessed — Generation does not establish trigger applicability. (`assessed_on`: null; `assessed_by`: null)
- **Purpose:** Classify sensitive, personal, confidential, licensed, regulated, or production
  data across collection, flow, retention, and deletion.
- **Questions it must answer:** What data exists and where does it flow?; How is it classified,
  retained, minimized, and deleted?; Who owns each decision?
- **Intended audience:** data_owners, security_privacy_reviewers, operators
- **Expected owner or maintainer:** data_owner
- **Required inputs:** data_inventory, architecture_flows, applicable_obligations, risk_model
- **Outputs / downstream consumers:** security_model, operations, validation,
  retention_and_deletion_controls
- **Recommended format:** JSON, Markdown, data_flow_diagram
- **Source-of-truth expectations:** Canonical project-specific classification and lifecycle
  model; no real data values belong in the dossier.
- **Dependencies and related artifacts:** ARC-0001, SEC-0001, PRV-0001
- **Creation timing:** Create before collecting or importing triggered data classes.
- **Update triggers:** data_class_or_flow_change, retention_change, provider_change, incident
- **Review cadence:** on_data_flow_or_obligation_change_and_at_least_quarterly_when_active
- **Validation / quality checks:** stores_and_flows_covered, classification_and_owner_present,
  retention_deletion_and_minimization_tested, no_sensitive_values_embedded
- **Inclusion triggers:** personal_data, confidential_data, licensed_data, regulated_data,
  production_data
- **Omission or combination:** Omit only after data triggers are assessed as not applicable; a
  small low-risk inventory may combine with SEC-0001.
- **Representative evidence:** `CF:project-dossier/v0.2/canonical/domain-data-model.md`;
  `COE:project-dossier/canonical/security-privacy-legal.md`; Recommended: generalized lifecycle
  model

#### SUP-0001 — Supply-chain, dependency, vendor, and license inventory

- **Category / classification:** supply_chain / conditional
- **Minimum profile:** high-assurance
- **Type applicability default:** not_assessed — Generation does not establish trigger applicability. (`assessed_on`: null; `assessed_by`: null)
- **Purpose:** Track external code, models, content, datasets, packages, services, vendors,
  versions, licenses, provenance, and update risk.
- **Questions it must answer:** Which external inputs are relied upon?; Under what version,
  license, rights, and trust assumptions?; How are updates and vulnerabilities handled?
- **Intended audience:** supply_chain_owner, security_legal_reviewers, maintainers
- **Expected owner or maintainer:** supply_chain_owner
- **Required inputs:** dependency_inventory, source_index, licenses_and_terms,
  provider_assessments
- **Outputs / downstream consumers:** security_gates, release, operations, provenance,
  reproducibility
- **Recommended format:** SBOM, JSON, Markdown
- **Source-of-truth expectations:** Machine inventory should be generated from lockfiles or
  declared sources where possible; judgments and exceptions remain project-maintained.
- **Dependencies and related artifacts:** PRV-0001, SEC-0001, RES-0001
- **Creation timing:** Create before relying on external code, content, models, data, packages,
  or vendors.
- **Update triggers:** dependency_or_vendor_change, license_change, vulnerability, source_expiry
- **Review cadence:** on_dependency_change_and_per_release
- **Validation / quality checks:** versions_and_sources_exact, licenses_and_rights_recorded,
  vulnerability_and_update_policy_present, generated_inventory_fresh
- **Inclusion triggers:** external_code, models, content, datasets, packages,
  vendors_or_services
- **Omission or combination:** Omit only when the project has no external supply-chain input;
  very small inventories may combine with provenance.
- **Representative evidence:** `CF:project-dossier/v0.2/verification/verification-manifest.md`;
  `COE:project-dossier/provenance/source-index.yaml`; Recommended: portable supply-chain
  inventory

#### EVA-0001 — Quality rubric and evaluation suite

- **Category / classification:** evaluation / optional
- **Minimum profile:** high-assurance
- **Type applicability default:** not_assessed — Generation does not establish trigger applicability. (`assessed_on`: null; `assessed_by`: null)
- **Purpose:** Make repeated subjective, model-assisted, or high-impact quality review
  reproducible.
- **Questions it must answer:** What quality dimensions and thresholds apply?; Which fixtures,
  raters, and limitations make evaluation repeatable?
- **Intended audience:** quality_owners, reviewers, agent_operators
- **Expected owner or maintainer:** quality_owner
- **Required inputs:** requirements, quality_risks, representative_fixtures, scoring_method
- **Outputs / downstream consumers:** validation, agent_workflows, readiness_gates,
  continuous_improvement
- **Recommended format:** Markdown, JSON, tests, fixtures
- **Source-of-truth expectations:** Versioned rubric and fixtures own evaluation semantics;
  generated scores are point-in-time evidence.
- **Dependencies and related artifacts:** REQ-0001, VAL-0001, GOV-0001
- **Creation timing:** Create when quality judgments recur or material consequences justify
  calibrated evaluation.
- **Update triggers:** quality_standard_change, model_or_process_change, fixture_drift,
  evaluation_failure
- **Review cadence:** per_material_method_change_and_periodic_calibration
- **Validation / quality checks:** rubric_versioned, fixtures_representative_and_safe,
  scoring_reproducible, limitations_and_rater_variance_disclosed
- **Inclusion triggers:** repeated_agent_work, subjective_quality_review, model_evaluation,
  high_impact_review
- **Omission or combination:** Omit when ordinary objective validation is sufficient; combine
  with VAL-0001 only if rubric versioning and fixtures remain explicit.
- **Representative evidence:**
  `CF:project-dossier/v0.2/agent-handoff/evaluations/task-quality-rubric.md`; Recommended: no
  direct COE evaluation-suite equivalent

#### CTX-0001 — Bounded context packs

- **Category / classification:** agent_context / optional
- **Minimum profile:** high-assurance
- **Type applicability default:** not_assessed — Generation does not establish trigger applicability. (`assessed_on`: null; `assessed_by`: null)
- **Purpose:** Package selectively loaded, size-bounded, versioned context for a declared
  purpose and consumer without duplicating authority or permission.
- **Questions it must answer:** What exact purpose, consumer, task class, and scope apply?; Which
  exact source versions and authority states does it reference?; When does it expire, require
  revalidation, become invalid or revoked, and require deletion?; Which sensitivity and use
  restrictions apply?; What is excluded and what does possession of the pack not prove?
- **Intended audience:** agents, specialist_maintainers, reviewers
- **Expected owner or maintainer:** dossier_maintainer
- **Required inputs:** task_routing_needs, intended_consumer, task_class, bounded_scope,
  exact_source_versions_and_authority_status, context_budget, sensitivity_and_allowed_use,
  validity_and_revalidation, retention_and_deletion, owner_and_limitations
- **Outputs / downstream consumers:** agent_skills, workflows, handoff
- **Recommended format:** Markdown navigation plus a manifest conforming to
  `project-blueprint.context-pack-manifest.v1` when the type is applicable
- **Source-of-truth expectations:** Derived or curated navigation only; packs may narrow context
  but never replace sources or expand authority.
- **Dependencies and related artifacts:** DOS-0003, HOF-0001
- **Creation timing:** Create when the dossier is too large for reliable routine loading or
  specialist routing recurs.
- **Update triggers:** source_change, task_pattern_change, context_budget_breach, staleness,
  validity_expiry, invalidation_trigger, revocation, consumer_or_use_change,
  sensitivity_or_retention_change
- **Review cadence:** on_source_change_and_quarterly_when_active
- **Validation / quality checks:** identity_and_version_present, purpose_consumer_task_and_scope_exact,
  source_refs_versions_and_authority_status_exact, creation_freshness_validity_and_revalidation_valid,
  sensitivity_and_allowed_use_enforced, retention_and_deletion_explicit,
  invalidation_and_revocation_enforced, exclusions_and_size_budget_enforced, owner_and_limits_present,
  permission_grant_false, no_authority_expansion_or_mutable_fact_duplication
- **Inclusion triggers:** large_dossier, specialist_routing, repeated_agent_work
- **Omission or combination:** Omit when the dossier index and handoff already provide
  sufficient bounded context. Generation supplies only the High-Assurance optional schema and
  an unassessed entry point; it never creates a manifest or adopts CTX-0001.
- **Representative evidence:** `CF:project-dossier/v0.2/agent-handoff/context-packs/`; Inferred:
  COE compact handoff demonstrates bounded routing without separate packs

### 4.4 Physical representation crosswalk

This table is the complete blueprint-source mapping. `Profile` means the
smallest scaffold that includes the representation, not proof that a
conditional type applies. A combined representation lists multiple type IDs
and records `combined` applicability with a rationale in the project registry.

| Representation | Artifact type(s) | Path | Profile | Role | Source direction | Default applicability | Legacy v1 ID |
|---|---|---|---|---|---|---|---|
| `REP-0001` | `DOS-0001` | `project-dossier/README.md` | `minimal` | `navigation` | `navigation_only` | `required` | `DOS-0001` |
| `REP-0002` | `DOS-0002` | `project-dossier/AUTHORITY.md` | `minimal` | `interpretation_source` | `project_maintained_source` | `required` | `DOS-0002` |
| `REP-0003` | `DOS-0003` | `project-dossier/CANONICAL_SOURCE_MAP.md` | `minimal` | `source_map` | `project_maintained_source` | `required` | `DOS-0003` |
| `REP-0004` | `DOS-0004` | `project-dossier/ARTIFACT_CATALOG.json` | `minimal` | `generated_catalog` | `generated_from_artifact_registry` | `required` | `DOS-0004` |
| `REP-0005` | `DOS-0005` | `project-dossier/MANIFEST.json` | `minimal` | `generated_manifest` | `generated_from_managed_files` | `required` | `DOS-0005` |
| `REP-0006` | `DOS-0006` | `project-dossier/VERSION.md` | `minimal` | `version_source` | `project_maintained_source_seeded_by_generator` | `required` | `DOS-0006` |
| `REP-0007` | `DOS-0007` | `project-dossier/SUPERSESSION.json` | `minimal` | `lifecycle_source` | `project_maintained_source_seeded_by_generator` | `required` | `DOS-0007` |
| `REP-0008` | `DOS-0008` | `project-dossier/machine-readable/path-authority.json` | `minimal` | `generated_path_authority` | `generated_from_artifact_registry` | `required` | `DOS-0008` |
| `REP-0009` | `DOS-0005` | `project-dossier/CHECKSUMS.sha256` | `high-assurance` | `generated_checksums` | `generated_from_managed_files` | `not_assessed` | `DOS-0009` |
| `REP-0010` | `DEF-0001` | `project-dossier/canonical/executive-project-definition.md` | `minimal` | `canonical_human_source` | `project_maintained_source_seeded_by_generator` | `required` | `DEF-0001` |
| `REP-0011` | `REQ-0001` | `project-dossier/canonical/requirements-and-constraints.md` | `minimal` | `canonical_human_source` | `profile_dependent_record_source` | `required` | `REQ-0001` |
| `REP-0012` | `REQ-0001` | `project-dossier/machine-readable/requirements.json` | `standard` | `structured_record_source` | `authoritative_when_present` | `required` | `REQ-0002` |
| `REP-0013` | `ARC-0001` | `project-dossier/canonical/architecture-or-outcome-model.md` | `minimal` | `canonical_human_source` | `project_maintained_source_seeded_by_generator` | `required` | `ARC-0001` |
| `REP-0014` | `DEC-0001` | `.agent/decisions/README.md` | `minimal` | `external_live_store_navigation` | `external_live_store_navigation` | `required` | `DEC-0001` |
| `REP-0015` | `GOV-0001` | `project-dossier/canonical/constraints-gates-and-readiness.md` | `minimal` | `canonical_human_source` | `project_maintained_source_seeded_by_generator` | `required` | `GOV-0001` |
| `REP-0016` | `CUR-0001` | `project-dossier/current-state/README.md` | `minimal` | `current_state_source` | `project_maintained_source_seeded_by_generator` | `required` | `CUR-0001` |
| `REP-0017` | `CNF-0001` | `project-dossier/conformance/README.md` | `minimal` | `method_and_summary_source` | `profile_dependent_record_source` | `required` | `CNF-0001` |
| `REP-0018` | `CNF-0001` | `project-dossier/machine-readable/findings.json` | `standard` | `structured_record_source` | `authoritative_when_present` | `required` | `CNF-0002` |
| `REP-0019` | `PLN-0001` | `project-dossier/plans/README.md` | `minimal` | `method_and_summary_source` | `profile_dependent_record_source` | `required` | `PLN-0001` |
| `REP-0020` | `PLN-0001` | `project-dossier/machine-readable/plan.json` | `standard` | `structured_record_source` | `authoritative_when_present` | `required` | `PLN-0002` |
| `REP-0021` | `REG-0001` | `project-dossier/registers/README.md` | `minimal` | `method_and_summary_source` | `profile_dependent_record_source` | `required` | `REG-0001` |
| `REP-0022` | `REG-0001` | `project-dossier/machine-readable/raidq.json` | `standard` | `structured_record_source` | `authoritative_when_present` | `required` | `REG-0002` |
| `REP-0023` | `PRV-0001` | `project-dossier/provenance/README.md` | `minimal` | `method_and_summary_source` | `profile_dependent_record_source` | `required` | `PRV-0001` |
| `REP-0024` | `PRV-0001` | `project-dossier/machine-readable/sources.json` | `standard` | `structured_record_source` | `authoritative_when_present` | `required` | `PRV-0002` |
| `REP-0025` | `VAL-0001` | `project-dossier/validation/README.md` | `minimal` | `validation_method_source` | `project_maintained_source_seeded_by_generator` | `required` | `VAL-0001` |
| `REP-0026` | `GOV-0001` | `project-dossier/validation/QUALITY_GATES.json` | `minimal` | `proposed_gate_record_source` | `project_maintained_source_seeded_by_generator` | `required` | `VAL-0002` |
| `REP-0027` | `VAL-0001` | `project-dossier/machine-readable/evidence-index.json` | `standard` | `structured_record_source` | `authoritative_when_present` | `required` | `VAL-0003` |
| `REP-0028` | `HOF-0001` | `project-dossier/handoff/START_HERE.md` | `minimal` | `handoff_view` | `derived_navigation_maintained_by_task_owner` | `required` | `HOF-0001` |
| `REP-0029` | `HOF-0002` | `project-dossier/handoff/ADOPTION_CHECKLIST.md` | `minimal` | `adoption_checklist` | `project_maintained_source_seeded_by_generator` | `required` | `HOF-0002` |
| `REP-0030` | `SEC-0001` | `project-dossier/governance/README.md` | `high-assurance` | `conditional_entry_point` | `conditional_project_maintained_source` | `not_assessed` | `GOV-0002` |
| `REP-0031` | `MOD-0001` | `project-dossier/models/README.md` | `high-assurance` | `conditional_entry_point` | `conditional_project_maintained_source` | `not_assessed` | `MOD-0001` |
| `REP-0032` | `OPS-0001` | `project-dossier/operations/README.md` | `high-assurance` | `conditional_entry_point` | `conditional_project_maintained_source` | `not_assessed` | `OPS-0001` |
| `REP-0033` | `RES-0001` | `project-dossier/research/README.md` | `high-assurance` | `conditional_entry_point` | `conditional_project_maintained_source` | `not_assessed` | `RES-0001` |
| `REP-0034` | `TRN-0001` | `project-dossier/transition/README.md` | `high-assurance` | `conditional_entry_point` | `conditional_project_maintained_source` | `not_assessed` | `TRN-0001` |
| `REP-0035` | `HIS-0001` | `project-dossier/history/README.md` | `high-assurance` | `conditional_entry_point` | `conditional_project_maintained_source` | `not_assessed` | `HIS-0001` |
| `REP-0036` | `DOS-0010` | `project-dossier/machine-readable/artifact-registry.json` | `minimal` | `authoritative_registry` | `project_maintained_source_seeded_by_generator` | `required` | `—` |
| `REP-0037` | `DAT-0001` | `project-dossier/data/README.md` | `high-assurance` | `conditional_entry_point` | `conditional_project_maintained_source` | `not_assessed` | `—` |
| `REP-0038` | `SUP-0001` | `project-dossier/supply-chain/README.md` | `high-assurance` | `conditional_entry_point` | `conditional_project_maintained_source` | `not_assessed` | `—` |
| `REP-0039` | `EVA-0001` | `project-dossier/evaluation/README.md` | `high-assurance` | `conditional_entry_point` | `conditional_project_maintained_source` | `not_assessed` | `—` |
| `REP-0040` | `CTX-0001` | `project-dossier/context-packs/README.md` | `high-assurance` | `conditional_entry_point` | `conditional_project_maintained_source` | `not_assessed` | `—` |

## 5. Coverage profiles

**[Recommended]** Profiles are cumulative starting structures, not readiness
levels.

### Minimal viable dossier

Appropriate for a new, small, low-risk project with one principal context.

Required artifacts:

- DOS-0001 through DOS-0008 and DOS-0010;
- DEF-0001, REQ-0001, ARC-0001, DEC-0001;
- GOV-0001 combined with requirements if desired;
- CUR-0001, CNF-0001, PLN-0001, REG-0001;
- PRV-0001, VAL-0001, HOF-0001, HOF-0002.

Human-readable files may combine related concerns, but the artifact catalog
must preserve their distinct roles. The project-local artifact registry is
the metadata edit source; catalog, path-authority, and manifest outputs are
refreshable in every profile.

### Standard dossier

Use when active work needs structured traceability, durable evidence and review
records, or comparable information-governance controls. Contributor count by
itself is not a profile trigger.

Adds:

- authoritative JSON registries for requirements, findings, plans, RAIDQ,
  sources, and evidence;
- explicit review cadence and owners;
- traceability, dependency readiness, and a read-only ready-frontier derivation;
- evidence and handoff maintenance checks; and
- project extensions when domain rules are consumed mechanically, including
  disabled and unassessed operations/observability and security/supply-chain
  entry points that validate project-owned declarations without supplying
  operational or assurance facts.

### High-assurance or agent-operable dossier

Appropriate when external effects, sensitive information, regulated work,
multiple environments, protected coordination, long-lived agent operation or
handoff, audit, or reproducibility applies. Ordinary small-team concurrency by
itself is handled by the harness workflow modifier and does not require this
profile.

Adds every triggered conditional artifact plus:

- generated manifest, checksums, source fingerprint, and freshness report;
- immutable baseline and supersession controls;
- recovery and interrupted-refresh tests;
- independent CI or protected validation where risk warrants;
- data, supply-chain, approval, and retention evidence; and
- context/evaluation packages for repeated agent work. The Context Pack schema
  is available for a triggered CTX-0001 assessment, but no pack manifest is
  generated and schema presence does not establish applicability.

The scaffold includes trigger-assessment entry points for every conditional
and optional conceptual type, each initially `not_assessed`. An omitted type
remains in the registry as a dated, attributed `not_applicable` decision even
after its physical representation is removed. High Assurance is achieved only
after applicable triggers are resolved, applicable controls link current
evidence and reviewed representations, and its project-owned acceptance
demonstrations pass. The generated read-only check rejects an adopted
High-Assurance status while these trigger contracts remain unresolved; it
still cannot make a qualified security, privacy, legal, compliance, or
production-readiness conclusion.

## 6. Recommended directory structure

**[Recommended]** The reusable physical layout is:

```text
project-dossier/
├── README.md
├── AUTHORITY.md
├── CANONICAL_SOURCE_MAP.md
├── ARTIFACT_CATALOG.json               # generated registry mirror
├── MANIFEST.json                       # generated
├── CHECKSUMS.sha256                    # High Assurance, generated
├── VERSION.md
├── SUPERSESSION.json
├── canonical/
│   ├── executive-project-definition.md
│   ├── requirements-and-constraints.md
│   ├── architecture-or-outcome-model.md
│   └── constraints-gates-and-readiness.md
├── current-state/
├── conformance/
├── plans/
├── registers/
├── provenance/
├── validation/
├── handoff/
├── machine-readable/
│   ├── artifact-registry.json          # authoritative metadata source
│   ├── requirements.json
│   ├── findings.json
│   ├── plan.json
│   ├── raidq.json
│   ├── sources.json
│   ├── evidence-index.json
│   └── path-authority.json             # generated from registry
├── governance/                         # conditional SEC-0001
├── data/                               # conditional DAT-0001
├── models/                             # conditional
├── operations/                         # conditional
├── research/                           # conditional
├── supply-chain/                       # conditional SUP-0001
├── evaluation/                         # optional EVA-0001
├── context-packs/                      # optional CTX-0001
├── transition/                         # conditional
└── history/                            # conditional immutable records
```

Naming conventions:

- lower-kebab-case descriptive filenames;
- typed stable IDs: conceptual artifact types, `REP-####` representations, and
  schema-governed record instances;
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

**[Recommended]** The following outlines and field contracts make the taxonomy
directly implementable.

Recommended concise outlines:

| Artifact | Required sections |
|---|---|
| DOS-0001 | purpose/boundary; reading order; current pointers; layer map; freshness |
| DOS-0002 | role; precedence; path classes; conflict rules; non-authority rules |
| DOS-0003 | concern-to-source table; mirror direction; change route; conflicts |
| DOS-0004 | generated-on/generation ID; normalized type and representation entries; registry source fingerprint |
| DOS-0005 | generation ID/time; scope/exclusions; file digests; limitations |
| DOS-0006 | current version; adoption state; effective date; change summary; migration |
| DOS-0007 | predecessor; successor; effective date; reason; migration; retained history |
| DOS-0008 | path; representation ID; artifact-type IDs; state; authority; source direction; generated flag |
| DOS-0010 | registry role; types; representations; applicability; review; source direction; supersession |
| DEF-0001 | identity; problem; intended outcome; in/out scope; audiences; owners; success |
| REQ-0001 | vocabulary; active/proposed requirements; constraints; traceability |
| ARC-0001 | context; actors; components/workstreams; boundaries; flows; states; failure behavior |
| DEC-0001 | context; options; decision; authority; consequences; validation; successor |
| GOV-0001 | constraints; gate catalog; approval sources; readiness criteria; exceptions |
| CUR-0001 | subject; time/environment; method; present/absent/unknown; evidence; limitations |
| CNF-0001 | method; classification; findings; coverage; unresolved assessment |
| PLN-0001 | objective; hard dependency graph; work items; reciprocal tasks; gates; structured blockers; derived ready frontier; evidence; stop/rollback |
| REG-0001 | vocabularies; items; owners; impact; review/expiry; resolution |
| PRV-0001 | source classes; source records; rights/sensitivity; freshness; contradictions |
| VAL-0001 | commands/methods; evidence schema; results; limitations; freshness |
| HOF-0001 | current task; exact revision; recent evidence; blockers; next action; reading order |
| HOF-0002 | profile; adoption steps; project checks; unresolved items; closeout evidence |

### Structured field schemas

The strict JSON Schemas are versioned under generated `.agent/schemas/`. These
concise field contracts are sufficient to create equivalent stores in another
storage system:

| Structure | Required fields |
|---|---|
| Artifact type | `id`; `recommended_name`; `category`; `classification`; minimum `profile`; durable `applicability` with status/rationale/date/assessor; `purpose`; `questions`; `intended_audiences`; `owner_role`; `required_inputs`; `downstream_consumers`; `recommended_formats`; `source_of_truth_expectations`; `dependencies`; `creation_timing`; `update_triggers`; `review_cadence`; `validation_checks`; `triggers`; `omission_or_combination`; `representative_evidence` |
| Representation | `id` (`REP-####`); nonempty unique `artifact_type_ids`; confined unique `path`; `profile`; `representation_role`; `information_state`; `authority`; `source_direction`; `generated`; `owner_role`; cadence/triggers; `sensitivity`; `applicability`; `review`; nullable `superseded_by` |
| Type applicability | Core `required`; Conditional/Optional `not_assessed`, `applicable`, or `not_applicable`; `rationale`; nullable `assessed_on`; nullable `assessed_by`; `evidence_refs`; applied/omitted assessments require non-null date and assessor; adopted High-Assurance applicable types require resolving current evidence |
| Representation applicability | `required`, `applicable`, `not_applicable`, `not_assessed`, or `combined`; `rationale`; nullable `assessed_on`; `combined` requires multiple type IDs referring only to required/applicable types and explicit section/source-direction rationale |
| Review | `status` (`not_reviewed`, `reviewed`, `stale`, `not_applicable`); nullable `last_reviewed_on`; `basis`; owner role and cadence supplied by the representation |
| Requirement | stable record ID; statement; basis/source refs; status; owner; acceptance and validation method; decision, evidence, finding, and plan refs; successor when superseded |
| Finding | stable record ID; requirement refs; evidence refs; controlled classification; scope; impact; remediation refs; assessor; assessment time; limitations |
| Plan item | stable record ID; objective; finding/requirement refs; hard `PLAN-####` dependencies; reciprocal `TASK-####` refs; owner; status; gates; structured blocker refs; acceptance criteria; expected and closure evidence; stop/rollback conditions |
| RAIDQ item | stable record ID; item type; statement; owner; impact/probability as applicable; status; review/expiry; resolution condition; decision/evidence refs |
| Source | stable source ID; safe locator; source class; version or retrieval/observation date; intended use; sensitivity; rights/license when applicable; limitations; freshness rule; contradiction/successor refs |
| Evidence | stable evidence ID; exact subject/fingerprint; method/command and validator version; environment/scope; observed time; result; limitations; freshness; requirement/task/gate refs; successor |
| Supersession | stable record ID; predecessor; successor; effective date; reason; migration impact; retained-history location; authority basis |
| Handoff | exact revision; active task refs; current evidence refs; blockers/unknowns; next safe action; reading order; generated-integrity status; limitations |

`machine-readable/artifact-registry.json` is edited; the artifact catalog and
path-authority map are generated from it. Manifest, checksums, and integrity
reports are generated from managed sources. Human views generated from JSON
name their source. A project-maintained Markdown source with a generated
machine mirror states that direction explicitly; two independently edited
representations never own the same mutable record.

## 8. Relationships and lifecycle

**[Inferred] [Recommended]** The reusable lifecycle preserves these
relationships without collapsing information states.

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

Plan readiness is derived rather than stored. A `planned` item is on the ready
frontier only when every hard predecessor is `completed`, every referenced gate
is `passed` or validly `waived`, every structured blocker is resolved, and its
acceptance and expected-evidence contracts are populated. `depends_on` contains
only hard `PLAN-####` precedence edges; advisory relationships do not enter the
DAG. Execution tasks and plan items link reciprocally. An `in_progress` or
`completed` plan item is invalid if a hard predecessor ceases to be completed,
a gate ceases to be satisfied, a blocker becomes active, or linked task status
contradicts the plan.

Dates record provenance, observation, freshness, expiry, or a genuine external
constraint. They never satisfy a dependency, place work on the ready frontier,
or choose among independent ready items. Dependencies create a partial order;
current operator direction or an accepted priority/value/risk decision chooses
among multiple eligible items without granting new authority.

Lifecycle:

1. Initialize authority, the project artifact registry, version, definition,
   and empty registers.
2. Adopt sources and record provenance.
3. Define proposed requirements and decisions; accept only through valid
   project authority.
4. Inspect current state independently of target material.
5. Assess conformance and create traceable plans.
6. Derive the ready frontier and select only eligible work through current
   operator direction or an accepted priority/value/risk decision.
7. Execute selected work through reciprocally linked harness tasks whose own
   hard dependencies, gates, and blockers satisfy the task readiness contract.
8. Record evidence only after observation or execution.
9. Refresh catalog, path authority, manifest, and generated integrity; then
   update handoff pointers without copying mutable facts.
10. Supersede through successor records; archive immutable history when
   triggered.

## 9. Governance model

**[Inferred] [Recommended]** Apply the following governance model to keep the
dossier maintainable and safe for human/agent handoff.

- Canonical authority: DOS-0002 and DOS-0003 define dossier interpretation;
  operating authority remains outside the dossier.
- Ownership: every registry type and representation names an owner role,
  profile floor, applicability, review state, and cadence; type-level
  applicability preserves trigger and omission decisions.
- Change control: canonical changes require source/decision basis, affected
  artifact list, traceability update, and validation.
- Versioning: semantic dossier version; breaking information-contract changes
  increment major version.
- Supersession: successor record, effective date, reason, migration, retained
  history, no silent deletion.
- Provenance: consequential claims link source IDs and limitations.
- Traceability: unique IDs and references validated repository-wide.
- Dependency progression: readiness is a read-only derivation from completed
  hard predecessors, satisfied gates, resolved structured blockers, and
  reciprocal plan/task links; dates do not control sequencing.
- Artifact registry: authoritative project-local metadata; all physical
  artifact additions, removals, path changes, and applicability decisions
  begin here.
- Catalog/path authority: generated from the registry and rejected when stale
  or independently edited.
- Manifest/checksums: generated from declared scope; verified in the final
  read-only check; byte integrity only.
- Machine-readable representations: source direction declared and schema
  validated; profile-specific ownership is explicit.
- Drift detection: catalog/path coverage, source fingerprint, stale evidence,
  broken links/refs, and duplicated authority fail validation.
- Periodic review: per change for affected records; monthly for active
  registers/evidence; quarterly for authority/recovery; per release for exact
  integrity.
- Human/agent handoff: compact, exact revision, current task, fresh evidence,
  blockers, next action, no secret values or implied approval.

## 10. Adoption checklist and quality gates

**[Recommended]** Use this sequence and these objective gates when creating or
auditing a dossier.

Creation sequence:

1. Read target-project instructions and inspect the repository.
2. Select the smallest profile justified by named triggers.
3. Generate transactionally into an empty new-project target, or produce a
   read-only adoption crosswalk for an established project.
4. Confirm artifact registry type/representation coverage, assess every
   conditional trigger with a date, assessor, and rationale, link current
   evidence for applicable High-Assurance controls, retain omitted types as
   `not_applicable`, then refresh and confirm catalog/path-authority
   consistency.
5. Establish project definition, authority posture, source index, and owners.
6. Convert generated proposed baselines into project-specific records only
   from evidence or valid decisions.
7. Record current state from direct inspection.
8. Create requirements, findings, registers, and a hard-dependency plan with
   reciprocal task links and structured blockers.
9. Assess every project command and triggered extension. Configure applicable
   hooks with safe argv, owners, freshness, and declared effects, or record an
   owned `not_applicable` rationale; generation leaves them unassessed.
10. Run strict structure, schema, traceability, lifecycle, and integrity checks
    read-only. After confirming authority for declared effects, run configured
    project hooks only through their explicit evidence writer.
11. Derive the ready frontier, select an eligible item through valid direction,
    and complete a real linked task through evidence, review, closure, and
    handoff.
12. Refresh registry-derived views and generated integrity; run final
    read-only validation.

Objective quality gates:

- Completeness: every Core type has an active representation or explicit
  combination; every conditional/optional trigger is assessed in an adopted
  High-Assurance registry, every applicable type has a reviewed representation
  and current evidence links, and only a durably `not_applicable` type may be
  unrepresented.
- Consistency: one authority owner per concern; controlled statuses and schema
  versions; no contradictory mutable facts.
- Freshness: current evidence and generated reports match exact managed source;
  scaffold dates are not treated as review or observation dates.
- Traceability: every active requirement and completed plan item closes its
  required links.
- Dependency readiness: plan and task graphs are acyclic; execution states have
  completed hard predecessors, satisfied gates, resolved blockers, and
  reciprocal links; the ready frontier is derived without timeline ordering.
- Authority: every path is classified; no dossier content grants permission.
- Navigability: all entry links resolve; High profile directories are listed.
- Resumability: an unfamiliar maintainer identifies current task, revision,
  evidence, blocker, and next action within ten minutes.
- Claim boundary: structural conformance, harness adoption, and demonstrated
  product or production readiness remain separate conclusions.
- Integrity: manifest/checksums/report share one generation ID and scope.
- Safety: no secret values, escaping errors, path traversal, or untrusted
  instruction expansion.
- Truthfulness: skipped checks, dirty/untracked/ignored scope, limitations, and
  external effects are disclosed.

## 11. Gaps and new recommendations

The following are **[Recommended]**, not observed universal conventions:

- Use strict JSON as the portable kernel format; permit YAML only through a
  pinned, duplicate-key-safe parser extension.
- Maintain one project-local artifact registry and generate catalog and path
  authority views from it.
- Validate identifiers and references across dossier and harness as one
  namespace.
- Derive an unordered ready frontier from hard dependencies and gates. Keep
  timestamps and external deadlines as constraints or evidence metadata, never
  as implicit work-selection authority.
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
- Record reference checkout revision, role, authority status, and dirty state
  in a structured evidence registry so future audits can reproduce the
  reference analysis.

Unresolved universal limits:

- no dossier can establish legal, security, privacy, accessibility, financial,
  or production readiness without qualified project-specific evidence;
- external tool/platform authority cannot be created by repository files;
- domain correctness requires extensions and specialists;
- a generated skeleton is not an adopted dossier; and
- projects without a repository/filesystem require an adapted storage and
  instruction mechanism while preserving the same information contracts.
