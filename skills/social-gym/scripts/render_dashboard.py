#!/usr/bin/env python3
"""Render a privacy-safe markdown or HTML progress dashboard from a profile."""

import argparse
import html
import sys
from pathlib import Path

from shared import (
    COMPETENCY_KEYS,
    STAGES,
    compute_profile_progress,
    load_profile,
    scenario_category,
)


STAGE_LABELS = {
    "unassessed": "Unassessed",
    "emerging": "Emerging",
    "developing": "Developing",
    "reliable": "Reliable",
}

STAGE_ORDER = ["unassessed", "emerging", "developing", "reliable"]

NEXT_REQUIREMENT = {
    "unassessed": "至少 1 条相关正向证据",
    "emerging": "≥3 条正向，其中 ≥2 条 first + 无辅助，跨 ≥2 个情境类别",
    "developing": "≥5 条 first + 无辅助，跨 ≥3 个情境类别和 ≥2 个模式",
    "reliable": "保持跨情境、跨模式稳定（复核当前阶段）",
}


def recent_scenario_tags(profile):
    tags = set()
    for session in profile.get("recent_sessions", [])[-5:]:
        tags.update(session.get("scenario_tags", []))
    return sorted(tags)


def render_markdown(profile):
    progress = compute_profile_progress(profile)
    lines = [
        "# Social Gym Progress",
        "",
        f"- Current focus: {profile.get('current_focus') or 'none'}",
        f"- Recent sessions: {len(profile.get('recent_sessions', []))}",
        f"- Language: {profile.get('preferences', {}).get('language', 'zh-CN')}",
        "",
        "## Stages",
        "",
        "| Competency | Stage | Reconfirmation | Evidence |",
        "| --- | --- | --- | ---: |",
    ]
    for key in COMPETENCY_KEYS:
        stage, needs_reconfirmation = progress[key]
        count = len(profile["competencies"][key].get("evidence", []))
        marker = "yes" if needs_reconfirmation else ""
        lines.append(
            f"| {key} | {STAGE_LABELS[stage]} | {marker} | {count} |"
        )

    lines.extend(
        [
            "",
            "## Latest supporting evidence",
            "",
        ]
    )
    latest = []
    for key in COMPETENCY_KEYS:
        for item in profile["competencies"][key].get("evidence", [])[-3:]:
            latest.append((key, item))
    if not latest:
        lines.append("No evidence recorded yet.")
    else:
        lines.append("| Competency | Behavior | Mode | Scenario tags |")
        lines.append("| --- | --- | --- | --- |")
        for key, item in latest:
            tags = ", ".join(item.get("scenario_tags", []))
            lines.append(
                f"| {key} | {item.get('behavior', '')} | "
                f"{item.get('mode', '')} | {tags} |"
            )

    lines.extend(
        [
            "",
            "## Scenario coverage (latest 5 sessions)",
            "",
        ]
    )
    tags = recent_scenario_tags(profile)
    lines.append(", ".join(tags) if tags else "No completed scenarios yet.")

    lines.extend(
        [
            "",
            "## Requirements for the next stage",
            "",
        ]
    )
    for key in COMPETENCY_KEYS:
        stage, _ = progress[key]
        lines.append(f"- {key} ({STAGE_LABELS[stage]}): {NEXT_REQUIREMENT[stage]}")

    return "\n".join(lines) + "\n"


def escape_text(value):
    return html.escape(str(value), quote=True)


def stage_segment(key, stage, count, reconfirmation):
    index = STAGE_ORDER.index(stage)
    steps = []
    for position, name in enumerate(STAGE_ORDER):
        if position <= index:
            label = STAGE_LABELS[name]
            status = "done" if position < index else "current"
            cls = f"sg-step {status}"
        else:
            label = STAGE_LABELS[name]
            cls = "sg-step"
        steps.append(
            f'<span class="{cls}" title="{escape_text(label)}">'
            f"{escape_text(label)}</span>"
        )
    flag = (
        '<span class="sg-reconfirmation">needs reconfirmation</span>'
        if reconfirmation
        else ""
    )
    return (
        f'<div class="sg-competency">'
        f'<div class="sg-competency-head"><h3>{escape_text(key)}</h3>{flag}</div>'
        f'<div class="sg-ladder">{"".join(steps)}</div>'
        f'<p class="sg-meta">{escape_text(str(count))} evidence items; '
        f'next: {escape_text(NEXT_REQUIREMENT[stage])}</p>'
        f"</div>"
    )


def render_html(profile):
    template = (Path(__file__).resolve().parents[1] / "assets" / "dashboard-template.html").read_text(
        encoding="utf-8"
    )
    progress = compute_profile_progress(profile)
    segments = "".join(
        stage_segment(
            key,
            progress[key][0],
            len(profile["competencies"][key].get("evidence", [])),
            progress[key][1],
        )
        for key in COMPETENCY_KEYS
    )

    evidence_rows = []
    for key in COMPETENCY_KEYS:
        for item in profile["competencies"][key].get("evidence", [])[-3:]:
            evidence_rows.append(
                "<tr>"
                f"<td>{escape_text(key)}</td>"
                f"<td>{escape_text(item.get('behavior', ''))}</td>"
                f"<td>{escape_text(item.get('mode', ''))}</td>"
                f"<td>{escape_text(', '.join(item.get('scenario_tags', [])))}</td>"
                "</tr>"
            )
    evidence_table = (
        "<table><thead><tr><th>Competency</th><th>Behavior</th>"
        "<th>Mode</th><th>Scenario tags</th></tr></thead><tbody>"
        + "".join(evidence_rows)
        + "</tbody></table>"
    )
    if not evidence_rows:
        evidence_table = "<p>No evidence recorded yet.</p>"

    coverage = ", ".join(recent_scenario_tags(profile)) or "No completed scenarios yet."

    requirement_rows = "".join(
        f"<li>{escape_text(key)} ({escape_text(STAGE_LABELS[progress[key][0]])}): "
        f"{escape_text(NEXT_REQUIREMENT[progress[key][0]])}</li>"
        for key in COMPETENCY_KEYS
    )

    focus = escape_text(profile.get("current_focus") or "none")
    language = escape_text(profile.get("preferences", {}).get("language", "zh-CN"))
    session_count = str(len(profile.get("recent_sessions", [])))
    updated = escape_text(profile.get("updated_at", ""))

    header = (
        f"Current focus: {focus} · Sessions: {session_count} · Language: {language} · "
        f"Updated: {updated}"
    )
    summary = ", ".join(
        escape_text(f"{key}: {STAGE_LABELS[progress[key][0]]}")
        for key in COMPETENCY_KEYS
    )
    replacements = {
        "{{SG_HEADER}}": escape_text(header),
        "{{SG_SUMMARY}}": summary,
        "{{SG_LADDERS}}": segments,
        "{{SG_EVIDENCE}}": evidence_table,
        "{{SG_COVERAGE}}": escape_text(coverage),
        "{{SG_REQUIREMENTS}}": requirement_rows,
    }
    rendered = template
    for token, value in replacements.items():
        rendered = rendered.replace(token, value)
    return rendered


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", required=True)
    parser.add_argument("--format", choices=["markdown", "html"], required=True)
    parser.add_argument("--output", help="write output to a file instead of stdout")
    args = parser.parse_args(argv)

    profile, errors = load_profile(args.profile)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    rendered = render_html(profile) if args.format == "html" else render_markdown(profile)
    if args.output:
        output_path = Path(args.output)
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")
        except OSError as exc:
            print(f"error: cannot write output: {exc}", file=sys.stderr)
            return 1
        print(f"OK: wrote {output_path}")
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    sys.exit(main())
