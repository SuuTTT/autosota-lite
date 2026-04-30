# AutoSOTA Lite Skill Map

Plugin skill directories should remain direct children of `plugins/autosota-lite/skills/` so Codex can discover each `SKILL.md` reliably. Use this map for category organization instead of nesting discoverable skills under category folders.

## Pipeline

- `autosota-research-loop`: end-to-end reproduction and benchmark-safe improvement.
- `autosota-optimization-pipeline`: post-baseline iteration coordinator.
- `autosota-agent-resource`: paper-to-repository grounding and asset discovery.
- `autosota-agent-objective`: objective and rubric construction.
- `autosota-agent-scheduler`: lifecycle scheduling.
- `autosota-agent-monitor`: long-running run supervision.
- `autosota-agent-supervisor`: scientific validity and red-line governance.

## Reimplementation

- `autosota-reimplementation`: CleanRL-style, compact, comparable implementations and JAX rewrites.
- `autosota-agent-fix`: runtime and dependency repair.
- `autosota-agent-init-fix`: setup and initialization repair.

## Optimization

- `autosota-agent-ideator`: generated benchmark-safe ideas.
- `autosota-human-idea-ingest`: human idea normalization and review.
- `structural-entropy-proposal`: Structural Entropy and hierarchy domain knowledge.
- `autosota-runtime-cost-estimator`: runtime and GPU rental estimates.

## Common Operations

- `autosota-common-key-manager`: credentials and external service auth hygiene.
- `autosota-result-logger`: standardized logs, WandB, and GitHub result sync.
- `autosota-common-iteration-notifier`: Slack or channel notifications.
- `autosota-vastai-scheduler`: Vast.ai search, launch, monitor, and cleanup.

## Writing And Publishing

- `scientific-writing-reverse-engineering`: model-paper sentence-function analysis.
- `autosota-paper-writer`: manuscripts and human-readable reports.
- `autosota-common-publisher`: blog, release note, short social, and TikTok-style drafts.

## Layout Decision

Do not reorganize discoverable skills like this unless the plugin loader is proven to recurse:

```text
skills/
  optimization/
    autosota-agent-ideator/
      SKILL.md
```

Keep this instead:

```text
skills/
  autosota-agent-ideator/
    SKILL.md
references/
  skill-map.md
```

