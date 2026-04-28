# Research Report: Abstraction + TD-MPC2

## Research Mode

- **Mode used**: Browser research fallback.
- **Reason**: `OPENAI_API_KEY` was not configured, so API deepresearch was unavailable.
- **Date**: 2026-04-27.
- **Query focus**: How state/task abstraction ideas could inform admissible TD-MPC2 optimization hypotheses.

## Task and Metric Framing

TD-MPC2 is a model-based reinforcement learning method for continuous control. It plans in the latent space of a learned implicit, decoder-free world model and reports strong data efficiency and final performance across 104 online RL tasks spanning DMControl, Meta-World, ManiSkill2, and MyoSuite. The official project page emphasizes use of one hyperparameter set across tasks and multitask scaling up to a single large agent trained across 80 tasks.

Relevant metrics depend on the benchmark: DMControl commonly reports episode return, while Meta-World, ManiSkill2, and MyoSuite commonly report success rate or task-specific return. Any AutoSOTA hypothesis should preserve the original benchmark metric, environment steps, dataset split, and evaluation command.

Sources:

- TD-MPC2 paper abstract and results: https://arxiv.org/abs/2310.16828
- Official TD-MPC2 project page: https://www.tdmpc2.com/
- Official implementation: https://github.com/nicklashansen/tdmpc2

## Relevant Patterns

### TD-MPC2 Already Performs Task-Oriented Abstraction

TD-MPC2 maps observations into a latent representation `z = h(s, e)`, predicts latent dynamics `z' = d(z, a, e)`, predicts rewards and terminal values, and uses a policy prior to guide latent-space MPC. This is already a learned abstraction pipeline: the agent does not reconstruct observations, but learns a task-useful state representation optimized for prediction, value estimation, reward prediction, and planning.

Optimization implication: abstraction ideas should usually target the encoder, latent normalization, transition objective, task embeddings, or planning interface rather than adding a separate symbolic abstraction layer.

Source:

- OpenReview PDF, architecture and objective sections: https://openreview.net/pdf/cdd8c302808d5e351cc3b1f56f3be3100dbb8eb7.pdf

### Markov-Preserving Abstraction Is the Key Scientific Constraint

State abstraction work highlights that learned abstract states must preserve enough information for the decision process to remain approximately Markov. One practical approach combines inverse model estimation with temporal contrastive learning to encourage representations that preserve action-relevant dynamics, including in continuous control settings.

Optimization implication: abstraction objectives are most admissible when they improve latent Markovianity or action-conditional predictiveness without changing the reward, metric, dataset split, or evaluation logic.

Source:

- Learning Markov State Abstractions for Deep Reinforcement Learning: https://arxiv.org/abs/2106.04379

### Low-Dimensional, Action-Conditioned SRL Is a Natural Fit for Control

State representation learning for control emphasizes compact features that evolve over time and are influenced by agent actions. This aligns with TD-MPC2's latent dynamics and short-horizon planning: better latent compactness and action-conditioned predictability can reduce planning burden and improve sample efficiency.

Optimization implication: useful levers include latent dimension, SimNorm grouping/temperature, temporal prediction horizon, inverse-dynamics auxiliaries, and representation regularization. These should be treated as model or training changes, not evaluation changes.

Source:

- State Representation Learning for Control overview: https://arxiv.org/abs/1802.04181

## TD-MPC2 Design Details That Matter for Hypotheses

- TD-MPC2 jointly optimizes latent joint-embedding prediction, reward prediction, and value prediction.
- Reward and value prediction use discrete regression with cross-entropy in a log-transformed space, improving robustness across reward scales.
- The architecture uses MLPs with LayerNorm and Mish activations.
- SimNorm projects latent representations into fixed-dimensional simplices via softmax; the paper states this is important for stability and sparsity.
- TD targets use an ensemble of Q-functions, with targets computed from a conservative subsample.
- MPC uses latent rollouts, MPPI-style sampling, a terminal value bootstrap, a policy prior, and warm-started planning.
- Multitask TD-MPC2 uses learnable task embeddings and action masking to support different embodiments/action spaces.

Source:

- OpenReview PDF, method and appendix details: https://openreview.net/pdf/cdd8c302808d5e351cc3b1f56f3be3100dbb8eb7.pdf

## Concrete Optimization Levers

### Candidate A: Tune SimNorm Abstraction Shape

- **Type**: PARAM
- **Risk**: LOW to MEDIUM
- **Lever**: latent dimension, SimNorm group count, simplex size, and temperature.
- **Rationale**: SimNorm is a core TD-MPC2 abstraction mechanism. Adjusting its granularity can change sparsity and latent separability while preserving protocol.
- **Audit note**: Admissible if training and evaluation budgets remain unchanged and the same metrics/environment splits are used.

### Candidate B: Add an Inverse-Dynamics Auxiliary Loss

- **Type**: ALGO
- **Risk**: MEDIUM
- **Lever**: predict action `a_t` from adjacent latent states `(z_t, z_{t+1})`.
- **Rationale**: Markov abstraction literature uses inverse-model objectives to preserve action-relevant distinctions. This may improve latent controllability for planning.
- **Audit note**: Must not use privileged future information beyond training transitions already available in replay. Keep evaluation unchanged.

### Candidate C: Add Temporal Contrastive Regularization

- **Type**: ALGO
- **Risk**: MEDIUM
- **Lever**: encourage temporally adjacent or action-consistent latent states to be structured differently from negatives.
- **Rationale**: Temporal contrastive learning can help abstract states preserve dynamics-relevant structure.
- **Audit note**: Needs careful implementation to avoid using test trajectories or changing data access. Safer for online training replay than benchmark test data.

### Candidate D: Task-Embedding Initialization or Regularization

- **Type**: PARAM/CODE
- **Risk**: LOW to MEDIUM
- **Lever**: task embedding norm, initialization from similar tasks, embedding regularization.
- **Rationale**: TD-MPC2 relies on task embeddings for multitask abstraction. Better embedding geometry may improve transfer and reduce interference.
- **Audit note**: For single-task runs, this may be irrelevant. For multitask or finetuning protocols, preserve allowed task metadata and training data.

### Candidate E: Planner Abstraction Sensitivity Sweep

- **Type**: PARAM
- **Risk**: LOW
- **Lever**: planning horizon, number of MPPI samples, policy-prior sample fraction, warm-start behavior.
- **Rationale**: If abstraction quality changes, the planner may need different rollout depth or sampling. Short horizons depend heavily on terminal value quality; longer horizons stress latent dynamics.
- **Audit note**: Usually admissible if compute budget changes are allowed by the paper protocol. If wall-clock or sample budgets are fixed, route to review.

### Candidate F: Representation-Diagnostics-Only Pass

- **Type**: CODE
- **Risk**: LOW
- **Lever**: add logging for latent norm, SimNorm entropy, prediction error by horizon, Q ensemble disagreement, and task-embedding norms.
- **Rationale**: Diagnostics can identify whether failure comes from abstraction collapse, transition drift, or planner/value mismatch.
- **Audit note**: Admissible if logging does not alter training/evaluation behavior.

## Invalid or Review-Required Shortcuts

- Do not modify benchmark rewards, success thresholds, or evaluation scripts.
- Do not tune on held-out test results unless the protocol permits it.
- Do not use expert labels, privileged simulator state, or task metadata unavailable to the original method.
- Do not replace TD-MPC2 with a stronger external policy/model unless the paper protocol allows method replacement.
- Do not add observation reconstruction losses if they materially change the method scope without explicit review; reconstruction may be scientifically interesting but can shift the decoder-free premise of TD-MPC2.

## Recommended First Hypotheses

1. Start with SimNorm and latent-dimension sweeps because they directly target TD-MPC2's abstraction bottleneck and are relatively easy to audit.
2. Add representation diagnostics before changing algorithmic objectives.
3. If diagnostics show poor action-conditioned latent separation or transition drift, test an inverse-dynamics auxiliary loss.
4. Use temporal contrastive regularization only after checking replay sampling and negative construction against protocol constraints.
