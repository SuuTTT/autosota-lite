# One-File Implementation Contract

Use this contract when creating or reviewing CleanRL-style AI research implementations.

## File Shape

Each implementation should be runnable as one script:

```text
implementations/<method>_<task>[_jax].py
```

The file should contain, in this order when practical:

1. Imports and small compatibility checks.
2. Dataclass or argparse CLI config.
3. Seeding and deterministic setup helpers.
4. Dataset or environment construction.
5. Model definitions.
6. Loss, metrics, and eval functions.
7. Checkpoint save/load helpers.
8. Main train loop.
9. CLI entrypoint.

Avoid splitting core behavior into non-obvious local modules. Shared utility imports are acceptable only for stable infrastructure such as logging adapters, benchmark wrappers, or artifact uploaders.

## Runtime Contract

Every implementation should declare its runtime assumptions:

- Base image: `vastai/pytorch:<exact-tag>`.
- Added packages and pinned versions.
- Python, PyTorch, CUDA, and GPU details.
- Whether the file is expected to run on CPU, single GPU, or multiple GPUs.
- Known unsupported source-repo features.

Use `dependency_policy.md` when selecting or repairing dependencies. The canonical implementation should run with the smallest package set practical on the selected Vast.ai image.

## Standard CLI

Prefer these common flags across implementations:

- `--seed`
- `--total-steps` or `--total-timesteps`
- `--dataset` or `--env-id`
- `--data-dir`
- `--eval-interval`
- `--save-interval`
- `--log-dir`
- `--checkpoint`
- `--device`
- `--batch-size`
- `--learning-rate`
- `--num-workers`
- `--precision`
- `--compile`
- `--track`

Keep paper or method-specific flags explicit and documented in the argparse help text.

## Logging Contract

Every run should log:

- Full CLI config.
- Source repo URL or local path and commit when available.
- Implementation file path and git commit when available.
- Dataset, split, metric name, and metric direction.
- Seed, hardware, framework versions, precision, and device.
- Training loss and task metrics at regular intervals.
- Eval command and eval results.
- Runtime, throughput, and peak memory when available.
- Checkpoint and artifact paths.

Prefer JSONL or TensorBoard-compatible scalar logs. Human-readable console logs are useful but not sufficient for comparison.

## Validation Ladder

Run the smallest meaningful checks before expensive training:

1. `python <file> --help`
2. Import or syntax check.
3. Model construction and parameter count.
4. One batch or one environment rollout.
5. One optimizer update.
6. One eval pass.
7. Short smoke run.
8. Source-parity comparison.
9. Full reproduction run.

## Comparison Matrix Columns

Use these columns when updating `comparison_matrix.md`:

```text
method | task | framework | base_image | added_packages | source_ref | implementation | status | metric | score | metric_direction | seed | train_command | eval_command | wall_time | throughput | peak_memory | hardware | logs | artifacts | notes
```

Status values:

- `inventory`
- `ported`
- `smoke-pass`
- `parity-pass`
- `full-run`
- `jax-rewrite`
- `optimized`
- `blocked`

## Style Rules

- Optimize for readability first, then speed.
- Keep tensor shapes named in local variable names or comments at risky boundaries.
- Prefer one canonical train loop over framework magic.
- Keep defaults close to the source repo or paper.
- Use stable seed handling and log every non-default argument.
- Keep benchmark adapters thin and explicit.
- Mark approximations, unsupported features, and source deviations in `porting_notes.md`.
- Use bundled CleanRL files under `external_code/cleanrl/` as structural references for RL ports, while preserving upstream license and manifest information.
