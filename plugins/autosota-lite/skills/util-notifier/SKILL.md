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

The bundled `notify.py` posts to Slack via an **Incoming Webhook** (one URL → one channel, no bot install).

### One-time setup

1. https://api.slack.com/apps → **Create New App** → From scratch → name it (e.g. "AutoSOTA Notifier") → pick the workspace.
2. Left sidebar → **Incoming Webhooks** → toggle **Activate** → **Add New Webhook to Workspace** → pick the channel.
3. Copy the URL (`https://hooks.slack.com/services/T.../B.../...`).
4. Store the URL in `.env.local` at the repo root (gitignored — see `autosota-common-key-manager`):

   ```bash
   echo 'SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...' >> /workspace/autosota-lite/.env.local
   ```

5. Verify with `python3 plugins/autosota-lite/skills/autosota-common-key-manager/check_keys.py --services slack`.

### Sending

```bash
python3 plugins/autosota-lite/skills/autosota-common-iteration-notifier/notify.py \
  --project autosota-research/run-2026-04-30 \
  --status complete \
  --idea "se-001 structural-entropy regularizer" \
  --metric "score 0.612 → 0.638" \
  --validity valid \
  --artifacts "https://wandb.ai/sudingli21/autosota/runs/abc123" \
  --next-step "review and merge PR #42"
```

Use `--dry-run` first to preview the rendered message without sending.

### Rules

- Never paste the webhook URL into chat or commit it. The script reads it from env / `.env.local`.
- Do not include secrets, full stack traces, or huge logs in notifications. Link or reference artifact paths instead.
- If the webhook is missing or not authorized, fall back to printing the rendered message as a draft (use `--dry-run`).

