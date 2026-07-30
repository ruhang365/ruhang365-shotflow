# Google Flow portability validation

Status: **PLANNED — NOT AN APPROVED GENERATION GATE**

The user has reported access to Google Flow and prior use. No current account,
credit balance, model selection, or output has been verified for this
repository.

## Role in ShotFlow evidence

Google Flow is a second-stage portability check, not a replacement for the
Seedance Gate 4 A/B. Mixing Flow into the current five paid jobs would change
both the prompt mechanism and provider, so any result could not be attributed
to ShotFlow.

After Gate 4 is complete, select one case without cherry-picking based on Flow
output. Freeze a separate Flow protocol before generation and label its result
as cross-provider evidence.

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

Before any Flow credit is consumed, a new gate must show the exact active model,
displayed credit cost, duration, aspect ratio, reference roles, two prompts, and
maximum attempts.
