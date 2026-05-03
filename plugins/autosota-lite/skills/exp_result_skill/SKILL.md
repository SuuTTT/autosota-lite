# Skill: Provisional Experiment & Results Workbench with Configurable Multi-Panel Figures

## Purpose

Generate a complete provisional **Experiments / Results** section for a research paper from partial evidence, plus an editable review workbench.

This skill is designed for the common early-paper situation where only partial evidence exists, for example:
- one seed,
- one environment,
- one dataset,
- a few preliminary curves,
- public benchmark numbers,
- planned but unfinished ablations or robustness experiments.

The output is a draft scaffold, not final scientific evidence. It must clearly mark what is real, public, estimated, artificial, derived, or modified.

---

## Core outputs

Given a method and currently available data, generate:

1. `results_section.tex`  
   A complete LaTeX draft for the experiment/result section.

2. `result_workbench.json`  
   A machine-readable editable workbench with all tables, multi-panel figure groups, per-panel data, shared figure configs, provenance tags, and export metadata.

3. `editable_review.html`  
   A self-contained editable HTML dashboard.

4. `review.md`  
   A Markdown fallback for static review when HTML rendering of figures/equations is undesirable.

5. LaTeX tables and placeholder figure references.

---

## Mandatory provenance labels

Every table cell, curve panel, curve series, point, visual asset, and claim must use one of:

- `experimented` — directly measured in the user's current experiments.
- `public` — imported from public benchmark/paper/leaderboard.
- `estimated` — interpolated or extrapolated from partial evidence.
- `artificial` — invented placeholder for layout/story review.
- `modified` — edited by the user inside the review workbench.
- `derived` — computed from other values or generated from the planned experiment matrix.

The HTML must show these labels visibly.

---

## Experiment section template

Use this default structure:

```text
5. Experiments

5.1 Setup
Table: environments, metrics, training budget, seeds, baselines.

5.2 Main Results
Table:
    rows = methods
    columns = environments/tasks
    cells = final score.

5.3 Learning and Sample Efficiency
Multi-panel curve group:
    one panel per task/environment
    x-axis = environment steps
    y-axis = evaluation return/success
    lines = methods
    shade/envelope = seed uncertainty.

5.4 Ablation Study
Table:
    rows = full method and variants
    columns = metrics/tasks
    cells = final score.

5.5 Generalization
Table or multi-panel curve group:
    rows/x-axis = unseen test condition or difficulty
    columns/lines = methods
    cells/y-axis = performance.

5.6 Robustness
Multi-panel curve group:
    one panel per task, perturbation type, or condition
    x-axis = perturbation strength
    y-axis = performance
    lines = methods.

5.7 Scalability and Efficiency
Multi-panel curve group:
    one panel per task or problem family
    x-axis = problem size
    y-axis = performance.

Table:
    rows = methods
    columns = training time, inference time, memory, parameters.

5.8 Qualitative Analysis
Multi-panel visualization group:
    one panel per task/trajectory/example
    visualization = trajectory plot, rollout rendering, heatmap, graph, or video placeholder.

5.9 Case Study / Failure Cases
Table or visualization:
    rows = failure modes
    columns = frequency and explanation.
```

---

## Best-practice data model for multi-panel figures

Manage multi-panel graphs with **one shared figure-group config** plus **one panel-specific data block per task/condition**.

```text
FigureGroup
├── config: shared layout/style/axis/legend/export settings
├── panels:
│   ├── panel_1: task-specific data and optional overrides
│   ├── panel_2: task-specific data and optional overrides
│   └── panel_3: task-specific data and optional overrides
└── provenance: real/public/estimated/artificial/modified/derived
```

The canonical JSON schema is:

```json
{
  "id": "learning_efficiency",
  "number": "5.3",
  "title": "Learning and Sample Efficiency",
  "kind": "panel_group",
  "figure_type": "multi_panel_curve",
  "panel_type": "line",
  "description": "One panel per task/environment.",
  "config": {
    "layout": {
      "columns": 3,
      "panelWidth": 360,
      "panelHeight": 260,
      "gap": 18,
      "sharedLegend": true,
      "legendPosition": "bottom",
      "showPanelLetters": true
    },
    "style": {
      "fontSize": 12,
      "titleFontSize": 14,
      "lineWidth": 2,
      "markerSize": 3,
      "showGrid": true,
      "showEnvelope": true,
      "showValueLabels": false
    },
    "axes": {
      "xLabel": "Environment steps",
      "yLabel": "Evaluation return",
      "xScale": "linear",
      "yScale": "linear",
      "shareX": true,
      "shareY": false
    },
    "series": {
      "methods": ["TRACE", "DreamerV3", "TD-MPC2", "PlaNet"],
      "methodOrder": ["TRACE", "TD-MPC2", "DreamerV3", "PlaNet"],
      "highlightMethods": ["TRACE"]
    },
    "provenanceDisplay": {
      "showBadges": true,
      "showModifiedWarning": true,
      "showArtificialWatermark": true
    },
    "export": {
      "formats": ["json", "svg"],
      "exportEachPanel": true,
      "exportWholeGroup": true
    }
  },
  "panels": [
    {
      "id": "walker_walk",
      "title": "Walker Walk",
      "task": "Walker Walk",
      "xLabel": "Environment steps",
      "yLabel": "Evaluation return",
      "series": [
        {
          "name": "TRACE",
          "provenance": "experimented",
          "points": [
            {"x": 100000, "y": 420, "std": 20, "provenance": "experimented"}
          ]
        }
      ]
    }
  ]
}
```

### Best-practice defaults

For RL/control learning curves:

```json
{
  "layout": {
    "columns": 3,
    "sharedLegend": true,
    "legendPosition": "bottom",
    "showPanelLetters": true
  },
  "style": {
    "fontSize": 10,
    "titleFontSize": 11,
    "lineWidth": 2,
    "markerSize": 2.5,
    "showEnvelope": true,
    "showGrid": true,
    "showValueLabels": false
  },
  "axes": {
    "shareX": true,
    "shareY": false
  }
}
```

Use `shareX: true` for learning curves because all panels usually use environment steps. Use `shareY: false` for raw RL returns unless all tasks are normalized to the same scale.

---

## HTML requirements

The editable HTML must support:

### Tables
- direct cell editing;
- provenance dropdown per cell;
- automatic provenance change to `modified` after editing;
- export buttons located immediately next to the table:
  - Export JSON,
  - Export CSV,
  - Export LaTeX.

### Multi-panel curves and visualizations
- one card per panel;
- per-panel editable JSON textarea;
- Apply JSON edits + redraw;
- per-panel export buttons:
  - Export panel JSON,
  - Export panel SVG;
- group-level simple controls:
  - number of columns,
  - panel width,
  - panel height,
  - font size,
  - line width,
  - marker size,
  - legend position,
  - show/hide uncertainty envelope,
  - share x-axis,
  - share y-axis,
  - show/hide provenance badges;
- group-level advanced config editor:
  - editable JSON textarea for the entire `config` object;
  - Apply config + redraw button;
- group-level export:
  - Export group JSON,
  - Export group SVG.

### Whole workbench
- Export whole workbench JSON;
- Export self-contained HTML snapshot.

---

## Table design rules

- Highlight the author's method using boldface.
- Bold the best result.
- Underline the second-best result.
- Add metric arrows in headers, e.g. `Return ($\uparrow$)`, `Error ($\downarrow$)`.
- Use two decimals by default.
- Use `mean $\pm$ std` when multiple seeds are available.
- Mark artificial/estimated entries in LaTeX comments or provenance badges.

---

## Figure design rules

- Use multi-panel line charts for learning and robustness sections.
- Use one panel per task/environment by default.
- Use transparent uncertainty envelopes when seed variance is available.
- Use consistent legends and axis labels across panels.
- Keep data separate from visual style.
- Make panel layout configurable, because authors will decide later how many panels to include in the final paper.

---

## Honesty constraint

Never present artificial or estimated values as completed experiments. The workbench may generate a polished draft, but it must keep all provisional evidence visibly labeled and easy to replace.
