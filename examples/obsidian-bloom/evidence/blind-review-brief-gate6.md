# Obsidian Bloom Gate 6 Blind A/B Review Brief

Act as an independent, read-only continuity reviewer. Do not infer which workflow produced either variant. Continuity and causal correctness take priority over surface beauty.

## Media

- Accepted Clip 01 final frame: `<controller-temp>/reference.png`
- Variant A contact sheet: `<controller-temp>/variant-a-contact.png`
- Variant A video: `<controller-temp>/variant-a.mp4`
- Variant B contact sheet: `<controller-temp>/variant-b-contact.png`
- Variant B video: `<controller-temp>/variant-b.mp4`

The controller supplies these neutral temporary files. Provider run identifiers
and machine-specific temporary paths are not part of the review input.

Inspect the reference and both variants visually. The contact sheets contain one frame per second in chronological order. Inspect the videos too if your environment supports local video reading. If you cannot directly inspect at least the reference and both contact sheets, return `INVALID_NO_VISUAL_ACCESS` and do not guess.

## Frozen target beat

1. The first frame must continue from the accepted final frame: same bottle identity, cap position, camera, horizon, light, material, and the exterior droplet.
2. The black cap rises vertically by more than 1 cm. It must not tilt, hinge, morph, or move sideways.
3. Only after the cap opens, one thin amber vapor ribbon emerges from the exposed neck.
4. The ribbon makes one clean clockwise orbit around the neck. It must not emerge from, attach to, or travel through the bottle body, bottle base, exterior droplet, or liquid surface.
5. The final state keeps the cap hovering, the bottle centered and stable, and the original premium dark-glass material and studio lighting.

## Scoring

Score each dimension from 0 to 2, for a maximum of 12:

- Subject identity
- Product parts and exterior droplet
- Space, camera, and direction
- Motion handoff and causal order
- Light, material, and physics
- Story beat completion

Choose the better continuity result. A tie is allowed. Do not reward a more dramatic image if it violates the frozen beat.

Return exactly these sections:

Conclusion: VALID_VISUAL_REVIEW or INVALID_NO_VISUAL_ACCESS
Variant A: six named scores and total
Variant B: six named scores and total
Winner: A, B, or Tie
P0: continuity-breaking observations
P1: important quality observations
P2: minor observations
Keep: what should be preserved
Change: what should change
Final principles: one concise decision rule
