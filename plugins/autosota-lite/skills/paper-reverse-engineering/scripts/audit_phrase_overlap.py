#!/usr/bin/env python3
"""Report shared word sequences between a draft and exemplar text files."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


WORD = re.compile(r"[a-z]+(?:[-'][a-z]+)*")


def tokens(path: Path) -> list[str]:
    return WORD.findall(path.read_text(errors="replace").lower())


def ngrams(items: list[str], size: int) -> set[tuple[str, ...]]:
    return {tuple(items[i:i + size]) for i in range(len(items) - size + 1)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--draft", type=Path, required=True)
    parser.add_argument("--exemplar", type=Path, action="append", required=True)
    parser.add_argument("--size", type=int, default=8)
    args = parser.parse_args()
    draft = ngrams(tokens(args.draft), args.size)
    hits = []
    for exemplar in args.exemplar:
        for match in sorted(draft & ngrams(tokens(exemplar), args.size)):
            hits.append((exemplar, " ".join(match)))
    for exemplar, phrase in hits:
        print(f"{exemplar}: {phrase}")
    print(f"overlap_count={len(hits)} size={args.size}")
    return 1 if hits else 0


if __name__ == "__main__":
    raise SystemExit(main())
