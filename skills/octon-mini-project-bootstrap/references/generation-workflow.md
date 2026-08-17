# Creation, Adoption, Maintenance, Recovery, and Upgrade

## Guided setup

Use `scripts/octon.py init|adopt|upgrade setup` when project facts or policy
selections are not already supplied through legacy flags. The command reads the
target without running detected hooks, refreshing projections, querying a
provider, or changing the target. Write a setup-session artifact only to an
explicit path outside the target, then answer or resume it through the same
catalog used by conversational agents and TTY interaction.

Determine the mode from evidence: an empty target initializes, an established
project without valid Octon Mini provenance adopts, and a snapshot with valid
provenance upgrades. Stop on ambiguity. Ask only eligible unresolved questions
in catalog dependency order. Keep observations, inferences, recommendations,
owner selections, accepted-authority references, unknowns, deferred matters,
and runtime authorization separate. A setup answer is never standing
permission or accepted project authority.

Summarize the reviewed session, then pass it to the existing planner with
`--setup-session`. The resulting init, adopt, or upgrade plan binds the session
digest and current target, instruction, catalog, and Octon Mini inputs. Apply
uses the existing transaction engine and rejects stale bindings. Legacy-style
setup flags on the current `octon` interface map to stable question IDs; this
does not preserve the old `pb` command.

## New project

1. Use `scripts/octon.py init plan` with an explicit profile and layout, or finish
   a guided setup session and pass it with `--setup-session`. A TTY-only
   `octon init` may propose Minimal but must receive confirmation.
2. Review the plan sections separately: observations, inferences, explicit
   decisions, and authorization gates. Hook detection runs no candidate or
   version command and adopts nothing.
3. Accept the exact digest with `octon init apply`. Apply stages the entire
   scaffold, refresh, structural check, and release-tier tests before writing.
4. If supplied, the first task is built only from explicit semantics. Resume
   with generated `./octon work resume`.
5. Assess hooks, collaboration, SCM, and mandatory domain triggers separately.
   Run the explicit project-check writer only after reviewing declared side
   effects and current authority.

## Established project

Use `scripts/octon.py adopt plan|apply`, optionally with a reviewed guided setup
session. Default semantic inspection is bounded to
200 allowlisted UTF-8 text/config files, 256 KiB each, and 4 MiB total. It
excludes symlinks, binaries, ignored/generated/vendor/dependency/build/coverage
paths, credentials, private keys, `.env*`, and sensitivity-marked paths.
Sensitive or larger inspection requires an exact path-scoped opt-in.

The proposal classifies collisions, likely functional equivalents,
authority-bearing conflicts, safe and review-required additions, missing
project facts, hook candidates, and ambiguity. Review functional equivalence
and authority preservation explicitly. Apply refuses every existing-path
overwrite, stages the complete release tier, preserves project bytes, and
leaves adoption `in_progress`.

## Routine work and maintenance

Generated commands use plan/apply receipts:

```text
./octon work start --help
./octon work close --help
./octon work handoff --help
./octon work resume
./octon maintain registry plan
./octon maintain hooks plan --help
./octon maintain collaboration plan --help
./octon maintain refresh --apply
```

`state/current.json` is fully derived. `state/focus.json` is the small
authoritative source for current operator focus and next action. Refresh is
non-inferential and never edits the authoritative artifact registry. Registry
reconciliation may propose reuse and IDs but requires explicit ownership,
applicability, source direction, representation role, omission, supersession,
and stable-ID choices.

Project checks support selected hooks and changed-scope routing. Current
evidence is bounded; overflow is archived immutably with successor links. Hook
execution and evidence writing remain separate from read-only `check` and from
generated-integrity refresh.

If the installed Git portfolio and accepted workflow are applicable, a project
may separately adopt the disabled `work_completion` block. Record exact
repository/provider/check/eligible-reviewer/hook/cleanup assessments without
changing accepted workflow authority. Close a task with its explicit staging,
commit, PR/review, and concurrent-handback inputs; include any in-repository
close-plan path in the exact staging inventory, while the resulting current
close receipt and unchanged postimages are bound automatically; then run
`./octon work finish plan`. The optional
completion event uses the existing `commands.work_completion_plan` hook and
may run only that exact read-only command. Apply accepts the reviewed digest
and a current task-scoped external authorization attestation; resume uses the
Git-common-directory receipt. Never refresh during planning or describe a
receipt as release or production readiness.

Maintain decision questions in the project-owned governance register. Keep
recommendations, owner selections, and accepted `DEC-####` authority separate;
reconcile every decision and trade-off review exactly once and derive the
minimum closure graph before broad implementation. A read-only decision review
does not refresh generated outputs.

## Recovery

Run `./octon doctor` first. Structured diagnostics identify root cause, authority
source, dependent symptoms, safe next action, and whether repair is derived or
project-owned. Doctor is read-only unless the operator explicitly accepts a
derived-only repair digest.

- Pending journal: `./octon transaction recover --pending <path>` restores exact
  preimages only while all paths still match before or planned-after states.
- Applied receipt: `./octon transaction rollback --receipt <path>` refuses any
  independently changed post-apply path.
- Stale plan, evidence, or instruction fingerprint: re-plan; never force.
- Interrupted refresh: diagnose, run explicit derived refresh, then read-only
  check. Project-check evidence is not repaired by integrity refresh.

## Upgrade

`scripts/octon.py upgrade plan|apply`, optionally with a reviewed guided setup
session, performs a three-way comparison among the
recorded old installed inventory, current project, and candidate snapshot. It
classifies unchanged pristine, exact-pristine update, project-modified,
additive, removed upstream, conflicting, derived, and provenance paths.

Automatic handling is limited to new noncolliding Octon Mini-owned paths,
exact-pristine non-authoritative implementation assets, and derived
regeneration. Instructions, policy, project configuration/hooks, workflow
adoption, dossier sources/registries, records, current facts, stable IDs,
deletions/moves, permissions, and symlinks require proposal-bound review.

The work-completion engine/schema are safe additions only when absent and
noncolliding. The disabled project configuration, workflow package version,
accepted decisions, hook commands, provider and branch settings, cleanup, and
authorization policy require explicit review; upgrade never enables the
completion hook.

For 3.1→4.0, first run the reviewed legacy inventory seed workflow in
`migrate_3_1_0_to_4_0_0.py`. It refuses assessed collaboration and every unknown
static pristine baseline. The seed is never applied directly; the upgrader
rechecks it and produces the only mutation receipt. Run the migration and
release suites, then reassess adoption and readiness independently.

This is the explicit Project Blueprint 3.x→Octon Mini 4.0 cross-brand
migration. Legacy launchers, origin records, and schema identities are inputs
to transform only. A successful upgrade installs `octon` and current Octon Mini
provenance and retains no `pb` alias or runtime compatibility path.

Earlier executable migrations remain closed reference transformations rather
than in-place upgrade tools. See the matching file under `migrations/`.
