# Runtime Estimation Formulas

Use measured or reported throughput whenever available. Formula-only estimates are `LOW` confidence unless supported by comparable logs.

## Core Formulas

```text
runtime_hours = total_steps / steps_per_second / 3600 * overhead_factor
total_steps = num_updates * num_envs * num_steps
num_updates = total_timesteps / (num_envs * num_steps)
autosota_loop_hours = one_iteration_hours * iterations * rerun_factor
total_seed_hours = one_run_hours * num_seeds
expected_cost = runtime_hours * dollars_per_hour + storage_cost + bandwidth_cost
high_cost = expected_cost * safety_multiplier
```

## Overhead Factors

- `1.10` for clean eval-only runs.
- `1.25` for stable training runs.
- `1.50` for RL with checkpointing, eval, or logging.
- `2.00` for unstable research repos or heavy debugging.

## Practical Notes

- Use wall-clock reported runtime directly when hardware and workload match.
- For RL, include eval, checkpoint, logging, environment reset, and video overhead when enabled.
- For AutoSOTA loops, include reruns for failed ideas, invalid runs, dependency fixes, and audit reruns when known. If unknown, use a transparent `rerun_factor` and list it as an assumption.
- For concurrent experiments, distinguish elapsed wall-clock time from total GPU-hours or instance-hours.
