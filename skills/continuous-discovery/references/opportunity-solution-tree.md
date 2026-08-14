# Opportunity Solution Tree

The OST maps a desired outcome to opportunities to solutions. It is the map that keeps discovery honest: an opportunity is the progress the user wants; a solution is one concrete way to get it.

## Three layers

1. **Desired Outcome** — the high-level goal (one per tree).
2. **Opportunities** — the distinct unmet needs under that outcome.
3. **Solutions** — ≥3 concrete approaches per opportunity.

```
Desired Outcome: 提高 Agent 开发和 Debug 效率
│
├── O1 不知道 Agent 为什么失败
│   ├── S1 Execution Replay
│   ├── S2 Failure Analyzer
│   └── S3 AI Debugger
├── O2 Agent 经常进入错误 Loop
│   ├── S4 Loop Detector
│   └── S5 Budget Guard
└── O3 不知道 Prompt 修改是否有效
    ├── S6 Evaluation
    └── S7 Agent Regression Test
```

## The no-jump rule

Never collapse an opportunity into a solution. "Agent Debug 很困难" is an opportunity; "做一个 Agent Replay" is a solution. Write the opportunity first, then generate solutions under it.

## Solution generation rules

- ≥3 solutions per opportunity.
- Each solution is a genuinely different path. `Replay v1 / v2 / v3` is NOT variety — it's one solution with cosmetic variants.
- A solution names a mechanism, not a brand or a feature-list.
- If you can't generate 3 distinct paths, the opportunity is probably too narrow — broaden it.

## Distinguishing opportunity from solution

| Opportunity (progress) | Solution (mechanism) |
|---|---|
| 快速定位 Agent 失败原因 | Execution Replay |
| 知道 Agent 是否卡住 | Loop Detector |
| 判断 Prompt 修改是否有效 | Evaluation |

## Updating the tree

When new evidence changes an opportunity's confidence, update the tree in `state/discovery_state.json`, don't create a parallel doc.
