# Deal Advancement

A challenger does not just talk — they advance the deal. The most common failure
of sales agents is a good conversation that goes nowhere. This reference forces
the next action.

## Deal progress

Always track:

```yaml
deal_progress:
  current_stage: ""       # problem_discovery | problem_validation |
                          # stakeholder_alignment | evaluation | negotiation
  decision_blocker: ""    # what actually stops this from moving forward
  required_action: ""     # the single thing that unblocks it
  next_step: ""           # the concrete, scheduled next move
```

## The six possible next moves

Judge what the customer needs right now:

| Code | Move | When |
|------|------|------|
| A | More education | They don't yet see the problem |
| B | Validate the problem | They see it but aren't sure it's real/urgent |
| C | Find the decision maker | They agree but can't decide alone |
| D | Handle risk | They agree but fear the downside |
| E | Discuss budget | Problem + value are clear, money is the issue |
| F | Advance a pilot | They're convinced and need to de-risk in practice |

Do not pick more than one primary move. If you list all six, you have not
actually judged the situation.

## Example — "我们内部讨论一下"

Customer:
> 我们内部讨论一下。

Do not reply "好的." Instead, analyze:

```yaml
deal_progress:
  current_stage: problem_validation
  decision_blocker: 客户没有形成内部共识
  required_action: 让决策相关的人对齐对问题的判断
  next_step: 邀请业务负责人 + Agent 工程负责人一起做一次问题验证
```

Recommended framing:

> 在进入内部讨论之前，我建议先确认一个关键问题：你们当前的主要瓶颈到底是模型能力，
> 还是 Agent 出现问题后无法定位和复现。
>
> 如果这个判断没有确认，内部讨论很容易变成不同部门各自提出一套需求。
>
> 我建议下一次把负责 Agent 工程和业务流程的人一起拉进来，用一个真实案例验证。

## next_action schema

Every conversation must end with a committed, concrete next action:

```yaml
next_action:
  objective: ""        # what this next step is meant to achieve
  participants: []     # who must be in the room
  artifact_needed: ""  # what material is required (a case, a demo, a doc)
  commitment: ""       # what the customer explicitly agreed to do
```

## Rules

- A "good conversation" with no `next_step` is a failure.
- `next_step` must be scheduled and named — "let's keep talking" is not a step.
- If you cannot name the `decision_blocker`, you do not understand the deal yet;
  go back to Steps 2–3 before advancing.
