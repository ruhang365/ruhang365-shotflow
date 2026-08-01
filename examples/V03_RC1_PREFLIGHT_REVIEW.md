# v0.3 RC1 preflight contradiction review

Review date: 2026-08-01

This is a read-only review before paid generation. It tests whether each
accepted Clip 01 endpoint, frozen baseline, Ordered Sequence `1.1`, compiled
`provider-direct-v4` Prompt, and `anchor-frame-v2` policy form a coherent A/B
candidate. It is not output evidence and cannot support an improvement claim.

## Frozen review scope

Each valid visual reviewer inspected both accepted Clip 01 final-frame PNGs
and received the two exact baseline Prompts, v0.3 Prompts, and Sequence JSON
files. Provider Handoff manifests were independently regenerated from the
frozen inputs, compared field by field, schema-validated, and checked by the
controller. They add the same positive `anchor-frame-v2` wrapper and the same
authoritative final-frame hash to each A/B pair.

Reviewers reported visible facts, direct contradictions, positive-text status,
A/B fairness, and predictive risks. They were instructed not to predict a
winner. A response without real access to both PNGs was invalid.

## Counted reviewers

| Reviewer | Actual model | Visual access | Obsidian Bloom | The Sky Mender |
| --- | --- | --- | --- | --- |
| Codex controller | `gpt-5.6-sol` | valid | READY with registered risks | READY with registered risks |
| Antigravity / agy | `gemini-3.6-flash-high` | valid | READY with registered risks | READY |
| Claude Code | `claude-sonnet-5` | valid | READY with registered risks | READY with registered risks |

The valid Claude call reported `$0.06801465`. No reviewer edited files,
submitted provider jobs, or scored imagined outputs.

## Invalid calls disclosed

- Antigravity request for `gemini-3.1-pro-high`: invalid because the backend
  mapped it to another model and headless file permission was denied.
- Antigravity `gpt-oss-120b-medium`: invalid because it explicitly returned
  `VISUAL_ACCESS=INVALID`.
- Claude Opus call without exact paths: invalid; `$0.17915875`.
- Claude Opus call with paths: invalid because its answer cross-mapped two
  files even though their SHA-256 values and first lines proved the files were
  correct; `$0.12125875`.
- Claude Opus budget-capped call: invalid because it returned no review after
  reaching the budget boundary; provider metadata reported `$0.28442075`.

Invalid calls are not counted toward the three-reviewer requirement.

## Findings kept in the preregistration

No counted reviewer found a P0 blocker or an internal Sequence reference error.
All three judged the two variants to target the same core Clip 02 story outcome.
All three confirmed that v0.3 uses positive visible states rather than a
prohibition list.

Obsidian Bloom retains two disclosed comparison differences:

- the frozen baseline describes a `front-left diagonal facet`, while the
  accepted frame and v0.3 observation describe the visible asymmetric
  front-right facet;
- the frozen baseline asks the exterior droplet to end lower, while v0.3 spends
  its three-change budget on collar settle, cap lift, and the localized amber
  neck orbit, keeping the accepted droplet attached.

These are consequences of the preregistered baseline-versus-observed-state
method, not post-review edits. The baseline stays frozen. The counted reviewers
also disagreed on how strongly the single still proves collar displacement and
droplet vertical position. Those ambiguities remain public predictive risks.

The Sky Mender review found no direct state contradiction. Registered risks are
the large cable-driven return arc, two-boot contact geometry, hand-light seam
contact, and the repair-to-dawn transition within five seconds.

## Decision

- Gate 7 Obsidian Bloom: **READY FOR COST-SPECIFIC APPROVAL**, not authorized.
- Gate 8 The Sky Mender: **FROZEN AND BLOCKED** until Gate 7 receives a valid
  majority v0.3 win.
- Effectiveness claim: **NOT ALLOWED** by this review.
