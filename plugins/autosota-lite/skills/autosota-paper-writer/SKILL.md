---
name: autosota-paper-writer
description: Draft, revise, and export ML research manuscripts from AutoSOTA artifacts, experiment logs, methods, results, references, and model-paper writing patterns, including LaTeX paper directories and human-readable reports.
---

# AutoSOTA Paper Writer

## Purpose
Automate the drafting of high-quality ML research papers by analyzing project artifacts (results, methodology, code) and following established patterns from top-tier conference publications (NeurIPS, ICLR, etc.).

## Context Reference
Refer to high-star repository patterns (e.g., standard LaTeX templates, Overleaf integrations, and common section structures).

## Modes

### 1. Abstract & Introduction
Draft the core narrative, motivation, and problem statement. Highlight the "SOTA" contribution.

### 2. Methodology
Translate code and algorithmic descriptions into formal LaTeX-formatted methodology sections.

### 3. Results & Evaluation
Generate tables and figure captions from `scores.jsonl` and `logs/`.

### 4. Bibliography
Automatically manage `.bib` files based on references found in the codebase and `research_report.md`.

## Workflow
1. Read `research_report.md` and `objective.md`.
2. Analyze `scores.jsonl` for experimental data.
3. Generate LaTeX source files in a `paper/` directory.
