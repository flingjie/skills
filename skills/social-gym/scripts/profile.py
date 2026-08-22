#!/usr/bin/env python3
"""Validate, initialize, and summarize a social-gym profile."""

import argparse
import sys

from shared import (
    COMPETENCY_KEYS,
    STAGES,
    load_profile,
    new_profile,
    retain_caps,
    validate_profile,
    write_profile_atomic,
)


def cmd_validate(args):
    profile, errors = load_profile(args.profile)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"OK: {args.profile} is valid")
    return 0


def cmd_init(args):
    existing, errors = load_profile(args.profile)
    if existing is not None and not errors:
        if not args.force:
            print(
                f"error: profile already exists and is valid: {args.profile}; "
                "use --force to replace after a backup",
                file=sys.stderr,
            )
            return 1
        backup = True
    else:
        backup = False

    profile = new_profile(language=args.language)
    try:
        write_profile_atomic(args.profile, profile, backup=backup)
    except OSError as exc:
        print(f"error: cannot write profile: {exc}", file=sys.stderr)
        return 1
    print(f"OK: initialized {args.profile}")
    return 0


def cmd_summary(args):
    profile, errors = load_profile(args.profile)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"profile: {args.profile}")
    print(f"schema_version: {profile.get('schema_version')}")
    print(f"created_at: {profile.get('created_at')}")
    print(f"updated_at: {profile.get('updated_at')}")
    print(f"language: {profile.get('preferences', {}).get('language')}")
    print(f"diagnostic: {profile.get('diagnostic', {}).get('status')}")
    print(f"current_focus: {profile.get('current_focus')}")
    print(f"recent_sessions: {len(profile.get('recent_sessions', []))}")
    if profile.get("active_session"):
        active = profile["active_session"]
        print(
            "active_session: "
            f"{active.get('mode')} / {active.get('status')} / turn {active.get('turn')}"
        )
    for key in COMPETENCY_KEYS:
        entry = profile.get("competencies", {}).get(key, {})
        count = len(entry.get("evidence", []))
        reconfirmation = entry.get("needs_reconfirmation", False)
        print(
            f"{key}: {entry.get('stage')} evidence={count} "
            f"needs_reconfirmation={reconfirmation}"
        )
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser(
        "validate", help="validate a profile without modifying it"
    )
    validate_parser.add_argument("--profile", required=True)
    validate_parser.set_defaults(func=cmd_validate)

    init_parser = subparsers.add_parser("init", help="create a new empty profile")
    init_parser.add_argument("--profile", required=True)
    init_parser.add_argument("--language", default="zh-CN")
    init_parser.add_argument(
        "--force",
        action="store_true",
        help="replace an existing valid profile (keeps a .bak backup)",
    )
    init_parser.set_defaults(func=cmd_init)

    summary_parser = subparsers.add_parser("summary", help="print a profile summary")
    summary_parser.add_argument("--profile", required=True)
    summary_parser.set_defaults(func=cmd_summary)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
