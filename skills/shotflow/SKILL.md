---
name: shotflow
description: Plan and continue multi-shot AI video sequences from accepted real outputs instead of planned prompts. Use when creating Clip 01/Clip 02 sequences, repairing character or prop drift, preserving screen direction and open motion, compiling a next-shot prompt from a final frame or video, running a fair continuity A/B test, or scoring an AI video sequence across identity, wardrobe/props, space, motion, light/material, and story beat.
---

# ShotFlow

Turn an accepted AI video shot into an authoritative continuity state, then compile the next shot from what actually happened.

## Workflow

1. Create or open a ShotFlow project.
2. Plan only the current shot. Record all five grammar axes.
3. Freeze any baseline next-shot prompt before generating the current shot.
4. Generate the current shot with the user's approved provider workflow.
5. Accept one result and record its real video, final frame, and complete observation.
6. Compare planned and observed state. Treat observed state as authoritative.
7. Compile the next shot from the accepted observation.
8. Generate baseline and ShotFlow variants with identical model settings and references.
9. Score both variants with the six-dimension rubric.

Never label a next shot continuity-safe before a complete accepted observation exists.

## Run the CLI

From a repository clone, run:

```bash
python3 skills/shotflow/scripts/shotflow.py --help
```

If the package is installed, use `shotflow` directly.

Core command order:

```text
shotflow init
shotflow plan
shotflow observe
shotflow diff
shotflow compile-next
shotflow score
```

Keep generated video and frames under the project directory before binding them. The CLI rejects external paths and records relative paths plus SHA-256 hashes.

## Plan a shot

Supply a JSON plan with:

- a non-empty `planned` state;
- all five `grammar` axes;
- optional continuity locks and a reference shot ID.

Read [cinematic-grammar.md](references/cinematic-grammar.md) before authoring grammar. Describe concrete visual decisions. Do not use a director name as a substitute for camera, light, color, composition, or material behavior.

## Observe an accepted result

Record all six observed categories:

- `identity`
- `wardrobe_props`
- `space_direction`
- `motion`
- `light_material`
- `story_beat`

Read [continuity-contract.md](references/continuity-contract.md) before observing or compiling. Record visible facts, including unwanted drift. Do not silently preserve a planned fact that the accepted video contradicted.

## Compile the next shot

Use `compile-next` only after `observe`. Preserve the exact observed endpoint, prop ownership, screen direction, light source, material state, and geography. Change only what the new story beat requires.

The CLI emits a frozen prompt and hash. Present that prompt to the user before any paid or credit-consuming generation. Submit it unchanged after approval.

## Use Seedance 2.0

Read [seedance-2.0.md](references/seedance-2.0.md) when the chosen provider is Seedance. Treat only `seedance2.0_vision` as forward-tested in v0.1. Keep every A/B parameter and reference identical.

## Score results

Score every applicable dimension with:

- `0`: continuity break;
- `1`: minor or ambiguous drift;
- `2`: preserved;
- `n/a`: genuinely not applicable.

Do not hide applicable dimensions with `n/a`. A score is evidence from the supplied evaluation, not automatic video understanding.

## Safety and provenance

- Never store credentials, account links, cookies, tokens, or private run URLs.
- Preserve required AI-generation labels and provider marks.
- Use only original or authorized people, brands, music, and source media.
- Keep unsupported provider adapters marked unverified.
- Do not claim ShotFlow improves continuity until a fair A/B evaluation supports it.
