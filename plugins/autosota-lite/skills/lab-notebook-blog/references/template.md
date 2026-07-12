# Lab Notebook Post — Template & Checklist

Use this skeleton verbatim, filling in the brackets. Match the host repo's existing
Jekyll conventions (layout name, permalink style, MathJax setup) before publishing.

## Jekyll front matter

```yaml
---
layout: post
title: "Lab Notebook: Every Active Track, Explained From Scratch"
date: YYYY-MM-DD
tags: [<domain>, <method-1>, <method-2>, lab-notebook]
---
```

## Section skeleton

```markdown
> **TL;DR.** <N> concurrent tracks, serving <goals: papers / competition /
> platform / other>. <One-sentence project state.> This post explains each
> track from first principles — no prior context assumed — with its status and
> what it feeds. <The single most newsworthy or uncomfortable headline, stated
> plainly.>

**Minimal shared context** (60 seconds): <the domain, in one sentence; the
flagship result/artifact, with its one headline number; the evaluation
methodology every section relies on, with the one mechanism a reader must
understand>. Everything below builds on, stress-tests, or extends that setup.

---

## 1. <Track name>

**What it is.** <2–3 sentences, first principles. Gloss every term of art
inline on first use.>

**Why it exists.** <The question it answers, or the failure/gap that forced
it. Tell the honest causal story.>

**Status.** <shipped | done | in flight | launching | planned>. <Verified
numbers only, with n / units / baseline / caveats. If planned: time estimate.>

**Feeds.** <GOAL category: competition | paper | platform | other> — <the
specific consumer: which paper, which model line, which deployment>.

## 2. <Track name>
<same four-part structure — repeat for every active track>

## <K>. Planned: <future track name>
<same four-part structure; Status must include an explicit time estimate,
e.g. "~2 GPU-days on one 3090, after track 5 lands", and the label "planned">

## <last>. The papers (if the project has a paper goal)
<one paragraph per venue/deadline; which tracks rewrite which numbers; note
anonymity constraints explicitly ("under anonymous review, so no repository
links here")>

---

## The dependency map

<Pipelines in prose, grouped by goal, referencing tracks by section number:>
**<Goal A> → <output>:** track (i) produces X, tracks (j),(k) supply Y, flowing
into Z — <gating condition, e.g. "nothing submits until the re-gated table
lands">. **<Goal B> → <output>:** ... **<Goal C> → <output>:** ...
<Close with the one-sentence through-line all tracks share.>
```

## Per-track writing rules

- **What it is** answers "explain this to a smart outsider in 3 sentences".
  If a sentence needs a second term of art to gloss the first, restructure.
- **Why it exists** is a question or a failure, never "because it seemed
  interesting". If the track exists because a previous attempt failed, say what
  failed and why (with the diagnosed mechanism if known).
- **Status** numbers: each one must have been read from a result JSON/log in
  this session. Keep a private ledger while drafting:

  | # | Claim in post | Source file | Value in file |
  |---|---------------|-------------|---------------|

- **Feeds** must name a goal category AND a concrete consumer. "Feeds the
  paper" is incomplete; "Feeds the AAAI-27 eval-wall paper (section 5 numbers)"
  is complete.

## Pre-publish checklist

Run every item; do not publish with an unchecked box.

- [ ] **Traceability:** every number in the post appears in the source ledger
      with a file path, and the value in the post matches the file exactly
      (re-open each file and compare; do not trust the draft).
- [ ] **Coverage:** every active/queued workstream found in plans, results
      dirs, memory notes, and running jobs has a numbered section; none
      silently dropped (including stalled or embarrassing ones).
- [ ] **Goals categorized:** every track's **Feeds** line names one of
      competition / paper / platform / other, plus a concrete consumer.
- [ ] **Future tracks:** all planned tracks included, each labeled "planned"
      with an explicit time estimate.
- [ ] **First principles:** a cold reader test — every acronym, codename, and
      term of art is glossed on first use or covered by the shared-context
      paragraph.
- [ ] **Honesty:** corrections and nulls are stated as prominently as wins;
      no in-flight track carries a projected number.
- [ ] **Dependency map:** every numbered track appears in the map; map claims
      match the body's **Feeds** lines.
- [ ] **No secrets / anonymity leaks:** no credentials, tokens, hostnames,
      box IDs/IPs, internal URLs; no links or names that deanonymize
      under-review submissions; no other party's private info.
- [ ] **Jekyll:** front matter valid; date/filename consistent
      (`YYYY-MM-DD-slug.md`); relative links point at `.html` targets as the
      repo's existing posts do; renders correctly on Pages after push.
