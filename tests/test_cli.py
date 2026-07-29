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
            media.write_bytes(b"video")
            frame.write_bytes(b"frame")
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
                "--contract-out",
                str(contract),
                "--prompt-out",
                str(prompt),
            )
            self.assertTrue(json.loads(contract.read_text())["continuity_safe"])
            self.assertIn("tool in left hand", prompt.read_text())

            clip2 = project / "artifacts" / "clip-02.mp4"
            clip2_frame = project / "artifacts" / "clip-02-final.png"
            clip2.write_bytes(b"clip2")
            clip2_frame.write_bytes(b"clip2frame")
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
