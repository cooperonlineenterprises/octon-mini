# Guided setup fixtures

The `valid` answer batches are non-authorizing inputs. Tests replace their
all-zero `session_digest` with the exact current session digest before use.
They contain no project authority, credentials, endpoints, identities, or
standing external-action permission.

`invalid/mutations.json` is an executable mutation inventory. The guided setup
tests apply every named mutation to a current session or answer batch and
require a specific fail-closed diagnostic. A passing positive fixture alone is
not acceptance evidence.

Session, question-generation, and reinspection artifacts are written only to
test-owned temporary paths outside the target. Tests fingerprint the target
before and after read-only setup operations and never refresh generated
artifacts.
