# autosota-lite

`autosota-lite` is a local Codex plugin suite for ML paper reproduction and improvement workflows. It provides a set of specialized skills to automate research, resource management, and implementation tasks.

## Available Skills

Codex plugin skills should stay as direct children of `plugins/autosota-lite/skills/`. Category organization is tracked in `plugins/autosota-lite/references/skill-map.md`; nested category folders under `skills/` are avoided because direct `SKILL.md` discovery is the stable plugin layout.

### Pipeline & Orchestration

**Core Lifecycle:**
- **autosota-research-loop**: Coordinates the end-to-end research process with six modes (setup, baseline, ideation, iteration, audit, report). Ensures benchmark safety, metric freezing, and scientific validity throughout.
- **autosota-optimization-pipeline**: Post-baseline iteration orchestrator integrating generated ideas, human feedback, domain knowledge, code reimplementation, result logging, notifications, and publishing workflows.
- **autosota-agent-scheduler**: General job scheduling, lifecycle management, and process orchestration for long-running experiments.
- **autosota-agent-monitor**: Long-running experiment supervision with deadlock detection, phase-aware tracking, and pathological stalling intervention.
- **autosota-agent-monitor-scheduler**: Combined monitoring and scheduling for persistent context management, execution reset recovery, and iterative optimization (Normal vs Leap paths).

**Research Context & Governance:**
- **autosota-agent-resource**: Paper-to-repository grounding that maps paper assets, repositories, datasets, checkpoints, and research dependencies.
- **autosota-agent-objective**: Research objective construction, rubric definition, and success metrics refinement.
- **autosota-agent-supervisor**: Scientific validity enforcement, benchmark red-line governance, and experimental integrity auditing.

### Code Reimplementation & Debugging

- **autosota-reimplementation**: Automated code rewriting and porting to CleanRL or JAX styles, producing compact and comparable implementations.
- **autosota-agent-fix**: Runtime error diagnosis and repair, dependency resolution, and general debugging workflows.
- **autosota-agent-init-fix**: Initialization, setup-phase configuration, and environment repair for dependency and version compatibility issues.

### Optimization & Ideation

**Idea Generation & Refinement:**
- **autosota-agent-ideator**: AI-driven generation of benchmark-safe improvement ideas and structured experiment design.
- **autosota-human-idea-ingest**: Human idea ingestion, normalization, domain knowledge integration, and collaborative refinement.
- **structural-entropy-proposal**: Structural Entropy methodology, encoding trees, hierarchies, and decoding-information workflows for advanced optimization.

**Resource & Cost Management:**
- **autosota-runtime-cost-estimator**: GPU cost estimation, hardware recommendations based on workload profiles, and Vast.ai rental cost prediction.

### Experiment Results & Reporting

**Results Management:**
- **exp_result_skill**: Generates provisional Experiments/Results sections with configurable multi-panel figures, editable review workbench, and mandatory provenance tracking (experimented, public, estimated, artificial, modified, derived).
- **autosota-result-logger**: Standardized result logging to WandB, GitHub Gists, and local repositories with credential-safe schema validation.

### Writing & Publication

**Rhetorical & Structural Analysis:**
- **scientific-writing-reverse-engineering**: Model-paper reverse-engineering using Hilary Glasman-Deal methods for sentence-by-sentence rhetorical function analysis; generates writing maps without plagiarism.
- **scientific_writing_reverse_engineering_skill**: Enhanced variant with interactive HTML review workbench, editable writing maps, figure rendering tools, and example outputs.

**Paper & Report Generation:**
- **autosota-paper-writer**: Manuscripts, human-readable reports, and research paper drafting grounded in experimental results and validated findings.
- **autosota-common-publisher**: Blog posts, release notes, short-form social content, and TikTok-style scripts drafted from validated experimental results.

### Common Operations & Infrastructure

**Credentials & Notifications:**
- **autosota-common-key-manager**: Credential and API key hygiene for WandB, GitHub, Vast.ai, Slack, Overleaf, and publishing services without leaking secrets.
- **autosota-common-iteration-notifier**: Iteration completion, failure, and review-needed notifications via Slack with draft fallback options.

**Remote Compute:**
- **autosota-vastai-scheduler**: Vast.ai instance search, cost filtering, launch, monitoring, and cleanup with integrated cost estimation.

### Incomplete / Placeholder

- **autosota-rl-experiment-section**: RL-specific experiment section generation (under development; no SKILL.md yet).

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
