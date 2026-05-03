# autosota-lite

`autosota-lite` is a local Codex plugin suite for ML paper reproduction and improvement workflows. It provides a set of specialized skills to automate research, resource management, and implementation tasks.

## Skills Overview

See **[SKILLS_MAP.md](SKILLS_MAP.md)** for complete skill organization and quick lookup by task.

All skills use the prefix system for easy discovery:

```
sota-*          AutoSOTA core (reproduce, improve, iterate)
steer-*         Human steering & guidance  
paper-*         Writing, analysis, results
optimize-*      Code & iteration optimization
util-*          Infrastructure & utilities
```

### Quick Examples

**Reproduce & improve a paper:**
```bash
sota-collect-resources          # Find papers/datasets
sota-reproduce-and-iterate      # Run the code
sota-idea-generator             # Generate improvements
sota-iterate-and-improve        # Implement changes
paper-writer                    # Write findings
util-notifier                   # Notify team
```

**Speed up slow code:**
```bash
sota-optimize-iteration         # Profile training
optimize-reimplementation       # Rewrite fast parts
util-gpu-scheduler              # Add GPUs if needed
paper-result-logger             # Track improvements
```

**All skills:** `/workspace/autosota-lite/plugins/autosota-lite/skills/`

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
