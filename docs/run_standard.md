# Run Standard

## Scope

This standard defines operational requirements for Formal Experiments and the
engineering checks that prepare them.

It applies in full to:

- formal training;
- formal evaluation;
- formal inference;
- formal dataset validation; and
- other runs explicitly authorized as Formal Experiments by an approved plan.

Routine diagnostics, unit tests, isolated smoke tests, implementation
preflights, Engineering Discovery attempts, and non-formal pilots apply only
the sections and evidence requirements necessary for their declared scope.

This standard must not convert non-formal work into a Formal Experiment.
Formal and non-formal scope is defined by `docs/experiment_protocol.md`.

Read `AGENTS.md`, `docs/experiment_protocol.md`, and the applicable plan before
execution. When delegated roles or independent audits are required, follow
`docs/subagent_workflow.md`.

## Run Identity and Output Structure

Every Formal Experiment run must use:

- an approved experiment ID;
- a distinct run ID;
- a resolved configuration; and
- a new output directory.

Never overwrite an existing formal run directory or any canonical evidence
already referenced by a plan, result, audit, ledger entry, report, or paper
claim.

A material research-configuration change requires a new configuration identity
and, when required by `docs/experiment_protocol.md`, a revised or new
experiment plan.

An exact rerun under the same approved Formal Experiment Plan retains the
experiment ID but uses:

- a new run ID;
- a new output directory; and
- a recorded reason for the rerun.

A bounded engineering retry or diagnostic attempt retains its task or discovery
ID. Use an attempt identifier when separate evidence is needed. It does not
require a new experiment ID.

Recommended formal output structure:

```text
outputs/{experiment_id}_{run_id}/
├── resolved_config.yaml
├── run_metadata.json
├── environment.txt
├── logs.txt
├── train_log.csv
├── metrics_summary.json
├── checkpoints/
│   ├── best.pt
│   └── last.pt
├── predictions/
└── qualitative/
```

A timestamp may be used as all or part of the run ID.

Not every formal run requires every artifact in the recommended structure.
Omissions must be intentional and recorded in the applicable plan, result
report, or run metadata.

A non-formal diagnostic, pilot, or discovery attempt does not require the full
formal output structure. Preserve only the artifacts necessary to verify its
declared engineering purpose.

## Required Metadata

### Formal Runs

For a Formal Experiment, `run_metadata.json` must record, when applicable:

- executed command;
- experiment ID and run ID;
- plan and resolved configuration paths;
- Git commit hash and working-tree status;
- configuration path and SHA-256 hash;
- Python, PyTorch, CUDA, compiler, GPU, and device information;
- random seed and determinism settings;
- dataset manifest, version, split, and sample counts;
- model, checkpoint, and VAE identity;
- checkpoint source and resume state;
- preprocessing and evaluation identity;
- output directory;
- start time, end time, and terminal status; and
- permitted retry or restart identity.

Save the parsed and resolved configuration as `resolved_config.yaml`. Do not
rely only on an editable source YAML file.

Preserve sufficient environment information to reconstruct the material
runtime cohort. The exact format may be a package export, version report,
container identity, environment lock, or equivalent evidence appropriate to
the project.

### Non-Formal Diagnostics, Pilots, and Discovery Attempts

A non-formal run records only the information needed to verify its declared
scope, such as:

- task, discovery, or attempt identity, when one exists;
- command or check invoked;
- relevant code and environment identity;
- input type, sample identity, or synthetic fixture;
- observed outcome;
- material warning or limitation; and
- artifact paths required for the engineering handoff.

A unit test or local diagnostic does not require a complete formal
`run_metadata.json` unless the applicable plan or final engineering handoff
explicitly requires one.

### Evidence Finalization

Metadata, checksums, evidence indexes, and summarized logs may be finalized
after the child process exits.

A receipt-finalization, stream-capture, checksum-index, path-format, or
metadata-format defect does not by itself invalidate the executed computation.

Evaluate whether the preserved evidence still allows verification of:

- the executed command;
- method and model identity;
- input and dataset identity;
- checkpoint and VAE identity;
- environment and device;
- metric or output; and
- terminal outcome.

Do not rerun an expensive or formal computation solely to repair a
non-material evidence-format defect when the original execution remains
verifiable. Record an append-only correction, provenance clarification, or
non-blocking audit finding instead.

A metadata or logging defect is material when it prevents verification of the
executed method, data, environment, metric, result, or research claim.

## Configuration Rules

Formal Experiment settings and settings that affect a claimed engineering
handoff must be configuration-driven or explicitly recorded.

Record, when applicable:

- model and architecture;
- dataset and split;
- preprocessing;
- optimization;
- scheduler;
- loss;
- evaluation;
- checkpoint and VAE;
- output;
- seed and determinism;
- resume behavior; and
- retry or restart policy.

Do not silently resume from a checkpoint.

A resumed run must identify:

- the checkpoint;
- the source experiment and run;
- the intended resume semantics; and
- any state that was not restored.

Checkpoint metadata must identify the associated experiment ID, run ID, and
resolved configuration.

If exact continuation is claimed, preserve, as applicable:

- model state;
- optimizer state;
- scheduler state;
- gradient-scaler state;
- epoch or step;
- best metric and monitor direction;
- sampler or dataloader state; and
- random-number-generator state.

A restart that does not restore all state required for exact continuation must
be labelled as a restart, warm start, partial resume, or other accurate
identity. It must not be described as exact continuation.

Unit-test fixtures, synthetic constants, mock paths, and local diagnostic
values may remain in test code when they are not research settings and their
scope is clear.

Do not force every synthetic check or parser fixture into a separate external
configuration file merely to imitate a Formal Experiment configuration.

## Dataset Validation and Safety

Treat source datasets, annotations, manifests, checkpoints, and outputs as
valuable artifacts.

### Formal Data Execution

Before formal data execution:

- never modify source data in place;
- make preprocessing reproducible and configuration-driven;
- validate dataset structure;
- verify the declared manifest and split;
- clearly fail on missing files, duplicate identifiers, invalid labels, shape
  mismatches, and suspected train/test leakage;
- do not silently skip corrupted samples during formal evaluation;
- record every exclusion rule and excluded sample count;
- do not use held-out test data for tuning, checkpoint selection, threshold
  selection, stopping-rule adjustment, or model selection; and
- preserve the identity of the exact samples evaluated.

Maintain a dataset manifest that records, as applicable:

- source;
- version;
- split definition;
- sample counts;
- preprocessing assumptions;
- exclusions;
- pairing or grouping rules; and
- relevant integrity hashes when practical.

A change to formal sample inclusion, split, pairing, exclusion, or
preprocessing is a material research change unless already authorized by the
plan.

### Non-Formal Data Use

A non-formal pilot or Engineering Discovery check may use:

- synthetic data;
- an explicitly labelled unvalidated sample;
- a small read-only subset; or
- an `Unproven` prepared asset

when the purpose is limited to interface, shape, runtime, memory, device, or
feasibility validation.

Such inputs must be labelled non-formal, exploratory, or `Unproven`.

They must not be used for:

- formal metric reporting;
- dataset comparison;
- threshold selection;
- checkpoint selection;
- model selection; or
- research claims.

Full dataset-manifest and split validation is required before formal data
execution, not before every synthetic or non-formal engineering check.

## Minimum Validation Before a Formal Run

Before a long or expensive Formal Experiment, verify the applicable items:

1. Dataset validation succeeds on representative real samples.
2. One batch can be loaded and forwarded through the model.
3. Losses, outputs, and metrics expected at this stage are finite.
4. Backward pass and optimizer step succeed, if training.
5. Checkpoint save and restore behavior works, if checkpointing is required.
6. Evaluation can run independently from stored artifacts.
7. Inference produces the required output format.
8. Model, checkpoint, VAE, dataset, and device identities match the plan.
9. The output path and applicable metadata files are created correctly.
10. Required fallbacks are disabled or explicitly authorized.

These checks are implementation-readiness checks, not Formal Experiment
results.

A failed readiness check may be repaired and rerun within the approved local
repair authority and repair budget.

It does not require:

- a new experiment ID;
- a new plan;
- a new ledger entry; or
- a separate archive dossier

unless it reveals a material contract change, exceeds the approved scope, or
meets another escalation condition in `docs/experiment_protocol.md`.

Record skipped checks and their reason in the applicable:

- plan;
- implementation audit; or
- run metadata.

Do not create a Formal Experiment result report when formal execution never
began.

The independent readiness audit, when required, follows
`docs/subagent_workflow.md`.

## Version and Toolchain Changes

Do not change Python, PyTorch, CUDA, compiler, native-extension, package
ownership, or related runtime versions merely because a package resolver
accepts them.

Before an authorized change to the target environment, retain the transition
evidence required by `docs/experiment_protocol.md`.

The operational review must be proportional to the affected contract and the
declared transition risk.

When applicable, verify:

1. Source-declared support and relevant upstream compatibility evidence.
2. Affected build syntax, CUDA/C++ and Python APIs, ABI assumptions, compiler
   expectations, and GPU architecture flags.
3. A dry-run package transaction listing removals, replacements, downloads,
   and package ownership conflicts.
4. A verified compatible path or approved equivalent implementation for every
   affected unsupported or unverified API.
5. A bounded post-change native build, import, runtime, and synthetic smoke
   check on the required device.
6. Absence of silent CPU fallback or unauthorized runtime substitution.
7. Preservation of the declared interface and behavior.

If these controls do not establish compatibility, record **BLOCKED** or
`CONTRACT_ESCALATION`.

Do not continue by:

- changing syntax opportunistically;
- replacing vendor source silently;
- expanding the authorized package transaction;
- weakening the declared device requirement; or
- treating successful installation as proof of runtime compatibility.

For native-extension or ABI version problems, prefer an authorized disposable
direct-compile probe after the applicable static review and before changing the
target environment.

Use:

- a clean source copy;
- the intended compiler and CUDA cohort;
- the target GPU architecture flags; and
- the declared interface contract.

Retain the first reproducing build failure and the final verification evidence.

A disposable direct-compile or compatibility probe may use bounded local
repairs within its approved discovery envelope.

The following defects do not require a new plan when they remain within the
authorized source, dependency, interface, ABI, device, and research boundary:

- include-path defects;
- build-command defects;
- working-directory defects;
- environment-variable defects; and
- other non-material invocation defects.

A Conda/pip CUDA-runtime ownership overlap may be tolerated only in an
authorized disposable diagnostic environment.

It must:

- be recorded as a limitation;
- not mutate the target environment; and
- not be used as a target-environment compatibility handoff.

A declared lightweight Python dependency that does not change Python,
PyTorch, CUDA, compiler, native-extension, or runtime ownership may follow the
lower-risk dependency procedure authorized by `AGENTS.md`.

## Errors and Diagnostic Events

Preserve errors and the logs necessary to understand them.

During a Formal Experiment, inspect the immediate cause before changing any
setting.

Use the retry and repair budget declared by the applicable plan, discovery
envelope, or formal retry policy.

When no explicit budget exists, use the smallest reasonable number of low-risk
attempts and stop before the work expands into:

- a material contract change;
- target-environment mutation;
- a new resource requirement;
- a research-condition change; or
- an unauthorized fallback.

There is no universal fixed limit of two diagnostic attempts.

Preserve:

- the first reproducing failure;
- the final verification evidence; and
- additional intermediate attempts only when needed to explain a material
  decision, regression, incident, or escalation.

Do not require a canonical receipt, ledger entry, audit, or archive dossier for
every intermediate diagnostic attempt.

During a Formal Experiment, do not change a research condition in response to
an error.

A pre-authorized operational retry or restart may proceed when it preserves the
formal contract and the retry policy is recorded.

Otherwise, stop and disclose the failure.

The following are diagnostic events requiring investigation before continuing
a Formal Experiment:

- NaN or Inf loss, gradients, outputs, or metrics;
- out-of-memory errors;
- missing or incompatible checkpoints;
- missing data or malformed dataset records;
- unavailable device or unexpected CPU fallback;
- tensor shape or dtype mismatch;
- output identical or nearly identical to input when transformation is
  expected;
- silent sample exclusion;
- unexpected model, checkpoint, VAE, or dataset identity;
- invalid metric output; and
- evidence that the executed command differs materially from the approved
  plan.

A warning, informational message, or non-empty stderr stream is not
automatically a run failure.

It becomes blocking when it indicates:

- invalid computation;
- silent fallback;
- data loss;
- numerical corruption;
- material contract violation;
- unauthorized environment behavior; or
- inability to verify the result.

Do not respond to an error by:

- changing multiple research hyperparameters;
- replacing a model, checkpoint, VAE, dataset, metric, or baseline;
- reinstalling or mutating the target environment;
- deleting artifacts;
- weakening an acceptance criterion; or
- changing the stopping rule

without the authority required by `docs/experiment_protocol.md`.

Material deviation is defined by `docs/experiment_protocol.md`.

Repair authority, audit triggers, and escalation sequence are defined by
`docs/subagent_workflow.md`.

## Code and Validation Standards

Do not introduce silent fallbacks.

Required components that are missing, disabled, invalid, or incompatible must
produce:

- a clear error;
- an explicit blocked state; or
- an explicitly authorized and recorded fallback.

A fallback must not silently change:

- model or method identity;
- checkpoint or VAE;
- dataset or split;
- preprocessing;
- metric;
- device;
- dtype;
- precision;
- resource boundary; or
- research interpretation.

For every material code change, add or update the smallest relevant test when
practical, and run the applicable:

- unit test;
- regression test;
- smoke test;
- parser or fixture test;
- CLI validation; or
- synthetic contract check.

Materiality is defined by `docs/experiment_protocol.md`.

For a non-material local repair, run the smallest relevant regression or
validation.

A non-material repair does not require a separate:

- Formal Experiment;
- experiment ID;
- independent audit;
- ledger entry; or
- archive dossier

unless it is part of a declared final engineering handoff or another explicit
governance trigger.

Keep module boundaries clear and avoid unrelated refactors.

Nonfunctional placeholders must:

- raise `NotImplementedError`; or
- provide a clear TODO and fail-loud behavior.

They must not appear complete or silently produce plausible output.

Engineering execution success establishes only the declared technical handoff.
It does not establish research success or acceptance.
