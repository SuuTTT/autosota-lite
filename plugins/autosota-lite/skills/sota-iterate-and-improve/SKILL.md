---
name: autosota-agent-fix
description: AgentFix skill for diagnosing runtime failures, retrieving known repair protocols before improvising, applying protocol-preserving engineering fixes, and recording reusable failure memory for AutoSOTA replication runs.
---

# AutoSOTA AgentFix: Runtime Conflict Repair

Use this skill when an AutoSOTA replication run hits a runtime, installation, environment, path, download, GPU, cache, or evaluation-command failure. AgentFix turns failure handling into a structured loop: classify the error, retrieve a known repair protocol, apply the smallest valid engineering repair, verify execution, and record memory so the same failure is not rediscovered.

## Operating Rule

Follow **retrieval before repair**. If the failure matches a known operational class, consult the relevant existing skill, note, log, or memory artifact before attempting arbitrary debugging.

AgentFix may repair the engineering path to execution, but it must not alter the scientific protocol. Do not change evaluation semantics, metric definitions, dataset splits, labels, reported constraints, or method choices that affect comparability with the original paper.

## Inputs

- Current repository state and command history.
- Execution environment details: Python version, CUDA/toolchain status, package manager, container boundaries, GPU visibility, disk and shared-memory limits.
- Failure signal: traceback, stderr, exit code, timeout, missing output, corrupted artifact, or silent evaluation mismatch.
- Failure memory: local run logs, global recurring-error notes, structured repair skills, and previous attempted fixes.

## Repair Loop

1. **Capture the failure**
   - Save the failing command, working directory, exit code, stderr/stdout tail, environment variables that matter, and any generated logs.
   - Preserve enough context to reproduce the failure without rerunning expensive steps blindly.

2. **Normalize the signature**
   - Reduce noisy traces into a stable signature: package name, exception class, missing file, CUDA/Python version, HTTP host, command, or path pattern.
   - Group semantically equivalent failures together, such as repeated incompatible reinstall attempts or alternate paths pointing to the same missing artifact.

3. **Classify the failure family**
   - Package installation: pip, conda, source build, wheel availability, dependency resolver, lockfile conflicts.
   - CUDA/toolchain: missing `nvcc`, driver/runtime mismatch, incompatible torch or CUDA extension build.
   - Network/download: blocked container internet, inaccessible model hubs, mirror requirements, transient timeouts, corrupted partial downloads.
   - Runtime environment: Python-version mismatch, missing compiler tools, missing system libraries, permission errors, disk exhaustion, shared-memory insufficiency.
   - Repository layout: broken paths, missing utility scripts, symbolic-link issues, assumed working directory, absent checkpoints, partial reconstruction.
   - Evaluation command: wrong entrypoint, missing config, malformed CLI flags, output path mismatch, script silently assuming another directory layout.

4. **Retrieve before repairing**
   - Search available skills and notes for the classified failure family.
   - Check local memory first, such as `logs/fixes.jsonl`, `logs/agentfix.jsonl`, `memory/failures.jsonl`, or run-specific notes.
   - Check cross-paper or plugin-level repair notes when present.
   - Prefer previously successful remedies for the same normalized signature and avoid remedies already recorded as failed.

5. **Choose an admissible repair**
   - Select the smallest engineering change that preserves the paper protocol.
   - Prefer environment, dependency, path, cache, or wrapper-command fixes before modifying research code.
   - When code edits are necessary, isolate them to compatibility glue, path resolution, logging, or dependency shims unless the original implementation is plainly broken.
   - Record why the repair is admissible under AgentSupervisor-style scientific red lines.

6. **Apply and verify**
   - Apply one repair at a time.
   - Rerun the narrowest command that can validate the fix.
   - If the failure changes, record the transition instead of treating it as the same error.
   - If the repair fails, mark it exhausted for the normalized signature and move to the next distinct strategy.

7. **Update memory**
   - Append a structured record of the failure, attempted repair, result, and next recommendation.
   - Promote repeated successful fixes into a stable skill or repair note.

## Memory Record

Use JSON Lines when possible. A minimal record should include:

```json
{
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "paper_or_repo": "owner/repo or local path",
  "command": "command that failed",
  "signature": "normalized failure signature",
  "family": "package|cuda|network|runtime|layout|evaluation|other",
  "repair": "specific action attempted",
  "result": "success|failed|partial|superseded",
  "evidence": "short verification output or log path",
  "protocol_preserved": true,
  "next": "recommended next action if unresolved"
}
```

Prefer appending to an existing repair memory file. If none exists, create `logs/agentfix.jsonl` in the active reproduction workspace.

## Common Repair Protocols

- **Pip or build failures**: retry with mirrors, pin compatible wheels, downgrade incompatible build dependencies, install prebuilt packages, move `git+https` cloning outside restricted containers, or switch to a development image when CUDA extensions require `nvcc`.
- **Network or model downloads**: use approved mirror endpoints for HuggingFace, pip, or conda; prefetch outside containers that lack internet; clear corrupted partial artifacts only after recording their paths.
- **CUDA mismatch**: inspect `nvidia-smi`, `nvcc --version`, torch CUDA build, and driver compatibility; align wheels with the available runtime before rebuilding extensions.
- **Python migration**: prefer a compatible interpreter or dependency pin over broad source edits; if source edits are needed, keep them to compatibility APIs.
- **Path assumptions**: fix working directory, config paths, symlinks, or wrapper scripts before changing evaluation logic.
- **Shared memory or disk exhaustion**: lower dataloader workers, set cache paths, clean corrupted caches, enlarge `/dev/shm`, or redirect temporary outputs without changing data splits.
- **Missing checkpoints or artifacts**: retrieve documented artifacts, reconstruct expected directories, or mark the run blocked if the artifact is unavailable and scientifically required.
- **Evaluation-command mismatch**: recover the command from README, paper, config files, or scripts; keep metrics and dataset split settings unchanged.

## Cycle Prevention

Before repeating an action, compare it to prior repairs for the normalized signature. Do not loop among equivalent fixes such as reinstalling the same incompatible package, toggling two broken paths, or alternating mirrors without changing the root cause. If three distinct repairs fail, pause to reclassify the failure family and inspect whether the apparent error is downstream of an earlier missing artifact or environment mismatch.

## Output

When reporting an AgentFix intervention, include:

- Failure family and normalized signature.
- Retrieved protocol or memory used.
- Repair action applied.
- Verification command and result.
- Memory record location.
- Scientific-protocol preservation note.
