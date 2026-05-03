---
name: structural-entropy-proposal
description: Use when asked to propose, design, or assess an integration of Structural Information Theory, Structural Entropy (SE), encoding trees, decoding information, or SE-based hierarchy discovery in a baseline AI paper, codebase, repository, model, algorithm, or experiment. Helps agents inspect a project and produce a rigorous SE integration proposal with math, implementation options, experiments, risks, and citations.
metadata:
  short-description: Propose SE integrations for AI projects
---

# Structural Entropy Proposal

Use this skill to turn a baseline paper, repo, or AI method into a concrete proposal for integrating Structural Entropy (SE). The expected output is a research or engineering proposal, not a vague literature summary.

## Workflow

1. **Understand the baseline**
   - Identify the project type: GNN, graph learning, RL, self-supervised learning, vision, language/model architecture, optimization, planning, or other.
   - Extract the baseline's core objects: states, nodes, samples, tokens, modules, transitions, losses, pooling/abstraction steps, exploration strategy, or augmentation pipeline.
   - Find where the baseline already builds or could build an information system: graph `G = (V, E, W)`, transition matrix, affinity matrix, attention graph, kNN graph, superpixel graph, state graph, module graph, or hypergraph.

2. **Map the baseline to SE**
   - Define vertices, edges, weights, and volume. State assumptions for directed, weighted, dynamic, or learned graphs.
   - Define the candidate encoding tree `T`: leaves are base entities; internal nodes are modules, communities, macro-states, clusters, concepts, or hierarchy levels.
   - Decide whether the integration uses discrete SE optimization, a fast stochastic heuristic, or differentiable soft assignment.
   - Use [references/math-and-algorithms.md](references/math-and-algorithms.md) when formulas, operators, or reproducible calculation details are needed.

3. **Choose the integration paradigm**
   - For graph representation learning or GNN pooling, consider SE-guided pooling or hierarchy construction.
   - For contrastive learning, use an SE-stable anchor view or SE-aware augmentation policy.
   - For RL, use SE state abstraction, SE intrinsic motivation, or SE-based option discovery.
   - For vision, construct a superpixel/region graph and use SE minimization for hierarchical segmentation or multiscale features.
   - For end-to-end neural methods, use differentiable SE with a soft assignment matrix and add an SE regularizer or hierarchy module.
   - Use [references/integration-patterns.md](references/integration-patterns.md) for concrete patterns and proposal language.

4. **Write the proposal**
   Include:
   - Baseline summary and the specific limitation SE addresses.
   - SE formulation: graph construction, encoding tree, entropy objective, and decoding information if useful.
   - Proposed method: modules changed, losses added, algorithms inserted, computational cost, and training/inference behavior.
   - Implementation plan: files/components to modify if a repo is available; pseudocode if only a paper is available.
   - Experiments: datasets/tasks, baselines, ablations, metrics, statistical checks, and expected failure modes.
   - Risks and mitigations: graph quality, scalability, differentiability, non-stationarity, over-clustering, and added hyperparameters.
   - Citations: foundational SE theory, survey/application papers, and any domain-specific SE method.
   - Use [references/proposal-template.md](references/proposal-template.md) for a compact structure.

## Quality Bar

- Be explicit about what `V`, `E`, `W`, `2m`, `V_alpha`, `g_alpha`, and `T` mean in the target project.
- Do not claim SE improves results without proposing experiments that could falsify the claim.
- Separate implementable changes from speculative research extensions.
- For repos, inspect code before proposing file-level edits. Match existing model, data, and training abstractions.
- For papers, distinguish directly supported claims from hypotheses inferred from the SE framework.
- If current citations or paper details are needed, browse or use scholarly sources rather than relying on memory.

## Reference Files

- [references/math-and-algorithms.md](references/math-and-algorithms.md): SE definitions, entropy formulas, optimization operators, stochastic search, differentiable variants.
- [references/integration-patterns.md](references/integration-patterns.md): domain-specific SE integration patterns for GNNs, contrastive learning, RL, and vision.
- [references/proposal-template.md](references/proposal-template.md): reusable proposal outline and checklists.
