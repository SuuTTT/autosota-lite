---
name: sota-workflow-orchestrator
description: Orchestrate multi-skill workflows for SOTA improvements and paper writing. Automate end-to-end pipelines with testing, comparison, and notifications.
---

# SOTA Workflow Orchestrator

Use this skill to orchestrate complex workflows combining multiple skills. Automate end-to-end pipelines for:
- **Beat SOTA:** Reimplement code cleaner/faster and prove improvements
- **Write Papers:** From idea + references to complete draft with results

## Core Concept

**Workflow = orchestrated chain of skills + checkpoints + comparisons + notifications**

Instead of running skills manually one-by-one, define a workflow once and automate the entire pipeline.

---

## Pre-Built Workflows

### 1. Beat SOTA (Code Performance/Efficiency/Readability)

**Goal:** Improve upon published code in 3 dimensions: performance, efficiency (memory/speed), or readability (deployment complexity)

**Pipeline:**
```
1. sota-collect-resources
   Find paper + source code + official results
   
2. Baseline Score
   Run original code, capture metrics
   (speed, memory, accuracy, loss curve)
   
3. code-reverse-engineering
   Analyze code, extract abstract model
   
4. sota-iterate-and-improve (reimplement)
   Implement with:
   - Better tech stack (PyTorch vs TensorFlow)
   - Faster algorithms (vectorization)
   - Cleaner code (single file vs modules)
   - Better deployment (minimal deps)
   
5. Comparison Test
   Run reimplementation, capture metrics
   Compare vs original:
   - Performance (accuracy, loss)
   - Speed (wall-clock time per epoch)
   - Memory (peak memory usage)
   - Readability (code size, complexity)
   - Deployment (dependencies count)
   
6. util-notifier
   Post results to Slack + email
   Format: comparison table + metrics
   
Output: Improved code + comparison report
```

**Metrics to track:**

```yaml
Performance:
  - Final accuracy/loss (must match ±5%)
  - Convergence speed (steps to target)
  - Best-epoch plateau

Efficiency:
  - Wall-clock time per epoch
  - Memory usage (peak, avg)
  - GPU utilization
  - Throughput (samples/sec)

Readability:
  - Code lines (source vs reimplemented)
  - Cyclomatic complexity
  - Type hints coverage
  - Documentation

Deployment:
  - Dependency count
  - Library versions
  - Install size
  - Inference latency
```

### 2. Write Paper from Idea

**Goal:** From initial idea + reference papers to complete paper draft with experiments (+ auto-publish to Overleaf + blog)

**Pipeline:**
```
1. steer-human-ingest
   Input: your idea + improvements over SOTA
   
2. sota-collect-resources
   Find similar papers, baseline implementations
   
3. paper-reverse-engineering
   Analyze writing style of reference papers
   Extract: sentence-function models, structure
   
4. Write Structure
   Create outline + evidence map
   
5. sota-iterate-and-improve (optional)
   If implementing new idea, code it up
   
6. paper-result-logger
   Log experiments + results
   
7. paper-writer
   Draft complete paper using:
   - Writing models from step 3
   - Your method from step 5
   - Results from step 6
   
8. Comparison Analysis
   Compare your results vs baselines
   Create result tables + figures
   
9. (NEW) Publish to Overleaf
   Auto-create Overleaf project
   Upload LaTeX + figures
   Generate shareable link
   
10. (NEW) Publish to Blog
    Auto-create blog post announcement
    Push to GitHub blog with KaTeX formulas
    Link to Overleaf project
   
11. util-notifier
    Post draft + Overleaf link + blog link to Slack
   
Output: Paper draft + Overleaf project + blog post + experiment results
```

**Outputs:**
- `paper_outline.md` (structure)
- `writing_models.md` (rhetorical patterns)
- `experiment_results.md` (metrics, tables)
- `main.tex` or `paper.md` (draft)

---

## Workflow Definition Format

Define workflows as simple YAML:

```yaml
name: Beat SOTA Code
description: Reimplement code cleaner/faster, compare metrics

stages:
  - name: "Collect Resources"
    skill: sota-collect-resources
    inputs:
      paper_url: ${PAPER_URL}
      repo_url: ${REPO_URL}
    outputs:
      - paper_pdf
      - source_code
      - official_results

  - name: "Baseline Score"
    skill: custom-baseline-test
    inputs:
      source_code: ${stages.1.outputs.source_code}
    outputs:
      - baseline_metrics
      - baseline_logs
    capture_metrics:
      - accuracy
      - speed_per_epoch
      - memory_peak
      - gpu_utilization

  - name: "Code Analysis"
    skill: code-reverse-engineering
    inputs:
      source_code: ${stages.1.outputs.source_code}
      paper_pdf: ${stages.1.outputs.paper_pdf}
    outputs:
      - code_map
      - algorithm_pseudocode
      - implementation_plan

  - name: "Reimplement"
    skill: sota-iterate-and-improve
    inputs:
      implementation_plan: ${stages.3.outputs.implementation_plan}
      starter_code: ${stages.3.outputs.starter_code}
    outputs:
      - reimplemented_code

  - name: "Test & Compare"
    skill: sota-compare-metrics
    inputs:
      original_code: ${stages.1.outputs.source_code}
      original_metrics: ${stages.2.outputs.baseline_metrics}
      new_code: ${stages.4.outputs.reimplemented_code}
    outputs:
      - comparison_table
      - comparison_report
      - improvement_summary
    metrics:
      - accuracy_diff
      - speed_improvement
      - memory_reduction
      - code_quality_score

  - name: "Publish Blog Announcement"
    skill: util-github-git-push
    inputs:
      title: "Beat SOTA: {{project_name}} Reimplementation"
      content: |
        {{comparison_summary}}
        
        **Results:**
        - Speed: {{speed_improvement}}% faster
        - Memory: {{memory_reduction}}% less
        - Code: {{code_quality_improvement}}
        
        See [full comparison]({{comparison_report_link}})
      tags: ["sota", "optimization", "{{target_dimension}}"]
      github_token: ${secrets.GITHUB_TOKEN}
      description: "Beat SOTA on {{target_dimension}}: {{improvement_summary}}"
    timeout: 5 minutes
  
  - name: "Notify"
    skill: util-notifier
    inputs:
      message: ${stages.publish_blog.outputs.message}
      channels:
        - slack: "#sota-improvements"
        - email: "team@example.com"
      attachments:
        - ${stages.test.outputs.comparison_table}
        - ${stages.publish_blog.outputs.blog_url}
```

---

## Auto-Publishing to GitHub & Overleaf

### New Skill: util-github-git-push

The workflow orchestrator now includes automatic publishing:

**Publish to GitHub Blog:**
```yaml
- id: publish_blog
  name: "Publish to Blog"
  skill: util-github-git-push
  action: publish_blog_post
  inputs:
    title: ${stage_write.outputs.paper_title}
    content: ${stage_write.outputs.blog_markdown}
    tags: ["paper", "research", "${venue}"]
    github_token: ${secrets.GITHUB_TOKEN}
    blog_repo: "https://github.com/SuuTTT/suuttt.github.io.git"
    description: "Paper draft with KaTeX formulas and results"
  outputs:
    - blog_url
    - commit_hash
  timeout: 5 minutes
```

**Publish to Overleaf:**
```yaml
- id: publish_overleaf
  name: "Publish to Overleaf"
  skill: util-github-git-push
  action: publish_paper_to_overleaf
  inputs:
    title: ${stage_write.outputs.paper_title}
    content: ${stage_write.outputs.paper_latex}
    overleaf_token: ${secrets.OVERLEAF_API_TOKEN}
    paper_type: "arxiv"  # or "conference", "workshop"
  outputs:
    - overleaf_project_id
    - overleaf_project_url
  timeout: 5 minutes
```

---

## Key Features

### 1. Checkpoint System

Stop/resume at any stage:

```yaml
workflow.run(
  checkpoint="test_and_compare",  # resume from this stage
  skip_completed=True              # don't re-run earlier stages
)
```

### 2. Metrics Capture

Automatically capture metrics at each stage:

```python
workflow.metrics
# Returns:
{
  "baseline": {
    "accuracy": 0.95,
    "speed": 42.3,      # seconds per epoch
    "memory": 2048,     # MB
  },
  "reimplemented": {
    "accuracy": 0.951,
    "speed": 28.1,      # 33% faster
    "memory": 1536,     # 25% less
  },
  "improvement": {
    "accuracy": +0.1%,
    "speed": +33%,
    "memory": -25%,
  }
}
```

### 3. Comparison Framework

Built-in comparison between original vs reimplemented:

```python
comparison = workflow.compare(
  dimensions=["performance", "speed", "memory", "readability"],
  format="table"
)
```

Output:
```
╔═══════════════════════════════════════════════════════════╗
║          Original vs Reimplemented Comparison            ║
╠═══════════════════════════════════════════════════════════╣
║ Metric           │ Original  │ Reimplemented │ Improvement║
╠═══════════════════════════════════════════════════════════╣
║ Accuracy         │ 95.0%     │ 95.1%         │ +0.1%     ║
║ Speed (sec/ep)   │ 42.3      │ 28.1          │ +33%      ║
║ Memory (MB)      │ 2048      │ 1536          │ -25%      ║
║ Code Lines       │ 1850      │ 240           │ -87%      ║
║ Dependencies     │ 12        │ 3             │ -75%      ║
╚═══════════════════════════════════════════════════════════╝
```

### 4. Flexible Notifications

Notify at multiple points:

```yaml
notifications:
  - on_stage_complete:
      stage: "Baseline Score"
      send_to: ["slack"]
      message: "Baseline captured: {{baseline_metrics}}"
  
  - on_stage_complete:
      stage: "Reimplement"
      send_to: ["slack"]
      message: "Code reimplemented, starting tests..."
  
  - on_workflow_complete:
      send_to: ["slack", "email"]
      message: "✅ Beat SOTA!\n{{improvement_summary}}"
      attach: ["comparison_table.md", "comparison_report.pdf"]
```

---

## Use Cases

### Case 1: Beat SOTA on Speed

You want to reimplement a slow research algorithm in PyTorch.

```python
workflow = WorkflowOrchestrator("beat_sota_speed")
workflow.configure({
    "paper_url": "https://arxiv.org/abs/1234.5678",
    "repo_url": "https://github.com/author/repo",
    "target": "speed",  # optimize for wall-clock time
    "acceptable_accuracy_drop": 0.5,  # within 0.5% is OK
})
workflow.run()
# Output: "Reimplemented code 3.2x faster while maintaining accuracy"
```

### Case 2: Beat SOTA on Memory

Small model for deployment.

```python
workflow = WorkflowOrchestrator("beat_sota_efficiency")
workflow.configure({
    "target": "memory",
    "deployment_env": "mobile",  # minimize size
    "constraint": "must fit in 100MB",
})
workflow.run()
# Output: "Model compressed to 42MB, 2.4x reduction"
```

### Case 3: Beat SOTA on Readability

Clean code that's easy to extend.

```python
workflow = WorkflowOrchestrator("beat_sota_readability")
workflow.configure({
    "target": "readability",
    "metrics": [
        "lines_of_code",
        "type_hints_coverage",
        "cyclomatic_complexity",
        "dependencies_count"
    ]
})
workflow.run()
# Output: "Reduced code by 87%, added type hints, 3 deps vs 12"
```

### Case 4: Write Paper from Idea (with Auto-Publishing)

Start with idea, end with published paper (Overleaf + blog).

```python
workflow = WorkflowOrchestrator("write_paper_from_idea")
workflow.configure({
    "idea": "Combine PPO with entropy regularization for better exploration",
    "reference_papers": [
        "https://arxiv.org/abs/1707.06347",  # PPO
        "https://arxiv.org/abs/1805.00909",  # Maximum Entropy RL
    ],
    "target_venue": "NeurIPS",
    "implement_method": True,  # code it up
    "publish_to_overleaf": True,  # NEW: auto-create Overleaf project
    "publish_to_blog": True,      # NEW: auto-push to GitHub blog
})
workflow.run()
# Output: paper draft + Overleaf project + blog post + Slack notification
```

**Workflow auto-publishes:**
1. ✅ Paper draft to Overleaf (LaTeX format)
2. ✅ Blog announcement to GitHub with KaTeX formulas
3. ✅ Slack notification with links to both

**Links sent to Slack:**
```
📄 New Paper: "Combine PPO with Entropy Regularization"
  
Overleaf:    https://www.overleaf.com/project/abcd1234
Blog:        https://sudingli.com/posts/2026-05-03-combine-ppo-entropy
GitHub:      https://github.com/SuuTTT/suuttt.github.io/blob/master/content/projects/2026-05-03-...md
```

---

## Output Artifacts

### After Beat SOTA workflow:

```
sota_workflow_results/
├── comparison_report.md          # formatted comparison
├── comparison_table.csv          # metrics in CSV
├── metrics.json                  # all numbers
├── original_code/                # from collected resources
├── reimplemented_code.py         # your clean version
├── baseline_logs/                # original run logs
├── reimplement_logs/             # your run logs
├── improvement_summary.txt       # one-page summary
└── notification.md               # what was sent to Slack
```

### After Write Paper workflow:

```
paper_workflow_results/
├── paper.tex or paper.md         # complete draft
├── paper_outline.md              # structure
├── writing_models.md             # rhetorical analysis
├── evidence_map.md               # what evidence is used
├── experiments/
│   ├── results.csv
│   ├── figures/
│   └── tables.md
├── references.bib
└── notification.md               # Slack update
```

---

## Workflow Status & Monitoring

Monitor workflow progress:

```python
workflow = WorkflowOrchestrator("beat_sota_speed")
workflow.run(monitor=True)

# During execution:
workflow.status()
# Output:
# Stage 1/6: Collect Resources ✓
# Stage 2/6: Baseline Score ⏳ (running...)
# Stage 3/6: Code Analysis ⏳
# Stage 4/6: Reimplement ⏰
# Stage 5/6: Test & Compare ⏰
# Stage 6/6: Notify ⏰
```

Resume if interrupted:

```python
workflow.resume()
# Continues from where it stopped
```

---

## Integration with Existing Skills

Each workflow stage calls an existing skill:

```
sota-workflow-orchestrator (COORDINATOR)
├─ stage 1 ──→ sota-collect-resources
├─ stage 2 ──→ [custom-baseline-test]
├─ stage 3 ──→ code-reverse-engineering
├─ stage 4 ──→ sota-iterate-and-improve
├─ stage 5 ──→ [sota-compare-metrics]
└─ stage 6 ──→ util-notifier
```

The orchestrator:
- Chains skills together
- Passes outputs of one skill as inputs to next
- Captures metrics at each stage
- Handles errors + retries
- Sends notifications
- Produces comparison reports

---

## Workflow Templates

Pre-defined workflows for common tasks:

```
Templates/
├── beat_sota_speed.yaml
├── beat_sota_memory.yaml
├── beat_sota_readability.yaml
├── beat_sota_deployment.yaml
├── write_paper_from_idea.yaml
├── extend_sota_method.yaml
└── compare_algorithms.yaml
```

Each template is:
- Ready to use (fill in URLs/ideas)
- Customizable (modify any stage)
- Documented (examples in each)

---

## Example: Complete Beat SOTA Workflow

```yaml
name: "Beat OpenAI Baselines PPO"
description: "Reimplement PPO in PyTorch, 30% faster"

config:
  paper_url: "https://arxiv.org/abs/1707.06347"
  repo_url: "https://github.com/openai/baselines"
  env: "CartPole-v1"
  target_dimension: "speed"
  acceptable_accuracy_drop: "1.0%"

stages:
  - id: collect
    name: "Collect Resources"
    skill: sota-collect-resources
    
  - id: baseline
    name: "Get Baseline Score"
    skill: run-original-code
    inputs:
      code: ${collect.outputs.source_code}
      env: ${config.env}
    capture:
      - accuracy
      - speed_per_epoch
      - memory_peak
  
  - id: analyze
    name: "Reverse Engineer Code"
    skill: code-reverse-engineering
    inputs:
      code: ${collect.outputs.source_code}
    outputs:
      - code_map
      - starter_code
  
  - id: reimplement
    name: "Reimplement in PyTorch"
    skill: sota-iterate-and-improve
    inputs:
      template: ${analyze.outputs.starter_code}
      constraint: "match accuracy ±1%"
    outputs:
      - code
  
  - id: test
    name: "Test & Compare"
    skill: sota-compare-metrics
    inputs:
      original: ${baseline.outputs}
      reimplemented: ${reimplement.outputs}
    produces:
      - comparison_table
      - improvement_summary
  
  - id: notify
    name: "Notify Team"
    skill: util-notifier
    inputs:
      message: ${test.outputs.improvement_summary}
      channels:
        - slack: "#sota"
        - email: "team@example.com"

success_criteria:
  - accuracy_preserved: ">=99%"  # 1% drop is OK
  - speed_improved: ">=1.2x"     # must be faster
  - code_cleaner: "true"         # fewer lines + type hints

  - id: publish_blog
    name: "Publish Blog Announcement"
    skill: util-github-git-push
    inputs:
      title: "Beat SOTA: {{improvement_title}}"
      content: |
        # {{improvement_title}}
        
        We reimplemented {{original_paper}} with improved performance:
        
        $$\text{Speedup} = \frac{T_{\text{original}}}{T_{\text{reimplemented}}} = {{speed_improvement}}x$$
        
        **Metrics:**
        - Accuracy: {{baseline_accuracy}}% → {{reimplemented_accuracy}}% ({{accuracy_delta}})
        - Speed: {{baseline_speed}}s/epoch → {{reimplemented_speed}}s/epoch ({{speed_improvement}}x faster)
        - Memory: {{baseline_memory}}MB → {{reimplemented_memory}}MB ({{memory_reduction}}% less)
        - Code: {{baseline_lines}} lines → {{reimplemented_lines}} lines ({{code_reduction}}% reduction)
        
        [View full comparison]({{comparison_report_link}})
      tags: ["sota", "optimization", "reimplement"]
      github_token: ${secrets.GITHUB_TOKEN}
      description: "Beat SOTA: {{improvement_summary}}"
    timeout: 5 minutes
  
  - id: notify
    name: "Notify Team"
    skill: util-notifier
    inputs:
      message: "✅ Beat SOTA: {{improvement_title}}\n\n{{improvement_summary}}\n\nBlog: {{publish_blog.outputs.blog_url}}"
      channels:
        - slack: "#sota"
        - email: "team@example.com"
      attachments:
        - ${test.outputs.comparison_table}
        - ${publish_blog.outputs.blog_url}
```

---

## Complete Example: Write Paper from Idea with Auto-Publishing

```yaml
name: "Write Paper + Publish to Overleaf + Blog"
description: "From idea to complete paper (Overleaf) with blog announcement"

config:
  idea: "Combine PPO with entropy regularization"
  reference_papers:
    - "https://arxiv.org/abs/1707.06347"  # PPO
    - "https://arxiv.org/abs/1805.00909"  # Maximum Entropy RL
  target_venue: "NeurIPS"
  implement_method: true
  publish_overleaf: true
  publish_blog: true

stages:
  - id: ingest_idea
    name: "Ingest Idea"
    skill: steer-human-ingest
    inputs:
      idea: ${config.idea}
      references: ${config.reference_papers}
    outputs:
      - idea_structured
      - key_concepts

  - id: collect
    name: "Collect Resources"
    skill: sota-collect-resources
    inputs:
      idea: ${ingest_idea.outputs.idea_structured}
      references: ${config.reference_papers}
    outputs:
      - reference_papers_pdf
      - implementation_baselines

  - id: analyze_papers
    name: "Analyze Writing Style"
    skill: paper-reverse-engineering
    inputs:
      papers: ${collect.outputs.reference_papers_pdf}
    outputs:
      - writing_models
      - rhetorical_patterns

  - id: write_structure
    name: "Write Structure"
    inputs:
      idea: ${ingest_idea.outputs.idea_structured}
      writing_models: ${analyze_papers.outputs.writing_models}
    outputs:
      - outline
      - evidence_map

  - id: implement
    name: "Implement Method"
    condition: ${config.implement_method}
    skill: sota-iterate-and-improve
    inputs:
      idea: ${ingest_idea.outputs.idea_structured}
      baselines: ${collect.outputs.implementation_baselines}
    outputs:
      - implementation_code
      - method_description

  - id: log_results
    name: "Log Experiment Results"
    skill: paper-result-logger
    inputs:
      implementation: ${implement.outputs.implementation_code}
      baselines: ${collect.outputs.implementation_baselines}
    outputs:
      - results_metrics
      - result_figures
      - result_tables

  - id: write_paper
    name: "Write Paper Draft"
    skill: paper-writer
    inputs:
      outline: ${write_structure.outputs.outline}
      writing_models: ${analyze_papers.outputs.writing_models}
      method_description: ${implement.outputs.method_description}
      results: ${log_results.outputs.results_metrics}
      figures: ${log_results.outputs.result_figures}
    outputs:
      - paper_markdown
      - paper_latex
      - paper_bib

  - id: publish_overleaf
    name: "Publish to Overleaf"
    condition: ${config.publish_overleaf}
    skill: util-github-git-push
    action: publish_paper_to_overleaf
    inputs:
      title: ${write_paper.outputs.paper_title}
      content: ${write_paper.outputs.paper_latex}
      overleaf_token: ${secrets.OVERLEAF_API_TOKEN}
      paper_type: "arxiv"
    outputs:
      - overleaf_project_id
      - overleaf_project_url

  - id: publish_blog
    name: "Publish Blog Announcement"
    condition: ${config.publish_blog}
    skill: util-github-git-push
    action: publish_blog_post
    inputs:
      title: "New Paper: {{paper_title}}"
      content: |
        {{paper_abstract}}
        
        **Key Contributions:**
        {{key_contributions}}
        
        **Results:**
        {{result_summary}}
        
        [Read full paper on Overleaf]({{overleaf_project_url}})
        
        **Formulas:**
        {{key_equations}}
      tags: ["paper", "research", "${config.target_venue}"]
      github_token: ${secrets.GITHUB_TOKEN}
      blog_repo: "https://github.com/SuuTTT/suuttt.github.io.git"
      description: ${write_paper.outputs.paper_abstract}
    outputs:
      - blog_url
      - commit_hash

  - id: notify
    name: "Notify Team"
    skill: util-notifier
    inputs:
      message: |
        📄 New Paper Published!
        
        **Title:** {{write_paper.outputs.paper_title}}
        **Venue:** ${config.target_venue}
        
        📋 Overleaf: {{publish_overleaf.outputs.overleaf_project_url}}
        📝 Blog: {{publish_blog.outputs.blog_url}}
        💾 Code: {{implement.outputs.implementation_code}}
      channels:
        - slack: "#papers"
        - email: "team@example.com"
      attachments:
        - ${write_paper.outputs.paper_markdown}
        - ${log_results.outputs.result_figures}

success_criteria:
  - paper_complete: "true"
  - overleaf_published: "{{config.publish_overleaf}}"
  - blog_published: "{{config.publish_blog}}"
  - results_included: "true"
```

---

## Benefits

✅ **Automation:** Run entire pipeline with one command  
✅ **Reproducibility:** Same workflow every time  
✅ **Monitoring:** See progress at each stage  
✅ **Comparison:** Automatic metrics capture + reporting  
✅ **Notifications:** Stay informed without manual updates  
✅ **Checkpoints:** Resume from any stage  
✅ **Reusable:** Templates for common tasks  
✅ **Extensible:** Add custom skills/stages easily  

---

## Typical Execution

```bash
# Define workflow
sotaflow beat_sota_speed \
  --paper "https://arxiv.org/abs/1707.06347" \
  --repo "https://github.com/openai/baselines" \
  --target speed

# Run it
sotaflow run beat_sota_speed

# Monitor
sotaflow status beat_sota_speed

# Get results
sotaflow results beat_sota_speed
# Shows: comparison table, improvement summary, metrics

# Share
sotaflow notify beat_sota_speed slack #sota
# Posts results to Slack
```

---

## What Gets Automated

For "Beat SOTA Speed" workflow:

```
❌ MANUAL (without workflow):
1. Download paper + code (5 min)
2. Set up environment (10 min)
3. Run original code (30 min)
4. Document baseline (5 min)
5. Analyze code (1 hour)
6. Reimplement (2-3 hours)
7. Run reimplemented code (30 min)
8. Compare metrics manually (15 min)
9. Write comparison report (15 min)
10. Post to Slack (5 min)
Total: ~5 hours, lots of manual steps

✅ AUTOMATED (with workflow):
1. Define workflow once
2. Run: sotaflow run beat_sota_speed
3. Get results + comparison + notification
Total: ~30 min running time + setup, 100% automated
```

---

## Next Steps

1. Define your workflow (YAML template)
2. Configure stages (URLs, parameters)
3. Run: `workflow.run()`
4. Monitor progress
5. Get results + notification
6. Compare metrics automatically
