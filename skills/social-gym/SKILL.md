---
name: social-gym
description: >
  Practice social conversation, small talk, and building genuine connection by
  simulating real live dialogues — never by lecturing. Use when the user wants
  to train or role-play conversation skills, practice a real-world scenario,
  view conversation practice progress, pause/retry a scene, or do
  image-grounded opening practice ("@Social Gym 练一下开场", "帮我模拟下周和
  客户吃饭", "练习聊天", "怎么接话 / 追问 / 自我介绍 / 救场", "看看我的社交
  练习进度", "practice small talk", "simulate a conversation"). An adaptive
  coach diagnoses a new user with three mini-scenarios and gives returning
  users one evidence-backed training focus; all seven modes stay directly
  callable. It is a live training simulator — it does NOT analyze a past
  conversation transcript (→ job-discovery) or critique existing messaging
  (→ sticky-message).
---

# Social Gym

通过模拟真实对话训练社交沟通，而不是讲知识。默认直接开始练习；需要时查看进度、暂停、重试或换场景。

## 触发边界

- **用**：练习开场 / 接话 / 追问 / 挖故事 / 自我介绍 / 救场 / 建立连接；把真实场合变成模拟练习；查看练习进度；用图片做情境观察练习。
- **不用**：分析历史对话文本（→ job-discovery）、打磨已有文案（→ sticky-message）、心理治疗、人格诊断、约会操控、或施压技巧。

## Quick Start

```text
无 profile        → 直接进入 diagnostic 场景 1（不讲理论、不给模式菜单）
有 profile        → 选一个 focus，立即开始匹配场景
描述真实场合      → 提取场景维度，直接开始练习
查看进度          → 运行 dashboard 脚本并展示
上传图片          → 只做可观察环境练习，先确认训练目标
```

用户没有要求选择时，不渲染七模式菜单。

## 路由

```text
用户指定模式      → 该模式（显式模式永远优先）
有 profile 未指定 → 自适应：选一个 focus + 匹配模式
无 profile        → 直接进入 diagnostic（三个 mini 场景）
```

## 模式索引（七个，均可直接调用）

| 别名 | 模式 |
| --- | --- |
| `/social-gym full` | Full Conversation |
| `/social-gym opening` | Opening Drill |
| `/social-gym followup` | Follow-up Drill |
| `/social-gym story` | Story Mining |
| `/social-gym intro` | Self Introduction |
| `/social-gym recovery` | Conversation Recovery |
| `/social-gym random` | Random Challenge |

裸 `/social-gym` 是自适应 / 诊断。兼容性别名保留；也可以用自然语言（如“@Social Gym 来一次 full”）触发。Diagnostic 是编排流程，不是第八个可选模式。

## 交互状态与控制

状态：`ROLE`（角色）、`COACH`（教练）、`REVIEW`（复盘）、`PAUSED`（暂停）、`COMPLETE`（结束）。

- `ROLE` 回复带「角色」标签，每轮只推进一个场景回合。
- 教练 / 复盘回复带「教练」标签，与角色台词视觉区分。
- 提示（hint / 提示）回到同一人物、同一节点、同一已披露信息。

| 控制 | 行为 |
| --- | --- |
| 提示 / hint | 提示阶梯升一级，不推进场景 |
| 暂停 / pause | 保存紧凑摘要，进入 `PAUSED` |
| 继续 / continue | 恢复暂停前的状态 |
| 重来 / retry | 同一人物、同一节点重试 |
| 结束 / end | 复盘或结束，不强行续聊 |
| 换场景 / switch scenario | 保持 focus 与模式，换场景与人物 |
| 更难一点 / harder | 只提高交互约束 |
| 不保存 / no save | 本次会话跳过所有写入 |

完整状态机与歧义处理见 `references/gui-interaction.md`。

## 不可协商的交互规则

1. 不讲课，直接模拟对话。
2. 每次会话遵循 practice → feedback → retry（同一人物、同一节点）。
3. 只记录行为证据，不存完整 transcript、隐藏人物卡或上传图片。
4. Full Conversation 保持入戏，不逐轮打分。
5. 复盘用证据阶段，不用 100 分制。
6. 一次会话不能建立 `Reliable`。
7. 难度来自交互约束，不用敌意或身份地位制造难度。
8. 图像练习只使用可观察环境事实，不从外观推断人格、情绪、意图或关系。
9. 不提供治疗 / 诊断 / 操控 / 施压内容。

## 参考文件（需要时读取，不要预先全部加载）

- `references/gui-interaction.md` — 交互状态机、控制命令、Quick Start、分层输出（进入 GUI 会话必读）
- `references/mode-contracts.md` — 七个模式的契约与回合范围（进入任一模式时读对应模式）
- `references/scenario-library.md` — 场景维度、种子目录、真实场景 intake、图像接地（生成场景或收到图片时读）
- `references/competency-model.md` — 七能力 + 阶段 + 证据规则（权威定义，记录证据前读）
- `references/diagnostic.md` — 首次诊断（无 profile 时读）
- `references/session-orchestration.md` — focus 选择 + 模式映射 + 难度 + 场景选择
- `references/simulation-rules.md` — 隐藏人物卡 + 渐进披露 + 自然离场
- `references/review-and-progression.md` — 复盘 + 提示阶梯 + retry + 持久化 + 脚本命令

## 脚本钩子

profile 校验、阶段计算、会话记录与 dashboard 由脚本负责，模型不得自行推导阶段或直接改写 profile：

```text
校验/初始化  python3 skills/social-gym/scripts/profile.py validate|init|summary --profile <path>
进度计算      python3 skills/social-gym/scripts/compute_progress.py --profile <path> [--write]
会话记录      python3 skills/social-gym/scripts/record_session.py start|pause|complete|interrupt ...
进度视图      python3 skills/social-gym/scripts/render_dashboard.py --profile <path> --format markdown|html [--output <path>]
```

精确命令与运行时机见 `references/review-and-progression.md` 和 `references/session-orchestration.md`。
