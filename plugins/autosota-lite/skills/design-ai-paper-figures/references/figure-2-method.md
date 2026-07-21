# Figure 2: Method, Framework, Or Architecture

## Purpose

Figure 2 should let a technical reviewer identify:

- inputs and outputs;
- standard versus novel components;
- the main intermediate representation;
- where learning or optimization occurs;
- the objective and supervision;
- training/inference differences;
- the claimed technical contribution.

## Choose A Visual Grammar

### Representation transformation

Use for encoder, diffusion, transformer, multimodal, or feature-learning methods.

Show input modalities, representation geometry, the novel transformation, and output. Make tensor dimensions or token roles visible only where they clarify the contribution.

### Hierarchy or graph construction

Use for structural entropy, graphs, trees, clustering, retrieval, or multiscale models.

Show the raw affinity/feature structure becoming a graph or hierarchy, the optimization criterion acting on it, and how the resulting structure changes prediction or selection. Let the graph/tree carry the visual interest rather than surrounding it with many boxes.

### Iterative denoising or refinement

Use for diffusion, optimization, active learning, editing, and feedback systems.

Show a small number of meaningful states along a trajectory and place the learned score, policy, or feedback signal adjacent to the transition it controls.

### Agent/environment loop

Use for agents and RL.

Separate observation, internal state/memory, policy or planner, action, and environment transition. Show rewards, critiques, or human feedback on their actual edge. Distinguish training rollouts from deployment behavior.

### Candidate generation and selection

Use for reranking, prompt robustness, uncertainty, ensembling, or search.

Show one input yielding a structured candidate set, the proposed reference-free score or decision process, and the selected output. If an oracle is used only for evaluation, place it in a clearly separate audit lane.

### Training and inference braid

Use when supervision or auxiliary modules disappear at test time.

Use one shared central model, with a training lane above and inference lane below. Use solid lines for deployed computation and dashed lines for training-only signals.

## Hierarchy And Emphasis

Allocate visual weight in this order:

1. proposed novelty;
2. representation or operation the novelty changes;
3. input/output examples;
4. standard backbone;
5. auxiliary losses or implementation detail.

Do not give every module the same rectangle, border, and font weight. Standard components can be compact and muted. The novel mechanism should have the strongest shape, local detail, and annotation.

## Shapes And Lines

Use a consistent semantic legend:

- rounded or plain rectangles: learned modules;
- unfilled operators: deterministic transformations;
- stacked planes or strips: tensors/sequences;
- circles or small nodes: tokens, graph nodes, variables;
- solid arrows: inference/data flow;
- dashed arrows: supervision, optional, or training-only flow;
- brackets or background bands: stages, not decorative cards.

Adapt this legend to the domain, but never change a shape's meaning midway through the figure.

## Equations

Include only equations that expose the novelty or connect the diagram to the paper's notation. Prefer one local equation near the operation it defines over a detached equation panel.

- Use exactly the manuscript's symbols.
- Render vector equations; never use screenshots.
- Keep LaTeX source in the build workspace or figure notes.
- Define uncommon symbols in the caption.
- Check minus signs, superscripts, subscripts, and Greek glyphs after export.

## Rejection Tests

Redesign Figure 2 if any answer is yes:

- Is the novel component visually indistinguishable from a standard encoder?
- Does the diagram look like cloud infrastructure or a product workflow?
- Are there many equally weighted boxes with long prose labels?
- Are arrows crossing modules or labels?
- Is training-time information shown as available during inference?
- Are equations decorative or disconnected from the flow?
- Can a reviewer not locate the output or objective?
- Does the architecture contradict method-section notation?
- Is Figure 2 just a more detailed copy of Figure 1?

## Caption Pattern

Write the caption in this order:

1. name the method and its end-to-end purpose;
2. explain the novel mechanism and visual encodings;
3. distinguish training-only, inference, or audit paths;
4. define symbols and abbreviations not obvious from the artwork.
