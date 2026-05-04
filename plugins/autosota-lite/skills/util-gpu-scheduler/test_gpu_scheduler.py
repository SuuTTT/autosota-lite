#!/usr/bin/env python3
"""
Simple test script for GPU scheduler skill
Trains a tiny model, logs to WandB, and notifies Slack on completion
"""

import sys
import json
import time
import subprocess
import os
from datetime import datetime

def run_training():
    """Simple training loop that logs to WandB"""
    try:
        import wandb
        import torch
        import torch.nn as nn
        import torch.optim as optim
    except ImportError as e:
        print(f"Error: {e}")
        print("Installing dependencies...")
        os.system("pip install -q torch wandb")
        import wandb
        import torch
        import torch.nn as nn
        import torch.optim as optim

    # Initialize WandB
    run = wandb.init(
        project="autosota-gpu-scheduler-test",
        name=f"test-run-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        config={
            "model": "tiny-mlp",
            "epochs": 5,
            "batch_size": 32,
            "learning_rate": 0.001,
        }
    )

    print("\n" + "="*60)
    print("GPU Scheduler Test: WandB + Slack Notification")
    print("="*60)
    print(f"\n✅ WandB initialized: {run.get_url()}")

    # Create a tiny model
    model = nn.Sequential(
        nn.Linear(10, 32),
        nn.ReLU(),
        nn.Linear(32, 32),
        nn.ReLU(),
        nn.Linear(32, 1)
    )

    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.MSELoss()

    # Dummy training loop
    print("\n" + "="*60)
    print("Training...")
    print("="*60)

    for epoch in range(5):
        # Dummy batch
        x = torch.randn(32, 10)
        y = torch.randn(32, 1)

        optimizer.zero_grad()
        output = model(x)
        loss = criterion(output, y)
        loss.backward()
        optimizer.step()

        # Log to WandB
        wandb.log({
            "epoch": epoch,
            "loss": float(loss.item()),
            "accuracy": 0.85 + (epoch * 0.03),
        })

        print(f"Epoch {epoch+1}/5: loss={loss.item():.4f}")
        time.sleep(1)

    print("\n✅ Training complete!")

    # Finish WandB run
    run.finish()
    print(f"✅ WandB run saved: {run.get_url()}")

    return {
        "status": "success",
        "final_loss": float(loss.item()),
        "epochs": 5,
        "wandb_url": run.get_url(),
    }


def notify_slack(metrics):
    """Send completion notification to Slack"""
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        print("⚠️ SLACK_WEBHOOK_URL not set, skipping notification")
        return

    try:
        import requests
    except ImportError:
        os.system("pip install -q requests")
        import requests

    # Format message
    message = {
        "text": "✅ GPU Scheduler Test Complete!",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        f"*GPU Scheduler Test Results*\n\n"
                        f"Status: ✅ {metrics['status']}\n"
                        f"Epochs: {metrics['epochs']}\n"
                        f"Final Loss: {metrics['final_loss']:.6f}\n"
                        f"WandB: <{metrics['wandb_url']}|View Run>\n"
                        f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}"
                    )
                }
            }
        ]
    }

    response = requests.post(webhook_url, json=message)
    if response.status_code == 200:
        print("✅ Slack notification sent!")
    else:
        print(f"⚠️ Slack notification failed: {response.status_code}")


def main():
    print("\n" + "="*60)
    print("GPU SCHEDULER TEST SCRIPT")
    print("="*60)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"Environment: {sys.platform}")

    # Check credentials
    wandb_key = os.getenv("WANDB_API_KEY")
    slack_url = os.getenv("SLACK_WEBHOOK_URL")

    if not wandb_key:
        print("⚠️ WANDB_API_KEY not set")
    else:
        print("✅ WANDB_API_KEY found")

    if not slack_url:
        print("⚠️ SLACK_WEBHOOK_URL not set")
    else:
        print("✅ SLACK_WEBHOOK_URL found")

    # Run training
    metrics = run_training()

    # Send notification
    print("\n" + "="*60)
    print("Sending Slack notification...")
    print("="*60)
    notify_slack(metrics)

    # Print final report
    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60)
    print(json.dumps(metrics, indent=2))
    print(f"\nEnd time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")


if __name__ == "__main__":
    main()
