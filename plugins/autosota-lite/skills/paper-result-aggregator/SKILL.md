---
name: autosota-result-logger
description: Standardize AutoSOTA experiment logs, sync metrics and artifacts to Weights & Biases or GitHub, validate score schemas, and keep credential handling separate from logs and chat transcripts.
---

# AutoSOTA Result Logger

## Purpose
Unified logging of experiment results to external platforms like Weights & Biases (WandB) and GitHub, ensuring automatic credential management and consistent reporting.

## Implementation Details
The core logic resides in `scripts/result_logger.py`, which handles data extraction from `scores.jsonl` and secure transmission to external APIs.

## Features
- **WandB Integration**: Sync local logs/metrics to WandB dashboards.
- **GitHub Updates**: Auto-commit `scores.jsonl` or update gist-based dashboards.
- **Credential Handling**: Automatically retrieve API keys from environment variables or secure local stores without manual intervention.

## Credential Chain
The logger searches for credentials in this order (first match wins, never prints values):

1. Process env: `WANDB_API_KEY`, `GITHUB_TOKEN`.
2. Repo-local `.env.local` (auto-loaded at logger init; gitignored — see `autosota-common-key-manager`).
3. `~/.netrc` for WandB; `~/.github_token` for GitHub.

Run `python3 plugins/autosota-lite/skills/autosota-common-key-manager/check_keys.py` before any sync to verify keys actually validate against the upstream API.

## Remote (Vast.ai) Logging
When the training job runs **inside a Vast.ai container**, the logger needs `WANDB_API_KEY` to be injected into that container — your local env vars are not visible there. Use the vastai scheduler's `--pass-env` flag:

```bash
python3 vastai_scheduler.py launch \
  --pass-env WANDB_API_KEY \
  --job-cmd 'pip install -q wandb && python3 train.py && python3 result_logger.py --mode wandb --project autosota-research' \
  ...
```

`--pass-env` reads `WANDB_API_KEY` from your local shell and forwards it via Docker-style `-e KEY=VALUE`. Never embed the key in `--job-cmd` itself.

## Modes

### 1. Configure
Set up logging targets and verify connectivity/permissions.
- Checks for `WANDB_API_KEY` and `GITHUB_TOKEN`.
- Verifies `scores.jsonl` exists and is readable.

### 2. Live Sync
Stream metrics from running jobs to WandB.
- Command: `python scripts/result_logger.py --mode wandb --project <PROJECT_NAME>`

### 3. Summary Report
Upload final artifacts, plots, and summary metrics to a GitHub repository or release.
- Command: `python scripts/result_logger.py --mode github --gist_id <GIST_ID>`

## Data Schema
Ensures all logs include:
- `timestamp`
- `commit_hash`
- `config_params`
- `metrics` (loss, accuracy, etc.)
