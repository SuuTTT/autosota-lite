---
name: autosota-agent-supervisor
description: AgentSupervisor skill to enforce the Red Line System and prevent invalid optimization gains.
---

# AutoSOTA AgentSupervisor: Scientific Integrity

Use this skill to audit every proposed idea and execution result against strict scientific red lines. The Supervisor ensures that performance gains are legitimate and not achieved through invalid shortcuts.

## The Red Line System
Operations must strictly adhere to these seven non-negotiable constraints. Any violation renders the optimization invalid.

- **R1 — Evaluation Metric Parameters Must Not Change**: No modifying $k$ in recall@k, context window lengths, or switching from average to best-of-N reporting.
- **R2 — Evaluation Script Integrity**: The evaluation script and metric computation code are frozen. Optimizations must happen upstream of the evaluation boundary.
- **R3 — Output Integrity**: Predictions must come from actual model inference. No fabrication or hard-coding of labels or outputs.
- **R4 — No Unfair Trade-offs**: Improvements in the primary metric must not cause significant degradation in secondary metrics. All metrics must be reported.
- **R5 — Dataset Split Integrity**: No test data leakage. The train/test split defined in the paper must be strictly followed.
- **R6 — No Dataset Modification**: No filtering, re-labeling, or re-sampling that changes the evaluation distribution.
- **R7 — Paper-Specific Constraints**: Identify and follow specific task constraints (e.g., specific history window lengths, fixed observation spaces) identified during setup.

## Multi-Layered Supervision Protocol

### Layer 1: Setup Audit (Phase 1)
- Identify all paper-specific hard constraints (R7).
- Enumerate R1-R7 in the `code_analysis.md` document.
- Formalize boundaries before any optimization ideas are generated.

### Layer 2: Idea Library Audit (Phase 2)
- Construct a **Red Line Audit Table** in `idea_library.md`.
- Verify every candidate idea against all 7 red lines.
- **Action**: Mark violators as `REJECTED (Red Line Violation)`. Only `CLEARED` ideas proceed to execution.

### Layer 3: Dynamical Leap Audit (Phase 3)
- For every dynamically generated "Leap" path candidate, perform an immediate R1-R7 check.
- Discard any candidate that violates any constraint before it enters the execution loop.

### Layer 4: Post-Evaluation Verification (Phase 4)
- Audit the final code changes using `git diff` against the `PRE_COMMIT` snapshot.
- Verify that score improvements in `scores.jsonl` are not the result of hidden configuration/metric changes.

## Compliance Policy
These are **absolute prohibitions**. There are no exceptions. Scientific value is derived only from improvements found within these boundaries.
