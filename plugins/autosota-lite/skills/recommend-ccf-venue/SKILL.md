---
name: recommend-ccf-venue
description: Recommend and rank the next CCF-listed or strategically relevant conference, journal, special issue, workshop, or artifact track for an existing research paper. Use when choosing where to submit or resubmit a paper, comparing conference versus journal routes, planning around deadlines, routing a portfolio across graph/structural-entropy/ML/RL/robotics/bio/game/audio venues, or checking whether a venue is timely, in scope, and realistically attainable.
---

# Recommend a CCF Venue

Produce an evidence-based submission route, not a prestige-only venue list. Match
the paper's actual contribution, evidence, maturity, and calendar to current venue
requirements.

## Establish the paper profile

Read the manuscript, abstract, evidence ledger, or repository when available.
Extract:

- primary and secondary research fields;
- contribution type: method, theory, diagnostic, benchmark, system, resource, or
  domain application;
- strongest verified results and weakest evidence boundary;
- domain-specific experiments already present;
- conference history, simultaneous submissions, and extension constraints;
- readiness date, desired decision speed, CCF preference, and journal tolerance.

Do not infer missing experiments or claim that a generic method fits a domain venue
without domain data, metrics, and baselines.

## Build the candidate set

Read `references/ccf-cross-field-deadline-tracker-2026-05-28.md` as a historical
candidate index when the paper concerns graph mining, structural entropy, ML/RL,
robotics, bioinformatics, games, audio, multimedia, or related journals. Its dates
are a snapshot, never current authority.

Add candidates from the current official CCF list and the paper's actual field.
Include both:

1. the best next conference route; and
2. one rolling or fixed-deadline journal route when the work is mature enough.

Keep artifact, demo, workshop, challenge, short-paper, and full-paper tracks
separate. Never present one as a substitute for another without labeling it.

## Verify every live fact

Browse before recommending. For each finalist, verify from primary sources:

- current edition and official venue page;
- abstract, paper, supplementary, and timezone deadlines;
- track scope and paper type;
- page limits, anonymity, dual-submission, resubmission, and author limits;
- current CCF category/rank from the official CCF list when rank matters;
- journal or special-issue status from the publisher's call page.

Use deadline aggregators only to discover candidates. Cite the official CFP or
publisher page in the answer. Mark an unannounced deadline `TBD`; never promote a
date extrapolated from a previous year as confirmed.

## Apply hard gates

Remove or clearly block a candidate when:

- its deadline has passed or the manuscript cannot be ready in time;
- the contribution is outside scope;
- a required domain evaluation is missing;
- an archival dual submission or overlapping-submission policy prevents it;
- the intended author list violates a submission cap;
- the manuscript would require a qualitatively different paper rather than a
  legitimate reframing or extension.

For a withdrawn, deleted, rejected, or concurrently submitted paper, verify the
venue's resubmission and archival-overlap rules before proposing a new target.

## Score viable candidates

Score each candidate out of 100:

| Dimension | Points | Question |
|---|---:|---|
| Scope fit | 25 | Is the central contribution native to the venue? |
| Evidence fit | 20 | Are the datasets, baselines, metrics, and scale credible there? |
| Contribution fit | 15 | Does the venue value this paper type? |
| Selectivity readiness | 15 | Is the novelty/evidence package competitive? |
| Deadline readiness | 10 | Can a verified submission be completed without rushing? |
| CCF/strategic value | 10 | Does it meet the author's ranking and career objective? |
| Logistics | 5 | Are format, review cycle, and publication model acceptable? |

Do not let CCF rank override scope. A lower-ranked native venue is usually safer
than a prestigious venue requiring a fictional framing.

Assign one verdict:

- `SUBMIT`: strong fit and ready;
- `SUBMIT AFTER FIXES`: viable with named, achievable additions;
- `MONITOR`: strong candidate whose official CFP/deadline is not open;
- `JOURNAL ROUTE`: mature work better served by a full-length version;
- `DO NOT ROUTE`: scope, evidence, policy, or timing mismatch.

## Return a decision-ready recommendation

Lead with one primary recommendation and one fallback. Then provide a compact
table containing:

| Rank | Venue/track | Verified deadline | CCF status | Score | Verdict | Why it fits | Required changes |
|---:|---|---|---|---:|---|---|---|

Finish with:

1. a backward plan from the nearest verified deadline;
2. the three highest-value manuscript changes for the primary venue;
3. a rejected-candidate list explaining tempting but unsuitable venues;
4. official source links and the date each was checked;
5. uncertainties requiring author confirmation.

For a portfolio, prevent thin slicing and conflicting simultaneous submissions.
Map each paper to a distinct claim owner and venue route, flag substantial overlap,
and state which papers should be combined, paused, or converted into journal
extensions.

## Integrity rules

- Never fabricate CCF ranks, deadlines, acceptance rates, special issues, or CFPs.
- Never recommend omitting a genuine author to evade a submission cap.
- Never treat a predicted deadline as official.
- Never recommend superficial domain relabeling.
- Never guarantee acceptance; express fit and risk separately.
- Prefer honest scope and a coherent paper over maximizing the number of
  submissions.
