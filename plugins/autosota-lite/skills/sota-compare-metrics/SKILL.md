---
name: sota-compare-metrics
description: Compare metrics between original and reimplemented code. Produce comparison tables, improvement analysis, and formatted reports.
---

# SOTA Compare Metrics

Compare original research code with your reimplementation across multiple dimensions: performance, speed, memory, readability, and deployment.

## Purpose

After reimplementing code, prove that your version is better (or equally good) using objective metrics.

## Use Cases

- **Speed:** Original takes 2 hours/epoch, yours takes 90 min → 25% faster
- **Memory:** Original uses 8GB, yours uses 5GB → 37% reduction
- **Readability:** Original 2000 lines, yours 200 lines → 90% smaller
- **Deployment:** Original needs 12 packages, yours needs 3 → 75% fewer deps

## Required Inputs

```yaml
original:
  code: path/to/original_code
  logs: path/to/original_run_logs
  metrics: {accuracy: 0.95, speed: 42.3, memory: 2048}

reimplemented:
  code: path/to/reimplemented_code
  logs: path/to/reimplemented_run_logs
  metrics: {accuracy: 0.951, speed: 28.1, memory: 1536}

dimensions:
  - performance      # accuracy, loss, convergence
  - speed           # wall-clock time per epoch
  - memory          # peak memory usage
  - readability     # code lines, complexity
  - deployment      # dependencies, install size
```

## Metrics Captured

### Performance Dimension
```
- Final accuracy / loss
- Convergence speed (steps to target)
- Best epoch plateau
- Variance across runs
```

### Speed Dimension
```
- Wall-clock time per epoch
- Time per sample
- Throughput (samples/sec)
- GPU utilization
- CPU utilization
```

### Memory Dimension
```
- Peak memory usage
- Average memory usage
- Memory per sample
- Memory growth rate
```

### Readability Dimension
```
- Lines of code
- Cyclomatic complexity
- Type hints coverage
- Function documentation coverage
- Test coverage
```

### Deployment Dimension
```
- Dependency count
- Dependency versions
- Total install size
- Model size (if applicable)
- Inference latency
```

## Output Artifacts

```
comparison_results/
├── comparison_table.md        # formatted table
├── comparison_table.csv       # CSV for spreadsheets
├── improvement_summary.txt    # one-page summary
├── detailed_report.md         # full analysis
├── metrics.json              # all numbers
├── visualizations/
│   ├── accuracy_curve.png
│   ├── speed_comparison.png
│   ├── memory_comparison.png
│   └── code_metrics.png
└── comparison_checklist.md    # validation
```

## Comparison Table Output

```
╔════════════════════════════════════════════════════════════════════╗
║           Original vs Reimplemented: Detailed Comparison          ║
╠════════════════════════════════════════════════════════════════════╣
║ PERFORMANCE                                                        ║
├────────────────────────────────────────────────────────────────────┤
║ Metric          │ Original  │ Reimplemented │ Delta    │ Verdict  ║
╠────────────────────────────────────────────────────────────────────╣
║ Final Accuracy  │ 95.00%    │ 95.10%        │ +0.10%   │ ✓ MATCH  ║
║ Best Epoch Loss │ 0.145     │ 0.142         │ -1.9%    │ ✓ BETTER ║
║ Convergence     │ 150 steps │ 148 steps     │ -1.3%    │ ~ SAME   ║
╠════════════════════════════════════════════════════════════════════╣
║ SPEED                                                              ║
├────────────────────────────────────────────────────────────────────┤
║ Metric          │ Original  │ Reimplemented │ Delta    │ Verdict  ║
╠────────────────────────────────────────────────────────────────────╣
║ Time/Epoch      │ 42.3 sec  │ 28.1 sec      │ +33.4%   │ ✓ FASTER ║
║ Samples/Sec     │ 1204 smp  │ 1816 smp      │ +50.7%   │ ✓ FASTER ║
║ GPU Util        │ 67%       │ 84%           │ +25.4%   │ ✓ BETTER ║
╠════════════════════════════════════════════════════════════════════╣
║ MEMORY                                                             ║
├────────────────────────────────────────────────────────────────────┤
║ Metric          │ Original  │ Reimplemented │ Delta    │ Verdict  ║
╠────────────────────────────────────────────────────────────────────╣
║ Peak Memory     │ 2048 MB   │ 1536 MB       │ -25.0%   │ ✓ LESS   ║
║ Avg Memory      │ 1824 MB   │ 1328 MB       │ -27.2%   │ ✓ LESS   ║
║ Memory/Sample   │ 1.52 MB   │ 0.97 MB       │ -36.2%   │ ✓ LESS   ║
╠════════════════════════════════════════════════════════════════════╣
║ READABILITY                                                        ║
├────────────────────────────────────────────────────────────────────┤
║ Metric          │ Original  │ Reimplemented │ Delta    │ Verdict  ║
╠────────────────────────────────────────────────────────────────────╣
║ Lines of Code   │ 1850      │ 240           │ -87.0%   │ ✓ MUCH CLEANER ║
║ Complexity      │ 42        │ 8             │ -81.0%   │ ✓ SIMPLER   ║
║ Type Hints      │ 10%       │ 100%          │ +90%     │ ✓ BETTER    ║
║ Doc Coverage    │ 45%       │ 100%          │ +55%     │ ✓ BETTER    ║
╠════════════════════════════════════════════════════════════════════╣
║ DEPLOYMENT                                                         ║
├────────────────────────────────────────────────────────────────────┤
║ Metric          │ Original  │ Reimplemented │ Delta    │ Verdict  ║
╠────────────────────────────────────────────────────────────────────╣
║ Dependencies    │ 12        │ 3             │ -75.0%   │ ✓ MUCH LIGHTER ║
║ Install Size    │ 850 MB    │ 180 MB        │ -78.8%   │ ✓ MUCH SMALLER ║
║ Import Time     │ 4.2 sec   │ 0.8 sec       │ +81.0%   │ ✓ FASTER    ║
║ Model Size      │ 45 MB     │ 42 MB         │ -6.7%    │ ~ SAME      ║
╚════════════════════════════════════════════════════════════════════╝

SUMMARY
───────────────────────────────────────────────────────────────────────
✅ PERFORMANCE: Reimplementation matches original results
✅ SPEED:      33% faster per epoch
✅ MEMORY:     25% lower peak memory
✅ READABILITY: 87% fewer lines, 100% type hints
✅ DEPLOYMENT: 75% fewer dependencies

VERDICT: ✅ REIMPLEMENTATION SUCCESSFUL
Your code beats the original on speed, memory, and maintainability
while maintaining accuracy.
```

## Improvement Summary (For Notification)

```
🎉 Beat SOTA: PPO Reimplementation

Performance: ✓ Matches (95.1% vs 95.0%)
Speed:       ✓ 33% faster (28.1s vs 42.3s per epoch)
Memory:      ✓ 25% reduction (1536 vs 2048 MB)
Code:        ✓ 87% smaller (240 vs 1850 lines)
Deps:        ✓ 75% fewer (3 vs 12)

Full report: comparison_report.md
```

## Validation Rules

Before comparing, validate that reimplementation is valid:

```python
# Accuracy must be within threshold
assert abs(new_accuracy - original_accuracy) <= acceptable_drop

# Shape consistency check
assert shapes_match(original_output, reimplemented_output)

# Performance bounds check
assert not has_nan(reimplemented_metrics)
assert not has_infinity(reimplemented_metrics)

# Reproducibility check
assert runs_are_consistent(reimplemented_code)
```

## Comparison Dimensions

### 1. Performance (Must Match)
```yaml
accuracy_drop_tolerance: 1.0%      # Can be 1% worse
loss_threshold: similar            # Loss should be similar
convergence_speed: within 2x       # Should converge in 2x steps max
```

### 2. Speed (Should Improve)
```yaml
wall_clock_improvement: >=0%       # Can be same speed
samples_per_sec: higher is better
gpu_utilization: >=70%
```

### 3. Memory (Should Improve)
```yaml
peak_memory_reduction: >=0%        # Can be same memory
average_memory: lower is better
memory_per_sample: lower is better
```

### 4. Readability (Should Improve)
```yaml
lines_of_code: fewer is better
cyclomatic_complexity: lower is better
type_hints_coverage: 100% is ideal
documentation: complete is ideal
```

### 5. Deployment (Should Improve)
```yaml
dependency_count: fewer is better
total_size: smaller is better
inference_speed: faster is better
```

## Usage

```python
from sota_compare_metrics import CompareMetrics

comparator = CompareMetrics(
    original_code="path/to/original",
    original_metrics={"accuracy": 0.95, "speed": 42.3},
    
    reimplemented_code="path/to/reimplemented",
    reimplemented_metrics={"accuracy": 0.951, "speed": 28.1},
    
    dimensions=["performance", "speed", "memory", "readability"]
)

# Generate comparison
comparison = comparator.compare()

# Get summary
summary = comparator.summary()
print(summary)
# Output: "✅ Beat SOTA: 33% faster, 25% less memory"

# Get table
table = comparator.table(format="markdown")
print(table)

# Get all metrics
metrics = comparator.metrics_dict()
# Returns: {original: {...}, reimplemented: {...}, delta: {...}}
```

## Output Formats

```python
# Markdown table
comparator.table(format="markdown")

# CSV for spreadsheets
comparator.table(format="csv")

# JSON for programmatic use
comparator.table(format="json")

# HTML for web
comparator.table(format="html")

# Text for terminal
comparator.table(format="text")
```

## Metrics Definition

Define custom metrics for your domain:

```yaml
custom_metrics:
  - name: inference_latency
    unit: ms
    measure: "time to inference on 1 sample"
    is_better: lower
    
  - name: throughput
    unit: samples/sec
    measure: "samples processed per second"
    is_better: higher
    
  - name: model_size
    unit: MB
    measure: "serialized model size"
    is_better: lower
```

## Visualization

Generate comparison charts:

```python
comparator.plot_comparison(
    dimensions=["speed", "memory", "accuracy"],
    output_dir="comparison_plots/"
)
# Produces: speed_comparison.png, memory_comparison.png, etc.
```

## Integration with Workflows

Used in `sota-workflow-orchestrator`:

```yaml
- stage: "Test & Compare"
  skill: sota-compare-metrics
  inputs:
    original_code: ${baseline.outputs.code}
    original_metrics: ${baseline.outputs.metrics}
    new_code: ${reimplement.outputs.code}
    new_metrics: ${reimplement.outputs.metrics}
  outputs:
    - comparison_table
    - improvement_summary
    - detailed_report
```

## Success Criteria

Your comparison is successful when:

✅ **Correctness**
- Accuracy matches original (±acceptable%)
- All metrics are valid (no NaN/Inf)

✅ **Improvement**
- At least ONE dimension is better (speed, memory, or readability)
- No dimension gets worse (except expected accuracy trade-off)

✅ **Reportability**
- Comparison table is clear
- Summary is concise
- Report is professional
