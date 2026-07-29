#!/usr/bin/env python3
"""Append or update a public-safe ShotFlow generation attempt."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from shotflow.core import ShotFlowError  # noqa: E402
from shotflow.evidence import STATUSES, VARIANTS, record_attempt  # noqa: E402


def optional_path(value: str | None) -> Path | None:
    return Path(value) if value else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-dir", required=True)
    parser.add_argument("--variant", choices=VARIANTS, required=True)
    parser.add_argument("--status", choices=STATUSES, required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--attempt-id")
    parser.add_argument("--source-video")
    parser.add_argument("--source-final-frame")
    parser.add_argument("--output-video")
    parser.add_argument("--output-final-frame")
    parser.add_argument("--reason", default="")
    args = parser.parse_args()
    try:
        entry = record_attempt(
            Path(args.case_dir),
            args.variant,
            args.status,
            Path(args.prompt),
            attempt_id=args.attempt_id,
            source_video=optional_path(args.source_video),
            source_final_frame=optional_path(args.source_final_frame),
            output_video=optional_path(args.output_video),
            output_final_frame=optional_path(args.output_final_frame),
            reason=args.reason,
        )
    except (ShotFlowError, ValueError, FileNotFoundError) as exc:
        print(f"record_attempt: error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(entry, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
