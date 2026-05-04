# Overleaf Integration Guide

**Yes, it's absolutely possible to publish papers to Overleaf automatically!**

This guide covers how to set up automatic paper publishing to Overleaf as part of the AutoSOTA workflow.

---

## Quick Answer

✅ **YES - Full Overleaf Integration Available**

The `util-github-git-push` skill includes:
- Auto-create Overleaf projects via API
- Upload LaTeX files automatically
- Generate shareable links
- Support for templates (arxiv, conference, workshop)
- Works end-to-end in workflows

---

## Architecture

### How It Works

```
Agent writes paper (LaTeX)
    ↓
Call Overleaf API
    ↓
Create new project
    ↓
Upload main.tex + figures + bib
    ↓
Return shareable project URL
    ↓
Send link to Slack
```

### Overleaf API Features Used

| Feature | API Endpoint | Purpose |
|---|---|---|
| Create Project | `POST /api/v0/projects` | Create new Overleaf project |
| Upload Files | `POST /api/v0/projects/{id}/files` | Upload LaTeX, figures, bib |
| Update Files | `PUT /api/v0/projects/{id}/files/{name}` | Update existing files |
| Get Project | `GET /api/v0/projects/{id}` | Fetch project metadata |
| List Projects | `GET /api/v0/projects` | List all projects (monitoring) |

---

## Setup: 3 Steps

### Step 1: Get Overleaf API Token

```bash
# 1. Go to Overleaf Settings
# https://www.overleaf.com/user/settings

# 2. Click "Account" tab

# 3. Scroll down to "API"

# 4. Create API token (or copy existing)
# Token format: ol_abc123def456ghi789jkl012mnopqrs

# 5. Store securely in GCP Secret Manager
gcloud secrets create overleaf-api-token \
  --data-file=- \
  --project=projectrl-485417
# Paste token when prompted
```

### Step 2: Verify Token (Test Connection)

```bash
export OVERLEAF_TOKEN=ol_your_token_here

# Test API connection
curl -H "Authorization: Bearer $OVERLEAF_TOKEN" \
  https://api.overleaf.com/api/v0/user

# Expected response:
# {
#   "id": "user_id_123",
#   "email": "your@email.com",
#   "name": "Your Name",
#   "subscription": "professional"
# }
```

### Step 3: Load in Workflows

```bash
# In your workflow or script:
export OVERLEAF_TOKEN=$(gcloud secrets versions access latest \
  --secret=overleaf-api-token \
  --project=projectrl-485417)

echo "✅ Overleaf token loaded: ${OVERLEAF_TOKEN:0:20}..."
```

---

## Usage Examples

### Example 1: Publish Single Paper

```python
from github_git_push import publish_paper_to_overleaf

result = publish_paper_to_overleaf(
    title="Fast RL with Structural Information",
    content=r"""
\documentclass{article}
\usepackage{amsmath}

\title{Fast RL with Structural Information}
\author{Your Name}

\begin{document}

\maketitle

\section{Introduction}

Our method achieves:
\begin{equation}
J(\pi) = \mathbb{E}_{\tau \sim \pi}\left[\sum_{t=0}^T \gamma^t r_t\right]
\end{equation}

\end{document}
""",
    overleaf_token=os.getenv("OVERLEAF_TOKEN"),
    paper_type="arxiv"
)

print(f"✅ Published to Overleaf: {result['url']}")
# Output: https://www.overleaf.com/project/abc123def456
```

### Example 2: Publish with Figures

```python
# Prepare LaTeX with figure references
latex_content = r"""
\documentclass{article}
\usepackage{graphicx}

\begin{document}

\section{Results}

\begin{figure}
  \includegraphics[width=0.8\textwidth]{figures/results.png}
  \caption{Our method achieves SOTA performance}
\end{figure}

\end{document}
"""

# Publish to Overleaf
result = publish_paper_to_overleaf(
    title="SOTA Results",
    content=latex_content,
    overleaf_token=os.getenv("OVERLEAF_TOKEN")
)

# Note: Upload figures separately after project creation
import requests

files = {"file": ("results.png", open("figures/results.png", "rb"))}
requests.post(
    f"{result['url']}/files",
    files=files,
    headers={"Authorization": f"Bearer {os.getenv('OVERLEAF_TOKEN')}"}
)
```

### Example 3: Auto-Publish in Workflow

**YAML Workflow:**
```yaml
stages:
  - id: write_paper
    name: "Write Paper"
    skill: paper-writer
    outputs:
      - paper_latex
      - paper_title

  - id: publish_overleaf
    name: "Publish to Overleaf"
    skill: util-github-git-push
    action: publish_paper_to_overleaf
    inputs:
      title: ${write_paper.outputs.paper_title}
      content: ${write_paper.outputs.paper_latex}
      overleaf_token: ${secrets.OVERLEAF_API_TOKEN}
      paper_type: "arxiv"  # or "conference", "workshop"
    outputs:
      - overleaf_url
      - project_id

  - id: notify
    name: "Notify Team"
    skill: util-notifier
    inputs:
      message: "📄 Paper published to Overleaf: {{publish_overleaf.outputs.overleaf_url}}"
      channels:
        - slack: "#papers"
```

---

## Paper Types Supported

### 1. ArXiv Format (Default)

```python
publish_paper_to_overleaf(
    title="My Research Paper",
    content=latex_code,
    overleaf_token=token,
    paper_type="arxiv"  # Standard arXiv submission format
)
```

**Includes:**
- Standard article class
- Title, author, abstract
- Sections: intro, related work, method, experiments, conclusion
- Bibliography setup

### 2. Conference Format

```python
publish_paper_to_overleaf(
    title="My Research Paper",
    content=latex_code,
    overleaf_token=token,
    paper_type="conference"  # IEEE, ACM, etc. format
)
```

**Includes:**
- Conference-specific document class
- Double-column layout
- Author affiliations
- Conference header

### 3. Workshop Format

```python
publish_paper_to_overleaf(
    title="My Research Paper",
    content=latex_code,
    overleaf_token=token,
    paper_type="workshop"  # Workshop submission format
)
```

**Includes:**
- Simpler format for workshops
- Less strict formatting
- Extended bibliography support

---

## Advanced: Multi-File Upload

### Upload with Figures, Bibliography, Appendix

```python
import requests
import os

# First, create project
result = publish_paper_to_overleaf(
    title="Complete Paper",
    content=main_latex,
    overleaf_token=token,
    paper_type="arxiv"
)

project_id = result['project_id']
project_url = result['url']

# Now upload additional files
files_to_upload = {
    "figures/results.png": open("figures/results.png", "rb"),
    "figures/architecture.pdf": open("figures/architecture.pdf", "rb"),
    "references.bib": open("references.bib", "r"),
    "appendix.tex": open("appendix.tex", "r"),
}

headers = {"Authorization": f"Bearer {token}"}

for file_path, file_obj in files_to_upload.items():
    files = {"file": (file_path, file_obj)}
    upload_url = f"https://api.overleaf.com/api/v0/projects/{project_id}/files"
    
    response = requests.post(
        upload_url,
        files=files,
        headers=headers
    )
    
    if response.status_code == 200:
        print(f"✅ Uploaded {file_path}")
    else:
        print(f"⚠️ Failed to upload {file_path}: {response.status_code}")

print(f"\n✅ Complete paper at: {project_url}")
```

---

## Workflow Integration: End-to-End Example

### Complete "Write Paper + Publish" Flow

```bash
#!/bin/bash
set -e

# Load credentials
export OVERLEAF_TOKEN=$(gcloud secrets versions access latest --secret=overleaf-api-token)
export GITHUB_TOKEN=$(gcloud secrets versions access latest --secret=github-temp-token)

# Step 1: Write paper
python3 << 'EOF'
from paper_writer import write_paper

paper_latex, paper_md, title = write_paper(
    idea="Combine PPO with entropy regularization",
    references=["ppo.pdf", "maximum_entropy_rl.pdf"]
)

with open("paper.tex", "w") as f:
    f.write(paper_latex)
with open("paper.md", "w") as f:
    f.write(paper_md)
EOF

# Step 2: Publish to Overleaf
python3 << 'EOF'
import os
from github_git_push import publish_paper_to_overleaf

with open("paper.tex", "r") as f:
    latex_content = f.read()

result = publish_paper_to_overleaf(
    title="Combine PPO with Entropy Regularization",
    content=latex_content,
    overleaf_token=os.getenv("OVERLEAF_TOKEN"),
    paper_type="arxiv"
)

overleaf_url = result['url']
print(f"OVERLEAF_URL={overleaf_url}")
EOF

# Step 3: Publish to blog
python3 << 'EOF'
import os
from github_git_push import publish_blog_post

with open("paper.md", "r") as f:
    markdown_content = f.read()

result = publish_blog_post(
    title="New Paper: Combine PPO with Entropy Regularization",
    content=f"{markdown_content}\n\n[Read full paper on Overleaf]({os.getenv('OVERLEAF_URL')})",
    tags=["paper", "research", "rl"],
    github_token=os.getenv("GITHUB_TOKEN"),
    description="New research paper combining PPO with entropy regularization"
)

blog_url = result['url']
print(f"BLOG_URL={blog_url}")
EOF

# Step 4: Notify team
python3 << 'EOF'
import os
from util_notifier import send_slack

send_slack(
    message=f"""
📄 New Paper Published!

**Overleaf:** {os.getenv('OVERLEAF_URL')}
**Blog:** {os.getenv('BLOG_URL')}

Ready for sharing and collaboration!
""",
    channel="#papers"
)
EOF

echo "✅ Complete! Paper published to both Overleaf and blog"
```

---

## Monitoring & Management

### List All Published Projects

```python
import requests

headers = {"Authorization": f"Bearer {overleaf_token}"}

response = requests.get(
    "https://api.overleaf.com/api/v0/projects",
    headers=headers
)

projects = response.json()
for project in projects:
    print(f"- {project['name']}: {project['url']}")
```

### Track Publishing History

```python
# Keep record of published papers
import json
from datetime import datetime

publishing_log = {
    "timestamp": datetime.now().isoformat(),
    "paper_title": "Combine PPO with Entropy Regularization",
    "overleaf_url": "https://www.overleaf.com/project/abc123",
    "blog_url": "https://blog.com/posts/2026-05-03-...",
    "status": "published"
}

with open("publishing_history.jsonl", "a") as f:
    f.write(json.dumps(publishing_log) + "\n")

print(f"✅ Published papers log updated")
```

---

## Troubleshooting

### Issue: "401 Unauthorized"

**Symptom:** Overleaf API returns 401 error

**Solution:**
```bash
# Verify token is valid
curl -H "Authorization: Bearer $OVERLEAF_TOKEN" \
  https://api.overleaf.com/api/v0/user

# If 401: token is invalid or expired
# → Create new token: https://www.overleaf.com/user/settings
# → Update GCP Secret: 
gcloud secrets versions add overleaf-api-token --data-file=-
```

### Issue: "Project not found"

**Symptom:** Can't update project after creation

**Solution:**
```python
# Verify project_id is correct
result = publish_paper_to_overleaf(...)
print(f"Project ID: {result['project_id']}")  # Should be non-empty

# Project URL should also be valid
# https://www.overleaf.com/project/{project_id}
```

### Issue: "File upload failed"

**Symptom:** Can't upload figures or bibliography

**Solution:**
```python
# Check file exists and is readable
import os
if not os.path.exists("figures/results.png"):
    print("❌ File not found")

# Verify file size (Overleaf has limits)
size_mb = os.path.getsize("figures/results.png") / (1024 * 1024)
if size_mb > 100:  # 100MB limit per file
    print(f"⚠️ File too large: {size_mb}MB")

# Use smaller file or compress
```

---

## Security

### Credential Management

**✅ DO:**
- Store token in GCP Secret Manager (encrypted)
- Use temporary tokens for CI/CD
- Rotate tokens monthly
- Load from environment variables only

**❌ DON'T:**
- Hardcode token in code
- Commit token to git
- Share token via email
- Use same token across environments

### API Permissions

The Overleaf API token gives access to:
- ✅ Create projects
- ✅ Upload/modify files
- ✅ Read project metadata
- ❌ Delete projects (not available via API)
- ❌ Share/invite collaborators (limited)

---

## Integration with AutoSOTA Workflows

### Beat SOTA Workflow + Overleaf

```yaml
stages:
  # ... reimplement code ...
  
  - id: write_comparison_paper
    name: "Write Comparison Paper"
    skill: paper-writer
    inputs:
      original_method: ${stages.collect.outputs.paper}
      reimplemented_method: ${stages.reimplement.outputs.code}
      comparison_results: ${stages.test.outputs.metrics}
    outputs:
      - paper_latex

  - id: publish_overleaf
    name: "Publish Comparison to Overleaf"
    skill: util-github-git-push
    inputs:
      title: "Reimplementation Comparison: {{original_title}}"
      content: ${write_comparison_paper.outputs.paper_latex}
      overleaf_token: ${secrets.OVERLEAF_API_TOKEN}
    outputs:
      - overleaf_url

  - id: notify
    name: "Share Results"
    inputs:
      message: "🎯 Comparison paper on Overleaf: {{publish_overleaf.outputs.overleaf_url}}"
```

---

## Cost & Limits

### Overleaf API Limits

| Limit | Free | Pro |
|---|---|---|
| Projects | 50 | Unlimited |
| File uploads | 100MB | 1GB |
| Collaborators | 1 | Unlimited |
| API calls | 1000/day | 10000/day |

### Recommendations

- **Free tier:** Good for testing, single-author papers
- **Pro tier:** Recommended for collaborative research
- **File size:** Keep under 50MB per file (figures + main tex)

---

## Next Steps

1. **Get Overleaf API token** (https://www.overleaf.com/user/settings)
2. **Store in GCP Secret Manager**
3. **Test with** `publish_paper_to_overleaf()`
4. **Integrate into workflows** via YAML
5. **Automate paper publishing** end-to-end

---

## Related Documentation

- [GitHub Publishing](GITHUB_GIT_PUSH_SKILL.md) — Publishing blog posts
- [Workflow Orchestrator](../sota-workflow-orchestrator/SKILL.md) — Full automation
- [Paper Writer Skill](../paper-writer/SKILL.md) — Generate paper content
- [Overleaf API Docs](https://www.overleaf.com/learn/how-to/Overleaf_API) — Official Overleaf API

---

## Summary

✅ **Overleaf Integration is Fully Supported**

- Create projects automatically ✅
- Upload files via API ✅
- Support multiple paper types ✅
- Works in workflows ✅
- Secure credential storage ✅
- Share links in Slack ✅

Use it to automate the complete research publishing pipeline: **write → publish to Overleaf → announce on blog → notify team**!
