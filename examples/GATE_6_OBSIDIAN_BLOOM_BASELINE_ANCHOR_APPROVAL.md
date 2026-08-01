# Obsidian Bloom baseline — anchor-frame-v1

Status: **CLOSED — BASELINE ACCEPTED; SHOTFLOW APPROVAL PENDING**

This gate registered one quality-first provider test. The approved job completed
without a Premium confirmation and no retry, upscale, publication, or model
switch was performed.

## Recorded outcome

- Attempt: `obsidian-bloom-002`
- Model tool: `generate_video_seedance_v2_0`
- Submission Prompt SHA-256: `a57845e028ee38f9a20ac77943f332a68c97c01f83b6267e1f576bcf26bdc67f`
- New video SHA-256: `a9f996fbeb577146fef8e0873d13d1b323f83b02be07b04d35afedf08211cf50`
- Actual media: 1920×1080, 24fps, 5.041667 seconds
- Opening-frame review: `accepted`
- Opening-frame SSIM against the accepted endpoint: `0.835808`
- Required ending action: `present` — cap opens, amber vapor appears, and the
  exterior droplet descends
- Premium confirmation returned: `none`
- Container-level AIGC label: `absent`; any public derivative must add a visible
  Lovart / Seedance 2.0 disclosure
- Retry, upscale, fallback, or publication performed: `none`

The generated first frame preserves the accepted bottle, rounded black cap,
silver collar, exterior amber droplet, camera side, hovering position, liquid
horizon, lighting, and material state. It does not insert an empty establishing
frame. The baseline is valid for the registered A/B; this is not evidence that
ShotFlow improves continuity.

Known deviations remain for blinded scoring: the cap rises visibly farther
than the requested one centimeter, and the silver petal ring's final placement
fully behind the collar is ambiguous. These do not invalidate the artifact as
the pre-registered baseline, but they prevent a perfect prompt-fidelity score.

## Frozen one-job scope

- Platform: Lovart
- Model tool: `generate_video_seedance_v2_0`
- Display model: Seedance 2.0
- Lovart reasoning mode: `thinking`
- Ratio: `16:9`
- Resolution request: `provider-native` (no Lovart selector is exposed)
- Minimum accepted raster: `1280×720`
- Duration: `5` seconds
- Variant: `clip-02-baseline`
- Provider Handoff profile: `anchor-frame-v1`
- New submissions performed: `1`
- Automatic retry, recharge, fallback, upscale, or publication: `none`
- Evidence state before generation: `verified=false`

## Quality decision

The Lovart model preference UI exposes Seedance 2.0, Seedance 2.0 Fast, and
Seedance 2.0 Mini, but no resolution selector. For this quality-first run, keep
the standard Seedance 2.0 model and hard-bind
`generate_video_seedance_v2_0`. Do not switch to Fast or Mini, and do not allow
automatic model fallback.

Accept the provider's native output only when it is at least 1280×720. Record
the measured raster, frame rate, duration, and SHA-256. Do not upscale. The
ShotFlow variant must later use the same model path and produce the same raster,
or the pair is not a valid A/B comparison.

## Read-only capability audit — 2026-08-01

- The installed official Lovart Skill v1.0.11 lists
  `generate_video_seedance_v2_0`, but exposes no command that returns its native
  resolution matrix.
- The current account is in unlimited mode. The live unlimited-model response
  does not include Seedance 2.0, so this path remains Premium and may require a
  separate credit confirmation.
- A no-generation question to the Lovart Agent returned a text-only refusal to
  enumerate the internal tool schema. No new media task or credit confirmation
  was created.
- The latest existing Lovart-routed Seedance 2.0 artifact was downloaded again
  through the official Skill and matched the registered SHA-256
  `35c1d96474d8a95b9bf83db7db2a7fa48b11b1fc7e0be514dde1100d10a6f256`.
  Its measured media remains 1280×720, 24fps, 5.061950 seconds.

Conclusion: native 1920×1080 support is unavailable as a selectable contract in
the current UI. The experiment therefore uses provider-native output with a
1280×720 minimum and reports the actual raster instead of claiming 1080p.

## Sole reference

Only the accepted Clip 01 final frame is attached. The source video is
intentionally withheld so a generic attachment interface cannot restart it or
misinterpret its opening as the continuation point.

| Order | Role | SHA-256 |
| --- | --- | --- |
| 1 | Authoritative accepted final frame | `56d6455da0310b8acce2364af99229825307b70bae8f677306496c1fa08e8a0e` |

The actual first generated frame must match the bottle identity, cap and collar
geometry, exterior droplet, near-frontal camera side, hovering position, liquid
horizon, reflections, and material state before the action advances.

## Frozen Prompt and manifest

- Creative Prompt: [`obsidian-bloom/prompts/clip-02-baseline-frozen.txt`](obsidian-bloom/prompts/clip-02-baseline-frozen.txt)
- Creative Prompt SHA-256: `5b0cd96768dfd861ddd790d05de78f91c100242cb8975f7dca4a117fb19d1884`
- Exact submission Prompt: [`obsidian-bloom/prompts/clip-02-baseline-anchor-v1.txt`](obsidian-bloom/prompts/clip-02-baseline-anchor-v1.txt)
- Submission Prompt SHA-256: `a57845e028ee38f9a20ac77943f332a68c97c01f83b6267e1f576bcf26bdc67f`
- Provider Handoff: [`obsidian-bloom/evidence/provider-handoff-baseline-anchor-v1.json`](obsidian-bloom/evidence/provider-handoff-baseline-anchor-v1.json)
- Handoff SHA-256: `49b20665c3b4e4a96bc8420e577a1ad3a898f986eee1b4856261496d4ed3094b`

The provider submission Prompt must be copied unchanged from the frozen file.

## Acceptance rules

- Require exactly one new video SHA-256.
- Verify the media is at least 1280×720 and record its actual raster before
  creative review.
- Extract and manually review the actual first frame against attachment 1.
- Reject any opening reset, geometry change, extra bottle, camera-side jump, or
  liquid-plane jump even if later frames look attractive.
- Preserve the result and receipt whether accepted or rejected.
- Do not submit the ShotFlow variant under this gate.

This baseline gate is closed. Do not retry it. The ShotFlow variant requires a
separate explicit approval under its own gate.
