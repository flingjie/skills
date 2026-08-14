# Problem Finding

The most important part of human selling. Do not accept the stated problem as
the real one.

## The layers

```text
Stated Problem
      ↓
Symptoms
      ↓
Underlying Cause
      ↓
Real Constraint
      ↓
Job To Be Done
```

## Worked example

客户说：

> 我们需要一个 Multi-Agent 系统。

Do NOT immediately respond "our Multi-Agent supports…". Instead hold multiple
hypotheses:

- 单 Agent 无法处理复杂任务？
- 任务流程不可控？
- 现有 Agent 不稳定？
- 团队需要任务分工？
- 想降低人工成本？

## Output model

```yaml
problem_analysis:
  stated_problem:
    "需要 Multi-Agent"

  possible_root_problems:
    - 单 Agent 任务复杂度过高
    - Agent 执行不可控
    - 任务需要不同专业能力
    - Workflow 缺乏可观测性

  confidence:
    low

  next_discovery_question:
    "你们考虑 Multi-Agent，是因为单 Agent 已经无法完成任务，
     还是主要希望提升复杂任务的稳定性？"
```

## Rules

- Always generate multiple root-problem hypotheses before choosing one.
- Mark `confidence` explicitly (low / medium / high). Never present a hypothesis
  as fact.
- The right move at `low` confidence is a discovery question, not a pitch.
- Distinguish: the stated problem is what they asked for; the real problem is
  what they would still need even if the stated solution vanished.

## The test question

> If you could achieve the outcome without [stated solution], would [stated
> solution] still be necessary?
