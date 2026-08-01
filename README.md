# ShotFlow — AI Video Continuity Compiler & Benchmark

**Compile the next shot from what actually happened, then benchmark whether it
really continued.**

> Your model says it continued. ShotFlow checks whether it actually did.

[中文说明](README.zh-CN.md) · [Examples](examples/) · [Skill](skills/shotflow/) · [Schemas](schemas/) · [Pro boundary](PRO.md)

![The Sky Mender accepted Clip 01, generated with Xiaoyunque / Seedance 2.0](examples/sky-mender/evidence/clip-01-preview.gif)

## Evidence status

ShotFlow `v0.4.0-rc1` is a software and preregistered-evidence release with **no
effectiveness claim**. Historical evidence remains unchanged: two earlier
controlled Clip 02 A/B pairs were blindly reviewed and the baseline won both;
Gate 7 then returned unequal native resolutions and was invalid before scoring.
RC1 adds Ordered Sequence `1.2`, contract `1.3`, the shorter
`provider-direct-v5`, `anchor-frame-v3`, deterministic 720p blind-review media,
and an account-free `shotflow demo`. No v0.4 provider job has been submitted.

| Case | Role | Status |
| --- | --- | --- |
| The Sky Mender | flagship spectacle | v0.4 Gate 10 inputs frozen; blocked until Gate 9 passes |
| Storm Deck | physical action | Lovart Kling O1 and two Seedance 2.0 baselines rejected; corrected handoff was acknowledged but the opening still broke, so the case is closed at its attempt cap |
| Obsidian Bloom | fictional product film | v0.4 Gate 9 inputs frozen; awaiting a separate six-job generation approval |

The v0.4 experiment prospectively separates native Provider evidence from
canonical review media. Every native result must be at least 1280×720 and is
hashed unchanged; both sides are then symmetrically encoded to 1280×720 for
blind review, never cropped or upscaled. Gate 9 runs three Obsidian Bloom pairs
with one authorized cap lift. Gate 10 runs three Sky Mender pairs with two
sequential changes and starts only after Gate 9 passes. See the
[protocol](examples/V04_EVALUATION_PROTOCOL.md),
[preflight review](examples/V04_RC1_PREFLIGHT_REVIEW.md),
[Gate 9](examples/GATE_9_OBSIDIAN_BLOOM_V04_RC1_APPROVAL.md), and
[Gate 10](examples/GATE_10_SKY_MENDER_V04_RC1_APPROVAL.md).

All prior failed or invalid evidence remains public: the
[Sky Mender review](examples/sky-mender/reviews/clip-02-blind-review-v1.md),
[Obsidian Bloom review](examples/obsidian-bloom/reviews/clip-02-blind-review-anchor-v1.md),
and [closed Gate 7](examples/GATE_7_OBSIDIAN_BLOOM_V03_RC1_APPROVAL.md).
Generated media keeps its required AI disclosure; full v0.4 A/B media requires
a separate publication approval.

## The problem

Most multi-shot AI video workflows write Clip 02 from the original plan. But Clip 01 rarely ends exactly as planned: a prop changes hands, a cape tears, the camera crosses the axis, or an unfinished motion lands somewhere unexpected.

ShotFlow makes the accepted output authoritative:

```text
plan Clip 01
    ↓
generate and accept a real result
    ↓
observe identity · props · space · motion · light · story
    ↓
diff planned vs observed
    ↓
compile Clip 02 from the real endpoint
    ↓
score the handoff
```

It is a continuity compiler and an evidence-first benchmark, not another
collection of cinematic adjectives.

## 60-second start

Requirements: Python 3.10+; no runtime dependencies.

```bash
git clone https://github.com/ruhang365/ruhang365-shotflow.git
cd ruhang365-shotflow
python3 -m pip install .

shotflow init my-sequence --title "My sequence"
shotflow --help
```

Try the complete compiler without an account or generation:

```bash
shotflow demo shotflow-offline-demo
```

Run directly from a clone without installation:

```bash
python3 skills/shotflow/scripts/shotflow.py --help
```

Install the Skill in Codex:

```bash
mkdir -p ~/.codex/skills
cp -R skills/shotflow ~/.codex/skills/shotflow
```

Other directory-based agent hosts can use the same Skill folder, but their discovery path may differ.

## Core workflow

Plan the current shot from a JSON specification:

```bash
shotflow plan \
  --project my-sequence \
  --shot-id clip-01 \
  --beat "The cable catches before the fall resolves." \
  --spec clip-01-plan.json \
  --prompt clip-01.txt
```

After accepting a real result, place the media inside the project and record all six observation categories. Core rejects unrecognized video and image signatures as obvious non-media files; this lightweight gate does not replace decode validation or provider provenance:

```bash
shotflow observe \
  --project my-sequence \
  --shot-id clip-01 \
  --state clip-01-observed.json \
  --media my-sequence/artifacts/clip-01.mp4 \
  --final-frame my-sequence/artifacts/clip-01-final.png

shotflow diff --project my-sequence --shot-id clip-01
```

Compile the next shot:

```bash
shotflow compile-next \
  --project my-sequence \
  --from-shot clip-01 \
  --next-shot clip-02-shotflow \
  --beat "The worker regains contact and seals the fissure." \
  --grammar clip-02-grammar.json \
  --sequence clip-02-sequence.json \
  --contract-out clip-02-contract.json \
  --prompt-out clip-02-shotflow.txt
```

Score an accepted result:

```bash
shotflow score \
  --project my-sequence \
  --shot-id clip-02-shotflow \
  --evaluation clip-02-evaluation.json
```

## Public interfaces

- [`shotflow.project.json` v1](schemas/shotflow.project.schema.json) stores provider settings, entities, props, planned shots, observations, locks, artifact hashes, prompts, and evaluations.
- [`ObservationPatch` v1](schemas/observation-patch.schema.json) is the shared human/Core and future Pro analyzer output.
- [`Generation Attempt Ledger` v1](schemas/generation-attempt.schema.json) records every submitted, accepted, rejected, or failed run without private provider identifiers.
- [`Ordered Sequence` 1.0/1.1/1.2](schemas/ordered-sequence.schema.json) keeps legacy output byte-compatible and adds the single-active-change evidence profile in 1.2.
- [`Provider Handoff` 1.0/1.1/1.2](schemas/provider-handoff.schema.json) binds reference roles and Prompt hashes; positive-only `anchor-frame-v3` uses only the accepted endpoint.
- [`Evaluation Pair` v1](schemas/evaluation-pair.schema.json) records native and canonical media, Provider settings, blind mapping, hashes, and review state.
- Provider adapters describe portable settings. RC1 still marks only `seedance2.0_vision` through Xiaoyunque as forward-tested; Lovart-routed models remain separate evidence until accepted.
- The five-axis grammar covers narrative moment, camera movement, light/color, space/composition, and material/physics.
- The six-dimension rubric covers identity, wardrobe/props, space, motion, light/material, and story beat.

Observed state always overrides planned state. Missing observations cannot produce a continuity-safe contract.

Sequence `1.2` compiles contract `1.3` with `provider-direct-v5`: complete
observations and visual tests remain in JSON, while the Provider Prompt carries
only opening match, stable facts, sequential changes, and final proof. The
`anchor-frame-v3` submission is capped at 1,200 characters. Sequence 1.0/1.1
retain frozen byte-compatible output.

## Fair A/B protocol

For every case:

1. freeze the baseline Clip 02 prompt before Clip 01 generation;
2. generate and accept one Clip 01;
3. bind the real Clip 01 endpoint using one frozen Provider Handoff profile;
4. give baseline and ShotFlow variants the same model, parameters, profile, and references;
5. change only whether Clip 02 uses the accepted observation;
6. blind the variant labels during scoring.

ShotFlow will not claim improvement unless Gate 9 and Gate 10 each win at least
two of three pairs, each improves the normalized case mean by at least 20
points, opening-frame match passes, and the remaining release gates are met.

During a real run, keep the public-safe attempt ledger current:

```bash
python3 tools/record_attempt.py \
  --case-dir examples/sky-mender \
  --variant clip-01 \
  --status submitted \
  --prompt examples/sky-mender/prompts/clip-01.txt
```

## Core and Pro

Core is complete for manual continuity work and stays local:

- project state and artifact hashes;
- five-axis shot planning;
- human ObservationPatch creation;
- diff, next-shot compilation, and scoring;
- generic provider interface and verified Seedance profile.

The future Pro beta may auto-read video and fill an ObservationPatch with timestamped evidence and confidence. It will not change the Core format or make Core projects dependent on a cloud account. Pro development starts only after 200 GitHub Stars or five real Core testers.

## Clean-room and rights

ShotFlow's code, prompts, grammar, examples, and workflow were written from scratch. [`zy-cinematic-realism`](https://github.com/popopo-99/zy-cinematic-realism) is acknowledged as prior art for structured cinematic prompt design, but its CC BY-NC files, director cards, text, code, and media are not included or adapted.

- Code, Skill, schemas, and templates: Apache-2.0.
- Original documentation and example media: CC BY 4.0 where copyright or related rights exist.
- Generated media must preserve required AI labels and provider marks.
- Ruhang365 names and marks are not licensed as trademarks.

See [Notices](NOTICE.md) and [Third-party notices](THIRD_PARTY_NOTICES.md).

## Contributing

Real output evidence matters more than an adapter name. Read [CONTRIBUTING.md](CONTRIBUTING.md) before proposing a provider adapter or showcase. Contributions use the Developer Certificate of Origin sign-off.

The 90-day target is 1,000 Stars, 20 external public works, and three code or adapter contributors. A community gallery opens only after three qualifying external works.
