# Worked Example: Shared Record Identifier Contract

This fictional, domain-neutral example demonstrates the governance method. It
is not an accepted Octon Mini decision, target-project authority,
implementation evidence, or readiness claim.

## Executive summary

Example Project needs one stable identifier contract before several teams can
author records independently. One question is evidence-first because an
import/export round trip has not been demonstrated. A later presentation-label
choice can run in parallel and does not block the underlying identifier
contract.

| Measure | Count |
|---|---:|
| Total registered | 2 |
| Unresolved | 2 |
| Blocking | 1 |
| Evidence-first | 1 |

## Dashboard

| ID | Title | Type | Timing | Lifecycle | Blocking | Recommendation | Owner selection | Authority |
|---|---|---|---|---|---|---|---|---|
| DREG-1001 | Choose the canonical record identifier shape | architecture decision | evidence-first | evidence in progress | yes | OPT-A | blank | blank |
| DREG-1002 | Choose the human-facing display label rule | product-policy decision | required later | open | no | OPT-B | blank | blank |

The blank selection and authority cells are intentional. Recommendations have
not been converted into owner choices.

## DREG-1001 — Choose the canonical record identifier shape

- Exact decision: choose the syntax and comparison rule used by every
  authoritative record reference.
- Practical importance: inconsistent identifiers would break traceability and
  make records appear missing or duplicated.
- Accepted constraints: identifiers are immutable after publication; unknown
  records remain unknown; the existing accepted character-encoding decision
  remains in force.
- Exclusions: display labels, storage technology, and migration execution are
  separate matters.
- Owner role: project owner.
- Reviewers: architecture owner and data-integrity reviewer.

### Options

| Option | Description | Advantages | Disadvantages and risks | Best fit |
|---|---|---|---|---|
| OPT-A | Fixed namespace prefix plus zero-padded sequence | deterministic; readable; easy validation | central allocation may become a bottleneck | bounded record classes with one allocator per namespace |
| OPT-B | Random opaque identifier | decentralized; collision-resistant | less readable; import normalization is unproven | independently created records across many writers |
| OPT-C | Human-authored descriptive slug | memorable | rename pressure; normalization and collision risk | non-authoritative display only |

Recommendation: OPT-A, medium confidence. The accepted compromise is central
namespace allocation in exchange for deterministic traceability. This is not
an owner selection.

Evidence-producing step: the evidence owner will round-trip 10,000 synthetic
records through the two supported interchange paths, verify byte-stable
identity and unknown-reference preservation, and stop the spike if any
identifier changes, collides, or converts an unknown reference into an absent
one. Until that result exists, the decision remains evidence-first.

### Layer 1

| Gate | OPT-A | OPT-B | OPT-C |
|---|---|---|---|
| Safety and deterministic correctness | pass | pass | fail |
| Authoritative ownership and data integrity | pass | pass | fail |
| Privacy, security, rights, consent, and isolation | pass | pass | pass |
| Preservation of unknown or pending state | unknown | unknown | fail |
| Applicable legal, specialist, and product-policy constraints | pass | pass | pass |
| Compatibility with currently accepted authority | pass | pass | tension treated as fail for this scope |

OPT-C is disqualified before scoring. OPT-A and OPT-B remain evidence-first;
neither receives a total.

### Layer 2 after the round-trip evidence exists

The following illustrative scores are not yet current evidence; they show how
the eligible comparison would be recorded after Layer 1 passes.

| Attribute | Weight | OPT-A | OPT-B |
|---|---:|---:|---:|
| Safety and correctness | 1 | 5 | 5 |
| Authority and data integrity | 1 | 5 | 4 |
| Privacy, security, rights, and consent | 1 | 4 | 4 |
| Reliability, durability, and recovery | 1 | 5 | 5 |
| Simplicity and implementation risk | 1 | 4 | 4 |
| Flexibility and evolvability | 1 | 3 | 5 |
| Portability and compatibility | 1 | 5 | 5 |
| Performance and scalability | 1 | 4 | 5 |
| Operability and auditability | 1 | 5 | 3 |
| User effort and accessibility | 1 | 4 | 2 |
| Cost and resource efficiency | 1 | 4 | 4 |
| Reversibility and blast radius | 1 | 3 | 4 |

Default weights are used and every attribute appears once. No total is shown
because the example's Layer 1 evidence remains unknown.

Evidence strength is `none`; recommendation confidence is `medium`. The worst
credible failure is silent identifier translation that attaches evidence to
the wrong record. The exit path is a successor decision plus an explicit
crosswalk migration that preserves old identifiers.

Disposition: `reaffirm pending evidence`. Compatibility: `unknown` because the
round-trip behavior has not been observed. The issue affects the canonical
identifier contract and both interchange components; it can silently break
traceability; implementation must not change beyond an isolated spike; the
project owner and data-integrity reviewer require validation evidence before
an ADR can be accepted.

## Already-settled decisions

| Authority | Settled scope | Constrains | Review treatment |
|---|---|---|---|
| `DEC-0100` (fictional) | supported character encoding | DREG-1001 | inspected as a non-reopenable option constraint |

This fictional accepted record remains outside the register; it constrains the
identifier choice but is not silently reopened or treated as a new option.

## DREG-1002 — Choose the human-facing display label rule

This is a separate product-policy choice, not another identifier option.
Labels never replace canonical identifiers. The options are owner-authored,
automatically derived, or a constrained combination. The recommendation is a
constrained combination, but the owner-selection section remains blank. The
question is `required later` and may proceed in parallel with the DREG-1001
spike because it does not alter identifier authority.

## Matters that are not open decisions

| Matter | Classification | Route |
|---|---|---|
| Execute the round-trip | validation work | evidence task for DREG-1001 |
| Draft the identifier grammar | contract draft | CLOSE-1001 |
| Demonstrate release import recovery | operational readiness | later gate evidence |
| Add a display tooltip | ordinary reversible implementation choice | implementation task after DREG-1002 |

## Minimum closure sequence

| Closure ID | Kind | Decision refs | Depends on | Blocks broad implementation |
|---|---|---|---|---|
| CLOSE-1001 | contract draft | DREG-1001 | none | yes |
| CLOSE-1002 | evidence-first spike | DREG-1001 | CLOSE-1001 | yes |
| CLOSE-1003 | owner decision | DREG-1001 | CLOSE-1002 | yes |
| CLOSE-1004 | ADR or approval | DREG-1001 | CLOSE-1003 | yes |
| CLOSE-1005 | owner decision | DREG-1002 | none | no |

CLOSE-1001 and CLOSE-1005 may run in parallel. Read-only inventory, synthetic
fixture design, and the isolated reversible spike may begin before full
closure. Broad implementation that creates or persists authoritative record
identifiers must wait for CLOSE-1004. Nothing in this worked example closes
that boundary.

## Separate conclusions

| Conclusion | Result |
|---|---|
| Architecture quality | partially supported by a bounded option analysis |
| Documentation completeness | partially supported for this example only |
| Implementation evidence | not assessed |
| Specialist approval | not assessed |
| Release readiness | not assessed |
| Production readiness | not assessed |
| Product efficacy or commercial viability | not assessed |
