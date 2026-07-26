# Experiment Protocol

## Scope

This protocol governs every formal experiment: a run intended to produce
research evidence, compare methods, support a decision, or appear in a report.
It does not apply to formatting, import checks, unit tests, or isolated smoke
tests that are clearly labelled as non-formal.

Read `AGENTS.md` and the latest relevant entries in
`reports/experiment_log.md` before applying this protocol.

## Planning Hierarchy and Development Gate

A project-level research plan defines the research direction, module roles,
phase order, and decision boundaries. It is a roadmap, not an authorization to
implement a module or execute a run. Each formal experiment must be traced to
a bounded phase and its approved plan.

## Engineering Discovery Plans

An Engineering Discovery Plan is an optional, non-formal phase used to resolve
technical feasibility before freezing a formal experiment contract. It is the
appropriate place to explore a bounded toolchain or dependency cohort, native
build closure, import path, command contract, data contract, or tensor-shape
implementation. It must not produce a research metric, comparison, or claim.

The planner writes one bounded discovery plan rather than a new formal plan for
each local compile or shape failure. The plan must declare:

- frozen research boundary and immutable source/baseline identity;
- permitted technical candidates and forbidden fallbacks;
- local-repair authority for the developer;
- finite elapsed-time, candidate-combination, and smoke-check repair budget;
- required raw logs, regression tests, and compatibility handoff;
- stopping and escalation criteria.

The discovery plan does not authorize a CUDA, PyTorch, system, dataset, or
research-decision change that otherwise requires approval. Its engineering
audit may establish a compatibility handoff, but never formal experiment or
research acceptance. A subsequent formal experiment plan must cite that
handoff and freeze one compatible contract.

Before a formal experiment may execute, the planner, developer, and
engineering auditor complete a development gate. If a discovery phase is
needed, it completes before the formal experiment plan is frozen:

1. A planner subagent writes `reports/plans/{experiment_id}_plan.md` and
   declares its type as `Engineering Discovery` or `Formal Experiment`.
2. A developer subagent implements only the approved scope and adds or updates
   the smallest relevant tests.
3. An independent engineering auditor verifies the implementation contract:
   code and CLI execution, config contract, declared data and tensor shapes,
   and applicable short smoke tests. The auditor writes
   `reports/audits/{experiment_id}_implementation_audit.md`.
4. A recorder subagent appends the engineering outcome and evidence paths to
   `reports/experiment_log.md` and creates an implementation archive dossier
   at `reports/archive/implementation/{status}/{experiment_id}/`.

The engineering audit must state its scope explicitly. For an Engineering
Discovery Plan, **ACCEPTED** means that the declared compatibility handoff is
complete. For a Formal Experiment Plan, it means that the audited
implementation is ready for the declared formal run. Neither meaning supports
a method, metric, or paper claim.

## Experiment Lifecycle

1. Assign a unique experiment ID.
2. Complete the development gate above.
3. Confirm execution authority and resource availability.
4. The recorder records the planned formal experiment in
   `reports/experiment_log.md`.
5. The executor runs the approved plan without unrecorded protocol changes.
6. Create a result report regardless of outcome.
7. The recorder records the execution outcome and result path in
   `reports/experiment_log.md` without claiming acceptance. A failed,
   interrupted, or blocked execution also receives an archive dossier.
8. Obtain an independent research audit under `docs/subagent_workflow.md`.
9. The recorder records the audited outcome in `reports/experiment_log.md`.
   Only a research audit with status **ACCEPTED** receives an entry under
   `reports/accepted/{experiment_id}/`; every other audit status receives an
   archive dossier under its matching status directory.

Only an audited experiment with status **ACCEPTED** may be used as completed
evidence in later plans, summaries, or paper claims.

## Plan Requirements

The planner subagent must create:

`reports/plans/{experiment_id}_plan.md`

Use this template:

```md
# {experiment_id}: {short title}

## Plan Type

Engineering Discovery | Formal Experiment

## Status

Draft | Approved | Superseded | Cancelled

## Objective

## Hypothesis

## Baseline and Comparison

## Dataset and Split

## Fixed Conditions

## Primary Variable

## Required Controls

## Configuration and Resource Budget

## Metrics and Evaluation Procedure

## Acceptance Criteria

## Failure and Stopping Criteria

## Expected Artifacts

## Risks and Validity Threats
```

The plan must make every comparison fair by declaring the dataset, split,
preprocessing, resolution, seed policy, evaluation procedure, compute budget,
checkpoint policy, and any method-specific exceptions.

It must also identify the project-level plan and phase that authorize its
scope, plus the implementation contract that the engineering audit must check.

An Engineering Discovery Plan additionally declares its discovery envelope,
local-repair authority, finite repair budget, compatibility handoff, and
escalation criteria. A Formal Experiment plan identifies any accepted
engineering-discovery handoff and freezes one compatible technical contract.

## Experimental Design Rules

Each ablation changes one primary variable while holding the declared fixed
conditions constant. If multiple changes are required, label the experiment as
a combined configuration rather than an ablation.

Do not use held-out test data for model selection, threshold selection,
hyperparameter tuning, or failure-driven iteration. Do not modify a baseline
without assigning a new configuration and disclosing the difference.

Required controls must be completed before a causal claim is accepted. A
missing control makes the result incomplete, not implicitly negative or
positive.

## Result Requirements

After every formal experiment, create:

`reports/results/{experiment_id}_result.md`

Use this template:

```md
# {experiment_id}: Result

## Status

Success | Failure | Interrupted | Inconclusive | Blocked

## Executed Protocol

## Deviations from Plan

## Evidence

## Metrics

## Comparison with Closest Valid Baseline

## Interpretation

### Supported

### Not Supported

### Unproven

## Artifact Paths

## Recommended Next Action
```

Record deviations honestly. A run with a material undeclared deviation must not
be treated as an execution of the original plan.

## Acceptance Rules

Acceptance criteria must be defined before execution and must be measurable.
They may include required artifacts, valid controls, expected engineering
behavior, metric thresholds, or pre-registered decision rules.

Acceptance must not depend solely on a desirable metric. It requires valid
provenance, a fair comparison, protocol compliance, and an evidence-backed
interpretation.

## Experiment Log Entry Format

Append entries to `reports/experiment_log.md` using:

```md
## YYYY-MM-DD — [Experiment ID or Task ID] — [Status]

- **Objective:**
- **Change or decision:**
- **Evidence:**
- **Interpretation:**
- **Artifacts:**
- **Next action:**
```

Use dated corrections instead of editing historical entries.

For development-gate entries, identify the phase, implementation audit status,
tests or smoke checks performed, and the linked plan and audit paths. The
recorder must not convert engineering readiness into a research conclusion.

## Accepted Review and Archive Dossiers

`reports/accepted/` is a success-only review surface, not a second research
ledger. Its index and per-experiment entries may list only independently
research-audited **ACCEPTED** experiments, with links to the canonical plan,
result, audit, and output paths.

Every engineering audit receives an archive dossier at:

`reports/archive/implementation/{status}/{experiment_id}/`

Every formal outcome receives an archive dossier according to this category
mapping: `Failure` and `Interrupted` use `failed/`; `Blocked` uses `blocked/`;
research-audit `REJECTED` uses `rejected/`; and research-audit `INCOMPLETE`
uses `incomplete/`. The dossier must state the terminal status, exact evidence
paths, and required follow-up. It is an index to canonical immutable artifacts,
not a reason to move, delete, overwrite, or conceal them.

The append-only `reports/experiment_log.md` remains the complete concise index
of all outcomes. This layout applies to future work only; historical artifacts
are not relocated without explicit authorization.
