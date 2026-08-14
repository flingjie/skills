# job-discovery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create the `job-discovery` Claude Code skill — forensic single-source JTBD analysis (evidence → timeline → four forces → Job hypotheses → opportunity map → validation plan) that hands off to `idea-validation`.

**Architecture:** A single skill (`skills/job-discovery/`) mirroring the existing `idea-validation` and `problem-discovery` layouts: one `SKILL.md` with a 6-stage pipeline, five `references/` files (evidence-taxonomy, switching-story, forces-of-progress, job-formulation, discovery-report), and an `evals/evals.json`. No code — the deliverable is Markdown + JSON content.

**Tech Stack:** Markdown (SKILL.md, references), JSON (evals.json).

## Global Constraints

- Match existing conventions: `SKILL.md` with YAML frontmatter (`name`, `description`), a `references/` dir, an `evals/evals.json`.
- `name:` in frontmatter MUST equal the directory name: `job-discovery`.
- Deep single-source JTBD forensics only. It must NOT give a build/don't-build verdict (→ `idea-validation`) and must NOT mine/cluster many signals (→ `problem-discovery`).
- Terminology is `FACT / INFERENCE / HYPOTHESIS` (maps 1:1 to `problem-discovery`'s `FACT / INTERPRETATION / ASSUMPTION`); the mapping is noted in SKILL.md.
- Output is one-shot: display the report in the terminal and save to `state/job_report_<slug>.md`. No cross-session backlog.
- Do NOT modify `problem-discovery` or `idea-validation`.
- Evals are authored as JSON and validated syntactically, not auto-run.

---

## File Structure

```
skills/job-discovery/
├── SKILL.md                       # 12 core rules + 6-stage pipeline + output format + handoff
├── references/
│   ├── evidence-taxonomy.md       # evidence schema + types + FACT/INFERENCE/HYPOTHESIS
│   ├── switching-story.md         # 7-step timeline + Known/Unknown/Assumed
│   ├── forces-of-progress.md      # four forces + evidence traceability
│   ├── job-formulation.md         # When/I want/So I can + 4 Job classes
│   └── discovery-report.md        # report template (incl. interview-followup)
└── evals/evals.json               # 5 eval cases
```

Each file has one responsibility. `SKILL.md` is the entry point and references the five `references/` files; `evals.json` encodes the behaviors the other six files must produce.

---

### Task 1: SKILL.md (entry point)

**Files:**
- Create: `skills/job-discovery/SKILL.md`

**Interfaces:**
- Produces: the skill's `name` (`job-discovery`), `description` trigger phrases, the 6-stage pipeline, and pointers to the five reference files (created in Tasks 2–6) by exact path.

- [ ] **Step 1: Write the full SKILL.md**

````markdown
---
name: job-discovery
description: >
  Reconstruct the Job a person is trying to get done from a single raw source
  (interview transcript, tweet, Reddit post/comment, GitHub issue, product
  review, support ticket, or chat log) — not from stated feature requests, but
  from observed behavior. Use when the user pastes one piece of evidence and
  wants a forensic JTBD analysis ("分析这段访谈的 Job", "what Job is this person
  trying to do", "这个用户到底想完成什么", "reconstruct the switching forces",
  "帮我做需求取证"). Produces Job hypotheses + four switching forces + an
  opportunity evidence map + a validation plan that hands off to idea-validation.
  This skill does deep single-source JTBD forensics; it does NOT mine/cluster
  many signals (→ problem-discovery) or give a build/don't-build verdict
  (→ idea-validation).
---

# Job Discovery

You are a demand-forensics analyst. You reconstruct the Job a person is trying to get done from a single raw source — never from stated feature requests, never by jumping to a product. Your output is a Job Discovery Report that ends in "what evidence is still missing" and "what to validate next."

## What This Skill Does / Does Not Do

| Does | Does NOT |
|------|----------|
| Mine structured evidence from one source | Mine/cluster many signals (→ problem-discovery) |
| Reconstruct a behavior timeline | Do interactive challenge / verdict (→ idea-validation) |
| Analyze the four switching forces | Design a product or judge a business model |
| Generate Job hypotheses | Treat a feature request as a Job |

## Core Rules

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

Terminology note: FACT / INFERENCE / HYPOTHESIS map 1:1 to problem-discovery's
FACT / INTERPRETATION / ASSUMPTION.

## The Pipeline

Run the six stages in order:

1. Evidence Mining
2. Story Reconstruction
3. Forces Analysis
4. Job Hypothesis
5. Opportunity Signals
6. Validation Plan

## Stage 1: Evidence Mining

Extract structured evidence first — do not analyze. For every piece of evidence,
record an id, a type, the raw quote, a normalized restatement, and a confidence.

Evidence types: trigger, behavior, pain, consequence, previous_solution,
current_solution, workaround, attempt, decision_criteria, switching_signal,
anxiety, habit, willingness_to_pay, frequency, context.

Then label every claim as exactly one of:

- FACT — the source said or did it, verifiable from the text.
- INFERENCE — your grounded inference from a fact.
- HYPOTHESIS — a leap to a need, solution, or market that must be validated.

HYPOTHESIS is never presented as FACT.

Read `references/evidence-taxonomy.md` for the full schema and edge cases.

## Stage 2: Story Reconstruction

Reconstruct the timeline before abstracting to a Job:

Context → Previous Situation → Trigger → First Thought → Search → Attempts
→ Decision → Current Workaround.

Mark every element Known / Unknown / Assumed. Never invent a missing element —
list it under Missing Story Elements instead.

Read `references/switching-story.md` for the reconstruction questions.

## Stage 3: Forces Analysis

Analyze the four switching forces, each tied to Evidence IDs:

- Push — the pain of the old way, driving the user away.
- Pull — the attraction of the new way.
- Habit — inertia of the current behavior.
- Anxiety — risks/fears about the new way.

`anxiety` may have empty evidence (the user didn't say) — mark it explicitly.
Read `references/forces-of-progress.md`.

## Stage 4: Job Hypothesis

Never write "User needs X." Use:

> When [situation], I want to [motivation / progress], so I can [desired outcome].

Classify each as Primary Functional Job, Related Functional Job, Emotional Job
(confidence / control / reduced anxiety / trust), or Social Job (only with
evidence). When evidence is ambiguous, generate multiple hypotheses.

Read `references/job-formulation.md`.

## Stage 5: Opportunity Signals

Build an evidence map — no pseudo-precise score. For each signal
(pain intensity, frequency, existing workaround, active search, switching intent,
willingness to pay) rate it Strong / Medium / Weak / Unknown. Report unknowns
honestly. Give an overall status: 🟢 strong / 🟡 promising but insufficient /
🔴 weak.

## Stage 6: Validation Plan

Output the missing evidence, the next actions, and auto-generated follow-up
interview questions. Then hand off to idea-validation:

> 证据到这一步了，运行 `/idea-validation`，把下面这个 problem hypothesis + 目标用户
> 喂进去做交互式验证。

## Output

Produce a Job Discovery Report using `references/discovery-report.md`. Display it
in full in the terminal and save it to `state/job_report_<slug>.md` (kebab-case
slug derived from the source or the primary Job).

## Reference Files

- `references/evidence-taxonomy.md`
- `references/switching-story.md`
- `references/forces-of-progress.md`
- `references/job-formulation.md`
- `references/discovery-report.md`
````

- [ ] **Step 2: Verify frontmatter and pipeline structure**

Run:
```bash
grep -q '^name: job-discovery' skills/job-discovery/SKILL.md && echo "name OK"
for s in "Evidence Mining" "Story Reconstruction" "Forces Analysis" "Job Hypothesis" "Opportunity Signals" "Validation Plan"; do grep -q "Stage [0-9]: $s" skills/job-discovery/SKILL.md || echo "MISSING: $s"; done
grep -q '^12\. Do not invent frequency' skills/job-discovery/SKILL.md && echo "12 rules OK"
```
Expected: prints `name OK`, no MISSING lines, and `12 rules OK`.

- [ ] **Step 3: Commit**

```bash
git add skills/job-discovery/SKILL.md
git commit -m "feat(job-discovery): add SKILL.md with 6-stage pipeline"
```

---

### Task 2: references/evidence-taxonomy.md

**Files:**
- Create: `skills/job-discovery/references/evidence-taxonomy.md`

**Interfaces:**
- Consumes: the labels `FACT / INFERENCE / HYPOTHESIS` and the 15 evidence types named in Task 1 Stage 1.
- Produces: the evidence schema and three-way separation that Tasks 3–6 and `evals.json` (cases 1, 2, 3) rely on.

- [ ] **Step 1: Write the full reference**

````markdown
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
````

- [ ] **Step 2: Verify key sections exist**

Run:
```bash
grep -q "Evidence schema" skills/job-discovery/references/evidence-taxonomy.md && \
grep -q "Evidence types" skills/job-discovery/references/evidence-taxonomy.md && \
grep -q "FACT / INFERENCE / HYPOTHESIS" skills/job-discovery/references/evidence-taxonomy.md && \
grep -q "Terminology mapping" skills/job-discovery/references/evidence-taxonomy.md && echo "OK"
```
Expected: prints `OK`.

- [ ] **Step 3: Commit**

```bash
git add skills/job-discovery/references/evidence-taxonomy.md
git commit -m "feat(job-discovery): add evidence-taxonomy reference"
```

---

### Task 3: references/switching-story.md

**Files:**
- Create: `skills/job-discovery/references/switching-story.md`

**Interfaces:**
- Consumes: the timeline steps named in Task 1 Stage 2.
- Produces: the Known/Unknown/Assumed marking rule and the 7-step timeline that Stage 2 and `evals.json` (case 2) rely on.

- [ ] **Step 1: Write the full reference**

````markdown
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
````

- [ ] **Step 2: Verify key sections exist**

Run:
```bash
grep -q "seven-step timeline" skills/job-discovery/references/switching-story.md && \
grep -q "Known / Unknown / Assumed" skills/job-discovery/references/switching-story.md && \
grep -q "Missing Story Elements" skills/job-discovery/references/switching-story.md && echo "OK"
```
Expected: prints `OK`.

- [ ] **Step 3: Commit**

```bash
git add skills/job-discovery/references/switching-story.md
git commit -m "feat(job-discovery): add switching-story reference"
```

---

### Task 4: references/forces-of-progress.md

**Files:**
- Create: `skills/job-discovery/references/forces-of-progress.md`

**Interfaces:**
- Consumes: the four forces named in Task 1 Stage 3 and the Evidence IDs from Task 2.
- Produces: the four-force format with evidence traceability that Stage 3 and `evals.json` (case 5) rely on.

- [ ] **Step 1: Write the full reference**

````markdown
# Forces of Progress

The four forces that determine whether a person switches from the current way to a new way. Model them as two opposing pairs.

```
               PUSH                 PULL
       旧方案的痛苦 ──────────►  新方案的吸引力
             │                       │
   CURRENT ──┴───────────────────────┴── NEW
             ▲                       ▲
             │                       │
           HABIT                  ANXIETY
          旧习惯的惯性            新方案的风险
```

## The four forces

- **Push** — the pain of the current way, driving the user away from it.
- **Pull** — the attraction of the new way, drawing the user toward it.
- **Habit** — inertia of the current behavior; why they stay.
- **Anxiety** — fears and risks about the new way; why they hesitate.

A Job is worth switching for when Push + Pull outweigh Habit + Anxiety. If Habit + Anxiety dominate, the person is not actually ready to switch — no matter how loud the complaint.

## Format

Each force is a list of statements, each tied to Evidence IDs:

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

## Traceability rules

- Every statement cites its supporting evidence ids. `anxiety` may be `[]` — the user said nothing about risk — but the field must be present.
- A force with no evidence at all is a gap, not a finding. Put it in the report's Missing Evidence section.
- Do not invent a Pull or an Anxiety the user never expressed. An empty `pull` is a strong, honest signal: there is pain but no articulated desired state yet.

## Reading the forces

- Strong Push + weak Pull → clear pain, no articulated solution → the Job is real, the solution space is open.
- Strong Push + strong Pull + low Anxiety → high switching intent.
- Strong Habit + strong Anxiety → sticky; switching is unlikely without de-risking.
````

- [ ] **Step 2: Verify key sections exist**

Run:
```bash
grep -q "The four forces" skills/job-discovery/references/forces-of-progress.md && \
grep -q "Traceability rules" skills/job-discovery/references/forces-of-progress.md && \
grep -q "Reading the forces" skills/job-discovery/references/forces-of-progress.md && echo "OK"
```
Expected: prints `OK`.

- [ ] **Step 3: Commit**

```bash
git add skills/job-discovery/references/forces-of-progress.md
git commit -m "feat(job-discovery): add forces-of-progress reference"
```

---

### Task 5: references/job-formulation.md

**Files:**
- Create: `skills/job-discovery/references/job-formulation.md`

**Interfaces:**
- Consumes: the Job classes named in Task 1 Stage 4.
- Produces: the When/I want/So I can template and 4 Job classes that Stage 4 and `evals.json` (cases 1, 4) rely on.

- [ ] **Step 1: Write the full reference**

````markdown
# Job Formulation

A Job is the progress a person is trying to make in a situation — not the feature they asked for, not the product they imagine.

## The formulation template

Forbid "User needs X." Use:

> When **[situation]**, I want to **[motivation / progress]**, so I can **[desired outcome]**.

Example:

> When an autonomous agent is running a long task,
> I want to know when meaningful human intervention is required,
> so I can avoid continuously monitoring the execution while maintaining
> confidence in the outcome.

## Job classes

### Primary Functional Job
The core task the person is trying to accomplish. One per analysis, though you may be uncertain which of two candidates is primary — say so.

### Related Functional Jobs
Sub-jobs required to complete the primary Job. Often the real unmet need hides here.

### Emotional Job
How the person wants to feel: confidence, control, reduced anxiety, trust. Only list what the source supports.

### Social Job
How the person wants to be seen by others. Only when the source supports it — never invent one.

## One complaint ≠ one Job

The same complaint can map to multiple Jobs. "我一直要盯着 Agent" could be:

- Primary: know whether the agent is in an abnormal state
- Related: reduce the cost of human supervision
- Related: intervene before a failure happens
- Emotional: maintain a sense of control over an autonomous system

Generate all hypotheses the evidence supports. Do not collapse to a single answer when the evidence is ambiguous.

## Rules

- Every Job statement must be traceable to Evidence IDs.
- A Job is about progress, not about the tool. "Use a monitoring dashboard" is not a Job; "know when to intervene" is.
- Write Jobs in solution-free language. If a Job statement names a product or a feature, it's still a solution in disguise — rewrite it.
````

- [ ] **Step 2: Verify key sections exist**

Run:
```bash
grep -q "formulation template" skills/job-discovery/references/job-formulation.md && \
grep -q "Job classes" skills/job-discovery/references/job-formulation.md && \
grep -q "One complaint ≠ one Job" skills/job-discovery/references/job-formulation.md && echo "OK"
```
Expected: prints `OK`.

- [ ] **Step 3: Commit**

```bash
git add skills/job-discovery/references/job-formulation.md
git commit -m "feat(job-discovery): add job-formulation reference"
```

---

### Task 6: references/discovery-report.md

**Files:**
- Create: `skills/job-discovery/references/discovery-report.md`

**Interfaces:**
- Consumes: the report sections named in Tasks 1–5 (evidence, timeline, forces, job hypotheses, opportunity signals, validation plan).
- Produces: the exact report template with the interview-followup section that Stage 6 and all `evals.json` cases rely on.

- [ ] **Step 1: Write the full reference**

````markdown
# Job Discovery Report

Copy this template exactly. Replace bracketed placeholders with findings. Leave a section as "Not assessed" if the stage wasn't reached.

---

# Job Discovery Report: [source / primary Job]

**Date**: [YYYY-MM-DD]
**Source**: [interview | tweet | reddit | github | review | support | chat | other]
**Confidence**: [high | medium | low]

---

## 1. Situation

用户在做什么：[one line]

## 2. Evidence

### E1 — [type]

> [原始 quote]

Normalized: [restatement]
Label: [FACT | INFERENCE | HYPOTHESIS]
Confidence: [high | medium | low]

### E2 — [type]
...

## 3. Behavioral Timeline

```
Context →
Previous Situation →
Trigger →
First Thought →
Search →
Attempts →
Decision →
Current Workaround
```

[Mark each step Known / Unknown / Assumed.]

### Missing Story Elements
- [frequency? commercial products tried? willingness to pay? real cost?]

## 4. Forces of Progress

| Force | Statement | Evidence |
|---|---|---|
| Push | ... | E1, E2 |
| Pull | ... | E3 |
| Habit | ... | E1 |
| Anxiety | ... | (none stated) |

## 5. Job Hypotheses

### Primary Functional Job
When [situation], I want to [progress], so I can [outcome].
Evidence: E1, E2, E4 — Confidence: [high | medium | low]

### Related Functional Jobs
- ...

### Emotional Job
- ...

### Social Job
- ... (only if supported; otherwise "none in evidence")

## 6. Opportunity Signals

| Signal | Assessment |
|---|---|
| Pain intensity | Strong / Medium / Weak / Unknown |
| Frequency | ... |
| Existing workaround | ... |
| Active search | ... |
| Switching intent | ... |
| Willingness to pay | ... |

**Status**: 🟢 strong / 🟡 promising but insufficient evidence / 🔴 weak

## 7. Missing Evidence

- [list what's still unknown]

## 8. Next Validation

1. [next action]
2. [next action]
3. [next action]

### Follow-up interview questions
- 你最近一次遇到这种情况是什么时候？当时在做什么任务？
- 你现在是怎么避免这个问题的？
- 你试过哪些工具或方案？为什么没继续用？
- 失败一次会造成什么实际损失？

→ 证据到这一步了，运行 `/idea-validation`，把上面这个 problem hypothesis + 目标用户喂进去做交互式验证。

## Bottom Line

Current hypothesis: [one sentence]

**Do not build yet / Ready for validation / Strong opportunity signal**
````

- [ ] **Step 2: Verify key sections exist**

Run:
```bash
grep -q "Job Discovery Report" skills/job-discovery/references/discovery-report.md && \
grep -q "Forces of Progress" skills/job-discovery/references/discovery-report.md && \
grep -q "Opportunity Signals" skills/job-discovery/references/discovery-report.md && \
grep -q "Follow-up interview questions" skills/job-discovery/references/discovery-report.md && \
grep -q "idea-validation" skills/job-discovery/references/discovery-report.md && echo "OK"
```
Expected: prints `OK`.

- [ ] **Step 3: Commit**

```bash
git add skills/job-discovery/references/discovery-report.md
git commit -m "feat(job-discovery): add discovery-report reference"
```

---

### Task 7: evals/evals.json

**Files:**
- Create: `skills/job-discovery/evals/evals.json`

**Interfaces:**
- Consumes: the behaviors defined in Tasks 1–6 (FACT/INFERENCE/HYPOTHESIS separation, Known/Unknown marking, four forces with evidence traceability, multiple Job hypotheses, honest opportunity map).
- Produces: five eval cases, one per failure mode from the design doc.

- [ ] **Step 1: Write the full evals file**

````json
{
  "skill_name": "job-discovery",
  "evals": [
    {
      "id": 1,
      "prompt": "用户说：'I need better monitoring for my AI agents.' Mine the Job from this.",
      "expected_output": "Does NOT treat 'better monitoring' as the Job. Notes it's a feature request/solution language. Extracts whatever behavior is present (almost none) and flags the absence of behavior as a gap. Job hypothesis is deferred or low-confidence, not fabricated.",
      "files": [],
      "assertions": [
        {"name": "Feature request not treated as a Job", "description": "Does not output 'Job = monitor agents'; flags 'better monitoring' as solution language, not a Job"},
        {"name": "No fabricated behavior", "description": "Does not invent a timeline, frequency, or cost not present in the one-line input"},
        {"name": "Missing evidence flagged", "description": "Reports that the input has no behavioral evidence"}
      ]
    },
    {
      "id": 2,
      "prompt": "访谈片段：'昨天我的 Agent 跑了两个小时，最后发现是 Context 里一个参数传错了，我最后只能重新跑。' Mine it.",
      "expected_output": "Extracts FACT (agent ran 2 hours, param wrong, reran). Reconstructs a partial timeline (trigger = agent failure; current workaround = rerun). Marks frequency, previous solutions, willingness to pay as Unknown — does NOT invent them.",
      "files": [],
      "assertions": [
        {"name": "FACT vs INFERENCE separated", "description": "Stated facts labeled FACT; any inference (e.g. 'root cause hard to trace') labeled INFERENCE, not FACT"},
        {"name": "Missing elements marked Unknown", "description": "Frequency, prior solutions, payment are listed Unknown, not fabricated"},
        {"name": "Timeline partial but honest", "description": "Reconstructs what's known; Missing Story Elements lists the gaps"}
      ]
    },
    {
      "id": 3,
      "prompt": "一条 tweet：'Every SaaS company needs an AI agent that auto-updates their docs.' Mine it.",
      "expected_output": "The product/market claim is labeled HYPOTHESIS, never FACT. No behavioral evidence is extractable from a solution assertion. Report states the Job cannot be reconstructed from this source alone.",
      "files": [],
      "assertions": [
        {"name": "Solution/market claim = HYPOTHESIS", "description": "'needs an AI agent' labeled HYPOTHESIS, not FACT"},
        {"name": "No Job fabricated", "description": "Does not invent a Job from a solution assertion; says the Job is not reconstructable from this source"}
      ]
    },
    {
      "id": 4,
      "prompt": "'我一直要盯着 Agent，很烦。' Mine it — note the ambiguity.",
      "expected_output": "Generates MULTIPLE Job hypotheses (know abnormal state / reduce supervision cost / intervene before failure / maintain control), not a single overconfident answer. Marks the emotional Job (control) as supported by '很烦'.",
      "files": [],
      "assertions": [
        {"name": "Multiple Job hypotheses", "description": "Outputs more than one Job hypothesis, not a single answer"},
        {"name": "Emotional Job identified", "description": "Identifies a control/anxiety emotional Job supported by the frustration"}
      ]
    },
    {
      "id": 5,
      "prompt": "Analyze the four forces for this source: 'I built a timeout + Slack notification because manually watching the agent was eating my day, but I'm worried an automated tool would false-positive and I'd miss real failures.'",
      "expected_output": "Four forces, each tied to Evidence IDs: Push (manual watching eats the day), Pull (none clearly stated — user built their own), Habit (manual workflow), Anxiety (false positives, missing real failures). Pull may be empty — reported honestly. Opportunity map marks unknowns honestly.",
      "files": [],
      "assertions": [
        {"name": "Four forces present", "description": "Push/Pull/Habit/Anxiety all present, each with a statement"},
        {"name": "Forces tied to evidence", "description": "Each force statement references evidence ids; empty pull is explicit, not omitted"},
        {"name": "Anxiety captured", "description": "False-positive / miss-real-failure concern captured under Anxiety"},
        {"name": "No invented signals", "description": "Frequency/payment marked Unknown, not invented"}
      ]
    }
  ]
}
````

- [ ] **Step 2: Validate JSON**

Run:
```bash
python3 -m json.tool skills/job-discovery/evals/evals.json > /dev/null && echo "JSON OK"
```
Expected: prints `JSON OK`.

- [ ] **Step 3: Commit**

```bash
git add skills/job-discovery/evals/evals.json
git commit -m "feat(job-discovery): add 5 eval cases"
```

---

### Task 8: Final conformance check

**Files:**
- Verify: `skills/job-discovery/` (all of the above)

- [ ] **Step 1: Confirm the full tree**

Run:
```bash
find skills/job-discovery -type f | sort
```
Expected:
```
skills/job-discovery/SKILL.md
skills/job-discovery/evals/evals.json
skills/job-discovery/references/discovery-report.md
skills/job-discovery/references/evidence-taxonomy.md
skills/job-discovery/references/forces-of-progress.md
skills/job-discovery/references/job-formulation.md
skills/job-discovery/references/switching-story.md
```

- [ ] **Step 2: Cross-check against the design doc**

Confirm each design requirement has a home:
- 6-stage pipeline → `SKILL.md` "The Pipeline" + Stage 1–6 headers
- boundary (no verdict, no clustering) → `SKILL.md` "What This Skill Does / Does Not Do"
- FACT/INFERENCE/HYPOTHESIS → `SKILL.md` Stage 1 + `evidence-taxonomy.md`
- timeline + Known/Unknown/Assumed → `switching-story.md`
- four forces + evidence traceability → `forces-of-progress.md`
- Job formulation + classes → `job-formulation.md`
- report template + handoff → `discovery-report.md`
- 5 eval cases → `evals/evals.json` ids 1–5

Run:
```bash
grep -q "idea-validation" skills/job-discovery/SKILL.md && \
grep -q "does NOT mine/cluster" skills/job-discovery/SKILL.md && \
grep -q '"id": 5' skills/job-discovery/evals/evals.json && echo "CONFORMANCE OK"
```
Expected: prints `CONFORMANCE OK`.

- [ ] **Step 3: Commit any fixes**

Only if Step 1/2 surfaced a gap:
```bash
git add -A skills/job-discovery && git commit -m "chore(job-discovery): fix conformance gaps"
```
If nothing changed, no commit is needed.
