#!/usr/bin/env bash
set -eu

launch_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_root=$(dirname -- "$launch_dir")
demo_root=$(mktemp -d /tmp/shotflow-launch-en-XXXXXX)
demo_model=${SHOTFLOW_DEMO_MODEL:-gpt-5.6-sol}
demo_effort=${SHOTFLOW_DEMO_REASONING_EFFORT:-low}
demo_output="$demo_root/quick-entry.txt"

cp -R "$repo_root/skills/shotflow" "$demo_root/skill"
cp "$repo_root/examples/forward-tests/frames/T03.png" \
  "$demo_root/accepted-final-frame.png"

clear
printf '%s\n\n' 'ShotFlow — Final Frame to Next-Shot Prompt'
printf '%s\n' 'Attachment: accepted-final-frame.png'
printf '%s\n\n' 'Next-shot intent: The amber glow inside the lower bottle gradually intensifies and holds while the product geometry stays unchanged.'
printf '%s\n\n' 'Agent is reading the frame and compiling one visible change…'

if codex \
  --model "$demo_model" \
  --config "model_reasoning_effort=\"$demo_effort\"" \
  --sandbox read-only \
  --ask-for-approval never \
  --cd "$demo_root" \
  exec \
  --ephemeral \
  --ignore-rules \
  --skip-git-repo-check \
  --output-last-message "$demo_output" \
  'Read skill/SKILL.md completely and inspect the attached accepted final frame. Apply ShotFlow Quick Entry 1.0 to this intent: The amber glow inside the lower bottle gradually intensifies and holds while the product geometry stays unchanged. Output only the final Quick Entry artifact. Do not edit files and do not submit or generate video.' \
  --image "$demo_root/accepted-final-frame.png" \
  >/dev/null 2>&1; then
  printf '%s\n' 'AGENT OUTPUT'
  sed -n '1,240p' "$demo_output"
else
  printf '%s\n' 'Demo failed before producing a public-safe artifact.'
  exit 1
fi

if [ "${SHOTFLOW_DEMO_HOLD:-0}" = "1" ]; then
  printf '\n%s\n' 'Demo complete — generation submitted: no'
  read -r _
fi
