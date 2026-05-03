# Reverse Engineering Skills

Two complementary skills for understanding and replicating research:

---

## 📄 Paper Reverse Engineering

**What:** Extract rhetorical structure and writing models from papers

**How:** Sentence-by-sentence function labeling → abstract writing patterns → apply to your own work

**Output:** Paper draft with same rhetorical structure as model papers

**Use when:** Writing your own paper in a similar field/style

```
Model Paper
    ↓
Analyze sentence functions
(FIELD_CONTEXT, LIMITATION, PURPOSE, METHOD, RESULT, etc.)
    ↓
Extract writing models
(ordered sentence-function patterns)
    ↓
Apply to your project
(fill in your method, evidence, results)
    ↓
Your Paper (same rhetoric, new content)
```

---

## 💻 Code Reverse Engineering

**What:** Extract abstract architecture and algorithms from research code

**How:** Code analysis → architecture mapping → algorithm pseudocode → clean reimplementation

**Output:** Fast, clean reimplementation (PyTorch/JAX, CleanRL style)

**Use when:** Code from paper is slow, messy, or you need to integrate/extend it

```
Source Code
    ↓
Analyze architecture
(data structures, algorithms, dependencies)
    ↓
Extract code model
(pseudocode, design choices, critical patterns)
    ↓
Design fast tech stack
(PyTorch + CleanRL by default)
    ↓
Reimplement cleanly
(match source results ±5%)
    ↓
Your Implementation (cleaner, faster)
```

---

## The Relationship

| Aspect | Paper RE | Code RE |
|--------|----------|---------|
| **Analyzes** | Papers | Source code |
| **Extracts** | Writing patterns | Algorithms & architecture |
| **Output** | Paper draft | Reimplemented code |
| **Level** | Rhetorical/content | Technical/implementation |
| **Prevents** | Plagiarism | Copy-pasting code |
| **Goal** | Good writing | Fast, clean code |

---

## Workflow Example: Improve PPO from OpenAI Baselines

### 1. Analyze Paper
```
Read: "Proximal Policy Optimization Algorithms" (Schulman et al. 2017)
Use: paper-reverse-engineering
Output: writing_model.md (how to describe your PPO variant)
```

### 2. Analyze Source Code
```
Repo: openai/baselines/ppo2
Use: code-reverse-engineering
Output: code_map.md, algorithm_pseudocode.md, starter_code.py
```

### 3. Reimplement Code
```
Tech stack: PyTorch + CleanRL
Base: starter_code.py from step 2
Add: your improvement (better exploration, different loss, etc.)
Test: match paper results ±5%
```

### 4. Write Your Paper
```
Use: paper-writer (with writing model from step 1)
Content: your method (from reimplemented code)
Results: your improvements
```

---

## Code Reverse Engineering Details

### What Gets Extracted

**Data Structures:**
```
Networks: policy (action logits), value (state value)
Buffers: rollout storage (obs, action, reward, done, value, log_prob)
Shapes: how data flows through the system
```

**Algorithms:**
```
1. Rollout collection (N envs × T steps)
2. Advantage estimation (GAE or bootstrap)
3. Loss computation (policy + value + entropy)
4. Gradient update (mini-batch SGD)
```

**Design Choices:**
```
- Vectorized or serial rollout collection?
- On-policy or off-policy?
- How is batching done?
- What's the critical bottleneck?
```

### Why Abstract Models Matter

```
❌ BAD: Copy-paste source code
    Pro: works immediately
    Con: hard to understand, hard to modify, slow, dependencies

✅ GOOD: Extract abstract model
    Pro: understand how it works, fast reimplementation, easy to extend
    Con: takes effort upfront (but pays off)
```

### Tech Stack Steering (Default: Fast)

**By speed (fast → slower):**
1. **JAX** — JIT + XLA compilation, multi-GPU trivial
2. **PyTorch** — Native GPU ops, fast iteration
3. **TensorFlow 2.x** — Good but heavier
4. **TensorFlow 1.x** — Slow, deprecated (avoid)

**CleanRL Style Defaults:**
- Single file or minimal modules
- No heavy abstractions
- PyTorch + gymnasium
- Vectorized rollout collection
- Type hints + docstrings

---

## Example Output Structure

```
code-reverse-engineering/
├── code_map.md              (architecture analysis)
├── algorithm_pseudocode.md  (abstract algorithms)
├── implementation_plan.md   (step-by-step guide)
├── starter_code.py          (CleanRL template)
├── validation_checklist.md  (correctness criteria)
└── REIMPLEMENT.md           (full guide for complex methods)
```

---

## Validation Checklist

After reimplementation, verify:

```
Correctness:
  ✓ Shapes match source
  ✓ Learning curves similar
  ✓ Final results ±5% of source

Performance:
  ✓ Wall-clock time comparable or faster
  ✓ Memory usage acceptable
  ✓ GPU utilization >80%

Code Quality:
  ✓ Single file or minimal modules
  ✓ No unnecessary abstractions
  ✓ Type hints throughout
  ✓ Can be easily extended
```

---

## When to Use Code RE

**Use code-reverse-engineering when:**
- Source code is available but messy
- You want a clean reference implementation
- You need to integrate the method into your system
- You plan to extend or improve the method
- Paper results are reproducible but code is slow

**Don't use when:**
- You just need to run their code once
- Source code is already clean and well-documented
- You're not modifying the algorithm

---

## Default Tech Stack

```python
# Imports (typical reimplementation)
import jax
import jax.numpy as jnp
import gymnasium as gym
from flax import linen as nn
import optax

# Or PyTorch
import torch
import torch.nn as nn
from torch.optim import Adam

# Structure (CleanRL style)
# - Single file or minimal modules
# - Classes: PolicyNetwork, ValueNetwork
# - Functions: rollout_collection, update_policy, main
# - No heavy frameworks (no Ray, no Stable-Baselines abstractions)
```

---

## Comparison: Paper-RE vs Code-RE

**Paper Reverse Engineering:**
```
Hilary Glasman-Deal approach
Extract: sentence function labels
Build: writing models (FIELD_CONTEXT, LIMITATION, PURPOSE, etc.)
Apply: to your own writing
Output: Paper with matching rhetoric
```

**Code Reverse Engineering:**
```
Software engineering approach
Extract: architecture, algorithms, data flow
Build: code models (pseudocode, patterns)
Apply: to fast reimplementation
Output: Clean, fast code matching source results
```

**Both share:**
- ✓ Extract abstract patterns (not literal copies)
- ✓ Map to your context (paper or code)
- ✓ Validate against source (no plagiarism, matching results)
- ✓ Document the process
