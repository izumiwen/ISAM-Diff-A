# Run Standard

## Scope

Apply this standard before and during training, evaluation, inference, dataset
validation, or any run that produces stored outputs. Read `AGENTS.md` first.

## Run Identity and Output Structure

Every formal run must use a resolved configuration and a new output directory.
Never overwrite an existing run directory. A rerun or changed configuration
requires a new experiment or run ID.

Recommended structure:

```text
outputs/{experiment_id}_{timestamp}/
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

Not every run needs every artifact, but omissions must be intentional and
recorded in the result report.

## Required Metadata

`run_metadata.json` must record, when applicable:

- Executed command
- Experiment and run IDs
- Git commit hash and working-tree status
- Configuration path and SHA-256 hash
- Python, PyTorch, CUDA, GPU, and device information
- Random seed and determinism settings
- Dataset manifest, version, and split
- Checkpoint source and resume state
- Start and end time

Save the parsed and resolved configuration as `resolved_config.yaml`; do not
rely only on an editable source YAML file.

## Configuration Rules

Use configuration files instead of hidden constants for experiment settings.
Record model, dataset, preprocessing, optimization, scheduler, loss,
evaluation, output, and resume settings where applicable.

Do not silently resume from a checkpoint. A resumed run must identify the
checkpoint and preserve sufficient state for the declared resume behavior.

Checkpoint metadata must identify the associated experiment ID, run ID, and
resolved configuration. If exact continuation is claimed, preserve model,
optimizer, scheduler, scaler, epoch, best metric, and RNG state as applicable.

## Dataset Validation and Safety

Treat source datasets, annotations, checkpoints, and outputs as valuable
artifacts.

- Never modify source data in place.
- Make preprocessing reproducible and configuration-driven.
- Validate dataset structure before a formal run.
- Clearly fail on missing files, duplicate identifiers, invalid labels, shape
  mismatches, and suspected train/test leakage.
- Do not silently skip corrupted samples during formal evaluation.
- Record every exclusion rule and excluded sample count.
- Do not use held-out test data for tuning or model selection.

Maintain a dataset manifest that records source, version, split definition,
sample counts, preprocessing assumptions, and relevant integrity hashes when
practical.

## Minimum Validation Before a Formal Run

Before a long run, verify the applicable items:

1. Dataset validation succeeds on real samples.
2. One batch can be loaded and forwarded through the model.
3. Loss and metrics are finite.
4. Backward pass and optimizer step succeed, if training.
5. Checkpoint save and restore behavior works, if checkpointing.
6. Evaluation can run independently from stored artifacts.
7. Inference produces the required output format.
8. The output path and metadata files are created correctly.

Record skipped checks and their reason.

## Errors and Diagnostic Events

Preserve errors and relevant logs. During a formal run, inspect the immediate
cause before changing settings. Make at most two low-risk diagnostic attempts,
then stop and report if unresolved. A separately approved non-formal
Engineering Discovery Plan may instead use its declared finite repair budget
for short build, import, CLI, or synthetic-shape checks. It must preserve every
attempt and may not use the exception to start a formal run, change a research
condition, or silently change CUDA, PyTorch, system, dataset, or baseline
conditions.

The following are diagnostic events requiring investigation before continuing
with formal experiments:

- NaN or Inf loss, gradients, outputs, or metrics
- Out-of-memory errors
- Missing or incompatible checkpoints
- Missing data or malformed dataset records
- Unavailable device or unexpected CPU fallback
- Tensor shape or dtype mismatch
- Output identical or nearly identical to input when transformation is expected

Do not respond to an error by changing multiple hyperparameters, replacing a
model, reinstalling the environment, or deleting artifacts without approval.

## Code and Validation Standards

Do not introduce silent fallbacks. Required components that are missing,
disabled, invalid, or incompatible must produce a clear error or an explicit
blocked state.

For every material code change, add or update the smallest relevant test when
practical, and run the relevant test, smoke test, or CLI validation. Keep
module boundaries clear and avoid unrelated refactors.

Nonfunctional placeholders must raise `NotImplementedError` or provide a clear
TODO. They must not appear complete.
