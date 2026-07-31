# Google Flow portability validation

Status: **GATE 5 INVALID — BROWSER PROMPT INPUT STILL UNSAFE**

After Gate 4 stopped for insufficient Xiaoyunque credits, the user clarified
that the Seedance queue must remain assigned to Xiaoyunque after its daily
credit refresh. Google Flow is assigned only additional cross-provider tasks.
The authenticated Flow interface showed a `PRO` badge, `1,050` credits,
`Veo 3.1 - Quality`, direct video frame mode, 16:9, one output, and `100`
credits per submission. A temporary project named `ShotFlow Gate 5 Draft` now
contains the accepted Clip 01 final frame in the start-frame role with the end
frame empty. A provider-specific eight-second Prompt pair was frozen, but the
paid execution failed to submit that text correctly.

Flow created three independent tasks whose internal Prompt was only `G`. Two
were triggered when automated `Enter` input intended to create a blank line was
interpreted as submission; a third was triggered by the explicit Create action.
All three produced videos, but none is valid baseline or ShotFlow evidence. The
balance fell from `1,050` to `750`, an observed cost of `300` credits against an
authorized maximum of `200`. ShotFlow was not submitted. See the
[public-safe attempt ledger](sky-mender/evidence/flow-gate-5-attempts.json).

## Provider allocation policy

- Work already started as a Xiaoyunque / Seedance experiment remains on
  Xiaoyunque so its model, duration, resolution, references, and comparison
  contract do not change mid-experiment.
- New work may combine Xiaoyunque and Google Flow when each provider has a
  pre-registered role. Results remain provider-specific and are never pooled as
  if they came from one controlled experiment.
- Xiaoyunque remains appropriate for the retained Seedance VIP / 1080p queue.
  Flow may handle new eight-second portability, exploration, or supplementary
  shots after its Prompt is entered safely.
- Every credit-consuming provider run still requires its own exact Prompt,
  model, settings, references, attempt budget, and explicit approval.

## Zero-credit Browser input canary

On 2026-07-31, Browser plugin `26.727.40816` was tested with the single-line
canary `SHOTFLOW_INPUT_CANARY_20260731_NO_SUBMIT`. No `Enter` key or Create
action was used.

- Input method: Browser Playwright `locator.fill()`
- Result: failed
- Failure mode: the canary was written into a Slate zero-width placeholder
  node, while Flow retained its Prompt placeholder and kept Create disabled
- Balance: `750` before and after
- Independent video tasks: `3` before and after
- New submissions and credit consumption: `0`

This reproduces the underlying incompatibility without spending credits. The
current Browser `fill()` path changes DOM content but does not update Flow's
Slate/React editor state. Until a later canary passes, Codex Browser may inspect
settings, attach approved media, monitor results, download outputs, and record
evidence, but it must not enter paid Flow Prompts.

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

Gate 5 demonstrated that those preflight checks are insufficient for Flow's
Slate-based editor: DOM-visible text did not prove the internal submitted
Prompt. Any future gate must first prove Prompt entry without a paid submission,
must not use automated `Enter`, and requires a new explicit credit approval.
The current safe fallback is native user paste with no `Enter`, followed by
user-controlled Create; Codex may resume monitoring only after submission.
