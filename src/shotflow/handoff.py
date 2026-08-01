"""Provider-neutral reference handoff manifests.

The Core CLI never submits provider jobs. This module prepares an auditable
handoff that keeps attachment roles, prompt hashes, and output selection rules
explicit for an external runner.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable

from .core import (
    SCHEMA_VERSION,
    ShotFlowError,
    build_artifact,
    find_shot,
    load_project,
    sha256_text,
)


HANDOFF_VERSION = "1.0"
CAUSAL_HANDOFF_VERSION = "1.1"
VIDEO_CONTEXT_PROFILE = "video-context-v1"
ANCHOR_FRAME_PROFILE = "anchor-frame-v1"
ANCHOR_FRAME_V2_PROFILE = "anchor-frame-v2"
HANDOFF_PROFILES = (
    VIDEO_CONTEXT_PROFILE,
    ANCHOR_FRAME_PROFILE,
    ANCHOR_FRAME_V2_PROFILE,
)

VIDEO_CONTEXT_DIRECTIVE = """REFERENCE BINDING — APPLY BEFORE THE CREATIVE INSTRUCTIONS:
- Attachment 1 is the authoritative opening frame from the accepted previous shot. The first generated frame must match its subject, prop placement, pose, camera side, and spatial geography before the action advances.
- Attachment 2 is the accepted previous-shot video. Use it only for identity, material, lighting, and incoming-motion context; do not restart from its opening or insert an empty establishing frame.
- If the two references appear to conflict, Attachment 1 wins because it is the observed endpoint.

CREATIVE INSTRUCTIONS — KEEP UNCHANGED:
"""

ANCHOR_FRAME_DIRECTIVE = """ANCHOR-FRAME BINDING — APPLY BEFORE THE CREATIVE INSTRUCTIONS:
- Attachment 1 is the only media reference and the authoritative opening frame from the accepted previous shot. Start directly from this exact subject, prop geometry, pose, camera side, composition, lighting, and material state.
- No source video is attached. Treat incoming motion and unresolved forces stated in the creative instructions as observed state to continue from Attachment 1; do not invent earlier frames.
- Do not insert an empty establishing frame, recreate the previous shot, or move any visible element before the requested continuation begins.

CREATIVE INSTRUCTIONS — KEEP UNCHANGED:
"""

ANCHOR_FRAME_V2_DIRECTIVE = """OPENING-FRAME AUTHORITY:
- Attachment 1 is the accepted previous-shot endpoint and the authoritative opening frame.
- Generated frame 1 reproduces its subject, geometry, pose, camera, composition, lighting, and material state.
- The creative timeline begins from this matched state.

CREATIVE INSTRUCTIONS:
"""


def compile_submission_prompt(
    creative_prompt: str,
    profile: str = VIDEO_CONTEXT_PROFILE,
) -> str:
    """Wrap an approved creative prompt with provider-neutral reference roles."""

    if not creative_prompt.strip():
        raise ShotFlowError("Creative prompt must not be empty")
    if profile not in HANDOFF_PROFILES:
        raise ShotFlowError(f"Unknown provider handoff profile {profile!r}")
    if profile == ANCHOR_FRAME_V2_PROFILE:
        directive = ANCHOR_FRAME_V2_DIRECTIVE
    elif profile == ANCHOR_FRAME_PROFILE:
        directive = ANCHOR_FRAME_DIRECTIVE
    else:
        directive = VIDEO_CONTEXT_DIRECTIVE
    return directive + creative_prompt.rstrip() + "\n"


def prepare_provider_handoff(
    project_path: str | Path,
    *,
    source_shot_id: str,
    variant: str,
    creative_prompt_path: Path,
    platform: str,
    model_tool: str,
    profile: str = VIDEO_CONTEXT_PROFILE,
    known_output_paths: Iterable[Path] = (),
    opening_frame_review: str = "pending",
) -> dict[str, Any]:
    """Create a public-safe manifest for an external provider runner."""

    if not variant.strip() or not platform.strip() or not model_tool.strip():
        raise ShotFlowError("Variant, platform, and model tool must not be empty")
    if profile not in HANDOFF_PROFILES:
        raise ShotFlowError(f"Unknown provider handoff profile {profile!r}")
    if opening_frame_review not in {"pending", "accepted", "rejected"}:
        raise ShotFlowError("Opening-frame review must be pending, accepted, or rejected")
    project_file, project = load_project(project_path)
    source = find_shot(project, source_shot_id)
    if source.get("status") != "observed" or not source.get("observed"):
        raise ShotFlowError("Provider handoff requires an accepted observed source shot")
    artifacts = source.get("artifacts")
    if not isinstance(artifacts, dict):
        raise ShotFlowError("Observed source shot is missing artifacts")
    video = artifacts.get("video")
    final_frame = artifacts.get("final_frame")
    if not isinstance(video, dict) or not isinstance(final_frame, dict):
        raise ShotFlowError("Provider handoff requires source video and final frame")

    prompt_artifact = build_artifact(project_file, creative_prompt_path, "prompt")
    creative_prompt = creative_prompt_path.read_text(encoding="utf-8")
    submission_prompt = compile_submission_prompt(creative_prompt, profile)
    known_hashes = sorted(
        {
            build_artifact(project_file, path, "prior_output")["sha256"]
            for path in known_output_paths
        }
    )
    references = [
        {
            "attachment_index": 1,
            "role": "authoritative_opening_frame",
            "authority": "accepted_observed_endpoint",
            "artifact": deepcopy(final_frame),
        }
    ]
    if profile == VIDEO_CONTEXT_PROFILE:
        references.append(
            {
                "attachment_index": 2,
                "role": "motion_context_video",
                "authority": "context_only",
                "artifact": deepcopy(video),
            }
        )
    return {
        "handoff_version": (
            CAUSAL_HANDOFF_VERSION
            if profile == ANCHOR_FRAME_V2_PROFILE
            else HANDOFF_VERSION
        ),
        "project_schema_version": SCHEMA_VERSION,
        "profile": profile,
        "project_id": project["project"]["id"],
        "variant": variant,
        "source_shot_id": source_shot_id,
        "provider": {
            "platform": platform,
            "model_tool": model_tool,
        },
        "creative_prompt": prompt_artifact,
        "submission_prompt": {
            "text": submission_prompt,
            "sha256": sha256_text(submission_prompt),
            "creative_prompt_sha256": prompt_artifact["sha256"],
        },
        "references": references,
        "known_output_sha256": known_hashes,
        "acceptance_gates": {
            "new_artifact_hash_required": True,
            "opening_frame_match_required": True,
            "opening_frame_review": opening_frame_review,
            "continuity_safe": False,
        },
    }


def select_single_new_output(
    project_path: str | Path,
    output_paths: Iterable[Path],
    known_output_sha256: Iterable[str],
) -> dict[str, Any]:
    """Reject historical artifacts and require exactly one new output hash."""

    project_file, _ = load_project(project_path)
    known = set(known_output_sha256)
    candidates = [
        build_artifact(project_file, path, "video") for path in output_paths
    ]
    new = [item for item in candidates if item["sha256"] not in known]
    if len(new) != 1:
        raise ShotFlowError(
            "Expected exactly one new provider artifact after excluding known hashes; "
            f"found {len(new)}"
        )
    return new[0]
