"""ShotFlow public package."""

from .core import (
    CHECKPOINT_PHASES,
    GRAMMAR_AXES,
    SCORE_DIMENSIONS,
    SEQUENCE_ANCHORS,
    ShotFlowError,
    compile_next_shot,
    diff_states,
    score_evaluation,
    validate_ordered_sequence,
)

__all__ = [
    "CHECKPOINT_PHASES",
    "GRAMMAR_AXES",
    "SCORE_DIMENSIONS",
    "SEQUENCE_ANCHORS",
    "ShotFlowError",
    "compile_next_shot",
    "diff_states",
    "score_evaluation",
    "validate_ordered_sequence",
]

__version__ = "0.2.0"
