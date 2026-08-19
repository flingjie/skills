#!/usr/bin/env python3
"""List project-scoped skills (name + description), one line each.

Scans only project-local skill directories — `.claude/skills/` and a top-level
`skills/` — and never `~/.claude/skills` (global) or plugin directories. That
scope is what keeps the list limited to the current project.
"""

import glob
import os
import re
import sys

# Project-local roots only. Deliberately excluded:
#   ~/.claude/skills  (global) and plugin dirs.
PROJECT_ROOTS = (".claude/skills", "skills")


def parse_skill(path):
    """Return (name, description) from a SKILL.md's frontmatter, or None."""
    text = open(path, encoding="utf-8").read()
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    if not m:
        return None
    fm = m.group(1)

    name_m = re.search(r"^name:\s*([^\s]+)", fm, re.M)
    name = name_m.group(1) if name_m else os.path.basename(os.path.dirname(path))

    desc_m = re.search(r"^description:\s*([^\n]*)", fm, re.M)
    if not desc_m:
        return name, ""
    first = desc_m.group(1).strip()
    if first != ">":
        return name, first

    # Folded scalar (">"): continuation lines are indented deeper than the key.
    indent = len(desc_m.group(0)) - len(desc_m.group(0).lstrip())
    lines = []
    for line in fm[desc_m.end():].lstrip("\n").splitlines():
        if not line.strip():
            break
        if len(line) - len(line.lstrip()) <= indent:
            break
        lines.append(line.strip())
    return name, " ".join(lines)


def main():
    seen, rows = set(), []
    for root in PROJECT_ROOTS:
        if not os.path.isdir(root):
            continue
        for f in sorted(glob.glob(os.path.join(root, "**", "SKILL.md"), recursive=True)):
            rp = os.path.realpath(f)
            if rp in seen:
                continue
            seen.add(rp)
            parsed = parse_skill(f)
            if parsed:
                rows.append(parsed)

    if not rows:
        print("No project skills found.")
        sys.exit(0)

    rows.sort(key=lambda r: r[0].lower())
    width = max(len(n) for n, _ in rows) + 2
    for n, d in rows:
        print(f"{n:<{width}}{d}")
    print(f"\n{len(rows)} project skill(s) — global/plugin skills excluded.")


if __name__ == "__main__":
    main()
