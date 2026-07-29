# Contributing

ShotFlow welcomes Core fixes, tests, provider adapters, grammar improvements, and evidence-backed showcases.

## Before opening a pull request

1. Keep Core usable without accounts, membership, cloud analysis, or Pro code.
2. Preserve `observed` as the highest authority.
3. Do not add a provider to the verified list without a real reproducible run.
4. Do not include credentials, private URLs, cookies, account IDs, copyrighted film clips, celebrity likenesses, real brand assets, or unlicensed music.
5. Preserve AI-generation labels and describe media rights.
6. Run:

```bash
python3 -m unittest discover -s tests -v
python3 tools/freeze_examples.py
python3 tools/check_repository.py
```

## Provider adapter evidence

Include:

- official provider documentation;
- exact model identifier and parameters;
- a sanitized project and artifact hashes;
- accepted and rejected attempt counts;
- one real output or public-safe evidence;
- limitations and unverified features.

Documentation-only adapters remain unverified.

## Showcase evidence

Use the Showcase issue template. A public work must disclose the AI provider, show at least two consecutive shots, describe what was observed between them, and confirm rights to shared media.

## Developer Certificate of Origin

Every commit must include a sign-off:

```text
Signed-off-by: Your Name <your-email@example.com>
```

Add it with `git commit -s`. The sign-off certifies the contribution under the [Developer Certificate of Origin 1.1](https://developercertificate.org/).

No Contributor License Agreement service is used.
