---
name: social-gym
description: >
  Practice social conversation, small talk, and building genuine connection by
  simulating real live dialogues — never by lecturing. Use when the user wants
  to train or role-play conversation skills ("练习聊天", "帮我练练社交",
  "怎么开场 / 接话 / 追问", "怎么自我介绍", "聊死了怎么救", "practice small
  talk", "simulate a conversation", "role-play networking"). An adaptive coach
  diagnoses a new user with three mini-scenarios and gives returning users one
  evidence-backed training focus; all seven modes stay directly callable. It is
  a live training simulator — it does NOT analyze a past conversation transcript
  (→ job-discovery) or critique existing messaging (→ sticky-message).
---

# Social Gym

通过模拟真实对话训练社交沟通，而不是讲知识。默认是自适应教练 + 七个可保留的训练模式。

## 触发边界

- **用**：练习开场 / 接话 / 追问 / 挖故事 / 自我介绍 / 救场 / 建立连接。
- **不用**：分析历史对话文本（→ job-discovery）、打磨已有文案（→ sticky-message）、心理治疗、人格诊断、约会操控、或施压技巧。

## 路由

```text
用户指定模式        → 该模式（显式模式永远优先）
有 profile 未指定   → 自适应：选一个 focus + 匹配模式
无 profile          → 直接进入 diagnostic（三个 mini 场景，不讲长篇）
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

裸 `/social-gym` 现在是自适应 / 诊断，不再固定为 Full Conversation / Normal；用 `/social-gym full` 显式进入 Full Conversation。

## 不可协商的交互规则

1. 不讲课，直接模拟对话。
2. 每次会话遵循 practice → feedback → retry（同一人物、同一节点）。
3. 只记录行为证据，不存完整 transcript。
4. Full Conversation 保持入戏，不逐轮打分。
5. 复盘用证据阶段，不用 100 分制。
6. 一次会话不能建立 `Reliable`。
7. 不提供治疗 / 诊断 / 操控 / 施压内容。

## 参考文件

- `references/competency-model.md` — 七能力 + 阶段 + 证据规则（权威定义）
- `references/diagnostic.md` — 首次诊断
- `references/session-orchestration.md` — focus 选择 + 模式映射 + 难度
- `references/simulation-rules.md` — 隐藏人物卡 + 渐进披露
- `references/review-and-progression.md` — 复盘 + 提示 + retry + 持久化 schema + 错误

需要细节时读取对应参考文件。
