# First-use Diagnostic

当 profile 不存在时，立刻用简短说明 + 第一个场景开始。不讲理论、不让用户先配置所有偏好。

诊断是三个 mini 场景，共约 7–9 个用户回合。

## Scenario 1: Enter the Conversation

观察：

- Opening
- Self-introduction & Hook
- 基础 Listening & Reaction

场景含一个共享环境线索 + 一个让对方自然问“你在做什么”的机会。

## Scenario 2: Develop a Thread

观察：

- Listening & Reaction
- Threading
- Story Development
- Reciprocity

对方在数轮中提供分层信息。用户需注意到有潜力的线索，而非机械采访。

## Scenario 3: Respond to Friction

观察：

- Recovery & Exit
- 弱投入下的 Threading
- 边界尊重

场景含短回答、分心、兴趣消退、或被打断。正确结果可能是换线或体面离场，而非强行延续。

## 诊断定位

诊断是抽样，不是认证。只有实际达到阈值才可设 `Emerging` 或 `Developing`；绝不设 `Reliable`。观察不足的能力保持 `Unassessed`。

## 结束输出

- 一个观察到的强项
- 一个最高杠杆成长点
- 初始阶段摘要
- 推荐的首个训练重点
- 邀请开始该练习

## 初始 profile 行为

初始 profile 只含诊断中实际观察到的证据；未观察能力为 `Unassessed` 且 `evidence: []`。设置 `diagnostic.status: "complete"` 与 `completed_at`。`recent_sessions` 追加一条 `mode: "diagnostic"`、`focus: "baseline"` 的记录。初始 profile 不含 `Reliable` 阶段。
