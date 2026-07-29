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
