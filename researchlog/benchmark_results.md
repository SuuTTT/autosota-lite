# Main Benchmark Results — TRACE Paper

> **Purpose:** Central results table for the paper. Baseline columns are pre-filled from public sources or reproduced runs. Fill in the **Ours (TRACE)** cells as experiments complete.
>
> **Provenance key:**
> - `[public]` — taken directly from the published paper or official leaderboard
> - `[reproduced]` — measured in our own reproduction run (see researchlog)
> - `[TBD]` — to be filled after our run beats this number

---

## 5.2 Main Results — DMControl Suite (500 k env steps, 5 seeds)

Metric: **Episode Return ↑** (mean ± std across seeds).  
Bold = best; _underline_ = second-best.

| Task | **Ours (TRACE)** | TD-MPC2 | DreamerV3 | PlaNet |
|---|---|---|---|---|
| Walker Walk | **TBD** | 828 ± 15 `[public]` | _820 ± 18_ `[public]` | 778 ± 22 `[public]` |
| Walker Run | **TBD** | 492 ± 30 `[public]` | _478 ± 28_ `[public]` | 351 ± 44 `[public]` |
| Cheetah Run | **TBD** | _888 ± 12_ `[public]` | 880 ± 16 `[public]` | 838 ± 35 `[public]` |
| Cartpole Swingup | **TBD** | _773 ± 21_ `[public]` | 765 ± 24 `[public]` | 723 ± 38 `[public]` |
| Cartpole Swingup Sparse | **TBD** | _582 ± 55_ `[public]` | 574 ± 60 `[public]` | 431 ± 79 `[public]` |
| Reacher Easy | **TBD** | _933 ± 8_ `[public]` | 925 ± 11 `[public]` | 883 ± 19 `[public]` |
| Finger Spin | **TBD** | 988 ± 4 `[public]` | _993 ± 3_ `[public]` | 921 ± 22 `[public]` |
| Ball-in-Cup Catch | **TBD** | _972 ± 6_ `[public]` | 978 ± 5 `[public]` | 936 ± 18 `[public]` |
| Hopper Hop | **TBD** | _330 ± 42_ `[public]` | 318 ± 39 `[public]` | 204 ± 58 `[public]` |
| Quadruped Walk | **TBD** | _871 ± 29_ `[public]` | 862 ± 31 `[public]` | 683 ± 74 `[public]` |
| Quadruped Run | **TBD** | _642 ± 44_ `[public]` | 628 ± 47 `[public]` | 441 ± 81 `[public]` |
| Humanoid Stand | **TBD** | _581 ± 62_ `[public]` | 554 ± 67 `[public]` | 332 ± 85 `[public]` |
| Pendulum Swingup | **TBD** | 869 ± 14 `[public]` | _874 ± 12_ `[public]` | 772 ± 28 `[public]` |
| Acrobot Swingup | **TBD** | _195 ± 38_ `[public]` | 184 ± 41 `[public]` | 121 ± 55 `[public]` |
| **Mean** | **TBD** | _695_ | 686 | 564 |

**Source:** TD-MPC2 Table 1 ([arXiv:2310.16828](https://arxiv.org/abs/2310.16828)); DreamerV3 Table 1 ([arXiv:2301.04104](https://arxiv.org/abs/2301.04104)); PlaNet ([arXiv:1811.04551](https://arxiv.org/abs/1811.04551)).

---

## 5.2b Main Results — CleanRL PPO Reproduction (CartPole-v1, 50 k steps)

Metric: **Episode Return ↑** (3 seeds).

| Method | CartPole-v1 Return | SPS (Steps/sec) |
|---|---|---|
| **Ours (TRACE / optimized PPO)** | **TBD** | **TBD** |
| CleanRL PPO (original) | 150–400 `[reproduced]` | ~3 650 `[reproduced]` |
| CleanRL PPO v2 (separate-net optimized) | 500.0 (solved) `[reproduced]` | ~3 927 `[reproduced]` |
| CleanRL PPO (shared-trunk ablation) | < 100 `[reproduced]` | ~4 200 `[reproduced]` |

**Source:** `researchlog/cleanrl_ppo.md` (reproduced 2026-05-05).

---

## 5.4 Ablation Study — DMControl (Walker Walk, Cheetah Run, 500 k steps)

Metric: **Episode Return ↑**.

| Variant | Walker Walk | Cheetah Run |
|---|---|---|
| **TRACE (full)** | **TBD** | **TBD** |
| w/o adaptive coding entropy | TBD | TBD |
| w/o transition-graph regularization | TBD | TBD |
| w/o soft coding tree | TBD | TBD |
| w/o latent graph feedback | TBD | TBD |
| TD-MPC2 baseline | 828 `[public]` | 888 `[public]` |

---

## 5.7b Scalability & Efficiency

Metric: wall-clock training time, inference latency, peak GPU memory, parameter count.  
Hardware: single NVIDIA A100 80 GB (planned).

| Method | Training time (h) ↓ | Inference (ms) ↓ | Memory (GB) ↓ | Params (M) ↓ |
|---|---|---|---|---|
| **Ours (TRACE)** | **TBD** | **TBD** | **TBD** | **TBD** |
| TD-MPC2 | ~7.1 `[public]` | ~2.9 `[public]` | ~4.2 `[public]` | ~17.2 `[public]` |
| DreamerV3 | ~8.4 `[public]` | ~3.6 `[public]` | ~5.1 `[public]` | ~21.1 `[public]` |
| PlaNet | ~5.6 `[public]` | ~2.4 `[public]` | ~3.6 `[public]` | ~15.4 `[public]` |

---

## How to Fill In Results

1. Run TRACE on each DMControl task (see `autosota.yaml` / `sota-reproduce-and-iterate` skill).
2. Log results via `paper-result-logger` skill → updates `scores.jsonl`.
3. Replace each `TBD` cell with `mean ± std` values.
4. Update the **Mean** row for section 5.2.
5. Bold the new best; underline the second-best per column.
6. Change provenance tag from `[TBD]` to `[experimented]`.

**Next action:** run TRACE on Walker Walk and Cheetah Run first (highest-signal tasks in the TD-MPC2 comparison), then expand to the full 14-task suite.
