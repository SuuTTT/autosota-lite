---
name: autosota-agent-objective
description: Implement AgentObjective from AutoSOTA to construct a tree-structured evaluation rubric. This skill maps macro research goals into dense, quantifiable feedback.
---

# AutoSOTA AgentObjective: Automated Objective Rubric Construction

Use this skill to convert unstructured literature (PDF/Text) and codebases into a machine-verifiable evaluation hierarchy.

## Core Responsibilities

1. **Tree-Structured Recursive Decomposition**: 
   - Start from a root goal (e.g., "Full Replication").
   - Perform BFS-style expansion to decompose parent goals into binary (Pass/Fail) sub-tasks.
   - Categorize nodes: `Result Match`, `Methodology Implementation`, `Environment Configuration`, `Metric Correctness`.

2. **Hierarchical Context Injection**:
   - **Shallow**: Abstracts, ToC, Introduction for strategic goals.
   - **Intermediate**: Methodology, Tables, Figures for algorithmic facets.
   - **Deep**: Repository-level context (preprocess, utils) for atomic engineering logic.

3. **Metric Grounding**:
   - Extract the exact target value $g^*$ and metric type from tables.
   - Identify data splits (train/val/test) and reporting protocols (e.g., "Best of 5").

## Output
A `rubric.json` or `rubric.md` file detailing the verification points.
