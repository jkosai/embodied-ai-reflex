#!/usr/bin/env python3
"""V0 schema-v0.4 logger. Device approval is never evidence of execution."""
import argparse
import json
import math
import time
import uuid
from pathlib import Path

from pipeline import CONDITIONS, RESPONSES, simulated_device_payloads

SCHEMA_VERSION = "0.4"


def nullable_numbers(value):
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, dict):
        return {k: nullable_numbers(v) for k, v in value.items()}
    if isinstance(value, list):
        return [nullable_numbers(v) for v in value]
    return value


def make_canonical_frame(*, episode_index, frame_index, timestamp_s, device_payload,
                         session_id, trial_id, device_id, condition, participant_id=None,
                         phase="calibration", operator_note=None):
    p = device_payload
    if p.get("record_type") != "frame":
        raise ValueError("not a telemetry frame (boot/status messages are not trials)")
    if condition not in CONDITIONS or p.get("condition") != condition:
        raise ValueError("device condition does not match the trial condition")
    required = {"mode", "classified_event", "requested_response", "approved_response",
                "executed_response", "physically_executed", "safety_clamp",
                "safety_reason", "heater_output", "safe_state_entered", "valid",
                "raw_sensor_value", "filtered_sensor_value", "contact_duration_s",
                "event_confidence", "interaction_intensity", "temperature_c", "device_timestamp_s"}
    if not required <= p.keys():
        raise ValueError("incomplete v0.4 device telemetry; upgrade firmware")
    for key in ("physically_executed", "safety_clamp", "safe_state_entered", "valid"):
        if not isinstance(p[key], bool):
            raise ValueError(f"{key} must be a JSON boolean")
    if p["requested_response"] not in RESPONSES or p["approved_response"] not in RESPONSES:
        raise ValueError("unknown response vocabulary")
    executed = p["executed_response"]
    if p["physically_executed"]:
        if executed not in RESPONSES:
            raise ValueError("execution requires an explicit device-reported response")
        if p["mode"] == "simulated-prehardware":
            raise ValueError("simulation cannot claim physical execution")
    elif executed is not None:
        raise ValueError("unexecuted responses must be null")
    heater_output = p["heater_output"]
    if heater_output is not None and (isinstance(heater_output, bool)
            or not isinstance(heater_output, (int, float))
            or not math.isfinite(heater_output) or not 0 <= heater_output <= 1):
        raise ValueError("heater_output must be null or a finite duty in [0, 1]")
    if p["mode"] == "simulated-prehardware" and heater_output != 0:
        raise ValueError("non-actuating simulation must report zero heater output")
    if p["safety_clamp"] and not isinstance(p["safety_reason"], str):
        raise ValueError("safety intervention requires a reason")
    return nullable_numbers({
        "schema_version": SCHEMA_VERSION, "record_type": "frame",
        "episode_index": episode_index, "frame_index": frame_index,
        "timestamp": round(timestamp_s, 4), "device_timestamp_s": p.get("device_timestamp_s"),
        "session_id": session_id, "trial_id": trial_id, "participant_id": participant_id,
        "device_id": device_id,
        "observation": {
            "state": {k: p.get(k) for k in ("capacitance", "force", "force_rate",
                      "raw_sensor_value", "filtered_sensor_value", "temperature_c", "contact_duration_s", "valid")},
            "derived": {"classified_event": p["classified_event"],
                        "event_confidence": p.get("event_confidence"),
                        "interaction_intensity": p.get("interaction_intensity")}},
        "task": "compare fixed and context-sensitive touch/thermal responses",
        "context": {"identity_class": "not_tested", "identity_confidence": None,
                    "interaction_context": None,
                    "physiology": {k: None for k in ("heart_rate_bpm", "resting_heart_rate_bpm",
                        "heart_rate_delta_bpm", "recent_activity", "measurement_age_s", "source_class")}},
        "policy": {"requested_response": p["requested_response"], "requested_parameters": None},
        "action": None,
        "execution": {"executed_response": executed, "physically_executed": p["physically_executed"],
                      "heater_output": p["heater_output"], "executed_parameters": None,
                      "latency_s": None, "duration_s": None},
        "safety": {"approved_response": p["approved_response"], "safety_clamp": p["safety_clamp"],
                   "reason": p["safety_reason"], "safe_state_entered": p["safe_state_entered"]},
        "experiment": {"condition": condition, "mode": p["mode"], "phase": phase,
                       "operator_note": operator_note}})


def serial_payloads(port, baud):
    try:
        import serial
    except ImportError as exc:
        raise SystemExit("pyserial is required: pip install pyserial") from exc
    with serial.Serial(port, baudrate=baud, timeout=2) as ser:
        for raw in ser:
            try:
                payload = json.loads(raw.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                print("Skipping malformed serial line")
                continue
            if isinstance(payload, dict) and payload.get("record_type") == "frame":
                yield payload
            elif isinstance(payload, dict) and "status" not in payload:
                raise ValueError("unversioned telemetry; upgrade firmware before recording trials")


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--simulate", action="store_true")
    mode.add_argument("--serial", metavar="PORT")
    parser.add_argument("--baud", type=int, default=115200)
    parser.add_argument("--output", default="v0_session.jsonl")
    parser.add_argument("--frames", type=int, default=80, help="maximum accepted frames")
    parser.add_argument("--condition", choices=CONDITIONS, required=True)
    parser.add_argument("--session-id")
    parser.add_argument("--trial-id")
    parser.add_argument("--participant-id", help="optional pseudonym, never a name")
    parser.add_argument("--device-id")
    parser.add_argument("--phase", choices=("calibration", "formal"), default="calibration")
    parser.add_argument("--operator-note")
    parser.add_argument("--scenario", choices=("normal", "overtemperature", "sensor_fault", "timeout"), default="normal")
    args = parser.parse_args()
    if args.frames < 1:
        parser.error("--frames must be positive")
    if args.serial and args.scenario != "normal":
        parser.error("--scenario applies only to simulation")
    session_id = args.session_id or f"session-{uuid.uuid4().hex[:12]}"
    trial_id = args.trial_id or f"trial-{uuid.uuid4().hex[:12]}"
    device_id = args.device_id or ("v0-rig-sim" if args.simulate else "v0-rig-01")
    source = (simulated_device_payloads(args.frames, args.condition, args.scenario)
              if args.simulate else serial_payloads(args.serial, args.baud))
    start = time.monotonic()
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    # Preserve original trials: existing paths are never overwritten.
    with out_path.open("x", encoding="utf-8") as output:
        for payload in source:
            frame = make_canonical_frame(
                episode_index=0, frame_index=count,
                timestamp_s=payload["device_timestamp_s"] if args.simulate else time.monotonic() - start,
                device_payload=payload, session_id=session_id, trial_id=trial_id, device_id=device_id,
                condition=args.condition, participant_id=args.participant_id,
                phase=args.phase, operator_note=args.operator_note)
            output.write(json.dumps(frame, separators=(",", ":"), allow_nan=False) + "\n")
            output.flush()
            count += 1
            if count >= args.frames:
                break
    print(f"Wrote {count} frames to {out_path} (trial {trial_id}, {args.condition})")


if __name__ == "__main__":
    main()
