#!/usr/bin/env python3
"""Compute deterministic competency stages and reconfirmation flags."""

import argparse
import json
import sys
from datetime import datetime, timezone

from shared import (
    COMPETENCY_KEYS,
    compute_profile_progress,
    load_profile,
    retain_caps,
    write_profile_atomic,
)


def utc_now():
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def cmd_compute(args):
    profile, errors = load_profile(args.profile)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    progress = compute_profile_progress(profile)
    for key in COMPETENCY_KEYS:
        stage, needs_reconfirmation = progress[key]
        stored = profile["competencies"][key]
        print(
            f"{key}: {stored.get('stage')} -> {stage} "
            f"needs_reconfirmation={needs_reconfirmation}"
        )

    if args.write:
        changed = retain_caps(profile)
        for key in COMPETENCY_KEYS:
            stage, needs_reconfirmation = progress[key]
            profile["competencies"][key]["stage"] = stage
            profile["competencies"][key]["needs_reconfirmation"] = needs_reconfirmation
        profile["updated_at"] = utc_now()
        if changed:
            print("note: retention caps applied")
        try:
            write_profile_atomic(args.profile, profile, backup=True)
        except OSError as exc:
            print(f"error: cannot write profile: {exc}", file=sys.stderr)
            return 1
        print(f"OK: wrote {args.profile}")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", required=True)
    parser.add_argument(
        "--write",
        action="store_true",
        help="write computed stages back to the profile atomically",
    )
    parser.set_defaults(func=cmd_compute)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
