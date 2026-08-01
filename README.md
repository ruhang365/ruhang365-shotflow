# ShotFlow — AI Video Continuity Compiler & Benchmark

**Compile the next shot from what actually happened, then benchmark whether it
really continued.**

> Your model says it continued. ShotFlow checks whether it actually did.

[中文说明](README.zh-CN.md) · [Examples](examples/) · [Skill](skills/shotflow/) · [Schemas](schemas/) · [Pro boundary](PRO.md)

![The Sky Mender accepted Clip 01, generated with Xiaoyunque / Seedance 2.0](examples/sky-mender/evidence/clip-01-preview.gif)

## Evidence status

ShotFlow `v0.3.0-rc1` is a software and offline-candidate release with **no
effectiveness claim**. Three real Seedance Clip 01 results have been accepted,
observed, and hashed. Two earlier controlled Clip 02 A/B pairs were blindly
reviewed — and **the baseline won both**. Those failures remain public evidence.
RC1 adds causal change budgets, positive-only `anchor-frame-v2`, and the
1800-character `provider-direct-v4` compiler. Gate 7 later ran once per variant
in Lovart unlimited mode, but unequal native resolutions invalidated the pair
before blind scoring.

| Case | Role | Status |
| --- | --- | --- |
| The Sky Mender | flagship spectacle | historical attempts rejected; v0.3 Gate 8 blocked because Gate 7 produced no eligible pair |
| Storm Deck | physical action | Lovart Kling O1 and two Seedance 2.0 baselines rejected; corrected handoff was acknowledged but the opening still broke, so the case is closed at its attempt cap |
| Obsidian Bloom | fictional product film | historical `anchor-frame-v1` pair lost; v0.3 Gate 7 closed when baseline returned 1280×720 and v0.3 returned 1920×1080 |

All accepted Clip 01 originals are 1920×1080, 24fps, 5.125 seconds and retain
the provider's container-level `AIGC Label=1`. The Lovart Gate 6 outputs are
also 1920×1080 but have no container AIGC label, so any public derivative must
add a visible disclosure. See the [Sky Mender blind review](examples/sky-mender/reviews/clip-02-blind-review-v1.md),
the [Obsidian Bloom blind review](examples/obsidian-bloom/reviews/clip-02-blind-review-anchor-v1.md),
and the [closed Gate 2 ledger](examples/GATE_2_APPROVAL.md).

The standard non-VIP `seedance2.0_direct` run stopped because that model rejects
`1080p`. Gate 4 then used the user-selected `seedance2.0_vision` VIP model at
`1080p`. Its first job returned no media because the account had insufficient
credits. One explicitly approved retry later returned a valid video, but the
fissure remained visibly open and dawn did not appear after repair. The result
was rejected and The Sky Mender was frozen rather than retried again. Later
generation moved to Lovart without treating the platform as the model.
A Kling O1 pilot was rejected for weak story progression. A Lovart-routed
Seedance 2.0 pilot reached the ending but began from the wrong spatial state.
A corrected handoff then bound the accepted final frame as the authoritative
first attachment and filtered historical artifact hashes. Lovart acknowledged
those roles, but the retry repeated the opening break and returned 720p instead
of the requested 1080p. It was rejected at the fifth-attempt cap. No case is
authorized for unattended generation. Gate 7 used its two-attempt cap in
Lovart unlimited mode, returned unequal native resolutions, and closed without
blind scoring or a retry. See the
[closed Storm Deck gate](examples/GATE_4_STORM_DECK_BASELINE_APPROVAL.md).
The previous registered mechanism, `anchor-frame-v1`, withheld the source video
when provider-specific reference roles are unproved. Obsidian Bloom's baseline
and ShotFlow handoffs now use the same accepted final frame as their sole media
reference. Lovart exposes no resolution selector, so both gates register
provider-native output with a 1280×720 minimum and no upscale. The standard
Seedance 2.0 model remains fixed for quality; Fast and Mini are excluded. The
baseline then returned 1920×1080 and passed its opening-frame gate. The
separately approved ShotFlow job also returned 1920×1080, but its cap hinged,
the exterior droplet fell, and its amber ribbon connected to the base/liquid
surface. Three blind visual reviewers unanimously preferred the baseline
(`9.67/12` versus `3.33/12`), so the ShotFlow attempt was rejected without a
retry.

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
- [`Ordered Sequence` 1.0/1.1](schemas/ordered-sequence.schema.json) keeps 1.0 byte-compatible and adds protected states, one to three authorized transitions, checkpoint `active_changes`, and final proof in 1.1.
- [`Provider Handoff` v1](schemas/provider-handoff.schema.json) binds reference roles, submission Prompt hashes, historical artifact exclusion, and the opening-frame gate. Positive-only `anchor-frame-v2` uses only the accepted endpoint; legacy profiles remain supported.
- Provider adapters describe portable settings. RC1 still marks only `seedance2.0_vision` through Xiaoyunque as forward-tested; Lovart-routed models remain separate evidence until accepted.
- The five-axis grammar covers narrative moment, camera movement, light/color, space/composition, and material/physics.
- The six-dimension rubric covers identity, wardrobe/props, space, motion, light/material, and story beat.

Observed state always overrides planned state. Missing observations cannot produce a continuity-safe contract.

Sequence `1.1` compiles contract `1.2` with `provider-direct-v4`: the complete
observation, five-axis grammar, and visual tests remain in JSON, while the
provider Prompt carries only the opening match, protected states, authorized
changes, five checkpoints, and final proof. Its limit is 1800 characters.
Sequence `1.0` continues to emit contract `1.1` / `provider-direct-v3` with
frozen byte-compatible output.

## Fair A/B protocol

For every case:

1. freeze the baseline Clip 02 prompt before Clip 01 generation;
2. generate and accept one Clip 01;
3. bind the real Clip 01 endpoint using one frozen Provider Handoff profile;
4. give baseline and ShotFlow variants the same model, parameters, profile, and references;
5. change only whether Clip 02 uses the accepted observation;
6. blind the variant labels during scoring.

ShotFlow will not claim improvement unless it wins a majority review in at least two of three cases and improves the average rubric score by at least 20 points.

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
