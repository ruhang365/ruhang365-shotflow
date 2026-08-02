# ShotFlow — 从最终帧到下一镜头 Prompt

**上传已接受的最终帧，用一句话描述下一镜头，得到一条可直接提交给
Seedance 的连续性 Prompt。**

> 下一镜头从画面中真实存在的状态出发，而不是从旧 Prompt 原本希望发生的
> 状态出发。

[English](README.md) · [案例](examples/) · [Skill](skills/shotflow/) · [Schema](schemas/) · [Pro 边界](PRO.md)

![《黑曜之息》已接受最终帧](examples/obsidian-bloom/evidence/clip-01-final-frame.jpg)

## 安装后的快速工作流

把已接受的最终帧附给具备视觉能力、已安装 ShotFlow Skill 的 Agent，然后输入：

```text
使用 $shotflow 读取这张已接受的最终帧。
下一镜头意图：瓶内下部的琥珀光逐渐增强并保持，产品几何结构不变。
```

ShotFlow 会读取真实像素，锁定可见主体、道具、机位、空间、光线和材质，只为
用户要求的变化分配时间，最后返回：

```text
SEEDANCE PROMPT
FRAME 1 AUTHORITY:
附件 1 是已接受终点；生成首帧匹配可见产品、机位、构图、光线和材质。

KEEP STABLE
- 居中的黑色切面瓶、闭合瓶盖、非对称银色 collar 与左上方附着液滴保持稳定。
- 正面锁定机位、冷色背景与底部琥珀反光保持稳定。

CHANGE | 0.50-4.25s
瓶内下部的琥珀光逐渐增强到温暖且清晰可见的亮度。

FINAL PROOF | 4.25-5.00s
增强后的琥珀光在几何结构不变的瓶内稳定保持。

提交方式
- 附件 1：这张最终帧，并作为唯一媒体参考
- 时长：5 秒
- 比例：16:9
- 已提交生成：否
```

不需要源视频、项目文件、JSON、CLI、服务商账号、API Key 或付费生成。见
[Quick Entry 1.0 契约](skills/shotflow/references/quick-entry.md)和
[示例输出](examples/quick-entry/obsidian-bloom-output.txt)。

在 Codex 中只需粘贴一次安装请求：

```text
使用 $skill-installer 安装这个 ShotFlow Skill：
https://github.com/ruhang365/ruhang365-shotflow/tree/main/skills/shotflow
```

Codex 只会把 `skills/shotflow` 文件夹下载到 Skill 目录；用户不用安装仓库
源码、Python 包或 CLI。Skill 会在下一轮对话中可用。届时附上最终帧并输入：
`使用 $shotflow 读取这张已接受的最终帧。` 其他 Agent 平台也可以通过各自的
Skill 管理器导入同一个 [`skills/shotflow`](skills/shotflow/) 文件夹。

## 当前证据边界

`v0.4.0` **不包含效果改善声明**。其 RC2 证据验证视觉 Agent 能否遵守
Quick Entry 1.0 契约，不证明 Seedance 一定精确
执行 Prompt，也不证明 ShotFlow 优于其他方法。

| 案例 | 作用 | 当前状态 |
| --- | --- | --- |
| 天幕修补师 | 旗舰视觉奇观 | Gate 10 已冻结并延期；没有提交 v0.4 任务 |
| 暴风甲板 | 现实动作 | Lovart 的 Kling O1 与两条 Seedance 2.0 普通组均被拒绝；修正交接仍发生首帧断裂，案例在尝试上限处关闭 |
| 黑曜之息 | 虚构产品广告 | 单条 Showcase 已生成一次并被拒绝；不重试 |

RC2 隔离前向测试已完成：启用两张预登记替补帧后，固定计分集 **4/5 通过**，
覆盖 OpenAI、Anthropic 与 Google 三个模型家族。结果只证明 Skill 的跨 Agent
可移植性，不是真人测试或视频效果证据，也不触发 Pro；测试没有调用视频服务商。
见[机器可读结果](examples/forward-tests/results-v04-rc2.json)、
[被拒绝的 Showcase 记录](examples/SHOWCASE_OBSIDIAN_BLOOM.md)、
[AI 前向测试协议](FOUNDING_TESTER_SPRINT.md)、
[延期的 v0.4 评审协议](examples/V04_EVALUATION_PROTOCOL.md)、
[三方预注册审查](examples/V04_RC1_PREFLIGHT_REVIEW.md)、
[Gate 9](examples/GATE_9_OBSIDIAN_BLOOM_V04_RC1_APPROVAL.md) 与
[Gate 10](examples/GATE_10_SKY_MENDER_V04_RC1_APPROVAL.md)。

正式版发布后又完成了 5 个隔离模拟用户角色测试。初始结果为 **4/5** 通过
确定性契约；保留的失败输出既超过 1,200 字符，也擅自判断了含糊的屏幕方向与
人物身体侧。通用规则修正后，一张未见画面的复测能够先要求澄清。它们只是 AI
角色模拟，不是真人、需求验证、人类可用性证据或视频效果证据。见
[测试协议](examples/simulated-user-tests/protocol-v040.json)和
[测试结果](examples/simulated-user-tests/results-v040.json)，另有
[可读报告](examples/simulated-user-tests/README.md)。

历史失败或无效证据继续公开保留，没有删除、补评分或包装成胜利。失败的
《黑曜之息》Showcase 媒体不公开，也不再生成香水瓶视频。Gate 9/10、重试和
完整媒体发布继续停止，除非用户未来单独建立新闸门。见
[《天幕修补师》盲评](examples/sky-mender/reviews/clip-02-blind-review-v1.md)、
[《黑曜之息》盲评](examples/obsidian-bloom/reviews/clip-02-blind-review-anchor-v1.md)
与[已关闭的 Gate 7](examples/GATE_7_OBSIDIAN_BLOOM_V03_RC1_APPROVAL.md)。

## 它解决什么

常见工作流会根据原始计划预写 Clip 02。但 Clip 01 的真实结果经常偏离计划：道具换手、衣服破损、机位越轴、光源变化，或者动作停在意料之外的位置。

ShotFlow 把已接受最终帧当作事实源：

```text
已接受最终帧 + 一句下一镜头意图
                 ↓
            可见连续性锁
                 ↓
            单一因果变化
                 ↓
       可直接提交 Seedance 的 Prompt
```

项目/CLI 编译器与 Benchmark 工具继续保留，供需要清单、审计和评分的团队使用。

## 高级：本地编译器

需要 Python 3.10+，运行时零第三方依赖。

```bash
git clone https://github.com/ruhang365/ruhang365-shotflow.git
cd ruhang365-shotflow
python3 -m pip install .

shotflow init my-sequence --title "我的连续镜头"
shotflow --help
```

无需账号、API Key、视频生成或积分即可运行完整编译演示：

```bash
shotflow demo shotflow-offline-demo
```

不安装也可以从仓库直接运行：

```bash
python3 skills/shotflow/scripts/shotflow.py --help
```

其他使用目录式 Skill 的 Agent 也能复用，但发现路径可能不同。

## 高级项目命令

```text
shotflow init
shotflow plan
shotflow observe
shotflow diff
shotflow compile-next
shotflow score
shotflow demo
```

- `plan`：只计划当前镜头，记录五轴电影语法。
- `observe`：绑定真实视频、最终帧和六类完整观察。
- `diff`：暴露原计划与真实结果的差异。
- `compile-next`：读取五阶段 Ordered Sequence，从真实状态生成下一镜头合同与冻结 Prompt。
- `score`：用统一量表验收真实结果。

所有视频与最终帧必须放在项目目录内。CLI 会拒绝无法识别媒体文件头的明显伪文件，但该轻量门禁不代表完整解码成功，也不证明服务商来源。CLI 只保存相对路径、大小和 SHA-256，不保存账号、Token、Cookie 或私密运行链接。

## 稳定接口

- [`shotflow.project.json` v1](schemas/shotflow.project.schema.json)：项目、模型、实体、道具、镜头、观察、连续性锁、素材哈希、Prompt 和评分。
- [`ObservationPatch` v1](schemas/observation-patch.schema.json)：Core 人工观察与未来 Pro 自动分析共用的输出格式。
- [`Generation Attempt Ledger` v1](schemas/generation-attempt.schema.json)：记录每次提交、接受、拒绝和失败，不写入服务商私密标识。
- [`Ordered Sequence` 1.0/1.1/1.2](schemas/ordered-sequence.schema.json)：旧版本保持字节兼容；1.2 新增单一活跃变化、首帧保持与最终停留门禁。
- [`Provider Handoff` 1.0/1.1/1.2](schemas/provider-handoff.schema.json)：固定参考素材角色与 Prompt 哈希；纯正向 `anchor-frame-v3` 只使用已接受终点。
- [`Evaluation Pair` v1](schemas/evaluation-pair.schema.json)：记录原生与统一评审素材、服务商参数、盲化映射、哈希和评审状态。
- 五轴电影语法：叙事时刻、镜头运动、光线色彩、空间构图、材质物理。
- 六项连续性量表：人物身份、服装道具、空间方向、动作承接、光线材质、故事节拍。

真实观察始终覆盖计划状态。没有完整观察，不得输出 `continuity_safe=true`。

Sequence `1.2` 使用 contract `1.3` 与 `provider-direct-v5`：JSON 保留完整
观察、五轴电影语法、checkpoint 和 `visual_test`，服务商 Prompt 只发送首帧
匹配、稳定事实、顺序变化和最终可见证明；`anchor-frame-v3` 提交文本最长
1200 字符。Sequence `1.0/1.1` 继续生成字节兼容的旧输出。

## 延期的高级路径：严格 A/B

以下协议继续保留但当前不执行。没有新的明确 Benchmark 决定，不得提交
Gate 9/10。

每组案例都遵守：

1. 在 Clip 01 生成前冻结普通方法的 Clip 02 Prompt；
2. 只接受一个 Clip 01 作为共同起点；
3. 用一个冻结的 Provider Handoff profile 绑定 Clip 01 的真实终点；
4. 普通组与 ShotFlow 组使用相同模型、参数、profile 和参考素材；
5. 唯一变量是 Clip 02 是否读取真实观察；
6. 评分时隐藏组别。

只有 Gate 9 与 Gate 10 各自至少胜出三对中的两对、每个案例归一化平均分提升
至少 20 分、首帧匹配与其余发布门槛全部通过，才会公开有限的连续性改善声明。

## Core 与 Pro

公开 Core 已包含完整的人工连续性工作流，不依赖会员或云服务。未来 Pro 只负责自动读取视频，生成带时间证据和置信度的 ObservationPatch。

达到 200 个公开 GitHub Stars 后才启动 Pro Beta；模拟用户测试不会触发 Pro，
现在不创建空私库。

## 原创与许可

ShotFlow 的代码、Prompt、电影语法、案例和工作流均为洁净室原创。项目会把 [`zy-cinematic-realism`](https://github.com/popopo-99/zy-cinematic-realism) 列为结构化电影提示设计的 prior art，但不复制或改写其 CC BY-NC 文件、导演卡片、文本、代码与素材。

- 代码、Skill、Schema、模板：Apache-2.0。
- 原创文档与案例媒体：在可主张权利的范围内使用 CC BY 4.0。
- AI 生成内容保留法规及平台要求的标识。
- 开源许可不授予入行365商标权。

贡献前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。90 天目标为 1,000 Stars、20 个外部公开作品和 3 名代码或适配器贡献者。
