# Changelog

## [Unreleased]

### Added

#### New Skills Discovered & Documented
- **autosota-agent-monitor-scheduler**: Combined monitoring and scheduling for Vast.ai job lifecycle management, deadlock prevention, and persistent context across execution resets. Includes Memory Templates and Reverse Engineer Report.
- **exp_result_skill**: Provisional Experiments/Results section generation with multi-panel configurable figures, editable HTML workbench, and mandatory provenance tracking (experimented, public, estimated, artificial, modified, derived).
- **scientific_writing_reverse_engineering_skill**: Enhanced variant of scientific writing reverse engineering with interactive HTML review workbench, rendering tools, and example writing maps.

#### Documentation & Organization
- **Comprehensive skill categorization**: Reorganized `skill-map.md` with 7 major categories:
  - Pipeline & Orchestration (7 skills)
  - Code Reimplementation & Debugging (3 skills)
  - Optimization & Ideation (4 skills)
  - Experiment Results & Reporting (2 skills)
  - Writing & Publication (4 skills)
  - Common Operations & Infrastructure (4 skills)
  - Incomplete / Placeholder (1 skill)
- **Expanded README**: Detailed descriptions of all 24 discoverable skills with use cases and capabilities.
- **Placeholder tracking**: Documented `autosota-rl-experiment-section` as under development.

### Changed
- Updated `skill-map.md`: Moved from simple list format to categorized, detailed reference with capability descriptions.
- Enhanced README.md: Added comprehensive skill descriptions grouped by research workflow phase.
- Clarified relationship between `scientific-writing-reverse-engineering` (base skill) and `scientific_writing_reverse_engineering_skill` (enhanced variant with tools).

### Known Issues
- `autosota-rl-experiment-section`: No SKILL.md file; structure is placeholder-only.
- Instance shutdown: Instances may not terminate properly when using Gemini backend.
- Schema standardization: Result logging schema needs additional validation rules.

### Planned
- detect deadlock


#### High Priority

- **Unified credential management**: Implement best practices for all external services (WandB, GitHub, Vast.ai, Slack, Overleaf, publishing):
  - Centralized secrets vault (HashiCorp Vault or cloud provider managed secrets)
  - Encryption at rest for stored credentials
  - Per-service credential scoping and least-privilege access
  - Automated credential rotation policies with expiration tracking
  - Audit logging for all credential access
  - Environment-based configuration (dev/staging/prod separation)
  - Credential validation and health checks before API calls
  - Graceful degradation if credentials missing (skip optional services, warn user)
- Integration hooks for real-time Slack/email notifications during long-running tasks.

- update vastai scheduler, 
    - to avoid rent >0.1$/hour instances,
    - update a true run estimator,  for those task need to run long,rent a series of 30 40 50 short run to see how actually they behave, speed and GPU util, memory, cpu util etc.

#### Medium Priority
- Overleaf and blog platform direct integration for real-time collaboration. use mcp to sync markdown content with Overleaf projects and blogging platforms.
- Extended ablation study automation in `autosota-agent-ideator`.
- Cost tracking and budget alerts for Vast.ai instances.
- Complete `autosota-rl-experiment-section` with RL-specific features.
#### Future Research
- Reverse-engineering templates for other paper types (theory, surveys, reviews).
- Multi-model paper analysis for writing pattern discovery.
- Automated methodology validation against benchmark red-lines.
---

## 2026-05-01
### Skill Audit & Categorization
- Discovered 24 total discoverable skills across `plugins/autosota-lite/skills/`.
- Identified and documented 3 previously unlisted skills: `autosota-agent-monitor-scheduler`, `exp_result_skill`, `scientific_writing_reverse_engineering_skill`.
- Mapped all skills to research lifecycle phases and workflow categories.
- Updated `skill-map.md` with detailed capability descriptions.
- Updated README.md with comprehensive skill narratives.

## 2026-04-29
- **Result Logging Skill**: Implemented core logic in `result_logger.py` with support for WandB and GitHub Gists.
- **Credential Handling**: Added automatic detection of `WANDB_API_KEY` and `GITHUB_TOKEN`.
- Updated README.md with comprehensive skill list.
- Initialized changelog.md based on repository history.
