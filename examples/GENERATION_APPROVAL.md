# Generation approval gate

Status: **GATE 1 COMPLETE — THREE CLIP 01 OUTPUTS ACCEPTED**

## Fixed settings

- Provider: 小云雀
- Model: `seedance2.0_vision`
- Ratio: `16:9`
- Resolution: `1080p`
- Duration: `5` seconds
- Minimum accepted outputs: `9`
- Maximum video-generation attempts: `18`
- Automatic model downgrade: disabled
- Automatic recharge: disabled

## Attempt budget

| Case | Required outputs | Maximum attempts |
| --- | ---: | ---: |
| The Sky Mender | 3 | 8 |
| Storm Deck | 3 | 5 |
| Obsidian Bloom | 3 | 5 |
| **Total** | **9** | **18** |

Only a failed or continuity-breaking result may use a retry. Every attempt remains in the local evidence ledger.

## Two approval gates

### Gate 1 — Clip 01

Review the three `clip-01.txt` prompts and the three frozen `clip-02-baseline-frozen.txt` prompts. Approval authorizes only the initial Clip 01 submissions, one per case.

Completed on 2026-07-29 with one accepted submission per case. No generation retry was used. One rate-limited submission request was retried after the provider's required one-minute interval; it did not create a run and is not counted as a generation attempt.

### Gate 2 — Clip 02 variants

After each accepted Clip 01:

1. download the video without removing provider marks;
2. extract its final frame locally;
3. complete `observation.template.json`;
4. run `shotflow observe`, `diff`, and `compile-next`;
5. present the baseline and compiled ShotFlow Clip 02 prompts side-by-side.

Approval then authorizes the baseline and ShotFlow Clip 02 submissions for that case, with identical Clip 01 references and provider settings.

Current state: awaiting explicit approval of the six initial Clip 02 submissions in [GATE_2_APPROVAL.md](GATE_2_APPROVAL.md).

## Public disclosure

Every published case must say that it was AI generated with 小云雀 / Seedance 2.0. Inputs must remain original or authorized. Private account URLs, run IDs, credentials, and cookies stay outside the repository.
