# Google Flow portability validation

Status: **FLOW PROMPTS FROZEN — PAID GENERATION NOT APPROVED**

After Gate 4 stopped for insufficient Xiaoyunque credits, the user clarified
that the Seedance queue must remain assigned to Xiaoyunque after its daily
credit refresh. Google Flow is assigned only additional cross-provider tasks.
The authenticated Flow interface showed a `PRO` badge, `1,050` credits,
`Veo 3.1 - Quality`, direct video frame mode, 16:9, one output, and `100`
credits per submission. A temporary project named `ShotFlow Gate 5 Draft` now
contains the accepted Clip 01 final frame in the start-frame role with the end
frame empty. The Prompt remains empty, generation stayed disabled, and no Flow
credits were consumed. A provider-specific eight-second Prompt pair is now
frozen in the repository, but it has not been entered into Flow.

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
- Google's current credit table specifies eight-second output for
  `Veo 3.1 - Quality`, while the Seedance experiment is fixed at five seconds.
- The current official credit table lists 1080p upscaling at zero credits for
  Pro and does not make 4K upscaling available to Pro. Upscaling remains a
  separate output action and is disabled for the initial A/B.
- The inspected interface and current official documentation do not disclose
  native base resolution. Record the downloaded source media before making any
  resolution claim.
- Preserve Google SynthID and any visible watermark required by account or
  region settings.

Official references:

- [Google Flow models and supported features](https://support.google.com/flow/answer/16352836)
- [Google Flow access, credits, model switching, and watermarking](https://support.google.com/flow/answer/16353333)
- [Google Flow credit cost, eight-second Quality output, and upscale cost](https://support.google.com/flow/answer/16526234)
- [Google: Veo 3.1 reference consistency and 1080p/4K upscaling](https://blog.google/innovation-and-ai/technology/ai/veo-3-1-ingredients-to-video/)

## Proposed closest portability test

1. Use the accepted Clip 01 final frame as the first frame.
2. Use only the reference assets supported by the selected Flow model.
3. Use the frozen Flow-specific pair, which applies the same eight-second
   first-frame instruction to both variants and leaves each variant's remaining
   visual or continuity decisions unchanged.
4. Use the same Flow model, aspect ratio, duration, output count, and references
   for both variants.
5. Record any provider-enforced prompt, model, duration, or resolution change.
6. Score with the same six continuity dimensions, but report it separately from
   the Seedance aggregate.

Before any Flow credit is consumed, review the Flow-specific eight-second
Prompt pair and hashes displayed in full in Gate 5. A current authenticated Flow
screen must then reconfirm the active model, bound start frame, feature mode,
displayed credit cost and balance, aspect ratio, output count, and absence of
upscale. The fixed order is baseline first and ShotFlow second, with a maximum
of two submissions and no automatic retry.
