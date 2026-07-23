#!/usr/bin/env python3
"""Measure aggregate prose style without emitting source sentences."""

from __future__ import annotations

import argparse
import json
import math
import re
import statistics
from collections import Counter
from pathlib import Path


WORD = re.compile(r"[A-Za-z]+(?:[-'][A-Za-z]+)*")
BOUNDARY = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9(])")
MONITORED = {"we", "our", "this", "these", "that", "which", "however", "but", "while", "moreover", "may", "can", "show", "shows", "indicate", "indicates", "suggest", "suggests"}


def percentile(values: list[int], q: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * q
    low, high = math.floor(position), math.ceil(position)
    if low == high:
        return float(ordered[low])
    return ordered[low] * (high - position) + ordered[high] * (position - low)


def clean(text: str) -> str:
    text = re.sub(r"%.*", " ", text)
    text = re.sub(r"\\(?:cite\w*|ref|label)\{[^{}]*\}", " ", text)
    text = re.sub(r"\\[A-Za-z@]+\*?(?:\[[^\]]*\])?", " ", text)
    text = text.replace("{", " ").replace("}", " ")
    text = re.sub(r"\s+", " ", text)
    for form in ("et al.", "e.g.", "i.e.", "Fig.", "Eq.", "Sec.", "vs."):
        text = text.replace(form, form.replace(".", "<DOT>"))
    return text


def analyze(paths: list[Path]) -> dict:
    text = clean("\n".join(path.read_text(errors="replace") for path in paths))
    sentences = [part.replace("<DOT>", ".").strip() for part in BOUNDARY.split(text)]
    lengths = [len(WORD.findall(sentence)) for sentence in sentences]
    lengths = [length for length in lengths if 4 <= length <= 100]
    tokens = [token.lower() for token in WORD.findall(text)]
    counts = Counter(tokens)
    total = max(1, len(tokens))
    return {
        "files": [str(path) for path in paths],
        "words": len(tokens),
        "sentences": len(lengths),
        "sentence_words": {
            "mean": round(statistics.mean(lengths), 2) if lengths else 0,
            "median": round(statistics.median(lengths), 2) if lengths else 0,
            "p25": round(percentile(lengths, .25), 2) if lengths else 0,
            "p75": round(percentile(lengths, .75), 2) if lengths else 0,
            "under_12_pct": round(100 * sum(n < 12 for n in lengths) / max(1, len(lengths)), 2),
            "over_30_pct": round(100 * sum(n > 30 for n in lengths) / max(1, len(lengths)), 2),
        },
        "monitored_words_per_1k": {word: round(1000 * counts[word] / total, 2) for word in sorted(MONITORED)},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(analyze(args.paths), indent=2) + "\n"
    if args.out:
        args.out.write_text(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
