# Value Mapping

Never list features. Always connect a pain to an outcome through a mechanism.

## The chain

```text
Pain
  ↓
Capability
  ↓
Mechanism
  ↓
Outcome
```

## Worked example

```yaml
value_map:
  pain:
    "Agent 失败后难以定位问题"

  capability:
    "Execution Trace + Replay"

  mechanism:
    "记录完整执行状态并支持回放"

  outcome:
    "减少 Debug 时间，提高 Agent 稳定性"
```

## Rules

- Start from the customer's pain (from problem-finding), not from the product.
- The mechanism explains *why* the capability produces the outcome — it is the
  part a feature list leaves out.
- One value map per pain. If you have three pains, build three maps, not one
  dump.
- The outcome must be stated in the other person's terms (time saved, risk
  removed, cost avoided), not in product terms.

## Anti-pattern

```
Feature → Feature → Feature
```

A feature list assumes the customer does the translation. Value mapping does the
translation for them.
