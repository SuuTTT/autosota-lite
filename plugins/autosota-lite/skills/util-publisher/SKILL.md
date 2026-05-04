---
name: util-publisher
description: Publish research papers, blog posts, and results. Edit in Git → Push to GitHub → Import to Overleaf.
---

# Skill: util-publisher

Automate research publishing workflow: write locally in Git, push to GitHub, and import final versions to Overleaf for collaboration.

---

## Publication Workflow

```
Write Paper (Local)
    ↓
git push to GitHub
    ↓
Import to Overleaf (Direct)
    ↓
Share & Collaborate
```

### Why This Approach?

✅ **Version Control**: Full git history of all changes  
✅ **Offline Support**: Work locally without internet  
✅ **No API Limits**: No Overleaf API rate limits  
✅ **Easy Collaboration**: Multiple people edit via GitHub  
✅ **Automatic Sync**: Overleaf syncs from GitHub  
✅ **Safe**: Private GitHub repo, sync to Overleaf when ready  

---

## Quick Start

### 1. Create GitHub Repository

```bash
# https://github.com/new
# Name: my-paper
# Private: ✅
# Copy URL
```

### 2. Connect Local Repo

```bash
cd /workspace/my-paper-folder
git remote add origin https://github.com/YOUR_USERNAME/my-paper.git
git branch -M main
git push -u origin main
```

### 3. Edit and Push

```bash
# Edit main.tex in VSCode (or any editor)
git add main.tex
git commit -m "Update method section"
git push origin main
```

### 4. Import to Overleaf

In Overleaf:
1. **New Project** → **Import from GitHub**
2. **Authorize GitHub** (one-time)
3. **Select**: `your-username/my-paper`
4. **Click Import**

**Done!** Overleaf syncs automatically:
- Push to GitHub → Overleaf updates instantly
- Edit in Overleaf → Pull changes locally (if you enable syncing)

---

## Publication Targets

### 1. Research Paper (Overleaf)

**Workflow:**
```
Write paper locally
    ↓
git push to GitHub
    ↓
Overleaf imports from GitHub
    ↓
Real-time LaTeX compilation
    ↓
Share & download PDF
```

**Tools:**
- Write: Any text editor or VSCode
- Version Control: Git + GitHub
- Collaboration: Overleaf (synced from GitHub)

### 2. Blog Post Announcement (GitHub Blog)

**Workflow:**
```
Write blog post in Markdown
    ↓
git push to GitHub blog repo
    ↓
GitHub Pages auto-deploys
    ↓
Blog updates instantly
```

**Tools:**
- Script: `github_git_push.py` → `publish_blog_post()`
- Platform: GitHub Pages (or your blog)
- Formulas: KaTeX validation

### 3. Results Announcement (Slack)

**Workflow:**
```
Paper complete
    ↓
Generate summary
    ↓
Send to Slack with links
```

**Tools:**
- Integration: AutoSOTA workflows → Slack notifier

---

## Paper Directory Structure

```
my-paper/
├── main.tex              # Paper content
├── .gitignore           # Ignore LaTeX artifacts
├── README.md            # Instructions
├── code/                # Implementation
├── figures/             # Plots and images
├── references/          # Cited papers
└── .git/               # Version control
```

---

## Git Workflow: Local Edit

### Basic Workflow

```bash
# 1. Create paper repo locally
mkdir my-paper
cd my-paper
git init

# 2. Add files
echo "\documentclass{article}..." > main.tex
git add .
git commit -m "Initial paper draft"

# 3. Connect to GitHub
git remote add origin https://github.com/YOUR_USERNAME/my-paper.git
git branch -M main
git push -u origin main

# 4. Edit locally
vim main.tex        # Edit paper
git add main.tex
git commit -m "Update introduction"
git push origin main

# 5. See changes on GitHub and Overleaf
```

### Advanced: Feature Branches

```bash
# Create feature branch for major changes
git checkout -b feature/add-experiments

# Make edits
vim main.tex

# Commit
git add main.tex
git commit -m "Add experiment results section"
git push origin feature/add-experiments

# Create Pull Request on GitHub for review
# Then merge to main
```

---

## Overleaf Integration: Direct Import

### Setup (One-Time)

1. **Go to Overleaf**: https://www.overleaf.com/
2. **Create New Project** → **Import from GitHub**
3. **Click Authorize GitHub**
4. **Grant permissions** (repo access)

### Using Sync

1. **Select Repository**: `your-username/my-paper`
2. **Click Import**
3. **Overleaf creates project** synced to GitHub

### After Import

- **Push to GitHub** → Overleaf updates automatically
- **Edit in Overleaf** → Push changes to GitHub (via Overleaf menu)
- **Real-time collaboration** → Multiple people edit together

### Download & Share

In Overleaf:
- **Menu** → **Download** → **PDF** (compiled paper)
- **Menu** → **Download** → **Source** (all LaTeX files)
- **Share** → **Send link** (for collaboration)

---

## Blog Post Publishing

### Publish Blog Post to GitHub

```bash
# Using the github_git_push.py skill
python3 examples_publish_blog_post.py \
  --title "My Research Results" \
  --content "## Results\n..." \
  --tags "research,sota" \
  --blog-repo "https://github.com/YOU/blog.git" \
  --github-token "ghp_your_token"
```

### Or Use Python Directly

```python
from github_git_push import publish_blog_post

publish_blog_post(
    title="My Research Results",
    content="## Results\n\nOur method achieves...",
    tags=["research", "sota"],
    github_token="ghp_...",
    blog_repo="https://github.com/YOU/blog.git"
)
```

### Requirements

- **GitHub Token**: Create at https://github.com/settings/tokens/new
  - Scopes: `repo`, `workflow`
- **Blog Repository**: Your GitHub blog repo
  - Structure: `_posts/` (Jekyll) or `content/posts/` (Hugo)

---

## Scripts Included

### `github_git_push.py`

**Functions:**
- `publish_blog_post()` — Push blog post to GitHub
- `validate_formulas()` — Check KaTeX formulas
- `setup_git_auth()` — Configure git authentication

**Use Cases:**
```python
# Publish blog post
publish_blog_post(
    title="Paper announcement",
    content=markdown_content,
    tags=["paper", "research"],
    github_token=token
)

# Validate formulas before publishing
warnings = validate_formulas(content)
if warnings:
    print("⚠️ Formula issues found")
```

### `examples_publish_blog_post.py`

Complete example script for publishing blog posts with:
- Hugo/Jekyll frontmatter generation
- KaTeX formula validation
- GitHub push automation
- Error handling

### `examples_publish_paper_to_github.py`

Example: Create LaTeX paper structure and push to GitHub:
- Directory structure (code/, figures/, references/)
- .gitignore for LaTeX artifacts
- README with instructions
- Ready for Overleaf import

---

## Grounding Rules

When publishing, follow these rules:

1. **Accuracy**: Use only validated results
2. **Transparency**: Label preliminary results clearly
3. **Context**: Include dataset names, metrics, hardware info
4. **Citations**: Link sources and cited papers
5. **Privacy**: Don't expose secrets or private details
6. **Caveats**: Include benchmark limitations

---

## Integration with AutoSOTA Workflows

### Write Paper Workflow

```yaml
stages:
  - id: write_paper
    skill: paper-writer
    outputs:
      - paper_markdown
      - paper_latex

  - id: publish_github
    skill: util-publisher
    action: push_to_github
    inputs:
      content: ${write_paper.outputs.paper_latex}
      repo: "my-paper"
      branch: "main"

  - id: notify
    skill: util-notifier
    inputs:
      message: "📄 Paper pushed to GitHub. Import to Overleaf!"
      channels: ["slack"]
```

### Blog Announcement Workflow

```yaml
stages:
  - id: generate_summary
    outputs:
      - blog_content
      - title
      - tags

  - id: publish_blog
    skill: util-publisher
    action: publish_blog_post
    inputs:
      title: ${generate_summary.outputs.title}
      content: ${generate_summary.outputs.blog_content}
      tags: ${generate_summary.outputs.tags}
      github_token: ${secrets.GITHUB_TOKEN}

  - id: notify_slack
    inputs:
      message: "📝 Blog post published!"
```

---

## File Locations

**Skill Directory**: 
```
/workspace/autosota-lite/plugins/autosota-lite/skills/util-publisher/
```

**Files**:
- `SKILL.md` — This documentation
- `github_git_push.py` — Core publishing script
- `examples_publish_blog_post.py` — Blog publishing example
- `examples_publish_paper_to_github.py` — Paper structure example
- `README.md` — Quick reference

---

## Common Workflows

### Workflow 1: Write Paper → GitHub → Overleaf

```bash
# 1. Create local repo
mkdir my-paper && cd my-paper && git init

# 2. Write paper
echo "\documentclass{article}..." > main.tex

# 3. Commit locally
git add main.tex
git commit -m "Initial draft"

# 4. Push to GitHub
git remote add origin https://github.com/YOU/my-paper.git
git branch -M main
git push -u origin main

# 5. Import to Overleaf (in Overleaf UI)
# New Project → Import from GitHub → Select my-paper

# 6. Edit and sync
vim main.tex
git add main.tex
git commit -m "Update section"
git push origin main
# Overleaf auto-updates!
```

### Workflow 2: Blog Post Announcement

```bash
# 1. Write blog post
cat > blog_post.md << 'EOF'
# My Research Results

## Abstract
...

## Key Findings
...
EOF

# 2. Publish to blog
python3 examples_publish_blog_post.py \
  --title "My Research Results" \
  --content-file blog_post.md \
  --tags "research,sota" \
  --github-token "ghp_..."

# 3. Gets published to GitHub blog automatically!
```

### Workflow 3: Paper + Blog Announcement

```bash
# 1. Edit paper locally
git push origin main

# 2. Generate blog post from paper abstract
python3 -c "
from github_git_push import publish_blog_post
publish_blog_post(
    title='New Paper: ...',
    content='[View on GitHub](link)',
    tags=['paper', 'research'],
    github_token='ghp_...'
)
"

# 3. Paper on GitHub, announcement on blog, team notified!
```

---

## Troubleshooting

### "Repository not found"

**Fix**: Verify URL and GitHub token
```bash
git remote -v
# Should show correct origin URL
```

### "Not authorized to access"

**Fix**: Create new GitHub token
```bash
# https://github.com/settings/tokens/new
# Scopes: repo, workflow
export GITHUB_TOKEN=ghp_new_token
```

### "Formula validation errors"

**Fix**: Check LaTeX delimiters
```bash
# Check for unmatched $$
grep -o '\$\$' main.tex | wc -l
# Should be even number
```

---

## Advantages of Git-First Approach

| Aspect | Git Repo | Overleaf API |
|--------|----------|--------------|
| **Version Control** | ✅ Full history | ❌ Limited |
| **Offline Work** | ✅ Works offline | ❌ Needs internet |
| **API Limits** | ✅ None | ❌ Yes |
| **Collaboration** | ✅ Easy (GitHub) | ✅ Yes |
| **Security** | ✅ Private by default | ⚠️ Needs token |
| **Multi-platform** | ✅ Works anywhere | ✅ Overleaf only |

---

## Summary

**util-publisher** enables the optimal workflow:

1. ✅ **Write locally** in Git (offline support)
2. ✅ **Push to GitHub** (version control, collaboration)
3. ✅ **Import to Overleaf** (real-time compilation)
4. ✅ **Share & Download** (PDF ready)

**No API calls needed. Simple, secure, powerful.**

---

## Next Steps

1. Create GitHub repo
2. Write paper locally
3. `git push` to GitHub
4. Import to Overleaf
5. Edit, commit, push → Overleaf syncs automatically

**That's it! Happy publishing!** 🚀
