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
