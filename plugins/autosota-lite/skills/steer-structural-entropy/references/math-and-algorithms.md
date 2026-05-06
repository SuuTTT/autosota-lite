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

## References To Cite

- Li, A., & Pan, Y. (2016). Structural information and dynamical complexity of networks. IEEE Transactions on Information Theory.
- Rosvall, M., & Bergstrom, C. T. (2008). Maps of random walks on complex networks reveal community structure. PNAS.
- Li, Angsheng (2024). Artificial Intelligence Science: The Mathematical Principles of Intelligence.
- Su, D., et al. (2025). A Survey of Structural Entropy: Theory, Methods, and Applications. IJCAI.
