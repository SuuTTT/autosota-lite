---
name: autosota-common-key-manager
description: Manage API credentials securely for WandB, Slack, Gmail, and GitHub integrations. Supports both local (.env.local) and GCP Secret Manager storage.
---

# AutoSOTA Common Key Manager

Securely manage credentials for WandB, Slack, Gmail, and GitHub. No secrets in chat, logs, or git.

## Quick Start

**Use mode** (for agents/developers):
```python
# Credentials are automatically loaded from GCP or .env.local
# Just call your service:
import wandb
wandb.init(project="my-project")  # Uses WANDB_API_KEY
wandb.log({"loss": 0.5})
```

**Deploy mode** (one-time setup):
```bash
# 1. Add credentials to /workspace/autosota-lite/.env.local
# 2. Verify they work:
python3 check_keys.py --services wandb,slack,email
# 3. (Optional) Push to GCP Secret Manager:
python3 enable_and_setup_secrets.py
```

---

## Mode 1: Deploy (One-Time Setup)

### Option A: Local Only (.env.local)

**Best for:** Local dev, quick testing

1. Create `/workspace/autosota-lite/.env.local`:
```
WANDB_API_KEY=wandb_v1_xxxxx
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/T00/B00/xxx
GMAIL_USER=your.email@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
```

2. Verify:
```bash
cd plugins/autosota-lite/skills/autosota-common-key-manager
python3 check_keys.py --services wandb,slack,email
```

### Option B: GCP Secret Manager

**Best for:** Production, shared environments

1. **Enable API** (manual step in GCP console):
   - Visit: https://console.cloud.google.com/apis/library/secretmanager.googleapis.com?project=projectrl-485417
   - Click **ENABLE**

2. **Store credentials**:
```bash
cd plugins/autosota-lite/skills/autosota-common-key-manager
python3 enable_and_setup_secrets.py
```

3. **Verify**:
```bash
export GCP_PROJECT_ID=projectrl-485417
python3 check_keys.py --gcp-project projectrl-485417 --services wandb,slack,email
```

---

## Mode 2: Use (Agent/Developer Usage)

Credentials are automatically loaded. Just use the services:

### WandB Logging
```python
import wandb

wandb.init(project="my-project", entity="my-entity")
wandb.log({"step": 1, "loss": 0.5, "accuracy": 0.95})
wandb.finish()
```

### Slack Notification
```python
import requests
import os

webhook_url = os.getenv("SLACK_WEBHOOK_URL")
requests.post(webhook_url, json={"text": "Training complete!"})
```

### Gmail Notification
```python
import smtplib
from email.mime.text import MIMEText
import os

msg = MIMEText("Training complete!")
msg["Subject"] = "Run finished"
msg["From"] = os.getenv("GMAIL_USER")
msg["To"] = os.getenv("GMAIL_USER")

with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(os.getenv("GMAIL_USER"), os.getenv("GMAIL_APP_PASSWORD"))
    server.send_message(msg)
```

---

## Service Credentials Map

| Service | Env Var(s) | GCP Secret | Need? |
|---------|-----------|-----------|-------|
| WandB | `WANDB_API_KEY` | `autosota-wandb-api-key` | ✓ Yes |
| Slack | `SLACK_WEBHOOK_URL` | `autosota-slack-webhook-url` | Optional |
| Gmail | `GMAIL_USER`, `GMAIL_APP_PASSWORD` | `autosota-gmail-user`, `autosota-gmail-app-password` | Optional |
| GitHub | `GITHUB_TOKEN` | N/A | Optional |

### Getting Credentials

**WandB API Key:**
- https://wandb.ai/settings/keys

**Slack Webhook URL:**
- https://api.slack.com/apps → Your App → Incoming Webhooks

**Gmail App Password:**
- https://myaccount.google.com/apppasswords (requires 2FA enabled)
- Select "Mail" and "Windows Computer"

---

## Load Priority

Credentials are loaded in this order:
1. Shell environment variables (highest priority)
2. GCP Secret Manager (if `GCP_PROJECT_ID` is set)
3. `.env.local` file (fallback)

---

## Rules

- Never paste secrets into chat, logs, or commit to git
- Never commit `.env` or `.env.local` files
- `.env.local` is gitignored — keep credentials there
- Redact secrets in output (show only first 6 chars)
- Rotate keys immediately if exposed

---

## Troubleshooting

**"credentials not found"**
- Verify `.env.local` exists and is readable
- Or verify GCP Secret Manager has the secrets with: `python3 list_secrets.py`

**"SMTP login failed"**
- Use Gmail **app password**, not your account password
- Get it from: https://myaccount.google.com/apppasswords

**"Secret Manager API not enabled"**
- Enable manually: https://console.cloud.google.com/apis/library/secretmanager.googleapis.com
- Then run: `python3 enable_and_setup_secrets.py`

---

## Commands Reference

```bash
# Verify credentials are ready
python3 check_keys.py --services wandb,slack,email

# Load from GCP and verify
python3 check_keys.py --gcp-project projectrl-485417 --services wandb,slack,email

# Store all credentials in GCP
python3 enable_and_setup_secrets.py

# List secrets in GCP
python3 list_secrets.py projectrl-485417

# Full integration test (log to WandB, post to Slack, email report)
python3 test_full_workflow.py projectrl-485417
```
