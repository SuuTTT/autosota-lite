#!/usr/bin/env python3
"""Cost-aware Vast.ai batch scheduler.

The scheduler searches live Vast.ai offers, estimates total task cost, rents the
lowest-cost matching instance when explicitly confirmed, and injects an on-start
script that destroys the instance after the user command exits.
"""

from __future__ import annotations

import argparse
import ast
import base64
import json
import math
import os
import re
import shlex
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Embedded Python metrics script (base64-encoded at import time so that the
# bash on-start probe script can run it without quoting/escaping issues).
# ---------------------------------------------------------------------------
_PROBE_METRICS_PY = """\
import csv, json, os, re, statistics

def read_cpu(path):
    line = open(path).read().split()
    return [int(x) for x in line[1:]]

def parse_meminfo(path):
    d = {}
    for ln in open(path):
        m = re.match(r'(\\w+):\\s+(\\d+)', ln)
        if m:
            d[m.group(1)] = int(m.group(2))
    return d

try:
    cpu0 = read_cpu('/tmp/vs_cpu_start.txt')
    cpu1 = read_cpu('/tmp/vs_cpu_end.txt')
    idle_delta = cpu1[3] - cpu0[3]
    total_delta = sum(cpu1) - sum(cpu0)
    cpu_util = round((1 - idle_delta / total_delta) * 100, 1) if total_delta > 0 else None
except Exception:
    cpu_util = None

try:
    mem = parse_meminfo('/tmp/vs_meminfo_end.txt')
    ram_used_gb = round((mem.get('MemTotal', 0) - mem.get('MemAvailable', 0)) / 1024 / 1024, 2)
    ram_total_gb = round(mem.get('MemTotal', 0) / 1024 / 1024, 2)
except Exception:
    ram_used_gb = ram_total_gb = None

gpu_util, gpu_mem_util, gpu_mem_mb = [], [], []
try:
    with open('/workspace/vastai-job/gpu_samples.csv') as f:
        for row in csv.reader(f):
            try:
                gpu_util.append(float(row[0].strip()))
                gpu_mem_util.append(float(row[1].strip()))
                gpu_mem_mb.append(float(row[2].strip()))
            except (ValueError, IndexError):
                pass
except FileNotFoundError:
    pass

def avg_max(vals):
    if not vals:
        return {'avg': None, 'max': None}
    return {'avg': round(statistics.mean(vals), 1), 'max': round(max(vals), 1)}

metrics = {
    'duration_seconds': int(os.environ.get('PROBE_DURATION', '0')),
    'job_exit_code': int(os.environ.get('JOB_EXIT', '-1')),
    'cpu_util_pct': cpu_util,
    'ram_used_gb': ram_used_gb,
    'ram_total_gb': ram_total_gb,
    'gpu_util_pct': avg_max(gpu_util),
    'gpu_mem_util_pct': avg_max(gpu_mem_util),
    'gpu_mem_used_mb': avg_max(gpu_mem_mb),
    'gpu_samples_count': len(gpu_util),
}
print('[vastai-scheduler probe-metrics ' + json.dumps(metrics) + ']')
"""
_PROBE_METRICS_B64: str = base64.b64encode(_PROBE_METRICS_PY.encode()).decode()


DEFAULT_AVOID_COUNTRIES = "CN,US"
DEFAULT_IMAGE = "vastai/pytorch"


@dataclass(frozen=True)
class SchedulerConfig:
    runtime_hours: float
    disk_gb: float
    upload_gb: float
    download_gb: float
    gpu_names: list[str]
    num_gpus: int
    min_gpu_ram_gb: float | None
    min_cpu_cores: float | None
    min_cpu_ram_gb: float | None
    min_reliability: float
    max_hourly_cost: float
    max_storage_cost: float
    max_inet_up_cost: float
    max_inet_down_cost: float
    avoid_countries: list[str]
    extra_query: str | None
    limit: int
    order: str
    offer_type: str


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def run_vastai(args: list[str]) -> tuple[int, str]:
    proc = subprocess.run(
        ["vastai", *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return proc.returncode, proc.stdout.strip()


def ensure_ssh_key_registered() -> None:
    """Check if any SSH key is registered in Vast.ai; if not, register the local public key."""
    code, output = run_vastai(["show", "ssh-keys", "--raw"])
    if code == 0:
        try:
            keys = json.loads(output)
            if keys:
                return  # At least one key is already registered
        except json.JSONDecodeError:
            pass

    # No keys found or error reading keys, attempt to register local public key
    pub_key_path = Path.home() / ".ssh" / "id_ed25519.pub"
    if not pub_key_path.exists():
        # Maybe it's RSA?
        pub_key_path = Path.home() / ".ssh" / "id_rsa.pub"

    if pub_key_path.exists():
        print(f"Registering local public key {pub_key_path} with Vast.ai...", file=sys.stderr)
        code, output = run_vastai(["create", "ssh-key", str(pub_key_path)])
        if code != 0:
            print(f"Warning: Failed to register SSH key: {output}", file=sys.stderr)
    else:
        print("Warning: No local SSH public key found and none registered in Vast.ai. SSH access might fail.", file=sys.stderr)


def instance_exists(instance_id: int) -> bool:
    for _ in range(3):
        code, output = run_vastai(["show", "instances", "--raw"])
        if code == 0:
            try:
                rows = json.loads(output)
                return any(row.get("id") == instance_id for row in rows if isinstance(row, dict))
            except json.JSONDecodeError:
                pass
        time.sleep(2)
    return False


def instance_logs(instance_id: int, tail: int = 200) -> str:
    _, output = run_vastai(["logs", str(instance_id), "--tail", str(tail)])
    return output


def redact_sensitive(text: str) -> str:
    for marker in ("instance_api_key", "api_key", "CONTAINER_API_KEY"):
        if marker in text:
            try:
                parsed = json.loads(text)
            except json.JSONDecodeError:
                return text.replace(marker, f"{marker}_redacted")
            if isinstance(parsed, dict):
                for key in list(parsed):
                    if "api_key" in key.lower():
                        parsed[key] = "[redacted]"
                return json.dumps(parsed, indent=2, sort_keys=True)
    return text


_SENSITIVE_SUBSTRINGS = frozenset(["api_key", "token", "secret", "password"])


def redact_mapping(data: dict[str, Any]) -> dict[str, Any]:
    redacted = dict(data)
    for key in list(redacted):
        key_lower = key.lower()
        if any(pat in key_lower for pat in _SENSITIVE_SUBSTRINGS):
            redacted[key] = "[redacted]"
    return redacted


def parse_csv(value: str) -> list[str]:
    return [part.strip() for part in value.split(",") if part.strip()]


def quote_query_value(value: str) -> str:
    if any(ch.isspace() for ch in value):
        return json.dumps(value)
    return value


def build_query(config: SchedulerConfig) -> str:
    parts = [
        "rentable=true",
        "rented=false",
        "verified=true",
        f"reliability>{config.min_reliability}",
        f"num_gpus>={config.num_gpus}",
        f"disk_space>={config.disk_gb}",
        f"dph_total<={config.max_hourly_cost}",
        f"storage_cost<={config.max_storage_cost}",
        f"inet_up_cost<={config.max_inet_up_cost}",
        f"inet_down_cost<={config.max_inet_down_cost}",
    ]
    if config.gpu_names:
        gpu_values = ",".join(quote_query_value(name) for name in config.gpu_names)
        parts.append(f"gpu_name in [{gpu_values}]")
    if config.min_gpu_ram_gb is not None:
        parts.append(f"gpu_ram>={config.min_gpu_ram_gb}")
    if config.min_cpu_cores is not None:
        parts.append(f"cpu_cores_effective>={config.min_cpu_cores}")
    if config.min_cpu_ram_gb is not None:
        parts.append(f"cpu_ram>={config.min_cpu_ram_gb}")
    if config.avoid_countries:
        countries = ",".join(config.avoid_countries)
        parts.append(f"geolocation notin [{countries}]")
    if config.extra_query:
        parts.append(config.extra_query)
    return " ".join(parts)


def search_offers(config: SchedulerConfig) -> list[dict[str, Any]]:
    query = build_query(config)
    code, output = run_vastai(
        [
            "search",
            "offers",
            query,
            "--type",
            config.offer_type,
            "--storage",
            str(config.disk_gb),
            "--limit",
            str(config.limit),
            "--order",
            config.order,
            "--raw",
        ]
    )
    if code != 0:
        raise RuntimeError(f"vastai search failed:\n{output}")
    try:
        rows = json.loads(output)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"vastai search did not return JSON:\n{output}") from exc
    if not isinstance(rows, list):
        raise RuntimeError(f"unexpected vastai search response: {rows!r}")
    return rows


def field_float(row: dict[str, Any], key: str, default: float = 0.0) -> float:
    value = row.get(key, default)
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def hourly_cost(row: dict[str, Any]) -> float:
    for key in ("dph_total", "discounted_dph_total", "dph_total_adj"):
        value = field_float(row, key, math.nan)
        if not math.isnan(value) and value > 0:
            return value
    search = row.get("search")
    if isinstance(search, dict):
        value = field_float(search, "totalHour", math.nan)
        if not math.isnan(value) and value > 0:
            return value
    return 0.0


def estimated_total_cost(row: dict[str, Any], config: SchedulerConfig) -> float:
    compute_and_disk = config.runtime_hours * hourly_cost(row)
    network = (
        config.upload_gb * field_float(row, "inet_up_cost")
        + config.download_gb * field_float(row, "inet_down_cost")
    )
    return compute_and_disk + network


def summarize_offer(row: dict[str, Any], config: SchedulerConfig) -> dict[str, Any]:
    return {
        "offer_id": row.get("id") or row.get("ask_contract_id"),
        "gpu": f"{row.get('num_gpus')}x {row.get('gpu_name')}",
        "gpu_ram_gb": round(field_float(row, "gpu_ram") / 1024, 2),
        "cpu_cores_effective": row.get("cpu_cores_effective"),
        "cpu_ram_gb": round(field_float(row, "cpu_ram") / 1024, 2),
        "disk_space_gb": row.get("disk_space"),
        "disk_bw_mb_s": row.get("disk_bw"),
        "inet_down_mbps": row.get("inet_down"),
        "inet_up_mbps": row.get("inet_up"),
        "inet_down_cost_usd_per_gb": row.get("inet_down_cost"),
        "inet_up_cost_usd_per_gb": row.get("inet_up_cost"),
        "storage_cost_usd_per_gb_month": row.get("storage_cost"),
        "hourly_usd": round(hourly_cost(row), 6),
        "bid_price_usd": round(suggested_bid_price(row), 6) if config.offer_type == "bid" else None,
        "estimated_total_usd": round(estimated_total_cost(row, config), 6),
        "reliability": row.get("reliability"),
        "geolocation": row.get("geolocation"),
        "duration_days": row.get("duration"),
        "verified": row.get("verification") or row.get("verified"),
    }


def choose_offer(rows: list[dict[str, Any]], config: SchedulerConfig) -> dict[str, Any] | None:
    if not rows:
        return None
    eligible = [row for row in rows if hourly_cost(row) <= config.max_hourly_cost]
    if not eligible:
        excluded = len(rows)
        print(
            f"Warning: all {excluded} offer(s) exceed max_hourly_cost=${config.max_hourly_cost:.3f}/hr; "
            "raise --max-hourly-cost to include them.",
            file=sys.stderr,
        )
        return None
    return min(eligible, key=lambda row: (estimated_total_cost(row, config), -field_float(row, "reliability")))


def suggested_bid_price(row: dict[str, Any]) -> float:
    """Return the per-machine interruptible bid price Vast.ai expects."""
    candidates = [
        field_float(row, "dph_base"),
        field_float(row, "min_bid"),
        hourly_cost(row) - field_float(row, "storage_total_cost"),
    ]
    return max(value for value in candidates if value >= 0)


def build_onstart(job_cmd: str, destroy_on_success_only: bool = False) -> str:
    destroy_condition = "[[ $status -eq 0 ]]" if destroy_on_success_only else "true"
    return f"""#!/usr/bin/env bash
set -uo pipefail
export DEBIAN_FRONTEND=noninteractive
mkdir -p /workspace/vastai-job
LOG=/workspace/vastai-job/job.log
STATUS=/workspace/vastai-job/status.json
echo "[vastai-scheduler $(TZ=Asia/Shanghai date '+%Y-%m-%dT%H:%M:%S%z')] started at $(date -Is)" | tee -a "$LOG"
if ! command -v vastai >/dev/null 2>&1; then
  python3 -m pip install --quiet vastai >>"$LOG" 2>&1 || pip install --quiet vastai >>"$LOG" 2>&1
fi
set +e
bash -lc {shlex.quote(job_cmd)} 2>&1 | tee -a "$LOG"
status=${{PIPESTATUS[0]}}
set -e
printf '{{"finished_at":"%s","exit_code":%s}}\n' "$(date -Is)" "$status" > "$STATUS"
echo "[vastai-scheduler $(TZ=Asia/Shanghai date '+%Y-%m-%dT%H:%M:%S%z')] job exited with $status at $(date -Is)" | tee -a "$LOG"
if {destroy_condition}; then
  echo "[vastai-scheduler $(TZ=Asia/Shanghai date '+%Y-%m-%dT%H:%M:%S%z')] destroying instance ${{CONTAINER_ID:-unknown}}" | tee -a "$LOG"
  vastai destroy instance "$CONTAINER_ID" --api-key "$CONTAINER_API_KEY" >>"$LOG" 2>&1
else
  echo "[vastai-scheduler $(TZ=Asia/Shanghai date '+%Y-%m-%dT%H:%M:%S%z')] leaving failed instance running for debugging" | tee -a "$LOG"
fi
"""


def print_estimate(config: SchedulerConfig, rows: list[dict[str, Any]]) -> dict[str, Any]:
    chosen = choose_offer(rows, config)
    payload = {
        "generated_at": now(),
        "query": build_query(config),
        "runtime_hours": config.runtime_hours,
        "disk_gb": config.disk_gb,
        "upload_gb": config.upload_gb,
        "download_gb": config.download_gb,
        "avoid_countries": config.avoid_countries,
        "offer_type": config.offer_type,
        "chosen_offer": summarize_offer(chosen, config) if chosen else None,
        "offers": [summarize_offer(row, config) for row in rows],
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def create_instance(
    offer_id: int,
    image: str,
    disk_gb: float,
    label: str,
    onstart_cmd: str,
    use_ssh: bool,
    direct: bool,
    bid_price: float | None,
    env_vars: dict[str, str] | None = None,
) -> dict[str, Any]:
    args = [
        "create",
        "instance",
        str(offer_id),
        "--image",
        image,
        "--disk",
        str(disk_gb),
        "--label",
        label,
        "--onstart-cmd",
        onstart_cmd,
        "--raw",
    ]
    if use_ssh:
        args.append("--ssh")
    if direct:
        args.append("--direct")
    if bid_price is not None:
        args.extend(["--bid_price", str(bid_price)])
    if env_vars:
        # VastAI --env takes a single Docker-style string: "-e K1=V1 -e K2=V2"
        env_str = " ".join(f"-e {k}={v}" for k, v in env_vars.items())
        args.extend(["--env", env_str])
    code, output = run_vastai(args)
    if code != 0:
        raise RuntimeError(f"vastai create instance failed:\n{redact_sensitive(output)}")
    if output.lower().startswith("failed with error"):
        raise RuntimeError(f"vastai create instance failed:\n{redact_sensitive(output)}")
    try:
        parsed = json.loads(output.replace("'", '"'))
    except json.JSONDecodeError:
        try:
            parsed = ast.literal_eval(output)
        except (SyntaxError, ValueError):
            return {"raw": output}
    if not isinstance(parsed, dict):
        return {"raw": output}
    if parsed.get("success") is False or "error" in parsed:
        contract_id = parsed.get("new_contract")
        if contract_id:
            run_vastai(["destroy", "instance", str(contract_id), "--raw"])
        raise RuntimeError(f"vastai create instance failed; partial contract {contract_id or 'none'} destroyed:\n{redact_sensitive(output)}")
    return parsed


def monitor_cleanup(instance_id: int, timeout_minutes: float, poll_seconds: float) -> dict[str, Any]:
    time.sleep(5)  # Brief settle so the instance shows up in 'show instances'; short jobs may already be gone.
    deadline = time.time() + timeout_minutes * 60
    last_logs = ""
    saw_job_exit = False
    while time.time() < deadline:
        if not instance_exists(instance_id):
            return {"instance_id": instance_id, "gone": True, "local_destroyed": False, "saw_job_exit": saw_job_exit}
        last_logs = instance_logs(instance_id)
        if "[vastai-scheduler] job exited" in last_logs:
            saw_job_exit = True
            time.sleep(min(poll_seconds, 10))
            if instance_exists(instance_id):
                run_vastai(["destroy", "instance", str(instance_id), "--raw"])
                time.sleep(5)
                return {
                    "instance_id": instance_id,
                    "gone": not instance_exists(instance_id),
                    "local_destroyed": True,
                    "saw_job_exit": True,
                }
        time.sleep(poll_seconds)
    return {
        "instance_id": instance_id,
        "gone": not instance_exists(instance_id),
        "local_destroyed": False,
        "saw_job_exit": saw_job_exit,
        "timeout": True,
        "last_log_tail": "\n".join(last_logs.splitlines()[-20:]),
    }


def build_probe_onstart(job_cmd: str, duration_seconds: int) -> str:
    """Build an on-start bash script that runs job_cmd for duration_seconds, samples hardware
    metrics, and emits a structured [vastai-scheduler probe-metrics {...}] log line."""
    escaped = shlex.quote(job_cmd)
    return f"""#!/usr/bin/env bash
set -uo pipefail
export DEBIAN_FRONTEND=noninteractive
mkdir -p /workspace/vastai-job
LOG=/workspace/vastai-job/job.log
echo "[vastai-scheduler probe-start duration={duration_seconds}s] at $(date -Is)" | tee -a "$LOG"
if ! command -v vastai >/dev/null 2>&1; then
  python3 -m pip install --quiet vastai >>"$LOG" 2>&1 || pip install --quiet vastai >>"$LOG" 2>&1
fi

# GPU continuous sampling via nvidia-smi (one line every 5 s)
GPU_CSV=/workspace/vastai-job/gpu_samples.csv
nvidia-smi --query-gpu=utilization.gpu,utilization.memory,memory.used,memory.total,temperature.gpu \\
  --format=csv,noheader,nounits -l 5 > "$GPU_CSV" 2>/dev/null &
GPU_PID=$!

# Baseline CPU snapshot
head -1 /proc/stat > /tmp/vs_cpu_start.txt

# Run the job for at most {duration_seconds} seconds
set +e
timeout {duration_seconds} bash -lc {escaped} >>"$LOG" 2>&1
JOB_EXIT=$?
export JOB_EXIT
set -e

# Stop GPU sampler
kill "$GPU_PID" 2>/dev/null || true
wait "$GPU_PID" 2>/dev/null || true

# End-state snapshots
head -1 /proc/stat > /tmp/vs_cpu_end.txt
cp /proc/meminfo /tmp/vs_meminfo_end.txt

# Decode and run the embedded metrics script
export PROBE_DURATION={duration_seconds}
echo '{_PROBE_METRICS_B64}' | base64 -d | python3 | tee -a "$LOG"

echo "[vastai-scheduler] job exited at $(date -Is)" | tee -a "$LOG"
vastai destroy instance "$CONTAINER_ID" --api-key "$CONTAINER_API_KEY" >>"$LOG" 2>&1 || true
"""


def extract_probe_metrics(log_text: str) -> dict[str, Any] | None:
    """Extract the last probe-metrics JSON object from a log string, if present."""
    for line in reversed(log_text.splitlines()):
        m = re.search(r"\[vastai-scheduler probe-metrics (\{.*\})\]", line)
        if m:
            try:
                return json.loads(m.group(1))
            except json.JSONDecodeError:
                pass
    return None


def monitor_probe(instance_id: int, timeout_minutes: float, poll_seconds: float) -> dict[str, Any]:
    """Like monitor_cleanup but also captures probe-metrics from instance logs."""
    time.sleep(5)
    deadline = time.time() + timeout_minutes * 60
    last_logs = ""
    probe_metrics: dict[str, Any] | None = None
    saw_job_exit = False
    while time.time() < deadline:
        if not instance_exists(instance_id):
            return {
                "instance_id": instance_id,
                "gone": True,
                "local_destroyed": False,
                "saw_job_exit": saw_job_exit,
                "probe_metrics": probe_metrics,
            }
        last_logs = instance_logs(instance_id, tail=500)
        if probe_metrics is None:
            probe_metrics = extract_probe_metrics(last_logs)
        if "[vastai-scheduler] job exited" in last_logs:
            saw_job_exit = True
            if probe_metrics is None:
                probe_metrics = extract_probe_metrics(last_logs)
            time.sleep(min(poll_seconds, 10))
            if instance_exists(instance_id):
                run_vastai(["destroy", "instance", str(instance_id), "--raw"])
                time.sleep(5)
            return {
                "instance_id": instance_id,
                "gone": not instance_exists(instance_id),
                "local_destroyed": True,
                "saw_job_exit": True,
                "probe_metrics": probe_metrics,
            }
        time.sleep(poll_seconds)
    return {
        "instance_id": instance_id,
        "gone": not instance_exists(instance_id),
        "local_destroyed": False,
        "saw_job_exit": saw_job_exit,
        "probe_metrics": probe_metrics,
        "timeout": True,
        "last_log_tail": "\n".join(last_logs.splitlines()[-20:]),
    }



def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--runtime-hours", type=float, required=True, help="Expected task wall-clock runtime.")
    parser.add_argument("--disk-gb", type=float, default=40.0, help="Disk to request and price, in GiB.")
    parser.add_argument("--upload-gb", type=float, default=0.0, help="Estimated upload from instance, in GB.")
    parser.add_argument("--download-gb", type=float, default=0.0, help="Estimated download to instance, in GB.")
    parser.add_argument("--gpu", default="", help="Comma-separated GPU names, e.g. 'RTX 4090,RTX 3090'.")
    parser.add_argument("--num-gpus", type=int, default=1)
    parser.add_argument("--min-gpu-ram-gb", type=float, default=None)
    parser.add_argument("--min-cpu-cores", type=float, default=None, help="Minimum effective CPU cores.")
    parser.add_argument("--min-cpu-ram-gb", type=float, default=None)
    parser.add_argument("--min-reliability", type=float, default=0.98)
    parser.add_argument(
        "--max-hourly-cost",
        type=float,
        default=0.10,
        help="Hard cap on instance hourly cost in USD/hr. Offers above this are excluded. Default: $0.10/hr.",
    )
    parser.add_argument("--max-storage-cost", type=float, default=0.20, help="Max $/GB/month.")
    parser.add_argument("--max-inet-up-cost", type=float, default=0.02, help="Max $/GB.")
    parser.add_argument("--max-inet-down-cost", type=float, default=0.02, help="Max $/GB.")
    parser.add_argument(
        "--avoid-countries",
        default=DEFAULT_AVOID_COUNTRIES,
        help="Comma-separated ISO country codes to avoid. Default avoids China and United States.",
    )
    parser.add_argument("--extra-query", default=None, help="Additional Vast.ai query expression.")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--order", default="dph", help="Vast.ai search order.")
    parser.add_argument("--offer-type", choices=["on-demand", "bid", "reserved"], default="on-demand")


def config_from_args(args: argparse.Namespace) -> SchedulerConfig:
    return SchedulerConfig(
        runtime_hours=args.runtime_hours,
        disk_gb=args.disk_gb,
        upload_gb=args.upload_gb,
        download_gb=args.download_gb,
        gpu_names=parse_csv(args.gpu),
        num_gpus=args.num_gpus,
        min_gpu_ram_gb=args.min_gpu_ram_gb,
        min_cpu_cores=args.min_cpu_cores,
        min_cpu_ram_gb=args.min_cpu_ram_gb,
        min_reliability=args.min_reliability,
        max_hourly_cost=args.max_hourly_cost,
        max_storage_cost=args.max_storage_cost,
        max_inet_up_cost=args.max_inet_up_cost,
        max_inet_down_cost=args.max_inet_down_cost,
        avoid_countries=parse_csv(args.avoid_countries),
        extra_query=args.extra_query,
        limit=args.limit,
        order=args.order,
        offer_type=args.offer_type,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Search, estimate, and launch cost-aware Vast.ai jobs.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    estimate_parser = subparsers.add_parser("estimate", help="Search offers and estimate task cost.")
    add_common_args(estimate_parser)
    estimate_parser.add_argument("--save-json", type=Path, default=None)

    launch_parser = subparsers.add_parser("launch", help="Rent the lowest-cost matching offer and run a job.")
    add_common_args(launch_parser)
    launch_parser.add_argument("--job-cmd", required=True, help="Command to run inside the Vast.ai container.")
    launch_parser.add_argument("--image", default=DEFAULT_IMAGE)
    launch_parser.add_argument("--label", default=f"vastai-scheduler-{now()}")
    launch_parser.add_argument("--ssh", action="store_true", help="Enable SSH injection.")
    launch_parser.add_argument("--no-direct", action="store_true", help="Disable direct networking.")
    launch_parser.add_argument("--destroy-on-success-only", action="store_true")
    launch_parser.add_argument("--no-monitor-cleanup", action="store_true", help="Return immediately after create instead of waiting for job exit and destroying locally if needed.")
    launch_parser.add_argument("--cleanup-timeout-minutes", type=float, default=30.0)
    launch_parser.add_argument("--cleanup-poll-seconds", type=float, default=15.0)
    launch_parser.add_argument("--yes", action="store_true", help="Actually create the instance.")
    launch_parser.add_argument("--save-json", type=Path, default=None)
    launch_parser.add_argument(
        "--pass-env",
        default="",
        help=(
            "Comma-separated env var names to read from the local environment and inject into "
            "the container (e.g. WANDB_API_KEY,GITHUB_TOKEN). Values come from your shell — "
            "never hardcode them here. Vars not set locally are skipped with a warning."
        ),
    )

    probe_parser = subparsers.add_parser(
        "probe",
        help=(
            "Run a series of short probe jobs to measure actual GPU/CPU/memory utilisation "
            "before committing to a long run."
        ),
    )
    add_common_args(probe_parser)
    probe_parser.add_argument("--job-cmd", required=True, help="Command to benchmark inside each probe instance.")
    probe_parser.add_argument(
        "--probe-durations",
        default="30,40,50",
        help="Comma-separated probe durations in seconds (default: '30,40,50').",
    )
    probe_parser.add_argument("--image", default=DEFAULT_IMAGE)
    probe_parser.add_argument("--label", default=f"vastai-probe-{now()}")
    probe_parser.add_argument("--ssh", action="store_true", help="Enable SSH injection.")
    probe_parser.add_argument("--no-direct", action="store_true", help="Disable direct networking.")
    probe_parser.add_argument("--cleanup-timeout-minutes", type=float, default=10.0)
    probe_parser.add_argument("--cleanup-poll-seconds", type=float, default=10.0)
    probe_parser.add_argument("--yes", action="store_true", help="Actually rent and run probe instances.")
    probe_parser.add_argument("--save-json", type=Path, default=None)
    probe_parser.add_argument(
        "--pass-env",
        default="",
        help="Comma-separated env var names to inject into probe containers.",
    )

    args = parser.parse_args()
    config = config_from_args(args)
    rows = search_offers(config)
    estimate = print_estimate(config, rows)
    if args.save_json:
        args.save_json.write_text(json.dumps(estimate, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if args.command == "estimate":
        return 0 if rows else 1

    # -----------------------------------------------------------------------
    # probe: rent a series of short instances and collect hardware metrics
    # -----------------------------------------------------------------------
    if args.command == "probe":
        probe_durations = [int(d.strip()) for d in args.probe_durations.split(",") if d.strip().isdigit()]
        if not probe_durations:
            print("Error: --probe-durations must be a comma-separated list of integers, e.g. '30,40,50'.", file=sys.stderr)
            return 1

        env_vars: dict[str, str] = {}
        for var_name in parse_csv(getattr(args, "pass_env", "")):
            value = os.environ.get(var_name)
            if value is None:
                print(f"Warning: --pass-env variable {var_name!r} not set locally; skipping.", file=sys.stderr)
            else:
                env_vars[var_name] = value

        probe_results = []
        for duration in probe_durations:
            print(f"\n=== Probe run: {duration}s ===", file=sys.stderr)
            chosen = choose_offer(rows, config)
            if not chosen:
                probe_results.append({"duration_seconds": duration, "error": "no_matching_offers"})
                continue
            offer_summary = summarize_offer(chosen, config)
            if not args.yes:
                probe_results.append({"duration_seconds": duration, "dry_run": True, "offer": offer_summary})
                continue
            offer_id = int(chosen.get("id") or chosen.get("ask_contract_id"))
            if args.ssh:
                ensure_ssh_key_registered()
            try:
                created = create_instance(
                    offer_id=offer_id,
                    image=args.image,
                    disk_gb=config.disk_gb,
                    label=f"{args.label}-{duration}s",
                    onstart_cmd=build_probe_onstart(args.job_cmd, duration),
                    use_ssh=args.ssh,
                    direct=not args.no_direct,
                    bid_price=suggested_bid_price(chosen) if config.offer_type == "bid" else None,
                    env_vars=env_vars or None,
                )
            except RuntimeError as exc:
                probe_results.append({"duration_seconds": duration, "error": str(exc)})
                continue
            contract_id = created.get("new_contract")
            if not contract_id:
                probe_results.append({
                    "duration_seconds": duration,
                    "error": "no_contract_id",
                    "create_response": redact_mapping(created),
                })
                continue
            cleanup = monitor_probe(int(contract_id), args.cleanup_timeout_minutes, args.cleanup_poll_seconds)
            probe_results.append({
                "duration_seconds": duration,
                "offer": offer_summary,
                "metrics": cleanup.pop("probe_metrics", None),
                "cleanup": cleanup,
            })

        result = {"generated_at": now(), "probe_series": probe_results}
        if args.save_json:
            args.save_json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0

    # -----------------------------------------------------------------------
    # launch
    # -----------------------------------------------------------------------
    chosen = choose_offer(rows, config)
    if not chosen:
        print("No matching offers found; nothing to launch.", file=sys.stderr)
        return 1

    offer_id = int(chosen.get("id") or chosen.get("ask_contract_id"))
    onstart = build_onstart(args.job_cmd, destroy_on_success_only=args.destroy_on_success_only)
    if not args.yes:
        print(
            "\nDry run only. Re-run with --yes to rent this offer. "
            "The injected on-start script will destroy the instance after the job exits.",
            file=sys.stderr,
        )
        return 0

    if args.ssh:
        ensure_ssh_key_registered()

    env_vars = {}
    for var_name in parse_csv(getattr(args, "pass_env", "")):
        value = os.environ.get(var_name)
        if value is None:
            print(
                f"Warning: --pass-env variable {var_name!r} is not set in the local environment; skipping.",
                file=sys.stderr,
            )
        else:
            env_vars[var_name] = value

    created = create_instance(
        offer_id=offer_id,
        image=args.image,
        disk_gb=config.disk_gb,
        label=args.label,
        onstart_cmd=onstart,
        use_ssh=args.ssh,
        direct=not args.no_direct,
        bid_price=suggested_bid_price(chosen) if config.offer_type == "bid" else None,
        env_vars=env_vars or None,
    )
    result = {"created_at": now(), "offer": estimate["chosen_offer"], "create_response": redact_mapping(created)}
    contract_id = created.get("new_contract")
    if contract_id and not args.no_monitor_cleanup:
        result["cleanup"] = monitor_cleanup(int(contract_id), args.cleanup_timeout_minutes, args.cleanup_poll_seconds)
    if args.save_json:
        args.save_json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
