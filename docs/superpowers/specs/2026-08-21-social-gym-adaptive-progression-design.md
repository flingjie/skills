# Social Gym Adaptive Progression Design

**Date:** 2026-08-21  
**Status:** Approved design  
**Scope:** Optimize the existing `social-gym` skill while preserving all seven training modes.

## 1. Summary

`social-gym` currently provides rich conversation simulations, targeted drills, four difficulty levels, feedback, and retry behavior. However, each invocation is effectively an isolated exercise. The skill does not establish a baseline, retain evidence of improvement, select exercises based on recurring weaknesses, or distinguish a one-off good response from reliable mastery.

This design adds an adaptive coaching layer above the seven existing modes. A new user completes a lightweight three-scenario diagnostic. A returning user receives one evidence-backed training focus selected from a persistent competency profile. Every session follows a practice-feedback-retry loop and records only compact behavioral evidence, not full transcripts. Progress uses evidence-based mastery stages rather than a 100-point score.

The seven existing modes remain directly callable:

1. Full Conversation
2. Opening Drill
3. Follow-up Drill
4. Story Mining
5. Self Introduction
6. Conversation Recovery
7. Random Challenge

## 2. Goals

- Turn independent exercises into a cross-session learning system.
- Identify a user's highest-leverage weakness from observed behavior.
- Make progress measurable without false numeric precision.
- Adapt mode, scenario, and difficulty while respecting explicit user choices.
- Preserve realistic simulation and prevent the role-played person from becoming an overly cooperative chatbot.
- Make feedback concise, behavioral, and immediately actionable.
- Preserve all seven existing modes and their explicit invocation paths.
- Add regression evals for routing, simulation, progression, persistence, and failure handling.

## 3. Non-goals

- Building a fixed course with mandatory unlocks.
- Adding points, streaks, badges, leaderboards, or other gamification.
- Analyzing historical conversation transcripts; that remains outside this skill's boundary.
- Saving full role-play transcripts in the progression store.
- Providing therapy, personality diagnosis, dating manipulation, or techniques for pressuring another person.
- Adding voice, video, multi-user simulation, or external services.
- Replacing the user's explicit mode selection with automatic routing.

## 4. Existing Problems

The current implementation is a single 1,114-line `SKILL.md` with no supporting references or evals. Its breadth is a strength, but several behaviors are underspecified:

- the default session has no memory of prior performance;
- the 100-point review implies precision without defining evidence thresholds;
- several dimensions overlap, such as Curiosity, Follow-up, Story Mining, Naturalness, and Connection;
- there is no rule for when a skill is learned versus merely demonstrated once;
- difficulty describes persona behavior but not how evidence should be interpreted across contexts;
- simulation state, progressive disclosure, and role consistency depend on ad hoc model behavior;
- the review format is long enough to compete with actual practice;
- no eval protects the seven modes, the no-lecture default, or the retry loop.

## 5. Architecture

The optimized skill consists of three layers with separate responsibilities.

### 5.1 Adaptive Coach

The adaptive coach owns session-level decisions:

- load and validate the profile;
- start the diagnostic when no profile exists;
- select one training focus for a returning user;
- choose a compatible mode, difficulty, persona, and scenario;
- preserve an explicitly requested mode;
- request a review and retry at the appropriate time;
- convert observed behavior into evidence;
- update the profile after the retry or at an early session exit.

The adaptive coach does not role-play the person directly and does not define competency thresholds. It orchestrates those components.

### 5.2 Training Modes

The seven modes generate and run exercises. They do not maintain independent levels or scores. A mode receives:

- one target competency;
- a difficulty;
- scenario preferences and diversity constraints;
- relevant profile evidence;
- simulation rules.

A mode returns observations about behavior actually elicited in that exercise. It must not claim evidence for a competency the session did not expose.

### 5.3 Competency and Evidence Model

The competency model defines observable behaviors, evidence records, mastery stages, and transition rules. It is shared by every mode, which prevents the same behavior from receiving conflicting interpretations in different drills.

## 6. Proposed File Structure

```text
skills/social-gym/
├── SKILL.md
├── references/
│   ├── competency-model.md
│   ├── diagnostic.md
│   ├── session-orchestration.md
│   ├── simulation-rules.md
│   └── review-and-progression.md
└── evals/
    └── evals.json
```

Responsibilities:

- `SKILL.md`: purpose, trigger boundary, routing, default behavior, mode index, and non-negotiable interaction rules.
- `competency-model.md`: seven competencies, observable evidence, mastery stages, and transition rules.
- `diagnostic.md`: the three diagnostic scenarios, observation coverage, and initial profile behavior.
- `session-orchestration.md`: focus selection, mode mapping, difficulty selection, diversity, and session lifecycle.
- `simulation-rules.md`: hidden persona card, progressive disclosure, role consistency, and difficulty behavior.
- `review-and-progression.md`: concise review, hint ladder, retry comparison, persistence schema, and errors.
- `evals/evals.json`: behavioral regression cases.

Runtime state is stored separately at:

```text
state/social_gym_profile.json
```

## 7. Competency Model

The profile tracks seven trainable competencies.

### 7.1 Opening

Observable target behaviors:

- uses the shared situation or an immediate observation;
- is easy to answer without demanding disclosure;
- matches the setting and relationship distance;
- avoids a rehearsed pitch or forced cleverness.

### 7.2 Listening & Reaction

Observable target behaviors:

- acknowledges what the other person just said;
- reacts before asking the next question;
- reflects emotional or situational meaning without over-interpreting;
- avoids treating the answer as a prompt for an unrelated question.

### 7.3 Threading

Observable target behaviors:

- notices a specific live conversational thread;
- follows that thread instead of jumping to a questionnaire;
- connects the next response to the other person's wording;
- changes threads when the current one has no energy.

### 7.4 Story Development

Observable target behaviors:

- moves naturally from fact to experience, motivation, change, or turning point;
- uses context-sensitive questions rather than repeating “why?”;
- recognizes when a story has emotional or narrative potential;
- does not force depth when the other person declines it.

### 7.5 Reciprocity

Observable target behaviors:

- shares relevant personal context without taking over the conversation;
- uses acknowledge → explore → share → return when appropriate;
- avoids both interview mode and monologue mode;
- gives the other person room to redirect or ask back.

### 7.6 Self-introduction & Hook

Observable target behaviors:

- explains what the user does in clear, audience-appropriate language;
- includes an interesting problem or point of view;
- leaves a natural open loop;
- avoids a résumé or technology-list dump.

### 7.7 Recovery & Exit

Observable target behaviors:

- distinguishes a weak thread from a person who wants to disengage;
- can follow, switch, pause, or exit based on the signal;
- repairs a minor awkward moment without over-apologizing;
- ends respectfully rather than forcing every conversation to continue.

### 7.8 Outcome Indicators

`Curiosity`, `Naturalness`, and `Connection` remain useful review language but are not standalone mastery tracks. They are outcomes inferred from the seven observable competencies. They must not receive independent levels or generate duplicate evidence.

## 8. Mastery Stages and Evidence Rules

Each competency has one of four stages:

```text
Unassessed → Emerging → Developing → Reliable
```

- `Unassessed`: insufficient behavior has been observed.
- `Emerging`: at least one relevant positive behavior has appeared, but it is assisted, isolated, or inconsistent.
- `Developing`: the behavior has appeared independently in multiple distinct contexts.
- `Reliable`: the behavior remains present across varied modes, contexts, and difficulty constraints.

### 8.1 Evidence Record

Each evidence item stores:

```json
{
  "session_id": "2026-08-21T19:30:00Z-opening-01",
  "observed_at": "2026-08-21T19:33:00Z",
  "competency": "threading",
  "polarity": "positive",
  "behavior_code": "thread_followed",
  "behavior": "Reacted to the career-change clue and followed that thread instead of jumping to company facts.",
  "mode": "full_conversation",
  "difficulty": "normal",
  "scenario_tags": ["meetup", "stranger", "career-change"],
  "attempt": "retry",
  "assistance": "attention_hint"
}
```

Allowed `polarity` values are `positive` and `counter`. Allowed `attempt` values are `first` and `retry`. Allowed `assistance` values are `none`, `attention_hint`, `strategy_hint`, `direction_examples`, and `full_example`. `behavior_code` comes from the authoritative per-competency taxonomy in `competency-model.md`; examples include `react_before_ask`, `thread_followed`, `question_jumping`, `conversation_hijack`, `resume_dump`, and `forced_continuation`.

A distinct scenario category is a unique combination of setting, relationship distance, and interaction constraint—for example, `meetup + stranger + open`, rather than merely a different topic in the same social setup. This prevents superficial prompt variation from satisfying cross-context mastery thresholds.

The evidence record contains a behavioral summary, not a full transcript. A short excerpt may appear in the user-facing review but is not persisted by default.

### 8.2 Stage Transitions

Transitions are deterministic:

- `Unassessed → Emerging`: at least one relevant positive item.
- `Emerging → Developing`: at least three positive items, including at least two first-attempt items with `assistance: none`, across at least two distinct scenario categories.
- `Developing → Reliable`: at least five first-attempt positive items with `assistance: none`, across at least three scenario categories and at least two modes; among the three newest observations for that competency, at least two must be positive and no counter `behavior_code` may repeat.

Evidence after a `full_example` demonstrates practice participation but cannot satisfy an independent-evidence threshold. A successful retry without wording supplied by the coach is positive learning evidence, but it does not count as first-attempt independent evidence.

### 8.3 Counter Evidence and Reconfirmation

A single counter item never lowers a stage. Two counter items with the same `behavior_code` among the latest three observations for that competency set:

```json
"needs_reconfirmation": true
```

The competency becomes a priority for a future session but retains its current stage. Reconfirmation clears after two first-attempt, unassisted positive items in two distinct scenarios. This prevents one bad day from erasing progress while still detecting regression.

The store retains at most the newest 20 evidence items per competency. Stage and reconfirmation calculations use retained evidence only.

## 9. Persistent Profile

The state file has this shape:

```json
{
  "schema_version": 1,
  "created_at": "2026-08-21T19:30:00Z",
  "updated_at": "2026-08-21T19:45:00Z",
  "preferences": {
    "goals": [],
    "scenario_tags": [],
    "language": "zh-CN"
  },
  "diagnostic": {
    "status": "complete",
    "completed_at": "2026-08-21T19:45:00Z"
  },
  "current_focus": "threading",
  "competencies": {
    "opening": {
      "stage": "emerging",
      "needs_reconfirmation": false,
      "evidence": []
    }
  },
  "recent_sessions": [
    {
      "session_id": "2026-08-21T19:30:00Z-diagnostic-01",
      "mode": "diagnostic",
      "difficulty": "normal",
      "scenario_tags": ["meetup"],
      "focus": "baseline",
      "result": "complete"
    }
  ]
}
```

The real file contains all seven competency keys. `recent_sessions` retains the newest 30 session summaries. It does not contain transcripts.

## 10. First-use Diagnostic

When the profile does not exist, the skill starts immediately with a short explanation and the first scenario. It must not deliver a theory lecture or ask the user to configure every preference first.

The diagnostic consists of three mini-scenarios totaling approximately 7–9 user turns.

### Scenario 1: Enter the Conversation

Observes:

- Opening
- Self-introduction & Hook
- basic Listening & Reaction

The scenario includes a shared environmental cue and a natural opportunity for the simulated person to ask what the user does.

### Scenario 2: Develop a Thread

Observes:

- Listening & Reaction
- Threading
- Story Development
- Reciprocity

The simulated person provides layered information over several turns. The user must notice a promising clue rather than interview mechanically.

### Scenario 3: Respond to Friction

Observes:

- Recovery & Exit
- Threading under weak engagement
- respect for boundaries

The scenario includes a short answer, distraction, fading interest, or interrupted conversation. The correct outcome may be a switch or graceful exit rather than continuation.

The diagnostic remains a sample, not a certification. It may set `Emerging` or `Developing` only when the corresponding thresholds are actually met; it cannot set `Reliable`. Competencies with inadequate observations remain `Unassessed`.

At the end, the user receives:

- one observed strength;
- one highest-leverage growth area;
- the initial stage summary;
- the recommended first training focus;
- an invitation to begin that exercise.

## 11. Session Orchestration

### 11.1 Default Invocation

```text
Load profile
  ↓
Missing profile? ── yes → diagnostic
  ↓ no
Select one focus
  ↓
Select mode, difficulty, persona, and scenario
  ↓
Announce one behavioral objective
  ↓
Run exercise
  ↓
Review one strength and one leverage miss
  ↓
Retry the same node
  ↓
Compare behavior
  ↓
Persist evidence and next focus
```

### 11.2 Focus Selection Priority

The coach chooses in this order:

1. a competency explicitly requested by the user;
2. a competency marked `needs_reconfirmation`;
3. the lowest-stage competency with sufficient evidence to identify a repeated weakness;
4. an `Unassessed` competency that has not been sampled;
5. the least recently tested competency.

Tie-breakers favor the user's preferred real-world scenarios, then mode and scenario diversity.

### 11.3 Mode Mapping

Primary mappings:

- Opening → Opening Drill or Full Conversation
- Listening & Reaction → Follow-up Drill or Full Conversation
- Threading → Follow-up Drill, Story Mining, or Full Conversation
- Story Development → Story Mining or Full Conversation
- Reciprocity → Full Conversation or Random Challenge
- Self-introduction & Hook → Self Introduction or Full Conversation
- Recovery & Exit → Conversation Recovery or Random Challenge

The planner must not select the same mode for three adaptive sessions in a row when another appropriate mode exists.

### 11.4 Explicit Mode Invocation

If the user requests a mode, that choice wins. The coach may adapt the scenario, focus, and difficulty within the requested mode. It may briefly state the selected focus but must not redirect the user to a different mode unless the requested mode cannot exercise the stated goal, in which case it asks one concise clarifying question.

### 11.5 Difficulty Selection

- New or `Emerging` competency: start at Easy or Normal.
- `Developing`: normally use Normal, occasionally Hard for transfer testing.
- `Reliable`: use Hard or Expert for reconfirmation and generalization.
- After repeated counter evidence, reduce only the interaction constraint needed to isolate the skill; do not automatically make the whole scenario Easy.

Difficulty changes between sessions, not unpredictably mid-session, unless Random Challenge explicitly includes an unexpected event.

## 12. Simulation Rules

Every role-play creates a hidden persona card with:

- background relevant to the scenario;
- current purpose;
- mood and social energy;
- conversational style;
- active interests and low-interest topics;
- information available at surface, fact, experience, motivation, story, and emotion layers;
- boundaries;
- conditions for increased engagement;
- conditions for disengagement or a natural ending.

Only information justified by the current layer and conversation is revealed. The role-played person:

- has their own agenda and does not exist solely to reward the user;
- may answer briefly, redirect, ask back, become interested, lose interest, or leave;
- remains consistent with established facts and emotional state;
- does not become hostile merely to simulate difficulty;
- does not disclose sensitive or deep material simply because the user asked a direct question.

Difficulty is behavioral:

- `Easy`: visible clues, high willingness to engage, forgiving transitions.
- `Normal`: available but layered clues, ordinary social effort.
- `Hard`: weaker clues, limited attention, selective engagement, or mild ambiguity.
- `Expert`: multiple participants, time pressure, competing goals, interruptions, or ambiguous signals.

A person's status or perceived value is not itself a difficulty mechanic.

## 13. Feedback, Hints, and Retry

### 13.1 Coaching Timing

During Full Conversation, the assistant remains in character. It does not provide turn-by-turn praise or instruction unless:

- the user explicitly asks for live coaching;
- the user asks for help;
- the user is clearly stuck;
- the scene naturally ends.

Targeted one-response drills may evaluate after the response because evaluation is part of their mode contract.

### 13.2 Default Review

The default review is concise:

```text
本轮证据
- 一个做得好的具体行为
- 一个最高杠杆的错失机会

今天的一个重点
- 下一次只改变的一个行为

Retry
- 同一人物、同一节点、同一已知信息

档案变化
- 新增的证据
- 阶段变化，或明确说明“证据已增加，阶段暂不变化”
```

The review cites concrete behavior from the current exchange. It does not use a 100-point score. A user may request a deeper narrative review, but deeper output still follows the evidence model. If the user asks for a numeric score, explain that the skill uses evidence-backed stages because its scores are not psychometrically calibrated, then provide the behavioral summary and stage evidence instead.

### 13.3 Hint Ladder

When the user is stuck, escalate only as needed:

1. `attention_hint`: identify a clue worth noticing;
2. `strategy_hint`: suggest react, follow, share, switch, or exit;
3. `direction_examples`: provide two possible directions, not one canonical line;
4. `full_example`: provide a complete example only on explicit request or after lower-level hints fail.

The assistance level is attached to resulting evidence.

### 13.4 Retry Comparison

The retry preserves the same persona, conversation state, and disclosed information. It evaluates behavioral change, not stylistic polish. The comparison asks whether the user:

- reacted before questioning;
- followed the current thread;
- reduced question jumping;
- balanced exploration and sharing;
- recognized a switch or exit signal.

Both the original miss and the adjusted behavior remain evidence. A successful retry does not erase the original observation.

## 14. Error Handling and User Control

- **Missing profile:** start the diagnostic.
- **Malformed or unsupported profile:** do not overwrite it silently. Explain that progress cannot be loaded and ask whether to rebuild the profile. Continue practice in memory if the user declines.
- **Write failure:** finish the session, disclose that the record was not saved, and do not claim cross-session progress was updated.
- **Insufficient evidence:** leave the competency `Unassessed`; do not infer a stage.
- **Interrupted session:** save only observations already supported by behavior and mark the session `interrupted`; do not generate a complete-session conclusion.
- **Changed goals or preferred scenarios:** update preferences without deleting competency evidence.
- **Profile reset:** confirm before deleting or replacing the file.
- **User asks to see progress:** show stages, recent supporting evidence, reconfirmation flags, and current focus without exposing hidden persona cards.
- **User asks not to save:** run the session in memory and skip all profile writes.

## 15. Backward Compatibility

All seven existing modes remain available and retain their central purpose. The optimization changes defaults and review behavior:

- a bare invocation becomes diagnostic or adaptive rather than always Full Conversation / Normal;
- existing explicit mode invocations continue to route to that mode;
- `/social-gym full` is added as an explicit Full Conversation alias so the former bare-invocation behavior remains directly available;
- the uncalibrated 100-point review is retired and replaced by evidence-backed stages; an optional deeper narrative review remains available;
- the core retry loop remains mandatory;
- existing principles such as Curiosity over Cleverness, React Before Asking, Avoid Conversation Hijacking, Hook over Résumé, and Connection over Performance remain represented in the competency model and feedback rules.

There is no pre-existing profile migration because the current skill has no persistent state.

## 16. Evaluation Strategy

`evals/evals.json` will contain approximately 12–16 high-value cases in four groups.

### 16.1 Routing and Compatibility

- bare invocation with no state starts diagnostic scenario 1 without a lecture;
- bare invocation with a profile selects one evidence-backed focus;
- all existing explicit modes route correctly, and `/social-gym full` directly starts Full Conversation;
- explicit mode selection is not overridden by adaptive routing.

### 16.2 Simulation Behavior

- the assistant advances one turn and waits;
- hidden information is not dumped at the start;
- Full Conversation stays in character rather than grading each turn;
- Hard and Expert use interaction constraints rather than hostility;
- the simulated conversation may end naturally when interest is absent.

### 16.3 Evidence and Progression

- only elicited competencies receive evidence;
- a single success cannot produce `Reliable`;
- repeated independent evidence across contexts advances a stage;
- a single counter item does not lower a stage;
- a repeated counter pattern sets `needs_reconfirmation`;
- retry evidence preserves assistance and attempt metadata;
- persisted state excludes full transcript content;
- the review cites behavior and states whether the stage changed.

### 16.4 Errors and Boundaries

- malformed state is not silently overwritten;
- a write failure is disclosed;
- interrupted sessions do not receive fabricated complete scores;
- resetting state requires confirmation;
- a request to analyze a past transcript is kept outside the simulation contract.

Each eval includes a prompt, optional state fixture, expected output, file expectations, and independently judgeable assertions.

## 17. Manual Acceptance Paths

### 17.1 New User

1. Invoke `/social-gym` with no profile.
2. Confirm the skill starts diagnostic scenario 1 directly.
3. Complete all three mini-scenarios.
4. Confirm the initial profile contains only supported evidence and no `Reliable` stages.
5. Confirm the skill offers one recommended first focus.

### 17.2 Returning User

1. Start with a profile containing a repeated Threading weakness.
2. Invoke `/social-gym` without a mode.
3. Confirm Threading is selected and mapped to an appropriate non-repeated mode.
4. Complete the scene and retry the same node.
5. Confirm both attempts are represented in evidence and the stage changes only if thresholds are met.

### 17.3 Explicit Mode User

1. Start with a profile whose highest-priority weakness is Recovery.
2. Invoke `/social-gym story`.
3. Confirm Story Mining remains the active mode.
4. Confirm scenario and difficulty use relevant profile context without redirecting to Recovery.
5. Confirm only competencies actually observed receive evidence.

## 18. Acceptance Criteria

The implementation is complete when:

- all seven existing modes remain directly callable, with `/social-gym full` providing explicit access to Full Conversation after the bare invocation becomes adaptive;
- a new user enters a three-scenario diagnostic without a long explanation;
- a returning user receives exactly one evidence-backed training focus;
- explicit mode selection always wins over automatic mode selection;
- every mastery stage is explainable from retained behavioral evidence;
- one session cannot establish `Reliable` mastery;
- simulation uses a consistent hidden persona with progressive disclosure;
- default feedback contains concrete evidence, one focus, and a same-node retry;
- the profile stores summaries and evidence rather than full transcripts;
- malformed state and write failures are surfaced rather than hidden;
- profile reset is confirmed before destructive action;
- evals cover default routing, all explicit modes, simulation behavior, progression rules, and state failures.

## 19. Implementation Constraints

- Keep `SKILL.md` concise enough to serve as an executable routing contract; move detailed, mode-independent rules to references.
- Avoid duplicate rules across reference files. Each behavior must have one authoritative definition.
- Use the repository's existing `evals/evals.json` convention.
- Match the repository's existing relative `state/` persistence convention.
- Do not add dependencies, scripts, or runtime services for this optimization.
- Do not implement features outside the goals and acceptance criteria in this document.
