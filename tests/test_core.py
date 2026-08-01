from __future__ import annotations

import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from shotflow.core import (
    ShotFlowError,
    add_or_replace_plan,
    apply_score,
    compile_next_shot,
    diff_states,
    new_project,
    observe_shot,
    render_prompt,
    score_evaluation,
    validate_ordered_sequence,
    validate_project,
    write_json,
)


MP4_BYTES = b"\x00\x00\x00\x18ftypisom\x00\x00\x00\x00"
PNG_BYTES = b"\x89PNG\r\n\x1a\nshotflow"


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

SEQUENCE = {
    "sequence_version": "1.0",
    "duration_seconds": 5,
    "anchors": {
        "identity": "One worker in the observed torn red cape remains visible.",
        "wardrobe_props": "The repair tool remains in the left hand and the cable stays taut.",
        "space_direction": "The worker remains right of the fissure on the accepted camera side.",
        "light_material": "Cold storm light and amber seam light remain on wet metal.",
    },
    "checkpoints": [
        {
            "phase": "match",
            "start_seconds": 0,
            "end_seconds": 0.5,
            "state": "The opening frame matches the accepted suspended pose and taut cable.",
            "visual_test": "Cape, cable, tool hand, fissure side, and horizon match the endpoint.",
        },
        {
            "phase": "continue",
            "start_seconds": 0.5,
            "end_seconds": 1.5,
            "state": "The existing swing carries the worker toward the fissure as cable tension increases.",
            "visual_test": "Body direction follows the incoming arc and the cable remains visibly taut.",
        },
        {
            "phase": "initiate",
            "start_seconds": 1.5,
            "end_seconds": 2.5,
            "state": "The worker regains tower contact and places the amber repair tool on the fissure.",
            "visual_test": "Hand, tool, and fissure share one clear contact point.",
        },
        {
            "phase": "resolve",
            "start_seconds": 2.5,
            "end_seconds": 4.25,
            "state": "Amber repair light closes the fissure from the contact point across the visible seam.",
            "visual_test": "The open seam visibly becomes one continuous repaired metal edge.",
        },
        {
            "phase": "hold",
            "start_seconds": 4.25,
            "end_seconds": 5,
            "state": "The worker holds beside the sealed seam as restrained dawn light appears behind it.",
            "visual_test": "The final frame shows contact, a sealed seam, stable cable tension, and dawn proof.",
        },
    ],
}

CAUSAL_SEQUENCE = {
    "sequence_version": "1.1",
    "duration_seconds": 5,
    "anchors": {
        "identity": "One worker in the torn red cape remains visible.",
        "wardrobe_props": "The repair tool remains in the left hand.",
        "space_direction": "The worker remains right of the fissure.",
        "light_material": "Cold storm light remains on wet metal.",
    },
    "change_budget": {
        "protected": [
            {"id": "worker-identity", "state": "The same worker and torn red cape remain visible."},
            {"id": "camera-side", "state": "The camera side and fixed horizon remain stable."},
        ],
        "transitions": [
            {
                "id": "swing-settle",
                "subject": "the worker and cable",
                "from_state": "the body swings right on a taut cable",
                "transition": "the swing reaches the fissure and slows",
                "to_state": "the worker holds beside the fissure",
                "proof": "the cable stays taut while the body reaches the tower",
            },
            {
                "id": "seam-repair",
                "subject": "the visible fissure",
                "from_state": "the amber seam remains open",
                "transition": "repair light travels from the tool contact point",
                "to_state": "one continuous repaired edge remains",
                "proof": "the final frame shows a closed metal edge",
            },
        ],
    },
    "checkpoints": [
        {
            "phase": "match",
            "start_seconds": 0,
            "end_seconds": 0.5,
            "state": "The opening matches the suspended worker and taut cable.",
            "visual_test": "Worker, cable, tool hand, fissure side, and horizon match.",
            "active_changes": [],
        },
        {
            "phase": "continue",
            "start_seconds": 0.5,
            "end_seconds": 1.5,
            "state": "The existing swing carries the worker toward the fissure.",
            "visual_test": "The incoming arc and cable tension remain readable.",
            "active_changes": ["swing-settle"],
        },
        {
            "phase": "initiate",
            "start_seconds": 1.5,
            "end_seconds": 2.5,
            "state": "The repair tool touches the fissure at one clear point.",
            "visual_test": "Hand, tool, and fissure share one contact point.",
            "active_changes": ["seam-repair"],
        },
        {
            "phase": "resolve",
            "start_seconds": 2.5,
            "end_seconds": 4.25,
            "state": "Amber repair light closes the visible seam from the contact point.",
            "visual_test": "The open seam becomes one repaired metal edge.",
            "active_changes": ["seam-repair"],
        },
        {
            "phase": "hold",
            "start_seconds": 4.25,
            "end_seconds": 5,
            "state": "The worker holds beside the sealed seam and taut cable.",
            "visual_test": "The final frame proves the sealed seam and stable worker.",
            "active_changes": [],
        },
    ],
}


class CoreTests(unittest.TestCase):
    def test_new_project_marks_only_verified_model(self) -> None:
        standard = new_project("Standard")
        verified = new_project("Verified", model="seedance2.0_vision")
        unverified = new_project("Other", model="unverified-model")
        self.assertEqual(standard["provider"]["model"], "seedance2.0_direct")
        self.assertEqual(standard["provider"]["parameters"]["resolution"], "720p")
        self.assertFalse(standard["provider"]["verified"])
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
            compile_next_shot(
                project, "clip-01", "clip-02", "Continue", GRAMMAR, SEQUENCE
            )

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
            frame.write_bytes(PNG_BYTES)
            with self.assertRaisesRegex(ShotFlowError, "inside the project"):
                observe_shot(
                    project_file,
                    project,
                    "clip-01",
                    OBSERVED,
                    external,
                    frame,
                )

    def test_artifacts_reject_unrecognized_media_signatures(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            project_file = root / "shotflow.project.json"
            project = new_project("Signature gate")
            add_or_replace_plan(project, "clip-01", "Begin", PLAN)
            video = root / "clip-01.mp4"
            frame = root / "clip-01-final.png"
            video.write_bytes(b"not a video")
            frame.write_bytes(PNG_BYTES)
            with self.assertRaisesRegex(ShotFlowError, "Video artifact"):
                observe_shot(
                    project_file, project, "clip-01", OBSERVED, video, frame
                )

            video.write_bytes(MP4_BYTES)
            frame.write_bytes(b"not an image")
            with self.assertRaisesRegex(ShotFlowError, "Final-frame artifact"):
                observe_shot(
                    project_file, project, "clip-01", OBSERVED, video, frame
                )

    def test_full_state_flow_uses_observed_state(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            project_file = root / "shotflow.project.json"
            project = new_project("Sky Mender")
            add_or_replace_plan(project, "clip-01", "Begin repair", PLAN)
            media = root / "clip-01.mp4"
            frame = root / "clip-01-final.png"
            media.write_bytes(MP4_BYTES + b"accepted")
            frame.write_bytes(PNG_BYTES + b"accepted")
            observe_shot(project_file, project, "clip-01", OBSERVED, media, frame)
            contract = compile_next_shot(
                project,
                "clip-01",
                "clip-02-shotflow",
                "Seal the widening fissure",
                GRAMMAR,
                SEQUENCE,
            )
            self.assertTrue(contract["continuity_safe"])
            self.assertEqual(contract["observed_state"], OBSERVED)
            self.assertIn("left hand", contract["compiled_prompt"]["text"])
            self.assertEqual(
                contract["compiled_prompt"]["profile"], "provider-direct-v3"
            )
            prompt = contract["compiled_prompt"]["text"]
            self.assertTrue(
                prompt.startswith("CONTINUE FROM THE ACCEPTED FINAL FRAME.")
            )
            self.assertLess(
                prompt.index("Seal the widening fissure"),
                prompt.index("left hand"),
            )
            self.assertIn(
                "Five visible checkpoints", prompt
            )
            self.assertIn("narrative rhythm", prompt)
            self.assertEqual(prompt.count(" | "), 5)
            self.assertNotIn("Opening continuity locks", prompt)
            self.assertNotIn("Hard rule", prompt)
            self.assertNotIn("Do not", prompt)
            self.assertEqual(contract["ordered_sequence"], SEQUENCE)
            self.assertEqual(
                project["shots"][-1]["execution_sequence"], SEQUENCE
            )

            shotflow_media = root / "clip-02.mp4"
            shotflow_frame = root / "clip-02-final.png"
            shotflow_media.write_bytes(MP4_BYTES + b"shotflow result")
            shotflow_frame.write_bytes(PNG_BYTES + b"shotflow frame")
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

    def test_ordered_sequence_rejects_negative_directive(self) -> None:
        sequence = deepcopy(SEQUENCE)
        sequence["checkpoints"][2]["state"] = "Do not move the camera."
        with self.assertRaisesRegex(ShotFlowError, "visible positive state"):
            validate_ordered_sequence(sequence, 5)

    def test_ordered_sequence_rejects_gap_and_wrong_phase(self) -> None:
        gap = deepcopy(SEQUENCE)
        gap["checkpoints"][1]["start_seconds"] = 0.75
        with self.assertRaisesRegex(ShotFlowError, "previous checkpoint ends"):
            validate_ordered_sequence(gap, 5)

        phase = deepcopy(SEQUENCE)
        phase["checkpoints"][3]["phase"] = "hold"
        with self.assertRaisesRegex(ShotFlowError, "phase must be 'resolve'"):
            validate_ordered_sequence(phase, 5)

    def test_ordered_sequence_rejects_count_and_duration_mismatch(self) -> None:
        count = deepcopy(SEQUENCE)
        count["checkpoints"].pop()
        with self.assertRaisesRegex(ShotFlowError, "exactly five"):
            validate_ordered_sequence(count, 5)

        duration = deepcopy(SEQUENCE)
        duration["duration_seconds"] = 8
        with self.assertRaisesRegex(ShotFlowError, "provider duration"):
            validate_ordered_sequence(duration, 5)

    def test_causal_sequence_compiles_change_budget_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            project_file = root / "shotflow.project.json"
            project = new_project("Causal compiler")
            add_or_replace_plan(project, "clip-01", "Begin repair", PLAN)
            media = root / "clip-01.mp4"
            frame = root / "clip-01-final.png"
            media.write_bytes(MP4_BYTES + b"accepted")
            frame.write_bytes(PNG_BYTES + b"accepted")
            observe_shot(project_file, project, "clip-01", OBSERVED, media, frame)
            contract = compile_next_shot(
                project,
                "clip-01",
                "clip-02-v4",
                "The worker seals the fissure and holds beside it.",
                GRAMMAR,
                CAUSAL_SEQUENCE,
            )
        prompt = contract["compiled_prompt"]["text"]
        self.assertEqual(contract["contract_version"], "1.2")
        self.assertEqual(contract["compiled_prompt"]["profile"], "provider-direct-v4")
        self.assertIn("PROTECTED THROUGHOUT", prompt)
        self.assertIn("AUTHORIZED CHANGES IN ORDER", prompt)
        self.assertIn("FINAL PROOF", prompt)
        self.assertLessEqual(len(prompt), 1800)
        self.assertNotRegex(prompt, r"(?i)do not|must not|without|avoid|hard rule")

    def test_causal_sequence_rejects_change_budget_conflicts(self) -> None:
        duplicate = deepcopy(CAUSAL_SEQUENCE)
        duplicate["change_budget"]["transitions"][0]["id"] = "worker-identity"
        with self.assertRaisesRegex(ShotFlowError, "Duplicate change budget id"):
            validate_ordered_sequence(duplicate, 5)

        unknown = deepcopy(CAUSAL_SEQUENCE)
        unknown["checkpoints"][1]["active_changes"] = ["unknown-change"]
        with self.assertRaisesRegex(ShotFlowError, "unknown transitions"):
            validate_ordered_sequence(unknown, 5)

        unused = deepcopy(CAUSAL_SEQUENCE)
        for checkpoint in unused["checkpoints"]:
            checkpoint["active_changes"] = []
        with self.assertRaisesRegex(ShotFlowError, "unused transitions"):
            validate_ordered_sequence(unused, 5)

    def test_causal_sequence_rejects_invalid_active_and_negative_text(self) -> None:
        match_change = deepcopy(CAUSAL_SEQUENCE)
        match_change["checkpoints"][0]["active_changes"] = ["swing-settle"]
        with self.assertRaisesRegex(ShotFlowError, "cannot have active changes"):
            validate_ordered_sequence(match_change, 5)

        negative = deepcopy(CAUSAL_SEQUENCE)
        negative["change_budget"]["protected"][0]["state"] = "Do not change the worker."
        with self.assertRaisesRegex(ShotFlowError, "visible positive state"):
            validate_ordered_sequence(negative, 5)

    def test_causal_provider_prompt_rejects_over_1800_characters(self) -> None:
        overlong = deepcopy(CAUSAL_SEQUENCE)
        for checkpoint in overlong["checkpoints"]:
            checkpoint["state"] = "Visible continuous state " + ("x" * 320)
        validate_ordered_sequence(overlong, 5)
        with self.assertRaisesRegex(ShotFlowError, "exceeds 1800"):
            render_prompt("The repair completes visibly.", GRAMMAR, overlong)

    def test_obsidian_v3_regression_compiles_short_ordered_prompt(self) -> None:
        repository = Path(__file__).resolve().parents[1]
        case = repository / "examples" / "obsidian-bloom"
        project = json.loads(
            (case / "shotflow.project.json").read_text(encoding="utf-8")
        )
        grammar = json.loads(
            (case / "plan" / "clip-02-grammar-v3.json").read_text(
                encoding="utf-8"
            )
        )
        sequence = json.loads(
            (case / "plan" / "clip-02-sequence-v3.json").read_text(
                encoding="utf-8"
            )
        )
        contract = compile_next_shot(
            project,
            "clip-01",
            "clip-02-shotflow-v3-offline",
            "The level cap rises, exposes the neck, and releases one thin amber orbit.",
            grammar,
            sequence,
        )
        prompt = contract["compiled_prompt"]["text"]
        legacy = (case / "prompts" / "clip-02-shotflow-v2.txt").read_text(
            encoding="utf-8"
        )
        frozen = (
            case / "prompts" / "clip-02-shotflow-v3-offline.txt"
        ).read_text(encoding="utf-8")
        self.assertEqual(contract["contract_version"], "1.1")
        self.assertEqual(contract["compiled_prompt"]["profile"], "provider-direct-v3")
        self.assertEqual(len(contract["ordered_sequence"]["checkpoints"]), 5)
        self.assertTrue(
            all(
                checkpoint["visual_test"]
                for checkpoint in contract["ordered_sequence"]["checkpoints"]
            )
        )
        self.assertLess(len(prompt), len(legacy) * 0.8)
        self.assertEqual(prompt, frozen)
        self.assertIn("begins at the exposed neck", prompt)
        self.assertIn("attached droplet remains visible", prompt)
        self.assertNotRegex(prompt, r"(?i)do not|must not|without|avoid|hard rule")

    def test_v4_rc1_examples_match_frozen_compiler_output(self) -> None:
        repository = Path(__file__).resolve().parents[1]
        for case_id in ("obsidian-bloom", "sky-mender"):
            with self.subTest(case=case_id):
                case = repository / "examples" / case_id
                project = json.loads(
                    (case / "shotflow.project.json").read_text(encoding="utf-8")
                )
                grammar = json.loads(
                    (case / "plan" / "clip-02-grammar-v4.json").read_text(
                        encoding="utf-8"
                    )
                )
                sequence = json.loads(
                    (case / "plan" / "clip-02-sequence-v4.json").read_text(
                        encoding="utf-8"
                    )
                )
                contract = compile_next_shot(
                    project,
                    "clip-01",
                    "clip-02-v4-rc1-regression",
                    "The registered story outcome completes and holds visibly.",
                    grammar,
                    sequence,
                )
                frozen = (
                    case / "prompts" / "clip-02-shotflow-v4-rc1.txt"
                ).read_text(encoding="utf-8")
                self.assertEqual(contract["contract_version"], "1.2")
                self.assertEqual(
                    contract["compiled_prompt"]["profile"], "provider-direct-v4"
                )
                self.assertEqual(contract["compiled_prompt"]["text"], frozen)
                self.assertLessEqual(len(frozen), 1800)


if __name__ == "__main__":
    unittest.main()
