#!/usr/bin/env python3
"""
Git push and blog publishing helper for agent-written papers and blog posts
Handles GitHub authentication, KaTeX formula rendering, and Overleaf integration
"""

import os
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Literal
from datetime import datetime


def setup_git_auth(
    auth_type: Literal["ssh", "token"],
    ssh_key_path: Optional[str] = None,
    github_token: Optional[str] = None
) -> None:
    """
    Configure git authentication for the current session

    Args:
        auth_type: "ssh" (local) or "token" (rented instance)
        ssh_key_path: Path to SSH private key (for ssh auth)
        github_token: GitHub token (for token auth)
    """
    if auth_type == "ssh":
        if not ssh_key_path or not Path(ssh_key_path).exists():
            raise FileNotFoundError(f"SSH key not found: {ssh_key_path}")

        # Configure git to use SSH key
        os.environ["GIT_SSH_COMMAND"] = f"ssh -i {ssh_key_path} -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
        print(f"✅ Git configured for SSH key: {ssh_key_path}")

    elif auth_type == "token":
        if not github_token:
            raise ValueError("GitHub token required for token auth")

        # Configure git to use token in HTTPS URL
        subprocess.run(
            ["git", "config", "--global", "credential.helper", "store"],
            check=True,
            capture_output=True
        )

        # Store token
        with open(Path.home() / ".git-credentials", "w") as f:
            f.write(f"https://x-access-token:{github_token}@github.com\n")
        os.chmod(Path.home() / ".git-credentials", 0o600)

        print("✅ Git configured for token authentication")


def ensure_katex_support(content: str) -> str:
    """
    Ensure blog post has KaTeX shortcode for formula rendering

    Args:
        content: Markdown content (after frontmatter)

    Returns:
        Content with {{< katex >}} added if not present
    """
    if "{{< katex >}}" not in content:
        return "{{< katex >}}\n\n" + content
    return content


def validate_formulas(content: str) -> list[str]:
    """
    Check for common formula rendering issues

    Args:
        content: Markdown content

    Returns:
        List of warnings if any issues found
    """
    warnings = []

    # Remove code blocks and tables from validation (they contain $ but aren't formulas)
    lines = content.split("\n")
    in_code_block = False
    filtered_lines = []

    for line in lines:
        # Skip code block markers
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue

        # Skip lines in code blocks
        if in_code_block:
            continue

        # Skip table rows (they contain |)
        if "|" in line and line.strip().startswith("|"):
            continue

        # Skip YAML frontmatter and variable references (e.g., ${...})
        if line.startswith("${") or line.startswith("  - ") and "${" in line:
            continue

        filtered_lines.append(line)

    filtered_content = "\n".join(filtered_lines)

    # Only check for severely broken formulas
    # Block equations with unmatched delimiters
    block_count = filtered_content.count("$$")
    if block_count % 2 != 0:
        # This might be false positive from variable references, so be lenient
        if "$$" in filtered_content:
            warnings.append("⚠️ Check: Possible unmatched $$ delimiters")

    return warnings


def push_to_github(
    repo_url: str,
    commit_message: str,
    files: dict[str, str],
    branch: str = "master",
    auth_type: Literal["ssh", "token"] = "token",
    ssh_key_path: Optional[str] = None,
    github_token: Optional[str] = None,
    work_dir: Optional[str] = None,
    dry_run: bool = False
) -> dict:
    """
    Commit and push files to GitHub

    Args:
        repo_url: GitHub repo URL
        commit_message: Commit message
        files: Dict of {file_path: content}
        branch: Target branch (default: master for blog, main for others)
        auth_type: "ssh" or "token"
        ssh_key_path: SSH key path (required if auth_type="ssh")
        github_token: GitHub token (required if auth_type="token")
        work_dir: Working directory (temp if not specified)
        dry_run: If True, don't actually push

    Returns:
        {"status": "success" | "error", "url": "...", "commit": "...", "message": "..."}
    """

    work_dir = Path(work_dir or tempfile.mkdtemp())
    os.chdir(work_dir)

    try:
        # Setup auth before cloning
        setup_git_auth(auth_type, ssh_key_path, github_token)

        # Clone or fetch existing repo
        git_dir = work_dir / ".git"
        if not git_dir.exists():
            # Prepare URL for token auth
            clone_url = repo_url
            if auth_type == "token" and "https://" in repo_url:
                clone_url = repo_url.replace(
                    "https://",
                    f"https://x-access-token:{github_token}@"
                )

            print(f"📦 Cloning {repo_url}...")
            result = subprocess.run(
                ["git", "clone", clone_url, "."],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                return {
                    "status": "error",
                    "message": f"Clone failed: {result.stderr}"
                }
        else:
            print(f"📝 Updating existing repo...")
            subprocess.run(["git", "pull"], capture_output=True, check=True)

        # Configure git identity
        subprocess.run(
            ["git", "config", "user.email", "agent@autosota.dev"],
            check=True,
            capture_output=True
        )
        subprocess.run(
            ["git", "config", "user.name", "AutoSOTA Agent"],
            check=True,
            capture_output=True
        )

        # Write files
        for file_path, content in files.items():
            full_path = work_dir / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content)
            print(f"  ✓ Created {file_path}")

        # Stage files
        for file_path in files.keys():
            subprocess.run(
                ["git", "add", file_path],
                check=True,
                capture_output=True
            )

        # Commit
        result = subprocess.run(
            ["git", "commit", "-m", commit_message],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return {
                "status": "error",
                "message": f"Commit failed: {result.stderr}"
            }

        # Get commit hash
        commit_hash = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()[:8]

        if dry_run:
            print(f"✅ [DRY-RUN] Would push {commit_hash} to {branch}")
            return {
                "status": "success",
                "message": f"Dry-run successful (would push {commit_hash})",
                "dry_run": True
            }

        # Push
        print(f"🚀 Pushing to {branch}...")
        result = subprocess.run(
            ["git", "push", "origin", branch],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return {
                "status": "error",
                "message": f"Push failed: {result.stderr}"
            }

        return {
            "status": "success",
            "url": repo_url.replace(".git", ""),
            "commit": commit_hash,
            "message": commit_message,
            "branch": branch
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Git operation failed: {str(e)}"
        }


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
) -> dict:
    """
    Create and push a new blog post to GitHub blog (Hugo format)

    Args:
        title: Blog post title
        content: Markdown content (without frontmatter)
        tags: Post tags
        github_token: GitHub token for authentication
        blog_repo: Blog repository URL
        auth_type: "token" or "ssh"
        description: Post description (optional)
        date: Post date (YYYY-MM-DD format, defaults to today)
        dry_run: If True, don't actually push

    Returns:
        {"status": "success" | "error", ...}
    """

    # Use provided date or today
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    # Generate slug from title
    slug = title.lower()
    slug = "".join(c if c.isalnum() or c in "-" else "-" for c in slug)
    slug = "-".join(filter(None, slug.split("-")))[:50]  # Limit length

    # Create filename
    filename = f"content/projects/{date}-{slug}.md"

    # Ensure KaTeX support
    content = ensure_katex_support(content)

    # Validate formulas
    warnings = validate_formulas(content)
    if warnings:
        print("⚠️ Formula validation warnings:")
        for warning in warnings:
            print(f"  {warning}")

    # Create Hugo frontmatter
    frontmatter = f"""---
title: "{title}"
date: {date}
description: "{description or title}"
layout: "post"
showTableOfContents: true
math: true
katex: true
tags: {json.dumps(tags)}
---

"""

    full_content = frontmatter + content

    result = push_to_github(
        repo_url=blog_repo,
        commit_message=f"Blog: {title}",
        files={filename: full_content},
        branch="master",
        auth_type=auth_type,
        github_token=github_token if auth_type == "token" else None,
        dry_run=dry_run
    )

    if result["status"] == "success":
        if not result.get("dry_run"):
            post_url = f"{result['url']}/tree/master/{filename}"
            print(f"\n✅ Blog post published!")
            print(f"   Title: {title}")
            print(f"   File: {filename}")
            print(f"   Commit: {result.get('commit', 'N/A')}")
        else:
            print(f"\n✅ Dry-run successful")
            print(f"   Would create: {filename}")

    return result


def publish_paper_to_overleaf(
    title: str,
    content: str,
    overleaf_token: str,
    paper_type: str = "arxiv",
    dry_run: bool = False
) -> dict:
    """
    Create/update Overleaf project with paper

    Args:
        title: Paper title
        content: LaTeX content
        overleaf_token: Overleaf API token
        paper_type: Paper template type (arxiv, conference, workshop)
        dry_run: If True, just validate

    Returns:
        {"status": "success" | "error", ...}
    """
    try:
        import requests
    except ImportError:
        return {
            "status": "error",
            "message": "requests library not found. Install: pip install requests"
        }

    api_url = "https://api.overleaf.com/api/v0/projects"

    headers = {
        "Authorization": f"Bearer {overleaf_token}",
        "Content-Type": "application/json"
    }

    project_data = {
        "name": title,
        "template": paper_type
    }

    if dry_run:
        print(f"✅ [DRY-RUN] Would create Overleaf project: {title}")
        return {
            "status": "success",
            "message": f"Dry-run successful (would create {title})",
            "dry_run": True
        }

    try:
        response = requests.post(
            api_url,
            json=project_data,
            headers=headers,
            timeout=10
        )

        if response.status_code == 201:
            project = response.json()
            project_id = project["project_id"]

            # Upload content
            files = {"file": ("main.tex", content)}
            upload_url = f"{api_url}/{project_id}/files"

            upload_response = requests.post(
                upload_url,
                files=files,
                headers={"Authorization": f"Bearer {overleaf_token}"},
                timeout=10
            )

            if upload_response.status_code == 200:
                print(f"✅ Paper published to Overleaf: {project['url']}")
                return {
                    "status": "success",
                    "project_id": project_id,
                    "url": project["url"]
                }

        return {
            "status": "error",
            "message": f"Overleaf API error: {response.status_code}"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Overleaf publish failed: {str(e)}"
        }


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python github_git_push.py [publish-blog|test]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "test":
        print("Testing blog post publishing...")

        test_content = """## Test: Auto-Push Skill

This is a test blog post demonstrating KaTeX formula rendering.

### Mathematical Example

The auto-push skill uses the following optimization objective:

$$
L = \\arg\\min_\\theta \\sum_{i=1}^{n} \\|f_\\theta(x_i) - y_i\\|^2
$$

Where:
- $f_\\theta$ is the neural network
- $\\theta$ are parameters
- $(x_i, y_i)$ are training pairs

This ensures formulas render correctly on the blog!
"""

        token = os.getenv("GITHUB_TOKEN")
        if not token:
            print("❌ GITHUB_TOKEN not set")
            sys.exit(1)

        result = publish_blog_post(
            title="Testing Auto-Push Skill",
            content=test_content,
            tags=["test", "auto-push", "skill"],
            github_token=token,
            description="Test post for auto-push skill validation",
            dry_run=True  # Start with dry-run
        )

        print(f"\nResult: {json.dumps(result, indent=2)}")
