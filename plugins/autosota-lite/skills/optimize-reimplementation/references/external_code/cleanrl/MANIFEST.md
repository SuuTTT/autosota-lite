# CleanRL Reference Manifest

These files are bundled as reference implementations for CleanRL-style structure. They are not runtime dependencies.

Source repository: `https://github.com/vwxyzjn/cleanrl`

Retrieved from `master` at commit:

```text
fe8d8a03c41a7ef5b523e2e354bd01c363e786bb
```

Retrieved on: 2026-04-28

## Files

| File | Purpose | Upstream URL |
| --- | --- | --- |
| `ppo.py` | PPO for discrete-action environments | `https://raw.githubusercontent.com/vwxyzjn/cleanrl/master/cleanrl/ppo.py` |
| `ppo_continuous_action.py` | PPO for continuous-action environments | `https://raw.githubusercontent.com/vwxyzjn/cleanrl/master/cleanrl/ppo_continuous_action.py` |
| `dqn.py` | DQN for discrete-action environments | `https://raw.githubusercontent.com/vwxyzjn/cleanrl/master/cleanrl/dqn.py` |
| `sac_continuous_action.py` | SAC for continuous-action environments | `https://raw.githubusercontent.com/vwxyzjn/cleanrl/master/cleanrl/sac_continuous_action.py` |
| `LICENSE` | Upstream MIT license | `https://raw.githubusercontent.com/vwxyzjn/cleanrl/master/LICENSE` |

## Refresh Procedure

When updating these references:

1. Check upstream commit with `git ls-remote https://github.com/vwxyzjn/cleanrl.git HEAD`.
2. Download only the needed single-file references and `LICENSE`.
3. Update this manifest with the commit, retrieval date, and file list.
4. Do not modify the vendored reference files unless clearly marked as local examples.
5. If a reference file imports utilities not bundled here, treat it as a style reference and do not assume it runs standalone inside this skill.
