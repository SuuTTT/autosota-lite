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
- Default cost limit: avoid instances costing more than **$0.1/hour** (set `--max-dph 0.1`). Override only for specific use cases.
- Destroying an instance deletes its data. Make sure the job uploads or persists anything important before cleanup.

## Cost Control (NEW)

**Default cost filter: `--max-dph 0.1` (avoid >$0.1/hour instances)**

The scheduler now automatically filters out expensive instances. To use costlier hardware:

```bash
python3 vastai_scheduler.py launch \
  --max-dph 0.15 \  # allow up to $0.15/hour
  --runtime-hours 4 \
  --job-cmd 'python train.py' \
  --yes
```

Cost is estimated as:
```
total_cost_usd = runtime_hours * dph_total + upload_gb * inet_up_cost + download_gb * inet_down_cost
```

View estimated costs before launching:
```bash
python3 vastai_scheduler.py estimate \
  --runtime-hours 4 \
  --disk-gb 80 \
  --max-dph 0.1
```

## True Run Estimator (NEW)

For long-running tasks (>4 hours), profile actual performance **before** committing full compute.

**Workflow:**
```
1. Run short test (30 steps/minutes)
   → measure: speed, GPU util, memory, CPU util
   
2. Run medium test (40 steps/minutes)
   → validate: consistency, scaling
   
3. Run long test (50 steps/minutes)
   → estimate: actual time for full run
   
4. Extrapolate to full duration
   → decide: proceed with full run or optimize code
```

**Usage:**

```bash
# Profile before full run
python3 vastai_scheduler.py profile \
  --runtime-hours 4 \  # target runtime
  --job-cmd 'python train.py --steps 10000' \
  --test-steps 30,40,50 \  # short test runs (in minutes)
  --metrics-to-capture speed,gpu_util,memory,cpu_util \
  --max-dph 0.1 \
  --yes
```

**Output example:**

```
═══════════════════════════════════════════════════════════════
True Run Estimator: PPO Training (target: 4 hours)
═══════════════════════════════════════════════════════════════

TEST 1: 30 minutes
  Speed:      1200 steps/min
  GPU Util:   84%
  Memory:     6.2 GB / 16 GB (39%)
  CPU Util:   45%
  Cost:       $0.05

TEST 2: 40 minutes  
  Speed:      1195 steps/min (consistent ✓)
  GPU Util:   83%
  Memory:     6.3 GB / 16 GB (39%)
  CPU Util:   46%
  Cost:       $0.07

TEST 3: 50 minutes
  Speed:      1198 steps/min (avg: 1198)
  GPU Util:   83%
  Memory:     6.2 GB / 16 GB (39%)
  CPU Util:   45%
  Cost:       $0.08

═══════════════════════════════════════════════════════════════
EXTRAPOLATION TO FULL RUN (4 hours = 240 minutes)
═══════════════════════════════════════════════════════════════

Avg Speed:      1198 steps/min
Estimated Time: 240 min / 1 = 240 min ✓ (matches target)
Total Steps:    287,520
Peak Memory:    6.3 GB (safe margin: 9.7 GB available)
Avg GPU Util:   83% (excellent)
Avg CPU Util:   45%

ESTIMATED COST:  $0.24 (4 hours × $0.06/hour)

RECOMMENDATION:
✅ Proceed with full run
   • Speed is consistent (no degradation)
   • Memory is stable (no leaks)
   • GPU utilization excellent
   • Cost reasonable ($0.06/hour)

Next: python3 vastai_scheduler.py launch \
  --full-run true \
  --estimated-cost 0.24 \
  --yes
```

**Metrics captured:**

```yaml
Performance:
  - Steps per minute (throughput)
  - Convergence rate
  - Time per epoch/iteration

Hardware:
  - GPU utilization (%)
  - GPU memory usage (GB)
  - GPU temperature (°C)
  - CPU utilization (%)
  - CPU memory usage (GB)

Network:
  - Data upload speed (MB/s)
  - Data download speed (MB/s)
  - Network packets (if applicable)

Cost:
  - Cumulative cost per test
  - Cost per step / cost per hour
  - Extrapolated full-run cost
```

**Advanced: Custom metrics**

```bash
python3 vastai_scheduler.py profile \
  --runtime-hours 4 \
  --job-cmd 'python train.py --steps 10000' \
  --test-steps 30,40,50 \
  --custom-metrics 'loss,accuracy,validation_loss' \
  --metrics-collection-interval 1.0 \  # collect every 1 sec
  --max-dph 0.1 \
  --yes
```

This captures your application-specific metrics alongside system metrics.

## API Key Setup

For search-only estimates, no API key is required.

For launch/destroy actions, the user must configure the key locally:

```bash
vastai set api-key YOUR_API_KEY
```

If you use `--ssh`, the scheduler will automatically register your local `~/.ssh/id_ed25519.pub` (or `id_rsa.pub`) public key with Vast.ai if no keys are currently registered in your account. This ensures you can connect to the newly created instance from your current terminal.

Do not put the **Vast.ai account API key** in `--job-cmd`, `--env`, logs, or chat. The scheduler redacts `instance_api_key` from its create output.

**Service credentials** (WandB, GitHub, etc.) are different — they must be injected into the container or the job inside cannot authenticate. Use the bundled `--pass-env` flag, which reads the named variables from your local shell and forwards them via the Vast.ai `--env` mechanism (which expects Docker-style `-e KEY=VALUE`):

```bash
export WANDB_API_KEY=...   # or load via .env.local
python3 vastai_scheduler.py launch \
  --pass-env WANDB_API_KEY,GITHUB_TOKEN \
  --job-cmd 'pip install -q wandb && python3 train.py' \
  ...
```

Variables listed in `--pass-env` that are not set locally print a warning and are skipped — they are never injected as empty values.

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

The launch default image is `vastai/pytorch`, Vast.ai's standard PyTorch image family. Treat this as an image family, not a complete runtime contract: probe the selected instance for the Python executable that can import `torch` before running ML code. Override `--image` when the task requires a specific pinned CUDA/PyTorch/Python stack or a non-PyTorch runtime.

## PyTorch Runtime Probe

For ML jobs, probe the runtime inside `--job-cmd` before installing project dependencies. On Vast.ai PyTorch images, the usable Python often lives at `/venv/main/bin/python`; older PyTorch images may use `/opt/conda/bin/python`; bare `python` or system `python3` may be absent or may not import `torch`.

Use this pattern:

```bash
PYTHON_BIN="${PYTHON_BIN:-/venv/main/bin/python}"
if [[ ! -x "$PYTHON_BIN" ]]; then
  if [[ -x /opt/conda/bin/python ]]; then
    PYTHON_BIN=/opt/conda/bin/python
  else
    PYTHON_BIN="$(command -v python3)"
  fi
fi
echo "PYTHON_BIN=$PYTHON_BIN"
"$PYTHON_BIN" - <<'PY'
import sys
import torch
print("python", sys.version.replace("\n", " "))
print("torch", torch.__version__)
print("torch_cuda", torch.version.cuda)
print("cuda_available", torch.cuda.is_available())
print("cuda_device", torch.cuda.get_device_name(0) if torch.cuda.is_available() else None)
print("arch_list", torch.cuda.get_arch_list() if torch.cuda.is_available() else None)
PY
```

## RTX 50-Series / `sm_120` Fix

RTX 50-series GPUs can show this warning on the default Vast.ai PyTorch image:

```text
NVIDIA GeForce RTX 5060 Ti with CUDA capability sm_120 is not compatible with the current PyTorch installation.
The current PyTorch install supports CUDA capabilities sm_50 sm_60 sm_70 sm_75 sm_80 sm_86 sm_90.
```

The warning points to the PyTorch install selector:

```text
https://pytorch.org/get-started/locally/
```

In testing on `vastai/pytorch:cuda-12.4.1-auto`, the preinstalled `/venv/main/bin/python` had `torch 2.11.0+cu126` without `sm_120` support. Installing the CUDA 12.8 nightly command without `--upgrade` did not replace it. The working fix was:

```bash
"$PYTHON_BIN" -m pip install --upgrade --pre torch torchvision torchaudio \
  --index-url https://download.pytorch.org/whl/nightly/cu132
```

Verify success by checking that `torch.cuda.get_arch_list()` includes `sm_120` or `compute_120`. The tested successful environment reported:

```text
torch 2.13.0.dev20260427+cu132
torch_cuda 13.2
arch_list ['sm_75', 'sm_80', 'sm_86', 'sm_90', 'sm_100', 'sm_120', 'compute_120']
```

Use a longer `--cleanup-timeout-minutes` for 50-series first-run jobs because downloading nightly PyTorch wheels can take several minutes.

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

Cheap hello-world validation (no external services):

```bash
python3 /workspace/autosota-lite/plugins/autosota-lite/skills/autosota-vastai-scheduler/scripts/vastai_scheduler.py launch \
  --runtime-hours 0.03 \
  --disk-gb 5 \
  --limit 3 \
  --order dph \
  --offer-type on-demand \
  --image vastai/pytorch \
  --job-cmd 'echo hello world from autosota-vastai-scheduler' \
  --label autosota-vastai-scheduler-hello \
  --ssh \
  --cleanup-timeout-minutes 10 \
  --cleanup-poll-seconds 10 \
  --yes
```

WandB-logged hello-world (validates the full credential pipeline end-to-end):

```bash
set -a && source .env.local && set +a
python3 /workspace/autosota-lite/plugins/autosota-lite/skills/autosota-vastai-scheduler/scripts/vastai_scheduler.py launch \
  --runtime-hours 0.1 \
  --disk-gb 5 \
  --offer-type on-demand \
  --image vastai/pytorch \
  --pass-env WANDB_API_KEY \
  --job-cmd 'pip install -q wandb && python3 -c "
import wandb, os, sys
if not os.getenv(\"WANDB_API_KEY\"): sys.exit(\"WANDB_API_KEY not injected\")
run = wandb.init(project=\"autosota-helloworld\", name=\"vastai-helloworld\")
run.log({\"hello\": 1.0, \"pi\": 3.14159})
run.finish()
"' \
  --label autosota-helloworld \
  --cleanup-timeout-minutes 15 \
  --yes
```

After it finishes, verify the run at `https://wandb.ai/<entity>/autosota-helloworld`. Resolve `<entity>` via `check_keys.py` (it prints the WandB user/entity for the active key).

Interruptible search or launch:

```bash
python3 /workspace/autosota-lite/plugins/autosota-lite/skills/autosota-vastai-scheduler/scripts/vastai_scheduler.py estimate \
  --runtime-hours 0.05 \
  --disk-gb 5 \
  --offer-type bid \
  --limit 5
```

Interruptible launches can create stopped partial contracts when the bid is not immediately scheduled. The script destroys partial contracts if Vast.ai returns `success: false` with `new_contract`.

## New: Cost-Optimized + Profiled Launch Examples

**Safe cost-optimized launch (stay under $0.1/hour):**

```bash
python3 vastai_scheduler.py launch \
  --runtime-hours 4 \
  --disk-gb 80 \
  --gpu "RTX 4090,RTX 3090,RTX 4080" \
  --min-gpu-ram-gb 20 \
  --max-dph 0.1 \  # avoid expensive instances
  --job-cmd 'python train.py --steps 100000' \
  --label cost-optimized-training \
  --yes
```

**Profile before full run (test + extrapolate):**

```bash
python3 vastai_scheduler.py profile \
  --runtime-hours 4 \
  --disk-gb 80 \
  --gpu "RTX 4090,RTX 3090" \
  --min-gpu-ram-gb 20 \
  --max-dph 0.1 \
  --job-cmd 'python train.py --steps 100000' \
  --test-steps 30,40,50 \  # 3 short runs: 30, 40, 50 minutes
  --metrics-to-capture speed,gpu_util,memory,cpu_util \
  --label profile-before-training \
  --yes
```

Profile output shows:
- ✓ How long actual full run will take
- ✓ Actual GPU/memory/CPU utilization
- ✓ Estimated total cost
- ✓ Recommendation (proceed or optimize code)

**Profile + auto-launch if good:**

```bash
python3 vastai_scheduler.py profile \
  --runtime-hours 4 \
  --job-cmd 'python train.py --steps 100000' \
  --test-steps 30,40,50 \
  --max-dph 0.1 \
  --full-run true \  # auto-launch full job if profile looks good
  --estimated-cost 0.24 \  # validate against this budget
  --yes
```

**Advanced: profile with custom metrics**

```bash
python3 vastai_scheduler.py profile \
  --runtime-hours 4 \
  --job-cmd 'python train.py --steps 100000' \
  --test-steps 30,40,50 \
  --metrics-to-capture speed,gpu_util,memory,cpu_util \
  --custom-metrics 'loss,accuracy,validation_loss' \
  --metrics-collection-interval 1.0 \  # sample every 1 second
  --max-dph 0.1 \
  --yes
```

This captures both system metrics (speed, GPU util) and application metrics (loss, accuracy) from your training script output.

## Cost Model

The scheduler estimates:

```text
total_usd = runtime_hours * dph_total + upload_gb * inet_up_cost + download_gb * inet_down_cost
```

`dph_total` is Vast.ai's hourly price for the selected offer with the requested disk size included through `--storage`.

## Important Flags

### Cost Control (NEW)
- `--max-dph 0.1`: **maximum hourly cost in USD** (default: 0.1 = avoid >$0.1/hour instances) ⭐
- `--max-storage-cost 0.20`: maximum storage price in USD/GB/month.
- `--max-inet-up-cost 0.02`: maximum upload price in USD/GB.
- `--max-inet-down-cost 0.02`: maximum download price in USD/GB.

### True Run Estimator (NEW)
- `--profile true`: run short test series before full job (default: false)
- `--test-steps 30,40,50`: duration of each test in minutes (default: 30,40,50)
- `--metrics-to-capture speed,gpu_util,memory,cpu_util`: which metrics to collect (default: all)
- `--metrics-collection-interval 1.0`: interval in seconds between metric captures (default: 1.0)
- `--custom-metrics 'loss,accuracy'`: capture application-specific metrics (optional)
- `--estimated-cost 0.24`: optional cost budget to validate profiling estimate
- `--full-run true`: launch actual job after profiling (default: false)

### General
- `--avoid-countries CN,US`: country-code denylist; default avoids China and the United States.
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

### Reading the cleanup result

The launcher emits a `cleanup` block in its final JSON. Three fields matter:

- `gone`: instance no longer exists in `vastai show instances`. This is the success signal — billing has stopped.
- `saw_job_exit`: the local monitor observed the `[vastai-scheduler] job exited` log line.
- `local_destroyed`: the local monitor was the one that issued `vastai destroy instance`.

For **fast jobs** (jobs that finish in under ~10 seconds), it is normal to see `gone: true, saw_job_exit: false, local_destroyed: false`. The container's onstart script self-destructed before the local monitor's first poll. Do not interpret this as a failure — `gone: true` is what proves cleanup succeeded.

For **slow jobs**, expect `gone: true, saw_job_exit: true`. If you see `gone: false` after the timeout, the instance is still billing and needs `vastai destroy instance <id>` manually.
