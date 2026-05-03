---
name: scientific-writing-reverse-engineering
description: Use a Hilary Glasman-Deal style reverse-engineering workflow to analyze published scientific papers sentence by sentence, extract section-specific sentence-function writing models, and generate a complete manuscript from the user's project, method, and experimental results without copying source text.
---

# Scientific Writing Reverse Engineering

Use this skill when the user wants to write a scientific paper by imitating the rhetorical structure of strong papers in the same field. The approach follows the spirit of Hilary Glasman-Deal's *Science Research Writing for Native and Non-Native Speakers of English*: do not memorize abstract rules; instead, study published papers, label what each sentence does, abstract reusable writing models, and adapt those models to the user's own research.

## Core Principle

Reverse-engineer sentence function, not sentence wording.

The output should be a complete paper or section draft built from the user's actual method, evidence, and results. Never copy or closely paraphrase model-paper sentences.

## Required Inputs

Collect or ask for:

- Target journal, conference, or field.
- Three to five model papers from the target venue or field.
- The user's project description, method, algorithm, system, theory, or experiment notes.
- Experimental results, tables, figures, logs, metrics, and comparison baselines.
- Any required template, call for papers, author instructions, or page limit.

If model papers are not provided, ask the user for them or, when appropriate, search for recent papers from the target venue. If only one or two papers are available, proceed but label the writing model as provisional.

## Workflow

### 1. Prepare Model Papers

For each model paper:

1. Extract text if needed from PDF, LaTeX, Word, Markdown, or HTML.
2. Identify the paper type: method, theory, empirical, system, survey, dataset, clinical, control, robotics, or other.
3. Record the section structure and subsection order.
4. Prefer papers with a similar contribution type and evidence style to the user's project.

Do not load or quote large chunks of model-paper prose into the final answer. Use extracted text only for analysis.

### 2. Sentence-by-Sentence Function Labeling

For each important section, label each sentence by its rhetorical function. At minimum, analyze:

- Abstract.
- Introduction.
- Related work or background.
- Problem formulation / preliminaries, if present.
- Method / algorithm / framework.
- Experiment setup.
- Results.
- Discussion.
- Conclusion.

Use concise function labels. Examples:

- `FIELD_CONTEXT`: establishes the research area.
- `IMPORTANCE`: explains why the topic matters.
- `KNOWN_PROGRESS`: states what existing work can do.
- `LIMITATION`: identifies a weakness or unsolved issue.
- `GAP`: narrows the exact missing piece.
- `PURPOSE`: states what this paper aims to do.
- `METHOD_OVERVIEW`: summarizes the proposed method.
- `MECHANISM`: explains how the method works.
- `CONTRIBUTION`: lists a contribution.
- `SETUP`: describes data, task, benchmark, or protocol.
- `RESULT`: reports an observed result.
- `COMPARISON`: compares with baselines or prior work.
- `INTERPRETATION`: explains what the result means.
- `LIMITATION_SCOPE`: states boundaries of the claim.
- `FUTURE_WORK`: gives next steps.

Create a table or compact list like:

```text
Model paper A, Abstract
S1 FIELD_CONTEXT: establishes the broad problem.
S2 LIMITATION: says current methods struggle with [abstract issue].
S3 PURPOSE+METHOD_OVERVIEW: introduces the proposed approach.
S4 MECHANISM: explains the key mechanism.
S5 SETUP: gives evaluation scope.
S6 RESULT: summarizes main result.
S7 IMPLICATION: states why the result matters.
```

### 3. Abstract the Writing Model

From the sentence labels, build reusable section models. A section model is an ordered sentence-function plan, not a text template copied from a paper.

For each section, produce:

```text
Section: Abstract
Sentence-function model:
1. FIELD_CONTEXT
2. LIMITATION
3. PURPOSE
4. METHOD_OVERVIEW
5. MECHANISM
6. SETUP
7. RESULT
8. IMPLICATION_OR_SCOPE
```

Then create abstract sentence patterns with placeholders:

```text
FIELD_CONTEXT: [Research area] is important for [application/context].
LIMITATION: However, [existing approach] often struggles with [specific limitation].
PURPOSE: This paper studies/proposes [method] for [target problem].
RESULT: Experiments on [benchmark/task] show [measured result], compared with [baseline].
SCOPE: These results suggest [cautious implication], while [limitation] remains.
```

Sentence patterns may be inspired by the model papers' function, but must use new wording.

### 4. Build The User Paper Evidence Map

Before drafting, map the user's project into the writing model:

- Problem and motivation.
- Specific research gap.
- Proposed method and mechanism.
- Differences from prior work.
- Assumptions and scope.
- Datasets, benchmarks, tasks, metrics, and baselines.
- Main results and exact numbers.
- Negative, partial, failed, or inconclusive results.
- Limitations and future work.
- Citations already known.
- Citation placeholders needed.

If evidence is missing, mark it as `NEEDS_EVIDENCE` instead of inventing it.

### 5. Generate The Complete Paper

Use the selected section models to draft the complete paper in the requested format: LaTeX, Markdown, Word-compatible Markdown, or venue template.

For every section:

1. Follow the section's sentence-function model.
2. Fill each sentence function with the user's actual method and evidence.
3. Keep claims cautious when evidence is preliminary.
4. Add tables or figure placeholders from the user's results.
5. Add citation placeholders where needed.
6. Preserve venue conventions from model papers and templates.

When drafting a full paper, include at least:

- Title.
- Abstract.
- Keywords.
- Introduction.
- Related work or background, if expected by the venue.
- Problem formulation / preliminaries, if needed.
- Method.
- Experiments or numerical examples.
- Discussion or limitations, if appropriate.
- Conclusion.
- References or BibTeX placeholders.

### 6. Non-Native English Writing Rules

Prefer:

- One clear function per sentence.
- Clear subject-verb-object structure.
- Short paragraphs with one main purpose.
- Repeated technical terms instead of unnecessary synonyms.
- Explicit connectors: however, therefore, in contrast, specifically, as a result.
- Measured claim verbs: show, indicate, suggest, improve, reduce, compare.

Avoid:

- Copying model-paper phrases.
- Long noun chains.
- Vague praise words such as novel, powerful, excellent, significant, or robust without evidence.
- Overclaiming from one seed, partial results, smoke tests, or small ablations.
- Hidden unsupported claims about theory, convergence, stability, causality, robustness, or generalization.

## Output Artifacts

When creating or revising a paper, produce these artifacts when useful:

- `writing_model.md`: sentence-function analysis and reusable section models.
- `evidence_map.md`: project-method-result mapping, with unsupported claims flagged.
- Manuscript file: e.g. `main.tex`, `paper.md`, or venue-template `.tex`.
- `references.bib` or citation placeholder list.
- Tables or figure-placeholder files derived from actual results.

## Final Response Format

Report:

- Model papers analyzed.
- Writing model created or updated.
- Project evidence used.
- Manuscript files created or changed.
- Claims marked as needing evidence.
- Validation performed, such as source checks, citation-key checks, or LaTeX compile attempt.

## Integrity Checklist

Before finalizing, verify:

- The paper follows sentence-function models rather than copied text.
- No model-paper sentence is copied or closely paraphrased.
- Every numerical claim comes from provided results or is marked as missing.
- Citation placeholders are not presented as real citations.
- The claim strength matches the evidence.
- The manuscript format follows the target venue as closely as local materials allow.
