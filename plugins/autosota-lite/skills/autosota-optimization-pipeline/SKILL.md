---
name: autosota-optimization-pipeline
description: Coordinate AutoSOTA optimization iterations that combine generated ideas, human ideas, domain-knowledge ideas such as Structural Entropy, reimplementation work, logging, notifications, and publishable outputs while preserving benchmark validity.
---

# AutoSOTA Optimization Pipeline

Use this skill when the user wants to organize or run the improvement loop after a baseline exists. This is a coordinator skill: it selects the right specialized skill for each stage and keeps the iteration auditable.

## Pipeline

1. **Intake**
   - Read `objective.md`, `red_lines.md`, `code_analysis.md`, `research_report.md`, `idea_library.md`, `scores.jsonl`, and `autosota.yaml` when present.
   - If a user supplies an idea directly, route through `autosota-human-idea-ingest`.
   - If ideas need to be generated, route through `autosota-agent-ideator`.

2. **Domain Knowledge**
   - For Structural Entropy, hierarchy, encoding trees, state abstraction, or decoding information, use `structural-entropy-proposal`.
   - Store domain-specific hypotheses in `idea_library.md` with type `DOMAIN`.
   - Mark assumptions separately from cited facts.

3. **Implementation Route**
   - Use `autosota-reimplementation` when the codebase should be made compact, CleanRL-style, JAX-based, or easier to compare.
   - Use `autosota-agent-fix` for runtime and dependency failures.
   - Use `autosota-agent-supervisor` before changes that could affect metric validity, test data, eval scripts, or benchmark comparability.

4. **Evaluation And Logging**
   - Record every attempted run in `scores.jsonl`.
   - Use `autosota-result-logger` for WandB, GitHub, or local standardized logs.
   - Use `autosota-common-key-manager` before configuring external services.

5. **Notification And Feedback**
   - Use `autosota-common-iteration-notifier` to notify Slack or another configured channel when long-running work completes, fails, or needs human review.
   - Use `autosota-paper-writer` for manuscripts and reports.
   - Use `autosota-common-publisher` for blog, social, or short-form post drafts after results are validated.

## Iteration Rule

Attempt one meaningful change per iteration. Each iteration must record:

- active idea id,
- files changed,
- command run,
- score or failure,
- validity decision,
- next action.

Recommend `KEEP` only when the change is valid under red-line rules and improves the selected metric against the relevant baseline. Recommend `ROLLBACK` for invalid, unverified, or worse results.

