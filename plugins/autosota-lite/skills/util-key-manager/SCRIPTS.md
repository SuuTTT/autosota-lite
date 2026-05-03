# Scripts Reference

## Deploy Mode

**`enable_and_setup_secrets.py`** — Store credentials in GCP
```bash
python3 enable_and_setup_secrets.py
```
- Reads credentials from `/workspace/autosota-lite/.env.local`
- Creates secrets in GCP Secret Manager
- Verifies all three services (WandB, Slack, Gmail)

---

## Use Mode

**`check_keys.py`** — Verify credentials are ready
```bash
# Local (.env.local)
python3 check_keys.py --services wandb,slack,email

# GCP Secret Manager
python3 check_keys.py --gcp-project projectrl-485417 --services wandb,slack,email
```

**`test_gcp_integration.py`** — Test all services end-to-end
```bash
python3 test_gcp_integration.py --project projectrl-485417 --services wandb,slack,email
```

**`test_full_workflow.py`** — Full demo (log to WandB, notify Slack, email)
```bash
python3 test_full_workflow.py projectrl-485417
```

**`list_secrets.py`** — List all secrets in GCP
```bash
python3 list_secrets.py projectrl-485417
```

---

## Core Modules

**`gcp_secrets.py`** — Load secrets from GCP into environment
```python
from gcp_secrets import load_autosota_secrets
results = load_autosota_secrets("projectrl-485417")
# Credentials now in os.environ: WANDB_API_KEY, SLACK_WEBHOOK_URL, etc.
```
