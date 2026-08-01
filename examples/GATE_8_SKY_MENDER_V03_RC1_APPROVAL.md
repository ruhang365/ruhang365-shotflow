# Gate 8 — The Sky Mender v0.3 RC1

Status: **BLOCKED — GATE 7 CLOSED WITH AN INVALID PAIR**

Gate 8 is the cross-type and flagship validation. Gate 7 produced unequal
native resolutions and closed without a valid blind review, so Gate 8 is not
authorized. It does not reopen or alter the historical Sky Mender attempt
ledger.

## Fixed provider conditions

- Lovart, `generate_video_seedance_v2_0`, `thinking`, 16:9, 5 seconds
- Same accepted Clip 01 final frame only under `anchor-frame-v2`
- One baseline and one v0.3 job; maximum two jobs
- Same native resolution for both and at least 1280×720
- No retry, upscale, downgrade, fallback, or automatic confirmation
- Current cost and balance must be shown for a new explicit user approval

## Frozen inputs

| Input | SHA-256 |
| --- | --- |
| [Public JPEG preview of accepted frame](sky-mender/evidence/clip-01-final-frame.jpg) | Authoritative local PNG hash in both handoffs: `f05efcff94c047cdf46f681daf8996896e257ea3e9a6e54f1d36944b81bba1cd` |
| [Baseline creative Prompt](sky-mender/prompts/clip-02-baseline-frozen.txt) | `065e32b4788d3e86faec7226b451f843227d6b32f0f941ddff73ee9161288e35` |
| [v0.3 creative Prompt](sky-mender/prompts/clip-02-shotflow-v4-rc1.txt) | `5d22afd7c083e7abb94b201e2f1f331ee37cf7b5110b6462b563bee4b08a7951` |
| [Ordered Sequence 1.1](sky-mender/plan/clip-02-sequence-v4.json) | `6ebf0e6c16fd3756d117b697a2d677441484a753fd04ca6617349cd8d76723e8` |
| [Five-axis grammar](sky-mender/plan/clip-02-grammar-v4.json) | `8faa29c78709d20f6c9fbd7326cf8b2cae7613eb2970b136d3a6f7117b06913c` |
| [Baseline handoff](sky-mender/evidence/provider-handoff-baseline-v03-gate8.json) | `97b50ccf9155bbcedb7805670be018e9ddbb18d86e4bd814015cc6e317d456a9` |
| [v0.3 handoff](sky-mender/evidence/provider-handoff-shotflow-v4-rc1-gate8.json) | `0d904a2ae87f5c1bf8cf50c192dacc7a9499feb95b87a451957db6526cf72aba` |

## Stable-release rule

Both Gate 7 and Gate 8 must have majority v0.3 wins, their combined normalized
mean improvement must be at least 20 points, and The Sky Mender must pass the
user's “worth a social launch” acceptance. Full A/B media requires separate
user approval before public upload. Otherwise RC1 and all failure evidence stay
public, while stable v0.3 and positive claims remain blocked.
