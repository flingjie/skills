# Design: `continuous-discovery` Skill

**Date**: 2026-08-14
**Status**: Approved (pending user review)

## 1. Purpose

`continuous-discovery` is a Claude Code skill that turns customer opportunities
into validated solutions through a continuous loop — Opportunity Solution Tree,
solution generation, assumption mapping, experiment design, and a learning loop —
maintained in a persistent Discovery State. It is based on Teresa Torres's
*Continuous Discovery Habits*.

It is the **advance-and-validate engine** of the customer-discovery stack, sitting
downstream of the understanding/取证 skills.

## 2. Relationship to the other skills

`continuous-discovery` **starts from an opportunity** — it does not collect
signals, extract evidence, or identify opportunities (those are delegated to the
existing skills).

| Skill | Responsibility | continuous-discovery's relationship |
|---|---|---|
| `problem-discovery` | mine/cluster many signals → recurring problems | upstream: produces candidate problems |
| `job-discovery` | single-source JTBD forensics → Job + forces + opportunity | upstream: produces opportunities |
| `idea-validation` | interactive Mom Test challenge + verdict | sibling: validates one idea interactively |
| `continuous-discovery` (this) | opportunity → solution → assumption → experiment → learn | the ongoing advance-and-validate loop |

Boundary in one sentence: **the upstream skills produce opportunities;
`continuous-discovery` advances an opportunity toward a validated solution through
experiments.**

## 3. Scope boundary

**Does:**
- Ingest an opportunity (verify it has evidence backing; flag if not)
- Build/update an Opportunity Solution Tree
- Generate ≥3 path-distinct solutions per opportunity
- Extract assumptions (value/usability/adoption/business)
- Identify the riskiest assumption
- Design the cheapest-reliable experiment
- Ingest an experiment result and update the Discovery State (confidence, learning, next question)

**Does NOT:**
- Collect signals (→ `problem-discovery`)
- Identify Jobs/opportunities from raw evidence (→ `job-discovery`)
- Do interactive challenge / a build/don't-build verdict (→ `idea-validation`)
- Actually run experiments (the user or other agents run them; the skill designs and ingests results)

## 4. Core loop (from opportunity)

```
1. Ingest Opportunity
2. Build/Update OST
3. Generate Solutions (≥3, path-distinct)
4. Extract Assumptions (value/usability/adoption/business)
5. Identify Riskiest Assumption
6. Design Experiment (cheapest reliable)
7. (user runs the experiment)
8. Learn & Update State
```

## 5. Two entry modes

- **`expand`** — given an opportunity, run steps 1–6: produce the OST, solutions,
  assumptions, and experiment design.
- **`learn`** — given an experiment result, run step 8: update confidence, record a
  learning, produce the next question.

## 6. Core principles

1. Opportunity ≠ Solution — always generate ≥3 solutions; never collapse an
   opportunity into its first solution.
2. A solution must be decomposed into assumptions.
3. Validate the riskiest assumption first — the one whose falsity would kill the
   opportunity, not the one that is easiest to test.
4. Discovery is a loop — persistent state, not a one-off report.
5. Solution failure ≠ Opportunity failure — a failed solution may still point at a
   valid opportunity; update confidence and next question, don't discard.

(Evidence-first, past-behavior-over-intent, and problem≠opportunity are upstream
concerns owned by `problem-discovery` / `job-discovery` / `idea-validation`; this
skill verifies an opportunity has evidence but does not collect it.)

## 7. Stage details

### Opportunity Solution Tree (Steps 2–3)

Three layers: desired outcome → opportunities → solutions. Opportunities and
solutions are distinct — an opportunity is the progress the user wants ("locate a
failure cause fast"), a solution is a concrete way to get it ("replay / analyzer /
debugger").

```
Desired Outcome: 提高 Agent 开发和 Debug 效率
│
├── O1 不知道 Agent 为什么失败
│   ├── S1 Execution Replay
│   ├── S2 Failure Analyzer
│   └── S3 AI Debugger
├── O2 Agent 经常进入错误 Loop
│   ├── S4 Loop Detector
│   └── S5 Budget Guard
└── O3 不知道 Prompt 修改是否有效
    ├── S6 Evaluation
    └── S7 Agent Regression Test
```

### Solution generation rule (Step 3)

≥3 solutions per opportunity, each a genuinely different path — forbid `Replay v1 /
v2 / v3` pseudo-variety.

### Assumption framework (Steps 4–5)

Four categories per solution:

```yaml
assumptions:
  value:     [用户确实需要理解 execution, Replay 能帮助定位, 定位能省时间]
  usability: [用户能理解 Replay, 用户能找到关键步骤]
  adoption:  [用户愿意把 Replay 纳入日常流程]
  business:  [用户愿意付费]
```

Riskiest assumption = the one whose falsity would kill the opportunity, not the one
easiest to test.

### Experiment design (Step 6)

Cheapest reliable experiment (not the easiest to run):

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

Experiment ladder (cheap → expensive): `interview → prototype → fake door →
concierge → wizard of oz → MVP → production`. Principle: don't build before
validating.

## 8. Discovery State

Single source of truth: `state/discovery_state.json`.

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

Nesting: `opportunities → solutions → assumptions`; `experiments` and `learnings`
are top-level arrays linked by id. The OST is a human-readable view generated from
this state, not a separate source of truth.

## 9. Learning loop (Step 8)

An experiment result updates state rather than emitting a bare "pass/fail":

```yaml
learning:
  experiment: EXP-003
  result: partially_validated
  conclusion: "Replay 有价值，但用户真正要的不是 Replay，而是快速定位 Failure"
  opportunity_update: { confidence: high }
  next_question: "诊断时哪些信息最有用？"
```

Solution failure ≠ Opportunity failure: update the opportunity's confidence and the
next question; don't discard the opportunity.

## 10. Files

```
continuous-discovery/
├── SKILL.md                        # core principles + loop + two modes + Never/Prefer + output
├── references/
│   ├── opportunity-solution-tree.md  # OST structure + no-jump rule + 3+ solutions
│   ├── assumption-framework.md       # 4 assumption classes + riskiest-assumption
│   ├── experiment-patterns.md        # experiment design + ladder + cheapest-reliable
│   └── discovery-state.md            # single JSON schema + learning loop + solution≠opportunity
└── evals/evals.json                  # 5 eval cases
```

No separate `templates/` or `examples/` dir (YAGNI); the state schema is a reference.

## 11. Evals (5 cases)

| # | Case | Behavior under test |
|---|---|---|
| 1 | "做一个 Agent Debug 工具" | not a solution-first jump; abstract to an opportunity first |
| 2 | one opportunity | ≥3 path-distinct solutions, not v1/v2/v3 |
| 3 | one solution | four assumption classes, not value-only |
| 4 | several assumptions | riskiest assumption = greatest cost if false, not easiest to test |
| 5 | experiment result "users prefer logs" | update confidence + record learning + next question, don't discard the opportunity |

## 12. Out of scope (YAGNI)

- Signal collection / evidence extraction / opportunity identification (→ upstream skills)
- Interactive challenge / verdict (→ `idea-validation`)
- Actually running experiments
- A multi-file `.discovery/` knowledge base (single JSON state instead)
- A multi-sub-agent decomposition (Signal Collector / OST Manager / … as separate agents)
