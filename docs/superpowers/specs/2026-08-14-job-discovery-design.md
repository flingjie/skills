# Design: `job-discovery` Skill

**Date**: 2026-08-14
**Status**: Approved (pending user review)

## 1. Purpose

`job-discovery` is a Claude Code skill that reconstructs, from a single raw source
(an interview transcript, a tweet, a Reddit post/comment, a GitHub issue, a product
review, a support ticket, or chat logs), the Job a person is trying to get done —
not from stated feature requests, but from observed behavior.

It is a **demand-forensics / Job-hypothesis-generation** skill. Its output is a
structured Job Discovery Report that ends in "what evidence is still missing" and
"what to validate next", handing off to the existing `idea-validation` skill.

## 2. Relationship to the other skills

`job-discovery` is **fully independent** and **accepts overlap** with
`problem-discovery` and `idea-validation`. The three differ on the axis of breadth
vs. depth vs. verdict:

| | `problem-discovery` | `job-discovery` (this) | `idea-validation` |
|---|---|---|---|
| Unit | many signals | one source | one idea + user |
| Axis | breadth (cluster recurring problems) | depth (forensic JTBD on one person) | verdict |
| Answers | "which problems recur?" | "what Job is this person trying to do, and what forces drive switching?" | "should we build?" |
| Output | problem clusters + confidence | Job hypotheses + forces + opportunity map + validation plan | Build / Continue / Reject |

The overlap is deliberately in the evidence-extraction layer (both do a
FACT/inference/hypothesis three-way separation). The genuinely new content is the
forensic JTBD depth: story reconstruction, the four forces, Job classification, and
the opportunity evidence map.

**Terminology note:** `job-discovery` uses `FACT / INFERENCE / HYPOTHESIS`. These map
1:1 to `problem-discovery`'s `FACT / INTERPRETATION / ASSUMPTION` (HYPOTHESIS is the
JTBD-appropriate name for "a leap that needs validation"). The SKILL.md notes this
mapping so the whole skill system stays mutually translatable.

**Naming note:** `problem-discovery` finds *problems* (pain); `job-discovery` finds
*Jobs* (progress/motivation). The two `description` fields must be written to keep the
trigger boundary clear — `job-discovery` triggers on "why / motivation / switching /
Job", `problem-discovery` on "complaints / mining / clustering".

## 3. Scope boundary

**Does:**
- Mine structured evidence from a single raw source
- Reconstruct a behavior timeline
- Analyze the four switching forces
- Generate multiple Job hypotheses (When/I want/So I can)
- Build an opportunity evidence map
- Identify missing evidence and produce a validation plan

**Does NOT:**
- Mine/cluster many signals (→ `problem-discovery`)
- Do interactive challenge or a build/don't-build verdict (→ `idea-validation`)
- Design a product or judge a business model

## 4. Core pipeline (6 stages)

```
1. Evidence Mining      structured evidence + FACT/INFERENCE/HYPOTHESIS separation
2. Story Reconstruction timeline + Known/Unknown/Assumed
3. Forces Analysis      Push / Pull / Habit / Anxiety, each tied to Evidence IDs
4. Job Hypothesis       When [situation] I want to [progress] so I can [outcome]
                        + primary/related/emotional/social classification
5. Opportunity Signals  evidence map (Strong/Medium/Weak/Unknown)
6. Validation Plan      missing evidence + next actions + follow-up questions → idea-validation
```

"Forensic" is the default attitude of the whole pipeline, not a separate mode.

## 5. Stage details

### Stage 1 — Evidence Mining

Uniform evidence schema:

```yaml
evidence:
  - id: E1
    type: behavior      # trigger|behavior|pain|consequence|previous_solution|
                        # current_solution|workaround|attempt|decision_criteria|
                        # switching_signal|anxiety|habit|willingness_to_pay|frequency|context
    quote: "I checked the logs every 10 minutes."
    normalized: "User repeatedly monitors agent execution."
    confidence: high    # high|medium|low
```

Three-way separation on every claim:

| Label | Meaning | Example |
|---|---|---|
| FACT | stated/done, verifiable from text | "agent 跑了 2 小时" |
| INFERENCE | grounded inference from a fact | "执行状态难以理解" |
| HYPOTHESIS | leap to need/solution/market | "他们需要一个监控平台" |

HYPOTHESIS is never presented as FACT.

### Stage 2 — Story Reconstruction

Eight-step timeline; missing elements are marked, never invented:

```
Context → Previous Situation → Trigger → First Thought → Search → Attempts
→ Decision → Current Workaround
```

Output `Known / Unknown / Assumed`; a `Missing Story Elements` list captures the
Unknowns (frequency? tried commercial products? willingness to pay? real cost of
failure?).

### Stage 3 — Forces Analysis

Four forces, each tied to Evidence IDs:

```yaml
forces:
  push:
    - statement: "Manual monitoring consumes attention."
      evidence: [E1, E2]
  pull:
    - statement: "Automatic anomaly detection."
      evidence: [E3]
  habit:
    - statement: "Developer is used to manually checking logs."
      evidence: [E1]
  anxiety:
    - statement: "Automatic monitoring may produce false positives."
      evidence: []
```

`anxiety.evidence` may be empty (the user didn't say), but must be explicit. Force
strength determines whether the Job is worth switching for.

### Stage 4 — Job Hypothesis

Forbid `User needs X`. Use:

```
When [situation], I want to [motivation / progress], so I can [desired outcome].
```

Classification: **Primary Functional Job**, **Related Functional Jobs**,
**Emotional Job** (confidence / control / reduced anxiety / trust), **Social Job**
(only when evidence supports it). When evidence is ambiguous, generate multiple
hypotheses — never a single overconfident answer.

### Stage 5 — Opportunity Signals

No pseudo-precise score (no "87/100"). An opportunity evidence map:

| Signal | Assessment |
|---|---|
| Pain intensity | Strong / Medium / Weak / Unknown |
| Frequency | … |
| Existing workaround | … |
| Active search | … |
| Switching intent | … |
| Willingness to pay | … |

Final status: 🟢/🟡/🔴 (e.g. "🟡 Promising but insufficient evidence"). Never invent
frequency, willingness to pay, or market size — report unknowns honestly.

### Stage 6 — Validation Plan

Output `missing_evidence` + `next_actions` + auto-generated follow-up interview
questions ("你最近一次遇到是什么时候？当时在做什么任务？你现在怎么避免？试过哪些方案？为什么没继续用？") → hand off to `idea-validation`.

## 6. Core rules (verbatim into SKILL.md)

1. Never treat a feature request as a Job.
2. Extract evidence before making interpretations.
3. Separate FACT / INFERENCE / HYPOTHESIS.
4. Prefer observed behavior over stated preference.
5. Reconstruct the user's situation and timeline before defining a Job.
6. Identify the trigger that caused the user to seek change.
7. Look for failed attempts, existing solutions, workarounds, switching behavior.
8. Generate multiple Job hypotheses when evidence supports ambiguity.
9. Every major inference should reference supporting evidence.
10. Explicitly identify missing evidence.
11. Do not recommend building unless there is sufficient behavioral evidence.
12. Do not invent frequency, severity, willingness to pay, or market demand.

## 7. Output

A Job Discovery Report (see `references/discovery-report.md` for the exact template),
displayed in full in the terminal and saved to `state/job_report_<slug>.md` (matching
`idea-validation`'s `state/problem_report_<slug>.md` convention). One-shot — no
cross-session backlog.

## 8. Files

```
job-discovery/
├── SKILL.md                       # 12 core rules + 6-stage pipeline + output format + anti-patterns + handoff
├── references/
│   ├── evidence-taxonomy.md       # evidence schema + types + FACT/INFERENCE/HYPOTHESIS
│   ├── switching-story.md         # 8-step timeline + Known/Unknown/Assumed
│   ├── forces-of-progress.md      # four forces + evidence traceability
│   ├── job-formulation.md         # When/I want/So I can + 4 Job classes
│   └── discovery-report.md        # report template (incl. interview-followup section)
└── evals/evals.json               # 5 eval cases
```

## 9. Evals (5 cases)

| # | Case | Behavior under test |
|---|---|---|
| 1 | "我需要更好的监控" | feature request not treated as a Job; reconstruct from behavior |
| 2 | incomplete interview | missing elements marked Unknown, not invented |
| 3 | "用户需要一个监控平台" assertion | labeled HYPOTHESIS, not FACT |
| 4 | ambiguous complaint | multiple Job hypotheses, not a single answer |
| 5 | four-force analysis | each force tied to Evidence ID; opportunity map marks unknowns honestly |

## 10. Out of scope (YAGNI)

- Multi-signal clustering (→ `problem-discovery`)
- Interactive challenge / verdict (→ `idea-validation`)
- Persistent job-hypothesis backlog (one-shot + report file only)
- A literal `/job-discovery forensic` sub-command (forensic is the default attitude)
- A separate `templates/` directory (templates live in `references/`, per existing convention)
- Solution design or business-model judgment
