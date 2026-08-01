"""Account-free bundled ShotFlow demonstration."""

from __future__ import annotations

import base64
from pathlib import Path
from typing import Any

from .core import (
    ShotFlowError,
    add_or_replace_plan,
    compile_next_shot,
    new_project,
    observe_shot,
    save_project,
    shot_diff,
    write_json,
)


DEMO_MP4 = "AAAAIGZ0eXBpc29tAAACAGlzb21pc28yYXZjMW1wNDEAAAMVbW9vdgAAAGxtdmhkAAAAAAAAAAAAAAAAAAAD6AAAAGQAAQAAAQAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAj90cmFrAAAAXHRraGQAAAADAAAAAAAAAAAAAAABAAAAAAAAAGQAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAABAAAAAABAAAAAQAAAAAAAkZWR0cwAAABxlbHN0AAAAAAAAAAEAAABkAAAAAAABAAAAAAG3bWRpYQAAACBtZGhkAAAAAAAAAAAAAAAAAAAoAAAABABVxAAAAAAALWhkbHIAAAAAAAAAAHZpZGUAAAAAAAAAAAAAAABWaWRlb0hhbmRsZXIAAAABYm1pbmYAAAAUdm1oZAAAAAEAAAAAAAAAAAAAACRkaW5mAAAAHGRyZWYAAAAAAAAAAQAAAAx1cmwgAAAAAQAAASJzdGJsAAAAvnN0c2QAAAAAAAAAAQAAAK5hdmMxAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAABAAEABIAAAASAAAAAAAAAABFUxhdmM2Mi4yOC4xMDAgbGlieDI2NAAAAAAAAAAAAAAAGP//AAAANGF2Y0MBZAAK/+EAF2dkAAqs2V7ARAAAAwAEAAADAFA8SJZYAQAGaOvjyyLA/fj4AAAAABBwYXNwAAAAAQAAAAEAAAAUYnJ0AAAAAAAAN7QAAAAAAAAABhzdHRzAAAAAAAAAAEAAAABAAAEAAAAABxzdHNjAAAAAAAAAAEAAAABAAAAAQAAAAEAAAAUc3RzegAAAAAAAALJAAAAAQAAABRzdGNvAAAAAAAAAAEAAANFAAAAYnVkdGEAAABabWV0YQAAAAAAAAAhaGRscgAAAAAAAAAAbWRpcmFwcGwAAAAAAAAAAAAAAAAtaWxzdAAAACWpdG9vAAAAHWRhdGEAAAABAAAAAExhdmY2Mi4xMi4xMDAAAAAIZnJlZQAAAtFtZGF0AAACrgYF//+q3EXpvebZSLeWLNgg2SPu73gyNjQgLSBjb3JlIDE2NSByMzIyMiBiMzU2MDVhIC0gSC4yNjQvTVBFRy00IEFWQyBjb2RlYyAtIENvcHlsZWZ0IDIwMDMtMjAyNSAtIGh0dHA6Ly93d3cudmlkZW9sYW4ub3JnL3gyNjQuaHRtbCAtIG9wdGlvbnM6IGNhYmFjPTEgcmVmPTMgZGVibG9jaz0xOjA6MCBhbmFseXNlPTB4MzoweDExMyBtZT1oZXggc3VibWU9NyBwc3k9MSBwc3lfcmQ9MS4wMDowLjAwIG1peGVkX3JlZj0xIG1lX3JhbmdlPTE2IGNocm9tYV9tZT0xIHRyZWxsaXM9MSA4eDhkY3Q9MSBjcW09MCBkZWFkem9uZT0yMSwxMSBmYXN0X3Bza2lwPTEgY2hyb21hX3FwX29mZnNldD0tMiB0aHJlYWRzPTEgbG9va2FoZWFkX3RocmVhZHM9MSBzbGljZWRfdGhyZWFkcz0wIG5yPTAgZGVjaW1hdGU9MSBpbnRlcmxhY2VkPTAgYmx1cmF5X2NvbXBhdD0wIGNvbnN0cmFpbmVkX2ludHJhPTAgYmZyYW1lcz0zIGJfcHlyYW1pZD0yIGJfYWRhcHQ9MSBiX2JpYXM9MCBkaXJlY3Q9MSB3ZWlnaHRiPTEgb3Blbl9nb3A9MCB3ZWlnaHRwPTIga2V5aW50PTI1MCBrZXlpbnRfbWluPTEwIHNjZW5lY3V0PTQwIGludHJhX3JlZnJlc2g9MCByY19sb29rYWhlYWQ9NDAgcmM9Y3JmIG1idHJlZT0xIGNyZj0yMy4wIHFjb21wPTAuNjAgcXBtaW49MCBxcG1heD02OSBxcHN0ZXA9NCBpcF9yYXRpbz0xLjQwIGFxPTE6MS4wMACAAAAAE2WIhAA3//7hA/gU1tC+XvVfQUE="
DEMO_PNG = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAACXBIWXMAAAABAAAAAQBPJcTWAAAAGUlEQVR4nGOUUjVhIAWwkKR6VMOohiGlAQDBPwCxn7CwuAAAAABJRU5ErkJggg=="


GRAMMAR = {
    "narrative_moment": "One restrained product action completes and holds.",
    "camera_movement": "The camera remains locked at the observed endpoint.",
    "light_color": "Cool left light and amber underlight remain stable.",
    "space_composition": "The bottle stays centered above the low horizon.",
    "material_physics": "The rigid cap rises vertically while glass and liquid stay settled.",
}

PLANNED = {
    "identity": "one dark glass bottle",
    "wardrobe_props": "black cap and silver collar",
    "space_direction": "centered front view",
    "motion": "the cap remains closed",
    "light_material": "cool studio light on dark glass",
    "story_beat": "the product remains still",
}

OBSERVED = {
    "identity": "one squat smoky-glass bottle with broad shoulders",
    "wardrobe_props": "level black cap, asymmetric silver collar, and attached upper-left amber droplet",
    "space_direction": "near-frontal centered bottle above a low liquid horizon",
    "motion": "the bottle and liquid plane have settled",
    "light_material": "cool left reflection and amber underlight on glass and metal",
    "story_beat": "the product holds before the cap release",
}

SEQUENCE = {
    "sequence_version": "1.2",
    "duration_seconds": 5,
    "anchors": {
        "identity": "One squat smoky-glass bottle keeps its broad shoulders.",
        "wardrobe_props": "The black cap, silver collar, and attached droplet retain their geometry.",
        "space_direction": "The near-frontal bottle stays centered above the low horizon.",
        "light_material": "Cool left light and amber underlight preserve the accepted materials.",
    },
    "change_budget": {
        "protected": [
            {"id": "bottle-body", "state": "The bottle body, collar, and attached droplet remain stable."},
            {"id": "studio-state", "state": "The locked camera, low horizon, reflections, and underlight remain stable."},
        ],
        "transitions": [
            {
                "id": "cap-lift",
                "subject": "the level black cap",
                "from_state": "the cap rests on the silver neck",
                "transition": "the rigid cap rises straight upward by one centimeter",
                "to_state": "the level cap holds one centimeter above the exposed neck",
                "proof": "a clear vertical gap remains beneath the level unchanged cap",
            }
        ],
    },
    "checkpoints": [
        {"phase": "match", "start_seconds": 0, "end_seconds": 0.5, "state": "The opening matches the accepted bottle, cap, collar, droplet, camera, and light.", "visual_test": "Silhouette, geometry, horizon, and reflections match.", "active_changes": []},
        {"phase": "continue", "start_seconds": 0.5, "end_seconds": 1.25, "state": "The complete accepted product state remains settled.", "visual_test": "All protected facts remain visible.", "active_changes": []},
        {"phase": "initiate", "start_seconds": 1.25, "end_seconds": 2.5, "state": "The rigid level cap rises straight upward.", "visual_test": "A vertical gap opens above the silver neck.", "active_changes": ["cap-lift"]},
        {"phase": "resolve", "start_seconds": 2.5, "end_seconds": 4.25, "state": "The cap reaches one centimeter above the exposed neck.", "visual_test": "The cap stays level and the bottle remains fixed.", "active_changes": ["cap-lift"]},
        {"phase": "hold", "start_seconds": 4.25, "end_seconds": 5, "state": "The level cap holds above the exposed neck while the product state remains stable.", "visual_test": "The final frame proves the cap gap and every protected fact.", "active_changes": []},
    ],
}


def create_demo(directory: Path) -> dict[str, Any]:
    directory = directory.expanduser().resolve()
    if directory.exists() and any(directory.iterdir()):
        raise ShotFlowError(f"Demo directory is not empty: {directory}")
    directory.mkdir(parents=True, exist_ok=True)
    artifacts = directory / "artifacts"
    prompts = directory / "prompts"
    artifacts.mkdir()
    prompts.mkdir()
    project_file = directory / "shotflow.project.json"
    project = new_project("ShotFlow Offline Demo")
    add_or_replace_plan(
        project,
        "clip-01",
        "The product settles before its cap release.",
        {"planned": PLANNED, "grammar": GRAMMAR},
        "A product bottle settles before the cap rises.\n",
    )
    source_video = artifacts / "clip-01-fixture.mp4"
    source_frame = artifacts / "clip-01-final-fixture.png"
    source_video.write_bytes(base64.b64decode(DEMO_MP4 + "="))
    source_frame.write_bytes(base64.b64decode(DEMO_PNG))
    observe_shot(project_file, project, "clip-01", OBSERVED, source_video, source_frame)
    diff = shot_diff(project, "clip-01")
    contract = compile_next_shot(
        project,
        "clip-01",
        "clip-02-shotflow",
        "The level cap rises vertically and holds above the exposed neck.",
        GRAMMAR,
        SEQUENCE,
    )
    save_project(project_file, project)
    write_json(directory / "clip-01-diff.json", diff)
    write_json(directory / "clip-02-contract.json", contract)
    prompt_path = prompts / "clip-02-shotflow.txt"
    prompt_path.write_text(contract["compiled_prompt"]["text"], encoding="utf-8")
    return {
        "project_file": str(project_file),
        "diff_file": str(directory / "clip-01-diff.json"),
        "contract_file": str(directory / "clip-02-contract.json"),
        "prompt_file": str(prompt_path),
        "contract_version": contract["contract_version"],
        "prompt_profile": contract["compiled_prompt"]["profile"],
        "continuity_safe": contract["continuity_safe"],
        "generation_submitted": False,
    }
