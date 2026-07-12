---
name: lab-notebook-blog
description: Use when asked to write a "lab notebook" blog post, project status post, active-tracks overview, or research-campaign explainer that covers every active and queued track of a research project from scratch. Applicable when a multi-track project (papers + competition + platform + experiments in flight) needs a single public post that explains each track from first principles, reports only verified numbers, states what each track feeds, lists planned future tracks with time estimates, and ends with a dependency map — published as a Jekyll post on the project's GitHub Pages.
metadata:
  short-description: Write an active-tracks lab-notebook blog post
---

# Lab Notebook Blog Post

Use this skill to generate a blog post that explains **every active track of a research project from scratch** — no prior context assumed — and publish it on the project's GitHub Pages. The expected output is a self-contained public post a newcomer can read cold, not an internal status dump. The exemplar this skill distills is a post covering eleven concurrent tracks of a game-AI campaign, each explained from first principles with verified numbers and an explicit dependency map.

## Workflow

1. **Inventory every track**
   - Sweep all sources of active work: plan files (`plans/`, `PLAN*.md`, `HANDOFF*.md`), results directories, memory/state notes, running jobs (tmux/cron/GPU boxes), open branches, and recent commits.
   - A "track" is any workstream with its own question and its own success criterion — include in-flight, queued, recently shipped (if other tracks depend on it), and planned-but-not-started.
   - Also inventory the project's **goals** (competition entries, paper deadlines, platform/infrastructure, other) — every track must map to at least one.
   - Do not drop tracks that are stalled or embarrassing; a lab notebook that omits the correction-in-progress is not a lab notebook.

2. **Gather verified numbers only (verification discipline)**
   - For every quantitative claim, read the number **from the result JSON / log / harvested artifact** — never from memory, never from a previous prose summary, never extrapolated.
   - Record next to each number the file path it came from (kept in your working notes, not necessarily in the post).
   - If a number is not yet in a result file, the status is "in flight" with no number. A track with zero verified numbers still gets a section — with an honest "launching / in flight" status.
   - Negative and corrected results are first-class: if a headline number is being revised downward, say so explicitly and prominently.

3. **Write each track with the four-part structure**
   For every track, in this order:
   - **What it is.** 2–3 sentences from first principles. Every term of art gets an inline gloss the first time it appears ("knowledge distillation — training a student network to match a teacher's output distribution"). Assume the reader knows nothing about the project or the domain.
   - **Why it exists.** The concrete question this track answers, or the failure/gap that forced it into existence. The best "why" sections tell the honest causal story ("gates optimized placement, but the final ranked by score — so this gate exists").
   - **Status.** One of: shipped / done / in flight / launching / planned. Attach only numbers verified in step 2, with enough context that the number means something (n, units, baseline, caveats). State standing caveats ("good prediction has repeatedly failed to convert into control").
   - **Feeds.** What the track's output flows into, categorized by GOAL: **competition**, **paper**, **platform**, or **other**. Name the specific consumer (which paper, which model line).

4. **Include planned future tracks with time estimates**
   - Tracks that exist only in plans get the same four-part treatment plus an explicit time estimate (e.g. "~2 GPU-days on one 3090", "1 week after track 5 lands").
   - Mark them clearly as planned so a reader never mistakes an intention for a result.

5. **Write the framing: TL;DR + minimal shared context**
   - Open with a blockquoted **TL;DR**: how many tracks, which goals they serve (papers / competition / platform), and the single most newsworthy or uncomfortable headline — stated plainly.
   - Follow with a **"minimal shared context"** paragraph (target: readable in 60 seconds) giving exactly the background every section relies on — the domain, the flagship result, and any evaluation methodology that recurs across tracks. Everything below it must build only on this paragraph.

6. **End with a dependency map**
   - A closing section that draws the pipelines in prose (or a diagram): which tracks feed which, grouped by goal ("Integrity → papers", "Corpus → competition", "Infrastructure → platform").
   - Reference tracks by their section numbers so the map is checkable against the body.
   - Close with the project's through-line — the one-sentence principle all tracks share.

7. **Publish as a Jekyll post on the project's Pages**
   - Use [references/template.md](references/template.md) for the exact section skeleton and Jekyll front matter (`layout: post`, `title`, `date`, `tags`).
   - File goes to the project's Pages source (typically `docs/blog/YYYY-MM-DD-slug.md` or `_posts/`), matching the repo's existing post conventions (check `_config.yml` and an existing post for layout name, permalink style, and math rendering).
   - Cross-link other Pages documents with relative `.html` links as the existing posts do.
   - Run the pre-publish checklist in the template. Then commit and push; verify the page renders on Pages.

## Quality Bar

- **Every number traceable to a result file.** If you cannot point at the JSON/log a figure came from, the figure does not go in the post. Multi-track projects fabricate numbers by paraphrase; this post must not.
- **From-first-principles means it.** A reader with zero project context must be able to follow every section using only the minimal-shared-context paragraph. No unexplained jargon, acronym, or internal codename — gloss on first use or cut.
- **Honest status over flattering status.** Corrections, nulls, and degenerate results are reported with the same prominence as wins, including the diagnosed cause when known. "In flight" never carries a projected number.
- **Every track categorized by goal** (competition / paper / platform / other) in its **Feeds** line, and the dependency map must account for every numbered track — no orphans.
- **Future tracks carry time estimates** and are unmistakably labeled as planned.
- **No secrets or anonymity leaks.** Before publishing: no credentials, hostnames, box IPs, or API keys; no links that would deanonymize work under double-blind review (say "under anonymous review, so no repository links here"); no other party's private information.
- The post is a durable public artifact: write it so it is still comprehensible and honest when read a year later.

## Reference Files

- [references/template.md](references/template.md): the section skeleton (Jekyll front matter, TL;DR, shared context, per-track structure, dependency map) and the pre-publish checklist.
