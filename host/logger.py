#!/usr/bin/env python3
"""
V0 host-side logger.

Modes:
  python logger.py --simulate
  python logger.py --serial COM3
"""

from __future__ import annotations

import argparse
import json
import random
import time
from pathlib import Path
from typing import Any, Dict, Iterator, Optional

SCHEMA_VERSION = "0.3"


def make_canonical_frame(
    *,
    episode_index: int,
    frame_index: int,
    timestamp_s: float,
    device_payload: Dict[str, Any],
    session_id: str,
    trial_id: str,
    device_id: str,
) -> Dict[str, Any]:
    requested = device_payload.get("requested_response")
    approved = device_payload.get("approved_response")
    physically_executed = bool(device_payload.get("physically_executed", False))

    return {
        "schema_version": SCHEMA_VERSION,
        "record_type": "frame",
        "episode_index": episode_index,
        "frame_index": frame_index,
        "timestamp": round(timestamp_s, 4),
        "session_id": session_id,
        "trial_id": trial_id,
        "participant_id": "p001",
        "device_id": device_id,
        "observation": {
            "state": {
                "capacitance": device_payload.get("capacitance"),
                "force": device_payload.get("force"),
                "force_rate": device_payload.get("force_rate"),
                "temperature_c": device_payload.get("temperature_c"),
                "contact_duration_s": device_payload.get("contact_duration_s"),
            },
            "derived": {
                "contact_state": (
                    "contact"
                    if (device_payload.get("force") or 0) > 0.05
                    else "none"
                ),
                "event_label": device_payload.get("event"),
                "confidence": None,
            },
        },
        "task": "characterize human contact response",
        "context": {
            "identity_class": "not_tested",
            "identity_confidence": None,
            "interaction_context": None,
            "physiology": {
                "heart_rate_bpm": None,
                "resting_heart_rate_bpm": None,
                "heart_rate_delta_bpm": None,
                "recent_activity": None,
                "measurement_age_s": None,
                "source_class": None,
            },
        },
        "policy": {
            "requested_response": requested,
            "requested_parameters": None,
        },
        "action": None,
        "execution": {
            "executed_response": approved if physically_executed else None,
            "executed_parameters": None,
            "latency_s": None,
            "duration_s": None,
        },
        "safety": {
            "intervention": bool(device_payload.get("safety_intervention", False)),
            "reason": device_payload.get("safety_reason"),
            "safe_state_entered": bool(
                device_payload.get("safety_intervention", False)
                and approved == "none"
            ),
        },
        "experiment": {
            "condition": "simulation",
            "operator_note": None,
        },
    }


def simulated_device_payloads(count: int = 80) -> Iterator[Dict[str, Any]]:
    previous_force = 0.0
    contact_start: Optional[float] = None
    start = time.monotonic()

    for i in range(count):
        t = time.monotonic() - start
        phase = (i // 20) % 4

        if phase == 0:
            force = 0.0
        elif phase == 1:
            force = 0.24 + random.uniform(-0.02, 0.02)
        elif phase == 2:
            force = 0.56 + random.uniform(-0.03, 0.03)
        else:
            force = 0.0

        touching = force > 0.05
        if touching and contact_start is None:
            contact_start = t
        if not touching:
            contact_start = None

        duration = (t - contact_start) if contact_start is not None else 0.0
        force_rate = force - previous_force

        if not touching and previous_force > 0.05:
            event = "release"
        elif not touching:
            event = "none"
        elif force > 0.80 or force_rate > 0.45:
            event = "rapid_or_high_force"
        elif duration >= 1.0:
            event = "sustained_contact"
        else:
            event = "light_contact"

        requested = "warm_low" if event == "sustained_contact" else "none"

        yield {
            "capacitance": round(
                (0.72 if touching else 0.10) + random.uniform(-0.01, 0.01), 3
            ),
            "force": round(force, 3),
            "force_rate": round(force_rate, 3),
            "temperature_c": round(22.0 + 0.02 * i, 2),
            "contact_duration_s": round(duration, 3),
            "event": event,
            "requested_response": requested,
            "approved_response": requested,
            "safety_intervention": False,
            "safety_reason": None,
            "physically_executed": False,
        }

        previous_force = force
        time.sleep(0.01)


def serial_payloads(port: str, baud: int) -> Iterator[Dict[str, Any]]:
    try:
        import serial
    except ImportError as exc:
        raise SystemExit(
            "pyserial is required for --serial mode. Install with: pip install pyserial"
        ) from exc

    with serial.Serial(port, baudrate=baud, timeout=2) as ser:
        for raw in ser:
            line = raw.decode("utf-8", errors="replace").strip()
            if not line or not line.startswith("{"):
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                print(f"Skipping malformed serial line: {line!r}")


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--simulate", action="store_true")
    mode.add_argument("--serial", metavar="PORT")
    parser.add_argument("--baud", type=int, default=115200)
    parser.add_argument("--output", default="v0_session.jsonl")
    parser.add_argument("--frames", type=int, default=80)
    args = parser.parse_args()

    out_path = Path(args.output)
    start = time.monotonic()

    source = (
        simulated_device_payloads(args.frames)
        if args.simulate
        else serial_payloads(args.serial, args.baud)
    )

    frame_count = 0
    with out_path.open("w", encoding="utf-8") as f:
        for frame_index, payload in enumerate(source):
            canonical = make_canonical_frame(
                episode_index=0,
                frame_index=frame_index,
                timestamp_s=time.monotonic() - start,
                device_payload=payload,
                session_id="session-001",
                trial_id="trial-001",
                device_id="v0-rig-sim" if args.simulate else "v0-rig-01",
            )
            f.write(json.dumps(canonical, separators=(",", ":")) + "\n")
            frame_count += 1

            if frame_index % 10 == 0:
                print(
                    f"frame={frame_index:03d} "
                    f"event={canonical['observation']['derived']['event_label']} "
                    f"requested={canonical['policy']['requested_response']}"
                )

            if args.simulate and frame_count >= args.frames:
                break

    print(f"Wrote {frame_count} frames to {out_path}")


if __name__ == "__main__":
    main()
