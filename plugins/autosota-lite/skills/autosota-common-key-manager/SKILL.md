---
name: autosota-common-key-manager
description: Manage API keys and service credentials for AutoSOTA workflows, including WandB, GitHub, Vast.ai, Slack, Overleaf, blogs, and publishing tools, without exposing secrets in chat, logs, commands, or committed files.
---

# AutoSOTA Common Key Manager

Use this skill before connecting AutoSOTA runs to external services or when a key, token, or credential path is missing.

## Rules

- Never ask the user to paste private keys or tokens into chat.
- Never commit `.env`, `.env.local`, key files, shell history, service tokens, or generated credential caches.
- Prefer environment variables, service CLIs, OS keychains, or project-local ignored config files.
- Redact secrets in logs and command summaries.
- If a secret was pasted into chat or committed, advise rotation and remove the committed value without repeating it.

## Local Secret Storage (`.env.local`)

Keep service credentials in a single `.env.local` file at the repo root. This file is never committed.

```bash
# .env.local  (gitignored — never commit)
WANDB_API_KEY=your_key_here
GITHUB_TOKEN=your_token_here
OPENAI_API_KEY=your_key_here
```

Source it in your shell session before running any job:

```bash
set -a && source .env.local && set +a
```

Or use `--load-env-local` in `check_keys.py` (it loads the file automatically if it exists).

Always verify `.env.local` is gitignored:

```bash
grep -q '.env.local' .gitignore || echo '.env.local' >> .gitignore
grep -q '.env' .gitignore || echo '.env' >> .gitignore
```

## Service Map

| Service | Primary method | Fallback |
|---------|---------------|---------|
| WandB | `WANDB_API_KEY` env var | `wandb login` → `~/.netrc` |
| GitHub | `GITHUB_TOKEN` env var | `gh auth login` or configured connector |
| Vast.ai | `vastai set api-key` → `~/.vast_api_key` | `VASTAI_API_KEY` env var |
| Slack | Configured Slack connector | Do not store bot tokens in repo |
| Overleaf/blogs | Connector or local CLI auth | Create draft artifact for manual posting |
| OpenAI | `OPENAI_API_KEY` env var | Fallback to browser-based research |

## Verification

Before any job launch, run the bundled checker to confirm credentials are ready:

```bash
python3 /workspace/autosota-lite/plugins/autosota-lite/skills/autosota-common-key-manager/check_keys.py
# Or check specific services only:
python3 check_keys.py --services wandb,vastai
```

Exit code 0 = all ready. Non-zero = something needs attention.

## Injecting Service Keys into Remote Jobs (Vast.ai)

The Vast.ai **account** API key must never appear in `--job-cmd`, `--env`, logs, or chat. Vast.ai handles it internally via `CONTAINER_API_KEY` inside the container.

**Service credentials** (WandB, GitHub, etc.) must be injected explicitly, because the container has no access to your local environment. Use `--pass-env` in the vastai scheduler:

```bash
export WANDB_API_KEY=...   # set locally (or loaded from .env.local)

python3 vastai_scheduler.py launch \
  --job-cmd 'pip install -q wandb && python3 train.py' \
  --pass-env WANDB_API_KEY \
  --runtime-hours 2 \
  --yes
```

`--pass-env` reads the named env vars from your **local** shell and injects them into the container via `vastai create instance --env`. The values never appear in chat or git history — only in Vast.ai's runtime environment for that specific instance.

You can pass multiple vars:

```bash
--pass-env WANDB_API_KEY,GITHUB_TOKEN
```

Any var listed in `--pass-env` that is missing locally will print a warning and be skipped, not silently injected as empty.

## Workflow

1. Identify the service and action: read, write, upload, notify, rent, publish, or sync.
2. Run `check_keys.py --services <services>` to verify credentials without printing secret values.
3. Source `.env.local` if env vars are not already exported.
4. Verify minimum permissions with a harmless read or dry-run when possible.
5. Write only non-secret config to tracked files.
6. Add missing ignored secret paths to `.gitignore` when needed.
7. For remote jobs: use `--pass-env` to forward only the service credentials that the job requires.

## Key Rotation

If a credential is suspected compromised or was accidentally exposed in chat or a commit:

1. Immediately revoke the key in the service dashboard (WandB → Settings → API keys; Vast.ai → Account → API keys).
2. Generate a replacement key.
3. Update `.env.local` (or `vastai set api-key`) with the new key.
4. If it was committed: remove from git history with `git filter-repo` or open a private fork. Do not use `--force-push` to a shared branch without team coordination.
5. Re-run `check_keys.py` to confirm the new key is active.
