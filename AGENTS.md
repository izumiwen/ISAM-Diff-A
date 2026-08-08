# AGENTS.md

## Purpose

This repository is a deep-learning research project. Make scoped,
reproducible, and evidence-based progress. Optimize for valid evidence, clear
provenance, and reversible changes—not the appearance of progress.

This file contains durable repository-wide agent rules only. Keep model
designs, changing paths, experiment-specific decisions, and results in their
designated files.

Detailed experiment lifecycle, role workflow, run procedure, audit templates,
archive layout, and status-specific handling belong to their designated
governance documents and must not be duplicated here.

## Instruction Priority

Follow instructions in this order:

1. Explicit user request
2. This `AGENTS.md`
3. Applicable canonical governance documents:
   - `docs/experiment_protocol.md`
   - `docs/subagent_workflow.md`
   - `docs/run_standard.md`
4. The current approved plan
5. Existing repository conventions

A plan may specialize an applicable governance rule within its permitted scope,
but it must not silently weaken or contradict a repository-wide research
boundary.

When canonical governance documents overlap, apply the document responsible for
that subject rather than combining every requirement cumulatively:

- Formal and non-formal scope, material deviation, research evidence,
  acceptance, ledger triggers, and archive triggers:
  `docs/experiment_protocol.md`
- Role assignment, role combination, independence, delegation sequence, and
  audit status:
  `docs/subagent_workflow.md`
- Run identity, execution evidence, retry handling, dataset execution safety,
  and environment or toolchain operations:
  `docs/run_standard.md`

If instructions conflict within the same responsibility area, or task scope is
materially unclear, stop and ask before making a material decision.

Do not modify `AGENTS.md` unless the user explicitly asks.

## Required Protocols

Before Formal Experiment planning or execution, read:

`docs/experiment_protocol.md`

Before assigning delegated planning, engineering audit, execution, research
audit, or recording functions, read:

`docs/subagent_workflow.md`

Before Formal Experiment execution, a target-environment transition, or a final
engineering compatibility handoff, read the applicable sections of:

`docs/run_standard.md`

Read the latest relevant entries in `reports/experiment_log.md` before:

- formal planning;
- formal execution;
- decision-changing engineering work;
- evidence reuse;
- revising a research claim or plan; or
- work whose correctness depends on prior research outcomes.

Routine local repairs do not require rereading unrelated ledger history.

## Default Working Procedure

Before modifying files, inspect relevant code, configs, tests, records, and Git
status.

Make the smallest change that addresses the task, state material assumptions,
and preserve unrelated user changes.

Validation and evidence must be proportional to the task's scope and risk. A
routine local repair does not require Formal Experiment artifacts.

After modifying files, run the smallest relevant validation and report what
changed, what was verified, and what remains unverified.

Code inspection alone is not evidence of success.

## Autonomy Boundaries

The agent may, without asking:

- read project files;
- create task-scoped files;
- run formatting and linting;
- run unit tests;
- run CLI help and parser checks;
- run short smoke tests using synthetic data or a small read-only subset;
- produce low-risk diagnostics;
- update task-local metadata; and
- apply authorized local repairs within an approved scope.

The agent may draft or update a plan without asking only when:

- a plan is required by the applicable governance scope; and
- the requested work is already authorized.

The agent must not create a new plan merely to formalize an in-scope local
repair.

The agent must ask before:

- downloading large files;
- starting a single training, evaluation, or inference job expected to exceed
  15 minutes;
- using substantial GPU resources beyond a smoke test;
- changing the research question;
- changing the method or baseline identity;
- changing a dataset split;
- changing the primary metric or evaluation procedure;
- changing an acceptance threshold or stopping rule;
- changing system, CUDA, PyTorch, compiler, or native-extension environments;
- deleting, relocating, or overwriting research artifacts; or
- performing a remote or external action such as:
  - upload;
  - push;
  - pull-request creation;
  - issue creation;
  - publication; or
  - external submission.

The agent may create a local commit only when explicitly requested or when the
repository workflow already grants that authority.

Pushing a commit or performing any other remote repository action requires
explicit user authorization.

A lightweight declared Python dependency may be installed without separate
approval only when:

- it does not change Python, PyTorch, CUDA, compiler, native-extension, or
  runtime ownership;
- it does not expand the authorized environment boundary; and
- the applicable environment files are updated.

## Non-Negotiable Research Rules

- Do not modify source data in place.
- Do not tune on held-out test data.
- Do not overwrite historical runs, checkpoints, outputs, plans, results, or
  audit reports.
- Do not silently fall back when required data, checkpoints, modules, devices,
  environments, or configurations are unavailable.
- Do not rename a modified baseline as the original baseline.
- Do not present successful execution, metric improvement, or a qualitative
  example as proof of a research claim without the required evidence.
- Do not conceal:
  - a Formal Experiment outcome;
  - a material engineering blocker; or
  - evidence that changes a research decision or claim boundary.
- Do not mark a Formal Experiment as research-accepted without an independent
  Research Auditor.
- Do not treat engineering readiness as research acceptance.
- Do not silently replace a model, checkpoint, VAE, dataset, split,
  preprocessing procedure, metric, acceptance criterion, stopping rule, or
  required control.

Intermediate local-repair failures remain in their relevant diagnostics. They
do not require separate experiment-ledger entries or archive dossiers unless
they meet a material trigger in `docs/experiment_protocol.md`.

Use these labels precisely:

- **Observed**
- **Supported**
- **Unproven**
- **Blocked**

Do not turn an assumption into a conclusion.

## Project Experiment Log

Maintain the append-only, version-controlled research ledger at:

`reports/experiment_log.md`

Append a concise entry for:

- Formal Experiment authorization;
- a meaningful Formal Experiment start;
- a terminal Formal Experiment outcome;
- an independent Research Audit decision;
- an accepted engineering compatibility handoff;
- a material blocker that changes feasibility, schedule, plan, or claim
  boundary; or
- new evidence that changes a research decision.

Do not append separate entries for:

- intermediate Engineering Discovery attempts;
- local repairs within an approved scope;
- import, CLI, parser, fixture, or smoke-test failures;
- formatting or Markdown corrections;
- receipt finalization;
- checksum-index formatting; or
- repeated status updates that do not change the research state.

Never rewrite or delete history.

Correct an error with a new dated entry that references the original entry.

## Review Surface and Failure Archive

`reports/accepted/` is the research-success-only review surface.

It may contain only Formal Experiments whose independent Research Audit status
is **ACCEPTED**.

An accepted entry must link to its canonical immutable plan, result, research
audit, and output paths.

An Engineering Audit alone never qualifies an experiment for the accepted
surface.

Archive dossiers are created only for the material triggers defined by
`docs/experiment_protocol.md`, including, as applicable:

- an accepted engineering compatibility handoff;
- a material terminal engineering blocker;
- a target-environment or toolchain transition;
- a material engineering incident;
- a Formal Experiment execution outcome; or
- a non-accepted terminal Research Audit outcome.

Intermediate local-repair failures, repeated smoke-test attempts, and
non-material findings do not require separate archive dossiers.

The archive root is:

`reports/archive/`

The accepted review root is:

`reports/accepted/`

The operational archive path schema and dossier layout are defined in:

`reports/archive/README.md`

An archive dossier:

- records the exact status;
- links to canonical evidence paths;
- states why the outcome is material enough to preserve;
- records required follow-up; and
- must not delete, overwrite, move, reinterpret, or silently replace canonical
  artifacts.

`reports/experiment_log.md` remains the concise ledger for meaningful research
outcomes and decision-changing blockers.

Apply this organization prospectively. Do not relocate historical artifacts
without explicit user authorization.

## Phase Development and Formal Experiment Delegation

The project-level research plan is a roadmap. It does not by itself authorize
implementation, formal execution, or a research claim.

Role functions must be separated when an agent would otherwise approve or audit
its own substantive work.

Detailed role assignment, role combination, independence, sequence, and audit
status are defined in:

`docs/subagent_workflow.md`

The following repository-wide independence rules are mandatory:

- An Engineering Auditor must not audit implementation it performed.
- A Research Auditor must be independent of planning, development, and
  execution of the same Formal Experiment.
- An Executor must not act as the Research Auditor for the same Formal
  Experiment.
- An agent must not create evidence and then independently certify that same
  evidence as research-accepted.

Routine engineering and in-scope local repairs do not require the complete
multi-role lifecycle.

Recording is an administrative function. It does not require a separate
independent subagent, and it does not carry acceptance authority.

An accepted Engineering Audit establishes only the declared implementation or
compatibility handoff. It does not establish a research result.

Only an independent Research Audit with status **ACCEPTED** may support a
completed research claim.

If an independent Research Auditor required for formal research acceptance is
unavailable, research acceptance is **BLOCKED**.

## Engineering Discovery and Local Repair Authority

An Engineering Discovery Plan is used only when a material technical
uncertainty prevents a credible Formal Experiment contract or final
compatibility handoff.

Relevant uncertainties may include:

- toolchain;
- dependency cohort;
- build or ABI compatibility;
- import or CLI contract;
- data or tensor contract;
- device execution; or
- another material implementation interface.

Routine diagnostics and repairs already authorized by:

- the current task;
- an approved plan;
- an approved discovery envelope; or
- this `AGENTS.md`

do not require an Engineering Discovery Plan.

An Engineering Discovery Plan must declare:

- frozen research boundary;
- immutable source or baseline identity;
- permitted technical candidates;
- forbidden fallbacks;
- allowed local repairs;
- finite repair budget;
- required compatibility handoff;
- stopping criteria; and
- escalation criteria.

Within an approved plan's interface and discovery envelope, the developer may
directly repair local implementation defects, including:

- build commands;
- working directories;
- include paths;
- CLI arguments;
- parser and fixture defects;
- Markdown and path-representation defects;
- receipt and log-capture implementation;
- configuration wiring; and
- incorrect transformations of an already declared data or tensor shape.

An in-scope local repair does not require, for each attempt:

- a new experiment ID;
- a new plan;
- a new planner pass;
- a separate audit;
- a separate experiment-log entry; or
- a separate archive dossier.

Within an approved discovery envelope, intermediate failures are engineering
observations rather than separate terminal phases.

For bounded local repair evidence, retain:

- the first reproducing failure;
- the final verification evidence; and
- additional intermediate diagnostics only when they explain a material
  decision, regression, incident, or escalation.

Run the smallest relevant reproducing or regression check after a local repair.

Escalate when the repair changes or reveals ambiguity in:

- module interface;
- data or tensor contract;
- method or model identity;
- architecture;
- baseline;
- dataset or split;
- checkpoint or VAE;
- research-relevant preprocessing;
- primary metric or evaluation procedure;
- acceptance threshold;
- stopping rule;
- required control;
- research hypothesis; or
- claim boundary.

Missing authority, unavailable required artifacts, or a required
CUDA/PyTorch/system-environment change remain **BLOCKED** until the relevant
authority is obtained.

An Engineering Discovery Plan does not grant:

- silent fallback;
- target-environment mutation;
- research acceptance; or
- authority to change a Formal Experiment contract outside its declared scope.

Detailed repair sequence and audit triggers are defined in
`docs/subagent_workflow.md`.

Environment and toolchain procedures are defined in `docs/run_standard.md`.

## Safety and Reporting

Check Git status before and after material work.

Preserve unrelated changes in a dirty working tree.

Do not use destructive Git operations unless explicitly requested.

Keep datasets, checkpoints, outputs, caches, and environments out of Git unless
the user explicitly requests otherwise.

Reports should primarily be written in Traditional Chinese (zh-tw).

When an error occurs, use the retry and repair budget defined by the applicable
plan, discovery envelope, or formal retry policy.

When no explicit budget exists:

- use the smallest reasonable number of low-risk attempts;
- preserve the formal or declared engineering contract; and
- stop before the work expands into:
  - a material contract change;
  - target-environment mutation;
  - a new resource requirement;
  - a research-condition change; or
  - an unauthorized fallback.

There is no universal fixed limit of two diagnostic attempts.

Preserve:

- the first reproducing failure;
- the final verification evidence; and
- material intermediate diagnostics.

Do not require a canonical receipt, audit, ledger entry, or dossier for every
intermediate attempt.

A warning, informational message, or non-empty stderr stream is not
automatically a failure. Treat it as blocking only when it indicates invalid
computation, silent fallback, data loss, numerical corruption, contract
violation, or inability to verify the result.

At the end of material work or a delegated handoff, report:

1. Objective
2. Changes made
3. Validation evidence
4. Risks, limitations, or blocked items
5. Next action

For a routine local repair, a shorter report is sufficient when it still states
what changed, what was verified, and what remains unresolved.

Use exact paths, commands, metrics, and experiment IDs when available.

Avoid vague claims such as "should work" or "probably fixed."

## Agent skills

### Issue tracker

Issues 與 PRD 使用 GitHub Issues 管理。詳見 `docs/agents/issue-tracker.md`。

### Triage labels

使用預設五種 triage 標籤。詳見 `docs/agents/triage-labels.md`。

### Domain docs

使用 single-context 文件配置。詳見 `docs/agents/domain.md`。
