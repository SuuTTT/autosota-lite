# SKILL: autosota-result-logger

## Purpose
Unified logging of experiment results to external platforms like Weights & Biases (WandB) and GitHub, ensuring automatic credential management and consistent reporting.

## Features
- **WandB Integration**: Sync local logs/metrics to WandB dashboards.
- **GitHub Updates**: Auto-commit `scores.jsonl` or update gist-based dashboards.
- **Credential Handling**: Automatically retrieve API keys from environment variables or secure local stores without manual intervention.

## Modes

### 1. Configure
Set up logging targets and verify connectivity/permissions.

### 2. Live Sync
Stream metrics from running jobs to WandB.

### 3. Summary Report
Upload final artifacts, plots, and summary metrics to a GitHub repository or release.

## Data Schema
Ensures all logs include:
- `timestamp`
- `commit_hash`
- `config_params`
- `metrics` (loss, accuracy, etc.)
