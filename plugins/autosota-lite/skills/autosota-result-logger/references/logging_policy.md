# Credentials and Logging Policy

## Credential Management
The `autosota-result-logger` skill automatically searches for credentials in the following order:
1.  **Environment Variables**: `WANDB_API_KEY`, `GITHUB_TOKEN`.
2.  **Secret Stores**: Looks for `~/.netrc` (for WandB) or `~/.github_token`.
3.  **Local Workspace Secrets**: Checks for a `.secrets.yaml` in the repository root (excluded from git).

## WandB Project Structure
- Projects should be named according to the `objective.md` or `autosota.yaml`.
- Run names should include the date and the specific idea ID from `idea_library.md`.

## GitHub Reporting
- Summaries are preferred over raw data dumps.
- Update `research_report.md` via git commits to maintain a history of results alongside code changes.
