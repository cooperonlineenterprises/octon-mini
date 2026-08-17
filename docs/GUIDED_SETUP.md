# Guided, Resumable Setup

This is the canonical human-readable procedure for installing, adopting,
using, or upgrading Octon Mini through a guided interview. The sole
authoritative question inventory is
`shared/source-contracts/setup-questions.json`; this document does not duplicate
or override question definitions.

## Purpose and boundaries

Guided setup is one orchestration layer over existing mechanisms:

- initialization ends in the existing `init` plan and apply;
- established-project adoption ends in the existing adoption proposal/review,
  `adopt` plan, and apply;
- upgrade ends in the existing three-way proposal/review, `upgrade` plan, and
  apply; and
- collaboration, hooks, packages, workflows, work completion, transactions,
  receipts, generation, and validation retain their current authorities.

There is no second installer or apply engine. A setup session is review input,
not project configuration, accepted authority, a receipt, or runtime
authorization. `permission_grant` is always `false`.

## Agent procedure

An AI agent conducting setup must:

1. Determine the mode from evidence. An empty or new target is initialization;
   established content without Octon Mini provenance is adoption; valid installed
   provenance is upgrade. Invalid, contradictory, or Octon Mini-like state
   without valid provenance is ambiguous and stops.
2. Read all applicable target instructions.
3. Inspect the target read-only. Do not execute detected hooks, refresh
   projections, install packages, write receipts, fetch, query a provider, or
   change an external system.
4. Keep directly observed facts, evidence-based inferences, recommendations,
   user selections, accepted-authority references, unresolved unknowns,
   deferred matters, and runtime authorization separate.
5. Do not ask for safely observable facts. Report the observation and its
   evidence instead.
6. Ask only dependency-eligible unresolved questions, normally one to three per
   interaction.
7. For each question, explain its importance; offer mutually exclusive choices
   where appropriate; state any recommendation and rationale separately; do not
   preselect an answer; allow `unknown`, `deferred`, or `not_applicable` only
   where the catalog permits; and explain what the state blocks.
8. Summarize every answer, recommendation, authority reference, unknown,
   deferral, blocker, and minimum closure step before planning.
9. Generate the exact digest-bound plan through `init`, `adopt`, or `upgrade`.
10. Require explicit acceptance of that plan digest before apply.
11. Validate and report structural conformance, project adoption,
    implementation evidence, specialist approval, release readiness, production
    readiness, and efficacy or commercial viability separately.

A conversational answer is not accepted project authority. When a selection
needs durable authority, record it as a selection, name the required ADR or
approval, and leave acceptance pending until that process completes.

## Interfaces

Each mode exposes the same setup engine:

```text
./octon init setup --target <path>
./octon adopt setup --target <path>
./octon upgrade setup --target <path>
```

These examples use the Unix/macOS form. On Windows, invoke the same extensionless
Python launcher and arguments as `python -B octon init setup --target <path>` or
`py -3 -B octon init setup --target <path>`, substituting `adopt` or `upgrade`
as needed. The platform form changes only launcher invocation, not setup
semantics, authority, artifacts, or command identity.

With no `--output`, the command prints a question batch and writes nothing.
An explicit `--output` creates one new session outside the target. It refuses
overwrite:

```text
./octon init setup --target <path> --output <external-session-01.json>
```

A conversational agent writes a strict answer batch bound to the displayed
session digest, then creates an immutable successor:

```text
./octon init setup \
  --target <path> \
  --session <external-session-01.json> \
  --answers <answers-01.json> \
  --output <external-session-02.json>
```

`--tty` uses the same catalog and validation rules. `--batch-size` is 1, 2, or
3. Current `octon` setup flags remain supported; their mapping to stable
question IDs is defined once in the shared session engine. A setup-session
plan uses:

```text
./octon init plan --target <path> --setup-session <session.json> --output <plan.json>
./octon adopt plan --target <path> --setup-session <session.json> --output <proposal-or-plan.json>
./octon upgrade plan --target <path> --setup-session <session.json> --output <proposal-or-plan.json>
```

Adoption and upgrade proposal/review artifacts remain separate because they
already own collision and path-disposition authority.

After an exact transaction plan exists, record its digest and path in a new
immutable session successor without changing the target:

```text
./octon init setup --target <path> \
  --session <session.json> \
  --record-plan <plan.json> \
  --output <session-with-plan-reference.json>
```

The plan remains bound to the predecessor session it reviewed. Preserve both
artifacts; recording the reference does not accept or apply the plan.

## Answer batch

An answer batch uses
`octon-mini.bootstrap.setup-answers.v1`, has `permission_grant: false`, names the
exact `session_digest`, and contains unique question IDs. Each answer records:

- `answered`, `unknown`, `deferred`, or `not_applicable`;
- a value only for `answered`;
- `user`, `agent`, `tty`, `cli`, or `review_artifact` as collection channel;
- evidence source, observation time, optional expiry, confidence, and
  limitations.

The information role comes from the catalog, not from the answer writer. This
prevents a user selection from being relabeled accepted authority. Accepted
authority string references must begin `authority:` or `external:` and still
must resolve under the project authority process. Runtime authorization is
never collectable during setup. Secret-shaped content and secret-bearing keys
are rejected.

## Session model and resume

`octon-mini.bootstrap.setup-session.v1` records:

- session identity, sequence, timestamps, status, and predecessor;
- mode and exact target identity;
- target revision, dirty-state observation, and content fingerprint;
- governing-instruction fingerprint;
- Octon Mini source, candidate, and installed versions and provenance;
- question-catalog version and digest;
- explicit selected profile and layout when supplied;
- question states plus reconciled answered, unknown, deferred, and
  inapplicable inventories;
- recommendations separately from user selections;
- accepted-authority references separately from selections;
- blockers and next eligible questions;
- generated-plan references when a reviewed successor records them;
- one minimum dependency-ordered closure sequence for pending decisions,
  evidence, packages, hook configuration, reviews, and approvals, with
  parallel-safe steps marked;
- work-completion status, missing prerequisites, and minimum closure sequence;
- limitations and canonical session digest.

Sessions are immutable successors. Resume never overwrites a predecessor.
Target content/revision, instruction, catalog, Octon Mini version/provenance, or
material evidence changes fail closed. `--reinspect` creates a successor from
current observations. It preserves explicit unknown, deferred, and
inapplicable states only when the stable question ID and version are unchanged
and their dependencies remain eligible;
factual answers and selections must be reviewed again. New catalog questions
are unanswered, never silently defaulted.

## Question families

The catalog dependency-orders these families:

- project identity, profile from actual risk, physical layout, optional first
  task, and installed provenance;
- target instructions, existing governance, functional equivalents,
  authority-bearing collisions, adoption authority, ambiguity review, and
  preservation paths;
- aggregate write-capable-human evidence, actual independent review capacity,
  separate human/automation concurrency, external contribution, and solo
  preference;
- test, lint, build, and closure hook assessments with owner role, shell-free
  argv, version probe, timeout, freshness, write paths, external effects,
  rationale, and limitations;
- SCM, repository identity, remote/default branch, workflow selection,
  concurrent modifier, accepted workflow authority, provider assessment,
  integration method, exact hosted checks, eligible peer reviewers, and
  cleanup;
- evidence-triggered operations/observability, security/supply-chain, context,
  domain, and High-Assurance controls; and
- upgrade authority/evidence plus exact proposal-bound review dispositions.

Write-capable humans are people with both authority and practical ability to
write or integrate changes. Read-only users, bots, agents, automation, and
recent activity do not count. Team size selects only the collaboration band.
Assurance comes only from project risk and control needs. Unknown, stale, or
conflicting collaboration evidence selects no workflow.

Detection may recommend hook argv, SCM, project name, or layout, but it does
not execute or adopt them. Package absence never means `not_applicable`.

## Work-completion opt-in

The interview presents exactly three unselected conceptual choices:

1. Keep governed work completion disabled.
2. Enable on-demand `plan`, `apply`, and `resume` after prerequisites close.
3. Enable on-demand operation plus automatic read-only planning after task
   closure.

There is no automatic apply, commit, publish, pull request, review, merge,
synchronization, or cleanup choice. An enabling selection remains
`pending_prerequisites` until all of these are explicit and current:

- installed content-addressed small-team Git portfolio;
- accepted supported workflow authority;
- exact repository identity, remote, and default branch;
- provider assessment;
- exact hosted-check set, including explicitly empty;
- eligible provider identities for peer-review workflows;
- supported adopted integration method;
- configured read-only validation hooks;
- `git_hooks: require_none` and inactive `core.fsmonitor`;
- local and remote cleanup choices; and
- applicable assurance-control references, including an explicitly reviewed
  empty set where legitimate.

The session reports the smallest dependency-ordered closure sequence and which
configuration work can run in parallel. The base init/adopt/upgrade plan does
not enable work completion. A separate project-owned package, collaboration,
hook, decision, and configuration transaction closes the sequence. Setup never
creates standing authorization for later external operations.

## Read-only and write boundaries

Question generation and inspection may read target bytes, Git revision/status
with optional locks disabled, locally configured values, and valid Octon Mini
provenance. They do not run candidate commands or contact a hosted provider.
Fingerprint tests compare the target before and after.

Writing a session or plan is an explicit output action. Setup sessions are kept
outside the target so their creation cannot change mode or target fingerprints.
Transaction plans may use the existing transaction directory, which setup
fingerprints deliberately treat as non-project setup output; no legitimate
project source is excluded. Planning does not refresh generated outputs. Any
staleness observed by a separate read-only integrity check must be reported and
left unchanged; setup itself does not establish projection freshness.

Apply is bound to the exact session bytes/digest, exact plan digest, current
target/instruction fingerprints, and normal transaction preconditions. It
revalidates before the existing apply engine acts. A changed or missing session
blocks apply.

## Installation and migration

New Octon Mini snapshots include the strict session and answer schemas, but no
project answers, accepted decisions, workflow adoption, hooks, provider
settings, branch policy, or authorization. The catalog and engine live in the
Octon Mini Project Bootstrap skill source.

Existing independent Project Blueprint snapshots may remain as they are
without guided setup. They receive the new schemas and planner integration only
through an explicit Octon Mini upgrade; an installed skill receives the source
engine/catalog only through an explicit skill update. Project Blueprint
3.x→Octon Mini 4.0 uses the reviewed
cross-brand migration; legacy flags and identities may be recognized only as
migration inputs. There is no `pb` compatibility command. Upgrade preserves
project-owned files and accepted authority. New question definitions appear
unanswered, and existing answer artifacts are never overwritten or silently
migrated into authority.

Generated structural conformance proves only the declared structural checks.
It does not prove implementation, specialist approval, release, production,
product efficacy, or commercial viability.
