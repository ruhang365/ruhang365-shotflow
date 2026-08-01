# Gate 7 — Obsidian Bloom v0.3 RC1

Status: **FROZEN — NOT AUTHORIZED FOR GENERATION**

Gate 7 tests whether the causal change budget fixes the failure recorded under
Gate 6. It is a new pre-registered mechanism test, not a retry of the rejected
`anchor-frame-v1` result. Historical evidence remains unchanged.

## Fixed provider conditions

- Platform: Lovart
- Model tool: `generate_video_seedance_v2_0` (standard Seedance 2.0)
- Reasoning mode: `thinking`
- Ratio and duration: 16:9, 5 seconds
- Reference profile: `anchor-frame-v2`
- Media reference: the same accepted Clip 01 final frame only
- Output eligibility: both variants must have the same native resolution and
  both must be at least 1280×720
- Attempts: baseline once, ShotFlow v0.3 once; maximum two jobs
- Stop rules: no retry, upscale, downgrade, model switch, provider switch, or
  automatic confirmation

Lovart must show the current credit amount before either job is confirmed. A
new explicit user confirmation is required after the exact amount is visible.

## Frozen inputs

| Input | SHA-256 |
| --- | --- |
| [Public JPEG preview of accepted frame](obsidian-bloom/evidence/clip-01-final-frame.jpg) | Authoritative local PNG hash in both handoffs: `56d6455da0310b8acce2364af99229825307b70bae8f677306496c1fa08e8a0e` |
| [Baseline creative Prompt](obsidian-bloom/prompts/clip-02-baseline-frozen.txt) | `5b0cd96768dfd861ddd790d05de78f91c100242cb8975f7dca4a117fb19d1884` |
| [v0.3 creative Prompt](obsidian-bloom/prompts/clip-02-shotflow-v4-rc1.txt) | `e6b1186422b6422fd5048f1ee3bff4aad1f6b87cac0a68fe27068cf24c2f3cad` |
| [Ordered Sequence 1.1](obsidian-bloom/plan/clip-02-sequence-v4.json) | `fc86ff2b80c976229436769301645830bb87cf4d6eb977b9fccb2a8c08627d46` |
| [Five-axis grammar](obsidian-bloom/plan/clip-02-grammar-v4.json) | `de12b88ef8f81a9ec4f6381989857faddd160ad7e6f107732a3ac24f3dd86ef5` |
| [Baseline handoff](obsidian-bloom/evidence/provider-handoff-baseline-v03-gate7.json) | `cf5eea04570bd6f6a29786e15925ad9025ed18286abc48e9b57f136f01dbcc8c` |
| [v0.3 handoff](obsidian-bloom/evidence/provider-handoff-shotflow-v4-rc1-gate7.json) | `e551e3cf37ba7a0a651b53473881a1d8b855c416c363abd9b67727b0020d6581` |

The exact submission Prompt is stored inside each handoff together with its own
hash. Attachment 1 is the authoritative accepted endpoint in both jobs.

## Decision rule

Three vision-capable reviewers score neutral outputs on the six public
continuity dimensions. Gate 7 passes only if at least two of three prefer the
v0.3 variant. A loss, tie without majority, invalid pair, or failed job closes
Gate 7 and blocks Gate 8 without another attempt.
