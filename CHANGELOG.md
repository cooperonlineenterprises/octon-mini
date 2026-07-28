# Changelog

All notable blueprint contract changes are recorded here. Project-specific
snapshots do not upgrade automatically.

## 1.0.0 — 2026-07-27

First stable domain-neutral kernel release.

### Added

- self-contained project dossier blueprint with evidence-labeled reference
  crosswalk, 4-digit artifact taxonomy, coverage profiles, core
  specifications, lifecycle, governance, adoption gates, and new
  recommendations;
- evidence-labeled 17-section harness blueprint and source-evidence record;
- strict JSON seven-file governance kernel and local schema snapshot;
- generated artifact catalog and per-file path-authority mirror;
- transactional new-project generation and read-only existing-project
  adoption planning;
- cross-record reference, transition, traceability, plan-DAG, nested
  instruction, extension, secret-redaction, checksum, and freshness
  validation;
- restrictions-only versioned extension API with a disable-safe reference
  extension;
- mutually consistent high-assurance refresh outputs with shared generation
  IDs;
- Minimal, Standard, and High-Assurance end-to-end and adversarial acceptance
  tests;
- migration, release, installation, and CI guidance.

### Changed

- canonical structured outputs moved from constrained YAML to strict JSON;
- stable dossier record and artifact identifiers use four numeric digits;
- generated dossier registries start empty and unadopted rather than seeding
  active or authoritative project claims;
- integrity fingerprints cover the whole repository by default.

### Removed

- direct in-place generation into existing repositories;
- regex-only constrained-YAML validation;
- disconnected high-assurance checksum refresh behavior.
