# problem-discovery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create the `problem-discovery` Claude Code skill — mines internet/community signals into structured, recurring problems (clustered in a persistent backlog) that hand off to `idea-validation`.

**Architecture:** A single skill (`skills/problem-discovery/`) mirroring the existing `idea-validation` layout: one `SKILL.md` with a 5-stage loop (Capture → Extract → Detect → Cluster → Synthesize), two reference files (`signal-extraction.md`, `cluster-schema.md`), and an `evals/evals.json`. No code — the deliverable is Markdown + JSON content.

**Tech Stack:** Markdown (SKILL.md, references), JSON (evals.json + the `state/problem_clusters.json` schema).

## Global Constraints

- Match `idea-validation` conventions: `SKILL.md` with YAML frontmatter (`name`, `description`), a `references/` dir, an `evals/evals.json`.
- `name:` in frontmatter MUST equal the directory name: `problem-discovery`.
- Skill discovers and clusters problems only. It must NOT score pain or give a "build / don't build" verdict — that is `idea-validation`'s job.
- Persistent state lives in `state/problem_clusters.json`; load before Stage 4, save after Stage 5; never rewrite untouched clusters.
- Do NOT modify `idea-validation` (the reciprocal pointer is explicitly out of scope).
- Evals are authored as JSON and validated syntactically, but not auto-run — the eval runner is not committed to this repo.

---

## File Structure

```
skills/problem-discovery/
├── SKILL.md                          # frontmatter + 5-stage loop + boundary + handoff
├── references/
│   ├── signal-extraction.md          # extraction rules + FACT/INTERP/ASSUMPTION + per-source playbooks
│   └── cluster-schema.md             # JSON schema + confidence + job/friction matching
└── evals/evals.json                  # 5 eval cases
```

Each file has one responsibility. `SKILL.md` is the entry point and references the two `references/` files for detail; `evals.json` encodes the behaviors the other three files must produce.

---

### Task 1: SKILL.md (entry point)

**Files:**
- Create: `skills/problem-discovery/SKILL.md`

**Interfaces:**
- Produces: the skill's `name` (`problem-discovery`), `description` trigger phrases, and the 5-stage loop + boundary + handoff that reference the two files created in Tasks 2–3 by exact path.

- [ ] **Step 1: Write the full SKILL.md**

````markdown
---
name: problem-discovery
description: >
  Discover recurring, worth-solving problems by mining internet and community
  signals — tweets, Reddit threads, GitHub issues, interview notes — and
  clustering them into a persistent backlog of problem hypotheses. Use when the
  user wants to find real problems before building ("帮我看看社区里大家在抱怨什么",
  "what problems are worth solving", "mine these signals", "scan Reddit/Twitter/GitHub
  for pain points", "这个领域有什么值得做的问题"), or pastes raw complaints to make
  sense of ("这些抱怨是不是同一个问题"). Produces problem clusters + hypotheses that
  hand off to idea-validation for interactive validation. This skill discovers and
  clusters problems; it does NOT validate or score them.
---

# Problem Discovery

You are a problem-mining analyst. You turn raw signals into structured, recurring problems — never solutions, never verdicts. Your output is a candidate problem worth validating, handed off to `idea-validation`.

## What This Skill Does / Does Not Do

| Does | Does NOT |
|------|----------|
| Extract complaints from raw signals | Design solutions |
| Cluster recurring signals into problems | Score pain / give a "build or not" verdict |
| Accumulate evidence across sessions | Do interactive follow-up interviews |
| Produce a problem hypothesis | Validate demand |

If the user asks for a verdict or interactive validation, point them to `idea-validation`.

## The Loop

Every invocation runs the same five stages:

1. **Capture** — collect signals
2. **Extract** — pull structured fields from each signal
3. **Detect** — annotate pain hints
4. **Cluster** — match against the persistent backlog
5. **Synthesize** — update hypothesis + confidence + next action

## Stage 1: Capture

Two ways to collect signals. Paste-first.

**Paste (default).** The user pastes one or more raw signals, each optionally with a source and date. Accept tweets, Reddit posts/comments, GitHub issues, forum threads, interview notes, support tickets, reviews.

**Active search (optional).** If the user asks you to go find signals ("去 Reddit 搜一下 X 的抱怨"), orchestrate existing search skills — never implement search yourself:

- `smart-search` — route a query to a specific site
- `opencli-browser` — browse logged-in pages
- Web search — fallback

Feed whatever you find into Stage 2, same as pasted text.

## Stage 2: Extract

For each signal, extract these fields:

- **complaint** — the friction, in the user's own words where possible
- **trigger** — the situation/event that brings it up
- **current_behavior** — what they do today to cope
- **cost** — time, money, risk, or opportunity mentioned
- **source** — platform + URL + date

Then label every claim as exactly one of:

- **FACT** — something the source said or did, verifiable from the text
- **INTERPRETATION** — your inference from a fact ("execution state is hard to understand")
- **ASSUMPTION** — a leap to a need or solution ("they need a debugging platform")

Rule: raw text gives you FACTS and BEHAVIOR. Any "so they need X" is an ASSUMPTION — flag it, never present it as found. (Evidence ≠ Interpretation ≠ Solution.)

Read `references/signal-extraction.md` for per-source guidance and edge cases.

## Stage 3: Detect

Annotate pain hints present in the text — do NOT score, do NOT give a verdict:

- frequency hints ("every time", "weekly", "2-3 times a week")
- severity hints ("drives me crazy", "lost a deal", "gave up")
- cost hints ("hours", "$", "hired someone")

Record these as `freq_hint` / `sev_hint` / cost on the signal. They inform confidence later, but a verdict is idea-validation's job.

## Stage 4: Cluster

Match each extracted signal against the persistent backlog in `state/problem_clusters.json`.

**Match by job + friction, never by solution or product category.** Two signals belong to the same cluster when the user is trying to accomplish the same thing (job) and blocked by the same thing (friction) — regardless of what product words they mention.

- "agent stuck in loop, manual trace" + "agent reran 3×, can't see state" → SAME cluster (diagnose agent execution failure)
- two signals both saying "AI agent" but different jobs/frictions → DIFFERENT clusters

Read `references/cluster-schema.md` for the exact schema and matching rules.

## Stage 5: Synthesize

For the affected cluster, output in the terminal:

- the appended signal summary (complaint / trigger / cost / FACT vs ASSUMPTION)
- the problem hypothesis (one sentence, see template)
- confidence level (weak / medium / strong)
- evidence gaps (open questions)
- next action (keep mining, or hand off)

## Problem Hypothesis Template

> When **[user]** is **[trigger]**, they **[friction]**, and today they **[current behavior]**, costing **[cost]**.

## Confidence Levels

| Level | Condition | next_action |
|-------|-----------|-------------|
| weak | 1 signal / single source | keep mining |
| medium | 2–3 signals, ≥2 independent sources | light validation ok |
| strong | 3+ signals, ≥3 independent sources, concrete cost or frequency stated | hand off to idea-validation |

Independent sources matter: one person repeating themselves counts once.

## Handoff to idea-validation

When a cluster reaches **strong**, `next_action` becomes an explicit handoff:

> 这个 cluster 证据够了，运行 `/idea-validation`，把下面的 problem hypothesis 喂进去做交互式验证。

Translate the hypothesis into idea-validation's expected input: one concrete idea + a specific target user.

## State

All clusters live in `state/problem_clusters.json`. Load it at the start of Stage 4; save it after Stage 5. If the file doesn't exist yet, start with an empty `{ "clusters": [] }`.

## Reference Files

- `references/signal-extraction.md` — extraction rules + FACT/INTERP/ASSUMPTION + per-source playbooks
- `references/cluster-schema.md` — JSON schema + confidence + job/friction matching
````

- [ ] **Step 2: Verify frontmatter and loop structure**

Run:
```bash
grep -q '^name: problem-discovery' skills/problem-discovery/SKILL.md && echo "name OK"
for s in Capture Extract Detect Cluster Synthesize; do grep -q "Stage [0-9]: $s" skills/problem-discovery/SKILL.md || echo "MISSING: $s"; done
```
Expected: prints `name OK` and nothing else.

- [ ] **Step 3: Commit**

```bash
git add skills/problem-discovery/SKILL.md
git commit -m "feat(problem-discovery): add SKILL.md with 5-stage loop"
```

---

### Task 2: references/signal-extraction.md

**Files:**
- Create: `skills/problem-discovery/references/signal-extraction.md`

**Interfaces:**
- Consumes: the field names `complaint` / `trigger` / `current_behavior` / `cost` and the three labels FACT / INTERPRETATION / ASSUMPTION introduced in Task 1.
- Produces: the extraction rules and per-source playbooks that Task 3's schema consumes; `evals.json` cases 1 and 4 assert this behavior.

- [ ] **Step 1: Write the full reference**

````markdown
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
````

- [ ] **Step 2: Verify key sections exist**

Run:
```bash
grep -q "FACT / INTERPRETATION / ASSUMPTION" skills/problem-discovery/references/signal-extraction.md && \
grep -q "Per-source playbooks" skills/problem-discovery/references/signal-extraction.md && \
grep -q "Golden rule" skills/problem-discovery/references/signal-extraction.md && echo "OK"
```
Expected: prints `OK`.

- [ ] **Step 3: Commit**

```bash
git add skills/problem-discovery/references/signal-extraction.md
git commit -m "feat(problem-discovery): add signal-extraction reference"
```

---

### Task 3: references/cluster-schema.md

**Files:**
- Create: `skills/problem-discovery/references/cluster-schema.md`

**Interfaces:**
- Consumes: the extracted field names from Task 2 and the confidence/next_action vocabulary from Task 1.
- Produces: the exact `state/problem_clusters.json` shape, the three confidence levels, and the job+friction matching rules that `SKILL.md` Stage 4/5 and `evals.json` cases 2, 3, 5 depend on.

- [ ] **Step 1: Write the full reference**

````markdown
# Cluster Schema

The persistent backlog lives in `state/problem_clusters.json`. This file is the source of truth for what problems have been discovered and how strong the evidence is.

## File shape

```json
{
  "clusters": [
    {
      "id": "agent-loop-debugging",
      "title": "Agent 陷入 loop 后难以定位根因",
      "signals": [
        {
          "id": "sig-001",
          "source": "reddit",
          "url": "https://...",
          "date": "2026-08-13",
          "complaint": "manually inspect dozens of tool calls",
          "trigger": "agent gets stuck in a loop",
          "current_behavior": "manual inspection of tool calls",
          "cost": "hours of debugging time",
          "fact": "用户手动排查了几十个 tool call",
          "interpretation": "执行状态难以理解",
          "assumption": "用户需要一款调试平台"
        }
      ],
      "confidence": "medium",
      "evidence": { "signal_count": 2, "independent_sources": 2 },
      "open_questions": ["有多少开发者同样遇到？", "是否愿意切换？", "愿意付钱吗？"],
      "next_action": "keep mining"
    }
  ]
}
```

## Field meanings

### Cluster

- `id` — kebab-case, derived from the job+friction (e.g. `agent-loop-debugging`). Stable across sessions; used to append signals.
- `title` — one line, human-readable. Keep it about the problem, not a product.
- `signals[]` — every raw signal mapped to this cluster.
- `confidence` — `weak` | `medium` | `strong`.
- `evidence.signal_count` — number of signals in the cluster.
- `evidence.independent_sources` — number of distinct people/sources. Multiple posts by one person count once.
- `open_questions[]` — what's still unknown. These feed the handoff to validation.
- `next_action` — `keep mining` or `hand off to idea-validation`.

### Signal

- `id` — `sig-<NNN>`, unique within the file.
- `source` — `twitter` | `reddit` | `github` | `hackernews` | `interview` | `other`.
- `url` — optional; omit if unknown.
- `date` — ISO date; `unknown` if not provided.
- `complaint` / `trigger` / `current_behavior` / `cost` — extracted fields (see signal-extraction.md).
- `fact` / `interpretation` / `assumption` — the three-way separation.

## Confidence levels

| Level | Condition | next_action |
|-------|-----------|-------------|
| weak | 1 signal / single source | keep mining |
| medium | 2–3 signals, ≥2 independent sources | light validation ok |
| strong | 3+ signals, ≥3 independent sources, concrete cost or frequency stated | hand off to idea-validation |

Confidence is a floor, not a formula. Recompute it after every append: bump only if the new signal adds an independent source or a concrete cost/frequency that was missing.

## Matching rules

Match a new signal to an existing cluster by **job + friction**, never by product or category.

1. Identify the job: what is the user trying to accomplish?
2. Identify the friction: what blocks them?
3. Find the cluster whose job AND friction both match.

### Same cluster (examples)

- "agent stuck in loop, manual trace" + "agent reran 3×, can't see state" — job = debug agent execution, friction = can't locate root cause. SAME cluster, even though one mentions an observability tool and the other a debugger.

### Different clusters (examples)

- "agent can't be debugged" (job = debug) vs "agent is too slow" (job = run fast) — different jobs, different clusters, even though both are about agents.
- "agent debugging is hard" (single dev) vs "agent evals are hard for my team" (team lead) — different friction, different clusters.

### When in doubt

If job OR friction differs, create a new cluster. Merging two distinct problems into one is worse than having two clusters you later merge — the cost of a wrong merge is silent, the cost of a wrong split is just an extra cluster.

## Persistence

- Load the file at the start of Stage 4. If it's missing, start with `{ "clusters": [] }`.
- After Stage 5, write the file back. Never rewrite clusters you didn't touch.
- Keep `id` stable. Renaming an id orphans any external reference — prefer to keep the id and edit `title` instead.
````

- [ ] **Step 2: Verify schema sections exist**

Run:
```bash
grep -q "Field meanings" skills/problem-discovery/references/cluster-schema.md && \
grep -q "Confidence levels" skills/problem-discovery/references/cluster-schema.md && \
grep -q "Matching rules" skills/problem-discovery/references/cluster-schema.md && \
grep -q "state/problem_clusters.json" skills/problem-discovery/references/cluster-schema.md && echo "OK"
```
Expected: prints `OK`.

- [ ] **Step 3: Commit**

```bash
git add skills/problem-discovery/references/cluster-schema.md
git commit -m "feat(problem-discovery): add cluster-schema reference"
```

---

### Task 4: evals/evals.json

**Files:**
- Create: `skills/problem-discovery/evals/evals.json`

**Interfaces:**
- Consumes: the behaviors defined in Tasks 1–3 (extraction, FACT/ASSUMPTION separation, job+friction clustering, confidence levels, state persistence).
- Produces: five eval cases, one per failure mode from the design doc.

- [ ] **Step 1: Write the full evals file**

````json
{
  "skill_name": "problem-discovery",
  "evals": [
    {
      "id": 1,
      "prompt": "I found this Reddit comment: 'Every time my agent gets stuck in a loop I have to manually inspect dozens of tool calls to figure out where it went wrong. Took me 3 hours last night.' Mine this signal.",
      "expected_output": "Extracts complaint ('manually inspect dozens of tool calls'), trigger ('agent gets stuck in a loop'), current_behavior ('manual inspection'), cost ('3 hours'). Separates FACT (stated behavior/cost) from ASSUMPTION (no leap to 'they need a debugging platform'). Creates one cluster, confidence weak.",
      "files": [],
      "assertions": [
        {"name": "Extracts complaint/trigger/behavior/cost", "description": "All four fields present and grounded in the text"},
        {"name": "Separates fact from assumption", "description": "No solution/need leap presented as fact; any 'they need X' is labeled assumption"},
        {"name": "Creates one cluster with weak confidence", "description": "Single signal, single source → confidence weak, next_action keep mining"}
      ]
    },
    {
      "id": 2,
      "prompt": "Signal A: 'Agent keeps looping and I have to trace tool calls manually — we need an observability tool.' Signal B: 'My agent reran three times and I still can't see the execution state — considering a debugger.' Mine both.",
      "expected_output": "Merges A and B into ONE cluster (job=debug agent execution, friction=can't see root cause) despite A mentioning observability tool and B mentioning debugger. Confidence medium (2 signals, 2 sources).",
      "files": [],
      "assertions": [
        {"name": "Merges into one cluster", "description": "Both signals under one cluster id"},
        {"name": "Matches by job+friction not product words", "description": "Does not split into 'observability' and 'debugger' clusters"},
        {"name": "Confidence medium", "description": "2 signals, 2 independent sources → medium"}
      ]
    },
    {
      "id": 3,
      "prompt": "Signal A: 'My AI agent can't be debugged when it loops.' Signal B: 'My AI agent is too slow at inference.' Mine both.",
      "expected_output": "Splits into TWO clusters (A: debug; B: speed) despite both containing 'AI agent'. Different jobs/frictions must not be merged.",
      "files": [],
      "assertions": [
        {"name": "Two clusters", "description": "A and B land in different clusters"},
        {"name": "Not fooled by shared keyword", "description": "Does not merge just because both mention 'AI agent'"}
      ]
    },
    {
      "id": 4,
      "prompt": "Someone tweeted: 'Every SaaS company needs an AI agent that auto-updates their docs.' Mine this signal.",
      "expected_output": "Flags the product/market claim as ASSUMPTION, not fact. No concrete complaint/trigger/behavior/cost can be extracted from a solution assertion. Marks low-signal and notes missing specificity.",
      "files": [],
      "assertions": [
        {"name": "Solution claim flagged as assumption", "description": "'needs an AI agent' is labeled assumption, never written as fact"},
        {"name": "No invented evidence", "description": "Does not fabricate a complaint/trigger/cost that isn't in the text"}
      ]
    },
    {
      "id": 5,
      "prompt": "Append this signal to the existing cluster 'agent-loop-debugging' (already has 2 signals from 2 independent sources): 'Third dev this week: wasted half a day tracing a loop in production.' Mine it.",
      "expected_output": "Appends to the existing cluster, signal_count 3, independent_sources 3, cost ('half a day') now stated → confidence flips to strong, next_action becomes 'hand off to idea-validation'.",
      "files": [],
      "assertions": [
        {"name": "Appends to existing cluster", "description": "Does not create a new cluster; existing id is reused"},
        {"name": "Confidence strong + handoff", "description": "3 signals, 3 sources, concrete cost → strong, next_action = hand off"},
        {"name": "State reflects the append", "description": "state/problem_clusters.json reflects the appended signal and updated confidence"}
      ]
    }
  ]
}
````

- [ ] **Step 2: Validate JSON**

Run:
```bash
python3 -m json.tool skills/problem-discovery/evals/evals.json > /dev/null && echo "JSON OK"
```
Expected: prints `JSON OK`.

- [ ] **Step 3: Commit**

```bash
git add skills/problem-discovery/evals/evals.json
git commit -m "feat(problem-discovery): add 5 eval cases"
```

---

### Task 5: Final conformance check

**Files:**
- Verify: `skills/problem-discovery/` (all of the above)

- [ ] **Step 1: Confirm the full tree**

Run:
```bash
find skills/problem-discovery -type f | sort
```
Expected:
```
skills/problem-discovery/SKILL.md
skills/problem-discovery/evals/evals.json
skills/problem-discovery/references/cluster-schema.md
skills/problem-discovery/references/signal-extraction.md
```

- [ ] **Step 2: Cross-check against the design doc**

Confirm each design requirement has a home:
- 5-stage loop → `SKILL.md` "The Loop" + Stage 1–5 headers
- boundary (no verdict) → `SKILL.md` "What This Skill Does / Does Not Do"
- FACT/INTERP/ASSUMPTION → `SKILL.md` Stage 2 + `signal-extraction.md`
- cluster schema + confidence + matching → `cluster-schema.md`
- handoff → `SKILL.md` "Handoff to idea-validation"
- 5 eval cases → `evals/evals.json` ids 1–5

Run:
```bash
grep -q "Handoff to idea-validation" skills/problem-discovery/SKILL.md && \
grep -q "does NOT validate or score" skills/problem-discovery/SKILL.md && \
grep -q '"id": 5' skills/problem-discovery/evals/evals.json && echo "CONFORMANCE OK"
```
Expected: prints `CONFORMANCE OK`.

- [ ] **Step 3: Commit any fixes**

Only if Step 1/2 surfaced a gap:
```bash
git add -A skills/problem-discovery && git commit -m "chore(problem-discovery): fix conformance gaps"
```
If nothing changed, no commit is needed.
