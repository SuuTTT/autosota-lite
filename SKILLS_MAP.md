# AutoSOTA Skills Map

Skill organization by purpose. **Find your paper's skills in seconds.**

---

## 🎯 SOTA Enhancement (Core Loop)

**Goal:** Collect resources → Reproduce → Try ideas → Iterate & improve

| Skill | Purpose |
|-------|---------|
| `sota-collect-resources` | Find papers, datasets, code |
| `sota-reproduce-and-iterate` | Run existing code, test locally |
| `sota-idea-generator` | Generate new ideas from papers |
| `sota-iterate-and-improve` | Fix bugs, improve code |
| `sota-optimize-iteration` | Speed up training/experiments |

**When to use:**
- Running a paper locally? → `sota-reproduce-and-iterate`
- Improving results? → `sota-iterate-and-improve`
- Code too slow? → `sota-optimize-iteration`

---

## 🧠 Steering (Human Guidance)

**Goal:** Apply human expertise to guide iterations

| Skill | Purpose |
|-------|---------|
| `steer-human-ingest` | Incorporate human feedback |
| `steer-structural-entropy` | Use structural ideas to improve |

**When to use:**
- Have an idea? → `steer-human-ingest`
- Want to try a novel structural change? → `steer-structural-entropy`

---

## 📄 Paper (Writing & Results)

**Goal:** Document findings, write paper, represent results

| Skill | Purpose |
|-------|---------|
| `paper-writer` | Write paper sections |
| `paper-reverse-engineering` | Analyze paper methods & results (rhetorical) |
| `code-reverse-engineering` | Analyze & reimplement research code (architectural) |
| `paper-result-logger` | Log experiment results |
| `paper-result-aggregator` | Summarize & compare results |

**When to use:**
- Writing methods? → `paper-writer`
- Analyzing a paper's approach? → `paper-reverse-engineering`
- Reimplementing code cleanly? → `code-reverse-engineering`
- Recording experiment metrics? → `paper-result-logger`
- Creating result tables? → `paper-result-aggregator`

---

## ⚡ Optimization (Accelerate Iteration)

**Goal:** Speed up development cycle + automated workflows

| Skill | Purpose |
|-------|---------|
| `sota-workflow-orchestrator` | **[NEW]** Orchestrate multi-skill workflows with testing & comparison |
| `sota-compare-metrics` | **[NEW]** Compare original vs reimplemented across all dimensions |
| `optimize-reimplementation` | Reimplement code faster |

**When to use:**
- Want automated end-to-end pipeline? → `sota-workflow-orchestrator`
- Need to compare metrics? → `sota-compare-metrics`
- Further optimization after reimplementation? → `optimize-reimplementation`

---

## 🔧 Utility (Infrastructure Support)

**Goal:** Handle scheduling, logging, cost, monitoring

| Skill | Purpose |
|-------|---------|
| `util-key-manager` | Manage API credentials securely |
| `util-notifier` | Send notifications (Slack, email, WandB) |
| `util-publisher` | Publish results & papers |
| `util-gpu-scheduler` | Rent GPUs on Vast.ai |
| `util-cost-estimator` | Estimate compute costs |
| `util-monitor` | Monitor runs & logs |
| `util-monitor-scheduler` | Schedule monitoring |
| `util-init-fix` | Initialize system & fix issues |
| `util-supervisor` | Oversee multiple runs |
| `util-scheduler` | Schedule tasks |
| `util-objective` | Define optimization objectives |
| `util-rl-section` | Generate RL experiment sections |

**When to use:**
- Set up credentials? → `util-key-manager`
- Post results to Slack? → `util-notifier`
- Need GPUs? → `util-gpu-scheduler`
- Track costs? → `util-cost-estimator`

---

## 🔍 Quick Lookup by Task

**I want to...**

| Task | Skill |
|------|-------|
| Find papers & datasets | `sota-collect-resources` |
| Run code from a paper | `sota-reproduce-and-iterate` |
| Get new ideas | `sota-idea-generator` |
| Fix bugs in my code | `sota-iterate-and-improve` |
| Speed up training | `sota-optimize-iteration` |
| Use my insight to improve | `steer-human-ingest` |
| Try a new structural idea | `steer-structural-entropy` |
| Write paper sections | `paper-writer` |
| Understand paper methods | `paper-reverse-engineering` |
| **Reimplement code cleanly** | **`code-reverse-engineering`** |
| Log experiment results | `paper-result-logger` |
| Compare all results | `paper-result-aggregator` |
| Make code faster | `optimize-reimplementation` |
| Manage API keys safely | `util-key-manager` |
| Notify team on Slack | `util-notifier` |
| Publish results | `util-publisher` |
| Rent GPUs | `util-gpu-scheduler` |
| Estimate compute cost | `util-cost-estimator` |
| Watch my runs | `util-monitor` |

---

## Skill Prefixes

```
sota-*          AutoSOTA core (reproduce, improve, iterate)
steer-*         Human steering & guidance
paper-*         Writing, analysis, results
optimize-*      Code & iteration optimization
util-*          Infrastructure & utilities
```

**To find a skill:** Look for the prefix that matches your task category.

---

## Example Workflows

### "Beat SOTA Code (Automated End-to-End)"
**Use:** `sota-workflow-orchestrator` with "beat_sota_speed" template
```
1. Collect resources (paper + code)
2. Capture baseline metrics
3. Reverse engineer code
4. Reimplement (faster/cleaner)
5. Compare metrics (original vs reimplemented)
6. Notify via Slack
✓ Fully automated with one command
```

### "Improve SOTA on image classification"
1. `sota-collect-resources` — Find baseline papers
2. `sota-reproduce-and-iterate` — Get baseline working
3. `sota-idea-generator` → `steer-human-ingest` — Brainstorm improvements
4. `sota-iterate-and-improve` — Implement changes
5. `sota-optimize-iteration` — Speed up training
6. `sota-compare-metrics` — Compare vs original (if reimplemented)
7. `paper-result-logger` → `paper-result-aggregator` — Track results
8. `paper-writer` — Write findings
9. `util-notifier` — Post to Slack

### "Accelerate a slow training loop"
1. `sota-optimize-iteration` — Profile & optimize
2. `optimize-reimplementation` — Rewrite slow parts
3. `sota-compare-metrics` — Prove speedup
4. `util-gpu-scheduler` — Add more GPUs if needed
5. `paper-result-logger` — Track speedup

### "Analyze and extend a paper"
1. `paper-reverse-engineering` — Understand paper approach
2. `code-reverse-engineering` — Clean reimplement of source code
3. `sota-collect-resources` — Find related work
4. `steer-structural-entropy` — Design modifications
5. `sota-iterate-and-improve` — Implement improvements
6. `sota-compare-metrics` — Compare vs original
7. `paper-writer` — Document extension
8. `util-notifier` — Share results

### "Write Paper from Idea (Automated)"
**Use:** `sota-workflow-orchestrator` with "write_paper_from_idea" template
```
1. Ingest your idea
2. Collect reference papers
3. Analyze writing style
4. (Optional) Implement your method
5. Log experiment results
6. Write paper draft (auto-structured)
7. Notify team
✓ Paper draft + experiment results in one workflow
```

---

## Location

All skills: `/workspace/autosota-lite/plugins/autosota-lite/skills/`

**Example:**
```bash
ls /workspace/autosota-lite/plugins/autosota-lite/skills/sota-*
ls /workspace/autosota-lite/plugins/autosota-lite/skills/paper-*
```
