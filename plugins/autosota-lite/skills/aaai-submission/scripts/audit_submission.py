#!/usr/bin/env python3
"""Audit AAAI/OpenReview metadata, archive sizes, and repository links."""

from __future__ import annotations

import argparse
import json
import re
import sys
import tarfile
import zipfile
from pathlib import Path


REPO_URL = re.compile(
    r"https?://(?:www\.)?(?:github\.com|gitlab\.com|bitbucket\.org|"
    r"anonymousgithub\.com|anonymous\.4open\.science|huggingface\.co/"
    r"(?:datasets|spaces)|osf\.io|zenodo\.org|figshare\.com)/?\S*",
    re.IGNORECASE,
)
TEXT_SUFFIXES = {".tex", ".bib", ".md", ".txt", ".html", ".py", ".r", ".json", ".yaml", ".yml", ".ipynb", ".sh"}
MIB = 1024 * 1024


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def scan_text(label: str, text: str, errors: list[str]) -> None:
    for match in REPO_URL.findall(text):
        fail(errors, f"{label}: repository URL requires human disposition: {match}")


def scan_file(path: Path, errors: list[str]) -> None:
    if path.suffix.lower() in TEXT_SUFFIXES:
        scan_text(str(path), path.read_text(errors="replace"), errors)


def scan_archive(path: Path, errors: list[str]) -> None:
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as archive:
            for info in archive.infolist():
                if info.is_dir():
                    continue
                if (info.external_attr >> 16) & 0o170000 == 0o120000:
                    fail(errors, f"{path}: symbolic link in archive: {info.filename}")
                if Path(info.filename).suffix.lower() in TEXT_SUFFIXES:
                    scan_text(f"{path}:{info.filename}", archive.read(info).decode("utf-8", "replace"), errors)
    elif tarfile.is_tarfile(path):
        with tarfile.open(path) as archive:
            for member in archive.getmembers():
                if member.issym() or member.islnk():
                    fail(errors, f"{path}: symbolic link in archive: {member.name}")
                extracted = archive.extractfile(member) if member.isfile() else None
                if extracted and Path(member.name).suffix.lower() in TEXT_SUFFIXES:
                    scan_text(f"{path}:{member.name}", extracted.read().decode("utf-8", "replace"), errors)


def require(value: object, name: str, errors: list[str]) -> None:
    if value in (None, "", [], {}):
        fail(errors, f"metadata: missing required field {name}")


def audit_metadata(data: dict, errors: list[str]) -> None:
    for key in ("title", "tldr", "abstract", "primary_topic", "authors", "countries"):
        require(data.get(key), key, errors)
    secondary = data.get("secondary_topics", [])
    if not 1 <= len(secondary) <= 5:
        fail(errors, "metadata: secondary_topics must contain 1-5 entries")
    limit = data.get("tldr_character_limit")
    if limit is None:
        fail(errors, "metadata: record tldr_character_limit from the live form/schema")
    elif len(data.get("tldr", "")) > int(limit):
        fail(errors, f"metadata: TL;DR exceeds live limit ({len(data['tldr'])}/{limit})")
    for index, author in enumerate(data.get("authors", []), 1):
        for field in ("openreview_profile_ready", "full_publication_name", "current_position", "institution_email"):
            if not author.get(field):
                fail(errors, f"metadata: author {index} missing/false {field}")
        if author.get("dblp_status") not in {"url_present", "not_available", "disambiguation_declaration"}:
            fail(errors, f"metadata: author {index} needs a valid dblp_status")
    reviewer = data.get("reciprocal_reviewer", {})
    if reviewer.get("status") == "nominated":
        for field in ("nominee", "qualification_verified", "not_spc_ac_or_organizer", "agreed_to_review_load"):
            if not reviewer.get(field):
                fail(errors, f"metadata: nominated reciprocal reviewer missing/false {field}")
    elif reviewer.get("status") == "no_qualified_author":
        if not reviewer.get("author_confirmed"):
            fail(errors, "metadata: no-qualified-author declaration lacks author confirmation")
    else:
        fail(errors, "metadata: reciprocal_reviewer.status must be nominated or no_qualified_author")
    policy = data.get("policy_acknowledgements", {})
    for field in ("profiles_complete", "no_parallel_archival_review", "simultaneous_work_cited_anonymously", "license_accepted"):
        if not policy.get(field):
            fail(errors, f"metadata: policy acknowledgement missing/false {field}")
    scan_text("metadata", json.dumps(data, ensure_ascii=False), errors)


def check_upload(path: Path | None, limit_mib: int, label: str, errors: list[str]) -> None:
    if path is None:
        return
    if not path.exists():
        fail(errors, f"{label}: file does not exist: {path}")
        return
    size = path.stat().st_size
    if size > limit_mib * MIB:
        fail(errors, f"{label}: {size / MIB:.2f} MiB exceeds {limit_mib} MiB")
    scan_archive(path, errors)


def check_required_pdf(path: Path, label: str, errors: list[str]) -> None:
    if not path.exists():
        fail(errors, f"{label}: file does not exist: {path}")
    elif path.suffix.lower() != ".pdf":
        fail(errors, f"{label}: expected a standalone PDF: {path}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--main-pdf", type=Path, required=True)
    parser.add_argument("--checklist", type=Path, required=True)
    parser.add_argument("--scan", type=Path, nargs="*", default=[])
    parser.add_argument("--technical", type=Path)
    parser.add_argument("--media", type=Path)
    parser.add_argument("--code-data", type=Path)
    args = parser.parse_args()
    errors: list[str] = []
    audit_metadata(json.loads(args.metadata.read_text()), errors)
    check_required_pdf(args.main_pdf, "main paper", errors)
    check_required_pdf(args.checklist, "reproducibility checklist", errors)
    for path in args.scan:
        scan_file(path, errors)
    check_upload(args.technical, 10, "technical supplement", errors)
    check_upload(args.media, 50, "media supplement", errors)
    check_upload(args.code_data, 50, "code/data supplement", errors)
    if errors:
        print("BLOCKING")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS: metadata, sizes, and repository-link scan")
    return 0


if __name__ == "__main__":
    sys.exit(main())
