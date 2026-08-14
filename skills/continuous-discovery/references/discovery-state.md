# Discovery State

The persistent source of truth is `state/discovery_state.json`. Load it at the start, save it at the end. The OST is a view generated from this state, not a separate file.

## Schema

```json
{
  "goal": "提高 Agent 开发和 Debug 效率",
  "opportunities": [
    {
      "id": "O-001",
      "statement": "Agent 开发者缺少快速定位 execution loop 的能力",
      "evidence": ["E-001", "E-004"],
      "confidence": "medium",
      "solutions": [
        {
          "id": "S-001",
          "name": "Execution Replay",
          "assumptions": [
            {"id": "A-001", "type": "value", "statement": "用户需要理解 execution", "status": "unvalidated"},
            {"id": "A-002", "type": "adoption", "statement": "用户愿意纳入日常流程", "status": "unvalidated"}
          ]
        }
      ]
    }
  ],
  "experiments": [
    {"id": "EXP-001", "assumption": "A-001", "method": "prototype_test", "status": "designed"}
  ],
  "learnings": []
}
```

## Field meanings

- `goal` — the desired outcome; `null` until set.
- `opportunities[]` — each has `id` (O-NNN), `statement`, `evidence` (refs to upstream evidence ids), `confidence` (`low`|`medium`|`high`), and nested `solutions[]`.
- `opportunities[].solutions[]` — each has `id` (S-NNN), `name`, and nested `assumptions[]`.
- `solutions[].assumptions[]` — each has `id` (A-NNN), `type` (`value`|`usability`|`adoption`|`business`), `statement`, and `status` (`unvalidated`|`validated`|`invalidated`).
- `experiments[]` — each has `id` (EXP-NNN), `assumption` (A-id), `method`, `status` (`designed`|`running`|`done`), and optionally `result`.
- `learnings[]` — one entry per completed experiment.

## The learning loop

When a result comes in (entry mode `learn`), record a learning and update state:

```yaml
learning:
  experiment: EXP-003
  result: partially_validated
  conclusion: "Replay 有价值，但用户真正要的不是 Replay，而是快速定位 Failure"
  opportunity_update: { confidence: high }
  next_question: "诊断时哪些信息最有用？"
```

- `result` — `validated` | `partially_validated` | `invalidated`.
- `opportunity_update` — the change to the opportunity's confidence.
- `next_question` — the next thing worth testing.

## Solution failure ≠ Opportunity failure

A `invalidated` solution does NOT mean the opportunity is dead. Distinguish:

- opportunity validated + solution invalidated → generate a different solution.
- opportunity invalidated → the opportunity itself may be wrong; lower its confidence and reconsider the tree.

Update the opportunity's confidence, never discard it on a single failed solution.

## Persistence

- Load at start; if missing, start with `{ "goal": null, "opportunities": [], "experiments": [], "learnings": [] }`.
- Save at end. Keep `id`s stable; append, don't rewrite.
