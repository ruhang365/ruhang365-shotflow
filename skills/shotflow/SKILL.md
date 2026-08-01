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

For a zero-account first run, use `shotflow demo <directory>`. It creates a
small offline project, observed-state diff, contract `1.3`, and
`provider-direct-v5` Prompt without submitting a generation.

Keep generated video and frames under the project directory before binding them. The CLI rejects external paths and unrecognized media signatures, then records relative paths plus SHA-256 hashes. This signature gate rejects obvious fake files; it does not prove that a file fully decodes or came from the named provider.

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

Before compiling a new evidence candidate, prefer Ordered Sequence `1.2` with exactly five
contiguous phases: `match`, `continue`, `initiate`, `resolve`, and `hold`.
Separate one to four `protected` facts from one or two sequential authorized
`transitions`. Each checkpoint may activate at most one transition. Keep the
opening match for at least 0.5 seconds and final proof for at least 0.75
seconds. Give every phase a positive state and `visual_test`. Sequence `1.0`
and `1.1` remain supported with frozen output. Read
[continuity-contract.md](references/continuity-contract.md) for the complete
rules and [ordered-sequence.md](references/ordered-sequence.md) for the input
shape and concise example.

Run `compile-next` with `--sequence`. The CLI rejects gaps, overlaps, duration
mismatches, missing phases, negative directives, and overlong provider prompts.
Sequence `1.2` keeps the complete observation, grammar, and visual tests in
contract `1.3`. Its `provider-direct-v5` Prompt sends only the opening match,
stable facts, sequential changes, and final proof. The creative Prompt is
limited to 1,100 characters; the `anchor-frame-v3` submission is limited to
1,200.
Present that exact Prompt, settings, references, and attempt budget before any
paid or credit-consuming generation. Submit it unchanged after approval.

## Use Seedance 2.0

Read [seedance-2.0.md](references/seedance-2.0.md) when the chosen model family
is Seedance 2.0. Treat only `seedance2.0_vision` through Xiaoyunque as
forward-tested in RC1. A Lovart-routed Seedance 2.0 result is separate provider
evidence and remains unverified until it passes the continuity gates. Keep every
A/B model, parameter, platform, and reference identical.

Before any external provider submission, read
[provider-handoff.md](references/provider-handoff.md). Freeze one Handoff
profile for both A/B variants. Prefer positive-only `anchor-frame-v3` for
Sequence `1.2`; it submits the accepted final frame as the sole authoritative
media reference. Legacy anchor profiles remain supported. Use
`video-context-v1` only after context-only video roles are proved. Always
exclude historical artifact hashes and require a manual opening-frame review.

Default new projects to the full standard, non-VIP Seedance 2.0 channel
`seedance2.0_direct` at `720p`, with `verified=false` until its real forward test
passes.
Use the `generic` adapter for offline planning or an unverified provider; an
arbitrary model identifier remains `verified=false`.
Do not substitute `Seedance_2.0_mini_lite`: that identifier is the Mini trial
model, not the standard model. Use VIP only when the user explicitly selects
and approves that higher-cost queue.

## Score results

Score every applicable dimension with:

- `0`: continuity break;
- `1`: minor or ambiguous drift;
- `2`: preserved;
- `n/a`: genuinely not applicable.

Do not hide applicable dimensions with `n/a`. A score is evidence from the supplied evaluation, not automatic video understanding.

If a blinded result loses, preserve the attempt and review. Do not select only
the attractive output or claim a win. Revise the mechanism under a new prompt
profile, freeze it before another run, and require new credit approval.

When native resolutions differ, preserve both native receipts and use the
preregistered canonical review path in
[evaluation-pair.md](references/evaluation-pair.md). Canonical copies are
1280×720, 24fps, five seconds, H.264 CRF 18, Lanczos downscale only. Never crop
or upscale. Keep the A/B mapping hidden until every valid review is frozen.

## Safety and provenance

- Never store credentials, account links, cookies, tokens, or private run URLs.
- Preserve required AI-generation labels and provider marks.
- Use only original or authorized people, brands, music, and source media.
- Keep unsupported provider adapters marked unverified.
- Do not claim ShotFlow improves continuity until a fair A/B evaluation supports it.
