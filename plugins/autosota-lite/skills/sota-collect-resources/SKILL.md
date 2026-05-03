---
name: autosota-agent-resource
description: Implement AgentResource from AutoSOTA to bridge static literature and executable environments. This skill manages paper-to-repository grounding, readiness assessment, and external resource acquisition (datasets, weights).
---

# AutoSOTA AgentResource: Bridging Static Literature and Executable Environments

Use this skill to automate the transition from a research paper (PDF/URL) to an execution-ready experiment environment. This follows the architecture defined in Section 2.2 of the AutoSOTA paper.

## Core Responsibilities

- **Grounding**: Map a paper to its official code repository.
- **Curation & Readiness**: Assess if a repository is actionable for reproduction.
- **External Resource Acquisition**: Discover and download heavyweight dependencies like datasets and pre-trained weights.

## 1. Paper-to-Repository Grounding

1. **Link Extraction**: Scan paper front matter, footnotes, and project pages (e.g., github.io) for GitHub links.
2. **Repository Selection**: If multiple links exist, select the official/relevant repository.
3. **Normalization**: Shallow-clone the repository into a standardized local structure.
4. **Readiness Assessment**: Use abstract, file tree, and README to judge if the repository is a placeholder or actionable.

## 2. External Resource Acquisition

Modern AI repositories rarely contain datasets or weights. This module uses a two-phase process:

### Phase I: Symbolic Resource Discovery (Zero-Download)
1. **Dependency Parsing**: Inspect the repository structure, `requirements.txt`, `environment.yml`, and evaluation manifests.
2. **Global Resource Registry**: Create a metadata ledger mapping assets to their unique sequence IDs, source URLs, types (dataset/model), and estimated sizes.

### Phase II: Physical Download Execution
1. **Gated Selection**: Filter tasks based on estimated size to prevent runaway downloads.
2. **Semantic Storage**: Route resources into `datasets/`, `models/`, `checkpoints/`, or `misc/`.
3. **Polymorphic Retrieval**:
    - **Rule-based**: Use `huggingface-cli` for HF, `curl` for HTTP/HTTPS.
    - **LLM-driven**: Generate Python scripts for non-standard/obfuscated sources.

## Red Lines for Resource Acquisition

- Never download resources that exceed the pre-defined budget or local storage limits.
- Never modify the repository's internal structure in a way that breaks its own relative path assumptions.
- Respect the scientific protocol: ensure datasets match the versions mentioned in the paper.

## Output Format

Every execution of this skill should update the project's `resource_map.md` and `autosota.yaml` (if applicable) and end with the following summary:

```text
Status: <READY|BLOCKED|COMPLETE>
Paper Identity: <Title/ArXiv ID>
Repository Grounded: <GitHub URL>
Readiness Score: <High/Medium/Low - Reason>
External Resources Discovered: <List of URLs/Types>
Download Status: <Success/Partial/Failed - Artifact Paths>
Next Action: <Next step for environment initialization or baseline reproduction>
```
