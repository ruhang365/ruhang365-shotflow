# ShotFlow v0.4 preregistered evaluation protocol

Status: **STRICT BENCHMARK DEFERRED BY USER — NO V0.4 GENERATION SUBMITTED**

This protocol is prospective. It does not reopen, rescore, or reinterpret Gate
7 or Gate 8. Native-resolution variance is recorded as provider behavior. A/B
review uses separately encoded canonical copies so resolution cannot reveal a
variant or invalidate an otherwise decodable pair.

The six-job Gate 9/10 plan was stopped on 2026-08-01. Keep this protocol and its
hashes as preregistration history; do not execute it unless the user explicitly
reactivates a new benchmark round.

## Fixed generation conditions

- Lovart `generate_video_seedance_v2_0`
- account generation mode `unlimited`
- thread reasoning mode `thinking`
- 16:9, five seconds, provider-native output at or above 1280×720
- one accepted final frame under `anchor-frame-v3`
- one isolated provider thread for each experiment cell
- no Fast, Mini, other provider, upscale, creative retry, or output selection

Each case contains three pairs in the registered order:

1. baseline, then ShotFlow;
2. ShotFlow, then baseline;
3. baseline, then ShotFlow.

The normal cap is six jobs per case. A missing, corrupt, sub-720p, non-16:9,
or out-of-range-duration artifact is a technical failure, not a visual-quality
failure. One complete replacement pair may be proposed only after a new user
approval; the hard cap is eight jobs. A visually weak result remains in its
registered pair.

## Canonical review media

`tools/prepare_blind_pair.py` verifies native media and produces both neutral
variants as 1280×720, 24fps, exactly five seconds, H.264 CRF 18. It applies
Lanczos downscaling, strips audio and metadata, and never crops or upscales.
It also produces first frames, final frames, nine-frame contact sheets, native
and derived hashes. The mapping-bearing manifest is written under `internal/`;
the separate `reviewer/` directory contains only neutral `variant-a` /
`variant-b` filenames, a neutral `accepted-reference.png`, and a reviewer
manifest without Prompt, workflow, version, or A/B mapping data. Reviewers are
given only that directory.

## Blind review

Codex, Claude, and Gemini each receive the accepted frame, two canonical full
videos, their first/final frames, and contact sheets. A reviewer without access
to all visual inputs is invalid. Reviewers do not receive prompts, mappings,
workflow identity, or repository history.

Each applicable dimension is scored 0–2: subject identity, wardrobe/props,
space direction, motion handoff, light/material, and story beat. Opening-frame
match is a separate pass/fail decision.

A pair is a ShotFlow win only with at least two of three reviewer votes. A case
passes only when ShotFlow wins at least two pairs, improves the case mean by at
least 20 normalized points, and passes opening-frame match in at least two
pairs. Gate 10 starts only after Gate 9 passes.

For each reviewer and variant, the normalized score is
`sum(six dimension scores) / 12 * 100`. A case mean is the arithmetic mean of
all valid reviewer scores for that workflow across the three pairs. Improvement
is `ShotFlow case mean - baseline case mean`. A ShotFlow opening match passes a
pair when at least two of three valid reviewers mark it Pass; the case requires
that pair-level result in at least two pairs.

The baseline is deliberately strong, observation-informed natural-language
continuation prose. This experiment tests whether ShotFlow's explicit protected
facts and causal time budget outperform that strong prose under matched inputs;
it is not a comparison against a naive or observation-free Prompt. A null result
therefore means no demonstrated gain over this strong baseline, not that all
continuity planning is ineffective.

## Release boundary

Stable `v0.4.0` additionally requires both cases to pass, user acceptance that
The Sky Mender is worth a social launch, a 4/5 Founding Tester Sprint result,
and separate approval to publish complete A/B media. Otherwise RC1 and the
failure evidence remain public without an effectiveness claim.
