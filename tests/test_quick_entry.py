from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from shotflow.quick_entry import extract_quick_prompt, validate_quick_output


VALID_PROMPT = """SEEDANCE PROMPT
FRAME 1 AUTHORITY:
Attachment 1 is the accepted endpoint. Frame 1 matches the visible product, camera, light, and materials.

KEEP STABLE
- The centered black faceted bottle and asymmetric silver collar remain stable.
- The locked near-frontal camera and cool background remain stable.

CHANGE | 0.50-4.25s
The amber glow inside the lower bottle gradually intensifies to a warm, clearly visible level.

FINAL PROOF | 4.25-5.00s
The stronger amber glow holds inside the unchanged bottle.

SUBMIT WITH
- Attachment 1: the accepted final frame, as the only media reference
- Duration: 5 seconds
- Ratio: 16:9
- Generation submitted: no
"""


class QuickEntryTests(unittest.TestCase):
    def test_valid_output(self) -> None:
        self.assertEqual(validate_quick_output(VALID_PROMPT, expected_ratio="16:9"), [])
        prompt, submission = extract_quick_prompt(VALID_PROMPT)
        self.assertIn("FRAME 1 AUTHORITY", prompt)
        self.assertIn("Generation submitted: no", submission)

    def test_chinese_submission_block_is_supported(self) -> None:
        output = VALID_PROMPT.replace("SUBMIT WITH", "提交方式").replace(
            "- Attachment 1: the accepted final frame, as the only media reference\n"
            "- Duration: 5 seconds\n- Ratio: 16:9\n- Generation submitted: no",
            "- 附件 1：已接受最终帧，并作为唯一媒体参考\n"
            "- 时长：5 秒\n- 比例：16:9\n- 已提交生成：否",
        )
        self.assertEqual(validate_quick_output(output, expected_ratio="16:9"), [])

    def test_overlong_prompt_is_rejected(self) -> None:
        output = VALID_PROMPT.replace(
            "The stronger amber glow holds inside the unchanged bottle.",
            "The stronger amber glow holds. " + ("x" * 1200),
        )
        self.assertIn(
            "prompt_over_1200_characters",
            validate_quick_output(output, expected_ratio="16:9"),
        )

    def test_negative_directive_is_rejected(self) -> None:
        output = VALID_PROMPT.replace(
            "The stronger amber glow holds inside the unchanged bottle.",
            "Do not move the bottle.",
        )
        self.assertIn(
            "negative_directive",
            validate_quick_output(output, expected_ratio="16:9"),
        )

    def test_multiple_attachments_are_rejected(self) -> None:
        output = VALID_PROMPT.replace(
            "- Duration: 5 seconds", "- Attachment 2: source video\n- Duration: 5 seconds"
        )
        self.assertIn(
            "multiple_media_references",
            validate_quick_output(output, expected_ratio="16:9"),
        )

    def test_wrong_ratio_and_submission_state_are_rejected(self) -> None:
        output = VALID_PROMPT.replace("16:9", "9:16").replace(
            "Generation submitted: no", "Generation submitted: yes"
        )
        errors = validate_quick_output(output, expected_ratio="16:9")
        self.assertIn("wrong_or_missing_ratio", errors)
        self.assertIn("missing_not_submitted_state", errors)

    def test_private_terms_are_rejected(self) -> None:
        output = VALID_PROMPT + "API key: example"
        self.assertIn(
            "private_data_term",
            validate_quick_output(output, expected_ratio="16:9"),
        )

    def test_frozen_forward_test_protocol_has_real_unique_frames(self) -> None:
        root = Path(__file__).resolve().parents[1]
        protocol_path = root / "examples" / "forward-tests" / "protocol-v04-rc2.json"
        protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
        self.assertEqual(protocol["quick_entry_version"], "1.0")
        self.assertFalse(protocol["generation_allowed"])
        self.assertEqual(protocol["minimum_valid_authors"], 5)
        self.assertEqual(protocol["minimum_passing_outputs"], 4)
        self.assertEqual(len(protocol["cases"]), 5)
        self.assertGreaterEqual(
            len({case["author_lane"] for case in protocol["cases"]}),
            2,
        )
        hashes = set()
        for case in protocol["cases"]:
            frame = (protocol_path.parent / case["frame"]).resolve(strict=True)
            frame.relative_to(root / "examples")
            actual = hashlib.sha256(frame.read_bytes()).hexdigest()
            self.assertEqual(actual, case["frame_sha256"])
            self.assertEqual(case["ratio"], "16:9")
            hashes.add(actual)
        self.assertEqual(len(hashes), 5)

    def test_quick_entry_documents_visual_measurement_proxy(self) -> None:
        root = Path(__file__).resolve().parents[1]
        reference = (
            root / "skills" / "shotflow" / "references" / "quick-entry.md"
        ).read_text(encoding="utf-8")
        self.assertIn("one centimeter", reference)
        self.assertIn("visible relative bound", reference)


if __name__ == "__main__":
    unittest.main()
