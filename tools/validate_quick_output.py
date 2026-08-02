#!/usr/bin/env python3
"""Validate one saved Quick Entry 1.0 response."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from shotflow.quick_entry import QUICK_ENTRY_VERSION, extract_quick_prompt, validate_quick_output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--ratio", required=True)
    args = parser.parse_args()
    text = args.output.read_text(encoding="utf-8")
    prompt, _ = extract_quick_prompt(text)
    errors = validate_quick_output(text, expected_ratio=args.ratio)
    print(
        json.dumps(
            {
                "quick_entry_version": QUICK_ENTRY_VERSION,
                "valid": not errors,
                "prompt_characters": len(prompt),
                "errors": errors,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
