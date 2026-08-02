---
name: shotflow
description: Turn an accepted AI-video final frame plus one sentence of next-shot intent into a directly submittable Seedance continuity Prompt. Use when continuing a video from its last frame, preserving a character, product, or prop, repairing spatial or motion drift, compiling a next-shot Prompt, or using the advanced project, evidence, A/B, and scoring workflow.
---

# ShotFlow

Turn one accepted final frame and one sentence into the next Seedance-ready
continuity Prompt. The final frame is the visual authority.

## Quick Entry 1.0 — default

When the user supplies an accepted final frame and one-sentence intent:

1. Confirm that the frame is actually visible and inspect its pixels. Treat
   visible facts as authoritative.
2. Extract four compact locks: subject or product identity, props and geometry,
   camera and spatial layout, light and material.
3. Turn the sentence into one visible causal change. Ask the user to select one
   when the sentence contains independent changes. Use two changes only when
   the second cannot begin before the first is visibly complete.
4. Allocate 0.00–0.50s to opening match, up to 4.25s to the change, and
   4.25–5.00s to final proof.
5. Return exactly one positive, directly submittable Prompt. Target 800–1,000
   characters; 1,200 is the hard maximum. Add the attachment instruction and
   suggested settings after the Prompt.

Before returning, run two grounding checks. First, name a hand-to-object,
strap-to-object, or other ownership relationship only when the visible contact
or connection proves it; when an endpoint is ambiguous, lock the objects and
their visible positions separately. Second, scan the Prompt for negative
directive wording (`do not`, `must not`, `never`, `avoid`, `without`, and their
Chinese equivalents) and rewrite every occurrence as the positive visible
state that should hold. Describe individual hand actions only when each contact
is visually distinguishable.

Treat screen direction and anatomical direction as different facts. When
`left` or `right` could mean either screen-left/screen-right or the subject's
body side, ask one concise clarification before compiling. Do not infer a
named knee, hand, or side when the pixels do not distinguish it.

As the final step, count the complete Prompt body from `FRAME 1 AUTHORITY`
through `FINAL PROOF`, including headings and whitespace. If it exceeds 1,200
characters, shorten repeated locks and adjectives, then count again. Never
return an over-limit Prompt.

Do not require a source video, project, JSON, CLI, account, API Key, or
generation. Do not submit the Prompt. If no final frame is actually visible,
ask for it instead of inventing continuity facts. If the requested outcome
depends on a hidden surface, off-frame object, unknown prop owner, or another
fact the frame cannot prove, ask for clarification before compiling.

Translate uncalibrated physical quantities into visible, frame-relative proof.
For example, express “one centimeter” as a narrow gap relative to a visible
collar or edge. Preserve the intended small direction and endpoint, but do not
claim that a single frame establishes an exact real-world distance.

This file is complete for the default Quick Entry. Do not read advanced
references or run the CLI for an ordinary final-frame-plus-intent request.
Read [quick-entry.md](references/quick-entry.md) only when the user asks for the
formal contract or when maintaining its validator.

## Quick output contract

Return the useful artifact first:

```text
SEEDANCE PROMPT
[exact Prompt]

SUBMIT WITH
- Attachment 1: the accepted final frame, as the only media reference
- Duration: 5 seconds
- Ratio: [the actual frame ratio]
- Generation submitted: no
```

The Prompt must contain `FRAME 1 AUTHORITY`, `KEEP STABLE`, `CHANGE`, and
`FINAL PROOF`. Describe concrete visible facts rather than labels such as
“same character” or “same cinematic style.” Use positive states. Avoid a long
list of prohibitions, director names, unsupported off-frame detail, and extra
story changes the user did not request. Return plain text without a Markdown
code fence.

## Advanced routing — only on request

If the user asks for project manifests, CLI state, Provider Handoffs, scoring,
or a benchmark, read [advanced-workflow.md](references/advanced-workflow.md).
That reference routes to the cinematic grammar, continuity contract, ordered
sequence, Provider, Seedance, and evaluation references as needed.

Never submit a generation without explicit approval. Never store credentials,
account links, cookies, tokens, or private run URLs. Do not claim that ShotFlow
improves generated-video continuity until a fair A/B evaluation supports it.
