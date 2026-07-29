# The Sky Mender Clip 02 blind review — mechanism v1

Status: **FAILED THE PUBLIC CLAIM GATE**

Two independent AI reviewers received only the common Clip 01 final frame and
neutral Variant A/B media. They were not given Prompt text, repository context,
or the variant mapping.

The mapping was revealed after both reviews:

- Variant A: ShotFlow `clip-02-shotflow.txt`
- Variant B: frozen baseline

Public evidence after unblinding:

- [ShotFlow v1 preview](../evidence/clip-02-shotflow-preview.gif) and
  [receipt](../evidence/clip-02-shotflow-receipt.json)
- [baseline preview](../evidence/clip-02-baseline-preview.gif) and
  [receipt](../evidence/clip-02-baseline-receipt.json)

| Reviewer | ShotFlow | Baseline | Preferred | Clear winner |
| --- | ---: | ---: | --- | --- |
| independent-ai-01 | 91.67 | 100 | baseline | no |
| independent-ai-02 | 75 | 100 | baseline | yes |
| **Average** | **83.34** | **100** | **baseline** | — |

Both variants preserved identity, clothing, tower geography, the open cable
motion, and the storm material state. The baseline won because it more visibly
showed the repair action after tower contact. ShotFlow v1 emphasized the
observed state but allowed the required action to be diluted by the longer
contract.

No positive ShotFlow claim is permitted from this result. Attempt
`sky-mender-003` remains in the ledger as rejected evidence.

The next candidate uses the `provider-direct-v2` prompt profile: required action
and physical order first, explicit visible proof at the ending, minimum opening
continuity locks second, and the detailed state retained in the JSON contract
instead of repeated as the provider's main task.
