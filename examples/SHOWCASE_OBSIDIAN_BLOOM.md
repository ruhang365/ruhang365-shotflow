# Obsidian Bloom — single ShotFlow showcase

Status: **GENERATED ONCE — REJECTED FOR SHOWCASE**

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

## One-job generation result

- Provider: Lovart
- Model tool: standard Seedance 2.0, `generate_video_seedance_v2_0`
- Account mode: `fast` credit channel; this is not the Fast model
- Reasoning mode: `thinking`
- Ratio and duration: 16:9, five seconds
- Attempt budget: one job; consumed once with no retry, upscale, downgrade,
  fallback, or A/B mate

The user authorized this exact one-job gate on 2026-08-02. The run used a new
isolated `thinking` thread and the `fast` credit channel with standard Seedance
2.0. Lovart returned no additional credit confirmation. The native output is
1920x1080, 24 fps, and 5.041667 seconds.

The opening visibly matches the reference closely, and the bottle, asymmetric
collar, attached droplet, composition, and material lighting remain broadly
stable. The result is nevertheless rejected as the public Showcase: instead of
rising about one centimeter and holding, the cap continues upward, produces an
overlong silver neck column, and approaches or leaves the upper frame boundary.
The frozen one-attempt policy prevents a retry. This is execution evidence, not
an effectiveness claim. See the
[public-safe receipt](obsidian-bloom/evidence/showcase-v04-receipt.json).
