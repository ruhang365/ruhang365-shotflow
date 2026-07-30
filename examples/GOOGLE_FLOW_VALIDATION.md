# Google Flow portability validation

Status: **ADDITIONAL VALIDATION REQUESTED — LIVE SETTINGS PARTIALLY VERIFIED**

After Gate 4 stopped for insufficient Xiaoyunque credits, the user clarified
that the Seedance queue must remain assigned to Xiaoyunque after its daily
credit refresh. Google Flow is assigned only additional cross-provider tasks.
The authenticated Flow interface currently shows a `PRO` badge, `1,050`
credits, `Veo 3.1 - Quality`, direct video frame mode, 16:9, one output, and
`100` credits per submission. Duration, native resolution, upscale, and
first-frame-only submission support remain unverified. No Flow output has been
generated for this repository.

## Role in ShotFlow evidence

Google Flow is an additional cross-provider portability check, not a
continuation or replacement of the Seedance Gate 4 A/B. Its model, duration
contract, and supported reference roles differ, so Flow results cannot be
pooled into the Seedance aggregate or used to rewrite the paused Gate 4
outcome.

The first Flow case will be selected before seeing any Flow output. A separate
Flow protocol must be frozen before generation and its results must be labelled
as cross-provider evidence. The pre-registered two-output draft is
[Gate 5](GATE_5_GOOGLE_FLOW_APPROVAL.md).

## Current official constraints

- Flow exposes multiple video models and may switch to a compatible model when
  a selected feature is unsupported. Record the active model and displayed
  credit cost immediately before every generation.
- Veo 3.1 feature support differs by tier. Reference/ingredient workflows and
  first-frame workflows do not share one universal duration contract.
- Flow currently documents 4, 6, 8, and in some modes 10-second generation,
  while the Seedance experiment is fixed at five seconds.
- Veo 3.1 supports 1080p and 4K upscaling in Flow, but upscaling is a separate
  output property and must be recorded.
- Preserve Google SynthID and any visible watermark required by account or
  region settings.

Official references:

- [Google Flow models and supported features](https://support.google.com/flow/answer/16352836)
- [Google Flow access, credits, model switching, and watermarking](https://support.google.com/flow/answer/16353333)
- [Google: Veo 3.1 reference consistency and 1080p/4K upscaling](https://blog.google/innovation-and-ai/technology/ai/veo-3-1-ingredients-to-video/)

## Proposed closest portability test

1. Use the accepted Clip 01 final frame as the first frame.
2. Use only the reference assets supported by the selected Flow model.
3. Keep the baseline and ShotFlow prompt texts frozen and unchanged.
4. Use the same Flow model, aspect ratio, duration, output count, and references
   for both variants.
5. Record any provider-enforced prompt, model, duration, or resolution change.
6. Score with the same six continuity dimensions, but report it separately from
   the Seedance aggregate.

Before any Flow credit is consumed, a current authenticated Flow screen must
confirm the active model, feature mode, displayed credit cost and balance,
duration, aspect ratio, resolution or upscale setting, and supported reference
roles. A new gate must then freeze those values, the two exact prompts, and the
maximum attempt budget for explicit approval.
