# Project Blueprint Source Architecture Decisions

This file records accepted decisions for the `project-blueprint` source
repository. It is not copied into generated projects, does not grant
permission, and does not accept a pattern on behalf of any adopting project.

## SRC-DEC-0003 — Source-only architectural Pattern Catalog

| Field | Accepted decision |
|---|---|
| Status | `accepted` |
| Authority | Explicit repository-owner implementation authorization on 2026-08-11 |
| Scope | Project Blueprint source governance only |
| Placement | `patterns/` outside the universal kernel and all generated profile inventories |
| Decision | Maintain strict, versioned pattern records with governed lifecycle and promotion rules |
| Adoption effect | None; catalog presence and status never adopt a pattern into a project |
| Permission effect | None; every record requires `permission_grant: false` |
| Compatibility | Additive in Blueprint 3.1.0; harness kernel remains 3.0.0 |

Promotion is never automatic. `recommended` requires independent project
evidence and explicit architecture review. `stable` additionally requires an
explicit compatibility and migration-support commitment. One successful
project, proof, test, or usage count is insufficient.

The source/project boundary is runtime-enforced by the versioned generation
policy. Source paths default to `source_only`; version 2 explicitly enumerates
reviewed paths. Runtime generation uses only the requested profile's allowlist,
ignores and reports unreviewed additions, and blocks only capabilities whose
reviewed dependency or hard invariant fails. Repository validation remains
strict across every profile. Forbidden outputs, source confinement, and the
exact final staged tree remain fail-closed. This proportional degradation does
not authorize a new input or manual adoption.

## SRC-DEC-0004 — Semantic, binding, Context Pack, and claim envelopes

| Field | Accepted decision |
|---|---|
| Status | `accepted` |
| Authority | Explicit repository-owner implementation authorization on 2026-08-11 |
| Scope | Canonical dossier, harness, generation, optional Context Pack, and evidence-claim contracts |
| Placement | Canonical documentation, source semantic crosswalk, Generation Contract, and High-Assurance-only optional schema |
| Decision | Clarify information roles and input binding; validate adopted cross-boundary Context Packs; require bounded non-proof claims |
| Exclusion | No universal state enum and no new universal runtime mechanism |
| Permission effect | None; context possession and evidence cannot grant action authority |
| Compatibility | Additive; existing aggregate statuses and existing Context Pack prose remain unchanged until explicit reconciliation |

The semantic crosswalk explains meaning across aggregates but does not replace
their record-specific statuses. The optional Context Pack schema is available
only in newly generated High-Assurance snapshots; no pack record is generated
or adopted.

## SRC-DEC-0005 — Optional Architecture Proof family

| Field | Accepted decision |
|---|---|
| Status | `accepted` |
| Authority | Explicit repository-owner implementation authorization on 2026-08-11 |
| Scope | Source-only optional proof schema and templates |
| Placement | `patterns/architecture-proof/`; never a generated profile default |
| Decision | Provide one proof family for spikes, reference slices, provider qualification, adversarial fixture packs, and readiness evidence |
| Claim boundary | Completion proves only the exact hypothesis, subject, environment, and evidence recorded |
| Permission effect | None |
| Compatibility | Additive source tooling; no generated-project migration |

An Architecture Proof may conclude `supported`, `unsupported`, or
`inconclusive`. A template, happy path, or passing structural check never
establishes production readiness.

## SRC-DEC-0006 — Reviewed lifecycle and governed-change patterns

| Field | Accepted decision |
|---|---|
| Status | `accepted` |
| Authority | Explicit repository-owner implementation authorization on 2026-08-11 |
| Scope | Pattern Catalog admission only |
| Placement | `PAT-0001` and `PAT-0002` records at no higher than `reviewed` |
| Decision | Admit `lifecycle-disposition` and modular `governed-change-and-effects` for future project-specific evaluation |
| Implementation effect | None; no runtime, schema, template, generated path, extension, or profile default is authorized |
| Promotion gate | A concrete adopter must supply the applicable failure model and required proof before `experimental` or higher |
| Permission effect | None |

The governed-change record contains only the module names `impact`, `action`,
`mutation_effect`, and `recovery_incident`. It deliberately supplies no
universal verbs, action enum, external-effect infrastructure, or recovery
implementation.

## SRC-DEC-0007 — Authoritative profile manifest and explicit profile selection

| Field | Accepted decision |
|---|---|
| Status | `accepted` |
| Authority | Explicit repository-owner velocity-roadmap implementation authorization on 2026-08-12 |
| Scope | Blueprint source profiles, generated inventories, package declarations, acceptance coverage, and their independent-snapshot projections |
| Placement | `shared/source-contracts/profile-manifest.json` with a versioned source schema |
| Decision | Maintain one authoritative profile manifest and derive generator choices, project-local and derived paths, generated validator inventories, package declarations, and acceptance reporting from it |
| Selection effect | Non-interactive generation and adoption planning require an explicit profile; a future interactive flow may propose Minimal but cannot adopt it without confirmation |
| Permission effect | None; manifest data and profile recommendations grant no project authority |
| Compatibility | Breaking source-tooling transition in the 4.0.0 velocity program; existing independent snapshots remain unchanged until an explicit migration |

Generated projects receive only the selected, rendered projection needed for
their independent validator. They do not depend on the Blueprint source
manifest at runtime. The manifest remains allowlist-driven, source paths remain
`source_only` by default, and its documentation and acceptance projections are
validated rather than independently maintained.

## SRC-DEC-0008 — Staged repository-local transactions and derived operating state

| Field | Accepted decision |
|---|---|
| Status | `accepted` |
| Authority | Explicit repository-owner velocity-roadmap implementation authorization on 2026-08-12 |
| Scope | Generated repository-local lifecycle, maintenance, recovery, and evidence-index mutations |
| Decision | Use one closed plan/apply contract with canonical digests, instruction and path preimages, staging, declared derived writes, write-ahead recovery, exact receipts, and postimage-bound rollback |
| State effect | `state/current.json` becomes derived; non-derivable operator focus remains an explicit source in `state/focus.json` |
| Permission effect | None; a transaction executes only already-authorized repository-local work and cannot create authority, facts, review, evidence, or external-effect permission |
| Compatibility | Harness-kernel v4 change requiring explicit migration; existing independent snapshots remain unchanged |

There is no force bypass. Planning, check, doctor, resume, discovery, and
diagnostic modes are read-only. Generated-integrity refresh and project-check
evidence remain distinct explicit writers. An interrupted apply restores exact
preimages only while each affected path still matches its recorded preimage or
planned postimage.

## SRC-DEC-0009 — Progressive collaboration and trigger-installed capabilities

| Field | Accepted decision |
|---|---|
| Status | `accepted` |
| Authority | Explicit repository-owner velocity-roadmap implementation authorization on 2026-08-12 |
| Scope | Collaboration assessment, concurrent-work modifier, SCM selection, domain packages, and optional schemas |
| Decision | Derive solo, pair, or tiny only from current aggregate evidence used by the result; model concurrency separately; ship only trigger metadata in the kernel and install capability payloads through pinned, decision-bound transactions |
| Profile effect | None; collaboration and concurrency never select Minimal, Standard, or High Assurance |
| Permission effect | None; detection and derived workflow selection are proposals unless an accepted project decision adopts them |
| Compatibility | Collaboration profile v2 and package registry v1 require explicit migration or reviewed legacy seeding |

Missing trigger evidence is `not_assessed`, not `not_applicable`. Package
content, accepted trust decision, applicability when claimed, installed digest,
validation receipt, owner, and lifecycle state are independently bound. The
full Git portfolio and domain mechanisms are absent from every default profile.

## SRC-DEC-0010 — Bounded semantic adoption and three-way live upgrades

| Field | Accepted decision |
|---|---|
| Status | `accepted` |
| Authority | Explicit repository-owner velocity-roadmap implementation authorization on 2026-08-12 |
| Scope | Established-repository adoption and upgrades of generated independent snapshots |
| Decision | Inspect established projects through bounded allowlisted recipes; preserve all existing bytes; upgrade by comparing recorded old baseline, current project state, and candidate snapshot |
| Automatic boundary | Safe additions, exact-pristine non-authoritative implementation assets, and declared derived regeneration only |
| Review boundary | Instructions, policy, configuration, workflows, dossier sources and registries, records, stable IDs, deletions, moves, symlinks, permissions, and modified content |
| Permission effect | None; structural installation or upgrade never marks adoption or readiness |

Plans retain hashes and matched vocabulary rather than inspected content.
Every ambiguity is proposal-bound, previewable, and explicitly dispositioned.
Legacy 3.1 projects lacking an installed-baseline inventory require reviewed
seed data; no baseline is reconstructed by assertion or guess.

## SRC-DEC-0011 — Compact representation and tiered validation

| Field | Accepted decision |
|---|---|
| Status | `accepted` |
| Authority | Explicit repository-owner velocity-roadmap implementation authorization on 2026-08-12 |
| Scope | New-project physical dossier layout and generated validation cost |
| Decision | Default new snapshots to the compact representation map while retaining separated layout; expose fast, integration, and release tiers with bounded mutation baselines and explicit scale benchmarks |
| Semantic effect | None; combining physical representations does not combine authority ownership, lifecycle, stable artifact IDs, or substantive review obligations |
| Profile effect | None; layout remains independent of assurance and collaboration |
| Compatibility | Layout is recorded in origin inventory v2; moves between layouts require explicit registry-aware migration |

Primitive scaffolding runs structural checks plus the fast bounded mutation
tier before atomic placement. Guided init, adoption, upgrade, release
validation, and other consequential boundaries stage the complete applicable
release tier. Full-tree tests remain where host metadata, ignore behavior,
symlinks, whole-tree fingerprinting, or cross-file integration is material.

## Explicitly deferred by these decisions

The following remain outside the accepted implementation:

- resource accounting and quantitative reservations;
- bounded invalidation;
- generic policy or rights locks;
- corpus-use machinery;
- universal action, lifecycle, readiness, trust, or state enums; and
- external-effect infrastructure.

Their exact future triggers remain recorded in
`ARCHITECTURAL_PATTERN_INTEGRATION_REVIEW.md`.
