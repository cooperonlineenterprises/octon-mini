# Guided setup reference

Read this reference when initializing, adopting, or upgrading through a
conversation, TTY, or answer file. For the complete contract, read the bundled
`assets/octon-mini-source/docs/GUIDED_SETUP.md` and the authoritative
`assets/octon-mini-source/shared/source-contracts/setup-questions.json`.

Command examples use `./octon` on Unix/macOS. On Windows, invoke the same
extensionless launcher and arguments as `python -B octon` or `py -3 -B octon`.
This changes only interpreter entry, not command identity, setup semantics, or
authority.

## Required sequence

1. Read target instructions and run the mode-specific `setup` command without
   output first when only question generation is requested.
2. Stop if mode is ambiguous. Do not choose init, adopt, or upgrade from user
   wording when target evidence contradicts it.
3. Report observations separately. Do not ask for facts that were safely
   observed.
4. Ask the emitted questions in order, normally one to three. Do not preselect
   a choice. State the catalog recommendation separately.
5. Preserve allowed `unknown`, `deferred`, and `not_applicable` states and say
   what each blocks.
6. Bind every answer batch to the exact session digest. Store no secret,
   credential, unnecessary identity, endpoint, or runtime authorization.
7. Write sessions only to explicit paths outside the target. Create an
   immutable successor; never overwrite the prior session.
8. Reinspect on changed target/revision, instructions, catalog, Octon Mini
   version/provenance, or material evidence. Re-answer factual values and
   selections; do not silently carry them forward.
9. Summarize recommendations, selections, accepted-authority references,
   unknowns, deferrals, blockers, and the minimum dependency-ordered closure
   sequence, including parallel-safe steps.
10. Pass the reviewed session to the existing `plan --setup-session` command.
    Optionally record the exact plan through `setup --record-plan` into a new
    immutable session successor. Require explicit acceptance of the resulting
    plan digest before apply.

## Authority checks

- A recommendation is not a user selection.
- A user selection is not accepted authority.
- An `authority:` or `external:` reference is stored separately and must still
  resolve under the project process.
- Adoption and upgrade proposal/review artifacts remain authoritative for their
  dispositions.
- Setup never authorizes commit, push, PR, review, merge, synchronization,
  cleanup, package install, hook execution, or provider access.

## Work completion

Offer exactly disabled, on-demand, or on-demand plus plan-only closure-event
planning. Offer no automatic apply. An enabling selection remains pending
until the session reports every Git portfolio, workflow authority, repository,
provider, check, reviewer, integration, hook, hidden-Git-effect, cleanup, and
assurance prerequisite closed. Apply those changes later through existing
project-owned decision, package, collaboration, hook, and configuration
transactions.

## Reporting

Report structural conformance, adoption, implementation evidence, specialist
approval, release readiness, production readiness, and efficacy/commercial
viability separately. Setup completion proves none of the higher states.
