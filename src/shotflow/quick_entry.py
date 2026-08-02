"""Validation helpers for the final-frame-first Quick Entry 1.0 contract."""

from __future__ import annotations

import re


QUICK_ENTRY_VERSION = "1.0"
QUICK_PROMPT_LIMIT = 1200
PROMPT_HEADER = "SEEDANCE PROMPT"
SUBMISSION_HEADERS = ("SUBMIT WITH", "提交方式")
PROMPT_SECTIONS = (
    "FRAME 1 AUTHORITY",
    "KEEP STABLE",
    "CHANGE",
    "FINAL PROOF",
)
NEGATIVE_DIRECTIVES = re.compile(
    r"(?i)\b(?:do not|must not|never|avoid|without)\b|不要|禁止|不得|避免"
)
PRIVATE_DATA = re.compile(
    r"(?i)\b(?:api[_ -]?key|access[_ -]?key|secret[_ -]?key|bearer token|cookie|session id)\b"
)


def extract_quick_prompt(output: str) -> tuple[str, str]:
    """Return the Prompt and submission block from one Quick Entry response."""

    if PROMPT_HEADER not in output:
        return "", ""
    after_header = output.split(PROMPT_HEADER, 1)[1].lstrip(" \t:\r\n")
    positions = [
        (after_header.find(header), header)
        for header in SUBMISSION_HEADERS
        if after_header.find(header) >= 0
    ]
    if not positions:
        return after_header.strip(), ""
    position, header = min(positions, key=lambda item: item[0])
    return after_header[:position].strip(), after_header[position + len(header) :].strip()


def validate_quick_output(output: str, *, expected_ratio: str) -> list[str]:
    """Return stable validation error codes for Quick Entry 1.0 output."""

    errors: list[str] = []
    prompt, submission = extract_quick_prompt(output)
    if not prompt:
        errors.append("missing_seedance_prompt")
    if not submission:
        errors.append("missing_submit_with")
    if prompt and len(prompt) > QUICK_PROMPT_LIMIT:
        errors.append("prompt_over_1200_characters")
    for section in PROMPT_SECTIONS:
        if section not in prompt:
            errors.append(f"missing_{section.lower().replace(' ', '_')}")
    if NEGATIVE_DIRECTIVES.search(prompt):
        errors.append("negative_directive")
    if PRIVATE_DATA.search(output):
        errors.append("private_data_term")
    if "Attachment 2" in output or "附件 2" in output:
        errors.append("multiple_media_references")

    attachment_ok = (
        "Attachment 1" in submission
        and "only media reference" in submission.lower()
    ) or ("附件 1" in submission and "唯一媒体参考" in submission)
    if not attachment_ok:
        errors.append("missing_only_final_frame_attachment")

    duration_ok = bool(
        re.search(r"(?i)(?:duration\s*:\s*5\s*seconds|时长\s*[：:]\s*5\s*秒)", submission)
    )
    if not duration_ok:
        errors.append("missing_five_second_duration")
    if expected_ratio not in submission:
        errors.append("wrong_or_missing_ratio")

    not_submitted = bool(
        re.search(r"(?i)generation submitted\s*:\s*no", submission)
        or re.search(r"已提交生成\s*[：:]\s*否", submission)
    )
    if not not_submitted:
        errors.append("missing_not_submitted_state")
    return errors

