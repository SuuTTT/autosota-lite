# GCP Secret Manager Integration - Summary

**Date:** 2026-05-02  
**Status:** ✓ Complete - Ready for Testing

---

## What Was Implemented

A complete **Google Cloud Secret Manager integration** for AutoSOTA Lite that securely manages credentials for WandB, Slack, and Gmail without storing secrets in files or environment variables.

### New Files

| File | Purpose | Lines |
|------|---------|-------|
| `gcp_secrets.py` | Core GCP Secret Manager client | 120 |
| `test_gcp_integration.py` | End-to-end integration test | 280 |
| `check_keys.py` | Enhanced with `--gcp-project` flag and `check_email()` | 230 |
| `SKILL.md` | Updated with GCP setup guide and Gmail docs | 160 |
| `GCP_SECRET_MANAGER_GUIDE.md` | Complete setup & troubleshooting guide | 400+ |
| `setup_gcp_secrets.sh` | Automated setup script | 100 |

### Key Features

✓ **Application Default Credentials (ADC)** — No key files to manage  
✓ **Load Priority** — Shell env → GCP → .env.local (local fallback)  
✓ **Live API Validation** — Tests actual connectivity before use  
✓ **Gmail Support** — SMTP with app-specific passwords  
✓ **Slack Integration** — Incoming Webhooks  
✓ **WandB Integration** — GraphQL validation  
✓ **Graceful Fallbacks** — Works with or without GCP  

---

## Quick Start

### Option 1: Automated Setup (Recommended)

```bash
cd /workspace/autosota-lite
bash setup_gcp_secrets.sh
```

This script will:
1. Check for `gcloud` CLI
2. Ask for GCP project ID
3. Enable Secret Manager API
4. Set up Application Default Credentials (ADC)
5. Collect and store secrets
6. Install Python dependencies
7. Run the integration test

### Option 2: Manual Setup

Follow the step-by-step guide in `GCP_SECRET_MANAGER_GUIDE.md`.

### Option 3: One-Line Commands

If you already have secrets and ADC set up:

```bash
# Enable API
gcloud services enable secretmanager.googleapis.com --project=YOUR_PROJECT

# Create secrets (replace values)
echo -n "KEY" | gcloud secrets create autosota-wandb-api-key --data-file=- --project=YOUR_PROJECT
echo -n "URL" | gcloud secrets create autosota-slack-webhook-url --data-file=- --project=YOUR_PROJECT
echo -n "EMAIL" | gcloud secrets create autosota-gmail-user --data-file=- --project=YOUR_PROJECT
echo -n "PASS" | gcloud secrets create autosota-gmail-app-password --data-file=- --project=YOUR_PROJECT

# Test
pip install google-cloud-secret-manager
python3 plugins/autosota-lite/skills/autosota-common-key-manager/test_gcp_integration.py --project YOUR_PROJECT --services wandb,slack,email
```

---

## File Structure

```
/workspace/autosota-lite/
├── GCP_SECRET_MANAGER_GUIDE.md          (Setup guide with troubleshooting)
├── GCP_INTEGRATION_SUMMARY.md           (This file)
├── setup_gcp_secrets.sh                 (Automated setup script)
├── plugins/autosota-lite/skills/
│   └── autosota-common-key-manager/
│       ├── SKILL.md                     (Updated with GCP docs)
│       ├── gcp_secrets.py               (NEW)
│       ├── check_keys.py                (Enhanced with --gcp-project)
│       └── test_gcp_integration.py      (NEW)
```

---

## API Reference

### `gcp_secrets.py`

```python
from gcp_secrets import load_secrets, load_autosota_secrets

# Load a custom set of secrets
results = load_secrets(
    project_id="my-gcp-project",
    secret_map={
        "my-secret-name": "MY_ENV_VAR",
    }
)
# Returns: {"MY_ENV_VAR": "ok" | "missing" | "error"}

# Load canonical autosota-lite secrets
results = load_autosota_secrets("my-gcp-project")
# Loads WANDB_API_KEY, SLACK_WEBHOOK_URL, GMAIL_USER, GMAIL_APP_PASSWORD
```

### `check_keys.py`

```bash
# Check local (.env.local) credentials
python3 check_keys.py --services wandb,slack,email

# Check GCP Secret Manager credentials
python3 check_keys.py --gcp-project MY_GCP_PROJECT --services wandb,slack,email

# Check specific services
python3 check_keys.py --gcp-project MY_GCP_PROJECT --services wandb
```

### `test_gcp_integration.py`

```bash
# Full test
python3 test_gcp_integration.py --project MY_GCP_PROJECT --services wandb,slack,email

# Test specific service
python3 test_gcp_integration.py --project MY_GCP_PROJECT --services slack
```

---

## Using GCP Secrets in Your Code

### In Python Scripts

```python
import os
from gcp_secrets import load_autosota_secrets

# Load from GCP at startup
load_autosota_secrets("my-gcp-project")

# Use like normal env vars
wandb_key = os.getenv("WANDB_API_KEY")
slack_url = os.getenv("SLACK_WEBHOOK_URL")
gmail_user = os.getenv("GMAIL_USER")
```

### In Shell Scripts

```bash
# One-time load
python3 -c "from gcp_secrets import load_autosota_secrets; load_autosota_secrets('MY_PROJECT')"

# Now the env vars are set in this Python process...
# For shell scripts, use check_keys.py with --gcp-project before running jobs
```

---

## Secret Naming Convention

All secrets follow this pattern:

```
autosota-{service}-{credential-type}
```

| Secret Name | Env Var | Type | Example |
|-------------|---------|------|---------|
| `autosota-wandb-api-key` | `WANDB_API_KEY` | API Key | `wandb_v1_...` |
| `autosota-slack-webhook-url` | `SLACK_WEBHOOK_URL` | URL | `https://hooks.slack.com/...` |
| `autosota-gmail-user` | `GMAIL_USER` | Email | `your@gmail.com` |
| `autosota-gmail-app-password` | `GMAIL_APP_PASSWORD` | Password | (16 chars) |

---

## Load Priority

When loading credentials, the following order is used:

```
1. Shell environment variables (highest)
   Checked first: if set, use immediately
   
2. GCP Secret Manager
   If --gcp-project is set, load from GCP
   Requires: gcloud auth application-default login
   
3. .env.local file (fallback)
   For local development without GCP
   Never committed to git
```

Example:

```bash
# If WANDB_API_KEY is already set in shell, that takes priority
export WANDB_API_KEY=from_shell

# This loads it from GCP only if not already set
python3 -c "from gcp_secrets import load_autosota_secrets; load_autosota_secrets('project')"

# But you can force override with overwrite=True
from gcp_secrets import load_autosota_secrets
load_autosota_secrets("project", overwrite=True)
```

---

## Testing Checklist

### ✓ Pre-flight Checks

```bash
# 1. Verify gcloud is installed
gcloud --version

# 2. Verify ADC is configured
gcloud auth application-default print-access-token

# 3. Verify Secret Manager API is enabled
gcloud services list --enabled --project=YOUR_PROJECT | grep secretmanager

# 4. Verify secrets exist
gcloud secrets list --project=YOUR_PROJECT

# 5. Verify Python dependencies
pip list | grep google-cloud-secret-manager
```

### ✓ Integration Tests

```bash
cd /workspace/autosota-lite/plugins/autosota-lite/skills/autosota-common-key-manager

# 1. Test GCP secrets module directly
python3 -c "from gcp_secrets import load_autosota_secrets; load_autosota_secrets('YOUR_PROJECT'); import os; print(f'WANDB_API_KEY: {os.getenv(\"WANDB_API_KEY\")}')"

# 2. Test check_keys.py
python3 check_keys.py --gcp-project YOUR_PROJECT --services wandb,slack,email

# 3. Test full integration
python3 test_gcp_integration.py --project YOUR_PROJECT --services wandb,slack,email
```

---

## Known Limitations

1. **Email only supports Gmail** — SMTP with app-specific passwords
2. **ADC required** — No support for service account key files (by design)
3. **Secret updates** — New versions via `gcloud secrets versions add` take effect immediately
4. **Read-only** — The code only reads secrets, doesn't create/delete them (use `gcloud` CLI)

---

## Security Best Practices

### ✓ DO

- Use Application Default Credentials (ADC) for local development
- Use service account credentials in production/CI environments
- Rotate secrets regularly: `gcloud secrets versions add <name> --data-file=-`
- Grant minimal IAM permissions: `roles/secretmanager.secretAccessor` (read-only)
- Enable Secret Manager audit logging in GCP
- Use `.env.local` only in local dev (never commit)

### ✗ DON'T

- Store secrets in code, chat, or logs
- Use full GCP project Editor role for service accounts
- Share ADC credentials files (`~/.config/gcloud/application_default_credentials.json`)
- Commit `.env.local` or key files to git
- Log secret values (the code redacts them automatically)

---

## Troubleshooting

See the detailed troubleshooting section in `GCP_SECRET_MANAGER_GUIDE.md`.

Common issues:
- **"DefaultCredentialsError"** → Run `gcloud auth application-default login`
- **"Secret not found"** → Verify secret name matches exactly
- **"Permission denied"** → Grant IAM role: `roles/secretmanager.admin`
- **"Gmail authentication failed"** → Use app password, not Gmail password
- **"Slack webhook 404"** → Webhook URL is revoked, regenerate it

---

## Next Steps

1. **Run the setup script:**
   ```bash
   bash setup_gcp_secrets.sh
   ```

2. **Save your GCP project ID:**
   ```bash
   echo 'export GCP_PROJECT_ID=YOUR_PROJECT' >> ~/.bashrc
   source ~/.bashrc
   ```

3. **Use in workflows:**
   ```bash
   python3 check_keys.py --gcp-project $GCP_PROJECT_ID --services wandb,slack,email
   ```

4. **Integrate into CI/CD** (GitHub Actions, Cloud Build, etc.)

---

## Documentation Files

| File | Purpose |
|------|---------|
| `GCP_SECRET_MANAGER_GUIDE.md` | Complete setup guide with step-by-step instructions |
| `setup_gcp_secrets.sh` | Interactive automated setup script |
| `skills/autosota-common-key-manager/SKILL.md` | Integration with autosota-lite plugin system |
| `skills/autosota-common-key-manager/gcp_secrets.py` | Core Python module |
| `skills/autosota-common-key-manager/check_keys.py` | Credential verification CLI |
| `skills/autosota-common-key-manager/test_gcp_integration.py` | Integration test suite |

---

## Questions?

Refer to:
- **Setup help:** See `GCP_SECRET_MANAGER_GUIDE.md`
- **API reference:** See inline docstrings in `gcp_secrets.py`
- **GCP docs:** https://cloud.google.com/secret-manager/docs
- **Troubleshooting:** See last section of `GCP_SECRET_MANAGER_GUIDE.md`

---

**Ready to get started?**

```bash
bash setup_gcp_secrets.sh
```
