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
