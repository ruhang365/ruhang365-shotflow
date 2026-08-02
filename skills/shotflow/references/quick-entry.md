# Quick Entry 1.0 — final frame + one sentence

Use this as ShotFlow's default public workflow.

## Inputs

- one accepted final frame that the agent can inspect visually;
- one sentence describing the next visible action or outcome.

The frame, not the original plan, is the authority. Infer only facts visible in
the supplied image. If a hand, prop owner, hidden surface, or off-frame object
cannot be seen, do not invent it as a lock.

If no image is visible, ask the user to attach it. If the sentence requests
multiple independent changes, ask the user to choose one. If the result depends
on a hidden surface, off-frame object, or unknown owner, ask for clarification.

## Compile

Write one Prompt with this order:

1. `FRAME 1 AUTHORITY`: Attachment 1 is the accepted endpoint and generated
   frame 1 matches its visible subject, geometry, camera, composition, light,
   and material state.
2. `KEEP STABLE`: three or four concrete visible facts.
3. `CHANGE`: one causal visible change, with a start state, motion, and end
   state. A second sequential change is allowed only when necessary.
4. `FINAL PROOF`: one directly visible end state held for the final 0.75s.

Keep the opening match visible for at least 0.5s. Keep the entire submission at
or below 1,200 characters. Use positive instructions such as “the locked camera
remains near-frontal” and “the cap stays level.” Describe the one requested
change once; do not pad the Prompt with cinematic adjectives.

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
