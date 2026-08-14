# Experiment Patterns

Design the cheapest experiment that can reliably test the riskiest assumption. Cheapest reliable, not easiest to run.

## Experiment shape

```yaml
experiment:
  hypothesis: "Agent 开发者能通过 Replay 更快定位失败"
  method: prototype_test
  target_users: 5
  success_metric:
    - "80% 用户识别出失败原因"
    - "median diagnosis_time < 3min"
  evidence_required: [task completion, diagnosis time, user behavior]
```

- `hypothesis` — the specific assumption under test, as a falsifiable statement.
- `method` — one of the ladder below.
- `target_users` — who and how many.
- `success_metric` — observable, pre-committed thresholds.
- `evidence_required` — what to collect (behavior, not opinion).

## The experiment ladder (cheap → expensive)

1. **interview** — ask about past behavior (see idea-validation's Mom Test).
2. **prototype** — a clickable fake; observe use.
3. **fake door** — advertise the feature; measure click/interest.
4. **concierge** — do the job manually for the user.
5. **wizard of oz** — fake the automation behind the scenes.
6. **MVP** — the smallest real product.
7. **production** — full build.

Principle: don't build before validating. Climb only when the cheaper rung can't answer the question.

## Method ↔ assumption class

- value → interview / prototype / fake door
- usability → prototype / wizard of oz
- adoption → concierge / MVP
- business → fake door / concierge (pricing)

## Success criteria rules

- Pre-commit metrics BEFORE running — no moving the goalposts.
- Metrics observe behavior (task completion, time, retention), not opinions ("users said they liked it").
- Record `partially_validated` honestly when results are mixed.
