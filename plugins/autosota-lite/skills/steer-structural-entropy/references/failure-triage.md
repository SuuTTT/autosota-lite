# Task Alignment, Null Triage, And Confirmation

Use this reference before committing compute and whenever an SE experiment is null.

## 1. Task-Graph Alignment

SE minimizes the expected coding cost of a random walk under an encoding tree. It does not optimize an arbitrary downstream metric. Specify:

- the node entity and graph scale;
- the semantics of one random-walk transition;
- the task information expected to remain within low-cut modules;
- the mechanism connecting lower `H_T` to the task metric;
- nuisance variables likely to create stronger communities than the target signal.

Prefer graphs whose edge semantics are native to the task: environment transitions for state abstraction, spatial adjacency for segmentation, entailment for semantic consistency, or model-latent interactions for representation learning. Similarity alone is insufficient justification.

## 2. Conditional-Value Gate

Before a large model, compare SE features with:

- raw edge weights and node degrees;
- pairwise similarity summaries and dispersion;
- matched K-means, spectral, modularity, or Laplacian features;
- shape- and granularity-matched random trees.

Use group-disjoint validation. Continue only when SE adds stable predictive value beyond these controls. A lower `H_T` without a downstream gain demonstrates compressibility, not task usefulness.

## 3. Executable Faithfulness Checks

- Match entropy values against exhaustive partitions on tiny weighted graphs.
- Verify two-level tree entropy equals the corresponding partition entropy.
- Check every accepted optimizer move monotonically lowers the exact objective.
- Test node-permutation invariance.
- For directed graphs, test dangling nodes, strong connectivity, stationary-distribution residual, and edge-direction reversal.
- Verify graph insertion or inductive prediction cannot inspect held-out labels.

## 4. Null Triage

Diagnose four independent failure families:

1. **Implementation:** formula, normalization, cut, volume, tree, or sign error.
2. **Optimization:** local minima, collapse, wrong resolution, or unstable hierarchy.
3. **Representation:** edges encode nuisance similarity or discard task-relevant information.
4. **Objective alignment:** the graph is valid and compressible, but low structural entropy does not imply better task utility.

Evidence can isolate them. A nontrivial hierarchy rules out only the claim that no hierarchy exists. A stronger optimizer that lowers `H_T` but not the task metric points to objective alignment, not implementation.

## 5. Development And Confirmation Firewall

Freeze before each run:

- hypothesis and primary comparison;
- data and artifact hashes;
- group-disjoint splits;
- hyperparameter search space;
- metric, uncertainty procedure, success threshold, budget, and stopping rule.

Once outcomes are inspected, that pool is development data. Do not call subsequent tuning on it confirmation. Promote one frozen candidate only after a positive development gate, then evaluate once on a fresh dataset, architecture, environment, or prospectively held-out split.

Report nulls with exact effects and intervals. Stop post-hoc variants when the preregistered primary comparison fails decisively.
