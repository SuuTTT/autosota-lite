---
name: design-ai-paper-figures
description: "Design, redraw, audit, or prepare a production handoff for the first two figures of an AI/ML conference paper: an intuitive Figure 1 motivation/problem overview and an informative Figure 2 method/framework/architecture figure. Use for AAAI, NeurIPS, ICML, ICLR, CVPR, ACL, ACM, IEEE, or journal manuscripts when an AI agent or researcher needs conference-grade paper visuals, editable PowerPoint masters, PDF/PNG exports, LaTeX-ready figures, or a self-contained prompt for a presentation-capable tool. Adapt the workflow to the agent's image-generation, presentation-control, rendering, and file-editing capabilities."
---

# Design AI Paper Figures

Create a coordinated figure pair with different jobs:

- **Figure 1 earns attention:** explain the task, failure, or scientific motivation in one glance.
- **Figure 2 earns trust:** expose the proposed method's actual novelty, information flow, and outputs.

Treat these roles as defaults. If the target venue or paper uses a different figure order, preserve the roles while adapting the numbering.

## Route By Available Capabilities

Inspect the current agent's actual tools before promising artifacts. Determine whether the environment has:

- **presentation control:** create and edit native PowerPoint or an equivalent slide format;
- **image generation:** create or edit raster assets;
- **render/export:** render slides and export PDF/PNG;
- **file and manuscript access:** read the paper, evidence, and venue template.

Do not assume a branded tool, plugin, GUI, or API exists. Choose the first matching route:

1. **Presentation control + image generation:** build the editable master and generate only the isolated visual assets that need it.
2. **Presentation control without image generation:** build with native shapes, text, plots, and real paper assets. For any missing illustrative asset, add a clearly marked placeholder and provide a precise asset-generation prompt; do not fabricate the image.
3. **Image generation without presentation control:** generate isolated assets only when useful, then produce a complete assembly prompt for a presentation-capable tool. Do not claim that an editable deck was created. Put the fenced handoff prompt before any optional asset summary.
4. **Neither capability, including a text-only or CLI agent:** analyze the science and formulate both figure briefs, but place those briefs inside the self-contained production prompt. The response format is: one sentence naming the missing capability; the complete fenced prompt; one sentence asking the user to run it in a presentation-capable environment and attach the listed inputs. Do not output standalone briefs, ASCII layouts, recommendations, evidence ledgers, or unresolved questions before the prompt.

If rendering is unavailable, do not claim visual QA passed. Include the unperformed QA steps in the handoff.

Read [Capability routing and handoff](references/capability-routing-and-handoff.md) whenever the full editable-master route is unavailable.

**Hard completion check for routes 3 and 4:** the first substantive deliverable must be a fenced block whose first line is exactly `You are designing two coordinated, conference-grade figures for an AI/ML paper.` Copy and fill the production prompt template from the handoff reference. Put the figure briefs, evidence ledger, unresolved items, asset prompts, and QA instructions inside that block. Before returning, verify that exact first line exists inside a code fence.

## Read Before Designing

Read the manuscript, verified result tables, target venue template, and any user-supplied reference papers. Extract:

1. the paper's one-sentence problem;
2. the central failure or unmet need;
3. the proposed technical contribution;
4. the inputs, outputs, supervision, and objective;
5. the strongest verified evidence;
6. the final single- or double-column dimensions.

Do not infer unsupported model components or invent quantitative results. Mark unresolved scientific content as a question in the design brief, not as visible figure text.

Read these references as needed:

- [Figure 1 patterns](references/figure-1-motivation.md)
- [Figure 2 patterns](references/figure-2-method.md)
- [Editable PowerPoint construction](references/editable-powerpoint.md)
- [Paper-scale QA](references/paper-scale-qa.md)

## Write Two Figure Briefs

Before drawing, write a compact brief for each figure containing:

- **claim:** one sentence the reader should remember;
- **visual grammar:** the chosen composition pattern;
- **objects:** every semantic object that must appear;
- **labels:** short reader-facing text, usually noun phrases;
- **evidence:** any displayed value and its exact source;
- **caption contract:** what the caption must explain beyond the artwork;
- **size:** target width and aspect ratio in the manuscript.

Reject a brief if Figure 1 and Figure 2 tell the same story or reuse the same composition.

## Design Figure 1: Motivation

Make Figure 1 understandable to a general AI reviewer before they know the method.

1. Show one concrete input, ambiguity/failure, and consequence or desired behavior.
2. Prefer real domain evidence: an actual waveform, image, graph, prompt, prediction, trajectory, or data example.
3. Use at most three conceptual stages and one dominant reading direction.
4. Keep technical internals out unless one mechanism is necessary to understand the problem.
5. Use little text. Let contrast, correspondence, and failure examples carry the explanation.
6. Include numbers only when verified and essential to the motivation; distinguish aggregate values from examples.

Do not fill space with decorative icons, repeated boxes, a miniature method pipeline, or a dense taxonomy. See the Figure 1 reference for patterns and rejection tests.

## Design Figure 2: Method

Make Figure 2 sufficiently technical that a reviewer can reconstruct the method's logic.

1. Establish a visible spine from inputs through the novel computation to outputs/objective.
2. Give the paper's novelty the largest visual weight, not the input encoder or standard backbone.
3. Distinguish data, learned modules, deterministic operations, losses, and optional paths through shape and line semantics.
4. Show tensor, graph, hierarchy, temporal, or spatial structure where it matters; do not reduce everything to rectangles.
5. Separate training-only and inference-time paths when they differ.
6. Render equations correctly and define every symbol in the figure or caption.
7. Include enough detail to connect the diagram to method-section notation without reproducing the full algorithm.

Avoid "box soup": many equally weighted rounded rectangles connected by arrows. See the Figure 2 reference for architecture-specific patterns.

## Build An Editable Master

When presentation control is available, use its native shape, text, connector, media, and export operations and follow [Editable PowerPoint construction](references/editable-powerpoint.md). Do not require a specific vendor or agent platform.

Required deliverables unless the user narrows the request:

- one editable `.pptx` with one slide per figure;
- vector `.pdf` exports for LaTeX;
- 300 dpi `.png` previews;
- concise captions and optional `figure*.tex` wrappers;
- a source/evidence ledger for nontrivial visual assets and displayed values.

Keep all labels, arrows, shapes, and simple plots editable. Use a raster asset only for a real example or a semantic illustration that cannot reasonably be reconstructed. Never place a generated full-figure image into PowerPoint and call it editable. If image generation is available and helps establish a visual concept, generate individual isolated elements on transparent backgrounds and rebuild the composition with native shapes and text.

When presentation control is unavailable, do not substitute an uneditable mockup for the required master. Return the production handoff defined in [Capability routing and handoff](references/capability-routing-and-handoff.md).

## Apply Conference Styling

- Use a white or near-white background unless the manuscript has a validated dark style.
- Use one neutral ink color, one primary accent, and at most one secondary accent.
- Use colorblind-safe colors and never encode meaning by color alone.
- Keep borders thin, corners modest, arrows consistent, and whitespace functional.
- Avoid slide-title banners, UI cards, pills, gradients, shadows, decorative blobs, and clip-art aesthetics.
- Use sentence case and short labels. Avoid prose paragraphs inside the figure.
- Size text for the final printed figure, not for a full-screen slide.
- Match notation, terminology, colors, and object identity across both figures.

## Validate At Paper Scale

When rendering and manuscript compilation are available, follow [Paper-scale QA](references/paper-scale-qa.md). At minimum:

1. render the PPTX and inspect every slide;
2. export and inspect the PDF at final manuscript width;
3. test a grayscale version and a common color-vision-deficiency simulation;
4. verify no clipping, accidental overlap, crossing labels, malformed equations, or tiny text;
5. verify every visible claim against the manuscript or result artifact;
6. insert both figures into the paper and compile the affected pages;
7. inspect the full page, not only the standalone figure;
8. ask whether a reviewer can state Figure 1's problem and Figure 2's novelty after a five-second glance.

Iterate until the figures pass both visual QA and scientific-content QA. Do not deliver a first draft merely because it compiles. If the current environment cannot perform a check, mark it pending and include it verbatim in the handoff prompt.

## Report The Result

State:

- the one-sentence role of each figure;
- the created artifact paths;
- the source of any external image or displayed number;
- the manuscript pages visually checked;
- any unresolved scientific or venue-compliance concern.

For a handoff-only route, state clearly that no editable figure was produced, name the missing capability, and present the complete prompt in one fenced block that the user can submit to a capable tool without reconstructing hidden context. Fill unknown scientific details with explicit `TODO: confirm ...` instructions inside the prompt rather than omitting the prompt. End by asking the user to run that prompt in a presentation-capable environment and attach the listed inputs. Treat a response without the exact fenced-prompt first line from the hard completion check as a failed execution of this skill.
