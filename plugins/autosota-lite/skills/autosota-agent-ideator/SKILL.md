---
name: autosota-agent-ideator
description: AgentIdeator skill for constraint-aware hypothesis construction in AutoSOTA, producing research_report.md and idea_library.md with admissible PARAM, CODE, and ALGO hypotheses grounded in metrics, codebase capabilities, scientific constraints, and optimization levers.
---

# AutoSOTA AgentIdeator: Constraint-Aware Hypothesis Construction

Use this skill before expensive optimization begins, or when the hypothesis pool needs a principled refresh. AgentIdeator is not free-form brainstorming: it constructs a structured, auditable search space of improvement hypotheses that preserve the paper protocol.

## Operating Rule

Generate only hypotheses that can be evaluated under the original experimental contract. Reject ideas that depend on changing metrics, evaluation logic, dataset splits, labels, test-data access, output post-processing that violates the paper protocol, or any shortcut that breaks comparability with the baseline.

## Inputs

- Paper objective, reported metrics, dataset split, evaluation command, and methodological constraints.
- Repository cognition, ideally from `code_analysis.md`.
- External research prior, ideally from `research_report.md`.
- Existing idea pool and outcomes, ideally from `idea_library.md`.
- AgentSupervisor red lines for the current paper.

## Artifact Responsibilities

- **`research_report.md`**: AgentIdeator creates or refreshes this when external research context is missing or stale. It should summarize task-relevant SOTA patterns, empirical heuristics, community best practices, and concrete optimization strategies.
- **`idea_library.md`**: AgentIdeator creates and curates this as the systematized hypothesis library. It records admissible, rejected, and human-review ideas with audit notes.
- **`code_analysis.md`**: AgentIdeator reads this for implementation alignment, but usually does not own it. If missing, request or trigger code cognition before finalizing risky code-level ideas.

## Alignment Checks

For every hypothesis, enforce four alignments:

1. **Metric Alignment**
   - Targets the exact metric and objective reported by the paper.
   - Avoids generic "improve performance" claims without a path to the reported score.

2. **Implementation Alignment**
   - Maps to available files, configs, dependencies, checkpoints, or data artifacts.
   - States the likely intervention point and expected verification command.

3. **Constraint Alignment**
   - Preserves evaluation scripts, dataset splits, labels, method boundaries, and paper-specific invariants.
   - Routes uncertain cases to human review instead of silently accepting them.

4. **Lever Alignment**
   - Connects a high-level research insight to a concrete lever: hyperparameter, code path, algorithmic module, inference policy, data preprocessing allowed by the paper, or evaluation-compatible calibration.

## Hypothesis Taxonomy

Assign each hypothesis a granularity:

- **`PARAM`**: parameter, threshold, prompt, seed, scheduler, batch, cache, or config change.
- **`CODE`**: localized implementation change, compatibility fix, feature extraction adjustment, aggregation logic, or inference wrapper that preserves semantics.
- **`ALGO`**: structural or methodological change that remains within the paper's admissible scope.

Assign each hypothesis a risk:

- **`LOW`**: directly supported by paper/code and unlikely to affect comparability.
- **`MEDIUM`**: plausible but requires careful audit or limited-scope validation.
- **`HIGH`**: may be valid but touches methodology, evaluation-adjacent logic, or assumptions requiring explicit review.

Assign each hypothesis an admissibility status:

- **`ADMISSIBLE`**: preserves evaluation integrity.
- **`REJECTED`**: depends on a prohibited shortcut.
- **`REVIEW`**: cannot be judged without human or AgentSupervisor review.

## Workflow

1. **Ground the task**
   - Extract target metrics, baseline score, evaluation entrypoint, dataset split, frozen files, and paper-specific red lines.
   - Read `code_analysis.md` if available; otherwise perform targeted repository inspection sufficient to avoid ungrounded hypotheses.

2. **Build or refresh external prior**
   - Create or update `research_report.md` with task-specific literature patterns and best practices.
   - Keep the report actionable: each insight should imply one or more candidate levers.

3. **Generate candidate hypotheses**
   - Cover a balanced search space across `PARAM`, `CODE`, and `ALGO`.
   - Prefer high-evidence, low-risk hypotheses early; reserve high-risk ideas for explicit review.
   - Include rejected ideas when useful to document why tempting shortcuts are invalid.

4. **Audit admissibility**
   - Apply AgentSupervisor red lines before adding a candidate to the admissible pool.
   - Mark any idea that could change evaluation semantics, leak labels, alter splits, or overfit to test answers as `REJECTED`.

5. **Write the hypothesis library**
   - Save candidates to `idea_library.md`.
   - Include enough implementation detail for AgentScheduler to select and execute without rediscovering the rationale.

6. **Prepare scheduler handoff**
   - Prioritize hypotheses by expected value, risk, and cost.
   - Identify dependencies between ideas and note which can be tested independently.

## `idea_library.md` Entry Format

```markdown
### IDEA-{ID}: {Title}
- **Granularity**: PARAM | CODE | ALGO
- **Risk**: LOW | MEDIUM | HIGH
- **Admissibility**: ADMISSIBLE | REJECTED | REVIEW
- **Priority**: HIGH | MEDIUM | LOW
- **Metric Target**: {exact metric(s)}
- **Lever**: {concrete intervention point}
- **Evidence**: {paper/code/research_report support}
- **Hypothesis**: {why this should improve the metric}
- **Protocol Audit**: {why it preserves or violates constraints}
- **Implementation Sketch**: {files, configs, commands}
- **Status**: PENDING | IN-PROGRESS | SUCCESS | FAILED | REJECTED
- **Result**: {delta, notes, or reason rejected}
```

## `research_report.md` Expectations

The report should include:

- Task and metric framing.
- Relevant SOTA or community patterns.
- Empirical heuristics and failure modes.
- Concrete optimization levers mapped to candidate idea IDs.
- Warnings about invalid shortcuts or protocol-sensitive areas.

## Rejection Examples

Reject or route to review:

- Changing the metric implementation or acceptance threshold.
- Using labels, ground-truth answers, or test-set statistics unavailable under the paper protocol.
- Filtering hard examples or changing dataset splits.
- Post-processing outputs in a way the original method could not justify.
- Replacing the core method with a stronger external model when the paper requires a fixed model setting.

## Output

Report:

- Number of admissible, rejected, and review-required ideas.
- The highest-priority admissible ideas.
- The red-line risks discovered.
- Paths updated: usually `research_report.md` and `idea_library.md`.
