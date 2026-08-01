# Provider handoff

Provider submission stays outside the Core CLI. Before using any external
runner, choose one `Provider Handoff v1` profile and freeze it for both A/B
variants.

Use `anchor-frame-v2` with Sequence `1.1`. It sends a short positive-only
opening-authority wrapper, the exact frozen creative Prompt, and the accepted
final frame as the sole media reference. It does not add the legacy prohibition
list. Both A/B variants must use this profile and the same frame hash.

Use legacy `anchor-frame-v1` only when reproducing an earlier experiment. It
applies the same single-frame reference policy with its original wrapper.
Use either anchor profile when the provider exposes generic attachments or has
not proved that a source video can be bound as context-only. It sends:

1. the accepted final frame as the only attachment and authoritative opening
   state;
2. the frozen creative Prompt plus the exact provider submission Prompt hashes;
3. every previously returned output hash from the provider thread;
4. an opening-frame review gate that starts as `pending`.

Incoming motion must then be stated in the creative instructions from the
accepted observation. The runner must not infer or recreate earlier frames.

Use `video-context-v1` only when the provider's native or provider-specific
interface has demonstrated reliable reference roles. It sends:

1. the accepted final frame as attachment 1 and the authoritative opening state;
2. the accepted source video as attachment 2 and motion/identity context only;
3. the frozen creative Prompt and the exact provider submission Prompt hashes;
4. every previously returned output hash from the provider thread;
5. an opening-frame review gate that starts as `pending`.

The accepted observed endpoint always outranks the source video's opening. The
provider must not restart the earlier shot or insert an empty establishing
frame before continuing the action. Keep the chosen profile, final-frame hash,
platform, model, and generation settings identical between baseline and
ShotFlow variants.

Some provider threads return historical artifacts together with a new result.
Accept only a new SHA-256 not present before submission. If zero or multiple new
hashes remain, stop and resolve the ambiguity instead of guessing.

After generation, extract the actual first frame. A human must verify subject,
props, pose, camera side, and spatial geography against the accepted final
frame. Until that review passes, do not mark the shot continuity-safe even when
the later action or overall image quality is strong.

Prepare a manifest without submitting media:

```bash
python3 tools/prepare_provider_handoff.py \
  --project examples/storm-deck/shotflow.project.json \
  --from-shot clip-01 \
  --variant clip-02-baseline \
  --prompt examples/storm-deck/prompts/clip-02-baseline-frozen.txt \
  --platform Lovart \
  --model-tool generate_video_seedance_v2_0 \
  --profile anchor-frame-v2 \
  --output examples/storm-deck/evidence/provider-handoff.json
```
