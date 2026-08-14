# Guided Setup Worked Example

This example is domain-neutral and illustrative. Its values are not Project
Blueprint authority and must not be copied as project facts.

## Observed mode

An agent receives `/workspace/example` as the target. Read-only inspection
finds established source files, no `.project-blueprint-origin.json`, one root
`AGENTS.md`, and a local Git directory. The agent records:

- observation: target is an established project;
- observation: mode is `adoption`;
- observation: the instruction and target fingerprints;
- recommendation: assess Git because a local Git repository exists;
- unresolved: project name, assurance risk, layout, adoption authority,
  collaboration, hooks, workflow, packages, and work completion.

The recommendation is not an SCM selection.

## Conversation batches

The first batch asks three questions without preselection:

1. “What plain-language project name should the generated snapshot use?”
2. “Which assurance profile matches actual project risk and control needs?”
3. “How many humans currently have authority and practical ability to write or
   integrate changes?”

The user selects a name and Standard assurance because the project needs
durable traceability and periodic independent review. Collaboration evidence
is not yet current, so the user answers `unknown`. The session records:

- recommendation: a directory-derived name candidate;
- initialization input: the user-selected name;
- owner selection: `standard` with its risk rationale;
- unknown: write-capable-human count;
- no workflow recommendation or selection.

The second batch asks about layout, adoption authority, and governed work
completion. The user selects `compact`, supplies an exact
`authority:<project-adoption-scope>` reference, and selects on-demand work
completion. The session keeps these distinct:

- `compact` is an owner selection, not accepted policy authority;
- the adoption reference is recorded in the accepted-authority-reference
  inventory and still must resolve under the project process;
- on-demand work completion is a pending selection, not enabled.

The work-completion closure sequence reports, in order:

1. obtain current collaboration evidence;
2. select and accept one supported workflow;
3. install the content-addressed Git portfolio;
4. record exact repository, remote, and default branch;
5. assess the provider and exact hosted-check set;
6. select an allowed integration method, reviewers where required, and cleanup;
7. configure read-only validation hooks and the no-active-Git-hooks/inactive-
   `core.fsmonitor` controls; and
8. apply a separate reviewed work-completion configuration transaction.

Provider/check assessment, hook review, and assurance-reference collection may
run in parallel after the workflow and repository identity are known. No
external Git operation is authorized by any of these answers.

The user defers lint and build hook assessment. The session explains that
adoption can install the non-overwriting baseline, but final project adoption
and work-completion enablement remain blocked on explicit hook dispositions and
current evidence. Unknown and deferred states remain visible.

## Proposal and plan

The agent summarizes all observations, recommendations, selections, authority
references, unknowns, deferrals, and closure steps. It creates the existing
bounded adoption proposal. A possible functional equivalent is found, so the
agent does not fabricate an answer in the setup session. The user reviews the
existing proposal and supplies one exact proposal-digest-bound adoption review.

The agent then runs the existing adopter with `--setup-session`. The resulting
transaction plan:

- creates only absent Blueprint paths;
- preserves all project-owned files;
- binds the setup-session bytes and canonical digest;
- binds the adoption proposal, review, authority reference, and current target
  preimages;
- leaves adoption `in_progress`;
- leaves work completion disabled; and
- states that structural conformance is not implementation or readiness
  evidence.

Only after the user explicitly accepts the displayed transaction digest does
the existing apply engine run. Immediately before applying, it revalidates the
session, catalog, target, instructions, plan digest, and preimages.

## Separate conclusions

The completion report says:

- architecture quality: not assessed by setup;
- documentation completeness: generated baseline structurally present, with
  project content still incomplete;
- implementation evidence: not established;
- specialist approval: not established;
- release readiness: not assessed;
- production readiness: not assessed; and
- product efficacy or commercial viability: not assessed.

The example demonstrates orchestration and fail-closed state handling only.
