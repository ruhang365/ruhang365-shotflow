# Obsidian Bloom ShotFlow — anchor-frame-v1

Status: **CLOSED — GENERATED ONCE; REJECTED BY UNANIMOUS BLIND REVIEW**

This is the separately registered ShotFlow half of the A/B test. The baseline
produced one accepted 1920×1080 artifact and passed the opening-frame binding
gate. Baseline approval never authorizes this job.

## Frozen one-job scope

- Platform: Lovart
- Model tool: `generate_video_seedance_v2_0`
- Display model: Seedance 2.0
- Lovart reasoning mode: `thinking`
- Ratio: `16:9`
- Resolution request: `provider-native` (no Lovart selector is exposed)
- Minimum accepted raster: `1280×720`
- Duration: `5` seconds
- Variant: `clip-02-shotflow`
- Provider Handoff profile: `anchor-frame-v1`
- New submissions after a later explicit approval: `1`
- Automatic retry, recharge, fallback, upscale, or publication: `none`
- Evidence state before generation: `verified=false`

## A/B lock

Use the same platform, standard model tool, reasoning mode, ratio, duration,
measured raster, and sole final-frame reference as the accepted baseline run.
Do not use Seedance 2.0 Fast or Mini. The only intended experimental variable
is whether the creative Prompt follows the pre-frozen plan or the accepted
observed state.

| Order | Role | SHA-256 |
| --- | --- | --- |
| 1 | Authoritative accepted final frame | `56d6455da0310b8acce2364af99229825307b70bae8f677306496c1fa08e8a0e` |

## Frozen Prompt and manifest

- Anchor creative Prompt: [`obsidian-bloom/prompts/clip-02-shotflow-anchor-creative-v1.txt`](obsidian-bloom/prompts/clip-02-shotflow-anchor-creative-v1.txt)
- Creative Prompt SHA-256: `b1077b7e9ed15dc651680089dbf3031b6d37c02f73c2d2e8aadb96c5da263354`
- Exact submission Prompt: [`obsidian-bloom/prompts/clip-02-shotflow-anchor-v1.txt`](obsidian-bloom/prompts/clip-02-shotflow-anchor-v1.txt)
- Submission Prompt SHA-256: `ac68c50fa66334579184ed9ef570a8471efafb94a5fefee95a3f5bf76cc16821`
- Provider Handoff: [`obsidian-bloom/evidence/provider-handoff-shotflow-anchor-v1.json`](obsidian-bloom/evidence/provider-handoff-shotflow-anchor-v1.json)
- Handoff SHA-256: `a085fcb4c471e52d99ae3161292d863f95922a38e4b9902a09963e08cb0feb7d`

The provider submission Prompt must be copied unchanged from the frozen file.
Its first line was adapted from the historical video-plus-frame v2 Prompt to
refer only to the provided final frame; all observed continuity facts, action,
cinematic grammar, and ending proof remain unchanged.

## Stop conditions

- Do not submit if the baseline is below 1280×720 or fails opening-frame
  binding.
- Reject the pair as an invalid A/B if the two actual rasters differ.
- Require exactly one new video SHA-256.
- Reject any opening reset before scoring later continuity or story progression.
- Do not retry, upscale, switch models, or publish under this gate.
- Require a separate explicit approval immediately before submission.

## Execution receipt

- User approval: explicit
- Provider run identifiers: anonymized and retained outside the public repository
- New submissions: `1`
- Premium credit confirmation: not returned
- Output: `1920×1080`, H.264, 24fps, `5.061950` seconds
- Video SHA-256: `4d879f234e3f20e413061a9ad5a266dbb7e7f3e8208de3901a74343bab7dfd45`
- Opening-frame SSIM: `0.833104`
- Container AIGC label: absent; visible disclosure is required for any public derivative
- Retry, fallback, upscale, publication: none

The job passed the hard raster and opening-frame gates, then failed content
acceptance. In the blinded pair it was Variant A. Claude Opus 4.8, Gemini 3.6
Flash High, and an independent Codex GPT-5.6 reviewer unanimously selected
Variant B, the baseline. ShotFlow averaged `3.33/12`; the baseline averaged
`9.67/12`.

The cap hinged sideways, the exterior droplet fell to the lower surface, and
the amber ribbon connected to the bottle base/liquid surface and crossed the
bottle body. These are P0 violations of the frozen causal contract. Attempt
`obsidian-bloom-003` is therefore rejected and this gate permits no retry.

See the [blind review](obsidian-bloom/reviews/clip-02-blind-review-anchor-v1.md).
