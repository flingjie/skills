# Mode Contracts

七个训练模式各自的契约。每个模式定义：训练能力、回合范围、教练时机、完成条件、retry 节点、可记录证据与禁止推断。

所有模式共享 competency-model 的阶段与证据规则。模式本身没有独立等级或分数。

## Full Conversation

- 主能力：Reciprocity、Threading、Listening & Reaction；可观察 Opening、Story Development、Recovery & Exit。
- 建议回合：8–12 个用户回合。
- 教练时机：默认全程入戏；实时教练仅当用户请求、求助、明显卡住或场景自然结束时出现。
- 完成条件：达到场景自然结束点（人物目标达成、兴趣消退、时间压力或用户选择离场），或用户要求结束。
- Retry 节点：复盘时标记的最后一个有改进空间的节点。
- 可记录证据：实际观察到的行为；跨多个能力的证据分别记录。
- 禁止推断：未在对话中出现的证据；把一次成功当作 `Reliable`。

## Opening Drill

- 主能力：Opening；次能力：Self-introduction & Hook、Listening & Reaction。
- 建议回合：1–2 个用户回合。
- 教练时机：首轮回应后可立即评价，因为评价属于本模式契约。
- 完成条件：用户给出开场后完成评价与一次可选 retry。
- Retry 节点：开场那一轮。
- 可记录证据：开场的实际措辞所展示的行为；共享情境或当下观察的开场。
- 禁止推断：仅凭人物背景推断用户开场意图。

## Follow-up Drill

- 主能力：Threading；次能力：Listening & Reaction、Story Development。
- 建议回合：3–4 个用户回合。
- 教练时机：每轮结束后可给一句方向反馈，但不逐句重写。
- 完成条件：线索被跟进或明确换线，且完成评价与 retry。
- Retry 节点：questionnaire_mode 或 thread_dropped 出现的那一轮。
- 可记录证据：线索跟进、措辞连接、及时换线；反向：questionnaire_mode、thread_dropped。
- 禁止推断：把多个话题当作多条线索；把换线推断为放弃对话。

## Story Mining

- 主能力：Story Development；次能力：Threading、Reciprocity。
- 建议回合：4–6 个用户回合。
- 教练时机：人物提供分层信息后、用户机械提问时，或请求提示时。
- 完成条件：一次有效的 depth advance，或人物明确婉拒后用户尊重边界。
- Retry 节点：mechanical_why 或 depth_forced 出现的那一轮。
- 可记录证据：从事实推进到经历/动机/转变；上下文敏感提问；识别叙事潜力；尊重婉拒。
- 禁止推断：把追问次数当作深度；把婉拒后的停顿推断为失败。

## Self Introduction

- 主能力：Self-introduction & Hook；次能力：Opening。
- 建议回合：1 个用户回合。
- 教练时机：自我介绍后立即评价。
- 完成条件：用户给出自我介绍，完成评价与一次可选 retry。
- Retry 节点：自我介绍那一轮。
- 可记录证据：清晰解释、问题型 hook、开放环；反向：resume_dump。
- 禁止推断：从用户职业背景推断身份；把流畅度推断为连接质量。

## Conversation Recovery

- 主能力：Recovery & Exit；次能力：Threading、边界尊重。
- 建议回合：2–4 个用户回合。
- 教练时机：在人物给出弱线索或离场信号后提供反馈；信号出现前保持入戏。
- 完成条件：用户正确选择 follow / switch / pause / exit，或场景自然结束。
- Retry 节点：forced_continuation 或 signal 误读的那一轮。
- 可记录证据：signal_read、appropriate_response、graceful_exit、minor_repair；反向：forced_continuation。
- 禁止推断：把对方想离开推断为用户失败；把体面离场推断为未完成。

## Random Challenge

- 主能力：模式轮换，通常覆盖 Reciprocity、Recovery & Exit、Threading。
- 建议回合：3–6 个用户回合。
- 教练时机：按所选模式契约；随机事件出现时可在事件后给一句方向反馈。
- 完成条件：所选挑战的目标完成或用户结束。
- Retry 节点：随机事件中表现最弱的那一轮。
- 可记录证据：仅当实际行为匹配行为代码时才记录；跨能力分别记录。
- 禁止推断：把突发事件的意外感当作能力证据。

## 结束与提前退出

- 用户提前结束：只记录行为已支持的观察，session 标记 `interrupted`；复盘只覆盖已发生内容，不生成完整会话结论。
- 人物自然离开：按 simulation-rules 的自然结束条件执行；允许体面离场，不强行延续。
- 两种结束都保留已披露信息边界，不补造人物内心独白。

## 显式模式优先

用户明确指定的模式永远优先于自适应路由。即使 profile 的 focus 指向其它能力，也只在该模式内调整场景、难度与 focus 表述；不得改路由到别的模式。唯一例外：请求的模式无法训练所述目标时，只问一个简洁澄清问题。

## 诊断不是模式

Diagnostic 是首次使用的编排流程（三个 mini 场景），不是第八个用户可选训练模式。`/social-gym diagnostic` 不在模式索引中；无 profile 时自动进入，有 profile 时用普通自适应路由。
