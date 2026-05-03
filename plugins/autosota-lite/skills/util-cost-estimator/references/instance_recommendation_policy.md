# Instance Recommendation Policy

Use workload shape before GPU prestige. Vast.ai recommendations should balance runtime, reliability, CPU throughput, VRAM, RAM, disk, and interruption risk.

## CleanRL CartPole and Tiny Classic-Control Smoke Tests

- Recommend local CPU or a cheap CPU-heavy instance.
- Vast.ai GPU is usually unnecessary.
- If renting anyway, RTX 3060, RTX 3070, RTX 3080, or RTX 3090 budget offers are enough.
- Focus on CPU reliability and low price, not GPU power.

## CleanRL PPO Atari with EnvPool

- Default to RTX 4090 on-demand when price is reasonable.
- Use RTX 3090 as the budget option.
- Use RTX 4090, L40, or A40 when larger memory or safer headroom is useful.
- Usually avoid A100 or H100 unless running many parallel experiments, large models, or multi-GPU sweeps.
- Reason: EnvPool can make environment stepping very fast, so the workload may become CPU/GPU mixed. Prefer good CPU cores plus a strong GPU over expensive VRAM alone.

## MuJoCo and Vectorized Continuous-Control RL

- Default to RTX 4090 or RTX 3090.
- CPU quality matters for environment throughput.
- A100 and H100 are usually overkill unless many experiments are batched.

## Multi-Agent RL, Image-Based RL, and Large Batch Experiments

- Recommend RTX 4090, L40, A40, or A100 depending on memory.
- Consider A100 40GB or 80GB for large CNN or transformer policies, many parallel seeds, or high VRAM pressure.
- For many small parallel jobs, prefer multiple cheaper RTX 3090 or RTX 4090 instances over one H100.

## LLM-Based RL or RLHF

- Recommend A100 80GB, H100, or multi-GPU setups depending on model size.
- Treat this as a separate large-model workload, not as a small CleanRL-style test.

## Default for First AutoSOTA-Lite Concurrent RL Test

1. Start on Mac with analysis only.
2. Use Linux with local CPU/GPU for smoke tests if available.
3. If renting Vast.ai, start with an on-demand RTX 4090, 16+ vCPU, 32-64GB RAM, 50-100GB disk, and high reliability.
4. Use RTX 3090 if much cheaper.
5. Avoid A100/H100 until the workflow is proven.
6. Use interruptible only for disposable experiments, not long baselines.
