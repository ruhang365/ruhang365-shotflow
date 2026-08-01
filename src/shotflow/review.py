"""Deterministic preparation of neutral A/B review media."""

from __future__ import annotations

import json
import math
import shutil
import subprocess
from pathlib import Path
from typing import Any

from .core import ShotFlowError, sha256_file, utc_now, write_json


EVALUATION_PAIR_VERSION = "1.0"
TARGET_WIDTH = 1280
TARGET_HEIGHT = 720
TARGET_FPS = 24
TARGET_DURATION_SECONDS = 5.0
CONTACT_TIMES_SECONDS = (0.0, 0.625, 1.25, 1.875, 2.5, 3.125, 3.75, 4.375, 4.958)


def _require_binary(name: str) -> str:
    binary = shutil.which(name)
    if binary is None:
        raise ShotFlowError(f"Required media tool is unavailable: {name}")
    return binary


def _run(command: list[str]) -> None:
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode:
        message = result.stderr.strip() or result.stdout.strip() or "unknown error"
        raise ShotFlowError(f"Media command failed: {message}")


def probe_video(path: Path) -> dict[str, Any]:
    """Return the one-video-stream metadata required by the public protocol."""

    if not path.is_file():
        raise ShotFlowError(f"Video file does not exist: {path}")
    ffprobe = _require_binary("ffprobe")
    result = subprocess.run(
        [
            ffprobe,
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height,avg_frame_rate,nb_frames,codec_name,pix_fmt",
            "-show_entries",
            "format=duration",
            "-of",
            "json",
            str(path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        raise ShotFlowError(f"Video decode probe failed: {result.stderr.strip()}")
    try:
        payload = json.loads(result.stdout)
        stream = payload["streams"][0]
        duration = float(payload["format"]["duration"])
        numerator, denominator = stream["avg_frame_rate"].split("/", 1)
        fps = float(numerator) / float(denominator)
        width = int(stream["width"])
        height = int(stream["height"])
    except (KeyError, IndexError, TypeError, ValueError, ZeroDivisionError) as exc:
        raise ShotFlowError(f"Video probe returned incomplete metadata: {path}") from exc
    return {
        "name": path.name,
        "sha256": sha256_file(path),
        "bytes": path.stat().st_size,
        "width": width,
        "height": height,
        "fps": round(fps, 6),
        "duration_seconds": round(duration, 6),
        "frames": int(stream["nb_frames"]) if stream.get("nb_frames", "").isdigit() else None,
        "codec": stream.get("codec_name"),
        "pixel_format": stream.get("pix_fmt"),
    }


def validate_native_video(metadata: dict[str, Any]) -> None:
    width = metadata["width"]
    height = metadata["height"]
    duration = metadata["duration_seconds"]
    if width < TARGET_WIDTH or height < TARGET_HEIGHT:
        raise ShotFlowError("Native video must be at least 1280x720")
    if not math.isclose(width / height, 16 / 9, rel_tol=0, abs_tol=0.002):
        raise ShotFlowError("Native video must use a 16:9 raster")
    if not 4.8 <= duration <= 5.2:
        raise ShotFlowError("Native video duration must be between 4.8 and 5.2 seconds")


def _canonicalize(source: Path, destination: Path) -> None:
    ffmpeg = _require_binary("ffmpeg")
    _run(
        [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(source),
            "-t",
            f"{TARGET_DURATION_SECONDS:.3f}",
            "-vf",
            f"scale={TARGET_WIDTH}:{TARGET_HEIGHT}:flags=lanczos,fps={TARGET_FPS}",
            "-an",
            "-c:v",
            "libx264",
            "-crf",
            "18",
            "-preset",
            "slow",
            "-pix_fmt",
            "yuv420p",
            "-map_metadata",
            "-1",
            str(destination),
        ]
    )


def _extract_frame(source: Path, destination: Path, timestamp: float) -> None:
    ffmpeg = _require_binary("ffmpeg")
    _run(
        [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-ss",
            f"{timestamp:.3f}",
            "-i",
            str(source),
            "-frames:v",
            "1",
            str(destination),
        ]
    )


def _contact_sheet(source: Path, destination: Path) -> None:
    ffmpeg = _require_binary("ffmpeg")
    select = "+".join(
        f"eq(n\\,{min(round(value * TARGET_FPS), 119)})"
        for value in CONTACT_TIMES_SECONDS
    )
    _run(
        [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(source),
            "-vf",
            f"select='{select}',scale=384:216,tile=3x3",
            "-frames:v",
            "1",
            str(destination),
        ]
    )


def _artifact(path: Path) -> dict[str, Any]:
    return {
        "name": path.name,
        "sha256": sha256_file(path),
        "bytes": path.stat().st_size,
    }


def prepare_blind_pair(
    *,
    case_id: str,
    pair_id: str,
    reference_frame: Path,
    baseline_video: Path,
    shotflow_video: Path,
    baseline_prompt: Path,
    shotflow_prompt: Path,
    output_directory: Path,
    variant_a: str,
    platform: str,
    model_tool: str,
    generation_mode: str,
    reasoning_mode: str,
    generation_order: tuple[str, str],
) -> dict[str, Any]:
    """Create canonical media plus public and reviewer manifests."""

    if variant_a not in {"baseline", "shotflow"}:
        raise ShotFlowError("variant_a must be baseline or shotflow")
    if set(generation_order) != {"baseline", "shotflow"}:
        raise ShotFlowError("generation_order must contain baseline and shotflow once")
    if not all(
        value.strip()
        for value in (platform, model_tool, generation_mode, reasoning_mode)
    ):
        raise ShotFlowError("Provider metadata must not be empty")
    for path, label in (
        (reference_frame, "reference frame"),
        (baseline_prompt, "baseline prompt"),
        (shotflow_prompt, "ShotFlow prompt"),
    ):
        if not path.is_file():
            raise ShotFlowError(f"Missing {label}: {path}")
    baseline_native = probe_video(baseline_video)
    shotflow_native = probe_video(shotflow_video)
    validate_native_video(baseline_native)
    validate_native_video(shotflow_native)

    output_directory.mkdir(parents=True, exist_ok=False)
    internal_directory = output_directory / "internal"
    reviewer_directory = output_directory / "reviewer"
    internal_directory.mkdir()
    reviewer_directory.mkdir()
    mapping = {
        "A": variant_a,
        "B": "shotflow" if variant_a == "baseline" else "baseline",
    }
    sources = {"baseline": baseline_video, "shotflow": shotflow_video}
    canonical: dict[str, dict[str, Any]] = {}
    review_assets: dict[str, dict[str, Any]] = {}
    for label in ("A", "B"):
        source = sources[mapping[label]]
        video = reviewer_directory / f"variant-{label.lower()}.mp4"
        first = reviewer_directory / f"variant-{label.lower()}-first.png"
        final = reviewer_directory / f"variant-{label.lower()}-final.png"
        sheet = reviewer_directory / f"variant-{label.lower()}-contact.png"
        _canonicalize(source, video)
        _extract_frame(video, first, 0.0)
        _extract_frame(video, final, 4.958)
        _contact_sheet(video, sheet)
        canonical[mapping[label]] = probe_video(video)
        review_assets[label] = {
            "video": _artifact(video),
            "first_frame": _artifact(first),
            "final_frame": _artifact(final),
            "contact_sheet": _artifact(sheet),
        }

    native = {"baseline": baseline_native, "shotflow": shotflow_native}
    manifest = {
        "evaluation_pair_version": EVALUATION_PAIR_VERSION,
        "case_id": case_id,
        "pair_id": pair_id,
        "status": "ready_for_blind_review",
        "prepared_at": utc_now(),
        "generation_order": list(generation_order),
        "blind_mapping": mapping,
        "provider": {
            "platform": platform,
            "model_tool": model_tool,
            "generation_mode": generation_mode,
            "reasoning_mode": reasoning_mode,
            "ratio": "16:9",
            "requested_duration_seconds": 5,
        },
        "jobs": {
            variant: {
                "status": "completed_media_supplied",
                "visible_cost": null_cost,
                "thread_id_sha256": None,
            }
            for variant, null_cost in (("baseline", None), ("shotflow", None))
        },
        "reference": _artifact(reference_frame),
        "prompts": {
            "baseline": _artifact(baseline_prompt),
            "shotflow": _artifact(shotflow_prompt),
        },
        "native": native,
        "canonicalization": {
            "width": TARGET_WIDTH,
            "height": TARGET_HEIGHT,
            "fps": TARGET_FPS,
            "duration_seconds": TARGET_DURATION_SECONDS,
            "video_codec": "h264",
            "crf": 18,
            "scale_filter": "lanczos",
            "crop": False,
            "upscale": False,
            "audio": False,
            "contact_times_seconds": list(CONTACT_TIMES_SECONDS),
        },
        "canonical": canonical,
        "review_assets": review_assets,
        "review": None,
    }
    write_json(internal_directory / "evaluation-pair.json", manifest)
    neutral_reference = reviewer_directory / "accepted-reference.png"
    shutil.copyfile(reference_frame, neutral_reference)
    reviewer_manifest = {
        "evaluation_pair_version": EVALUATION_PAIR_VERSION,
        "case_id": case_id,
        "pair_id": pair_id,
        "reference": _artifact(neutral_reference),
        "provider": manifest["provider"],
        "variants": review_assets,
        "rubric": [
            "subject_identity",
            "wardrobe_props",
            "space_direction",
            "motion_handoff",
            "light_material",
            "story_beat",
        ],
        "opening_frame_match": "pass_or_fail",
    }
    write_json(reviewer_directory / "review-package.json", reviewer_manifest)
    return manifest
