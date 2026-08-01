"""Deterministic ShotFlow state operations."""

from __future__ import annotations

import hashlib
import json
import math
import re
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .providers import get_adapter

SCHEMA_VERSION = "1.0"
CONTRACT_VERSION = "1.1"
CAUSAL_CONTRACT_VERSION = "1.2"
PATCH_VERSION = "1.0"
SEQUENCE_VERSION = "1.0"
CAUSAL_SEQUENCE_VERSION = "1.1"
PROMPT_PROFILE = "provider-direct-v3"
CAUSAL_PROMPT_PROFILE = "provider-direct-v4"

CHECKPOINT_PHASES = ("match", "continue", "initiate", "resolve", "hold")
SEQUENCE_ANCHORS = (
    "identity",
    "wardrobe_props",
    "space_direction",
    "light_material",
)
NEGATIVE_DIRECTIVE = re.compile(
    r"\b(?:do not|don't|must not|never|avoid|without|cannot)\b|"
    r"(?:不要|不得|禁止|避免|不能)",
    re.IGNORECASE,
)
MAX_SEQUENCE_PROMPT_CHARS = 2400
MAX_CAUSAL_PROMPT_CHARS = 1800
CHANGE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

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
    model: str = "seedance2.0_direct",
    ratio: str = "16:9",
    resolution: str = "720p",
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


def _validate_positive_text(value: Any, field: str, maximum: int) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ShotFlowError(f"{field} must be a non-empty string")
    text = value.strip()
    if len(text) > maximum:
        raise ShotFlowError(f"{field} exceeds {maximum} characters")
    if NEGATIVE_DIRECTIVE.search(text):
        raise ShotFlowError(
            f"{field} uses a negative directive; rewrite it as a visible positive state"
        )
    return text


def validate_ordered_sequence(
    sequence: dict[str, Any],
    duration_seconds: int,
) -> None:
    if not isinstance(sequence, dict):
        raise ShotFlowError("Ordered sequence must be an object")
    version = sequence.get("sequence_version")
    if version not in {SEQUENCE_VERSION, CAUSAL_SEQUENCE_VERSION}:
        raise ShotFlowError(f"Unsupported sequence_version {version!r}")
    required = {"sequence_version", "duration_seconds", "anchors", "checkpoints"}
    if version == CAUSAL_SEQUENCE_VERSION:
        required.add("change_budget")
    missing = sorted(required - set(sequence))
    unknown = sorted(set(sequence) - required)
    if missing:
        raise ShotFlowError(
            "Ordered sequence is missing fields: " + ", ".join(missing)
        )
    if unknown:
        raise ShotFlowError(
            "Ordered sequence has unknown fields: " + ", ".join(unknown)
        )
    sequence_duration = sequence["duration_seconds"]
    if (
        isinstance(sequence_duration, bool)
        or not isinstance(sequence_duration, (int, float))
        or not math.isclose(float(sequence_duration), float(duration_seconds))
    ):
        raise ShotFlowError(
            "Ordered sequence duration_seconds must match the provider duration"
        )

    anchors = sequence["anchors"]
    if not isinstance(anchors, dict):
        raise ShotFlowError("Ordered sequence anchors must be an object")
    missing_anchors = sorted(set(SEQUENCE_ANCHORS) - set(anchors))
    unknown_anchors = sorted(set(anchors) - set(SEQUENCE_ANCHORS))
    if missing_anchors:
        raise ShotFlowError(
            "Ordered sequence is missing anchors: " + ", ".join(missing_anchors)
        )
    if unknown_anchors:
        raise ShotFlowError(
            "Ordered sequence has unknown anchors: " + ", ".join(unknown_anchors)
        )
    for category in SEQUENCE_ANCHORS:
        _validate_positive_text(anchors[category], f"anchors.{category}", 320)

    transition_ids: set[str] = set()
    if version == CAUSAL_SEQUENCE_VERSION:
        transition_ids = _validate_change_budget(sequence["change_budget"])

    checkpoints = sequence["checkpoints"]
    if not isinstance(checkpoints, list) or len(checkpoints) != len(CHECKPOINT_PHASES):
        raise ShotFlowError("Ordered sequence requires exactly five checkpoints")
    previous_end = 0.0
    checkpoint_fields = {
        "phase",
        "start_seconds",
        "end_seconds",
        "state",
        "visual_test",
    }
    if version == CAUSAL_SEQUENCE_VERSION:
        checkpoint_fields.add("active_changes")
    used_transitions: set[str] = set()
    for index, (checkpoint, expected_phase) in enumerate(
        zip(checkpoints, CHECKPOINT_PHASES, strict=True), start=1
    ):
        if not isinstance(checkpoint, dict):
            raise ShotFlowError(f"Checkpoint {index} must be an object")
        missing_checkpoint = sorted(checkpoint_fields - set(checkpoint))
        unknown_checkpoint = sorted(set(checkpoint) - checkpoint_fields)
        if missing_checkpoint:
            raise ShotFlowError(
                f"Checkpoint {index} is missing fields: "
                + ", ".join(missing_checkpoint)
            )
        if unknown_checkpoint:
            raise ShotFlowError(
                f"Checkpoint {index} has unknown fields: "
                + ", ".join(unknown_checkpoint)
            )
        if checkpoint["phase"] != expected_phase:
            raise ShotFlowError(
                f"Checkpoint {index} phase must be {expected_phase!r}"
            )
        start = checkpoint["start_seconds"]
        end = checkpoint["end_seconds"]
        if (
            isinstance(start, bool)
            or isinstance(end, bool)
            or not isinstance(start, (int, float))
            or not isinstance(end, (int, float))
        ):
            raise ShotFlowError(f"Checkpoint {index} times must be numbers")
        start_value = float(start)
        end_value = float(end)
        if not math.isclose(start_value, previous_end, abs_tol=1e-6):
            raise ShotFlowError(
                f"Checkpoint {index} must start when the previous checkpoint ends"
            )
        if end_value <= start_value:
            raise ShotFlowError(f"Checkpoint {index} end_seconds must follow its start")
        if end_value > float(duration_seconds) + 1e-6:
            raise ShotFlowError(f"Checkpoint {index} exceeds the provider duration")
        _validate_positive_text(
            checkpoint["state"], f"checkpoints[{index}].state", 360
        )
        _validate_positive_text(
            checkpoint["visual_test"], f"checkpoints[{index}].visual_test", 240
        )
        if version == CAUSAL_SEQUENCE_VERSION:
            active_changes = checkpoint["active_changes"]
            if not isinstance(active_changes, list) or any(
                not isinstance(item, str) for item in active_changes
            ):
                raise ShotFlowError(
                    f"checkpoints[{index}].active_changes must be an array of ids"
                )
            if len(active_changes) != len(set(active_changes)):
                raise ShotFlowError(
                    f"checkpoints[{index}].active_changes contains duplicate ids"
                )
            unknown_changes = sorted(set(active_changes) - transition_ids)
            if unknown_changes:
                raise ShotFlowError(
                    f"Checkpoint {index} references unknown transitions: "
                    + ", ".join(unknown_changes)
                )
            if expected_phase in {"match", "hold"} and active_changes:
                raise ShotFlowError(
                    f"Checkpoint phase {expected_phase!r} cannot have active changes"
                )
            used_transitions.update(active_changes)
        previous_end = end_value
    if not math.isclose(previous_end, float(duration_seconds), abs_tol=1e-6):
        raise ShotFlowError(
            "The final checkpoint must end at the provider duration"
        )
    unused_transitions = sorted(transition_ids - used_transitions)
    if unused_transitions:
        raise ShotFlowError(
            "Ordered sequence has unused transitions: " + ", ".join(unused_transitions)
        )


def _validate_change_id(value: Any, field: str) -> str:
    if not isinstance(value, str) or not CHANGE_ID.fullmatch(value):
        raise ShotFlowError(
            f"{field} must use lowercase letters, digits, and single hyphens"
        )
    if len(value) > 64:
        raise ShotFlowError(f"{field} exceeds 64 characters")
    return value


def _validate_change_budget(change_budget: Any) -> set[str]:
    if not isinstance(change_budget, dict):
        raise ShotFlowError("change_budget must be an object")
    required = {"protected", "transitions"}
    missing = sorted(required - set(change_budget))
    unknown = sorted(set(change_budget) - required)
    if missing:
        raise ShotFlowError(
            "change_budget is missing fields: " + ", ".join(missing)
        )
    if unknown:
        raise ShotFlowError(
            "change_budget has unknown fields: " + ", ".join(unknown)
        )

    protected = change_budget["protected"]
    transitions = change_budget["transitions"]
    if not isinstance(protected, list) or not 1 <= len(protected) <= 6:
        raise ShotFlowError("change_budget.protected requires 1 to 6 items")
    if not isinstance(transitions, list) or not 1 <= len(transitions) <= 3:
        raise ShotFlowError("change_budget.transitions requires 1 to 3 items")

    protected_ids: set[str] = set()
    for index, item in enumerate(protected, start=1):
        if not isinstance(item, dict) or set(item) != {"id", "state"}:
            raise ShotFlowError(
                f"change_budget.protected[{index}] requires only id and state"
            )
        item_id = _validate_change_id(
            item["id"], f"change_budget.protected[{index}].id"
        )
        if item_id in protected_ids:
            raise ShotFlowError(f"Duplicate change budget id {item_id!r}")
        protected_ids.add(item_id)
        _validate_positive_text(
            item["state"], f"change_budget.protected[{index}].state", 240
        )

    transition_ids: set[str] = set()
    transition_fields = {
        "id",
        "subject",
        "from_state",
        "transition",
        "to_state",
        "proof",
    }
    for index, item in enumerate(transitions, start=1):
        if not isinstance(item, dict) or set(item) != transition_fields:
            raise ShotFlowError(
                f"change_budget.transitions[{index}] requires exactly "
                "id, subject, from_state, transition, to_state, and proof"
            )
        item_id = _validate_change_id(
            item["id"], f"change_budget.transitions[{index}].id"
        )
        if item_id in transition_ids or item_id in protected_ids:
            raise ShotFlowError(f"Duplicate change budget id {item_id!r}")
        transition_ids.add(item_id)
        for field in transition_fields - {"id"}:
            _validate_positive_text(
                item[field], f"change_budget.transitions[{index}].{field}", 240
            )
    return transition_ids


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


def validate_media_signature(path: Path, kind: str) -> None:
    """Reject obvious non-media files without claiming full decode validation."""

    if kind not in {"video", "final_frame"}:
        return
    with path.open("rb") as handle:
        header = handle.read(16)
    if kind == "video":
        recognized = (
            header[4:8] == b"ftyp"  # MP4, MOV, and related ISO base media
            or header.startswith(b"\x1a\x45\xdf\xa3")  # WebM or Matroska
            or (header.startswith(b"RIFF") and header[8:12] == b"AVI ")
            or header.startswith((b"\x00\x00\x01\xba", b"\x00\x00\x01\xb3"))
        )
        label = "Video"
    else:
        recognized = (
            header.startswith(b"\x89PNG\r\n\x1a\n")
            or header.startswith(b"\xff\xd8\xff")
            or (header.startswith(b"RIFF") and header[8:12] == b"WEBP")
            or header.startswith((b"GIF87a", b"GIF89a", b"BM", b"II*\x00", b"MM\x00*"))
        )
        label = "Final-frame"
    if not recognized:
        raise ShotFlowError(
            f"{label} artifact has no recognized media signature: {path}"
        )


def build_artifact(project_file: Path, path: Path, kind: str) -> dict[str, Any]:
    resolved, relative = ensure_inside_project(project_file, path)
    validate_media_signature(resolved, kind)
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
    grammar: dict[str, Any],
    sequence: dict[str, Any],
) -> str:
    if sequence.get("sequence_version") == CAUSAL_SEQUENCE_VERSION:
        return render_causal_prompt(beat, grammar, sequence)
    beat_text = _validate_positive_text(beat, "beat", 320)
    for axis in GRAMMAR_AXES:
        _validate_positive_text(grammar[axis], f"grammar.{axis}", 360)
    checkpoints = sequence["checkpoints"]
    anchors = sequence["anchors"]
    lines = [
        "CONTINUE FROM THE ACCEPTED FINAL FRAME.",
        "",
        f"Story outcome: {beat_text}",
        "",
        "Five visible checkpoints — follow this exact order:",
    ]
    for index, checkpoint in enumerate(checkpoints, start=1):
        start = float(checkpoint["start_seconds"])
        end = float(checkpoint["end_seconds"])
        lines.append(
            f"{index}. {checkpoint['phase'].upper()} | {start:.2f}-{end:.2f}s — "
            f"{checkpoint['state'].strip()}"
        )
    lines.extend(
        [
            "",
            "Continuity anchors throughout:",
            f"- identity: {anchors['identity'].strip()}",
            f"- props: {anchors['wardrobe_props'].strip()}",
            f"- space: {anchors['space_direction'].strip()}",
            f"- light and material: {anchors['light_material'].strip()}",
            "",
            "Cinematic execution:",
            f"- narrative rhythm: {_render_value(grammar['narrative_moment'])}",
            f"- camera: {_render_value(grammar['camera_movement'])}",
            f"- composition: {_render_value(grammar['space_composition'])}",
            f"- lighting: {_render_value(grammar['light_color'])}",
            f"- physics: {_render_value(grammar['material_physics'])}",
            "",
            f"Completion: reach and clearly hold checkpoint 5 by "
            f"{float(sequence['duration_seconds']):.2f}s.",
        ]
    )
    prompt = "\n".join(lines).rstrip() + "\n"
    if len(prompt) > MAX_SEQUENCE_PROMPT_CHARS:
        raise ShotFlowError(
            f"Compiled provider prompt exceeds {MAX_SEQUENCE_PROMPT_CHARS} characters; "
            "shorten anchors or checkpoints"
        )
    return prompt


def render_causal_prompt(
    beat: str,
    grammar: dict[str, Any],
    sequence: dict[str, Any],
) -> str:
    beat_text = _validate_positive_text(beat, "beat", 320)
    for axis in GRAMMAR_AXES:
        _validate_positive_text(grammar[axis], f"grammar.{axis}", 360)
    checkpoints = sequence["checkpoints"]
    change_budget = sequence["change_budget"]
    lines = [
        "CONTINUE FROM THE ACCEPTED FINAL FRAME.",
        "",
        "OPENING MATCH",
        checkpoints[0]["state"].strip(),
        "",
        "PROTECTED THROUGHOUT",
    ]
    for item in change_budget["protected"]:
        lines.append(f"- {item['state'].strip()}")
    lines.extend(["", "AUTHORIZED CHANGES IN ORDER"])
    for index, item in enumerate(change_budget["transitions"], start=1):
        lines.append(
            f"{index}. {item['transition'].strip()} -> {item['to_state'].strip()}"
        )
    lines.extend(["", "FIVE VISIBLE CHECKPOINTS"])
    for index, checkpoint in enumerate(checkpoints, start=1):
        start = float(checkpoint["start_seconds"])
        end = float(checkpoint["end_seconds"])
        state = (
            "The opening match above holds."
            if checkpoint["phase"] == "match"
            else checkpoint["state"].strip()
        )
        lines.append(
            f"{index}. {checkpoint['phase'].upper()} | {start:.2f}-{end:.2f}s"
            f" — {state}"
        )
    lines.extend(["", "FINAL PROOF"])
    for item in change_budget["transitions"]:
        lines.append(f"- {item['proof'].strip()}")
    lines.append("- hold: Checkpoint 5 stays clearly visible.")
    prompt = "\n".join(lines).rstrip() + "\n"
    if len(prompt) > MAX_CAUSAL_PROMPT_CHARS:
        raise ShotFlowError(
            f"Compiled provider prompt exceeds {MAX_CAUSAL_PROMPT_CHARS} characters; "
            "shorten protected states, transitions, or checkpoints"
        )
    return prompt


def compile_next_shot(
    project: dict[str, Any],
    source_shot_id: str,
    next_shot_id: str,
    beat: str,
    grammar: dict[str, Any],
    sequence: dict[str, Any],
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
    duration_seconds = project["provider"]["parameters"]["duration_seconds"]
    validate_ordered_sequence(sequence, duration_seconds)
    prompt = render_prompt(beat, grammar, sequence)
    causal_sequence = sequence["sequence_version"] == CAUSAL_SEQUENCE_VERSION
    contract_version = (
        CAUSAL_CONTRACT_VERSION if causal_sequence else CONTRACT_VERSION
    )
    prompt_profile = CAUSAL_PROMPT_PROFILE if causal_sequence else PROMPT_PROFILE
    sequence_sha256 = sha256_text(canonical_json(sequence))
    contract = {
        "contract_version": contract_version,
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
        "observed_state_sha256": sha256_text(canonical_json(state)),
        "continuity_locks": continuity_locks_from_state(state),
        "grammar": deepcopy(grammar),
        "ordered_sequence": deepcopy(sequence),
        "ordered_sequence_sha256": sequence_sha256,
    }
    contract["compiled_prompt"] = {
        "text": prompt,
        "sha256": sha256_text(prompt),
        "frozen": True,
        "profile": prompt_profile,
    }
    next_shot = {
        "id": next_shot_id,
        "beat": beat,
        "status": "compiled",
        "planned": deepcopy(state),
        "grammar": deepcopy(grammar),
        "execution_sequence": deepcopy(sequence),
        "continuity_locks": deepcopy(contract["continuity_locks"]),
        "reference_shot_id": source_shot_id,
        "artifacts": {},
        "prompt": deepcopy(contract["compiled_prompt"]),
        "observed": None,
        "evaluation": None,
        "contract": {
            "version": contract_version,
            "continuity_safe": True,
            "source_video_sha256": video["sha256"],
            "source_final_frame_sha256": final_frame["sha256"],
            "ordered_sequence_sha256": sequence_sha256,
            "prompt_profile": prompt_profile,
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
