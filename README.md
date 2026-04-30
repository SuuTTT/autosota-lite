# autosota-lite

`autosota-lite` is a local Codex plugin suite for ML paper reproduction and improvement workflows. It provides a set of specialized skills to automate research, resource management, and implementation tasks.

## Available Skills

Codex plugin skills should stay as direct children of `plugins/autosota-lite/skills/`. Category organization is tracked in `plugins/autosota-lite/references/skill-map.md`; nested category folders under `skills/` are avoided because direct `SKILL.md` discovery is the stable plugin layout.

### Pipeline
- **autosota-research-loop**: Coordinates the end-to-end research process (setup, baseline, ideation, iteration, audit, report).
- **autosota-optimization-pipeline**: Coordinates generated ideas, human ideas, domain knowledge, reimplementation, logging, notifications, and publishing.
- **autosota-agent-resource**: Maps paper assets, repositories, datasets, and checkpoints.
- **autosota-agent-objective**: Defines and refines research objectives and success metrics.
- **autosota-agent-scheduler**: General job scheduling and process management.
- **autosota-agent-monitor**: Monitors long-running experiments and system health.
- **autosota-agent-supervisor**: High-level oversight of scientific validity and benchmark red lines.

### Reimplementation
- **autosota-reimplementation**: Automated rewriting and porting of code (e.g., to JAX or CleanRL styles).
- **autosota-agent-fix**: Debugs and resolves implementation errors.
- **autosota-agent-init-fix**: Specifically handles initialization and setup-related issues.

### Optimization
- **autosota-agent-ideator**: Specialized in benchmark-safe improvement ideas and experiment design.
- **autosota-human-idea-ingest**: Facilitates human-in-the-loop idea refinement.
- **structural-entropy-proposal**: Structural Entropy, encoding-tree, hierarchy, and decoding-information proposal workflow.
- **autosota-runtime-cost-estimator**: Estimates GPU costs and recommends hardware based on workload.

### Common Operations
- **autosota-common-key-manager**: Manages credentials for WandB, GitHub, Vast.ai, Slack, Overleaf, and publishing tools without leaking secrets.
- **autosota-result-logger**: Automated logging to WandB and GitHub with credential-safe schema checks.
- **autosota-common-iteration-notifier**: Sends or drafts completion, failure, and review-needed notifications.
- **autosota-vastai-scheduler**: Manages GPU instances and job submission on Vast.ai.
- **autosota-agent-monitor-scheduler**: Specialized monitoring for scheduled Vast.ai jobs.

### Writing And Publishing
- **scientific-writing-reverse-engineering**: Reverse-engineers sentence and paragraph functions from model papers.
- **autosota-paper-writer**: Drafts ML research papers and human-readable reports.
- **autosota-common-publisher**: Drafts blog posts, release notes, short social posts, and TikTok-style scripts from validated results.

## Structure

```text
plugins/autosota-lite/
  .codex-plugin/
    plugin.json
  skills/
    autosota-research-loop/
      SKILL.md
    autosota-optimization-pipeline/
      SKILL.md
  scripts/
  references/
    skill-map.md
.agents/
  plugins/
    marketplace.json
README.md
```

## Install and Test in Codex App

1. Open Codex App.
2. Open this workspace folder:

   ```text
   /Users/suu/Documents/Codex/2026-04-26/plugin-creator-users-suu-codex-skills
   ```

3. Open plugin settings or marketplace management in Codex App.
4. Add or refresh the local marketplace at:

   ```text
   .agents/plugins/marketplace.json
   ```

5. Install or enable `autosota-lite`.
6. Start a new Codex chat in a paper-reproduction workspace and ask:

   ```text
   Use autosota-research-loop in setup mode for this ML paper reproduction project.
   ```

## Install and Test in Codex CLI

From this workspace, confirm the plugin files are present:

```bash
find plugins/autosota-lite .agents/plugins -maxdepth 4 -type f | sort
```

Then launch Codex CLI from a target ML reproduction repository and reference this local plugin marketplace according to your Codex CLI configuration. The marketplace entry points to:

```text
./plugins/autosota-lite
```

For a quick content test, inspect the skill directly:

```bash
sed -n '1,220p' plugins/autosota-lite/skills/autosota-research-loop/SKILL.md
```

Expected result: Codex can discover a skill named `autosota-research-loop` with six modes and the required benchmark red-line rules.

## Pull and Use on Another Linux Server

On the Linux server, install or update Codex CLI first, then clone the GitHub repo that contains this plugin:

```bash
git clone <GITHUB_REPO_URL> autosota-lite-plugins
cd autosota-lite-plugins
```

Verify the plugin files:

```bash
find plugins/autosota-lite .agents/plugins -maxdepth 4 -type f | sort
```

Expected files:

```text
.agents/plugins/marketplace.json
plugins/autosota-lite/.codex-plugin/plugin.json
plugins/autosota-lite/references/.gitkeep
plugins/autosota-lite/scripts/.gitkeep
plugins/autosota-lite/skills/autosota-research-loop/SKILL.md
```

Copy or vendor the plugin into the ML paper repo where you want to use it:

```bash
cd /path/to/ml-paper-repo
mkdir -p .agents plugins
cp -R /path/to/autosota-lite-plugins/.agents/plugins .agents/
cp -R /path/to/autosota-lite-plugins/plugins/autosota-lite plugins/
```

Confirm the marketplace path is still valid from the ML repo root:

```bash
python3 -m json.tool .agents/plugins/marketplace.json
python3 -m json.tool plugins/autosota-lite/.codex-plugin/plugin.json
```

Start Codex CLI from the ML repo root:

```bash
codex
```

Then ask Codex:

```text
Use autosota-research-loop in setup mode for this ML paper reproduction repo.
```

Recommended first workflow:

```text
Use autosota-research-loop in setup mode. Identify objective.md, resource_map.md, red_lines.md, autosota.yaml, official eval command, frozen metric code, and frozen test data.
```

Then:

```text
Use autosota-research-loop in baseline mode. Reproduce the baseline if possible and update scores.jsonl after every eval.
```

Then:

```text
Use autosota-research-loop in ideation mode. Propose benchmark-safe improvement ideas.
```

Then:

```text
Use autosota-research-loop in iteration mode. Create a git checkpoint before edits, attempt one idea, update scores.jsonl and idea_library.md, and recommend KEEP only if valid and improved.
```

Before trusting any improvement:

```text
Use autosota-research-loop in audit mode. Verify metric code and test data are frozen and decide KEEP or ROLLBACK.
```
