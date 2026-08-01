# ShotFlow evidence cases

These three original cases are pre-registered A/B experiments, not finished
performance claims. Their real Clip 01 outputs are accepted and observed. The
first Clip 02 pair failed the ShotFlow claim gate. A later Sky Mender v2 retry
improved motion continuity but still failed the required visible story beat,
so that case is rejected and frozen with no further retries.

| Case | Role | Primary continuity stress | Clip 01 evidence |
| --- | --- | --- | --- |
| [The Sky Mender](sky-mender/) | Flagship spectacle | identity, prop hand, open motion, weather light | [preview](sky-mender/evidence/clip-01-preview.gif) · [receipt](sky-mender/evidence/clip-01-receipt.json) |
| [Storm Deck](storm-deck/) | Physical action | prop ownership, screen direction, inertia, geography | [preview](storm-deck/evidence/clip-01-preview.gif) · [receipt](storm-deck/evidence/clip-01-receipt.json) |
| [Obsidian Bloom](obsidian-bloom/) | Fictional product film | silhouette, cap geometry, reflection, liquid state | [preview](obsidian-bloom/evidence/clip-01-preview.gif) · [receipt](obsidian-bloom/evidence/clip-01-receipt.json) |

Each case freezes its baseline Clip 02 prompt before Clip 01 is generated. The ShotFlow Clip 02 prompt cannot exist until an accepted Clip 01 has been observed.

See [GATE_2_APPROVAL.md](GATE_2_APPROVAL.md) for the exact submitted prompts,
shared references, failed run state, and frozen v2 candidates.

[GATE_3_STANDARD_MODEL_APPROVAL.md](GATE_3_STANDARD_MODEL_APPROVAL.md) records
the stopped standard-model attempt.
[GATE_4_VIP_1080P_APPROVAL.md](GATE_4_VIP_1080P_APPROVAL.md) records the
subsequent VIP retry and the later retirement of the remaining Xiaoyunque/Flow
queue. Lovart Kling O1 and Seedance 2.0 Storm Deck pilots were both rejected.
The corrected one-job retry is recorded in
[GATE_4_STORM_DECK_BASELINE_APPROVAL.md](GATE_4_STORM_DECK_BASELINE_APPROVAL.md).
It repeated the opening-frame failure at 720p and closed Storm Deck at its
registered attempt cap.

The next registered mechanism is `anchor-frame-v1` for Obsidian Bloom. It gives
both A/B variants the same accepted final frame as their only media reference,
so a generic attachment interface cannot restart the source video. The
[baseline gate](GATE_6_OBSIDIAN_BLOOM_BASELINE_ANCHOR_APPROVAL.md) and separate
[ShotFlow gate](GATE_6_OBSIDIAN_BLOOM_SHOTFLOW_ANCHOR_APPROVAL.md) are frozen,
with separate approval boundaries. Lovart exposes no resolution selector, so
the registered experiment uses provider-native output with a 1280×720 minimum,
keeps the standard Seedance 2.0 model, and forbids Fast, Mini, fallback, and
upscale. Both jobs returned 1920×1080. The separately approved ShotFlow job
then lost a three-reviewer blind comparison because its cap hinged, droplet
fell, and amber ribbon connected to the bottle base/liquid surface. It was
rejected without retry. See the
[blind review](obsidian-bloom/reviews/clip-02-blind-review-anchor-v1.md).
The resulting `provider-direct-v3` candidate is frozen as an offline-only
[five-checkpoint sequence](obsidian-bloom/plan/clip-02-sequence-v3.json),
[positive grammar](obsidian-bloom/plan/clip-02-grammar-v3.json), and
[compiled Prompt](obsidian-bloom/prompts/clip-02-shotflow-v3-offline.txt). It is
not a generation approval.

Provider continuity is part of the experiment contract. The corrected Lovart
handoff fixes reference roles, excludes historical thread artifacts by hash,
and requires the first generated frame to pass manual continuity review.

## v0.3 RC1 causal-budget gates

RC1 freezes a new mechanism without claiming that it works better. Ordered
Sequence `1.1` separates stable `protected` facts from one to three authorized
`transitions`, binds them to checkpoint `active_changes`, and compiles a
positive `provider-direct-v4` Prompt with final proof. Both variants use the
same accepted final frame through `anchor-frame-v2`.

- [Preflight contradiction review](V03_RC1_PREFLIGHT_REVIEW.md)
- [Gate 7 — Obsidian Bloom](GATE_7_OBSIDIAN_BLOOM_V03_RC1_APPROVAL.md): frozen,
  awaiting a separate Lovart cost confirmation
- [Gate 8 — The Sky Mender](GATE_8_SKY_MENDER_V03_RC1_APPROVAL.md): frozen and
  blocked unless Gate 7 receives a majority v0.3 win

Gate 7 permits one baseline job and one v0.3 job only. A loss, invalid pair,
or failed job stops the sequence; it does not authorize retries or Gate 8.
