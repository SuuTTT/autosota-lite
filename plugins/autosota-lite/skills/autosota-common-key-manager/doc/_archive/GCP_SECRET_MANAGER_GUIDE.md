# GCP Secret Manager Integration Guide for AutoSOTA Lite

This guide walks you through setting up Google Cloud Secret Manager as the authoritative secret source for WandB, Slack, and Gmail credentials in AutoSOTA Lite.

---

## Table of Contents

1. [Architecture](#architecture)
2. [Prerequisites](#prerequisites)
3. [Step 1: Enable the Secret Manager API](#step-1-enable-the-secret-manager-api)
4. [Step 2: Authenticate with Application Default Credentials](#step-2-authenticate-with-application-default-credentials)
5. [Step 3: Create Secrets in GCP](#step-3-create-secrets-in-gcp)
6. [Step 4: Install Dependencies](#step-4-install-dependencies)
7. [Step 5: Run the Integration Test](#step-5-run-the-integration-test)
8. [Step 6: Use in Your Workflows](#step-6-use-in-your-workflows)
9. [Troubleshooting](#troubleshooting)

---

## Architecture

### Load Priority

Credentials are loaded in this order:

```
1. Shell environment variables (highest priority)
   └─ e.g., export WANDB_API_KEY=xyz

2. GCP Secret Manager (if --gcp-project is set)
   └─ Uses Application Default Credentials
   └─ No key files needed

3. .env.local file (local fallback)
   └─ For development without GCP
   └─ Never committed to git
```

### Secret Naming Convention

All secrets in GCP follow a consistent naming pattern:

| Environment Variable | GCP Secret Name | Purpose |
|----------------------|-----------------|---------|
| `WANDB_API_KEY` | `autosota-wandb-api-key` | WandB authentication |
| `SLACK_WEBHOOK_URL` | `autosota-slack-webhook-url` | Slack message delivery |
| `GMAIL_USER` | `autosota-gmail-user` | Gmail sender address |
| `GMAIL_APP_PASSWORD` | `autosota-gmail-app-password` | Gmail SMTP password |

---

## Prerequisites

- A Google Cloud Platform (GCP) project
- `gcloud` CLI installed ([install guide](https://cloud.google.com/sdk/docs/install))
- The following credentials:
  - **WandB API key** from https://wandb.ai/settings/keys
  - **Slack Webhook URL** from your Slack app configuration
  - **Gmail address** and **app-specific password** (see [Gmail Setup](#gmail-setup) section)
- Python 3.8+ with pip

---

## Step 1: Enable the Secret Manager API

Replace `YOUR_GCP_PROJECT` with your actual GCP project ID:

```bash
gcloud services enable secretmanager.googleapis.com --project=YOUR_GCP_PROJECT
```

**Verify it worked:**
```bash
gcloud services list --enabled --project=YOUR_GCP_PROJECT | grep secretmanager
```

You should see:
```
secretmanager.googleapis.com    Secret Manager API
```

---

## Step 2: Authenticate with Application Default Credentials

Application Default Credentials (ADC) is a simple way to authenticate without managing key files:

```bash
gcloud auth application-default login
```

This will:
1. Open your browser to Google's login page
2. Ask for permission to access GCP
3. Save a local credentials file at `~/.config/gcloud/application_default_credentials.json`

**Verify it worked:**
```bash
gcloud auth application-default print-access-token
```

If you see a long token, you're authenticated.

---

## Step 3: Create Secrets in GCP

### 3.1 WandB API Key

Get your API key from https://wandb.ai/settings/keys

```bash
echo -n "YOUR_WANDB_API_KEY" | gcloud secrets create autosota-wandb-api-key \
  --data-file=- \
  --project=YOUR_GCP_PROJECT
```

**Verify it was created:**
```bash
gcloud secrets list --project=YOUR_GCP_PROJECT | grep wandb
```

### 3.2 Slack Webhook URL

Get your Incoming Webhook URL from your Slack app: https://api.slack.com/apps

```bash
echo -n "https://hooks.slack.com/services/TXXXXXXXX/BXXXXXXXX/XXXXXXXXXXXXXXXX" | \
  gcloud secrets create autosota-slack-webhook-url \
  --data-file=- \
  --project=YOUR_GCP_PROJECT
```

**Verify it was created:**
```bash
gcloud secrets list --project=YOUR_GCP_PROJECT | grep slack
```

### 3.3 Gmail User

Store your Gmail address:

```bash
echo -n "your.email@gmail.com" | gcloud secrets create autosota-gmail-user \
  --data-file=- \
  --project=YOUR_GCP_PROJECT
```

### 3.4 Gmail App Password

#### First, Generate an App Password

1. Go to https://myaccount.google.com/security
2. Enable **2-Step Verification** if not already enabled
3. Go to https://myaccount.google.com/apppasswords
4. Select "Mail" and "Windows Computer" (or your device)
5. Copy the 16-character password

#### Store it in GCP

```bash
echo -n "YOUR_GMAIL_APP_PASSWORD" | gcloud secrets create autosota-gmail-app-password \
  --data-file=- \
  --project=YOUR_GCP_PROJECT
```

**Verify all secrets were created:**
```bash
gcloud secrets list --project=YOUR_GCP_PROJECT
```

You should see:
```
NAME                               CREATED             REPLICATION_POLICY
autosota-gmail-app-password        2026-05-02T...      automatic
autosota-gmail-user                2026-05-02T...      automatic
autosota-slack-webhook-url         2026-05-02T...      automatic
autosota-wandb-api-key             2026-05-02T...      automatic
```

---

## Step 4: Install Dependencies

Install the Google Cloud Secret Manager Python client:

```bash
pip install google-cloud-secret-manager
```

Verify the installation:
```bash
python3 -c "from google.cloud import secretmanager; print('✓ google-cloud-secret-manager installed')"
```

---

## Step 5: Run the Integration Test

Navigate to the key manager directory:

```bash
cd /workspace/autosota-lite/plugins/autosota-lite/skills/autosota-common-key-manager
```

Run the full integration test:

```bash
python3 test_gcp_integration.py --project YOUR_GCP_PROJECT --services wandb,slack,email
```

You should see detailed output for each service:

```
======================================================================
AutoSOTA Lite - GCP Secret Manager Integration Test
======================================================================

[GCP] Loading from project: YOUR_GCP_PROJECT
[GCP] WANDB_API_KEY: loaded ✓
[GCP] SLACK_WEBHOOK_URL: loaded ✓
[GCP] GMAIL_USER: loaded ✓
[GCP] GMAIL_APP_PASSWORD: loaded ✓

[WandB] Testing GraphQL authentication...
[WandB] ✓ SUCCESS
         Username: your-wandb-username
         Entity: your-entity
         Key: wandb_***

[Slack] Posting test message...
[Slack] ✓ SUCCESS
         HTTP Status: 200
         Response: ok

[Gmail] Testing SMTP connection and sending test email...
[Gmail] ✓ SUCCESS
         User: your.email@gmail.com
         SMTP: smtp.gmail.com:587 (TLS)
         Sent test email to: your.email@gmail.com

======================================================================
ALL TESTS PASSED (3)
```

---

## Step 6: Use in Your Workflows

### Option A: Check Credentials Before Running Jobs

```bash
python3 check_keys.py --gcp-project YOUR_GCP_PROJECT --services wandb,slack,email
```

This validates all credentials without exposing them:

```
[GCP] Loading secrets from project YOUR_GCP_PROJECT...
[GCP] WANDB_API_KEY: ok
[GCP] SLACK_WEBHOOK_URL: ok
[GCP] GMAIL_USER: ok
[GCP] GMAIL_APP_PASSWORD: ok

[WandB] OK — WANDB_API_KEY=wandb_*** (user: your-username, entity: your-entity)
[Slack] OK — webhook configured (https://hooks.slack.com/***)
[Gmail] OK — SMTP login successful (user: your.email@gmail.com)

All credentials ready.
```

### Option B: Use in Python Code

In your Python scripts, load GCP secrets before running code:

```python
from gcp_secrets import load_autosota_secrets

# Load from GCP
load_autosota_secrets("YOUR_GCP_PROJECT")

# Now use credentials from os.environ
import os
wandb_key = os.getenv("WANDB_API_KEY")
slack_url = os.getenv("SLACK_WEBHOOK_URL")
```

### Option C: Set GCP_PROJECT_ID Environment Variable

You can avoid typing the project ID each time:

```bash
export GCP_PROJECT_ID=YOUR_GCP_PROJECT

# Now these commands work without --gcp-project
python3 check_keys.py --services wandb,slack,email
python3 test_gcp_integration.py --services wandb,slack,email
```

---

## Troubleshooting

### "google-cloud-secret-manager not installed"

**Solution:**
```bash
pip install google-cloud-secret-manager
```

### "DefaultCredentialsError: Could not automatically determine credentials"

**Possible causes:**
1. You haven't run `gcloud auth application-default login` yet
2. ADC credentials file is missing or corrupted

**Solutions:**
```bash
# Re-authenticate
gcloud auth application-default login

# Check ADC status
gcloud auth application-default print-access-token

# If that fails, clear and re-auth
gcloud auth application-default revoke
gcloud auth application-default login
```

### "Secret not found in GCP"

**Solution:**
Verify the secret was created:
```bash
gcloud secrets list --project=YOUR_GCP_PROJECT
gcloud secrets versions access latest --secret=autosota-wandb-api-key --project=YOUR_GCP_PROJECT
```

If not found, re-create it (see [Step 3](#step-3-create-secrets-in-gcp)).

### "Permission denied" when accessing secrets

**Cause:** Your GCP account doesn't have the right IAM role.

**Solution:**
```bash
# Grant yourself Secret Manager Editor role
gcloud projects add-iam-policy-binding YOUR_GCP_PROJECT \
  --member=user:YOUR_EMAIL@gmail.com \
  --role=roles/secretmanager.admin
```

### Gmail SMTP Login Fails

**Possible causes:**
1. You're using your Gmail password instead of an app-specific password
2. 2-Step Verification is not enabled
3. The app password is wrong

**Solution:**
1. Go to https://myaccount.google.com/apppasswords
2. Generate a new app password
3. Update the secret in GCP:
   ```bash
   echo -n "NEW_APP_PASSWORD" | gcloud secrets versions add autosota-gmail-app-password \
     --data-file=- \
     --project=YOUR_GCP_PROJECT
   ```
4. Re-run the test:
   ```bash
   python3 test_gcp_integration.py --project YOUR_GCP_PROJECT --services email
   ```

### Slack Webhook Returns 404

**Cause:** The webhook URL is invalid or revoked.

**Solution:**
1. Go to https://api.slack.com/apps
2. Find your app and regenerate the Incoming Webhook URL
3. Update the secret:
   ```bash
   echo -n "NEW_WEBHOOK_URL" | gcloud secrets versions add autosota-slack-webhook-url \
     --data-file=- \
     --project=YOUR_GCP_PROJECT
   ```
4. Re-run the test:
   ```bash
   python3 test_gcp_integration.py --project YOUR_GCP_PROJECT --services slack
   ```

### WandB Key Validation Fails

**Cause:** The WandB API key is revoked, expired, or invalid.

**Solution:**
1. Go to https://wandb.ai/settings/keys
2. Generate a new API key
3. Update the secret:
   ```bash
   echo -n "NEW_WANDB_KEY" | gcloud secrets versions add autosota-wandb-api-key \
     --data-file=- \
     --project=YOUR_GCP_PROJECT
   ```
4. Re-run the test:
   ```bash
   python3 test_gcp_integration.py --project YOUR_GCP_PROJECT --services wandb
   ```

---

## Next Steps

- Add `export GCP_PROJECT_ID=YOUR_GCP_PROJECT` to your shell profile to avoid typing it each time
- Use GCP Secret Manager in your CI/CD pipelines (GitHub Actions, Cloud Build, etc.)
- Rotate secrets periodically using `gcloud secrets versions add`
- Set up secret expiration policies in GCP Secret Manager

---

## Reference

- [Google Cloud Secret Manager Docs](https://cloud.google.com/secret-manager/docs)
- [Application Default Credentials](https://cloud.google.com/docs/authentication/provide-credentials-adc)
- [WandB API Keys](https://docs.wandb.ai/guides/tracking/environment-variables)
- [Slack Incoming Webhooks](https://api.slack.com/messaging/webhooks)
- [Gmail App Passwords](https://support.google.com/accounts/answer/185833)
