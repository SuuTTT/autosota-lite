#!/usr/bin/env python3
"""
Render a scientific-writing reverse-engineering writing_map as an interactive HTML page.

Primary display rule:
- The hover/inspector card shows the MODEL PAPER'S original sentence first.
- If a project/user original sentence exists, it is shown separately as optional context.

Supported object fields:
- model_original_sentence | model_sentence | model_sentence_excerpt | original_sentence
- abstract_sentence_function
- model_pattern | reusable_model | abstract_model
- project_original_sentence | target_original_sentence | user_original_sentence
- rewritten_sentence | rewrite_of_sentence

Supported tuple/list formats:
- [model_original_sentence, abstract_sentence_function, rewritten_sentence]
- [model_original_sentence, abstract_sentence_function, rewritten_sentence, project_original_sentence]
- [model_original_sentence, abstract_sentence_function, model_pattern, rewritten_sentence, project_original_sentence]

Usage:
    python render_writing_map.py writing_map.json -o writing_map.html
"""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List


def first_nonempty(*values: Any) -> str:
    for value in values:
        if value is None:
            continue
        text = str(value).strip()
        if text:
            return text
    return ""


def normalize_item(item: Any, fallback_index: int) -> Dict[str, Any]:
    """Normalize one writing-map item to a common dictionary shape."""
    if isinstance(item, dict):
        return {
            "section": first_nonempty(item.get("section"), "Draft"),
            "sentence_index": item.get("sentence_index", fallback_index),
            "model_original_sentence": first_nonempty(
                item.get("model_original_sentence"),
                item.get("model_sentence"),
                item.get("model_sentence_excerpt"),
                item.get("original_sentence"),  # legacy: original_sentence means model sentence
            ),
            "abstract_sentence_function": first_nonempty(item.get("abstract_sentence_function")),
            "model_pattern": first_nonempty(
                item.get("model_pattern"), item.get("reusable_model"), item.get("abstract_model")
            ),
            "project_original_sentence": first_nonempty(
                item.get("project_original_sentence"),
                item.get("target_original_sentence"),
                item.get("user_original_sentence"),
            ),
            "rewritten_sentence": first_nonempty(
                item.get("rewritten_sentence"), item.get("rewrite_of_sentence")
            ),
            "category": first_nonempty(item.get("category")),
            "caution": first_nonempty(item.get("caution")),
        }

    if isinstance(item, (list, tuple)):
        if len(item) == 3:
            model, function, rewrite = item
            pattern, project_original = "", ""
        elif len(item) == 4:
            model, function, rewrite, project_original = item
            pattern = ""
        elif len(item) >= 5:
            model, function, pattern, rewrite, project_original = item[:5]
        else:
            raise ValueError(f"Tuple item #{fallback_index} must contain at least 3 fields.")
        return {
            "section": "Draft",
            "sentence_index": fallback_index,
            "model_original_sentence": str(model),
            "abstract_sentence_function": str(function),
            "model_pattern": str(pattern),
            "project_original_sentence": str(project_original),
            "rewritten_sentence": str(rewrite),
            "category": "",
            "caution": "",
        }

    raise ValueError(
        f"Item #{fallback_index} must be either an object or a tuple/list. Got: {item!r}"
    )


def group_by_section(items: Iterable[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for item in items:
        section = str(item.get("section") or "Draft")
        grouped.setdefault(section, []).append(item)
    return grouped


def esc_attr(value: Any) -> str:
    return html.escape(str(value or ""), quote=True)


def sentence_span(item: Dict[str, Any], absolute_index: int) -> str:
    rewritten = html.escape(str(item.get("rewritten_sentence", ""))).strip()
    if not rewritten:
        rewritten = "[PROJECT DETAIL NEEDED]"

    cls = "mapped-sentence"
    if item.get("caution"):
        cls += " caution"

    attrs = {
        "data-index": absolute_index,
        "data-section": item.get("section", ""),
        "data-sentence-index": item.get("sentence_index", ""),
        "data-model": item.get("model_original_sentence", ""),
        "data-function": item.get("abstract_sentence_function", ""),
        "data-pattern": item.get("model_pattern", ""),
        "data-project-original": item.get("project_original_sentence", ""),
        "data-rewrite": item.get("rewritten_sentence", ""),
        "data-caution": item.get("caution", ""),
    }
    attr_text = " ".join(f'{name}="{esc_attr(value)}"' for name, value in attrs.items())

    tooltip_parts = [
        '<span class="tooltip-card" role="tooltip">',
        f'<span class="tooltip-kicker">{html.escape(str(item.get("section", "Draft")))} sentence {html.escape(str(item.get("sentence_index", absolute_index)))}</span>',
        '<span class="tooltip-label primary">Model paper sentence</span>',
        f'<span class="tooltip-text">{html.escape(str(item.get("model_original_sentence", "")))}</span>',
        '<span class="tooltip-label">Abstract function</span>',
        f'<span class="tooltip-text">{html.escape(str(item.get("abstract_sentence_function", "")))}</span>',
    ]
    if item.get("model_pattern"):
        tooltip_parts.extend([
            '<span class="tooltip-label">Model pattern</span>',
            f'<span class="tooltip-text">{html.escape(str(item.get("model_pattern", "")))}</span>',
        ])
    if item.get("project_original_sentence"):
        tooltip_parts.extend([
            '<span class="tooltip-label">Project original sentence</span>',
            f'<span class="tooltip-text">{html.escape(str(item.get("project_original_sentence", "")))}</span>',
        ])
    if item.get("caution"):
        tooltip_parts.extend([
            '<span class="tooltip-label warning">Caution</span>',
            f'<span class="tooltip-text">{html.escape(str(item.get("caution", "")))}</span>',
        ])
    tooltip_parts.append('</span>')
    tooltip = "".join(tooltip_parts)

    return f'<span id="s{absolute_index}" class="{cls}" tabindex="0" {attr_text}>{rewritten}{tooltip}</span>'


def build_html(items: List[Dict[str, Any]], title: str) -> str:
    grouped = group_by_section(items)
    sections_html: List[str] = []
    absolute_index = 0
    for section, section_items in grouped.items():
        spans = []
        for item in section_items:
            absolute_index += 1
            spans.append(sentence_span(item, absolute_index))
        sentence_html = "\n".join(spans)
        sections_html.append(
            f'''
            <section class="paper-section">
              <h2>{html.escape(section)}</h2>
              <p class="rewritten-paper">{sentence_html}</p>
            </section>
            '''
        )

    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      --bg: #f7f7f8;
      --paper: #ffffff;
      --ink: #202124;
      --muted: #5f6368;
      --accent: #2f6fed;
      --accent-soft: #e8f0fe;
      --warning: #9a6700;
      --warning-soft: #fff3cd;
      --border: #dadce0;
      --shadow: 0 16px 40px rgba(32, 33, 36, 0.16);
    }}

    * {{ box-sizing: border-box; }}

    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.65;
    }}

    main {{
      max-width: 1240px;
      margin: 0 auto;
      padding: 42px 20px 72px;
    }}

    header {{ margin-bottom: 24px; }}

    h1 {{
      margin: 0 0 8px;
      font-size: clamp(2rem, 4vw, 3rem);
      line-height: 1.1;
      letter-spacing: -0.04em;
    }}

    .subtitle {{
      margin: 0;
      color: var(--muted);
      max-width: 840px;
    }}

    .layout {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) 390px;
      gap: 22px;
      align-items: start;
    }}

    .paper-section {{
      background: var(--paper);
      border: 1px solid var(--border);
      border-radius: 22px;
      padding: 28px;
      margin: 0 0 22px;
      box-shadow: 0 4px 18px rgba(32, 33, 36, 0.05);
    }}

    h2 {{
      margin: 0 0 16px;
      font-size: 0.92rem;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.12em;
    }}

    .rewritten-paper {{
      font-size: 1.08rem;
      margin: 0;
    }}

    .mapped-sentence {{
      position: relative;
      display: inline;
      padding: 2px 3px;
      border-radius: 6px;
      background-image: linear-gradient(var(--accent-soft), var(--accent-soft));
      background-size: 100% 38%;
      background-repeat: no-repeat;
      background-position: 0 94%;
      cursor: help;
      outline: none;
    }}

    .mapped-sentence:hover,
    .mapped-sentence:focus,
    .mapped-sentence.active {{
      background: var(--accent-soft);
    }}

    .mapped-sentence.caution {{
      background-image: linear-gradient(var(--warning-soft), var(--warning-soft));
    }}

    .mapped-sentence.caution:hover,
    .mapped-sentence.caution:focus,
    .mapped-sentence.caution.active {{
      background: var(--warning-soft);
    }}

    .tooltip-card {{
      display: none;
      position: absolute;
      z-index: 20;
      left: 0;
      bottom: calc(100% + 12px);
      width: min(560px, calc(100vw - 48px));
      padding: 16px 18px;
      border: 1px solid var(--border);
      border-radius: 16px;
      background: #fff;
      color: var(--ink);
      box-shadow: var(--shadow);
      font-size: 0.9rem;
      line-height: 1.45;
    }}

    .tooltip-card::after {{
      content: "";
      position: absolute;
      left: 24px;
      top: 100%;
      border-width: 8px;
      border-style: solid;
      border-color: #fff transparent transparent transparent;
    }}

    .mapped-sentence:hover .tooltip-card,
    .mapped-sentence:focus .tooltip-card {{ display: block; }}

    .tooltip-kicker,
    .inspector-kicker {{
      display: block;
      margin-bottom: 10px;
      color: var(--accent);
      font-size: 0.76rem;
      font-weight: 800;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }}

    .tooltip-label,
    .inspector-label {{
      display: block;
      margin: 12px 0 4px;
      color: var(--muted);
      font-size: 0.76rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.06em;
    }}

    .tooltip-label.primary,
    .inspector-label.primary {{ color: var(--accent); }}
    .tooltip-label.warning,
    .inspector-label.warning {{ color: var(--warning); }}

    .tooltip-text,
    .inspector-text {{ display: block; }}

    .inspector {{
      position: sticky;
      top: 20px;
      background: var(--paper);
      border: 1px solid var(--border);
      border-radius: 22px;
      padding: 22px;
      box-shadow: 0 4px 18px rgba(32, 33, 36, 0.05);
    }}

    .inspector h2 {{ margin-bottom: 8px; }}
    .inspector .hint {{ color: var(--muted); margin: 0 0 16px; font-size: 0.95rem; }}
    .inspector-block {{ border-top: 1px solid var(--border); padding-top: 12px; margin-top: 12px; }}
    .hidden {{ display: none; }}

    @media (max-width: 980px) {{
      .layout {{ grid-template-columns: 1fr; }}
      .inspector {{ position: static; }}
      .tooltip-card {{ width: min(520px, calc(100vw - 48px)); }}
    }}

    @media print {{
      body {{ background: #fff; }}
      main {{ padding: 0; }}
      .layout {{ display: block; }}
      .paper-section, .inspector {{ box-shadow: none; break-inside: avoid; }}
      .tooltip-card {{ display: none !important; }}
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <h1>{html.escape(title)}</h1>
      <p class="subtitle">Hover or click any highlighted rewritten sentence. The review card shows the <strong>model paper's original sentence</strong> first, then the abstract function, optional model pattern, optional project original sentence, and rewritten sentence.</p>
    </header>
    <div class="layout">
      <div class="paper">
        {''.join(sections_html)}
      </div>
      <aside class="inspector" aria-live="polite">
        <h2>Sentence map</h2>
        <p class="hint">Hover or click a rewritten sentence to inspect its model sentence and rhetorical function.</p>
        <div class="inspector-block">
          <span class="inspector-kicker" id="inspector-kicker">No sentence selected</span>
          <span class="inspector-label primary">Model paper sentence</span>
          <span class="inspector-text" id="inspector-model">Select a sentence to view the model paper sentence.</span>
          <span class="inspector-label">Abstract function</span>
          <span class="inspector-text" id="inspector-function">—</span>
          <div id="pattern-block" class="hidden">
            <span class="inspector-label">Model pattern</span>
            <span class="inspector-text" id="inspector-pattern">—</span>
          </div>
          <div id="project-original-block" class="hidden">
            <span class="inspector-label">Project original sentence</span>
            <span class="inspector-text" id="inspector-project-original">—</span>
          </div>
          <span class="inspector-label">Rewritten sentence</span>
          <span class="inspector-text" id="inspector-rewrite">—</span>
          <div id="caution-block" class="hidden">
            <span class="inspector-label warning">Caution</span>
            <span class="inspector-text" id="inspector-caution">—</span>
          </div>
        </div>
      </aside>
    </div>
  </main>
  <script>
    const fields = {{
      kicker: document.getElementById('inspector-kicker'),
      model: document.getElementById('inspector-model'),
      functionText: document.getElementById('inspector-function'),
      pattern: document.getElementById('inspector-pattern'),
      patternBlock: document.getElementById('pattern-block'),
      projectOriginal: document.getElementById('inspector-project-original'),
      projectOriginalBlock: document.getElementById('project-original-block'),
      rewrite: document.getElementById('inspector-rewrite'),
      caution: document.getElementById('inspector-caution'),
      cautionBlock: document.getElementById('caution-block')
    }};

    function setText(el, text) {{ el.textContent = text || '—'; }}
    function toggleBlock(block, text) {{ block.classList.toggle('hidden', !(text && text.trim())); }}

    function inspectSentence(span) {{
      document.querySelectorAll('.mapped-sentence.active').forEach(s => s.classList.remove('active'));
      span.classList.add('active');
      const section = span.dataset.section || 'Draft';
      const idx = span.dataset.sentenceIndex || span.dataset.index || '';
      setText(fields.kicker, `${{section}} sentence ${{idx}}`);
      setText(fields.model, span.dataset.model);
      setText(fields.functionText, span.dataset.function);
      setText(fields.pattern, span.dataset.pattern);
      toggleBlock(fields.patternBlock, span.dataset.pattern);
      setText(fields.projectOriginal, span.dataset.projectOriginal);
      toggleBlock(fields.projectOriginalBlock, span.dataset.projectOriginal);
      setText(fields.rewrite, span.dataset.rewrite || span.textContent);
      setText(fields.caution, span.dataset.caution);
      toggleBlock(fields.cautionBlock, span.dataset.caution);
    }}

    document.querySelectorAll('.mapped-sentence').forEach(span => {{
      span.addEventListener('mouseenter', () => inspectSentence(span));
      span.addEventListener('focus', () => inspectSentence(span));
      span.addEventListener('click', () => inspectSentence(span));
    }});
  </script>
</body>
</html>
'''


def load_writing_map(path: Path) -> List[Dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("The writing map JSON must be a list of objects or tuples.")
    return [normalize_item(item, index + 1) for index, item in enumerate(data)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a writing_map JSON file as interactive HTML.")
    parser.add_argument("input", type=Path, help="Path to writing_map.json")
    parser.add_argument("-o", "--output", type=Path, default=Path("writing_map.html"), help="Output HTML path")
    parser.add_argument("--title", default="Reverse-Engineered Scientific Draft", help="HTML page title")
    args = parser.parse_args()

    items = load_writing_map(args.input)
    html_text = build_html(items, args.title)
    args.output.write_text(html_text, encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
