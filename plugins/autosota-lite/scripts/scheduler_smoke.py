#!/usr/bin/env python3
"""Non-destructive AgentScheduler smoke test for an AutoSOTA workspace.

This script validates the scheduler lifecycle contract without launching an
expensive optimization loop. It inspects the target repo, reads existing
AutoSOTA artifacts, detects blockers, and persists scheduler state.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def run(cmd: list[str], cwd: Path) -> tuple[int, str]:
    proc = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return proc.returncode, proc.stdout.strip()


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def simple_yaml_value(text: str, key: str) -> str | None:
    pattern = re.compile(rf"^{re.escape(key)}:\s*[\"']?(.*?)[\"']?\s*$", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return None
    value = match.group(1).strip()
    return value or None


def score_summary(scores_text: str) -> dict[str, object] | None:
    lines = [line for line in scores_text.splitlines() if line.strip()]
    if not lines:
        return None
    last = lines[-1]
    try:
        return json.loads(last)
    except json.JSONDecodeError:
        return {"raw": last}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a non-destructive AutoSOTA AgentScheduler smoke test.")
    parser.add_argument("repo", type=Path, help="Target research repository")
    parser.add_argument("--state-dir", type=Path, default=None, help="Directory for smoke-test scheduler state")
    parser.add_argument("--paper-id", default=None, help="Paper/task identifier")
    parser.add_argument("--gpus", default="", help="Comma-separated GPU IDs assigned to the test")
    parser.add_argument("--eval-command", default=None, help="Override official_eval_command for this smoke test")
    args = parser.parse_args()

    repo = args.repo.resolve()
    if not repo.exists():
        print(f"error: repo does not exist: {repo}", file=sys.stderr)
        return 2

    state_dir = (args.state_dir or repo / ".autosota_scheduler_test").resolve()
    state_dir.mkdir(parents=True, exist_ok=True)

    autosota_yaml = read_text(repo / "autosota.yaml")
    project = args.paper_id or simple_yaml_value(autosota_yaml, "project") or repo.name
    eval_cmd = args.eval_command or simple_yaml_value(autosota_yaml, "official_eval_command")
    metric_name = simple_yaml_value(autosota_yaml, "  name") or simple_yaml_value(autosota_yaml, "name")
    metric_direction = simple_yaml_value(autosota_yaml, "  direction") or simple_yaml_value(autosota_yaml, "direction")

    git_status_code, git_status = run(["git", "status", "--short"], repo)
    head_code, head = run(["git", "rev-parse", "--short", "HEAD"], repo)
    tags_code, tags = run(["git", "tag", "--list", "_baseline"], repo)

    scores = score_summary(read_text(repo / "scores.jsonl"))
    required = ["autosota.yaml", "objective.md", "red_lines.md", "code_analysis.md", "idea_library.md", "research_report.md"]
    artifact_status = {name: (repo / name).exists() for name in required}

    blockers: list[str] = []
    warnings: list[str] = []
    if git_status_code != 0:
        blockers.append("git status failed")
    if git_status:
        warnings.append("worktree is dirty; destructive scheduler actions such as rollback/tagging are disabled for this smoke test")
    if not eval_cmd:
        blockers.append("official_eval_command missing from autosota.yaml")
    elif "???" in eval_cmd:
        blockers.append(f"official_eval_command has unresolved placeholder: {eval_cmd}")
    if not scores:
        warnings.append("scores.jsonl is missing or empty; Phase 0 baseline has not been recorded")
    if "_baseline" not in tags.splitlines():
        warnings.append("git tag _baseline is missing")
    missing = [name for name, exists in artifact_status.items() if not exists]
    if missing:
        warnings.append("missing AutoSOTA artifacts: " + ", ".join(missing))

    phase = "blocked" if blockers else "ready_for_phase3"
    state = {
        "updated_at": now(),
        "mode": "smoke_test",
        "repo": str(repo),
        "paper_id": project,
        "phase": phase,
        "head": head if head_code == 0 else None,
        "dirty_worktree": bool(git_status),
        "assigned_gpus": [int(x) for x in args.gpus.split(",") if x.strip().isdigit()],
        "metric": {
            "name": metric_name,
            "direction": metric_direction,
        },
        "official_eval_command": eval_cmd,
        "latest_score": scores,
        "artifacts": artifact_status,
        "blockers": blockers,
        "warnings": warnings,
        "next_action": (
            "resolve blockers before launching optimization"
            if blockers
            else "select next CLEARED idea and create PRE_COMMIT snapshot"
        ),
    }

    state_path = state_dir / "scheduler_state.json"
    report_path = state_dir / "scheduler_smoke_report.md"
    state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report_path.write_text(
        "\n".join(
            [
                f"# AgentScheduler Smoke Test: {project}",
                "",
                f"- Timestamp: {state['updated_at']}",
                f"- Repo: `{repo}`",
                f"- Phase: `{phase}`",
                f"- HEAD: `{state['head']}`",
                f"- Dirty worktree: `{state['dirty_worktree']}`",
                f"- Evaluation command: `{eval_cmd}`",
                f"- Latest score: `{json.dumps(scores, sort_keys=True)}`",
                f"- Blockers: {', '.join(blockers) if blockers else 'none'}",
                f"- Warnings: {', '.join(warnings) if warnings else 'none'}",
                f"- Next action: {state['next_action']}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(json.dumps({"state": str(state_path), "report": str(report_path), "phase": phase, "blockers": blockers}, indent=2))
    return 1 if blockers else 0


if __name__ == "__main__":
    raise SystemExit(main())
