# Session Orchestration

## 默认调用流程

```text
Load profile
  ↓
缺 profile? ── 是 → diagnostic
  ↓ 否
选一个 focus
  ↓
选 mode / difficulty / persona / scenario
  ↓
宣布一个行为目标
  ↓
跑练习
  ↓
复盘一个强项 + 一个最高杠杆错失
  ↓
同一节点 Retry
  ↓
对比行为
  ↓
持久化证据与下一个 focus
```

## Focus 选择优先级

1. 用户明确要求的能力；
2. `needs_reconfirmation: true` 的能力；
3. 有足够证据、处于最低阶段、且能识别出重复弱点的能力；
4. 尚未抽样过的 `Unassessed` 能力；
5. 最久未训练的能力。

平局时：优先用户偏好的真实场景，其次模式与情境多样性。

## 模式映射

- Opening → Opening Drill 或 Full Conversation
- Listening & Reaction → Follow-up Drill 或 Full Conversation
- Threading → Follow-up Drill / Story Mining / Full Conversation
- Story Development → Story Mining 或 Full Conversation
- Reciprocity → Full Conversation 或 Random Challenge
- Self-introduction & Hook → Self Introduction 或 Full Conversation
- Recovery & Exit → Conversation Recovery 或 Random Challenge

规划器在有其它合适模式时，不得连续 3 次自适应会话选择同一模式。

## 显式模式调用

用户指定模式时，该选择优先。教练可在该模式内调整 scenario / focus / difficulty。可简短说明所选 focus，但不得改路由到别的模式；除非该模式无法训练所述目标，此时只问一个简洁澄清问题。

## 难度选择

- 新能力或 `Emerging`：Easy 或 Normal。
- `Developing`：通常 Normal，偶尔 Hard 做迁移测试。
- `Reliable`：Hard 或 Expert 用于复核与泛化。
- 反复 counter 之后：只降低隔离该技能所需的交互约束，不自动把整个场景降为 Easy。

难度在会话之间变化，不在会话中途随意变，除非 Random Challenge 明确含突发事件。

## 会话生命周期

- 正常结束：持久化证据 + 更新 `current_focus` + 追加 `recent_sessions`。
- 提前退出：只保存行为已支持的观察，标记 `interrupted`，不生成完整会话结论。
