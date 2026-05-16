---
name: util-unzip
description: Extract zip archives and other compressed files (.zip, .tar.gz, .tar.bz2, .gz, .7z). Use this when you need to unpack downloaded datasets, model checkpoints, research code repos, or any compressed artifact before processing.
---

# AutoSOTA Util-Unzip: Extract Compressed Archives

Use this skill to extract zip archives and other compressed file formats. Handles `.zip`, `.tar.gz`, `.tar.bz2`, `.gz`, and `.7z` files commonly encountered when downloading datasets, model weights, or research code.

## Quick Reference

```bash
# Unzip a .zip file to a destination folder
unzip archive.zip -d /destination/folder

# Extract a .tar.gz file
tar -xzf archive.tar.gz -C /destination/folder

# Extract a .tar.bz2 file
tar -xjf archive.tar.bz2 -C /destination/folder

# Extract a .gz file (single file, not tar)
gunzip file.gz

# Extract a .7z file (requires p7zip)
7z x archive.7z -o/destination/folder
```

## Python API

### Unzip a .zip file (safe — guards against zip-slip)

```python
import zipfile, os

def unzip(archive_path: str, dest_dir: str) -> None:
    """Extract all contents of a zip archive to dest_dir.

    Validates every member path to prevent zip-slip path traversal.
    """
    dest_dir = os.path.realpath(dest_dir)
    os.makedirs(dest_dir, exist_ok=True)
    with zipfile.ZipFile(archive_path, "r") as zf:
        for member in zf.infolist():
            member_path = os.path.realpath(os.path.join(dest_dir, member.filename))
            if not member_path.startswith(dest_dir + os.sep) and member_path != dest_dir:
                raise ValueError(f"Unsafe path in archive: {member.filename}")
            zf.extract(member, dest_dir)
    print(f"Extracted {archive_path} → {dest_dir}")

# Usage
unzip("/data/dataset.zip", "/data/dataset/")
```

### Extract .tar.gz / .tar.bz2 (safe — guards against path traversal)

```python
import tarfile, os

def extract_tar(archive_path: str, dest_dir: str) -> None:
    """Extract a tar archive (.tar.gz or .tar.bz2) to dest_dir.

    Validates every member path to prevent path traversal attacks.
    """
    dest_dir = os.path.realpath(dest_dir)
    os.makedirs(dest_dir, exist_ok=True)
    with tarfile.open(archive_path, "r:*") as tf:
        for member in tf.getmembers():
            member_path = os.path.realpath(os.path.join(dest_dir, member.name))
            if not member_path.startswith(dest_dir + os.sep) and member_path != dest_dir:
                raise ValueError(f"Unsafe path in archive: {member.name}")
        tf.extractall(dest_dir)
    print(f"Extracted {archive_path} → {dest_dir}")

# Usage
extract_tar("/data/checkpoints.tar.gz", "/data/checkpoints/")
```

### Auto-detect format and extract

```python
import zipfile, tarfile, gzip, shutil, os

def extract(archive_path: str, dest_dir: str) -> None:
    """Detect archive format and extract to dest_dir.

    Uses safe extraction helpers that guard against path traversal.
    """
    os.makedirs(dest_dir, exist_ok=True)
    if zipfile.is_zipfile(archive_path):
        unzip(archive_path, dest_dir)
    elif tarfile.is_tarfile(archive_path):
        extract_tar(archive_path, dest_dir)
    elif archive_path.endswith(".gz"):
        # Single-file gzip (not tar): strip .gz extension for output name
        out_name = os.path.basename(archive_path[:-3])
        out_path = os.path.join(dest_dir, out_name)
        with gzip.open(archive_path, "rb") as f_in, open(out_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    else:
        raise ValueError(f"Unsupported archive format: {archive_path}")
    print(f"Extracted {archive_path} → {dest_dir}")

# Usage
extract("/data/model.zip", "/data/model/")
extract("/data/episodes.tar.gz", "/data/episodes/")
```

## Common Use Cases

### Unzip a downloaded HuggingFace dataset artifact

```bash
# After downloading from HuggingFace Hub
unzip /data/episodes.zip -d /data/episodes/
```

### Unzip a research repo downloaded as a zip from GitHub

```bash
wget https://github.com/org/repo/archive/refs/heads/main.zip -O repo.zip
unzip repo.zip -d /workspace/
```

### Unzip a Vast.ai checkpoint archive

```bash
# Transfer + extract in one step
scp user@host:/runs/checkpoint.tar.gz /data/
tar -xzf /data/checkpoint.tar.gz -C /data/checkpoints/
```

## Install Missing Tools

```bash
# Install unzip (Debian/Ubuntu)
apt-get install -y unzip

# Install p7zip for .7z support
apt-get install -y p7zip-full

# Python zipfile and tarfile are in the standard library (no install needed)
```

## Troubleshooting

**"End-of-central-directory signature not found"**
- The file may be incomplete or corrupt. Re-download it.

**"Bad magic number"** (tar)
- Wrong compression flag. Try `tar -xf archive.tar.gz` (auto-detect mode).

**Permission denied after extraction**
- Fix with: `chmod -R 755 /destination/folder`

**Archive contains unsafe paths (path traversal)**
- Inspect contents before extracting: `unzip -l archive.zip` or `tar -tzf archive.tar.gz`
- Use the Python API above, which respects the destination directory.
