# Code Reverse Engineering - Integration Guide

## Overview

`code-reverse-engineering` is a new skill for understanding and reimplementing research code from other repositories with clean, fast tech stacks (PyTorch/JAX, CleanRL style).

**Status:** Ready to use  
**Complements:** `paper-reverse-engineering` (writing), `optimize-reimplementation` (general optimization)  
**Category:** OPTIMIZATION (research code analysis & clean reimplementation)

---

## Design Philosophy

### The Problem with Research Code

Research code from papers often:
- ❌ Uses deprecated libraries (TensorFlow 1.x)
- ❌ Evolves ad-hoc without clear structure
- ❌ Is slow and memory-inefficient
- ❌ Hard to modify or extend
- ❌ Tight coupling between components

### The Solution: Abstract Models

Instead of copy-pasting code, extract the **abstract model**:

1. **Understand:** Read source code to extract architecture, algorithms, design choices
2. **Abstract:** Write pseudocode, create architecture diagrams, identify critical patterns
3. **Reimplement:** Clean, fast version using modern tech stack
4. **Validate:** Match source results within 5%

**Key benefit:** You understand HOW it works, not just WHAT it does.

---

## Relationship to Other Skills

### With `paper-reverse-engineering`

Both use the same "extract abstract patterns" approach but at different levels:

```
PAPER REVERSE ENGINEERING          CODE REVERSE ENGINEERING
├─ Level: Rhetorical               ├─ Level: Technical
├─ Input: Papers                   ├─ Input: Source code
├─ Extract: Sentence functions     ├─ Extract: Algorithms
├─ Output: Writing models          ├─ Output: Code architecture
├─ Goal: Good writing              ├─ Goal: Fast code
└─ Prevents: Plagiarism            └─ Prevents: Copy-pasting
```

**Typical workflow:**
1. `paper-reverse-engineering` — Understand HOW the paper is written
2. `code-reverse-engineering` — Understand HOW the code works
3. Add your improvements to the reimplemented code
4. Use `paper-writer` with your results

### With `optimize-reimplementation`

- **`code-reverse-engineering`:** Initial clean reimplementation from research code
- **`optimize-reimplementation`:** Further optimization of the reimplemented code

Think of it as:
1. Clean reimplementation (code-RE) → matches source results
2. Further optimization (optimize-RE) → faster/better than source

---

## When to Use

### Use `code-reverse-engineering` when:

✅ Source code is available but:
- Messy or hard to understand
- Slow or memory-inefficient
- Uses deprecated libraries
- Hard to modify or integrate

✅ You want to:
- Clean reimplementation as reference
- Integrate method into your pipeline
- Extend or improve the method
- Publish alongside your extension

### Don't use when:

❌ Source code is already:
- Well-documented and clean
- Fast enough for your use
- Your only goal is to run it once

❌ You plan to:
- Just use their pretrained model
- Only read their code (not modify)

---

## Methodology

### Step 1: Analyze Source Code Architecture

Read the code to extract abstract structure (not to copy it).

**Extract:**
- Data structures (network architectures, buffers, shapes)
- Algorithms (training loop, updates, sampling)
- Dependencies (libraries, critical APIs)
- Design patterns (OO vs functional, vectorized vs serial)

**Output:** `code_map.md`

### Step 2: Abstract the Code Model

Create reusable algorithm patterns using pseudocode and math.

**Extract:**
- High-level algorithm (pseudocode)
- Critical design choices (table: on-policy vs off-policy, etc.)
- Key patterns (what makes this work?)

**Output:** `algorithm_pseudocode.md`

### Step 3: Choose Tech Stack

Default: **PyTorch + CleanRL style** (single file, minimal abstractions)

Alternative options:
- JAX (if XLA/JIT needed)
- Stable-Baselines3 (if maturity needed)
- Ray RLlib (if distributed training needed)

**Reasoning:** PyTorch + CleanRL is fastest to develop, easiest to understand, easiest to modify.

**Output:** Tech stack choice with reasoning

### Step 4: Build Implementation Plan

Phased approach from abstract to concrete:

1. **Phase 1: Data Flow** — Shapes and types (no learning)
2. **Phase 2: Core Algorithm** — Single gradient step
3. **Phase 3: Learning** — One mini-batch training
4. **Phase 4: Integration** — One full episode
5. **Phase 5: Full Training** — Validate on actual task
6. **Phase 6: Optimization** — Performance tweaks

**Output:** `implementation_plan.md`

### Step 5: Create Code Template

CleanRL-style starter code with TODOs for custom logic.

```python
# Typical structure
class PolicyNetwork(nn.Module):
    """TODO: match source architecture"""
    pass

class ValueNetwork(nn.Module):
    """TODO: match source architecture"""
    pass

def rollout_collection(env, policy):
    """TODO: match source rollout collection"""
    pass

def update_policy(policy, value, rollouts):
    """TODO: implement source loss computation"""
    pass

def main():
    """TODO: main training loop"""
    pass
```

**Output:** `starter_code.py`

### Step 6: Validate Against Source

Correctness checklist:

```
Shapes & Types:
  ✓ Policy input/output shapes match
  ✓ Value output is scalar
  ✓ Rollout buffer shapes match

Learning:
  ✓ Loss decreases (no NaN/explosion)
  ✓ Learning curves similar
  ✓ Convergence speed within 2x

Results:
  ✓ Paper result: [value]
  ✓ Source code: [value]
  ✓ Reimplement: [value ± 5%]

Performance:
  ✓ Wall-clock time: [source] → [reimplement]
  ✓ Memory: [source] → [reimplement]
  ✓ GPU util: >80%
```

**Output:** `validation_checklist.md`

---

## Output Artifacts

```
code-reverse-engineering/
├── code_map.md                  # Architecture analysis
├── algorithm_pseudocode.md      # Algorithm patterns
├── implementation_plan.md       # Step-by-step guide
├── tech_stack_rationale.md      # Why PyTorch? Why CleanRL?
├── starter_code.py              # Template with TODOs
├── validation_checklist.md      # Correctness criteria
└── (optional) REIMPLEMENT.md    # Full guide for complex methods
```

---

## Default Tech Stack

### Primary: PyTorch + CleanRL

```python
import torch
import torch.nn as nn
from torch.optim import Adam
import gymnasium as gym

# Single file or minimal modules
# Vectorized rollout collection
# Type hints throughout
# No heavy abstractions
```

**Why PyTorch + CleanRL?**
- Fast iteration (easier to modify)
- Clean, readable code
- Minimal dependencies
- Good documentation
- Active community

### Alternative: JAX

```python
import jax
import jax.numpy as jnp
from flax import linen as nn
import optax
import gymnasium as gym

# Functional programming style
# JIT compilation for speed
# Multi-GPU/TPU via pmap
```

**Why JAX?**
- Faster execution (XLA compilation)
- Multi-GPU/TPU trivial
- Functional style (easier to reason about)

---

## Critical Patterns to Extract

**For RL algorithms:**
- Rollout collection (vectorized? async? serial?)
- Advantage estimation (GAE? bootstrapped? returns?)
- Loss computation (policy gradient? clipping? trust region?)
- Network architecture (shared? separate policy/value?)
- Exploration (entropy bonus? random actions? softmax?)

**For supervised learning:**
- Batch creation (random sampling? sequential?)
- Data augmentation (what types?)
- Loss computation (what formulation?)
- Regularization (L2? dropout? batch norm?)
- Learning rate schedule (constant? decay?)

**For generative models:**
- Forward/reverse process (parameterization?)
- Sampling strategy (temperature? top-k? nucleus?)
- Training objective (loss formulation?)
- Architecture (diffusion? VAE? GAN?)

---

## Example: PPO Reimplementation

### Source
```
Paper: "Proximal Policy Optimization Algorithms" (Schulman et al., 2017)
Code: openai/baselines/ppo2 (TensorFlow 1.x, slow)
```

### Output Artifacts

**code_map.md:**
```
Data Structures:
  - Policy: (obs_dim) -> logits[action_dim]
  - Value: (obs_dim) -> scalar
  - Rollout: (obs, action, reward, done, value, log_prob)

Algorithms:
  1. Collect rollouts: N parallel envs × T steps
  2. Compute advantages: GAE with γ=0.99, λ=0.95
  3. Update: mini-batch SGD with clipping

Design Choices:
  - Vectorized rollout collection (4-16 parallel)
  - On-policy, single GPU
  - Synchronous updates
```

**algorithm_pseudocode.md:**
```
for episode:
  1. Collect rollouts via ε-greedy
  2. Compute advantages: a = returns - values
  3. Update:
     loss = -log_prob * clipped_advantage + value_loss
     gradient_step(loss)
```

**starter_code.py:**
```python
class PPO:
    def __init__(self, env, ...):
        self.policy = PolicyNetwork()
        self.value = ValueNetwork()
    
    def collect_rollouts(self, num_steps):
        # TODO: implement vectorized rollout
        pass
    
    def compute_advantages(self, rollouts):
        # TODO: GAE advantage estimation
        pass
    
    def update(self, rollouts):
        # TODO: mini-batch policy update
        pass
    
    def train(self, num_episodes):
        for episode in range(num_episodes):
            rollouts = self.collect_rollouts(2048)
            self.update(rollouts)
```

---

## Integration into AutoSOTA Workflow

### Complete Improvement Loop

```
1. sota-collect-resources
   Find paper + source code

2. paper-reverse-engineering
   Analyze writing style of similar papers

3. code-reverse-engineering
   ← YOU ARE HERE
   Understand + reimplement source code cleanly

4. sota-idea-generator
   Generate improvement ideas

5. sota-iterate-and-improve
   Implement improvements

6. paper-result-logger
   Log experiment results

7. paper-writer
   Write your paper using learned writing style

8. util-notifier
   Share results
```

---

## Success Criteria

Your code-reverse-engineering is successful when:

✅ **Correctness**
- Results match source ±5%
- Learning curves similar
- All unit tests pass

✅ **Speed**
- Wall-clock time comparable or faster
- Memory usage acceptable
- GPU utilization >80%

✅ **Clarity**
- Code is self-documenting
- No unnecessary abstractions
- Easy to modify

✅ **Maintainability**
- Single file or minimal modules
- Type hints throughout
- Clear separation of concerns

---

## Comparison: When to Use Which

| Task | Skill |
|------|-------|
| Understand paper's writing | `paper-reverse-engineering` |
| Understand source code architecture | `code-reverse-engineering` |
| Optimize already-working code | `optimize-reimplementation` |
| Write paper sections | `paper-writer` |
| Log experiment results | `paper-result-logger` |

---

## Troubleshooting

**"My reimplementation doesn't match source results"**
- Check shapes (print data at each step)
- Verify hyperparameters (learning rate, batch size)
- Check random seed reproducibility
- Compare loss values at each step

**"My code is slower than source"**
- Profile first (identify bottleneck)
- Consider JAX (XLA compilation)
- Vectorize rollout collection
- Use native PyTorch ops (no custom loops)

**"I'm copying code from source"**
- Step back → re-analyze abstract model
- Write pseudocode → implement from scratch
- Don't look at source while coding
- Reference abstract model, not source code

---

## Next Steps

1. **Read** `SKILL.md` (complete methodology)
2. **Choose** your target paper/code
3. **Follow** the 6-step workflow
4. **Produce** the output artifacts
5. **Validate** against source
6. **Extend** with your improvements

---

## Questions?

See `SKILL.md` for detailed workflow, or refer to `REVERSE_ENGINEERING_GUIDE.md` for comparison with paper-reverse-engineering.
