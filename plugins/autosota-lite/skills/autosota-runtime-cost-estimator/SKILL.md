---
name: autosota-runtime-cost-estimator
description: Estimate training and evaluation runtime plus Vast.ai rental cost for ML/RL paper reproduction runs, AutoSOTA-style experiment loops, and concurrent or parallel RL workloads such as CleanRL with EnvPool. Use when Codex needs evidence-first runtime/cost estimates, platform-safe macOS analysis, Linux-only probing plans, Vast.ai search-only pricing recommendations, or required artifacts such as runtime_estimate.md, cost_estimate.md, cost_estimate.json, and autosota.yaml.
---

# AutoSOTA Runtime Cost Estimator

Estimate runtime and rental cost from evidence before formulas. Prefer paper, repo, configs, scripts, logs, benchmark tables, and prior runs over guesses. Use formulas only after evidence is exhausted, and label confidence clearly.

## Required First Step

Run `uname -s` before any estimation work and set the mode:

- `Darwin`: `mac_analysis_only`
- `Linux` without explicit user approval for probing: `linux_evidence_only`
- `Linux` with explicit user approval for bounded probing: `linux_pilot_allowed`

## Platform Rules

On Darwin/macOS:

- Do not run pilot benchmarks.
- Do not start training.
- Do not run GPU, CUDA, or `nvidia-smi` commands.
- Do not run long eval commands.
- Only inspect files, parse configs, read docs, and estimate from paper/repo evidence.

On Linux:

- Search paper and repo evidence first.
- Run a short pilot benchmark only when the user explicitly asks for runtime probing, the repo is configured, the command is safe, and duration is bounded.
- Never run full training unless the user explicitly asks.

## Evidence Search Order

Inspect these if present before estimating:

- `README.md`, `docs/`, `examples/`
- `scripts/`, `configs/`, shell launchers, Makefiles
- paper PDF, paper markdown, paper HTML, arXiv text, benchmark tables, result tables
- training scripts, evaluation scripts, Dockerfiles, environment files
- WandB links or included result logs
- `runs/`, `logs/`, `outputs/`, `wandb/`, `tensorboard/`
- command-line defaults in argparse, Hydra configs, YAML configs, shell scripts, Makefiles

Extract when possible:

- task type: eval-only, smoke test, full training, multi-seed benchmark, AutoSOTA iteration loop
- algorithm, environment, train command, eval command
- total timesteps, frames, epochs, updates, samples
- `num_envs`, workers, actors, `num_steps`, rollout length
- batch size, minibatches, update count, seeds
- eval, checkpoint, and logging frequency
- reported hardware: GPU, CPU, GPU count, RAM, disk
- wall-clock runtime and throughput: steps/sec, frames/sec, FPS, samples/sec, tokens/sec
- memory and storage usage
- likely bottleneck: CPU-env-bound, GPU-model-bound, environment simulation-bound, I/O-bound, or mixed

## Estimation Priority

Use this order:

1. Paper-reported runtime on known hardware.
2. Repo benchmark logs or README examples.
3. Training script defaults and total workload.
4. Prior run logs in `runs/` or `logs/`.
5. Linux-only pilot benchmark, only with explicit user approval.
6. Rough formula-based estimate with clear uncertainty.

Label every estimate:

- `HIGH`: paper or repo reports runtime and hardware clearly.
- `MEDIUM`: derived from script defaults and comparable logs.
- `LOW`: formula-only estimate with missing hardware or throughput.

Read `references/runtime_estimation_formulas.md` when applying formulas or overhead factors.

## CleanRL and EnvPool Handling

If the repo looks like CleanRL:

- Prefer `ppo.py` commands for tiny smoke tests.
- Prefer `ppo_atari_envpool.py` for concurrent or parallel RL tests.
- Parse `--total-timesteps`, `--num-envs`, `--num-steps`, `--num-minibatches`, `--seed`, `--env-id`, `--cuda`, `--track`, and `--capture-video`.
- Treat tracking and video capture as overhead.
- Recommend disabling video and optional logging for timing probes unless needed.

## Vast.ai Rules

Vast.ai prices are live marketplace prices. Do not invent exact live prices.

- If the user asks for live pricing and the Vast.ai CLI is available, run search-only offer queries.
- If the CLI is unavailable, provide setup instructions:
  - `pip install vastai`
  - `vastai set api-key YOUR_API_KEY`
- Never print API keys.
- Never create, rent, start, stop, destroy, or modify instances unless the user explicitly asks.
- Prefer on-demand instances for uninterrupted training.
- Mention interruptible instances only for cheap exploratory or disposable runs.
- If filters fail, inspect `vastai search offers --help` and adapt search-only commands.

Recommended search-only commands:

```bash
vastai search offers 'gpu_name=RTX_4090 num_gpus>=1 reliability>0.98 verified=true' --limit 10
vastai search offers 'gpu_name=RTX_3090 num_gpus>=1 reliability>0.98 verified=true' --limit 10
vastai search offers 'gpu_name=L40 num_gpus>=1 reliability>0.98 verified=true' --limit 10
vastai search offers 'gpu_name=A100 num_gpus>=1 reliability>0.98 verified=true' --limit 10
```

Read `references/instance_recommendation_policy.md` before recommending GPU or instance classes.

## Required Outputs

Create or update these in the active project workspace:

- `runtime_estimate.md`
- `cost_estimate.md`
- `cost_estimate.json`
- `autosota.yaml` if missing or incomplete

Do not fabricate unknown values. Use `null` in JSON and explicit "missing" notes in Markdown.

### `runtime_estimate.md`

Include:

1. Summary
2. Platform detected
3. Whether pilot benchmark was allowed
4. Evidence found in paper/repo
5. Workload type
6. Training/eval command
7. Workload size
8. Throughput evidence or assumptions
9. Runtime formula
10. Estimated runtime for smoke test, one baseline run, one optimization iteration, N seeds, and full AutoSOTA loop
11. Bottleneck analysis: CPU-bound, GPU-bound, environment simulation-bound, I/O-bound, mixed
12. Confidence level
13. Missing information
14. Recommended next measurement step

### `cost_estimate.md`

Include:

1. Summary
2. Vast.ai pricing caveat that live marketplace prices must be rechecked
3. Recommended instance class
4. Why that instance class fits the workload
5. Estimated cost formula
6. Cost estimate for smoke test, one full run, N seeds, one AutoSOTA iteration, and full AutoSOTA loop
7. Recommended Vast.ai search commands
8. How to choose an offer: reliability, verified host, GPU model, VRAM, CPU cores, RAM, disk, network, max duration, on-demand vs interruptible
9. Low, expected, and high estimate placeholders if live prices are unavailable
10. Risk notes
11. Final recommendation

### `cost_estimate.json`

Write this schema exactly, filling unknowns with `null`, empty arrays, or strings such as `"unknown"`:

```json
{
  "platform": "...",
  "mode": "mac_analysis_only | linux_evidence_only | linux_pilot_allowed",
  "workload_type": "...",
  "algorithm": "...",
  "environment": "...",
  "train_command": "...",
  "eval_command": "...",
  "target_steps": null,
  "num_envs": null,
  "num_seeds": null,
  "autosota_iterations": null,
  "reported_hardware": "...",
  "reported_runtime_hours": null,
  "measured_steps_per_sec": null,
  "estimated_runtime_hours_one_run": null,
  "estimated_runtime_hours_all_seeds": null,
  "estimated_runtime_hours_autosota_loop": null,
  "recommended_gpu_class": "...",
  "recommended_instance_reason": "...",
  "vastai_live_pricing_used": false,
  "vastai_offer_rows": [],
  "cost_formula": "...",
  "estimated_cost_low_usd": null,
  "estimated_cost_expected_usd": null,
  "estimated_cost_high_usd": null,
  "confidence": "LOW | MEDIUM | HIGH",
  "missing_info": []
}
```

## Pilot Proposal Rules

When the user asks for a Linux pilot proposal but not execution:

- Propose one bounded command, preferably around 60 seconds.
- State why it is safe and what it measures.
- Include logging destination.
- Recommend disabling tracking/video for timing.
- Do not run it.

When the user asks to run a Linux pilot:

- Verify platform is Linux.
- Verify the command is bounded and the repo appears configured.
- Confirm it is not full training.
- Capture elapsed time and throughput if available.
- Update the required artifacts with measured evidence.
