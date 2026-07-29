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
    shotflow = root / "prompts" / "clip-02-shotflow.txt"
    shotflow_v2 = root / "prompts" / "clip-02-shotflow-v2.txt"
    grammar = root / "plan" / "clip-02-grammar.json"
    source_shot = project["shots"][0]
    recorded = source_shot["prompt"]["sha256"]
    actual = sha256(clip1)
    if recorded != actual:
        raise ValueError(
            f"{case_id}: project Clip 01 prompt hash does not match prompt file"
        )
    observed = source_shot.get("observed")
    if observed and not shotflow.exists():
        raise ValueError(f"{case_id}: accepted Clip 01 is missing its ShotFlow prompt")
    active_shotflow = shotflow_v2 if shotflow_v2.exists() else shotflow
    shotflow_prompt = (
        {
            "path": active_shotflow.relative_to(root).as_posix(),
            "sha256": sha256(active_shotflow),
            "frozen": True,
            "requires_accepted_clip_01": True,
            "profile": (
                "provider-direct-v2" if shotflow_v2.exists() else "contract-first-v1"
            ),
        }
        if observed
        else {
            "path": None,
            "sha256": None,
            "frozen": False,
            "requires_accepted_clip_01": True,
            "profile": None,
        }
    )
    prompt_history: list[dict[str, Any]] = []
    if observed and shotflow_v2.exists():
        ledger = load_json(root / "attempts.json")
        v1_hash = sha256(shotflow)
        v1_attempt = next(
            (
                attempt
                for attempt in ledger["attempts"]
                if attempt["variant"] == "clip-02-shotflow"
                and attempt["prompt"]["sha256"] == v1_hash
            ),
            None,
        )
        prompt_history.append(
            {
                "path": "prompts/clip-02-shotflow.txt",
                "sha256": v1_hash,
                "profile": "contract-first-v1",
                "status": (
                    v1_attempt["status"]
                    if v1_attempt
                    else "superseded_before_generation"
                ),
            }
        )
    return {
        "experiment_version": "1.0",
        "case_id": case_id,
        "status": (
            "mechanism_v2_awaiting_generation_approval"
            if observed and shotflow_v2.exists()
            else "clip_01_accepted_gate_2_pending"
            if observed
            else "awaiting_generation_approval"
        ),
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
            "clip_02_shotflow": shotflow_prompt,
        },
        "next_shot_grammar": {
            "path": "plan/clip-02-grammar.json",
            "sha256": sha256(grammar),
        },
        "reference_policy": (
            "Use the same accepted Clip 01 video and final frame for baseline "
            "and ShotFlow Clip 02."
        ),
        "accepted_reference_hashes": (
            {
                "video_sha256": source_shot["artifacts"]["video"]["sha256"],
                "final_frame_sha256": source_shot["artifacts"]["final_frame"]["sha256"],
            }
            if observed
            else None
        ),
        "shotflow_prompt_history": prompt_history,
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
