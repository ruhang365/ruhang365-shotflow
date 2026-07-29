# Gate 3 approval — standard Seedance 2.0 model

Status: **STOPPED — STANDARD MODEL REJECTED THE APPROVED 1080P SETTINGS**

This gate replaces the incomplete VIP Clip 02 run. It does not alter or erase
the historical VIP evidence.

## Why all six Clip 02 videos must be regenerated

The fair A/B variable is the Prompt mechanism. Baseline and ShotFlow must use
the same model, parameters, Clip 01 video, and final frame. A new standard-model
ShotFlow result cannot be compared with the previous VIP baseline.

The three accepted Clip 01 videos remain valid shared references. For each case,
both Clip 02 variants will use the same Clip 01 video and final frame.

## Fixed settings

- Provider: 小云雀 / Xiaoyunque
- Xiaoyunque model value / proposed CLI model ID: `seedance2.0_direct`
- Visible product tier: full `Seedance 2.0`, not Mini, Fast, or VIP
- Queue policy: effect-first; the slower non-VIP queue is acceptable
- Ratio: `16:9`
- Resolution: `1080p`
- Duration: `5` seconds
- Initial submissions authorized by this gate: `6`
- Automatic retry: disabled
- Automatic recharge: disabled
- Automatic downgrade: disabled
- Current adapter evidence state: `verified=false`

Successful real outputs are required before this model can be marked
forward-tested. The current web client maps `seedance2.0_direct` to
“Seedance 2.0” and maps `Seedance_2.0_mini_lite` to
“Seedance 2.0 Mini 体验版”. The installed CLI does not yet list the full standard
model in its help text, so a service rejection must stop the run without retry,
fallback, or model substitution.

## Gate outcome

On 2026-07-30, the first frozen job (The Sky Mender baseline) was submitted
with the approved prompt, shared references, and fixed settings. The provider
rejected it before returning a `thread_id` or `run_id`:

> `seedance2.0_direct` does not support `1080p`; the service reported that
> `1080p` is limited to `seedance2.0_vision` and `Seedance_2.5`.

The remaining five jobs were not submitted. No retry, recharge, resolution
downgrade, or model substitution was performed. Continuing requires a new
decision because either the resolution or model must change.

## Frozen jobs

| Case | Variant | Exact Prompt | Prompt SHA-256 |
| --- | --- | --- | --- |
| The Sky Mender | baseline | [`clip-02-baseline-frozen.txt`](sky-mender/prompts/clip-02-baseline-frozen.txt) | `065e32b4788d3e86faec7226b451f843227d6b32f0f941ddff73ee9161288e35` |
| The Sky Mender | ShotFlow v2 | [`clip-02-shotflow-v2.txt`](sky-mender/prompts/clip-02-shotflow-v2.txt) | `8b4654143c531b237c4797aac666a7cde70b9f184b5327c92f61fcc2b36b1201` |
| Storm Deck | baseline | [`clip-02-baseline-frozen.txt`](storm-deck/prompts/clip-02-baseline-frozen.txt) | `3d7e34a97bf97aaad1131deccaf9200603fd7ca56c729669b67bbddd5cc777fb` |
| Storm Deck | ShotFlow v2 | [`clip-02-shotflow-v2.txt`](storm-deck/prompts/clip-02-shotflow-v2.txt) | `a9f1d5136dca79a0944c24a9bb940befa194fdd54c9ffd768098e5dabf0e9439` |
| Obsidian Bloom | baseline | [`clip-02-baseline-frozen.txt`](obsidian-bloom/prompts/clip-02-baseline-frozen.txt) | `5b0cd96768dfd861ddd790d05de78f91c100242cb8975f7dca4a117fb19d1884` |
| Obsidian Bloom | ShotFlow v2 | [`clip-02-shotflow-v2.txt`](obsidian-bloom/prompts/clip-02-shotflow-v2.txt) | `55344974177eb1c9d5caf622c8e5efd7e91f45fd1f4044051a4921008021ef4d` |

## Shared reference hashes

| Case | Clip 01 video SHA-256 | Final-frame SHA-256 |
| --- | --- | --- |
| The Sky Mender | `09564c755fc4b845f501e5bcf68e4192b65bc00e8a2be395159a05c831c99243` | `f05efcff94c047cdf46f681daf8996896e257ea3e9a6e54f1d36944b81bba1cd` |
| Storm Deck | `d7e36d9b270a3f9280dca19d50afe856177c3426e1a12a0b3511dbc811a2a198` | `5b32eb1a7519d543be037cf86c8e2079803d8f9a7be99174184c691c4faec5f6` |
| Obsidian Bloom | `af845de5b3eff841f1b142b6ae03bf66e0585d073129da7856f6ebfb9180d827` | `56d6455da0310b8acce2364af99229825307b70bae8f677306496c1fa08e8a0e` |

This approval is now closed by the provider rejection. Any retry, resolution
change, model change, publication, or social post requires a separate decision.
