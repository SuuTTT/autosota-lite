# Workflow Orchestration Guide

Combine multiple skills into automated pipelines for common research tasks.

---

## Two New Skills for Automation

### 1. `sota-workflow-orchestrator`
**Purpose:** Chain skills together into automated workflows with testing & comparison

Orchestrates end-to-end pipelines:
- Collect resources → Get baseline → Analyze code → Reimplement → Test → Notify
- Idea → References → Write outline → Write sections → Publish results

### 2. `sota-compare-metrics`
**Purpose:** Compare original vs reimplemented code across 5 dimensions

Produces:
- Formatted comparison tables
- Improvement summaries
- Detailed reports with visualizations

---

## Pre-Built Workflows

### Workflow 1: Beat SOTA Code (Speed/Memory/Readability)

**Goal:** Reimplement research code cleaner/faster, prove improvements automatically

**Pipeline:**
```
┌─────────────────────────────────────────────────────────────┐
│ 1. Collect Resources                                        │
│    Paper + Source Code + Official Results                  │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ 2. Baseline Score                                           │
│    Run original code, capture metrics                      │
│    (accuracy, speed, memory, code lines, deps)            │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ 3. Code Analysis (code-reverse-engineering)                │
│    Extract abstract model, architecture, algorithms        │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ 4. Reimplement (sota-iterate-and-improve)                  │
│    Clean, fast version using PyTorch/JAX                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ 5. Test & Compare (sota-compare-metrics)                   │
│    Run reimplemented code                                  │
│    Compare metrics: speed, memory, readability, deps       │
│    Generate comparison table + improvement summary         │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ 6. Notify (util-notifier)                                  │
│    Post results to Slack + email                           │
│    "✅ Beat SOTA: 33% faster, 25% less memory"            │
└─────────────────────────────────────────────────────────────┘

OUTPUT: comparison_report.md + code + metrics
```

**Usage:**
```bash
# Run with default settings
sotaflow run beat_sota_speed \
  --paper "https://arxiv.org/abs/1707.06347" \
  --repo "https://github.com/openai/baselines"

# Customize target metric
sotaflow run beat_sota_speed \
  --paper "..." \
  --repo "..." \
  --target memory  # or: speed, readability, deployment

# Run specific dimension
sotaflow run beat_sota_speed \
  --paper "..." \
  --repo "..." \
  --dimensions "speed,memory"
```

**Output Example:**
```
╔═══════════════════════════════════════════════════════════════╗
║  Original vs Reimplemented: PPO Comparison                  ║
╠═══════════════════════════════════════════════════════════════╣
║ Speed       │ 42.3 sec/epoch → 28.1 sec/epoch  │ +33% faster║
║ Memory      │ 2048 MB → 1536 MB                │ -25% less  ║
║ Code        │ 1850 lines → 240 lines           │ -87%       ║
║ Dependencies│ 12 packages → 3 packages         │ -75%       ║
║ Accuracy    │ 95.0% → 95.1%                    │ ✓ matched  ║
╚═══════════════════════════════════════════════════════════════╝

✅ VERDICT: Beat SOTA
Your code is faster, lighter, and cleaner while maintaining accuracy
```

### Workflow 2: Write Paper from Idea

**Goal:** From idea + reference papers to complete draft with experiments

**Pipeline:**
```
┌─────────────────────────────────────────────────────────────┐
│ 1. Ingest Idea (steer-human-ingest)                         │
│    Your idea + improvements over SOTA                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ 2. Collect Resources (sota-collect-resources)               │
│    Find reference papers + similar implementations          │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ 3. Analyze Papers (paper-reverse-engineering)               │
│    Sentence-function analysis of reference papers          │
│    Extract: writing models, structure, rhetoric             │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ 4. Write Structure                                          │
│    Create paper outline using writing models                │
│    Plan: abstract, intro, method, experiments, conclusion   │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ 5. (Optional) Implement Method (sota-iterate-and-improve)   │
│    Code your idea                                           │
│    Run experiments                                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ 6. Log Results (paper-result-logger)                        │
│    Capture metrics, results, comparisons                    │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ 7. Write Paper (paper-writer)                               │
│    Fill paper outline with your content + results           │
│    Using writing models from step 3                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ 8. Finalize & Share (util-notifier)                         │
│    Post draft + results to team                             │
└─────────────────────────────────────────────────────────────┘

OUTPUT: paper.tex or paper.md + experiment_results.csv
```

**Usage:**
```bash
sotaflow run write_paper_from_idea \
  --idea "Combine PPO with entropy regularization" \
  --references "paper1.pdf,paper2.pdf" \
  --target_venue "NeurIPS" \
  --implement true
```

**Output Example:**
```
Paper draft generated: paper.md (4000 words)
├── Abstract (200 words) ✓
├── Introduction (800 words) ✓
├── Related Work (600 words) ✓
├── Method (1200 words) ✓
├── Experiments (800 words) ✓
├── Results (300 words) ✓
├── Conclusion (100 words) ✓
└── References (automatic)

Experiment results:
├── results.csv (metrics logged)
├── figures/ (generated plots)
└── tables/ (comparison tables)

Next: Review draft, add citations, finalize
```

---

## Workflow Definition Format

Define workflows as YAML for reusability:

```yaml
# beat_sota_speed.yaml
name: "Beat SOTA Code on Speed"
description: "Reimplement research code faster, compare metrics"

metadata:
  category: "optimization"
  complexity: "medium"
  estimated_time: "2-4 hours"
  required_skills:
    - sota-collect-resources
    - code-reverse-engineering
    - sota-iterate-and-improve
    - sota-compare-metrics
    - util-notifier

config:
  paper_url: ""           # User provides
  repo_url: ""            # User provides
  env: "CartPole-v1"
  target_dimension: "speed"
  acceptable_accuracy_drop: "1%"

stages:
  - id: collect
    name: "Collect Resources"
    skill: sota-collect-resources
    timeout: 10 minutes
    
  - id: baseline
    name: "Get Baseline Score"
    skill: run-original-code
    inputs:
      code: ${collect.outputs.source_code}
      env: ${config.env}
      num_runs: 3
    capture_metrics:
      - accuracy
      - speed_per_epoch
      - memory_peak
    timeout: 1 hour
  
  - id: analyze
    name: "Reverse Engineer Code"
    skill: code-reverse-engineering
    inputs:
      source_code: ${collect.outputs.source_code}
    outputs:
      - code_map.md
      - algorithm_pseudocode.md
      - starter_code.py
    timeout: 2 hours
  
  - id: reimplement
    name: "Reimplement"
    skill: sota-iterate-and-improve
    inputs:
      template: ${analyze.outputs.starter_code}
      tech_stack: "pytorch"
      constraint: "match accuracy ±${config.acceptable_accuracy_drop}"
    outputs:
      - reimplemented_code.py
    timeout: 4 hours
  
  - id: test
    name: "Test & Compare"
    skill: sota-compare-metrics
    inputs:
      original_code: ${collect.outputs.source_code}
      original_metrics: ${baseline.outputs.metrics}
      reimplemented_code: ${reimplement.outputs.reimplemented_code}
      dimensions:
        - performance
        - speed
        - memory
        - readability
        - deployment
    outputs:
      - comparison_table.md
      - comparison_report.pdf
      - improvement_summary.txt
      - metrics.json
    timeout: 1 hour
  
  - id: notify
    name: "Notify Team"
    skill: util-notifier
    inputs:
      message: ${test.outputs.improvement_summary}
      attachment: ${test.outputs.comparison_table.md}
      channels:
        - slack: "#sota"
        - email: "team@example.com"
    timeout: 5 minutes

notifications:
  on_success:
    - channel: "slack"
      message: "✅ Beat SOTA! ${test.outputs.improvement_summary}"
  
  on_failure:
    - channel: "slack"
      message: "❌ Workflow failed at stage: ${failed_stage}"

success_criteria:
  - accuracy_preserved: ${config.acceptable_accuracy_drop}
  - speed_improved: ">=1.2x"  # must be at least 20% faster
  - code_improved: true        # fewer lines or better structure
```

---

## Customization Examples

### Example 1: Focus on Memory Efficiency

```bash
sotaflow run beat_sota_speed \
  --paper "https://arxiv.org/abs/2004.14294" \
  --repo "https://github.com/pytorch/vision" \
  --target memory \
  --max-memory "512MB"
```

Result: Optimizes for memory reduction, accuracy drop up to 2%, speed improvement secondary

### Example 2: Focus on Deployment (Minimal Dependencies)

```bash
sotaflow run beat_sota_speed \
  --paper "..." \
  --repo "..." \
  --target deployment \
  --max-deps 3
```

Result: Minimize dependencies, speed/memory improvements secondary

### Example 3: Write Paper with Implementation

```bash
sotaflow run write_paper_from_idea \
  --idea "Add dynamic network pruning to BERT" \
  --references "bert.pdf,pruning.pdf,quantization.pdf" \
  --target_venue "ACL" \
  --implement true \
  --dataset "GLUE" \
  --gpus 8
```

Result: Paper draft + experiment results on GLUE benchmark

---

## Workflow Status & Monitoring

```bash
# Check workflow status
sotaflow status beat_sota_speed

# Output:
# Stage 1/6: Collect Resources ✓ (5 min)
# Stage 2/6: Baseline Score ✓ (45 min)
# Stage 3/6: Code Analysis ✓ (90 min)
# Stage 4/6: Reimplement ⏳ (running... 120 min elapsed)
# Stage 5/6: Test & Compare ⏰
# Stage 6/6: Notify ⏰

# Watch in real-time
sotaflow watch beat_sota_speed

# Get detailed logs
sotaflow logs beat_sota_speed --stage reimplement

# Get latest metrics
sotaflow metrics beat_sota_speed
```

---

## Resume from Checkpoint

If workflow is interrupted:

```bash
# Resume from where it stopped
sotaflow resume beat_sota_speed

# Or resume from specific stage
sotaflow resume beat_sota_speed --from-stage test

# Without re-running earlier stages
sotaflow resume beat_sota_speed --skip-completed
```

---

## Integration with Existing Skills

**Workflow orchestrator calls existing skills:**

```
sota-workflow-orchestrator (coordinator)
├─ Stage 1 → sota-collect-resources
├─ Stage 2 → [custom baseline runner]
├─ Stage 3 → code-reverse-engineering
├─ Stage 4 → sota-iterate-and-improve
├─ Stage 5 → sota-compare-metrics
└─ Stage 6 → util-notifier
```

**No new implementations needed** — just chains existing skills!

---

## Benefits of Workflows

### Reproducibility
```bash
# Same workflow every time
sotaflow run beat_sota_speed --paper X --repo Y
sotaflow run beat_sota_speed --paper X --repo Y
# Same results both times
```

### Automation
```bash
# Without workflow: 5 hours, 10+ manual steps
# With workflow: 3 hours running, 1 command

sotaflow run beat_sota_speed --paper X --repo Y
# [go do other work while it runs]
# [get Slack notification when done]
```

### Comparison
```bash
# Automatic metric capture at each stage
sotaflow metrics beat_sota_speed
# Shows: baseline vs reimplemented across all dimensions
```

### Monitoring
```bash
# Check progress without interrupting
sotaflow status beat_sota_speed
# Shows: which stage running, time elapsed, ETA
```

### Documentation
```bash
# Workflow is self-documenting
sotaflow explain beat_sota_speed
# Shows: what each stage does, why it matters
```

---

## Typical Execution Timeline

### Beat SOTA Speed Workflow

```
Total: ~3 hours of execution + setup

Stage 1: Collect Resources      [5-10 min]
Stage 2: Baseline Score         [30-60 min] ← depends on dataset
Stage 3: Code Analysis          [60-90 min] ← depends on code size
Stage 4: Reimplement            [60-180 min] ← depends on method
Stage 5: Test & Compare         [30-60 min] ← depends on dataset
Stage 6: Notify                 [1-5 min]

Total: 3-7 hours (mostly waiting for training/testing)
User time: ~30 minutes (setup + reviews + decisions)
```

### Write Paper from Idea Workflow

```
Total: ~2-4 hours of execution + writing

Stage 1: Ingest Idea            [5 min]
Stage 2: Collect Resources      [10-15 min]
Stage 3: Analyze Papers         [30-45 min]
Stage 4: Write Structure        [15-20 min] ← auto-generated
Stage 5: (Optional) Implement   [2-6 hours] ← if coding
Stage 6: Log Results            [10-15 min]
Stage 7: Write Paper            [30-60 min] ← auto-drafted
Stage 8: Share                  [2-5 min]

Total: 2-10 hours (depends on implementation)
User time: ~1-2 hours (review + edit)
```

---

## What Gets Automated

**WITHOUT workflows:** Manual orchestration
```
1. Manually run skill 1 → copy output
2. Manually run skill 2 with skill 1's output
3. Manually run skill 3 with skill 2's output
...
10. Manually post results to Slack
Time: lots of manual work, error-prone
```

**WITH workflows:** One command
```
sotaflow run beat_sota_speed --paper X --repo Y

[workflow runs all steps automatically]
[captures metrics at each stage]
[posts to Slack when done]
Time: hands-off, reproducible, auditable
```

---

## Next Steps

1. **Choose a pre-built workflow** (beat_sota_speed or write_paper_from_idea)
2. **Configure parameters** (paper URL, repo URL, target, etc.)
3. **Run:** `sotaflow run workflow_name --param1 value1 --param2 value2`
4. **Monitor:** `sotaflow status workflow_name`
5. **Get results:** Check Slack notification + `sotaflow results workflow_name`
