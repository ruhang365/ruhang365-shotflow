---
name: shotflow
description: Turn an accepted AI-video final frame plus one sentence of next-shot intent into a directly submittable Seedance continuity Prompt. Use when continuing a video from its last frame, preserving a character, product, or prop, repairing spatial or motion drift, compiling a next-shot Prompt, or using the advanced project, evidence, A/B, and scoring workflow.
---

# ShotFlow

Turn one accepted final frame and one sentence into the next Seedance-ready
continuity Prompt. The final frame is the visual authority.

## Quick path — default

When the user supplies an accepted final frame and one-sentence intent:

1. Inspect the actual frame pixels. Treat visible facts as authoritative.
2. Extract four compact locks: subject or product identity, props and geometry,
   camera and spatial layout, light and material.
3. Turn the sentence into one visible causal change. Use two changes only when
   the second cannot begin before the first is visibly complete.
4. Allocate 0.00–0.50s to opening match, up to 4.25s to the change, and
   4.25–5.00s to final proof.
5. Return exactly one positive, directly submittable Prompt of at most 1,200
   characters, plus the attachment instruction and suggested settings.

Do not require a source video, project, JSON, CLI, account, API Key, or
generation. Do not submit the Prompt. If no final frame is actually visible,
ask for it instead of inventing continuity facts.

Read [quick-entry.md](references/quick-entry.md) for the exact output contract.

## Quick output contract

Return the useful artifact first:

```text
SEEDANCE PROMPT
[exact Prompt]

SUBMIT WITH
- Attachment 1: the accepted final frame, as the only media reference
- Duration: 5 seconds
- Ratio: preserve the frame ratio; use 16:9 for the bundled showcase
- Generation submitted: no
```

The Prompt must describe concrete visible facts rather than labels such as
“same character” or “same cinematic style.” Use positive states. Avoid a long
list of prohibitions, director names, unsupported off-frame detail, and extra
story changes the user did not request.

## Advanced project workflow

Use the project workflow only when the user asks for manifests, repeatable CLI
state, scoring, or a benchmark:

1. Plan the current shot and record all five grammar axes.
2. Accept one result and record its video, final frame, and complete observation.
3. Compare planned and observed state; observed state is authoritative.
4. Compile the next shot, optionally prepare a Provider Handoff, and score an
   accepted continuation.

Never label a next shot continuity-safe before a complete accepted observation exists.

## Run the CLI — advanced

From a repository clone, run:

```bash
python3 skills/shotflow/scripts/shotflow.py --help
```

If the package is installed, use `shotflow` directly.

Advanced command order:

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

## Plan a shot — advanced

Supply a JSON plan with:

- a non-empty `planned` state;
- all five `grammar` axes;
- optional continuity locks and a reference shot ID.

Read [cinematic-grammar.md](references/cinematic-grammar.md) before authoring grammar. Describe concrete visual decisions. Do not use a director name as a substitute for camera, light, color, composition, or material behavior.

## Observe an accepted result — advanced

Record all six observed categories:

- `identity`
- `wardrobe_props`
- `space_direction`
- `motion`
- `light_material`
- `story_beat`

Read [continuity-contract.md](references/continuity-contract.md) before observing or compiling. Record visible facts, including unwanted drift. Do not silently preserve a planned fact that the accepted video contradicted.

## Compile the next shot — advanced

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

## Score results and benchmark — deferred advanced path

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

Gate 9 and Gate 10 are deferred by user decision. Do not reactivate, submit,
retry, or reinterpret them unless the user explicitly starts a new benchmark.
Preserve all historical evidence unchanged.

## Safety and provenance

- Never store credentials, account links, cookies, tokens, or private run URLs.
- Preserve required AI-generation labels and provider marks.
- Use only original or authorized people, brands, music, and source media.
- Keep unsupported provider adapters marked unverified.
- Do not claim ShotFlow improves continuity until a fair A/B evaluation supports it.
