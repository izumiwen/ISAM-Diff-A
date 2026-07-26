# AGENTS.md

## Purpose

This repository is a deep-learning research project. Make scoped,
reproducible, and evidence-based progress. Optimize for valid evidence, clear
provenance, and reversible changes—not the appearance of progress.

This file contains durable agent rules only. Keep model designs, changing
paths, experiment-specific decisions, and results in their designated files.


## Instruction Priority

Follow instructions in this order:

1. Explicit user request
2. This `AGENTS.md`
3. The current approved experiment plan
4. Existing repository conventions

If instructions conflict or task scope is unclear, stop and ask before making
a material decision. Do not modify `AGENTS.md` unless the user explicitly asks.

## Required Protocols

Before drafting or executing a formal experiment, read:

`docs/experiment_protocol.md`

Before delegating experiment planning or acceptance, read:

`docs/subagent_workflow.md`

Before running training, evaluation, inference, or dataset validation, read:

`docs/run_standard.md`

Read the latest relevant entries in `reports/experiment_log.md` before starting
research, implementation, or a formal experiment.

## Default Working Procedure

Before modifying files, inspect relevant code, configs, tests, records, and
Git status. Make the smallest change that addresses the task, state material
assumptions, and preserve unrelated user changes.

After modifying files, run the smallest relevant validation and report what
changed, what was verified, and what remains unverified. Code inspection alone
is not evidence of success.

## Autonomy Boundaries

The agent may, without asking, read project files, create task-scoped files,
run formatting, linting, unit tests, CLI help checks, and short smoke tests
using synthetic data or a small subset. It may also write plans, reports,
metadata, and low-risk diagnostics.

The agent must ask before downloading large files; starting a training or
evaluation job expected to exceed 15 minutes; using substantial GPU resources
beyond a smoke test; changing the research question, baseline, dataset split,
primary metric, or acceptance threshold; changing system, CUDA, or PyTorch
environments; deleting or overwriting research artifacts; or performing any
external action such as upload or pull-request creation. After completing an
experiment phase, the agent may commit and push the phase's changes to the
repository.

A lightweight declared Python dependency may be installed only when it does
not change CUDA/PyTorch versions and the environment files are updated.

## Non-Negotiable Research Rules

- Do not modify source data in place.
- Do not tune on held-out test data.
- Do not overwrite historical runs, checkpoints, outputs, plans, results, or
  audit reports.
- Do not silently fall back when required data, checkpoints, modules, devices,
  or configurations are unavailable.
- Do not rename a modified baseline as the original baseline.
- Do not present a successful execution, metric improvement, or qualitative
  example as proof of a research claim without the required evidence.
- Do not hide failed, interrupted, rejected, or inconclusive experiments.
- Do not mark a formal experiment as accepted without an independent auditor.

Use these labels precisely: **Observed**, **Supported**, **Unproven**, and
**Blocked**. Do not turn an assumption into a conclusion.

## Project Experiment Log

Maintain the append-only, version-controlled research ledger at:

`reports/experiment_log.md`

Append a concise entry when a formal experiment is planned, starts, ends, is
audited, is blocked, or when new evidence changes a research decision. Do not
add entries for trivial edits or repeated status updates.

Never rewrite or delete history. Correct an error with a new dated entry that
references the original entry.

## Review Surface and Failure Archive

`reports/accepted/` is the success-only review surface. It may contain only
experiments whose independent research audit status is **ACCEPTED**. Each
accepted entry must link to its immutable plan, result, research audit, and
output directory; an engineering audit alone never qualifies for this surface.

All other terminal outcomes remain visible in the append-only experiment log
but are preserved through a deeper archive dossier at one of:

- `reports/archive/implementation/{status}/{experiment_id}/`
- `reports/archive/failed/{experiment_id}/`
- `reports/archive/blocked/{experiment_id}/`
- `reports/archive/rejected/{experiment_id}/`
- `reports/archive/incomplete/{experiment_id}/`

An archive dossier records the exact status, evidence paths, and required
follow-up. It links to immutable plans, results, audits, and output artifacts;
it must not delete, overwrite, move, or silently replace those artifacts.
`reports/experiment_log.md` remains the complete concise ledger for accepted
and non-accepted work, while `reports/accepted/` is the streamlined inspection
entry point. Apply this organization prospectively; do not relocate historical
artifacts without explicit user authorization.

## Phase Development and Formal Experiment Delegation

The project-level research plan is a roadmap. It does not by itself authorize
implementation, a formal run, or a research claim. Each phase must use the
following independent roles in order:

- A planner subagent writes the bounded phase or experiment plan; it does not
  implement the plan.
- A developer subagent implements only an approved phase plan and supplies
  scoped tests and implementation evidence.
- An engineering auditor subagent, independent of the planner and developer,
  verifies code execution, declared data and tensor shapes, configuration and
  CLI contracts, and applicable short smoke tests. It does not repair code.
- An executor runs an authorized formal experiment and records the result.
- A research auditor subagent, independent of the planner, developer, and
  executor, determines whether the formal experiment's evidence is accepted.
- A recorder subagent that did not plan, develop, execute, or audit the same
  phase appends concise, evidence-linked outcomes to
  `reports/experiment_log.md` and creates the required accepted entry or
  archive dossier. It records rather than reinterprets the approved plan,
  result, and audit.

An accepted engineering audit establishes implementation readiness only; it
does not establish a research result. Only an independent research audit with
status **ACCEPTED** may support a research claim. If the required independent
role is unavailable, the corresponding stage is **BLOCKED**; self-certification
is not a substitute.

## Engineering Discovery and Local Repair Authority

When toolchain, dependency, build, import, CLI, data-contract, or tensor-shape
uncertainty prevents a credible formal plan, the planner may create an
**Engineering Discovery Plan**. It is non-formal engineering work, not a
research experiment. It must declare the frozen research boundary, permitted
technical candidates, allowed local repairs, a finite repair budget, required
smoke checks, stopping criteria, and the compatibility handoff required before
a formal experiment plan may be written.

Within an approved plan's declared interface and discovery envelope, the
developer may directly repair local implementation defects such as build
commands, working directories, include paths, CLI arguments, receipt writers,
and incorrect transformations of an already declared data or tensor shape. The
developer must add or update a reproducing test, retain raw diagnostic output,
and record the repair evidence for engineering audit. A local repair does not
require a new planner pass.

The developer must escalate to the planner when the repair changes or reveals
an ambiguous module interface, data or tensor contract, model architecture,
baseline, dataset split, primary metric, acceptance threshold, research
hypothesis, or method identity. Missing authority, unavailable required
artifacts, or a required CUDA/PyTorch/system-environment change remain
**BLOCKED** until the relevant authority is obtained; an Engineering Discovery
Plan does not grant a silent fallback or an environment change.

## Safety and Reporting

Check Git status before and after material work. Preserve unrelated changes in
a dirty working tree. Do not use destructive Git operations unless explicitly
requested. Keep datasets, checkpoints, outputs, caches, and environments out
of Git unless the user explicitly requests otherwise.

Reports should primarily be written in Traditional Chinese (zh-tw).

When an error occurs outside an approved Engineering Discovery Plan, preserve
evidence, inspect the immediate cause, and make at most two low-risk diagnostic
attempts. Stop and report if unresolved. An Engineering Discovery Plan may use
its explicitly declared finite repair budget instead; it must bound elapsed
time, candidate combinations, and smoke checks, preserve every failed attempt,
and stop at its declared escalation criteria.

At the end of each task, report:

1. Objective
2. Changes made
3. Validation evidence
4. Risks, limitations, or blocked items
5. Next action

Use exact paths, commands, metrics, and experiment IDs when available. Avoid
vague claims such as "should work" or "probably fixed."
