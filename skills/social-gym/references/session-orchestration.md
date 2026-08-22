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

## 场景选择

- 用 scenario-library 的维度生成场景，不逐字复用最近 5 个会话的 setting。
- 最近 3 个会话不重复同一 persona pattern。
- 自适应路由优先选择抽样不足的情境类别；真实场景 intake 优先于种子目录。
- 每次开始前输出 transfer card：开场锚点、可能线索、一个要避免的行为、出口选项。

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
- 暂停：保存 `active_session`（mode / status / turn / focus / scenario tags / difficulty / 紧凑 resume summary），不存完整 transcript。
- 恢复：只用紧凑 summary 重建同一人物身份、已确立事实、当前节点与已披露信息边界。
- 不保存：跳过所有 profile 写入，报告会话仅在内存中。

## 脚本生命周期钩子

```text
开始会话前      python3 skills/social-gym/scripts/profile.py validate --profile state/social_gym_profile.json
会话开始/暂停   python3 skills/social-gym/scripts/record_session.py start|pause --profile ... --session ...
会话结束        python3 skills/social-gym/scripts/record_session.py complete --profile ... --session ... --evidence ...
中断            python3 skills/social-gym/scripts/record_session.py interrupt --profile ... --evidence ...
查看进度        python3 skills/social-gym/scripts/render_dashboard.py --profile ... --format markdown|html
```

脚本是 profile 校验、阶段计算、记录与 dashboard 的权威实现；模型不得自行推导阶段或直接改写 profile。完整命令见 review-and-progression.md。
