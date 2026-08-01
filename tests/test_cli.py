from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
WRAPPER = REPOSITORY_ROOT / "skills" / "shotflow" / "scripts" / "shotflow.py"
MP4_BYTES = b"\x00\x00\x00\x18ftypisom\x00\x00\x00\x00"
PNG_BYTES = b"\x89PNG\r\n\x1a\nshotflow"

GRAMMAR = {
    "narrative_moment": "The action continues from the real endpoint.",
    "camera_movement": "Track laterally at subject speed.",
    "light_color": "Keep the accepted source direction.",
    "space_composition": "Preserve screen direction and landmarks.",
    "material_physics": "Preserve inertia, wetness, and contact.",
}

PLAN = {
    "grammar": GRAMMAR,
    "planned": {
        "identity": "worker",
        "wardrobe_props": "tool in right hand",
        "space_direction": "screen-right",
        "motion": "reaching",
        "light_material": "cold wet metal",
        "story_beat": "repair starts",
    },
}

OBSERVED = {
    "identity": "worker with torn red cape",
    "wardrobe_props": "tool in left hand",
    "space_direction": "screen-right beside fissure",
    "motion": "swinging on taut cable",
    "light_material": "cold wet metal with amber bounce",
    "story_beat": "cable catches as fissure widens",
}

EVALUATION = {
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
        "identity": "One worker with the torn red cape remains visible.",
        "wardrobe_props": "The repair tool remains in the left hand and the cable stays taut.",
        "space_direction": "The worker remains screen-right beside the fissure.",
        "light_material": "Cold wet metal keeps the accepted amber bounce.",
    },
    "checkpoints": [
        {"phase": "match", "start_seconds": 0, "end_seconds": 0.5, "state": "The opening matches the accepted suspended pose.", "visual_test": "Cape, cable, hand, fissure, and horizon match."},
        {"phase": "continue", "start_seconds": 0.5, "end_seconds": 1.5, "state": "The taut cable carries the worker along the incoming swing.", "visual_test": "The body follows the existing arc and cable tension stays visible."},
        {"phase": "initiate", "start_seconds": 1.5, "end_seconds": 2.5, "state": "The worker reaches tower contact and places the tool on the fissure.", "visual_test": "Hand, tool, and fissure form one readable contact point."},
        {"phase": "resolve", "start_seconds": 2.5, "end_seconds": 4.25, "state": "Amber repair light seals the fissure across the visible seam.", "visual_test": "The open seam becomes one continuous repaired edge."},
        {"phase": "hold", "start_seconds": 4.25, "end_seconds": 5, "state": "The worker holds beside the sealed seam in stable cable tension.", "visual_test": "The final frame clearly shows contact and a sealed seam."}
    ]
}


class CliTests(unittest.TestCase):
    def run_cli(
        self, *arguments: str, cwd: Path | None = None, expected: int = 0
    ) -> subprocess.CompletedProcess[str]:
        environment = dict(os.environ)
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        result = subprocess.run(
            [sys.executable, str(WRAPPER), *arguments],
            cwd=cwd or REPOSITORY_ROOT,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(
            result.returncode,
            expected,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        return result

    def test_complete_cli_workflow(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            project = root / "demo"
            self.run_cli("init", str(project), "--title", "Demo")
            initialized = json.loads(
                (project / "shotflow.project.json").read_text(encoding="utf-8")
            )
            self.assertEqual(
                initialized["provider"]["model"], "seedance2.0_direct"
            )
            self.assertEqual(
                initialized["provider"]["parameters"]["resolution"], "720p"
            )
            self.assertFalse(initialized["provider"]["verified"])

            plan_file = root / "plan.json"
            prompt_file = root / "baseline.md"
            plan_file.write_text(json.dumps(PLAN), encoding="utf-8")
            prompt_file.write_text("Frozen baseline prompt.\n", encoding="utf-8")
            self.run_cli(
                "plan",
                "--project",
                str(project),
                "--shot-id",
                "clip-01",
                "--beat",
                "Begin repair",
                "--spec",
                str(plan_file),
                "--prompt",
                str(prompt_file),
            )

            media = project / "artifacts" / "clip-01.mp4"
            frame = project / "artifacts" / "clip-01-final.png"
            media.write_bytes(MP4_BYTES + b"clip1")
            frame.write_bytes(PNG_BYTES + b"clip1")
            observation = root / "observation.json"
            observation.write_text(json.dumps(OBSERVED), encoding="utf-8")
            self.run_cli(
                "observe",
                "--project",
                str(project),
                "--shot-id",
                "clip-01",
                "--state",
                str(observation),
                "--media",
                str(media),
                "--final-frame",
                str(frame),
            )

            diff = self.run_cli(
                "diff",
                "--project",
                str(project),
                "--shot-id",
                "clip-01",
            )
            self.assertEqual(json.loads(diff.stdout)["authoritative_source"], "observed")

            grammar = root / "grammar.json"
            grammar.write_text(json.dumps(GRAMMAR), encoding="utf-8")
            sequence = root / "sequence.json"
            sequence.write_text(json.dumps(SEQUENCE), encoding="utf-8")
            contract = root / "contract.json"
            prompt = root / "compiled.md"
            self.run_cli(
                "compile-next",
                "--project",
                str(project),
                "--from-shot",
                "clip-01",
                "--next-shot",
                "clip-02-shotflow",
                "--beat",
                "Seal the fissure",
                "--grammar",
                str(grammar),
                "--sequence",
                str(sequence),
                "--contract-out",
                str(contract),
                "--prompt-out",
                str(prompt),
            )
            self.assertTrue(json.loads(contract.read_text())["continuity_safe"])
            self.assertIn("left hand", prompt.read_text())
            self.assertEqual(prompt.read_text().count(" | "), 5)

            clip2 = project / "artifacts" / "clip-02.mp4"
            clip2_frame = project / "artifacts" / "clip-02-final.png"
            clip2.write_bytes(MP4_BYTES + b"clip2")
            clip2_frame.write_bytes(PNG_BYTES + b"clip2")
            self.run_cli(
                "observe",
                "--project",
                str(project),
                "--shot-id",
                "clip-02-shotflow",
                "--state",
                str(observation),
                "--media",
                str(clip2),
                "--final-frame",
                str(clip2_frame),
            )

            evaluation = root / "evaluation.json"
            evaluation.write_text(json.dumps(EVALUATION), encoding="utf-8")
            scored = self.run_cli(
                "score",
                "--project",
                str(project),
                "--shot-id",
                "clip-02-shotflow",
                "--evaluation",
                str(evaluation),
            )
            self.assertEqual(json.loads(scored.stdout)["score"], 100)

    def test_invalid_json_returns_validation_exit_code(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            project = root / "demo"
            self.run_cli("init", str(project), "--title", "Demo")
            invalid = root / "invalid.json"
            invalid.write_text("{", encoding="utf-8")
            result = self.run_cli(
                "plan",
                "--project",
                str(project),
                "--shot-id",
                "clip-01",
                "--beat",
                "Begin",
                "--spec",
                str(invalid),
                expected=2,
            )
            self.assertIn("Invalid JSON", result.stderr)


if __name__ == "__main__":
    unittest.main()
