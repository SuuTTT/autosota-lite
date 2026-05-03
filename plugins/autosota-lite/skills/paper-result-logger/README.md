# Provisional Experiment & Results Workbench v5

This package implements a reusable skill for drafting and reviewing a paper's experiment/results section when data is incomplete.

## v5 change

v5 adds a **best-practice multi-panel figure config**:

- every multi-panel figure has one shared `config` object;
- each panel stores only task/condition-specific data;
- the HTML exposes simple controls for common layout/style choices;
- the HTML also exposes an advanced config JSON editor;
- changing config or data redraws the figure group;
- each panel and each whole group can be exported.

## Main files

- `SKILL.md` — skill specification.
- `example_output/result_workbench.json` — source workbench data structure with v5 `config` blocks.
- `example_output/editable_review.html` — self-contained editable dashboard.
- `example_output/review.md` — Markdown fallback review.
- `example_output/results_section.tex` — generated LaTeX section.
- `render_panel_workbench.py` — render a workbench JSON into HTML and migrate v4 layouts into v5 config.
- `templates/editable_review_template.html` — HTML template.

## Usage

```bash
python render_panel_workbench.py example_output/result_workbench.json example_output/editable_review.html
```

Open `example_output/editable_review.html` in a browser.

## Recommended config pattern

```json
{
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
      "shareX": true,
      "shareY": false
    }
  },
  "panels": [
    {"id": "walker_walk", "title": "Walker Walk", "series": []}
  ]
}
```
