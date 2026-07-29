"""Public-safe generation attempt ledger."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from .core import ShotFlowError, read_json, sha256_file, utc_now, write_json

LEDGER_VERSION = "1.0"
ATTEMPT_CAPS = {
    "sky-mender": 8,
    "storm-deck": 5,
    "obsidian-bloom": 5,
}
VARIANTS = ("clip-01", "clip-02-baseline", "clip-02-shotflow")
STATUSES = ("submitted", "accepted", "rejected", "failed")


def _inside(case_root: Path, path: Path) -> tuple[Path, str]:
    root = case_root.resolve()
    resolved = path.expanduser().resolve(strict=True)
    try:
        relative = resolved.relative_to(root)
    except ValueError as exc:
        raise ShotFlowError(f"Evidence file must stay inside {case_root}: {path}") from exc
    return resolved, relative.as_posix()


def _artifact(case_root: Path, path: Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    resolved, relative = _inside(case_root, path)
    return {
        "path": relative,
        "sha256": sha256_file(resolved),
        "bytes": resolved.stat().st_size,
    }


def load_ledger(case_root: Path) -> tuple[Path, dict[str, Any]]:
    path = case_root / "attempts.json"
    if not path.exists():
        return path, {
            "ledger_version": LEDGER_VERSION,
            "case_id": case_root.name,
            "attempts": [],
        }
    ledger = read_json(path)
    if ledger.get("ledger_version") != LEDGER_VERSION:
        raise ShotFlowError("Unsupported attempt ledger version")
    if ledger.get("case_id") != case_root.name:
        raise ShotFlowError("Attempt ledger case_id does not match its directory")
    if not isinstance(ledger.get("attempts"), list):
        raise ShotFlowError("Attempt ledger attempts must be a list")
    return path, ledger


def record_attempt(
    case_root: Path,
    variant: str,
    status: str,
    prompt_path: Path,
    *,
    attempt_id: str | None = None,
    source_video: Path | None = None,
    source_final_frame: Path | None = None,
    output_video: Path | None = None,
    output_final_frame: Path | None = None,
    reason: str = "",
) -> dict[str, Any]:
    case_root = case_root.expanduser().resolve(strict=True)
    if variant not in VARIANTS:
        raise ShotFlowError(f"Unknown attempt variant {variant!r}")
    if status not in STATUSES:
        raise ShotFlowError(f"Unknown attempt status {status!r}")
    if variant != "clip-01" and (source_video is None or source_final_frame is None):
        raise ShotFlowError("Clip 02 attempts require the shared Clip 01 references")
    if status == "accepted" and (output_video is None or output_final_frame is None):
        raise ShotFlowError("Accepted attempts require output video and final frame")
    if status in {"rejected", "failed"} and not reason.strip():
        raise ShotFlowError(f"{status} attempts require a reason")

    prompt = _artifact(case_root, prompt_path)
    if prompt is None:
        raise ShotFlowError("Prompt is required")
    project = read_json(case_root / "shotflow.project.json")
    ledger_path, ledger = load_ledger(case_root)
    attempts = ledger["attempts"]
    existing = None
    if attempt_id:
        existing = next((item for item in attempts if item["attempt_id"] == attempt_id), None)
        if existing is None:
            raise ShotFlowError(f"Attempt {attempt_id!r} does not exist")
        if existing["variant"] != variant:
            raise ShotFlowError("Attempt variant cannot change")
        if existing["prompt"]["sha256"] != prompt["sha256"]:
            raise ShotFlowError("Attempt prompt cannot change after submission")
    else:
        cap = ATTEMPT_CAPS.get(case_root.name)
        if cap is None:
            raise ShotFlowError(f"No registered attempt cap for {case_root.name!r}")
        if len(attempts) >= cap:
            raise ShotFlowError(f"Attempt cap reached for {case_root.name}: {cap}")
        attempt_id = f"{case_root.name}-{len(attempts) + 1:03d}"

    entry = {
        "attempt_id": attempt_id,
        "variant": variant,
        "status": status,
        "recorded_at": utc_now(),
        "provider": deepcopy(project["provider"]),
        "prompt": prompt,
        "references": {
            "source_video": _artifact(case_root, source_video),
            "source_final_frame": _artifact(case_root, source_final_frame),
        },
        "output": {
            "video": _artifact(case_root, output_video),
            "final_frame": _artifact(case_root, output_final_frame),
        },
        "reason": reason.strip(),
    }
    if existing:
        attempts[attempts.index(existing)] = entry
    else:
        attempts.append(entry)
    write_json(ledger_path, ledger)
    return entry
