---
name: autosota-agent-monitor
description: AgentMonitor skill for tracking long-horizon AutoSOTA execution traces, detecting deadlocks and stalled progress, managing persistent external memory, enforcing budgets, and issuing high-level supervisory actions without replacing the execution agent.
---

# AutoSOTA AgentMonitor: Execution Tracking and Deadlock Prevention

Use this skill during long-running replication or optimization runs. AgentMonitor observes the execution trace, tracks global state, prevents local debugging loops, maintains external memory, and issues high-level interventions such as continue, resume with guidance, fallback, terminate, or rollback.

## Operating Rule

AgentMonitor supervises; it does not become the main execution agent. Give phase-aware guidance and budget decisions, but leave low-level repair implementation to AgentFix or the active execution agent.

## Inputs

- Streamed execution trace: assistant messages, tool calls, command outputs, errors, edits, evaluation results, and termination signals.
- Persistent memory files: `code_analysis.md`, `idea_library.md`, `research_report.md`, repair logs, score logs, and modification records.
- Runtime limits: wall-clock budget, interaction budget, compute/GPU budget, and process responsiveness thresholds.
- Current objective and target metric.

## State Model

Continuously infer the current phase:

- **Setup**: environment creation, dependency installation, Docker/manual setup.
- **Cognition**: repository exploration, entrypoint discovery, constraint extraction.
- **Ideation**: research report creation, hypothesis library construction.
- **Experiment**: implementation of a selected idea.
- **Evaluation**: running metrics and comparing scores.
- **Repair**: diagnosing runtime failures through AgentFix.
- **Reporting**: exporting results, logs, and reproducibility notes.
- **Blocked**: no viable action without missing artifact, human input, or budget extension.

## Deadlock Signals

Intervene when any of these appear:

- Repeated fixes against the same normalized error with no state transition.
- Reinstalling or rebuilding semantically equivalent dependency sets.
- Alternating between two broken paths or commands.
- Long output streams without progress toward setup, evaluation, or reporting.
- Repeated edits to the same file with no metric improvement or new evidence.
- Environment repair consumes the run while the target evaluation is never reached.
- The agent forgets the global target metric, current best score, or active idea.
- Process hangs, exceeds budget, or leaves orphaned subprocesses.

## Supervisory Actions

Choose the least disruptive action that restores progress:

- **CONTINUE**: current trajectory is productive; let execution proceed.
- **RESUME_WITH_GUIDANCE**: restate objective, current phase, next checkpoint, or relevant memory file.
- **CONSULT_SKILL**: direct the agent to AgentFix, AgentSupervisor, AgentIdeator, or another relevant skill.
- **FALLBACK**: switch strategy, such as manual Docker setup, prebuilt wheels, alternate entrypoint, or narrower reproduction target.
- **ROLLBACK**: return to a previously validated state when a branch causes severe regression or instability.
- **TERMINATE**: stop when time, compute, or validity bounds are exceeded.
- **CLEANUP**: kill unresponsive process groups and record what was interrupted.

## Persistent Memory Responsibilities

- **`code_analysis.md`**: AgentMonitor ensures this exists after one-time code cognition and remains the global map of pipeline workflow, key files, entrypoints, evaluation commands, and immutable constraints.
- **`idea_library.md`**: AgentMonitor updates statuses, attempted modifications, metric deltas, failures, and scheduler notes during execution. AgentIdeator owns initial hypothesis construction.
- **`research_report.md`**: AgentMonitor reads this to keep execution aligned with external research priors. It may append execution-derived observations, but AgentIdeator owns major research refreshes.
- **Repair memory**: ensure AgentFix records repeated failures and exhausted remedies in `logs/agentfix.jsonl` or an existing repair log.
- **Score and run logs**: preserve evaluation commands, outputs, commit/state identifiers, and final reproducibility notes.

## Workflow

1. **Initialize external state**
   - Confirm the target objective and metric.
   - Locate or create memory files.
   - Record initial budget and baseline state.

2. **Track phase transitions**
   - Map trace events to current phase.
   - Treat successful setup, first baseline run, completed idea implementation, and metric evaluation as major state transitions.

3. **Detect stagnation**
   - Compare recent actions against prior trace and memory.
   - Normalize repeated errors before judging them as new progress.
   - Escalate if repeated attempts do not produce a new phase, new evidence, or a narrower diagnosis.

4. **Issue high-level intervention**
   - Provide concise guidance that changes search direction without hand-coding the patch.
   - Name the memory artifact or skill the execution agent should consult.
   - Include budget or rollback constraints when relevant.

5. **Maintain memory**
   - Update `idea_library.md` after each attempted idea.
   - Update `code_analysis.md` only when durable pipeline knowledge changes.
   - Append run observations to logs rather than relying on conversation memory.

6. **Control budget and processes**
   - Track elapsed time, rounds, and compute usage.
   - Stop or clean up unresponsive commands.
   - Prefer narrow validation commands before full expensive reruns.

## `code_analysis.md` Minimum Contents

```markdown
# Code Cognition Map: {Project}

## Objective and Metric
- Target:
- Baseline:
- Evaluation command:

## Pipeline
- Data:
- Model:
- Inference:
- Evaluation:

## Key Files
| File | Role | Notes |
|---|---|---|

## Constraints and Red Lines
- Frozen evaluation logic:
- Dataset split:
- Paper-specific restrictions:

## Retrieval Pointers
- Symbols, scripts, configs, or commands useful for future localization.
```

## Intervention Record

When AgentMonitor intervenes, record:

```markdown
### MON-{ID}: {timestamp}
- **Phase**: Setup | Cognition | Ideation | Experiment | Evaluation | Repair | Reporting | Blocked
- **Signal**: {deadlock or progress signal}
- **Action**: CONTINUE | RESUME_WITH_GUIDANCE | CONSULT_SKILL | FALLBACK | ROLLBACK | TERMINATE | CLEANUP
- **Guidance**: {high-level instruction}
- **Budget**: {remaining time/rounds/compute}
- **Memory Updated**: {paths}
```

## Output

Report:

- Current inferred phase.
- Progress since last transition.
- Deadlock or budget risks.
- Supervisory action selected.
- Memory files updated.
- Next checkpoint for the execution agent.
