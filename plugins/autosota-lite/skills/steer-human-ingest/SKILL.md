---
name: autosota-human-idea-ingest
description: Ingest user-proposed research intuitions into AutoSOTA by preserving the human prior in research_report.md, expanding it into audited scheduler-ready hypotheses in idea_library.md, and routing protocol-sensitive ideas through AgentSupervisor before execution.
---

# AutoSOTA Human Idea Ingest

Use this skill when the user contributes a research intuition, preferred direction, suspected bottleneck, or concrete improvement idea. Human ideas are first-class priors, but they still pass through the same validity, evidence, and scheduling gates as generated ideas.

## Operating Rule

Preserve the user's intent while converting it into executable, protocol-respecting hypotheses. Do not execute a human idea just because it is human-authored; audit it for metric alignment, implementation plausibility, scientific constraints, and risk.

## Artifact Responsibilities

- **`research_report.md`**: Add the idea under a `Human Priors` or `User Hypotheses` section. Record the intuition, rationale, external evidence, conflicting evidence, and open questions.
- **`idea_library.md`**: Add one or more concrete derived hypotheses with granularity, risk, admissibility, implementation sketch, and scheduler status.
- **`red_lines.md`**: Update only if the human idea reveals a new constraint or tempting invalid shortcut.
- **`scores.jsonl`**: Do not update until a scheduled run produces evidence.

## Workflow

1. **Capture the human prior**
   - Quote or paraphrase the user's idea faithfully.
   - Identify the target metric, expected mechanism, and affected code area.
   - Mark whether the idea is broad, concrete, or already executable.

2. **Ground with evidence**
   - Search existing artifacts first: `code_analysis.md`, `research_report.md`, `idea_library.md`, scores, and logs.
   - When useful, perform external research and cite primary sources or official project material.
   - Distinguish direct evidence from analogy or inference.

3. **Decompose into hypotheses**
   - Convert broad ideas into concrete candidates.
   - Prefer a low-risk probe before a high-risk rewrite.
   - Keep separate hypotheses for parameter probes, code-local probes, and algorithmic changes.

4. **Audit admissibility**
   - Preserve frozen metrics, evaluation scripts, dataset splits, labels, and task definitions.
   - Mark reward shaping, test-set leakage, altered evaluation semantics, or post-hoc output hacks as `REJECTED`.
   - Mark methodology-touching ideas as `REVIEW` unless the protocol case is clear.

5. **Prepare scheduler handoff**
   - Choose the smallest cleared probe as the next executable idea.
   - Record dependencies, expected runtime, validation command, and rollback condition.

## `research_report.md` Pattern

```markdown
## Human Prior: {short title}
- **User idea**: {faithful statement}
- **Mechanism**: {why it might work}
- **Evidence**: {paper/code/literature support}
- **Counter-evidence or risks**: {why it might fail}
- **Executable probes**: {idea IDs}
```

## `idea_library.md` Pattern

```markdown
### IDEA-{ID}: {title}
- **Origin**: Human prior
- **Granularity**: PARAM | CODE | ALGO
- **Risk**: LOW | MEDIUM | HIGH
- **Admissibility**: CLEARED | REVIEW | REJECTED
- **Priority**: HIGH | MEDIUM | LOW
- **Metric Target**: {exact metric}
- **Lever**: {file/config/algorithmic component}
- **Evidence**: {supporting artifact or source}
- **Hypothesis**: {testable prediction}
- **Protocol Audit**: {why evaluation integrity is preserved}
- **Implementation Sketch**: {commands or files}
- **Status**: PENDING | IN-PROGRESS | SUCCESS | FAILED | REJECTED
- **Result**: TBD
```

## Output

Report:

- Human prior captured.
- Research evidence added.
- Derived ideas and admissibility states.
- Next executable Scheduler idea.
- Any ideas rejected or requiring review.
