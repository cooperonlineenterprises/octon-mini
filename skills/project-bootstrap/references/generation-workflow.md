# Creation, Adoption, Maintenance, Recovery, and Upgrade

## New project

1. Use `scripts/pb.py init plan` with an explicit profile and layout. A TTY-only
   `pb init` may propose Minimal but must receive confirmation.
2. Review the plan sections separately: observations, inferences, explicit
   decisions, and authorization gates. Hook detection runs no candidate or
   version command and adopts nothing.
3. Accept the exact digest with `pb init apply`. Apply stages the entire
   scaffold, refresh, structural check, and release-tier tests before writing.
4. If supplied, the first task is built only from explicit semantics. Resume
   with generated `./pb work resume`.
5. Assess hooks, collaboration, SCM, and mandatory domain triggers separately.
   Run the explicit project-check writer only after reviewing declared side
   effects and current authority.

## Established project

Use `scripts/pb.py adopt plan|apply`. Default semantic inspection is bounded to
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
./pb work start --help
./pb work close --help
./pb work handoff --help
./pb work resume
./pb maintain registry plan
./pb maintain hooks plan --help
./pb maintain collaboration plan --help
./pb maintain refresh --apply
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

Maintain decision questions in the project-owned governance register. Keep
recommendations, owner selections, and accepted `DEC-####` authority separate;
reconcile every decision and trade-off review exactly once and derive the
minimum closure graph before broad implementation. A read-only decision review
does not refresh generated outputs.

## Recovery

Run `./pb doctor` first. Structured diagnostics identify root cause, authority
source, dependent symptoms, safe next action, and whether repair is derived or
project-owned. Doctor is read-only unless the operator explicitly accepts a
derived-only repair digest.

- Pending journal: `./pb transaction recover --pending <path>` restores exact
  preimages only while all paths still match before or planned-after states.
- Applied receipt: `./pb transaction rollback --receipt <path>` refuses any
  independently changed post-apply path.
- Stale plan, evidence, or instruction fingerprint: re-plan; never force.
- Interrupted refresh: diagnose, run explicit derived refresh, then read-only
  check. Project-check evidence is not repaired by integrity refresh.

## Upgrade

`scripts/pb.py upgrade plan|apply` performs a three-way comparison among the
recorded old installed inventory, current project, and candidate snapshot. It
classifies unchanged pristine, exact-pristine update, project-modified,
additive, removed upstream, conflicting, derived, and provenance paths.

Automatic handling is limited to new noncolliding Blueprint-owned paths,
exact-pristine non-authoritative implementation assets, and derived
regeneration. Instructions, policy, project configuration/hooks, workflow
adoption, dossier sources/registries, records, current facts, stable IDs,
deletions/moves, permissions, and symlinks require proposal-bound review.

For 3.1→4.0, first run the reviewed legacy inventory seed workflow in
`migrate_3_1_0_to_4_0_0.py`. It refuses assessed collaboration and every unknown
static pristine baseline. The seed is never applied directly; the upgrader
rechecks it and produces the only mutation receipt. Run the migration and
release suites, then reassess adoption and readiness independently.

Earlier executable migrations remain closed reference transformations rather
than in-place upgrade tools. See the matching file under `migrations/`.
