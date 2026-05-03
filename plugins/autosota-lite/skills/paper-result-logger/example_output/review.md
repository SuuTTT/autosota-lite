# TRACE: Transition-Graph Regularization via Adaptive Coding Entropy for Data-Driven Control — Multi-Panel Experiment Workbench Review

> Draft-only review. Artificial and estimated values are placeholders and must be replaced before submission.

## Provenance
- **EXPERIMENTED**: `experimented`
- **PUBLIC**: `public`
- **ESTIMATED**: `estimated`
- **ARTIFICIAL**: `artificial`
- **MODIFIED**: `modified`
- **DERIVED**: `derived`


## Multi-panel figure config

Each curve/visualization section now uses a shared `config` object plus per-panel data. In the HTML dashboard you can edit:

- simple controls: columns, size, font, line width, marker size, legend, envelope, shared axes, and provenance badges;
- advanced JSON: the full figure-group `config` object;
- per-panel JSON: the data for each task/condition.

Exports are available for individual panels, whole figure groups, and the entire workbench.

## 5.1 Setup
environments, metrics, training budget, seeds, baselines

| Environment/Task | Primary metric | Training budget | Seeds | Baselines |
| --- | --- | --- | --- | --- |
| Walker Walk<br><sub>derived</sub> | Return (↑)<br><sub>derived</sub> | 500k steps<br><sub>derived</sub> | 5<br><sub>derived</sub> | TD-MPC2, DreamerV3, PlaNet<br><sub>derived</sub> |
| Cheetah Run<br><sub>derived</sub> | Return (↑)<br><sub>derived</sub> | 500k steps<br><sub>derived</sub> | 5<br><sub>derived</sub> | TD-MPC2, DreamerV3, PlaNet<br><sub>derived</sub> |
| Cartpole Swingup<br><sub>derived</sub> | Return (↑)<br><sub>derived</sub> | 500k steps<br><sub>derived</sub> | 5<br><sub>derived</sub> | TD-MPC2, DreamerV3, PlaNet<br><sub>derived</sub> |
| Reacher Easy<br><sub>derived</sub> | Return (↑)<br><sub>derived</sub> | 500k steps<br><sub>derived</sub> | 5<br><sub>derived</sub> | TD-MPC2, DreamerV3, PlaNet<br><sub>derived</sub> |

## 5.2 Main Results
methods × tasks final-score table

| Method | Walker Walk Return (↑) | Cheetah Run Return (↑) | Cartpole Swingup Return (↑) | Reacher Easy Return (↑) |
| --- | --- | --- | --- | --- |
| TRACE<br><sub>derived</sub> | 840<br><sub>experimented</sub> | 903<br><sub>artificial</sub> | 791<br><sub>artificial</sub> | 954<br><sub>artificial</sub> |
| TD-MPC2<br><sub>derived</sub> | 828<br><sub>public</sub> | 888<br><sub>public</sub> | 773<br><sub>artificial</sub> | 933<br><sub>artificial</sub> |
| DreamerV3<br><sub>derived</sub> | 820<br><sub>public</sub> | 880<br><sub>public</sub> | 765<br><sub>artificial</sub> | 925<br><sub>artificial</sub> |
| PlaNet<br><sub>derived</sub> | 778<br><sub>artificial</sub> | 838<br><sub>artificial</sub> | 723<br><sub>artificial</sub> | 883<br><sub>artificial</sub> |

## 5.3 Learning and Sample Efficiency
one learning-curve panel per task/environment

- Asset type: `panel_group / line`
- Number of panels: `4`
- Panels:
  - `learning_walker_walk` — Walker Walk
  - `learning_cheetah_run` — Cheetah Run
  - `learning_cartpole_swingup` — Cartpole Swingup
  - `learning_reacher_easy` — Reacher Easy

## 5.4 Ablation Study
full method and variants

| Variant | Walker Walk Return (↑) | Cheetah Run Return (↑) | Cartpole Swingup Return (↑) | Reacher Easy Return (↑) |
| --- | --- | --- | --- | --- |
| TRACE<br><sub>experimented</sub> | 840<br><sub>experimented</sub> | 903<br><sub>artificial</sub> | 791<br><sub>artificial</sub> | 954<br><sub>artificial</sub> |
| w/o adaptive coding entropy<br><sub>derived</sub> | 828<br><sub>artificial</sub> | 887<br><sub>artificial</sub> | 771<br><sub>artificial</sub> | 930<br><sub>artificial</sub> |
| w/o transition-graph regularization<br><sub>derived</sub> | 816<br><sub>artificial</sub> | 875<br><sub>artificial</sub> | 759<br><sub>artificial</sub> | 918<br><sub>artificial</sub> |
| w/o soft coding tree<br><sub>derived</sub> | 804<br><sub>artificial</sub> | 863<br><sub>artificial</sub> | 747<br><sub>artificial</sub> | 906<br><sub>artificial</sub> |
| w/o latent graph feedback<br><sub>derived</sub> | 792<br><sub>artificial</sub> | 851<br><sub>artificial</sub> | 735<br><sub>artificial</sub> | 894<br><sub>artificial</sub> |

## 5.5 Generalization
one panel per task showing unseen-condition difficulty curves

- Asset type: `panel_group / line`
- Number of panels: `3`
- Panels:
  - `gen_walker_walk` — Walker Walk unseen difficulty
  - `gen_cheetah_run` — Cheetah Run unseen difficulty
  - `gen_cartpole_swingup` — Cartpole Swingup unseen difficulty

## 5.6 Robustness
one panel per perturbation type or task

- Asset type: `panel_group / line`
- Number of panels: `3`
- Panels:
  - `rob_observation_noise` — observation noise
  - `rob_action_noise` — action noise
  - `rob_dynamics_shift` — dynamics shift

## 5.7a Scalability: performance curves
one panel per problem-size axis

- Asset type: `panel_group / line`
- Number of panels: `3`
- Panels:
  - `scale_state_dimension` — state dimension
  - `scale_action_dimension` — action dimension
  - `scale_planning_horizon` — planning horizon

## 5.7b Scalability and Efficiency: cost table
training time, inference time, memory, parameters

| Method | Training time (h) ↓ | Inference time (ms) ↓ | Memory (GB) ↓ | Parameters (M) ↓ |
| --- | --- | --- | --- | --- |
| TRACE<br><sub>derived</sub> | 7.8<br><sub>artificial</sub> | 3.2<br><sub>artificial</sub> | 4.8<br><sub>artificial</sub> | 18.5<br><sub>artificial</sub> |
| TD-MPC2<br><sub>derived</sub> | 7.1<br><sub>artificial</sub> | 2.9<br><sub>artificial</sub> | 4.2<br><sub>artificial</sub> | 17.2<br><sub>artificial</sub> |
| DreamerV3<br><sub>derived</sub> | 8.4<br><sub>artificial</sub> | 3.6<br><sub>artificial</sub> | 5.1<br><sub>artificial</sub> | 21.1<br><sub>artificial</sub> |
| PlaNet<br><sub>derived</sub> | 5.6<br><sub>artificial</sub> | 2.4<br><sub>artificial</sub> | 3.6<br><sub>artificial</sub> | 15.4<br><sub>artificial</sub> |

## 5.8 Qualitative Analysis
one qualitative diagnostic panel per task/example

- Asset type: `panel_group / heatmap`
- Number of panels: `3`
- Panels:
  - `qual_walker_walk` — Walker Walk transition modules
  - `qual_cheetah_run` — Cheetah Run transition modules
  - `qual_cartpole_swingup` — Cartpole Swingup transition modules

## 5.9 Case Study / Failure Cases
failure modes, frequency, explanation

| Failure mode | Frequency (%) ↓ | Explanation | Mitigation |
| --- | --- | --- | --- |
| latent module collapse<br><sub>artificial</sub> | 12.0<br><sub>artificial</sub> | regularization too strong<br><sub>artificial</sub> | reduce lambda_TRACE or add warmup<br><sub>artificial</sub> |
| poor long-horizon rollout<br><sub>artificial</sub> | 18.0<br><sub>artificial</sub> | world-model compounding error<br><sub>artificial</sub> | shorter imagination horizon or uncertainty penalty<br><sub>artificial</sub> |
| sparse reward sensitivity<br><sub>artificial</sub> | 9.0<br><sub>artificial</sub> | weak early transition signal<br><sub>artificial</sub> | pretraining or reward-balanced replay<br><sub>artificial</sub> |
