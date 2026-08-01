# ShotFlow — AI 视频连续性编译器与 Benchmark

**从真实结果编译下一镜头，再验证它是否真的接上了。**

> 模型说它续上了，ShotFlow 负责检查它是否真的续上。

[English](README.md) · [案例](examples/) · [Skill](skills/shotflow/) · [Schema](schemas/) · [Pro 边界](PRO.md)

![《天幕修补师》已接受的 Clip 01，由小云雀 / Seedance 2.0 生成](examples/sky-mender/evidence/clip-01-preview.gif)

## 当前证据状态

ShotFlow v0.2 Core 已实现并可测试。三组真实 Seedance Clip 01 已经生成、
接受、观察并记录哈希。两组受控 Clip 02 A/B 已完成盲评，结果都是
**普通组获胜**。因此目前不宣称 ShotFlow 已提升连续性；失败结果保留为证据，
并已推动 `provider-direct-v3` 编译器修订。v3 目前仅完成离线验证，尚未授权
付费生成。

| 案例 | 作用 | 当前状态 |
| --- | --- | --- |
| 天幕修补师 | 旗舰视觉奇观 | Clip 02 v1 落败；v2 改善动作连续性但未完成关键结尾，案例已拒绝并冻结 |
| 暴风甲板 | 现实动作 | Lovart 的 Kling O1 与两条 Seedance 2.0 普通组均被拒绝；修正交接仍发生首帧断裂，案例在尝试上限处关闭 |
| 黑曜之息 | 虚构产品广告 | `anchor-frame-v1` 两组均返回 1920×1080；三名盲评一致选择普通组，ShotFlow 组拒绝且不重试 |

所有已接受 Clip 01 原始视频均为 1920×1080、24fps、5.125 秒，并保留平台
容器级 `AIGC Label=1`。Lovart Gate 6 两个输出同为 1920×1080，但容器没有
AIGC 标识，因此任何公开衍生版本都必须增加可见披露。见
[《天幕修补师》盲评](examples/sky-mender/reviews/clip-02-blind-review-v1.md)、
[《黑曜之息》盲评](examples/obsidian-bloom/reviews/clip-02-blind-review-anchor-v1.md)
与[已关闭的 Gate 2 清单](examples/GATE_2_APPROVAL.md)。

标准非 VIP 模型 `seedance2.0_direct` 因不支持 1080p 已停止。Gate 4 随后
改用用户选择的 `seedance2.0_vision` VIP 模型与 1080p。第一条任务因账号
积分不足结束；每日积分刷新后，经过一次明确批准的重试获得了有效视频，
但裂缝最终仍未封闭，也没有在修复后出现黎明，因此结果被拒绝，《天幕修补师》
停止重试并冻结。后续生成转到 Lovart，但平台与模型继续分开记录：Kling O1
因故事动作推进不足被拒绝；Lovart 路由的 Seedance 2.0 虽完成后半段动作，
首帧却丢失人物并把箱子放到错误一侧，同样被拒绝。修正后的交接合同把已接受
最终帧固定为第一个权威附件并排除线程历史产物；Lovart 在文字中确认了角色，
但重试仍重复首帧断裂，实际分辨率也只有 720p，而不是批准的 1080p。该结果在
第 5 次尝试上限处被拒绝。当前没有任何剩余案例获得无人值守生成授权。见
[已关闭的《暴风甲板》定向重试闸门](examples/GATE_4_STORM_DECK_BASELINE_APPROVAL.md)。
下一套已登记机制是 `anchor-frame-v1`：Provider 尚未证明引用角色可靠时，
只提交已接受的最终帧，不提交源视频。《黑曜之息》普通组与 ShotFlow 组已冻结
相同的唯一媒体参考。Lovart 不提供分辨率选项，因此两组如实记录平台原生输出，
最低接受 1280×720，不做超分；质量优先继续固定标准 Seedance 2.0，排除 Fast
与 Mini。普通组实际返回 1920×1080 并通过首帧门禁；随后单独批准的 ShotFlow
组也返回 1920×1080，但瓶盖侧翻、外置液滴掉落，琥珀光带还错误连接瓶底/液面。
三名视觉盲评一致选择普通组（`9.67/12` 对 `3.33/12`），因此 ShotFlow 组被拒绝
且不重试。

## 它解决什么

常见工作流会根据原始计划预写 Clip 02。但 Clip 01 的真实结果经常偏离计划：道具换手、衣服破损、机位越轴、光源变化，或者动作停在意料之外的位置。

ShotFlow 把已接受的视频当作事实源：

```text
计划 Clip 01
    ↓
生成并接受真实结果
    ↓
观察人物 · 道具 · 空间 · 动作 · 光线 · 剧情
    ↓
比较计划与真实状态
    ↓
从真实终点编译 Clip 02
    ↓
验收动作承接与连续性
```

它不是电影感形容词或导演姓名合集，而是一套连续性编译器与证据优先的
Benchmark。

## 60 秒开始

需要 Python 3.10+，运行时零第三方依赖。

```bash
git clone https://github.com/ruhang365/ruhang365-shotflow.git
cd ruhang365-shotflow
python3 -m pip install .

shotflow init my-sequence --title "我的连续镜头"
shotflow --help
```

不安装也可以从仓库直接运行：

```bash
python3 skills/shotflow/scripts/shotflow.py --help
```

安装到 Codex：

```bash
mkdir -p ~/.codex/skills
cp -R skills/shotflow ~/.codex/skills/shotflow
```

其他使用目录式 Skill 的 Agent 也能复用，但发现路径可能不同。

## 核心命令

```text
shotflow init
shotflow plan
shotflow observe
shotflow diff
shotflow compile-next
shotflow score
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
- [`Ordered Sequence` v1](schemas/ordered-sequence.schema.json)：定义五个连续计时的正向状态、精简观察锚点和逐阶段视觉验收条件。
- [`Provider Handoff` v1](schemas/provider-handoff.schema.json)：固定参考素材角色、提交 Prompt 哈希、历史产物排除规则和首帧门禁。`anchor-frame-v1` 只使用已接受终点；只有 Provider 已证明能可靠绑定“仅作上下文”的源视频时，才使用 `video-context-v1`。
- 五轴电影语法：叙事时刻、镜头运动、光线色彩、空间构图、材质物理。
- 六项连续性量表：人物身份、服装道具、空间方向、动作承接、光线材质、故事节拍。

真实观察始终覆盖计划状态。没有完整观察，不得输出 `continuity_safe=true`。

新的 `compile-next` 默认使用 `provider-direct-v3`：JSON 合同保留完整观察和
五项 `visual_test`，服务商 Prompt 只发送
`match → continue → initiate → resolve → hold` 五个正向状态、精简锚点和完整五轴电影语法，并强制不超过 2400 字符。

## 公平 A/B

每组案例都遵守：

1. 在 Clip 01 生成前冻结普通方法的 Clip 02 Prompt；
2. 只接受一个 Clip 01 作为共同起点；
3. 用一个冻结的 Provider Handoff profile 绑定 Clip 01 的真实终点；
4. 普通组与 ShotFlow 组使用相同模型、参数、profile 和参考素材；
5. 唯一变量是 Clip 02 是否读取真实观察；
6. 评分时隐藏组别。

只有 ShotFlow 在至少两组案例中获得多数胜出，且平均分提升至少 20 分，才会公开宣称连续性改善。

## Core 与 Pro

公开 Core 已包含完整的人工连续性工作流，不依赖会员或云服务。未来 Pro 只负责自动读取视频，生成带时间证据和置信度的 ObservationPatch。

达到 200 Stars 或 5 名真实 Core 测试者后才启动 Pro Beta；现在不创建空私库。

## 原创与许可

ShotFlow 的代码、Prompt、电影语法、案例和工作流均为洁净室原创。项目会把 [`zy-cinematic-realism`](https://github.com/popopo-99/zy-cinematic-realism) 列为结构化电影提示设计的 prior art，但不复制或改写其 CC BY-NC 文件、导演卡片、文本、代码与素材。

- 代码、Skill、Schema、模板：Apache-2.0。
- 原创文档与案例媒体：在可主张权利的范围内使用 CC BY 4.0。
- AI 生成内容保留法规及平台要求的标识。
- 开源许可不授予入行365商标权。

贡献前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。90 天目标为 1,000 Stars、20 个外部公开作品和 3 名代码或适配器贡献者。
