# Quantitative experiment plots

## Figure contract

Before plotting, record:

- one conclusion the figure supports;
- comparison unit and fair baseline set;
- source file and exact fields for every panel;
- inclusion/exclusion rules with before/after counts;
- aggregation level, seeds, smoothing, normalization, and transformations;
- uncertainty definition (`SD`, `SE`, confidence interval, bootstrap interval, or none);
- single-column, double-column, or full-page target;
- required vector and preview outputs.

Do not invent statistics, error bars, sample sizes, or missing observations. Do not
silently drop failed runs or zero-coded missing values.

## Choose the visual grammar

| Scientific question | Preferred forms | Common failure |
|---|---|---|
| Compare methods across tasks | dot/interval plot, grouped bar only for a small set | crowded bars and unreadable legends |
| Show training or scaling behavior | line plus uncertainty band | smoothing without showing or documenting it |
| Show distribution | box/violin plus raw points when feasible | hiding sample size and multimodality |
| Show paired change | paired dots/slope graph | independent bars that erase pairing |
| Show relation | scatter with fitted relationship and uncertainty | implying causality from a trend line |
| Show matrix/structure | heatmap with meaningful ordering | rainbow palette and illegible cells |
| Show ablation | aligned dot/bar plot with reference line | mixing incompatible metrics on one axis |

Avoid radar charts unless angular geometry is scientifically meaningful. Avoid
dual y-axes when readers could infer a relationship from arbitrary scaling.

## Measure manuscript dimensions

Use the target template. A temporary line such as
`\typeout{COLUMNWIDTH=\the\columnwidth}` exposes the compiled width in TeX points.
Convert with `inches = points / 72.27`. Set `figsize` to the final physical size so
LaTeX does not shrink labels after export.

## Reproducible Matplotlib baseline

```python
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams.update({
    "font.size": 8,
    "axes.labelsize": 8,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
    "legend.fontsize": 7,
    "axes.linewidth": 0.7,
    "lines.linewidth": 1.4,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "svg.fonttype": "none",
    "savefig.bbox": "tight",
})

column_width_in = measured_tex_points / 72.27
fig, ax = plt.subplots(figsize=(column_width_in, 0.62 * column_width_in))
# Plot from verified data with explicit labels and uncertainty semantics.
fig.savefig("figure.pdf")
fig.savefig("figure.svg")
fig.savefig("figure.png", dpi=300)
```

Adapt font family to the venue and verify the embedded result. Style packages such
as SciencePlots may be layered in, but measure width and inspect font substitution.

## Multi-panel rules

- Give each panel one role in the evidence chain.
- Use lowercase panel labels consistently and keep them outside the data region.
- Share axes and legends when scales and semantics match.
- Align plot areas, not merely outer image boxes.
- Use the same method color/marker identity throughout the paper.
- Reserve annotations for the comparison the caption discusses.
- Keep panel order consistent with the Results section and caption.

## Caption contract

The caption must define task, metric direction, aggregation, uncertainty, sample
count or seeds, statistical annotations, panel mapping, and the intended takeaway.
Do not make the artwork carry a paragraph of prose.

## QA

Inspect standalone PDF/SVG and the compiled paper page. Verify:

- labels remain readable at 100% page zoom;
- axes include units and metric direction is unambiguous;
- error bars and bands are defined;
- legends match visual order and do not cover evidence;
- grayscale and common color-vision simulations preserve distinctions;
- fonts are embedded and text remains selectable/editable;
- no clipping, rasterized vector elements, inconsistent scales, or unexplained smoothing;
- every plotted value reproduces from the source-data map.
