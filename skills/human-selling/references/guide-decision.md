# Guide Decision

The goal is not "close the deal" — it is to move to a reasonable next step that
matches where the other person actually is.

## Decision stages

```text
unaware
  ↓
problem-aware
  ↓
solution-aware
  ↓
evaluating
  ↓
decision
```

The same message does not work across stages.

| Stage | Goal | Next step (not a pitch) |
|-------|------|--------------------------|
| unaware | 帮助发现问题 | One discovery question |
| problem-aware | 澄清问题 | Sharpen the problem together |
| solution-aware | 比较不同方案 | Frame the options honestly |
| evaluating | 降低风险 | Demo / PoC / benchmark / trial |
| decision | 让决策更稳 | Remove the last blocker |

## Output model

```yaml
next_step:
  current_stage: evaluating
  recommended_action: "进行一个小范围 PoC"
  ask: |
    如果方便的话，我们可以先挑一个真实任务，
    用一周时间跑一个 PoC，
    看是否能解决你们现在的 Debug 问题。
```

## Rules

- Identify the stage first, then recommend. Never push "decision" on someone who
  is still "unaware".
- The recommended next step should be the smallest thing that de-risks the next
  decision, not the biggest thing you can ask for.
- A conversation without a `next_step` is a conversation that went nowhere.
- "Keep in touch" is not a next step — name a concrete, small action.

## The litmus test

If you cannot say which stage they are in, you do not yet understand them well
enough to advance. Return to attunement.
