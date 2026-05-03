# Deploy Mode: Store Credentials

One-time setup to store your API credentials.

## Option A: Local Only (Quick)

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

**Note:** `.env.local` is gitignored. Keep it locally only.

---

## Option B: GCP Secret Manager (Recommended for production)

### Step 1: Enable API
Go to: https://console.cloud.google.com/apis/library/secretmanager.googleapis.com?project=projectrl-485417
- Click **ENABLE**
- Wait 30 seconds

### Step 2: Store Credentials
```bash
cd plugins/autosota-lite/skills/autosota-common-key-manager

# Create .env.local first (for temporary storage)
# Then run:
python3 enable_and_setup_secrets.py
```

This will:
- Move credentials from `.env.local` to GCP
- Install `google-cloud-secret-manager`
- Verify all three services work

### Step 3: Verify
```bash
export GCP_PROJECT_ID=projectrl-485417
python3 check_keys.py --gcp-project projectrl-485417 --services wandb,slack,email
```

Should print: `All credentials ready.`

---

## Getting Your Credentials

**WandB API Key:**
- https://wandb.ai/settings/keys
- Copy key starting with `wandb_`

**Slack Webhook URL:**
- https://api.slack.com/apps
- Select your app → Incoming Webhooks
- Copy the full URL

**Gmail:**
- Email: your.email@gmail.com
- App password: https://myaccount.google.com/apppasswords
  - Requires 2FA enabled
  - Select "Mail" + "Windows Computer"
  - Copy the 16-character code (spaces included)

---

## Troubleshooting

**"Secret Manager API not enabled"**
- Visit console link above and click ENABLE

**"credentials not found"**
- Make sure `.env.local` exists and is readable
- Verify with: `cat .env.local`

**"SMTP login failed"**
- Use Gmail **app password**, not your account password
- Get fresh one from: https://myaccount.google.com/apppasswords
