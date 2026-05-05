---
name: code-reverse-engineering
description: Reverse-engineer research code to extract abstract architecture, algorithms, and patterns. Steer fast reimplementation with CleanRL-style defaults (JAX/PyTorch, minimal deps, fast iteration).
---

# Code Reverse Engineering

Use this skill to understand and reimplement research code from other repositories. Extract the abstract model (architecture, algorithms, data flow), not literal code. Then reimplement cleanly with fast tech stacks.

## Core Principle

**Extract abstract model, not literal code.**

The output is a clean reimplementation that:
1. ✓ Replicates the paper's results
2. ✓ Uses fast, modern tech (JAX, PyTorch, CleanRL style)
3. ✗ Does NOT copy source code verbatim
4. ✓ Is simpler and faster than the original

## When to Use

- Paper includes code but it's slow, messy, or hard to extend
- You want a clean reference implementation
- You need to integrate the method into your pipeline
- You're improving/extending the paper's method

## Required Inputs

Collect or ask for:

- **Source repo URL** — Link to the original research code
- **Paper reference** — Published paper or arXiv preprint
- **Target tech stack** — Default: `JAX` or `PyTorch` + minimal deps (CleanRL style)
- **Use case** — What you'll use the reimplementation for (training, research, integration, extension)
- **Correctness criteria** — How to verify the reimplement matches the original (same paper results, specific metrics, convergence curves)

## Workflow

### 1. Analyze Source Code Architecture

Read the source code to extract the abstract structure. Do NOT read the code to copy it.

For each major component, document:

**Data structures:**
- Input/output shapes and types
- State representations
- Buffers and caches
- Hyperparameters

**Algorithms:**
- Main training loop structure
- Update rules (loss computation, gradients, optimization)
- Sampling/rollout generation
- Logging and checkpoints

**Dependencies:**
- External libraries used (TensorFlow, PyTorch, Jax, OpenAI Gym, etc.)
- Critical APIs (e.g., `env.step()`, `model.forward()`)
- Custom utilities or preprocessing

**Pattern & philosophy:**
- Is it object-oriented or functional?
- Does it use batching, async, or distributed training?
- How does it handle randomness and reproducibility?
- What's the performance bottleneck (compute, memory, I/O)?

Create a code map like:

```text
Source: openai/baselines/ppo/ppo.py

1. DATA STRUCTURES
   - Observation shape: (env.observation_space,)
   - Action shape: (env.action_space.n,) or (env.action_space.shape,)
   - Rollout buffer: stores (obs, action, reward, done, value, log_prob)
   - Network: policy head (logits/mean) + value head

2. ALGORITHMS
   - Rollout collection: N environments, T timesteps per worker
   - Advantage computation: GAE with γ, λ
   - Policy loss: -log_prob * advantage (with clipping)
   - Value loss: MSE(value_pred, target)
   - Update: gradient descent on (policy_loss + c*value_loss)

3. DEPENDENCIES
   - TensorFlow 1.x (eager mode)
   - OpenAI Gym (env.step, env.reset)
   - NumPy (advantage computation)

4. PHILOSOPHY
   - Vectorized environments (4-16 parallel)
   - On-policy, single GPU
   - Synchronous rollout collection
   - Wallclock time ~30 min per 1M steps (on tested hardware)
```

### 2. Abstract the Code Model

From the code map, create reusable algorithm patterns. Use pseudocode and math, not literal code.

For each algorithm, write:

```text
Algorithm: Proximal Policy Optimization (PPO)

Input: environment, policy network, value network, hyperparameters
Output: trained policy

for episode in 1..max_episodes:
  1. Collect rollouts:
     for step in 1..horizon:
       action ← policy(observation)
       observation', reward, done ← env.step(action)
       store (obs, action, reward, done)
  
  2. Compute returns & advantages:
     returns ← cumulative_discounted_reward(rewards, done, γ)
     advantages ← returns - value_pred  (or GAE)
     normalize advantages
  
  3. Update policy & value:
     for mini_batch in shuffle(all_transitions):
       policy_loss ← -log_prob * clipped_advantage
       value_loss ← (value_pred - target)^2
       total_loss ← policy_loss + c_1 * value_loss + c_2 * entropy
       gradient_step(policy, value, total_loss)
```

Then extract critical design choices:

```text
CRITICAL DESIGN CHOICES:
- Rollout strategy: [vectorized | serial | async]
- Value function: [state value V(s) | state-action Q(s,a)]
- Advantage normalization: [yes | no]
- Gradient updates: [mini-batch SGD | full batch]
- Clipping: [policy gradient clipping | trust region]
- Entropy: [none | added to loss]
```

### 3. Map to Target Tech Stack

Choose a fast, clean tech stack. Default recommendations:

**Fast RL implementations (recommended):**
- `CleanRL` (PyTorch, single-file, fast)
- `JAX` (functional, JIT compilation)
- `Stable-Baselines3` (PyTorch, mature)
- `Ray RLlib` (distributed, advanced)

**Choice matrix:**

| Need | Tech | Why |
|------|------|-----|
| Single-machine, fast | PyTorch + CleanRL | Minimal deps, fast iteration |
| GPU acceleration | JAX | JIT compilation, XLA backend |
| Distributed training | JAX + pmap | Multi-GPU/TPU out of box |
| Simplicity + maturity | Stable-Baselines3 | Well-tested, good docs |
| Research + extension | PyTorch + custom | Maximum flexibility |

**Default: PyTorch + CleanRL style**
- Single file or minimal modules
- No heavy abstractions (classes OK, but keep simple)
- Vectorized rollout collection (gymnasium or brax)
- Native PyTorch ops (no custom CUDA)

### 4. Build Implementation Plan

Create a step-by-step reimplementation guide:

```text
REIMPLEMENTATION PLAN: PPO

Phase 1: Data Flow (no learning yet)
  ✓ Define observation/action spaces
  ✓ Create dummy environment
  ✓ Implement rollout collection (action generation, step, store)
  ✓ Verify shapes and data types match source

Phase 2: Core Algorithm (single step)
  ✓ Implement policy network (same architecture as source)
  ✓ Implement value network
  ✓ Implement forward pass (obs -> logits, value)
  ✓ Implement advantage computation (GAE or simple)

Phase 3: Learning (one mini-batch)
  ✓ Implement loss computation (policy loss, value loss, entropy)
  ✓ Implement gradient step
  ✓ Test on dummy data (should reduce loss)

Phase 4: Integration (one episode)
  ✓ Collect rollouts
  ✓ Update once
  ✓ Log metrics
  ✓ Save checkpoint

Phase 5: Full Training
  ✓ Run on actual task
  ✓ Match hyperparameters from source
  ✓ Validate against paper results
  ✓ Optimize speed/memory

Phase 6: Validation
  ✓ Compare learning curves (source vs reimplement)
  ✓ Check final performance (±5% acceptable)
  ✓ Profile runtime & memory
```

### 5. Create Code Template

Generate starter code with TODOs for custom logic. Follow CleanRL style:

```python
# Single file or minimal module structure
import jax
import jax.numpy as jnp
from flax import linen as nn
import gymnasium as gym
from collections import deque

class PolicyNetwork(nn.Module):
    """Policy = observation -> action logits (or mean for continuous)"""
    action_dim: int
    
    @nn.compact
    def __call__(self, observation):
        # TODO: match source architecture
        x = nn.Dense(64)(observation)
        x = nn.relu(x)
        logits = nn.Dense(self.action_dim)(x)
        return logits

class ValueNetwork(nn.Module):
    """Value function = observation -> scalar value"""
    
    @nn.compact
    def __call__(self, observation):
        # TODO: match source architecture
        x = nn.Dense(64)(observation)
        x = nn.relu(x)
        value = nn.Dense(1)(x)
        return value.squeeze()

def rollout_collection(env, policy_fn, num_steps):
    """Collect rollout: trajectory of (obs, action, reward, done)"""
    # TODO: match source rollout collection
    pass

def compute_advantages(rewards, values, dones, gamma=0.99, lambda_=0.95):
    """GAE advantage computation"""
    # TODO: implement or use source algorithm
    pass

def update_policy(policy, value, rollouts, lr=3e-4):
    """One gradient update step"""
    # TODO: match source loss computation
    pass

def main():
    """Main training loop"""
    env = gym.make("CartPole-v1")
    
    for episode in range(num_episodes):
        rollouts = rollout_collection(...)
        advantages = compute_advantages(...)
        update_policy(...)
        
        if episode % log_interval == 0:
            print(f"Episode {episode}: reward={...}")

if __name__ == "__main__":
    main()
```

### 6. Validate Against Source

Create a correctness checklist:

```text
VALIDATION CHECKLIST:

Shapes & Types:
  ✓ Policy input shape matches source (e.g., (batch, obs_dim))
  ✓ Action output shape matches source
  ✓ Value output is scalar per observation
  ✓ Rollout buffer shapes match expected (T, N, ...)

Learning Dynamics:
  ✓ Loss decreases over time (no NaN, no explosion)
  ✓ Learning curves smooth (not oscillating wildly)
  ✓ Convergence speed within 2x of source (wall-clock)

Final Results:
  ✓ Paper result: [metric] = [value]
  ✓ Source code result: [metric] = [value]
  ✓ Reimplement result: [metric] = [value ± 5%]

Performance:
  ✓ Wall-clock time per 1M steps: [source] → [reimplement]
  ✓ Memory usage: [source] → [reimplement]
  ✓ GPU utilization: [%]
```

## Notebook Workflow

Use a Jupyter notebook as a **three-panel comparison document**: original code → abstraction → clean reimplementation. This makes the reverse-engineering process transparent and reviewable.

### Notebook Cell Structure

Each major component gets a triplet of cells:

```
[markdown]   ### Component Name
[python]     # ── ORIGINAL ──  (source code, read-only reference)
[markdown]   **Abstraction** (pseudocode + design choices)
[python]     # ── NEW CODE ──  (clean reimplementation)
[python]     # ── SMOKE TEST ── (minimal assert / forward pass check)
```

### Example Notebook Layout

````xml
<!-- filepath: reverse_engineering.ipynb -->
<VSCode.Cell language="markdown">
# Reverse Engineering: [Paper / Repo Name]

| | Source | Reimplementation |
|---|---|---|
| Framework | TensorFlow 1.x | PyTorch |
| Style | Class-heavy | CleanRL single-file |
| Lines | ~800 | ~200 |
</VSCode.Cell>

<VSCode.Cell language="python">
# Setup — install deps for both source inspection and reimplementation
# pip install torch gymnasium
</VSCode.Cell>

<VSCode.Cell language="markdown">
## 1. Policy Network

### Original Code (source reference — do not copy)
</VSCode.Cell>

<VSCode.Cell language="python">
# ── ORIGINAL ──
# Paste or fetch the source snippet here for reference only.
# Example from openai/baselines ppo.py:
#
# class MlpPolicy(object):
#     def __init__(self, sess, ob_space, ac_space, nbatch, nsteps, reuse=False):
#         ob_shape = (nbatch,) + ob_space.shape
#         with tf.variable_scope("model", reuse=reuse):
#             X = tf.placeholder(tf.float32, ob_shape)
#             activ = tf.tanh
#             h1 = activ(fc(X, 'pi_fc1', nh=64, init_scale=np.sqrt(2)))
#             h2 = activ(fc(h1, 'pi_fc2', nh=64, init_scale=np.sqrt(2)))
#             pi = fc(h2, 'pi', ac_space.n, init_scale=0.01)
#             vf = fc(h2, 'vf', 1)[:,0]
</VSCode.Cell>

<VSCode.Cell language="markdown">
### Abstraction

```
PolicyNetwork:
  Input:  observation (batch, obs_dim)
  Layers: Linear(obs_dim→64) → Tanh → Linear(64→64) → Tanh
  Heads:
    policy → Linear(64→action_dim)   # logits
    value  → Linear(64→1)            # scalar V(s)

Critical design choices:
  - Shared trunk, split heads
  - Tanh activations (not ReLU)
  - init_scale=0.01 on policy head (small init)
  - init_scale=sqrt(2) on hidden layers
```
</VSCode.Cell>

<VSCode.Cell language="python">
# ── NEW CODE ──
import torch
import torch.nn as nn
import numpy as np

def layer_init(layer, std=np.sqrt(2), bias_const=0.0):
    nn.init.orthogonal_(layer.weight, std)
    nn.init.constant_(layer.bias, bias_const)
    return layer

class PolicyNetwork(nn.Module):
    def __init__(self, obs_dim: int, action_dim: int):
        super().__init__()
        self.trunk = nn.Sequential(
            layer_init(nn.Linear(obs_dim, 64)), nn.Tanh(),
            layer_init(nn.Linear(64, 64)),      nn.Tanh(),
        )
        self.policy_head = layer_init(nn.Linear(64, action_dim), std=0.01)
        self.value_head  = layer_init(nn.Linear(64, 1),          std=1.0)

    def forward(self, obs):
        h = self.trunk(obs)
        return self.policy_head(h), self.value_head(h).squeeze(-1)
</VSCode.Cell>

<VSCode.Cell language="python">
# ── SMOKE TEST ──
obs_dim, action_dim, batch = 8, 4, 32
net = PolicyNetwork(obs_dim, action_dim)
obs = torch.randn(batch, obs_dim)
logits, value = net(obs)
assert logits.shape == (batch, action_dim), f"bad logits shape: {logits.shape}"
assert value.shape  == (batch,),            f"bad value shape: {value.shape}"
print("✓ PolicyNetwork shapes OK")
</VSCode.Cell>

<VSCode.Cell language="markdown">
## 2. Advantage Computation

### Original Code (source reference)
</VSCode.Cell>

<VSCode.Cell language="python">
# ── ORIGINAL ──
# From source (GAE computation):
# mb_advs = np.zeros_like(mb_rewards)
# lastgaelam = 0
# for t in reversed(range(nsteps)):
#     if t == nsteps - 1:
#         nextnonterminal = 1.0 - last_dones
#         nextvalues = last_values
#     else:
#         nextnonterminal = 1.0 - mb_dones[t+1]
#         nextvalues = mb_values[t+1]
#     delta = mb_rewards[t] + gamma * nextvalues * nextnonterminal - mb_values[t]
#     mb_advs[t] = lastgaelam = delta + gamma * lam * nextnonterminal * lastgaelam
</VSCode.Cell>

<VSCode.Cell language="markdown">
### Abstraction

```
GAE(rewards, values, dones, γ, λ):
  advantages[T-1..0]:
    δ_t = r_t + γ * V(s_{t+1}) * (1-done_t) - V(s_t)
    A_t = δ_t + γλ * (1-done_t) * A_{t+1}
  returns = advantages + values
```
</VSCode.Cell>

<VSCode.Cell language="python">
# ── NEW CODE ──
def compute_gae(rewards, values, dones, gamma=0.99, lam=0.95):
    """Generalized Advantage Estimation. All inputs: (T,) tensors."""
    T = len(rewards)
    advantages = torch.zeros(T)
    last_adv = 0.0
    for t in reversed(range(T)):
        mask = 1.0 - dones[t].float()
        next_val = values[t + 1] if t < T - 1 else 0.0
        delta = rewards[t] + gamma * next_val * mask - values[t]
        advantages[t] = last_adv = delta + gamma * lam * mask * last_adv
    return advantages, advantages + values
</VSCode.Cell>

<VSCode.Cell language="python">
# ── SMOKE TEST ──
T = 10
rewards = torch.ones(T)
values  = torch.zeros(T)
dones   = torch.zeros(T)
advs, returns = compute_gae(rewards, values, dones)
assert advs.shape == (T,)
print("✓ GAE shapes OK | mean adv:", advs.mean().item())
</VSCode.Cell>

<VSCode.Cell language="markdown">
## Validation Summary

| Component | Source result | Reimplement result | Match? |
|---|---|---|---|
| PolicyNetwork forward | shape (B, A) | shape (B, A) | ✓ |
| GAE advantages | ... | ... | ✓ |
| Final reward (CartPole) | 500 | ??? | pending |
</VSCode.Cell>
````

### Rules for the Notebook

1. **Original cells are read-only references** — paste the source snippet as a comment block; never execute it directly in the notebook.
2. **One abstraction markdown cell per component** — write pseudocode and critical design choices before writing new code.
3. **Every new-code cell must be followed by a smoke-test cell** — a cheap assert that checks shapes, dtypes, or a single forward pass.
4. **Validation summary table at the end** — track which components are verified against source results.

## Output Artifacts

- `reverse_engineering.ipynb` — Three-panel notebook (original → abstraction → new code)
- `code_map.md` — Architecture analysis (data structures, algorithms, dependencies)
- `algorithm_pseudocode.md` — Abstract algorithm patterns
- `implementation_plan.md` — Step-by-step reimplementation guide
- `starter_code.py` — Template with TODOs (CleanRL style, single file)
- `validation_checklist.md` — Correctness criteria
- Optional: `REIMPLEMENT.md` — Full guide (for complex methods)

## Tech Stack Defaults

```yaml
Language: Python 3.10+
ML Framework: 
  - PyTorch (default for RL)
  - JAX (if XLA/JIT needed)
Environments:
  - gymnasium (OpenAI)
  - brax (JAX physics)
Style:
  - CleanRL (single-file, minimal)
  - No heavy abstractions
  - Type hints throughout
Dependencies:
  - Keep minimal (PyTorch + gymnasium enough for most)
Acceleration:
  - Native PyTorch ops, no custom CUDA
  - JIT compile if using JAX
Performance:
  - Profile before optimizing
  - Vectorize rollout collection
  - Batch gradient updates
```

## Guidelines

✅ **DO:**
- Extract abstract patterns (not literal code)
- Use modern, fast tech stacks by default
- Keep code simple and readable
- Match source results within 5%
- Document critical design choices
- Profile and optimize

❌ **DON'T:**
- Copy-paste source code
- Add unnecessary abstractions
- Use deprecated libraries (TF 1.x, old PyTorch)
- Skip validation against paper
- Assume understanding without analysis
- Optimize before proving correctness

## Example: Reimplementing DQN

**Source:** `openai/baselines/dqn/dqn.py` (TensorFlow 1.x)

**Target:** PyTorch + CleanRL style

**Code map:** Vectorized environments → experience replay → Q-learning update

**Abstract model:**
```
for episode:
  1. Collect transitions via ε-greedy (replay buffer)
  2. Sample mini-batch from buffer
  3. Compute Q-targets: r + γ max_a' Q(s', a')
  4. Update Q: minimize (Q(s,a) - target)^2
```

**Tech choice:** PyTorch (Q-functions fit PyTorch's imperative style)

**Validation:** Learning curve should match source within 2x steps to convergence
