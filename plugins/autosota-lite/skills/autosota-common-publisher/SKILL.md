---
name: autosota-common-publisher
description: Turn validated AutoSOTA results, paper drafts, experiment summaries, and domain insights into blog posts, release notes, short social posts, or TikTok-style scripts without overstating unverified claims.
---

# AutoSOTA Common Publisher

Use this skill when the user wants external-facing writing after an experiment, paper draft, or domain proposal is ready.

## Publication Targets

- Research blog post.
- Project update or release note.
- Short social post.
- TikTok or short-video script.
- Overleaf or paper companion summary.

## Grounding Rules

- Use only validated results, explicitly labeled preliminary results, or clearly marked hypotheses.
- Do not convert a failed or invalid run into a success story.
- Preserve benchmark caveats, dataset names, metric direction, and hardware/runtime context.
- Cite papers or link sources when making research claims.
- Avoid exposing secrets, private repo paths, unpublished collaborator details, or non-public leaderboard claims.

## Workflow

1. Read the relevant source artifact: `research_report.md`, `paper/`, `scores.jsonl`, `idea_library.md`, `comparison_matrix.md`, or run logs.
2. Choose the target format and audience.
3. Extract the claim, evidence, caveat, and call to action.
4. Draft the content.
5. Add a short verification note listing which artifacts support the claims.

