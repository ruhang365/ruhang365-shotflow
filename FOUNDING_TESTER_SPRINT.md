# AI Forward-Test Sprint

Status: **COMPLETED — 4/5 COUNTED OUTPUTS PASSED — NO VIDEO GENERATION**

This protocol validates Quick Entry 1.0 across isolated visual AI sessions. It
does not represent human usability, generated-video quality, or an
effectiveness comparison. AI sessions do not count toward the Pro activation
gate.

Each author receives only:

```text
the ShotFlow Skill + one accepted final frame + one next-shot sentence
```

The author must actually inspect the frame and return the fixed Quick Entry 1.0
output. It receives no repository history, frozen expected facts, prior Prompt,
other test output, Provider account, or generation tool.

## Frozen author cases

| Test | Lane | Frame | Next-shot intent |
| --- | --- | --- | --- |
| T01 | Codex | Sky Mender suspended endpoint | The rope draws the worker toward the tower until both boots contact the ladder frame and hold. |
| T02 | Claude | Storm Deck endpoint | The worker pulls the orange case left until it rests beside the right knee and holds. |
| T03 | Gemini | Obsidian Bloom endpoint | The amber glow inside the lower bottle gradually intensifies and holds while the product geometry stays unchanged. |
| T04 | Codex | Sky Mender repair endpoint | The amber light in the gloved hands moves upward along the seam to the next visible rivet row and holds. |
| T05 | Claude | Storm Deck green-light endpoint | The green indicator pulses slowly twice and returns to a steady green. |

Two preregistered reserve frames were used after general grounding rules were
strengthened. R01 replaced T03; R02 replaced T05. The counted set was T01,
T02, T04, R01, and R02. T04 remained the single counted failure.

The machine-readable paths, hashes, ratios, and expected visible fact groups
live in `examples/forward-tests/protocol-v04-rc2.json`. Copy only the selected
frame and Skill into each scratch directory.

## Validation

Run `tools/validate_quick_output.py` first. It checks the fixed sections, 1,200
character limit, single final-frame attachment, five-second duration, ratio,
positive language, private-data terms, and `Generation submitted: no`.

Then give the frame, intent, and author output to two non-author visual model
families. They score whether:

- the subject, prop ownership, left/right geography, camera, light, and material
  locks come from visible pixels;
- the Prompt authorizes only the requested change;
- no hidden or off-frame fact is invented;
- opening match, causal change, and final visible proof are complete.

An author or reviewer without real image access is invalid and disclosed. A
third non-author reviewer resolves a disagreement. At most two unused historical
frames may replace invalid or failed author calls after a general Skill rule is
fixed. Original outputs remain unchanged.

Stable `v0.4.0` requires five valid author sessions, at least two model families,
and at least four passing outputs. General Skill fixes must be retested on an
unseen reserve frame. Gate 9/10, Showcase retries, and Provider generation stay
stopped. The frozen public-safe result, output hashes, invalid calls, and model
votes are in `examples/forward-tests/results-v04-rc2.json`.
