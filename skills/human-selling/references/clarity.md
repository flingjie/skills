# Clarity

Clarity is helping the other person see their own problem more accurately. It is
a reframe, not a replacement of their words with yours.

## Reframing

Original:

> 我们需要一个 AI Agent。

Reframe:

> 你们真正的问题可能不是缺少 Agent，而是现有业务流程无法稳定地自动化。

Go further:

```
Not:  "We need an Agent"
But:  "We need a reliable way to execute a repeatable business workflow."
```

## Output model

```yaml
reframe:
  before:
    "需要一个 Agent"

  after:
    "需要稳定执行业务流程的自动化能力"

  why_it_matters:
    - Agent 只是手段
    - 业务结果才是目标

  validation_question:
    "如果不用 Agent，而是有其他方式能稳定完成这个流程，
     Agent 对你来说还是必须的吗？"
```

## Rules

- A reframe is offered tentatively ("可能不是… 而是…"), not asserted.
- Always pair a reframe with a `validation_question` — let them confirm or
  correct it.
- The reframe moves from a means (a thing) to an outcome (a result). If your
  reframe is still a noun-for-noun swap, you haven't reframed.

## Why it matters

People buy outcomes, not objects. Clarity is the step that exposes the outcome.
