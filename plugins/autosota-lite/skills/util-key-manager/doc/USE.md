# Use Mode: Log to WandB & Notify

For agents and developers: how to use the stored credentials.

Credentials are **automatically loaded** from GCP or `.env.local`. Just use the services.

---

## WandB Logging

```python
import wandb

# Auto-loads WANDB_API_KEY
wandb.init(project="my-project", entity="my-entity")

# Log metrics
wandb.log({"step": 1, "loss": 0.5, "accuracy": 0.95})

# Save and finish
wandb.finish()
```

**Where do credentials come from?**
- Shell env: `export WANDB_API_KEY=...`
- Or GCP Secret Manager (automatic if `GCP_PROJECT_ID` is set)
- Or `.env.local` (fallback)

---

## Slack Notification

```python
import requests
import os

webhook_url = os.getenv("SLACK_WEBHOOK_URL")

# Post simple message
requests.post(webhook_url, json={"text": "✅ Training complete!"})

# Or rich message
requests.post(webhook_url, json={
    "text": "Training complete",
    "blocks": [{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*Status:* ✅ Complete\n*Loss:* 0.42\n*Accuracy:* 98.5%"
        }
    }]
})
```

---

## Gmail Notification

```python
import smtplib
from email.mime.text import MIMEText
import os

# Auto-loads GMAIL_USER and GMAIL_APP_PASSWORD
user = os.getenv("GMAIL_USER")
password = os.getenv("GMAIL_APP_PASSWORD")

# Create message
msg = MIMEText("Training complete! Loss: 0.42, Accuracy: 98.5%")
msg["Subject"] = "Training finished"
msg["From"] = user
msg["To"] = user

# Send via Gmail SMTP
with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
```

---

## Combining All Three

Full example: train model → log to WandB → notify Slack + email on completion

```python
import wandb
import requests
import smtplib
from email.mime.text import MIMEText
import os

def notify_complete(status, loss, accuracy):
    """Send notifications via Slack and email"""
    
    # Slack
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    requests.post(webhook_url, json={
        "text": f"✅ Training {status}\n📊 Loss: {loss}\n🎯 Accuracy: {accuracy}"
    })
    
    # Email
    user = os.getenv("GMAIL_USER")
    msg = MIMEText(f"Loss: {loss}, Accuracy: {accuracy}")
    msg["Subject"] = f"Training {status}"
    msg["From"] = user
    msg["To"] = user
    
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(user, os.getenv("GMAIL_APP_PASSWORD"))
        server.send_message(msg)

# Training loop
wandb.init(project="my-project")

for step in range(10):
    loss = 1.0 / (step + 1)
    accuracy = 0.8 + (step * 0.02)
    
    wandb.log({"step": step, "loss": loss, "accuracy": accuracy})
    print(f"Step {step}: loss={loss:.3f}, accuracy={accuracy:.3f}")

wandb.finish()

# Notify on completion
notify_complete("complete", loss=0.1, accuracy=0.98)
```

---

## Environment Variables

These are automatically available:

| Variable | Source | Example |
|----------|--------|---------|
| `WANDB_API_KEY` | Shell or GCP | `wandb_v1_xxxxx` |
| `SLACK_WEBHOOK_URL` | Shell or GCP | `https://hooks.slack.com/...` |
| `GMAIL_USER` | Shell or GCP | `user@gmail.com` |
| `GMAIL_APP_PASSWORD` | Shell or GCP | `xxxx xxxx xxxx xxxx` |

Access in code: `os.getenv("VARIABLE_NAME")`

---

## Verify Credentials

Before running your code:

```bash
python3 check_keys.py --services wandb,slack,email
```

Should print: `All credentials ready.`

With GCP:
```bash
python3 check_keys.py --gcp-project projectrl-485417 --services wandb,slack,email
```
