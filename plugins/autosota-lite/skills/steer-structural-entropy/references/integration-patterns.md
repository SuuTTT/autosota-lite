# Integration Patterns

## GNNs And Graph Representation Learning

Baseline limitation to target: heuristic pooling, local message passing without global hierarchy, oversquashing, loss of community semantics, or poor multiscale representation.

SE integration:

- Build `G` from the input graph, learned edge scores, or batched graph adjacency.
- Construct an encoding tree by SE minimization.
- Pool nodes according to modules in the tree.
- Pass module embeddings to higher GNN layers.
- Optionally add `H_T(G)` or decoding information regularization.

Proposal variants:

- Precompute SE tree for static graphs.
- Recompute tree periodically for dynamic learned graphs.
- Use differentiable SE pooling for end-to-end graph classification.

Experiments:

- Compare against TopKPool, DiffPool, ASAP, SAGPool, Graph U-Net, or domain baselines.
- Ablate tree depth, entropy objective, graph construction, hard vs soft assignments, and update frequency.
- Report accuracy plus hierarchy quality metrics such as modularity, conductance, tree entropy, and stability.

**Ablation caveat (2025 reproduction finding):** In graph pooling (SEP), shape-matched random coding trees and even fully shape-free random trees match SE tree performance on PROTEINS and NCI1. The benefit of multi-level pooling architecture is confirmed; the benefit of SE-specific membership or geometry is not. Plan ablations against shape-matched random trees before claiming that SE membership or geometry is the operative factor.

## Contrastive Learning And Data Augmentation

Baseline limitation to target: random edge/node dropping can remove semantic structure or create false positives/negatives.

SE integration:

- Build an SE encoding tree from the graph or sample affinity graph.
- Generate a stable anchor view by preserving low-entropy modules and high-decoding-information edges.
- Use SE-guided augmentations that perturb noisy/high-entropy parts while retaining structural cores.
- Weight positives by module proximity in the tree.

Experiments:

- Compare against random drop, feature masking, subgraph sampling, GraphCL, BGRL, or project-specific augmentations.
- Ablate anchor view only, SE-guided perturbation only, and combined objective.
- Measure downstream accuracy, representation stability, and robustness to graph noise.

## Reinforcement Learning

Baseline limitation to target: sparse rewards, inefficient exploration, enormous state spaces, weak abstraction, or brittle options.

State abstraction:

- Build a state-transition graph where vertices are states or learned latent states.
- Edge weights are transition counts, probabilities, visitation flow, or learned successor affinity.
- Minimize SE to cluster microscopic states into macro-states.
- Use macro-state IDs as abstract observations, option states, planning nodes, or replay strata.

Intrinsic motivation:

- Reward actions that reduce structural uncertainty or increase decoding information.
- A candidate intrinsic reward:

```text
r_int(t) = eta * max(0, D_T_new(G_t) - D_T_old(G_{t-1}))
```

Guardrails:

- Normalize by graph growth to avoid rewarding trivial expansion.
- Update the SE tree on a schedule, not every environment step, unless the graph is small.
- Report performance with and without extrinsic rewards.

Experiments:

- Compare sample efficiency, final return, coverage, and abstraction stability.
- Ablate graph construction, update period, tree depth, and intrinsic reward scale.

**Honest null results (2025 reproduction):**

- *SISA state abstraction (DMControl RAD-SAC, 6 tasks, 2 seeds):* Markov macro-state abstraction vs baseline — tied 3-3, average return slightly lower (682 vs 642). No clear benefit from SE state abstraction in continuous-control RL at this scale.
- *SISL skill learning (MuJoCo Fetch, HCSE regulariser on skill-VAE latent):* SI-on vs SI-off — BC_loss 0.3017 vs 0.3066 (wash, <2%), NVP slightly worse with SI. Structural regularisation in the skill-VAE latent space produced no meaningful gain at 30 epochs / 500 demos.
- *SIRD role discovery:* Long-schedule runs show no statistically significant gain over baseline in coordinated multi-agent scenarios.
- *Ablation (SI2E exploration bonus):* Granularity-matched random clusters match SE clusters on DoorKey-8×8 (random 0.96 mean, SE 0.92 mean); on hard env both arms are bimodal — seed stochasticity, not cluster choice, drives the outcome.

Conclusion: SE-based RL components are most effective in easy sparse-reward tasks; on harder tasks or continuous control, validate per-task and across multiple seeds before adoption. Multi-scale structure matters more than SE-optimal membership.

## Computer Vision

Baseline limitation to target: flat segmentation, label inefficiency, weak object hierarchy, or noisy region merging.

SE integration:

- Convert image/video to a superpixel or region graph.
- Vertices are superpixels, patches, objects, or tracked regions.
- Edge weights combine boundary strength, color/texture similarity, spatial adjacency, motion, or feature affinity.
- Use SE minimization to build a region hierarchy.
- Feed hierarchy into segmentation, detection, or representation learning.

Experiments:

- Compare against conventional superpixel merging, graph cuts, spectral clustering, or model-specific segmentation modules.
- Report mIoU, boundary F-score, object consistency, hierarchy stability, and label-efficiency curves.

## LLM Uncertainty Quantification

Baseline limitation to target: semantic entropy (flat clustering of sampled answers) discards hierarchical structure; cosine-similarity graphs conflate verbose-but-wrong answers with correct ones.

SE integration (SeSE pattern, Zhao et al. 2025):

- Sample N answers to a question from the LLM (N=10 typical).
- Build a **directed** semantic graph: nodes = answers; directed edges weighted by NLI entailment probability (premise→hypothesis, not symmetric).
- Compute stationary distribution π from the random walk on this graph.
- Build an encoding tree T by merge/combine operators (or selib `se_louvain`).
- Use `H_T(G)` as the uncertainty score: low entropy = answers cluster tightly = confident; high entropy = scattered answers = uncertain/hallucinating.

Key design choices:

- **Graph construction is the primary lever.** Cosine-similarity edges make all LLM answers look similar regardless of semantic agreement — the graph must use NLI entailment or an equivalent asymmetric semantic measure.
- **Directed vs undirected.** Use directed (stationary-π) formulation; undirected approximation can flip entropy ordering and produce sub-chance AUROC.
- **Sign convention.** Lower SE = more confident. High SE = uncertain. Fix and document the sign before any cross-dataset comparison.
- **K-constrained tree.** If answer count is small (N=10), free-k SE may over-segment. Try K=2 (binary: consistent vs inconsistent cluster) as a starting point.

Experiments:

- Compare against semantic entropy (Farquhar et al. 2024), p_true, length-normalized entropy, and discrete cluster entropy.
- Evaluate AUROC on factual QA (TriviaQA, NQ), arithmetic reasoning (GSM8K, SVAMP), and long-form claim generation separately — performance profiles differ by regime.
- Report results for each dataset under a single fixed sign convention.
- **Regime expectations (2025 reproduction):** factual QA — faithful SeSE beats semantic entropy by 0.07–0.16 AUROC; reasoning (GSM8K) — SE-family methods weak (p_true 0.833 dominates); long-form — flat baselines beat structural methods. Report regime-conditional performance honestly.

Reproducibility note: the official SeSE codebase used cosine-sim (not NLI entailment) and undirected graphs — reproducing the paper requires reimplementing the graph construction per the paper's spec, not the released code. Run selib as a cross-check to validate the signal independently.

## Skill Learning

Baseline limitation to target: skill discovery from demonstrations lacks an explicit structural prior; learned skill embeddings may not reflect multi-scale temporal or semantic organization.

SE integration (SISL pattern):

- Model the skill latent space as a graph: nodes = skill embeddings or trajectory segments; edges = temporal adjacency, semantic similarity, or HCSE community links.
- Apply HCSE as a regulariser on the skill-VAE latent space: encourage the latent distribution to respect community structure in the encoding tree.
- Use decoding information `D_T` as an auxiliary training signal to maximize the structural information captured by the skill representation.

Honest expectation: reproducing HCSE-regularised skill learning (SISL, MuJoCo Fetch) at small scale (500 demos, 30 epochs) shows no statistically significant gain over the SE-free baseline. The regulariser may require more data or longer training to manifest. Propose ablations that vary demo count and training length.

Experiments:

- Compare BC loss, NVP loss, and downstream task success rate with SI-on vs SI-off.
- Ablate: HCSE vs random tree regularizer; training epochs 30 vs 200.
- Report demo-efficiency curves across 3+ seeds.

## Bioinformatics

Baseline limitation to target: flat chromatin domain detection misses hierarchical organization; single-scale TAD callers can't resolve nested domains at different resolution.

SE integration (SuperTAD / deDoc pattern):

- Build a Hi-C contact frequency graph: nodes = genomic bins; edge weights = contact frequency (normalized by expected).
- Minimize `H_T(G)` to find the encoding tree whose leaves are individual bins and whose internal nodes are TADs at different scales.
- Read off hierarchical TAD boundaries as the tree's level structure.

Verified: SuperTAD reproduces on real Hi-C (GM12878, IMR90, chr19, 25kb) — coherent hierarchical domains recovered end-to-end from original code. deDoc processes 10^4 nodes in 74s (not computationally infeasible as sometimes claimed).

Experiments:

- Compare against Armatus, Topdom, or domain-size-matched baselines.
- Evaluate boundary precision/recall at each resolution level.
- Report runtime scaling: SuperTAD2's matrix-discretization variant substantially reduces cost for large genomes.

## General Neural Architecture Or Foundation Model Use

Use only when a meaningful graph exists. Candidate graphs include attention graphs, token co-occurrence graphs, module dependency graphs, retrieval graphs, concept graphs, or activation-neighborhood graphs.

Good proposal targets:

- SE regularization for attention sparsity and hierarchy.
- SE-based clustering of tokens, patches, experts, memories, or tools.
- Encoding-tree-based routing or compression.

Risks:

- Added hierarchy may be an expensive proxy for simpler regularizers.
- Learned graphs can be unstable early in training.
- Tree construction can become a training bottleneck.

Mitigations:

- Warm-start with frozen graph features.
- Update the hierarchy every `K` steps.
- Use sparse approximations and cap tree depth.
- Start with an offline analysis before changing training.
