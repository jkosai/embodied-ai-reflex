"""Regenerate only the named, synthetic public examples (never real trial logs)."""
import json
from pathlib import Path

from logger import make_canonical_frame
from pipeline import simulated_device_payloads


def main():
    destination = Path(__file__).resolve().parents[1] / "data" / "examples"
    fixtures = (("v0_simulated_session.jsonl", "context_sensitive", "normal"),
                ("v0_simulated_fixed.jsonl", "fixed", "normal"),
                ("v0_simulated_safety_rejection.jsonl", "context_sensitive", "overtemperature"))
    for filename, condition, scenario in fixtures:
        with (destination / filename).open("w", encoding="utf-8", newline="\n") as output:
            for index, payload in enumerate(simulated_device_payloads(80, condition, scenario)):
                record = make_canonical_frame(
                    episode_index=0, frame_index=index, timestamp_s=payload["device_timestamp_s"],
                    device_payload=payload, session_id="synthetic-session-001",
                    trial_id=f"synthetic-{condition}-{scenario}", device_id="v0-rig-sim",
                    condition=condition, operator_note=f"Synthetic {scenario} fixture; no physical execution.")
                output.write(json.dumps(record, separators=(",", ":"), allow_nan=False) + "\n")
        print(f"Generated {filename}")


if __name__ == "__main__":
    main()
