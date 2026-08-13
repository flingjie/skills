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
