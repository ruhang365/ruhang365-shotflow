# ShotFlow evidence cases

These three original cases are pre-registered A/B experiments, not finished
performance claims. Their real Clip 01 outputs are accepted and observed. The
first Clip 02 pair failed the ShotFlow claim gate; the remaining run stopped
when provider credits were insufficient.

| Case | Role | Primary continuity stress | Clip 01 evidence |
| --- | --- | --- | --- |
| [The Sky Mender](sky-mender/) | Flagship spectacle | identity, prop hand, open motion, weather light | [preview](sky-mender/evidence/clip-01-preview.gif) · [receipt](sky-mender/evidence/clip-01-receipt.json) |
| [Storm Deck](storm-deck/) | Physical action | prop ownership, screen direction, inertia, geography | [preview](storm-deck/evidence/clip-01-preview.gif) · [receipt](storm-deck/evidence/clip-01-receipt.json) |
| [Obsidian Bloom](obsidian-bloom/) | Fictional product film | silhouette, cap geometry, reflection, liquid state | [preview](obsidian-bloom/evidence/clip-01-preview.gif) · [receipt](obsidian-bloom/evidence/clip-01-receipt.json) |

Each case freezes its baseline Clip 02 prompt before Clip 01 is generated. The ShotFlow Clip 02 prompt cannot exist until an accepted Clip 01 has been observed.

See [GATE_2_APPROVAL.md](GATE_2_APPROVAL.md) for the exact submitted prompts,
shared references, failed run state, and frozen v2 candidates.

[GATE_3_STANDARD_MODEL_APPROVAL.md](GATE_3_STANDARD_MODEL_APPROVAL.md) records
the stopped standard-model attempt. The proposed successor is
[GATE_4_VIP_1080P_APPROVAL.md](GATE_4_VIP_1080P_APPROVAL.md). Google Flow remains
an independent portability check described in
[GOOGLE_FLOW_VALIDATION.md](GOOGLE_FLOW_VALIDATION.md).
