---
name: aaai-paper-polish-suite
description: "Coordinate final-stage polishing of an existing AI/ML manuscript for AAAI: reverse-engineer an appropriate writing model, polish author-written prose, redesign conceptual figures and quantitative plots, compile and inspect the paper, and prepare a policy-compliant OpenReview submission package. Use when drafts and results already exist and the goal is reviewer-facing clarity, visual consistency, evidence integrity, anonymity, supplement packaging, or submission readiness across the scientific-writing-reverse-engineering, design-ai-paper-figures, and aaai-submission skills."
---

# AAAI Paper Polish Suite

Coordinate three specialized skills without merging their responsibilities. Keep discoverable skills as direct children of the plugin's `skills/` directory.

## Route the work

Read the sibling skill required for each phase:

1. `../paper-reverse-engineering/SKILL.md` for exemplar selection, writing models, evidence maps, author-voice preservation, prose polish, and overlap checks.
2. `../design-ai-paper-figures/SKILL.md` for Figure 1, Figure 2, quantitative plots, source-data traceability, editable/vector deliverables, and paper-scale QA.
3. `../aaai-submission/SKILL.md` for live OpenReview fields, profiles, reciprocal reviewer, anonymity, file limits, external-repository-link prohibition, checklist, supplements, and desk-rejection audit.

If the user requests only one phase, use only that skill. For a full polish, follow the order below because later phases depend on stable claims and figures. For several papers, read [Portfolio consistency](references/portfolio-consistency.md).

## Phase 0: Freeze evidence and policy

Locate the author-written manuscript, verified results, current author kit, and live OpenReview form. Create a claim ledger. Read current venue AI-writing and figure policies. Mark missing evidence or attestations; do not infer them.

## Phase 1: Build and apply the writing model

Route the paper as mechanism-first, diagnostic/evaluation, benchmark/resource, or an explicit hybrid. Select three to five strong exemplars and record evidence. Model rhetorical moves and aggregate cadence without copying wording. Audit and polish only within venue policy. Run overlap, terminology, evidence, and claim-strength checks.

Do not optimize for an AI-detector score. Preserve author voice and project-specific reasoning.

## Phase 2: Build the visual system

Give Figure 1, Figure 2, and each experiment plot a distinct claim. Establish a consistent palette, typography, notation, and method identity. Use real evidence and source-data mappings. Measure the actual template width. Produce editable sources, vector PDF/SVG, and PNG previews. Compile figures into the paper and inspect full pages.

## Phase 3: Submission audit

Recompute every field-level number. Prepare metadata using the live form. Verify profiles and reciprocal-reviewer obligations. Build checklist and upload archives. Remove every external link to this paper's source/data, including anonymized repositories; place reviewer artifacts inside the Code and Data Supplement. Check sizes, anonymity, simultaneous-submission attestations, conflicts, license, rendering, and self-containment.

## Hard gates

Report `BLOCKING` when a number lacks evidence, causality exceeds design, a figure contains invented evidence, an external artifact link remains, an author/reviewer attestation is unresolved, or the paper violates template, page, anonymity, or venue-AI policy.

## Deliver one readiness report

Summarize the writing family and exemplars; claims changed or unsupported; figures and pages checked; fields and uploads prepared; `BLOCKING`, `AUTHOR_ACTION_REQUIRED`, and `READY` items; and paths to editable sources, audits, and final artifacts.
