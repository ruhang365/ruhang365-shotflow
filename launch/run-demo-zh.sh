#!/usr/bin/env bash
set -eu

launch_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_root=$(dirname -- "$launch_dir")
demo_root=$(mktemp -d /tmp/shotflow-launch-zh-XXXXXX)
demo_model=${SHOTFLOW_DEMO_MODEL:-gpt-5.6-sol}
demo_effort=${SHOTFLOW_DEMO_REASONING_EFFORT:-low}
demo_output="$demo_root/quick-entry.txt"

cp -R "$repo_root/skills/shotflow" "$demo_root/skill"
cp "$repo_root/examples/forward-tests/frames/T03.png" \
  "$demo_root/accepted-final-frame.png"

clear
printf '%s\n\n' 'ShotFlow — 从最终帧到下一镜头 Prompt'
printf '%s\n' '附件：accepted-final-frame.png'
printf '%s\n\n' '下一镜头意图：瓶内下部的琥珀光逐渐增强并保持，产品几何结构不变。'
printf '%s\n\n' 'Agent 正在读取画面并编译一个可见变化……'

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
  '完整阅读 skill/SKILL.md，并真实检查附带的已接受最终帧。使用 ShotFlow Quick Entry 1.0 处理这一意图：瓶内下部的琥珀光逐渐增强并保持，产品几何结构不变。只输出最终 Quick Entry 成果，不编辑文件，不提交或生成视频。' \
  --image "$demo_root/accepted-final-frame.png" \
  >/dev/null 2>&1; then
  printf '%s\n' 'AGENT 输出'
  sed -n '1,240p' "$demo_output"
else
  printf '%s\n' '演示未能生成可公开成果。'
  exit 1
fi

if [ "${SHOTFLOW_DEMO_HOLD:-0}" = "1" ]; then
  printf '\n%s\n' '演示完成——未提交生成'
  read -r _
fi
