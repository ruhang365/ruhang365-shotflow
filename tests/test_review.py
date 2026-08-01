from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from shotflow.core import ShotFlowError
from shotflow.review import prepare_blind_pair, probe_video


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "ffmpeg required")
class ReviewTests(unittest.TestCase):
    def make_video(self, path: Path, size: str, color: str) -> None:
        result = subprocess.run(
            [
                "ffmpeg",
                "-hide_banner",
                "-loglevel",
                "error",
                "-f",
                "lavfi",
                "-i",
                f"color=c={color}:s={size}:d=5.05:r=24",
                "-an",
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-y",
                str(path),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def make_frame(self, path: Path) -> None:
        result = subprocess.run(
            [
                "ffmpeg",
                "-hide_banner",
                "-loglevel",
                "error",
                "-f",
                "lavfi",
                "-i",
                "color=c=black:s=1920x1080",
                "-frames:v",
                "1",
                "-y",
                str(path),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_prepare_blind_pair_normalizes_both_sides(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            baseline = root / "baseline.mp4"
            shotflow = root / "shotflow.mp4"
            reference = root / "reference.png"
            baseline_prompt = root / "baseline.txt"
            shotflow_prompt = root / "shotflow.txt"
            self.make_video(baseline, "1280x720", "black")
            self.make_video(shotflow, "1920x1080", "gray")
            self.make_frame(reference)
            baseline_prompt.write_text("baseline\n", encoding="utf-8")
            shotflow_prompt.write_text("shotflow\n", encoding="utf-8")
            output = root / "review"
            manifest = prepare_blind_pair(
                case_id="case",
                pair_id="pair-01",
                reference_frame=reference,
                baseline_video=baseline,
                shotflow_video=shotflow,
                baseline_prompt=baseline_prompt,
                shotflow_prompt=shotflow_prompt,
                output_directory=output,
                variant_a="shotflow",
                platform="Lovart",
                model_tool="generate_video_seedance_v2_0",
                generation_mode="unlimited",
                reasoning_mode="thinking",
                generation_order=("baseline", "shotflow"),
            )
            self.assertEqual(manifest["blind_mapping"]["A"], "shotflow")
            for variant in ("baseline", "shotflow"):
                self.assertEqual(manifest["canonical"][variant]["width"], 1280)
                self.assertEqual(manifest["canonical"][variant]["height"], 720)
                self.assertEqual(manifest["canonical"][variant]["fps"], 24)
            reviewer = output / "reviewer"
            internal = output / "internal"
            self.assertTrue((reviewer / "review-package.json").is_file())
            self.assertTrue((reviewer / "accepted-reference.png").is_file())
            self.assertTrue((reviewer / "variant-a-contact.png").is_file())
            self.assertTrue((reviewer / "variant-b-contact.png").is_file())
            self.assertTrue((internal / "evaluation-pair.json").is_file())
            self.assertFalse((reviewer / "evaluation-pair.json").exists())
            self.assertEqual(
                probe_video(reviewer / "variant-a.mp4")["duration_seconds"], 5.0
            )

    def test_rejects_source_below_720p(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            low = root / "low.mp4"
            valid = root / "valid.mp4"
            reference = root / "reference.png"
            prompt = root / "prompt.txt"
            self.make_video(low, "640x360", "black")
            self.make_video(valid, "1280x720", "gray")
            self.make_frame(reference)
            prompt.write_text("prompt\n", encoding="utf-8")
            with self.assertRaisesRegex(ShotFlowError, "at least 1280x720"):
                prepare_blind_pair(
                    case_id="case",
                    pair_id="pair-01",
                    reference_frame=reference,
                    baseline_video=low,
                    shotflow_video=valid,
                    baseline_prompt=prompt,
                    shotflow_prompt=prompt,
                    output_directory=root / "review",
                    variant_a="baseline",
                    platform="Lovart",
                    model_tool="generate_video_seedance_v2_0",
                    generation_mode="unlimited",
                    reasoning_mode="thinking",
                    generation_order=("baseline", "shotflow"),
                )


if __name__ == "__main__":
    unittest.main()
