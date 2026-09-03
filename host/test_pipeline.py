import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

from pipeline import Classifier, Pipeline, SafetyController, request_response, simulated_device_payloads
from logger import make_canonical_frame, serial_payloads


def sensor(**changes):
    return {"raw_sensor_value": 0.25, "filtered_sensor_value": 0.25,
            "force_rate": 0.0, "temperature_c": 22.0, "contact_duration_s": 1.0,
            "valid": True, "communication_ok": True, "manual_stop": False, **changes}


def canonical(payload, **kwargs):
    return make_canonical_frame(episode_index=0, frame_index=0, timestamp_s=0,
        device_payload=payload, session_id="s", trial_id="t", device_id="d",
        condition="context_sensitive", **kwargs)


class PipelineTests(unittest.TestCase):
    def test_sensor_trace_reaches_tap_hold_and_release(self):
        rows = list(simulated_device_payloads())
        events = {r["classified_event"] for r in rows}
        self.assertTrue({"NONE", "CONTACT_START", "TAP", "PRESS", "SUSTAINED_HOLD", "RELEASE"} <= events)
        self.assertNotIn("STROKE", events)
        self.assertEqual(rows[-1]["device_timestamp_s"], 7.9)
        self.assertEqual(rows, list(simulated_device_payloads()))

    def test_fixed_condition_has_one_qualifying_contact_response(self):
        self.assertEqual({request_response(e, "fixed") for e in ("PRESS", "SUSTAINED_HOLD", "STROKE")}, {"WARM_SLOW"})
        self.assertEqual(request_response("SUSTAINED_HOLD", "context_sensitive"), "MAINTAIN")
        with self.assertRaises(ValueError):
            Pipeline("typo")

    def test_faults_override_all_heating_requests_and_latch(self):
        cases = [({"temperature_c": 35.0}, "simulated_temperature_limit"),
                 ({"valid": False}, "invalid_sensor_data"),
                 ({"temperature_c": math.nan}, "invalid_sensor_data"),
                 ({"filtered_sensor_value": math.inf}, "invalid_sensor_data"),
                 ({"raw_sensor_value": -1}, "invalid_sensor_data"),
                 ({"manual_stop": True}, "manual_stop_or_unknown"),
                 ({"communication_ok": False}, "communication_lost_or_unknown"),
                 ({"filtered_sensor_value": 0.9}, "excessive_input")]
        for response in ("WARM_SLOW", "WARM_MODERATE", "MAINTAIN"):
            for values, reason in cases:
                with self.subTest(response=response, values=values):
                    guard = SafetyController()
                    decision = guard.evaluate(response, sensor(**values), 0)
                    self.assertEqual(decision["approved_response"], "NO_RESPONSE")
                    self.assertEqual(decision["safety_reason"], reason)
                    self.assertEqual(guard.evaluate(response, sensor(), 1)["safety_reason"], reason)

    def test_timeout_spans_response_changes_and_resets_on_nonheating(self):
        guard = SafetyController()
        self.assertFalse(guard.evaluate("WARM_SLOW", sensor(), 0)["safety_clamp"])
        self.assertFalse(guard.evaluate("MAINTAIN", sensor(), 4.9)["safety_clamp"])
        self.assertEqual(guard.evaluate("WARM_MODERATE", sensor(), 5)["safety_reason"], "simulated_heating_timeout")
        guard = SafetyController()
        guard.evaluate("WARM_SLOW", sensor(), 0)
        guard.evaluate("RETURN_TO_BASELINE", sensor(), 4)
        self.assertFalse(guard.evaluate("MAINTAIN", sensor(), 6)["safety_clamp"])

    def test_safety_independent_of_condition(self):
        for condition in ("fixed", "context_sensitive"):
            rows = list(simulated_device_payloads(80, condition, "overtemperature"))
            self.assertTrue(rows[35]["safety_clamp"])
            self.assertEqual(rows[35]["approved_response"], "NO_RESPONSE")
            self.assertIn(rows[35]["requested_response"], ("MAINTAIN", "WARM_SLOW"))

    def test_simulator_fault_scenarios(self):
        for scenario, reason in (("sensor_fault", "invalid_sensor_data"),
                                 ("timeout", "simulated_heating_timeout")):
            rows = list(simulated_device_payloads(100, scenario=scenario))
            self.assertIn(reason, {r["safety_reason"] for r in rows})

    def test_execution_is_reported_not_inferred(self):
        payload = list(simulated_device_payloads())[35]
        record = canonical(payload)
        self.assertEqual(record["policy"]["requested_response"], "MAINTAIN")
        self.assertEqual(record["safety"]["approved_response"], "MAINTAIN")
        self.assertIsNone(record["execution"]["executed_response"])
        self.assertEqual(record["execution"]["heater_output"], 0)
        self.assertIsNone(record["participant_id"])
        # A future adapter reports actual execution explicitly, even when it differs.
        payload.update(mode="hardware", physically_executed=True, executed_response="NO_RESPONSE")
        self.assertEqual(canonical(payload)["execution"]["executed_response"], "NO_RESPONSE")
        payload["executed_response"] = None
        with self.assertRaises(ValueError):
            canonical(payload)

    def test_invalid_payloads_fail_instead_of_becoming_trials(self):
        good = list(simulated_device_payloads())[35]
        for patch_values in ({"condition": "fixed"}, {"physically_executed": "false"},
                             {"executed_response": "MAINTAIN"}, {"record_type": "boot"},
                             {"heater_output": 0.5}, {"heater_output": math.inf},
                             {"safety_clamp": True, "safety_reason": None},
                             {"physically_executed": True, "executed_response": "MAINTAIN"}):
            with self.subTest(patch_values=patch_values), self.assertRaises(ValueError):
                canonical({**good, **patch_values})
        self.assertIsNone(canonical({**good, "temperature_c": math.nan, "valid": False})["observation"]["state"]["temperature_c"])
        del good["raw_sensor_value"]
        with self.assertRaises(ValueError):
            canonical(good)

    def test_serial_skips_boot_and_malformed_lines(self):
        payload = next(simulated_device_payloads())
        class FakeSerial:
            def __init__(self, *args, **kwargs): pass
            def __enter__(self): return iter([b'{"status":"boot"}\n', b'bad\n', json.dumps(payload).encode()])
            def __exit__(self, *args): pass
        with patch.dict(sys.modules, {"serial": types.SimpleNamespace(Serial=FakeSerial)}):
            self.assertEqual(list(serial_payloads("test", 115200)), [payload])

    def test_cli_records_metadata_and_preserves_existing_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "trial.jsonl"
            command = [sys.executable, str(Path(__file__).with_name("logger.py")), "--simulate",
                       "--condition", "fixed", "--frames", "40", "--trial-id", "trial-A",
                       "--session-id", "session-test", "--phase", "formal", "--output", str(output)]
            subprocess.run(command, check=True, capture_output=True)
            original = output.read_bytes()
            rows = [json.loads(line) for line in original.splitlines()]
            self.assertEqual(len(rows), 40)
            self.assertEqual(rows[-1]["frame_index"], 39)
            self.assertTrue(all(r["trial_id"] == "trial-A" and r["experiment"]["condition"] == "fixed" for r in rows))
            self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)
            self.assertEqual(output.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
