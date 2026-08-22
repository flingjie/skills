#!/usr/bin/env python3
"""Shared profile validation and progression logic for social-gym scripts."""

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path


SCHEMA_VERSION = 1
MAX_EVIDENCE_PER_COMPETENCY = 20
MAX_RECENT_SESSIONS = 30

COMPETENCY_KEYS = [
    "opening",
    "listening_reaction",
    "threading",
    "story_development",
    "reciprocity",
    "self_introduction",
    "recovery_exit",
]

STAGES = ["unassessed", "emerging", "developing", "reliable"]

DIFFICULTIES = {"easy", "normal", "hard", "expert"}

POSITIVE_BEHAVIOR_CODES = {
    "opening": {
        "situational_open",
        "low_pressure_open",
        "context_matched_open",
    },
    "listening_reaction": {
        "acknowledge_before_ask",
        "react_before_ask",
        "reflect_meaning",
    },
    "threading": {
        "thread_followed",
        "wording_connected",
        "thread_switched_well",
    },
    "story_development": {
        "depth_advanced",
        "context_sensitive_prompt",
        "story_potential_seen",
    },
    "reciprocity": {
        "balanced_share",
        "ack_explore_share_return",
        "room_left",
    },
    "self_introduction": {
        "clear_explanation",
        "hook_with_problem",
        "open_loop",
    },
    "recovery_exit": {
        "signal_read",
        "appropriate_response",
        "graceful_exit",
        "minor_repair",
    },
}

COUNTER_BEHAVIOR_CODES = {
    "opening": {"rehearsed_pitch"},
    "listening_reaction": {"question_jumping", "no_reaction"},
    "threading": {"questionnaire_mode", "thread_dropped"},
    "story_development": {"mechanical_why", "depth_forced"},
    "reciprocity": {"interview_mode", "conversation_hijack"},
    "self_introduction": {"resume_dump"},
    "recovery_exit": {"forced_continuation"},
}

ALL_BEHAVIOR_CODES = {
    key: POSITIVE_BEHAVIOR_CODES[key] | COUNTER_BEHAVIOR_CODES[key]
    for key in COMPETENCY_KEYS
}

ATTEMPTS = {"first", "retry"}
ASSISTANCE_LEVELS = {
    "none",
    "attention_hint",
    "strategy_hint",
    "direction_examples",
    "full_example",
}


def utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def empty_competencies():
    return {
        key: {"stage": "unassessed", "needs_reconfirmation": False, "evidence": []}
        for key in COMPETENCY_KEYS
    }


def new_profile(language="zh-CN"):
    now = utc_now()
    return {
        "schema_version": SCHEMA_VERSION,
        "created_at": now,
        "updated_at": now,
        "preferences": {"goals": [], "scenario_tags": [], "language": language},
        "diagnostic": {"status": "incomplete", "completed_at": None},
        "current_focus": None,
        "competencies": empty_competencies(),
        "recent_sessions": [],
        "active_session": None,
    }


def load_profile(path):
    """Load and validate a profile. Returns (profile, errors)."""
    profile_path = Path(path)
    if not profile_path.exists():
        return None, [f"profile not found: {path}"]
    try:
        data = json.loads(profile_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return None, [f"invalid JSON: {exc}"]
    except OSError as exc:
        return None, [f"cannot read profile: {exc}"]
    errors = validate_profile(data)
    if errors:
        return data, errors
    return data, []


def validate_profile(profile):
    errors = []
    if not isinstance(profile, dict):
        return ["profile must be a JSON object"]

    if profile.get("schema_version") != SCHEMA_VERSION:
        errors.append(
            f"unsupported schema_version {profile.get('schema_version')!r}; expected {SCHEMA_VERSION}"
        )

    for key in (
        "created_at",
        "updated_at",
        "preferences",
        "diagnostic",
        "current_focus",
        "competencies",
        "recent_sessions",
    ):
        if key not in profile:
            errors.append(f"missing top-level key: {key}")

    if "created_at" in profile and not isinstance(profile["created_at"], str):
        errors.append("created_at must be a string")
    if "updated_at" in profile and not isinstance(profile["updated_at"], str):
        errors.append("updated_at must be a string")

    preferences = profile.get("preferences", {})
    if not isinstance(preferences, dict):
        errors.append("preferences must be an object")
    else:
        if not isinstance(preferences.get("goals", []), list):
            errors.append("preferences.goals must be a list")
        if not isinstance(preferences.get("scenario_tags", []), list):
            errors.append("preferences.scenario_tags must be a list")
        language = preferences.get("language")
        if not isinstance(language, str) or not language:
            errors.append("preferences.language must be a non-empty string")

    diagnostic = profile.get("diagnostic", {})
    if not isinstance(diagnostic, dict):
        errors.append("diagnostic must be an object")
    else:
        status = diagnostic.get("status")
        if status not in ("incomplete", "complete"):
            errors.append(f"invalid diagnostic.status: {status!r}")
        completed_at = diagnostic.get("completed_at")
        if completed_at is not None and not isinstance(completed_at, str):
            errors.append("diagnostic.completed_at must be a string or null")

    focus = profile.get("current_focus")
    if focus is not None and focus not in COMPETENCY_KEYS:
        errors.append(f"invalid current_focus: {focus!r}")

    competencies = profile.get("competencies", {})
    if not isinstance(competencies, dict):
        errors.append("competencies must be an object")
    else:
        for key in COMPETENCY_KEYS:
            if key not in competencies:
                errors.append(f"missing competency: {key}")
                continue
            entry = competencies[key]
            if not isinstance(entry, dict):
                errors.append(f"competency {key} must be an object")
                continue
            stage = entry.get("stage")
            if stage not in STAGES:
                errors.append(f"{key}.stage invalid: {stage!r}")
            if not isinstance(entry.get("needs_reconfirmation"), bool):
                errors.append(f"{key}.needs_reconfirmation must be a boolean")
            evidence = entry.get("evidence", [])
            if not isinstance(evidence, list):
                errors.append(f"{key}.evidence must be a list")
            else:
                for index, item in enumerate(evidence):
                    errors.extend(_validate_evidence(key, index, item))

    sessions = profile.get("recent_sessions", [])
    if not isinstance(sessions, list):
        errors.append("recent_sessions must be a list")
    else:
        for index, session in enumerate(sessions):
            errors.extend(_validate_session(index, session))

    active = profile.get("active_session")
    if active is not None:
        errors.extend(_validate_active_session(active))

    return errors


def _validate_evidence(competency, index, item):
    errors = []
    if not isinstance(item, dict):
        return [f"{competency}.evidence[{index}] must be an object"]
    if item.get("competency") != competency:
        errors.append(
            f"{competency}.evidence[{index}].competency must equal the owning competency"
        )
    if not isinstance(item.get("session_id"), str):
        errors.append(f"{competency}.evidence[{index}].session_id must be a string")
    if not isinstance(item.get("observed_at"), str):
        errors.append(f"{competency}.evidence[{index}].observed_at must be a string")
    polarity = item.get("polarity")
    if polarity not in ("positive", "counter"):
        errors.append(f"{competency}.evidence[{index}].polarity invalid: {polarity!r}")
    code = item.get("behavior_code")
    if code not in ALL_BEHAVIOR_CODES.get(competency, set()):
        errors.append(
            f"{competency}.evidence[{index}].behavior_code invalid for competency: {code!r}"
        )
    if not isinstance(item.get("behavior"), str) or not item.get("behavior").strip():
        errors.append(f"{competency}.evidence[{index}].behavior must be a non-empty string")
    if not isinstance(item.get("mode"), str):
        errors.append(f"{competency}.evidence[{index}].mode must be a string")
    if item.get("difficulty") not in DIFFICULTIES:
        errors.append(
            f"{competency}.evidence[{index}].difficulty invalid: {item.get('difficulty')!r}"
        )
    tags = item.get("scenario_tags")
    if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
        errors.append(f"{competency}.evidence[{index}].scenario_tags must be a list of strings")
    if item.get("attempt") not in ATTEMPTS:
        errors.append(f"{competency}.evidence[{index}].attempt invalid: {item.get('attempt')!r}")
    if item.get("assistance") not in ASSISTANCE_LEVELS:
        errors.append(
            f"{competency}.evidence[{index}].assistance invalid: {item.get('assistance')!r}"
        )
    return errors


def _validate_session(index, session):
    errors = []
    if not isinstance(session, dict):
        return [f"recent_sessions[{index}] must be an object"]
    if not isinstance(session.get("session_id"), str):
        errors.append(f"recent_sessions[{index}].session_id must be a string")
    if not isinstance(session.get("mode"), str):
        errors.append(f"recent_sessions[{index}].mode must be a string")
    if session.get("difficulty") not in DIFFICULTIES:
        errors.append(
            f"recent_sessions[{index}].difficulty invalid: {session.get('difficulty')!r}"
        )
    tags = session.get("scenario_tags")
    if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
        errors.append(
            f"recent_sessions[{index}].scenario_tags must be a list of strings"
        )
    if not isinstance(session.get("focus"), str):
        errors.append(f"recent_sessions[{index}].focus must be a string")
    if session.get("result") not in ("complete", "interrupted"):
        errors.append(
            f"recent_sessions[{index}].result invalid: {session.get('result')!r}"
        )
    return errors


def _validate_active_session(active):
    errors = []
    if not isinstance(active, dict):
        return ["active_session must be an object or null"]
    if not isinstance(active.get("session_id"), str):
        errors.append("active_session.session_id must be a string")
    if not isinstance(active.get("mode"), str):
        errors.append("active_session.mode must be a string")
    if active.get("status") not in ("active", "paused"):
        errors.append(f"active_session.status invalid: {active.get('status')!r}")
    if not isinstance(active.get("turn"), int) or active.get("turn") < 0:
        errors.append("active_session.turn must be a non-negative integer")
    focus = active.get("focus")
    if focus is not None and focus not in COMPETENCY_KEYS:
        errors.append(f"active_session.focus invalid: {focus!r}")
    tags = active.get("scenario_tags")
    if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
        errors.append("active_session.scenario_tags must be a list of strings")
    if active.get("difficulty") not in DIFFICULTIES:
        errors.append(
            f"active_session.difficulty invalid: {active.get('difficulty')!r}"
        )
    if not isinstance(active.get("resume_summary"), str) or not active.get(
        "resume_summary"
    ).strip():
        errors.append("active_session.resume_summary must be a non-empty string")
    return errors


def scenario_category(evidence_item):
    tags = evidence_item.get("scenario_tags", [])
    setting = ""
    relationship = ""
    constraint = ""
    for tag in tags:
        if tag.startswith("setting:"):
            setting = tag
        elif tag.startswith("relationship:"):
            relationship = tag
        elif tag.startswith("constraint:"):
            constraint = tag
    return f"{setting}|{relationship}|{constraint}"


def is_independent_positive(item):
    return (
        item.get("polarity") == "positive"
        and item.get("attempt") == "first"
        and item.get("assistance") == "none"
    )


def compute_competency(evidence):
    """Return (stage, needs_reconfirmation) for one competency's retained evidence."""
    if not evidence:
        return "unassessed", False

    positives = [item for item in evidence if item.get("polarity") == "positive"]
    independent = [item for item in evidence if is_independent_positive(item)]
    categories = {scenario_category(item) for item in independent}
    modes = {item.get("mode") for item in independent}
    latest_three = evidence[-3:]
    latest_positives = sum(
        1 for item in latest_three if item.get("polarity") == "positive"
    )
    counter_codes = [
        item.get("behavior_code")
        for item in latest_three
        if item.get("polarity") == "counter"
    ]
    repeated_counter = any(
        counter_codes.count(code) >= 2 for code in set(counter_codes)
    )

    if (
        len(independent) >= 5
        and len(categories) >= 3
        and len(modes) >= 2
        and latest_positives >= 2
        and not repeated_counter
    ):
        stage = "reliable"
    elif (
        len(positives) >= 3
        and len(independent) >= 2
        and len(categories) >= 2
    ):
        stage = "developing"
    elif len(positives) >= 1:
        stage = "emerging"
    else:
        stage = "unassessed"

    if repeated_counter:
        needs_reconfirmation = True
    elif len(independent) >= 2 and len(categories) >= 2:
        needs_reconfirmation = False
    else:
        needs_reconfirmation = bool(repeated_counter)

    return stage, needs_reconfirmation


def compute_profile_progress(profile):
    """Return a dict of competency key -> (stage, needs_reconfirmation)."""
    result = {}
    competencies = profile.get("competencies", {})
    for key in COMPETENCY_KEYS:
        entry = competencies.get(key, {})
        result[key] = compute_competency(entry.get("evidence", []))
    return result


def retain_caps(profile):
    """Apply retention caps in place and return True when anything changed."""
    changed = False
    competencies = profile.get("competencies", {})
    for key in COMPETENCY_KEYS:
        evidence = competencies.get(key, {}).get("evidence", [])
        if len(evidence) > MAX_EVIDENCE_PER_COMPETENCY:
            competencies[key]["evidence"] = evidence[-MAX_EVIDENCE_PER_COMPETENCY:]
            changed = True
    sessions = profile.get("recent_sessions", [])
    if len(sessions) > MAX_RECENT_SESSIONS:
        profile["recent_sessions"] = sessions[-MAX_RECENT_SESSIONS:]
        changed = True
    return changed


def write_profile_atomic(path, profile, backup=False):
    """Write profile atomically, optionally keeping a .bak of the old file."""
    profile_path = Path(path)
    profile_path.parent.mkdir(parents=True, exist_ok=True)
    if backup and profile_path.exists():
        backup_path = profile_path.with_suffix(profile_path.suffix + ".bak")
        backup_path.write_text(
            profile_path.read_text(encoding="utf-8"), encoding="utf-8"
        )
    data = json.dumps(profile, ensure_ascii=False, indent=2) + "\n"
    fd, temp_name = tempfile.mkstemp(
        prefix=f".{profile_path.name}.",
        suffix=".tmp",
        dir=str(profile_path.parent),
        text=True,
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, profile_path)
    except BaseException:
        try:
            os.unlink(temp_name)
        except OSError:
            pass
        raise
    return str(profile_path)
