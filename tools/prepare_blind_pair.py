#!/usr/bin/env python3
"""Prepare a deterministic neutral A/B review package."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from shotflow.core import ShotFlowError  # noqa: E402
from shotflow.review import prepare_blind_pair  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--pair-id", required=True)
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--shotflow", type=Path, required=True)
    parser.add_argument("--baseline-prompt", type=Path, required=True)
    parser.add_argument("--shotflow-prompt", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--variant-a", choices=("baseline", "shotflow"), required=True)
    parser.add_argument("--platform", required=True)
    parser.add_argument("--model-tool", required=True)
    parser.add_argument("--generation-mode", required=True)
    parser.add_argument("--reasoning-mode", required=True)
    parser.add_argument(
        "--generation-order",
        nargs=2,
        choices=("baseline", "shotflow"),
        required=True,
    )
    arguments = parser.parse_args()
    try:
        manifest = prepare_blind_pair(
            case_id=arguments.case_id,
            pair_id=arguments.pair_id,
            reference_frame=arguments.reference,
            baseline_video=arguments.baseline,
            shotflow_video=arguments.shotflow,
            baseline_prompt=arguments.baseline_prompt,
            shotflow_prompt=arguments.shotflow_prompt,
            output_directory=arguments.output_dir,
            variant_a=arguments.variant_a,
            platform=arguments.platform,
            model_tool=arguments.model_tool,
            generation_mode=arguments.generation_mode,
            reasoning_mode=arguments.reasoning_mode,
            generation_order=tuple(arguments.generation_order),
        )
    except ShotFlowError as exc:
        print(f"prepare_blind_pair: error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
