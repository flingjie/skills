# Competency Model

这是唯一权威定义：七个可训练能力、行为代码分类、掌握阶段、证据规则。
其它文件引用这里，不得重复定义同一行为。阶段与证据规则被每个模式共享，避免同一行为在不同 drill 里被冲突解读。

## 能力与可观察行为

每条能力列出正向与反向（counter）行为代码。`behavior_code` 必须来自下表。

### 1. Opening

正向：

- `situational_open` — 使用共享情境或当下观察开场
- `low_pressure_open` — 对方容易接话，不要求对方自我暴露
- `context_matched_open` — 与场景、关系距离匹配

反向：

- `rehearsed_pitch` — 背稿式开场、强行抖机灵

### 2. Listening & Reaction

正向：

- `acknowledge_before_ask` — 先接住对方刚说的话
- `react_before_ask` — 提问前先反应
- `reflect_meaning` — 复述情绪或情境含义，不过度解读

反向：

- `question_jumping` — 把回答当作无关问题的跳板
- `no_reaction` — 无任何反应直接抛下一个问题

### 3. Threading

正向：

- `thread_followed` — 注意到一条活的线索并跟进
- `wording_connected` — 下一条回应接住对方原话
- `thread_switched_well` — 当前线索没能量时及时换线

反向：

- `questionnaire_mode` — 跳到问卷式提问而非跟进线索
- `thread_dropped` — 忽略一条明显线索

### 4. Story Development

正向：

- `depth_advanced` — 从事实推进到经历 / 动机 / 转变 / 转折点
- `context_sensitive_prompt` — 用贴合上下文的提问，而非重复“为什么”
- `story_potential_seen` — 识别到情绪或叙事潜力

反向：

- `mechanical_why` — 机械重复“为什么？”
- `depth_forced` — 对方婉拒时仍强行挖深度

### 5. Reciprocity

正向：

- `balanced_share` — 分享相关自我而不抢话
- `ack_explore_share_return` — 使用 acknowledge → explore → share → return
- `room_left` — 给对方回问或转向的空间

反向：

- `interview_mode` — 只问不分享的采访模式
- `conversation_hijack` — 过早把话题转向自己

### 6. Self-introduction & Hook

正向：

- `clear_explanation` — 用对方听得懂的语言说清自己在做什么
- `hook_with_problem` — 包含有意思的问题或观点
- `open_loop` — 留下自然的开放环

反向：

- `resume_dump` — 简历 / 技术清单式倾倒

### 7. Recovery & Exit

正向：

- `signal_read` — 区分弱线索 vs 想离场
- `appropriate_response` — 按信号选择 follow / switch / pause / exit
- `graceful_exit` — 体面结束
- `minor_repair` — 修复小尴尬而不反复道歉

反向：

- `forced_continuation` — 强行延续本应结束的对话

## 结果指标 (Outcome Indicators)

`Curiosity`、`Naturalness`、`Connection` 是结果语言，不是独立训练轨道。它们由上面七项可观察能力推断，不设独立等级、不产生重复证据。

## 能力键 (Canonical Keys)

profile 中使用这些键：

```text
opening
listening_reaction
threading
story_development
reciprocity
self_introduction
recovery_exit
```

`current_focus` 也使用这些键。

## 掌握阶段

```text
Unassessed → Emerging → Developing → Reliable
```

- `Unassessed`：观察不足。
- `Emerging`：至少出现一次相关正向行为，但是被辅助、孤立、或不一致。
- `Developing`：行为在多个不同情境中独立出现。
- `Reliable`：行为在多种模式、情境、难度约束下保持。

## 证据记录

```json
{
  "session_id": "2026-08-21T19:30:00Z-opening-01",
  "observed_at": "2026-08-21T19:33:00Z",
  "competency": "threading",
  "polarity": "positive",
  "behavior_code": "thread_followed",
  "behavior": "Reacted to the career-change clue and followed that thread instead of jumping to company facts.",
  "mode": "full_conversation",
  "difficulty": "normal",
  "scenario_tags": ["meetup", "stranger", "career-change"],
  "attempt": "retry",
  "assistance": "attention_hint"
}
```

字段约束：

- `polarity`：`positive` | `counter`
- `attempt`：`first` | `retry`
- `assistance`：`none` | `attention_hint` | `strategy_hint` | `direction_examples` | `full_example`
- `behavior_code`：必须来自上文七项能力分类
- `behavior`：行为摘要，不是完整 transcript；不默认持久化完整原话

## 情境类别 (Scenario Category)

一个“不同情境类别”是 **setting + relationship distance + interaction constraint** 的唯一组合，例如 `meetup + stranger + open`，而不是同一社交情境下的不同话题。这防止靠换话题表面变化就满足跨情境掌握阈值。

## 阶段转换（确定性）

- `Unassessed → Emerging`：≥1 条相关正向证据。
- `Emerging → Developing`：≥3 条正向，其中 ≥2 条 `attempt: first` 且 `assistance: none`，且跨越 ≥2 个不同情境类别。
- `Developing → Reliable`：≥5 条 `attempt: first` 且 `assistance: none` 的正向，跨越 ≥3 个情境类别且 ≥2 个模式；且该能力最新 3 条观察中 ≥2 条正向、无重复 counter `behavior_code`。

`full_example` 之后的证据只代表“参与了练习”，不能作为独立证据。教练未提供措辞的成功 retry 是正向学习证据，但不计入 first-attempt 独立证据。

## 反向证据与复核 (Reconfirmation)

- 单条 counter 永不降低阶段。
- 最新 3 条观察中出现 2 条相同 `behavior_code` 的 counter → 该能力 `needs_reconfirmation: true`。
- 该能力成为未来会话优先项，但保留当前阶段。
- 复核在 2 条 `attempt: first`、`assistance: none` 的正向证据（跨 2 个不同情境）后清除。这防止一个坏日子抹掉进度，同时仍能检测退步。

## 保留上限

每个能力最多保留最新 20 条证据。阶段与复核计算只用保留的证据。
