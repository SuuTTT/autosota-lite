# Editable PowerPoint Construction

## Master Artifact

Treat the PPTX as the editable source of truth. Use one slide per figure and set the slide aspect ratio close to the intended paper figure. Do not design on a generic 16:9 slide and leave large unused margins.

Use the Presentations skill and its required artifact-tool workflow. Preserve source code for deterministic regeneration.

## Editable Elements

Build these with native PowerPoint elements:

- all visible text;
- boxes, bands, dividers, brackets, legends, and callouts;
- arrows and connectors;
- simple plots and axes when practical;
- masks, highlights, and emphasis marks.

Create connectors before nodes so edges remain behind shapes. Snap repeated objects to a consistent grid and keep line weights stable after export.

## Raster And Vector Assets

Use real paper evidence for domain examples when available. Crop non-destructively and retain the unmodified source in the build workspace.

Use generated imagery only for a semantic object that cannot be represented faithfully with shapes. Generate each object separately on a transparent background. Do not generate labels, arrows, equations, plots, or the entire composition as one bitmap.

Prefer vector PDF/SVG for equations, plots, icons, and scientific diagrams. Keep their source data or LaTeX beside the build script. If a complex equation cannot remain editable, keep it vector and record its exact LaTeX source.

## Typography

Use one font family compatible with the manuscript. Judge font size after insertion into the paper:

- final labels should usually be at least the venue's minimum, commonly 8--9 pt;
- section labels may be 9--11 pt;
- avoid oversized slide-deck typography;
- never solve crowding by shrinking all text.

Use sentence case, zero or normal letter spacing, and consistent mathematical italics.

## Export

Produce:

1. editable `.pptx`;
2. vector `.pdf` cropped to the figure bounds;
3. 300 dpi `.png` for quick review and web previews;
4. optional `.tex` wrapper with width, caption, label, and accessibility description.

Check that PDF export embeds fonts and preserves transparency. Check that PNG export does not introduce blurry labels or changed colors.

## Figure Pair Consistency

Reuse the same palette, type family, line semantics, and visual identity for recurring objects. Do not reuse the same whole layout. Figure 1 should remain intuitive and example-driven; Figure 2 should remain technical and mechanism-driven.
