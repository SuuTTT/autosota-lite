# Changelog

## [Unreleased]

### Added
- **Skill organization map**: Added `plugins/autosota-lite/references/skill-map.md` to organize skills by pipeline category while keeping plugin-discoverable skill folders flat.
- **autosota-optimization-pipeline**: Coordinates generated ideas, human ideas, domain knowledge, reimplementation, logging, notifications, and publishing.
- **autosota-common-key-manager**: Credential hygiene for WandB, GitHub, Vast.ai, Slack, Overleaf, and publishing services.
- **autosota-common-iteration-notifier**: Completion/failure/review-needed notification workflow for Slack or draft updates.
- **autosota-common-publisher**: Blog, release note, social, and TikTok-style publishing drafts grounded in validated results.
- **autosota-reimplementation**: Automated rewriting and porting of code (e.g., to JAX or CleanRL styles).
- **autosota-vastai-scheduler**: Integrated Vast.ai instance launching and monitoring.
- **autosota-runtime-cost-estimator**: Real-time GPU cost estimation and hardware recommendation.
- **autosota-agent-fix**: Automated debugging and error resolution.
- **autosota-agent-ideator**: AI-driven experiment design.
- **autosota-lite**: Initial plugin suite structure and research loop.

### Changed
- Moved `structural-entropy-proposal` from repo-local `.codex/skills/` into `plugins/autosota-lite/skills/` so it belongs to the plugin package.
- Added required YAML frontmatter to `autosota-paper-writer` and `autosota-result-logger` for skill discovery.

### TODO
- **Paper Writing Skill**: Create a skill for automated research paper drafting based on high-star repo patterns.
- **update scheduler**: more pipline including new skills

- the log is not well standard
- the key is not well managed
- the paper(any human readable) is not generated
- connect codex to chat or overleaf or blog or tiktok to fast feedback and iteration. get notify when the task done
-reverse engineer anything

- BUG to fix, instances seems not shutdown when using gemini.
---

## 2026-04-29
- **Result Logging Skill**: Implemented core logic in `result_logger.py` with support for WandB and GitHub Gists.
- **Credential Handling**: Added automatic detection of `WANDB_API_KEY` and `GITHUB_TOKEN`.
- Updated README.md with comprehensive skill list.
- Initialized changelog.md based on repository history.
