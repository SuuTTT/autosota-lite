# GCP Secret Manager Integration Architecture

## Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    AutoSOTA Lite Application                     │
│                                                                   │
│  Your Python Code / Scripts                                     │
│  ├─ check_keys.py --gcp-project PROJECT --services wandb,...   │
│  ├─ test_gcp_integration.py --project PROJECT                  │
│  └─ Custom scripts: from gcp_secrets import load_autosota_... │
└────────────────────────────┬────────────────────────────────────┘
                             │
                ┌────────────▼───────────────┐
                │   Load Priority Chain      │
                ├────────────────────────────┤
                │ 1. Shell env vars          │ ◄── Highest priority
                │    (export VAR=...)        │
                │                            │
                │ 2. GCP Secret Manager      │
                │    (if --gcp-project set)  │
                │                            │
                │ 3. .env.local              │ ◄── Local fallback
                │    (dev without GCP)       │
                └────────────┬───────────────┘
                             │
        ┌────────────────────┴────────────────────┐
        │                                         │
        ▼                                         ▼
   ┌──────────────────┐              ┌──────────────────────┐
   │   Local Dev      │              │   GCP Secret Manager │
   ├──────────────────┤              ├──────────────────────┤
   │ .env.local       │              │ autosota-*-*         │
   │ (gitignored)     │              │ (encrypted at rest)  │
   │                  │              │                      │
   │ WANDB_API_KEY    │              │ ADC auth             │
   │ SLACK_...        │              │ (no key files)       │
   │ GMAIL_...        │              │                      │
   └──────────────────┘              │ Access audit log     │
                                     └──────────────────────┘
```

---

## Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   autosota-common-key-manager              │
│                                                              │
│  SKILL.md ◄────────────────────────────────────────────────┐│
│  └─ Documentation & setup guide                             ││
│                                                              ││
│  gcp_secrets.py (NEW) ◄──────────────────────────────────┐ ││
│  ├─ load_secrets(project_id, secret_map)                 │ ││
│  ├─ load_autosota_secrets(project_id)                    │ ││
│  └─ Canonical autosota secret names                      │ ││
│                                                            │ ││
│  check_keys.py (ENHANCED) ◄──────────────────────────────┤ ││
│  ├─ check_wandb()      (existing)                        │ ││
│  ├─ check_slack()      (existing)                        │ ││
│  ├─ check_email()      (NEW)                             │ ││
│  ├─ check_vastai()     (existing)                        │ ││
│  ├─ check_github()     (existing)                        │ ││
│  └─ --gcp-project flag (NEW)                             │ ││
│                                                            │ ││
│  test_gcp_integration.py (NEW) ◄────────────────────────┤ ││
│  ├─ test_wandb()       GraphQL validation                │ ││
│  ├─ test_slack()       Webhook test message              │ ││
│  └─ test_gmail()       SMTP login + send email           │ ││
│                                                            │ ││
│  setup_gcp_secrets.sh (NEW)                               ││
│  └─ Interactive setup automation                         ││
└────────────────────────────────────────────────────────────┘
```

---

## Load Sequence

```
┌────────────────────────────────────────────────────┐
│ User calls check_keys.py --gcp-project PROJECT    │
└───────────────────┬────────────────────────────────┘
                    │
        ┌───────────▼──────────────┐
        │  Parse command-line args │
        │  --services wandb,slack  │
        │  --gcp-project PROJECT   │
        └───────────┬──────────────┘
                    │
        ┌───────────▼──────────────┐
        │  Load .env.local         │
        │  (existing env vars set) │
        └───────────┬──────────────┘
                    │
        ┌───────────▼──────────────────────────┐
        │  IF --gcp-project is set:            │
        │    import gcp_secrets                │
        │    load_autosota_secrets(PROJECT_ID) │
        │    ├─ Initialize SecretManager...    │
        │    ├─ Fetch autosota-wandb-api-key   │
        │    ├─ Fetch autosota-slack-webhook   │
        │    ├─ Fetch autosota-gmail-user      │
        │    └─ Fetch autosota-gmail-password  │
        │    Populate os.environ               │
        └───────────┬──────────────────────────┘
                    │
        ┌───────────▼──────────────────────┐
        │  For each requested service:     │
        │  ├─ Call check_wandb()          │
        │  ├─ Call check_slack()          │
        │  ├─ Call check_email()          │
        │  └─ Call check_github()         │
        │                                  │
        │  Each check():                  │
        │  ├─ Read env var (already set)  │
        │  ├─ Live validate (API call)    │
        │  └─ Print status (redacted)     │
        └───────────┬──────────────────────┘
                    │
        ┌───────────▼──────────────┐
        │  Exit code:              │
        │  0 = all passed          │
        │  1 = some failed         │
        └──────────────────────────┘
```

---

## Secret Name Mapping

```
┌──────────────────────────────────────────────────────────┐
│            GCP Secret Manager                            │
│  ┌────────────────────────────────────────────────────┐  │
│  │ Secret Name                 → Env Variable         │  │
│  ├────────────────────────────────────────────────────┤  │
│  │ autosota-wandb-api-key      → WANDB_API_KEY        │  │
│  │ autosota-slack-webhook-url  → SLACK_WEBHOOK_URL    │  │
│  │ autosota-gmail-user         → GMAIL_USER           │  │
│  │ autosota-gmail-app-password → GMAIL_APP_PASSWORD   │  │
│  └────────────────────────────────────────────────────┘  │
│                         ▲                                │
│                         │                                │
│              ┌──────────┴────────────┐                   │
│              │ load_secrets(         │                   │
│              │   project_id=...,     │                   │
│              │   secret_map={...}    │                   │
│              │ )                     │                   │
│              └──────────┬────────────┘                   │
│                         │                                │
│              ┌──────────┴────────────┐                   │
│              │ SecretManagerClient   │                   │
│              │ .access_secret_       │                   │
│              │ version()             │                   │
│              └──────────┬────────────┘                   │
│                         │                                │
│              ┌──────────┴────────────┐                   │
│              │ Application Default   │                   │
│              │ Credentials (ADC)     │                   │
│              │                       │                   │
│              │ gcloud auth           │                   │
│              │ application-default   │                   │
│              │ login                 │                   │
│              └───────────────────────┘                   │
└──────────────────────────────────────────────────────────┘
```

---

## IAM Permissions Required

```
┌──────────────────────────────────────────────────────────┐
│            Google Cloud IAM Roles                        │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  For local development (gcloud auth application-...):   │
│  ├─ roles/secretmanager.admin                           │
│  │  └─ Needed to create/update/view secrets             │
│  └─ roles/serviceusage.serviceUsageAdmin               │
│     └─ Needed to enable APIs                           │
│                                                           │
│  For production service account:                        │
│  └─ roles/secretmanager.secretAccessor                 │
│     └─ Read-only access (minimal permissions)          │
│                                                           │
│  Recommended least-privilege:                           │
│  └─ Custom role with only:                            │
│     ├─ secretmanager.versions.access                   │
│     └─ (no create/delete permissions)                  │
└──────────────────────────────────────────────────────────┘
```

---

## Integration Points

### Check Keys

```
check_keys.py
├─ Loads from .env.local (existing)
├─ Loads from GCP (NEW with --gcp-project)
└─ Validates each service:
   ├─ WandB (GraphQL API)
   ├─ Slack (Webhook URL validation)
   ├─ Gmail (SMTP login test)
   ├─ GitHub (gh CLI or token file)
   └─ Vast.ai (API key file)
```

### Custom Scripts

```python
# Your code
from gcp_secrets import load_autosota_secrets
import os

# Load at startup
load_autosota_secrets("my-gcp-project")

# Now use like normal env vars
wandb_key = os.getenv("WANDB_API_KEY")
slack_url = os.getenv("SLACK_WEBHOOK_URL")

# Rest of your code...
```

### Vast.ai Remote Jobs

```bash
# Local: Secrets in env
export WANDB_API_KEY=$(gcloud secrets versions access latest --secret=autosota-wandb-api-key --project=PROJECT)

# Submit job with --pass-env
python3 vastai_scheduler.py launch \
  --pass-env WANDB_API_KEY,GITHUB_TOKEN \
  ...
```

---

## Error Handling Flow

```
┌─────────────────────────────┐
│ Try to load secret from GCP │
└────────┬────────────────────┘
         │
    ┌────▼───────────────────┐
    │ Secret Manager API call│
    └────┬────────────────────┘
         │
    ┌────▼─────────────┬──────────────────┬──────────────────┐
    │                  │                  │                  │
Success           Not Found            Auth Error         Other Error
    │                  │                  │                  │
    ▼                  ▼                  ▼                  ▼
Populate         Return "missing"    Log to stderr     Return "error"
os.environ       Skip to fallback    Try fallback      Try fallback
Return "ok"      (continue)          (continue)        (continue)
    │                  │                  │                  │
    └──────────┬───────┴──────────┬───────┴──────────┬──────┘
               │                  │                  │
         ┌─────▼──────────────────▼──────────────────▼────┐
         │  If no value found in any source:             │
         │  ├─ Check is "optional" → Return True         │
         │  └─ Check is "required" → Return False        │
         └────────────────────────────────────────────────┘
```

---

## Security Boundaries

```
┌────────────────────────────────────────────────────────────┐
│                    Local Machine                          │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ AutoSOTA Lite Application                           │ │
│  │                                                      │ │
│  │ Sensitive Data (In Memory Only):                    │ │
│  │ ├─ WANDB_API_KEY                                    │ │
│  │ ├─ SLACK_WEBHOOK_URL                               │ │
│  │ ├─ GMAIL_APP_PASSWORD                              │ │
│  │ └─ (All redacted in logs/output)                    │ │
│  └──────────────────┬───────────────────────────────────┘ │
│                     │ TLS/mTLS                            │
│                     │                                     │
│  ┌──────────────────▼───────────────────────────────────┐ │
│  │ Application Default Credentials                     │ │
│  │ └─ Stored at ~/.config/gcloud/...                   │ │
│  │    (never transmitted for secrets API)              │ │
│  └──────────────────┬───────────────────────────────────┘ │
└─────────────────────┼────────────────────────────────────┘
                      │
     ┌────────────────▼────────────────┐
     │                                 │
┌────▼─────────────────────────────────▼──┐
│          Google Cloud Network            │
│                                          │
│  HTTPS/TLS Encrypted Tunnel              │
│  ├─ Authentication via ADC               │
│  └─ Encryption with mTLS option          │
└────┬─────────────────────────────────┬───┘
     │                                 │
     ▼                                 ▼
┌─────────────────┐           ┌─────────────────┐
│  Secret Manager │           │ Audit Logging   │
│                 │           │                 │
│  Storage:       │           │  Who accessed   │
│  - Encrypted    │           │  When accessed  │
│  - Replicated   │           │  Which secret   │
│  - Key rotation │           │  Access result  │
└─────────────────┘           └─────────────────┘
```

---

## File Layout

```
autosota-lite/
│
├── GCP_QUICKSTART.md                        ◄─ Start here
├── GCP_SECRET_MANAGER_GUIDE.md             ◄─ Setup guide
├── GCP_INTEGRATION_SUMMARY.md              ◄─ Full docs
├── ARCHITECTURE.md                         ◄─ You are here
└── plugins/autosota-lite/skills/
    └── autosota-common-key-manager/
        │
        ├── SKILL.md                        ◄─ Plugin docs
        │
        ├── gcp_secrets.py                  ◄─ Core module
        │   ├─ load_secrets()
        │   └─ load_autosota_secrets()
        │
        ├── check_keys.py                   ◄─ CLI verification
        │   ├─ check_wandb()
        │   ├─ check_slack()
        │   ├─ check_email()               (NEW)
        │   └─ --gcp-project flag          (NEW)
        │
        └── test_gcp_integration.py         ◄─ Integration tests
            ├─ test_wandb()
            ├─ test_slack()
            └─ test_gmail()
```

---

## Deployment Scenarios

### Local Development

```
Developer Machine
├─ gcloud auth application-default login
├─ .env.local (fallback)
└─ python3 check_keys.py --gcp-project PROJECT

Load Priority: Shell Env → GCP → .env.local
```

### CI/CD Pipeline (GitHub Actions)

```
GitHub Actions
├─ Service Account (OIDC federation)
├─ No key files needed (uses workload identity)
└─ python3 check_keys.py --gcp-project PROJECT

Load Priority: Shell Env → GCP
```

### Remote Job (Vast.ai)

```
Local Machine → Vast.ai Instance
├─ Load secrets locally
├─ Pass via --pass-env
└─ Instance uses env vars directly

Load Priority: Shell Env → .env.local
(GCP not available inside container)
```

---

## Performance Characteristics

```
┌─────────────────────────────────────┐
│         Load Time (First Call)      │
├─────────────────────────────────────┤
│ .env.local              ~ 1-5 ms    │
│ GCP Secret Manager      ~ 100-200ms │
│ Shell env var lookup    < 1 ms      │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│      Load Time (Subsequent Calls)   │
├─────────────────────────────────────┤
│ All (cached in os.environ)  < 1 ms  │
└─────────────────────────────────────┘
```

---

## Future Extensions

```
Potential additions (not yet implemented):
├─ Vault support (HashiCorp)
├─ AWS Secrets Manager
├─ Azure Key Vault
├─ Kubernetes Secrets
├─ Secret rotation automation
└─ Multi-region failover
```

---

**See also:** `GCP_QUICKSTART.md` for a quick start
