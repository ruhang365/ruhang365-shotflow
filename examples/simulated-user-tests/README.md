# Simulated-user QA for v0.4.0

This is internal product QA with five isolated AI personas. It is not a study
of five people.

## Result

- Initial deterministic contract result: **4/5 passed**.
- All five simulated personas said they would continue, but simulated intent is
  not demand evidence.
- No Provider account, video generation, or credits were used.
- The failed output remains unchanged and public in `outputs/S02.txt`.

The failed author produced a 1,267-character Prompt and guessed ambiguous
screen direction, anatomical direction, hand contact, and tether ownership.
The general Skill rules now require a final deterministic length count and a
clarification whenever screen-left/screen-right cannot be distinguished from a
subject's anatomical side.

An additional unseen-frame retest with `claude-opus-4-8` then asked for both
direction clarifications and did not compile or submit a Prompt. This retest is
recorded separately and does not change the original result to 5/5.

The installation finding also changed the public onboarding: Codex users now
ask the built-in `$skill-installer` to import the repository's
`skills/shotflow` folder. Python package and CLI installation remain advanced
developer options, not the Quick Entry path.

See `protocol-v040.json` for the frozen inputs and `results-v040.json` for
models, hashes, invalid calls, checks, and the claim boundary.

## Claim boundary

These results do not establish real-user usability, market demand, generated
video quality, or a continuity improvement over another workflow.
