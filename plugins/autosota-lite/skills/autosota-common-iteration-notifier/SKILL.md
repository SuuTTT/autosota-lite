---
name: autosota-common-iteration-notifier
description: Send or draft completion, failure, and review-needed notifications for AutoSOTA experiment iterations through Slack or other configured channels, using concise status summaries grounded in logs and scores.
---

# AutoSOTA Common Iteration Notifier

Use this skill when a long-running job completes, fails, improves a score, needs human review, or reaches a budget limit.

## Inputs

- `scores.jsonl`, latest run log, scheduler log, or WandB run URL.
- Active idea id and hypothesis from `idea_library.md`.
- Benchmark red-line status from `red_lines.md` or `autosota-agent-supervisor`.
- Destination: Slack channel, direct message, issue comment, or local draft.

## Message Shape

Keep notifications short and action-oriented:

```text
AutoSOTA update: <project/run>
Status: <complete|failed|needs review|budget reached>
Idea: <id and short name>
Metric: <baseline -> current, or failure reason>
Validity: <valid|invalid|unknown>
Artifacts: <log path, WandB URL, PR/commit if available>
Next: <one requested action or next planned step>
```

## Slack

When the Slack connector is available and the user asked to send, use the Slack workflow and post only after checking the destination. If sending is not available or not authorized, create a ready-to-send draft in the final response or a local artifact requested by the user.

Do not include secrets, full stack traces, or huge logs in notifications. Link or reference artifact paths instead.

