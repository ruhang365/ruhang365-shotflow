"""ShotFlow command-line interface."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Sequence

from . import __version__
from .core import (
    ShotFlowError,
    add_or_replace_plan,
    apply_score,
    compile_next_shot,
    json_output,
    load_project,
    new_project,
    observe_shot,
    read_json,
    resolve_project_file,
    save_project,
    shot_diff,
    write_json,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="shotflow",
        description="Compile cinematic continuity from accepted AI video outcomes.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)

    init = commands.add_parser("init", help="Create a ShotFlow project")
    init.add_argument("directory")
    init.add_argument("--title", required=True)
    init.add_argument("--provider", default="seedance-2.0")
    init.add_argument("--model", default="seedance2.0_direct")
    init.add_argument("--ratio", default="16:9")
    init.add_argument("--resolution", default="720p")
    init.add_argument("--duration", type=int, default=5)

    plan = commands.add_parser("plan", help="Record a planned shot")
    plan.add_argument("--project", default=".")
    plan.add_argument("--shot-id", required=True)
    plan.add_argument("--beat", required=True)
    plan.add_argument("--spec", required=True)
    plan.add_argument("--prompt")

    observe = commands.add_parser("observe", help="Bind accepted media and observation")
    observe.add_argument("--project", default=".")
    observe.add_argument("--shot-id", required=True)
    observe.add_argument("--state", required=True)
    observe.add_argument("--media", required=True)
    observe.add_argument("--final-frame", required=True)

    diff = commands.add_parser("diff", help="Compare planned and observed shot state")
    diff.add_argument("--project", default=".")
    diff.add_argument("--shot-id", required=True)
    diff.add_argument("--output")

    compile_next = commands.add_parser(
        "compile-next", help="Compile the next shot from accepted observed state"
    )
    compile_next.add_argument("--project", default=".")
    compile_next.add_argument("--from-shot", required=True)
    compile_next.add_argument("--next-shot", required=True)
    compile_next.add_argument("--beat", required=True)
    compile_next.add_argument("--grammar", required=True)
    compile_next.add_argument("--contract-out")
    compile_next.add_argument("--prompt-out")

    score = commands.add_parser("score", help="Apply the continuity scoring rubric")
    score.add_argument("--project", default=".")
    score.add_argument("--shot-id", required=True)
    score.add_argument("--evaluation", required=True)
    score.add_argument("--output")

    return parser


def _read_text(path: str | None) -> str | None:
    if path is None:
        return None
    try:
        return Path(path).read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ShotFlowError(f"File not found: {path}") from exc


def _write_optional_json(path: str | None, value: dict[str, Any]) -> None:
    if path:
        write_json(Path(path), value)


def run(args: argparse.Namespace) -> dict[str, Any]:
    if args.command == "init":
        project_directory = Path(args.directory).expanduser().resolve()
        project_directory.mkdir(parents=True, exist_ok=True)
        project_file = project_directory / "shotflow.project.json"
        if project_file.exists():
            raise ShotFlowError(f"Project already exists: {project_file}")
        project = new_project(
            title=args.title,
            provider_adapter=args.provider,
            model=args.model,
            ratio=args.ratio,
            resolution=args.resolution,
            duration_seconds=args.duration,
        )
        (project_directory / "artifacts").mkdir(exist_ok=True)
        (project_directory / "prompts").mkdir(exist_ok=True)
        write_json(project_file, project)
        return {"project_file": str(project_file), "schema_version": "1.0"}

    project_file, project = load_project(args.project)

    if args.command == "plan":
        specification = read_json(Path(args.spec))
        shot = add_or_replace_plan(
            project,
            shot_id=args.shot_id,
            beat=args.beat,
            specification=specification,
            prompt_text=_read_text(args.prompt),
        )
        save_project(project_file, project)
        return {"shot": shot, "project_file": str(project_file)}

    if args.command == "observe":
        patch = observe_shot(
            project_file,
            project,
            shot_id=args.shot_id,
            state_or_patch=read_json(Path(args.state)),
            media_path=Path(args.media),
            final_frame_path=Path(args.final_frame),
        )
        save_project(project_file, project)
        return {"observation": patch, "project_file": str(project_file)}

    if args.command == "diff":
        result = shot_diff(project, args.shot_id)
        _write_optional_json(args.output, result)
        return result

    if args.command == "compile-next":
        grammar = read_json(Path(args.grammar))
        contract = compile_next_shot(
            project,
            source_shot_id=args.from_shot,
            next_shot_id=args.next_shot,
            beat=args.beat,
            grammar=grammar,
        )
        save_project(project_file, project)
        _write_optional_json(args.contract_out, contract)
        if args.prompt_out:
            prompt_path = Path(args.prompt_out)
            prompt_path.parent.mkdir(parents=True, exist_ok=True)
            prompt_path.write_text(contract["compiled_prompt"]["text"], encoding="utf-8")
        return contract

    if args.command == "score":
        result = apply_score(project, args.shot_id, read_json(Path(args.evaluation)))
        save_project(project_file, project)
        _write_optional_json(args.output, result)
        return result

    raise ShotFlowError(f"Unsupported command {args.command!r}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = run(args)
    except (ShotFlowError, ValueError) as exc:
        print(f"shotflow: error: {exc}", file=sys.stderr)
        return 2
    print(json_output(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
