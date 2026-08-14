# Evidence Taxonomy

How to mine structured evidence from a raw source, and how to separate what the text proves from what you infer or hypothesize.

## Evidence schema

```yaml
evidence:
  - id: E1
    type: behavior
    quote: "I checked the logs every 10 minutes."
    normalized: "User repeatedly monitors agent execution."
    confidence: high    # high | medium | low
```

- `id` — `E1`, `E2`, … unique, referenced later by forces and job hypotheses.
- `type` — one of the types below.
- `quote` — the source's words, verbatim where possible.
- `normalized` — a neutral restatement.
- `confidence` — `high` (directly stated/observed), `medium` (partially stated), `low` (faint or second-hand).

## Evidence types

| Type | What it captures | Example quote |
|---|---|---|
| trigger | event that starts the story | "The agent got stuck for 40 minutes." |
| behavior | what the person does | "I checked the logs every 10 minutes." |
| pain | expressed frustration/cost | "It's driving me crazy." |
| consequence | result of the problem | "We missed the deadline." |
| previous_solution | what they used before | "We used a cron job." |
| current_solution | what they use now | "A spreadsheet plus Slack alerts." |
| workaround | a self-built partial fix | "I added a timeout and a Slack notification." |
| attempt | a tried-and-abandoned fix | "We tried Geckoboard, it didn't work." |
| decision_criteria | how they chose | "We needed something that supported our DB." |
| switching_signal | evidence of wanting to switch | "We're actively looking for a replacement." |
| anxiety | fear/risk about a new solution | "Automation might give false positives." |
| habit | inertia of current behavior | "I'm used to checking manually." |
| willingness_to_pay | stated budget/spend | "We'd pay $100/month for this." |
| frequency | how often it happens | "Two or three times a week." |
| context | situation/role/environment | "I'm a solo dev building agents." |

## FACT / INFERENCE / HYPOTHESIS

Label every claim with exactly one of these.

### FACT
The source said or did it; verifiable from the text alone.

- "我的 agent 跑了两个小时" (stated duration)
- "我手动排查了几十个 tool call" (stated behavior)
- "这种情况一周两三次" (stated frequency)

### INFERENCE
Your grounded inference from one or more facts.

- "执行状态难以理解" (from "手动排查了几十个 tool call")
- "这是高频痛点" (from "一周两三次")

### HYPOTHESIS
A leap to a need, solution, or market that must be validated.

- "他们需要一个监控平台" (solution leap)
- "所有 agent 开发者都需要" (market leap)

### Golden rule

> Evidence ≠ Inference ≠ Hypothesis.

Raw text proves only FACTs and behavior. Everything after that is inference or a leap. HYPOTHESIS is never presented as FACT. When in doubt, label a level up.

## Terminology mapping

These three labels map 1:1 to `problem-discovery`'s FACT / INTERPRETATION / ASSUMPTION. (HYPOTHESIS is the JTBD-appropriate name for "a leap that needs validation".)

## Edge cases

- **No frequency/payment stated** — leave those signals Unknown; do not invent them.
- **A feature request** ("we need an observability tool") — that's a HYPOTHESIS (the user's own solution leap), not the Job. Recover the underlying friction by asking what made them think of that tool.
- **One quote, multiple claims** — split into separate evidence entries; each claim gets its own label.
- **Second-hand** ("my colleague says") — confidence `low`, and flag the source distance.
