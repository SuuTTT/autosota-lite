---
name: autosota-vastai-scheduler
description: Search live Vast.ai offers, estimate task rental cost, avoid specified countries such as China and the United States, prefer low disk and network costs, rent the lowest-cost matching instance only when explicitly requested, run a batch command, and destroy the instance after completion.
---

# AutoSOTA Vast.ai Scheduler

Use this skill when the user wants a live Vast.ai scheduler that can estimate cost, select cheap offers, launch a disposable instance, run a command, and clean up billing by destroying the instance.

## Safety Rules

- Search and estimate are safe by default and do not need an API key.
- Renting or destroying instances is an account action. Do it only when the user explicitly asks.
- Never print or request that the user paste a Vast.ai API key into chat.
- If the user already pasted a key into chat, recommend rotating it in Vast.ai and setting the replacement locally.
- Prefer on-demand instances for non-disposable training. Use interruptible only when the user accepts preemption risk.
- Default country exclusions are `CN,US`; keep them unless the user explicitly changes them.
- Destroying an instance deletes its data. Make sure the job uploads or persists anything important before cleanup.

## API Key Setup

For search-only estimates, no API key is required.

For launch/destroy actions, the user must configure the key locally:

```bash
vastai set api-key YOUR_API_KEY
```

Do not put the account API key in `--job-cmd`, `--env`, logs, or chat. The scheduler redacts `instance_api_key` from its create output.

`CONTAINER_ID` is not an API key. It is the instance/contract ID inside the rented container. Vast.ai also injects `CONTAINER_API_KEY` inside the instance; the remote cleanup script attempts:

```bash
vastai destroy instance "$CONTAINER_ID" --api-key "$CONTAINER_API_KEY"
```

Remote self-destroy can fail on some images or permission setups, so the launcher also monitors logs locally and destroys the contract after it sees `[vastai-scheduler] job exited`.

## Bundled Scheduler

Run the bundled script:

```bash
python3 /workspace/autosota-lite/plugins/autosota-lite/skills/autosota-vastai-scheduler/scripts/vastai_scheduler.py --help
```

Estimate only:

```bash
python3 /workspace/autosota-lite/plugins/autosota-lite/skills/autosota-vastai-scheduler/scripts/vastai_scheduler.py estimate \
  --runtime-hours 4 \
  --disk-gb 80 \
  --download-gb 20 \
  --upload-gb 5 \
  --gpu "RTX 4090,RTX 3090" \
  --min-gpu-ram-gb 20
```

Dry-run launch:

```bash
python3 /workspace/autosota-lite/plugins/autosota-lite/skills/autosota-vastai-scheduler/scripts/vastai_scheduler.py launch \
  --runtime-hours 4 \
  --disk-gb 80 \
  --gpu "RTX 4090,RTX 3090" \
  --min-gpu-ram-gb 20 \
  --job-cmd 'nvidia-smi && python train.py' \
  --ssh
```

Real launch requires `--yes`:

```bash
python3 /workspace/autosota-lite/plugins/autosota-lite/skills/autosota-vastai-scheduler/scripts/vastai_scheduler.py launch \
  --runtime-hours 4 \
  --disk-gb 80 \
  --gpu "RTX 4090,RTX 3090" \
  --min-gpu-ram-gb 20 \
  --job-cmd 'nvidia-smi && python train.py' \
  --ssh \
  --yes
```

The default real launch waits for cleanup. Use `--no-monitor-cleanup` only for fire-and-forget jobs where another process will destroy the instance.

Cheap hello-world validation:

```bash
python3 /workspace/autosota-lite/plugins/autosota-lite/skills/autosota-vastai-scheduler/scripts/vastai_scheduler.py launch \
  --runtime-hours 0.03 \
  --disk-gb 5 \
  --limit 3 \
  --order dph \
  --offer-type on-demand \
  --image ubuntu:22.04 \
  --job-cmd 'echo hello world from autosota-vastai-scheduler' \
  --label autosota-vastai-scheduler-hello \
  --ssh \
  --cleanup-timeout-minutes 10 \
  --cleanup-poll-seconds 10 \
  --yes
```

Interruptible search or launch:

```bash
python3 /workspace/autosota-lite/plugins/autosota-lite/skills/autosota-vastai-scheduler/scripts/vastai_scheduler.py estimate \
  --runtime-hours 0.05 \
  --disk-gb 5 \
  --offer-type bid \
  --limit 5
```

Interruptible launches can create stopped partial contracts when the bid is not immediately scheduled. The script destroys partial contracts if Vast.ai returns `success: false` with `new_contract`.

## Cost Model

The scheduler estimates:

```text
total_usd = runtime_hours * dph_total + upload_gb * inet_up_cost + download_gb * inet_down_cost
```

`dph_total` is Vast.ai's hourly price for the selected offer with the requested disk size included through `--storage`.

## Important Flags

- `--avoid-countries CN,US`: country-code denylist; default avoids China and the United States.
- `--max-storage-cost 0.20`: maximum storage price in USD/GB/month.
- `--max-inet-up-cost 0.02`: maximum upload price in USD/GB.
- `--max-inet-down-cost 0.02`: maximum download price in USD/GB.
- `--extra-query 'duration>2'`: pass extra Vast.ai query filters.
- `--destroy-on-success-only`: keep failed jobs running for debugging. Warn the user that billing continues.
- `--offer-type bid`: search/rent interruptible instances; the scheduler passes a suggested `--bid_price`.
- `--no-monitor-cleanup`: skip local cleanup monitoring after create.
- `--cleanup-timeout-minutes 30`: max time to wait for job exit before returning.

## Cleanup Behavior

For real launches, the script injects an on-start command that:

1. runs the user's job command with `bash -lc`;
2. writes `/workspace/vastai-job/job.log`;
3. writes `/workspace/vastai-job/status.json`;
4. calls `vastai destroy instance "$CONTAINER_ID" --api-key "$CONTAINER_API_KEY"`;
5. locally polls `vastai logs`, detects job exit, and destroys the contract as a fallback.

Vast.ai supplies `CONTAINER_ID` and `CONTAINER_API_KEY` inside the instance, so the user's main API key is not copied into the container.
