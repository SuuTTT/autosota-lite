---
name: autosota-agent-scheduler
description: AgentScheduler skill for orchestrating the full AutoSOTA optimization lifecycle across research codebases, including baseline measurement, code cognition, idea scheduling, iterative git-backed optimization, best-state export, and multi-paper multi-GPU resource management.
---

# AutoSOTA AgentScheduler: Lifecycle Management

Use this skill to run or design the orchestration loop for optimizing reproduced research codebases. AgentScheduler coordinates the full lifecycle: environment initialization, measured baseline, repository cognition, idea library construction, iterative code modification and evaluation, state persistence, best-state recovery, export, and multi-paper resource scheduling.

## Operating Rule

Every scheduled optimization must preserve the paper's experimental contract. AgentScheduler may choose ideas, allocate resources, checkpoint code, and trigger repair/debugging, but it must route scientific-validity decisions through AgentSupervisor-style red lines and execute only ideas cleared by the audit.

## Related Skills

- Use **AgentInit** for environment initialization and baseline execution.
- Use **AgentFix** for runtime conflicts, failed installs, broken paths, CUDA/toolchain issues, and debug loops.
- Use **AgentIdeator** for `research_report.md` and initial `idea_library.md` construction.
- Use **AgentMonitor** for trace tracking, deadlock detection, budget interventions, and persistent memory updates.
- Use **AgentSupervisor** before executing any idea that may affect evaluation semantics or paper constraints.

## Core Artifacts

- `scores.jsonl`: append-only score ledger. Iteration 0 is the measured baseline.
- `code_analysis.md`: repository cognition map from Phase 1.
- `research_report.md`: external research prior, usually produced before or during Phase 2.
- `idea_library.md`: candidate pool and execution history.
- `logs/agentfix.jsonl`: repair memory for recurring failures.
- Git tags:
  - `_baseline`: unmodified measured baseline state.
  - `_best`: current best validated optimization state.
- Per-iteration git commits:
  - record `PRE_COMMIT` before modifying code.
  - commit successful implementation/evaluation states.

## Phase 0: Environment Initialization and Baseline Measurement

Goal: produce a runnable, versioned, measured baseline.

1. Launch or attach to the target paper container.
2. Initialize a lightweight git layer inside the repository if missing.
3. Commit the unmodified repository and tag it `_baseline`.
4. Discover or confirm the evaluation command.
5. Execute the full evaluation pipeline.
6. Record empirically measured baseline metrics as iteration 0 in `scores.jsonl`.
7. Tag the baseline as `_best` until an optimization beats it.

Baseline scores must come from the reproduced environment, not only from the paper's reported table.

## Phase 1: Code and Paper Understanding

Goal: build a durable cognition map before optimization begins.

1. Inspect repository layout, scripts, configs, evaluation code, data flow, and algorithmic branches.
2. Identify the primary metric, secondary metrics, runtime per evaluation, required hardware, and expensive steps.
3. Enumerate hard constraints:
   - frozen evaluation logic.
   - dataset split and label integrity.
   - paper-specific methodological boundaries.
   - forbidden shortcuts or post-processing.
4. Save findings to `code_analysis.md`.
5. Make the constraints explicit enough for AgentSupervisor to audit future ideas.

Use targeted retrieval after this phase instead of repeated full-repository scans.

## Phase 2: Idea Library Construction

Goal: produce a cleared, prioritized search space.

1. Trigger AgentIdeator to create or refresh `research_report.md`.
2. Create `idea_library.md` with at least ten candidate ideas when possible.
3. Interleave idea granularities:
   - **Micro**: single parameter, threshold, seed, prompt, or config changes.
   - **Meso**: function-level algorithmic changes or localized code improvements.
   - **Macro**: pipeline-stage restructuring within the original protocol.
4. Annotate each idea with:
   - `PARAM | CODE | ALGO`.
   - priority.
   - risk level.
   - implementation assumptions.
   - metric target.
   - expected cost.
5. Run a red-line audit.
6. Mark ideas as:
   - `CLEARED`: eligible for execution.
   - `REJECTED`: violates constraints.
   - `REVIEW`: requires human or AgentSupervisor review.

Only `CLEARED` ideas may enter the Phase 3 scheduler.

## Phase 3: Iterative Optimization Loop

Run up to `MAX_ITERATIONS`, stopping early if the primary metric exceeds the target threshold or if budget is exhausted.

Each iteration has eight required steps:

0. **Pre-Iteration Reflection**
   - Summarize best score, current state, recent idea types, remaining budget, and unresolved risks.
   - Decide Normal Path or Leap Path.

1. **Idea Selection**
   - Normal Path: choose the highest-value `CLEARED` idea from `idea_library.md`.
   - Leap Path: generate a novel structural idea from historical execution and code/research context.

2. **Git Snapshot**
   - Ensure the worktree is understood.
   - Commit the current state before edits.
   - Record `PRE_COMMIT`.

3. **Code Implementation**
   - Apply the selected idea with minimal, localized edits.
   - Preserve evaluation semantics and dataset constraints.

4. **Evaluation**
   - Run the narrowest valid evaluation first when possible.
   - Run the full evaluation before accepting a new best score.

5. **Debugging**
   - If execution fails, invoke AgentFix.
   - Respect a bounded debug budget.
   - On crash or exhausted debug budget, restore `PRE_COMMIT`.

6. **Result Recording**
   - Append metrics, commit hash, idea ID, command, runtime, and notes to `scores.jsonl`.
   - Record failures as well as successes.

7. **Idea Library Update**
   - Update idea status, result delta, implementation notes, and follow-up ideas.
   - Mark exhausted ideas to avoid repetition.

## Normal Path and Leap Path

Use Normal Path by default. Before each iteration, inspect the three most recent executed ideas.

Force **Leap Path** when all three were `PARAM` ideas. Leap Path must introduce a structurally informed `CODE` or `ALGO` idea derived from:

- observed failure modes.
- metric-specific bottlenecks.
- `research_report.md`.
- `code_analysis.md`.
- prior iteration results.

Leap Path ideas receive a **Honeymoon Period**:

- If the first Leap result does not beat `_best`, allow up to five subsequent iterations on the Leap-derived state.
- Use the period for debugging, parameterizing, or refining the structural change.
- If no improvement appears by the end of the period, roll back to the pre-Leap optimum.
- Record the pre-Leap commit and rollback decision in `idea_library.md` and `scores.jsonl`.

## Git and Score Discipline

- Never modify code for an iteration before recording `PRE_COMMIT`.
- Use `_baseline` for the measured unmodified state.
- Use `_best` for the best validated state.
- Advance `_best` only after a valid full evaluation improves the primary metric without unacceptable secondary-metric regression.
- Prefer an atomic `record_score.sh` helper when available; otherwise update `scores.jsonl` and `_best` in one clearly documented step.
- If evaluation crashes or the debug budget is exhausted, restore `PRE_COMMIT` and record the failed attempt.

## Phase 4: Finalization and Export

1. Restore the repository/container to `_best`.
2. Run final evaluation from `_best`.
3. Verify final metrics match the best recorded score.
4. Build or commit the optimized Docker image layer, conventionally `autosota/paper:optimized`.
5. Export the complete optimized repository to a host-accessible directory.
6. Export logs and artifacts:
   - `scores.jsonl`.
   - `code_analysis.md`.
   - `research_report.md`.
   - `idea_library.md`.
   - repair logs.
   - final evaluation output.
7. Clean up containers and release GPU memory.

## Multi-Paper Resource Management

Use a global scheduler when running multiple papers.

- Treat two GPUs as the basic compute unit.
- Each compute unit runs at most one active task.
- Papers waiting for optimization form a unified queue.
- Assign the next queued paper to the first available compute unit.
- Write scheduler state to disk after every assignment, completion, failure, or recovery action.

## Scheduler State

Persist state in a machine-readable file such as `scheduler_state.json`.

```json
{
  "updated_at": "YYYY-MM-DDTHH:MM:SSZ",
  "compute_units": [
    {
      "unit_id": "gpu-0-1",
      "gpus": [0, 1],
      "status": "idle|running|recovering|disabled",
      "paper_id": "paper-name-or-null",
      "pid": 12345,
      "started_at": "YYYY-MM-DDTHH:MM:SSZ"
    }
  ],
  "papers": [
    {
      "paper_id": "paper-name",
      "stage": "queued|configuring|baseline|optimizing|finalizing|done|failed|blocked",
      "assigned_unit": "gpu-0-1",
      "pid": 12345,
      "started_at": "YYYY-MM-DDTHH:MM:SSZ",
      "output_dir": "path/to/output",
      "last_result": "success|failed|unknown"
    }
  ]
}
```

## Recovery Mode

On scheduler restart:

1. Load persisted scheduler state.
2. For every `running` paper, check whether the recorded process ID is still alive.
3. If alive, keep the assignment and continue monitoring.
4. If not alive, inspect output artifacts:
   - success marker or final report.
   - `scores.jsonl`.
   - exported repository.
   - optimized Docker image layer.
   - failure logs.
5. Mark the paper `done`, `failed`, or `blocked`.
6. Free compute units whose processes have ended.
7. Resume dispatch from the global queue.

## Task Launch Procedure

When assigning a paper:

1. Create or reuse an isolated working directory/container.
2. Write allocated GPU IDs into the paper configuration.
3. If initial configuration is incomplete, run configuration discovery using replication image/logs as context.
4. Start the optimization agent in an independent process.
5. Persist `paper_id`, compute unit, PID, start time, output directory, and current stage.
6. Continue scheduling other units without depending on the user's terminal session.

## Completion Verification

A task is successful only when artifacts prove it:

- final score ledger exists and contains a best iteration.
- final evaluation output exists and matches the best state.
- optimized repository export exists.
- image build or container commit succeeded if required.
- red-line audit did not mark the winning change invalid.

After completion, clean up containers, kill remaining child processes, clear GPU memory, update scheduler state, and immediately dispatch the next queued task.

## Output

When reporting Scheduler activity, include:

- Current phase or global queue state.
- Active paper, compute unit, PID, and elapsed time.
- Best score versus baseline.
- Current idea or Leap/Honeymoon status.
- Last persisted state path.
- Next scheduled action.
