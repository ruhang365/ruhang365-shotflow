#!/usr/bin/env python3
"""Create or verify the pre-registered prompt manifests for public examples."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_ROOT = REPOSITORY_ROOT / "examples"
CASES = ("sky-mender", "storm-deck", "obsidian-bloom")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected an object in {path}")
    return value


def expected_manifest(case_id: str) -> dict[str, Any]:
    root = EXAMPLES_ROOT / case_id
    project = load_json(root / "shotflow.project.json")
    clip1 = root / "prompts" / "clip-01.txt"
    baseline = root / "prompts" / "clip-02-baseline-frozen.txt"
    grammar = root / "plan" / "clip-02-grammar.json"
    recorded = project["shots"][0]["prompt"]["sha256"]
    actual = sha256(clip1)
    if recorded != actual:
        raise ValueError(
            f"{case_id}: project Clip 01 prompt hash does not match prompt file"
        )
    return {
        "experiment_version": "1.0",
        "case_id": case_id,
        "status": "awaiting_generation_approval",
        "provider": project["provider"],
        "prompts": {
            "clip_01": {
                "path": "prompts/clip-01.txt",
                "sha256": actual,
                "frozen": True,
            },
            "clip_02_baseline": {
                "path": "prompts/clip-02-baseline-frozen.txt",
                "sha256": sha256(baseline),
                "frozen": True,
            },
            "clip_02_shotflow": {
                "path": None,
                "sha256": None,
                "frozen": False,
                "requires_accepted_clip_01": True,
            },
        },
        "next_shot_grammar": {
            "path": "plan/clip-02-grammar.json",
            "sha256": sha256(grammar),
        },
        "reference_policy": (
            "Use the same accepted Clip 01 video and final frame for baseline "
            "and ShotFlow Clip 02."
        ),
        "ai_generated_disclosure_required": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write", action="store_true", help="Write canonical experiment manifests"
    )
    arguments = parser.parse_args()
    failed = False
    for case_id in CASES:
        path = EXAMPLES_ROOT / case_id / "experiment.json"
        expected = expected_manifest(case_id)
        if arguments.write:
            path.write_text(
                json.dumps(expected, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            print(f"wrote {path.relative_to(REPOSITORY_ROOT)}")
            continue
        if not path.exists():
            print(f"missing {path.relative_to(REPOSITORY_ROOT)}", file=sys.stderr)
            failed = True
            continue
        actual = load_json(path)
        if actual != expected:
            print(f"stale {path.relative_to(REPOSITORY_ROOT)}", file=sys.stderr)
            failed = True
        else:
            print(f"ok {path.relative_to(REPOSITORY_ROOT)}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
