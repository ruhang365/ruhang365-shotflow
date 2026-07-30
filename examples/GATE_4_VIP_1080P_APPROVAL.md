# Gate 4 approval — Seedance 2.0 VIP at 1080p

Status: **CLOSED — STOPPED AFTER THE FIRST JOB**

This gate follows the provider rejection recorded in Gate 3. It does not erase
the failed standard-model attempt or the earlier VIP v1 evidence.

## Recorded outcome

The first authorized job, The Sky Mender ShotFlow v2, was submitted with the
exact frozen prompt, references, model, and settings below. The provider
completed the task without returning media because the account had insufficient
credits.

Execution stopped immediately under the pre-registered stop rules:

- New jobs submitted: `1`
- Media outputs received: `0`
- Remaining Xiaoyunque jobs submitted: `0`
- Automatic retry, recharge, downgrade, or model substitution: `none`

The failed public-safe attempt is recorded as `sky-mender-005` in
[`sky-mender/attempts.json`](sky-mender/attempts.json). Private account and task
identifiers are intentionally excluded.

## Why only five new videos are required

The existing Sky Mender baseline already used the exact frozen baseline prompt,
`seedance2.0_vision`, 16:9, 1080p, five seconds, and the accepted Clip 01 video
and final frame listed below. It is therefore a valid comparator for the new
ShotFlow v2 prompt and does not need to be purchased again.

Storm Deck and Obsidian Bloom still need both variants. The new paid workload is:

1. The Sky Mender — ShotFlow v2
2. Storm Deck — baseline
3. Storm Deck — ShotFlow v2
4. Obsidian Bloom — baseline
5. Obsidian Bloom — ShotFlow v2

## Fixed settings

- Provider: 小云雀 / Xiaoyunque
- CLI model ID: `seedance2.0_vision`
- Visible product tier: `Seedance 2.0 VIP`
- Ratio: `16:9`
- Resolution: `1080p`
- Duration: `5` seconds
- New submissions authorized by this gate: `5`
- Existing result reused: `1` Sky Mender baseline
- Automatic retry: disabled
- Automatic recharge: disabled
- Automatic downgrade or model substitution: disabled
- Adapter evidence state: `verified=true`

## Frozen paid jobs

| Case | Variant | Exact Prompt | Prompt SHA-256 |
| --- | --- | --- | --- |
| The Sky Mender | ShotFlow v2 | [`clip-02-shotflow-v2.txt`](sky-mender/prompts/clip-02-shotflow-v2.txt) | `8b4654143c531b237c4797aac666a7cde70b9f184b5327c92f61fcc2b36b1201` |
| Storm Deck | baseline | [`clip-02-baseline-frozen.txt`](storm-deck/prompts/clip-02-baseline-frozen.txt) | `3d7e34a97bf97aaad1131deccaf9200603fd7ca56c729669b67bbddd5cc777fb` |
| Storm Deck | ShotFlow v2 | [`clip-02-shotflow-v2.txt`](storm-deck/prompts/clip-02-shotflow-v2.txt) | `a9f1d5136dca79a0944c24a9bb940befa194fdd54c9ffd768098e5dabf0e9439` |
| Obsidian Bloom | baseline | [`clip-02-baseline-frozen.txt`](obsidian-bloom/prompts/clip-02-baseline-frozen.txt) | `5b0cd96768dfd861ddd790d05de78f91c100242cb8975f7dca4a117fb19d1884` |
| Obsidian Bloom | ShotFlow v2 | [`clip-02-shotflow-v2.txt`](obsidian-bloom/prompts/clip-02-shotflow-v2.txt) | `55344974177eb1c9d5caf622c8e5efd7e91f45fd1f4044051a4921008021ef4d` |

## Reused baseline

| Case | Variant | Prompt SHA-256 | Video SHA-256 |
| --- | --- | --- | --- |
| The Sky Mender | baseline | `065e32b4788d3e86faec7226b451f843227d6b32f0f941ddff73ee9161288e35` | `7361c6a3fbb8090c58514a1698a1ea90e56bb5349b2766d7a12c8c2605dcc51f` |

## Shared reference hashes

| Case | Clip 01 video SHA-256 | Final-frame SHA-256 |
| --- | --- | --- |
| The Sky Mender | `09564c755fc4b845f501e5bcf68e4192b65bc00e8a2be395159a05c831c99243` | `f05efcff94c047cdf46f681daf8996896e257ea3e9a6e54f1d36944b81bba1cd` |
| Storm Deck | `d7e36d9b270a3f9280dca19d50afe856177c3426e1a12a0b3511dbc811a2a198` | `5b32eb1a7519d543be037cf86c8e2079803d8f9a7be99174184c691c4faec5f6` |
| Obsidian Bloom | `af845de5b3eff841f1b142b6ae03bf66e0585d073129da7856f6ebfb9180d827` | `56d6455da0310b8acce2364af99229825307b70bae8f677306496c1fa08e8a0e` |

## Execution stop rules

- Submit jobs sequentially.
- Stop immediately on model rejection, insufficient credits, or missing media.
- A failed job is recorded but not retried automatically.
- Any retry, parameter change, sixth paid job, publication, or social post
  requires a new decision.

This gate is closed. Any Xiaoyunque retry or new paid submission requires a new
gate with the exact model, settings, references, prompts, and attempt budget.
