#!/usr/bin/env python3
"""
Enable Secret Manager API and create secrets from .env.local
Uses ADC credentials directly - no gcloud CLI
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load credentials from .env.local
env_file = Path(__file__).parent / ".env.local"
load_dotenv(env_file)

PROJECT_ID = "projectrl-485417"

print("╔════════════════════════════════════════════════════════════════╗")
print("║  GCP Secret Manager Setup - Enable API + Create Secrets       ║")
print("╚════════════════════════════════════════════════════════════════╝")
print()

# Step 1: Install dependencies
print("Step 1: Installing dependencies...")
try:
    from google.cloud import secretmanager
    from google.api_core import exceptions
    print("✓ Dependencies already installed")
except ImportError:
    print("Installing google-cloud-secret-manager...")
    os.system("pip install -q google-cloud-secret-manager python-dotenv")
    from google.cloud import secretmanager
    from google.api_core import exceptions
    print("✓ Dependencies installed")
print()

# Step 2: Enable Secret Manager API
print("Step 2: Enabling Secret Manager API...")
try:
    from googleapiclient import discovery
    from google.auth import default

    credentials, _ = default()
    service = discovery.build('servicemanagement', 'v1', credentials=credentials)

    request = service.services().enable(
        serviceName='secretmanager.googleapis.com',
        body={}
    )
    response = request.execute()
    print(f"✓ Secret Manager API enabled")
except Exception as e:
    # Try alternate method
    try:
        import subprocess
        result = subprocess.run(
            ['gcloud', 'services', 'enable', 'secretmanager.googleapis.com', f'--project={PROJECT_ID}'],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print("✓ Secret Manager API enabled")
        else:
            print(f"⚠ Note: Could not verify API enable via gcloud, but will attempt secret creation")
    except:
        print(f"⚠ Note: Could not enable API via gcloud, but will attempt secret creation")
        print(f"   (You may need to enable manually: https://console.cloud.google.com/apis/library/secretmanager.googleapis.com)")

print()

# Step 3: Create secrets from .env.local
print("Step 3: Creating secrets in GCP Secret Manager...")
print()

credentials_map = {
    "WANDB_API_KEY": "autosota-wandb-api-key",
    "SLACK_WEBHOOK_URL": "autosota-slack-webhook-url",
    "GMAIL_USER": "autosota-gmail-user",
    "GMAIL_APP_PASSWORD": "autosota-gmail-app-password",
}

client = secretmanager.SecretManagerServiceClient()
parent = f"projects/{PROJECT_ID}"

for env_var, secret_name in credentials_map.items():
    secret_value = os.getenv(env_var)

    if not secret_value:
        print(f"⚠ Skipped {secret_name}: {env_var} not found in .env.local")
        continue

    try:
        # Try to create new secret
        response = client.create_secret(
            request={
                "parent": parent,
                "secret_id": secret_name,
                "secret": {
                    "replication": {
                        "automatic": {}
                    }
                }
            }
        )
        print(f"✓ Created new secret: {secret_name}")
    except exceptions.AlreadyExists:
        print(f"✓ Secret {secret_name} already exists (will update)")
    except Exception as e:
        error_msg = str(e)
        if "Secret Manager API has not been used" in error_msg:
            print(f"❌ ERROR: Secret Manager API not enabled")
            print(f"   Enable it manually: https://console.cloud.google.com/apis/library/secretmanager.googleapis.com")
            sys.exit(1)
        elif "permission denied" in error_msg.lower():
            print(f"❌ ERROR: Permission denied accessing {secret_name}")
            print(f"   Make sure your GCP account has 'Secret Manager Admin' role")
            sys.exit(1)
        else:
            print(f"❌ Error creating {secret_name}: {error_msg[:100]}")
            sys.exit(1)

    # Add secret version
    try:
        response = client.add_secret_version(
            request={
                "parent": f"{parent}/secrets/{secret_name}",
                "payload": {"data": secret_value.encode("utf-8")}
            }
        )
        redacted = secret_value[:6] + "..." if len(secret_value) > 6 else secret_value
        print(f"✓ Added secret version: {secret_name} = {redacted}")
    except Exception as e:
        print(f"❌ Error adding secret version for {secret_name}: {str(e)[:100]}")
        sys.exit(1)

print()
print("╔════════════════════════════════════════════════════════════════╗")
print("║                   ✓ SECRETS CREATED!                          ║")
print("╚════════════════════════════════════════════════════════════════╝")
print()

# Step 4: Verify
print("Step 4: Verifying secrets...")
print()

try:
    from check_keys import check_wandb, check_slack, check_email

    print("Testing WandB...")
    if check_wandb():
        print("✓ WandB credentials valid")
    else:
        print("❌ WandB credentials invalid")

    print()
    print("Testing Slack...")
    if check_slack():
        print("✓ Slack webhook valid")
    else:
        print("❌ Slack webhook invalid")

    print()
    print("Testing Gmail SMTP...")
    if check_email():
        print("✓ Gmail credentials valid")
    else:
        print("❌ Gmail credentials invalid")

except ImportError as e:
    print(f"⚠ Could not import check_keys: {e}")
    print("  Skipping verification tests")

print()
print("✅ All done! Run check_keys.py to verify:")
print()
print("  export PATH=\"/root/google-cloud-sdk/bin:$PATH\"")
print("  export GCP_PROJECT_ID=projectrl-485417")
print("  cd /workspace/autosota-lite/plugins/autosota-lite/skills/autosota-common-key-manager")
print("  python3 check_keys.py --gcp-project projectrl-485417 --services wandb,slack,email")
print()
