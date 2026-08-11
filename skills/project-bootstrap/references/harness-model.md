# Harness Model

Read the first available harness definition:

- source checkout: `../../../harness/BLUEPRINT.md`;
- installed bundle: `../assets/blueprint-source/harness/BLUEPRINT.md`.

## Required layers

Generate the smallest justified profile around:

1. short root instruction routing;
2. the seven-file `.agent/` governance kernel;
3. project profile and extension contracts;
4. operational records and compact current state; and
5. optional `.agents/` capability packages and generated integrity.

The harness is project-local and subordinate to higher authority. Generated
policy remains non-authorizing and deny-by-default. Do not transfer
permissions, accepted decisions, current status, evidence, identities,
endpoints, or domain constants from this blueprint or another project.

## Information owners

- permission boundary: `.agent/policy.json`;
- precedence and trust: `.agent/context.json`;
- IDs and statuses: `.agent/schema.json`;
- state transitions: `.agent/lifecycle.json`;
- tool contracts: `.agent/tools.json`;
- commands and checks: `.agent/validators.json`;
- stable project hooks, collaboration assessment, and workflow adoption:
  `.agent/project.json`;
- provider-neutral workflow definitions: `.agent/workflows/small-team-git.json`;
- explicit target-project check evidence: `.agent/project-checks/evidence.json`;
- active work: `.agent/tasks/`;
- durable intent: `.agent/decisions/`;
- direct observation: `.agent/evidence/`;
- concise resumption: `.agent/state/`; and
- generated integrity: `.agent/generated/`, always non-authoritative.

The kernel uses strict JSON with duplicate-key rejection and a local schema
snapshot. Domain behavior enters only through a registered,
restrictions-only extension that declares compatibility, confined paths,
provenance, side effects, and a structured validator.

Task `dependencies` are hard `TASK-####` prerequisites. Entering or re-entering
execution passes through `ready`, which requires completed dependencies,
satisfied gates, resolved structured blockers, and reciprocal plan links. Use
the read-only ready-frontier command to identify eligible work; current
direction or an accepted priority/value/risk decision chooses among independent
items, never a date-based inference.

Each profile has a closed minimum governed-file inventory. Missing router,
kernel, state, script, schema, template, fixture, store, extension-registry,
or capability-baseline files are validation failures. Add project-specific
behavior only inside the validated extension and capability namespaces; do
not use an unregistered governance path.

## Collaboration and Git workflow boundary

Every profile includes the same four base workflows: `solo_direct`,
`solo_hybrid`, `pair_pr`, and `tiny_pr`. Classify one, two, and three-to-five
write-capable humans as `solo`, `pair`, and `tiny`; zero blocks, and more than
five is explicitly unsupported. Read-only humans, bots, automation, and recent
activity do not alter the write-capable-human count. Simultaneous humans or
agents add `concurrent_work` without changing the human band.

Assessment requires project-owned evidence, observation and freshness times,
limitations, and `confirmed`, `inferred`, `conflicted`, or `unknown`
confidence. Unknown, stale, or conflicting state selects nothing. Store only
aggregate counts and safe references, never collaborator identities. The
read-only assessment command reads the stored aggregate, writes nothing, uses
no network, and never runs under ordinary `--check`.

A recommendation cannot adopt or authorize a workflow. Adoption requires an
accepted project-owned decision, and each Git or hosted operation still follows
its own authority class. The workflow catalog is provider-neutral and every
operation reference resolves to the exact, fail-closed catalogs in
`.agent/tools.json`. GitHub is optional and generated projects assert no hosted
reviewer, check, protection, environment, release, credential, permission, or
CI fact.

Do not add GitFlow, merge queues, release trains, stacked-PR trains, fork-first
internal contribution, approval hierarchies or stages, dedicated release
manager handoffs, organization-wide rulesets, multi-environment promotion, or
enterprise issue/portfolio governance.

## Adoption boundary

Scaffolding proves only that the baseline files were generated consistently.
Target-project adoption must inspect actual scope and risks, resolve or
explicitly classify sentinels, record the authority posture, assess every
target-project hook, execute configured hooks only through the explicit
shell-free evidence writer, run read-only checks and mutation tests in a clean
environment, and complete a real task lifecycle. Structural conformance,
project-harness adoption, and demonstrated target-project readiness are
separate conclusions.

Standard and High Assurance include disabled, unassessed operations and
observability plus security and supply-chain extensions. Their strict records
can support production-governance adoption, but their presence or successful
validation proves neither external execution nor a qualified conclusion.
