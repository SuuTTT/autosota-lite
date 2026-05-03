# AutoSOTA Lite Skill Map

Plugin skill directories should remain direct children of `plugins/autosota-lite/skills/` so Codex can discover each `SKILL.md` reliably. Use this map for category organization instead of nesting discoverable skills under category folders.

## Pipeline & Orchestration

**Core Lifecycle:**
- `autosota-research-loop`: end-to-end reproduction and benchmark-safe improvement (six modes: setup, baseline, ideation, iteration, audit, report).
- `autosota-optimization-pipeline`: post-baseline iteration coordinator integrating generated ideas, human feedback, domain knowledge, reimplementation, logging, and publishing.
- `autosota-agent-scheduler`: general job scheduling, lifecycle management, and process orchestration.
- `autosota-agent-monitor`: long-running experiment supervision, deadlock detection, and phase-aware tracking.
- `autosota-agent-monitor-scheduler`: combined monitoring and scheduling for persistent context management across execution resets.

**Research Context & Governance:**
- `autosota-agent-resource`: paper-to-repository grounding; maps paper assets, repositories, datasets, and checkpoints.
- `autosota-agent-objective`: objective construction, rubric definition, and success metrics refinement.
- `autosota-agent-supervisor`: scientific validity enforcement and benchmark red-line governance.

## Code Reimplementation & Debugging

- `autosota-reimplementation`: automated rewriting and porting to CleanRL or JAX styles; compact, comparable implementations.
- `autosota-agent-fix`: runtime error repair, dependency resolution, and general debugging.
- `autosota-agent-init-fix`: initialization, setup-phase, and environment configuration repair.

## Optimization & Ideation

**Idea Generation & Refinement:**
- `autosota-agent-ideator`: AI-driven benchmark-safe improvement ideas and experiment design.
- `autosota-human-idea-ingest`: human idea ingestion, normalization, and collaborative refinement.
- `structural-entropy-proposal`: Structural Entropy methodology, encoding trees, hierarchies, and decoding-information proposal workflows.

**Resource & Cost Management:**
- `autosota-runtime-cost-estimator`: GPU cost estimation, hardware recommendations, and workload profiling.

## Experiment Results & Reporting

**Results Management:**
- `exp_result_skill`: provisional Experiments/Results section generation with configurable multi-panel figures, editable workbench, and provenance tracking.
- `autosota-result-logger`: standardized result logging to WandB, GitHub Gists, and local repositories with credential-safe schema validation.

## Writing & Publication

**Rhetorical & Structural Analysis:**
- `scientific-writing-reverse-engineering`: model-paper reverse-engineering for sentence-by-sentence rhetorical function analysis; generates writing maps without plagiarism.
- `scientific_writing_reverse_engineering_skill`: enhanced variant with editable review workbench, rendering tools, and example outputs.

**Paper & Report Generation:**
- `autosota-paper-writer`: manuscripts, human-readable reports, and research paper drafting grounded in experimental results.
- `autosota-common-publisher`: blog posts, release notes, short-form social content, and TikTok-style scripts from validated results.

## Common Operations & Infrastructure

**Credentials & Notifications:**
- `autosota-common-key-manager`: credential and API key hygiene for WandB, GitHub, Vast.ai, Slack, Overleaf, and publishing services.
- `autosota-common-iteration-notifier`: iteration notifications (completion, failure, review-needed) via Slack or draft updates.

**Remote Compute:**
- `autosota-vastai-scheduler`: Vast.ai instance search, launch, monitoring, and cleanup with cost estimation.

## Incomplete / Placeholder

- `autosota-rl-experiment-section`: RL-specific experiment section generation (under development; no SKILL.md).

## Directory Layout

Discoverable skills remain as direct children of `plugins/autosota-lite/skills/` so Codex discovery is reliable:

```text
skills/
  autosota-agent-ideator/
    SKILL.md
  autosota-research-loop/
    SKILL.md
  ...
references/
  skill-map.md
```

