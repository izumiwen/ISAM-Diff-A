# Subagent Workflow for Phase Development and Formal Experiments

## Purpose

This workflow separates phase planning, implementation, engineering readiness,
formal execution, and research acceptance so that an agent does not certify
its own work. Read `AGENTS.md` and `docs/experiment_protocol.md` before using
this workflow.

## Roles

### Orchestrator

The primary agent assigns experiment IDs, coordinates the sequence, confirms
scope and authority, executes or delegates approved implementation work, and
reports the final state.

The orchestrator may not self-accept a formal experiment.

### Planner Subagent

The planner subagent drafts either an Engineering Discovery Plan or a Formal
Experiment Plan. It may read repository state, prior plans, result reports,
audit reports, configurations, and the experiment log.

It may write only:

- `reports/plans/{experiment_id}_plan.md`
- Related planning notes explicitly requested by the orchestrator

It must not modify source code, model implementations, datasets, baselines,
configs, historical artifacts, or execute formal training or evaluation.

For an Engineering Discovery Plan, it must state the discovery envelope,
permitted technical candidates, local-repair authority, finite repair budget,
required compatibility handoff, and escalation criteria. It must not use a
new plan to restate an in-scope local implementation repair.

### Developer Subagent

The developer implements only the approved phase plan. It may modify the
module, configuration, scripts, and tests named by that plan, and may run unit
tests, CLI checks, and short synthetic smoke tests needed to demonstrate the
implementation contract.

It must preserve unrelated work, must not change the research question,
baseline, dataset split, primary metric, or acceptance threshold, and must not
start a formal training, evaluation, inference, or dataset-validation run
without the required execution authority.

The developer records the exact changed paths, commands, and observed output
needed for an engineering audit. It does not write its own audit or acceptance
decision.

Within the declared interface and discovery envelope, the developer may repair
local compile, import, command, working-directory, include-path, receipt, and
already-declared data or tensor-shape defects without a new planner pass. Each
repair must have a reproducing or regression test and retained raw diagnostic
output. The developer must stop at the plan's repair budget or escalation
criterion.

The developer escalates to the planner when a repair changes or exposes an
ambiguous module interface, data/tensor contract, architecture, baseline,
dataset split, metric, threshold, hypothesis, or method identity. It escalates
missing approval or required environment/artifact access as **BLOCKED** rather
than silently selecting an alternative.

### Engineering Auditor Subagent

The engineering auditor must not have planned or developed the phase. It is
read-only by default and may run non-destructive checks required by the plan,
including imports, CLI help, config validation, short synthetic smoke tests,
and assertions over declared data or tensor shapes.

It writes only:

- `reports/audits/{experiment_id}_implementation_audit.md`
- Temporary verification outputs that do not alter research artifacts

It must not repair code, change configurations, replace data, or treat an
implementation check as evidence that a research hypothesis is true.

For a non-accepted implementation audit, it must record exactly one repair
disposition:

- `LOCAL_REPAIR`: developer may apply a scoped repair without a new plan.
- `DISCOVERY_ENVELOPE`: developer may continue within the plan's declared
  technical candidates and repair budget.
- `CONTRACT_ESCALATION`: planner must clarify or revise the implementation
  contract.
- `RESEARCH_ESCALATION`: planner and, when required, the user must authorize a
  research-boundary change.
- `ENVIRONMENT_BLOCKED`: required authority, artifact, or environment is
  unavailable; no fallback is allowed.

### Executor

The executor carries out an authorized plan and records actual outputs. The
executor may be the orchestrator or a separately delegated implementation
agent, but it must not be the acceptance auditor.

The executor must not silently change the plan. Material deviations require a
new or revised plan and must be recorded.

### Research Auditor Subagent

The research auditor must not have drafted the plan, developed the phase, or
executed the experiment being audited. It is read-only by default.

It may inspect artifacts and run non-destructive checks, including config and
metadata comparison, checksum inspection, log inspection, output validation,
and metric recomputation from existing artifacts when practical.

It may write only:

- `reports/audits/{experiment_id}_audit.md`
- Temporary verification outputs that do not alter research artifacts

It must not repair code, edit configs, alter checkpoints or predictions, rerun
formal training for a better result, or infer missing evidence from summaries.

### Recorder Subagent

The recorder appends a concise, evidence-linked entry to
`reports/experiment_log.md` after an engineering audit, formal experiment, or
research audit. It may read the relevant approved plan, result, and audit, but
must not change source code, configs, outputs, plans, results, or audits.

The recorder must not have planned, developed, executed, or audited the same
phase.

It records the stated scope and status exactly, including **Observed**,
**Supported**, **Unproven**, and **Blocked** boundaries. It must not turn an
engineering audit into a research conclusion or reinterpret an auditor's
finding.

The recorder also creates one status dossier without duplicating or moving
canonical artifacts:

- Every engineering audit: `reports/archive/implementation/{status}/{experiment_id}/`
- Formal result `Failure` or `Interrupted`:
  `reports/archive/failed/{experiment_id}/`
- Formal result `Blocked` or research audit `BLOCKED`:
  `reports/archive/blocked/{experiment_id}/`
- Research audit `INCOMPLETE` or `REJECTED`:
  `reports/archive/incomplete/{experiment_id}/` or
  `reports/archive/rejected/{experiment_id}/`, respectively
- Research audit `ACCEPTED`: `reports/accepted/{experiment_id}/`

Each dossier identifies the status, links to the plan, result when present,
audit, and output directory, and states required follow-up. The recorder may
add an **ACCEPTED** experiment to `reports/accepted/index.md` only after the
independent research audit. This success-only surface must never include a
failed, blocked, rejected, incomplete, or engineering-only outcome.

## Required Sequence

Run the following sequence in order for each phase that leads to a formal
experiment:

1. Orchestrator assigns the experiment ID.
2. Planner subagent decides whether a bounded Engineering Discovery Plan is
   required. If so, it completes the discovery phase, engineering audit, and
   compatibility handoff before a separate Formal Experiment Plan is written.
3. Planner subagent writes the applicable plan.
4. Orchestrator confirms that development is authorized.
5. Developer implements the bounded phase and records implementation evidence.
6. Engineering auditor independently verifies the implementation contract and,
   if non-accepted, records a repair disposition.
7. Recorder appends the engineering-audit outcome to the experiment log and
   creates its archive dossier.
8. For `LOCAL_REPAIR` or `DISCOVERY_ENVELOPE`, the developer continues within
   the approved scope and budget, then returns to step 5. For any escalation or
   exhausted budget, stop and preserve the engineering-audit evidence.
9. A discovery **ACCEPTED** handoff requires a separate Formal Experiment Plan
   and its own development gate before formal execution may be authorized.
10. Orchestrator confirms that formal execution is authorized.
11. Executor runs the formal plan and writes the result report.
12. Recorder appends the execution outcome and result path without claiming
   acceptance.
13. Research auditor performs an independent audit.
14. Recorder appends the audited outcome to the experiment log.

Do not run the planner, developer, engineering auditor, executor, research
auditor, and recorder concurrently on the same phase. Their responsibilities
must remain temporally and logically separate.

## Engineering Audit Report

The engineering auditor must create:

`reports/audits/{experiment_id}_implementation_audit.md`

Use this template:

```md
# {experiment_id}: Implementation Audit

## Audit Status

ACCEPTED | INCOMPLETE | REJECTED | BLOCKED

## Scope Audited

## Changed Paths and Plan Boundary

## Code and CLI Checks

## Configuration Contract

## Data and Tensor Shape Checks

## Tests and Smoke Checks

## Findings

## Repair Disposition

## Research-Claim Boundary

## Required Follow-up
```

An engineering **ACCEPTED** status means only that the declared implementation
contract passed the recorded checks. It is not a formal experiment acceptance.

## Research Audit Report

The research auditor must create:

`reports/audits/{experiment_id}_audit.md`

Use this template:

```md
# {experiment_id}: Acceptance Audit

## Audit Status

ACCEPTED | INCOMPLETE | REJECTED | BLOCKED

## Scope Audited

## Evidence Inspected

## Protocol Compliance

## Comparison Validity

## Control Verification

## Artifact and Provenance Verification

## Metric Traceability

## Claim Boundary Review

## Findings

## Required Follow-up
```

The audit must verify:

- Consistency among experiment ID, plan, config, command, Git state, and output
  directory.
- Validity of the stated baseline and comparison conditions.
- Isolation of the primary variable, or explicit disclosure of all additional
  changes.
- Completion of required controls.
- Compliance of dataset usage and split with the plan.
- Existence of required metadata, logs, checkpoints, predictions, and outputs.
- Traceability of reported metrics to saved artifacts.
- Compliance with declared stopping and acceptance criteria.
- Whether the conclusion exceeds the available evidence.

## Audit Status Definitions

- **ACCEPTED:** All required evidence and pre-declared acceptance criteria are
  satisfied.
- **INCOMPLETE:** The experiment ran, but required controls, artifacts, or
  evidence are missing. It cannot support a research claim.
- **REJECTED:** A protocol violation, invalid comparison, data leakage,
  untraceable metric, or other validity failure invalidates the experiment.
- **BLOCKED:** Required resources or information are unavailable, preventing a
  complete audit.

Only **ACCEPTED** experiments may be cited as completed evidence in subsequent
plans, summaries, or paper claims. If an independent auditor is unavailable,
the formal acceptance status is **BLOCKED**.
