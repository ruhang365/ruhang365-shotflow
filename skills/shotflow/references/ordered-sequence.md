# Ordered Sequence v1

Supply this object to `shotflow compile-next --sequence sequence.json`.

```json
{
  "sequence_version": "1.0",
  "duration_seconds": 5,
  "anchors": {
    "identity": "One observed subject remains visible.",
    "wardrobe_props": "The observed wardrobe and held prop remain in their accepted state.",
    "space_direction": "Subject, camera side, horizon, and scale remain at the accepted endpoint.",
    "light_material": "The accepted light sources and material response remain stable."
  },
  "checkpoints": [
    {"phase": "match", "start_seconds": 0, "end_seconds": 0.5, "state": "The opening matches the accepted endpoint.", "visual_test": "Identity, props, pose, camera, and light match."},
    {"phase": "continue", "start_seconds": 0.5, "end_seconds": 1.5, "state": "The unresolved observed motion continues.", "visual_test": "Direction, contact, and force follow the incoming motion."},
    {"phase": "initiate", "start_seconds": 1.5, "end_seconds": 2.5, "state": "The cause of the new action becomes visible.", "visual_test": "The causal contact or trigger is readable."},
    {"phase": "resolve", "start_seconds": 2.5, "end_seconds": 4.25, "state": "The required effect visibly completes.", "visual_test": "The intended state change is fully readable."},
    {"phase": "hold", "start_seconds": 4.25, "end_seconds": 5, "state": "The completed state holds clearly.", "visual_test": "The final frame proves the outcome and continuity anchors."}
  ]
}
```

Use exactly these five phase names and this order. Make time ranges contiguous
from zero to the provider duration. Write positive visible states. Put
evaluation criteria in `visual_test`; the compiler retains them in the contract
and omits them from the provider Prompt. The compiled provider Prompt must stay
within the hard 2400-character limit.

Keep anchors concise and grounded in the accepted observation. The JSON
contract retains the complete observed state, its hash, the complete sequence,
and the sequence hash.
