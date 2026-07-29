"""Deterministic ShotFlow state operations."""

from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .providers import get_adapter

SCHEMA_VERSION = "1.0"
CONTRACT_VERSION = "1.0"
PATCH_VERSION = "1.0"
PROMPT_PROFILE = "provider-direct-v2"

GRAMMAR_AXES = (
    "narrative_moment",
    "camera_movement",
    "light_color",
    "space_composition",
    "material_physics",
)

SCORE_DIMENSIONS = (
    "subject_identity",
    "wardrobe_props",
    "space_direction",
    "motion_handoff",
    "light_material",
    "story_beat",
)

REQUIRED_OBSERVED_STATE = (
    "identity",
    "wardrobe_props",
    "space_direction",
    "motion",
    "light_material",
    "story_beat",
)


class ShotFlowError(ValueError):
    """Raised when project or workflow invariants are violated."""


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "shotflow-project"


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ShotFlowError(f"File not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ShotFlowError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ShotFlowError(f"Expected a JSON object in {path}")
    return data


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    temporary.replace(path)


def resolve_project_file(path: str | Path) -> Path:
    candidate = Path(path).expanduser().resolve()
    if candidate.is_dir():
        candidate = candidate / "shotflow.project.json"
    return candidate


def load_project(path: str | Path) -> tuple[Path, dict[str, Any]]:
    project_file = resolve_project_file(path)
    project = read_json(project_file)
    validate_project(project)
    return project_file, project


def save_project(project_file: Path, project: dict[str, Any]) -> None:
    project["updated_at"] = utc_now()
    validate_project(project)
    write_json(project_file, project)


def new_project(
    title: str,
    provider_adapter: str = "seedance-2.0",
    model: str = "seedance2.0_vision",
    ratio: str = "16:9",
    resolution: str = "1080p",
    duration_seconds: int = 5,
) -> dict[str, Any]:
    if duration_seconds < 1:
        raise ShotFlowError("duration_seconds must be positive")
    if not ratio.strip() or not resolution.strip() or not model.strip():
        raise ShotFlowError("model, ratio, and resolution must not be empty")
    adapter = get_adapter(provider_adapter)
    verified = model in adapter.verified_models
    now = utc_now()
    return {
        "schema_version": SCHEMA_VERSION,
        "project": {
            "id": slugify(title),
            "title": title,
            "created_at": now,
        },
        "updated_at": now,
        "provider": {
            "adapter": provider_adapter,
            "model": model,
            "verified": verified,
            "parameters": {
                "ratio": ratio,
                "resolution": resolution,
                "duration_seconds": duration_seconds,
            },
        },
        "entities": [],
        "props": [],
        "grammar_defaults": {axis: "" for axis in GRAMMAR_AXES},
        "shots": [],
    }


def validate_project(project: dict[str, Any]) -> None:
    if project.get("schema_version") != SCHEMA_VERSION:
        raise ShotFlowError(
            f"Unsupported schema_version {project.get('schema_version')!r}; "
            f"expected {SCHEMA_VERSION!r}"
        )
    for key in ("project", "provider", "entities", "props", "grammar_defaults", "shots"):
        if key not in project:
            raise ShotFlowError(f"Project is missing required field {key!r}")
    if not isinstance(project["shots"], list):
        raise ShotFlowError("Project field 'shots' must be a list")
    provider = project["provider"]
    if not isinstance(provider, dict):
        raise ShotFlowError("Project field 'provider' must be an object")
    adapter = get_adapter(str(provider.get("adapter", "")))
    model = provider.get("model")
    verified = provider.get("verified")
    if not isinstance(model, str) or not model.strip():
        raise ShotFlowError("Provider field 'model' must be a non-empty string")
    if not isinstance(verified, bool):
        raise ShotFlowError("Provider field 'verified' must be a boolean")
    expected_verified = model in adapter.verified_models
    if verified != expected_verified:
        raise ShotFlowError(
            "Provider verified flag does not match the adapter's forward-tested models"
        )
    parameters = provider.get("parameters")
    if not isinstance(parameters, dict):
        raise ShotFlowError("Provider field 'parameters' must be an object")
    unknown_parameters = sorted(set(parameters) - set(adapter.parameter_names))
    if unknown_parameters:
        raise ShotFlowError(
            f"Unsupported provider parameters: {', '.join(unknown_parameters)}"
        )
    duration = parameters.get("duration_seconds")
    if isinstance(duration, bool) or not isinstance(duration, int) or duration < 1:
        raise ShotFlowError("Provider duration_seconds must be a positive integer")
    for key in ("ratio", "resolution"):
        if not isinstance(parameters.get(key), str) or not parameters[key].strip():
            raise ShotFlowError(f"Provider parameter {key!r} must be non-empty")
    seen: set[str] = set()
    for shot in project["shots"]:
        if not isinstance(shot, dict) or not shot.get("id"):
            raise ShotFlowError("Every shot must be an object with an id")
        if shot["id"] in seen:
            raise ShotFlowError(f"Duplicate shot id {shot['id']!r}")
        seen.add(shot["id"])


def validate_grammar(grammar: dict[str, Any]) -> None:
    missing = [axis for axis in GRAMMAR_AXES if not str(grammar.get(axis, "")).strip()]
    unknown = sorted(set(grammar) - set(GRAMMAR_AXES))
    if missing:
        raise ShotFlowError(f"Grammar is missing axes: {', '.join(missing)}")
    if unknown:
        raise ShotFlowError(f"Grammar has unknown axes: {', '.join(unknown)}")


def validate_observed_state(state: dict[str, Any]) -> None:
    missing = [key for key in REQUIRED_OBSERVED_STATE if key not in state]
    if missing:
        raise ShotFlowError(
            "Observed state is incomplete; missing categories: " + ", ".join(missing)
        )
    for key in REQUIRED_OBSERVED_STATE:
        if state[key] in (None, "", [], {}):
            raise ShotFlowError(f"Observed state category {key!r} must not be empty")


def find_shot(project: dict[str, Any], shot_id: str) -> dict[str, Any]:
    for shot in project["shots"]:
        if shot["id"] == shot_id:
            return shot
    raise ShotFlowError(f"Shot {shot_id!r} does not exist")


def add_or_replace_plan(
    project: dict[str, Any],
    shot_id: str,
    beat: str,
    specification: dict[str, Any],
    prompt_text: str | None = None,
) -> dict[str, Any]:
    grammar = specification.get("grammar")
    planned = specification.get("planned")
    if not isinstance(grammar, dict):
        raise ShotFlowError("Plan specification requires a grammar object")
    if not isinstance(planned, dict) or not planned:
        raise ShotFlowError("Plan specification requires a non-empty planned object")
    validate_grammar(grammar)
    shot: dict[str, Any] = {
        "id": shot_id,
        "beat": beat,
        "status": "planned",
        "planned": deepcopy(planned),
        "grammar": deepcopy(grammar),
        "continuity_locks": deepcopy(specification.get("continuity_locks", [])),
        "reference_shot_id": specification.get("reference_shot_id"),
        "artifacts": {},
        "prompt": None,
        "observed": None,
        "evaluation": None,
    }
    if prompt_text is not None:
        shot["prompt"] = {
            "text": prompt_text,
            "sha256": sha256_text(prompt_text),
            "frozen": True,
        }
    current = next((item for item in project["shots"] if item["id"] == shot_id), None)
    if current and current.get("observed"):
        raise ShotFlowError(
            f"Shot {shot_id!r} already has accepted evidence and cannot be replanned"
        )
    existing = [item for item in project["shots"] if item["id"] != shot_id]
    existing.append(shot)
    project["shots"] = existing
    return shot


def ensure_inside_project(project_file: Path, artifact: Path) -> tuple[Path, str]:
    project_root = project_file.parent.resolve()
    resolved = artifact.expanduser().resolve(strict=True)
    try:
        relative = resolved.relative_to(project_root)
    except ValueError as exc:
        raise ShotFlowError(
            f"Artifact must be inside the project directory: {artifact}"
        ) from exc
    if ".git" in relative.parts:
        raise ShotFlowError("Artifacts inside .git are not allowed")
    return resolved, relative.as_posix()


def build_artifact(project_file: Path, path: Path, kind: str) -> dict[str, Any]:
    resolved, relative = ensure_inside_project(project_file, path)
    return {
        "kind": kind,
        "path": relative,
        "sha256": sha256_file(resolved),
        "bytes": resolved.stat().st_size,
    }


def normalize_observation_patch(
    state_or_patch: dict[str, Any],
    shot_id: str,
    media_sha256: str,
) -> dict[str, Any]:
    if "patch_version" not in state_or_patch:
        state = state_or_patch
        validate_observed_state(state)
        return {
            "patch_version": PATCH_VERSION,
            "project_schema_version": SCHEMA_VERSION,
            "shot_id": shot_id,
            "source": "human",
            "media_sha256": media_sha256,
            "observed_at": utc_now(),
            "confidence": 1.0,
            "evidence": [],
            "state": deepcopy(state),
        }
    patch = deepcopy(state_or_patch)
    if patch.get("patch_version") != PATCH_VERSION:
        raise ShotFlowError("Unsupported observation patch version")
    if patch.get("project_schema_version") != SCHEMA_VERSION:
        raise ShotFlowError("Observation patch targets an unsupported project schema")
    if patch.get("shot_id") != shot_id:
        raise ShotFlowError("Observation patch shot_id does not match the command")
    if patch.get("media_sha256") != media_sha256:
        raise ShotFlowError("Observation patch media hash does not match the bound video")
    confidence = patch.get("confidence")
    if not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
        raise ShotFlowError("Observation patch confidence must be between 0 and 1")
    state = patch.get("state")
    if not isinstance(state, dict):
        raise ShotFlowError("Observation patch requires a state object")
    validate_observed_state(state)
    if not isinstance(patch.get("evidence", []), list):
        raise ShotFlowError("Observation patch evidence must be a list")
    return patch


def observe_shot(
    project_file: Path,
    project: dict[str, Any],
    shot_id: str,
    state_or_patch: dict[str, Any],
    media_path: Path,
    final_frame_path: Path,
) -> dict[str, Any]:
    shot = find_shot(project, shot_id)
    if shot.get("observed"):
        raise ShotFlowError(
            f"Shot {shot_id!r} already has an accepted observation; use a new shot id"
        )
    media = build_artifact(project_file, media_path, "video")
    final_frame = build_artifact(project_file, final_frame_path, "final_frame")
    patch = normalize_observation_patch(state_or_patch, shot_id, media["sha256"])
    shot["artifacts"] = {"video": media, "final_frame": final_frame}
    shot["observed"] = patch
    shot["status"] = "observed"
    return patch


def _walk_diff(
    planned: Any,
    observed: Any,
    prefix: str,
    output: list[dict[str, Any]],
) -> None:
    if isinstance(planned, dict) and isinstance(observed, dict):
        keys = sorted(set(planned) | set(observed))
        for key in keys:
            path = f"{prefix}.{key}" if prefix else key
            if key not in planned:
                output.append(
                    {"path": path, "kind": "observed_only", "observed": observed[key]}
                )
            elif key not in observed:
                output.append(
                    {"path": path, "kind": "not_observed", "planned": planned[key]}
                )
            else:
                _walk_diff(planned[key], observed[key], path, output)
        return
    if planned != observed:
        output.append(
            {"path": prefix, "kind": "changed", "planned": planned, "observed": observed}
        )


def diff_states(planned: dict[str, Any], observed: dict[str, Any]) -> list[dict[str, Any]]:
    changes: list[dict[str, Any]] = []
    _walk_diff(planned, observed, "", changes)
    return changes


def shot_diff(project: dict[str, Any], shot_id: str) -> dict[str, Any]:
    shot = find_shot(project, shot_id)
    if not shot.get("observed"):
        raise ShotFlowError(
            f"Shot {shot_id!r} has no accepted observation; planned state is not evidence"
        )
    observed_state = shot["observed"]["state"]
    validate_observed_state(observed_state)
    return {
        "shot_id": shot_id,
        "authoritative_source": "observed",
        "continuity_safe_source": True,
        "changes": diff_states(shot["planned"], observed_state),
    }


def continuity_locks_from_state(state: dict[str, Any]) -> list[dict[str, Any]]:
    validate_observed_state(state)
    return [
        {
            "category": category,
            "value": deepcopy(state[category]),
            "source": "observed",
            "required": True,
        }
        for category in REQUIRED_OBSERVED_STATE
    ]


def _render_value(value: Any) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def render_prompt(
    beat: str,
    state: dict[str, Any],
    grammar: dict[str, Any],
) -> str:
    lines = [
        "CONTINUE FROM THE PROVIDED VIDEO AND FINAL FRAME.",
        "",
        "Required visible action:",
        f"- {beat}",
        f"- Physical order: {_render_value(grammar['narrative_moment'])}",
        "- The final seconds must visibly prove the required action. Do not stop at setup.",
        "",
        "Opening continuity locks — match before advancing the action:",
        f"- motion: {_render_value(state['motion'])}",
        f"- space: {_render_value(state['space_direction'])}",
        f"- subject: {_render_value(state['identity'])}",
        f"- props and wardrobe: {_render_value(state['wardrobe_props'])}",
        f"- light and material: {_render_value(state['light_material'])}",
        "",
        "Shot execution:",
        f"- camera: {_render_value(grammar['camera_movement'])}",
        f"- composition: {_render_value(grammar['space_composition'])}",
        f"- lighting: {_render_value(grammar['light_color'])}",
        f"- physics: {_render_value(grammar['material_physics'])}",
        "",
        "Hard rule: continue the accepted action from its real endpoint. "
        "Do not reset pose, prop ownership, screen direction, lighting source, "
        "material state, or spatial geography.",
    ]
    return "\n".join(lines).rstrip() + "\n"


def compile_next_shot(
    project: dict[str, Any],
    source_shot_id: str,
    next_shot_id: str,
    beat: str,
    grammar: dict[str, Any],
) -> dict[str, Any]:
    validate_grammar(grammar)
    source = find_shot(project, source_shot_id)
    observed = source.get("observed")
    if not observed:
        raise ShotFlowError(
            "Cannot compile a continuity-safe next shot without an accepted observation"
        )
    state = observed.get("state")
    if not isinstance(state, dict):
        raise ShotFlowError("Source observation has no state object")
    validate_observed_state(state)
    video = source.get("artifacts", {}).get("video")
    final_frame = source.get("artifacts", {}).get("final_frame")
    if not video or not final_frame:
        raise ShotFlowError("Source shot must bind a video and final frame")
    contract = {
        "contract_version": CONTRACT_VERSION,
        "project_schema_version": SCHEMA_VERSION,
        "source_shot_id": source_shot_id,
        "next_shot_id": next_shot_id,
        "continuity_safe": True,
        "authoritative_source": "observed",
        "source_artifacts": {
            "video_sha256": video["sha256"],
            "final_frame_sha256": final_frame["sha256"],
        },
        "beat": beat,
        "observed_state": deepcopy(state),
        "continuity_locks": continuity_locks_from_state(state),
        "grammar": deepcopy(grammar),
    }
    prompt = render_prompt(beat, state, grammar)
    contract["compiled_prompt"] = {
        "text": prompt,
        "sha256": sha256_text(prompt),
        "frozen": True,
        "profile": PROMPT_PROFILE,
    }
    next_shot = {
        "id": next_shot_id,
        "beat": beat,
        "status": "compiled",
        "planned": deepcopy(state),
        "grammar": deepcopy(grammar),
        "continuity_locks": deepcopy(contract["continuity_locks"]),
        "reference_shot_id": source_shot_id,
        "artifacts": {},
        "prompt": deepcopy(contract["compiled_prompt"]),
        "observed": None,
        "evaluation": None,
        "contract": {
            "version": CONTRACT_VERSION,
            "continuity_safe": True,
            "source_video_sha256": video["sha256"],
            "source_final_frame_sha256": final_frame["sha256"],
        },
    }
    existing = next(
        (shot for shot in project["shots"] if shot["id"] == next_shot_id), None
    )
    if existing and existing.get("observed"):
        raise ShotFlowError(
            f"Shot {next_shot_id!r} already has accepted evidence and cannot be replaced"
        )
    project["shots"] = [
        shot for shot in project["shots"] if shot["id"] != next_shot_id
    ] + [next_shot]
    return contract


def _parse_dimension(value: Any, dimension: str) -> tuple[int | None, str]:
    if isinstance(value, dict):
        score = value.get("score")
        note = str(value.get("note", ""))
    else:
        score = value
        note = ""
    if isinstance(score, str) and score.lower() in {"n/a", "na", "not_applicable"}:
        return None, note
    if isinstance(score, bool) or not isinstance(score, int) or score not in (0, 1, 2):
        raise ShotFlowError(
            f"Evaluation dimension {dimension!r} must be 0, 1, 2, or 'n/a'"
        )
    return score, note


def score_evaluation(evaluation: dict[str, Any]) -> dict[str, Any]:
    unknown = sorted(set(evaluation) - set(SCORE_DIMENSIONS))
    missing = [dimension for dimension in SCORE_DIMENSIONS if dimension not in evaluation]
    if unknown:
        raise ShotFlowError(f"Unknown evaluation dimensions: {', '.join(unknown)}")
    if missing:
        raise ShotFlowError(f"Missing evaluation dimensions: {', '.join(missing)}")
    total = 0
    applicable = 0
    normalized: dict[str, Any] = {}
    for dimension in SCORE_DIMENSIONS:
        score, note = _parse_dimension(evaluation[dimension], dimension)
        normalized[dimension] = {"score": "n/a" if score is None else score, "note": note}
        if score is not None:
            total += score
            applicable += 1
    if not applicable:
        raise ShotFlowError("At least one evaluation dimension must be applicable")
    percentage = round((total / (2 * applicable)) * 100, 2)
    return {
        "rubric_version": "1.0",
        "dimensions": normalized,
        "applicable_dimensions": applicable,
        "score": percentage,
        "maximum": 100,
    }


def apply_score(
    project: dict[str, Any], shot_id: str, evaluation: dict[str, Any]
) -> dict[str, Any]:
    shot = find_shot(project, shot_id)
    if not shot.get("observed") or not shot.get("artifacts", {}).get("video"):
        raise ShotFlowError(
            f"Shot {shot_id!r} must bind an accepted observed video before scoring"
        )
    result = score_evaluation(evaluation)
    result["evaluated_at"] = utc_now()
    shot["evaluation"] = result
    return result


def json_output(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2)


def require_keys(mapping: dict[str, Any], keys: Iterable[str], label: str) -> None:
    missing = [key for key in keys if key not in mapping]
    if missing:
        raise ShotFlowError(f"{label} is missing fields: {', '.join(missing)}")
