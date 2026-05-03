#!/usr/bin/env python3
"""Reusable RL experiment-section helpers and rliable-style plots.

The script reads JSONL experiment logs, normalizes them into benchmark matrices,
computes robust aggregate summaries, and can render a Markdown experiment section
or a small set of reusable plots.

The preferred backend is `rliable` when available. If it is not installed, the
script falls back to a pure-Python summary path with the same data contract.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        records.append(json.loads(line))
    return records


def _group_records(
    records: Sequence[Mapping[str, Any]],
    algorithm_field: str,
    run_id_field: str,
    task_field: str,
    score_field: str,
) -> tuple[dict[str, dict[str, dict[str, float]]], list[str]]:
    grouped: dict[str, dict[str, dict[str, float]]] = defaultdict(lambda: defaultdict(dict))
    tasks: set[str] = set()
    for record in records:
        algo = str(record[algorithm_field])
        run_id = str(record[run_id_field])
        task = str(record[task_field])
        score = float(record[score_field])
        grouped[algo][run_id][task] = score
        tasks.add(task)
    return grouped, sorted(tasks)


def _score_matrix_for_algo(
    runs: Mapping[str, Mapping[str, float]],
    tasks: Sequence[str],
) -> list[list[float]]:
    matrix: list[list[float]] = []
    for run_id in sorted(runs):
        run_scores = runs[run_id]
        row = [run_scores.get(task, math.nan) for task in tasks]
        if any(math.isnan(value) for value in row):
            continue
        matrix.append(row)
    return matrix


def build_score_dict(
    records: Sequence[Mapping[str, Any]],
    algorithm_field: str = "algorithm",
    run_id_field: str = "run_id",
    task_field: str = "task",
    score_field: str = "normalized_score",
) -> tuple[dict[str, list[list[float]]], list[str]]:
    grouped, tasks = _group_records(records, algorithm_field, run_id_field, task_field, score_field)
    score_dict = {algo: _score_matrix_for_algo(runs, tasks) for algo, runs in grouped.items()}
    return score_dict, tasks


def _flatten(values: Sequence[Sequence[float]]) -> list[float]:
    return [item for row in values for item in row]


def _iqm(values: Sequence[float]) -> float:
    data = sorted(values)
    if not data:
        return math.nan
    lower = len(data) // 4
    upper = len(data) - lower
    core = data[lower:upper]
    return statistics.fmean(core) if core else statistics.fmean(data)


def _optimality_gap(values: Sequence[float], target: float = 1.0) -> float:
    data = [max(0.0, target - float(v)) for v in values]
    return statistics.fmean(data) if data else math.nan


def _format_number(value: Any) -> str:
    if value is None:
        return "n/a"
    try:
        return f"{float(value):.4f}"
    except (TypeError, ValueError):
        return str(value)


def _bootstrap_ci(
    values: Sequence[float],
    fn,
    reps: int = 2000,
    alpha: float = 0.05,
) -> tuple[float, float]:
    if not values:
        return math.nan, math.nan
    rng = random.Random(0)
    estimates = []
    n = len(values)
    for _ in range(reps):
        sample = [values[rng.randrange(n)] for _ in range(n)]
        estimates.append(fn(sample))
    estimates.sort()
    lo = int((alpha / 2) * len(estimates))
    hi = max(lo, int((1 - alpha / 2) * len(estimates)) - 1)
    return estimates[lo], estimates[hi]


def _summarize_python(score_dict: Mapping[str, Sequence[Sequence[float]]]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    for algo, matrix in score_dict.items():
        flat = _flatten(matrix)
        if not flat:
            continue
        summary[algo] = {
            "mean": statistics.fmean(flat),
            "median": statistics.median(flat),
            "iqm": _iqm(flat),
            "optimality_gap": _optimality_gap(flat),
            "ci95": {
                "mean": _bootstrap_ci(flat, statistics.fmean),
                "median": _bootstrap_ci(flat, statistics.median),
                "iqm": _bootstrap_ci(flat, _iqm),
            },
        }
    return summary


def summarize_scores(score_dict: Mapping[str, Sequence[Sequence[float]]]) -> dict[str, Any]:
    try:
        import numpy as np  # type: ignore
        from rliable import library as rly  # type: ignore
        from rliable import metrics  # type: ignore
    except Exception:
        return _summarize_python(score_dict)

    aggregate_func = lambda x: np.array(
        [
            metrics.aggregate_median(x),
            metrics.aggregate_iqm(x),
            metrics.aggregate_mean(x),
            metrics.aggregate_optimality_gap(x),
        ]
    )
    aggregate_scores, aggregate_cis = rly.get_interval_estimates(score_dict, aggregate_func, reps=5000)
    summary: dict[str, Any] = {}
    metric_names = ["median", "iqm", "mean", "optimality_gap"]
    for algo, values in aggregate_scores.items():
        cis = aggregate_cis[algo]
        summary[algo] = {
            name: float(values[idx]) for idx, name in enumerate(metric_names)
        }
        summary[algo]["ci95"] = {
            name: [float(cis[idx][0]), float(cis[idx][1])] for idx, name in enumerate(metric_names)
        }
    return summary


def render_experiment_section(
    benchmark: str,
    tasks: Sequence[str],
    summary: Mapping[str, Any],
    protocol_version: str = "v1",
) -> str:
    lines = [
        f"## Experimental setup",
        f"- Benchmark: {benchmark}",
        f"- Tasks: {len(tasks)}",
        f"- Protocol: {protocol_version}",
        "",
        "## Protocol",
        "- Report raw and normalized scores separately.",
        "- Keep task order fixed across algorithms.",
        "- Use the same seed count and evaluation command for all methods.",
        "",
        "## Main results",
    ]
    for algo, metrics in sorted(summary.items()):
        ci = metrics.get("ci95", {})
        lines.append(
            f"- {algo}: IQM={_format_number(metrics.get('iqm'))} "
            f"(95% CI {tuple(ci.get('iqm', ('n/a', 'n/a')))}), "
            f"median={_format_number(metrics.get('median'))}, mean={_format_number(metrics.get('mean'))}"
        )
    lines += [
        "",
        "## Robustness views",
        "- Add performance profiles, probability-of-improvement plots, and sample-efficiency curves when checkpoints are available.",
        "- State any invalid, missing, or partially evaluated runs explicitly.",
    ]
    return "\n".join(lines)


def _write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _plot_with_matplotlib(summary: Mapping[str, Any], output: Path) -> None:
    try:
        import matplotlib.pyplot as plt  # type: ignore
    except Exception as exc:  # pragma: no cover - environment dependent
        raise RuntimeError("matplotlib is required for plots command") from exc

    algos = list(summary)
    iqm = [summary[a]["iqm"] for a in algos]
    median = [summary[a]["median"] for a in algos]

    fig, ax = plt.subplots(figsize=(max(6, len(algos) * 1.2), 4))
    xs = range(len(algos))
    ax.bar([x - 0.15 for x in xs], median, width=0.3, label="Median")
    ax.bar([x + 0.15 for x in xs], iqm, width=0.3, label="IQM")
    ax.set_xticks(list(xs))
    ax.set_xticklabels(algos, rotation=30, ha="right")
    ax.set_ylabel("Score")
    ax.set_title("RL aggregate metrics")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)


def _plot_performance_profile(score_dict: Mapping[str, Sequence[Sequence[float]]], output: Path) -> None:
    try:
        import numpy as np  # type: ignore
        import matplotlib.pyplot as plt  # type: ignore
        from rliable import library as rly  # type: ignore
        from rliable import plot_utils  # type: ignore
    except Exception as exc:  # pragma: no cover - environment dependent
        raise RuntimeError("rliable, numpy, and matplotlib are required for performance profiles") from exc

    thresholds = np.linspace(0.0, 1.0, 101)
    profiles, cis = rly.create_performance_profile(score_dict, thresholds)
    fig, ax = plt.subplots(figsize=(7, 5))
    plot_utils.plot_performance_profiles(
        profiles,
        thresholds,
        performance_profile_cis=cis,
        ax=ax,
        xlabel="Normalized score threshold",
    )
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)


def cmd_summary(args: argparse.Namespace) -> int:
    records = load_jsonl(args.input)
    score_dict, tasks = build_score_dict(
        records,
        algorithm_field=args.algorithm_field,
        run_id_field=args.run_id_field,
        task_field=args.task_field,
        score_field=args.score_field,
    )
    summary = summarize_scores(score_dict)
    payload = {"benchmark": args.benchmark, "tasks": tasks, "summary": summary}
    _write_json(args.output, payload)
    return 0


def cmd_section(args: argparse.Namespace) -> int:
    records = load_jsonl(args.input)
    score_dict, tasks = build_score_dict(
        records,
        algorithm_field=args.algorithm_field,
        run_id_field=args.run_id_field,
        task_field=args.task_field,
        score_field=args.score_field,
    )
    summary = summarize_scores(score_dict)
    text = render_experiment_section(args.benchmark, tasks, summary, protocol_version=args.protocol_version)
    args.output.write_text(text + "\n", encoding="utf-8")
    return 0


def cmd_plots(args: argparse.Namespace) -> int:
    records = load_jsonl(args.input)
    score_dict, _ = build_score_dict(
        records,
        algorithm_field=args.algorithm_field,
        run_id_field=args.run_id_field,
        task_field=args.task_field,
        score_field=args.score_field,
    )
    summary = summarize_scores(score_dict)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    _plot_with_matplotlib(summary, args.output_dir / "aggregate_metrics.png")
    _plot_performance_profile(score_dict, args.output_dir / "performance_profiles.png")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("input", type=Path, help="Experiment JSONL log.")
    common.add_argument("--benchmark", default="RL Benchmark")
    common.add_argument("--algorithm-field", default="algorithm")
    common.add_argument("--run-id-field", default="run_id")
    common.add_argument("--task-field", default="task")
    common.add_argument("--score-field", default="normalized_score")

    p = sub.add_parser("summary", parents=[common], help="Write JSON summary.")
    p.add_argument("-o", "--output", type=Path, required=True)
    p.set_defaults(func=cmd_summary)

    p = sub.add_parser("section", parents=[common], help="Write Markdown experiment section.")
    p.add_argument("-o", "--output", type=Path, required=True)
    p.add_argument("--protocol-version", default="v1")
    p.set_defaults(func=cmd_section)

    p = sub.add_parser("plots", parents=[common], help="Write reusable plots.")
    p.add_argument("-o", "--output-dir", type=Path, required=True)
    p.set_defaults(func=cmd_plots)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
