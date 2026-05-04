# GPU Scheduler Updates: Cost Control + True Run Estimator

Updated: `util-gpu-scheduler` (formerly vastai-scheduler)

---

## Overview

The GPU scheduler now includes:

1. **Cost Control** — Automatically filter out expensive instances
2. **True Run Estimator** — Profile actual performance before committing full compute

---

## 1️⃣ Cost Control

### Default: Avoid >$0.1/hour Instances

```bash
# NEW: Default behavior - only show instances under $0.1/hour
python3 vastai_scheduler.py launch \
  --runtime-hours 4 \
  --job-cmd 'python train.py' \
  --yes
# Only considers instances costing <$0.1/hour
```

### Custom Cost Limits

```bash
# Allow up to $0.15/hour
python3 vastai_scheduler.py launch \
  --max-dph 0.15 \
  --runtime-hours 4 \
  --job-cmd 'python train.py' \
  --yes

# Very conservative: stay under $0.05/hour
python3 vastai_scheduler.py launch \
  --max-dph 0.05 \
  --runtime-hours 4 \
  --job-cmd 'python train.py' \
  --yes
```

### Estimate Cost Before Launching

```bash
# See estimated costs for instances matching your criteria
python3 vastai_scheduler.py estimate \
  --runtime-hours 4 \
  --disk-gb 80 \
  --max-dph 0.1
```

**Output:**
```
Top 5 offers (under $0.10/hour):
  1. RTX 4090 (24GB)    $0.067/hr  →  total: $0.27 (4 hours)
  2. RTX 3090 (24GB)    $0.052/hr  →  total: $0.21
  3. RTX 4080 (12GB)    $0.048/hr  →  total: $0.19
  4. RTX A100 (40GB)    $0.089/hr  →  total: $0.36
  5. L40 (48GB)         $0.095/hr  →  total: $0.38
```

---

## 2️⃣ True Run Estimator

### Why Profile Before Full Run?

**Problem:** You have a 4-hour training job. But will it actually run in 4 hours on this hardware?
- Is GPU utilization stable?
- Will memory increase (leaks)?
- What's the actual throughput?

**Solution:** Run 3 quick tests (30, 40, 50 minutes) to measure actual behavior, then extrapolate to full run.

### Workflow

```
Step 1: Run 30-minute test
        → measure: speed, GPU util, memory, CPU util
        
Step 2: Run 40-minute test
        → validate: performance stable?
        
Step 3: Run 50-minute test
        → estimate: actual time for full run
        
Step 4: Auto-extrapolate
        → decide: proceed or optimize code first?
```

### Usage

**Basic profiling:**

```bash
python3 vastai_scheduler.py profile \
  --runtime-hours 4 \
  --job-cmd 'python train.py --steps 100000' \
  --test-steps 30,40,50 \  # minutes for each test
  --max-dph 0.1 \
  --yes
```

**With custom metrics:**

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

**Auto-launch full run if profiling looks good:**

```bash
python3 vastai_scheduler.py profile \
  --runtime-hours 4 \
  --job-cmd 'python train.py --steps 100000' \
  --test-steps 30,40,50 \
  --full-run true \  # auto-launch full job if profile OK
  --estimated-cost 0.24 \  # validate against budget
  --max-dph 0.1 \
  --yes
```

### Profile Output Example

```
═══════════════════════════════════════════════════════════════
True Run Estimator: PPO Training (target: 4 hours)
═══════════════════════════════════════════════════════════════

Instance:     RTX 4090 (24 GB) on us-west
Cost/hour:    $0.067
Max cost:     $0.27 (4 hours)

TEST 1: 30 minutes
  ✓ Speed:      1,200 steps/min
  ✓ GPU Util:   84% (stable)
  ✓ Memory:     6.2 GB / 24 GB (26%)
  ✓ CPU Util:   45%
  Cost:         $0.033

TEST 2: 40 minutes
  ✓ Speed:      1,195 steps/min (consistent)
  ✓ GPU Util:   83% (stable)
  ✓ Memory:     6.3 GB / 24 GB (26%)
  ✓ CPU Util:   46%
  Cost:         $0.045

TEST 3: 50 minutes
  ✓ Speed:      1,198 steps/min (avg: 1,198)
  ✓ GPU Util:   83% (stable)
  ✓ Memory:     6.2 GB / 24 GB (26%)
  ✓ CPU Util:   45%
  Cost:         $0.056

═══════════════════════════════════════════════════════════════
EXTRAPOLATION TO FULL RUN (4 hours = 240 minutes)
═══════════════════════════════════════════════════════════════

Avg Speed:         1,198 steps/min
Est. Full Time:    240 min ✓ (matches target)
Total Steps:       287,520
Peak Memory:       6.3 GB
Memory Headroom:   17.7 GB available ✓
Avg GPU Util:      83% (excellent)
Avg CPU Util:      45%

═══════════════════════════════════════════════════════════════
COST ANALYSIS
═══════════════════════════════════════════════════════════════

Test Series Total:    $0.134 (3 tests)
Full Run Est.:        $0.268 (4 hours @ $0.067/hr)
Total (tests + run):  $0.402

Budget Check:         ✓ Within $0.50 limit

═══════════════════════════════════════════════════════════════
RECOMMENDATION
═══════════════════════════════════════════════════════════════

✅ PROCEED WITH FULL RUN

Why:
  • Performance is stable (no degradation across tests)
  • Memory is stable (no leaks detected)
  • GPU utilization excellent (83%)
  • Cost is reasonable ($0.27 for 4-hour run)
  • Speed matches expectations (1,200 steps/min)

Next step:
  python3 vastai_scheduler.py launch \
    --full-run true \
    --estimated-cost 0.27 \
    --yes
```

---

## Metrics Captured

### System Metrics

```
Performance:
  • Steps/iterations per minute (throughput)
  • Time per epoch/iteration
  • Convergence rate

Hardware:
  • GPU utilization (%)
  • GPU memory usage (GB)
  • GPU temperature (°C)
  • CPU utilization (%)
  • CPU memory usage (GB)

Network:
  • Data upload speed (MB/s)
  • Data download speed (MB/s)
  • Network latency (if applicable)

Cost:
  • Cumulative cost per test
  • Cost per step
  • Cost per hour
  • Extrapolated total cost
```

### Custom Metrics (Application-Specific)

You can capture your training script's output:

```bash
--custom-metrics 'loss,accuracy,validation_loss,f1_score'
```

The scheduler will extract these from your job output (JSON, CSV, or key=value format).

---

## Safety Features

### Cost Guards

```
Default behavior:
  • Only show instances <$0.1/hour
  • Estimate total cost (runtime + storage + network)
  • Warn if estimated cost exceeds budget
  • Allow override with --max-dph flag
```

### Performance Guards (Profiling)

```
Before committing full compute:
  • Run short test (30 min)
  • Run medium test (40 min)
  • Run long test (50 min)
  • Validate: performance stable?
  • Validate: memory leaks?
  • Recommend: proceed or optimize?
```

---

## Examples

### Example 1: Quick Cost-Optimized Training

```bash
python3 vastai_scheduler.py launch \
  --runtime-hours 4 \
  --disk-gb 80 \
  --gpu "RTX 4090,RTX 3090" \
  --min-gpu-ram-gb 20 \
  --max-dph 0.1 \  # avoid expensive instances
  --job-cmd 'python train.py --steps 100000' \
  --label my-training-run \
  --cleanup-timeout-minutes 20 \
  --yes
```

**Result:** Finds cheapest instance <$0.1/hour, launches immediately.

### Example 2: Profile Before Large Run

```bash
python3 vastai_scheduler.py profile \
  --runtime-hours 24 \  # long job (1 day)
  --disk-gb 200 \
  --job-cmd 'python train.py --epochs 1000' \
  --test-steps 30,40,50 \  # profile with 30, 40, 50 min runs
  --metrics-to-capture speed,gpu_util,memory,cpu_util \
  --max-dph 0.1 \
  --yes
```

**Result:**
1. Runs 3 test jobs (30+40+50 min)
2. Shows actual performance metrics
3. Extrapolates to full 24-hour run
4. Estimates total cost
5. Recommends proceed or optimize

### Example 3: Profile + Auto-Launch

```bash
python3 vastai_scheduler.py profile \
  --runtime-hours 24 \
  --disk-gb 200 \
  --job-cmd 'python train.py --epochs 1000' \
  --test-steps 30,40,50 \
  --full-run true \  # auto-launch full job
  --estimated-cost 1.50 \  # validate budget
  --max-dph 0.1 \
  --yes
```

**Result:**
1. Profiles (3 short runs)
2. If profiling looks good, automatically launches full 24-hour training
3. Watches for completion and cleanup

### Example 4: Conservative Budget

```bash
python3 vastai_scheduler.py launch \
  --runtime-hours 4 \
  --max-dph 0.05 \  # very conservative: <$0.05/hour only
  --job-cmd 'python train.py' \
  --yes
```

**Result:** Only searches for instances <$0.05/hour (very cheap options).

---

## Flags Summary

### Cost Control

| Flag | Default | Purpose |
|------|---------|---------|
| `--max-dph` | 0.1 | Max hourly cost (USD) |
| `--max-storage-cost` | 0.20 | Max storage cost (USD/GB/month) |
| `--max-inet-up-cost` | 0.02 | Max upload cost (USD/GB) |
| `--max-inet-down-cost` | 0.02 | Max download cost (USD/GB) |

### Profiling

| Flag | Default | Purpose |
|------|---------|---------|
| `--profile` | false | Enable profiling (test before full run) |
| `--test-steps` | 30,40,50 | Duration of each test (minutes) |
| `--metrics-to-capture` | all | Which metrics to collect |
| `--metrics-collection-interval` | 1.0 | Sample interval (seconds) |
| `--custom-metrics` | none | Application-specific metrics |
| `--full-run` | false | Auto-launch full job after profiling |
| `--estimated-cost` | none | Budget to validate against |

---

## Cost Model

```
Total Cost = (runtime_hours × dph) + (upload_gb × inet_up_cost) + (download_gb × inet_down_cost)

Example (4-hour RTX 4090 run):
  Rental cost:     4 hours × $0.067/hr      = $0.268
  Upload cost:     10 GB × $0.005/GB        = $0.050
  Download cost:   50 GB × $0.002/GB        = $0.100
  ───────────────────────────────────────────────────
  Total cost:                                 $0.418
```

---

## When to Use Each Feature

### Cost Control (`--max-dph`)

✅ **Always use** — Filter out expensive instances by default

```bash
--max-dph 0.1  # avoid expensive hardware
```

### Profiling (`--profile`)

✅ **Use when:** Job runs >4 hours and you want to validate performance first

```bash
--profile true --test-steps 30,40,50 --full-run true
```

✅ **Use when:** You want to capture application-specific metrics

```bash
--custom-metrics 'loss,accuracy,validation_loss'
```

❌ **Don't use:** For quick <1 hour jobs where you're not worried about cost

---

## Troubleshooting

**"No instances found under $0.1/hour"**
- Increase budget: `--max-dph 0.15`
- Check available hardware: `--estimate` only
- Try different GPU requirements: `--gpu "A100,L40"`

**"Memory usage increasing (leak detected)"**
- Profiling shows memory growth
- Recommendation: check code for memory leaks
- Option: increase available GPU memory: `--min-gpu-ram-gb 40`

**"Speed degraded in test 3"**
- Profiling shows throughput dropped in longer run
- Recommendation: investigate code bottleneck
- Option: reduce batch size or optimize code before full run

---

## Summary

| Feature | Benefit |
|---------|---------|
| **Cost Control** | Avoid expensive instances, stay within budget |
| **True Run Estimator** | Know real performance before committing compute |
| **Auto-Profiling** | 3 quick tests → accurate extrapolation |
| **Metrics Collection** | Capture system + application metrics |
| **Smart Recommendation** | Proceed or optimize based on profiling |

Use together: Stay cost-conscious + validate performance = smart GPU spending!
