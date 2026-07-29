#!/usr/bin/env python3
"""Run ShotFlow from a repository clone without installing the package."""

from __future__ import annotations

import sys
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
SOURCE_ROOT = REPOSITORY_ROOT / "src"
if not SOURCE_ROOT.is_dir():
    raise SystemExit(
        "ShotFlow source was not found. Run this script from an intact repository clone."
    )

sys.path.insert(0, str(SOURCE_ROOT))

from shotflow.cli import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
