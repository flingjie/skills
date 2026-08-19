---
name: list-project-skills
description: >
  List the skills defined in the current project only — their names and
  descriptions, read from the project's .claude/skills/ or top-level skills/
  directory — explicitly excluding global (~/.claude/skills) and plugin skills.
  Use when the user wants to see what skills this project defines ("列出项目里的
  skill", "当前项目有哪些 skill", "这个项目有什么 skill", "有哪些本地 skill",
  "list project skills", "show available skills", "what skills does this
  project have"). It lists project-scoped skills only; it does NOT enumerate
  global or plugin skills.
---

# List Project Skills

## Purpose

Produce a clean list of the skills defined in the current project — one line
per skill, showing its name and description.

Scope is strictly project-local. Global and plugin skills are out of scope.

---

## Scope Boundary

| Included | Excluded |
|----------|----------|
| `.claude/skills/**/SKILL.md` (Claude Code project convention) | `~/.claude/skills/` (global) |
| `skills/**/SKILL.md` (this repo's top-level dir) | plugin directories (`~/.claude/plugins/`) |

Only scan project-local directories. Never scan the user's home skill directory
or plugin directories — that is what keeps the list limited to the current
project.

`.claude/skills` may be a symlink to `skills/` (as in this repo). Deduplicate
by real path so each skill appears exactly once.

---

## How to Run

From the project root:

```bash
python3 scripts/list-project-skills.py
```

---

## Output

Sorted alphabetically by name. One line per skill:

```text
challenger-selling     Move a complex B2B/SaaS/AI sales opportunity ...
daily-review           Guide a fast (5–10 minute) end-of-day reflection ...
list-project-skills    List the skills defined in the current project only ...

14 project skill(s) — global/plugin skills excluded.
```

---

## Notes

- Read the `name` from frontmatter; fall back to the directory name if absent.
- Descriptions use a folded `>` YAML scalar — unfold it to a single line.
- If no project skills exist, say so. Do not fall back to listing global skills.
