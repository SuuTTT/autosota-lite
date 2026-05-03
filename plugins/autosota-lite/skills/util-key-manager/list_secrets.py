#!/usr/bin/env python3
"""List all secrets in GCP Secret Manager (Python alternative to gcloud)"""

import sys
from google.cloud import secretmanager

PROJECT_ID = sys.argv[1] if len(sys.argv) > 1 else "projectrl-485417"

client = secretmanager.SecretManagerServiceClient()
parent = f"projects/{PROJECT_ID}"

print(f"Secrets in project {PROJECT_ID}:")
print("─" * 70)

secrets = client.list_secrets(request={"parent": parent})
count = 0

for secret in secrets:
    count += 1
    secret_name = secret.name.split("/")[-1]
    print(f"  ✓ {secret_name}")

print("─" * 70)
print(f"Total: {count} secrets")
