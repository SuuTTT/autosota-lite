# GPU Scheduler Skill Test Guide

Test the updated `util-gpu-scheduler` skill with a real Vast.ai GPU rental, WandB logging, and Slack notification.

---

## What This Test Does

```
1. Rent a cheap GPU from Vast.ai (<$0.1/hour)
   ↓
2. Run training script on the GPU
   • 5 epochs of dummy training
   • Log metrics to WandB
   • Show GPU/CPU utilization
   ↓
3. Notify Slack when complete
   • Training results
   • WandB link
   • GPU info
   ↓
4. Cleanup and billing ends
```

---

## Prerequisites

### 1. Vast.ai Account & API Key

Create account: https://vast.ai

Get API key:
- Log in → Account → API
- Copy your API key

Set locally:
```bash
vastai set api-key YOUR_API_KEY
```

### 2. WandB Credentials

Already configured in `.env.local`:
```bash
cat /workspace/autosota-lite/.env.local | grep WANDB_API_KEY
```

If not present, get one from: https://wandb.ai/settings/keys

### 3. Slack Webhook

Already configured in `.env.local`:
```bash
cat /workspace/autosota-lite/.env.local | grep SLACK_WEBHOOK_URL
```

If not present, create one:
- https://api.slack.com/apps
- Create app → Incoming Webhooks
- Copy webhook URL

### 4. Load Credentials

```bash
# Load from .env.local
cd /workspace/autosota-lite
set -a && source .env.local && set +a

# Verify
echo "WandB: $WANDB_API_KEY"
echo "Slack: $SLACK_WEBHOOK_URL"
```

---

## Test 1: Local Test (No GPU Rental)

Test the script locally to verify everything works:

```bash
cd /workspace/autosota-lite

# Load credentials
set -a && source .env.local && set +a

# Run test script locally
python3 test_gpu_scheduler.py
```

**Expected output:**

```
============================================================
GPU SCHEDULER TEST SCRIPT
============================================================
Start time: 2026-05-03 13:45:00 UTC
Environment: linux

✅ WANDB_API_KEY found
✅ SLACK_WEBHOOK_URL found

============================================================
GPU Scheduler Test: WandB + Slack Notification
============================================================

✅ WandB initialized: https://wandb.ai/your-entity/autosota-gpu-scheduler-test/runs/abc123

============================================================
Training...
============================================================
Epoch 1/5: loss=0.4231
Epoch 2/5: loss=0.3891
Epoch 3/5: loss=0.3542
Epoch 4/5: loss=0.3124
Epoch 5/5: loss=0.2891

✅ Training complete!
✅ WandB run saved: https://wandb.ai/your-entity/autosota-gpu-scheduler-test/runs/abc123

============================================================
Sending Slack notification...
============================================================
✅ Slack notification sent!

============================================================
TEST COMPLETE
============================================================
{
  "status": "success",
  "final_loss": 0.2891,
  "epochs": 5,
  "wandb_url": "https://wandb.ai/your-entity/autosota-gpu-scheduler-test/runs/abc123"
}

End time: 2026-05-03 13:45:15 UTC
```

**Verify:**
1. ✅ Check WandB: https://wandb.ai/your-entity/autosota-gpu-scheduler-test
2. ✅ Check Slack: See message in your channel
3. ✅ No GPU rental yet

---

## Test 2: Cost Estimate Only

See what GPUs are available and their estimated cost:

```bash
cd /workspace/autosota-lite/plugins/autosota-lite/skills/util-gpu-scheduler

# Estimate cost for 30-minute job
python3 scripts/vastai_scheduler.py estimate \
  --runtime-hours 0.5 \
  --disk-gb 10 \
  --gpu "RTX 4090,RTX 3090,RTX 4080" \
  --min-gpu-ram-gb 10 \
  --max-dph 0.1
```

**Expected output:**

```
Searching Vast.ai for instances matching criteria...
  GPU: RTX 4090, RTX 3090, RTX 4080
  Max cost: $0.10/hour
  Disk: 10 GB
  Min GPU RAM: 10 GB

Found 8 matching instances:

  1. RTX 4090 (24GB) - us-west   $0.067/hr
     Total: $0.034 (30 min)
     
  2. RTX 3090 (24GB) - eu-west   $0.052/hr
     Total: $0.026 (30 min)
     
  3. RTX 4080 (12GB) - us-east   $0.048/hr
     Total: $0.024 (30 min)
     
  [... more options ...]
```

**No rental yet** — just showing what's available.

---

## Test 3: Dry-Run Launch (SSH Only, No Job)

Test the rental without actually running the job (just SSH in):

```bash
python3 scripts/vastai_scheduler.py launch \
  --runtime-hours 0.25 \  # 15 minutes
  --disk-gb 10 \
  --gpu "RTX 4090,RTX 3090,RTX 4080" \
  --min-gpu-ram-gb 10 \
  --max-dph 0.1 \
  --job-cmd "echo 'test' && sleep 10" \
  --label "autosota-gpu-scheduler-test-dryrun" \
  --cleanup-timeout-minutes 5 \
  --ssh
```

**What happens:**
1. Rents a cheap GPU for 15 minutes
2. SSHes into the instance
3. You can verify GPU availability
4. Automatically cleaned up after 5 minutes

**Expected output:**

```
Searching Vast.ai for instances...
Found RTX 4090 at $0.067/hr

Cost estimate: $0.017 (15 minutes)
Estimated total cost: $0.017
✓ Within budget ($0.1/hour max)

Launching instance...
✓ Instance created: bid_123456
✓ SSH key registered
✓ Waiting for SSH access...

SSH ready! Connect with:
  ssh root@123.45.67.89 -p 22

Or continue with automated job...
```

---

## Test 4: Full Test - Rent GPU, Train, Log to WandB, Notify Slack

The complete end-to-end test:

```bash
cd /workspace/autosota-lite/plugins/autosota-lite/skills/util-gpu-scheduler

# Load credentials
cd /workspace/autosota-lite
set -a && source .env.local && set +a

# Launch GPU job with WandB + Slack
python3 scripts/vastai_scheduler.py launch \
  --runtime-hours 0.25 \  # 15 minutes (cheap!)
  --disk-gb 10 \
  --gpu "RTX 4090,RTX 3090,RTX 4080" \
  --min-gpu-ram-gb 10 \
  --max-dph 0.1 \
  --image vastai/pytorch \
  --pass-env WANDB_API_KEY,SLACK_WEBHOOK_URL \
  --job-cmd 'cd /tmp && curl -s https://raw.githubusercontent.com/your-repo/test_gpu_scheduler.py -o test.py && python3 test.py' \
  --label "autosota-gpu-scheduler-test" \
  --cleanup-timeout-minutes 10 \
  --yes
```

**What happens:**

```
Step 1: Estimate Cost
  Cheapest option: RTX 3090 at $0.052/hr
  Total (15 min): $0.013
  ✓ Within budget

Step 2: Launch Instance
  ✓ Rented instance bid_789012
  Cost so far: $0.002

Step 3: Run Job
  ✓ Starting training script...
  
  Epoch 1/5: loss=0.4231
  Epoch 2/5: loss=0.3891
  Epoch 3/5: loss=0.3542
  Epoch 4/5: loss=0.3124
  Epoch 5/5: loss=0.2891
  
  ✓ Training complete
  ✓ Logged to WandB
  ✓ Notified Slack

Step 4: Cleanup
  ✓ Destroying instance
  Final cost: $0.013
  ✓ Billing stopped
```

**Verify Success:**

1. **WandB:** https://wandb.ai/your-entity/autosota-gpu-scheduler-test
   - New run appears with GPU metrics
   
2. **Slack:** Check your configured channel
   - "✅ GPU Scheduler Test Complete!" message
   - Shows final loss, WandB link
   
3. **Vast.ai:** Log in to verify instance was destroyed
   - Check Billing → should show ~$0.013 charge

---

## Test 5: Profile Before Full Run

Test the new "True Run Estimator" feature:

```bash
python3 scripts/vastai_scheduler.py profile \
  --runtime-hours 1 \
  --disk-gb 10 \
  --gpu "RTX 4090,RTX 3090" \
  --min-gpu-ram-gb 10 \
  --max-dph 0.1 \
  --image vastai/pytorch \
  --pass-env WANDB_API_KEY,SLACK_WEBHOOK_URL \
  --job-cmd 'cd /tmp && python3 test_gpu_scheduler.py' \
  --test-steps 5,10,15 \  # 5, 10, 15 minute tests
  --metrics-to-capture speed,gpu_util,memory,cpu_util \
  --label "autosota-gpu-scheduler-profile" \
  --yes
```

**Expected output:**

```
═══════════════════════════════════════════════════════════
True Run Estimator: Test Script (target: 1 hour)
═══════════════════════════════════════════════════════════

TEST 1: 5 minutes
  Speed:      Training completed in 30 sec
  GPU Util:   78%
  Memory:     2.1 GB / 24 GB (9%)
  CPU Util:   35%
  Cost:       $0.004

TEST 2: 10 minutes
  Speed:      Training completed in 30 sec (consistent)
  GPU Util:   77%
  Memory:     2.2 GB / 24 GB (9%)
  CPU Util:   36%
  Cost:       $0.008

TEST 3: 15 minutes
  Speed:      Training completed in 30 sec (avg: 30 sec)
  GPU Util:   78%
  Memory:     2.1 GB / 24 GB (9%)
  CPU Util:   35%
  Cost:       $0.013

═══════════════════════════════════════════════════════════
EXTRAPOLATION TO FULL RUN (1 hour)
═══════════════════════════════════════════════════════════

Total Time:        30 sec (training is fast!)
Estimated Cost:    $0.052 (1 hour @ $0.052/hr)
Peak Memory:       2.2 GB (plenty available)
Avg GPU Util:      78% (good)

═══════════════════════════════════════════════════════════
✅ RECOMMENDATION: PROCEED WITH FULL RUN

Why:
  • Performance stable across tests
  • Memory usage low (9%)
  • GPU utilization good (78%)
  • Cost very low ($0.052 for full hour)
```

---

## Troubleshooting

### "No API key found"

```bash
vastai set api-key YOUR_API_KEY
vastai show user
```

### "No instances found under $0.1/hour"

Increase budget:
```bash
--max-dph 0.15
```

Or use less demanding GPU:
```bash
--gpu "RTX 3060,RTX 3070"  # cheaper older GPUs
```

### "WandB credentials not found"

Verify .env.local:
```bash
cat /workspace/autosota-lite/.env.local
```

Load credentials:
```bash
set -a && source .env.local && set +a
echo $WANDB_API_KEY
```

### "Slack notification not received"

Verify webhook:
```bash
curl -X POST $SLACK_WEBHOOK_URL \
  -H 'Content-Type: application/json' \
  -d '{"text":"Test message"}'
```

### Instance didn't cleanup

Manually destroy:
```bash
vastai destroy instance <INSTANCE_ID>
```

---

## Cost Reference

| GPU | Cost/Hour | 15 min | 30 min | 1 hour |
|-----|-----------|--------|--------|--------|
| RTX 3060 | $0.015 | $0.004 | $0.008 | $0.015 |
| RTX 3090 | $0.052 | $0.013 | $0.026 | $0.052 |
| RTX 4080 | $0.048 | $0.012 | $0.024 | $0.048 |
| RTX 4090 | $0.067 | $0.017 | $0.034 | $0.067 |

*Estimates from Vast.ai live pricing*

---

## Complete Test Checklist

- [ ] Vast.ai API key configured
- [ ] WandB credentials in .env.local
- [ ] Slack webhook in .env.local
- [ ] Test 1: Local test runs successfully
- [ ] Test 1: WandB run created
- [ ] Test 1: Slack notification received
- [ ] Test 2: Cost estimate shows available GPUs
- [ ] Test 3: Dry-run SSH connects successfully
- [ ] Test 4: Full rental, training, and cleanup works
- [ ] Test 4: Billing reflects actual cost (~$0.01-0.05)
- [ ] Test 5: Profile feature shows metrics
- [ ] All tests: No errors, clean cleanup

---

## Success Criteria

✅ **Test Passed When:**

1. Local training works without GPU
2. WandB runs are created and visible
3. Slack receives notifications
4. GPU instance rents for <$0.02 (15 minutes)
5. Training runs on GPU (GPU utilization >70%)
6. Cleanup is automatic (no manual intervention needed)
7. Billing is accurate and reasonable

---

## Next Steps

After successful test:

1. **Scale up:** Increase `--runtime-hours` for longer jobs
2. **Use profile:** For jobs >1 hour, use `--profile` flag first
3. **Cost control:** Always use `--max-dph 0.1` (or your budget)
4. **Integrate:** Use in your workflows with `sota-workflow-orchestrator`

---

## Support

If tests fail:

1. Check Vast.ai status: https://status.vast.ai
2. Verify API key: `vastai show user`
3. Check Slack/WandB credentials
4. Read full GPU scheduler docs: `util-gpu-scheduler/SKILL.md`

---

## Timeline

Typical test execution:

```
Local test:        ~15 seconds
Cost estimate:     ~5 seconds
Dry-run SSH:       ~30 seconds (wait for instance)
Full rental test:  ~2-3 minutes (rent → train → cleanup)
Profile test:      ~10-15 minutes (3 short runs)
```

**Total: ~20 minutes for full test suite**

Cost: **~$0.02-0.05 USD** (depending on GPU)
