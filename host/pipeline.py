"""Deterministic, non-actuating V0 reference pipeline. Limits are test fixtures."""
import math

CONDITIONS = ("fixed", "context_sensitive")
HEATING = {"WARM_SLOW", "WARM_MODERATE", "MAINTAIN"}
RESPONSES = HEATING | {"NO_RESPONSE", "RETURN_TO_BASELINE"}


def sensors_valid(frame):
    fields = ("raw_sensor_value", "filtered_sensor_value", "force_rate",
              "temperature_c", "contact_duration_s")
    return (frame.get("valid") is True
            and all(isinstance(frame.get(k), (int, float))
                    and not isinstance(frame[k], bool) and math.isfinite(frame[k]) for k in fields)
            and 0 <= frame["raw_sensor_value"] <= 1
            and 0 <= frame["filtered_sensor_value"] <= 1
            and -10 <= frame["temperature_c"] <= 80
            and frame["contact_duration_s"] >= 0)


class Classifier:
    def __init__(self):
        self.was_touching = False
        self.last_duration = 0.0

    def classify(self, frame):
        if not sensors_valid(frame):
            self.was_touching = False
            self.last_duration = 0.0
            return "INVALID_INPUT"
        force = frame["filtered_sensor_value"]
        touching = force > 0.05
        if not touching:
            event = ("TAP" if self.last_duration < 0.3 else "RELEASE") if self.was_touching else "NONE"
        elif force > 0.8 or frame["force_rate"] > 0.45:
            event = "EXCESSIVE_INPUT"
        elif not self.was_touching:
            event = "CONTACT_START"
        elif frame["contact_duration_s"] >= 1.0:
            event = "SUSTAINED_HOLD"
        else:
            event = "PRESS"
        self.was_touching = touching
        self.last_duration = frame["contact_duration_s"] if touching else 0.0
        return event


def request_response(event, condition):
    if condition not in CONDITIONS:
        raise ValueError("unknown condition")
    if event == "RELEASE":
        return "RETURN_TO_BASELINE"
    if condition == "fixed":
        return "WARM_SLOW" if event in {"PRESS", "SUSTAINED_HOLD", "STROKE"} else "NO_RESPONSE"
    return {"PRESS": "WARM_SLOW", "SUSTAINED_HOLD": "MAINTAIN",
            "STROKE": "WARM_MODERATE"}.get(event, "NO_RESPONSE")


class SafetyController:
    """Condition-independent guard. Faults latch until explicit reinitialization.

    Heating budget tracks approved heating intent, not physical heater activity.
    """
    def __init__(self, max_temperature_c=35.0, max_heating_s=5.0):
        self.max_temperature_c = max_temperature_c
        self.max_heating_s = max_heating_s
        self.heating_start = None
        self.last_time = None
        self.fault = None

    def evaluate(self, requested, frame, now_s):
        reason = self.fault
        if reason is None:
            if not math.isfinite(now_s) or (self.last_time is not None and now_s < self.last_time):
                reason = "invalid_clock"
            elif frame.get("manual_stop") is not False:
                reason = "manual_stop_or_unknown"
            elif frame.get("communication_ok") is not True:
                reason = "communication_lost_or_unknown"
            elif not sensors_valid(frame):
                reason = "invalid_sensor_data"
            elif frame["temperature_c"] >= self.max_temperature_c:
                reason = "simulated_temperature_limit"
            elif frame["filtered_sensor_value"] > 0.8 or frame["force_rate"] > 0.45:
                reason = "excessive_input"
            elif requested not in RESPONSES:
                reason = "invalid_request"
            elif requested in HEATING:
                if self.heating_start is None:
                    self.heating_start = now_s
                if now_s - self.heating_start >= self.max_heating_s:
                    reason = "simulated_heating_timeout"
            else:
                self.heating_start = None
        self.last_time = now_s
        self.fault = reason
        return {"approved_response": "NO_RESPONSE" if reason else requested,
                "safety_clamp": reason is not None, "safety_reason": reason}


class Pipeline:
    def __init__(self, condition):
        if condition not in CONDITIONS:
            raise ValueError("unknown condition")
        self.condition = condition
        self.classifier = Classifier()
        self.safety = SafetyController()

    def step(self, frame, now_s):
        event = self.classifier.classify(frame)
        requested = request_response(event, self.condition)
        decision = self.safety.evaluate(requested, frame, now_s)
        return {**frame, "valid": sensors_valid(frame), "record_type": "frame", "device_timestamp_s": now_s,
                "mode": "simulated-prehardware", "condition": self.condition,
                "classified_event": event, "event_confidence": None,
                "interaction_intensity": frame["filtered_sensor_value"] if sensors_valid(frame) else None,
                "requested_response": requested, **decision,
                "executed_response": None, "physically_executed": False,
                "heater_output": 0.0, "safe_state_entered": decision["safety_clamp"]}


def simulated_device_payloads(count=80, condition="context_sensitive", scenario="normal"):
    pipeline = Pipeline(condition)
    previous_force = 0.0
    contact_start = None
    for i in range(count):
        t = round(i * 0.1, 4)
        phase = i % 80
        force = 0.25 if (10 <= phase < 12 or 20 <= phase < 60) else 0.0
        if scenario == "timeout" and i >= 20:
            force = 0.25
        if force > 0.05 and contact_start is None:
            contact_start = t
        if force <= 0.05:
            contact_start = None
        frame = {"capacitance": 0.7 if force else 0.1,
                 "force": force, "raw_sensor_value": force, "filtered_sensor_value": force,
                 "force_rate": round(force - previous_force, 4),
                 "temperature_c": 36.0 if scenario == "overtemperature" and i >= 35 else 22.0,
                 "contact_duration_s": round(t - contact_start, 4) if contact_start is not None else 0.0,
                 "valid": not (scenario == "sensor_fault" and i >= 35),
                 "communication_ok": True, "manual_stop": False}
        yield pipeline.step(frame, t)
        previous_force = force
