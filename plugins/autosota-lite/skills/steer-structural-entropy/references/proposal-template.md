# Proposal Template

Use this outline when asked to produce an SE integration proposal.

## Title

`Structural-Entropy-Guided <abstraction/pooling/exploration/segmentation> for <baseline/project>`

## 1. Baseline And Gap

- What the baseline does.
- Where it handles structure, hierarchy, uncertainty, pooling, abstraction, exploration, or augmentation.
- Why the current mechanism may discard or fail to exploit multiscale structure.

## 2. SE Formulation

Define:

- `V`: base entities.
- `E`: interactions, transitions, affinities, or learned relations.
- `W`: edge weights and normalization.
- `2m`: total graph volume.
- `T`: encoding tree and what internal nodes mean.
- `H_1(G)`: baseline uncertainty.
- `H_T(G)`: hierarchy-conditioned uncertainty.
- `D_T(G) = H_1(G) - H_T(G)`: optional decoding information objective or metric.

State any departures from the undirected weighted setting.

## 3. Proposed Method

Describe the method as a small number of concrete components:

- Graph construction.
- Tree construction or differentiable assignment.
- Integration point in the baseline model/training loop.
- Added loss, reward, pooling operation, or data augmentation rule.
- Inference-time behavior.

Include pseudocode when useful:

```text
for each training epoch:
    build/update graph G from baseline representations
    estimate encoding tree T by SE minimization
    compute SE-guided modules/views/rewards/features
    optimize baseline objective plus SE objective
```

### 3b. Faithfulness Checklist

Before implementing, verify the proposed graph matches the paper spec on each dimension:

- [ ] Graph type: directed (use stationary-π) vs undirected (use degree/2m)
- [ ] Edge semantics: what relationship do edges represent? (entailment, transition probability, cosine similarity, spatial adjacency…)
- [ ] Edge weight normalization: row-stochastic, symmetric, raw counts?
- [ ] Tree construction: which operators? (merge/combine/split/lift/join); which level? (2D vs full tree)
- [ ] Entropy formula: 1D SE vs tree SE vs 2D SE; confirm V_alpha, g_alpha, 2m definitions
- [ ] Sign convention: lower entropy = more confident/structured; higher = uncertain/noisy
- [ ] K-constraint: free-k minimization or fixed-K? (free-k over-segments heterogeneous graphs)
- [ ] Reference implementation: use selib as cross-check to validate entropy computation independently

Failure to match the paper on graph construction is the most common cause of null results in SE reproduction. The SE formula is rarely wrong; the graph is almost always the problem.

## 4. Implementation Plan

For a repo:

- Name likely files or modules to inspect/change.
- Identify new utilities: graph builder, SE entropy calculator, tree optimizer, integration wrapper, tests.
- Specify configuration knobs: tree depth, update interval, entropy weight, graph sparsity, random seed.

For a paper-only baseline:

- Describe algorithmic changes at the level of equations, modules, and training steps.
- State what implementation assumptions are required.

## 5. Experiments

Minimum experiment set:

- Original baseline.
- Baseline plus SE integration.
- Ablation without entropy minimization.
- Ablation with random or heuristic hierarchy.
- Sensitivity to tree depth and entropy weight.
- Runtime/memory overhead.

Metrics:

- Task metric.
- Structural metric: `H_T`, decoding information, conductance, modularity, hierarchy stability, or abstraction purity.
- Robustness metric where relevant.

## 6. Risks

Address:

- Graph construction may encode spurious relations.
- SE optimization can be expensive.
- Differentiable assignments can collapse.
- Dynamic environments make trees stale.
- Improvement may come from added parameters rather than SE.

Add mitigations and falsification criteria.

## 7. Citations

Use relevant citations:

- Li & Pan 2016 for core SE math.
- Rosvall & Bergstrom 2008 for map-equation-style stochastic hierarchy/community search.
- Li 2024 for AI Science, encoding trees, strategy, decoding information, and 5D cognition when agent modeling is central.
- Su et al. 2025 survey for taxonomy and modern SE applications such as LSENet, SEP, SISA, SEGA, DeSE, Hi-PART, HCSE, SLED, or SIT-HSS.
- selib (github.com/SuuTTT/structural-entropy-benchmark) for validated reference optimizers (se_louvain, se_hier, se_gnn, se_optimize_fixed_k).
- Zhao et al. 2025 (SeSE, UAI 2026 Oral) for LLM UQ with directed semantic-graph SE.
- Pan et al. 2025 (HCSE) for two-level Louvain + tree SE construction used in SISA/SISL/SeSE long-form.
- Farquhar et al. 2024 (semantic entropy) as the baseline to beat in LLM UQ proposals.
