#!/usr/bin/env python3
"""Verify that all required service credentials are configured.

Run before launching any job that talks to WandB, GitHub, or Vast.ai.
Exit code 0 = all checked services are ready; 1 = something is missing.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def _load_env_local() -> None:
    """Source .env.local from the workspace root into the current process."""
    for candidate in (
        Path(".env.local"),
        Path(__file__).parents[5] / ".env.local",  # repo root
    ):
        if candidate.exists():
            print(f"[env] Loading {candidate}", file=sys.stderr)
            for line in candidate.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key and key not in os.environ:
                    os.environ[key] = value
            break


def _redact(value: str | None, show_chars: int = 6) -> str:
    if not value:
        return "(empty)"
    visible = value[:show_chars]
    return f"{visible}{'*' * max(0, len(value) - show_chars)}"


def check_wandb() -> bool:
    key = os.getenv("WANDB_API_KEY")
    if not key:
        netrc = Path.home() / ".netrc"
        if netrc.exists() and "api.wandb.ai" in netrc.read_text():
            print("[WandB] OK — credentials in ~/.netrc (skipping live API check)")
            return True
        print("[WandB] MISSING")
        print("  Fix: export WANDB_API_KEY=<key>  or add to .env.local  or run: wandb login")
        return False
    # Live-validate the key against the WandB GraphQL API.
    import json as _json
    import urllib.error
    import urllib.request

    try:
        req = urllib.request.Request(
            "https://api.wandb.ai/graphql",
            data=b'{"query":"{ viewer { username entity } }"}',
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = _json.loads(resp.read().decode())
        viewer = (data.get("data") or {}).get("viewer") or {}
        username = viewer.get("username")
        entity = viewer.get("entity")
        if not username:
            print(f"[WandB] KEY SET but API returned no user — key likely invalid")
            return False
        print(f"[WandB] OK — WANDB_API_KEY={_redact(key)} (user: {username}, entity: {entity})")
        return True
    except urllib.error.HTTPError as exc:
        print(f"[WandB] KEY SET but API rejected it (HTTP {exc.code}) — likely revoked or invalid")
        return False
    except Exception as exc:
        print(f"[WandB] KEY SET but live check failed ({type(exc).__name__}: {exc}) — assuming OK")
        return True


def check_vastai() -> bool:
    key_file = Path.home() / ".vast_api_key"
    env_key = os.getenv("VASTAI_API_KEY")
    if key_file.exists():
        key = key_file.read_text().strip()
        if key:
            print(f"[VastAI] OK — ~/.vast_api_key={_redact(key)}")
            return True
    if env_key:
        print(f"[VastAI] OK — VASTAI_API_KEY={_redact(env_key)}")
        return True
    print("[VastAI] MISSING")
    print("  Fix: vastai set api-key <key>   (stores to ~/.vast_api_key)")
    return False


def check_github() -> bool:
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if not token:
        gh_file = Path.home() / ".github_token"
        if gh_file.exists():
            token = gh_file.read_text().strip()
    if token:
        print(f"[GitHub] OK — token={_redact(token)}")
        return True
    try:
        result = subprocess.run(
            ["gh", "auth", "status"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            print("[GitHub] OK — gh CLI authenticated")
            return True
    except FileNotFoundError:
        pass
    print("[GitHub] MISSING (optional for WandB-only jobs)")
    print("  Fix: export GITHUB_TOKEN=<token>  or run: gh auth login")
    return False


def check_openai() -> bool:
    key = os.getenv("OPENAI_API_KEY")
    if key:
        print(f"[OpenAI] OK — OPENAI_API_KEY={_redact(key)}")
        return True
    print("[OpenAI] not set (optional — needed for ideator Deep Research)")
    return True  # not required for most workflows


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--services",
        default="wandb,vastai,github",
        help="Comma-separated services to check (default: wandb,vastai,github).",
    )
    parser.add_argument(
        "--load-env-local",
        action="store_true",
        default=True,
        help="Load .env.local before checking (default: true).",
    )
    args = parser.parse_args(argv)

    if args.load_env_local:
        _load_env_local()

    service_checks = {
        "wandb": check_wandb,
        "vastai": check_vastai,
        "github": check_github,
        "openai": check_openai,
    }

    requested = [s.strip().lower() for s in args.services.split(",") if s.strip()]
    results: dict[str, bool] = {}
    for svc in requested:
        fn = service_checks.get(svc)
        if fn is None:
            print(f"[{svc}] unknown service — skipped")
            continue
        try:
            results[svc] = fn()
        except Exception as exc:
            print(f"[{svc}] ERROR — {exc}")
            results[svc] = False

    print()
    failures = [s for s, ok in results.items() if not ok]
    if not failures:
        print("All credentials ready.")
        return 0
    print(f"Missing: {', '.join(failures)}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
