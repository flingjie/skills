# Signal Extraction

How to turn one raw signal into the structured fields the loop needs, and how to separate what the text proves from what you're inferring.

## Fields to extract

For every signal:

- **complaint** — the friction, in the user's own words where possible. Quote when short, paraphrase only when the quote is long.
- **trigger** — the situation or event that brings the complaint up ("agent gets stuck in a loop", "month-end reporting").
- **current_behavior** — what they do today to cope ("manually inspect tool calls", "copy-paste into a spreadsheet").
- **cost** — any time, money, risk, or opportunity the source mentions. Leave blank if none is stated — do NOT invent a cost.
- **source** — platform, URL, date. Record "unknown" when the user didn't provide.

## FACT / INTERPRETATION / ASSUMPTION

Label every claim with exactly one of these. The label goes on the claim, not the person.

### FACT

Something the source said or did, verifiable from the text alone.

- "我的 agent 跑了两个小时" (they stated a duration)
- "我手动排查了几十个 tool call" (they stated a behavior)
- "这种情况一周两三次" (they stated a frequency)

### INTERPRETATION

Your inference from one or more facts. It goes beyond what's stated but is grounded.

- "执行状态难以理解" (inferred from "手动排查了几十个 tool call")
- "这是他们的高频痛点" (inferred from "一周两三次")

Interpretations are useful for clustering but must be labeled — they are not evidence.

### ASSUMPTION

A leap to a need, a market, or a solution.

- "用户需要一款调试平台" (solution leap)
- "所有 agent 开发者都会遇到" (market leap)
- "这是一个大市场" (market leap)

Assumptions NEVER become facts or evidence. They go into `open_questions` or are dropped. The whole point of handoff to idea-validation is to test assumptions.

### Golden rule

> Evidence ≠ Interpretation ≠ Solution.

Raw text proves only FACTS and BEHAVIOR. Everything after that is inference or a leap. When in doubt, label it a level up (fact → interpretation → assumption).

## Per-source playbooks

### Twitter / X

- Look for complaints in replies and quote-tweets, not the OP's polished tweet.
- A single viral complaint is often ONE source (the author) — don't count the likes as independent sources.
- "this keeps happening", "every time", "nobody has solved X" are frequency/severity hints, not evidence.

### Reddit

- Comments, not just posts: the complaint often lives in the second-highest comment.
- Upvotes are a weak proxy for how many people *agree*, not how many *suffer*. Don't convert upvotes into a signal count.
- A thread with the same person replying multiple times = 1 source.

### GitHub Issues / Discussions

- "+1" reactions and duplicate issues are the strongest "many people" signal here — but still estimate distinct users, don't treat every +1 as a person.
- The issue body is a complaint; the maintainer's response reveals the current workaround ("use this flag", "we're not doing this").
- Labels like `bug`, `enhancement`, `wontfix` tell you severity and whether a workaround exists.

### Hacker News

- Look for the "painful thing I built a hack around" comment pattern.
- The parent post may be a product launch; the complaint is in the comments about "why didn't you just X".

### Interview notes

- Treat as raw text too: quote the person, don't editorialize.
- A pasted interview has MORE context than a tweet — but the same rule holds: what they *did* is fact, what you *conclude* is interpretation/assumption.

## Edge cases

- **No cost mentioned** — leave cost blank; do not estimate. A missing cost is itself a signal to mine more.
- **Vague complaint** ("this is annoying") — extract it as-is, mark it low-signal, and note the missing specificity in `open_questions`.
- **Complaint is actually a solution request** ("we need an observability tool") — that's the user's ASSUMPTION, not the complaint. Recover the complaint by asking: what friction made them think of that tool?
- **One person, many posts** — collapse to a single source; note the repetition in the signal, don't inflate `independent_sources`.
