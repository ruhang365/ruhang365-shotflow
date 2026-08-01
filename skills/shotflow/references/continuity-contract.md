# Continuity contract

## Authority order

1. Accepted observed state
2. User-fixed facts not contradicted by the accepted result
3. Current story beat
4. Planned state

Observed state wins whenever planned and observed state disagree.

## Complete observation

Record:

- identity: visible face, body, silhouette, age cues, and stable identifiers;
- wardrobe_props: clothing state, damage, prop appearance, ownership, and hand;
- space_direction: subject position, screen direction, landmarks, depth, and camera side;
- motion: pose, velocity, open action, balance, and physical forces;
- light_material: source direction, exposure, weather, surface state, and deformation;
- story_beat: what visibly completed and what remains unresolved.

Record facts, not intentions. Include defects that remain in the accepted clip.

## Open-motion handoff

Prefer an endpoint with unfinished causal energy:

- a cable becomes taut;
- a hand reaches but has not grasped;
- a door is still moving;
- a body crosses the frame edge;
- an object begins to fall.

Start the next shot by continuing that exact action. Do not reset the subject into a neutral pose.

## Provider-facing prompt

Keep the complete observed state in the JSON contract for audit. Render the
provider-facing prompt with the `provider-direct-v3` profile. Give it exactly
five timed visible states in this order:

1. `match`: reproduce the accepted endpoint as the opening state;
2. `continue`: carry the unresolved observed motion or force forward;
3. `initiate`: make the new action's cause visibly occur;
4. `resolve`: make the required effect visibly complete;
5. `hold`: hold the final proof long enough to evaluate.

Write every checkpoint, compact anchor, beat, and grammar decision as a
positive visible state. The compiler rejects negative directives such as
`do not`, `must not`, `avoid`, and `without`. Translate them into the state that
should be visible instead.

Give every checkpoint a `visual_test` in the Ordered Sequence JSON. Keep those
tests and the complete observation in the contract for human or Pro evaluation;
send only the five checkpoint states and compact anchors to the provider. This
keeps the creative Prompt shorter than the evidence contract.

The five time ranges must be contiguous, begin at zero, and end at the provider
duration. Keep `match` brief, give the causal action enough time in `initiate`
and `resolve`, and reserve a visible final hold.

## Fair A/B comparison

- Freeze the baseline next-shot prompt before Clip 01 generation.
- Use the same accepted Clip 01, final frame, model, duration, ratio, resolution, and references for both variants.
- Change only whether the next-shot prompt incorporates the accepted observation.
- Preserve failed results and attempt counts.
- Blind the variant labels during scoring.

## Six-dimension rubric

Use `0`, `1`, `2`, or `n/a` for:

1. subject_identity
2. wardrobe_props
3. space_direction
4. motion_handoff
5. light_material
6. story_beat

A continuity claim requires evidence across the applicable dimensions, not a visually attractive single frame.
