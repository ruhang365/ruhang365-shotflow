# Storm Deck targeted baseline retry

Status: **CLOSED — RETRY REJECTED; ATTEMPT CAP REACHED**

This gate replaces the rejected Lovart runs. The Kling O1 result advanced too
little; the first Lovart-routed Seedance 2.0 result started from an empty frame
and moved the case to the wrong side. The explicitly approved retry completed,
but repeated the same opening break and returned 720p instead of 1080p.

## Recorded outcome

- Attempt: `storm-deck-005`
- Submission Prompt SHA-256: `51563429cb54ea55b0673504935ce6edda29dcdce54601448b12b4c75bb63fac`
- New video SHA-256: `35c1d96474d8a95b9bf83db7db2a7fa48b11b1fc7e0be514dde1100d10a6f256`
- Actual media: 1280×720, 24fps, 5.061950 seconds
- Opening-frame review: `rejected`
- Continuity-safe: `false`
- Retry, upscale, or fallback performed: `none`

The provider acknowledged the attachment roles in text, but the actual first
frame again omitted the worker and moved the case to the far left. The retry
was visually very close to the previous failed result after resolution
normalization (`SSIM All=0.928347`). Media evidence overrides the provider's
success message. The fifth registered Storm Deck attempt closes this gate.

## Approved one-job budget

- Platform: Lovart
- Model tool: `generate_video_seedance_v2_0`
- Display model: Seedance 2.0
- Lovart reasoning mode: `thinking`
- Ratio: `16:9`
- Requested resolution: `1080p`
- Duration: `5` seconds
- Variant: `clip-02-baseline`
- New submissions: `1`
- Automatic retry, recharge, model fallback, upscale, or publication: `none`
- Evidence state before and after this run: `verified=false`

Lovart did not return a credit confirmation for the previous Seedance 2.0 run.
If it returns one for this retry, stop and show the exact cost before confirming.

## Reference roles

The [Provider Handoff manifest](storm-deck/evidence/provider-handoff.json) fixes
the attachment roles for both future A/B variants:

| Order | Role | SHA-256 |
| --- | --- | --- |
| 1 | Authoritative accepted final frame | `5b32eb1a7519d543be037cf86c8e2079803d8f9a7be99174184c691c4faec5f6` |
| 2 | Accepted source video, motion context only | `d7e36d9b270a3f9280dca19d50afe856177c3426e1a12a0b3511dbc811a2a198` |

The first generated frame must match attachment 1 before the action advances.
The provider must not restart from attachment 2's opening or insert an empty
establishing frame.

## Frozen creative Prompt

Path: [`storm-deck/prompts/clip-02-baseline-frozen.txt`](storm-deck/prompts/clip-02-baseline-frozen.txt)

SHA-256: `3d7e34a97bf97aaad1131deccaf9200603fd7ca56c729669b67bbddd5cc777fb`

The creative Prompt remains unchanged. Lovart receives the exact provider
submission Prompt below so the reference roles are explicit.

## Exact provider submission Prompt

SHA-256: `51563429cb54ea55b0673504935ce6edda29dcdce54601448b12b4c75bb63fac`

```text
REFERENCE BINDING — APPLY BEFORE THE CREATIVE INSTRUCTIONS:
- Attachment 1 is the authoritative opening frame from the accepted previous shot. The first generated frame must match its subject, prop placement, pose, camera side, and spatial geography before the action advances.
- Attachment 2 is the accepted previous-shot video. Use it only for identity, material, lighting, and incoming-motion context; do not restart from its opening or insert an empty establishing frame.
- If the two references appear to conflict, Attachment 1 wins because it is the observed endpoint.

CREATIVE INSTRUCTIONS — KEEP UNCHANGED:
Continue immediately from the previous shot in one continuous five-second take. The same rescue worker in the yellow storm suit keeps the left hand on the red emergency case's black strap while both continue sliding screen-right. The taut safety line arrests the worker first; the case pivots around the caught strap, stops short of the railing, and the worker pulls it back toward the fixed blue container row. Keep the worker on the right knee until the case changes direction. Keep both silver latches, the plain white helmet, upper-left safety anchor, downhill water flow, overhead blue work lights, and the same camera side. End as the worker secures the case against a deck cleat and its small green status beacon activates. Real inertia, friction, rain, line tension, and hand contact; no reset pose, no prop duplication, no cut, no orbit, no text, no real company markings.
```

## Artifact and acceptance rules

- Ignore every returned artifact whose SHA-256 is already in the handoff manifest.
- Require exactly one new video hash after the task completes.
- Extract the actual first frame and compare it with attachment 1.
- Reject the result if subject, case position, pose, camera side, or spatial
  geography jumps, even if later frames look strong.
- Do not submit the ShotFlow variant under this approval.
- Do not retry Storm Deck without a new mechanism and a new registered cap.
