---
name: autosota-agent-monitor-scheduler
description: Combined AgentMonitor and AgentScheduler skill for lifecycle management, deadlock prevention, and iterative optimization (Normal vs Leap paths).
---

# AutoSOTA AgentMonitor & AgentScheduler

Use this skill to orchestrate long-horizon experiments, prevent pathological stalling, and manage persistent context across execution resets.

## AgentMonitor (Supervision & Deadlock Intervention)
- **Phase-Aware Tracking**: Formally track the system state $s_t$ through the execution trace $\mathcal{T}_{0:t}$ (Setup, Cognition, Experiment, Eval, Reporting).
- **Deadlock Detection**: Intervene when characteristic pathologies emerge:
    - **Local Debugging Loops**: Repeated low-value fixes on the same code region/error.
    - **Transient Engineering Focus**: Endlessly repairing environment errors without advancing to the target objective.
- **Supervisory Actions ($a_t^{sup}$)**:
    - **Continue/Resume**: Proceed with high-level guidance.
    - **Fallback**: Pivot to a manual/alternate approach (e.g., manual Docker vs. auto-install).
    - **Terminate/Rollback**: Clean up process groups and revert to `PRE_COMMIT` if budget is exceeded or regression occurs.
- **Budget Control**: Monitor wall-clock time and interaction rounds to ensure responsiveness.

## Persistent Context Management (External Memory)
Maintain three core documents to bound context growth while preserving global awareness. Use the templates defined in `MEM_TEMPLATES.md`:
1. **`code_analysis.md`**: The "Code Cognition Map." A one-time distillation of repository workflow, entry points, and constraints.
2. **`idea_library.md`**: The dynamic idea pool. Externalizes the optimization trajectory (Candidate -> Status -> Result).
3. **`research_report.md`**: The knowledge grounding. Contains distilled SOTA techniques and literature-derived optimization strategies.

## AgentScheduler (Optimization Loop)
- **Phase 0–4**: Baseline measurement -> Code Cognition -> Idea Library -> Iterative Loop -> Export.
- **Normal Path**: Select established ideas from `idea_library.md`.
- **Leap Path (Leap Rule)**: If last 3 ideas were `PARAM`, force a `LEAP` (structural/methodological shift).
- **Efficiency**: Use retrieval-augmented localization (grep/symbolic search) instead of repeated full-repo scans.

