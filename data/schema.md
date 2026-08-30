# Public Data Schema

Version: **0.2**

This schema defines the minimum structured record for public V0 experiment data.

Version 0.2 changes the collection model from a custom event log toward an **episode/frame structure that can be exported into LeRobotDataset v3 or another robot-learning dataset later**. It does not require LeRobot at collection time.

## Design goals

- Preserve original experiment data even if the learning stack changes.
- Keep observations and actions separate.
- Preserve episode boundaries and per-frame timestamps.
- Preserve the distinction between **requested behavior** and **executed behavior**.
- Keep safety/audit information even when a downstream ML format does not have a native field for it.
- Allow natural-language task annotations without storing private conversation.
- Use pseudonymous participant identifiers only.
- Missing data should be `null`, not `0`.

## Compatibility model

LeRobotDataset v3 represents low-dimensional states, actions, and timestamps as tabular time-series data, with schema and episode metadata stored separately.

For future compatibility, the canonical V0 record keeps these concepts:

| V0 concept | Future LeRobot-style mapping |
|---|---|
| `episode_index` | episode grouping / metadata |
| `frame_index` | frame order inside an episode |
| `timestamp` | frame time in seconds |
| `observation.state` | numeric sensor/state vector |
| `action` | numeric action representation once defined |
| `task` | natural-language task annotation |
| audit/safety fields | retained as project-specific auxiliary features or sidecar analysis data |

The exact numeric `action` representation is **not frozen yet**. V0 continues to log semantic requested/executed responses separately until the hardware-policy boundary is tested.

## Canonical JSONL frame

```json
{
  "schema_version": "0.2",
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
    "interaction_context": null
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

## Required structural fields

| Field | Type | Description |
|---|---|---|
| `schema_version` | string | Public schema version. |
| `record_type` | string | `frame`, `episode_summary`, or `annotation`. |
| `episode_index` | integer | Zero-based episode identifier within the dataset/export batch. |
| `frame_index` | integer | Zero-based frame identifier within the episode. |
| `timestamp` | number | Seconds from the start of the episode. |
| `session_id` | string | Pseudonymous experiment session identifier. |
| `trial_id` | string | Identifier for one trial. |
| `participant_id` | string/null | Pseudonymous participant identifier. |
| `device_id` | string | Stable prototype configuration identifier. |
| `task` | string/null | Sanitized natural-language task annotation. No raw conversation. |

## Observation fields

`observation.state` is the canonical home for numeric embodiment observations.

Current V0 candidates:

- capacitance
- force
- force rate
- measured temperature
- contact duration

Field names and units must be documented before a released dataset is treated as stable.

Derived event labels remain separate from raw/numeric state so that later classifiers can be retrained without losing the original measurements.

## Action fields

`action` is reserved for the eventual **numeric action representation exposed to a learning policy**.

Do not populate it merely to imitate a robot-learning dataset.

Until the control boundary is validated, continue logging:

- `policy.requested_response`
- `policy.requested_parameters`
- `execution.executed_response`
- `execution.executed_parameters`

This preserves the distinction between what a higher layer asked for and what the safety-constrained body actually did.

When a stable numeric action space exists, document an explicit conversion between the semantic/audit representation and `action`.

## Language/task annotations

Natural-language annotations should describe the experiment or task, not private conversation.

Appropriate examples:

```text
characterize sustained human contact
respond safely to contact while maintaining thermal limits
compare fixed and context-sensitive physical responses
```

Avoid:

- raw chat transcripts
- intimate conversation excerpts
- names
- inferred emotional claims presented as facts

If later tooling supports richer persistent/event language annotations, those should remain sanitized semantic labels.

## Public vs. private fields

### Appropriate for public data

- episode/frame/timestamp structure
- pseudonymous trial/session IDs
- sensor measurements needed to evaluate the experiment
- coarse event labels
- sanitized task labels
- requested vs. executed response
- response timing
- safety interventions
- experimental condition labels

### Keep private by default

- real names
- account identifiers
- phone/watch hardware identifiers
- raw voice, face, or biometric templates
- raw conversation text
- private relationship content
- authentication tokens
- API keys
- unpublished calibration thresholds
- unpublished control gains or tuning values
- exact mappings intentionally withheld for IP review

## CSV export

A flattened analysis CSV may include:

```text
schema_version
episode_index
frame_index
timestamp
session_id
trial_id
participant_id
device_id
task
capacitance
force
force_rate
temperature_c
contact_duration_s
contact_state
event_label
event_confidence
identity_class
identity_confidence
interaction_context
requested_response
executed_response
latency_s
duration_s
safety_intervention
safety_reason
safe_state_entered
condition
operator_note
```

CSV is an analysis/export convenience. The canonical collection model should preserve episode/frame structure.

## Versioning

If fields are added or their meaning changes, increment `schema_version`.

Do not silently reuse a field for a different meaning.

A future LeRobot exporter should be implemented as a conversion layer rather than replacing or mutating the original V0 records.
