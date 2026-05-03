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

## Output Artifacts

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
