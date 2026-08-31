# Public Data Schema

Version: **0.3**

This is the canonical public record format for V0.

It is project-owned. A later exporter may convert it to LeRobotDataset v3 or another robotics dataset format.

## Frame record

```json
{
  "schema_version": "0.3",
  "record_type": "frame",
  "episode_index": 0,
  "frame_index": 0,
  "timestamp": 0.0,
  "session_id": "session-001",
  "trial_id": "trial-001",
  "participant_id": "p001",
  "device_id": "v0-rig-01",
  "observation": {
    "state": {
      "capacitance": null,
      "force": null,
      "force_rate": null,
      "temperature_c": null,
      "contact_duration_s": null
    },
    "derived": {
      "contact_state": null,
      "event_label": null,
      "confidence": null
    }
  },
  "task": "characterize human contact response",
  "context": {
    "identity_class": "not_tested",
    "identity_confidence": null,
    "interaction_context": null,
    "physiology": {
      "heart_rate_bpm": null,
      "resting_heart_rate_bpm": null,
      "heart_rate_delta_bpm": null,
      "recent_activity": null,
      "measurement_age_s": null,
      "source_class": null
    }
  },
  "policy": {
    "requested_response": null,
    "requested_parameters": null
  },
  "action": null,
  "execution": {
    "executed_response": null,
    "executed_parameters": null,
    "latency_s": null,
    "duration_s": null
  },
  "safety": {
    "intervention": false,
    "reason": null,
    "safe_state_entered": false
  },
  "experiment": {
    "condition": null,
    "operator_note": null
  }
}
```

## Notes

- `timestamp` is seconds from episode start.
- Missing data is `null`, not zero.
- `observation.state` holds numeric embodiment measurements.
- Derived labels remain separate from raw measurements.
- `action` is intentionally unresolved until the policy/actuator boundary is tested.
- `requested_response` and `executed_response` remain separate.
- Physiological fields are measurements, not emotional or medical labels.
- Identity confidence is not authorization.
- Raw conversation is not stored here.

## LeRobot compatibility

| V0 | Future export |
|---|---|
| `episode_index` | episode grouping |
| `frame_index` | frame order |
| `timestamp` | frame time |
| `observation.state` | observation vector |
| `action` | policy action once defined |
| `task` | task / language annotation |

Project-specific safety and audit fields may remain auxiliary data during export.

## Keep private by default

Do not publish:

- names or direct identifiers
- phone/watch hardware identifiers
- raw voice, face, or biometric templates
- raw conversation
- private relationship content
- credentials or API keys
- unnecessary physiological history
- raw wearable exports
- unpublished calibration thresholds
- unpublished control gains
- intentionally withheld implementation details
