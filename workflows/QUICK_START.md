# Workflows Quick Start

Get started with pre-built research automation workflows in 60 seconds.

---

## Setup (One-time)

### 1. Install orchestrator
```bash
cd /workspace/autosota-lite
pip install -e .
```

### 2. Set credentials
```bash
# GitHub (required for publishing)
export GITHUB_TOKEN="ghp_your_token_here"

# Slack (optional, for notifications)
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."

# Email (optional, for notifications)
export GMAIL_USER="your@email.com"
export GMAIL_APP_PASSWORD="xxxx xxxx xxxx xxxx"

# Or save to .env.local
echo "GITHUB_TOKEN=ghp_..." >> /workspace/autosota-lite/.env.local
```

---

## Run a Workflow

### Option 1: Write a Paper from Idea (30-60 min)

```bash
cd /workspace/autosota-lite

python -m sota_workflow_orchestrator run workflows/write-paper-from-idea.yaml \
  --idea-title "World Models Based on Structural Entropy" \
  --idea-description "We present a framework for learning compact world models using information-theoretic principles. Our approach achieves 25% better sample efficiency and 40% smaller models." \
  --target-venue "NeurIPS"
```

**What happens:**
1. ✅ Finds 15 reference papers on world models
2. ✅ Analyzes writing style and structure
3. ✅ Creates outline and evidence map
4. ✅ Implements your method in PyTorch
5. ✅ Runs experiments (GPU-scheduled)
6. ✅ Writes complete paper
7. ✅ Pushes to GitHub + creates blog post
8. ✅ Notifies Slack + email

**Output:**
- `paper-world-models.../main.tex` on GitHub
- Blog post on your blog
- Slack notification with links

---

### Option 2: Beat SOTA Code (1-2 hours)

```bash
cd /workspace/autosota-lite

python -m sota_workflow_orchestrator run workflows/beat-sota-speed.yaml \
  --paper-url "https://arxiv.org/abs/1707.06347" \
  --repo-url "https://github.com/openai/baselines" \
  --target-dimension "speed" \
  --speed-target "30% faster"
```

**What happens:**
1. ✅ Downloads paper and original code
2. ✅ Runs baseline tests (3 runs averaged)
3. ✅ Reverse-engineers code to find bottlenecks
4. ✅ Reimplements optimized version
5. ✅ Tests optimized version
6. ✅ Compares metrics (speed, memory, accuracy)
7. ✅ Publishes results to blog
8. ✅ Pushes code to GitHub
9. ✅ Notifies Slack with comparison table

**Output:**
- Optimized code on GitHub
- Blog post with results table
- Comparison metrics (JSON)
- Slack notification with improvements

---

## Monitor Workflow

### Check status (while running)
```bash
python -m sota_workflow_orchestrator status write-paper-from-idea
# Output:
# ✅ Collect References — completed (5 min)
# ✅ Analyze Writing Style — completed (3 min)
# ✅ Create Outline — completed (2 min)
# 🔄 Implement Method — in progress (12 min elapsed)
# ⏳ Run Experiments — queued
# ...
```

### Watch live logs
```bash
tail -f /tmp/sota_workflow.log
```

### View metrics
```bash
python -m sota_workflow_orchestrator metrics write-paper-from-idea
```

---

## Resume from Checkpoint

If workflow stops at any point, resume without re-running earlier stages:

```bash
# Resume from "Write Full Paper" stage
python -m sota_workflow_orchestrator run write-paper-from-idea.yaml \
  --checkpoint "Write Full Paper" \
  --skip-completed
```

**Available checkpoints for paper workflow:**
- `Collect References` — After finding papers
- `Analyze Writing Style` — After style analysis
- `Create Outline` — After outline generation
- `After Implementation` — After coding
- `Run Experiments` — After experiments complete
- `Write Full Paper` — After writing draft
- `Publish Blog Announcement` — After blog publication

---

## Common Tasks

### Add your own workflow

1. Copy `beat-sota-speed.yaml` or `write-paper-from-idea.yaml`
2. Modify stages to match your pipeline
3. Run with:
   ```bash
   python -m sota_workflow_orchestrator run workflows/your-workflow.yaml
   ```

### View workflow definition
```bash
cat workflows/write-paper-from-idea.yaml
# Shows: inputs, stages, outputs, checkpoints
```

### Dry run (test without executing)
```bash
python -m sota_workflow_orchestrator run workflows/write-paper-from-idea.yaml \
  --idea-title "Test" \
  --dry-run
# Shows: execution plan, stages, inputs/outputs
```

### Change notification channels
Edit in workflow YAML:
```yaml
stages:
  - name: "Notify Team"
    inputs:
      channels:
        - "slack:#my-channel"
        - "email:me@example.com"
```

---

## Troubleshooting

### Workflow stuck?
```bash
# Check logs for specific stage
python -m sota_workflow_orchestrator logs write-paper-from-idea --stage "Implement Method"

# Resume from earlier checkpoint
python -m sota_workflow_orchestrator run write-paper-from-idea.yaml \
  --checkpoint "Create Outline" \
  --skip-completed
```

### Missing credentials?
```bash
# Check what's set
printenv | grep -E "GITHUB|SLACK|GMAIL|WANDB"

# Set token
export GITHUB_TOKEN="ghp_..."

# Or use GCP Secret Manager (recommended)
gcloud secrets create autosota-github-token --data-file=- <<<'ghp_...'
```

### Test a single skill
```bash
# Instead of full workflow, test individual skill
python -m sota_collect_resources --paper "https://arxiv.org/abs/1707.06347" --repo "https://github.com/openai/baselines"
```

---

## Next Steps

1. **Try a workflow:**
   ```bash
   python -m sota_workflow_orchestrator run workflows/write-paper-from-idea.yaml \
     --idea-title "Your idea" \
     --target-venue "NeurIPS"
   ```

2. **Monitor progress:**
   ```bash
   python -m sota_workflow_orchestrator status write-paper-from-idea
   ```

3. **Create custom workflow:**
   - Based on workflow YAML structure
   - Use stages from existing workflows
   - Combine skills as needed

---

## Workflow Cheat Sheet

```bash
# Run workflow
python -m sota_workflow_orchestrator run workflows/NAME.yaml --PARAM VALUE

# Check status
python -m sota_workflow_orchestrator status NAME

# View logs
python -m sota_workflow_orchestrator logs NAME --stage "Stage Name"

# Get metrics
python -m sota_workflow_orchestrator metrics NAME

# List workflows
ls workflows/*.yaml

# Dry run (no execution)
python -m sota_workflow_orchestrator run workflows/NAME.yaml --dry-run
```

---

**Tip:** For production use, set credentials in GCP Secret Manager instead of environment variables. See README.md for details.
