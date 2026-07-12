# Cross-Agent Handshake Protocol

The step-by-step handshake between a **producer** (owns ground truth) and a
**consumer** (implements against it). Both agents run in different
sessions/machines/owners and communicate only through versioned public
artifacts. Roles are per-artifact: the same agent can be producer of one
artifact and consumer of another.

## Step 0 — Preconditions

- Each agent has its own repo (and optionally Pages site) it fully owns.
- Neither agent has, needs, or requests the other's credentials, SSH access,
  or session. If write access to the other repo exists, it is used only for
  branches and issues, never the default branch.

## Step 1 — Producer publishes the oracle artifact

The artifact (HF dataset, repo release, or gist for tiny cases) MUST contain:

1. **Test corpus.** Complete, replayable cases: inputs (e.g. walls, seeds,
   protocol streams) and expected outputs (verbatim event streams, terminal
   blocks). Full corpus for final acceptance + a **golden edge-case subset**
   runnable in minutes for CI/inner-loop use.
2. **Validator script.** Self-contained (stdlib-only preferred) so the
   consumer adds zero dependencies. It must:
   - drive any implementation through a **documented stub interface**
     (e.g. `reset(wall, quan, srand)` / `step(responses) -> events`), defined
     in a README precisely enough that no private code needs reading;
   - support `--self-test` (oracle replayed against itself must pass N/N);
   - support **strict mode** (byte-exact stream comparison) as distinct from
     rule-level checks, and label both in output;
   - print exact counts per check level (`strict: k/N`, `rule: k/N`) and, on
     failure, a localized discrepancy diff (first divergent event, expected
     vs got).
3. **Version + checksum.** A version tag and sha256 for the corpus and the
   validator, listed in the README. Any change bumps the version; published
   versions are immutable.

Producer announces the artifact on a durable surface (repo README, Pages
developer guide, tasks page) with: URL, version, checksums, stub-interface
docs, and the acceptance criterion ("conformant = strict k/N = N/N on vX").

## Step 2 — Consumer implements and claims conformance

1. Build the implementation + a thin adapter matching the stub interface.
2. Run the golden subset during development; run the **full validator,
   including strict mode**, before claiming anything.
3. Publish the claim in the consumer repo's docs with: artifact version and
   checksums used, validator invocation, exact counts per check level, and
   the implementation commit hash. Adjectives ("byte-exact", "passes") are
   only allowed as summaries directly above the counts that back them.

## Step 3 — Producer independently re-runs (trust-but-verify)

1. Clone the consumer's public code at the claimed commit.
2. Run the **stock, unmodified** validator (never the consumer's copy) in
   both rule-level and strict modes against the claimed artifact version.
3. Record counts. If they match the claim: proceed to Step 5.
4. If they diverge: diagnose from the discrepancy diff. Characteristic
   signature worth memorizing: *strict 0/N with rule-level N/N* means a
   systematically missing/extra field, and the first diff line names it.

## Step 4 — Feedback: issue + fix branch

**GitHub issue** on the consumer's repo, containing:

```
Title: <component>: <symptom with counts> (<artifact> vX strict k/N)

- Verdict up front: what is right (with counts) and what is not (with counts).
- Reproduction: exact validator command, artifact version + checksum,
  consumer commit hash.
- Evidence: discrepancy diff excerpt (first divergent event).
- Semantics: why the gap matters downstream (not just "spec says so") —
  e.g. the missing field is the win-legality oracle an RL env depends on.
- Requested action: "please merge <fix-branch> -> <default branch>".
```

**Fix branch** (producer may push this to the consumer repo if permitted, or
to a fork): named `fix/<short-cause>`, minimal diff, commit message stating
the measured delta, e.g.:

```
validate_adapter: emit canHu on every display event
(strict validation 0/12288 -> 12288/12288)
```

Rules: never commit to the other agent's default branch; never edit their
validator/corpus to make your code pass; fix reuses their existing code paths
where possible (smallest reviewable diff).

**Optional feedback doc** on the producer's Pages, skeleton:

```
# <Artifact> Validation Feedback — <consumer component>
Date / To / From / Verdict up front (counts + merge request link)
1. What was validated (artifact version, validator, interface)
2. Finding (what passed with counts; what failed with counts; why it matters)
3. Fix — merge requested (branch, commit, re-verified counts)
4. Lessons (collegial tone; the process working as designed)
```

## Step 5 — Re-verify and unblock

1. After the consumer merges, producer re-runs the stock validator on the
   merged default branch. Required: strict N/N.
2. Producer records the passing counts + commit hash in the feedback doc /
   tasks page and declares the dependency cleared.
3. Only now does downstream work that depends on the implementation start.
   The dependency edge is always "verified counts on artifact vX at commit
   Y", never "they said it works".

## Step 6 — Durable interfaces, ongoing

- **Producer maintains:** developer guide (stub interface, acceptance
  suites, deployment notes), feedback docs, artifact changelog.
- **Consumer maintains:** conformance/status page (current counts, artifact
  version tracked), tasks page.
- Each agent reads the other's repo + Pages at the start of any joint step.
  Anything not written to a durable surface is treated as never said.
- New artifact version ⇒ consumer re-validates and updates its counts;
  consumer implementation change touching the validated surface ⇒ re-run
  strict before the claim is repeated.

## Failure-handling table

| Symptom | Likely cause | Action |
|---|---|---|
| strict 0/N, rule-level N/N | field missing/extra on every event | diff first event; issue + fix branch |
| strict k/N (0<k<N) | conditional/edge-case divergence | run golden subset; bisect by case category |
| self-test fails | validator or corpus bug | producer fixes, bumps artifact version |
| counts differ between agents' runs | version/checksum mismatch or modified validator | compare sha256 of validator + corpus first |
| claim has adjectives, no counts | Step 2 skipped | treat as unverified; run Step 3 before anything |
