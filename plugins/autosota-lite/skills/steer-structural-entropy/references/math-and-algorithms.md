# Math And Algorithms

## Core Objects

Model the environment, dataset, model, or behavior as an information system:

- `G = (V, E, W)`: directed or undirected weighted graph.
- `A`: irreducible non-negative matrix when the system is naturally represented by affinities, transitions, attention, influence, or co-occurrence.
- Encoding tree `T`: rooted tree with root `lambda`; leaves are base entities; internal nodes are modules, abstractions, communities, macro-states, or concepts.
- Decoding information: `D_T(A) = H_1(A) - H_T(A)`, the uncertainty eliminated by tree `T`.

For weighted graphs, replace degree and cut counts with weighted volume and weighted cut. For directed graphs, state whether volume uses in-degree, out-degree, total degree, or stationary random-walk mass.

## 1D Structural Entropy

For undirected graph `G` with degree `d_i` and total volume `2m = sum_i d_i`:

```text
H_1(G) = - sum_i (d_i / 2m) log2(d_i / 2m)
```

Interpretation: baseline uncertainty of locating a random-walk step by node identity.

## Tree Structural Entropy

Given encoding tree `T`:

```text
H_T(G) = - sum_{alpha in T, alpha != lambda}
          (g_alpha / 2m) log2(V_alpha / V_parent(alpha))
```

Definitions:

- `V_alpha`: volume of module `alpha`, the sum of base-node degrees inside `alpha`.
- `V_parent(alpha)`: volume of `alpha`'s parent in the encoding tree.
- `g_alpha`: cut of module `alpha`, the number or total weight of edges leaving `alpha`.

Optimization objective:

```text
T* = argmin_T H_T(G)
```

The optimal tree is the knowledge tree or hierarchy that best compresses structural uncertainty.

## Heuristic Tree Operators

Use when the project can tolerate discrete hierarchy construction before or during training.

Initialize `T` with all base nodes as leaves under root. Repeatedly evaluate local tree edits and apply the edit with the largest positive entropy decrease:

```text
Delta = H_T - H_T_new
apply edit if Delta > 0
stop when no edit reduces H_T
```

Operators:

- Merging: combine two leaves into a new module.
- Combining: combine sibling modules into a larger module.
- Splitting: divide a module into submodules.
- Lifting: move a node/module upward to reduce unnecessary depth.
- Joining: move a node/module into another branch when it lowers entropy.

Proposal guidance: specify which operators are required for the first version. A practical initial implementation often starts with merge/combine and adds split/lift/join after proving value.

## Fast Stochastic Search

Use for large graphs where exact or exhaustive tree edits are too expensive.

Louvain-like recursive procedure:

1. Start with each node in its own module.
2. Visit nodes in random order.
3. Move each node to the neighboring module with the largest decrease in SE or a related map-equation objective.
4. Repeat until no single-node move improves the objective.
5. Compress modules into supernodes and recurse to build higher tree levels.

This is appropriate for million-edge graphs, online approximation, and precomputing hierarchies for downstream learning.


Design choices to specify:

- fixed graph vs learned graph,
- one-level pooling vs multi-level tree,
- hardening schedule for assignments,
- computational complexity of dense vs sparse assignment,
- stability constraints to avoid collapsed clusters.

## Directed Graph SE

For directed graphs, replace degree and volume with stationary-distribution mass from a random walk:

1. Compute transition matrix `P`: `P[i,j] = W[i,j] / sum_k W[i,k]`.
2. Solve for the stationary distribution `π` (left eigenvector for eigenvalue 1; normalize so `sum_i π_i = 1`).
3. Define flow matrix `F[i,j] = π_i * P[i,j]`.
4. Replace `d_i / 2m → π_i` in 1D SE, and `V_alpha / 2m → sum_{i in alpha} π_i`, `g_alpha / 2m → sum_{i in alpha, j not in alpha} F[i,j]` in tree SE.

This formulation is used by SeSE (Zhao et al. 2025) for LLM semantic graphs where edges carry asymmetric NLI-entailment probabilities. The undirected approximation can flip the entropy ordering. Always state which formulation the proposal uses.

## B. HCSE (Hierarchical Community Structural Entropy) and selib

HCSE (Pan et al. 2025) is a two-level construction:

- Phase 1: Run Louvain to obtain an initial community partition `C`.
- Phase 2: Build a module-level graph from `C`, then compute `H_T` where the internal node is the community level and leaves are base nodes.

HCSE is used in SISA (state abstraction), SISL (skill learning), and SeSE (long-form claim graphs).

**selib** (Su et al. 2025) is a pip-installable library of standardized SE optimizers cross-validated to 1.8e-15 against a reference implementation:

- `se_louvain`: multilevel 2D-SE minimizer; beats CoDeSEG (WWW 2025) and deDoc on all 6 benchmark graphs.
- `se_hier`: encoding-tree optimizer warm-started from Paris; reaches lower `H_T` than both BBM and HCSE on every graph tested.
- `se_gnn`: differentiable 2D-SE with Sinkhorn balanced-assignment head; prevents the cluster collapse that pure SE minimization induces.
- `se_optimize_fixed_k`: K-constrained optimizer; lifts ARI from 0.53 to 0.77 on LFR at μ=0.3 and recovers karate-club two-faction split at ARI 0.88 vs free-k ARI 0.29.

Cite selib alongside the survey: github.com/SuuTTT/structural-entropy-benchmark.

## Resolution Control: Free-k Over-Segmentation

Free-resolution SE over-segments graphs with heterogeneous degree distributions:

- Karate club: free-k SE → 6 groups (ARI 0.29 vs the two known factions); K-constrained SE → ARI 0.88 (above Infomap 0.77, Louvain 0.51).
- LFR μ=0.3: free-k ARI 0.53; K-constrained ARI 0.77; K-constrained overtakes classical baselines at μ=0.4.

Design rule: if the target cluster count K is known or estimable, use `se_optimize_fixed_k`. If K is unknown, use multilevel minimization (`se_louvain`) but validate on a calibration set with known community structure.

## Graph Construction Primacy

SE is only as good as the graph it receives. Empirical finding from SeSE LLM UQ reproduction:

- Using cosine-similarity sentence-embedding edges: all verbose LLM answers cluster together → entropy near-constant → no discriminative signal.
- Using directed NLI-entailment edges (matching the paper spec): confident answers concentrate in one dense module (low SE) while hallucinating answers fragment into disconnected modules → strong signal; faithful SeSE beats semantic-entropy baseline by 0.07–0.16 AUROC across 3 datasets.

Lesson: inspect and validate the graph-construction step before attributing results to the SE formula. A faithful paper-code match on the graph definition is the primary predictor of whether the integration will work.

## References To Cite

- Li, A., & Pan, Y. (2016). Structural information and dynamical complexity of networks. IEEE Transactions on Information Theory.
- Rosvall, M., & Bergstrom, C. T. (2008). Maps of random walks on complex networks reveal community structure. PNAS.
- Li, Angsheng (2024). Artificial Intelligence Science: The Mathematical Principles of Intelligence.
- Su, D., et al. (2025). A Survey of Structural Entropy: Theory, Methods, and Applications. IJCAI.
- Pan, Y., et al. (2025). HCSE: Hierarchical Community Structural Entropy for Graphs.
- Zhao, Y., et al. (2025). SeSE: Semantic Structural Entropy for LLM Uncertainty Quantification. UAI 2026 Oral.
