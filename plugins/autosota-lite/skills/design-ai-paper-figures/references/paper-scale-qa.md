# Paper-Scale Quality Assurance

## Artifact Checks

- Render every PPTX slide to PNG and inspect it.
- Run the presentation overflow/overlap validator.
- Export to vector PDF and verify page bounds and embedded fonts.
- Confirm that all intended text remains editable in the PPTX.
- Confirm generated or external assets have provenance records.

## Scientific Checks

- Match every component name to the manuscript.
- Match every equation to the manuscript source.
- Match every displayed number to a frozen result artifact.
- Distinguish measured, illustrative, hypothetical, and oracle values.
- Verify training-only information is not presented as inference input.
- Verify the caption does not claim more than the experiment supports.

## Readability Checks

Insert the exported PDF into the manuscript and compile it at final width.

Compute the effective printed font size before approval:

```text
scale factor = placed manuscript width / exported figure width
effective font size = source font size x scale factor
```

Use consistent physical units for both widths. A readable source slide is not
evidence of readable paper text. Reject any label whose effective size falls
below the venue minimum; redesign the composition instead of relying on zoom.

- Inspect at 100% page view and printed scale.
- Confirm the smallest text meets venue requirements.
- Confirm no label wraps unexpectedly.
- Confirm arrows terminate unambiguously.
- Confirm legends do not require color alone.
- Confirm equations, subscripts, and Greek symbols render correctly.
- Confirm no important detail disappears in grayscale.
- Test common red-green color-vision deficiencies.
- Check contrast for thin lines and pale fills.

## Five-Second Tests

Ask a reader unfamiliar with the implementation, or perform a fresh-context audit:

- Figure 1: Can they state the task and central problem?
- Figure 2: Can they point to the proposed novelty and trace input to output?

Failure means the visual hierarchy is wrong even if every component is technically present.

## Page-Level Checks

Inspect the complete manuscript page containing each figure:

- figure and caption remain together;
- figure does not dominate or leave awkward whitespace;
- neighboring text introduces the figure before it appears;
- caption is readable and not redundant;
- float placement does not break section flow;
- no LaTeX overflow or font substitution warnings are introduced.

Record the rendered manuscript pages used for the final audit.
