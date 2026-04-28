# Dependency And Bit-Rot Policy

Use this policy when creating a clean one-file implementation or repairing an older research repo.

## Runtime Base

Default to Vast.ai's standard PyTorch image family:

```text
vastai/pytorch:<project-selected-tag>
```

Choose and pin the exact tag per project after checking the current Docker Hub or Vast.ai docs. Record the tag in `implementation_contract.md`, `porting_notes.md`, and run logs. Do not assume a tag from memory, and do not assume that the untagged image exposes a `python` command or a system `python3` with `torch` importable.

Record:

- Docker image and tag.
- Python version.
- CUDA, cuDNN, PyTorch, torchvision, and torchaudio versions when present.
- GPU model and driver as reported by `nvidia-smi`.
- Added pip packages and versions.

Run this probe before installing research dependencies:

```bash
for py in /opt/conda/bin/python /venv/main/bin/python python python3; do
  if command -v "$py" >/dev/null 2>&1 || [[ -x "$py" ]]; then
    "$py" - <<'PY' && break
import sys
import torch
print("python", sys.executable)
print("torch", torch.__version__)
print("cuda", torch.version.cuda)
PY
  fi
done
```

If no interpreter can import `torch`, stop and fix the runtime contract before porting the research code.

## Minimal Install Rule

Start with packages already available in the selected Vast.ai image. Add only what the one-file implementation needs.

Common small additions:

- `gymnasium` for RL environments.
- `tyro` for dataclass CLI parity with CleanRL.
- `tensorboard` for scalar logging.
- `optax` for JAX optimizers.
- `flax` or `equinox` only when they simplify JAX model code.
- `pytest` only when tests are part of the deliverable.

Avoid in the canonical implementation unless required by the source method:

- Hydra or large config stacks.
- Lightning or accelerator frameworks.
- WandB, MLflow, or hosted logging clients.
- Notebook-only dependencies.
- Full source-repo installs just to reach a small utility.
- Old CUDA or PyTorch downgrades as a first response to bit rot.

## Bit-Rot Fix Order

1. Run the original minimal command and capture the failure.
2. Identify whether the break is API drift, dependency resolution, missing data, hardware assumption, or source bug.
3. Prefer current API replacements over old version pinning.
4. Add a tiny compatibility shim only when it keeps the clean implementation readable.
5. Pin the smallest set of versions needed for repeatability.
6. Verify import, CLI help, one batch, one train step, and one eval step.
7. Record the fix and remaining risk in `porting_notes.md`.

## Requirements File Shape

Keep project requirements short and explicit:

```text
# Base image: vastai/pytorch:<tag>
# Generated for: <implementation file>
gymnasium==<version>
tyro==<version>
tensorboard==<version>
```

For JAX variants, separate framework-specific packages:

```text
# Base image: vastai/pytorch:<tag>
# JAX package selection depends on CUDA support in the selected image.
jax==<version>
jaxlib==<version>
optax==<version>
```

Do not vendor wheel files or large package caches into the implementation library.
