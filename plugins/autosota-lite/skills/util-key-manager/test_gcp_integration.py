#!/usr/bin/env python3
"""End-to-end integration test for GCP Secret Manager with WandB, Slack, and Gmail.

Usage:
    python test_gcp_integration.py --project YOUR_GCP_PROJECT_ID [--services wandb,slack,email]

Sets up a Gmail app password at: https://myaccount.google.com/apppasswords
"""
from __future__ import annotations

import argparse
import json as _json
import os
import smtplib
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from email.mime.text import MIMEText


def _redact(value: str | None, show_chars: int = 6) -> str:
    if not value:
        return "(empty)"
    visible = value[:show_chars]
    return f"{visible}{'*' * max(0, len(value) - show_chars)}"


def test_wandb(wandb_key: str | None) -> bool:
    """Test WandB API credentials via GraphQL."""
    if not wandb_key:
        print("[WandB] SKIP — WANDB_API_KEY not set")
        return False

    print("[WandB] Testing GraphQL authentication...")
    try:
        req = urllib.request.Request(
            "https://api.wandb.ai/graphql",
            data=b'{"query":"{ viewer { username entity } }"}',
            headers={
                "Authorization": f"Bearer {wandb_key}",
                "Content-Type": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = _json.loads(resp.read().decode())

        viewer = (data.get("data") or {}).get("viewer") or {}
        username = viewer.get("username")
        entity = viewer.get("entity")

        if not username:
            print(f"[WandB] FAILED — API returned no user; key is invalid")
            return False

        print(f"[WandB] ✓ SUCCESS")
        print(f"         Username: {username}")
        print(f"         Entity: {entity}")
        print(f"         Key: {_redact(wandb_key)}")
        return True

    except urllib.error.HTTPError as exc:
        print(f"[WandB] FAILED — HTTP {exc.code}")
        print(f"         Likely: revoked, invalid, or expired key")
        return False
    except Exception as exc:
        print(f"[WandB] FAILED — {type(exc).__name__}: {exc}")
        return False


def test_slack(webhook_url: str | None) -> bool:
    """Test Slack Incoming Webhook with a real message POST."""
    if not webhook_url:
        print("[Slack] SKIP — SLACK_WEBHOOK_URL not set")
        return False

    if not webhook_url.startswith("https://hooks.slack.com/services/"):
        print(f"[Slack] SKIP — webhook URL format looks wrong: {_redact(webhook_url, show_chars=40)}")
        return False

    print("[Slack] Posting test message...")
    timestamp = datetime.now().isoformat()
    payload = {
        "text": f"[autosota-lite] GCP Secrets integration test\nTimestamp: {timestamp}",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "AutoSOTA Lite - GCP Secret Manager Test",
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"✓ Test message sent successfully\nTime: {timestamp}",
                },
            },
        ],
    }

    try:
        data = _json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            webhook_url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            response_text = resp.read().decode()
            status = resp.status

        print(f"[Slack] ✓ SUCCESS")
        print(f"         HTTP Status: {status}")
        print(f"         Response: {response_text}")
        return True

    except urllib.error.HTTPError as exc:
        print(f"[Slack] FAILED — HTTP {exc.code}")
        print(f"         Response: {exc.read().decode()}")
        return False
    except Exception as exc:
        print(f"[Slack] FAILED — {type(exc).__name__}: {exc}")
        return False


def test_gmail(gmail_user: str | None, gmail_pass: str | None) -> bool:
    """Test Gmail SMTP credentials and send a test email."""
    if not gmail_user or not gmail_pass:
        print("[Gmail] SKIP — GMAIL_USER or GMAIL_APP_PASSWORD not set")
        return False

    print("[Gmail] Testing SMTP connection and sending test email...")

    try:
        # Create email message.
        msg = MIMEText("GCP Secret Manager integration test successful.")
        msg["Subject"] = "[autosota-lite] GCP credential test"
        msg["From"] = gmail_user
        msg["To"] = gmail_user

        # Connect and send.
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=10) as server:
            server.starttls()
            server.login(gmail_user, gmail_pass)
            result = server.sendmail(gmail_user, [gmail_user], msg.as_string())

        if result:
            print(f"[Gmail] WARNING — Some recipients rejected: {result}")
            return False

        print(f"[Gmail] ✓ SUCCESS")
        print(f"         User: {gmail_user}")
        print(f"         SMTP: smtp.gmail.com:587 (TLS)")
        print(f"         Sent test email to: {gmail_user}")
        return True

    except smtplib.SMTPAuthenticationError:
        print(f"[Gmail] FAILED — Authentication error")
        print(f"         Check app password at: https://myaccount.google.com/apppasswords")
        return False
    except smtplib.SMTPException as exc:
        print(f"[Gmail] FAILED — SMTP error: {exc}")
        return False
    except Exception as exc:
        print(f"[Gmail] FAILED — {type(exc).__name__}: {exc}")
        return False


def load_gcp_secrets(project_id: str) -> dict[str, str]:
    """Load secrets from GCP Secret Manager."""
    try:
        from gcp_secrets import load_autosota_secrets

        print(f"[GCP] Loading from project: {project_id}")
        results = load_autosota_secrets(project_id)

        for env_var, status in results.items():
            if status == "ok":
                print(f"[GCP] {env_var}: loaded ✓")
            elif status == "missing":
                print(f"[GCP] {env_var}: not found in Secret Manager")
            else:
                print(f"[GCP] {env_var}: {status}")

        return results
    except ImportError as e:
        print(f"[GCP] ERROR: {e}")
        print("[GCP] Install with: pip install google-cloud-secret-manager")
        sys.exit(1)
    except Exception as e:
        print(f"[GCP] ERROR: {e}")
        sys.exit(1)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project",
        required=True,
        help="GCP project ID",
    )
    parser.add_argument(
        "--services",
        default="wandb,slack,email",
        help="Comma-separated services to test (default: wandb,slack,email)",
    )
    args = parser.parse_args(argv)

    print("=" * 70)
    print("AutoSOTA Lite - GCP Secret Manager Integration Test")
    print("=" * 70)
    print()

    # Load secrets from GCP.
    load_gcp_secrets(args.project)
    print()

    # Run tests.
    test_functions = {
        "wandb": test_wandb,
        "slack": test_slack,
        "email": test_gmail,
    }

    requested = [s.strip().lower() for s in args.services.split(",") if s.strip()]
    results: dict[str, bool] = {}

    for svc in requested:
        fn = test_functions.get(svc)
        if fn is None:
            print(f"[{svc}] unknown service — skipped")
            continue

        print()
        try:
            if svc == "wandb":
                results[svc] = fn(os.getenv("WANDB_API_KEY"))
            elif svc == "slack":
                results[svc] = fn(os.getenv("SLACK_WEBHOOK_URL"))
            elif svc == "email":
                results[svc] = fn(os.getenv("GMAIL_USER"), os.getenv("GMAIL_APP_PASSWORD"))
            else:
                results[svc] = False
        except Exception as exc:
            print(f"[{svc}] ERROR — {exc}")
            results[svc] = False

    # Summary.
    print()
    print("=" * 70)
    passed = [s for s, ok in results.items() if ok]
    failed = [s for s, ok in results.items() if not ok]

    if failed:
        print(f"FAILED ({len(failed)}):", ", ".join(failed))
        return 1
    else:
        print(f"ALL TESTS PASSED ({len(passed)})")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
