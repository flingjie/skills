# Assumption Framework

Every solution rests on unproven assumptions. Before building, extract them and find the one most worth testing.

## Four classes

```yaml
assumptions:
  value:     [用户确实需要理解 execution, Replay 能帮助定位, 定位能省时间]
  usability: [用户能理解 Replay, 用户能找到关键步骤]
  adoption:  [用户愿意把 Replay 纳入日常流程]
  business:  [用户愿意付费]
```

- **value** — the solution actually creates value the user wants.
- **usability** — the user can use it to get that value.
- **adoption** — the user will integrate it into their routine.
- **business** — it can sustain itself (payment, cost).

## Extraction

For a solution, ask:
- value: 用户真的需要这个吗？它真能帮用户完成目标吗？
- usability: 用户能理解并使用它吗？关键操作找得到吗？
- adoption: 用户愿意把它纳入日常吗？有什么会阻止他们坚持用？
- business: 用户愿意付钱吗？谁拍板？

## The riskiest assumption

Identify the assumption whose falsity would kill the opportunity — not the one easiest to test.

- If "Replay 能帮助定位" is false, the Replay solution collapses.
- "用户愿意付费" being false does NOT kill the opportunity — you can test payment later.

Test order = risk to the opportunity, not convenience.

## Rule

Every assumption is `unvalidated` until an experiment says otherwise. An assumption with no experiment is a claim, not evidence.
