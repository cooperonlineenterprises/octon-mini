# 3.1.0 to 4.0.0 live-snapshot fixture

The executable fixture is built dynamically by
`scripts/test_migration_3_1_0_to_4_0_0.py`. It creates a disposable separated
snapshot, adds task and evidence records, rewrites only the versioned 3.1-era
contract markers, and then exercises reviewed inventory seeding plus the live
three-way upgrader.

The fixture verifies:

- read-only inspection and unchanged target bytes;
- exact old-baseline review binding and deterministic seed generation;
- stale-seed and changed-path refusal;
- proposal-bound review of every non-automatic path;
- staged apply, structural validation, exact receipt generation, rollback,
  and rollback refusal after an independent change; and
- separation of structural conformance, harness adoption, and readiness.

This is a deterministic contract fixture, not a claim that every historical
3.1 repository has the same pristine bytes. A real 3.1 project must provide
its reviewed old baseline hashes. Unknown static baselines, assessed legacy
collaboration, authority conflicts, symlinks, moves, deletions, permissions,
or modified project-owned paths remain manual review gates.
