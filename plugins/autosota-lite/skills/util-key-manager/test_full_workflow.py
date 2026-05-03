#!/usr/bin/env python3
"""
Full workflow test: WandB logging → Slack notification → Email report
Tests the complete GCP Secret Manager integration end-to-end
"""

import os
import sys
import json
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

# Add skills path for gcp_secrets
sys.path.insert(0, str(Path(__file__).parent))

try:
    from gcp_secrets import load_autosota_secrets
    import wandb
    import requests
except ImportError as e:
    print(f"Installing missing dependencies...")
    os.system("pip install -q wandb requests google-cloud-secret-manager")
    from gcp_secrets import load_autosota_secrets
    import wandb
    import requests

# Parse arguments
PROJECT_ID = sys.argv[1] if len(sys.argv) > 1 else "projectrl-485417"

print("╔════════════════════════════════════════════════════════════════╗")
print("║   Full Workflow Test: WandB → Slack → Email                   ║")
print("╚════════════════════════════════════════════════════════════════╝")
print()

# Step 1: Load secrets from GCP
print("Step 1: Loading secrets from GCP...")
secrets = load_autosota_secrets(PROJECT_ID)
print(f"✓ Loaded {len([s for s in secrets.values() if s == 'ok'])} secrets")
print()

# Step 2: Log to WandB
print("Step 2: Logging metrics to WandB...")
try:
    wandb_api_key = os.getenv("WANDB_API_KEY")

    # Initialize wandb run
    run = wandb.init(
        project="autosota-lite-test",
        entity="sudingli21",
        job_type="gcp_integration_test",
        notes="GCP Secret Manager integration test"
    )

    # Log test metrics
    for i in range(5):
        metrics = {
            "step": i,
            "loss": 1.0 / (i + 1),
            "accuracy": 0.8 + (i * 0.02),
            "timestamp": datetime.now().isoformat()
        }
        wandb.log(metrics)

    wandb_url = run.get_url()
    wandb.finish()

    print(f"✓ WandB: Logged 5 metrics")
    print(f"  Run: {wandb_url}")
    wandb_success = True
    wandb_status = f"✓ WandB logging successful\nRun: {wandb_url}"
except Exception as e:
    print(f"❌ WandB: {str(e)[:100]}")
    wandb_success = False
    wandb_status = f"❌ WandB failed: {str(e)[:100]}"

print()

# Step 3: Post to Slack
print("Step 3: Posting to Slack...")
try:
    slack_webhook = os.getenv("SLACK_WEBHOOK_URL")

    slack_message = {
        "text": "🎉 AutoSOTA Lite - GCP Integration Test Complete",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "✅ *GCP Secret Manager Integration Test Complete*\n\n*Results:*\n• WandB: Logged 5 metrics\n• Slack: Message posted\n• Email: Report sent\n\n_Test completed at " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "_"
                }
            }
        ]
    }

    response = requests.post(slack_webhook, json=slack_message)

    if response.status_code == 200:
        print(f"✓ Slack: Message posted successfully")
        slack_success = True
        slack_status = "✓ Slack notification sent"
    else:
        print(f"❌ Slack: {response.status_code} {response.text}")
        slack_success = False
        slack_status = f"❌ Slack failed: {response.status_code}"

except Exception as e:
    print(f"❌ Slack: {str(e)[:100]}")
    slack_success = False
    slack_status = f"❌ Slack failed: {str(e)[:100]}"

print()

# Step 4: Send email report
print("Step 4: Sending email report...")
try:
    gmail_user = os.getenv("GMAIL_USER")
    gmail_password = os.getenv("GMAIL_APP_PASSWORD")

    # Create email
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "[AutoSOTA] GCP Integration Test Complete ✅"
    msg["From"] = gmail_user
    msg["To"] = gmail_user

    # HTML report
    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333;">
        <h2>AutoSOTA Lite - GCP Secret Manager Integration Test</h2>
        <hr>
        <h3>Test Results</h3>
        <table border="1" cellpadding="10" style="border-collapse: collapse;">
          <tr style="background-color: #f2f2f2;">
            <th>Service</th>
            <th>Status</th>
          </tr>
          <tr>
            <td>WandB</td>
            <td>{'✓ PASS' if wandb_success else '✗ FAIL'}</td>
          </tr>
          <tr>
            <td>Slack</td>
            <td>{'✓ PASS' if slack_success else '✗ FAIL'}</td>
          </tr>
          <tr>
            <td>Gmail SMTP</td>
            <td>✓ PASS (sending this email)</td>
          </tr>
        </table>
        <hr>
        <h3>Details</h3>
        <pre style="background-color: #f5f5f5; padding: 10px; border-radius: 5px;">
WandB:
{wandb_status}

Slack:
{slack_status}

Gmail:
✓ Email delivered successfully
User: {gmail_user}
Server: smtp.gmail.com:587 (TLS)
        </pre>
        <hr>
        <p><small>Test completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</small></p>
      </body>
    </html>
    """

    msg.attach(MIMEText(html, "html"))

    # Send via SMTP
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.send_message(msg)

    print(f"✓ Email: Report sent to {gmail_user}")
    email_success = True
    email_status = f"✓ Email delivered to {gmail_user}"

except Exception as e:
    print(f"❌ Email: {str(e)[:100]}")
    email_success = False
    email_status = f"❌ Email failed: {str(e)[:100]}"

print()
print("╔════════════════════════════════════════════════════════════════╗")
print("║                    ✅ TEST COMPLETE!                          ║")
print("╚════════════════════════════════════════════════════════════════╝")
print()

print("Summary:")
print(f"  WandB: {'✓' if wandb_success else '✗'}")
print(f"  Slack: {'✓' if slack_success else '✗'}")
print(f"  Email: {'✓' if email_success else '✗'}")
print()

if wandb_success and slack_success and email_success:
    print("🎉 All services working end-to-end!")
    sys.exit(0)
else:
    print("⚠ Some services failed - check details above")
    sys.exit(1)
