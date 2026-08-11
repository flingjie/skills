# Scoring Guide

Detailed calibration for the three pain dimensions. Read this when you need to distinguish between close scores or handle ambiguous cases.

## Frequency

The anchor question: "How many times has this actually happened in the past [period]?"

### Calibration examples

| Scenario | Score | Why |
|----------|-------|-----|
| "I think it happened once last year, maybe" | 1 | Vague memory, not a recurring pattern |
| "We deal with this every quarterly review" | 4 | Predictable but infrequent |
| "Every sprint planning it comes up" | 6 | Bi-weekly, regular annoyance |
| "I hit this 2-3 times a week" | 8 | Frequent enough to be a real friction |
| "This is my morning. Every day starts with this." | 10 | Dominates daily workflow |

### Edge cases

- **Seasonal problems** (tax filing, annual budgeting): High severity during the season, but low frequency across the year. Use the frequency DURING the active period, but note the seasonality. A tax problem that costs 40 hours in March is a 7-8 during tax season, but the annual average might be a 3. Report both and explain.
- **"It depends"**: Push for a concrete number. "About how many times last month? The month before?" If they truly can't estimate, score it a 3 (unclear pattern) and flag as unverified.
- **Prevented by workaround**: If the problem would happen daily but the user has a workaround that prevents it, score the frequency of the workaround being needed, not the hypothetical frequency.

## Severity

The anchor question: "What's the actual cost — time, money, or opportunity — when this happens?"

### Calibration examples

| Scenario | Score | Why |
|----------|-------|-----|
| "It's a minor formatting thing, I just fix it and move on" | 2 | Not really a problem |
| "It's annoying but I'm used to it by now" | 4 | Habituated pain — the user has stopped noticing |
| "I complain about this to my coworkers at least once a week" | 6 | Social signaling of real frustration |
| "I've spent hours googling for a solution, tried three tools, nothing works" | 8 | Active search behavior — strong signal |
| "We lost a $50k deal because this took too long" | 10 | Quantified business loss |

### Edge cases

- **Emotional vs. economic cost**: "It drives me crazy" without a time/money anchor is a 4-5. "It costs us $500/month in manual labor" is an 8+. Concrete cost always scores higher.
- **The user doesn't think it's a problem**: If you're in role 2 (building for others) and the person describing the problem seems only mildly bothered, that's a real signal. Don't inflate the score because YOU think it should hurt more.
- **Learned helplessness**: "There's no way around it, everyone in this industry deals with it." This sounds like low severity but it's actually high — the user has given up. Probe: "If there WERE a solution, what would change?" Score based on the revealed gap, not the stated acceptance.

## Workaround Quality

The anchor question: "If I gave you a magic wand, would you keep doing it the current way?"

Higher score = worse current solution = bigger opportunity. This dimension is INVERTED from intuition.

### Calibration examples

| Scenario | Score | Why |
|----------|-------|-----|
| "We use [SaaS tool] and it handles this perfectly" | 1 | No gap to fill |
| "We use [SaaS tool], it's mostly fine but lacks one feature" | 4 | Gap exists but switching cost is high |
| "I built a Google Sheet with formulas, it kind of works" | 6 | Homemade solution — indicates real need |
| "It's emails back and forth, Slack DMs, a Notion page, and a weekly meeting. Takes 3 people." | 8 | Multi-tool, multi-person chaos |
| "We just... don't do it. We've given up. We eat the cost." | 10 | Problem is avoided entirely — no solution exists |

### Edge cases

- **No workaround because no need**: Score 1-2. If nobody has tried to solve it, the problem might not be real. Differentiate from "no workaround because it's impossible" (score 9-10).
- **The workaround is "I pay someone else to do it"**: This is a STRONG signal. Score 7+ — the user is literally spending money on a proxy solution.
- **Engineer-built internal tool**: Score 5-7. It exists, so there's demand, but it took engineering time to build, which is itself a cost. The question is whether a better external solution would be worth switching.

## Common Mistakes

### Mistake 1: Averaging without evidence
Don't score 5 because "it could be anything." If you can't point to something the user said that justifies the score, leave it blank and flag it. A scored dimension without evidence is misleading.

### Mistake 2: Scoring the idea, not the problem
The pain score measures the PROBLEM, not how cool the solution is. A brilliant AI solution to a 3/30 problem is still a bad investment.

### Mistake 3: Anchoring to the first number mentioned
If the user says "it's a 8 out of 10," don't accept it. Ask: "What makes it an 8? What would a 6 look like? What would a 10 look like?" Self-ratings are often inflated.

### Mistake 4: Ignoring distribution
"Some users hit this daily, most never hit it" — don't average. Report the distribution: "For power users (20% of base), frequency is 9. For casual users, it's 1." A small group with intense pain can still be a viable market.

## Interpreting Total Scores

The total is the sum of Frequency + Severity + Workaround Quality (max 30).

| Total | Interpretation |
|-------|---------------|
| 24-30 | Exceptional pain. Multiple strong signals. Unambiguous demand. |
| 18-23 | Real, validated problem. Evidence is solid. Worth building. |
| 12-17 | Problem might be real but evidence is thin. Need more interviews. |
| 6-11 | Weak signal. Could be a feature request, not a product. One or two more interviews might clarify. |
| 0-5 | No evidence of a real problem. Do not build. |

Note: These ranges overlap with the recommendation thresholds in SKILL.md. The total score is a guide, not a formula. Evidence quality can override the score — a 22-point score with only self-reported data is weaker than a 16-point score backed by 10 user interviews.
