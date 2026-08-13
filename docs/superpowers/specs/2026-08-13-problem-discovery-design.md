# Design: `problem-discovery` Skill

**Date**: 2026-08-13
**Status**: Approved (pending user review)

## 1. Purpose

`problem-discovery` is a Claude Code skill that mines internet/community signals
(tweets, Reddit threads, GitHub issues, interview notes) to discover **recurring
problems**, cluster them into a **persistent backlog**, and produce a
**problem hypothesis** that hands off to the existing `idea-validation` skill for
interactive validation.

It is the front stage of a two-stage flow:

```
problem-discovery        idea-validation
(discover problems)  →   (validate + verdict)
```

## 2. Relationship to `idea-validation`

`idea-validation` already exists and is mature (SKILL.md + 3 references + 4 evals).
It validates whether a *specific* idea solves a *real* problem, using The Mom Test
(interactive challenge + pain scoring + verdict).

`problem-discovery` must **not** duplicate any of that. Its unique job is the part
`idea-validation` has no answer for: turning many raw signals into a small number of
candidate problems worth validating.

| | `problem-discovery` | `idea-validation` |
|---|---|---|
| Answers | "Which problems recur in this space?" | "Does this specific idea solve a real problem?" |
| Input | Raw signals (many) | One idea + target user |
| Output | Problem clusters + hypothesis (many→few) | Verdict: Build / Continue / Reject (one) |
| Tone | Generative — surface patterns | Defensive — challenge assumptions |
| Interaction | Analyze pasted text (no follow-ups) | Interactive interview |

Boundary in one sentence: **`problem-discovery` narrows N signals down to candidate
problems; `idea-validation` interrogates ONE candidate to a verdict.**

## 3. Core Loop

Every invocation runs the same 5-stage loop:

```
1. CAPTURE    collect raw signals (paste-first; optional active search via existing skills)
2. EXTRACT    per signal: complaint / trigger / current_behavior / cost / source
              + mandatory FACT / INTERPRETATION / ASSUMPTION separation
3. DETECT     light pain annotation (frequency/severity/cost hints in text) — NO verdict
4. CLUSTER    match against clusters in state/ → append + raise confidence, or create new
5. SYNTHESIZE update problem hypothesis + confidence + evidence gaps + next action
```

### Two governing decisions

1. **Extract and score are separate.** Stage 3 only *annotates* pain hints; it never
   produces a "build / don't build" verdict. That verdict is `idea-validation`'s job
   (it can ask follow-ups; raw-text mining cannot). This keeps the two skills
   zero-overlap.

2. **FACT / INTERPRETATION / ASSUMPTION separation is mandatory.** Raw text only
   yields facts ("they said / did X") and behavior. Any "so they need product Y" leap
   is an ASSUMPTION, flagged and deferred to validation. This is The Mom Test
   discipline applied to text that can't be interrogated.
   (Principle: `Evidence ≠ Interpretation ≠ Solution`.)

## 4. Cluster Data Model

**Storage**: `state/problem_clusters.json` — single JSON file, the cross-session
source of truth. The terminal always shows the latest state; no per-cluster markdown
until `idea-validation` writes its own report.

**Schema** (one entry):

```json
{
  "clusters": [
    {
      "id": "agent-loop-debugging",
      "title": "Agent 陷入 loop 后难以定位根因",
      "signals": [
        {
          "id": "sig-001",
          "source": "reddit", "url": "...", "date": "2026-08-13",
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

### Confidence (three levels)

| Level | Condition | next_action |
|---|---|---|
| `weak` | 1 signal / single source | keep mining |
| `medium` | 2–3 signals, ≥2 independent sources | keep mining |
| `strong` | 3+ signals, ≥3 independent sources, concrete cost or frequency stated | hand off to `idea-validation` |

Confidence = f(signal count, independent source count, whether concrete cost or
frequency is stated). **Independent sources matter**: one person repeating themselves
across posts counts as 1 source, not accumulation.

### Matching rule

Match a new signal to a cluster by **job (what the user is trying to accomplish) +
friction (what blocks them)** — **never** by proposed solution or product category.

- Same cluster: `"agent stuck in loop, manual trace"` + `"agent reran 3×, can't see
  state"` — both are "diagnose agent execution failure", even if one mentions an
  observability tool and the other a debugger.
- Different clusters: two signals both containing "AI agent" — do NOT merge unless
  job + friction also match.

## 5. I/O

### Input (two modes, paste-first)

1. **Paste (default)**: user pastes one or more raw signals, optionally with source.
   Triggers: "帮我看看这些抱怨是不是同一个问题", "挖一下这几条 Reddit/issue".
2. **Active search (optional)**: user says "去 Reddit 搜 X 的抱怨". The skill
   **orchestrates** existing search skills — `smart-search` (site routing),
   `opencli-browser` (logged-in browsing), `WebSearch` (fallback) — then feeds results
   through the same EXTRACT→CLUSTER pipeline. It **never reimplements search**.

### Output (terminal)

After processing, show the full updated state of the affected cluster: appended
signal summary (complaint / trigger / cost / FACT vs ASSUMPTION), the synthesized
problem hypothesis, evidence gaps, and next action.

### Handoff to `idea-validation`

When a cluster reaches `strong`, `next_action` becomes an explicit handoff:

> 这个 cluster 证据够了，运行 `/idea-validation`，把下面的 problem hypothesis 喂进去做交互式验证。

The hypothesis is translated into `idea-validation`'s expected input shape (one
concrete idea + target user). Optional reciprocal change: a one-line pointer in
`idea-validation`'s SKILL.md ("need candidate problems before interviewing? →
`problem-discovery`"). **Default: do not touch idea-validation** — out of scope for v1.

## 6. Files & Evals

```
skills/problem-discovery/
├── SKILL.md                          # 5-stage loop + boundary + handoff
├── references/
│   ├── signal-extraction.md          # extraction rules + FACT/INTERP/ASSUMPTION separation
│   └── cluster-schema.md             # JSON schema + confidence + job/friction matching
└── evals/evals.json
```

Source-specific playbooks (Twitter/Reddit/GitHub signal shapes) live as a *section*
inside `signal-extraction.md`, not a separate file — split only if real divergence
emerges (YAGNI).

### Eval cases (each targets a real failure mode)

| # | Case | Behavior under test |
|---|---|---|
| 1 | Single Reddit complaint | correct complaint/trigger/behavior/cost extraction + FACT vs ASSUMPTION separation |
| 2 | Two signals of the SAME problem (one says "observability tool", other "debugger") | merged into ONE cluster (match by job/friction, not product words) |
| 3 | Two signals of DIFFERENT problems (both contain "AI agent") | split into TWO clusters (not fooled by shared keyword) |
| 4 | A "users need product X" assertion | flagged as ASSUMPTION, never written as fact |
| 5 | Append signal to existing cluster (seeded state) | evidence accumulates, confidence medium→strong, next_action flips to handoff |

## 7. Out of Scope (YAGNI)

- Interactive follow-up questioning (→ `idea-validation`)
- Pain-score verdict / "should we build" (→ `idea-validation`)
- Implementing search itself (→ orchestrate `smart-search` / `opencli-*`)
- Sub-skill decomposition (single skill, matches `idea-validation` convention)
- Modifying `idea-validation` (optional reciprocal pointer only, default untouched)
