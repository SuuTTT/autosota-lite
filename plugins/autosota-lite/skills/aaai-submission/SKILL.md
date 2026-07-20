---
name: aaai-submission
description: Use when preparing an AAAI (or any OpenReview double-blind) conference submission from an existing paper + verified results — generating the copy-ready OpenReview field package (title, TL;DR, abstract, topics, authors) and enforcing the submission discipline (every number read from the results file, framework-first framing, honest scope, double-blind hygiene, OpenReview field limits). Produces a single click-to-copy HTML artifact the author pastes into OpenReview.
metadata:
  short-description: Generate a verified, double-blind-clean OpenReview submission package
---

# AAAI / OpenReview Submission Package

Use this skill to turn a finished paper and its results file into a **copy-paste-ready OpenReview submission** and to catch the mistakes that waste a submission slot. The output is one self-contained HTML page: each OpenReview field (Title, TL;DR, Abstract, Topics, Authors, Country) in its own click-to-copy block, with character counts, a double-blind checklist, and step-by-step submit instructions. The author does the final click.

This skill distills a real campaign where the abstract went through five drafts because of avoidable errors: fabricated numbers, single-model undersell, LaTeX `---` leaking into plain text, a 299-char TL;DR against a 250 limit, and stale claims that no longer matched the results file.

## Workflow

1. **Locate the two sources of truth, and only trust them.**
   - The **paper source** (`main.tex`) for the claims and framing.
   - The **results file** (`audit.json`, `results.json`, harvested `metrics.npy` — whatever the project treats as ground truth) for every number.
   - Never take a number from the paper prose, a prior summary, memory, or a chat message. Papers drift from their own tables; results files do not.

2. **Verify every quantitative claim in the abstract/TL;DR against the results file (verification discipline).**
   - Re-compute each headline number in code from the results file (gains as `(baseline-ours)/baseline`, "wins N/M cells", "up to X%"). Print expected vs. claimed.
   - This is the single highest-value step. Projects fabricate or drift numbers repeatedly; a reviewer *will* recompute from released data. One wrong bolded number in an abstract is a credibility hit that outweighs any polish.
   - If a claim can't be traced to the results file, cut it or mark it "in flight" — do not ship it.

3. **Frame framework-first, not single-model.**
   - If the contribution is a *mechanism* that generalizes (e.g., a mask/module that drops into multiple backbones), the abstract must lead with the mechanism, not "we tweak model X." "We replace X's attention with Y" reads as a minor delta; "Y is a backbone-agnostic mechanism; it drops unchanged into three backbones and X of Y cells beat every baseline" reads as a contribution.
   - Enumerate the instantiations and the strongest *aggregate* claim the results support (per-cell best across all baselines, not just "beats one backbone").

4. **State scope honestly — report the boundary as a finding.**
   - If the method wins on some data regimes and loses on others, say where and why. A scoped, mechanism-explained result ("SOTA on datasets with a real local dependency graph; reduces to the backbone on diffuse/low-channel data") is stronger and more defensible than an overclaimed sweep a reviewer disproves in one run.
   - Cheap **signal test before any full grid**: 1-seed head-to-head (ours vs. its backbone) on a candidate dataset answers go/no-go for ~$0 before committing a campaign. Kill dead directions early; don't cherry-pick the one cell that survived.

5. **Enforce the OpenReview field constraints (these are hard rules).**
   - **TL;DR ≤ 250 characters.** Count it in code; the platform hard-rejects over-limit. Show the count in the artifact.
   - **Abstract renders markdown** — use `**bold**` on load-bearing claims (numbers, "backbone-agnostic", "zero parameters"). Inline math `$...$` renders.
   - **No LaTeX `---`/`--` em-dash notation in the pasted text** — it appears literally as hyphens. Use the actual em-dash `—`. (The `.tex` file keeps `---`; only the copy-ready plain-text/markdown version is converted.)
   - **Title: strip identifying prefixes** — the model/system name in a double-blind title is deanonymizing; use the descriptive title only.

6. **Run the double-blind hygiene check on the paper PDF/source.**
   - No author names, affiliations, or acknowledgements in the submission build.
   - No identifying URLs (a GitHub username in a repo link deanonymizes even a private repo) — replace with "anonymized supplementary."
   - No "our prior work [self-cite]" phrasing; no leftover venue names from a previous submission target.
   - Confirm the build compiles and the page/format limits are met for the *target* venue's style file (swap placeholder templates before the deadline, not after).

7. **Emit the artifact + submit instructions.**
   - One HTML page, click-to-copy blocks per field, char counts, theme-aware, self-contained.
   - Include: which fields still need author action (e.g., "4 co-authors each need an OpenReview profile linked"), the abstract-vs-full-paper deadline split (abstract days before the PDF), and the exact OpenReview navigation.
   - Keep the artifact synced: every time the paper abstract changes, re-verify numbers and re-publish to the *same* URL.

## Quality requirements

- **Every number in the package traces to the results file, re-computed in code this session.** No exceptions, no "it was right last time."
- **The TL;DR is measured, not estimated, to be ≤250 characters.**
- **Framework-level claims use the strongest *honest* aggregate** the results support, and scope/negative results are stated, not hidden.
- **The pasted abstract contains zero LaTeX artifacts** (`---`, `\emph`, `~\cite`, `\%`); it is clean markdown + Unicode.
- **Double-blind is verified on the actual build**, not assumed.
- **The author's only remaining action is the submission click** — every field is copy-ready.

## Pipeline lessons that protect submission numbers

Numbers reach the abstract through an experiment pipeline; these failures silently corrupt them and are worth checking when results look "off":

- **`FAIL` must not read as done.** A crashed run that logs an empty/`0.0000` result which then satisfies a done-check is never retried, and a min-MSE ranking may even let the `0.0000` *win* the cell. Detect empty output explicitly; release the claim on failure.
- **One experiment queue per box.** Stacking multiple 8-GPU queues oversubscribes CPU/IO and mass-crashes runs (whose failures then look like "the method lost").
- **Fake 3-seed.** Separate processes with a fixed global seed produce bit-identical "seeds"; real variance needs the framework's own multi-iteration seeding. Bit-identical seed triples in a results file are a red flag.
- **Missing-value contamination.** Datasets that encode missing readings as 0 (e.g., METR-LA) bias evaluation and corrupt correlation-derived structure; mask or interpolate before both training and structure estimation.
- **Config-collision in harvest.** Different configs sharing a result key silently merge; key on a config fingerprint, and prefer the ≥3-seed entry the paper tables actually render.

## Conference → journal positioning

If a framework result is promoted to the conference paper, the extended/benchmark story becomes the journal (conference→journal pipeline). Record which paper owns which claim so the two don't double-publish the same headline. Do this *before* submission while both drafts are still editable.
