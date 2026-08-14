# Switching Story

Reconstruct the user's timeline before you abstract to a Job. The point is the story — what actually happened — not your summary of it.

## The seven-step timeline

For each step, record what the source reveals, and mark it **Known**, **Unknown**, or **Assumed**.

1. **Context** — the situation/role/environment. ("I'm a solo dev building agents.")
2. **Previous Situation** — how they completed the task before the problem existed.
3. **Trigger** — the event that made the old way stop being acceptable.
4. **First Thought** — when they realized the old way was no longer enough.
5. **Search** — what they started looking for.
6. **Attempts** — what they tried, and why each didn't stick.
7. **Decision** — why they settled on the current approach.
8. **Current Workaround** — how they cope today.

## Known / Unknown / Assumed

- **Known** — stated or directly observed in the source.
- **Unknown** — not in the source; you do not know it.
- **Assumed** — you're filling a gap with an educated guess; label it and justify it.

Never silently upgrade an Unknown to an Assumed, or an Assumed to a Known.

## Missing Story Elements

Emit an explicit list of what's missing, e.g.:

- 用户遇到这个问题的频率
- 是否尝试过商业产品
- 是否愿意付费
- 失败造成的实际成本
- 是谁拍板购买

A story with many Unknowns is not a weak analysis — it's an honest one. The Unknowns become the Validation Plan's missing_evidence.

## Reconstruction questions

If you are extracting from a live or pasted interview, these are the probes per step (adapt to the source; do not fabricate answers):

- Context: 你在什么场景下做这件事？你的角色是什么？
- Previous Situation: 之前你是怎么完成这个任务的？
- Trigger: 发生了什么事情，让你觉得之前的方式不行了？
- First Thought: 你是什么时候意识到需要改变的？
- Search: 你开始找什么？
- Attempts: 你试过哪些方案？结果如何？
- Decision: 最终为什么选择了现在的做法？
- Current Workaround: 你现在是怎么勉强解决的？

## When the source is a post/issue/review (not an interview)

You often get only fragments (a trigger + a complaint, no timeline). Reconstruct what you can, and put the rest under Missing Story Elements — do not pad.
