# Experiment Protocol

## Scope

This protocol governs every **Formal Experiment**: an explicitly authorized run
intended to produce research evidence, compare methods, evaluate a research
hypothesis, support a research decision, or appear in a report or paper.

A run is formal only when it is authorized by an approved Formal Experiment
Plan. The fact that an activity may inform later planning does not by itself
make that activity a Formal Experiment.

This protocol does not govern routine formatting, import checks, unit tests,
CLI checks, implementation preflights, environment diagnostics, engineering
exploration, isolated smoke tests, or pilots that are clearly labelled as
non-formal.

For this protocol, “support a decision” means support for a research decision
concerning a method, model, architecture, dataset, split, checkpoint, VAE,
research-relevant preprocessing procedure, metric, acceptance criterion, or
research claim. It does not include a local engineering decision whose outcome
is not used as research evidence.

A pilot or non-formal feasibility check may inform whether a Formal Experiment
should be planned. Its outputs must not be cited as confirmatory research
evidence. Any result intended to support a formal comparison or claim must be
executed again under an approved Formal Experiment Plan unless the original run
was explicitly authorized as formal before execution.

Operational documents may define how work is performed, delegated, logged, or
archived, but they must not silently enlarge the scope of this protocol or
convert non-formal engineering work into a Formal Experiment.

Read `AGENTS.md` and the latest relevant entries in
`reports/experiment_log.md` before applying this protocol.

## Planning Hierarchy and Development Gate

A project-level research plan defines the research direction, module roles,
phase order, and decision boundaries. It is a roadmap, not an authorization to
implement a module or execute a Formal Experiment.

Each Formal Experiment must be traced to a bounded research phase and an
approved Formal Experiment Plan.

One approved phase plan may authorize multiple bounded implementation repairs,
diagnostic attempts, regression checks, and smoke checks within its declared
interface, research boundary, and repair budget.

A new or revised plan is required when a proposed change:

- changes or makes ambiguous the research question or method identity;
- changes a model, architecture, dataset, split, checkpoint, VAE,
  research-relevant preprocessing procedure, metric, acceptance criterion,
  stopping rule, baseline identity, or primary comparison condition;
- changes a declared data or tensor contract rather than correcting an
  implementation to conform to that contract;
- exceeds the approved discovery envelope or repair budget;
- requires new environment, resource, artifact, or external authority; or
- would otherwise change the interpretation of the evidence produced.

Formatting, command invocation, working directory, include path, receipt
formatting, Markdown links, log-capture implementation, checksum-index
formatting, and test-fixture defects do not require a new plan when their repair
does not alter the declared interface, executed method, research evidence, or
research boundary.

## Engineering Discovery Plans

An Engineering Discovery Plan is an optional, non-formal phase used to resolve
a material technical uncertainty before freezing a Formal Experiment contract.

It is appropriate when a credible Formal Experiment Plan cannot yet freeze one
of the following:

- a bounded toolchain or dependency cohort;
- native build or ABI compatibility;
- an import or command contract;
- a data or tensor-shape contract;
- an implementation interface;
- a device-execution requirement; or
- another technical condition required for formal execution.

Routine diagnostics and low-risk local repairs already authorized by
`AGENTS.md`, an existing approved plan, or an existing discovery envelope do
not require a separate Engineering Discovery Plan.

Engineering Discovery must not produce a formal research metric, formal method
comparison, or research claim. Its purpose is to establish a technical
compatibility handoff or a material technical blocker.

The planner writes one bounded discovery plan rather than a new plan for each
local compile, import, CLI, path, receipt, logging, test-fixture, or shape
failure. The plan must declare:

- frozen research boundary and immutable source or baseline identity;
- objective and unresolved technical uncertainty;
- permitted technical candidates and forbidden fallbacks;
- local-repair authority for the developer;
- finite elapsed-time, candidate-combination, and smoke-check repair budget;
- required raw diagnostics, regression tests, and compatibility handoff;
- conditions that constitute a material blocker; and
- stopping and escalation criteria.

Within an approved discovery envelope, a failed diagnostic or smoke check is
an intermediate engineering observation. It is not automatically a terminal
phase outcome.

The developer may continue through bounded repairs until:

- the declared compatibility handoff is established;
- the repair budget is exhausted;
- a stopping criterion is reached;
- the required authority or artifact is unavailable; or
- a material contract or research-boundary escalation is discovered.

Raw failed-attempt diagnostics must be retained. An intermediate discovery
attempt does not require its own canonical result report, experiment-log entry,
independent audit, or archive dossier.

An independent engineering audit is required when:

- the discovery phase claims a final compatibility handoff;
- a material blocker terminates the discovery phase;
- the work proposes a transition of the target environment;
- an incident requires evidence to be preserved independently of the working
  phase; or
- the applicable plan explicitly requires an intermediate audit because of
  material risk.

An Engineering Discovery Plan does not authorize a CUDA, PyTorch, Python,
compiler, system, dataset, checkpoint, VAE, metric, or research-decision change
that otherwise requires approval.

An accepted discovery handoff establishes only the declared technical
compatibility. It does not constitute Formal Experiment readiness unless the
formal implementation contract has also been checked, and it never constitutes
research acceptance.

A subsequent Formal Experiment Plan must cite any discovery handoff on which it
depends and freeze one compatible technical contract.

### Version and Toolchain Transition Gate

A proposed change to the target Python, PyTorch, CUDA, compiler,
native-extension, package-manager ownership, or runtime dependency cohort
requires:

- explicit authorization for the exact transition scope;
- preserved evidence describing the pre-change environment;
- a documented source and interface compatibility assessment;
- a pre-change transaction dry run identifying removals, replacements,
  downloads, and ownership conflicts;
- a bounded post-change build, import, device, and synthetic-contract
  verification; and
- a defined rollback or blocked outcome when the transition cannot be
  validated.

Package installation or dependency-resolution success is not compatibility
evidence.

Do not mutate the target environment when:

- target-version support is undeclared or materially uncertain;
- the affected source, API, ABI, compiler, or device contract has not been
  reviewed;
- the proposed transaction expands beyond the authorized package set;
- an equivalent implementation would change a declared interface or behavior;
  or
- required evidence cannot be preserved.

The resulting status is **BLOCKED** or `CONTRACT_ESCALATION` until the exact
transition scope is approved.

A temporary or disposable compatibility diagnostic may be used only when it is
separately authorized, does not modify the target environment, and does not
alter immutable vendor source.

Evidence from a disposable diagnostic environment is not by itself a
compatibility handoff for the target environment.

The operational procedure for version, toolchain, native-extension, package,
environment, device, and runtime verification is defined in
`docs/run_standard.md`.

### Development Readiness Gate

Before a Formal Experiment executes, its implementation must satisfy the
engineering-readiness checks applicable to the approved Formal Experiment
Plan.

The readiness check must verify, as applicable:

- code and CLI execution;
- the resolved configuration contract;
- declared model and module identity;
- declared data and tensor shapes;
- checkpoint and VAE identity;
- device requirements and prohibited fallbacks;
- output and metadata paths; and
- the smallest relevant unit, regression, or synthetic smoke checks.

Role assignment, independence requirements, audit report responsibilities,
repair dispositions, and delegation order are defined in
`docs/subagent_workflow.md`.

The canonical implementation-audit path remains:

`reports/audits/{experiment_id}_implementation_audit.md`

An accepted engineering audit means only that the implementation is ready for
the declared formal run, or that a declared discovery compatibility handoff is
complete.

Engineering readiness does not establish that:

- the research hypothesis is true;
- the method improves over a baseline;
- a metric is accepted;
- a causal claim is supported; or
- the experiment may be cited as completed research evidence.

Intermediate local repairs within an approved interface and repair budget do
not restart the complete role sequence. They return to engineering verification
at the level required by their materiality and risk.

## Experiment Lifecycle

A Formal Experiment follows this lifecycle:

1. Assign a unique experiment ID.
2. Create and approve
   `reports/plans/{experiment_id}_plan.md`.
3. Complete any required Engineering Discovery and applicable development
   readiness checks.
4. Confirm execution authority, required artifacts, environment, device, and
   resource availability.
5. Record the planned Formal Experiment in
   `reports/experiment_log.md`.
6. The executor runs the approved plan without unrecorded material changes.
7. If formal model, data, metric, or research-evidence execution began, create
   `reports/results/{experiment_id}_result.md` regardless of whether the run
   succeeded, failed, was interrupted, became inconclusive, or was blocked
   during execution.
8. Record the terminal execution outcome and result path in
   `reports/experiment_log.md` without claiming research acceptance.
9. Obtain an independent research audit before the result is:
   - promoted to completed research evidence;
   - used to authorize a later research decision;
   - used as an accepted baseline;
   - summarized as a supported result; or
   - cited in a report, presentation, or paper claim.
10. Record the research-audit outcome in
    `reports/experiment_log.md`.
11. Only a research audit with status **ACCEPTED** may receive an entry under
    `reports/accepted/{experiment_id}/`.

A pre-execution engineering blocker does not require a Formal Experiment result
report when no formal model, data, metric, or research-evidence execution
occurred.

A material pre-execution blocker may be recorded once in the experiment log,
linked issue, or applicable engineering audit when it changes the research
schedule, feasibility judgment, approved plan, or claim boundary.

Repeated local repair failures, parser failures, formatting defects, receipt
finalization, test-fixture corrections, and other intermediate engineering
events must not be represented as separate Formal Experiment outcomes unless
they independently meet the formal scope defined above.

Only an independently research-audited experiment with status **ACCEPTED** may
be used as completed evidence in later plans, accepted comparisons, summaries,
or paper claims.

## Plan Requirements

The planner subagent creates:

`reports/plans/{experiment_id}_plan.md`

A plan must identify:

- its plan type;
- its authorizing project-level phase;
- its scope and authority;
- the implementation contract to be checked;
- its stopping and escalation boundaries; and
- the evidence required before the plan may be considered complete.

A routine local repair authorized by an existing plan, `AGENTS.md`, or an
existing discovery envelope does not require a separate plan.

### Formal Experiment Plan Template

Use the following template for a Formal Experiment:

```md
# {experiment_id}: {short title}

## Plan Type

Formal Experiment

## Status

Draft | Approved | Superseded | Cancelled

## Authorizing Research Phase

## Objective

## Hypothesis

## Baseline and Comparison

## Dataset and Split

## Fixed Conditions

## Model, Checkpoint, and VAE Contract

## Preprocessing and Data Isolation Contract

## Primary Variable

## Required Controls

## Configuration and Resource Budget

## Metrics and Evaluation Procedure

## Acceptance Criteria

## Failure and Stopping Criteria

## Expected Artifacts

## Risks and Validity Threats

## Required Engineering Handoffs
```

The Formal Experiment Plan must make every comparison fair by declaring, as
applicable:

- dataset and split;
- source-data and manifest identity;
- preprocessing and resolution;
- seed policy;
- evaluation procedure;
- compute and resource budget;
- model, architecture, checkpoint, and VAE identity;
- checkpoint-selection policy;
- metric implementation and monitor direction;
- baseline identity;
- required controls;
- permitted fallback policy; and
- any method-specific exception.

The plan must define acceptance criteria before execution. It must also define
which conditions require stopping, which conditions permit a bounded retry, and
which conditions require a revised plan.

A Formal Experiment Plan that depends on an Engineering Discovery handoff must
identify that handoff and freeze one compatible technical contract.

### Engineering Discovery Plan Template

Use the following template when a distinct Engineering Discovery Plan is
required:

```md
# {experiment_id}: {short title}

## Plan Type

Engineering Discovery

## Status

Draft | Approved | Superseded | Cancelled

## Authorizing Research Phase

## Objective and Technical Uncertainty

## Frozen Research Boundary

## Immutable Source and Baseline Identity

## Permitted Technical Candidates

## Forbidden Fallbacks

## Local-Repair Authority

## Repair Budget

## Required Checks and Diagnostics

## Compatibility Handoff

## Material Blockers

## Stopping and Escalation Criteria

## Expected Artifacts
```

Engineering Discovery plans do not require a research hypothesis, research
baseline comparison, formal dataset evaluation, research metric, or research
acceptance threshold unless one of those items is itself the technical contract
being verified without producing a research result.

When a plan changes a version or toolchain cohort, it must identify:

- the exact authorized transaction boundary;
- the pre-change compatibility evidence;
- the affected source, build, API, ABI, and device contracts;
- the applicable procedure in `docs/run_standard.md`;
- the required regression or synthetic-contract checks; and
- the conditions that require an equivalent implementation, rollback, blocked
  status, or contract escalation.

## Experimental Design Rules

These rules apply to Formal Experiments, formal comparisons, and research
claims. They do not convert non-formal engineering diagnostics or synthetic
implementation checks into research evidence.

Each ablation changes one primary variable while holding the declared fixed
conditions constant.

If multiple primary changes are required, label the experiment as a combined
configuration rather than an ablation.

Do not use held-out test data for:

- model selection;
- checkpoint selection;
- threshold selection;
- hyperparameter tuning;
- stopping-rule adjustment; or
- failure-driven iteration.

Do not modify a baseline without assigning a new configuration identity and
disclosing the difference.

Do not silently replace a model, checkpoint, VAE, dataset, split,
preprocessing procedure, metric implementation, acceptance criterion, or
stopping rule.

Fallback behavior must be explicitly authorized and recorded. An unavailable
required model, artifact, dataset, device, checkpoint, VAE, module, or
configuration does not authorize a silent substitute.

Required controls must be completed before the corresponding causal claim is
accepted.

A missing required control makes the relevant claim **Unproven** or the
evidence **INCOMPLETE**. It must not be interpreted as implicitly negative or
positive evidence.

Engineering execution success must not be presented as research success.

## Result Requirements

After a Formal Experiment in which formal model, data, metric, or
research-evidence execution began, create:

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

The result must record what actually executed rather than only what the plan
intended.

Record all deviations honestly and distinguish material research deviations
from non-material administrative or engineering defects.

A **material deviation** changes, substitutes, obscures, or makes unverifiable
one or more of the following:

- research question or hypothesis;
- method or model identity;
- architecture;
- dataset, split, sample inclusion, or data isolation;
- checkpoint or checkpoint-selection procedure;
- VAE;
- research-relevant preprocessing;
- baseline or primary comparison condition;
- metric implementation or evaluation procedure;
- acceptance criterion;
- stopping rule;
- required control;
- authorized resource or device boundary; or
- evidence needed to determine what research procedure actually executed.

A run with a material undeclared deviation must not be treated as an execution
of the original plan.

Depending on whether the executed work remains scientifically interpretable,
the result must instead be:

- stopped and replanned;
- reported under a revised configuration identity;
- marked **INCOMPLETE**;
- marked **REJECTED** by research audit; or
- preserved only as non-formal engineering evidence.

A formatting, Markdown, path-representation, log-capture, receipt-finalization,
checksum-index, warning-handling, parser, or test-fixture defect is not by
itself a material research deviation.

Such a defect becomes material only when it prevents verification of the
executed method, model, data, checkpoint, VAE, metric, comparison, result, or
claim.

Non-material defects must still be disclosed and corrected prospectively or by
an append-only correction. They do not by themselves redefine the scientific
execution or require a new Formal Experiment.

Formal evidence must preserve sufficient provenance to reproduce or verify the
result, including the applicable:

- approved plan;
- resolved configuration;
- command;
- code or source identity;
- environment and device identity;
- model, checkpoint, and VAE identity;
- dataset, split, and manifest identity;
- seed policy;
- raw logs;
- metric outputs;
- result report; and
- research audit.

## Acceptance Rules

Acceptance criteria must be defined before execution and must be measurable.

They may include:

- required artifacts;
- required controls;
- engineering behavior relevant to the formal contract;
- metric thresholds;
- equivalence bounds;
- reproducibility requirements; or
- pre-registered decision rules.

Acceptance must not depend solely on a desirable metric.

It requires:

- valid and sufficient provenance;
- a fair comparison;
- compliance with the material research contract;
- completion of required controls;
- an evidence-backed interpretation; and
- claims that remain within the demonstrated evidence boundary.

Research-audit findings must be evaluated according to their effect on:

- research validity;
- reproducibility;
- evidence integrity;
- fairness of comparison;
- data isolation;
- method identity; and
- claim support.

Auditors must report non-substantive documentation, formatting, path, receipt,
or logging defects, but such defects do not by themselves require rejection or
invalidate an otherwise verifiable result.

A non-material defect may require:

- an append-only correction;
- a prospective implementation repair;
- a documentation follow-up;
- a provenance clarification; or
- a non-blocking audit finding.

**REJECTED** is reserved for a material validity or evidence-integrity failure,
including, for example:

- held-out test leakage or tuning;
- silent model, checkpoint, VAE, dataset, split, baseline, metric, or method
  substitution;
- an invalid or unfair comparison;
- fabricated, overwritten, concealed, or materially inconsistent evidence;
- an untraceable formal metric;
- a material deviation that prevents evaluation of the approved research
  question; or
- a claim that materially exceeds the available evidence.

**INCOMPLETE** applies when evidence necessary to evaluate the formal research
result is missing, when a required control is absent, or when the result cannot
yet support the planned conclusion.

Missing evidence unrelated to the scientific conclusion should be recorded as
a non-blocking correction or follow-up rather than automatically making the
entire research result incomplete.

A successful engineering audit establishes implementation readiness only. It
does not satisfy the research acceptance rules in this section.

## Experiment Log Entry Format

`reports/experiment_log.md` is an append-only concise research ledger. It is
not a complete engineering transaction log.

Append entries for:

- authorization of a Formal Experiment;
- start of a Formal Experiment when the start is a meaningful project
  milestone;
- terminal outcome of a Formal Experiment;
- an independent research-audit decision;
- an accepted engineering compatibility handoff;
- a material engineering blocker that changes feasibility, schedule, plan, or
  claim boundary; or
- new evidence that changes a research decision.

Do not append separate entries for:

- intermediate Engineering Discovery attempts;
- local repairs within an approved envelope;
- unit, import, CLI, parser, fixture, or smoke-test failures;
- formatting or Markdown corrections;
- receipt finalization;
- checksum-index formatting;
- repeated status updates; or
- administrative changes that do not change the research state.

Those details remain in the applicable raw diagnostics, audit report, task log,
issue, or implementation evidence.

Append entries using:

```md
## YYYY-MM-DD — [Experiment ID or Task ID] — [Status]

- **Objective:**
- **Change or decision:**
- **Evidence:**
- **Interpretation:**
- **Artifacts:**
- **Next action:**
```

Use dated corrections instead of editing or deleting historical entries.

For an accepted engineering compatibility handoff, identify:

- the bounded phase;
- the compatibility claim;
- the implementation-audit status;
- the material checks performed; and
- the linked plan and audit paths.

For a material engineering blocker, record one concise terminal or
decision-changing entry rather than one entry for every failed attempt.

The recorder must preserve the distinction between:

- engineering readiness;
- formal execution;
- research acceptance;
- Supported evidence;
- Unproven claims; and
- Blocked work.

The recorder must not convert engineering readiness into a research
conclusion, reinterpret an auditor’s finding, or create a stronger claim than
the canonical plan, result, and audit support.

## Accepted Review and Archive Dossiers

`reports/accepted/` is a success-only review surface, not a second research
ledger.

Its index and per-experiment entries may list only independently
research-audited **ACCEPTED** experiments, with links to the canonical plan,
result, audit, and output paths.

The accepted entry path remains:

`reports/accepted/{experiment_id}/`

An accepted entry must not move, duplicate as a replacement, overwrite, or
silently alter the canonical evidence.

An engineering archive dossier is required when:

- an Engineering Discovery phase establishes an accepted compatibility
  handoff;
- a material terminal engineering blocker changes project feasibility,
  authority, or the formal research path;
- an environment or toolchain transition produces evidence that must be
  preserved independently; or
- an engineering incident requires a durable review surface.

The engineering dossier path remains:

`reports/archive/implementation/{status}/{experiment_id}/`

Intermediate local-repair failures, routine non-material audit findings,
formatting corrections, receipt finalization, and repeated smoke-test attempts
do not require separate archive dossiers.

A formal-outcome archive dossier is required when:

- formal execution began;
- formal research evidence was produced;
- a terminal outcome materially changes a research decision or claim boundary;
  or
- an independent research audit assigns a non-accepted terminal status.

Formal archive categories remain:

- `Failure` or `Interrupted`:
  `reports/archive/failed/{experiment_id}/`
- formal `Blocked` or research-audit `BLOCKED`:
  `reports/archive/blocked/{experiment_id}/`
- research-audit `REJECTED`:
  `reports/archive/rejected/{experiment_id}/`
- research-audit `INCOMPLETE`:
  `reports/archive/incomplete/{experiment_id}/`

A dossier must state:

- the exact status;
- the reason the outcome is material enough to preserve as a dossier;
- canonical plan, result, audit, log, and output paths;
- the supported, unsupported, unproven, and blocked boundaries; and
- the required follow-up.

A dossier is an index to canonical immutable artifacts. It is not a reason to
move, delete, overwrite, conceal, reinterpret, or silently replace them.

The operational archive layout and dossier-construction procedure are defined
in `reports/archive/README.md` and `docs/subagent_workflow.md`.

The append-only `reports/experiment_log.md` remains the concise index of
meaningful research outcomes and decision-changing blockers. It is not required
to enumerate every local engineering attempt.

This layout applies prospectively. Historical artifacts and historical ledger
entries must not be relocated, deleted, consolidated, or rewritten without
explicit authorization.
