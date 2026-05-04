# Skill: util-github-git-push

Automatically publish agent-written papers to Overleaf and blog posts to your GitHub blog, with secure credential management and KaTeX formula validation.

---

## Quick Start

### Publish Blog Post

```bash
# Load credentials
set -a && source .env.local && set +a
export GITHUB_TOKEN=$(gcloud secrets versions access latest --secret=github-temp-token)

# Publish to your blog
python plugins/autosota-lite/skills/util-key-manager/github_git_push.py \
  << 'EOF'
import os
from github_git_push import publish_blog_post

publish_blog_post(
    title="My Research Findings",
    content="## Results\n\nOur method achieves 95% accuracy.",
    tags=["research", "sota"],
    github_token=os.getenv("GITHUB_TOKEN"),
    blog_repo="https://github.com/SuuTTT/suuttt.github.io.git"
)
EOF
```

### Publish Paper to Overleaf

```bash
from github_git_push import publish_paper_to_overleaf

publish_paper_to_overleaf(
    title="Fast RL with Structural Information",
    content=r"\documentclass{article}...",
    overleaf_token=os.getenv("OVERLEAF_API_TOKEN")
)
```

---

## Architecture

### Three-Tier Credential Strategy

```
Local Machine (Persistent)
  ↓
  SSH key (~/.ssh/github_rsa)
  ↓
  Stored in GCP Secret Manager (encrypted)

Rented GPU Instance (Ephemeral)
  ↓
  Temporary GitHub token (30 min expiry)
  ↓
  Stored in GCP Secret Manager
  ↓
  Auto-revoke after job completes
```

### Security Model

| Environment | Auth | Expiry | Risk |
|---|---|---|---|
| Local | SSH key | Never | Low (machine-specific) |
| GPU rental | Temp token | 30 min | Very low (ephemeral) |
| CI/CD | GitHub App | 1 hour | Minimal (auto-generated) |

---

## API Reference

### `publish_blog_post()`

**Function signature:**
```python
def publish_blog_post(
    title: str,
    content: str,
    tags: list[str],
    github_token: str,
    blog_repo: str = "https://github.com/SuuTTT/suuttt.github.io.git",
    auth_type: str = "token",
    description: Optional[str] = None,
    date: Optional[str] = None,
    dry_run: bool = False
) -> dict
```

**Parameters:**
- `title` (str): Blog post title
- `content` (str): Markdown content (without frontmatter)
- `tags` (list[str]): Post tags for categorization
- `github_token` (str): GitHub personal access token or temporary token
- `blog_repo` (str): GitHub blog repository URL (default: your blog)
- `auth_type` (str): "token" or "ssh"
- `description` (str, optional): Brief post summary
- `date` (str, optional): Post date (YYYY-MM-DD, defaults to today)
- `dry_run` (bool): If True, validate without pushing

**Returns:**
```python
{
    "status": "success" | "error",
    "message": "Human-readable status",
    "commit": "Short commit hash",
    "dry_run": True | False
}
```

**Example:**
```python
result = publish_blog_post(
    title="GPU Scheduling Best Practices",
    content="## Overview\n\nWhen renting GPUs...",
    tags=["gpu", "optimization", "vast-ai"],
    github_token=os.getenv("GITHUB_TOKEN")
)

if result["status"] == "success":
    print(f"✅ Published: {result['commit']}")
```

### `publish_paper_to_overleaf()`

**Function signature:**
```python
def publish_paper_to_overleaf(
    title: str,
    content: str,
    overleaf_token: str,
    paper_type: str = "arxiv",
    dry_run: bool = False
) -> dict
```

**Parameters:**
- `title` (str): Paper title
- `content` (str): LaTeX content
- `overleaf_token` (str): Overleaf API token
- `paper_type` (str): "arxiv", "conference", or "workshop"
- `dry_run` (bool): If True, validate without creating

**Returns:**
```python
{
    "status": "success" | "error",
    "project_id": "overleaf_project_id",
    "url": "https://www.overleaf.com/project/..."
}
```

### `validate_formulas()`

**Function signature:**
```python
def validate_formulas(content: str) -> list[str]
```

**Purpose:** Check for common KaTeX formula rendering issues

**Returns:** List of warnings (empty if valid)

**Example:**
```python
from github_git_push import validate_formulas

warnings = validate_formulas(content)
if warnings:
    print("⚠️ Formula issues found:")
    for warning in warnings:
        print(f"  {warning}")
```

### `setup_git_auth()`

**Function signature:**
```python
def setup_git_auth(
    auth_type: Literal["ssh", "token"],
    ssh_key_path: Optional[str] = None,
    github_token: Optional[str] = None
) -> None
```

**Purpose:** Configure git authentication for current session

**Parameters:**
- `auth_type`: "ssh" (local machine) or "token" (rented instance)
- `ssh_key_path`: Path to SSH private key (required if auth_type="ssh")
- `github_token`: GitHub token (required if auth_type="token")

---

## KaTeX Formula Support

### Automatic KaTeX Shortcode

The skill automatically adds `{{< katex >}}` shortcode if missing:

```python
content = "Some markdown with formulas"
# Result: "{{< katex >}}\n\nSome markdown with formulas"
```

### Formula Validation

The skill validates:
- ✅ Matched `$$` delimiters for block equations
- ✅ Proper inline formula syntax (`$...$`)
- ✅ No mixing of delimiters (`\(...\)` vs `$...$`)
- ✅ Skips validation in code blocks and tables

### Common Issues Fixed

**Before:** Raw formula text on blog
**After:** Rendered mathematical expressions via KaTeX

**Issue:** Unmatched delimiters
```markdown
❌ $x + y$$ renders incorrectly
✅ $x + y$ renders correctly
```

**Issue:** Mixed delimiters
```markdown
❌ \(x = y\) doesn't work in KaTeX
✅ $x = y$ works correctly
```

---

## Integration with Workflows

### `write_paper_from_idea` Workflow

```yaml
stages:
  # ... existing write stage ...
  
  - id: publish_overleaf
    name: "Publish to Overleaf"
    skill: util-github-git-push
    inputs:
      title: ${stage_write.outputs.paper_title}
      content: ${stage_write.outputs.paper_latex}
      overleaf_token: ${secrets.OVERLEAF_API_TOKEN}
      paper_type: "arxiv"
    timeout: 2 minutes
  
  - id: publish_blog
    name: "Announce on Blog"
    skill: util-github-git-push
    inputs:
      title: "New Paper: ${stage_write.outputs.paper_title}"
      content: "📄 Check out our latest paper on Overleaf..."
      tags: ["paper", "research"]
      github_token: ${secrets.GITHUB_TOKEN}
    timeout: 2 minutes
```

### Command-line Usage

```bash
sotaflow run write_paper_from_idea \
  --idea "Combine PPO with entropy regularization" \
  --publish-blog true \
  --publish-overleaf true
```

---

## Credential Management

### Local Machine Setup

```bash
# 1. Generate SSH key (one-time)
ssh-keygen -t ed25519 -f ~/.ssh/github_rsa -N ""

# 2. Store in GCP Secret Manager
gcloud secrets create github-ssh-private-key \
  --data-file=~/.ssh/github_rsa \
  --project=projectrl-485417

# 3. Add public key to GitHub
cat ~/.ssh/github_rsa.pub
# → Copy to GitHub Settings → SSH Keys
```

### Rented Instance Setup

```bash
# 1. Create temporary token on GitHub
# Scopes: repo, workflow
# Expiry: 30 days
# Token: ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 2. Store in GCP Secret Manager
gcloud secrets create github-temp-token --data-file=- --project=projectrl-485417
# (paste token)

# 3. Load in instance
export GITHUB_TOKEN=$(gcloud secrets versions access latest --secret=github-temp-token)

# 4. Token auto-expires, instance destroyed → no manual cleanup needed
```

### Overleaf Token

```bash
# 1. Get token from Overleaf Settings → Account → API
# Token: ol_xxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 2. Store in GCP
gcloud secrets create overleaf-api-token --data-file=- --project=projectrl-485417

# 3. Load in script
export OVERLEAF_TOKEN=$(gcloud secrets versions access latest --secret=overleaf-api-token)
```

---

## Security Best Practices

### ✅ DO

- Use SSH keys for local machines (persistent, tied to device)
- Use temporary tokens for ephemeral hardware (30 min expiry)
- Store all credentials in GCP Secret Manager (encrypted, auditable)
- Rotate tokens regularly (monthly for long-lived PATs)
- Use GitHub Apps for production deployments (auto-generated tokens)

### ❌ DON'T

- Hardcode tokens in code or config files
- Store SSH keys on rented instances
- Commit secrets to git (even in .gitignore)
- Use long-lived PATs for CI/CD
- Share credentials between environments

---

## Examples

### Example 1: Local Blog Post Publishing

```bash
#!/bin/bash
set -a && source .env.local && set +a

python3 << 'EOF'
import os
from github_git_push import publish_blog_post

content = """
## My Latest Research

The key insight is:

$$
f(x) = \sum_{i=1}^n x_i^2
$$

This is proven in our paper.
"""

result = publish_blog_post(
    title="Key Insights from Latest Research",
    content=content,
    tags=["research", "sota"],
    github_token=os.getenv("GITHUB_TOKEN"),
    description="Summary of our latest findings"
)

print(f"✅ Published: {result['commit']}")
EOF
```

### Example 2: GPU Instance Auto-Publish

```bash
#!/bin/bash
# Inside Vast.ai instance after training

export GITHUB_TOKEN=$(gcloud secrets versions access latest --secret=github-temp-token)

python3 << 'EOF'
import os
import json
from github_git_push import publish_blog_post

# Load training results
with open("results.json") as f:
    results = json.load(f)

# Publish summary
publish_blog_post(
    title=f"GPU Training Results - {results['date']}",
    content=f"""
## Training on Vast.ai GPU

- **Loss:** {results['final_loss']:.6f}
- **Speed:** {results['steps_per_sec']} steps/sec
- **GPU Util:** {results['gpu_util']}%

Performance metrics:
$$
L_{{final}} = {results['final_loss']:.6f}
$$
""",
    tags=["gpu", "training", "vast-ai"],
    github_token=os.getenv("GITHUB_TOKEN")
)
EOF

# Instance destroyed → token expires automatically
```

### Example 3: Dry-Run Testing

```bash
python3 << 'EOF'
from github_git_push import publish_blog_post

# Test without pushing
result = publish_blog_post(
    title="Test Post",
    content="This is a test.",
    tags=["test"],
    github_token="ghp_test_token",
    dry_run=True  # No actual push
)

print(f"Would create: {result['message']}")
# Output: "Dry-run successful (would push abc1234)"
EOF
```

---

## Troubleshooting

### Issue: "Permission denied (publickey)"

**Symptom:** SSH push fails with permission error

**Solution:**
- Check SSH key permissions: `chmod 600 ~/.ssh/github_rsa`
- Verify key is added to GitHub Settings → SSH Keys
- Test connection: `ssh -T git@github.com`

### Issue: Formula rendering fails on blog

**Symptom:** Math shows as raw `$$...$$` text

**Solution:**
1. Verify `math: true` in frontmatter
2. Check `{{< katex >}}` shortcode is present
3. Run validation: `validate_formulas(content)`
4. Fix unmatched `$$` delimiters

### Issue: Overleaf API returns 401

**Symptom:** "Unauthorized" error when publishing

**Solution:**
- Verify token isn't expired (Overleaf → Settings → API)
- Check token has correct scopes (docs, write)
- Test token: `curl -H "Authorization: Bearer $OVERLEAF_TOKEN" https://api.overleaf.com/api/v0/user`

### Issue: GitHub token expired

**Symptom:** "Bad credentials" error

**Solution:**
- Create new token: https://github.com/settings/tokens/new
- For rented instances: Use temporary tokens with 30-day expiry
- For local: Create personal token with 60-90 day expiry

---

## Metrics & Monitoring

The skill tracks:
- `publish_attempts` (total posts attempted)
- `publish_success` (successful pushes)
- `formula_warnings` (KaTeX validation issues)
- `auth_failures` (credential problems)
- `sync_time` (seconds to complete)

Monitor via:
```bash
python plugins/autosota-lite/skills/util-key-manager/github_git_push.py metrics
```

---

## Related Skills

- `util-key-manager` — Credential management and storage
- `sota-workflow-orchestrator` — Chain skills together
- `util-notifier` — Send Slack/email notifications
- `paper-writer` — Generate paper content

---

## Testing

Run the test script:
```bash
python plugins/autosota-lite/skills/util-key-manager/github_git_push.py test
```

This validates:
- ✅ KaTeX formula rendering
- ✅ GitHub authentication
- ✅ Overleaf API connectivity
- ✅ Dry-run functionality

---

## Next Steps

1. **Configure credentials** (GitHub token, Overleaf token)
2. **Test locally** with dry-run
3. **Integrate into workflows** (write_paper_from_idea)
4. **Deploy to GPU instances** for auto-publish on training completion

See [GITHUB_AUTH_SETUP.md](GITHUB_AUTH_SETUP.md) for detailed credential configuration.
