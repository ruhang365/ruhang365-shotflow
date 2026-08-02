# Advanced project, Provider, and evaluation workflow

Read this only when the user asks for manifests, repeatable CLI state, Provider
submission preparation, scoring, or a benchmark. Quick Entry does not need it.

## Project workflow

1. Plan the current shot and record all five grammar axes.
2. Accept one result and record its video, final frame, and complete observation.
3. Compare planned and observed state; observed state is authoritative.
4. Compile the next shot, optionally prepare a Provider Handoff, and score an
   accepted continuation.

Never label a next shot continuity-safe before a complete accepted observation exists.

## Run the CLI

From a repository clone, run:

```bash
python3 skills/shotflow/scripts/shotflow.py --help
```

If the package is installed, use `shotflow` directly.

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

Keep generated video and frames under the project directory before binding
them. The CLI rejects external paths and unrecognized media signatures, then
records relative paths plus SHA-256 hashes. This signature gate rejects obvious
fake files; it does not prove that a file fully decodes or came from the named
provider.

## Plan and observe

Supply a JSON plan with a non-empty `planned` state, all five `grammar` axes,
and optional continuity locks and a reference shot ID. Read
[cinematic-grammar.md](cinematic-grammar.md) before authoring grammar. Describe
concrete visual decisions rather than using a director name.

Record all six observed categories: `identity`, `wardrobe_props`,
`space_direction`, `motion`, `light_material`, and `story_beat`. Read
[continuity-contract.md](continuity-contract.md) before observing or compiling.
Record visible facts, including unwanted drift. Do not preserve a planned fact
that the accepted video contradicted.

## Compile the next shot

Use `compile-next` only after `observe`. Preserve the exact observed endpoint,
prop ownership, screen direction, light source, material state, and geography.
Change only what the new story beat requires.

Prefer Ordered Sequence `1.2` with exactly five contiguous phases: `match`,
`continue`, `initiate`, `resolve`, and `hold`. Separate one to four `protected`
facts from one or two sequential authorized `transitions`. Each checkpoint may
activate at most one transition. Keep the opening match for at least 0.5 seconds
and final proof for at least 0.75 seconds. Give every phase a positive state and
`visual_test`. Sequence `1.0` and `1.1` remain supported with frozen output.
Read [ordered-sequence.md](ordered-sequence.md) for the input shape.

The CLI rejects gaps, overlaps, duration mismatches, missing phases, negative
directives, and overlong provider prompts. Sequence `1.2` keeps the complete
observation, grammar, and visual tests in contract `1.3`. Its
`provider-direct-v5` Prompt sends only the opening match, stable facts,
sequential changes, and final proof. The creative Prompt is limited to 1,100
characters; the `anchor-frame-v3` submission is limited to 1,200.

Present the exact Prompt, settings, references, and attempt budget before any
paid or credit-consuming generation. Submit it unchanged only after approval.

## Seedance and Provider handoff

Read [seedance-2.0.md](seedance-2.0.md) when the chosen model family is Seedance
2.0. Treat only `seedance2.0_vision` through Xiaoyunque as forward-tested in
RC1. Lovart-routed Seedance 2.0 remains separate provider evidence. Keep every
A/B model, parameter, platform, and reference identical.

Before external submission, read [provider-handoff.md](provider-handoff.md).
Freeze one Handoff profile for both A/B variants. Prefer positive-only
`anchor-frame-v3` for Sequence `1.2`, with the accepted final frame as the sole
authoritative media reference. Exclude historical artifact hashes and require
a manual opening-frame review.

Default new projects to the full standard, non-VIP Seedance 2.0 channel
`seedance2.0_direct` at `720p`, with `verified=false` until its real forward
test passes. Use the `generic` adapter for offline planning or an unverified
provider. Do not substitute the Mini trial identifier. Use VIP only when the
user explicitly selects and approves that higher-cost queue.

## Score and benchmark — deferred

Score every applicable dimension with `0` for a continuity break, `1` for
minor or ambiguous drift, `2` for preserved, and `n/a` only when genuinely not
applicable. A score is supplied evaluation evidence, not automatic video
understanding.

If a blinded result loses, preserve the attempt and review. Do not cherry-pick
an attractive output or claim a win. Revise the mechanism under a new frozen
profile and require new credit approval.

When native resolutions differ, preserve both native receipts and read
[evaluation-pair.md](evaluation-pair.md). Canonical copies are 1280×720, 24fps,
five seconds, H.264 CRF 18, Lanczos downscale only. Never crop or upscale.

Gate 9 and Gate 10 are deferred. The Obsidian Bloom Showcase was rejected at
its one-attempt limit. Do not reactivate, retry, submit, or reinterpret these
experiments unless the user explicitly starts a new benchmark. Preserve all
historical evidence unchanged.

## Safety and provenance

- Never store credentials, account links, cookies, tokens, or private run URLs.
- Preserve required AI-generation labels and provider marks.
- Use only original or authorized people, brands, music, and source media.
- Keep unsupported provider adapters marked unverified.
- Do not claim continuity improvement without fair A/B evidence.
