# Gate 5 draft — Google Flow portability A/B

Status: **DRAFT — PARTIALLY VERIFIED; DURATION AND OUTPUT SETTINGS PENDING**

This is an additional cross-provider test. It does not replace, complete, or
enter the aggregate for the Xiaoyunque / Seedance Gate 4 experiment.

## Pre-registered case and workload

- Case: The Sky Mender
- Provider surface: Google Flow
- Variants: frozen baseline and ShotFlow v2
- Required new outputs: `2`
- Output count per submission: `1`
- Maximum submissions: `2`
- Automatic retry: disabled
- Model switching: disabled unless disclosed by Flow before submission
- Upscaling: disabled unless separately frozen below
- Publication: not authorized by this gate

The Sky Mender is selected before any Flow output is generated. This prevents
case selection based on which result happens to look best.

## Frozen prompts

| Variant | Exact Prompt | SHA-256 | Bytes |
| --- | --- | --- | ---: |
| baseline | [`sky-mender/prompts/clip-02-baseline-frozen.txt`](sky-mender/prompts/clip-02-baseline-frozen.txt) | `065e32b4788d3e86faec7226b451f843227d6b32f0f941ddff73ee9161288e35` | 820 |
| ShotFlow v2 | [`sky-mender/prompts/clip-02-shotflow-v2.txt`](sky-mender/prompts/clip-02-shotflow-v2.txt) | `8b4654143c531b237c4797aac666a7cde70b9f184b5327c92f61fcc2b36b1201` | 2,371 |

The texts must be submitted unchanged. If Flow rejects or rewrites either
prompt, stop and record the provider-enforced change before any retry.

## Frozen shared reference

Both variants use the same accepted Clip 01 final frame in the same reference
role:

| Role | File | SHA-256 | Bytes |
| --- | --- | --- | ---: |
| first frame | [`sky-mender/artifacts/clip-01-final-frame.png`](sky-mender/artifacts/clip-01-final-frame.png) | `f05efcff94c047cdf46f681daf8996896e257ea3e9a6e54f1d36944b81bba1cd` | 1,099,668 |

The accepted Clip 01 video is intentionally not included unless the live Flow
mode supports the same video reference role for both variants. This makes Gate
5 a first-frame portability test, not a video-to-video comparison.

## Live settings

The following values were read from the authenticated Flow interface without
creating a project, uploading media, entering a prompt, or submitting a
generation:

| Field | Verified value |
| --- | --- |
| Account tier | `PRO` badge; full plan name not displayed |
| Current balance | `1,050` Google Flow credits |
| Active model | `Veo 3.1 - Quality` |
| Other visible models | `Omni Flash`, `Veo 3.1 - Lite`, `Veo 3.1 - Fast` |
| Feature mode | Direct `Video` → `Frames`; separate start and end frame slots are visible |
| First-frame-only submission support | `PENDING` — not tested because no media or prompt was entered |
| Duration | `PENDING` |
| Aspect ratio | `16:9`; `9:16` is also visible |
| Output count | `x1`; `x2`, `x3`, and `x4` are also visible |
| Native output resolution | `PENDING` |
| Upscale setting and cost | `PENDING` |
| Credits per submission | `100` at the inspected `Veo 3.1 - Quality` / `16:9` / `x1` combination |
| Total maximum credits | `200` for the two frozen submissions |
| Sufficient balance confirmed | `YES` at inspection time: `1,050 ≥ 200` |

Additional read-only observations:

- Flow opened in agent mode with generation confirmation set to `Always`.
- The account panel showed visible watermarking as disabled. This does not
  establish whether SynthID is present.
- Existing video detail pages remained loading and the browser connection later
  interrupted, so duration, native resolution, and upscale could not be
  evidenced safely.
- No model was switched. Costs and compatibility for other models remain
  unverified.

## Execution and stop rules

1. Verify that both jobs can use the same model, first-frame role, duration,
   aspect ratio, resolution, and output count.
2. Display the completed settings table, two exact prompts, reference, and
   maximum credit cost for explicit approval.
3. Submit one job at a time.
4. Record the active model and displayed cost again immediately before each
   submission because Flow may select a compatible model.
5. Stop on insufficient credits, a model switch, rejected prompt, missing
   reference, missing media, or any provider-enforced parameter change.
6. Do not retry, upscale, add outputs, or change parameters without a new
   decision.
7. Preserve SynthID and any visible AI disclosure.

Gate 5 is not approved while any live setting remains `PENDING`. The inspected
balance and credit cost must also be rechecked immediately before approval.
