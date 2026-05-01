# Scientific Writing Reverse Engineering Skill

## Purpose

Given:

1. a **model paper** whose rhetorical structure should be studied, and
2. a **target project** whose paper, proposal, notes, codebase, or partial draft needs to be written,

produce a sentence-by-sentence **writing map**. Each map item connects a sentence from the **model paper** to a reusable rhetorical function and a new sentence for the target project.

The central output is:

```text
(model_original_sentence, abstract_sentence_function, rewritten_sentence)
```

If the target project already includes draft prose, proposal text, notes, or a paper sentence, include it as an optional fourth field:

```text
(model_original_sentence, abstract_sentence_function, rewritten_sentence, project_original_sentence)
```

The skill is designed for research writing practice, not plagiarism. The agent should abstract rhetorical moves, grammar, section logic, and discourse functions while avoiding transfer of the model paper's scientific claims, data, novelty claims, or wording into the target paper.

---

## Key Display Rule

In all review interfaces, hover cards, tables, and inspector panels, the **primary original sentence** must be the **model paper's original sentence**.

If the user also supplied an original target-paper sentence, project proposal sentence, code comment, or notes sentence, show that as a separate optional field named **project_original_sentence** or **target original sentence**.

Do not label the user's sentence simply as "original sentence," because this creates ambiguity. Use:

- **Model paper sentence**: exact sentence from the model paper.
- **Abstract function**: reusable rhetorical job of that model sentence.
- **Model pattern**: optional abstract sentence template.
- **Project original sentence**: optional sentence or note from the user's material.
- **Rewritten sentence**: new sentence for the user's paper.

---

## When to Use This Skill

Use this skill when the user asks to:

- imitate the structure of a scientific paper;
- reverse-engineer a model article, abstract, introduction, methods, results section, discussion, or grant-style text;
- produce a sentence-by-sentence writing plan;
- rewrite a target project using the rhetorical skeleton of another paper;
- generate a hover-based webpage in which the visible text is the rewritten paper and the hover card shows the model paper sentence, abstract function, optional model pattern, optional project original sentence, and rewritten sentence.

Do **not** use this skill to copy a model paper into a new paper. The model paper sentence is displayed for review and learning only. The rewritten sentence must be an original target-project sentence.

---

## Required Inputs

Ask for or infer the following.

### Model Paper

The source text to reverse engineer. This can be a full paper, section, abstract, paragraph, or excerpt.

### Target Project Material

Any material describing the user's project. This may be:

- a draft paper;
- a proposal;
- project notes;
- code and README files;
- experimental logs;
- bullet points;
- a short project brief.

Useful project details include:

- field or discipline;
- research topic;
- research gap;
- study aim;
- data, method, model, experiment, or corpus;
- key variables or materials;
- expected or actual findings;
- contribution or implication;
- target section: abstract, introduction, methods, results, discussion, conclusion, etc.

If the target project brief is incomplete, make conservative placeholders rather than inventing unsupported scientific claims. Mark uncertain content with `[PROJECT DETAIL NEEDED: ...]`.

---

## Output Schema

Prefer object form for readability.

### Preferred Object Form

```json
[
  {
    "section": "Introduction",
    "sentence_index": 1,
    "model_original_sentence": "Exact sentence from the model paper.",
    "abstract_sentence_function": "Establishes the broad importance of the research area.",
    "model_pattern": "X has become an important paradigm for Y.",
    "project_original_sentence": "Optional original sentence from the user's paper, proposal, notes, or project material.",
    "rewritten_sentence": "New sentence for the user's target paper."
  }
]
```

The field `project_original_sentence` is optional and should be omitted or left empty if the user did not provide a draft sentence.

### Tuple Form

Use this when the user explicitly asks for tuples:

```json
[
  [
    "Exact sentence from the model paper.",
    "Establishes the broad importance of the research area.",
    "New sentence for the user's target paper."
  ]
]
```

Optional four-item tuple:

```json
[
  [
    "Exact sentence from the model paper.",
    "Establishes the broad importance of the research area.",
    "New sentence for the user's target paper.",
    "Optional original sentence from the user's material."
  ]
]
```

For backward compatibility, renderers may accept `original_sentence`, but it must be interpreted as the **model paper sentence**, not as the user's project sentence.

---

## Procedure

### 1. Segment the Model Text

Split the model paper or section into sentences. Preserve section labels when available.

Rules:

- Do not split inside common abbreviations such as `e.g.`, `i.e.`, `Fig.`, `Dr.`, or `et al.`.
- Keep citation markers attached to the sentence they support.
- If a sentence is extremely long and contains multiple rhetorical moves, keep it as one sentence unless the user asks for clause-level mapping.
- If headings are present, record them as section metadata, not as sentences, unless the heading itself functions rhetorically.

### 2. Identify the Sentence Function

For each model sentence, ask: **What job is this sentence doing in the paper?**

Common functions include:

- introduces the broad research area;
- establishes importance or urgency;
- summarizes known knowledge;
- narrows the topic;
- identifies a limitation or gap;
- contrasts prior findings;
- defines the unresolved problem;
- states the aim of the current study;
- previews the method or dataset;
- states the hypothesis or research question;
- describes experimental design;
- reports a main result;
- compares the result with prior work;
- interprets the mechanism;
- explains practical or theoretical significance;
- acknowledges a limitation;
- proposes future work;
- concludes with the main contribution.

### 3. Abstract the Sentence

Remove domain-specific nouns, methods, data, results, and claims. Retain the rhetorical logic.

Example:

```text
Model paper sentence: Although several studies have examined microbial activity in coastal sediments, little is known about how seasonal temperature shifts affect nitrogen cycling in deep-sea environments.

Abstract function: Contrasts existing research with a specific remaining knowledge gap.

Model pattern: Although several studies have examined X, little is known about how Y affects Z in context C.
```

The field `abstract_sentence_function` should be concise. Put the reusable syntax in `model_pattern` when possible.

### 4. Rewrite for the Target Project

Use the abstract function to write a new sentence for the user's project.

Rules:

- Match the rhetorical function, not the exact words.
- Use accurate project details from the user.
- Do not invent methods, data, results, or claims.
- If the needed project detail is missing, insert a bracketed placeholder.
- Use the target paper's desired tense and section conventions.
- Keep the rewritten sentence publication-style, clear, and concise.
- If target project prose is available, preserve correct technical content while improving structure and flow.

### 5. Generate the Interactive Review Page

The visible page should show the **rewritten paper**.

On hover or click, each rewritten sentence should reveal:

1. **Model paper sentence** — exact sentence from the model paper.
2. **Abstract function** — rhetorical function of the model sentence.
3. **Model pattern** — optional reusable abstract pattern.
4. **Project original sentence** — optional; show only if supplied.
5. **Rewritten sentence** — the sentence currently shown in the draft.

The card must not treat the user's original sentence as the primary original. The user's sentence is secondary evidence/context only.

### 6. Quality Check

Before finalizing, verify each row:

- The hover card clearly labels the **model paper sentence**.
- The project original sentence is optional and separately labeled.
- The rewritten sentence performs the same rhetorical job as the model sentence.
- The wording is not a close paraphrase of the model paper.
- The rewritten sentence is scientifically plausible for the target project.
- The abstract function is general enough to reuse.
- Claims are supported by the user's provided project information.
- Citation-dependent claims from the model are not transferred unless the user provides equivalent evidence.

---

## Recommended Agent Prompt

```text
You are a scientific writing reverse-engineering assistant.

Task:
Given a model paper or section and target project material, create a sentence-by-sentence writing_map.

For each sentence in the model text, produce:
1. model_original_sentence: the exact model paper sentence;
2. abstract_sentence_function: the rhetorical function of the sentence;
3. model_pattern: an optional reusable abstract template;
4. project_original_sentence: optional original user/project sentence if available;
5. rewritten_sentence: a new sentence for the target project that performs the same function without copying the model wording.

Constraints:
- Preserve the order and section logic of the model paper where useful.
- Do not transfer unsupported scientific claims from the model paper.
- Do not imitate wording too closely.
- Use bracketed placeholders for missing project details.
- Return valid JSON in object form.
- In any hover UI, show the model paper sentence first; show the project original sentence only as an optional separate field.

Model text:
<<<MODEL_TEXT>>>

Target project material:
<<<PROJECT_MATERIAL>>>
```

---

## Example

This fictional example demonstrates the required display logic.

### Model Text

```text
Reinforcement learning has produced striking advances in games and simulated control, yet deploying these methods in open-ended decision-making settings remains difficult. A central obstacle is that exploration in sparse-reward environments yields trajectories that are expensive to collect and weakly informative for credit assignment. We introduce Preference-Weighted Offline Policy Optimization, an algorithm that converts pairwise trajectory preferences into conservative advantage estimates.
```

### Target Project Material

```text
Topic: offline reinforcement learning for language-model agents
Draft/project note: Logged agent traces contain sparse success labels, and the project proposes TraceQ to convert trace outcomes into action-level targets.
```

### Writing Map

```json
[
  {
    "section": "Introduction",
    "sentence_index": 1,
    "model_original_sentence": "Reinforcement learning has produced striking advances in games and simulated control, yet deploying these methods in open-ended decision-making settings remains difficult.",
    "abstract_sentence_function": "Acknowledges broad progress in the field while narrowing to a persistent deployment challenge.",
    "model_pattern": "X has produced advances in Y, yet Z remains difficult.",
    "project_original_sentence": "Logged agent traces contain sparse success labels.",
    "rewritten_sentence": "Language-model agents have achieved promising results in tool-use and web-navigation tasks, yet improving them from narrow logged traces remains difficult."
  },
  {
    "section": "Introduction",
    "sentence_index": 2,
    "model_original_sentence": "A central obstacle is that exploration in sparse-reward environments yields trajectories that are expensive to collect and weakly informative for credit assignment.",
    "abstract_sentence_function": "Identifies the main technical obstacle and explains why it creates learning difficulty.",
    "model_pattern": "A central obstacle is that A yields B that are C and D.",
    "project_original_sentence": "The project proposes TraceQ to convert trace outcomes into action-level targets.",
    "rewritten_sentence": "A central obstacle is that logged agent executions usually provide only sparse outcome labels, leaving intermediate decisions weakly supervised for credit assignment."
  },
  {
    "section": "Introduction",
    "sentence_index": 3,
    "model_original_sentence": "We introduce Preference-Weighted Offline Policy Optimization, an algorithm that converts pairwise trajectory preferences into conservative advantage estimates.",
    "abstract_sentence_function": "Introduces the proposed method and states what it converts or transforms.",
    "model_pattern": "We introduce X, a method that converts A into B.",
    "project_original_sentence": "",
    "rewritten_sentence": "We introduce TraceQ, an offline reinforcement-learning framework that converts execution traces and outcome judgments into calibrated action-level advantage targets."
  }
]
```

---

## Implementation Notes for Renderers

A renderer should support both new and legacy fields:

- model sentence: `model_original_sentence`, `model_sentence`, `model_sentence_excerpt`, or legacy `original_sentence`;
- function: `abstract_sentence_function`;
- pattern: `model_pattern`, `reusable_model`, or `abstract_model`;
- project original: `project_original_sentence`, `target_original_sentence`, or `user_original_sentence`;
- rewrite: `rewritten_sentence` or `rewrite_of_sentence`.

Hover/click cards should display fields in this order:

1. Model paper sentence
2. Abstract function
3. Model pattern, if present
4. Project original sentence, if present
5. Rewritten sentence
