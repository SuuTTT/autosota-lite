---
name: scientific-writing-reverse-engineering
description: Reverse-engineer strong scientific papers into section-specific rhetorical and aggregate style models, then audit or polish an existing author-written manuscript without copying source text. Use for AAAI and other research papers when selecting 3-5 exemplars, labeling sentence functions, building mechanism/diagnostic/benchmark writing models, measuring cadence and controlled word frequencies, reducing generic AI-like prose, checking evidence, or auditing phrase overlap and venue AI-writing policy.
---

# Scientific Writing Reverse Engineering

Model how strong papers reason and pace information. Do not copy their sentences,
rare phrases, or topic vocabulary, and do not optimize to deceive an AI detector.
The useful target is project-specific, evidence-shaped prose that survives expert
review and provenance checks.

## Set the allowed mode

Read the current venue policy before editing. For AAAI, treat the workflow as
analysis and polishing of author-written text: preserve author responsibility,
keep the author's final wording and scientific judgment, and document AI's role as
required. Do not silently turn notes into an AI-authored submission when the venue
allows only editing or polishing.

Choose one mode:

- `MODEL_ONLY`: analyze exemplars and create writing models;
- `AUDIT`: label problems and recommend edits without rewriting;
- `POLISH`: line-edit author-written prose while preserving meaning and voice;
- `RESTRUCTURE`: reorder author-written claims and paragraphs with tracked rationale;
- `DRAFT_WHERE_ALLOWED`: draft from an evidence map only when venue policy permits.

## Select exemplars

Use three to five papers per contribution family, not one universal style donor.
Prefer, in order:

1. target-venue award or distinguished papers with close contribution type;
2. accepted target-venue papers with close evidence and section structure;
3. strong field papers when the target venue lacks a close match.

Record acceptance/award evidence and state when review scores are unavailable.
Never claim an exemplar had no negative review unless the complete public record
supports it.

For AAAI-oriented work, read [the category models](references/aaai-writing-models.md).

## Build two models

### Rhetorical model

Label every important sentence by function: context, stakes, prior capability,
failure, gap, purpose, mechanism, setup, result, comparison, interpretation,
scope, limitation, or implication. Derive ordered move sequences for each section
and paragraph. Model function, not wording.

### Aggregate surface model

Measure at section level:

- mean, median, quartiles, and spread of sentence length;
- proportion of short and long sentences;
- paragraph-length distribution;
- first-person, contrast, transition, and stance/evidence-verb frequency;
- citation density and terminology consistency.

Run `scripts/analyze_prose_style.py` on extracted exemplar prose and the draft.
Treat ranges as descriptive bands, not quotas. Do not imitate rare content words,
distinctive collocations, or exact sentence skeletons.

## Build the evidence map

Before polishing, map each claim to its result file, table, figure, derivation,
scope, uncertainty, and comparison. Mark unsupported content `NEEDS_EVIDENCE`.
Do not strengthen claim verbs during polishing.

## Preserve author voice

Estimate the author's baseline from clearly author-written sections. Preserve
stable terminology, preferred directness, and natural variation. Use exemplar
statistics only to correct material outliers, such as uniformly long sentences,
repeated paragraph openers, or monotonous cadence.

Remove common synthetic-prose signals when they hurt clarity:

- generic importance claims without a decision or failure;
- repeated `Moreover`/`Furthermore` openers;
- ornamental adjective stacks and automatic three-item lists;
- vague `this/these` references without a technical noun;
- identical paragraph shape and sentence length;
- claims that restate the abstract without adding evidence.

Do not add randomness or errors to appear human.

## Polish by function

For each paragraph:

1. state its function and evidence obligation;
2. keep one main argumentative job;
3. order claim -> evidence/mechanism -> interpretation -> local consequence;
4. use stable technical nouns and concrete verbs;
5. use short sentences for conclusions or caveats and long sentences only when a
   condition, comparison, and consequence must stay together;
6. show the author any edit that changes scope, causality, or interpretation.

## Audit integrity

Run `scripts/audit_phrase_overlap.py` against the exemplars. Treat an eight-word
match as a review item and a distinctive match as blocking. Also verify:

- every number traces to a result artifact;
- no citation is invented;
- causal verbs match the design;
- limitations appear where they qualify claims;
- terminology is consistent;
- the final prose complies with the venue's AI-writing policy.

## Deliver

Produce only the artifacts relevant to the selected mode:

- `writing_model.md`: exemplar ledger, section moves, and aggregate style bands;
- `evidence_map.md`: claims, sources, uncertainty, and missing evidence;
- `writing_audit.md`: issue, location, rationale, and proposed action;
- polished manuscript or tracked patch where allowed;
- `overlap_report.txt` and validation summary.

Report which sentences changed meaning or claim strength for explicit author review.
