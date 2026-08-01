from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from shotflow.core import (
    GRAMMAR_AXES,
    REQUIRED_OBSERVED_STATE,
    ShotFlowError,
    add_or_replace_plan,
    new_project,
    observe_shot,
    write_json,
)
from shotflow.handoff import (
    ANCHOR_FRAME_PROFILE,
    ANCHOR_FRAME_V2_PROFILE,
    prepare_provider_handoff,
    select_single_new_output,
)


MP4_BYTES = b"\x00\x00\x00\x18ftypisom\x00\x00\x00\x00"
PNG_BYTES = b"\x89PNG\r\n\x1a\nshotflow"


class HandoffTests(unittest.TestCase):
    def create_project(self, temporary: str, *, observed: bool = True) -> tuple[Path, Path]:
        root = Path(temporary) / "case"
        root.mkdir()
        project_file = root / "shotflow.project.json"
        project = new_project("Case")
        specification = {
            "planned": {"story_beat": "Continue the action."},
            "grammar": {axis: f"{axis} decision" for axis in GRAMMAR_AXES},
        }
        add_or_replace_plan(project, "clip-01", "Open motion", specification)
        video = root / "clip-01.mp4"
        frame = root / "clip-01-final.png"
        video.write_bytes(MP4_BYTES + b"source-video")
        frame.write_bytes(PNG_BYTES + b"source-frame")
        if observed:
            state = {key: f"observed {key}" for key in REQUIRED_OBSERVED_STATE}
            observe_shot(project_file, project, "clip-01", state, video, frame)
        write_json(project_file, project)
        prompt = root / "clip-02.txt"
        prompt.write_text("Continue the rescue.\n", encoding="utf-8")
        return project_file, prompt

    def test_handoff_puts_observed_final_frame_first(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project, prompt = self.create_project(temporary)
            old = project.parent / "old.mp4"
            old.write_bytes(MP4_BYTES + b"old-output")
            manifest = prepare_provider_handoff(
                project,
                source_shot_id="clip-01",
                variant="clip-02-baseline",
                creative_prompt_path=prompt,
                platform="Lovart",
                model_tool="generate_video_seedance_v2_0",
                known_output_paths=[old],
            )
            self.assertEqual(
                manifest["references"][0]["role"],
                "authoritative_opening_frame",
            )
            self.assertEqual(manifest["profile"], "video-context-v1")
            self.assertEqual(manifest["references"][0]["attachment_index"], 1)
            self.assertEqual(manifest["references"][1]["role"], "motion_context_video")
            self.assertIn("Attachment 1 is the authoritative", manifest["submission_prompt"]["text"])
            self.assertEqual(len(manifest["known_output_sha256"]), 1)
            self.assertFalse(manifest["acceptance_gates"]["continuity_safe"])

            rejected = prepare_provider_handoff(
                project,
                source_shot_id="clip-01",
                variant="clip-02-baseline",
                creative_prompt_path=prompt,
                platform="Lovart",
                model_tool="generate_video_seedance_v2_0",
                opening_frame_review="rejected",
            )
            self.assertEqual(
                rejected["acceptance_gates"]["opening_frame_review"],
                "rejected",
            )

    def test_anchor_frame_profile_uses_only_observed_final_frame(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project, prompt = self.create_project(temporary)
            manifest = prepare_provider_handoff(
                project,
                source_shot_id="clip-01",
                variant="clip-02-shotflow",
                creative_prompt_path=prompt,
                platform="Lovart",
                model_tool="generate_video_seedance_v2_0",
                profile=ANCHOR_FRAME_PROFILE,
            )
            self.assertEqual(manifest["profile"], "anchor-frame-v1")
            self.assertEqual(len(manifest["references"]), 1)
            self.assertEqual(
                manifest["references"][0]["artifact"]["kind"],
                "final_frame",
            )
            self.assertIn(
                "No source video is attached",
                manifest["submission_prompt"]["text"],
            )

    def test_anchor_frame_v2_uses_positive_opening_authority(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project, prompt = self.create_project(temporary)
            manifest = prepare_provider_handoff(
                project,
                source_shot_id="clip-01",
                variant="clip-02-shotflow-v4",
                creative_prompt_path=prompt,
                platform="Lovart",
                model_tool="generate_video_seedance_v2_0",
                profile=ANCHOR_FRAME_V2_PROFILE,
            )
            submission = manifest["submission_prompt"]["text"]
            self.assertEqual(manifest["handoff_version"], "1.1")
            self.assertEqual(manifest["profile"], "anchor-frame-v2")
            self.assertEqual(len(manifest["references"]), 1)
            self.assertIn("Generated frame 1 reproduces", submission)
            self.assertNotRegex(
                submission,
                r"(?i)do not|must not|without|avoid|hard rule",
            )

    def test_v03_gate_handoffs_match_frozen_inputs(self) -> None:
        repository = Path(__file__).resolve().parents[1]
        cases = {
            "obsidian-bloom": ("gate7", "clip-02-baseline-v03-gate7"),
            "sky-mender": ("gate8", "clip-02-baseline-v03-gate8"),
        }
        for case_id, (gate, baseline_variant) in cases.items():
            root = repository / "examples" / case_id
            fixtures = (
                (
                    f"provider-handoff-baseline-v03-{gate}.json",
                    baseline_variant,
                    "clip-02-baseline-frozen.txt",
                ),
                (
                    f"provider-handoff-shotflow-v4-rc1-{gate}.json",
                    "clip-02-shotflow-v4-rc1",
                    "clip-02-shotflow-v4-rc1.txt",
                ),
            )
            for manifest_name, variant, prompt_name in fixtures:
                with self.subTest(case=case_id, variant=variant):
                    frozen = json.loads(
                        (root / "evidence" / manifest_name).read_text(
                            encoding="utf-8"
                        )
                    )
                    regenerated = prepare_provider_handoff(
                        root / "shotflow.project.json",
                        source_shot_id="clip-01",
                        variant=variant,
                        creative_prompt_path=root / "prompts" / prompt_name,
                        platform="Lovart",
                        model_tool="generate_video_seedance_v2_0",
                        profile=ANCHOR_FRAME_V2_PROFILE,
                    )
                    regenerated["known_output_sha256"] = frozen[
                        "known_output_sha256"
                    ]
                    self.assertEqual(regenerated, frozen)

    def test_handoff_rejects_unobserved_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project, prompt = self.create_project(temporary, observed=False)
            with self.assertRaisesRegex(ShotFlowError, "accepted observed"):
                prepare_provider_handoff(
                    project,
                    source_shot_id="clip-01",
                    variant="clip-02-baseline",
                    creative_prompt_path=prompt,
                    platform="Lovart",
                    model_tool="generate_video_seedance_v2_0",
                )

    def test_new_output_selection_excludes_history(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project, _ = self.create_project(temporary)
            old = project.parent / "old.mp4"
            new = project.parent / "new.mp4"
            old.write_bytes(MP4_BYTES + b"old-output")
            new.write_bytes(MP4_BYTES + b"new-output")
            manifest = prepare_provider_handoff(
                project,
                source_shot_id="clip-01",
                variant="clip-02-baseline",
                creative_prompt_path=project.parent / "clip-02.txt",
                platform="Lovart",
                model_tool="generate_video_seedance_v2_0",
                known_output_paths=[old],
            )
            selected = select_single_new_output(
                project,
                [old, new],
                manifest["known_output_sha256"],
            )
            self.assertEqual(selected["path"], "new.mp4")
            with self.assertRaisesRegex(ShotFlowError, "exactly one new"):
                select_single_new_output(project, [old], manifest["known_output_sha256"])


if __name__ == "__main__":
    unittest.main()
