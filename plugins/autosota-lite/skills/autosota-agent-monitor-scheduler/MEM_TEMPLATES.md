# AutoSOTA External Memory Templates

These templates ensure consistency across different agents and iterations.

## 1. Code Analysis (`code_analysis.md`)
```markdown
# Code Cognition Map: {Project Name}

## Workflow Overview
- **Data Pipeline**: How data flows from raw input to training/eval.
- **Training Entrypoint**: `path/to/train.py` (Key arguments: ...)
- **Evaluation Entrypoint**: `path/to/eval.py` (Key arguments: ...)

## Key Components
| File | Responsibility | Critical Functions |
|---|---|---|
| `model.py` | Neural architecture | `Forward()`, `Loss()` |
| `env.py` | Sim/Env wrappers | `Step()`, `Reset()` |

## Constraints & Red Lines
- [R1] metric X must not change.
- [R2] eval script is frozen.
```

## 2. Idea Library (`idea_library.md`)
```markdown
# Idea Library

### IDEA-{ID}: {Title}
- **Type**: [CODE | PARAM | LEAP]
- **Priority**: [HIGH | MEDIUM | LOW]
- **Risk**: [HIGH | MEDIUM | LOW]
- **Description**: {What and where?}
- **Hypothesis**: {Why it works?}
- **Status**: [PENDING | IN-PROGRESS | SUCCESS | FAILED]
- **Result**: {Delta and observations}
```

## 3. Research Report (`research_report.md`)
```markdown
# Research Report: {Task}

## SOTA Techniques (2023-2026)
- **Insight 1**: {Summary} -> {Actionable Strategy}
- **Insight 2**: {Summary} -> {Actionable Strategy}

## Root Cause Analysis
- **Failure Mode A**: {Observation from baseline}
- **Potential Fix**: {Link to Idea ID}

## Optimization Seeding
- List of ideas to be ported to `idea_library.md`.
```
