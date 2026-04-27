---
name: autosota-research-loop
description: Run an AutoSOTA-style workflow for ML paper reproduction, baseline reproduction, experiment iteration, score auditing, and benchmark-safe improvement in real machine learning repositories.
---

# AutoSOTA Research Loop

Use this skill when the user asks for AutoSOTA, ML paper reproduction, reproducing a baseline, improving a reported score, iterating on experiments, auditing scores, checking benchmark validity, or preparing a reproduction report. This is one large v0 skill that coordinates setup, baseline, ideation, iteration, audit, and report work without adding extra skills.

The core promise: improve research velocity without weakening benchmark integrity. Metric code and test data are frozen unless the official benchmark maintainers publish a new version and the user explicitly chooses to migrate.

## Non-Negotiable Red Lines

These rules apply in every mode:

- Never modify ground-truth labels.
- Never modify the test split.
- Never modify official metric calculation.
- Never hard-code answers.
- Never skip hard examples.
- Never silently change the eval command.
- Treat metric code and test data as frozen.

If a user request, repo script, or proposed idea conflicts with these rules, stop and explain the conflict. If an eval command must change for a legitimate reason, record the old command, new command, reason, date, and expected score impact in `red_lines.md` and the active run log before executing it.

## Required Workspace Files

Require or create these files when applicable to the active mode:

- `resource_map.md`: Paper, code, dataset, checkpoint, eval script, benchmark docs, leaderboard, and issue tracker links or local paths.
- `objective.md`: Target claim, benchmark, metric direction, target split, allowed resources, constraints, and acceptance criteria.
- `code_analysis.md`: Repository map, training/eval entrypoints, dependency notes, data flow, protected files, and risk areas.
- `red_lines.md`: Frozen metric/test data rules, protected files, protected commands, known official eval command, and approved deviations.
- `idea_library.md`: Ideas, hypotheses, type labels, status, result summaries, validity, decision, and next action.
- `scores.jsonl`: One JSON object per eval, including crashed, partial, worse, neutral, invalid, and improved runs.
- `autosota.yaml`: Project config for dataset paths, commands, metrics, seeds, budgets, and report settings.
- `runs/`: Per-run configs, outputs, predictions, checkpoints, diffs, and artifacts.
- `logs/`: Terminal logs, eval logs, training logs, environment captures, and audit notes.

When starting in an incomplete workspace, create only the missing files needed for the current mode. Do not invent scores, paper claims, dataset facts, official commands, package versions, or leaderboard positions.

## Global Operating Rules

- Before modifying code, configs, scripts, prompts, preprocessing, training settings, or eval settings, create a git checkpoint. Prefer a real commit when appropriate; otherwise record the current branch, `git status --short`, and commit SHA in the mode output and in the active log.
- Do not modify files outside the intended experiment scope. Read protected files before touching adjacent code.
- Run the smallest meaningful validation before expensive training or eval.
- After every eval, append a record to `scores.jsonl`. An eval includes official eval, validation eval, smoke eval with metrics, ablation eval, failed eval, crashed eval, and invalid eval.
- After every idea attempt, update `idea_library.md` with status, result, validity, decision, and next action.
- Recommend `KEEP` only when the run is valid under the red-line rules and improves the selected metric against the relevant baseline.
- Recommend `ROLLBACK` when the run is invalid, crashes, cannot be evaluated, worsens the selected metric, or improves only by violating the audit rules.
- If the last three attempted ideas in `idea_library.md` were `PARAM`-only ideas, choose a non-`PARAM` idea next. This leap rule is mandatory unless the user explicitly asks to continue parameter search.
- Prefer official benchmark documentation and repository scripts over ad hoc assumptions.
- Keep every experiment reproducible from a command, config, commit/checkpoint, seed, metric output, artifact path, and log path.
- Use deterministic seeds when supported.
- Make one meaningful change per iteration so metric deltas can be interpreted.
- Treat failed runs as useful evidence and record them.
- For current leaderboards, package versions, benchmark rules, or paper errata that may have changed, verify from primary sources before relying on memory.

## Mode Selection

If the user names a mode, run that mode. If they do not name a mode:

- Use `setup` for a new paper, new repo, unclear objective, missing benchmark constraints, or missing workspace files.
- Use `baseline` when the goal is reproducing the reported result or establishing a first score.
- Use `ideation` when the baseline exists and the user wants next experiments.
- Use `iteration` when an idea is selected or the user asks Codex to try improvements.
- Use `audit` before trusting a score gain, opening a PR, or writing final claims.
- Use `report` when the user wants a summary, writeup, README, issue, PR note, or experiment memo.

## Strict Output Format

Every mode must end with exactly this structure, filling `N/A` only when genuinely not applicable:

```text
Mode: <setup|baseline|ideation|iteration|audit|report>
Status: <READY|BLOCKED|RUNNING|COMPLETE|FAILED>
Git checkpoint: <commit sha, branch/status snapshot, or N/A with reason>
Files read: <comma-separated paths>
Files changed: <comma-separated paths or none>
Commands run: <exact commands or none>
Eval command: <exact eval command or N/A>
Score update: <scores.jsonl entry summary, pending, or N/A>
Idea update: <idea_library.md entry summary, pending, or N/A>
Decision: <KEEP|ROLLBACK|REVISE|AUDIT_REQUIRED|N/A>
Evidence: <metrics, logs, artifacts, and audit facts>
Risks: <remaining benchmark, data, implementation, or reproducibility risks>
Next action: <one concrete next step>
```

## setup Mode

Goal: establish the reproduction workspace, official target, and integrity boundaries before experiments begin.

Required steps:

1. Read the paper, repo README, benchmark docs, available configs, and existing workspace files.
2. Create or update `resource_map.md`, `objective.md`, `code_analysis.md`, `red_lines.md`, and `autosota.yaml`.
3. Identify the official dataset split, metric direction, metric implementation, canonical eval command, expected baseline, hardware assumptions, and known paper/repo caveats.
4. Mark metric code and test data as frozen in `red_lines.md`.
5. Create `runs/` and `logs/` if experiments are expected.
6. Do not modify research code unless setup explicitly requires a config or documentation change; if it does, create a git checkpoint first.

Mode-specific output requirements:

- `Evidence` must include the target metric, metric direction, official eval command, protected files, and missing resources.
- `Next action` must be the exact baseline command or the single blocker to resolve.

## baseline Mode

Goal: reproduce the published or expected baseline as faithfully as possible.

Required steps:

1. Read `objective.md`, `autosota.yaml`, `resource_map.md`, `code_analysis.md`, and `red_lines.md`.
2. Confirm the official eval command has not changed silently.
3. Create a git checkpoint before modifying any code, config, dependency lockfile, preprocessing path, or eval setting.
4. Run dependency, data, and smoke checks before expensive jobs.
5. Execute the canonical train/eval path without changing metric logic, test data, ground-truth labels, answer paths, or hard-example coverage.
6. Save logs under `logs/` and artifacts under `runs/`.
7. Append every eval result to `scores.jsonl`, including failed or crashed evals.
8. If a baseline reproduction issue becomes an idea candidate, add or update it in `idea_library.md`.

Mode-specific output requirements:

- `Score update` must identify the appended `scores.jsonl` run id or explain why no eval ran.
- `Decision` should be `AUDIT_REQUIRED` for any baseline score that will be used as a comparison point.
- `Evidence` must include baseline score, paper/expected score, delta, command, artifacts, logs, and environment notes.

## ideation Mode

Goal: propose legitimate reproduction fixes or improvement ideas that preserve benchmark integrity.

Required steps:

1. Read `code_analysis.md`, `objective.md`, `red_lines.md`, `scores.jsonl`, `idea_library.md`, and relevant logs.
2. Check the last attempted ideas in `idea_library.md`. If the last three were `PARAM`-only, select at least one non-`PARAM` idea next.
3. Generate ideas that obey all red-line rules.
4. Label every idea with exactly one primary type: `BUGFIX`, `REPRO`, `MODEL`, `TRAINING`, `DATA_PIPELINE`, `EVAL_HYGIENE`, `EFFICIENCY`, `ANALYSIS`, or `PARAM`.
5. For each idea, record hypothesis, expected impact, cost, risk, files likely touched, validation command, official eval command, and rollback plan.
6. Update `idea_library.md` with the ranked ideas and selected next attempt.

Mode-specific output requirements:

- `Idea update` must summarize the new or changed `idea_library.md` entries.
- `Decision` must be `N/A` unless an existing attempted idea is being judged.
- `Next action` must name the one selected idea and its first validation command.

## iteration Mode

Goal: implement and test one controlled idea at a time.

Required steps:

1. Read `idea_library.md`, `scores.jsonl`, `objective.md`, `red_lines.md`, `autosota.yaml`, and relevant code.
2. Apply the leap rule: if the last three attempted ideas were `PARAM`-only, choose a non-`PARAM` idea next unless the user explicitly overrides it.
3. Select one idea and mark it `IN_PROGRESS` in `idea_library.md`.
4. Record hypothesis, files to edit, git checkpoint, validation command, official eval command, and rollback plan before editing.
5. Create a git checkpoint before modifying code or configs.
6. Make the minimal scoped change needed to test the idea.
7. Run the smallest meaningful validation first, then the official eval when justified.
8. Append every eval result to `scores.jsonl`.
9. Update `idea_library.md` after the attempt with status, metrics, validity, decision, and next action.
10. Recommend `KEEP` only if the result is valid and improved. Recommend `ROLLBACK` if invalid, crashed, unevaluable, or worse. Use `REVISE` only for a valid but inconclusive result that should not be kept as an improvement claim.

Mode-specific output requirements:

- `Git checkpoint` must show the checkpoint created before edits.
- `Score update` must identify every appended eval record.
- `Idea update` must include final idea status and decision.
- `Decision` must be `KEEP`, `ROLLBACK`, or `REVISE`.
- `Evidence` must include metric delta versus the relevant baseline, validity status, changed files, logs, and artifacts.

## audit Mode

Goal: verify that a baseline, claimed reproduction, or improvement is real and benchmark-compliant.

Required steps:

1. Read `red_lines.md`, `scores.jsonl`, `idea_library.md`, `objective.md`, `autosota.yaml`, relevant logs, and relevant diffs.
2. Compare code, configs, data files, eval scripts, and commands against the protected files and commands in `red_lines.md`.
3. Confirm that ground-truth labels, test split, metric calculation, answer paths, and hard-example coverage were not modified.
4. Confirm metric code and test data are frozen.
5. Verify that every eval has a `scores.jsonl` record with command, checkpoint/commit, seed when applicable, metrics, logs, and artifacts.
6. Verify that every attempted idea has an `idea_library.md` update.
7. Re-run or spot-check the official eval command when feasible.
8. Mark invalid, crashed, missing-artifact, or worse runs as `ROLLBACK` candidates.

Mode-specific output requirements:

- `Decision` must be `KEEP` only if the audited result is valid and improved.
- `Decision` must be `ROLLBACK` if the result is invalid, crashed, unevaluable, or worse.
- `Evidence` must list audit checks passed/failed, protected files reviewed, score records reviewed, and idea records reviewed.
- `Risks` must include any missing logs, missing artifacts, uncontrolled randomness, dependency drift, or command drift.

## report Mode

Goal: produce a transparent reproduction and improvement report.

Required steps:

1. Read `objective.md`, `resource_map.md`, `code_analysis.md`, `idea_library.md`, `scores.jsonl`, `red_lines.md`, `autosota.yaml`, and relevant logs.
2. Summarize the paper target, benchmark, metric direction, environment, official eval command, baseline, iterations, best valid result, and audit status.
3. Include commands, checkpoints/commits, configs, seeds, metrics, log paths, and artifact paths.
4. Distinguish confirmed results from hypotheses, failed experiments, invalid runs, and unaudited improvements.
5. State that metric code and test data were frozen, or explicitly list any unresolved concern.
6. Do not claim SOTA, paper parity, or improvement unless the result is valid and audited.

Mode-specific output requirements:

- `Score update` is usually `N/A` unless the report mode also runs an eval.
- `Idea update` is usually `N/A` unless the report changes idea statuses.
- `Decision` must summarize the strongest supportable claim: `KEEP`, `ROLLBACK`, `AUDIT_REQUIRED`, or `N/A`.
- `Evidence` must include the best valid score, baseline score, delta, official command, artifacts, and audit status.

## `idea_library.md` Entry Template

```markdown
## <idea-id>: <short title>

- Type: <BUGFIX|REPRO|MODEL|TRAINING|DATA_PIPELINE|EVAL_HYGIENE|EFFICIENCY|ANALYSIS|PARAM>
- Status: <PROPOSED|IN_PROGRESS|ATTEMPTED|KEPT|ROLLED_BACK|REVISED|BLOCKED>
- Hypothesis: <why this might help>
- Expected impact: <metric and direction>
- Risk: <benchmark, implementation, compute, or reproducibility risk>
- Files likely touched: <paths>
- Validation command: <exact command>
- Official eval command: <exact command>
- Git checkpoint: <sha/status snapshot>
- Result: <metric, crash, invalid, or pending>
- Validity: <valid|invalid|unknown and why>
- Decision: <KEEP|ROLLBACK|REVISE|AUDIT_REQUIRED|N/A>
- Next action: <one concrete next step>
```

## `scores.jsonl` Record Template

```json
{"timestamp":"2026-04-27T00:00:00Z","mode":"iteration","run_id":"iteration-001","idea_id":"idea-001","idea_type":"MODEL","commit":"<git-sha-or-checkpoint>","command":"<exact eval command>","config":"autosota.yaml","dataset_split":"<validation|test|other>","metric_name":"<metric>","metric_direction":"<higher_is_better|lower_is_better>","metrics":{"<metric>":0.0},"validity":"<valid|invalid|crashed|unknown>","decision":"<KEEP|ROLLBACK|REVISE|AUDIT_REQUIRED|N/A>","artifacts":["runs/iteration-001"],"logs":["logs/iteration-001.log"],"notes":"<short note>"}
```

## Minimal `autosota.yaml` Shape

```yaml
project: ""
paper: ""
benchmark: ""
metric:
  name: ""
  direction: ""
official_eval_command: ""
train_command: ""
validation_command: ""
dataset:
  train: ""
  validation: ""
  test: ""
frozen:
  metric_code: []
  test_data: []
  label_files: []
seeds: []
budget:
  max_hours: null
  max_runs: null
outputs:
  runs_dir: runs
  logs_dir: logs
```
