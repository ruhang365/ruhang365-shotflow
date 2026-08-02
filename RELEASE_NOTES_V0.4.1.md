# ShotFlow v0.4.1

ShotFlow's default path is now a focused AI Skill: install one GitHub Skill
folder, attach an accepted final frame, add one next-shot sentence, and receive
a Seedance-ready continuity Prompt.

## What changed

- Codex onboarding now uses the built-in `$skill-installer`; Quick Entry does
  not require a repository clone, Python package, or CLI installation.
- The default `SKILL.md` was reduced from 228 lines to 95 lines. Project state,
  Provider, CLI, scoring, and deferred Benchmark instructions moved to an
  on-demand advanced reference.
- Prompt generation targets 800–1,000 characters with a hard 1,200-character
  limit and a final count after editing.
- Ambiguous screen-left/screen-right and anatomical left/right requests now
  require clarification instead of a guessed body side.
- The repository includes five simulated-user QA outputs, the preserved 4/5
  initial result, and an unseen-frame post-fix retest. These are AI simulations,
  not five people.
- A live Chinese forward run records the accepted frame, intent, public install
  path, exact outputs, hashes, model settings, token counts, wall time, and the
  explicit no-generation state.
- GitHub CI now uses the official Node 24-based Action versions.

## Install in Codex

```text
Use $skill-installer to install the ShotFlow Skill from:
https://github.com/ruhang365/ruhang365-shotflow/tree/main/skills/shotflow
```

On the next turn, attach an accepted final frame and write:

```text
Use $shotflow on this accepted final frame.
Next-shot intent: [one visible next-shot change]
```

## Evidence boundary

The real forward run proves that a visual Agent can turn one accepted frame and
one sentence into a contract-valid Prompt. It does not prove that Seedance will
execute the Prompt precisely or that ShotFlow improves generated-video
continuity. No video Provider was called and no generation credits were used.
