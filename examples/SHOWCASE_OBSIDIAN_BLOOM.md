# Obsidian Bloom — single ShotFlow showcase

Status: **PROMPT FROZEN — ONE GENERATION NOT YET AUTHORIZED**

This replaces the active Gate 9 six-job A/B plan with one quality-first public
workflow example. It is a showcase, not benchmark evidence and not proof that
ShotFlow outperforms another method.

## Two user inputs

1. Accepted final frame:
   [`artifacts/clip-01-final-frame.png`](obsidian-bloom/artifacts/clip-01-final-frame.png)
2. Next-shot intent: “The black cap rises straight up by one centimeter,
   reveals the silver neck, and holds level.”

ShotFlow visually locks the bottle silhouette, asymmetric collar, attached
upper-left droplet, camera, liquid horizon, cool reflection, and amber
underlight. The only change is the vertical cap lift.

## Directly submittable artifact

- [Seedance Prompt](obsidian-bloom/prompts/clip-02-showcase-v04.txt)
- Prompt SHA-256: `dc35090179d9326d6f054c997fadb44282fec6fdffe626909cb14c742f7f5307`
- Accepted frame SHA-256: `56d6455da0310b8acce2364af99229825307b70bae8f677306496c1fa08e8a0e`
- Attachment policy: accepted final frame first and as the only media reference

## Proposed one-job generation gate

- Provider: Lovart
- Model tool: standard Seedance 2.0, `generate_video_seedance_v2_0`
- Account mode: `unlimited`
- Reasoning mode: `thinking`
- Ratio and duration: 16:9, five seconds
- Attempt budget: one job; no retry, upscale, downgrade, fallback, or A/B mate

Accept only when the opening visibly matches the reference, the cap translates
vertically while staying level, the bottle/collar/droplet remain stable, and the
final cap gap holds clearly. If Lovart asks for credit confirmation, stop and
show the amount. Generation requires a separate explicit user approval after a
read-only account/mode check.
