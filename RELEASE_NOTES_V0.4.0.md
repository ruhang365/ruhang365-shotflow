# ShotFlow v0.4.0

ShotFlow turns one accepted final frame and one next-shot sentence into a
directly submittable Seedance continuity Prompt.

## What is stable

- Quick Entry 1.0: one visible frame, one causal change, one Prompt at or below
  1,200 characters.
- Positive `FRAME 1 AUTHORITY → KEEP STABLE → CHANGE → FINAL PROOF` output.
- One final-frame attachment, five-second duration, original aspect ratio, and
  an explicit `Generation submitted: no` state.
- Visual grounding rules for prop ownership, hand contact, spatial relations,
  uncalibrated measurements, and hidden facts.
- The existing zero-dependency Python CLI, schemas, demo, evidence, and scoring
  interfaces remain available as the advanced path.

## Validation

The frozen RC2 forward test passed 4 of 5 counted isolated AI author cases
across OpenAI, Anthropic, and Google model families. Original failures, reserve
cases, reviewer votes, invalid calls, and SHA-256 hashes are public in
`examples/forward-tests/results-v04-rc2.json`.

This validates the frozen Skill contract across visual AI sessions. It is not
a human-usability result, no video was generated for this gate, and it does not
show that ShotFlow improves Seedance output quality.

## Try it

```bash
git clone --depth 1 https://github.com/ruhang365/ruhang365-shotflow.git
mkdir -p ~/.codex/skills
cp -R ruhang365-shotflow/skills/shotflow ~/.codex/skills/shotflow
```

Attach an accepted final frame and say:

```text
Use $shotflow on this accepted final frame.
Next-shot intent: [one visible next-shot change]
```

ShotFlow does not submit a generation or consume provider credits.

The release demo is a real ephemeral visual-Agent session. Its public-safe
receipt is in `launch/demo-assets.json`; the MP4 is staged as a Release asset,
not committed to Git.
