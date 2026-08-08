# Subagent Workflow for Phase Development and Formal Experiments

## Purpose

This workflow separates material phase planning, implementation, engineering
readiness, formal execution, research acceptance, and administrative recording
so that an agent does not certify its own research work.

It governs:

- delegated Engineering Discovery handoffs;
- Formal Experiment development and readiness;
- authorized formal execution;
- independent research acceptance; and
- decision-changing engineering escalations.

It does not require a full multi-role lifecycle for:

- routine diagnostics;
- authorized local repairs;
- import, CLI, parser, fixture, or path checks;
- isolated smoke tests;
- implementation preflights;
- non-formal pilots; or
- other work excluded from formal scope by `docs/experiment_protocol.md`.

Whether work is formal or non-formal is determined by
`docs/experiment_protocol.md`. This workflow must not enlarge that scope.

Read `AGENTS.md`, `docs/experiment_protocol.md`, and the latest relevant entries
in `reports/experiment_log.md` before using this workflow.

Role separation is based on decision risk and conflict of interest rather than
a mechanical requirement that every named role be assigned to a different
agent. The independence requirements stated for Engineering Auditor and
Research Auditor remain mandatory.

## Roles

### Orchestrator

The primary agent:

- assigns experiment or task IDs when required;
- classifies work as routine engineering, Engineering Discovery, or Formal
  Experiment;
- confirms scope and authority;
- coordinates the applicable sequence;
- executes or delegates approved implementation and execution work;
- verifies that required audits occur at the correct handoff; and
- reports the final state.

The orchestrator may perform or delegate implementation, execution, and
administrative recording when permitted by the applicable plan.

The orchestrator must not act as the independent Research Auditor for a Formal
Experiment in which it drafted the plan, developed the implementation, or
executed the research work.

The orchestrator must not reinterpret an auditor's verdict, promote engineering
readiness into research acceptance, or strengthen a claim beyond the canonical
plan, result, and audit.

### Planner Subagent

The planner subagent drafts either:

- an Engineering Discovery Plan when a material technical uncertainty requires
  a bounded discovery envelope; or
- a Formal Experiment Plan when formal research execution is proposed.

A planner is required only when:

- a new plan is required;
- a material contract must be revised or clarified;
- a discovery envelope or repair budget must be expanded;
- new environment, artifact, data, resource, or external authority is required;
  or
- the research boundary or interpretation of evidence would change.

The planner must not create a successor plan merely to authorize an in-scope
local repair already covered by:

- an approved plan;
- an approved discovery envelope;
- `AGENTS.md`; or
- the declared local-repair authority of the developer.

The planner may read repository state, prior plans, result reports, audit
reports, configurations, and the experiment log.

It may write only:

- `reports/plans/{experiment_id}_plan.md`
- Related planning notes explicitly requested by the orchestrator

It must not modify source code, model implementations, datasets, baselines,
configs, historical artifacts, or execute formal training or evaluation.

For an Engineering Discovery Plan, it must state:

- the discovery envelope;
- frozen research boundary;
- immutable source or baseline identity;
- permitted technical candidates;
- forbidden fallbacks;
- local-repair authority;
- finite repair budget;
- required compatibility handoff;
- material blocker conditions; and
- stopping and escalation criteria.

It must not use a new plan to restate an in-scope local implementation repair.

For a version or toolchain transition, the planner defines the exact authorized
transition boundary and cites the operational procedure in
`docs/run_standard.md`.

The plan must identify the affected source, build, API, ABI, runtime, package,
device, and interface contracts that are material to the handoff. It must mark
missing authority or material compatibility evidence **BLOCKED** or
`CONTRACT_ESCALATION`, not infer compatibility from resolver or installation
success.

### Developer Subagent

The developer implements only the approved plan or authorized local engineering
scope.

It may modify the module, configuration, scripts, and tests named by that scope,
and may run:

- unit tests;
- import checks;
- CLI checks;
- parser and fixture checks;
- short synthetic smoke tests; and
- bounded diagnostics needed to demonstrate the implementation contract.

It must preserve unrelated work.

It must not change, without required planning and authority:

- the research question;
- method or model identity;
- architecture;
- baseline identity;
- dataset or split;
- checkpoint or VAE;
- research-relevant preprocessing;
- primary metric or evaluation procedure;
- acceptance criterion;
- stopping rule;
- required control; or
- research claim boundary.

It must not start a formal training, evaluation, inference, or
dataset-validation run without the required execution authority.

The developer records the exact changed paths, commands, and observed outputs
needed for the applicable engineering handoff. It does not write its own audit
or acceptance decision.

Within the declared interface and discovery envelope, the developer may repair
local defects without a new planner pass, including:

- compile and import defects;
- command and working-directory defects;
- include-path defects;
- parser and fixture defects;
- Markdown and path-representation defects;
- receipt and log-capture implementation defects; and
- already-declared data or tensor-shape defects.

A local repair within the approved scope does not require:

- a new plan;
- a new experiment ID;
- a separate audit for each attempt;
- a separate experiment-log entry for each attempt; or
- a separate archive dossier for each attempt.

Each bounded repair must have an appropriate reproducing or regression check.

Retain:

- the first reproducing failure;
- the final verification evidence; and
- additional intermediate diagnostics only when they are needed to explain a
  material decision, regression, incident, or escalation.

The developer batches bounded repairs and presents the stabilized implementation
for audit when the applicable handoff criterion is reached.

The developer must stop when:

- the plan's repair budget is exhausted;
- a stopping criterion is reached;
- a material contract ambiguity is discovered;
- a required authority or artifact is unavailable; or
- a proposed repair would change the research boundary.

For a version or toolchain transition, the developer must preserve the required
pre-change evidence before mutating the target environment and follow the
procedure in `docs/run_standard.md`.

An incompatible source, API, ABI, build, runtime, or device contract without
authorized equivalence evidence is an escalation, not a silent compatibility
patch.

The developer escalates when a repair changes or exposes ambiguity in:

- module interface;
- data or tensor contract;
- architecture;
- baseline;
- dataset or split;
- checkpoint or VAE;
- metric or threshold;
- hypothesis;
- stopping rule; or
- method identity.

Missing approval or required environment, artifact, data, or resource access is
reported as **BLOCKED**, not resolved through an unauthorized fallback.

### Engineering Auditor Subagent

The engineering auditor verifies a declared implementation or compatibility
handoff.

An Engineering Auditor is required for:

- a final Engineering Discovery compatibility handoff;
- Formal Experiment implementation readiness;
- a target environment or toolchain transition;
- a material terminal engineering blocker or incident; or
- an intermediate gate explicitly required by the plan because of material
  risk.

An Engineering Auditor is not required for every intermediate local repair,
diagnostic attempt, parser correction, fixture correction, or smoke-test
failure within an approved scope.

The engineering auditor must not have implemented the work being audited.

Planning participation alone does not automatically disqualify an engineering
auditor when:

- the acceptance contract is objective and unambiguous;
- the auditor did not implement the audited work; and
- the auditor is not interpreting its own unresolved planning ambiguity.

When the planner would be interpreting its own ambiguous contract, use a
separate auditor or escalate the contract.

The engineering auditor is read-only by default and may run non-destructive
checks required by the plan, including:

- imports;
- CLI help;
- configuration validation;
- parser and fixture checks;
- short synthetic smoke tests;
- checksum and metadata inspection;
- device checks; and
- assertions over declared data or tensor shapes.

For a version or toolchain transition, the auditor verifies the material
handoff requirements defined by the plan and `docs/run_standard.md`, including:

- required evidence predating target-environment mutation;
- compliance with the authorized transaction boundary;
- preservation of declared interfaces and behavior;
- required build, import, runtime, and device evidence; and
- absence of unauthorized fallback.

It writes only:

- `reports/audits/{experiment_id}_implementation_audit.md`
- Temporary verification outputs that do not alter research artifacts

It must not:

- repair code;
- change configurations;
- replace data;
- create missing evidence;
- modify canonical artifacts; or
- treat an implementation check as evidence that a research hypothesis is
  true.

The engineering auditor classifies findings as:

- **Blocking Finding:** prevents the declared engineering handoff because it
  affects a material contract, evidence requirement, reproducibility, or
  authorized boundary.
- **Non-Blocking Correction:** should be corrected or clarified but does not
  prevent verification of the declared handoff.
- **Observation:** relevant context that does not require correction.
- **Follow-up Recommendation:** prospective improvement outside the current
  acceptance requirement.

An implementation audit may be **ACCEPTED** with documented non-blocking
corrections when all evidence material to the declared handoff is satisfied.

For a non-accepted implementation audit, it records one repair disposition:

- `LOCAL_REPAIR`: the developer may apply a scoped repair without a new plan.
- `DISCOVERY_ENVELOPE`: the developer may continue within the approved
  technical candidates and repair budget.
- `CONTRACT_ESCALATION`: the planner must clarify or revise a material
  implementation contract.
- `RESEARCH_ESCALATION`: the planner and, when required, the user must authorize
  a research-boundary change.
- `ENVIRONMENT_BLOCKED`: required authority, artifact, environment, data, or
  resource is unavailable; no unauthorized fallback is allowed.

### Executor

The executor carries out an authorized Formal Experiment Plan and records the
actual outputs.

The executor may be:

- the orchestrator;
- the developer; or
- a separately delegated implementation agent.

The executor must not be the Research Auditor for the same Formal Experiment.

The executor must not silently change the plan.

Material deviation is defined by `docs/experiment_protocol.md`. A material
deviation requires stopping, disclosure, revised planning, or a new
configuration identity as required by that protocol.

A non-material administrative, formatting, path, receipt, or logging defect
must be disclosed and corrected, but it does not by itself redefine the
scientific execution.

A pre-execution engineering failure is not a formal execution outcome when the
formal child process, data processing, model execution, or metric execution
never began.

### Research Auditor Subagent

The Research Auditor performs independent scientific acceptance review.

The Research Auditor must not have:

- drafted the Formal Experiment Plan;
- developed the implementation;
- executed the experiment; or
- altered the formal evidence being audited.

This independence requirement must not be waived merely because the result is
negative, failed, inexpensive, or inconvenient to review.

The Research Auditor is read-only by default.

It may inspect artifacts and run non-destructive checks, including:

- plan, config, command, and metadata comparison;
- source and Git-state inspection;
- checksum inspection;
- raw-log inspection;
- output validation;
- split and manifest verification;
- checkpoint and VAE identity verification; and
- metric recomputation from existing artifacts when practical.

It may write only:

- `reports/audits/{experiment_id}_audit.md`
- Temporary verification outputs that do not alter research artifacts

It must not:

- repair code;
- edit configs;
- alter checkpoints, predictions, manifests, or outputs;
- rerun formal training for a better result;
- create missing required controls;
- infer missing evidence from summaries; or
- strengthen a claim beyond the available evidence.

The Research Auditor evaluates material scientific validity separately from
administrative conformance.

Non-material documentation, formatting, path, receipt, or logging defects must
be reported, but they do not by themselves invalidate an otherwise verifiable
result.

Independent research audit is required before a Formal Experiment result is:

- promoted to completed research evidence;
- used to authorize a later research decision;
- used as an accepted baseline;
- summarized as a supported result; or
- cited in a report, presentation, or paper claim.

### Recorder Function

Recording is an administrative function, not an acceptance authority.

The recorder function may be performed by:

- the orchestrator; or
- another agent that did not issue the research acceptance decision.

It does not require a separate independent subagent for every phase.

The recorder appends a concise, evidence-linked entry to
`reports/experiment_log.md` only for events permitted by
`docs/experiment_protocol.md`, including:

- authorization of a Formal Experiment;
- a meaningful formal start;
- a terminal Formal Experiment outcome;
- an independent research-audit decision;
- an accepted engineering compatibility handoff;
- a material engineering blocker that changes feasibility, schedule, plan, or
  claim boundary; or
- new evidence that changes a research decision.

The recorder must not append separate entries for:

- intermediate discovery attempts;
- local repairs within an approved envelope;
- unit, import, CLI, parser, fixture, or smoke-test failures;
- formatting or Markdown corrections;
- receipt finalization;
- checksum-index formatting; or
- repeated status updates that do not change the research state.

The recorder may read the relevant canonical plan, result, audit, and artifact
paths, but must not change source code, configs, outputs, plans, results, or
audits as part of the recording function.

It records the stated scope and status exactly, including **Observed**,
**Supported**, **Unproven**, and **Blocked** boundaries.

It must not:

- turn an engineering audit into a research conclusion;
- reinterpret an auditor's finding;
- change an audit status;
- create missing evidence; or
- strengthen a claim.

The recorder creates a status dossier only when the applicable trigger in
`docs/experiment_protocol.md` is satisfied.

Engineering dossier path:

`reports/archive/implementation/{status}/{experiment_id}/`

Formal archive paths:

- Formal result `Failure` or `Interrupted`:
  `reports/archive/failed/{experiment_id}/`
- Formal result `Blocked` or research audit `BLOCKED`:
  `reports/archive/blocked/{experiment_id}/`
- Research audit `INCOMPLETE`:
  `reports/archive/incomplete/{experiment_id}/`
- Research audit `REJECTED`:
  `reports/archive/rejected/{experiment_id}/`
- Research audit `ACCEPTED`:
  `reports/accepted/{experiment_id}/`

Intermediate local-repair failures, routine non-material findings, formatting
corrections, receipt finalization, and repeated smoke-test attempts do not
receive separate dossiers.

Each required dossier:

- identifies the exact status;
- links to canonical plan, result when present, audit, log, and output paths;
- states why the outcome is material enough to preserve;
- records required follow-up; and
- does not duplicate, move, overwrite, or replace canonical artifacts.

The recorder may add an **ACCEPTED** experiment to the accepted review surface
only after an independent Research Audit.

The accepted surface must never include a failed, blocked, rejected,
incomplete, or engineering-only outcome.

The operational archive layout and dossier-construction procedure are defined
in `reports/archive/README.md`.

## Required Sequence

The orchestrator first classifies the work according to
`docs/experiment_protocol.md`.

### Routine Engineering and Authorized Local Repair

Routine engineering and local repairs already authorized by `AGENTS.md`, an
approved plan, or an approved discovery envelope do not enter the complete
multi-role lifecycle.

The applicable sequence is:

1. Confirm the existing scope and authority.
2. Reproduce the issue when practical.
3. Apply bounded repairs within the declared interface.
4. Run the relevant regression, unit, CLI, parser, fixture, or smoke check.
5. Preserve the first reproducing failure and final verification evidence.
6. Escalate only if a material contract, authority, resource, or research
   boundary is reached.

No separate plan, experiment ID, audit, experiment-log entry, or archive
dossier is required for each intermediate repair attempt.

### Engineering Discovery

When a material technical uncertainty requires Engineering Discovery:

1. Orchestrator assigns the bounded discovery ID when required.
2. Planner writes one Engineering Discovery Plan.
3. Orchestrator confirms development authority.
4. Developer works within the discovery envelope and repair budget.
5. Developer batches bounded repairs and stabilizes the declared compatibility
   handoff.
6. Engineering Auditor reviews the final handoff.
7. If the audit disposition is `LOCAL_REPAIR` or `DISCOVERY_ENVELOPE`, the
   developer continues within the same plan and budget, then returns to step 5.
8. If the audit requires `CONTRACT_ESCALATION`,
   `RESEARCH_ESCALATION`, or `ENVIRONMENT_BLOCKED`, stop and preserve the
   material evidence.
9. The recorder function appends one concise ledger entry and creates a dossier
   only for:
   - an accepted compatibility handoff;
   - a material terminal blocker;
   - a target environment or toolchain transition; or
   - a material incident.
10. An accepted discovery handoff establishes only the declared engineering
    compatibility. A separate Formal Experiment Plan is still required before
    formal execution.

### Formal Experiment

For a Formal Experiment:

1. Orchestrator assigns the experiment ID.
2. Planner writes the Formal Experiment Plan.
3. Orchestrator confirms development authority.
4. Developer implements the bounded formal contract.
5. Engineering Auditor independently verifies Formal Experiment readiness.
6. For an in-scope local repair, the developer repairs within the same plan and
   returns to step 5 without a new experiment ID or separate ledger entry.
7. For a material escalation, stop and obtain revised planning or authority.
8. Orchestrator confirms formal execution authority.
9. Executor runs the Formal Experiment and writes the result report when formal
   execution began.
10. Recorder appends the meaningful execution outcome without claiming
    research acceptance.
11. Before the result is promoted, reused, or cited as completed evidence, the
    Research Auditor performs an independent audit.
12. Recorder appends the research-audit outcome and creates the required
    accepted or archive dossier.

Roles that determine or audit the same artifact must remain temporally and
logically separated.

Independent preparatory work on unrelated artifacts may proceed in parallel
when it:

- cannot influence the audited decision;
- cannot mutate shared canonical evidence;
- does not violate an applicable plan; and
- does not create ambiguity about responsibility.

The Research Auditor must never operate concurrently with execution or evidence
mutation for the Formal Experiment being audited.

## Engineering Audit Report

The Engineering Auditor creates:

`reports/audits/{experiment_id}_implementation_audit.md`

Use this template:

```md
# {experiment_id}: Implementation Audit

## Audit Status

ACCEPTED | INCOMPLETE | REJECTED | BLOCKED

## Scope Audited

## Handoff Claimed

## Evidence Required for the Handoff

## Evidence Not Required for the Handoff

## Changed Paths and Plan Boundary

## Code and CLI Checks

## Configuration Contract

## Data and Tensor Shape Checks

## Tests and Smoke Checks

## Materiality Assessment

### Blocking Findings

### Non-Blocking Corrections

### Observations

## Repair Disposition

LOCAL_REPAIR | DISCOVERY_ENVELOPE | CONTRACT_ESCALATION |
RESEARCH_ESCALATION | ENVIRONMENT_BLOCKED | NOT_APPLICABLE

## Research-Claim Boundary

## Required Follow-up
```

An Engineering Audit with status **ACCEPTED** means only that the declared
implementation or compatibility handoff passed the material recorded checks.

It is not a Formal Experiment acceptance and does not establish that a research
hypothesis is true.

`Repair Disposition` is required for a non-accepted audit. It may be
`NOT_APPLICABLE` for an accepted handoff.

An audit may be **ACCEPTED** with documented non-blocking corrections when all
evidence material to the declared handoff is satisfied.

A non-material formatting, documentation, receipt, path, warning, or logging
defect does not by itself determine the Engineering Audit status.

## Research Audit Report

The Research Auditor creates:

`reports/audits/{experiment_id}_audit.md`

Use this template:

```md
# {experiment_id}: Acceptance Audit

## Audit Status

ACCEPTED | INCOMPLETE | REJECTED | BLOCKED

## Scope Audited

## Evidence Inspected

## Material Protocol Compliance

## Scientific Validity

## Administrative and Documentation Findings

## Comparison Validity

## Control Verification

## Artifact and Provenance Verification

## Metric Traceability

## Claim Boundary Review

## Blocking Validity Findings

## Non-Blocking Corrections

## Findings

## Required Follow-up
```

The audit verifies, as applicable:

- consistency among experiment ID, approved plan, resolved config, command,
  source or Git state, and output directory;
- validity of the stated method, baseline, checkpoint, VAE, and comparison
  conditions;
- isolation of the primary variable, or explicit disclosure of additional
  changes;
- completion of required controls;
- compliance of dataset usage, sample inclusion, manifest, and split with the
  plan;
- absence of held-out test tuning or leakage;
- existence and integrity of required metadata, logs, checkpoints,
  predictions, and outputs;
- traceability of reported metrics to saved artifacts;
- compliance with declared stopping and acceptance criteria;
- reproducibility of the material research procedure; and
- whether the conclusion exceeds the available evidence.

The Research Auditor must distinguish:

- material scientific validity failures;
- missing evidence necessary to evaluate the research result;
- blocked access or authority;
- non-material administrative corrections; and
- unsupported or unproven claims.

## Audit Status Definitions

Engineering and Research Audits use the same status labels but apply them to
different handoffs.

### Engineering Audit Status

- **ACCEPTED:** The material evidence required for the declared implementation
  or compatibility handoff is satisfied. Non-blocking corrections may remain.
- **INCOMPLETE:** Evidence or a check necessary for the declared engineering
  handoff is missing, but the issue can be completed within the existing scope
  or repair budget.
- **REJECTED:** The implementation materially violates the approved contract,
  the claimed handoff is invalid, or the evidence integrity cannot be trusted.
- **BLOCKED:** Required authority, artifact, environment, data, device, or
  external dependency is unavailable, preventing the handoff.

### Research Audit Status

- **ACCEPTED:** The research design, comparison, required controls, provenance,
  metrics, and claim boundary are sufficient for the stated conclusion.
- **INCOMPLETE:** Evidence or a required control necessary to evaluate the
  research result is missing. The result cannot yet support the planned claim.
- **REJECTED:** A material validity or evidence-integrity failure invalidates
  the research result, including data leakage, silent substitution, invalid
  comparison, fabricated or overwritten evidence, an untraceable metric, or a
  material deviation that prevents evaluation of the approved research
  question.
- **BLOCKED:** Required artifacts, authority, resources, or information are
  unavailable, preventing completion of the independent audit.

A non-material formatting, documentation, receipt, path, warning, or logging
defect does not by itself determine an audit status.

Only a Research Audit with status **ACCEPTED** may be cited as completed
evidence in subsequent plans, summaries, presentations, reports, or paper
claims.

If an independent Research Auditor is unavailable, the formal research
acceptance status is **BLOCKED**.
