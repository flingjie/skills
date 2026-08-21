# Social Gym Codex GUI Enhancement Implementation Plan

> **For agentic workers:** Execute tasks in order. Track progress by changing each `- [ ]` to `- [x]` only after its verification command passes. Preserve the seven existing training modes and all current progression semantics.

**Goal:** Upgrade `social-gym` from a text-only role-play workflow into a richer, reliable Codex GUI training experience with quick-start routing, explicit role/coach controls, deterministic profile updates, resumable sessions, progress views, image-grounded scenarios, and regression coverage.

**Architecture:** Keep `SKILL.md` as a concise router and interaction contract. Put mode behavior, GUI conventions, and scenario generation in references. Move profile validation, stage computation, session recording, and dashboard rendering into deterministic Python scripts. Use Markdown as the universal GUI fallback and HTML/Visualizations only as progressive enhancement.

**Tech Stack:** Markdown, YAML, JSON, Python 3 standard library, HTML/CSS. No external runtime dependencies.

**Source Design:** `docs/superpowers/specs/2026-08-21-social-gym-adaptive-progression-design.md`

---

## Global Constraints

- Preserve all seven direct modes: `full`, `opening`, `followup`, `story`, `intro`, `recovery`, and `random`.
- Preserve the evidence stages and thresholds in `references/competency-model.md` unless a task explicitly migrates the schema.
- Default GUI flow starts practice immediately; do not open with a seven-mode menu or a theory lecture.
- Full Conversation remains in character by default; coaching appears only on a control command, a request for help, a natural ending, or review.
- Persist behavioral summaries only. Never persist full transcripts or hidden persona cards.
- Support a no-save session that performs no profile writes.
- Hard and Expert difficulty use interaction constraints, never hostility or abuse.
- Do not infer personality, intent, identity, emotion, or sensitive traits from an uploaded image.
- Do not make Visualizations availability a requirement for core training.
- Do not add external services, MCP dependencies, voice, cloud sync, or gamification in this implementation.
- Keep `SKILL.md` under 500 lines and avoid duplicating authoritative definitions from references.
- Use `apply_patch` for authored file changes. Do not overwrite unrelated worktree changes.

---

## Target File Structure

```text
skills/social-gym/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   ├── icon-small.svg
│   └── icon-large.png                 # optional; add only if a real asset is produced
├── scripts/
│   ├── profile.py
│   ├── record_session.py
│   ├── compute_progress.py
│   └── render_dashboard.py
├── references/
│   ├── competency-model.md
│   ├── diagnostic.md
│   ├── gui-interaction.md
│   ├── mode-contracts.md
│   ├── review-and-progression.md
│   ├── scenario-library.md
│   ├── session-orchestration.md
│   └── simulation-rules.md
└── evals/
    ├── evals.json
    └── fixtures/
        ├── developing-threading.json
        ├── reliable-threading.json
        └── malformed-profile.json
```

Runtime outputs remain outside the skill package:

```text
state/social_gym_profile.json
state/social-gym-dashboard.html
```

---

## Task 1: Add GUI-facing skill metadata

**Files:**

- Create: `skills/social-gym/agents/openai.yaml`
- Create: `skills/social-gym/assets/icon-small.svg`
- Optional create: `skills/social-gym/assets/icon-large.png`

**Implementation:**

- [ ] Create an original, simple icon suitable for the GUI skill picker. Avoid text inside the icon.
- [ ] Generate `agents/openai.yaml` using the `skill-creator` generator rather than relying on hand-authored metadata.
- [ ] Set these interface values:
  - `display_name`: `Social Gym`
  - `short_description`: `通过真实对话模拟训练开场、接话、追问和救场`
  - `default_prompt`: `开始一次适合我当前水平的社交对话训练。`
- [ ] Keep `policy.allow_implicit_invocation: true`.
- [ ] Reference only assets that actually exist.

**Verification:**

```bash
test -f skills/social-gym/agents/openai.yaml
grep -q 'display_name:.*Social Gym' skills/social-gym/agents/openai.yaml
grep -q 'allow_implicit_invocation: true' skills/social-gym/agents/openai.yaml
test -f skills/social-gym/assets/icon-small.svg
```

**Done when:** Social Gym has a readable display name, description, default prompt, and valid icon in the Codex GUI skill selector.

---

## Task 2: Define the GUI interaction state machine

**Files:**

- Create: `skills/social-gym/references/gui-interaction.md`

**Implementation:**

- [ ] Define the session states: `ROLE`, `COACH`, `REVIEW`, `PAUSED`, and `COMPLETE`.
- [ ] Define legal transitions and what must remain unchanged across each transition.
- [ ] Define these natural-language controls and Chinese/English aliases:
  - hint / 提示
  - pause / 暂停
  - continue / 继续
  - retry / 重来
  - end / 结束
  - switch scenario / 换场景
  - harder / 更难一点
  - no save / 不保存
- [ ] Require one scenario turn per assistant response while in `ROLE`.
- [ ] Require visually distinct labels for role-play and coaching output.
- [ ] Specify that a hint returns to the same persona, node, and disclosed information.
- [ ] Specify Quick Start behavior with exactly three conceptual entry points: direct practice, real-world scenario, and progress view. Do not render a menu unless the user asks for choices.
- [ ] Define graceful behavior for ambiguous control phrases and mid-session topic changes.

**Verification:**

```bash
for state in ROLE COACH REVIEW PAUSED COMPLETE; do grep -q "$state" skills/social-gym/references/gui-interaction.md || echo "MISSING: $state"; done
for control in 提示 暂停 继续 重来 结束 换场景 更难一点 不保存; do grep -q "$control" skills/social-gym/references/gui-interaction.md || echo "MISSING: $control"; done
```

**Done when:** Another Codex instance can deterministically identify the current interaction layer and handle every control without resetting the scene accidentally.

---

## Task 3: Specify all seven mode contracts

**Files:**

- Create: `skills/social-gym/references/mode-contracts.md`

**Implementation:**

- [ ] Define a contract for each existing mode containing:
  - primary and observable secondary competencies;
  - expected user-turn range;
  - coaching timing;
  - completion conditions;
  - retry node;
  - evidence that may be recorded;
  - evidence that must not be inferred.
- [ ] Set suggested ranges:
  - Opening: 1–2 turns
  - Follow-up: 3–4 turns
  - Story: 4–6 turns
  - Full: 8–12 turns
  - Recovery: 2–4 turns
  - Intro: 1 turn
  - Random: 3–6 turns
- [ ] Define what happens when a user ends early or the simulated person naturally leaves.
- [ ] Preserve the rule that an explicit mode always wins over adaptive routing.
- [ ] Define diagnostic as an orchestration flow, not an eighth user-selectable training mode.

**Verification:**

```bash
for mode in "Full Conversation" "Opening Drill" "Follow-up Drill" "Story Mining" "Self Introduction" "Conversation Recovery" "Random Challenge"; do grep -q "$mode" skills/social-gym/references/mode-contracts.md || echo "MISSING: $mode"; done
grep -q 'explicit.*mode\|显式模式' skills/social-gym/references/mode-contracts.md
```

**Done when:** Session length, feedback timing, retry behavior, and evidence coverage are unambiguous for every mode.

---

## Task 4: Build a compositional scenario library

**Files:**

- Create: `skills/social-gym/references/scenario-library.md`
- Modify: `skills/social-gym/references/simulation-rules.md`
- Modify: `skills/social-gym/references/session-orchestration.md`

**Implementation:**

- [ ] Define scenario dimensions rather than fixed scripts:
  - setting;
  - relationship distance;
  - interaction goal;
  - interaction constraint;
  - social energy;
  - language/cultural context.
- [ ] Provide a compact seed catalog for work, community, learning, casual, online, and group settings.
- [ ] Add diversity rules:
  - no repeated setting in the latest five completed sessions when alternatives exist;
  - no repeated persona pattern in the latest three sessions;
  - prefer under-sampled scenario categories for progression evidence.
- [ ] Add a real-world scenario intake that extracts scenario dimensions from the user's description without forcing a questionnaire.
- [ ] Add a transfer-card output with opening anchor, likely cues, one behavior to avoid, and an exit option.
- [ ] Extend simulation rules so personas have independent goals and can naturally disengage.
- [ ] Keep identity/status from being used as a difficulty mechanism.

**Verification:**

```bash
for dimension in setting relationship constraint; do grep -qi "$dimension" skills/social-gym/references/scenario-library.md || echo "MISSING: $dimension"; done
grep -q 'latest five\|最近五' skills/social-gym/references/scenario-library.md
grep -q 'latest three\|最近三' skills/social-gym/references/scenario-library.md
```

**Done when:** The skill can generate varied scenarios from reusable dimensions and translate a user's real event into a focused practice without inventing personal facts.

---

## Task 5: Implement deterministic profile and progression logic

**Files:**

- Create: `skills/social-gym/scripts/profile.py`
- Create: `skills/social-gym/scripts/compute_progress.py`
- Create: `skills/social-gym/evals/fixtures/developing-threading.json`
- Create: `skills/social-gym/evals/fixtures/reliable-threading.json`
- Create: `skills/social-gym/evals/fixtures/malformed-profile.json`
- Modify: `skills/social-gym/references/review-and-progression.md`

**Interfaces:**

```text
python3 skills/social-gym/scripts/profile.py validate --profile <path>
python3 skills/social-gym/scripts/profile.py init --profile <path> [--language zh-CN]
python3 skills/social-gym/scripts/profile.py summary --profile <path>
python3 skills/social-gym/scripts/compute_progress.py --profile <path> [--write]
```

**Implementation:**

- [ ] Use Python standard library only.
- [ ] Validate schema version, all seven competency keys, stage values, evidence enums, and behavior codes.
- [ ] Reject malformed or unsupported profiles without overwriting them.
- [ ] Implement the existing deterministic stage thresholds exactly.
- [ ] Implement `needs_reconfirmation` set and clear rules exactly.
- [ ] Retain at most 20 evidence entries per competency and 30 recent sessions.
- [ ] Make writes atomic using a temporary sibling file followed by `os.replace`.
- [ ] Create a recoverable backup before migrating or replacing a valid existing profile.
- [ ] Return non-zero exit codes and concise errors on invalid data.
- [ ] Document script invocation in `review-and-progression.md`; make the script authoritative for stage computation.

**Tests:**

- [ ] Add `unittest` coverage for:
  - Unassessed → Emerging;
  - Emerging → Developing;
  - Developing → Reliable;
  - single counter does not downgrade;
  - repeated counter sets reconfirmation;
  - two independent positives clear reconfirmation;
  - assisted retry does not count as independent first attempt;
  - retention caps;
  - malformed input is not overwritten.

Place tests under `tests/social_gym/` if the repository convention permits; otherwise use `skills/social-gym/scripts/tests/` and document the chosen location.

**Verification:**

```bash
python3 skills/social-gym/scripts/profile.py validate --profile skills/social-gym/evals/fixtures/developing-threading.json
python3 skills/social-gym/scripts/compute_progress.py --profile skills/social-gym/evals/fixtures/reliable-threading.json
python3 -m unittest discover -s tests/social_gym -p 'test_*.py'
```

Expected: valid fixtures pass, Reliable is computed for the Reliable fixture, all tests pass, and malformed input returns non-zero without modification.

**Done when:** Profile validity and progression no longer depend on free-form model arithmetic.

---

## Task 6: Implement safe session recording and resume

**Files:**

- Create: `skills/social-gym/scripts/record_session.py`
- Modify: `skills/social-gym/references/review-and-progression.md`
- Modify: `skills/social-gym/references/session-orchestration.md`

**Interfaces:**

```text
python3 skills/social-gym/scripts/record_session.py start --profile <path> --session <json>
python3 skills/social-gym/scripts/record_session.py pause --profile <path> --resume-summary <text>
python3 skills/social-gym/scripts/record_session.py complete --profile <path> --session <json> --evidence <json>
python3 skills/social-gym/scripts/record_session.py interrupt --profile <path> --evidence <json>
```

**Implementation:**

- [ ] Add an optional `active_session` object with mode, status, turn, focus, scenario tags, difficulty, and compact resume summary.
- [ ] Never store full transcript turns or the hidden persona card.
- [ ] Resume with the same persona identity, established facts, current node, and disclosed-information boundary using only the compact summary.
- [ ] On complete/interrupted sessions, call shared profile validation and progression logic rather than duplicating it.
- [ ] Support `--no-save` by skipping every write and reporting that the session is in-memory only.
- [ ] On write failure, keep the conversation usable and never claim that progress was saved.

**Verification:**

```bash
python3 -m unittest discover -s tests/social_gym -p 'test_*.py'
rg -n 'transcript|persona_card|hidden persona' skills/social-gym/evals/fixtures state 2>/dev/null || true
```

Manually inspect generated fixture output to confirm that no transcript or hidden persona content was persisted.

**Done when:** A session can pause, resume, finish, or be interrupted without fabricating conclusions or leaking simulated private state.

---

## Task 7: Render GUI-friendly progress views

**Files:**

- Create: `skills/social-gym/scripts/render_dashboard.py`
- Create: `skills/social-gym/assets/dashboard-template.html`
- Modify: `skills/social-gym/references/review-and-progression.md`

**Interfaces:**

```text
python3 skills/social-gym/scripts/render_dashboard.py \
  --profile state/social_gym_profile.json \
  --format markdown

python3 skills/social-gym/scripts/render_dashboard.py \
  --profile state/social_gym_profile.json \
  --format html \
  --output state/social-gym-dashboard.html
```

**Implementation:**

- [ ] Provide a Markdown summary as the universal fallback.
- [ ] Provide a self-contained HTML dashboard with no external scripts, fonts, or network calls.
- [ ] Display all seven stages, current focus, reconfirmation, latest supporting evidence, scenario coverage, and requirements for the next stage.
- [ ] Use stage ladders or segmented progress, not numerical scores or radar charts.
- [ ] Include a text summary and table for accessibility; do not rely on color alone.
- [ ] Escape every profile-derived string before inserting it into HTML.
- [ ] Do not expose hidden personas, transcripts, or raw internal prompts.
- [ ] Treat interactive Visualizations as an optional follow-up, not part of this renderer.

**Verification:**

```bash
python3 skills/social-gym/scripts/render_dashboard.py --profile skills/social-gym/evals/fixtures/developing-threading.json --format markdown
python3 skills/social-gym/scripts/render_dashboard.py --profile skills/social-gym/evals/fixtures/developing-threading.json --format html --output /tmp/social-gym-dashboard.html
test -s /tmp/social-gym-dashboard.html
grep -q '<html' /tmp/social-gym-dashboard.html
```

Open the HTML through the Codex file preview and verify readable layout, keyboard-visible controls if any, and correct stage data.

**Done when:** Users can understand current progress and exactly what evidence is missing without reading JSON.

---

## Task 8: Add image-grounded scenario training

**Files:**

- Modify: `skills/social-gym/references/gui-interaction.md`
- Modify: `skills/social-gym/references/scenario-library.md`
- Modify: `skills/social-gym/references/simulation-rules.md`

**Implementation:**

- [ ] Define how an attached image can ground setting observations and situational opening drills.
- [ ] Require the user to identify the desired training outcome when it is not clear from context.
- [ ] Permit only observable environmental details: layout, objects, signage, activity, spatial relationship, and visible interaction constraints.
- [ ] Prohibit inference of personality, emotional state, intent, profession, relationship, protected attributes, or willingness to engage from appearance.
- [ ] Never identify or speculate about real people in the image.
- [ ] Provide a non-image fallback scenario when image inspection is unavailable.
- [ ] Record scenario evidence as `image_grounded` without retaining the uploaded image in the profile.

**Verification:** Add eval cases for a conference photo, an ambiguous group scene, and a request to judge who is easiest to approach.

**Done when:** Images enrich situational opening practice without becoming a source of unsupported social or identity inference.

---

## Task 9: Refactor SKILL.md into the new entry-point contract

**Files:**

- Modify: `skills/social-gym/SKILL.md`

**Implementation:**

- [ ] Update the frontmatter description to front-load GUI-friendly triggers such as real-world scenario practice, progress viewing, pause/retry, and image-grounded opening practice.
- [ ] Keep the boundary against transcript analysis, therapy, diagnosis, manipulation, and pressure tactics.
- [ ] Replace slash-command-first wording with natural language and `@Social Gym` examples; preserve slash aliases as compatibility paths.
- [ ] Add Quick Start routing.
- [ ] Add the interaction state/control summary.
- [ ] Point to `gui-interaction.md`, `mode-contracts.md`, and `scenario-library.md` with explicit read conditions.
- [ ] Point to scripts with exact commands and specify when each must run.
- [ ] Keep authoritative competency rules in `competency-model.md`, not duplicated in SKILL.md.
- [ ] Keep the file concise and imperative.

**Verification:**

```bash
wc -l skills/social-gym/SKILL.md
for ref in gui-interaction.md mode-contracts.md scenario-library.md competency-model.md review-and-progression.md; do grep -q "$ref" skills/social-gym/SKILL.md || echo "MISSING: $ref"; done
grep -q '不保存\|no-save' skills/social-gym/SKILL.md
```

Expected: fewer than 500 lines, every required reference linked, and no duplicated threshold tables.

**Done when:** A freshly triggered Codex instance can route into practice, use controls, load only relevant references, and call deterministic scripts at lifecycle boundaries.

---

## Task 10: Expand behavioral and GUI regression evals

**Files:**

- Modify: `skills/social-gym/evals/evals.json`

**Implementation:**

- [ ] Preserve all existing 16 evals.
- [ ] Add activation tests for natural requests and `@Social Gym` invocation.
- [ ] Add GUI interaction tests:
  - first screen has one clear action;
  - role/coach labels remain distinct;
  - pause/continue preserves the node;
  - hint escalation preserves assistance level;
  - end permits a graceful exit;
  - switch-scenario preserves focus but changes scenario.
- [ ] Add profile reliability tests matching Tasks 5 and 6.
- [ ] Add scenario diversity tests.
- [ ] Add dashboard privacy and accessibility tests.
- [ ] Add image-grounding safety tests.
- [ ] Add negative-trigger tests for historical transcript analysis, copy editing, therapy, and manipulative requests.
- [ ] Ensure every eval assertion observes output behavior rather than hidden reasoning.

**Verification:**

```bash
python3 -m json.tool skills/social-gym/evals/evals.json >/dev/null
python3 - <<'PY'
import json
from pathlib import Path
p = Path('skills/social-gym/evals/evals.json')
data = json.loads(p.read_text())
ids = [case['id'] for case in data['evals']]
assert len(ids) == len(set(ids)), 'duplicate eval ids'
assert len(ids) >= 30, f'expected at least 30 evals, found {len(ids)}'
print(f'{len(ids)} evals OK')
PY
```

**Done when:** At least 30 evals protect routing, interaction, progression, persistence, diversity, privacy, image safety, and non-trigger boundaries.

---

## Task 11: Validate and forward-test the complete skill

**Files:**

- Modify as required by failures discovered during validation.

**Implementation:**

- [ ] Run the skill-creator validator against `skills/social-gym/`.
- [ ] Run all Python unit tests.
- [ ] Validate every JSON fixture and eval file.
- [ ] Confirm `agents/openai.yaml` still matches the final `SKILL.md`; regenerate if stale.
- [ ] Confirm `.gitignore` excludes runtime state but not skill fixtures/assets.
- [ ] Forward-test with fresh agents only if explicitly authorized at execution time. Give each agent the skill path and a realistic user request without revealing expected answers.
- [ ] Use at least these forward-test scenarios:
  1. first-time diagnostic;
  2. returning user with repeated `questionnaire_mode`;
  3. explicit Full Conversation with pause → hint → continue → review → retry;
  4. real-world work dinner scenario;
  5. image-grounded opening request;
  6. no-save session;
  7. corrupted profile;
  8. progress dashboard request.
- [ ] Record failures as changes to the skill/evals, then rerun validation.

**Verification:**

```bash
python3 /Users/lingjiefan/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/social-gym
python3 -m unittest discover -s tests/social_gym -p 'test_*.py'
python3 -m json.tool skills/social-gym/evals/evals.json >/dev/null
git diff --check
git status --short
```

**Done when:** Structural validation, unit tests, JSON validation, and diff checks pass; forward tests either pass or their failures are captured by new regression assertions.

---

## Task 12: Final acceptance review

- [ ] A new user enters the first diagnostic scene without a menu or lecture.
- [ ] A returning user gets exactly one evidence-backed focus.
- [ ] Explicit mode invocation always wins.
- [ ] Every role-play assistant turn advances only one scene turn.
- [ ] Pause, hint, retry, continue, end, switch scenario, harder, and no-save work consistently.
- [ ] Full Conversation stays in character unless coaching is requested or the scene ends.
- [ ] Retry uses the same persona and node.
- [ ] Profile writes are atomic and validated.
- [ ] Progress stages are computed by scripts, not improvised by the model.
- [ ] No profile contains transcripts, hidden persona cards, or uploaded images.
- [ ] Markdown progress works without GUI preview features.
- [ ] HTML progress renders correctly in Codex GUI preview.
- [ ] Image-grounded training uses only observable environmental facts.
- [ ] Existing seven modes and 16 eval cases remain present.
- [ ] Skill validation, unit tests, JSON validation, and `git diff --check` pass.

---

## Recommended Execution Order and Milestones

### Milestone 1 — Rich interaction without new runtime state

Complete Tasks 1–4 and 9. Ship when GUI metadata, state controls, mode contracts, Quick Start, and varied scenarios work through conversation alone.

### Milestone 2 — Reliable cross-session coaching

Complete Tasks 5–7. Ship when validated profile updates, pause/resume, deterministic progression, and Markdown/HTML progress views pass tests.

### Milestone 3 — Multimodal and regression hardening

Complete Tasks 8, 10, 11, and 12. Ship when image-grounded training, expanded evals, validation, and acceptance review pass.

Do not start plugin packaging, MCP/cloud sync, voice training, or gamification until all three milestones are accepted through real GUI sessions.
