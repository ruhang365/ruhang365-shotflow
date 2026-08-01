# Obsidian Bloom Clip 02 blind review — anchor-frame-v1

Status: **SHOTFLOW LOST — NO POSITIVE CLAIM PERMITTED**

The accepted Clip 01 final frame was the only media reference for both jobs.
Both variants used Lovart, standard Seedance 2.0, `thinking`, 16:9, five
seconds, provider-native output, one submission, and no retry, fallback, or
upscale. Both returned 1920×1080 video.

Reviewers received neutral Variant A/B media and the same frozen action rubric.
They were not shown the Prompt text, workflow name, or mapping. The mapping was
revealed only after scoring:

- Variant A: ShotFlow `clip-02-shotflow-anchor-v1.txt`
- Variant B: frozen baseline `clip-02-baseline-anchor-v1.txt`

## Valid reviewers

| Reviewer | Actual model | Visual input | A / ShotFlow | B / baseline | Winner |
| --- | --- | --- | ---: | ---: | --- |
| Claude Code | `claude-opus-4-8` | accepted frame + both contact sheets | 2/12 | 11/12 | B |
| Antigravity | `gemini-3.6-flash-high` | accepted frame + both contact sheets | 3/12 | 10/12 | B |
| Independent Codex reviewer | `gpt-5.6-sol` | accepted frame + both contact sheets | 5/12 | 8/12 | B |
| **Average** | — | — | **3.33/12** | **9.67/12** | **baseline** |

The initial tool-free Claude invocation correctly returned
`INVALID_NO_VISUAL_ACCESS` and was not counted. The normal Antigravity wrapper
also produced no review because its local read permission was denied. A
separate `gpt-oss-120b-medium` attempt also returned
`INVALID_NO_VISUAL_ACCESS` and was not counted. The valid Claude run exposed
only the read-only image tool. The valid Gemini run used an isolated temporary
directory, plan mode, and sandboxed read access. The independent Codex reviewer
received no task history and was restricted to the three neutral images. The
controller, which knew the random mapping, audited but did not vote. None of the
three counted reviewers saw the A/B mapping.

## Public evidence boundary

The public repository retains the frozen Prompts, provider handoffs, output
SHA-256 values, reviewer models, scores, and consensus. Raw 1080p variant videos
and temporary contact sheets remain outside Git, so this report is auditable as
a run ledger but its visual judgments cannot be replayed from the repository
alone. Do not present this report as independently reproducible media evidence
until approved public media assets exist.

## Consensus

Variant A preserved the premium dark-glass look but broke the required physical
chain:

1. the cap tilted and hinged sideways instead of translating vertically;
2. the exterior droplet fell to the lower surface;
3. amber appeared from or connected to the bottle base/liquid surface;
4. the ribbon crossed the bottle body instead of orbiting only the neck.

Variant B kept the bottle centered, lifted the cap vertically, and kept most of
the amber motion near the exposed neck. It still has two non-fatal deviations:
the amber begins slightly early, and the contact sheet does not prove one exact
clockwise orbit around the neck.

## Decision

Attempt `obsidian-bloom-003` is rejected. The result is retained as negative
evidence, but ShotFlow may not claim an improvement from this pair. There is no
retry under Gate 6.

The experiment also shows a mechanism problem worth fixing before any new paid
case: long negative constraints did not prevent the generator from inventing a
more dramatic but causally wrong ribbon. The next compiler revision should use
a shorter ordered beat with verifiable intermediate states rather than adding
more prohibitions.

The Claude visual review reported `total_cost_usd=0.0947555`. Lovart returned no
credit confirmation or amount for either generation job.
