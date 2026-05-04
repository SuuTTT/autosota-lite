# Workflow Registry

Reusable orchestrated pipelines combining multiple skills to complete complex research tasks.

---

## Pre-Built Workflows

### 1. **write-paper-from-idea.yaml**

Convert a research idea into a complete paper with experiments, code, and blog announcement.

**Pipeline:**
```
Idea 
  ↓
Collect References (sota-collect-resources)
  ↓
Analyze Writing Style (code-reverse-engineering)
  ↓
Create Outline (paper-writer)
  ↓
Implement Method (sota-iterate-and-improve)
  ↓
Write Full Paper (paper-writer)
  ↓
Push to GitHub (util-publisher)
  ↓
Create Blog Announcement (util-publisher)
  ↓
Notify Team (util-notifier)
```

**Inputs:**
- `idea_title` — Research topic (e.g., "World Models with Structural Entropy")
- `idea_description` — 2-3 paragraph description of your contribution
- `target_venue` — "NeurIPS", "ICML", "ICLR", etc.

**Outputs:**
- `github_repository` — GitHub repo with paper + code + figures
- `blog_announcement` — Published blog post with KaTeX formulas
- `experiment_results` — Metrics and results tables

**Usage:**
```bash
python -m sota_workflow_orchestrator run workflows/write-paper-from-idea.yaml \
  --idea-title "World Models Based on Structural Entropy" \
  --idea-description "We present a novel approach using structural entropy for compact world model learning" \
  --target-venue "NeurIPS"
```

**Time to complete:** 30-60 minutes (depending on experiment runtime)

---

### 2. **beat-sota-speed.yaml**

Reimplement published code to be faster while maintaining accuracy, automatically compare results.

**Pipeline:**
```
Paper + Repo
  ↓
Collect Original (sota-collect-resources)
  ↓
Baseline Test (util-gpu-scheduler)
  ↓
Analyze Code (code-reverse-engineering)
  ↓
Reimplement Faster (sota-iterate-and-improve)
  ↓
Test Optimized (util-gpu-scheduler)
  ↓
Compare Results (sota-compare-metrics)
  ↓
Publish Results (util-publisher)
  ↓
Notify Team (util-notifier)
```

**Inputs:**
- `paper_url` — arXiv link or paper PDF URL
- `repo_url` — Original GitHub repository
- `target_dimension` — "speed" | "memory" | "readability"

**Outputs:**
- `comparison` — Detailed metrics comparison report
- `blog_post` — Published blog announcement with results
- `code` — Optimized reimplementation

**Usage:**
```bash
python -m sota_workflow_orchestrator run workflows/beat-sota-speed.yaml \
  --paper-url "https://arxiv.org/abs/1707.06347" \
  --repo-url "https://github.com/openai/baselines" \
  --target-dimension "speed"
```

**Time to complete:** 1-2 hours (baseline test + reimplementation + comparison)

---

## Workflow Stages and Features

### Checkpointing

Resume workflows from any stage without re-running earlier steps:

```bash
# Resume from "Write Full Paper" stage
python -m sota_workflow_orchestrator run write-paper-from-idea.yaml \
  --checkpoint "Write Full Paper" \
  --skip-completed
```

### Metrics Capture

Automatically logs metrics at each stage for later analysis:

```bash
python -m sota_workflow_orchestrator metrics write-paper-from-idea
# Shows: stage name, duration, outputs, errors
```

### Notifications

Workflows automatically notify via Slack and email on:
- Completion ✅
- Errors ❌
- Stage transitions

Configure in your credentials:
```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/..."
export GMAIL_USER="your@email.com"
export GMAIL_APP_PASSWORD="xxxx xxxx xxxx xxxx"
```

---

## Creating Custom Workflows

Use these pre-built workflows as templates. Structure:

```yaml
name: "Your Workflow Name"
description: "What it does"
version: "1.0"

inputs:
  param1: string
  param2: string

stages:
  - name: "Stage Name"
    skill: skill-name
    inputs: {...}
    outputs: [...]

outputs:
  result1: ${stages.N.outputs.name}
```

Key concepts:
- **`stages`** — Sequential or parallel skill invocations
- **`inputs`** — Parameters passed to the skill
- **`outputs`** — Data produced for downstream stages
- **`${stages.N.outputs.name}`** — Reference previous stage outputs

---

## File Structure

```
workflows/
├── README.md                           # This file
├── write-paper-from-idea.yaml          # Write paper from idea → code → blog
├── beat-sota-speed.yaml                # Optimize code for speed
└── examples/                           (Future)
    ├── beat-sota-memory.yaml
    ├── beat-sota-readability.yaml
    ├── reproduce-sota.yaml
    └── compare-approaches.yaml
```

---

## Troubleshooting

### Workflow stuck at a stage

```bash
# Check detailed logs
python -m sota_workflow_orchestrator logs write-paper-from-idea --stage "Write Full Paper"

# Resume from previous stage
python -m sota_workflow_orchestrator run write-paper-from-idea.yaml \
  --checkpoint "Create Outline" \
  --skip-completed
```

### Missing credentials

Workflows require:
- `GITHUB_TOKEN` — Create at https://github.com/settings/tokens/new (repo scope)
- `WANDB_API_KEY` — Optional, for logging metrics
- `SLACK_WEBHOOK_URL` — Optional, for notifications
- `GMAIL_USER` + `GMAIL_APP_PASSWORD` — Optional, for email notifications

Set via:
```bash
# GCP Secret Manager (recommended)
gcloud secrets create autosota-github-token --data-file=- <<<'ghp_...'

# Or .env.local
echo "GITHUB_TOKEN=ghp_..." >> /workspace/autosota-lite/.env.local
```

---

## Next Steps

1. **Try a workflow:**
   ```bash
   python -m sota_workflow_orchestrator run workflows/write-paper-from-idea.yaml \
     --idea-title "Your Research Idea" \
     --target-venue "NeurIPS"
   ```

2. **Monitor progress:**
   ```bash
   watch -n 5 'python -m sota_workflow_orchestrator status write-paper-from-idea'
   ```

3. **Create custom workflow:**
   - Copy one of the examples
   - Modify stages to match your pipeline
   - Run with same orchestrator command

---

**Created:** May 4, 2026  
**Status:** Production-ready  
**Updated:** Registered 2 core workflows
