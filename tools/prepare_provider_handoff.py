#!/usr/bin/env python3
"""Prepare an auditable provider handoff without submitting a generation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from shotflow.core import ShotFlowError, write_json  # noqa: E402
from shotflow.handoff import HANDOFF_PROFILES, prepare_provider_handoff  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--from-shot", required=True)
    parser.add_argument("--variant", required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--platform", required=True)
    parser.add_argument("--model-tool", required=True)
    parser.add_argument(
        "--profile",
        choices=HANDOFF_PROFILES,
        default="video-context-v1",
    )
    parser.add_argument("--known-output", action="append", default=[])
    parser.add_argument(
        "--opening-frame-review",
        choices=("pending", "accepted", "rejected"),
        default="pending",
    )
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        manifest = prepare_provider_handoff(
            args.project,
            source_shot_id=args.from_shot,
            variant=args.variant,
            creative_prompt_path=Path(args.prompt),
            platform=args.platform,
            model_tool=args.model_tool,
            profile=args.profile,
            known_output_paths=[Path(path) for path in args.known_output],
            opening_frame_review=args.opening_frame_review,
        )
        if args.output:
            write_json(Path(args.output), manifest)
    except (ShotFlowError, ValueError, FileNotFoundError) as exc:
        print(f"prepare_provider_handoff: error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
