# autosota-lite

A lightweight AutoSOTA-style workflow plugin for reproducing, auditing, improving, and estimating ML paper reproduction work.

## Runtime and Vast.ai cost estimator skill

Use `autosota-runtime-cost-estimator` to estimate training/evaluation runtime and Vast.ai rental cost for ML/RL paper reproduction runs, AutoSOTA-style experiment loops, and concurrent RL workloads such as CleanRL with EnvPool.

Example 1: Mac analysis-only

```text
Use autosota-runtime-cost-estimator. I am on Mac. Do not run a pilot benchmark. Search the repo/paper and estimate runtime/cost for CleanRL PPO CartPole.
```

Example 2: Linux evidence-first

```text
Use autosota-runtime-cost-estimator. Search repo evidence first. Do not run a pilot yet. Estimate CleanRL PPO Atari EnvPool runtime.
```

Example 3: Linux propose pilot

```text
Use autosota-runtime-cost-estimator. Propose a 60-second pilot benchmark command for CleanRL PPO Atari EnvPool, but do not run it.
```

Example 4: Vast.ai live offers

```text
Use autosota-runtime-cost-estimator. Query Vast.ai offers for RTX 3090, RTX 4090, L40, and A100. Do not rent anything.
```

Warning: Vast.ai prices are marketplace prices and must be rechecked at decision time. The skill should never rent instances unless explicitly asked.
