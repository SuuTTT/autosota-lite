---
name: autosota-agent-init-fix
description: Combined AgentInit and AgentFix skill for environment initialization and automated failure repair.
---

# AutoSOTA AgentInit & AgentFix: Environment & Repair

Use this skill to transform a brittle repository into an executable baseline and resolve cascading runtime failures.

## AgentInit (Initialization)
- **Phase I: Analysis**: Map paper assets and rubric to an execution plan.
- **Phase II: Construction**: Resolve dependencies, validate GPU/CUDA, and locate entrypoints.
- **Phase III: Protocol Discovery**: Extract exact configurations (HYDRA, YAML, CLI) for baseline reproduction.

## AgentFix (Failure Repair)
- **Signature Recognition**: Map error tracebacks to known failure families (pip, CUDA, path, OOM).
- **Retrieval Before Repair**: Consult a skill registry for verified fix protocols.
- **Memory-Augmented Debugging**: Record attempted repairs in `logs/fixes.jsonl` to prevent cyclical reasoning.
- **Constraint-Preserving Edit**: Repair engineering paths/scripts without altering scientific semantics.
