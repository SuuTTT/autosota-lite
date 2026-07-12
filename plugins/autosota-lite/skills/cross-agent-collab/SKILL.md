---
name: cross-agent-collab
description: Use when two autonomous agents (different sessions, machines, or owners) must build against each other's work — e.g. one agent owns a reference implementation or dataset and another must implement a compatible engine, environment, client, or pipeline. Covers publishing machine-checkable oracle artifacts (HF datasets, gists), validator scripts with documented interfaces, trust-but-verify re-runs of conformance claims, feedback via GitHub issues plus fix branches (never pushing to the other agent's master), and docs pages as the durable cross-agent interface. Applicable to any producer/consumer handshake between agents that do not share credentials, boxes, or mutable state.
metadata:
  short-description: Coordinate two agents via oracle artifacts + verification
---

# Cross-Agent Collaboration

Use this skill to coordinate two autonomous agents that cannot share a session, a machine, or credentials — a **producer** who owns the ground truth (reference data, a judge, a spec) and a **consumer** who must implement against it. The coordination medium is exclusively **versioned public artifacts** (GitHub repos/issues/branches, HuggingFace datasets, Pages docs) plus **machine-checkable acceptance tests**. The pattern distilled here caught a real integration bug the same day it shipped: a consumer engine claimed "byte-exact" replay, the producer's independent strict re-run read **0/12,288** (one missing field that turned out to be safety-critical), and an issue + fix branch got it to 12,288/12,288 without either agent touching the other's session.

## Workflow

1. **Producer: publish a machine-checkable oracle artifact**
   - Package the ground truth as a versioned, self-contained artifact: an HF dataset or repo release containing (a) the full test corpus (e.g. 12,288 replayable games: inputs, verbatim expected event streams, expected terminal outputs), (b) a **golden edge-case subset** small enough to run in minutes, and (c) a stdlib-only **validator script** that drives any conforming implementation and reports exact pass counts.
   - Document the **implementation stub interface** the validator expects (e.g. `reset(wall, quan, srand)` / `step(responses)`) precisely enough that the consumer never needs to read the producer's private code.
   - The validator must have a `--self-test` mode (oracle vs itself must pass N/N) and a **strict mode** (byte-exact stream comparison), and it must print counts, not verdict adjectives.
   - Checksum and version the artifact. Never hand over mutable state (a shared box, a live DB, an unversioned scratch dir).

2. **Consumer: implement against the artifact, claim conformance with numbers**
   - The consumer builds its implementation plus a thin adapter matching the documented stub interface, runs the producer's validator locally, and publishes the claim **with exact counts and the artifact version/checksum used** — "12,288/12,288 strict on testset v1.2", not "byte-exact".
   - The claim lives in a durable place the producer can read: the consumer's repo docs or Pages, not a chat message.

3. **Producer: independently re-run the validator (trust-but-verify)**
   - Before depending on the consumer's implementation, the producer re-runs the **unmodified stock validator** against the consumer's public code, including **strict mode**, and records counts.
   - This step is not optional courtesy — it is where the real bug surfaced: the consumer's docs claimed byte-exact replay, but strict mode had never actually been executed; the producer's re-run read 0/12,288 (all rule-level checks green, every display event missing the judge's `canHu` win-eligibility field).
   - Diagnose from the validator's discrepancy diff. A clean signal like "0/N strict, N/N rule-level" localizes the bug immediately.

4. **Feedback: GitHub issue with evidence + a fix branch — never touch their master**
   - File an issue on the consumer's repo containing: exact counts before, the discrepancy diff excerpt, the **reproduction command** (validator invocation, artifact version), and the semantic argument for why the gap matters (e.g. why the "cosmetic" field is load-bearing for RL legality).
   - Push the fix to a **branch** (e.g. `fix/canhu-strict`) with a commit message stating the measured delta ("strict validation 0/12288 → 12288/12288"), and **request merge in the issue**. Never merge into or push to the other agent's default branch yourself — their master is theirs, even when you have write access.
   - Optionally publish a feedback doc on your own Pages telling the full story (verdict up front, what was validated, finding, fix, lessons) — see [references/protocol.md](references/protocol.md) for the doc skeleton.

5. **Re-verify strict pass before depending on it**
   - After the consumer merges, the producer re-runs the stock validator once more on the merged default branch and records the passing counts. Only then does the downstream work (e.g. an RL pilot on the consumer's engine) get unblocked.
   - The dependency edge is: *verified counts on a versioned artifact*, never *the other agent said it works*.

6. **Docs pages as the durable interface**
   - Each side maintains public docs the other reads: the producer's **developer guide** (how to implement the stub, how to run acceptance suites), the producer's **feedback doc** (validation verdicts), and each side's **tasks/status page**. Agents read each other's repos and Pages; they never share credentials, sessions, or boxes.
   - Every cross-agent request or result must land in one of these durable surfaces. If it only exists in a conversation, it does not exist.

## Anti-Patterns (each observed in the wild)

- **Claiming verification without running the strict mode.** "Byte-exact" was written in docs on the strength of rule-level checks; the strict run — which costs minutes — had never been executed and failed 0/12,288. Rule-level pass and byte-exact pass are different theorems; claim only what you ran, with the count.
- **Assuming metadata fields are cosmetic.** The missing `canHu` array looked like display metadata; it is the per-step win-legality oracle, safety-critical for any RL environment built on the engine. Default: reproduce every field the oracle emits, *then* argue about whether it matters.
- **Sharing mutable state instead of versioned artifacts.** A shared box, live directory, or unversioned dataset makes claims unreproducible and lets one agent silently break the other. Everything crossing the agent boundary is versioned, checksummed, and immutable per version.
- **Merging into the other agent's master yourself.** Even with access, the fix goes on a branch and the merge is requested via issue. Ownership boundaries are what make two-agent claims auditable.
- **Verdict adjectives instead of counts.** "Passes", "works", "byte-exact" are not evidence. "12,288/12,288 strict, validator sha256 `…`, testset v1.2" is.

## Quality Bar

- **Artifacts versioned and checksummed.** Every artifact crossing the agent boundary carries a version and a checksum, and every claim names the version it was measured on.
- **Validation counts reported exactly.** Pass/fail totals as `k/N` for each check level (rule-level, strict), never rounded, never summarized as adjectives. Self-test result reported alongside.
- **Issues contain reproduction commands.** Any agent (or human) reading the issue can re-run the exact validator invocation and get the same counts — command line, artifact version, code commit.
- **Independent re-runs, both directions.** The producer re-runs before trusting a conformance claim; the consumer re-runs after merging a producer-supplied fix. No claim is depended on by the agent who didn't run it.
- **No credential or session sharing.** All coordination through public GitHub/HF/Pages surfaces. If a step seems to require the other agent's box, redesign the step.
- Before relying on this skill in a new pairing, run the self-check in [references/test-scenario.md](references/test-scenario.md) end to end.

## Reference Files

- [references/protocol.md](references/protocol.md): the step-by-step producer/consumer handshake, artifact and validator requirements, issue and feedback-doc skeletons.
- [references/test-scenario.md](references/test-scenario.md): a runnable self-check — publish a tiny oracle, write a validator, play the consumer with a seeded bug, and show the issue + fix-branch loop catches it.
