from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from shotflow.core import ShotFlowError
from shotflow.evidence import record_attempt


ROOT = Path(__file__).resolve().parents[1]
MP4_BYTES = b"\x00\x00\x00\x18ftypisom\x00\x00\x00\x00"
PNG_BYTES = b"\x89PNG\r\n\x1a\nshotflow"


class EvidenceTests(unittest.TestCase):
    def create_case(self, temporary: str) -> Path:
        source = ROOT / "examples" / "storm-deck"
        target = Path(temporary) / "storm-deck"
        shutil.copytree(
            source,
            target,
            ignore=shutil.ignore_patterns("artifacts", ".shotflow-private"),
        )
        (target / "artifacts").mkdir()
        (target / "attempts.json").write_text(
            '{\n  "ledger_version": "1.0",\n'
            '  "case_id": "storm-deck",\n  "attempts": []\n}\n',
            encoding="utf-8",
        )
        return target

    def test_attempt_lifecycle_preserves_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            case = self.create_case(temporary)
            prompt = case / "prompts" / "clip-01.txt"
            submitted = record_attempt(case, "clip-01", "submitted", prompt)
            self.assertEqual(submitted["attempt_id"], "storm-deck-001")

            video = case / "artifacts" / "clip-01.mp4"
            frame = case / "artifacts" / "clip-01-final.png"
            video.write_bytes(MP4_BYTES + b"video")
            frame.write_bytes(PNG_BYTES + b"frame")
            accepted = record_attempt(
                case,
                "clip-01",
                "accepted",
                prompt,
                attempt_id="storm-deck-001",
                output_video=video,
                output_final_frame=frame,
            )
            self.assertEqual(accepted["status"], "accepted")
            self.assertEqual(accepted["prompt"]["sha256"], submitted["prompt"]["sha256"])

    def test_clip2_requires_shared_references(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            case = self.create_case(temporary)
            prompt = case / "prompts" / "clip-02-baseline-frozen.txt"
            with self.assertRaisesRegex(ShotFlowError, "shared Clip 01"):
                record_attempt(case, "clip-02-baseline", "submitted", prompt)

    def test_rejected_attempt_requires_reason(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            case = self.create_case(temporary)
            prompt = case / "prompts" / "clip-01.txt"
            with self.assertRaisesRegex(ShotFlowError, "require a reason"):
                record_attempt(case, "clip-01", "rejected", prompt)


if __name__ == "__main__":
    unittest.main()
