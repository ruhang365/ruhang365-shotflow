from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from shotflow.core import (
    ShotFlowError,
    add_or_replace_plan,
    apply_score,
    compile_next_shot,
    diff_states,
    new_project,
    observe_shot,
    score_evaluation,
    validate_project,
    write_json,
)


GRAMMAR = {
    "narrative_moment": "The cable catches before the fall.",
    "camera_movement": "Track laterally with a fixed horizon.",
    "light_color": "Cold sky camera-left, amber repair seam.",
    "space_composition": "Subject moves screen-right beside the fissure.",
    "material_physics": "Wet cloth drags downwind before the cable tightens.",
}

PLAN = {
    "grammar": GRAMMAR,
    "planned": {
        "identity": "worker in a red cape",
        "wardrobe_props": "repair tool in right hand",
        "space_direction": "moving screen-right",
        "motion": "reaching for the fissure",
        "light_material": "cold storm light on wet metal",
        "story_beat": "the repair begins",
    },
}

OBSERVED = {
    "identity": "worker in a torn red cape",
    "wardrobe_props": "repair tool in left hand",
    "space_direction": "hanging right of the fissure, facing screen-right",
    "motion": "swinging right with a taut cable",
    "light_material": "cold sky camera-left, amber seam on wet metal",
    "story_beat": "the repair cable catches but the fissure widens",
}

PERFECT_SCORE = {
    "subject_identity": 2,
    "wardrobe_props": 2,
    "space_direction": 2,
    "motion_handoff": 2,
    "light_material": 2,
    "story_beat": 2,
}


class CoreTests(unittest.TestCase):
    def test_new_project_marks_only_verified_model(self) -> None:
        verified = new_project("Verified")
        unverified = new_project("Other", model="unverified-model")
        self.assertTrue(verified["provider"]["verified"])
        self.assertFalse(unverified["provider"]["verified"])

    def test_project_rejects_false_verified_claim(self) -> None:
        project = new_project("Other", model="unverified-model")
        project["provider"]["verified"] = True
        with self.assertRaisesRegex(ShotFlowError, "forward-tested"):
            validate_project(project)

    def test_diff_preserves_planned_and_observed_values(self) -> None:
        changes = diff_states(
            {"prop": {"hand": "right"}, "planned_only": True},
            {"prop": {"hand": "left"}, "observed_only": True},
        )
        by_path = {change["path"]: change for change in changes}
        self.assertEqual(by_path["prop.hand"]["kind"], "changed")
        self.assertEqual(by_path["prop.hand"]["observed"], "left")
        self.assertEqual(by_path["planned_only"]["kind"], "not_observed")
        self.assertEqual(by_path["observed_only"]["kind"], "observed_only")

    def test_score_excludes_not_applicable(self) -> None:
        evaluation = dict(PERFECT_SCORE)
        evaluation["wardrobe_props"] = "n/a"
        result = score_evaluation(evaluation)
        self.assertEqual(result["score"], 100)
        self.assertEqual(result["applicable_dimensions"], 5)

    def test_score_rejects_all_not_applicable(self) -> None:
        with self.assertRaisesRegex(ShotFlowError, "At least one"):
            score_evaluation({key: "n/a" for key in PERFECT_SCORE})

    def test_compile_requires_observation(self) -> None:
        project = new_project("No observation")
        add_or_replace_plan(project, "clip-01", "Begin", PLAN)
        with self.assertRaisesRegex(ShotFlowError, "accepted observation"):
            compile_next_shot(project, "clip-01", "clip-02", "Continue", GRAMMAR)

    def test_artifacts_must_stay_inside_project(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            project_file = root / "project" / "shotflow.project.json"
            project_file.parent.mkdir()
            project = new_project("Safe paths")
            write_json(project_file, project)
            add_or_replace_plan(project, "clip-01", "Begin", PLAN)
            external = root / "outside.mp4"
            external.write_bytes(b"video")
            frame = project_file.parent / "frame.png"
            frame.write_bytes(b"frame")
            with self.assertRaisesRegex(ShotFlowError, "inside the project"):
                observe_shot(
                    project_file,
                    project,
                    "clip-01",
                    OBSERVED,
                    external,
                    frame,
                )

    def test_full_state_flow_uses_observed_state(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            project_file = root / "shotflow.project.json"
            project = new_project("Sky Mender")
            add_or_replace_plan(project, "clip-01", "Begin repair", PLAN)
            media = root / "clip-01.mp4"
            frame = root / "clip-01-final.png"
            media.write_bytes(b"accepted video")
            frame.write_bytes(b"accepted frame")
            observe_shot(project_file, project, "clip-01", OBSERVED, media, frame)
            contract = compile_next_shot(
                project,
                "clip-01",
                "clip-02-shotflow",
                "Seal the widening fissure",
                GRAMMAR,
            )
            self.assertTrue(contract["continuity_safe"])
            self.assertEqual(contract["observed_state"], OBSERVED)
            self.assertIn("repair tool in left hand", contract["compiled_prompt"]["text"])

            shotflow_media = root / "clip-02.mp4"
            shotflow_frame = root / "clip-02-final.png"
            shotflow_media.write_bytes(b"shotflow result")
            shotflow_frame.write_bytes(b"shotflow frame")
            observe_shot(
                project_file,
                project,
                "clip-02-shotflow",
                OBSERVED,
                shotflow_media,
                shotflow_frame,
            )
            result = apply_score(project, "clip-02-shotflow", PERFECT_SCORE)
            self.assertEqual(result["score"], 100)

            with self.assertRaisesRegex(ShotFlowError, "cannot be replanned"):
                add_or_replace_plan(project, "clip-02-shotflow", "Replace", PLAN)

            with self.assertRaisesRegex(ShotFlowError, "accepted observation"):
                observe_shot(
                    project_file,
                    project,
                    "clip-02-shotflow",
                    OBSERVED,
                    shotflow_media,
                    shotflow_frame,
                )

    def test_score_rejects_unobserved_shot(self) -> None:
        project = new_project("No media")
        add_or_replace_plan(project, "clip-01", "Begin", PLAN)
        with self.assertRaisesRegex(ShotFlowError, "accepted observed video"):
            apply_score(project, "clip-01", PERFECT_SCORE)


if __name__ == "__main__":
    unittest.main()
