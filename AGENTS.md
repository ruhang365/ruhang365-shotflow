# ShotFlow repository rules

## Product invariant

The accepted observed shot is the highest authority. Never mark a next shot continuity-safe when the source shot has no complete accepted observation.

## Scope

- Keep Core local, account-free, and fully usable with human observations.
- Keep Pro automation outside this repository until the activation gate is met.
- Keep provider submission outside the Core CLI.
- Treat only `seedance2.0_vision` as forward-tested in v0.1.

## Generation boundary

- Do not submit a paid or credit-consuming generation without showing the exact prompt, model, settings, references, and attempt budget, then receiving explicit user approval.
- Do not downgrade the model, recharge, retry, or publish automatically.
- Record every attempt in the public-safe ledger.
- Never commit credentials, private run links, account identifiers, cookies, or raw 1080p videos.

## Originality and rights

- Use clean-room film grammar and original examples.
- Do not copy or adapt files, director cards, prompts, text, code, or media from `zy-cinematic-realism`.
- Keep third-party material as links and notices unless a compatible contribution has explicit provenance.
- Preserve AI-generation labels and accept only original or authorized inputs.

## Validation

Run:

```bash
python3 -m unittest discover -s tests -v
python3 tools/freeze_examples.py
python3 tools/check_repository.py
python3 /Users/fzy/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/shotflow
```

Treat installability, workflow correctness, generated-output evidence, public release, and social publication as separate acceptance states.
