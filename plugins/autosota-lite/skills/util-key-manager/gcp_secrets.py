#!/usr/bin/env python3
"""Load secrets from Google Cloud Secret Manager into os.environ.

Requires: pip install google-cloud-secret-manager
Auth: Application Default Credentials (gcloud auth application-default login)
"""
from __future__ import annotations

import os
import sys
from typing import Any

# Canonical autosota-lite secret names and their environment variable mappings.
AUTOSOTA_SECRETS = {
    "autosota-wandb-api-key": "WANDB_API_KEY",
    "autosota-slack-webhook-url": "SLACK_WEBHOOK_URL",
    "autosota-gmail-user": "GMAIL_USER",
    "autosota-gmail-app-password": "GMAIL_APP_PASSWORD",
}


def load_secrets(
    project_id: str,
    secret_map: dict[str, str],
    overwrite: bool = False,
) -> dict[str, str]:
    """Load secrets from GCP Secret Manager into os.environ.

    Args:
        project_id: GCP project ID.
        secret_map: Mapping of {secret_name → env_var_name}.
                    Secret names are looked up in Secret Manager as-is.
        overwrite: If True, overwrite existing env vars. Default False.

    Returns:
        Status dict: {env_var_name → "ok" | "missing" | "error"}.

    Raises:
        ImportError: If google-cloud-secret-manager is not installed.
        google.auth.exceptions.DefaultCredentialsError: If ADC is not configured.
    """
    try:
        from google.cloud import secretmanager
    except ImportError as e:
        raise ImportError(
            "google-cloud-secret-manager not installed. "
            "Install with: pip install google-cloud-secret-manager"
        ) from e

    client = secretmanager.SecretManagerServiceClient()
    results = {}

    for secret_name, env_var in secret_map.items():
        # Skip if already set in environment and not overwriting.
        if env_var in os.environ and not overwrite:
            results[env_var] = "ok (env)"
            continue

        try:
            # Fetch the secret.
            parent = f"projects/{project_id}"
            secret_resource = f"{parent}/secrets/{secret_name}/versions/latest"
            response = client.access_secret_version(request={"name": secret_resource})
            secret_value = response.payload.data.decode("utf-8")

            # Load into environment.
            os.environ[env_var] = secret_value
            results[env_var] = "ok"

        except Exception as exc:
            # Distinguish between "not found" and other errors.
            if "NOT_FOUND" in str(exc):
                results[env_var] = "missing"
            else:
                results[env_var] = f"error ({type(exc).__name__})"

    return results


def load_autosota_secrets(project_id: str, overwrite: bool = False) -> dict[str, str]:
    """Load canonical autosota-lite secrets from GCP Secret Manager.

    Args:
        project_id: GCP project ID.
        overwrite: If True, overwrite existing env vars. Default False.

    Returns:
        Status dict: {env_var_name → "ok" | "missing" | "error"}.
    """
    return load_secrets(project_id, AUTOSOTA_SECRETS, overwrite=overwrite)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project",
        required=True,
        help="GCP project ID.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing environment variables.",
    )
    args = parser.parse_args()

    try:
        results = load_autosota_secrets(args.project, overwrite=args.overwrite)
        print("[GCP Secrets Manager]")
        for env_var, status in results.items():
            print(f"  {env_var}: {status}")
        sys.exit(0)
    except Exception as e:
        print(f"[GCP Secrets Manager] ERROR: {e}", file=sys.stderr)
        sys.exit(1)
