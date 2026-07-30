# Gate 5 draft — Google Flow portability A/B

Status: **FAILED — PROMPT SUBMISSION MISMATCH; THREE INVALID TASKS**

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
- Upscaling: disabled for the initial A/B; any later upscale is a separate action
- Publication: not authorized by this gate

The Sky Mender is selected before any Flow output is generated. This prevents
case selection based on which result happens to look best.

## Source prompts

| Variant | Exact Prompt | SHA-256 | Bytes |
| --- | --- | --- | ---: |
| baseline | [`sky-mender/prompts/clip-02-baseline-frozen.txt`](sky-mender/prompts/clip-02-baseline-frozen.txt) | `065e32b4788d3e86faec7226b451f843227d6b32f0f941ddff73ee9161288e35` | 820 |
| ShotFlow v2 | [`sky-mender/prompts/clip-02-shotflow-v2.txt`](sky-mender/prompts/clip-02-shotflow-v2.txt) | `8b4654143c531b237c4797aac666a7cde70b9f184b5327c92f61fcc2b36b1201` | 2,371 |

These original Seedance prompts remain unchanged and are not submitted to Flow.

## Frozen Flow prompts

| Variant | Exact Prompt | SHA-256 | Bytes |
| --- | --- | --- | ---: |
| baseline Flow v1 | [`sky-mender/prompts/clip-02-baseline-flow-v1.txt`](sky-mender/prompts/clip-02-baseline-flow-v1.txt) | `7d3736086362cceadb7fdf565513ab9d75a2e03af313284e52522b3164f49970` | 822 |
| ShotFlow Flow v1 | [`sky-mender/prompts/clip-02-shotflow-flow-v1.txt`](sky-mender/prompts/clip-02-shotflow-flow-v1.txt) | `f6c444d462ca00d2103b4423fbd6a24d5e72dd847a0228df6c60cdaef095a2eb` | 2,402 |

The provider adaptation is deliberately narrow and symmetric:

1. Both variants begin with the exact same provider instruction:
   `GENERATE ONE CONTINUOUS EIGHT-SECOND CONTINUATION FROM THE PROVIDED FIRST FRAME.`
2. The baseline's conflicting five-second sentence is removed; all remaining
   visual decisions are byte-for-byte identical to its source prompt.
3. ShotFlow's video-and-final-frame opening is replaced by the same shared
   first-frame instruction; all remaining continuity-contract text is
   byte-for-byte identical to its source prompt.

If Flow rejects, rewrites, or silently changes either Prompt, stop and record
the provider-enforced change. Do not retry.

### Exact baseline Flow v1

```text
GENERATE ONE CONTINUOUS EIGHT-SECOND CONTINUATION FROM THE PROVIDED FIRST FRAME.

The same sky-repair worker in the red oilcloth cape swings screen-right on the taut safety cable, keeps the amber repair torch in the right hand, plants both boots on the outer rib, and drags the torch upward along the luminous fissure until the opening seals. Track closer beside the worker without crossing the tower axis. Keep the cable anchored lower-left, keep cold storm daylight from upper camera-left, and let the amber seam reflect on wet brass and cloth. The sealed sky opens into a restrained pale dawn behind the worker. Preserve the worker, cape shape, tower geography, screen direction, tool, cable tension, wet material response, and physically causal motion. No reset pose, no new tools, no cut, no orbit, no text, no logo.
```

### Exact ShotFlow Flow v1

```text
GENERATE ONE CONTINUOUS EIGHT-SECOND CONTINUATION FROM THE PROVIDED FIRST FRAME.

Required visible action:
- The worker regains tower contact, visibly seals the fissure with the amber repair light, and only then reveals a restrained dawn.
- Physical order: Continue from the real caught swing and complete the repair only after the worker regains physical contact.
- The final seconds must visibly prove the required action. Do not stop at setup.

Opening continuity locks — match before advancing the action:
- motion: The worker ends suspended almost horizontally away from the tower with residual screen-right motion blur. The cable is taut toward the lower frame rather than the planned lower-left anchor, the cape trails screen-right, and physical contact with the tower has not resumed.
- space: At the accepted endpoint the worker is fully screen-right of the bright vertical fissure and tower, not left of it. The tower occupies the left half of frame, open storm sky occupies the right, and the camera stays on the same exterior side.
- subject: One adult sky-repair worker remains visible as a dark segmented climbing silhouette with a long red cape; facial detail is indistinct at this distance.
- props and wardrobe: The red cape remains attached and trails away from the torso. An amber repair light remains visible in the hand nearest the tower. A thin safety cable exits the lower torso and continues out of frame; no equipment damage is clearly visible.
- light and material: Soft cold-gray storm light exposes the steel tower and clouds. The vertical fissure and handheld amber light add warm edge illumination to the worker; the steel remains dull and weathered rather than glossy.

Shot execution:
- camera: Track beside the real endpoint at matched speed; preserve the accepted camera side and avoid an axis-crossing orbit.
- composition: Preserve the worker-fissure-tower relationship and accepted screen direction; reveal dawn only behind the repaired seam.
- lighting: Retain the accepted storm source direction and material exposure; let the repaired seam motivate any warmer change.
- physics: Continue actual cable tension, cape drag, body inertia, wetness, and tool contact before allowing recovery.

Hard rule: continue the accepted action from its real endpoint. Do not reset pose, prop ownership, screen direction, lighting source, material state, or spatial geography.
```

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

The following values combine the authenticated Flow interface, the temporary
project setup, and current official Google documentation. No prompt was entered
and no generation was submitted:

| Field | Verified value |
| --- | --- |
| Account tier | `PRO` badge; full plan name not displayed |
| Pre-execution balance | `1,050` Google Flow credits |
| Active model | `Veo 3.1 - Quality` |
| Other visible models | `Omni Flash`, `Veo 3.1 - Lite`, `Veo 3.1 - Fast` |
| Feature mode | Direct `Video` → `Frames`; the accepted Clip 01 frame is attached to the start-frame slot and the end-frame slot is empty |
| First-frame-only submission support | Supported by the selected interface and listed for Veo 3.1 in the official model table; paid service submission is not yet exercised |
| Duration | `8 seconds` for `Veo 3.1 - Quality` according to the official credit table; the current interface did not expose a duration control |
| Aspect ratio | `16:9`; `9:16` is also visible |
| Output count | `x1`; `x2`, `x3`, and `x4` are also visible |
| Native output resolution | Not disclosed by the inspected interface or current official documentation; measure the downloaded source media after generation and make no advance native-resolution claim |
| Upscale setting and cost | Disabled for the initial A/B. Official documentation lists 1080p upscaling at `0` credits for Pro and 4K as unavailable to Pro; either remains a separate post-generation action requiring a new decision |
| Credits per submission | `100` at the inspected `Veo 3.1 - Quality` / `16:9` / `x1` combination |
| Total maximum credits | `200` for the two frozen submissions |
| Sufficient balance confirmed | `YES` at inspection time: `1,050 ≥ 200` |

Official settings sources:

- [Flow models and supported features](https://support.google.com/flow/answer/16352836)
- [Flow AI credits and video duration](https://support.google.com/flow/answer/16526234)
- [Flow access, model switching, and watermarking](https://support.google.com/flow/answer/16353333)
- [Google: Veo 3.1 reference consistency and 1080p/4K upscaling](https://blog.google/innovation-and-ai/technology/ai/veo-3-1-ingredients-to-video/)

## Temporary project evidence

- Project name: `ShotFlow Gate 5 Draft`
- Uploaded media: only
  [`sky-mender/artifacts/clip-01-final-frame.png`](sky-mender/artifacts/clip-01-final-frame.png)
- Uploaded SHA-256:
  `f05efcff94c047cdf46f681daf8996896e257ea3e9a6e54f1d36944b81bba1cd`
- Current role: start frame; end frame empty
- Current model: `Veo 3.1 - Quality`
- Current settings: `Video` → `Frames`, `16:9`, `x1`, displayed cost
  `100`
- Prompt field at temporary-setup completion: empty
- Submission state at temporary-setup completion: generate remained disabled;
  `0` credits consumed
- Persistence: the project name and uploaded media were auto-saved. The
  start-frame role did not persist after reopening the project, so it was
  rebound from the existing media library.
- Upload behavior: the interface briefly showed `99%` and a failed state, then
  completed automatically after approximately 15 seconds. No retry was issued.

Additional observations:

- Flow opened in agent mode with generation confirmation set to `Always`.
- The account panel showed visible watermarking as disabled. This does not
  override Google's documented watermark policy and does not establish whether
  SynthID is present.
- Current Google documentation says Flow outputs include invisible SynthID.
- No model was switched. Costs and compatibility for other models remain
  unverified.

## Resolved protocol conflict

The frozen baseline begins with:

> Continue immediately from the previous shot in one continuous five-second
> take.

The ShotFlow v2 prompt had no explicit duration. Submitting both source Prompts
unchanged to an eight-second provider would have exposed only the baseline to a
conflicting duration instruction. Flow v1 resolves that asymmetry with one
shared provider line and no other content changes.

## Paid execution outcome

The paid execution did not produce a valid baseline or ShotFlow comparison.
[The public-safe receipt](sky-mender/evidence/flow-gate-5-receipt.json) records
the following:

- Authorized maximum: two tasks and `200` credits
- Actual result: three independent tasks and `300` observed credits
- Balance: `1,050` before execution and `750` after execution
- Submitted internal Prompt for all three tasks: `G`
- Outputs: three videos exist, but all are invalid for the experiment
- ShotFlow Prompt: not submitted
- A/B scoring, effect claims, and showcase use: prohibited

Two `Enter` keystrokes intended to create the baseline Prompt's blank line were
interpreted by Flow as paid submissions. A later explicit Create action
submitted a third task. The editor visually presented more text than Flow's
internal submitted Prompt state retained. The two accidental tasks caused the
execution to exceed the authorized maximum by one task and `100` credits.

Only the third invalid output was downloaded to the ignored private evidence
directory. It is an unmodified H.264 video at 1280×720, 24 fps, and 8.000
seconds with SHA-256
`160defd544c8dd2a5bfe234e28b10adf4b47b2f4baabe2f85f645f4596fa2461`.
No invalid output is committed or published.

## Execution and stop rules for any future gate

1. Verify the two Flow Prompt hashes and shared-reference hash.
2. Display the completed settings table, both exact prompts, reference, fixed
   submission order, and maximum credit cost for explicit approval.
3. Submit the baseline first and ShotFlow second, one job at a time.
4. Record the active model, bound start frame, displayed cost, and balance again
   immediately before each submission because Flow may select a compatible
   model.
5. Stop on insufficient credits, a model switch, rejected prompt, missing
   reference, missing media, or any provider-enforced parameter change.
6. Do not retry, upscale, add outputs, or change parameters without a new
   decision.
7. Download and record the source media's actual resolution before any
   post-generation upscale decision.
8. Preserve SynthID and any visible AI disclosure.

Gate 5 is closed as an invalid execution. It must not be retried under the
existing approval. Any future Flow gate requires a new explicit credit
authorization and a Prompt-entry method that has been proven without paid
submission. Automated `Enter` input is prohibited.
