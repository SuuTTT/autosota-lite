#!/usr/bin/env python3
"""Send AutoSOTA iteration notifications to Slack via Incoming Webhook.

Reads SLACK_WEBHOOK_URL from the environment (or .env.local). Builds a short
status message in the shape described in SKILL.md and POSTs it to Slack.
Use --dry-run to render the payload without sending.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


def _load_env_local() -> None:
    for candidate in (Path.cwd() / ".env.local", Path("/workspace/autosota-lite/.env.local")):
        if candidate.exists():
            for line in candidate.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, _, v = line.partition("=")
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if k and k not in os.environ:
                    os.environ[k] = v
            return


def build_message(args: argparse.Namespace) -> str:
    lines = [
        f"*AutoSOTA update*: {args.project}",
        f"Status: `{args.status}`",
    ]
    if args.idea:
        lines.append(f"Idea: {args.idea}")
    if args.metric:
        lines.append(f"Metric: {args.metric}")
    if args.validity:
        lines.append(f"Validity: `{args.validity}`")
    if args.artifacts:
        lines.append(f"Artifacts: {args.artifacts}")
    if args.next_step:
        lines.append(f"Next: {args.next_step}")
    return "\n".join(lines)


def post_to_slack(webhook_url: str, text: str, channel: str | None) -> tuple[int, str]:
    payload: dict[str, object] = {"text": text}
    if channel:
        payload["channel"] = channel
    req = urllib.request.Request(
        webhook_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", errors="replace") if exc.fp else str(exc)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, help="Project / run identifier (e.g. autosota-research/run-2026-04-30).")
    parser.add_argument(
        "--status",
        required=True,
        choices=["complete", "failed", "needs-review", "budget-reached", "started"],
    )
    parser.add_argument("--idea", default="", help="Idea id and short name from idea_library.md.")
    parser.add_argument("--metric", default="", help="Baseline → current, or failure reason.")
    parser.add_argument("--validity", default="", choices=["", "valid", "invalid", "unknown"])
    parser.add_argument("--artifacts", default="", help="Log path, WandB URL, PR or commit.")
    parser.add_argument("--next-step", default="", help="One requested action or next planned step.")
    parser.add_argument("--channel", default=None, help="Override webhook default channel (e.g. '#autosota').")
    parser.add_argument("--dry-run", action="store_true", help="Print the payload without sending.")
    args = parser.parse_args(argv)

    _load_env_local()
    text = build_message(args)

    if args.dry_run:
        print("[dry-run] would POST to Slack:")
        print(text)
        return 0

    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        print("ERROR: SLACK_WEBHOOK_URL not set (env var or .env.local).", file=sys.stderr)
        print("See SKILL.md for webhook setup steps.", file=sys.stderr)
        return 1

    status, body = post_to_slack(webhook_url, text, args.channel)
    if status == 200 and body.strip().lower() == "ok":
        print("[notifier] posted to Slack.")
        return 0
    print(f"[notifier] FAILED — HTTP {status}: {body}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
