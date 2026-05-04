---
name: util-hf-dataset
description: Create, upload, download, and load datasets on HuggingFace Hub. Use this when you need to persist RL/ML episode data, share datasets between machines (e.g. Vast.ai → local), or load existing datasets for training. Handles npz/pkl/parquet formats, large dataset chunking, and streaming. Requires HF_TOKEN in .env.local.
---

# HuggingFace Dataset Skill

Upload, download, and load datasets from HuggingFace Hub. Designed for RL episode data (npz files), model checkpoints, and experiment artifacts.

## Quick Reference

```bash
# Load token
set -a && source /workspace/autosota-lite/.env.local && set +a

# Upload a folder of npz files
python3 hf_upload.py --folder /data/episodes --repo sudingli21/carracing-v3-random-10k

# Download a dataset
python3 hf_download.py --repo sudingli21/carracing-v3-random-10k --dest /data/episodes

# Load in Python for training
python3 -c "from hf_load import load_episodes; eps = load_episodes('sudingli21/carracing-v3-random-10k')"
```

## Token Setup

`HF_TOKEN` must be in `/workspace/autosota-lite/.env.local`:
```
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
Get write token at: https://huggingface.co/settings/tokens

---

## Upload

### Upload folder of npz episodes (recommended for RL data)

```python
import os
from huggingface_hub import HfApi, create_repo

HF_TOKEN = os.environ["HF_TOKEN"]
REPO_ID   = "sudingli21/carracing-v3-random-10k"   # username/dataset-name
FOLDER    = "/workspace/vastai-job/episodes"        # local folder with .npz files

api = HfApi(token=HF_TOKEN)

# Create repo if it doesn't exist
create_repo(REPO_ID, repo_type="dataset", private=False, exist_ok=True, token=HF_TOKEN)

# Upload (resumes automatically on re-run — already-uploaded files are skipped)
api.upload_folder(
    folder_path=FOLDER,
    repo_id=REPO_ID,
    repo_type="dataset",
    commit_message="Add CarRacing-v3 episodes",
    ignore_patterns=["*.pyc", "__pycache__"],
)
print(f"Uploaded to: https://huggingface.co/datasets/{REPO_ID}")
```

### Upload single file

```python
api.upload_file(
    path_or_fileobj="/path/to/ep_000000.npz",
    path_in_repo="data/ep_000000.npz",
    repo_id=REPO_ID,
    repo_type="dataset",
)
```

### Upload large dataset in chunks (>50GB)

```python
import os, glob
from huggingface_hub import HfApi, create_repo

api = HfApi(token=os.environ["HF_TOKEN"])
files = sorted(glob.glob("/data/episodes/*.npz"))

# Upload in batches of 1000 files
BATCH = 1000
for i in range(0, len(files), BATCH):
    batch = files[i:i+BATCH]
    # Write batch to temp dir with symlinks
    import tempfile, shutil, pathlib
    with tempfile.TemporaryDirectory() as tmp:
        for f in batch:
            shutil.copy2(f, tmp)
        api.upload_folder(folder_path=tmp, repo_id=REPO_ID, repo_type="dataset",
                          commit_message=f"Add batch {i//BATCH}")
    print(f"Uploaded batch {i//BATCH+1}/{len(files)//BATCH+1}")
```

---

## Download

### Download entire dataset

```python
from huggingface_hub import snapshot_download

local_dir = snapshot_download(
    repo_id="sudingli21/carracing-v3-random-10k",
    repo_type="dataset",
    local_dir="/workspace/world_model/data/episodes",
    token=os.environ.get("HF_TOKEN"),  # not needed for public repos
)
print(f"Downloaded to: {local_dir}")
```

### Download specific files (partial download)

```python
from huggingface_hub import hf_hub_download

# Download one file
path = hf_hub_download(
    repo_id="sudingli21/carracing-v3-random-10k",
    filename="ep_000000.npz",
    repo_type="dataset",
    local_dir="/data/episodes",
)
```

### CLI download

```bash
pip install -q huggingface_hub
huggingface-cli download sudingli21/carracing-v3-random-10k \
    --repo-type dataset --local-dir /workspace/world_model/data/episodes
```

---

## Load for Training

### Load npz episodes lazily (memory-efficient)

```python
import os, glob, numpy as np

def load_episodes(local_dir: str):
    """Iterate over episodes without loading all into RAM."""
    for path in sorted(glob.glob(os.path.join(local_dir, "*.npz"))):
        ep = np.load(path)
        yield ep["obs"], ep["actions"], ep["rewards"], ep["dones"]

# Usage in training loop
for obs, actions, rewards, dones in load_episodes("/data/episodes"):
    # obs: (T, H, W, C) uint8  — T varies per episode
    # actions: (T, action_dim) float32
    pass
```

### Load into a flat buffer (for VAE/RNN training)

```python
import numpy as np, glob, os

def load_flat_buffer(local_dir: str, max_episodes: int = None):
    paths = sorted(glob.glob(os.path.join(local_dir, "*.npz")))[:max_episodes]
    all_obs, all_acts, all_rews, all_dones = [], [], [], []
    for p in paths:
        ep = np.load(p)
        all_obs.append(ep["obs"])
        all_acts.append(ep["actions"])
        all_rews.append(ep["rewards"])
        all_dones.append(ep["dones"])
    return (np.concatenate(all_obs), np.concatenate(all_acts),
            np.concatenate(all_rews), np.concatenate(all_dones))

obs, actions, rewards, dones = load_flat_buffer("/data/episodes", max_episodes=1000)
print(f"Loaded: obs={obs.shape}, actions={actions.shape}")
```

### Stream directly from Hub (no download needed)

```python
from huggingface_hub import hf_hub_download
import numpy as np, io

def stream_episode_from_hub(repo_id: str, ep_idx: int, token: str = None):
    """Stream a single episode from Hub without downloading all."""
    path = hf_hub_download(
        repo_id=repo_id, filename=f"ep_{ep_idx:06d}.npz",
        repo_type="dataset", token=token,
    )
    return np.load(path)

ep = stream_episode_from_hub("sudingli21/carracing-v3-random-10k", 0)
```

---

## Dataset Format (CarRacing-v3)

Each `ep_XXXXXX.npz` file contains:
| Key | Shape | Dtype | Description |
|-----|-------|-------|-------------|
| `obs` | `(T, 96, 96, 3)` | uint8 | RGB frames (0-255) |
| `actions` | `(T, 3)` | float32 | [steering, gas, brake] |
| `rewards` | `(T,)` | float32 | per-step reward |
| `dones` | `(T,)` | bool | episode termination flag |

- T ≤ 1000 steps (max_steps per episode)
- ~4 MB per episode (compressed npz)
- 10,000 episodes total → ~40 GB on disk

---

## Common Patterns

### Check dataset exists and get file count
```python
from huggingface_hub import HfApi
api = HfApi()
files = api.list_repo_files("sudingli21/carracing-v3-random-10k", repo_type="dataset")
npz_files = [f for f in files if f.endswith(".npz")]
print(f"Episodes on Hub: {len(npz_files)}")
```

### Resume interrupted upload (safe to re-run)
`upload_folder` is idempotent — already-uploaded files are skipped automatically.

### Inject HF_TOKEN into Vast.ai job
```bash
python3 vastai_scheduler.py launch ... --pass-env "HF_TOKEN" ...
```
Inside the job script, use `os.environ["HF_TOKEN"]` directly.

---

## Rules

- Never print or log `HF_TOKEN` values
- Use `private=False` for public research datasets; `private=True` for proprietary data
- Always use `exist_ok=True` in `create_repo` to make upload scripts idempotent
- For datasets >10GB, prefer npz over pkl (3× smaller with `np.savez_compressed`)
