# Figure 1: Motivation And Problem Intuition

## Purpose

Figure 1 should let a broad AI reviewer answer three questions quickly:

1. What is the task?
2. What goes wrong or remains difficult?
3. Why does this paper need to exist?

It is a visual abstract of the problem, not a compressed method section.

## Strong Composition Patterns

### Same input, unstable outcomes

Use when equivalent prompts, perturbations, annotators, environments, or seeds produce meaningfully different predictions.

Composition: one shared example on the left, two or three equivalent conditions in the center, divergent outputs on the right, and one concise consequence.

### Current behavior versus desired behavior

Use when the paper fixes a recognizable failure.

Composition: shared input, a restrained "current" path showing the failure, and a visually stronger "desired" path showing the scientific goal. Avoid depicting the proposed architecture in the desired path.

### Hidden structure matters

Use when a flat representation loses hierarchy, topology, uncertainty, causality, temporal order, or compositional structure.

Composition: a real observation, its misleading flat view, and the latent organization that the task requires.

### Human/agent decision under uncertainty

Use for interactive learning, review, editing, RL, or agent-assistance papers.

Composition: uncertain model output, a small set of possible interventions, and the measurable downstream effect. Keep the loop conceptual.

### Benchmark blind spot

Use for evaluation/protocol papers.

Composition: one method appears stable under the conventional measurement, then the same evidence viewed under the proposed audit reveals variance, headroom, leakage, or a missing axis.

## Visual Evidence

Prefer a real example from the paper's evaluation set. Crop and simplify it while retaining semantic truth. Examples include:

- waveform plus spectrogram;
- source image plus prediction overlay;
- prompt variants plus model outputs;
- graph before and after a perturbation;
- trajectory with alternative actions;
- table fragment converted into an intuitive comparison.

Label whether a value is per-example, aggregate, illustrative, or hypothetical. Do not place an aggregate number next to a single example in a way that implies it was measured on that example.

## Rejection Tests

Redesign Figure 1 if any answer is yes:

- Does it require reading the method section first?
- Are there more than three visual stages?
- Does it contain a full encoder/backbone/loss pipeline?
- Is most of the canvas occupied by text or equally weighted boxes?
- Could the figure belong to almost any AI paper after replacing four labels?
- Is the main visual decorative rather than evidentiary?
- Does it repeat Figure 2's architecture?
- Is the problem still unclear when viewed in grayscale at column width?

## Caption Pattern

Write the caption in this order:

1. name the task or phenomenon;
2. explain the contrast shown;
3. identify the scientific consequence;
4. qualify any values or examples.

Do not narrate every arrow. The caption should add precision that the artwork cannot carry cleanly.
