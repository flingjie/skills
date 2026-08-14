# continuous-discovery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create the `continuous-discovery` Claude Code skill — turn opportunities into validated solutions via an Opportunity Solution Tree, assumption mapping, experiment design, and a learning loop held in a persistent `state/discovery_state.json`.

**Architecture:** A single skill (`skills/continuous-discovery/`) mirroring the existing `idea-validation`/`problem-discovery`/`job-discovery` layouts: one `SKILL.md` with the loop + two entry modes, four `references/` files (opportunity-solution-tree, assumption-framework, experiment-patterns, discovery-state), and an `evals/evals.json`. No code — Markdown + JSON content.

**Tech Stack:** Markdown (SKILL.md, references), JSON (evals.json + the `state/discovery_state.json` schema).

## Global Constraints

- Match existing conventions: `SKILL.md` with YAML frontmatter (`name`, `description`), a `references/` dir, an `evals/evals.json`.
- `name:` in frontmatter MUST equal the directory name: `continuous-discovery`.
- Starts from an opportunity. It must NOT collect signals (→ `problem-discovery`), identify Jobs/opportunities from raw evidence (→ `job-discovery`), or give a build/don't-build verdict (→ `idea-validation`).
- Persistent state is a single `state/discovery_state.json` (load at start, save at end). No multi-file `.discovery/` dir.
- No separate `templates/` or `examples/` dir.
- Do NOT modify the other skills.
- Evals are authored as JSON and validated syntactically, not auto-run.

---

## File Structure

```
skills/continuous-discovery/
├── SKILL.md                          # core principles + loop + two modes + Never/Prefer + output
├── references/
│   ├── opportunity-solution-tree.md  # OST + no-jump rule + 3+ solutions
│   ├── assumption-framework.md       # 4 assumption classes + riskiest assumption
│   ├── experiment-patterns.md        # experiment design + ladder
│   └── discovery-state.md            # JSON schema + learning loop + solution≠opportunity
└── evals/evals.json                  # 5 eval cases
```

Each file has one responsibility. `SKILL.md` is the entry point and references the four `references/` files; `evals.json` encodes the behaviors the other five files must produce.

---

### Task 1: SKILL.md (entry point)

**Files:**
- Create: `skills/continuous-discovery/SKILL.md`

**Interfaces:**
- Produces: the skill's `name` (`continuous-discovery`), `description` trigger phrases, the core principles, the loop, the two entry modes, and pointers to the four reference files (Tasks 2–5) by exact path.

- [ ] **Step 1: Write the full SKILL.md**

````markdown
---
name: continuous-discovery
description: >
  Turn customer opportunities into validated solutions through a continuous
  loop — Opportunity Solution Tree, solution generation, assumption mapping,
  experiment design, and a learning loop — maintained in a persistent
  Discovery State. Use when the user has an opportunity (from job-discovery or
  problem-discovery) and wants to advance it ("把这个机会展开成方案", "build an
  opportunity solution tree", "这个方案有哪些假设", "design an experiment",
  "验证这个假设", "update my discovery state with this result"). Based on
  Continuous Discovery Habits (Teresa Torres). Starts from an opportunity — it
  does NOT collect signals (→ problem-discovery), identify Jobs (→ job-discovery),
  or give a build/don't-build verdict (→ idea-validation).
---

# Continuous Discovery

You are a Continuous Discovery Agent. You turn opportunities into validated solutions through a loop of solution generation, assumption mapping, and experiments — never by jumping straight to a solution, and never by declaring an opportunity validated without evidence.

## What This Skill Does / Does Not Do

| Does | Does NOT |
|------|----------|
| Build/update an Opportunity Solution Tree | Collect signals (→ problem-discovery) |
| Generate ≥3 path-distinct solutions per opportunity | Identify Jobs/opportunities from raw evidence (→ job-discovery) |
| Extract value/usability/adoption/business assumptions | Give a build/don't-build verdict (→ idea-validation) |
| Design the cheapest-reliable experiment | Run the experiment (the user does) |
| Ingest results and update the Discovery State | Emit a one-off report |

## Core Principles

1. Opportunity ≠ Solution — always generate ≥3 solutions; never collapse an
   opportunity into its first solution.
2. A solution must be decomposed into assumptions.
3. Validate the riskiest assumption first — the one whose falsity would kill the
   opportunity, not the one easiest to test.
4. Discovery is a loop — persistent state, not a one-off report.
5. Solution failure ≠ Opportunity failure — a failed solution may still point at a
   valid opportunity; update confidence and next question, don't discard.

## Two Entry Modes

- **expand** — given an opportunity, run steps 1–6.
- **learn** — given an experiment result, run step 8.

## The Loop

1. Ingest Opportunity — verify it has evidence; flag if not.
2. Build/Update OST.
3. Generate Solutions — ≥3, path-distinct.
4. Extract Assumptions — value/usability/adoption/business.
5. Identify Riskiest Assumption.
6. Design Experiment — cheapest reliable.
7. (user runs the experiment)
8. Learn & Update State.

## Stage details (pointers)

- OST + solution generation: `references/opportunity-solution-tree.md`
- Assumptions + riskiest: `references/assumption-framework.md`
- Experiment design + ladder: `references/experiment-patterns.md`
- State schema + learning loop: `references/discovery-state.md`

## Never

- Treat a feature request as a validated opportunity.
- Jump directly from problem to solution.
- Generate pseudo-variety (Replay v1 / v2 / v3).
- Assume willingness to pay without evidence.
- Declare an opportunity validated without an experiment.
- Confuse solution validation with opportunity validation.

## Prefer

- Evidence over interpretation.
- Opportunities over feature requests.
- Multiple solutions over the first solution.
- Small experiments over large implementations.
- Continuous learning over one-time research.

## Output

Load `state/discovery_state.json` at the start (create
`{ "goal": null, "opportunities": [], "experiments": [], "learnings": [] }` if
missing); save it back at the end. Display the updated state and, for `expand`, a
human-readable OST view; for `learn`, the updated confidence and next question.

## Reference Files

- `references/opportunity-solution-tree.md`
- `references/assumption-framework.md`
- `references/experiment-patterns.md`
- `references/discovery-state.md`
````

- [ ] **Step 2: Verify frontmatter, principles, modes, and loop**

Run:
```bash
grep -q '^name: continuous-discovery' skills/continuous-discovery/SKILL.md && echo "name OK"
for s in "Ingest Opportunity" "Build/Update OST" "Generate Solutions" "Extract Assumptions" "Identify Riskiest Assumption" "Design Experiment" "Learn & Update State"; do grep -q "$s" skills/continuous-discovery/SKILL.md || echo "MISSING: $s"; done
grep -q '^5\. Solution failure ≠ Opportunity failure' skills/continuous-discovery/SKILL.md && echo "5 principles OK"
grep -q '^## Two Entry Modes' skills/continuous-discovery/SKILL.md && echo "modes OK"
```
Expected: prints `name OK`, no MISSING lines, `5 principles OK`, `modes OK`.

- [ ] **Step 3: Commit**

```bash
git add skills/continuous-discovery/SKILL.md
git commit -m "feat(continuous-discovery): add SKILL.md with loop + two modes"
```

---

### Task 2: references/opportunity-solution-tree.md

**Files:**
- Create: `skills/continuous-discovery/references/opportunity-solution-tree.md`

**Interfaces:**
- Consumes: the OST vocabulary (`desired outcome` / `opportunity` / `solution`) and the ≥3-solutions rule from Task 1.
- Produces: the OST structure + no-jump rule that Tasks 3–5 and `evals.json` (cases 1, 2) rely on.

- [ ] **Step 1: Write the full reference**

````markdown
# Opportunity Solution Tree

The OST maps a desired outcome to opportunities to solutions. It is the map that keeps discovery honest: an opportunity is the progress the user wants; a solution is one concrete way to get it.

## Three layers

1. **Desired Outcome** — the high-level goal (one per tree).
2. **Opportunities** — the distinct unmet needs under that outcome.
3. **Solutions** — ≥3 concrete approaches per opportunity.

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

## The no-jump rule

Never collapse an opportunity into a solution. "Agent Debug 很困难" is an opportunity; "做一个 Agent Replay" is a solution. Write the opportunity first, then generate solutions under it.

## Solution generation rules

- ≥3 solutions per opportunity.
- Each solution is a genuinely different path. `Replay v1 / v2 / v3` is NOT variety — it's one solution with cosmetic variants.
- A solution names a mechanism, not a brand or a feature-list.
- If you can't generate 3 distinct paths, the opportunity is probably too narrow — broaden it.

## Distinguishing opportunity from solution

| Opportunity (progress) | Solution (mechanism) |
|---|---|
| 快速定位 Agent 失败原因 | Execution Replay |
| 知道 Agent 是否卡住 | Loop Detector |
| 判断 Prompt 修改是否有效 | Evaluation |

## Updating the tree

When new evidence changes an opportunity's confidence, update the tree in `state/discovery_state.json`, don't create a parallel doc.
````

- [ ] **Step 2: Verify key sections exist**

Run:
```bash
grep -q "Three layers" skills/continuous-discovery/references/opportunity-solution-tree.md && \
grep -q "no-jump rule" skills/continuous-discovery/references/opportunity-solution-tree.md && \
grep -q "Solution generation rules" skills/continuous-discovery/references/opportunity-solution-tree.md && \
grep -q "≥3 solutions per opportunity" skills/continuous-discovery/references/opportunity-solution-tree.md && echo "OK"
```
Expected: prints `OK`.

- [ ] **Step 3: Commit**

```bash
git add skills/continuous-discovery/references/opportunity-solution-tree.md
git commit -m "feat(continuous-discovery): add opportunity-solution-tree reference"
```

---

### Task 3: references/assumption-framework.md

**Files:**
- Create: `skills/continuous-discovery/references/assumption-framework.md`

**Interfaces:**
- Consumes: the assumption decomposition rule from Task 1.
- Produces: the four assumption classes and the riskiest-assumption rule that Task 4 and `evals.json` (cases 3, 4) rely on.

- [ ] **Step 1: Write the full reference**

````markdown
# Assumption Framework

Every solution rests on unproven assumptions. Before building, extract them and find the one most worth testing.

## Four classes

```yaml
assumptions:
  value:     [用户确实需要理解 execution, Replay 能帮助定位, 定位能省时间]
  usability: [用户能理解 Replay, 用户能找到关键步骤]
  adoption:  [用户愿意把 Replay 纳入日常流程]
  business:  [用户愿意付费]
```

- **value** — the solution actually creates value the user wants.
- **usability** — the user can use it to get that value.
- **adoption** — the user will integrate it into their routine.
- **business** — it can sustain itself (payment, cost).

## Extraction

For a solution, ask:
- value: 用户真的需要这个吗？它真能帮用户完成目标吗？
- usability: 用户能理解并使用它吗？关键操作找得到吗？
- adoption: 用户愿意把它纳入日常吗？有什么会阻止他们坚持用？
- business: 用户愿意付钱吗？谁拍板？

## The riskiest assumption

Identify the assumption whose falsity would kill the opportunity — not the one easiest to test.

- If "Replay 能帮助定位" is false, the Replay solution collapses.
- "用户愿意付费" being false does NOT kill the opportunity — you can test payment later.

Test order = risk to the opportunity, not convenience.

## Rule

Every assumption is `unvalidated` until an experiment says otherwise. An assumption with no experiment is a claim, not evidence.
````

- [ ] **Step 2: Verify key sections exist**

Run:
```bash
grep -q "Four classes" skills/continuous-discovery/references/assumption-framework.md && \
grep -q "riskiest assumption" skills/continuous-discovery/references/assumption-framework.md && \
grep -q "value" skills/continuous-discovery/references/assumption-framework.md && \
grep -q "usability" skills/continuous-discovery/references/assumption-framework.md && \
grep -q "adoption" skills/continuous-discovery/references/assumption-framework.md && \
grep -q "business" skills/continuous-discovery/references/assumption-framework.md && echo "OK"
```
Expected: prints `OK`.

- [ ] **Step 3: Commit**

```bash
git add skills/continuous-discovery/references/assumption-framework.md
git commit -m "feat(continuous-discovery): add assumption-framework reference"
```

---

### Task 4: references/experiment-patterns.md

**Files:**
- Create: `skills/continuous-discovery/references/experiment-patterns.md`

**Interfaces:**
- Consumes: the cheapest-reliable-experiment principle from Task 1 and the assumption classes from Task 3.
- Produces: the experiment shape and the experiment ladder that Task 5 and `evals.json` (case 5) rely on.

- [ ] **Step 1: Write the full reference**

````markdown
# Experiment Patterns

Design the cheapest experiment that can reliably test the riskiest assumption. Cheapest reliable, not easiest to run.

## Experiment shape

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

- `hypothesis` — the specific assumption under test, as a falsifiable statement.
- `method` — one of the ladder below.
- `target_users` — who and how many.
- `success_metric` — observable, pre-committed thresholds.
- `evidence_required` — what to collect (behavior, not opinion).

## The experiment ladder (cheap → expensive)

1. **interview** — ask about past behavior (see idea-validation's Mom Test).
2. **prototype** — a clickable fake; observe use.
3. **fake door** — advertise the feature; measure click/interest.
4. **concierge** — do the job manually for the user.
5. **wizard of oz** — fake the automation behind the scenes.
6. **MVP** — the smallest real product.
7. **production** — full build.

Principle: don't build before validating. Climb only when the cheaper rung can't answer the question.

## Method ↔ assumption class

- value → interview / prototype / fake door
- usability → prototype / wizard of oz
- adoption → concierge / MVP
- business → fake door / concierge (pricing)

## Success criteria rules

- Pre-commit metrics BEFORE running — no moving the goalposts.
- Metrics observe behavior (task completion, time, retention), not opinions ("users said they liked it").
- Record `partially_validated` honestly when results are mixed.
````

- [ ] **Step 2: Verify key sections exist**

Run:
```bash
grep -q "Experiment shape" skills/continuous-discovery/references/experiment-patterns.md && \
grep -q "experiment ladder" skills/continuous-discovery/references/experiment-patterns.md && \
grep -q "fake door" skills/continuous-discovery/references/experiment-patterns.md && \
grep -q "wizard of oz" skills/continuous-discovery/references/experiment-patterns.md && \
grep -q "cheapest" skills/continuous-discovery/references/experiment-patterns.md && echo "OK"
```
Expected: prints `OK`.

- [ ] **Step 3: Commit**

```bash
git add skills/continuous-discovery/references/experiment-patterns.md
git commit -m "feat(continuous-discovery): add experiment-patterns reference"
```

---

### Task 5: references/discovery-state.md

**Files:**
- Create: `skills/continuous-discovery/references/discovery-state.md`

**Interfaces:**
- Consumes: the persistent-state principle from Task 1 and the experiment shape from Task 4.
- Produces: the `state/discovery_state.json` schema and the learning loop that `SKILL.md` Stage 8 and `evals.json` (case 5) rely on.

- [ ] **Step 1: Write the full reference**

````markdown
# Discovery State

The persistent source of truth is `state/discovery_state.json`. Load it at the start, save it at the end. The OST is a view generated from this state, not a separate file.

## Schema

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

## Field meanings

- `goal` — the desired outcome; `null` until set.
- `opportunities[]` — each has `id` (O-NNN), `statement`, `evidence` (refs to upstream evidence ids), `confidence` (`low`|`medium`|`high`), and nested `solutions[]`.
- `solutions[].assumptions[]` — each has `id` (A-NNN), `type` (`value`|`usability`|`adoption`|`business`), `statement`, and `status` (`unvalidated`|`validated`|`invalidated`).
- `experiments[]` — each has `id` (EXP-NNN), `assumption` (A-id), `method`, `status` (`designed`|`running`|`done`), and optionally `result`.
- `learnings[]` — one entry per completed experiment.

## The learning loop

When a result comes in (entry mode `learn`), record a learning and update state:

```yaml
learning:
  experiment: EXP-003
  result: partially_validated
  conclusion: "Replay 有价值，但用户真正要的不是 Replay，而是快速定位 Failure"
  opportunity_update: { confidence: high }
  next_question: "诊断时哪些信息最有用？"
```

- `result` — `validated` | `partially_validated` | `invalidated`.
- `opportunity_update` — the change to the opportunity's confidence.
- `next_question` — the next thing worth testing.

## Solution failure ≠ Opportunity failure

A `invalidated` solution does NOT mean the opportunity is dead. Distinguish:

- opportunity validated + solution invalidated → generate a different solution.
- opportunity invalidated → the opportunity itself may be wrong; lower its confidence and reconsider the tree.

Update the opportunity's confidence, never discard it on a single failed solution.

## Persistence

- Load at start; if missing, start with `{ "goal": null, "opportunities": [], "experiments": [], "learnings": [] }`.
- Save at end. Keep `id`s stable; append, don't rewrite.
````

- [ ] **Step 2: Verify key sections exist**

Run:
```bash
grep -q "Schema" skills/continuous-discovery/references/discovery-state.md && \
grep -q "Field meanings" skills/continuous-discovery/references/discovery-state.md && \
grep -q "learning loop" skills/continuous-discovery/references/discovery-state.md && \
grep -q "Solution failure ≠ Opportunity failure" skills/continuous-discovery/references/discovery-state.md && \
grep -q "state/discovery_state.json" skills/continuous-discovery/references/discovery-state.md && echo "OK"
```
Expected: prints `OK`.

- [ ] **Step 3: Commit**

```bash
git add skills/continuous-discovery/references/discovery-state.md
git commit -m "feat(continuous-discovery): add discovery-state reference"
```

---

### Task 6: evals/evals.json

**Files:**
- Create: `skills/continuous-discovery/evals/evals.json`

**Interfaces:**
- Consumes: the behaviors defined in Tasks 1–5 (no-jump rule, ≥3 path-distinct solutions, four assumption classes, riskiest-assumption, learning loop + solution≠opportunity).
- Produces: five eval cases, one per failure mode from the design doc.

- [ ] **Step 1: Write the full evals file**

````json
{
  "skill_name": "continuous-discovery",
  "evals": [
    {
      "id": 1,
      "prompt": "我想做一个 Agent Debug 工具。帮我 discovery。",
      "expected_output": "Does not jump to a solution. Notes 'Agent Debug 工具' is a solution, not an opportunity; abstracts to the underlying opportunity (e.g. 开发者缺少快速定位失败原因的能力) before generating solutions.",
      "files": [],
      "assertions": [
        {"name": "Not solution-first", "description": "Does not treat 'Agent Debug 工具' as the opportunity; abstracts to an opportunity first"},
        {"name": "Opportunity before solutions", "description": "Writes an opportunity statement before any solution"}
      ]
    },
    {
      "id": 2,
      "prompt": "Opportunity: Agent 开发者缺少快速定位 execution failure 的能力。帮我展开。",
      "expected_output": "Generates ≥3 path-distinct solutions (e.g. Execution Replay, Failure Analyzer, AI Debugger), NOT cosmetic variants of one idea (no Replay v1/v2/v3).",
      "files": [],
      "assertions": [
        {"name": "At least 3 solutions", "description": "≥3 solutions under the opportunity"},
        {"name": "Path-distinct", "description": "Solutions are genuinely different mechanisms, not version variants"}
      ]
    },
    {
      "id": 3,
      "prompt": "Solution: Execution Replay。帮我拆假设。",
      "expected_output": "Extracts assumptions across all four classes (value/usability/adoption/business), not just value.",
      "files": [],
      "assertions": [
        {"name": "Four classes covered", "description": "Assumptions span value, usability, adoption, business — not value-only"},
        {"name": "Assumptions are falsifiable", "description": "Each assumption is a specific claim an experiment could test"}
      ]
    },
    {
      "id": 4,
      "prompt": "假设：A1 Replay 能帮助定位问题；A2 用户愿意付费；A3 用户能理解 Replay 界面。哪个最该先验证？",
      "expected_output": "Identifies A1 (Replay 能帮助定位) as the riskiest — if false, the whole Replay solution collapses — rather than A2 (payment, testable later) or A3 (usability, cheaper to test). Chooses by cost-of-being-wrong, not ease-of-testing.",
      "files": [],
      "assertions": [
        {"name": "Riskiest = highest cost if false", "description": "Picks the assumption whose falsity kills the solution (A1), not the easiest to test"},
        {"name": "Reasoning given", "description": "Explains why A1 over A2/A3"}
      ]
    },
    {
      "id": 5,
      "prompt": "实验结果：4/5 用户看懂了 Replay，但 3/5 说他们真正需要的是快速定位失败原因而不是回放本身，2/5 更喜欢直接看日志。",
      "expected_output": "Records a learning (Replay 有价值但用户真正要的是快速定位失败); updates the opportunity confidence rather than discarding it; sets next_question = 诊断时哪些信息最有用. Does NOT declare the opportunity dead.",
      "files": [],
      "assertions": [
        {"name": "Learning recorded", "description": "Records a learning with result/conclusion/next_question"},
        {"name": "Opportunity not discarded", "description": "Updates opportunity confidence rather than removing it (solution≠opportunity)"},
        {"name": "Next question generated", "description": "Produces the next question to test"}
      ]
    }
  ]
}
````

- [ ] **Step 2: Validate JSON**

Run:
```bash
python3 -m json.tool skills/continuous-discovery/evals/evals.json > /dev/null && echo "JSON OK"
```
Expected: prints `JSON OK`.

- [ ] **Step 3: Commit**

```bash
git add skills/continuous-discovery/evals/evals.json
git commit -m "feat(continuous-discovery): add 5 eval cases"
```

---

### Task 7: Final conformance check

**Files:**
- Verify: `skills/continuous-discovery/` (all of the above)

- [ ] **Step 1: Confirm the full tree**

Run:
```bash
find skills/continuous-discovery -type f | sort
```
Expected:
```
skills/continuous-discovery/SKILL.md
skills/continuous-discovery/evals/evals.json
skills/continuous-discovery/references/assumption-framework.md
skills/continuous-discovery/references/discovery-state.md
skills/continuous-discovery/references/experiment-patterns.md
skills/continuous-discovery/references/opportunity-solution-tree.md
```

- [ ] **Step 2: Cross-check against the design doc**

Confirm each design requirement has a home:
- loop + two modes → `SKILL.md` "The Loop" + "Two Entry Modes"
- boundary (no signal-collection/verdict) → `SKILL.md` "What This Skill Does / Does Not Do"
- OST + no-jump + 3+ solutions → `opportunity-solution-tree.md`
- four assumption classes + riskiest → `assumption-framework.md`
- experiment design + ladder → `experiment-patterns.md`
- state schema + learning loop + solution≠opportunity → `discovery-state.md`
- 5 eval cases → `evals/evals.json` ids 1–5

Run:
```bash
grep -q "does NOT collect signals" skills/continuous-discovery/SKILL.md && \
grep -q "build/don't-build verdict" skills/continuous-discovery/SKILL.md && \
grep -q '"id": 5' skills/continuous-discovery/evals/evals.json && echo "CONFORMANCE OK"
```
Expected: prints `CONFORMANCE OK`.

- [ ] **Step 3: Commit any fixes**

Only if Step 1/2 surfaced a gap:
```bash
git add -A skills/continuous-discovery && git commit -m "chore(continuous-discovery): fix conformance gaps"
```
If nothing changed, no commit is needed.
