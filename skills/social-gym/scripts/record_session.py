#!/usr/bin/env python3
"""Record session lifecycle events with validated, atomic profile updates."""

import argparse
import json
import sys
from datetime import datetime, timezone

from shared import (
    COMPETENCY_KEYS,
    compute_profile_progress,
    load_profile,
    retain_caps,
    validate_profile,
    write_profile_atomic,
)


def utc_now():
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def parse_json_value(raw, label):
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"error: {label} is not valid JSON: {exc}", file=sys.stderr)
        return None


def apply_progress(profile):
    progress = compute_profile_progress(profile)
    for key in COMPETENCY_KEYS:
        stage, needs_reconfirmation = progress[key]
        profile["competencies"][key]["stage"] = stage
        profile["competencies"][key]["needs_reconfirmation"] = needs_reconfirmation
    return progress


def finish_write(args, profile):
    if args.no_save:
        print("note: no-save session; profile writes skipped, session is in-memory only")
        return True
    retain_caps(profile)
    profile["updated_at"] = utc_now()
    try:
        write_profile_atomic(args.profile, profile, backup=True)
    except OSError as exc:
        print(f"error: cannot write profile: {exc}", file=sys.stderr)
        print("conversation stays usable, but progress was NOT saved", file=sys.stderr)
        return False
    print(f"OK: wrote {args.profile}")
    return True


def cmd_start(args):
    profile, errors = load_profile(args.profile)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    session = parse_json_value(args.session, "session")
    if session is None:
        return 1
    if not isinstance(session, dict):
        print("error: session must be an object", file=sys.stderr)
        return 1
    active = {
        "session_id": session.get("session_id"),
        "mode": session.get("mode"),
        "status": "active",
        "turn": session.get("turn", 0),
        "focus": session.get("focus"),
        "scenario_tags": session.get("scenario_tags", []),
        "difficulty": session.get("difficulty", "normal"),
        "resume_summary": session.get("resume_summary", ""),
    }
    profile["active_session"] = active
    errors = validate_profile(profile)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    if not finish_write(args, profile):
        return 1
    print(f"session started: {session.get('session_id', '')}")
    return 0


def cmd_pause(args):
    profile, errors = load_profile(args.profile)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    active = profile.get("active_session")
    if not isinstance(active, dict):
        print("error: no active session to pause", file=sys.stderr)
        return 1
    active["status"] = "paused"
    active["resume_summary"] = args.resume_summary
    errors = validate_profile(profile)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    if not finish_write(args, profile):
        return 1
    print("session paused")
    return 0


def cmd_complete(args):
    profile, errors = load_profile(args.profile)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    session = parse_json_value(args.session, "session")
    evidence = parse_json_value(args.evidence, "evidence")
    if session is None or evidence is None:
        return 1
    if not isinstance(session, dict):
        print("error: session must be an object", file=sys.stderr)
        return 1
    if not isinstance(evidence, list):
        print("error: evidence must be a list", file=sys.stderr)
        return 1

    competencies = profile["competencies"]
    for item in evidence:
        if not isinstance(item, dict):
            print("error: evidence item must be an object", file=sys.stderr)
            return 1
        competency = item.get("competency")
        if competency not in competencies:
            print(
                f"error: evidence references unknown competency {competency!r}",
                file=sys.stderr,
            )
            return 1
        competencies[competency]["evidence"].append(item)

    recent = {
        "session_id": session.get("session_id"),
        "mode": session.get("mode"),
        "difficulty": session.get("difficulty", "normal"),
        "scenario_tags": session.get("scenario_tags", []),
        "focus": session.get("focus", ""),
        "result": "complete",
    }
    profile["recent_sessions"].append(recent)
    profile["active_session"] = None
    if session.get("focus") in COMPETENCY_KEYS:
        profile["current_focus"] = session["focus"]

    errors = validate_profile(profile)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    apply_progress(profile)
    if not finish_write(args, profile):
        return 1
    print(f"session complete: {session.get('session_id', '')}")
    return 0


def cmd_interrupt(args):
    profile, errors = load_profile(args.profile)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    evidence = parse_json_value(args.evidence, "evidence")
    if evidence is None:
        return 1
    if not isinstance(evidence, list):
        print("error: evidence must be a list", file=sys.stderr)
        return 1

    competencies = profile["competencies"]
    for item in evidence:
        if not isinstance(item, dict):
            print("error: evidence item must be an object", file=sys.stderr)
            return 1
        competency = item.get("competency")
        if competency not in competencies:
            print(
                f"error: evidence references unknown competency {competency!r}",
                file=sys.stderr,
            )
            return 1
        competencies[competency]["evidence"].append(item)

    active = profile.get("active_session")
    if isinstance(active, dict):
        recent = {
            "session_id": active.get("session_id", "interrupted"),
            "mode": active.get("mode"),
            "difficulty": active.get("difficulty", "normal"),
            "scenario_tags": active.get("scenario_tags", []),
            "focus": active.get("focus", ""),
            "result": "interrupted",
        }
        profile["recent_sessions"].append(recent)
    profile["active_session"] = None

    errors = validate_profile(profile)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    apply_progress(profile)
    if not finish_write(args, profile):
        return 1
    print("session interrupted; only supported observations were saved")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", required=True)
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="validate and report without writing anything",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    start = subparsers.add_parser("start")
    start.add_argument("--session", required=True, help="session JSON object")
    start.set_defaults(func=cmd_start)

    pause = subparsers.add_parser("pause")
    pause.add_argument("--resume-summary", required=True)
    pause.set_defaults(func=cmd_pause)

    complete = subparsers.add_parser("complete")
    complete.add_argument("--session", required=True, help="session JSON object")
    complete.add_argument("--evidence", required=True, help="evidence JSON list")
    complete.set_defaults(func=cmd_complete)

    interrupt = subparsers.add_parser("interrupt")
    interrupt.add_argument("--evidence", required=True, help="evidence JSON list")
    interrupt.set_defaults(func=cmd_interrupt)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
