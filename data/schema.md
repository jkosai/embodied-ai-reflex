# Public Data Schema

Version: **0.4**. Canonical, project-owned JSONL; one record per sampled frame.
See `examples/` for complete generated records. Missing/unavailable measurements are JSON `null`,
never invented zeros. Non-finite sensor values are serialized as null and invalidated by the controller.

## Pipeline contract

```text
sensor input -> classified event -> requested response -> safety evaluation -> executed response -> log
```

The policy request is immutable evidence of intent. Safety records a separate approved response and
clamp/rejection reason. Execution records only what the output adapter reports actually executing.
Approval is not execution. The current non-actuating builds always report null execution, false
physical execution, and zero commanded heater output, including when a warming request is approved.

## Fields and units

| Path | Meaning |
|---|---|
| `schema_version`, `record_type` | `"0.4"`, `"frame"` |
| `session_id`, `trial_id` | Session grouping and unique trial identifier; configurable, otherwise generated |
| `episode_index`, `frame_index` | Zero-based indices; one invocation is one trial/episode |
| `timestamp` | Seconds since host episode start; virtual episode seconds in host simulation |
| `device_timestamp_s` | Device uptime seconds, or virtual simulation time; not a UTC timestamp |
| `participant_id` | Optional pseudonym; null by default |
| `device_id` | Rig label, not a personal device identifier |
| `observation.state.raw_sensor_value` | Unfiltered normalized force fixture, 0–1; not Newtons/ADC counts |
| `observation.state.filtered_sensor_value` | Explicit passthrough of the same fixture until filtering is calibrated |
| `observation.state.force` | Retained normalized force channel |
| `observation.state.force_rate` | Force difference per sample, not force per second |
| `observation.state.capacitance` | Normalized simulated capacitive channel, not farads |
| `observation.state.temperature_c` | Surface-temperature channel in degrees Celsius; simulated currently |
| `observation.state.contact_duration_s` | Current uninterrupted contact duration in seconds; zero after release |
| `observation.state.valid` | Controller-reported sensor validity |
| `observation.derived.classified_event` | Event vocabulary below |
| `observation.derived.event_confidence` | Null until confidence is meaningfully calibrated |
| `observation.derived.interaction_intensity` | Valid normalized filtered force, 0–1; null for invalid input |
| `policy.requested_response` | Semantic request before safety evaluation |
| `safety.approved_response` | Safety-approved/substituted request; never used to infer execution |
| `safety.safety_clamp` | Boolean; true on rejection or safe fallback, including a latched fault |
| `safety.reason` | Stable reason string or null when no intervention |
| `safety.safe_state_entered` | Output adapter reports its safe/off state; a simulation claim only in simulated mode |
| `execution.executed_response` | Explicit output-adapter report, or null when no physical execution occurred |
| `execution.physically_executed` | Boolean; false in simulation |
| `execution.heater_output` | Commanded heater duty, 0–1; zero in this stub, not measured thermal power |
| `execution.latency_s`, `execution.duration_s` | Null until measured |
| `experiment.condition` | `fixed` or `context_sensitive`; must match device telemetry |
| `experiment.mode` | Data origin: currently `simulated-prehardware`, even over serial |
| `experiment.phase` | `calibration` (default) or `formal`; does not certify hardware readiness |
| `experiment.operator_note` | Optional sanitized note |

`task`, `context`, `action`, requested/executed parameter slots retain the v0.3 structure.
Identity is `not_tested`; physiology/context measurements and numeric action remain null.
Recognition is not authorization. Raw conversation is never logged here.

## Event and response vocabulary

Events: `NONE`, `CONTACT_START`, `TAP`, `PRESS`, `SUSTAINED_HOLD`, `RELEASE`,
`EXCESSIVE_INPUT`, `INVALID_INPUT`. `STROKE` is reserved and can be tested at the request layer;
the current force-only classifier never claims to detect it.
`TAP` is emitted on a brief contact ending; longer contact endings emit `RELEASE`.
The classifier emits a state/event on every sample, so PRESS/HOLD/NONE can repeat.

Responses: `NO_RESPONSE`, `WARM_SLOW`, `WARM_MODERATE`, `MAINTAIN`, `RETURN_TO_BASELINE`.
These are symbolic requests; no numeric thermal trajectories have been validated or implemented.
`MAINTAIN` counts as heating for safety budgeting. Return-to-baseline means stop heating and passive cooling,
not an active cooling command. Faults substitute `NO_RESPONSE` and latch until controller reinitialization.

Reasons include `invalid_sensor_data`, `simulated_temperature_limit`, `simulated_heating_timeout`,
`excessive_input`, `manual_stop_or_unknown`, `communication_lost_or_unknown`, and `invalid_request`.
The host reference additionally detects `invalid_clock` on non-finite/backward virtual time.

## Migration from v0.3

- Preserve old logs as v0.3; do not relabel them as v0.4 or infer missing measurements.
- `observation.derived.event_label` becomes `classified_event`; `confidence` becomes `event_confidence`.
- `safety.intervention` becomes `safety_clamp`; `approved_response` is now preserved in canonical safety data.
- Condition is an experimental variable; the old `"simulation"` condition becomes a separate mode field.
- Remove hardcoded participant/trial metadata. Add raw/filtered input, intensity, validity, heater output,
  physical-execution flag, phase, and device time.
- Firmware wire records now carry `record_type`, condition, explicit execution, and renamed fields.
  Upgrade both sides together. The logger rejects incomplete/unversioned data and condition mismatches.
- Lowercase `light_contact`, `sustained_contact`, `rapid_or_high_force`, `release`, `none` and
  `warm_low`, `warm_medium`, `motor_away` belong to the old vocabulary. Retain their original meanings in old data;
  no automatic conversion can reconstruct the new classifier's missing timing information.

## Export and privacy

Episode/frame indices, timestamps, state observations, task, and the future action slot remain available
for a later LeRobot-style exporter. Keep project-specific audit fields as auxiliary data and preserve source logs.

Public examples must be synthetic or explicitly sanitized. Keep names, personal identifiers, credentials,
biometrics, raw conversation, wearable exports, private relationship content, unpublished calibration/control
parameters, and private project material out of GitHub. Real trials default to ignored `data/raw/` paths
in the documented commands; publishing a real dataset requires separate sanitization.
