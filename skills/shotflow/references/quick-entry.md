# Quick Entry 1.0 — final frame + one sentence

Use this as ShotFlow's default public workflow.

## Inputs

- one accepted final frame that the agent can inspect visually;
- one sentence describing the next visible action or outcome.

The frame, not the original plan, is the authority. Infer only facts visible in
the supplied image. If a hand, prop owner, hidden surface, or off-frame object
cannot be seen, do not invent it as a lock.

Treat contact and ownership as separate visual claims. Name a relationship
only when the connection or contact point is visible. If a strap crosses behind
two objects, describe its visible diagonal and endpoints separately rather
than assigning it to the nearer object. If individual hands cannot be
distinguished, describe the visible contact area rather than inventing which
hand holds which object.

If no image is visible, ask the user to attach it. If the sentence requests
multiple independent changes, ask the user to choose one. If the result depends
on a hidden surface, off-frame object, or unknown owner, ask for clarification.

Treat screen direction and anatomical direction as separate claims. If `left`
or `right` could refer either to the image or to the subject's body, ask which
meaning the user intends. Do not assign a named knee, hand, or body side unless
the pixels make it distinguishable.

## Compile

Write one Prompt with this order:

1. `FRAME 1 AUTHORITY`: Attachment 1 is the accepted endpoint and generated
   frame 1 matches its visible subject, geometry, camera, composition, light,
   and material state.
2. `KEEP STABLE`: three or four concrete visible facts.
3. `CHANGE`: one causal visible change, with a start state, motion, and end
   state. A second sequential change is allowed only when necessary.
4. `FINAL PROOF`: one directly visible end state held for the final 0.75s.

Keep the opening match visible for at least 0.5s. Keep the Prompt body from
`FRAME 1 AUTHORITY` through `FINAL PROOF`, including headings and whitespace,
within a target range of 800–1,000 characters and never above 1,200. Use
positive instructions such as “the locked camera remains near-frontal” and
“the cap stays level.” Describe the one requested change once; do not pad the
Prompt with cinematic adjectives.

Before returning, scan the Prompt for `do not`, `must not`, `never`, `avoid`,
`without`, `不要`, `禁止`, `不得`, and `避免`. Replace each with the positive
visible state to preserve. Count the final Prompt after all edits; if it is
over 1,200 characters, shorten repeated locks and adjectives, then count
again. Never return an over-limit Prompt. Return plain text with no Markdown
code fence.

## Convert measurements into visual proof

A single frame does not establish real-world scale. Keep the intent of words
such as “one centimeter,” “slightly,” or “a little,” but compile the endpoint
as a visible relative bound:

- “the cap rises one centimeter” becomes “the cap rises only until a narrow
  gap smaller than the visible collar height appears, then holds level”;
- “move slightly left” becomes “move left by less than the visible subject
  width, then hold at the named landmark.”

Do not promise exact physical distance unless the frame contains a reliable
visible scale reference.

## Output

Return exactly this structure, with the Prompt before explanation:

```text
SEEDANCE PROMPT
FRAME 1 AUTHORITY:
[visible opening authority]

KEEP STABLE
[three or four visible locks]

CHANGE
[one authorized causal change]

FINAL PROOF
[one visible endpoint held for the final 0.75s]

SUBMIT WITH
- Attachment 1: the accepted final frame, as the only media reference
- Duration: 5 seconds
- Ratio: [the actual frame ratio]
- Generation submitted: no
```

The submission block must state:

- the final frame is Attachment 1 and the only media reference;
- five-second duration;
- the frame's aspect ratio;
- no generation was submitted.

If the user asks for actual generation, show the exact frozen Prompt, provider,
model, duration, aspect ratio, reference hash, and one-attempt budget, then wait
for explicit approval.
