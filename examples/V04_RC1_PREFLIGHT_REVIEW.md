# ShotFlow v0.4 RC1 preregistration review

Status: **RC INPUT REVIEW COMPLETE — NO V0.4 PROVIDER JOB SUBMITTED**

This review covers the frozen Gate 9 and Gate 10 reference frames, Prompts,
Ordered Sequences, Provider Handoffs, evaluation protocol, neutral-media tool,
and public schemas. It is a contradiction review, not an effectiveness claim or
a generation approval.

## Reviewer access and outcome

| Lane | Resolved model | Visual access | Text access | Final-freeze status | Outcome |
| --- | --- | --- | --- | --- | --- |
| Codex controller | `gpt-5.6-sol` | valid | valid | valid | no P0/P1 contradiction after remediation |
| Claude Code | `claude-opus-4-8` | valid | valid | valid | no P0/P1 contradiction after remediation |
| Antigravity / Gemini | `gemini-3.1-pro-high` reported by the wrapper | valid in the initial review | valid in the initial review | invalid | the final rerun was auto-denied read access and returned empty output |

The Gemini final rerun is disclosed as invalid rather than silently replaced or
downgraded. The initial valid Gemini review found no blocking contradiction and
identified only non-blocking timing observations. The final frozen inputs are
therefore supported by two valid final-freeze reviewers plus one valid
pre-remediation reviewer. This is sufficient to publish a no-claim RC, but it
does not waive the later rule that each real blind A/B pair needs three valid
visual reviewers.

The collaboration smoke test also reported one wrapper warning: the
`agy-safe` default model was unavailable, while the independent authenticated
print-mode check succeeded. No dangerous permission bypass was used.

## Remediation applied before the final freeze

1. The mapping-bearing evaluation manifest now lives under `internal/`; the
   physically separate `reviewer/` directory contains only neutral A/B assets,
   a neutral reference filename, and a mapping-free manifest.
2. The normalized-score formula, case-mean calculation, improvement formula,
   and pair-level opening-match rule are explicit.
3. The protocol discloses that the baseline is strong,
   observation-informed prose. A null result means no demonstrated advantage
   over that baseline, not that continuity planning is ineffective.
4. The Sky Mender hand-light anchor now matches the accepted frame, and its
   final proof is a directly visible planted-boots state rather than a temporal
   precedence claim.

After remediation, 40 unit and CLI tests, schema validation, frozen-manifest
verification, repository checks, Skill validation, wheel installation, and the
account-free demo passed.

## Residual disclosed limitations

- Obsidian Bloom's 0.50–1.25 second stable interval is implicit in `KEEP
  STABLE`; the baseline states the hold in prose. This is an intentional format
  difference, not an unregistered visual change.
- Native outputs may retain subtle sharpness differences after symmetric 720p
  normalization. Native hashes and metadata remain separate evidence.
- The Sky Mender logical `project_id` is `the-sky-mender` while its directory
  slug is `sky-mender`; both A/B arms use the same logical ID, so it cannot leak
  the mapping.
- Provider metadata remains visible to reviewers because it is identical for A
  and B. Prompt, workflow identity, version labels, repository history, and the
  A/B mapping remain hidden.

## Freeze hashes

| Input | Obsidian Bloom | The Sky Mender |
| --- | --- | --- |
| accepted frame | `56d6455da0310b8acce2364af99229825307b70bae8f677306496c1fa08e8a0e` | `f05efcff94c047cdf46f681daf8996896e257ea3e9a6e54f1d36944b81bba1cd` |
| Ordered Sequence 1.2 | `508b39308ad1c0f4818d32928c4015806e22684419d60d62c66686979ace85b2` | `52b03c98bf1044355f5925b4cd2c250099591609eab09025298124bca2e64bfc` |
| baseline creative Prompt | `8736e9840ef88178a53c85e5db757a2e07f00a6228fc50612d3759b854ea0c6d` | `c5b0154434330a47cd7c398d821d18564bc9227bf1fc8c9f01abb6841948735e` |
| ShotFlow compiled Prompt | `06f5a7613e314795cf559aab470dc72e09ea773f9d7a5550a1e540d950dc0d41` | `c645f7633aaefeb122ed793c84d0224af31cbfa4cc852c0f315567311ec2fe37` |
| baseline Handoff 1.2 | `e04db8d044feed2b9a2daaae753e3794bff568b31cb724bbd67777e1ff2e41a4` | `0a173902c7a379edd360e2bd36f5edcc05047d0dc882e784aae8829a5529a94e` |
| ShotFlow Handoff 1.2 | `feed940ad552a1b07a67222490a9f76aad4003b70f3a98fb03803ad7c6166c30` | `ce1fc9d9f592f6d7133cfb52b55d68f0cd443101053b9a51974626441c72b87f` |

Decision: **READY FOR `v0.4.0-rc1` SOFTWARE RELEASE.** Gate 9 generation remains
unauthorized until its separate six-job approval is presented and accepted.
