# Example: AI Agent Sales

A worked Challenger Sales Brief for a customer who says they want an AI Agent to
improve customer service. Illustrative — adapt names and numbers to the real
deal.

## Input

```yaml
customer:
  company: 某电商平台
  industry: 电商
contact:
  role: CTO
context:
  conversation: |
    客户表示他们想做一个 AI Agent，目前主要问题是客服人员成本越来越高。
product:
  description: |
    Agent 开发与运行平台，支持 Agent 构建、观测、评估和 Replay。
goal:
  objective: reframe
```

## 1. Surface Demand

客户明确提出：想用 AI Agent 降低客服人力成本。

## 2. Current Thinking

客户当前认为：客服效率低，是因为"人工客服数量不足"，所以加一个 AI Agent 就好。

## 3. Hidden Problem

- 运营层：客服重复处理大量相似问题，但复杂问题仍要靠人。
- 结构层：企业知识没有结构化，SOP 依赖人工经验，问题处理无法复用。
- 根因：知识分散、SOP 依赖个人经验、失败案例无法沉淀。
- 不行动的成本：人员规模随业务线性增长、服务质量不稳定、新员工培训成本上升。

## 4. Assumptions to Challenge

| 客户假设 | 风险 | 挑战方向 |
|---|---|---|
| AI 客服数量越多，效率越高 | 错误回答会被规模化放大 | 数量不是瓶颈，可复用的知识才是 |
| Prompt 优化能解决准确率 | 无法定位真实失败原因 | 失败不可复现，Prompt 只能反复试错 |
| 部署 Agent 就算完成 AI 转型 | 缺乏持续评估和优化机制 | 上线只是开始，没有 Learning Loop |

## 5. Commercial Insight

> 很多团队认为 Agent 项目的主要问题是模型准确率，但实际导致 Agent 无法规模化的，
> 通常不是模型能力，而是团队无法系统记录、分类和复现 Agent 的失败模式。
>
> 因此真正的问题不是"如何继续优化 Prompt"，而是"如何建立 Agent 的 Evaluation
> 和 Learning Loop"。

## 6. Problem Reframe

从：如何增加一个 AI 客服。

转变为：如何把企业知识和问题处理流程，转化为一个可持续优化的自动化决策系统。

## 7. Challenger Narrative

### Warmer
最近很多 AI 客服团队都遇到一个类似问题：Agent 上线后，反而需要更多人来盯它的回答。

### Reframe
大多数团队认为问题是 Prompt，但实际上 Prompt 往往只是问题暴露的位置。

### Rational Drowning
如果每次 Agent 出错都依赖人工排查，随着 Agent 数量增加，Debug 成本会呈非线性增长。

### Emotional Impact
最终工程师每天都在重复：查看 Trace → 猜测失败原因 → 修改 Prompt → 重新运行 → 出现新的问题。

### New Way
真正需要的是：Observe → Classify → Replay → Evaluate → Learn。

### Solution
我们的平台提供了这套 Evaluation 和 Learning Loop 的运行时能力。

## 8. Tailored Message

针对 CTO：从系统角度，这不是 Prompt Engineering 问题，而是缺少 Agent Runtime
Observability。

## 9. Deal Advancement

当前阶段：problem_validation。下一步目标：让客户确认瓶颈是"失败不可复现"而非"模型不够准"。
建议行动：用一个真实客服失败案例，现场演示"记录 → 复现 → 定位"三步。

## 10. Questions

1. 你们现在一个客服 Agent 出错了，从发现到定位大概要多久？
2. 目前你们是怎么记录和分类 Agent 的失败案例的？
3. 如果下个月 Agent 数量翻倍，维护人力的投入会怎么变？
