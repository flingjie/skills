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
