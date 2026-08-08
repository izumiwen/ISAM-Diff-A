# 計畫範本

Canonical 計畫要求定義於 `docs/experiment_protocol.md`。只有 Formal Experiment 或 material technical uncertainty 需要獨立 Engineering Discovery Plan；已由 `AGENTS.md`、核准計畫或既有 discovery envelope 授權的 routine local repair 不需要新計畫。

## Formal Experiment Plan

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

## Engineering Discovery Plan

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
