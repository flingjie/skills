# Persona Tailoring

One insight, re-expressed per role. The underlying problem is the same; the
consequence that matters changes by who is listening.

## Principle

Do not change the insight — change which consequence you lead with. Each role
cares about a different failure mode of the same problem.

## Role → frame

| Role | Leads with |
|------|-----------|
| CTO | System / architecture / observability / engineering risk |
| CEO | Scale / economics / strategic exposure |
| Product Manager | Prioritization / where to invest / which failures matter |
| CFO / buyer | Cost structure / ROI / risk of overspend |
| Ops / line lead | Day-to-day friction / headcount / service quality |

## Worked example

Insight (one underlying claim): the bottleneck is not the model's accuracy but
the inability to record, classify, and reproduce failure modes.

- **CTO** — 从系统角度，这不是 Prompt Engineering 问题，而是缺少 Agent Runtime
  Observability。
- **CEO** — 如果 Agent 每增加一个业务场景，都需要线性增加人工维护成本，那么 AI
  并没有真正产生规模效应。
- **Product Manager** — 当前最大的问题可能不是 Agent 能不能回答，而是团队不知道
  哪些失败最值得优先优化。

## How to tailor

1. Identify the role (`contact.role`).
2. Ask: what does this role get blamed for if this problem persists?
3. Lead the reframe with that consequence.

Do not fabricate a persona-specific pain the customer never mentioned. If the
role is unknown, present the insight role-neutrally and list which consequence
each role would care about most.
