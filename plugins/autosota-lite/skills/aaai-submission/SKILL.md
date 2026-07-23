---
name: aaai-submission
description: Prepare and audit an AAAI-27 or OpenReview double-blind submission from an existing author-written paper and verified results. Use for copy-ready OpenReview fields, author/profile readiness, topic selection, reciprocal-reviewer nomination, supplement packaging, external-repository-link prohibition, reproducibility checklist checks, anonymity, file limits, and final desk-rejection-risk review.
---

# AAAI / OpenReview Submission

Prepare a submission whose claims, metadata, files, and attestations agree. Treat
the live venue form and current author kit as authoritative; do not rely on dates,
limits, topics, or policies remembered from an earlier year.

## Read the live constraints

For AAAI-27, read [the captured OpenReview form](references/aaai27-openreview-form.md).
If the live form or official author kit is available, compare it with the snapshot
and record any difference. Never silently resolve conflicting deadlines or time
zones. Report both sources and ask the author to verify the venue's authoritative
deadline when they disagree.

## Establish sources of truth

Use:

1. the paper source and compiled submission PDF for wording, claims, anonymity,
   page count, and self-containment;
2. result artifacts for every quantitative claim;
3. the live OpenReview form for fields, cardinalities, file channels, and limits;
4. the current official author kit for template and checklist requirements;
5. author-confirmed profile, conflict, simultaneous-submission, and reciprocal-
   reviewer information.

Never infer an attestation, reviewer qualification, author profile status, or
country. Mark unresolved fields `AUTHOR_ACTION_REQUIRED`.

## Verify the claims

- Recompute every abstract and TL;DR number from the result artifact in this session.
- Print the derivation, expected value, displayed value, and rounding rule.
- Remove or flag a claim that cannot be traced.
- State scope and negative results that materially qualify the headline.
- Lead with the contribution type: mechanism, diagnostic, or benchmark—not an
  incidental backbone or implementation.

## Build the OpenReview field package

Prepare copy-ready title, authors, TL;DR, abstract, primary topic, one to five
secondary topics, and countries of institutions. Preserve TeX only where the live
field explicitly supports it. Count against limits read from the current form or
schema; do not hard-code a historical limit.

Check that every author already has an up-to-date OpenReview profile containing
the required publication name, current position, institution-affiliated email,
and DBLP URL when available. Incomplete profiles are a desk-rejection risk.

## Package submission files

- Upload the main paper as PDF.
- Upload the answered standalone reproducibility checklist.
- Keep the main paper self-contained. A technical supplement is optional,
  reviewers need not read it, and the current AAAI-27 form limits it to 10 MB.
- A media supplement is optional and limited to 50 MB.
- A code/data supplement is optional, archive-based, and limited to 50 MB.

### Prohibit external paper-source/data repositories

Do not link the submission's source code or data to any external repository. This
includes public, private, and anonymized services such as GitHub, AnonymousGitHub,
GitLab, Hugging Face repositories, OSF, or similar hosts. Package reviewer-facing
code, scripts, data, and instructions inside the Code and Data Supplement archive.

Scan the paper, OpenReview fields, supplements, README files, scripts, notebooks,
and archive contents for repository URLs. Distinguish citations to third-party
prior work from links to this submission's artifacts, but allow **zero** external
links to the paper's own source/data. Do not replace them with an anonymized link;
remove them and point to the uploaded supplement.

Run `scripts/audit_submission.py` on the metadata and all text-bearing submission
materials. Treat every reported repository URL as blocking until a human confirms
it is a conventional third-party citation rather than a paper-artifact link.

## Verify reciprocal-reviewer obligations

Before the live form's nomination lock:

- determine whether any author satisfies the stated archival-publication threshold;
- exclude SPCs, ACs, and organizers;
- verify the candidate with the official qualification checker and DBLP;
- obtain the candidate's agreement to the stated reviewing load;
- select either a qualified nominee or the explicit no-qualified-author declaration.

Do not guess. The form warns that failing to nominate an available qualified author,
or failure by the nominee to complete reviews, can cause desk rejection.

## Verify policy attestations

Require author confirmation that:

- all profiles are complete;
- neither the manuscript nor a substantially similar version is under review at
  another archival venue;
- relevant simultaneous submissions are cited anonymously as `under review`;
- conflicts are complete;
- the displayed license is accepted.

## Compile and inspect

Use the current official AAAI template in submission mode. Compile the actual
submission source, check page count and references, render the PDF, and inspect
every page. Verify no author names, affiliations, acknowledgements, identifying
artifact URLs, PDF metadata, hidden annotations, or deanonymizing self-citations.

## Deliver

Produce:

- a copy-ready field artifact with live character counts;
- a field-by-field source ledger;
- a file/size manifest;
- an external-link scan report;
- a profile and reciprocal-reviewer checklist;
- a policy-attestation checklist;
- a short `BLOCKING`, `AUTHOR_ACTION_REQUIRED`, and `READY` summary.

The author performs the final submission click.
