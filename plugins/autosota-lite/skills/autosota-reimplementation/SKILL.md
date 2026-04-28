---
name: autosota-reimplementation
description: Standardize AI research code into CleanRL-style one-file implementations for readable reproduction, faster training iteration, fair comparison, and optional JAX rewrites for slow PyTorch or framework-heavy repos.
---

# AutoSOTA Reimplementation

Use this skill when the user wants to turn an AI research repository, paper method, baseline, or experiment into a compact, auditable, CleanRL-style implementation library. The goal is to make code easier to read, train, compare, profile, and optimize without weakening benchmark integrity or creating a fragile dependency stack.

The core promise: preserve the scientific contract while making the implementation small enough that one file tells the whole training story.

## When To Use

Use this skill for:

- Converting a new research codebase into a standardized one-file implementation.
- Building or extending an external library of comparable one-file AI implementations.
- Refactoring multi-file research code for readability, training efficiency, or experiment iteration speed.
- Fixing bit rot in older research repos by replacing brittle setup assumptions with a minimal, current dependency contract.
- Creating matched PyTorch and JAX implementations when the original is slow or difficult to scale.
- Comparing several methods under a shared CLI, logging, seeding, eval, and artifact format.

## Red Lines

These rules apply to every reimplementation:

- Do not change official metrics, test data, labels, or evaluation splits.
- Do not silently replace the benchmark protocol, preprocessing contract, model family, or allowed resources.
- Do not use hidden test statistics, answer leakage, benchmark-specific shortcuts, or hard-coded outputs.
- Do not claim equivalence until outputs, metrics, seeds, and eval commands are compared against the source implementation.
- Do not optimize speed by changing semantics unless the change is explicitly marked as an approximation or ablation.
- Do not add dependency-heavy frameworks, launchers, or logging services to the canonical implementation unless the source method genuinely requires them.

If a speed rewrite needs a semantic change, record it as a controlled variant, not as the canonical reproduction.

## Required Artifacts

Create or update these files in the target implementation library when applicable:

- `implementation_index.md`: Inventory of one-file implementations, source repos, papers, tasks, frameworks, status, and comparison groups.
- `implementation_contract.md`: Local contract for CLI flags, logging, checkpointing, eval, seeds, config style, and file layout. Use `references/implementation_contract.md` as the default.
- `porting_notes.md`: Source repo map, files read, behavior preserved, deviations, unresolved assumptions, and validation evidence.
- `comparison_matrix.md`: Baseline scores, reproduced scores, runtime, memory, hardware, seeds, commands, and artifact paths.
- `runs/`: Logs, metrics, checkpoints, profiler traces, and generated artifacts.
- `implementations/`: One-file implementations, preferably named by task and method, such as `ppo_atari.py`, `dreamer_minigrid.py`, or `vit_cifar10_jax.py`.
- `tests/`: Smoke tests, shape tests, determinism checks, CLI tests, and source-parity tests when feasible.

Do not invent scores, paper claims, dataset facts, hardware numbers, or source behavior. Mark unknowns plainly.

## Dependency Policy

Use the minimum dependency set that runs cleanly on Vast.ai's standard PyTorch image family. Treat `vastai/pytorch` from Docker Hub as the default runtime base and pin the exact tag in each project once selected. Check the current Vast.ai docs or Docker Hub tag list before choosing a tag because available CUDA, PyTorch, Python, and Ubuntu versions change over time.

Prefer dependencies already present in the selected image. Add only the smallest missing packages needed for the implementation, such as `gymnasium`, `tyro`, `tensorboard`, `optax`, or `flax`, and pin versions in a project-local requirements file. Avoid installing full source repos, experiment platforms, hydra stacks, notebooks, or cloud logging clients for the canonical path.

When fixing bit rot:

- Replace deprecated APIs with current equivalents while preserving behavior.
- Prefer small compatibility shims over broad version downgrades.
- Log the base image tag, Python version, framework versions, CUDA version, and added packages.
- Keep source-repo quirks in `porting_notes.md` instead of spreading them through the clean implementation.
- Validate with `python <implementation> --help`, import, one train step, and one eval step in the target image.

See `references/dependency_policy.md` for the default runtime contract.

## External Reference Library

Use bundled reference implementations as style and structure guides, not as hidden dependencies. The basic reference library is CleanRL because it demonstrates compact single-file RL implementations with consistent CLI, logging, seeding, training loops, and eval flow.

Bundled CleanRL references live under `references/external_code/cleanrl/`:

- `ppo.py`: discrete-action PPO reference.
- `ppo_continuous_action.py`: continuous-action PPO reference.
- `dqn.py`: discrete-action DQN reference.
- `sac_continuous_action.py`: continuous-action SAC reference.
- `MANIFEST.md`: source commit, URLs, retrieval date, and refresh notes.
- `LICENSE`: upstream MIT license.

When porting a method, read only the relevant reference file and `MANIFEST.md`. Do not copy CleanRL code blindly into a new implementation; adapt the structural pattern to the target paper, source repo, and benchmark.

## Workflow

1. **Inventory the source**
   - Read the paper or method description, README, configs, training entrypoints, eval scripts, data pipeline, model definition, loss code, and logging/checkpoint code.
   - Identify the canonical train command, eval command, task, metric direction, supported datasets, default hyperparameters, and expected score.
   - Record source files and commands in `porting_notes.md`.

2. **Define the target contract**
   - Read or create `implementation_contract.md`.
   - Choose the canonical framework for the port: PyTorch first for readability and source parity, JAX when the user asks for speed, scaling, accelerator throughput, or the source implementation is slow.
   - Use `references/implementation_contract.md` for the one-file style, `references/dependency_policy.md` for the runtime contract, and `references/jax_rewrite.md` for JAX-specific rewrites.
   - For RL algorithms, inspect the closest CleanRL reference in `references/external_code/cleanrl/`.

3. **Write the one-file implementation**
   - Keep the full training loop, model, loss, optimizer, data pipeline, eval hook, logging, checkpointing, and CLI in one readable file.
   - Prefer explicit code over deep helper abstractions. Small local functions are fine when they clarify model, loss, data, eval, or logging boundaries.
   - Keep CLI flags stable across implementations so methods can be compared by command-line diff.
   - Preserve source defaults unless the user explicitly asks for a variant.

4. **Validate behavior**
   - Run the cheapest checks first: import, CLI help, config parse, model shape, one minibatch, one train step, one eval step.
   - Compare parameter counts, tensor shapes, losses on a fixed tiny batch, metric direction, and checkpoint load/save against the source where possible.
   - Run at least a smoke train/eval before claiming the port works.

5. **Measure efficiency**
   - Record wall-clock time, examples or environment steps per second, peak memory, hardware, framework, precision, compilation time, and batch size.
   - For JAX, report both first-step compile cost and steady-state throughput.
   - Add results to `comparison_matrix.md`.

6. **Iterate safely**
   - Make one meaningful change per optimization iteration.
   - Separate canonical reproduction changes from speed variants, ablations, or approximations.
   - Update `porting_notes.md`, `implementation_index.md`, and `comparison_matrix.md` after each validated port or rewrite.

## Implementation Quality Bar

A port is not complete until it has:

- A single executable file with a consistent CLI and no hidden notebook-only state.
- Reproducible seeds for Python, NumPy, framework, data loaders, and environments when supported.
- A minimal dependency list that works on the selected `vastai/pytorch` image tag.
- Clear logging of config, commit or source version, metric, runtime, hardware, and artifacts.
- A smoke test or short run that exercises train and eval.
- A source-parity note explaining what matched, what intentionally differs, and what remains unverified.
- A comparison row with score and runtime fields filled or marked `pending`.

## JAX Rewrite Rule

Use JAX when the source is bottlenecked by Python loops, poor accelerator utilization, many small tensor ops, slow environment batching, or the user asks for faster iteration. Keep a PyTorch or source-faithful port as the semantic reference when practical. See `references/jax_rewrite.md` before writing or reviewing JAX code.

## Output

End with:

```text
Mode: <inventory|port|jax-rewrite|compare|optimize>
Status: <READY|BLOCKED|RUNNING|COMPLETE|FAILED>
Files read: <paths>
Files changed: <paths or none>
Commands run: <exact commands or none>
Source contract: <train/eval command, metric, dataset, expected behavior>
Runtime contract: <vastai/pytorch tag, added packages, pinned versions>
Implementation: <path, framework, CLI, status>
Validation: <tests, smoke runs, parity checks, logs>
Efficiency: <runtime, throughput, memory, hardware, or pending>
Comparison update: <comparison_matrix.md or implementation_index.md update>
Risks: <semantic, benchmark, dependency, performance, or reproducibility risks>
Next action: <one concrete next step>
```
