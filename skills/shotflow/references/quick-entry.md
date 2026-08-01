# Final frame + one sentence

Use this as ShotFlow's default public workflow.

## Inputs

- one accepted final frame that the agent can inspect visually;
- one sentence describing the next visible action or outcome.

The frame, not the original plan, is the authority. Infer only facts visible in
the supplied image. If a hand, prop owner, hidden surface, or off-frame object
cannot be seen, do not invent it as a lock.

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

## Output

Return the Prompt before explanation. Then state:

- the final frame is Attachment 1 and the only media reference;
- five-second duration;
- the frame's aspect ratio;
- no generation was submitted.

If the user asks for actual generation, show the exact frozen Prompt, provider,
model, duration, aspect ratio, reference hash, and one-attempt budget, then wait
for explicit approval.
