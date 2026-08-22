import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from shared import (
    MAX_EVIDENCE_PER_COMPETENCY,
    compute_competency,
    compute_profile_progress,
    empty_competencies,
    load_profile,
    new_profile,
    retain_caps,
    scenario_category,
    validate_profile,
)


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[3]
FIXTURES = Path(__file__).resolve().parents[2] / "evals" / "fixtures"


def evidence(
    polarity="positive",
    behavior_code="thread_followed",
    attempt="first",
    assistance="none",
    mode="followup_drill",
    tags=None,
    observed_at="2026-08-22T08:00:00Z",
    session_id="s1",
    competency="threading",
):
    return {
        "session_id": session_id,
        "observed_at": observed_at,
        "competency": competency,
        "polarity": polarity,
        "behavior_code": behavior_code,
        "behavior": f"{behavior_code} observed",
        "mode": mode,
        "difficulty": "normal",
        "scenario_tags": tags
        or ["setting:meetup", "relationship:stranger", "constraint:open"],
        "attempt": attempt,
        "assistance": assistance,
    }


class ComputeCompetencyTest(unittest.TestCase):
    def test_unassessed_to_emerging(self):
        items = [evidence()]
        stage, reconfirmation = compute_competency(items)
        self.assertEqual(stage, "emerging")
        self.assertFalse(reconfirmation)

    def test_emerging_to_developing(self):
        items = [
            evidence(),
            evidence(
                tags=["setting:learning", "relationship:peer", "constraint:open"],
                session_id="s2",
            ),
            evidence(
                behavior_code="wording_connected",
                tags=["setting:meetup", "relationship:stranger", "constraint:open"],
                session_id="s3",
            ),
        ]
        stage, _ = compute_competency(items)
        self.assertEqual(stage, "developing")

    def test_developing_to_reliable(self):
        items = [
            evidence(session_id="r1", mode="followup_drill"),
            evidence(session_id="r2", mode="followup_drill"),
            evidence(
                session_id="r3",
                mode="story_mining",
                tags=["setting:learning", "relationship:peer", "constraint:open"],
            ),
            evidence(
                session_id="r4",
                mode="story_mining",
                behavior_code="wording_connected",
                tags=["setting:learning", "relationship:peer", "constraint:open"],
            ),
            evidence(
                session_id="r5",
                mode="full_conversation",
                tags=["setting:work", "relationship:colleague", "constraint:distracted"],
            ),
            evidence(
                session_id="r6",
                mode="full_conversation",
                behavior_code="thread_followed",
                tags=["setting:work", "relationship:colleague", "constraint:distracted"],
            ),
        ]
        stage, _ = compute_competency(items)
        self.assertEqual(stage, "reliable")

    def test_single_counter_does_not_downgrade(self):
        items = [
            evidence(session_id="a"),
            evidence(
                session_id="b",
                tags=["setting:learning", "relationship:peer", "constraint:open"],
            ),
            evidence(
                session_id="c",
                behavior_code="wording_connected",
                tags=["setting:meetup", "relationship:stranger", "constraint:open"],
            ),
            evidence(polarity="counter", behavior_code="questionnaire_mode"),
        ]
        stage, reconfirmation = compute_competency(items)
        self.assertEqual(stage, "developing")
        self.assertFalse(reconfirmation)

    def test_repeated_counter_sets_reconfirmation(self):
        items = [
            evidence(session_id="a"),
            evidence(
                session_id="b",
                tags=["setting:learning", "relationship:peer", "constraint:open"],
            ),
            evidence(
                session_id="c",
                behavior_code="wording_connected",
                tags=["setting:meetup", "relationship:stranger", "constraint:open"],
            ),
            evidence(
                polarity="counter",
                behavior_code="questionnaire_mode",
                session_id="d",
            ),
            evidence(
                polarity="counter",
                behavior_code="questionnaire_mode",
                session_id="e",
            ),
        ]
        stage, reconfirmation = compute_competency(items)
        self.assertEqual(stage, "developing")
        self.assertTrue(reconfirmation)

    def test_two_independent_positives_clear_reconfirmation(self):
        items = [
            evidence(session_id="a"),
            evidence(
                session_id="b",
                tags=["setting:learning", "relationship:peer", "constraint:open"],
            ),
            evidence(
                polarity="counter",
                behavior_code="questionnaire_mode",
                session_id="d",
            ),
            evidence(
                polarity="counter",
                behavior_code="questionnaire_mode",
                session_id="e",
            ),
            evidence(
                session_id="f",
                tags=["setting:work", "relationship:colleague", "constraint:open"],
            ),
            evidence(
                session_id="g",
                mode="story_mining",
                tags=["setting:learning", "relationship:peer", "constraint:open"],
            ),
        ]
        stage, reconfirmation = compute_competency(items)
        self.assertEqual(stage, "developing")
        self.assertFalse(reconfirmation)

    def test_assisted_retry_is_not_independent_first_attempt(self):
        items = [
            evidence(session_id="a"),
            evidence(
                session_id="b",
                behavior_code="wording_connected",
                attempt="retry",
                assistance="strategy_hint",
            ),
        ]
        stage, _ = compute_competency(items)
        self.assertEqual(stage, "emerging")

    def test_full_example_does_not_count_as_independent(self):
        items = [
            evidence(session_id="a"),
            evidence(
                session_id="b",
                tags=["setting:learning", "relationship:peer", "constraint:open"],
            ),
            evidence(
                session_id="c",
                behavior_code="wording_connected",
                attempt="first",
                assistance="full_example",
            ),
        ]
        stage, _ = compute_competency(items)
        self.assertEqual(stage, "developing")

    def test_retention_cap_keeps_newest(self):
        items = [evidence(session_id=str(index)) for index in range(25)]
        self.assertEqual(len(items), 25)
        profile = new_profile()
        profile["competencies"]["threading"]["evidence"] = items
        retain_caps(profile)
        kept = profile["competencies"]["threading"]["evidence"]
        self.assertEqual(len(kept), MAX_EVIDENCE_PER_COMPETENCY)
        self.assertEqual(kept[-1]["session_id"], "24")
        self.assertEqual(kept[0]["session_id"], "5")


class ProfileValidationTest(unittest.TestCase):
    def test_new_profile_is_valid(self):
        self.assertEqual(validate_profile(new_profile()), [])

    def test_malformed_profile_has_errors(self):
        malformed = {"schema_version": 1, "competencies": {}}
        errors = validate_profile(malformed)
        self.assertTrue(errors)

    def test_malformed_input_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source = FIXTURES / "malformed-profile.json"
            target = Path(temp_dir) / "malformed-profile.json"
            target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
            original = target.read_text(encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS_DIR / "compute_progress.py"),
                    "--profile",
                    str(target),
                    "--write",
                ],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(target.read_text(encoding="utf-8"), original)


class ProfileFixtureTest(unittest.TestCase):
    def test_developing_fixture_is_valid_and_developing(self):
        profile, errors = load_profile(FIXTURES / "developing-threading.json")
        self.assertEqual(errors, [])
        progress = compute_profile_progress(profile)
        self.assertEqual(progress["threading"][0], "developing")

    def test_reliable_fixture_is_valid_and_reliable(self):
        profile, errors = load_profile(FIXTURES / "reliable-threading.json")
        self.assertEqual(errors, [])
        progress = compute_profile_progress(profile)
        self.assertEqual(progress["threading"][0], "reliable")


if __name__ == "__main__":
    unittest.main()
