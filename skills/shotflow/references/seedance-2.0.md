# Seedance 2.0 adapter

## Verified v0.1 profile

```json
{
  "adapter": "seedance-2.0",
  "model": "seedance2.0_vision",
  "verified": true,
  "parameters": {
    "ratio": "16:9",
    "resolution": "1080p",
    "duration_seconds": 5
  }
}
```

Do not mark Fast, Mini, or another provider verified without a real forward test.

The Core default is the lower-cost normal-user
`Seedance_2.0_mini_lite`. Keep it `verified=false` until a real forward test
passes. `seedance2.0_vision` remains historical verified evidence; do not use it
by default when a standard-model run is sufficient.

## Generation boundary

ShotFlow compiles and freezes the prompt. It does not submit paid jobs.

Before submitting:

1. Confirm the official provider tool is installed and authenticated without printing credentials.
2. Confirm model access and remaining credits.
3. Show the exact prompt, model, duration, ratio, resolution, references, and maximum attempts.
4. Wait for explicit user approval to consume credits.
5. Submit the approved prompt unchanged.
6. Record public-safe provenance and artifact hashes; keep account and private run URLs local.

## Reference handoff

Use the accepted Clip 01 video and extracted final frame for both baseline and ShotFlow Clip 02 variants. Keep reference ordering identical. Do not remove provider or AI-generation marks from results.

## Public evidence

Record:

- provider and model;
- duration, ratio, and resolution;
- prompt SHA-256;
- source video and final-frame SHA-256;
- attempt number and accepted/rejected status;
- disclosure that the media was AI generated.

Do not publish access keys, cookies, account identifiers, private run links, or hidden provider responses.
