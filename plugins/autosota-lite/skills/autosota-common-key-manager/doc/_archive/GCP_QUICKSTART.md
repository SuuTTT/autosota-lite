# GCP Secret Manager - Quick Start

Everything you need to integrate Google Cloud Secret Manager with AutoSOTA Lite for WandB, Slack, and Gmail.

## 🚀 Get Started in 5 Minutes

### Step 1: Run the Setup Script

```bash
bash setup_gcp_secrets.sh
```

This will:
- Prompt for your GCP project ID
- Enable Secret Manager API
- Authenticate with Application Default Credentials
- Collect and store your secrets
- Run integration tests

### Step 2: Verify It Works

```bash
cd plugins/autosota-lite/skills/autosota-common-key-manager
python3 check_keys.py --gcp-project YOUR_GCP_PROJECT --services wandb,slack,email
```

### Step 3: Use in Your Workflows

From shell:
```bash
python3 check_keys.py --gcp-project YOUR_GCP_PROJECT --services wandb,slack,email
```

From Python:
```python
from gcp_secrets import load_autosota_secrets
load_autosota_secrets("YOUR_GCP_PROJECT")
# Now use os.getenv("WANDB_API_KEY"), etc.
```

---

## 📖 Full Documentation

- **Setup guide with all steps:** [GCP_SECRET_MANAGER_GUIDE.md](./GCP_SECRET_MANAGER_GUIDE.md)
- **Complete summary & API reference:** [GCP_INTEGRATION_SUMMARY.md](./GCP_INTEGRATION_SUMMARY.md)
- **Plugin documentation:** [plugins/autosota-lite/skills/autosota-common-key-manager/SKILL.md](./plugins/autosota-lite/skills/autosota-common-key-manager/SKILL.md)

---

## 🔑 What Secrets Are Supported

| Service | Secret | How to Get |
|---------|--------|-----------|
| **WandB** | API Key | https://wandb.ai/settings/keys |
| **Slack** | Webhook URL | https://api.slack.com/apps → Incoming Webhooks |
| **Gmail** | Email & App Password | https://myaccount.google.com/apppasswords |

---

## ⚡ Commands Cheat Sheet

```bash
# Automated setup (recommended)
bash setup_gcp_secrets.sh

# Manual: Create a secret
echo -n "YOUR_VALUE" | gcloud secrets create autosota-secret-name --data-file=- --project=YOUR_PROJECT

# Verify credentials from GCP
python3 plugins/autosota-lite/skills/autosota-common-key-manager/check_keys.py \
  --gcp-project YOUR_PROJECT --services wandb,slack,email

# Run full integration test
python3 plugins/autosota-lite/skills/autosota-common-key-manager/test_gcp_integration.py \
  --project YOUR_PROJECT --services wandb,slack,email

# Update a secret (creates new version)
echo -n "NEW_VALUE" | gcloud secrets versions add autosota-secret-name --data-file=- --project=YOUR_PROJECT

# List all secrets
gcloud secrets list --project=YOUR_PROJECT
```

---

## 🔐 Security Highlights

✓ **No key files** — Uses Application Default Credentials (ADC)  
✓ **Encrypted at rest** — GCP Secret Manager encryption  
✓ **Audit trail** — All access logged in GCP  
✓ **Graceful fallback** — Works without GCP via .env.local  
✓ **Secret redaction** — Never prints full values to logs  

---

## ⚠️ Requirements

- **gcloud CLI** ([install](https://cloud.google.com/sdk/docs/install))
- **Python 3.8+** with pip
- **GCP project** with billing enabled
- **Service credentials:**
  - WandB API key
  - Slack Incoming Webhook URL
  - Gmail account with app-specific password

---

## 🆘 Troubleshooting

### "gcloud: command not found"
Install from https://cloud.google.com/sdk/docs/install

### "DefaultCredentialsError"
Run: `gcloud auth application-default login`

### "Secret not found"
Check: `gcloud secrets list --project=YOUR_PROJECT`

### Gmail SMTP fails
Use **app password** (not Gmail password): https://myaccount.google.com/apppasswords

See **[GCP_SECRET_MANAGER_GUIDE.md](./GCP_SECRET_MANAGER_GUIDE.md)** for full troubleshooting.

---

## 📚 Files Overview

```
.
├── setup_gcp_secrets.sh                    ← Run this first
├── GCP_QUICKSTART.md                       ← You are here
├── GCP_SECRET_MANAGER_GUIDE.md             ← Detailed setup guide
├── GCP_INTEGRATION_SUMMARY.md              ← Full documentation
└── plugins/autosota-lite/skills/autosota-common-key-manager/
    ├── SKILL.md                            ← Plugin documentation
    ├── gcp_secrets.py                      ← Core module
    ├── check_keys.py                       ← Verification CLI
    └── test_gcp_integration.py             ← Integration tests
```

---

**Ready?** Run: `bash setup_gcp_secrets.sh`
