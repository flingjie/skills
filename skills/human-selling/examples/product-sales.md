# Example: Product Sales

A worked example — selling an Agent platform to a customer who asked for a
Multi-Agent system. Illustrative.

## Situation

客户说："我们需要一个 Multi-Agent 系统。" 联系人：CTO，企业正在规模化 Agent 应用。

## Other Person Model

- 角色：CTO
- 目标：让 Agent 应用稳定规模化
- 痛点：单 Agent 任务失败后难定位
- 约束：已有部分自建能力
- 担忧：再引入新平台可能推倒重来

## Real Problem Hypothesis

- 表面：需要 Multi-Agent
- 可能根因：单 Agent 复杂任务不可控 / 任务需要分工 / workflow 缺乏可观测性
- 置信度：low

## Recommended Strategy

不要直接介绍 Multi-Agent 能力。先问一个澄清问题，判断"需要 Multi-Agent"到底是
任务分工需求，还是稳定性和可观测性需求。

## Suggested Conversation

> 你们考虑 Multi-Agent，是因为单 Agent 已经无法完成任务，还是主要希望提升复杂
> 任务的稳定性？

（若客户说"任务失败后很难定位"——）

> 明白。那可能真正的问题不是"再叠加一层 Multi-Agent"，而是先让每一个 Agent 的
> 执行过程可观测、可回放。我们做的 Execution Trace + Replay，正好是这一层。

## Next Best Question

> 现在一个 Agent 执行失败了，你们从发现问题到定位根因，通常要多久？
