# Profile, Layout, and Collaboration Selection

These are independent axes. Do not make team size a risk profile, make layout
an assurance level, or count agents as human writers.

Guided setup asks for these axes through the canonical setup-question catalog.
It may present an evidence-based recommendation, but it never preselects an
answer. Preserve `unknown` or `deferred` when allowed, and keep a user selection
separate from any accepted authority needed to adopt project policy.

## Assurance profile

- **Minimal** — early, low-risk, or low-integration work. It includes the full
  deny-by-default kernel, transactional workflow interface, decisions/tasks,
  derived current state, focus, diagnosis/recovery, validation fixtures, and
  the core dossier. This is the interactive recommendation, never a silent
  non-interactive default.
- **Standard** — add structured traceability, durable review/evidence records,
  requirements/findings/plans/RAIDQ, events, artifacts, and an empty extension
  registry when those needs are real.
- **High Assurance** — add sensitivity, protected enforcement, long-lived
  operation, role separation, reproducibility, checkpoints, trust/transition/
  history controls, and checksums. Conditional controls remain unassessed
  until project owners assess them.

Operations/observability, security/supply-chain, the sample restriction, and
the optional Context Pack schema are trigger-installed packages, not universal
profile payloads. Their absence never establishes non-applicability.

## Physical layout

- **compact** (new-project default) combines conceptual artifact types only
  where authority, ownership, lifecycle, sensitivity, review, and retention
  are compatible;
- **separated** keeps distinct representations when those concerns differ or
  a project prefers explicit files.

Both preserve conceptual artifact IDs. Layout changes require explicit
registry migration; representation IDs are never silently reassigned.

## Collaboration

- **solo**: one write-capable human; use only the explicit solo integration
  preference;
- **pair**: two write-capable humans; use independent-review-capacity evidence;
- **tiny**: three to five write-capable humans; use independent-review-capacity
  evidence;
- above five: outside the supported portfolio, not a trigger for a larger
  assurance profile.

Add `concurrent_work` only when current evidence shows simultaneous human,
agent, or automation work. Every fact used by a result requires a source,
observation time, expiry, and limitations. Missing, stale, or conflicting
evidence selects no workflow. `solo_direct`, `solo_hybrid`, `pair_pr`, and
`tiny_pr` remain proposals until an accepted project-owned decision adopts one.
When explicitly enabled, every supported workflow uses the same governed
`work.finish` engine. Assurance controls may add checks or review gates but do
not select a second engine; generated completion and its event hook start
disabled and grant no authority.

## SCM and packages

The kernel stores only a compact SCM trigger and pinned Git-portfolio digest.
Detection proposes Git but does not select it. An accepted decision triggers a
transactional, content-addressed vendor install. Non-Git projects carry no
active portfolio dependency.

Choose the smallest profile that covers actual risk. No selection creates
policy trust, collaborator identity, approval, evidence, permission, adoption,
or readiness.
