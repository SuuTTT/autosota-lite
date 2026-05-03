#!/usr/bin/env python3
"""Render an editable experiment workbench HTML.

The renderer supports the v5 figure-group schema:
  section.kind == "panel_group"
  section.config = {layout, style, axes, series, provenanceDisplay, export}
  section.panels = [panel-specific data]

It also migrates older v4 workbenches that stored panel layout in section.layout.

Usage:
    python render_panel_workbench.py result_workbench.json editable_review.html
"""
import json
import sys
from copy import deepcopy
from pathlib import Path

DEFAULT_CONFIG = {
    "layout": {
        "columns": 3,
        "panelWidth": 360,
        "panelHeight": 260,
        "gap": 18,
        "sharedLegend": True,
        "legendPosition": "bottom",
        "showPanelLetters": True,
    },
    "style": {
        "fontSize": 12,
        "titleFontSize": 14,
        "lineWidth": 2,
        "markerSize": 3,
        "showGrid": True,
        "showEnvelope": True,
        "showValueLabels": False,
    },
    "axes": {
        "xLabel": "x",
        "yLabel": "y",
        "xScale": "linear",
        "yScale": "linear",
        "shareX": True,
        "shareY": False,
    },
    "series": {
        "methods": [],
        "methodOrder": [],
        "highlightMethods": [],
    },
    "provenanceDisplay": {
        "showBadges": True,
        "showModifiedWarning": True,
        "showArtificialWatermark": True,
    },
    "export": {
        "formats": ["json", "svg"],
        "exportEachPanel": True,
        "exportWholeGroup": True,
    },
}

LEGACY_KEY_MAP = {
    "panelWidth": ("layout", "panelWidth"),
    "panelHeight": ("layout", "panelHeight"),
    "columns": ("layout", "columns"),
    "legendPosition": ("layout", "legendPosition"),
    "markerSize": ("style", "markerSize"),
    "fontSize": ("style", "fontSize"),
    "showEnvelope": ("style", "showEnvelope"),
}


def deep_merge(base, override):
    out = deepcopy(base)
    for k, v in (override or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def migrate_workbench(workbench):
    """Normalize workbench to the v5 config schema without destroying source fields."""
    default_config = deep_merge(DEFAULT_CONFIG, workbench.get("defaultFigureConfig", {}))
    for section in workbench.get("sections", []):
        if section.get("kind") != "panel_group":
            continue
        config = deep_merge(default_config, section.get("config", {}))

        # v4 compatibility: migrate flat section.layout into config.layout/style.
        legacy_layout = section.get("layout", {}) or {}
        for old_key, (group, new_key) in LEGACY_KEY_MAP.items():
            if old_key in legacy_layout:
                config.setdefault(group, {})[new_key] = legacy_layout[old_key]

        # Infer method lists if absent.
        methods = []
        for panel in section.get("panels", []):
            for series in panel.get("series", []) or []:
                name = series.get("name")
                if name and name not in methods:
                    methods.append(name)
        config.setdefault("series", {})
        if not config["series"].get("methods"):
            config["series"]["methods"] = methods
        if not config["series"].get("methodOrder"):
            config["series"]["methodOrder"] = methods

        # Infer axis labels from first panel if absent/default.
        first_panel = next(iter(section.get("panels", []) or []), {})
        config.setdefault("axes", {})
        if config["axes"].get("xLabel") in (None, "x") and first_panel.get("xLabel"):
            config["axes"]["xLabel"] = first_panel["xLabel"]
        if config["axes"].get("yLabel") in (None, "y") and first_panel.get("yLabel"):
            config["axes"]["yLabel"] = first_panel["yLabel"]

        section["config"] = config
        section["figure_type"] = section.get("figure_type", "multi_panel_curve")
        section.setdefault("panel_type", section.get("panel_type", "line"))
    return workbench


def main():
    if len(sys.argv) != 3:
        print("Usage: python render_panel_workbench.py result_workbench.json editable_review.html")
        raise SystemExit(1)
    workbench_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])
    template_path = Path(__file__).parent / "templates" / "editable_review_template.html"
    workbench = migrate_workbench(json.loads(workbench_path.read_text(encoding="utf-8")))
    # Persist migrated config beside the rendered HTML so exported artifacts start from v5 schema.
    workbench_path.write_text(json.dumps(workbench, indent=2, ensure_ascii=False), encoding="utf-8")
    template = template_path.read_text(encoding="utf-8")
    html = template.replace("__WORKBENCH_JSON__", json.dumps(workbench).replace("</script>", "<\\/script>"))
    out_path.write_text(html, encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
