#!/usr/bin/env python3
"""Repository integrity checks with no third-party dependencies."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IGNORED_PARTS = {".git", "__pycache__", ".venv", "artifacts", "build", "dist"}
MAX_TRACKED_BYTES = 5 * 1024 * 1024
FORBIDDEN_MEDIA = {".mp4", ".mov", ".avi", ".mkv"}
SECRET_PATTERNS = (
    re.compile(r"XYQ_ACCESS_KEY\s*=\s*[\"'][^\"']+[\"']"),
    re.compile(r"Authorization:\s*Bearer\s+[A-Za-z0-9._-]{16,}", re.IGNORECASE),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
)


def files() -> list[Path]:
    tracked = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT,
        capture_output=True,
        check=False,
    )
    if tracked.returncode == 0 and tracked.stdout:
        return [
            ROOT / relative.decode("utf-8")
            for relative in tracked.stdout.split(b"\0")
            if relative
        ]
    return [
        path
        for path in ROOT.rglob("*")
        if path.is_file() and not (set(path.relative_to(ROOT).parts) & IGNORED_PARTS)
    ]


def check_json(paths: list[Path], failures: list[str]) -> None:
    for path in paths:
        if path.suffix != ".json":
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            failures.append(f"invalid JSON: {path.relative_to(ROOT)}: {exc}")


def check_size_and_media(paths: list[Path], failures: list[str]) -> None:
    for path in paths:
        relative = path.relative_to(ROOT)
        if path.stat().st_size > MAX_TRACKED_BYTES:
            failures.append(f"file exceeds 5 MiB: {relative}")
        if path.suffix.lower() in FORBIDDEN_MEDIA:
            failures.append(f"raw video belongs in release assets, not Git: {relative}")


def check_secrets(paths: list[Path], failures: list[str]) -> None:
    for path in paths:
        if path.suffix.lower() not in {
            ".md",
            ".txt",
            ".py",
            ".json",
            ".yml",
            ".yaml",
            ".toml",
        }:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(content):
                failures.append(
                    f"possible credential in {path.relative_to(ROOT)}: {pattern.pattern}"
                )


def check_skill(failures: list[str]) -> None:
    skill = ROOT / "skills" / "shotflow" / "SKILL.md"
    content = skill.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        failures.append("SKILL.md has no frontmatter")
        return
    _, frontmatter, _ = content.split("---", 2)
    keys = {
        line.split(":", 1)[0].strip()
        for line in frontmatter.splitlines()
        if ":" in line
    }
    if keys != {"name", "description"}:
        failures.append(f"SKILL.md frontmatter keys are {sorted(keys)}")
    if "TODO" in content:
        failures.append("SKILL.md still contains TODO")


def check_evidence_receipts(paths: list[Path], failures: list[str]) -> None:
    for receipt_path in paths:
        if not receipt_path.name.endswith("-receipt.json"):
            continue
        try:
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
        if receipt.get("public_media_approved") is False:
            if receipt.get("ai_generated_disclosure_required") is not True:
                failures.append(
                    "unpublished media is missing its future disclosure requirement: "
                    f"{receipt_path.relative_to(ROOT)}"
                )
            continue
        disclosure = receipt.get("aigc_disclosure", {})
        if disclosure.get("original_container_label_present") is not True:
            failures.append(
                f"missing original AIGC label proof: {receipt_path.relative_to(ROOT)}"
            )
        if disclosure.get("public_derivatives_have_visible_label") is not True:
            failures.append(
                f"missing visible preview disclosure: {receipt_path.relative_to(ROOT)}"
            )
        evidence_root = receipt_path.parent.resolve()
        for field in ("public_preview", "public_final_frame"):
            artifact = receipt.get(field, {})
            relative = artifact.get("path")
            if not isinstance(relative, str):
                failures.append(
                    f"missing {field} path: {receipt_path.relative_to(ROOT)}"
                )
                continue
            candidate = (evidence_root / relative).resolve()
            try:
                candidate.relative_to(evidence_root)
            except ValueError:
                failures.append(
                    f"unsafe {field} path: {receipt_path.relative_to(ROOT)}"
                )
                continue
            if not candidate.is_file():
                failures.append(
                    f"missing {field} file: {candidate.relative_to(ROOT)}"
                )
                continue
            actual_hash = hashlib.sha256(candidate.read_bytes()).hexdigest()
            if actual_hash != artifact.get("sha256"):
                failures.append(
                    f"{field} hash mismatch: {candidate.relative_to(ROOT)}"
                )
            if candidate.stat().st_size != artifact.get("bytes"):
                failures.append(
                    f"{field} size mismatch: {candidate.relative_to(ROOT)}"
                )


def main() -> int:
    paths = files()
    failures: list[str] = []
    check_json(paths, failures)
    check_size_and_media(paths, failures)
    check_secrets(paths, failures)
    check_skill(failures)
    check_evidence_receipts(paths, failures)
    required = (
        "LICENSE",
        "README.md",
        "README.zh-CN.md",
        "NOTICE.md",
        "pyproject.toml",
        "schemas/shotflow.project.schema.json",
        "schemas/observation-patch.schema.json",
        "schemas/generation-attempt.schema.json",
        "schemas/ordered-sequence.schema.json",
        "schemas/provider-handoff.schema.json",
        "schemas/evaluation-pair.schema.json",
        "skills/shotflow/references/quick-entry.md",
        "tools/validate_quick_output.py",
        "examples/quick-entry/obsidian-bloom-output.txt",
        "examples/forward-tests/protocol-v04-rc2.json",
        "examples/SHOWCASE_OBSIDIAN_BLOOM.md",
        "FOUNDING_TESTER_SPRINT.md",
    )
    for relative in required:
        if not (ROOT / relative).is_file():
            failures.append(f"missing required file: {relative}")
    if failures:
        for failure in failures:
            print(f"ERROR {failure}", file=sys.stderr)
        return 1
    print(f"repository checks passed ({len(paths)} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
