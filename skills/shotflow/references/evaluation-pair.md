# Evaluation Pair 1.0

After both A/B jobs return, preserve native hashes and metadata before creating
derived media. Run `tools/prepare_blind_pair.py` with the accepted frame,
frozen Prompts, native videos, Provider settings, generation order, and a fresh
output directory.

The tool rejects undecodable media, sources below 1280×720, non-16:9 rasters,
and durations outside 4.8–5.2 seconds. It re-encodes both variants to 1280×720,
24fps, five seconds, H.264 CRF 18 using Lanczos downscaling. It strips audio and
metadata and never crops or upscales.

Outputs are physically separated. `internal/evaluation-pair.json` keeps the
mapping and hashes. The `reviewer/` directory contains neutral A/B videos,
first/final frames, nine-frame contact sheets, a neutral accepted reference,
and `review-package.json` without Prompt, workflow, version, or mapping data.

Give reviewers only the `reviewer/` directory. A reviewer
without both complete videos and the reference is invalid. Score identity,
wardrobe/props, space, motion, light/material, and story beat from 0–2. Record
opening-frame match separately as pass/fail. Reveal the mapping only after all
valid reviews are frozen. Never replace a visually weak result.
