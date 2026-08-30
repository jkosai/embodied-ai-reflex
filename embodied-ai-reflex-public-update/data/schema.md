# Public Data Schema

Version: **0.1**

This schema defines the minimum structured record for public V0 experiment data.

The goal is to make experiments inspectable without publishing raw conversation content, personal identifiers, secrets, or implementation details that are not required to evaluate the experiment.

## Design principles

- One record represents one sampled observation or one event, depending on `record_type`.
- Use UTC timestamps in ISO 8601 format.
- Keep sensor names stable across runs.
- Preserve the distinction between **requested** behavior and **executed** behavior.
- Record any safety clamp, substitution, timeout, or rejection explicitly.
- Use pseudonymous participant identifiers only.
- Do not store raw conversation text in this dataset.
- Do not encode inferred emotional state as fact.
- Missing data should be `null`, not `0`.

## Recommended JSONL record

```json
{
  "schema_version": "0.1",
  "record_type": "event",
  "timestamp_utc": "2026-08-30T16:00:00.000Z",
  "session_id": "session-001",
  "trial_id": "trial-001",
  "participant_id": "p001",
  "device_id": "v0-rig-01",

  "sensor": {
    "capacitance_raw": null,
    "force_raw": null,
    "force_normalized": null,
    "temperature_c": null,
    "contact_duration_ms": null
  },

  "derived": {
    "contact_state": null,
    "event_label": null,
    "confidence": null
  },

  "context": {
    "identity_class": "primary_user",
    "identity_confidence": null,
    "interaction_context": null
  },

  "behavior": {
    "requested_response": null,
    "executed_response": null,
    "response_started_ms": null,
    "response_duration_ms": null
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

## Field definitions

| Field | Type | Description |
|---|---|---|
| `schema_version` | string | Public schema version used for the record. |
| `record_type` | string | `sample`, `event`, `response`, or `summary`. |
| `timestamp_utc` | string | ISO 8601 UTC timestamp. |
| `session_id` | string | Pseudonymous experiment session identifier. |
| `trial_id` | string | Identifier for one trial within a session. |
| `participant_id` | string/null | Pseudonymous participant identifier. No names or contact information. |
| `device_id` | string | Stable identifier for the prototype configuration. |
| `sensor.capacitance_raw` | number/null | Raw or minimally processed capacitive observation, if published. |
| `sensor.force_raw` | number/null | Raw force/pressure sensor observation, if published. |
| `sensor.force_normalized` | number/null | Normalized force value, preferably documented as unitless. |
| `sensor.temperature_c` | number/null | Measured surface or relevant sensor temperature in °C. |
| `sensor.contact_duration_ms` | number/null | Contact duration at the time of the record. |
| `derived.contact_state` | string/null | Coarse physical state such as `none`, `contact`, or `sustained_contact`. |
| `derived.event_label` | string/null | Semantic event label used by the experiment. |
| `derived.confidence` | number/null | Optional classifier confidence on a documented 0–1 scale. |
| `context.identity_class` | string/null | Coarse class only, e.g. `primary_user`, `known_other`, `unknown`, `not_tested`. |
| `context.identity_confidence` | number/null | Confidence for identity class if applicable. |
| `context.interaction_context` | string/null | Sanitized experimental context label. Never raw conversation. |
| `behavior.requested_response` | string/null | High-level response requested by the higher layer. |
| `behavior.executed_response` | string/null | High-level response actually executed after local validation. |
| `behavior.response_started_ms` | number/null | Latency from event detection to executed response. |
| `behavior.response_duration_ms` | number/null | Duration of executed response. |
| `safety.intervention` | boolean | Whether local safety logic altered or rejected the requested response. |
| `safety.reason` | string/null | Coarse reason such as `temperature_limit`, `timeout`, `invalid_request`, or `sensor_fault`. |
| `safety.safe_state_entered` | boolean | Whether the controller entered its safe state. |
| `experiment.condition` | string/null | Experimental condition label, such as `fixed` or `context_sensitive`. |
| `experiment.operator_note` | string/null | Short sanitized note. Avoid personal or conversational content. |

## Public vs. private fields

### Appropriate for public data

- timestamps
- pseudonymous trial/session IDs
- sensor measurements needed to evaluate the experiment
- coarse event labels
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

A flattened CSV may use columns such as:

```text
schema_version
record_type
timestamp_utc
session_id
trial_id
participant_id
device_id
capacitance_raw
force_raw
force_normalized
temperature_c
contact_duration_ms
contact_state
event_label
event_confidence
identity_class
identity_confidence
interaction_context
requested_response
executed_response
response_started_ms
response_duration_ms
safety_intervention
safety_reason
safe_state_entered
condition
operator_note
```

## Versioning

If fields are added or their meaning changes, increment `schema_version`.

Do not silently reuse a field for a different meaning.
