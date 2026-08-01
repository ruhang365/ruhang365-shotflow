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
ATTEMPT_CAPS = {"sky-mender": 8, "storm-deck": 5, "obsidian-bloom": 5}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected an object in {path}")
    return value


def obsidian_gate7_result() -> dict[str, Any] | None:
    root = EXAMPLES_ROOT / "obsidian-bloom"
    baseline_path = root / "evidence" / "gate7-baseline-receipt.json"
    shotflow_path = root / "evidence" / "gate7-shotflow-receipt.json"
    if not baseline_path.exists() or not shotflow_path.exists():
        return None
    baseline = load_json(baseline_path)
    shotflow = load_json(shotflow_path)
    baseline_video = baseline.get("output", {}).get("video", {})
    shotflow_video = shotflow.get("output", {}).get("video", {})
    baseline_size = (baseline_video.get("width"), baseline_video.get("height"))
    shotflow_size = (shotflow_video.get("width"), shotflow_video.get("height"))
    if baseline_size == shotflow_size:
        return None
    if baseline.get("gate_decision", {}).get("eligible") is not False:
        return None
    if shotflow.get("gate_decision", {}).get("eligible") is not False:
        return None
    return {
        "status": "invalid_pair",
        "reason": (
            f"The baseline returned {baseline_size[0]}x{baseline_size[1]} and "
            f"v0.3 returned {shotflow_size[0]}x{shotflow_size[1]}. The "
            "pre-registered rule requires identical native resolution, so "
            "blind scoring and Gate 8 are blocked."
        ),
        "attempt_ids": ["obsidian-bloom-004", "obsidian-bloom-005"],
        "receipts": [
            {
                "path": baseline_path.relative_to(root).as_posix(),
                "sha256": sha256(baseline_path),
            },
            {
                "path": shotflow_path.relative_to(root).as_posix(),
                "sha256": sha256(shotflow_path),
            },
        ],
        "blind_review": "not_run",
        "retry_authorized": False,
        "gate_8_authorized": False,
    }


def expected_manifest(case_id: str) -> dict[str, Any]:
    root = EXAMPLES_ROOT / case_id
    project = load_json(root / "shotflow.project.json")
    clip1 = root / "prompts" / "clip-01.txt"
    baseline = root / "prompts" / "clip-02-baseline-frozen.txt"
    shotflow = root / "prompts" / "clip-02-shotflow.txt"
    shotflow_v2 = root / "prompts" / "clip-02-shotflow-v2.txt"
    shotflow_anchor = root / "prompts" / "clip-02-shotflow-anchor-creative-v1.txt"
    baseline_anchor_submission = (
        root / "prompts" / "clip-02-baseline-anchor-v1.txt"
    )
    shotflow_anchor_submission = (
        root / "prompts" / "clip-02-shotflow-anchor-v1.txt"
    )
    baseline_anchor_v2_submission = (
        root / "prompts" / "clip-02-baseline-anchor-v2.txt"
    )
    shotflow_anchor_v2_submission = (
        root / "prompts" / "clip-02-shotflow-anchor-v2.txt"
    )
    grammar = root / "plan" / "clip-02-grammar.json"
    grammar_v3 = root / "plan" / "clip-02-grammar-v3.json"
    sequence_v3 = root / "plan" / "clip-02-sequence-v3.json"
    prompt_v3 = root / "prompts" / "clip-02-shotflow-v3-offline.txt"
    grammar_v4 = root / "plan" / "clip-02-grammar-v4.json"
    sequence_v4 = root / "plan" / "clip-02-sequence-v4.json"
    prompt_v4 = root / "prompts" / "clip-02-shotflow-v4-rc1.txt"
    baseline_v5 = root / "prompts" / "clip-02-baseline-v04.txt"
    grammar_v5 = root / "plan" / "clip-02-grammar-v5.json"
    sequence_v5 = root / "plan" / "clip-02-sequence-v5.json"
    prompt_v5 = root / "prompts" / "clip-02-shotflow-v5-rc1.txt"
    provider_handoff = root / "evidence" / "provider-handoff.json"
    anchor_handoffs = sorted(
        (root / "evidence").glob("provider-handoff-*-anchor-v1.json")
    )
    causal_handoffs = sorted(
        (root / "evidence").glob("provider-handoff-*-gate[78].json")
    )
    evidence_handoffs = sorted(
        (root / "evidence").glob("provider-handoff-*-v04.json")
    )
    source_shot = project["shots"][0]
    recorded = source_shot["prompt"]["sha256"]
    actual = sha256(clip1)
    if recorded != actual:
        raise ValueError(
            f"{case_id}: project Clip 01 prompt hash does not match prompt file"
        )
    v3_files = (grammar_v3, sequence_v3, prompt_v3)
    if any(path.exists() for path in v3_files) and not all(
        path.exists() for path in v3_files
    ):
        raise ValueError(
            f"{case_id}: provider-direct-v3 grammar, sequence, and prompt must be frozen together"
        )
    v4_files = (grammar_v4, sequence_v4, prompt_v4)
    if any(path.exists() for path in v4_files) and not all(
        path.exists() for path in v4_files
    ):
        raise ValueError(
            f"{case_id}: provider-direct-v4 grammar, sequence, and prompt must be frozen together"
        )
    if all(path.exists() for path in v4_files) and len(causal_handoffs) != 2:
        raise ValueError(
            f"{case_id}: provider-direct-v4 requires exactly two Gate handoffs"
        )
    v5_files = (baseline_v5, grammar_v5, sequence_v5, prompt_v5)
    if any(path.exists() for path in v5_files) and not all(
        path.exists() for path in v5_files
    ):
        raise ValueError(
            f"{case_id}: provider-direct-v5 baseline, grammar, sequence, and prompt must be frozen together"
        )
    if all(path.exists() for path in v5_files) and len(evidence_handoffs) != 2:
        raise ValueError(
            f"{case_id}: provider-direct-v5 requires exactly two v0.4 handoffs"
        )
    observed = source_shot.get("observed")
    if observed and not shotflow.exists():
        raise ValueError(f"{case_id}: accepted Clip 01 is missing its ShotFlow prompt")
    active_shotflow = shotflow_v2 if shotflow_v2.exists() else shotflow
    active_attempt_status: str | None = None
    anchor_baseline_status: str | None = None
    anchor_shotflow_status: str | None = None
    gate7_baseline_status: str | None = None
    gate7_shotflow_status: str | None = None
    ledger = load_json(root / "attempts.json") if observed else None
    if ledger is not None and active_shotflow.exists():
        active_hash = sha256(active_shotflow)
        active_attempts = [
            attempt
            for attempt in ledger["attempts"]
            if attempt["variant"] == "clip-02-shotflow"
            and attempt["prompt"]["sha256"] == active_hash
        ]
        if active_attempts:
            active_attempt_status = active_attempts[-1]["status"]
    if ledger is not None and baseline_anchor_submission.exists():
        baseline_anchor_hash = sha256(baseline_anchor_submission)
        baseline_anchor_attempts = [
            attempt
            for attempt in ledger["attempts"]
            if attempt["variant"] == "clip-02-baseline"
            and attempt["prompt"]["sha256"] == baseline_anchor_hash
        ]
        if baseline_anchor_attempts:
            anchor_baseline_status = baseline_anchor_attempts[-1]["status"]
    if ledger is not None and shotflow_anchor_submission.exists():
        shotflow_anchor_hash = sha256(shotflow_anchor_submission)
        shotflow_anchor_attempts = [
            attempt
            for attempt in ledger["attempts"]
            if attempt["variant"] == "clip-02-shotflow"
            and attempt["prompt"]["sha256"] == shotflow_anchor_hash
        ]
        if shotflow_anchor_attempts:
            anchor_shotflow_status = shotflow_anchor_attempts[-1]["status"]
    if ledger is not None and baseline_anchor_v2_submission.exists():
        gate7_baseline_hash = sha256(baseline_anchor_v2_submission)
        gate7_baseline_attempts = [
            attempt
            for attempt in ledger["attempts"]
            if attempt["variant"] == "clip-02-baseline"
            and attempt["prompt"]["sha256"] == gate7_baseline_hash
        ]
        if gate7_baseline_attempts:
            gate7_baseline_status = gate7_baseline_attempts[-1]["status"]
    if ledger is not None and shotflow_anchor_v2_submission.exists():
        gate7_shotflow_hash = sha256(shotflow_anchor_v2_submission)
        gate7_shotflow_attempts = [
            attempt
            for attempt in ledger["attempts"]
            if attempt["variant"] == "clip-02-shotflow"
            and attempt["prompt"]["sha256"] == gate7_shotflow_hash
        ]
        if gate7_shotflow_attempts:
            gate7_shotflow_status = gate7_shotflow_attempts[-1]["status"]
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
        if ledger is None:
            raise ValueError(f"{case_id}: accepted Clip 01 is missing its ledger")
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
    gate7_result = obsidian_gate7_result()
    if (
        case_id == "obsidian-bloom"
        and gate7_result is not None
        and gate7_baseline_status == "failed"
        and gate7_shotflow_status == "failed"
    ):
        status = "gate_7_invalid_native_resolution_pair"
    elif (
        observed
        and ledger is not None
        and len(ledger["attempts"]) >= ATTEMPT_CAPS[case_id]
        and active_attempt_status is None
    ):
        status = "attempt_cap_reached_no_valid_ab"
    elif case_id == "obsidian-bloom" and len(anchor_handoffs) == 2:
        if anchor_shotflow_status == "accepted":
            status = "anchor_frame_v1_ab_ready_for_blind_review"
        elif anchor_shotflow_status in {"rejected", "failed"}:
            status = f"anchor_frame_v1_shotflow_{anchor_shotflow_status}"
        elif anchor_baseline_status == "accepted":
            status = "anchor_frame_v1_baseline_accepted_shotflow_pending_approval"
        elif anchor_baseline_status in {"rejected", "failed"}:
            status = f"anchor_frame_v1_baseline_{anchor_baseline_status}"
        else:
            status = "anchor_frame_v1_awaiting_generation_approval"
    elif observed and shotflow_v2.exists():
        status = {
            "accepted": "mechanism_v2_accepted",
            "rejected": "mechanism_v2_rejected",
            "submitted": "mechanism_v2_under_review",
        }.get(active_attempt_status, "mechanism_v2_awaiting_generation_approval")
    elif observed:
        status = "clip_01_accepted_gate_2_pending"
    else:
        status = "awaiting_generation_approval"
    manifest = {
        "experiment_version": "1.0",
        "case_id": case_id,
        "status": status,
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
            "Use the same accepted Clip 01 final frame as the only media "
            "reference for baseline and ShotFlow Clip 02. The source video is "
            "intentionally withheld under anchor-frame-v1."
            if anchor_handoffs
            else "Use the same accepted Clip 01 video and final frame for "
            "baseline and ShotFlow Clip 02."
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
    if provider_handoff.exists():
        manifest["provider_handoff"] = {
            "path": provider_handoff.relative_to(root).as_posix(),
            "sha256": sha256(provider_handoff),
        }
    if anchor_handoffs:
        manifest["provider_handoffs"] = []
        for handoff_path in anchor_handoffs:
            handoff = load_json(handoff_path)
            manifest["provider_handoffs"].append(
                {
                    "variant": handoff["variant"],
                    "profile": handoff["profile"],
                    "path": handoff_path.relative_to(root).as_posix(),
                    "sha256": sha256(handoff_path),
                    "submission_prompt_sha256": handoff["submission_prompt"][
                        "sha256"
                    ],
                }
            )
    if shotflow_anchor.exists():
        manifest["prompts"]["clip_02_shotflow_anchor"] = {
            "path": shotflow_anchor.relative_to(root).as_posix(),
            "sha256": sha256(shotflow_anchor),
            "frozen": True,
            "requires_accepted_clip_01": True,
            "profile": "anchor-frame-v1",
        }
    if all(path.exists() for path in v3_files):
        manifest["offline_prompt_candidate"] = {
            "profile": "provider-direct-v3",
            "status": "offline_only_not_authorized_for_generation",
            "grammar": {
                "path": grammar_v3.relative_to(root).as_posix(),
                "sha256": sha256(grammar_v3),
            },
            "ordered_sequence": {
                "path": sequence_v3.relative_to(root).as_posix(),
                "sha256": sha256(sequence_v3),
            },
            "compiled_prompt": {
                "path": prompt_v3.relative_to(root).as_posix(),
                "sha256": sha256(prompt_v3),
                "bytes": prompt_v3.stat().st_size,
            },
        }
    if all(path.exists() for path in v4_files):
        if case_id == "obsidian-bloom" and gate7_result is not None:
            rc_status = "gate_7_closed_invalid_native_resolution_pair"
        elif case_id == "sky-mender" and gate7_result is not None:
            rc_status = "gate_8_blocked_gate_7_invalid_pair"
        elif case_id == "obsidian-bloom":
            rc_status = "gate_7_awaiting_explicit_generation_approval"
        else:
            rc_status = "gate_8_blocked_until_gate_7_wins"
        manifest["rc_prompt_candidate"] = {
            "profile": "provider-direct-v4",
            "contract_version": "1.2",
            "status": rc_status,
            "grammar": {
                "path": grammar_v4.relative_to(root).as_posix(),
                "sha256": sha256(grammar_v4),
            },
            "ordered_sequence": {
                "path": sequence_v4.relative_to(root).as_posix(),
                "sha256": sha256(sequence_v4),
            },
            "compiled_prompt": {
                "path": prompt_v4.relative_to(root).as_posix(),
                "sha256": sha256(prompt_v4),
                "bytes": prompt_v4.stat().st_size,
            },
            "provider_handoffs": [
                {
                    "variant": handoff["variant"],
                    "profile": handoff["profile"],
                    "path": handoff_path.relative_to(root).as_posix(),
                    "sha256": sha256(handoff_path),
                    "submission_prompt_sha256": handoff["submission_prompt"][
                        "sha256"
                    ],
                }
                for handoff_path in causal_handoffs
                for handoff in [load_json(handoff_path)]
            ],
            "reference_policy": (
                "Both variants use the same accepted Clip 01 final frame as "
                "the only media reference under anchor-frame-v2."
            ),
        }
        if case_id == "obsidian-bloom" and gate7_result is not None:
            manifest["rc_prompt_candidate"]["gate_7_result"] = gate7_result
    if all(path.exists() for path in v5_files):
        manifest["v04_prompt_candidate"] = {
            "profile": "provider-direct-v5",
            "contract_version": "1.3",
            "sequence_version": "1.2",
            "handoff_profile": "anchor-frame-v3",
            "status": (
                "gate_9_awaiting_separate_generation_approval"
                if case_id == "obsidian-bloom"
                else "gate_10_blocked_until_gate_9_passes"
            ),
            "baseline_prompt": {
                "path": baseline_v5.relative_to(root).as_posix(),
                "sha256": sha256(baseline_v5),
                "bytes": baseline_v5.stat().st_size,
            },
            "grammar": {
                "path": grammar_v5.relative_to(root).as_posix(),
                "sha256": sha256(grammar_v5),
            },
            "ordered_sequence": {
                "path": sequence_v5.relative_to(root).as_posix(),
                "sha256": sha256(sequence_v5),
            },
            "compiled_prompt": {
                "path": prompt_v5.relative_to(root).as_posix(),
                "sha256": sha256(prompt_v5),
                "bytes": prompt_v5.stat().st_size,
            },
            "provider_handoffs": [
                {
                    "variant": handoff["variant"],
                    "profile": handoff["profile"],
                    "path": handoff_path.relative_to(root).as_posix(),
                    "sha256": sha256(handoff_path),
                    "submission_prompt_sha256": handoff["submission_prompt"][
                        "sha256"
                    ],
                    "submission_prompt_characters": len(
                        handoff["submission_prompt"]["text"]
                    ),
                }
                for handoff_path in evidence_handoffs
                for handoff in [load_json(handoff_path)]
            ],
            "reference_policy": (
                "Both variants use the same accepted Clip 01 final frame as "
                "the only media reference under anchor-frame-v3."
            ),
            "pair_count": 3,
            "generation_order": [
                ["baseline", "shotflow"],
                ["shotflow", "baseline"],
                ["baseline", "shotflow"],
            ],
            "canonical_review_raster": "1280x720",
        }
    return manifest


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
