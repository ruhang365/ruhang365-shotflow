# Ordered Sequence 1.2

Supply this object to `shotflow compile-next --sequence sequence.json`.

```json
{
  "sequence_version": "1.2",
  "duration_seconds": 5,
  "anchors": {
    "identity": "One observed subject remains visible.",
    "wardrobe_props": "The observed wardrobe and held prop remain in their accepted state.",
    "space_direction": "Subject, camera side, horizon, and scale remain at the accepted endpoint.",
    "light_material": "The accepted light sources and material response remain stable."
  },
  "change_budget": {
    "protected": [
      {"id": "subject-identity", "state": "The same observed subject and wardrobe remain visible."},
      {"id": "camera-side", "state": "The accepted camera side, horizon, and scale remain stable."}
    ],
    "transitions": [
      {
        "id": "action-resolve",
        "subject": "the observed unfinished action",
        "from_state": "the accepted endpoint contains visible unresolved energy",
        "transition": "the existing force carries the action to one readable contact",
        "to_state": "the subject holds the completed contact",
        "proof": "the final frame clearly shows the completed contact"
      }
    ]
  },
  "checkpoints": [
    {"phase": "match", "start_seconds": 0, "end_seconds": 0.5, "state": "The opening matches the accepted endpoint.", "visual_test": "Identity, props, pose, camera, and light match.", "active_changes": []},
    {"phase": "continue", "start_seconds": 0.5, "end_seconds": 1.5, "state": "The unresolved observed motion continues.", "visual_test": "Direction, contact, and force follow the incoming motion.", "active_changes": ["action-resolve"]},
    {"phase": "initiate", "start_seconds": 1.5, "end_seconds": 2.5, "state": "The cause of the new action becomes visible.", "visual_test": "The causal contact or trigger is readable.", "active_changes": ["action-resolve"]},
    {"phase": "resolve", "start_seconds": 2.5, "end_seconds": 4.25, "state": "The required effect visibly completes.", "visual_test": "The intended state change is fully readable.", "active_changes": ["action-resolve"]},
    {"phase": "hold", "start_seconds": 4.25, "end_seconds": 5, "state": "The completed state holds clearly.", "visual_test": "The final frame proves the outcome and continuity anchors.", "active_changes": []}
  ]
}
```

`protected` contains one to four stable visible states. `transitions` contains
one or two authorized changes with unique IDs and complete
`from_state → transition → to_state → proof` causality. Every transition ID
must appear in at least one non-`match`, non-`hold` `active_changes` list, and
every reference must resolve to a registered transition.

Only one transition may be active in a checkpoint. Its active checkpoints must
be contiguous, and multiple transitions activate in registered order. Keep
`match` at least 0.5 seconds and `hold` at least 0.75 seconds.

Use exactly the five phase names shown above and keep their ranges contiguous
from zero to the provider duration. Write positive visible states. Put
evaluation criteria in `visual_test`; the compiler retains them in the JSON
contract and omits them from the provider Prompt. Negative directives are
invalid in anchors, protected states, transitions, checkpoints, and visual
tests. The compiled `provider-direct-v5` creative Prompt must stay within
1,100 characters; `anchor-frame-v3` keeps the submission within 1,200.

Keep anchors concise and grounded in the accepted observation. The contract
retains the complete observed state, its hash, the five-axis grammar, complete
sequence, and sequence hash.

Sequence `1.2` compiles to contract `1.3`. Sequence `1.0` and `1.1` remain
accepted and retain byte-stable `provider-direct-v3` and `provider-direct-v4`
output.
