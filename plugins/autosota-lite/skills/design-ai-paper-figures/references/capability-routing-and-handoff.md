# Capability Routing And Production Handoff

## Capability Audit

Before producing artifacts, record yes/no for:

| Capability | Required for |
|---|---|
| Native presentation control | Editable PPTX or equivalent master |
| Image generation/editing | New raster examples or isolated illustrative assets |
| Slide rendering/export | PDF/PNG deliverables and visual inspection |
| Manuscript compilation | Final page-scale and float-placement QA |
| Source/evidence access | Scientifically grounded labels, equations, and values |

Never describe a planned artifact as completed. Never claim a visual check was performed when the environment cannot render the result.

## Routing Matrix

### Presentation control and image generation

Produce the full editable master. Use image generation only for isolated semantic assets. Keep labels, equations, arrows, plots, and layout native and editable.

### Presentation control only

Produce the editable master from native shapes, paper assets, and vector plots. If a raster illustration is essential, insert a labeled placeholder and add an asset prompt to the evidence ledger. The figure must remain understandable without the missing decoration.

### Image generation only

Generate isolated transparent-background assets only after the scientific briefs are stable. Return those assets plus the complete production prompt below. State that deck assembly, export, and paper-scale QA remain pending.

### Text, code, or CLI only

Do not fake presentation control with a screenshot or claim that a PPTX was visually designed. Perform the scientific analysis first, then return exactly:

1. one sentence stating that native presentation control is unavailable;
2. the complete fenced production prompt, with Figure 1 and Figure 2 briefs, verified labels, equations, evidence, and unresolved items filled inside it;
3. one sentence asking the user to run the prompt in a presentation-capable tool or agent and attach the manuscript and listed assets.

The agent may create supporting data, plots, or LaTeX snippets when its tools genuinely support them, but these do not replace the editable figure master.

A CLI/text-only response that contains standalone briefs but no fenced production prompt is incomplete. Do not place long briefs before the prompt; this risks truncating the required deliverable. Unknown details do not excuse omission: write them as explicit `TODO: confirm ...` items in the prompt so the receiving tool asks for or resolves them before drawing. Before returning, verify that the first substantive deliverable is a code fence containing the exact first line `You are designing two coordinated, conference-grade figures for an AI/ML paper.`

## Production Prompt Template

Return one fenced block using this structure. Replace every bracketed field with task-specific content. Do not leave hidden references such as “use the context above.” After the block, ask the user to run it in a presentation-capable environment and attach every input named by the prompt.

```text
You are designing two coordinated, conference-grade figures for an AI/ML paper.

INPUTS TO READ
- Paper/manuscript: [attach or paste accessible source]
- Verified evidence/results: [attach or paste exact values and provenance]
- Venue/template and final dimensions: [venue, one/two column, width, page limit]
- Existing figures or visual references: [attach or state none]

CAPABILITIES REQUIRED
- Native PowerPoint or equivalent presentation editing
- Slide rendering and PDF/PNG export
- Image generation only for the isolated assets explicitly listed below

SCIENTIFIC CONSTRAINTS
- Do not invent model components, equations, datasets, or numerical results.
- Match manuscript terminology and notation exactly.
- Distinguish measured, illustrative, hypothetical, and oracle values.
- Keep Figure 1 problem-driven and Figure 2 method-driven; do not duplicate layouts.

FIGURE 1 BRIEF
- Role: [one sentence]
- Claim: [one sentence]
- Visual grammar: [pattern]
- Composition: [left-to-right or other precise layout]
- Objects/assets: [complete list]
- Visible labels: [exact short labels]
- Evidence and provenance: [exact values and source]
- Caption contract: [what caption must establish]
- Final dimensions: [width/aspect ratio]

FIGURE 2 BRIEF
- Role: [one sentence]
- Claim: [one sentence]
- Visual grammar: [pattern]
- Information flow: [precise stages and branches]
- Novel component and emphasis: [what must dominate]
- Inputs/outputs/supervision/objective: [complete specification]
- Training versus inference paths: [exact distinction]
- Equations and symbol definitions: [exact notation]
- Visible labels: [exact short labels]
- Caption contract: [what caption must establish]
- Final dimensions: [width/aspect ratio]

ASSET GENERATION PROMPTS
- [Asset name]: [subject, scientific meaning, viewpoint, crop, aspect ratio, palette, transparent background, exclusions, resolution]
- Keep all text, arrows, equations, plots, and layout out of generated images.

EDITABLE CONSTRUCTION RULES
- Make every label, arrow, connector, shape, legend, and simple plot editable.
- Use generated images only as isolated assets; never embed a generated whole figure.
- Use a restrained white-background conference style, one neutral ink, one primary accent, and at most one secondary accent.
- Avoid UI cards, decorative gradients, stock icons, excessive rounded boxes, and software-architecture styling.
- Size fonts for the final printed manuscript, with no label below [venue minimum] after scaling.

DELIVERABLES
- Editable PPTX or equivalent native master, one slide per figure
- Cropped vector PDF exports
- 300 dpi PNG previews
- Final captions and optional LaTeX wrappers
- Source/evidence ledger for all values and nontrivial assets

MANDATORY QA
- Render and inspect every slide for clipping, overlap, crossings, and malformed equations.
- Compute effective printed font sizes after manuscript scaling.
- Test grayscale and common red-green color-vision deficiencies.
- Compile the figures into the manuscript and inspect the complete pages.
- Verify every visible claim against the supplied manuscript or evidence.
- Apply the five-second test: Figure 1 communicates the problem; Figure 2 exposes the novelty and input-to-output logic.

Return the editable artifacts and a short QA report. List any check you could not perform instead of claiming success.
```

## Asset Prompt Requirements

An asset prompt must be usable independently. Include:

- the object and its scientific role;
- camera/viewpoint or diagram perspective;
- background and transparency;
- aspect ratio and intended crop;
- palette and contrast constraints;
- what must not appear, especially text and labels;
- output resolution;
- whether the asset is illustrative or tied to real evidence.

Do not ask image generation to draw quantitative plots, equations, readable labels, or the complete figure.
